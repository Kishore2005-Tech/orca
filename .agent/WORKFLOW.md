# WORKFLOW.md
### Project: SIH26176 — ORCA (Ocean Research, Conservation & Analytics — Marine Ecosystems Reasoning with Collaborative Agents)
### Scope: Governs how any AI coding agent (Google Antigravity IDE, OpenCode, or equivalent) works on this repository.

This document is binding. It defines the mandatory sequence, checkpoints, and refusal conditions that govern every code change an AI agent makes to ORCA. An agent that skips a required step, fabricates a completion, or bypasses a human review gate defined here is non-compliant with this project, regardless of how plausible its output looks.

---

## 1. Workflow Principles

1. **Understand before you touch.** No agent may begin writing implementation code before completing Context Loading (§3), Requirement Analysis (§4), Documentation Review (§5), and Architecture Review (§6).
2. **Plan before code.** Any change beyond a trivial fix requires a written plan reviewed against `ARCHITECTURE_RULES.md` before implementation starts (see PLAN BEFORE CODE RULE).
3. **Small, coherent iterations.** ORCA is built one working, testable feature at a time — never as one large speculative implementation (see SMALL ITERATION RULE).
4. **Every change is verified, not assumed.** Lint, type-check, unit tests, integration tests, and build verification run after every meaningful change (see TEST AFTER CHANGE RULE).
5. **Science is not optional plumbing.** Any change touching marine data, agent reasoning, confidence, or evidence must pass the Scientific Review Rule (§ Scientific Review Rule) — this project's credibility depends on it.
6. **No fake completion, ever.** A feature is either genuinely done per the Definition of Done (§17), or it is explicitly reported as incomplete. There is no third option.
7. **Humans gate the decisions that matter.** Certain classes of change never ship on agent judgment alone (§ Human Review Gates).
8. **Documentation is a primary source, not an afterthought.** ORCA's existing docs (`AGENT_ARCHITECTURE.md`, `AGENT_CONTRACTS.md`, `REASONING_FRAMEWORK.md`, `EVIDENCE_AND_CONFLICT_FRAMEWORK.md`, `DATABASE_SCHEMA.md`, and the four governance documents) are the ground truth the agent must reconcile its work against, not background reading it can skim.

---

## 2. Repository Initialization

Before any work begins in a session, the agent must:

1. Confirm the working directory is the ORCA repository root (verify presence of `PROJECT_CONTEXT.md`, `ARCHITECTURE_RULES.md`, `/docs`, and a recognizable project manifest — `package.json`, `pyproject.toml`, etc.).
2. Confirm the current git branch and status (`git status`, `git log -1`) — never assume a clean working tree.
3. Confirm the environment can build/run at all (dependency install, environment variables present per `.env.example` or equivalent) before attributing any failure later in the session to the agent's own change.
4. If any of the above cannot be confirmed, the agent stops and reports the blocker rather than proceeding on assumptions.

---

## 3. Context Loading

**Mandatory initial context order** — read in this exact sequence before implementing any significant feature:

1. `PROJECT_CONTEXT.md`
2. `ARCHITECTURE_RULES.md`
3. `CODING_RULES.md`
4. `SCIENTIFIC_RULES.md`
5. `WORKFLOW.md` (this document)
6. Relevant documents under `/docs` (at minimum: `AGENT_ARCHITECTURE.md`, `AGENT_CONTRACTS.md`, `REASONING_FRAMEWORK.md`, `EVIDENCE_AND_CONFLICT_FRAMEWORK.md`, `DATABASE_SCHEMA.md`, plus any document whose title matches the feature area)

Then inspect, in this order:

- **Repository structure** — directory layout, module boundaries, existing conventions.
- **Existing code** — the specific files and modules the feature will touch, and their immediate neighbors.
- **Existing APIs** — endpoint contracts already in place; do not assume a new endpoint is needed without checking.
- **Database schema** — current state of tables versus `DATABASE_SCHEMA.md`; the two must be reconciled if they've drifted.
- **Datasets** — what real/representative marine data is actually available and connected, versus what is placeholder or mocked.
- **Environment configuration** — required environment variables, API keys, service dependencies.
- **Tests** — what's already covered, what's not, and what the existing test patterns look like.

An agent that proposes an implementation plan without having done this inspection has violated §1.1 regardless of the plan's apparent quality.

---

## 4. Requirement Analysis

For every incoming feature request or bug report, the agent must produce a structured requirement summary before planning:

- **What was asked** — restated precisely, in the agent's own words, to surface ambiguity early.
- **What is implied but not stated** — e.g., a request for "show wave risk" implies a confidence/evidence requirement per `REASONING_FRAMEWORK.md`, even if not mentioned.
- **What is explicitly out of scope** — stated, so scope creep and silent scope-shrinking are both visible.

If the requirement is ambiguous, follow § Handling Ambiguous Requirements before proceeding.

---

## 5. Documentation Review

Before planning implementation, the agent must check the feature against:

- `SCIENTIFIC_RULES.md` — does this feature touch a scientific claim, confidence, or evidence path?
- `AGENT_ARCHITECTURE.md` / `AGENT_CONTRACTS.md` — does this feature belong to an existing agent's responsibilities, or does it imply a new one? (New agents are not created lightly — see `AGENT_ARCHITECTURE.md` § Why Not More Agents.)
- `REASONING_FRAMEWORK.md` — does this feature intersect the reasoning pipeline (intent detection, evidence grounding, confidence estimation, recommendation gate)?
- `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` — does this feature produce or consume evidence, or touch conflict resolution?
- `DATABASE_SCHEMA.md` — does this feature require new tables/columns, or can it use what exists?

Any place where the requirement conflicts with existing documentation must be resolved per § Handling Conflicting Documentation before implementation begins — never silently implemented in whichever direction is easiest to code.

---

## 6. Architecture Review

Before implementation, the agent confirms:

- The change fits within an existing agent's defined responsibilities and does not silently expand a "Forbidden Responsibilities" boundary from `AGENT_ARCHITECTURE.md`.
- The change respects the Standard Response Envelope and per-agent contracts in `AGENT_CONTRACTS.md` — no ad hoc, unstructured output where a schema already exists.
- The change respects deterministic-vs-LLM boundaries from `REASONING_FRAMEWORK.md` §3–4 — no moving a decision that must be deterministic (routing, confidence scoring, the recommendation gate, verification verdicts) into free-form LLM judgment.
- The change does not bypass the evidence grounding requirements in `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` Part A.

If the change requires deviating from any of the above, this is a **major architecture change** and requires a Human Review Gate (§ Human Review Gates) before implementation.

---

## 7. Implementation Planning

For every major feature, the agent must produce a written plan identifying:

| Field | Content |
|---|---|
| **Objective** | What the feature achieves, in one or two sentences |
| **Files affected** | Concrete file paths, new and modified |
| **Dependencies** | New packages/services required, and why existing ones are insufficient |
| **Data required** | Which datasets/tables, and whether they are real, representative, or currently absent |
| **APIs required** | New or existing endpoints touched |
| **Scientific assumptions** | Any assumption about units, thresholds, baselines, or causality being made |
| **Architecture impact** | Which agent(s)/pipeline stage(s) are touched, and whether any contract changes |
| **Testing strategy** | What will be unit-tested, integration-tested, and scientifically validated |
| **Risks** | What could break, what could be scientifically wrong, what could silently degrade |
| **Acceptance criteria** | Concrete, checkable conditions for "done" |

This plan is the PLAN BEFORE CODE RULE artifact (see below) and must exist before implementation for anything beyond a trivial, localized fix.

---

## 8. Task Decomposition

Once a plan is approved, the agent breaks it into the smallest set of coherent, independently testable sub-tasks that together satisfy the acceptance criteria. Each sub-task should:

- Be completable and verifiable on its own (passes lint/type-check/tests before the next sub-task begins).
- Touch the minimum necessary surface area.
- Be sequenced so that dependencies (e.g., a schema migration before the code that uses it) come first.

This decomposition is what makes the SMALL ITERATION RULE enforceable in practice, not just in principle.

---

## 9. Implementation

- Implement one decomposed sub-task at a time, per SMALL ITERATION RULE.
- Follow `CODING_RULES.md` for style, structure, and language/framework conventions — this document does not override it.
- Every structured output (agent responses, evidence records, confidence values) must conform exactly to the schemas in `AGENT_CONTRACTS.md` and `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` — no free-form substitutions where a schema exists (this document's binding rule, consistent with those two).
- Do not implement placeholder/mock behavior without explicit, visible disclosure in code comments and in the sub-task's status report (see NO FAKE COMPLETION RULE).

---

## 10. Testing

After each sub-task:

1. **Lint** — must pass with zero new violations.
2. **Type check** — must pass with zero new errors.
3. **Unit tests** — new/changed logic must have unit tests; existing unit tests must still pass.
4. **Integration tests** — required wherever the change crosses an agent boundary, touches the database, or touches an external API/dataset.
5. **Build verification** — the project must still build/run cleanly end to end.

A sub-task is not complete until all applicable items above pass. See TEST AFTER CHANGE RULE.

---

## 11. Integration

When a sub-task's output feeds into another agent, pipeline stage, or existing feature:

- Verify the Standard Response Envelope fields are populated correctly end to end (`AGENT_CONTRACTS.md` §0).
- Verify the change does not break an existing agent's declared dependencies (`AGENT_ARCHITECTURE.md` § Dependencies per agent).
- Run integration tests covering the actual cross-boundary call, not just each side in isolation.
- Confirm the Coordinator can still consume the modified agent's output without special-case handling (per the Cross-Agent Consumption Guarantee in `AGENT_CONTRACTS.md`).

---

## 12. Scientific Validation

Before any marine-science-related feature is considered implemented, run the **Scientific Review Rule** (defined below) explicitly and record its result in the sub-task's status.

---

## 13. Code Review

Every non-trivial change is reviewed (by a human, or by a second agent pass acting as reviewer) against:

- `CODING_RULES.md` conformance.
- Whether the implementation actually matches the approved plan (§7) — deviations must be called out, not silently shipped.
- Whether structured schemas were respected (§9).
- Whether tests genuinely exercise the new behavior, not just pass trivially.

---

## 14. Security Review

Required whenever a change:
- Adds or modifies an API endpoint, especially anything accepting user input.
- Touches authentication, authorization, or `users` table logic.
- Adds a new external API integration or credential.
- Changes environment/configuration handling.

Minimum checks: input validation present, no secrets committed, no unsanitized query construction (SQL injection surface), no unbounded/untrusted data reaching a tool call or external fetch without validation. Any security-relevant change is also a Human Review Gate item (§ Human Review Gates).

---

## 15. Performance Review

Required whenever a change touches:
- `marine_observations` or other high-volume time-series queries — confirm the query pattern uses the indexes defined in `DATABASE_SCHEMA.md` §9, not a full scan.
- Spatial queries — confirm GIST-indexed columns and appropriate predicates (`ST_DWithin`, not unindexed distance computation over the whole table).
- Vector search — confirm the HNSW index is used and `top_k` is bounded.
- Any pipeline stage timeout budget — confirm the change does not silently exceed the per-agent `TIMEOUT` values in `AGENT_CONTRACTS.md`.

Performance review is a check, not a premature optimization exercise — per `DATABASE_SCHEMA.md` §10, do not add complexity (caching layers, materialized views, partitioning) unless a measured problem justifies it.

---

## 16. Final Verification

Before a feature is reported as done, the agent re-runs, in order: lint → type check → unit tests → integration tests → scientific validation (if applicable) → build. All must pass simultaneously on the current state of the branch, not on a remembered earlier pass.

---

## 17. Definition of Done

A feature is **done** only when all of the following are true:

- [ ] It matches the approved plan (§7), or deviations are explicitly documented and approved.
- [ ] It is implemented end to end — no missing backend behind a UI, no unconnected dataset, no uninvoked agent (see NO FAKE COMPLETION RULE).
- [ ] All applicable schemas (`AGENT_CONTRACTS.md`, `EVIDENCE_AND_CONFLICT_FRAMEWORK.md`) are respected in the actual code, not just intended.
- [ ] Lint, type check, unit tests, integration tests, and build all pass (§16).
- [ ] Scientific Review Rule has been applied and passed, if the feature is science-relevant.
- [ ] Code review has occurred (§13).
- [ ] Any applicable Human Review Gate has been passed (§ Human Review Gates).
- [ ] No hardcoded confidence scores, fabricated citations, or undisclosed mocks remain in the shipped path.
- [ ] The change is committed following the Git Workflow (§18).

If any box is unchecked, the feature is **not done** and must be reported as such.

---

## 18. Git Workflow

1. One branch per feature/fix, named descriptively (`feature/`, `fix/`, `chore/` prefix).
2. Commits are small and scoped to one sub-task each, with messages describing *what* and *why*, not just *what*.
3. No direct commits to the main/production branch — all changes go through a reviewable branch, even in solo/agent-driven development, so history remains a usable audit trail.
4. Before opening for review, the branch must independently pass Final Verification (§16) on a clean checkout.
5. Commit messages referencing a scientific or architectural decision should cite the governing document (e.g., "per REASONING_FRAMEWORK.md §10, block recommendation when evidence insufficient").

---

## 19. Rollback Strategy

- Every change that touches the database schema must have a corresponding down-migration or explicitly documented manual rollback path before it ships — no one-way schema changes without a plan back.
- Every deployed feature should be revertible by branch/commit revert without requiring a data backfill, unless the plan (§7) explicitly flagged and got sign-off for a non-trivial rollback.
- If a shipped change is found to violate the Scientific Review Rule or produces fabricated/ungrounded output in production, it is rolled back immediately, not patched forward under pressure — correctness is restored first, then a proper fix follows the full workflow again.

---

## 20. Handling Ambiguous Requirements

When a requirement is unclear:
1. The agent states its best-guess interpretation explicitly, in writing, before proceeding.
2. If the ambiguity affects scientific correctness, evidence handling, or architecture (i.e., touches anything in §5–6), the agent does **not** proceed on its own guess — it surfaces the ambiguity as a question and treats this as a Human Review Gate trigger.
3. If the ambiguity is purely cosmetic/UX and low-stakes, the agent may proceed on its stated best guess, but must flag it clearly in the sub-task report so it's easy to correct.

---

## 21. Handling Conflicting Documentation

When two governing documents (or a document and the actual codebase) disagree:
1. The agent does not silently pick one and implement it — this is exactly the kind of unresolved-conflict situation `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` Part B exists to prevent, applied here to documentation instead of live data.
2. The agent reports the specific conflict (quoting both sources) and treats it as a Human Review Gate item.
3. Once resolved by a human, the losing document is updated in the same change set — conflicting documentation is never left to linger for the next agent to trip over.

---

## 22. Handling Failed Tests

1. A failing test blocks progress to the next sub-task — it is not deferred "to fix later."
2. The agent first determines whether the failure is caused by its own change, a pre-existing flaky/broken test, or an environment issue — and states which, with evidence, before proceeding.
3. Pre-existing failures unrelated to the current change are reported, not silently fixed as a side quest unless trivial and clearly in scope — unrelated fixes belong in their own small iteration (§ Small Iteration Rule), not bundled invisibly into an unrelated feature's commit.
4. Under no circumstance is a test disabled, skipped, or loosened solely to make a build pass — that is a Definition of Done violation and a NO FAKE COMPLETION RULE violation.

---

## 23. Handling Agent Failures

("Agent" here refers to both ORCA's own domain agents and the AI coding agent operating this workflow.)

- If an ORCA domain agent (Ocean, Ecosystem, Fisheries, Safety, Geospatial, Knowledge/RAG, Verification, Coordinator) fails during development/testing, the coding agent follows the FALLBACK behavior already defined for that agent in `AGENT_CONTRACTS.md` — it does not invent new fallback behavior ad hoc.
- If the AI coding agent itself gets stuck (repeated failed attempts, unclear how to proceed, tool errors it cannot resolve), it stops, reports exactly what was tried and what failed, and escalates rather than looping indefinitely or shipping a partial fix disguised as complete.
- Any change made to an agent's failure-handling logic itself is an architecture change and requires a Human Review Gate.

---

## 24. Handling Data/API Failures

- Missing or unavailable data is never backfilled with an inferred/fabricated value — per `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` §B.6, absence is reported as absence.
- External API/dataset outages during development are reported, and the affected feature's testing proceeds against representative fixture data clearly labeled as such — never silently swapped in as if it were live data without disclosure.
- Any code path that currently depends on a mocked or unavailable data source must have that fact stated plainly in the sub-task status and the Definition of Done checklist — this is a direct instance of the NO FAKE COMPLETION RULE.

---

## 25. MVP Prioritization

See **MVP PRIORITY RULE** below — this section exists to confirm that all preceding process steps (planning, testing, review) still apply at MVP scope; MVP status changes *what* gets built next, not *how carefully* it gets built.

---

## Implementation Process (Canonical Flow)

Every feature, without exception, follows this sequence:

```
Requirement
    │
    ▼
Understand        (§3 Context Loading, §4 Requirement Analysis)
    │
    ▼
Inspect            (§3 repository/code/API/schema/dataset/env/test inspection)
    │
    ▼
Plan               (§7 Implementation Planning — PLAN BEFORE CODE RULE)
    │
    ▼
Architecture Check (§6 Architecture Review)
    │
    ▼
Implementation     (§8 Task Decomposition, §9 Implementation — SMALL ITERATION RULE)
    │
    ▼
Unit Tests         (§10 Testing — TEST AFTER CHANGE RULE)
    │
    ▼
Integration Tests  (§11 Integration)
    │
    ▼
Scientific Validation (§12 — SCIENTIFIC REVIEW RULE)
    │
    ▼
Review             (§13 Code Review, §14 Security Review, §15 Performance Review)
    │
    ▼
User Verification  (§ Human Review Gates, where applicable)
    │
    ▼
Complete           (§17 Definition of Done)
```

No stage may be skipped. A stage may be trivially fast (e.g., "Architecture Check: confirmed no architectural impact, one line reasoning") but it must still be explicitly performed and recorded, not silently omitted.

---

## PLAN BEFORE CODE RULE

**The agent must not perform large architectural changes without first producing and — where required by § Human Review Gates — getting sign-off on a written plan.**

- "Large" means: touches more than one agent's contract, changes a database table's shape, introduces a new agent, changes the reasoning pipeline's deterministic/LLM boundary, or changes confidence/evidence handling.
- The plan must use the template in §7 and must be produced *before* any implementation file is created or modified for that feature.
- Small, localized fixes (a typo, a clearly-scoped bug fix with no architectural surface) are exempt from the full plan template but still require the agent to state, in one or two sentences, why it judges the change to be small.

---

## SMALL ITERATION RULE

**Implement one coherent feature at a time. Never generate the entire application, or a large unreviewed swath of it, in a single unbroken pass.**

- Each iteration corresponds to one sub-task from Task Decomposition (§8).
- Each iteration must independently pass Testing (§10) before the next begins.
- An iteration that turns out to be larger than expected is split further, not pushed through as-is.
- This rule exists specifically to keep every change reviewable, testable, and attributable — a single giant diff cannot be meaningfully code-reviewed, security-reviewed, or scientifically validated, which defeats the purpose of every other section in this document.

---

## TEST AFTER CHANGE RULE

**After every meaningful implementation step, the agent runs, in this order:**

1. Lint
2. Type check
3. Unit tests
4. Integration tests (where applicable to the change)
5. Build verification

"Meaningful" means any change that alters behavior, not purely cosmetic/comment edits. If any step fails, the agent fixes it before proceeding to the next sub-task — see § Handling Failed Tests. Results (pass/fail, and what was fixed) are recorded in the sub-task status, not merely asserted as "tests pass" without evidence.

---

## SCIENTIFIC REVIEW RULE

**Before completing any marine-science feature, the agent must explicitly verify and record:**

- **Parameter units** — every value's unit is present, correct, and consistent with `DATABASE_SCHEMA.md`'s `marine_observations.unit` / `EVIDENCE_AND_CONFLICT_FRAMEWORK.md`'s EGR `unit` field.
- **Timestamp** — `observed_at`/`valid_at` is present, correctly distinguished from retrieval/generation time, and not presented as current when stale (`REASONING_FRAMEWORK.md` §7).
- **Spatial coordinates** — location is resolved via Geospatial Agent / `locations` table, not an ad hoc unverified coordinate (`REASONING_FRAMEWORK.md` §8).
- **Source provenance** — every claim traces to a named source/dataset (`EVIDENCE_AND_CONFLICT_FRAMEWORK.md` Part A) — no unattributed numbers.
- **Observation vs. forecast** — `is_forecast` (or equivalent) is correctly set and surfaced to the user; a forecast is never presented as an observed fact.
- **Scientific assumptions** — any threshold, baseline, or classification rule used is the one defined in the governing documents (`REASONING_FRAMEWORK.md` §5), not an ad hoc value chosen during implementation.
- **Uncertainty** — confidence level/score is computed per the deterministic rules in `REASONING_FRAMEWORK.md` §9/§11 and `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` Part B — never hardcoded or LLM-guessed.
- **Unsupported conclusions** — no causal language without a study-backed citation (`REASONING_FRAMEWORK.md` §5), and no recommendation issued where the evidence-sufficiency gate (`REASONING_FRAMEWORK.md` §10) would block it.

A feature fails Scientific Review if any item above cannot be checked off with evidence from the actual code, not from the agent's description of what the code is supposed to do.

---

## NO FAKE COMPLETION RULE

**The agent must never report a feature as complete if any of the following is true:**

- The UI exists but the backend integration behind it is missing or stubbed.
- An API is mocked, without that fact being disclosed in both the code (comments/flags) and the status report.
- A dataset is referenced in code or documentation but not actually connected/queried.
- An agent is defined but never invoked in the real execution path.
- A confidence score is hardcoded rather than computed per `REASONING_FRAMEWORK.md` §11 / `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` Part B.
- A source citation is fabricated, guessed, or not traceable to an actual `evidence` record.
- Tests are missing for behavior classified as critical (anything touching safety, evidence grounding, confidence, or the recommendation gate).

Violating this rule is treated as a workflow failure requiring immediate correction, not a minor documentation gap — a false "done" is worse than an honest "not done" because it removes the signal that would otherwise trigger review.

---

## MVP PRIORITY RULE

**For the current SIH26176 prototype, feature and effort priority follows this order:**

1. **End-to-end functionality** — a complete, working path from user query to answer beats a polished fragment.
2. **Core agent collaboration** — the Coordinator successfully orchestrating at least the core domain agents (Ocean, Ecosystem/Fisheries/Safety as relevant, Geospatial) beats any single agent in isolation being deeply featured.
3. **Real/representative marine datasets** — connect actual or clearly-labeled representative data over building more UI around placeholder data.
4. **Evidence-grounded reasoning** — every claim traceable per `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` Part A, even if the dataset breadth is limited.
5. **Verification** — the Verification Agent actually running and gating output, even in a simplified form, before adding more domains.
6. **Explainability** — the Explanation stage producing genuinely traceable, cited output.
7. **Professional UI** — polish comes last, once the above is real.

**Explicitly avoid unnecessary enterprise complexity at this stage**: no speculative multi-tenant architecture, no premature partitioning/caching (per `DATABASE_SCHEMA.md` §10), no auth/roles system beyond what's needed to demo, no additional agents beyond those justified in `AGENT_ARCHITECTURE.md`. Every one of these is a valid *future* addition, not an MVP requirement — building them now is scope that competes directly with items 1–6 above.

---

## HUMAN REVIEW GATES

**The agent must stop and obtain explicit human review/approval before proceeding, in these cases:**

- **Major architecture changes** — anything altering agent boundaries, the orchestration/dependency graph, or the reasoning pipeline stages defined in `REASONING_FRAMEWORK.md`.
- **Scientific logic changes** — any change to thresholds, classification rules, confidence scoring formulas, or the causal-language/evidence-sufficiency constraints in `REASONING_FRAMEWORK.md` §5/§9/§10 and `EVIDENCE_AND_CONFLICT_FRAMEWORK.md`.
- **Data schema changes** — any modification to `DATABASE_SCHEMA.md`'s tables, especially `marine_observations`, `evidence`, or `recommendations`.
- **Agent responsibility changes** — adding, removing, merging, or reassigning responsibilities of any agent defined in `AGENT_ARCHITECTURE.md`.
- **Adding major dependencies** — a new external API, a new core library, a new infrastructure component.
- **Changing security configuration** — auth, credentials handling, input validation policy, CORS/network policy.

For each gate, the agent presents: what is changing, why, what was considered and rejected, and the specific risk being introduced. The agent does not proceed past the gate until it receives explicit approval — silence, ambiguity, or the agent's own confidence in the change is not approval.

---

## AI AGENT OPERATING DIRECTIVE

Any AI coding agent operating on the ORCA repository — including but not limited to Google Antigravity IDE and OpenCode — **must follow this workflow document in full**, together with the four governance documents it depends on:

1. `PROJECT_CONTEXT.md`
2. `ARCHITECTURE_RULES.md`
3. `CODING_RULES.md`
4. `SCIENTIFIC_RULES.md`

before implementing, modifying, or extending any part of ORCA. This applies regardless of how the task is phrased, how urgent it appears, or how confident the agent is that a shortcut is safe. Where this document and a user instruction conflict, the agent surfaces the conflict per § Handling Conflicting Documentation and seeks human resolution — it does not silently prioritize speed over the process defined here. This workflow is not a suggestion layered on top of ORCA's engineering practice; for the purposes of this repository, it **is** the engineering practice.