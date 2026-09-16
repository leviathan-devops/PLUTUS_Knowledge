/**
 * kgm/fleet.ts — the knowledge-graph-manager for the Plutus knowledge graph.
 * Built FROM manager-machine v1.0 (battery 37/0 green at copy time).
 *
 * Fleet:
 *   daemon:plutus-au-engine — the au daemon serving PLUTUS_Knowledge.
 *     observe = au daemon status (shallow) + a wire round-trip (deep);
 *     heal = detached `au daemon start` + status read-back (the CLI-lies law).
 *   lint:plutus-knowledge — the graph must carry ZERO diagnostics.
 *     observe = diagnostic_counts over the wire; NO heal — doctrine lint is
 *     surfaced (raised), never auto-fixed.
 *
 * Modes:
 *   bun kgm/fleet.ts                 → resume sweep (NULL-terminal rows) + one tick
 *   bun kgm/fleet.ts tick            → one tick only
 *   bun kgm/fleet.ts start-work <id> → crash-first work row, then EXIT WITHOUT
 *                                      terminal (the interrupt-resume proof seed)
 *
 * Kill path: this file runs on demand (no resident loop). The daemon itself:
 *   /home/leviathan/arsumbris/au-engine/target/release/au daemon stop <REPO>
 */
import { ManagerStore, Journal, tick, WorkLedger } from "./manager-machine/src/index.js";
import type { Desired } from "./manager-machine/src/index.js";
import { createConnection, type Socket } from "node:net";
import { realpathSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { Database } from "bun:sqlite";
const AU = "/home/leviathan/arsumbris/au-engine/target/release/au";
const REPO = "/home/leviathan/JARVIS_WORKSPACE/Shared_Workspace/PLUTUS/MASTER_CONTEXT";
const DB = process.env.MM_DB ?? join(homedir(), ".manager-machine/plutus-knowledge/store.sqlite");
const IDENTITY = "plutus-knowledge";
const JOURNAL = join(import.meta.dir, "journal", "journal.log");

// ── the daemon wire (WIRE.md schema 29): 4-byte BE length + JSON ────────────
function socketPath(): string {
  let h = 0xCBF29CE484222325n;
  for (const b of Buffer.from(realpathSync(REPO))) {
    h ^= BigInt(b);
    h = (h * 0x100000001B3n) & 0xFFFFFFFFFFFFFFFFn;
  }
  return join(homedir(), `.arsumbris/au-engine/run/${h.toString(16).padStart(16, "0")}.sock`);
}
function wireRead(req: Record<string, unknown>): Promise<unknown> {
  const { promise, resolve, reject } = Promise.withResolvers<unknown>();
  const s: Socket = createConnection({ path: socketPath() });
  const body = Buffer.from(JSON.stringify(req));
  const fail = (e: unknown) => { try { s.destroy(); } catch { /* already gone */ } reject(e); };
  s.on("error", fail);
  s.on("connect", () => s.write(Buffer.concat([Buffer.from([0, 0, body.length >> 8, body.length & 255]), body])));
  const chunks: Buffer[] = [];
  let header: Buffer | null = null;
  s.on("data", (d: Buffer) => {
    chunks.push(d);
    const buf = Buffer.concat(chunks);
    if (!header && buf.length >= 4) { header = buf.subarray(0, 4); }
    if (header && buf.length - 4 >= header.readUInt32BE(0)) {
      const ln = header.readUInt32BE(0);
      try { resolve(JSON.parse(buf.subarray(4, 4 + ln).toString("utf8"))); } catch (e) { fail(e); }
      s.destroy();
    }
  });
  setTimeout(() => fail(new Error("wire timeout 5s")), 5000).unref?.();
  return promise;
}
// ── Desired 1: the au daemon ────────────────────────────────────────────────
/** Wire-read result guard: pulls diagnostic_counts.total from an unknown frame. */
function diagTotal(frame: unknown): number | undefined {
  if (frame && typeof frame === "object" && "result" in frame) {
    const result = (frame as Record<string, unknown>).result;
    if (result && typeof result === "object" && "diagnostic_counts" in result) {
      const counts = (result as Record<string, unknown>).diagnostic_counts;
      if (counts && typeof counts === "object" && "total" in counts) {
        const total = (counts as Record<string, unknown>).total;
        return typeof total === "number" ? total : undefined;
      }
    }
  }
  return undefined;
}

function auStatus(): { ok: boolean; out: string } {
  const p = Bun.spawnSync([AU, "daemon", "status", REPO], { stdout: "pipe", stderr: "pipe" });
  const out = (p.stdout.toString() + p.stderr.toString()).trim();
  return { ok: p.exitCode === 0 && out.includes("ready=true"), out };
}

const auDaemon: Desired = {
  id: "daemon:plutus-au-engine",
  kind: "daemon",
  shallow: async () => {
    const st = auStatus();
    return { ok: st.ok, body: st.out.slice(0, 200) };
  },
  deep: async () => {
    try {
      const n = diagTotal(await wireRead({ read: "diagnostic_counts" }));
      return { ok: n !== undefined, body: `wire round-trip ok, diagnostics=${n}` };
    } catch (e) {
      return { ok: false, body: `wire round-trip FAILED: ${(e as Error).message}` };
    }
  },
  observe: async () => {
    const st = auStatus();
    if (!st.ok) return "daemon-down";
    try { await wireRead({ read: "diagnostic_counts" }); return null; }
    catch { return "socket-dead-while-status-ok"; }
  },
  heal: async (drift: string) => {
    const child = Bun.spawn([AU, "daemon", "start", REPO], {
      stdin: "ignore", stdout: "ignore", stderr: "ignore",
    });
    child.unref();
    for (let i = 0; i < 30; i++) {
      await new Promise((r) => setTimeout(r, 500)); // retry poll (loop body, not a named wrapper)
      const st = auStatus(); // READ-BACK: never trust the spawn alone
      if (st.ok) return `healed '${drift}': daemon restarted, read-back ready=true (pid ${child.pid})`;
    }
    throw new Error(`heal failed: daemon still down after 15s (spawn pid ${child.pid})`);
  },
};

// ── Desired 2: graph lint — zero diagnostics, no auto-heal (raise) ─────────
const graphLint: Desired = {
  id: "lint:plutus-knowledge",
  kind: "trigger",
  shallow: async () => {
    try {
      const n = diagTotal(await wireRead({ read: "diagnostic_counts" })) ?? -1;
      return { ok: n === 0, body: `diagnostics=${n}` };
    } catch (e) { return { ok: false, body: `wire FAILED: ${(e as Error).message}` }; }
  },
  observe: async () => {
    try {
      const n = diagTotal(await wireRead({ read: "diagnostic_counts" })) ?? -1;
      return n === 0 ? null : `diagnostics=${n}`;
    } catch { return "wire-unreachable"; }
  },
  // no heal: doctrine lint surfaces for the operator, never auto-edited
};

// ── boot ────────────────────────────────────────────────────────────────────
const store = new ManagerStore({ path: DB });
const journal = new Journal(JOURNAL);
const ledger = new WorkLedger(store, journal);
const mode = process.argv[2] ?? "tick-and-resume";

if (mode === "start-work") {
  const id = process.argv[3] ?? "anonymous-work";
  ledger.start(id, "kgm-work", { repo: REPO, note: "crash-first row; process exits without terminal" });
  console.log(`crash-first row written: ${id} (state=running, finished_at=NULL) — exiting WITHOUT finish (the interrupt marker)`);
  process.exit(0); // deliberate: leaves the NULL-terminal row for the resume sweep
}

if (mode === "tick" || mode === "tick-and-resume") {
  if (mode === "tick-and-resume") {
    // read-only second connection: ManagerStore.run is write-only (its API)
    const ro = new Database(DB, { readonly: true });
    const rows = ro.query("SELECT id FROM mm_work WHERE finished_at IS NULL").all() as unknown[];
    ro.close();
    for (const row of rows) {
      const id = (row as Record<string, unknown>).id;
      if (typeof id !== "string") continue;
      const plan = ledger.resumePlan(id);
      console.log(`resume sweep: ${id} → ${plan ? `checkpoint=${plan.checkpoint ?? "start"}` : "no plan (gone)"}`);
    }
  }
  const verdict = await tick({
    instanceId: IDENTITY,
    journal,
    lockPath: `${DB}.lock`,
    probes: [auDaemon, graphLint],
  });
  console.log("tick verdict:", JSON.stringify(verdict));
}
