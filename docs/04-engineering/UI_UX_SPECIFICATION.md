# ORCA UI/UX Specification

This document specifies ORCA's interface as a **marine intelligence operations product** — the visual and interaction language of an Earth-observation / mission-ops tool (think INCOIS, Windy, Planet, NASA Worldview), not a chat application with a data sidebar bolted on. "Ask ORCA" is one panel among many, not the front door.

Every screen below is specified against the data this product actually has, per `API_SPECIFICATION.md`, `EVIDENCE_AND_CONFLICT_FRAMEWORK.md`, and `REASONING_FRAMEWORK.md` — confidence, evidence, and the recommendation gate are treated as first-class visual elements throughout, not an afterthought tooltip.

---

## 0. Design Philosophy — Why This Is Not a Chatbot

1. **Map and dashboard are the home surface.** A user opens ORCA and sees current conditions, active advisories, and a live map — not an empty text box waiting for a question.
2. **Ask ORCA is a tool, not the product.** It's reachable from anywhere (persistent entry point), but its output renders as a structured intelligence card — confidence badge, citations, agent trace — never a scrolling chat transcript of bubbles.
3. **Every claim carries its evidence and confidence in the same view.** Nothing is stated without the user being able to see, in one interaction, where it came from and how sure ORCA is.
4. **Uncertainty is shown, never hidden or smoothed over.** Blocked recommendations, unresolved conflicts, and stale data are first-class UI states with their own visual treatment — not swallowed into a generic "something went wrong."
5. **Density is earned, not decorative.** This is a data-dense professional tool for people making real decisions (going out on the water, issuing an advisory, running a study) — usability and clarity take priority over visual flourish at every decision point.

### Visual System (applies across all screens)

- **Palette:** deep navy/slate base (`#0B1929`-family) for chrome and map backgrounds, so satellite/ocean-color data reads clearly against it; a restrained teal/cyan accent for interactive elements; a strict, non-negotiable status palette reserved *only* for safety/confidence meaning — green (safe/high confidence), amber (caution/medium confidence), red (danger/low confidence or blocked) — never used decoratively elsewhere, so color always carries information.
- **Typography:** a functional grotesk/sans-serif for UI text; tabular (monospaced-figure) numerals for all data values so columns of numbers align; clear three-level type hierarchy (screen title / section label / data value).
- **Iconography:** one fixed icon per agent domain (wave for Ocean, coral for Ecosystem, anchor for Fisheries, hazard triangle for Safety, pin for Geospatial, book for Knowledge/RAG, checkmark-shield for Verification, compass for Coordinator) used identically everywhere that agent appears, so users learn the vocabulary once.
- **Accessibility:** confidence and severity are always conveyed by icon + label + color together, never color alone; minimum touch target 44px; all data tables/charts have a text-equivalent view.
- **Progressive disclosure:** every screen leads with a plain-language summary and makes technical/raw detail one interaction away — never zero clicks (buried) and never zero-summary (dumped).

---

## 1. Dashboard

**Purpose:** the home operational overview — what's happening right now, anywhere the user cares about.
**User:** all roles; this is the default landing screen.

**Components:** safety alert ticker (only visible when active); key-metric cards (SST, wave height, active PFZ count, active advisories count) for the user's default region(s); map preview widget; recent queries/recommendations feed; mode-specific widget set (see §12–14).

**Information hierarchy:** (1) any active `DANGEROUS`-level safety alert, full-width, top, unmissable; (2) key metric cards; (3) map preview; (4) recent activity feed.

**Interactions:** click a metric card → drills into the corresponding observation layer on the Map (§2); click the alert ticker → Alerts screen (§11); click a recent recommendation → Recommendation Panel (§6) for that query.

**Loading state:** metric cards render as shimmering skeletons with fixed dimensions (no layout shift); alert ticker stays hidden until its own fetch resolves (never shows a false "no alerts" while still loading).

**Empty state:** no default region set → single prompt: "Select a region to see live conditions," with a location picker inline, not a blank dashboard.

**Error state:** partial failure (e.g., one data source down) shows the cards that loaded plus a small inline warning badge on the failed card ("SST unavailable — source unreachable") — the whole dashboard never goes blank for one failed widget.

**Mobile behavior:** single-column stack, alert ticker pinned to the very top of the viewport, map preview becomes a tappable thumbnail linking to the full-screen Map.

---

## 2. Marine Intelligence Map

**Purpose:** primary spatial exploration surface — SST, chlorophyll, currents, waves, wind, PFZ zones, and safety advisories as togglable layers over a live map.
**User:** all roles, primary tool for Scientist and Fisher modes.

**Components:** full-screen map canvas; layer control panel (toggle + opacity per layer); temporal scrub bar (steps through `observed_at` history, with a distinct visual treatment for forecast vs. observed frames); persistent legend; location search/geocode box; click-to-inspect popover.

**Information hierarchy:** map is dominant (≥80% of viewport); layer controls are a collapsible side panel; legend is a fixed, always-visible corner element; time scrub sits along the bottom edge.

**Interactions:** click any point → evidence popover (source, quality, `observed_at`, value); draw a bounding box → triggers an area query (`/observations`, `/map`); drag time scrub → re-renders the layer at that timestamp; toggle "forecast" → dashed/lower-opacity rendering distinct from solid observed data.

**Loading state:** map tiles load progressively (base map first, data layers streamed in); each layer toggle shows its own small loading spinner while its data fetches, independent of the others.

**Empty state:** a toggled-on layer with no data for the current region/time shows an explicit in-map banner — "No SST data available for this area/time" — never a silently blank layer that looks like zero readings.

**Error state:** one layer's fetch failure shows an error icon on that layer's toggle and a dismissible inline note; the rest of the map and other layers are unaffected.

**Mobile behavior:** layer controls become a bottom sheet (swipe up); time scrub becomes a compact horizontal slider; tapping a point opens the evidence popover as a full-screen card rather than a small floating popover.

---

## 3. Ask ORCA Interface

**Purpose:** natural-language entry point into the agent pipeline (`POST /query`) for questions the dashboard/map don't directly answer.
**User:** all roles; reachable via a persistent icon, not the app's main view.

**Components:** single input field with location-aware suggested prompts; response renders as one structured **answer card** (not a chat bubble): headline answer text, confidence badge, citation chips, contributing-agent icon row, "view reasoning" link; follow-up input stays available below the card.

**Information hierarchy:** question restated briefly at top of the card; answer text and confidence badge are the visual anchor; citation chips and agent icons sit below, clearly secondary; "view full reasoning" is a single link, not inline clutter.

**Interactions:** submit → triggers pipeline call, opens live Agent Activity Panel (§4) inline while waiting; click a citation chip → Evidence Panel (§5) filtered to that claim; click an agent icon → that agent's detail in §4; follow-up questions retain `conversation_context`.

**Loading state:** the Agent Activity Panel (§4) renders live and *is* the loading state — the user watches which agents are running, not a generic spinner.

**Empty state:** no query yet → 3–4 example prompts relevant to the user's current location and mode (e.g., Fisher mode suggests "Is it safe to fish today?").

**Error state:** pipeline timeout or failure surfaces the actual `blocked_reason`/error in plain language ("Unable to confirm current safety status — a required data source is unreachable") with a retry action — never a fabricated-sounding answer in its place.

**Mobile behavior:** full-screen input on open; answer card is the primary scrollable view; a sticky "Ask a follow-up" bar stays at the bottom.

---

## 4. Agent Activity Panel

**Purpose:** transparency into which agents ran for a given query, their status, and timing — live during execution, and reviewable afterward.
**User:** primarily Scientist and Government modes (trust-building, auditability); collapsible/secondary in Fisher mode.

**Components:** one row per invoked agent (icon, name, status, latency); rows grouped/indented to show parallel vs. sequential execution per the dependency graph; expandable row reveals that agent's raw envelope (`observations`, `confidence`, `warnings`, `errors`).

**Information hierarchy:** overall pipeline status (running / complete / partial / failed) at the top; agent rows below in execution order, visually grouped by parallel batch.

**Interactions:** click a row to expand its detail; hover a status icon for a one-line tooltip; click through to Evidence Panel (§5) from within an expanded row.

**Loading state:** the currently-running agent's row shows an animated pulse; completed rows show a static status icon; not-yet-started rows are dimmed/greyed, never blank.

**Empty state:** before any query has been run in the session, the panel shows a short explanatory placeholder ("Agent activity for your next question will appear here").

**Error state:** a failed agent's row turns to the red/error treatment with its specific error code and the fallback behavior that was applied (per `AGENT_CONTRACTS.md` FALLBACK), so the user sees *what* happened, not just that something did.

**Mobile behavior:** collapses by default to a compact horizontal status strip (e.g., 8 small dots colored by status); tapping expands the full list as a bottom sheet.

---

## 5. Evidence Panel

**Purpose:** drill-down view of the Evidence Grounding Records backing a specific claim, recommendation, or agent output.
**User:** all roles; especially load-bearing for Scientist and Government trust.

**Components:** list of evidence cards, each showing source, dataset, parameter, value + unit, location, `observed_at`, a quality badge (verified/provisional/estimated/flagged), retrieval-method icon, and reliability tier indicator.

**Information hierarchy:** grouped by the claim they support; within a group, sorted by reliability tier then recency, so the strongest evidence is seen first.

**Interactions:** click a card to open the source link/detail where available; filter by quality tier; sort by recency vs. reliability.

**Loading state:** skeleton list matching the expected card count where known, otherwise a generic 3-card skeleton.

**Empty state:** genuinely rare by design (a claim without evidence should have been blocked upstream per the Recommendation gate) — if it occurs, it's shown as a **prominent flagged state**, not a quiet blank list: "No evidence found for this claim — this should not normally happen; please report."

**Error state:** evidence fetch failure shows an inline retry control; citations already rendered elsewhere in the UI are never silently dropped because this panel failed to load.

**Mobile behavior:** opens as a full-screen slide-over rather than a side panel.

---

## 6. Recommendation Panel

**Purpose:** display the Coordinator's final gated output — a recommendation, or an explicit blocked state — with safety override always visually dominant when active.
**User:** all roles; the single most important screen for Fisher mode.

**Components:** verdict badge (`Recommended` / `Caution` / `Blocked` / `Dangerous`); recommendation text or `blocked_reason`; confidence badge (§7); safety-override banner (only rendered when `safety_override_active = true`); secondary context block (e.g., Fisheries season/quota status) visually separated and labeled "context, not the verdict"; link to full reasoning (§8).

**Information hierarchy:** safety-override banner, if present, is full-width, red, and above everything else on the screen — it cannot be scrolled past unnoticed; verdict badge and text second; confidence third; secondary domain context clearly demarcated last, so it's never mistaken for the safety verdict itself.

**Interactions:** expand "Why?" → Explainable Reasoning Graph (§8); share/export the recommendation; acknowledge an alert (marks read, never dismisses an active safety banner).

**Loading state:** skeleton card with a neutral gray placeholder badge — **never** a default green/safe badge while the real verdict is still being computed.

**Empty state:** when the gate blocked a recommendation, this *is* the state shown — clear `blocked_reason` text, not a blank panel implying nothing happened.

**Error state:** verification failure shows explicit "unable to verify — treat with caution" messaging and, where relevant, points to official/authoritative alternate sources (e.g., coast guard channel).

**Mobile behavior:** card layout; the safety banner becomes sticky at the top of the viewport as the user scrolls the rest of the card.

---

## 7. Confidence / Uncertainty Visualization

**Purpose:** one consistent visual language for confidence, used identically everywhere a claim appears across the whole product.
**User:** all roles.

**Components:** a fixed badge component — icon + label (High/Medium/Low) + color — always adjacent to the claim it qualifies; on tap/hover, a basis tooltip explains *why* ("single stale model source," "active verified advisory"); degrade indicators (small stale-data clock icon, conflict-triangle icon) attach to the same badge when relevant.

**Information hierarchy:** the badge is never detached from its claim — it does not live in a separate "confidence summary" area divorced from context.

**Interactions:** tap/hover → basis tooltip; tap "why" within the tooltip → Evidence Panel (§5) for the underlying records.

**Loading state:** neutral gray placeholder badge with no label — the system never guesses a confidence level to fill the gap while computing.

**Empty state:** not applicable — this component only ever renders paired with a claim.

**Error state:** if confidence computation itself fails, the badge explicitly reads "Confidence unavailable" rather than being omitted (an omitted badge would be indistinguishable from forgetting to render one).

**Mobile behavior:** compact badge (icon + color only) with tap-to-expand for the label and tooltip.

---

## 8. Explainable Reasoning Graph

**Purpose:** visualize the actual reasoning pipeline (`REASONING_FRAMEWORK.md` §1) that produced a specific answer — a node-link trace from Intent Detection through Recommendation, including where conflicts or evidence gaps occurred.
**User:** primarily Scientist and Government modes; available to Fisher mode as an optional "show me why" link, not a default view.

**Components:** node-link graph, one node per pipeline stage (Intent Detection → Query Decomposition → Agent Selection → Data Retrieval → Evidence Collection → Scientific Interpretation → Cross-Agent Reasoning → Conflict Detection → Verification → Confidence Estimation → Recommendation → Explanation); nodes colored by status (ok/warning/blocked); an optional overlay toggle labeling each node as "deterministic" or "LLM reasoning" (directly surfacing `REASONING_FRAMEWORK.md` §3's matrix).

**Information hierarchy:** left-to-right (or top-to-bottom on narrow screens) flow matching pipeline order; any conflict/blocked node is visually distinct (red outline) so it draws the eye without needing the overlay toggle.

**Interactions:** click a node → side panel with that stage's actual data (e.g., clicking "Evidence Collection" shows the evidence pool); zoom/pan for dense graphs; toggle the deterministic/LLM overlay.

**Loading state:** during a live query, nodes appear progressively as each pipeline stage actually completes — the graph *is* a live progress indicator, not just a post-hoc diagram.

**Empty state:** for older queries where a full trace wasn't retained, an explanatory message replaces the graph: "Detailed reasoning trace is not available for this result."

**Error state:** a broken/incomplete trace renders the stages that are available with an explicit gap marker at the missing stage, rather than failing to render anything.

**Mobile behavior:** the full node-link graph is replaced with a simplified vertical timeline/stepper (too dense to render meaningfully on a small screen) — tapping a step expands its detail inline.

---

## 9. Historical Comparison

**Purpose:** compare current conditions or a current recommendation against a historical baseline or a prior period.
**User:** primarily Scientist and Government modes.

**Components:** two period selectors; comparison charts (line/bar) per selected parameter; headline delta indicators (e.g., "+1.8°C vs. 10-year baseline"); optional side-by-side or swipe map comparison.

**Information hierarchy:** headline deltas at the top; supporting charts below; map comparison last, since it's the heaviest element.

**Interactions:** select two periods and a parameter set; toggle chart vs. map comparison view; export the comparison.

**Loading state:** chart-shaped skeletons per selected parameter.

**Empty state:** insufficient historical data for the selected range shows an explicit note plus the actual available range as a suggestion, not a blank chart.

**Error state:** a data gap in one period renders as a visible gap in the chart (broken line, not interpolated) — the system never fills a hole with a fabricated smooth trend.

**Mobile behavior:** side-by-side becomes a swipeable before/after card pair instead of two panels at once.

---

## 10. What-If Analysis

**Purpose:** constrained scenario exploration — re-running the pipeline against an adjusted location, date, or activity type — explicitly framed as a new evidence-grounded query, not a freeform simulation beyond what the data supports.
**User:** Scientist and Government modes for full parameter control; Fisher mode gets a simplified version (e.g., "What about tomorrow?").

**Components:** parameter adjustment controls (location shift, date shift, activity type selector); "Run scenario" action; baseline-vs-scenario comparison view reusing the Recommendation Panel (§6) layout for each side.

**Information hierarchy:** controls at top/side; the two recommendation results shown side by side, each clearly labeled ("Current" vs. "Scenario"), with confidence badges on both so a user can see if the scenario is *less* well-evidenced than the baseline.

**Interactions:** adjust controls → triggers a fresh `/query` call scoped to the new parameters; compare the two resulting confidence levels and verdicts directly.

**Loading state:** identical to Ask ORCA's live Agent Activity Panel (§4) — a what-if run is a real pipeline run, not a shortcut, and its loading state should look like one.

**Empty state:** no scenario run yet → guided example scenarios relevant to the user's last real query.

**Error state:** a failed scenario run gets the same explicit `blocked_reason` treatment as any other query — a hypothetical answer is never fabricated to fill a failed scenario.

**Mobile behavior:** multi-slider control panel becomes a simplified step-by-step wizard (one control per screen) rather than a dense simultaneous panel.

---

## 11. Alerts

**Purpose:** proactively surface active safety, regulatory, and ecological advisories for the user's regions of interest.
**User:** all roles; especially critical for Fisher and Government modes.

**Components:** alert feed list; severity badges; map pins per alert region; region subscription controls; an emergency-escalation info block (contact info per Safety Agent's `emergency_escalation` field) attached to any `DANGEROUS`-severity alert.

**Information hierarchy:** `DANGEROUS`-severity alerts are pinned to the top regardless of recency; below that, sorted by severity then recency.

**Interactions:** click an alert → jumps to Map (§2) centered on the affected region plus the relevant Recommendation Panel context; subscribe/unsubscribe per region; "mark read" only changes read state, it never dismisses or hides an active safety-critical alert from the feed.

**Loading state:** skeleton list rows.

**Empty state:** "No active advisories for your regions" — a calm, explicitly reassuring state (not just an empty list, which could be mistaken for a loading failure).

**Error state:** if the advisory feed itself can't be confirmed, the panel shows a prominent banner — "Unable to confirm current advisory status" — and never silently falls back to an empty list that could be misread as "all clear" (directly matching Safety Agent's fallback rule in `AGENT_CONTRACTS.md`).

**Mobile behavior:** rendered like a notification feed at the top level of the app; `DANGEROUS` alerts trigger a native push notification where permitted.

---

## 12. Scientist Mode

**Purpose:** a role configuration maximizing data depth, raw evidence, and analytical tooling.
**User:** researchers and marine scientists.

**Components:** Dashboard defaults to a dense multi-metric grid; Evidence Panel and Reasoning Graph are expanded by default rather than tucked behind a link; raw data export (CSV/JSON) on any chart or table; unit system toggle; dataset provenance always visible inline, not just on drill-down.

**Information hierarchy:** technical precision over simplicity — actual parameter names (`chlorophyll_a`, not "algae level"), full-precision values, explicit dataset/model names shown by default.

**Interactions:** bulk export; direct links to source datasets; read-only view of the statistical thresholds actually used (from `REASONING_FRAMEWORK.md` §5), so a scientist can audit the classification logic, not just trust it.

**Loading / Empty / Error states:** identical underlying components to the base screens above — Scientist Mode changes default panel configuration and density, not the state-handling behavior itself.

**Mobile behavior:** available on mobile, but the dense grid degrades to a tabbed layout (one metric group per tab) rather than trying to compress the full grid.

---

## 13. Fisher Mode

**Purpose:** a simplified, safety-first, high-contrast interface for people making a go/no-go decision, often outdoors, on a phone, sometimes with poor connectivity.
**User:** recreational and commercial fishers.

**Components:** large, unmissable safety-status banner as the very first thing shown; Recommendation Panel defaults to plain-language summary view; simplified map showing only PFZ zones and active advisories by default (other layers available but not shown by default); large touch targets; an explicit "last known safe state" indicator for offline/poor-connectivity use.

**Information hierarchy:** safety status first and largest, always; fisheries season/quota status second; everything else (evidence detail, reasoning graph, historical data) collapsed behind a single "More details" action.

**Interactions:** minimum taps to reach a safety answer from app open; plain-language summary shown by default with a toggle to reveal the underlying technical/evidence detail for anyone who wants it — technical detail is never removed, just deferred.

**Loading state:** optimized for slow connections — plain-language status text renders before map tiles finish loading, so the most important information arrives first.

**Empty state:** no location set yet → a single prompt asking for GPS permission or manual location entry, framed around "Get your local conditions."

**Error state:** connectivity failure shows the last cached safety status with an explicit, prominent "Last updated X ago — may be outdated" warning — stale data is never presented as current, matching the Safety Agent's core rule.

**Mobile behavior:** this mode **is** the primary mobile-first design target — it is the default mode on mobile unless the user has explicitly selected another.

---

## 14. Government Mode

**Purpose:** regional/jurisdiction-level oversight — monitoring across multiple zones, policy-relevant reporting, and audit access.
**User:** fisheries department officials, regulators, disaster-management coordinators.

**Components:** multi-region summary dashboard (active advisory count, active PFZ count, compliance flags per jurisdiction); aggregate map across the full jurisdiction; regulation/compliance reference panel; report export (PDF/CSV); audit trail access into `recommendations` and `verification_verdict` history across the region; alert-broadcast tooling (where in scope) for pushing advisories to registered users.

**Information hierarchy:** jurisdiction-wide summary at the top; region drill-down map second (reusing §2's Map component scoped to the jurisdiction); reporting/export tools accessible but visually secondary to the live status view.

**Interactions:** select a jurisdiction/region to drill down (reuses Dashboard/Map for that specific location); generate a report; review the verification/conflict audit trail for a given time window.

**Loading state:** skeleton summary cards plus a loading map, same pattern as the base Dashboard.

**Empty state:** no active advisories/PFZ in the jurisdiction → a reassurance state that explicitly distinguishes "no danger currently detected" from "no data available" (these must never be visually conflated, per `EVIDENCE_AND_CONFLICT_FRAMEWORK.md` §B.6's missing-data rule).

**Error state:** a partial aggregate-data failure names exactly which sub-regions failed to load, rather than showing an aggregate number that silently excludes them.

**Mobile behavior:** collapses to a summary-only view; the full multi-region aggregate tooling (broadcast, detailed audit trail) is deferred to desktop/tablet, where the information density genuinely requires the extra screen real estate.

---

## Summary: Cross-Screen Consistency Rules

- The confidence badge (§7) and evidence citation pattern (§5) render **identically** wherever they appear — Dashboard, Map popovers, Ask ORCA, Recommendation Panel — so a user only has to learn what they mean once.
- A safety override (§6, §11) is **always** the visually dominant element on any screen where it's relevant, regardless of what else that screen is showing.
- No screen ever shows a positive/reassuring default state while data is still loading — loading states are neutral, never optimistic.
- No screen ever silently substitutes "empty" for "unavailable" — the distinction between "we checked and there's nothing" and "we couldn't check" is preserved visually everywhere in the product, not just in Alerts and Government Mode where it's spelled out explicitly above.