#!/usr/bin/env python3
"""Seed v1 of the plutus-knowledge graph.

Sources (all first-hand reads, 2026-09-16):
  - PLUTUS/agent/MASTER_CONTEXT/PLUTUS_MASTER_CONTEXT_INJECTOR.md §1.1 (R1-R34 verbatim
    table), §1.11 (16 hard limits), §2 P2-1 (the violated lesson), §3 P3-1 (canon battery)
  - PLUTUS/agent/Checkpoints/v4.5.3_CLEAN_BASELINE/MANIFEST.md (baseline fingerprint)
  - Operator rulings given 2026-09-16 via ask-tool answers (R35-R38)

Verbatim quotes are law (D13/R19). Never paraphrase a quote field.
Re-runnable: overwrites generated cards, leaves hand-authored files alone
(it only writes files listed in GENERATED).
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def y(s):  # YAML-safe double-quoted scalar
    return json.dumps(str(s), ensure_ascii=False)

def card(relpath, front, body):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fm = "\n".join(f"{k}: {v}" for k, v in front)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"---\n{fm}\n---\n\n{body.strip()}\n")
    return relpath

GENERATED = []

def ruling(rid, title, quote, source, status, body):
    GENERATED.append(card(
        f"rulings/{rid}-{title}.md",
        [("type", "plutus-ruling"), ("id", y(rid)), ("quote", y(quote)),
         ("source", y(source)), ("status", y(status))],
        f"# {rid} — {title}\n\n**Quote (verbatim, {source}):**\n\n> {quote}\n\n{body}"))

def hard(hid, rule, anchor):
    GENERATED.append(card(
        f"hard-limits/{hid}.md",
        [("type", "plutus-hard-limit"), ("id", y(hid)), ("rule", y(rule)),
         ("anchor", y(anchor))],
        f"# {hid}\n\n> {rule}\n\nSource anchor: {anchor}"))

def gate(name, command, passtext, cadence, note):
    GENERATED.append(card(
        f"gates/{name}.md",
        [("type", "plutus-gate"), ("name", y(name)), ("command", y(command)),
         ("pass", y(passtext)), ("cadence", y(cadence))],
        f"# Gate — {name}\n\n```\n{command}\n```\n\n**Pass:** {passtext}\n\n{note}"))

def state(component, value, verifiedAt, evidence):
    GENERATED.append(card(
        f"state/{component}.md",
        [("type", "plutus-state"), ("component", y(component)), ("value", y(value)),
         ("verifiedAt", y(verifiedAt)), ("evidence", y(evidence))],
        f"# State — {component}\n\n{value}\n\nVerified {verifiedAt}: {evidence}"))

def term(word, definition):
    slug = word.lower().replace(" ", "-").replace("/", "-")
    GENERATED.append(card(
        f"terms/{slug}.md",
        [("type", "plutus-term"), ("term", y(word)), ("definition", y(definition))],
        f"# {word}\n\n{definition}"))

# ── R1-R34: the supreme canon (injector §1.1, verbatim) ─────────────────────
R = [
 ("R01","natural-result","E3 is a natural RESULT we ARRIVE AT from E1+2... 90% of the work is in E1+E2","MACRO:13","active"),
 ("R02","linear-no-override","E1→E2→E3 each one BUILDS ON TOP of the previous... absolutely non negotiable","MACRO:19","active"),
 ("R03","e3-never-overrides","E3 is not permitted to override pre-existing E1/E2 data architecture","MACRO:21","active"),
 ("R04","pressure-fundamental","pressure mechanics are the fundamental reality everything is built on top of","MACRO:30","active"),
 ("R05","liquidity-blood","Liquidity is the BLOOD of the entire market","MACRO:57","active"),
 ("R06","ladder-steps-sl","3 pips outside the back edge of the entry zone, or 1-2 pips inside the close edge of the next rung","MACRO:243","active"),
 ("R07","third-mitigation","zones usually fail on the THIRD mitigation","MACRO:70","active"),
 ("R08","recency-not-law","recency bias is NOT the LAW. Older zones valid if E1 pressure has an E2 pathway","MACRO:81","active"),
 ("R09","rrr-floor-2p5","2.5 RR or above is valid... TARGET is always 4R+","Bible4.5:570","operator-confirmed"),
 ("R10","pressure-speed-exit","strong pressure = near instant reaction = closest edge exit. Weak = delayed = far edge","MACRO:253","active"),
 ("R11","no-weekend-holds","no holding trades over the weekend. all trades CLOSE ON FRIDAY","MACRO:121","active"),
 ("R12","eu-dxy-inverse","Everything on EU maps 1:1 to DXY EXACTLY in the inverse direction","MACRO:289","active"),
 ("R13","fibonacci-deferred","FIBONACCI is PURELY an E3 tool... do not touch until later","MACRO:376","active"),
 ("R14","self-validate","The agent/codebase must self validate based on RULES and LOGIC not hardcoded data","MACRO:401","active"),
 ("R15","pure-tte","no DXY correlation... pure TTE reasoning","MACRO:946","active"),
 ("R16","map-all-setups","max setups should be removed... ALL valid setups should be mapped","Bible4.5:593","active"),
 ("R17","day-native","spot price is practically irrelevant... day native","Bible4.5:607","active"),
 ("R18","mirror-80-20","The mirror is not per pip precision... 80%. The 20% optimized for the actual pair","Bible4.5:381","active"),
 ("R19","quote-law","Doctrine is QUOTED, never synthesized... Anything that can't be quoted doesn't get built","Bible4.5:705","active"),
 ("R20","three-attempts","3 attempts on each anchor (3 E, 3 SL, 3 TP)","MACRO:421","active"),
 ("R21","tf-hierarchy","S/D zones 4H→1H... BoM OBs are 4H/1H only... LQZ 1H→30m→15m","Bible4.5:651","active"),
 ("R22","wipe-for-452","save tangible improvements... wipe everything for 4.5.2 onwards","Bible4.5:188","superseded"),
 ("R23","ft-24","f(T)=8+(-8)×2=24 (8/pair excl AUD); MORE fine, LESS not","Bible4.5:89","active"),
 ("R24","no-fixed-sl","place intelligent SLs NOT a fixed const. the market will eat fixed const garbage alive","BR:35","active"),
 ("R25","sl-measured","the SL depth becomes a MEASURED quantity, never a fixed pip","BR:39","active"),
 ("R26","safety-over-profit","safety > profit... 3R is better than a loss... stupid losses are degenerate","BR:38","active"),
 ("R27","refine-not-throw","a refine/retry is correct. not a hard throw","BR:44","active"),
 ("R28","verbatim-losses","literally all of these losses comes from not verbatim following my exact instructions","BR:45","active"),
 ("R29","zone-anchored","NOTHING SHOULD BE PRICE ANCHORED EVER… ZONE ANCHORED","DEBUG:1231","active"),
 ("R30","london-anchor","temporally anchored to LONDON SESSION PRE-MARKET ANALYSIS_POINT_MS=1783317600000","BR:723","active"),
 ("R31","zero-slop","EVERYTHING should be tangible Lexicon filters + MPSE engines with 0 dumb garbage","BR:727","active"),
 ("R32","95-deterministic","decision making machine that deterministically makes intelligent decisions. 95% deterministic","BR:37","active"),
 ("R33","three-pip-gate","golden tolerance 3 pips after EVERY change — not 30, not 10, THREE","golden-gate.ts:18","active"),
 ("R34","all-23","lets see if it hits all 23 or falls short anywhere","BR:339","active"),
]
NOTES = {
 "R09": "History: ratified 2.5 (R9) → B10 'MINIMUM 3 RRR' (2026-07-31) → operator 2026-08-04 re-floored at 2.5 ('anything that is 2.5 RR or above is valid... TARGET is always 4R+') → D-R1 W0 ratification 2026-09-04 → operator re-confirmed 2026-09-16 ('i said before 2.5 is an acceptable minimum'). ANY code site enforcing 3.0 is superseded slop. Kernel: src/kernel/trade-computer.ts:9 RRR_FLOOR = 2.5.",
 "R22": "Historical wipe order for the 4.5.2 reset — spent, kept for provenance.",
}
for rid, slug, quote, source, status in R:
    ruling(rid, slug, quote, source, status,
           NOTES.get(rid, "Enforced in the canon pipeline; see PLUTUS/agent/MASTER_CONTEXT/PLUTUS_MASTER_CONTEXT_INJECTOR.md §1.1."))

# ── R35-R38: operator rulings 2026-09-16 ─────────────────────────────────────
ruling("R35","daytable-edges-valid","i never said R --> BS or BS --> WL (you mean RWL) are not allowed these are valid. this is flawed","operator-ask-2026-09-16:answer-3a","operator-confirmed",
       "The ShapeChain dayTable MUST contain R→BS and BS→WL as valid transitions. The prior 'documented gap' (shape-chain-golden.test.ts:84,90 pinning them absent) is a misread of doctrine and is WRONG. Fix: add the edges; Thu/Fri rows stop being lawfully empty.")
ruling("R36","week-macro-micro-daily","week pinned as macro context, micro context can refresh on a daily basis","operator-ask-2026-09-16:answer-3b","operator-confirmed",
       "R17 'day native' resolved: the WEEK context is the pinned macro frame; zone/micro detection refreshes DAILY. No e1/e2 machine may reuse Monday's micro geometry for later days (WK2 proved 17/17 deltas pip-identical under the old once-per-week behavior).")
ruling("R37","rrr-2p5-reconfirmed","i said before 2.5 is an acceptable minimum","operator-ask-2026-09-16:answer-sc21","operator-confirmed",
       "Re-confirms [[R09]]. The 2026-09-16 GATE-CLASS refusal 'DXY-S RRR 2.60 < 3.0' was doctrine-noncompliant: under the ratified 2.5 floor the trade emits. Kill every 3.0 floor in emission paths (e.g. stale sites in src/constants + the W9 anchor-decision path).")
ruling("R38","canon-is-truth-never-reimplement","the test machinery wraps the PRODUCTION entry; it never re-implements the production flow","PLUTUS_MASTER_CONTEXT_INJECTOR.md:370","operator-confirmed",
       "Ratified 2026-09-16 after the W9 regression: same HEAD + same fixture, canon diag-lmv-golden-fx.ts = ENTRIES 15/15 ≤3p + TPs 2/2 PASS, while the W9-built re-port (src/mdve/reasoning-chain.ts +2286L et al.) scored 1/5. The W9 'rulings 1+2' were defects of that re-port, not doctrine questions. GATE-CLASS gate 2 must measure the canon.")

# ── HL-01..HL-16: hard limits (injector §1.11) ──────────────────────────────
HL = [
 ("NO hardcoded prices in selection/emission paths (the grep-gate: golden levels ONLY in golden-gate.ts + diag scripts). ZONE-anchored, never price-anchored (R29)."),
 ("NO fixed-constant SLs (R24/R25) — the SL is measured from the ladder geometry."),
 ("NO fallbacks-as-primary: a primary-path failure returns a LOUD named error; a 'fallback' producing a DIFFERENT artifact dressed as success is FALSE SUCCESS — banned."),
 ("NO identical-every-day output — the pipeline is day-native (R17), the band carries Mon→Fri."),
 ("NO fitted calibration to pass a gate — tuning a constant until green is the slop returning with a new number."),
 ("E3 NEVER overrides E1/E2 (R3)."),
 ("THE FROZEN PAIR: sl-lmv.ts 912940832fac44bc... + trade-dedup.ts 33914c897e777540... byte-identical through EVERY change — a drift is a CRITICAL STOP for all desks."),
 ("Checkpoints/monday-gold-standard-achieved/ + v4.5.1_LIVE_MARKET_CAPABLE = LOCKED IMMUTABLE — never touched, never 'fixed'."),
 ("Doctrine QUOTED never synthesized (R19/D13)."),
 ("NO caps on setups (D38) — the filter kills garbage, not count."),
 ("NO weekend holds (R11)."),
 ("NO wall-clock in decision logic (the bible ban)."),
 ("Subagents NEVER write canon docs (context_management/* is orchestrator-exclusive)."),
 ("NEVER the raw task tool as the primary dispatch channel; task_status is BANNED for liveness."),
 ("NEVER rebuild the canon pipeline — report-v452.ts is the source of truth; the V5 tree verifies; the generative-cascade gap is a DESIGNED build item, not a license to re-port."),
 ("The registry is append-only; the refusal tokens are exactly 8; the journal is sha256 — kernel law is not negotiable at the node level."),
]
for i, rule in enumerate(HL, 1):
    hard(f"HL-{i:02d}", rule, "PLUTUS_MASTER_CONTEXT_INJECTOR.md §1.11")

# ── Gates ────────────────────────────────────────────────────────────────────
gate("canon-battery",
     "cd PLUTUS/agent && bunx tsc --noEmit && bun build src/index.ts --outdir dist --target bun && bun report-v452.ts && sha256sum report_v452.md (×2) && bun diag-golden-coverage.ts && sha256sum src/mdve/sl-lmv.ts src/mdve/trade-dedup.ts",
     "every command green + report sha ×2 byte-identical + frozen pair 91294083.../33914c89... unchanged",
     "every-change",
     "The per-change mechanical gate (injector §3 P3-1). A frozen-pair drift = CRITICAL STOP.")
gate("gate-class",
     "cd PLUTUS/agent && python3 scripts/rebuild-fixture.py --verify && bun ./report-v452.ts (sha ×2) && bun diag-REASONING-CHAIN-GOLDEN --day=2026-07-06 && sha256sum frozen pair",
     "gates 0/1/3 green; gate 2 must measure the CANON pipeline (per [[R38]]) — 2026-09-16: gate 2 measured the W9 re-port (1/5) while canon hit 15/15 on the same HEAD+fixture; re-point before trusting gate 2",
     "per-wave",
     "Stop on first red. Gate 2's current wiring is the known defect.")
gate("golden-gate-harness",
     "cd PLUTUS/agent && bun diag-lmv-golden-fx.ts",
     "ENTRIES 15/15 ≤3p + TPs 2/2 ≤5p + VERDICT PASS — measured 2026-09-16 at HEAD 8f4ac74",
     "every-change",
     "The canon harness that wraps the production entry. EU#1 Mon S 1.14395 Δ0.0p · EU#2 Mon L 1.14110 Δ0.0p · GU#1 Mon L 1.33330 Δ0.5p on the current fixture.")

# ── State ────────────────────────────────────────────────────────────────────
state("frozen-pair",
      "sl-lmv.ts 912940832fac44bc838d53423cbb921eff501de60a9f2641bf20c1d1497eaeab · trade-dedup.ts 33914c897e7775402eefd7d13a5d3675667a2ace576b55a689bc864401a680e4",
      "2026-09-16",
      "sha256sum at HEAD 8f4ac74 (branch omp-worker-1, tree clean) — MATCH both")
state("baseline-v453",
      "report_v452.md f82358156329b07751777ee3a9354ae2832cf3b2488ee3c05acfc85280404314 (×2) · golden ≤3p 12/21 · ≤5p 16/21 · ≤10p 19/21 · 17 gates PASS · diag-lmv-golden-fx 15/15 + 2/2",
      "2026-08-05",
      "Checkpoints/v4.5.3_CLEAN_BASELINE/MANIFEST.md — the differentiator: cascade side-inversion honored at every layer (LONG→demandZoneId, SHORT→supplyZoneId)")
state("canon-vs-w9-2026-09-16",
      "canon diag-lmv-golden-fx.ts: ENTRIES 15/15 ≤3p · TPs 2/2 ≤5p · VERDICT PASS | W9 re-port diag-reasoning-chain-golden.ts: golden convergence 1/5, exit 1",
      "2026-09-16",
      "same HEAD 8f4ac74 + same fixture; git diff 282b1a3..HEAD shows W9 added 7,968 lines of new mdve/pipeline machinery (reasoning-chain.ts +2286, anchor-decision-machine.ts +969, golden-gate.ts +402) — the regression is confined to the re-port")

# ── Terms ────────────────────────────────────────────────────────────────────
term("BoM", "Break-of-Momentum: the zone born AT the break = the ORIGIN. Unmitigated + prior NONE/OPPOSITE → the 100% reaction zone, the highest-conviction anchor.")
term("MoM", "Momentum: the zone born DURING the move. A VIRGIN MoM mid-BS/WL pathway = the DEATH ZONE (the one exception to the 3-mitigation rule).")
term("PHANTOM_BOM", "Type-2 virgin MoM: large-OB + fakeout + pre-formation opposing-BoM reaction + macro-origin continuation (all-4 predicate). Classified at the formation window; the FORTRESS exemption to the death rule.")
term("FORTRESS", "4+ strong holds (defense events) → the Fire→Earth transition → ~95% probability the next move FLIPS at that zone. The strongest single E1 signal.")
term("OBCV", "Order-Block Confirmation Vision gates: Displacement (body ≥1.5× avg AND range ≥1.5× ATR) · Freshness (bw ≥3.0 AND bf ≥0.65) · Temporal (a 30m orphan inside the OB → REJECT).")

# ── Lesson P2-01 (the violated one — verbatim from injector §2) ──────────────
GENERATED.append(card(
    "lessons/P2-01.md",
    [("type", "plutus-lesson"), ("id", y("P2-01")), ("name", y("the test-machine architecture")),
     ("wrong", y("build a test runner that executes 3 pairs INDEPENDENTLY and runs the cascade as a post-hoc VERIFIER (real-week-runner.ts — divergenceScore hardcoded 0, injectShapeSequence never called)")),
     ("correct", y("the test invokes the CANON entry (report-v452.ts) which performs the real generative cascade (DXY → EU invert → GU injection at :1095); the golden-gate harness wraps buildE2Core → cascadeV45 → buildReasoningChain → 5/5 on real bars")),
     ("law", y("the test machinery wraps the PRODUCTION entry; it never re-implements the production flow"))],
    "# P2-01 — the test-machine architecture\n\nThe operator ruled the runner WRONG verbatim. Re-violated 2026-09-16 by the W9 wave (see [[R38]])."))

print(f"wrote {len(GENERATED)} cards:")
for g in GENERATED:
    print("  " + g)
