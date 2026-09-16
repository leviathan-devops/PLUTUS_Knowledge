---
type: plutus-gate
name: "golden-gate-harness"
command: "cd PLUTUS/agent && bun diag-lmv-golden-fx.ts"
pass: "ENTRIES 15/15 ≤3p + TPs 2/2 ≤5p + VERDICT PASS — measured 2026-09-16 at HEAD 8f4ac74"
cadence: "every-change"
---

# Gate — golden-gate-harness

```
cd PLUTUS/agent && bun diag-lmv-golden-fx.ts
```

**Pass:** ENTRIES 15/15 ≤3p + TPs 2/2 ≤5p + VERDICT PASS — measured 2026-09-16 at HEAD 8f4ac74

The canon harness that wraps the production entry. EU#1 Mon S 1.14395 Δ0.0p · EU#2 Mon L 1.14110 Δ0.0p · GU#1 Mon L 1.33330 Δ0.5p on the current fixture.
