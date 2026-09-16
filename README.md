---
type: au.engine.readme::au-engine
tldr: The operator-authored typed knowledge graph for the Plutus trading system — rulings quoted verbatim with file:line sources (D13); agents bind via the au daemon socket or au-mcp.
---

# Repo Overview

Plutus doctrine as a live typed graph: 38 rulings (R1-R34 canon + R35-R38 from
the 2026-09-16 operator session), 16 hard limits, gates, state fingerprints,
terms, and the P2-01 lesson. Every `plutus-ruling` card carries the operator's
words VERBATIM in `quote` plus a `file:line` `source` — the type system rejects
a card whose source does not match `something.md:123` form (D13 enforced
mechanically). Seeded 2026-09-16 from PLUTUS_MASTER_CONTEXT_INJECTOR.md §1 +
Checkpoints/v4.5.3_CLEAN_BASELINE/MANIFEST.md + OPERATOR-SESSION-2026-09-16.md.

## What this is

The single durable home of Plutus law. The engine (au) indexes this repo into
a typed, queryable graph: types in `type/*.type.yaml`, cards as ordinary
markdown with frontmatter in `rulings/`, `hard-limits/`, `lessons/`, `gates/`,
`state/`, `terms/`. Bad data surfaces as diagnostics and never blocks a save.
The graph is the antidote to doctrine-drift bugs like the 2026-09-16 W9
regression (a superseded 3.0 RRR floor lived in code beside its 2.5
replacement — see [[R37-rrr-2p5-reconfirmed]]).

## How to use this

- Query: the daemon serves framed JSON at ~/.arsumbris/au-engine/run/<hash>.sock
  (`{"read":"diagnostics"}`, `types`, `instances_of`, `overview`; wire = au-engine
  WIRE.md, schema 29). Start it: `au daemon start <this repo>` (foreground).
- Agents: bind via the socket or au-mcp (adapters for Claude Code/Codex today;
  any MCP harness via the daemon contract).
- Trust: cards are law; diagnostics are lint. A claim without a card is an
  opinion. Check state/ cards for the current verified fingerprint before
  trusting any gate claim.

## How to extend this

- Add a card: create `rulings/R39-<slug>.md` with frontmatter
  `type: plutus-ruling / id / quote / source / status`. The quote is the
  operator's words verbatim; the source is file:line. Save — the graph updates
  live; diagnostics flag what does not conform.
- New kind of law: add `type/<name>.type.yaml`, then author cards against it.
- Re-seed mechanically: `python3 tools/seed_v1.py` (overwrites generated
  files only — hand-authored cards are never touched).
- Never edit the engine's view; edit the files. Git is the history.
