---
type: plutus-ruling
id: "R38"
quote: "the test machinery wraps the PRODUCTION entry; it never re-implements the production flow"
source: "PLUTUS_MASTER_CONTEXT_INJECTOR.md:370"
status: "operator-confirmed"
---

# R38 — canon-is-truth-never-reimplement

**Quote (verbatim, PLUTUS_MASTER_CONTEXT_INJECTOR.md:370):**

> the test machinery wraps the PRODUCTION entry; it never re-implements the production flow

Ratified 2026-09-16 after the W9 regression: same HEAD + same fixture, canon diag-lmv-golden-fx.ts = ENTRIES 15/15 ≤3p + TPs 2/2 PASS, while the W9-built re-port (src/mdve/reasoning-chain.ts +2286L et al.) scored 1/5. The W9 'rulings 1+2' were defects of that re-port, not doctrine questions. GATE-CLASS gate 2 must measure the canon.
