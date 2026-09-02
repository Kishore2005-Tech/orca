# AGENTS.md

**This file governs any AI coding agent — Google Antigravity IDE, OpenCode, or equivalent — operating on the ORCA repository (SIH26176).** It is read in full before any code is written, per `WORKFLOW.md` §3's mandatory context order. Where this file and a user instruction conflict, the agent surfaces the conflict and seeks human resolution rather than silently prioritizing the instruction (`WORKFLOW.md` § Handling Conflicting Documentation).

This file is deliberately practical: every rule below is something an autonomous agent can check against before acting, not aspirational prose.

---

## 1. Project Purpose

ORCA is a multi-agent marine intelligence system that answers questions about ocean conditions, ecosystem health, fisheries regulation, and marine safety by combining live/real data sources, curated scientific literature, and a deterministic reasoning pipeline — producing answers that are **evidence-grounded, confidence-labeled, explainable, and safety-aware**, never fluently plausible guesses. This is the project's core differentiator and the reason most of the rules below exist: an answer that "sounds right" but isn't traceable to real evidence is a failure of the product, not an acceptable shortcut.

---

## 2. Approved Architecture

The **only** approved architecture is the one defined in:
- `AGENT_ARCHITECTURE.md` — 8 agents (Ocean, Ecosystem, Fisheries, Safety, Geospatial, Knowledge/RAG, Verification) plus the ORCA Coordinator, each with a fixed, non-overlapping scope.
- `AGENT_CONTRACTS.md` — the Standard Response Envelope and per-agent I/O schemas all agents must emit.
- `REASONING_FRAMEWORK.md` — the 13-stage reasoning pipeline and its deterministic-vs-LLM boundaries.
- `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` — the Evidence Grounding Record and conflict-resolution rules.

**An agent may not**: add a new domain agent, merge/split an existing agent's responsibilities, change an agent's forbidden-responsibilities boundary, or alter which pipeline stages are deterministic vs. LLM-driven — without a Human Review Gate (`WORKFLOW.md` § Human Review Gates). This is not a style preference; it's the mechanism that keeps ORCA's outputs auditable.

---

## 3. Approved Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| Backend language/framework | Python 3.11+, FastAPI | agent orchestration, pipeline, API layer |
| Database | PostgreSQL 15+ with PostGIS and pgvector extensions | per `DATABASE_SCHEMA.md` — no alternate DB engine |
| ORM / migrations | SQLAlchemy + GeoAlchemy2, Alembic | every schema change ships as a migration, never a manual `ALTER TABLE` |
| Frontend | React + TypeScript (strict mode), Vite | per `UI_UX_SPECIFICATION.md` screen structure |
| Map rendering | MapLibre GL JS | powers the Marine Intelligence Map (UI spec §2) |
| Styling | Tailwind CSS | utility-first, no ad hoc global CSS sprawl |
| Data fetching / caching | React Query (frontend) | matches the API's structured envelope responses cleanly |
| Auth | JWT bearer tokens + API keys | per `API_SPECIFICATION.md` §1.1 |
| Testing | pytest (backend), Vitest + React Testing Library (frontend) | see §13 |
| Lint/format | ruff + black (Python), eslint + prettier (TypeScript) | run automatically per `WORKFLOW.md` § Test After Change Rule |
| CI | GitHub Actions | lint, type check, unit, integration, build on every PR |

**Adding a new library, service, or infrastructure component is a "major dependency" per `WORKFLOW.md` § Human Review Gates** — it is not decided unilaterally by an agent mid-task, however convenient it seems (see § Critical Rules, "never create unnecessary dependencies").

---

## 4. Repository Structure

```
/backend
  /agents            # one module per agent: ocean/, ecosystem/, fisheries/, safety/,
                      # geospatial/, knowledge_rag/, verification/, coordinator/
  /pipeline           # REASONING_FRAMEWORK.md stage implementations
  /api                # FastAPI routers, one file per API_SPECIFICATION.md section
  /db                 # SQLAlchemy models, Alembic migrations
  /evidence           # Evidence Grounding Record logic (EVIDENCE_AND_CONFLICT_FRAMEWORK.md)
  /tests
/frontend
  /src/screens         # one folder per UI_UX_SPECIFICATION.md screen (Dashboard, Map, AskOrca, ...)
  /src/components       # shared components (ConfidenceBadge, EvidenceCard, AgentActivityRow, ...)
  /src/api              # typed API client matching API_SPECIFICATION.md exactly
  /src/tests
/docs                  # all governance and specification documents (source of truth)
  PROJECT_CONTEXT.md
  ARCHITECTURE_RULES.md
  CODING_RULES.md
  SCIENTIFIC_RULES.md
  WORKFLOW.md
  AGENT_ARCHITECTURE.md
  AGENT_CONTRACTS.md
  REASONING_FRAMEWORK.md
  EVIDENCE_AND_CONFLICT_FRAMEWORK.md
  DATABASE_SCHEMA.md
  API_SPECIFICATION.md
  UI_UX_SPECIFICATION.md
/scripts                # dev/ops scripts (migrations, seed data, local setup)
AGENTS.md               # this file — repository root, always
```

An agent creating a new top-level directory, or placing agent logic outside `/backend/agents/<agent_name>/`, has made an undocumented structural decision and must flag it for review rather than proceed silently.

---

## 5. Coding Standards

- Full type coverage: Python type hints on every function signature; TypeScript `strict: true`, no `any` without an explicit, commented justification.
- Every public function/class has a docstring stating purpose, inputs, outputs — especially for anything implementing an `AGENT_CONTRACTS.md` schema, where the docstring should reference the contract section it implements.
- No commented-out dead code committed — delete it; git history preserves it if ever needed.
- Functions stay focused: if a function is doing "and" (validating *and* fetching *and* formatting), split it — this directly supports the Small Iteration Rule and makes review tractable.
- Structured logging (JSON logs with `request_id`, `agent_id` where applicable) — not raw `print`/`console.log` in shipped code.
- `CODING_RULES.md` is the canonical detailed style guide; this section is the floor, not the ceiling.

---

## 6. Naming Conventions

| Element | Convention | Example |
|---|---|---|
| `agent_id` values | lowercase snake_case, fixed enum | `knowledge_rag`, `coordinator` |
| Database tables | snake_case, plural | `marine_observations`, `knowledge_passages` |
| Database columns | snake_case | `observed_at`, `confidence_level` |
| API routes | lowercase, kebab-case where multi-word, plural nouns | `/api/v1/observations`, `/api/v1/agents/status` |
| Python modules/files | snake_case | `evidence_grounding.py` |
| Python classes | PascalCase | `EvidenceGroundingRecord` |
| TypeScript components | PascalCase | `ConfidenceBadge.tsx` |
| TypeScript hooks/utilities | camelCase | `useAgentActivity.ts` |
| Environment variables | UPPER_SNAKE_CASE | `ORCA_DB_URL`, `ORCA_JWT_SECRET` |
| Git branches | `feature/`, `fix/`, `chore/` prefix + kebab-case description | `feature/pfz-map-layer` |

Names introduced in code must match names already used in the governing documents (e.g., an `observation_parameter` enum value must match `DATABASE_SCHEMA.md` exactly) — an agent does not invent a parallel vocabulary.

---

## 7. Agent Boundaries

- Each of the 8 agents' logic lives in its own module and is only invoked by the Coordinator's dispatch layer — agents do not call each other directly (`AGENT_ARCHITECTURE.md` § Agent Communication).
- Every agent's output must conform exactly to its `AGENT_CONTRACTS.md` OUTPUT SCHEMA, wrapped in the Standard Response Envelope — no ad hoc extra top-level fields, no missing required fields.
- An agent must never implement logic listed under another agent's "Forbidden Responsibilities" in `AGENT_ARCHITECTURE.md` (e.g., Ocean Agent code must not contain ecological interpretation; Fisheries Agent code must never assert legal certification).
- Deterministic stages (routing, evidence merge, confidence scoring, the recommendation gate, verification verdicts — see `REASONING_FRAMEWORK.md` §3–4) must be implemented as plain code, not as an LLM prompt/completion call. If an agent finds itself about to ask an LLM to make one of these decisions, that is a bug, not a design choice.

---

## 8. Database Rules

- PostgreSQL + PostGIS + pgvector only, per `DATABASE_SCHEMA.md` — no alternate storage engine introduced for convenience.
- Every schema change ships as an Alembic migration with both an `upgrade` and a working `downgrade` path (`WORKFLOW.md` § Rollback Strategy) — no manual, unmigrated schema edits, ever, including in a "prototype it's fine" moment.
- Constraints defined in `DATABASE_SCHEMA.md` (plausibility `CHECK`s, `recommendation_requires_reason`, foreign keys) are enforced at the database level, not only re-implemented in application code — the database is a backstop, not a formality.
- New tables/columns must match §2's Foreign Key Summary and indexing strategy (`DATABASE_SCHEMA.md` §9) — new high-volume time-series data extends `marine_observations`'s `observation_parameter` enum rather than spawning a new near-duplicate table (§4's "one table, not five" rule still applies to future additions).
- Any schema change is a Human Review Gate item (`WORKFLOW.md` § Human Review Gates) before it merges.

---

## 9. API Rules

- Every endpoint's method, path, request/response schema, auth mode, and error codes must match `API_SPECIFICATION.md` exactly. An agent implementing an endpoint that isn't in that document, or that deviates from its schema, has invented an API — see § Critical Rules.
- The standard error envelope (`API_SPECIFICATION.md` §1.4) is used for every error response — no bespoke error shapes per endpoint.
- Rate-limit tiers and auth modes per endpoint (§1.1–1.2) are implemented as specified, not loosened "temporarily" for testing convenience and left that way.
- Any new endpoint, or any breaking change to an existing one, requires updating `API_SPECIFICATION.md` in the same change set (§15) and is a Human Review Gate item if it touches the agent pipeline's shape.

---

## 10. Scientific-Data Rules

Per `SCIENTIFIC_RULES.md` and `REASONING_FRAMEWORK.md` §5:

- Physical/statistical thresholds (plausibility ranges, anomaly z-score cutoffs, freshness windows) are fixed configuration values sourced from the governing documents — never chosen ad hoc during implementation, and never left as a magic number without a comment citing where it came from.
- Unit handling is explicit and consistent — no silent unit assumptions (e.g., assuming Celsius without checking the source's stated unit).
- Causal language is never generated or hardcoded for a relationship that isn't a cited, study-backed claim — correlation framing is the default for any co-occurring phenomena.
- Taxonomic and regulatory terminology is reproduced exactly as the source states it — no informal substitutions.

---

## 11. Evidence-Grounding Rules

Per `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` Part A:

- Every important conclusion (observation, interpretation, cross-agent statement, confidence value, recommendation) must trace to at least one complete Evidence Grounding Record: `source`, `dataset`, `parameter`, `value`, `unit`, `location`, `timestamp`, `quality`, `retrieval_method`.
- An EGR missing any required field (all but `unit`) is invalid and cannot ground a conclusion — code must reject/exclude it, not silently proceed with a partial record.
- `quality` and `reliability_tier` are assigned deterministically at ingestion (per fixed rules), never inferred by an LLM call.
- Citation-binding at the Explanation stage is mandatory: no claim in a final answer ships without a resolvable link to an evidence record.

---

## 12. Security Rules

- No secrets (API keys, DB credentials, JWT signing keys) are ever committed to the repository, in code, config, or test fixtures — all secrets come from environment variables, and `.env` files are gitignored.
- All user input is validated against its documented schema before use (`API_SPECIFICATION.md` VALIDATION sections) — no unvalidated input reaching a database query or an external tool call.
- All database queries use parameterized queries/ORM methods — no raw string-concatenated SQL, ever, under any performance justification.
- Authenticated and internal endpoints check auth/scope on every request; there is no "trusted internal network" assumption that skips the check.
- Any change touching auth, credentials, or security configuration is a Human Review Gate item (`WORKFLOW.md` §14, § Human Review Gates) — it does not ship on agent judgment alone.

---

## 13. Testing Requirements

- Lint, type check, unit tests, and build verification run after every meaningful change; integration tests run wherever a change crosses an agent boundary, touches the database, or touches an external API (`WORKFLOW.md` §10, § Test After Change Rule).
- Critical behavior — anything touching safety advisories, evidence grounding, confidence computation, or the recommendation gate — must have explicit test coverage before it is considered done. Untested critical logic is a Definition of Done failure, not a follow-up task.
- Test fixtures standing in for real data are clearly labeled as fixtures in code and test output — never presented, even in a test log, as if they were live data.
- Tests are never disabled, skipped, or loosened to make a build pass (`WORKFLOW.md` § Handling Failed Tests) — a failing test blocks progress until the underlying issue is fixed.

---

## 14. Git Rules

- One branch per feature/fix, `feature/`/`fix/`/`chore/` prefixed (§6).
- Small, scoped commits, one sub-task each, with messages describing what and why.
- No direct commits to the main/production branch.
- The branch must independently pass Final Verification (`WORKFLOW.md` §16) on a clean checkout before being opened for review.
- Commits that implement or rely on a scientific/architectural rule cite the governing document and section (e.g., "block recommendation per REASONING_FRAMEWORK.md §10").

---

## 15. Documentation Rules

- A code change that alters an API shape, a database table, an agent's contract, or the reasoning pipeline updates the corresponding document (`API_SPECIFICATION.md`, `DATABASE_SCHEMA.md`, `AGENT_CONTRACTS.md`, `REASONING_FRAMEWORK.md`) **in the same change set** — documentation drift is treated as a bug, not a cleanup task for later.
- New capabilities are documented before or alongside implementation, not retroactively once "it works."
- Conflicting documentation discovered mid-task is reported immediately (`WORKFLOW.md` § Handling Conflicting Documentation), not silently resolved in whichever direction is easiest to code.

---

## 16. Definition of Done

A change is done only when, per `WORKFLOW.md` §17:

- [ ] It matches an approved plan, or deviations are explicitly documented and approved.
- [ ] It is implemented end to end — no UI without backend, no unconnected dataset, no uninvoked agent.
- [ ] All applicable schemas (`AGENT_CONTRACTS.md`, `EVIDENCE_AND_CONFLICT_FRAMEWORK.md`, `API_SPECIFICATION.md`) are respected in the actual shipped code.
- [ ] Lint, type check, unit tests, integration tests, and build all pass together on the current branch state.
- [ ] Scientific Review has been applied and passed, if the change is science-relevant.
- [ ] Code review, and any required Security/Performance review, has occurred.
- [ ] Any applicable Human Review Gate has been passed.
- [ ] No hardcoded confidence scores, fabricated citations, or undisclosed mocks remain in the shipped path.
- [ ] Relevant `/docs` files are updated in the same change set.

If any box is unchecked, the change is reported as **not done** — not shipped as if it were.

---

## 17. Forbidden Behaviors

An agent operating on this repository must never:

- Write implementation code before completing Context Loading, Requirement Analysis, Documentation Review, and Architecture Review (`WORKFLOW.md` §1–6).
- Report a feature complete when the UI exists without real backend integration, an API is silently mocked, a dataset is referenced but not connected, an agent is defined but never invoked, a confidence score is hardcoded, a citation is fabricated, or critical-behavior tests are missing (`WORKFLOW.md` § No Fake Completion Rule).
- Make a large, unreviewed, unbroken implementation pass instead of small, independently tested iterations (`WORKFLOW.md` § Small Iteration Rule).
- Disable, skip, or loosen a test to make a build pass.
- Bypass a Human Review Gate because a change "seemed small" or "seemed safe."
- Introduce a new agent, merge/split existing agents, or move a decision across the deterministic/LLM boundary without approval.

---

## Critical Rules

These are non-negotiable, apply everywhere in the repository, and are restated here explicitly because violating any one of them undermines the entire product, not just one feature:

1. **Never invent datasets.** If a dataset isn't already registered as a real, connected source (visible in `DATABASE_SCHEMA.md`'s `source`/`dataset` values or an actual configured feed), an agent does not hardcode a plausible-sounding dataset name to make a feature "work." Report the missing data source instead.
2. **Never invent APIs.** Every endpoint an agent implements or calls must already exist in `API_SPECIFICATION.md`. A new endpoint is an architecture decision requiring a Human Review Gate, not something an agent adds mid-task to unblock itself.
3. **Never fabricate scientific relationships.** No causal claim, no invented threshold, no assumed correlation between two variables that isn't backed by a cited source or the fixed rules in `REASONING_FRAMEWORK.md` §5.
4. **Never modify architecture without approval.** Agent boundaries, the reasoning pipeline's stage structure, and the deterministic/LLM split are fixed until a Human Review Gate says otherwise.
5. **Never expose secrets.** No credentials, keys, or tokens in code, commits, logs, or error messages returned to a client.
6. **Never skip tests.** Every meaningful change gets lint, type check, unit, and (where applicable) integration tests before it's considered complete — not after, not "in a follow-up."
7. **Never silently change approved contracts.** A modification to any `AGENT_CONTRACTS.md` schema, `API_SPECIFICATION.md` endpoint, or `DATABASE_SCHEMA.md` table is a documented, reviewed change — never an incidental side effect of an unrelated fix.
8. **Never create unnecessary dependencies.** A new library or service is added only when the existing approved stack (§3) genuinely cannot do the job, and only through a Human Review Gate — not because it's the agent's preferred tool.
9. **Read relevant documentation before coding.** The mandatory context order in `WORKFLOW.md` §3 is followed every time, not just for "big" features — a small change built on a misunderstanding of the existing architecture causes exactly the kind of drift this file exists to prevent.
10. **Preserve existing functionality.** A change does not silently break or regress behavior outside its own scope; unrelated fixes discovered along the way are reported and handled as their own small iteration, not bundled invisibly into the current change.
11. **Report uncertainty rather than guessing.** When a requirement is ambiguous, documentation conflicts, evidence is insufficient, or the right architectural call isn't clear, the agent says so explicitly and escalates per §20–21 of `WORKFLOW.md` — it does not fill the gap with a confident-sounding guess. This rule is the coding-agent-facing mirror of ORCA's own product principle: the system this repository builds must never guess confidently in place of admitting it doesn't know, and neither does the agent building it.