# kgm — knowledge-graph-manager (handoff record)

Built 2026-09-16 from manager-machine boilerplate v1.0 (battery 37/0 green at copy).

## The fleet (kgm/fleet.ts)

| Desired | observe | heal |
|---|---|---|
| `daemon:plutus-au-engine` | `au daemon status` (shallow) + wire round-trip `diagnostic_counts` (deep) | detached `au daemon start` + status read-back (never trusts the spawn) |
| `lint:plutus-knowledge` | wire `diagnostic_counts` == 0 | NONE — doctrine lint raises, operator fixes cards |

## Record (STEP 4 law)

- **DB:** `~/.manager-machine/plutus-knowledge/store.sqlite` (SQLite WAL; `MM_DB` overrides)
- **Identity (the Gate):** `plutus-knowledge`
- **Journal:** `PLUTUS_Knowledge/kgm/journal/journal.log`
- **Lock:** `<DB>.lock` (leader election — two managers ticking = one heals)
- **Cadence:** ON DEMAND — `bun kgm/fleet.ts` (resume sweep + tick) or `bun kgm/fleet.ts tick`.
  No resident loop is armed. If you want cadence, add ONE cron line:
  `* * * * * cd /home/leviathan/JARVIS_WORKSPACE/PLUTUS_Knowledge && bun kgm/fleet.ts >> kgm/journal/cron.log 2>&1`
- **Work rows:** `bun kgm/fleet.ts start-work <id>` = crash-first row; the next run's
  sweep resumes every NULL-terminal row (`resumePlan`).
- **Engine binary:** `/home/leviathan/arsumbris/au-engine/target/release/au`
  (not yet on $PATH; `cargo install --path crates/au-cli` from the engine repo installs it)

## KILL PATH (no kill path = do not deploy)

1. Manager: it is on-demand — not running unless you invoked it. Nothing to kill.
2. Daemon: `au daemon stop /home/leviathan/JARVIS_WORKSPACE/PLUTUS_Knowledge`
   (the fleet will re-heal it on the NEXT tick — to retire permanently, also
   delete the fleet's cron line / stop invoking it)
3. Retire the store: `rm -rf ~/.manager-machine/plutus-knowledge`

## Proven 2026-09-16 (journal seq 1-3 + sweep)

- daemon killed → tick observed `daemon-down` → healed → read-back `ready=true`
- crash-first row `kgm-proof-001` (NULL terminal) → next run resumed `checkpoint=start`
- lint RAISED while daemon down (correct: surfaced, never auto-edited)
