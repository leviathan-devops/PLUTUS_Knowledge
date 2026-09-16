---
type: plutus-ruling
id: "R35"
quote: "i never said R --> BS or BS --> WL (you mean RWL) are not allowed these are valid. this is flawed"
source: "OPERATOR-SESSION-2026-09-16.md:1"
status: "operator-confirmed"
---

# R35 — daytable-edges-valid

**Quote (verbatim, operator-ask-2026-09-16:answer-3a):**

> i never said R --> BS or BS --> WL (you mean RWL) are not allowed these are valid. this is flawed

The ShapeChain dayTable MUST contain R→BS and BS→WL as valid transitions. The prior 'documented gap' (shape-chain-golden.test.ts:84,90 pinning them absent) is a misread of doctrine and is WRONG. Fix: add the edges; Thu/Fri rows stop being lawfully empty.
