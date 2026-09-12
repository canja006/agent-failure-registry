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

## Second read, 2026-09-12 — v0.5.2, 23 modes

Prompted by the maintainers on issue #7: the seed set had grown to 23 and the
crosswalk still described 19. Re-read `src/agentdebug/schema/taxonomy.py` at
tag **v0.5.2** (`e180ac2`) and pinned this file to that tag rather than `main`
— they asked that integrations pin the taxonomy revision, and the first read
going stale in three weeks is the argument for it.

**What changed.** One new family, `observation` (4 modes), adapted from
TrajDebug's `obs` module (THU-KEG/TrajDebug, MIT). The module comment states
the reasoning plainly: reading environment and tool feedback wrongly had no
home, `memory.retrieval_failure` is failing to *retrieve* rather than
misreading what was retrieved, and `multimodal.perception_error` is images, UI
and audio only.

**The family is finer than AF-0042.** AF-0042 "Tool output misread" was
written from AgentRx and ToolFailBench, where the unit of analysis is a tool
call. This family splits that surface four ways — misread, ignored, wrongly
bound, read too early — and widens it from tool output to environment
observations. So three of the four cite AF-0042, and none of them `exact`:

- `observation.misread` → AF-0042 `overlaps`. Neither contains the other:
  AF-0042 is tool-scoped where this also covers environment observations, and
  AF-0042 still spans reading a truncated result as complete, which this
  taxonomy splits out as `observation.timing`.
- `observation.timing` → AF-0042 `overlaps`. Truncated-read-as-complete is one
  slice of it; a pending or not-yet-settled response that is not truncated has
  no AF mode.
- `observation.grounding_fail` → **GAP**, single source. The value is read
  correctly and bound to the wrong entity, element or field. AF-0042 is the
  nearest and is not it: nothing was misinterpreted.

**`observation.ignored` produced a mode.** It is the second independent source,
with ToolFailBench's `Result-Ignore`, for an observation that was returned and
then not used — the same pairing rule that produced AF-0174 from
`memory.retrieval_failure` and Model-or-Harness "Missed Read". Written as
**AF-0178 "Returned observation unused"**, and `Result-Ignore` re-pointed onto
it from AF-0042 (`broader`, its single-turn slice). AF-0042 keeps what its
title says: a return that was read and misinterpreted. AF-0178 is the return
that never entered the decision, which is a different repair.

That also answers, in one direction, the maintainers' point that several AF
modes landing on one category makes automatic comparison hard: where the
pressure came from AF being *coarser* than the source, the fix was to split AF,
not to add a fourth citation to AF-0042.
