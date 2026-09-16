---
type: plutus-gate
name: "canon-battery"
command: "cd PLUTUS/agent && bunx tsc --noEmit && bun build src/index.ts --outdir dist --target bun && bun report-v452.ts && sha256sum report_v452.md (×2) && bun diag-golden-coverage.ts && sha256sum src/mdve/sl-lmv.ts src/mdve/trade-dedup.ts"
pass: "every command green + report sha ×2 byte-identical + frozen pair 91294083.../33914c89... unchanged"
cadence: "every-change"
---

# Gate — canon-battery

```
cd PLUTUS/agent && bunx tsc --noEmit && bun build src/index.ts --outdir dist --target bun && bun report-v452.ts && sha256sum report_v452.md (×2) && bun diag-golden-coverage.ts && sha256sum src/mdve/sl-lmv.ts src/mdve/trade-dedup.ts
```

**Pass:** every command green + report sha ×2 byte-identical + frozen pair 91294083.../33914c89... unchanged

The per-change mechanical gate (injector §3 P3-1). A frozen-pair drift = CRITICAL STOP.
