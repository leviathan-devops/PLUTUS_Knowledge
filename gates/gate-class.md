---
type: plutus-gate
name: "gate-class"
command: "cd PLUTUS/agent && python3 scripts/rebuild-fixture.py --verify && bun ./report-v452.ts (sha ×2) && bun diag-REASONING-CHAIN-GOLDEN --day=2026-07-06 && sha256sum frozen pair"
pass: "gates 0/1/3 green; gate 2 must measure the CANON pipeline (per [[R38-canon-is-truth-never-reimplement]]) — 2026-09-16: gate 2 measured the W9 re-port (1/5) while canon hit 15/15 on the same HEAD+fixture; re-point before trusting gate 2"
cadence: "per-wave"
---

# Gate — gate-class

```
cd PLUTUS/agent && python3 scripts/rebuild-fixture.py --verify && bun ./report-v452.ts (sha ×2) && bun diag-REASONING-CHAIN-GOLDEN --day=2026-07-06 && sha256sum frozen pair
```

**Pass:** gates 0/1/3 green; gate 2 must measure the CANON pipeline (per [[R38-canon-is-truth-never-reimplement]]) — 2026-09-16: gate 2 measured the W9 re-port (1/5) while canon hit 15/15 on the same HEAD+fixture; re-point before trusting gate 2

Stop on first red. Gate 2's current wiring is the known defect.
