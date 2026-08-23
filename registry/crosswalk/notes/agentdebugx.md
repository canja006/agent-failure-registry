# AgentDebugX — full read, 2026-08-23

Read in full: `src/agentdebug/schema/taxonomy.py` (the 19-mode seed failure
taxonomy), `src/agentdebug/hub/bundle.py` (BundleManifest schema), and the
README, at `main` (last push 2026-08-21).

**What it is.** A local-first debugging framework: Diagnose = Detect →
Attribute → Recover, then Rerun validates the fix. The Detect stage
classifies into a **seed taxonomy of 19 failure modes** in 8 families
(memory 2, reflection 2, planning 3, action 4, system 3, multiagent 2,
verification 2, multimodal 1). Each seed mode carries stable dotted ids
(`memory.retrieval_failure`), textual signals, repair suggestions, and a
`source` citation — AgentDebug, MAST, Who&When, AgentRx, AgentSight — so the
taxonomy already crosswalks informally, which is the strongest possible sign
the maintainers think in exactly the terms AFR provides.

**Induction.** The seed set is "designed to be extended by generated,
project-specific taxonomy nodes" (taxonomy induction). Only the seed modes
are mapped; induced nodes are per-project and unmappable by definition. The
crosswalk should be re-checked against the seed set on each release.

**Error Hub.** `BundleManifest` already carries
`failure_mode_ids: List[str]` (plus `failure_families`,
`root_cause_step_index`, `root_cause_agent`, CC-BY-4.0 license, opt-in
contributor). Consequence for the outreach ask: **no schema change is needed
for bundles to interoperate with AF ids** — an AF id is derivable from
`failure_mode_ids` via the crosswalk. The issue was rewritten around that.

**Mapping highlights.**
- `memory.retrieval_failure` is the second independent source (with
  Model-or-Harness "Missed Read" / "Memory Following Failure") for the
  memory-read gap → **AF-0174 "Stored memory unused"** written from the pair.
- The three `action.*` invocation slices (invalid_action, format_error,
  parameter_error) are each finer than AF-0023 → AF-0023 `broader` ×3.
- `system.tool_execution_error` and `system.llm_limit` are deliberate
  catch-alls → AF splits them (AF-0149/0170 and AF-0125/0064/0130/0095).
- `action.wrong_tool`'s signal list includes "unknown tool", blurring
  AF-0157 into AF-0011 → overlaps to both, not exact.
- Remaining GAPs (single source): `reflection.causal_misattribution`,
  `multiagent.role_drift`, `multimodal.perception_error` (non-text
  perception; AF-0042 nearest).
