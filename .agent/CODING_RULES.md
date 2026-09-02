# CODING_RULES.md

# ORCA — Marine Ecosystems Reasoning with Collaborative Agents
## Coding Standards and Implementation Governance

**SIH Problem ID:** SIH26176
**Audience:** AI coding agents (Google Antigravity IDE, OpenCode) and human contributors
**Source of Truth:** `ARCHITECTURE_RULES.md`, `SYSTEM_ARCHITECTURE.md`, `AGENT_ARCHITECTURE.md`, `DATABASE_SCHEMA.md`, `PRD.md`, `PROJECT_MASTER.md`
**Document Status:** Governance — binding on all code written or modified
**Version:** 1.0
**Last Updated:** 30 August 2026

---

## 0. Relationship to ARCHITECTURE_RULES.md

`ARCHITECTURE_RULES.md` governs **what the system is allowed to look like** — service boundaries, agent responsibilities, data flow. This document governs **how code implementing that architecture is written** — style, typing, structure, testing, review. A code change that satisfies this document but violates `ARCHITECTURE_RULES.md` is still wrong; both must hold at once.

Where a technology or convention has not been decided by the team, this document says so explicitly: **`TBD – Requires Team Decision`**. No AI coding agent may resolve a `TBD` by picking a library or pattern on its own and proceeding as if it were settled.

---

## 1. Engineering Principles

1. **Readability over cleverness.** Code is read far more often than written; prefer the obvious implementation over the compact one.
2. **Small, single-responsibility units.** A function, class, or module does one thing (mirrors the agent-boundary discipline in `ARCHITECTURE_RULES.md §16`).
3. **Type safety is not optional.** Every function signature, API contract, and data structure crossing a boundary is typed (Python type hints / TypeScript types) — see §19.
4. **Fail loud, fail structured.** No silent failures on the reasoning path (`ARCHITECTURE_RULES.md ERR-2`).
5. **Testable by construction.** Code is written so it can be tested without standing up the entire system — pure functions where possible, dependency injection where not (§20).
6. **Consistency beats personal preference.** Follow the conventions in this document even when a contributor would personally choose differently.
7. **Smallest working implementation first.** Per the MVP Rule (§28 below and `ARCHITECTURE_RULES.md` MVP Simplification Rules), do not build for scale or flexibility the prototype does not need.

---

## 2. Approved Technology Stack

| Layer | Technology | Status |
|---|---|---|
| Frontend framework | Next.js / React | Approved (`PROJECT_MASTER.md §15.1`) |
| Frontend language | TypeScript | Approved |
| Backend language | Python | Approved (`PROJECT_MASTER.md §15.2, §15.5`) |
| Backend web framework | FastAPI | Approved for this document (resolves the framework TBD in `ARCHITECTURE_RULES.md §4`; consistent with Python-based backend and native async support for the Coordinator's status/progress channel) |
| Data validation (Python) | Pydantic | Approved — required for all API schemas and `AgentResult` typing (§7, §9) |
| Database | PostgreSQL + PostGIS + pgvector | Approved (`DATABASE_SCHEMA.md`) |
| Data processing | Pandas, NumPy, Xarray | Approved (`PROJECT_MASTER.md §15.5`) |
| Mapping / visualization (frontend) | Standard web mapping library (e.g., MapLibre/Leaflet-class tool) | `TBD – Requires Team Decision` (exact library) |
| LLM provider / model | Provider-agnostic (P8) | `TBD – Requires Team Decision` |
| Embedding model | Provider-agnostic (P8) | `TBD – Requires Team Decision` |
| Package manager (Python) | `TBD – Requires Team Decision` (e.g., `pip` + `venv`, `poetry`, `uv`) |
| Package manager (TypeScript) | `TBD – Requires Team Decision` (e.g., `npm`, `pnpm`) |
| Test framework (Python) | `TBD – Requires Team Decision` (e.g., `pytest`) — recommend `pytest`, not yet locked |
| Test framework (TypeScript) | `TBD – Requires Team Decision` (e.g., `Vitest`, `Jest`) |
| Linting / formatting (Python) | `TBD – Requires Team Decision` (e.g., `ruff`, `black`) |
| Linting / formatting (TypeScript) | `TBD – Requires Team Decision` (e.g., `ESLint`, `Prettier`) |
| CI/CD platform | `TBD – Requires Team Decision` (`ARCHITECTURE_RULES.md §23`) |

**Rule STACK-1:** No new layer/technology may be introduced without updating this table first. An AI coding agent proposing, e.g., a different backend framework, a different database, or a new frontend meta-framework must flag this as a stack change requiring sign-off, not implement it directly.

---

## 3. Repository Structure Rules

Following the governance structure proposed in `PROJECT_MASTER.md §27`, adapted to the modular-monolith architecture:

```text
/
├── PROJECT_MASTER.md
├── PRD.md
├── SYSTEM_ARCHITECTURE.md
├── ARCHITECTURE_RULES.md
├── CODING_RULES.md
│
├── frontend/
│   ├── app/                 # Next.js routes
│   ├── components/          # Reusable UI components (§4)
│   ├── lib/                 # API client, types, utilities
│   └── tests/
│
├── backend/
│   ├── api/                 # FastAPI routers only — no business logic (§9)
│   ├── coordinator/         # ORCA Coordinator module
│   ├── agents/
│   │   ├── ocean/
│   │   ├── ecosystem/
│   │   ├── fisheries/
│   │   ├── safety/
│   │   ├── geospatial/
│   │   ├── knowledge_rag/
│   │   └── verification/
│   ├── schemas/             # Pydantic models — shared AgentResult, API request/response schemas
│   ├── services/            # Confidence calculator, evidence store, source adapters
│   ├── db/                  # SQLAlchemy models / migrations
│   ├── config/              # Configuration loading (§15)
│   └── tests/
│
├── data/
│   └── catalog/              # data_sources catalog seed/reference files
│
└── docs/
    ├── architecture/
    └── decisions/            # Architecture Decision Records (§27)
```

**Rule REPO-1:** Each `agents/<name>/` directory contains exactly one agent's implementation and its unit tests, mirroring the one-agent-one-responsibility boundary in `ARCHITECTURE_RULES.md §16`. No agent's logic may be split across directories, and no directory may contain more than one agent's logic.

**Rule REPO-2:** `backend/api/` contains routers only — no Pandas/NumPy calculation, no direct database queries, no agent logic (`ARCHITECTURE_RULES.md BE-2`).

**Rule REPO-3:** `frontend/lib/` is the only place API calls are made from the frontend — components never call `fetch`/HTTP directly (§4).

---

## 4. Frontend Coding Standards

**Rule FE-C1:** Components are organized by responsibility: `components/chat/`, `components/map/`, `components/evidence/` — mirroring the three panels in `SYSTEM_ARCHITECTURE.md §15`. No cross-panel logic embedded in a single component.

**Rule FE-C2:** Components must not contain confidence calculation, evidence validation, or any scientific reasoning (`ARCHITECTURE_RULES.md FE-1`). If a component appears to need this, the calculation belongs in the backend response, not client-side derivation.

**Rule FE-C3:** All backend calls go through a single typed API client module (`frontend/lib/api.ts` or equivalent) — not scattered `fetch` calls inside components (`ARCHITECTURE_RULES.md FE-3`, `REPO-3`).

**Rule FE-C4:** Presentational components (pure rendering) are kept separate from container components (data fetching/state). A component that fetches data does not also contain complex conditional rendering logic beyond loading/error/success states.

**Rule FE-C5:** No API keys, data-source credentials, or LLM provider keys appear in any frontend file, including `.env.local` variables prefixed for client exposure (e.g., `NEXT_PUBLIC_*`) (`ARCHITECTURE_RULES.md FE-4`, SEC-1).

---

## 5. Backend Coding Standards

**Rule BE-C1:** The backend is organized into the module boundaries in §3 — API, Coordinator, Agents, Schemas, Services, DB, Config. A change that blurs these boundaries (e.g., a router function that also runs a confidence calculation) must be refactored before merge.

**Rule BE-C2:** Every module has a single, stated responsibility at the top of its file (a short docstring), referencing which `ARCHITECTURE_RULES.md` section it implements.

**Rule BE-C3:** No backend module imports directly from `frontend/`. No backend module imports the FastAPI `app` object except `api/` routers.

**Rule BE-C4:** Business/scientific logic (unit normalization, spatial filtering, confidence scoring, causal-language checks) lives in `services/` or the relevant `agents/<name>/` module — never inline inside a router handler (`ARCHITECTURE_RULES.md BE-2`).

---

## 6. Agent Coding Standards

Every agent module (`ARCHITECTURE_RULES.md §16`) must implement:

**Rule AGENT-C1: Clear responsibility.** A module-level docstring stating the agent's purpose, referencing `AGENT_ARCHITECTURE.md`.

**Rule AGENT-C2: Typed input.** A Pydantic model for the agent's task input (e.g., `OceanAgentInput`), not a raw `dict`.

**Rule AGENT-C3: Structured output.** Every agent returns the shared `AgentResult` Pydantic model (§7 below) — no agent defines its own ad hoc return shape.

**Rule AGENT-C4: Predictable failure behavior.** Every agent's failure paths (source unreachable, insufficient evidence, location unresolved, etc. — per its entry in `ARCHITECTURE_RULES.md §16`) are implemented as explicit, named result states, not generic exceptions bubbling up uncaught.

**Rule AGENT-C5: Logging.** Every agent invocation logs its start, completion/failure, and key decision points (which sources queried, which check failed) via the shared logging convention (§17) — writing to `agent_runs`/`agent_outputs` as specified in `DATABASE_SCHEMA.md §11–§12`.

**Rule AGENT-C6: Testable functions.** An agent's core logic (e.g., the combination rule in Fisheries Agent, the alignment check in Ecosystem Agent) is implemented as a pure function separable from I/O (database/network calls), so it can be unit tested without mocking the entire retrieval stack.

**Example skeleton (illustrative, not prescriptive of exact library choices):**

```python
class OceanAgentInput(BaseModel):
    location_id: UUID
    time_window: TimeRange
    requested_variables: list[VariableType]

class OceanAgent:
    """Retrieves and normalizes physical oceanographic variables.
    Implements AGENT_ARCHITECTURE.md §1. Forbidden: fishing/safety judgments,
    ecological interpretation (see ARCHITECTURE_RULES.md §16)."""

    def __init__(self, source_adapter: SourceAdapter, geo_service: GeospatialService):
        self._adapter = source_adapter
        self._geo = geo_service

    async def run(self, task: OceanAgentInput) -> AgentResult:
        ...
```

---

## 7. Python Standards

**Rule PY-1: Type hints are mandatory** on every function signature (parameters and return type), every class attribute, and every Pydantic model field. No untyped `def foo(x, y):` in reasoning-path code.

**Rule PY-2: Modular services.** Shared logic (confidence calculation, evidence formatting, spatial filtering) lives in `services/`, imported by agents — not duplicated per-agent.

**Rule PY-3: Pydantic validation everywhere data crosses a boundary** — API request/response bodies, agent inputs/outputs, configuration loading. Raw dicts must not cross a module boundary unvalidated.

**Rule PY-4: Exception handling is explicit and typed.** Catch specific exceptions (e.g., `SourceUnavailableError`), not bare `except:` or overly broad `except Exception:` without re-raising or explicitly converting to a defined failure state (`ARCHITECTURE_RULES.md ERR-2`).

**Rule PY-5: Clean imports.** No wildcard imports (`from x import *`). Imports are ordered: standard library, third-party, local — grouped and separated by a blank line.

**Rule PY-6: Testability.** Functions that perform I/O (database, HTTP) accept their dependencies as parameters or via constructor injection, not by importing a global client — this is what makes Rule AGENT-C6 possible.

```python
# Not acceptable — untyped, implicit dependency, bare except
def get_sst(loc, t):
    try:
        return db.query(...)
    except:
        return None

# Acceptable
async def get_sst(
    location: LocationRef,
    time_window: TimeRange,
    source_adapter: SourceAdapter,
) -> ObservationResult:
    try:
        return await source_adapter.fetch_sst(location, time_window)
    except SourceUnavailableError as exc:
        logger.warning("sst_source_unavailable", location=location.id, error=str(exc))
        return ObservationResult.unavailable(reason=str(exc))
```

---

## 8. TypeScript Standards

**Rule TS-1: Strict typing.** `tsconfig.json` must have `"strict": true`. No project-wide loosening of strictness to make errors disappear.

**Rule TS-2: Interfaces/types for every data shape crossing a boundary** — API responses, component props, state shapes. Prefer `interface` for object shapes that may be extended (API response types); `type` for unions/aliases.

**Rule TS-3: API response types are defined once and reused**, ideally generated or hand-mirrored from the backend Pydantic schemas (§9) so frontend and backend types cannot silently drift — exact generation mechanism (e.g., OpenAPI codegen): `TBD – Requires Team Decision`.

**Rule TS-4: Component boundaries are typed explicitly** — every component's props are a named interface, not inline object typing repeated across files.

**Rule TS-5: Avoiding unnecessary `any`.** `any` is not permitted except at a narrow, explicitly commented boundary (e.g., a third-party library with no types) — and even then, prefer `unknown` with a type guard over `any`.

```typescript
// Not acceptable
function renderEvidence(data: any) { ... }

// Acceptable
interface EvidenceItem {
  sourceName: string;
  datasetName: string;
  retrievedAt: string;
  confidenceLabel: "high" | "medium" | "low";
}

function renderEvidence(data: EvidenceItem[]) { ... }
```

---

## 9. API Standards

**Rule API-C1: Routers only in `api/`.** Each router file corresponds to one resource/concern (e.g., `queries.py`, `status.py`) and delegates immediately to the Coordinator or a service — no business logic inline (`ARCHITECTURE_RULES.md API-1, API-2`).

**Rule API-C2: Every request/response body is a Pydantic schema**, defined in `schemas/`, not a raw dict. Schemas are the single source of truth mirrored into TypeScript types (Rule TS-3).

**Rule API-C3: Dependency injection via FastAPI's `Depends`** for shared resources (database session, Coordinator instance, config) — no module-level global client instantiated inside a route handler.

**Rule API-C4: Validation happens at the schema boundary**, not manually inside the handler body — Pydantic's validation is the gate, not ad hoc `if` checks scattered through the function.

**Rule API-C5: Error responses are structured**, matching `ARCHITECTURE_RULES.md §18`'s failure table — a typed error schema (`{error_code, message, detail}`), never a raw exception traceback returned to the client.

```python
router = APIRouter(prefix="/queries", tags=["queries"])

@router.post("/", response_model=QueryResponse)
async def submit_query(
    body: QueryRequest,
    coordinator: Coordinator = Depends(get_coordinator),
) -> QueryResponse:
    result = await coordinator.handle_query(body)
    return result
```

**Rule API-C6:** Output-contract responses (FR-014) are represented by a single Pydantic schema (`RecommendationResponse`) with all eight sections as named, typed fields — never assembled as a free-form dict in the handler.

---

## 10. Database Standards

**Rule DB-C1:** All schema definitions live in `backend/db/models/`, mirroring `DATABASE_SCHEMA.md` table-for-table. No table is created ad hoc outside a tracked migration.

**Rule DB-C2:** Migrations are the only way schema changes reach the database — no manual `ALTER TABLE` against a running environment. Migration tool: `TBD – Requires Team Decision` (e.g., `Alembic`).

**Rule DB-C3:** ORM models mirror the constraints in `DATABASE_SCHEMA.md §22` exactly — `NOT NULL`, `CHECK`, and `UNIQUE` constraints are declared at the database level, not only enforced in application code (defense in depth, especially for `hazard_alerts.source_id`, per `ARCHITECTURE_RULES.md SEC-5`).

**Rule DB-C4:** No raw SQL string concatenation. Parameterized queries / ORM query builders only, to prevent injection.

**Rule DB-C5:** Every write to a reasoning-path table (`agent_runs`, `agent_outputs`, `evidence`, `conflicts`, `recommendations`) happens through a dedicated repository/service function, not scattered `session.add()` calls across agent code — keeps the write pattern auditable and consistent with `ARCHITECTURE_RULES.md DATABASE ACCESS RULES §2`.

---

## 11. Geospatial Data Coding Rules

**Rule GEO-C1:** All spatial columns use `GEOGRAPHY`, never `GEOMETRY` (`ARCHITECTURE_RULES.md GEO-1`) — enforced in the ORM model definitions.

**Rule GEO-C2:** Spatial filtering always goes through a shared helper function (e.g., `within_tolerance(point, source_id)`) that looks up the per-source tolerance from `data_sources` — no agent hardcodes a radius value inline.

**Rule GEO-C3:** Coordinates are always handled as `(longitude, latitude)` order internally (matching PostGIS/GeoJSON convention), with a single, tested conversion boundary if any external source uses `(lat, lon)` — never mixed silently.

**Rule GEO-C4:** All geospatial calculations (distance, containment) use PostGIS functions via the ORM/SQL layer — no manual haversine/great-circle math duplicated in Python application code.

---

## 12. AI/LLM Coding Rules

**Rule LLM-C1:** Every LLM call is wrapped in a typed function with a defined, bounded role (intent extraction, agent-level explanation, synthesis — per `SYSTEM_ARCHITECTURE.md §13`). No open-ended "ask the LLM anything" call exists in the reasoning path.

**Rule LLM-C2:** LLM calls that are expected to return structured data use a defined output schema (Pydantic model + structured-output prompting or a strict parser), never regex-scraping free text for values.

**Rule LLM-C3: Never treat generated text as authoritative scientific data.** Any numeric value appearing in an LLM's output text is never used as the source of truth for a claim — numeric values only ever originate from the structured data path (`observations`, `pfz_advisories`, `hazard_alerts`). The LLM narrates pre-computed values; it does not supply them (`ARCHITECTURE_RULES.md VERIFICATION RULES §5`).

**Rule LLM-C4: Never allow an LLM to directly modify production database records without explicit validation.** Any code path where an LLM's output results in a database write must pass through the same Pydantic schema validation and Verification Agent gate as any other agent output — no direct `LLM output → INSERT/UPDATE` shortcut.

**Rule LLM-C5:** Every LLM call is logged with its bounded role, and (where feasible) its prompt template version — not the raw prompt text if it contains sensitive data, but enough to reproduce the call for debugging.

**Rule LLM-C6:** Model/provider access is abstracted behind a single client interface (e.g., `LLMClient`), never called directly via a provider SDK scattered across agent files — keeps provider selection swappable per P8.

---

## 13. RAG Implementation Rules

**Rule RAG-C1:** Embedding and retrieval logic lives only in the Knowledge/RAG Agent module (`ARCHITECTURE_RULES.md RAG-4`) — no other agent imports the embedding client directly.

**Rule RAG-C2:** Corpus ingestion (adding a document to `knowledge_documents`/`knowledge_chunks`) is a separate, explicit script/process from the query-time retrieval path — never triggered implicitly by a user query.

**Rule RAG-C3:** Every retrieval call returns passages with their `document_id`, `title`, and `version` attached — a retrieval function that returns bare text strings without this metadata is non-compliant (violates FR-011 traceability).

**Rule RAG-C4:** Retrieved passages passed to the LLM for paraphrasing are capped in length/count (top-k, k documented) — no unbounded context stuffing.

---

## 14. Prompt Management Rules

**Rule PROMPT-1:** Prompts are stored as versioned template files (e.g., `agents/ocean/prompts/explain_claim.md`), not inline string-concatenated in Python code — keeps prompts reviewable and diffable.

**Rule PROMPT-2:** Every prompt template states, in a comment or accompanying metadata, which bounded role it serves (per `SYSTEM_ARCHITECTURE.md §13`'s three-role table) and what output schema it must produce.

**Rule PROMPT-3:** No prompt template instructs the model to state a causal relationship, invent a numeric value, or bypass the qualification/uncertainty requirements — prompts must actively reinforce FR-008/FR-013, not merely rely on downstream filtering to catch violations.

**Rule PROMPT-4:** Prompt changes are reviewed the same as code changes (§27) — a prompt is part of the system's behavior, not a throwaway string.

---

## 15. Environment Variable Rules

**Rule ENV-1: Never hardcode** API keys, passwords, tokens, private URLs, or credentials anywhere in source code, including test fixtures and example config committed to the repository.

**Rule ENV-2:** All secrets are loaded from environment variables or a secrets mechanism at runtime, accessed through a single typed configuration module (`backend/config/`) — no `os.environ.get()` scattered across agent/service files.

**Rule ENV-3:** A `.env.example` file (with placeholder, non-functional values) is committed; the real `.env` is git-ignored.

**Rule ENV-4:** Configuration values are validated at startup (fail fast if a required variable is missing) rather than failing later, mid-request, when the value is first used.

**Rule ENV-5:** Frontend environment variables intended for client exposure are clearly distinguished from server-only variables (per the framework's own convention, e.g., Next.js `NEXT_PUBLIC_` prefix) — and no credential is ever placed in a client-exposed variable (Rule FE-C5).

---

## 16. Error Handling

**Rule ERR-C1:** Every failure mode listed per-agent in `ARCHITECTURE_RULES.md §16` and in the failure table (`ARCHITECTURE_RULES.md §18`) is implemented as a named exception type or a named result-state enum — not inferred from a generic error message string.

**Rule ERR-C2:** No bare `except:`. No `except Exception: pass`. Every caught exception on the reasoning path either converts to a defined failure state visible in the response, or is re-raised after logging.

**Rule ERR-C3:** API-layer errors return structured error responses (Rule API-C5) with an `error_code` the frontend can branch on — not a message string the frontend must pattern-match.

**Rule ERR-C4:** Timeouts are explicit and bounded at every external call (source adapters, LLM calls) — no unbounded `await` on a network call in the reasoning path.

---

## 17. Logging

**Rule LOG-1:** Structured logging only — key-value fields (e.g., `logger.info("agent_completed", agent="ocean", query_id=..., duration_ms=...)`), not free-form string interpolation, so logs are queryable and match `agent_runs`/`agent_outputs` fields.

**Rule LOG-2:** Every agent run logs at minimum: start, completion/failure, sources queried, validation outcome — satisfying `ARCHITECTURE_RULES.md OBS-1`.

**Rule LOG-3:** No secret, credential, or full raw user query containing potentially sensitive content is logged at `INFO` level without consideration — log the query's structured intent, not necessarily verbatim raw text, unless required for debugging and appropriately scoped.

**Rule LOG-4:** Log levels are used consistently: `DEBUG` for development detail, `INFO` for normal orchestration events, `WARNING` for recoverable failures (e.g., source unavailable), `ERROR` for failures requiring attention.

---

## 18. Validation

**Rule VAL-1:** All external input (user query text, API request bodies) is validated against a Pydantic schema before any processing begins (Rule API-C4).

**Rule VAL-2:** All external data (retrieved observations, advisories, alerts) is validated against expected types/ranges/units before being used in agent reasoning (`ARCHITECTURE_RULES.md VERIFICATION RULES §6` — "external data must pass validation before reasoning").

**Rule VAL-3:** Validation failures produce a specific, typed error — not a generic `ValidationError` with no indication of which field or rule failed.

---

## 19. Type Safety

**Rule TYPE-1:** No `Any` (Python) or `any` (TypeScript) at a module boundary — internal, narrowly-scoped exceptions must be commented and justified (mirrors Rule TS-5, applied backend-side too).

**Rule TYPE-2:** Shared data shapes (e.g., `AgentResult`, `EvidenceReference`, `ConfidenceLabel`) are defined once, in `schemas/`, and imported everywhere they're used — never redefined per-agent with slightly different field names.

**Rule TYPE-3:** Enums (Python `Enum` / TypeScript union literal types) are used for fixed value sets (`data_type`, `confidence_label`, `agent_name`) rather than raw strings compared by value scattered through the codebase.

**Rule TYPE-4:** Static type checking is run in CI (or locally before commit) — Python: `mypy` or equivalent (`TBD – Requires Team Decision` on exact tool); TypeScript: `tsc --noEmit`. A change that introduces a type error is not mergeable.

---

## 20. Testing Standards

### Unit Testing
- Every agent's pure-logic functions (combination rules, alignment checks, confidence calculation) have unit tests with both valid and edge-case inputs.
- Every Pydantic schema has at least one test confirming it rejects invalid input.
- Geospatial helper functions (tolerance filtering, containment checks) are unit tested against known coordinate fixtures.

### Integration Testing
- Coordinator → Agent → Verification flow is tested with seeded database fixtures, confirming the correct agents are invoked for a given intent (mirrors `PRD.md FR-004` acceptance criterion).
- API endpoints are tested against their Pydantic response schemas, not just HTTP status codes.
- Database constraint tests confirm that invalid writes (e.g., a `hazard_alerts` row with null `source_id`) are rejected at the database layer, not only caught in application code.

### End-to-End Testing
- At least one scripted end-to-end test per core use case (`PRD.md §6` UC-01–UC-08 as applicable to MVP/Prototype scope) — submit a query, assert the final response matches the output contract and cites expected evidence.
- The demonstration acceptance criterion (`PROJECT_MASTER.md §19.5`) is itself testable: an E2E test can assert that the orchestration log answers all five required questions for a given scripted query.

### Priority Testing Areas (explicit focus, per project risk profile)
1. **Agent outputs** — every agent's `AgentResult` shape and failure-state behavior (Rule AGENT-C3/C4).
2. **Coordinator behavior** — correct routing, correct parallel/sequential dispatch, correct context merging across turns (FR-002).
3. **API contracts** — request/response schema conformance, error response structure.
4. **Data validation** — rejection of malformed/out-of-range external data before it reaches reasoning.
5. **Geospatial calculations** — tolerance filtering correctness, `GEOGRAPHY` distance accuracy.
6. **Conflict resolution** — seeded conflicting data reliably produces a surfaced conflict record (FR-010).
7. **Evidence verification** — the evidence-audit pattern (NFR-002): every claim in a test response resolves to ≥1 evidence row.

**Rule TEST-C1:** No pull request that touches an agent, the Coordinator, or the Verification module may merge without an accompanying or updated test for the changed behavior.

---

## 21. Security Standards

**Rule SEC-C1:** No hardcoded secrets (§15). CI should include a secret-scanning step where feasible — exact tool: `TBD – Requires Team Decision`.

**Rule SEC-C2:** All user input is sanitized before reaching the LLM layer or the database (`ARCHITECTURE_RULES.md SEC-2`).

**Rule SEC-C3:** No user authentication/account system is implemented (`ARCHITECTURE_RULES.md SEC-3`) — session handling uses only the opaque `conversation_sessions` token.

**Rule SEC-C4:** Dependencies are kept free of known critical vulnerabilities — a dependency audit step is run periodically; exact tool/cadence: `TBD – Requires Team Decision`.

**Rule SEC-C5:** `hazard_alerts` attribution fields are never made nullable in any migration, in any environment, including local development seed data (`ARCHITECTURE_RULES.md SEC-5`).

---

## 22. Performance Rules

**Rule PERF-1:** Only agents required by the routing table for a given intent are invoked (`ARCHITECTURE_RULES.md COORD-2`) — code must not "warm up" or speculatively call unrelated agents.

**Rule PERF-2:** The short-TTL response cache (`ARCHITECTURE_RULES.md ING-4`) is used for repeated source calls within a session before adding any other performance optimization.

**Rule PERF-3:** Database queries on `observations` use the documented indexes (`DATABASE_SCHEMA.md §21`) — a query added without confirming it hits an existing index (or justifying a new one) is not acceptable.

**Rule PERF-4:** No premature optimization (caching layers, query batching, async fan-out beyond what §10–§11 of `AGENT_ARCHITECTURE.md` already specifies) without a measured latency problem — this is an MVP-scale prototype (§28).

---

## 23. Dependency Management

**Rule DEP-C1:** New dependencies are added deliberately, with a one-line justification in the PR description — not pulled in casually for a small convenience function that could be hand-written in a few lines.

**Rule DEP-C2:** Dependency versions are pinned (exact versions or narrow ranges) in the lockfile — no unpinned `*` version ranges.

**Rule DEP-C3:** No dependency is added that duplicates an already-approved tool's function (e.g., a second HTTP client library when one is already standard) without justification.

**Rule DEP-C4:** Any dependency touching secrets, network access, or database access is reviewed with extra scrutiny before merge, given the security boundaries in §21.

---

## 24. Git Standards

**Rule GIT-1:** `main` (or the team's designated stable branch) is always in a working state — no direct commits of known-broken code.

**Rule GIT-2:** Feature branches are named descriptively and scoped to one logical change (e.g., `agent/fisheries-combination-rule`, `api/query-endpoint-schema`).

**Rule GIT-3:** No secrets, `.env` files, or generated build artifacts are committed — enforced via `.gitignore` and, where available, pre-commit hooks.

**Rule GIT-4:** Branches touching an agent's forbidden-responsibility boundary (`ARCHITECTURE_RULES.md §16`) require the reviewer to explicitly confirm the boundary was respected before merge (§27).

---

## 25. Commit Message Standards

**Rule COMMIT-1:** Commit messages follow a conventional structure: `<type>(<scope>): <short summary>`, e.g., `fix(safety-agent): enforce non-null source attribution`, `feat(coordinator): add parallel dispatch for independent sub-tasks`.

**Rule COMMIT-2:** Types are limited to a small, consistent set: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`. An AI coding agent must pick the closest matching type rather than inventing new ones.

**Rule COMMIT-3:** A commit that changes behavior governed by `ARCHITECTURE_RULES.md` or this document references the relevant rule ID in the commit body (e.g., "Implements VER-3 bounded retry for causal-language rewrite").

**Rule COMMIT-4:** No commit message may claim a rule/requirement is satisfied without the corresponding test existing in the same commit or PR (ties to Rule TEST-C1).

---

## 26. Documentation Standards

**Rule DOC-1:** Every agent module has a docstring stating its purpose, its `AGENT_ARCHITECTURE.md` reference section, and its forbidden responsibilities.

**Rule DOC-2:** Every Pydantic schema has field-level descriptions where the meaning is not self-evident from the name (especially `confidence_label`, `data_type`, `quality_flag` — values with a fixed, meaningful enumeration).

**Rule DOC-3:** Non-obvious architectural decisions made during implementation are recorded as a short Architecture Decision Record (ADR) in `docs/decisions/` — format: `TBD – Requires Team Decision`, but at minimum: date, decision, rationale, alternatives considered.

**Rule DOC-4:** README files at the repository root and within `frontend/`/`backend/` are kept current with setup instructions — an AI coding agent that changes how the project is run (new env var, new setup step) updates the relevant README in the same change.

---

## 27. Code Review Standards

**Rule REVIEW-1:** Every change to an agent, the Coordinator, or the Verification module is checked against its `ARCHITECTURE_RULES.md §16` boundary definition — reviewer confirms no forbidden responsibility was introduced.

**Rule REVIEW-2:** Every change to a Pydantic schema or database model is checked against `DATABASE_SCHEMA.md`'s constraint table (§22 there) — reviewer confirms no constraint was silently weakened.

**Rule REVIEW-3:** Every change touching prompt templates is checked against Rule PROMPT-3 — no prompt may be merged that could produce unqualified causal language or fabricated hazard content.

**Rule REVIEW-4:** No self-merge for changes affecting the reasoning path (agents, Coordinator, Verification, database schema) — at least one other reviewer (human or a second AI-agent review pass, per team process) confirms compliance with this document and `ARCHITECTURE_RULES.md`. Exact review tooling/process: `TBD – Requires Team Decision`.

---

## 28. Definition of Done

A change is **Done** only when all of the following hold:

1. Code follows the relevant sections of this document (type safety, structure, error handling, logging).
2. Code follows `ARCHITECTURE_RULES.md` — no forbidden responsibility crossed, no unauthorized new service/agent/table introduced.
3. Tests exist for the changed behavior, at the appropriate level (unit/integration/E2E per §20), and pass.
4. No hardcoded secret, credential, or private URL was introduced (§15, §21).
5. Static type checks pass (Rule TYPE-4).
6. If the change affects a PRD requirement (FR-xxx/NFR-xxx), the corresponding acceptance criterion in `PRD.md` is verifiably satisfied — not merely "looks right."
7. Documentation (docstrings, README, ADR if applicable) is updated in the same change.
8. The change does not introduce infrastructure, a dependency, or complexity beyond what the MVP/Prototype tier requires (`ARCHITECTURE_RULES.md §24`, MVP Simplification Rules) unless explicitly justified and approved.
9. Any `TBD – Requires Team Decision` the change depends on has been resolved and recorded (not silently assumed).

**MVP Rule (binding):** When a design choice could go either toward "quick, working, sufficient for the demonstration" or "flexible, general, enterprise-ready," the coding agent defaults to the former. Do not introduce infrastructure, abstraction layers, or configurability solely because it is common practice elsewhere or technically interesting — every addition must trace to an approved requirement, per Principle P9 in `ARCHITECTURE_RULES.md §1`.

---

## AI CODING DIRECTIVE

**This directive is binding on Google Antigravity IDE, OpenCode, and any other AI coding agent writing or modifying code in the ORCA repository.**

1. **Read this file, together with `ARCHITECTURE_RULES.md`, before writing or modifying any code.** Both documents must be consulted — architecture rules govern structure and boundaries; this document governs implementation quality and conventions.

2. **Follow every rule in this document unless an explicit architecture decision overrides it.** An "explicit architecture decision" means a recorded, human-approved change to this document or `ARCHITECTURE_RULES.md` (or an ADR under `docs/decisions/`) — not an inferred exception, not a judgment call made silently during code generation.

3. **Where this document marks a technology or convention `TBD – Requires Team Decision`, do not resolve it unilaterally.** Propose an option, state the tradeoff briefly, and flag it for sign-off before writing code that depends on the unresolved choice being one way or another.

4. **When a requested change would violate a rule here** (for example, introducing an untyped `any`, hardcoding a credential, skipping a test for agent/Coordinator/Verification logic, or bypassing Pydantic validation), **the coding agent must state which rule would be violated and why the change seems necessary, and must not proceed with the violation silently.**

5. **Treat the Definition of Done (§28) as the actual completion bar** for any task — not "the code runs," but "the code runs, is typed, is tested, follows structure, contains no secrets, and stays within MVP scope."

6. **When in doubt, choose the more boring, smaller, better-tested implementation over the more sophisticated one.** This mirrors `ARCHITECTURE_RULES.md`'s closing directive and applies at the code level exactly as it does at the architecture level.

---

*End of CODING_RULES.md*