# Model or Harness? — full read, 2026-08-23

Read in full: §3 (mechanism axis), §4 (methodology), §5 (failure families),
Appendix B (verbatim definitions) of arXiv 2607.28802 v1.

**What it is.** An interaction-centric taxonomy: every failure is an
*edge* (model ↔ owner / grader / third party / context / memory / tool /
peer / subagent / external environment / local environment) plus a
*fault side*. 41 role-specific failure modes; 36 are model-side, 5 are
other-side (Instruction–Grader Mismatch → owner; Context Rationale Erosion →
context/harness; Mistranslation → tool; Service Failure and Stale State
Delivery → environment). Root-cause rule: first unrecovered failure, citing
AgentRx. The example set is illustrative, not prevalence. Names that recur
across edges are qualified in the crosswalk: Delegation/Communication
Failure (peer | subagent), Recovery Failure (external | local environment).

## Direct hits on existing modes

| theirs | ours | relation |
|---|---|---|
| Tool Hallucination | AF-0011 | exact |
| Malformed Arguments | AF-0023 | exact |
| State Tracking Failure | AF-0058 (AF-0049, AF-0142 as sub-cases) | exact / narrower |
| Context Rationale Erosion | AF-0064 | exact |
| Satisficing | AF-0077 (+AF-0086 overlaps) | exact |
| Incorrect Tool Selection | AF-0157 | exact |
| Service Failure | AF-0170 (+AF-0130 narrower) | exact |
| Tool Feedback Neglect | AF-0042 | broader |
| Mistranslation | AF-0149 | broader |
| Domain Knowledge Deficit | AF-0125 | broader |
| Delegation/Communication Failure (subagent) | AF-0071 | broader |

State Tracking Failure is the first external source for **AF-0142** (stale
context re-read), which had been the registry's only orphan.

## Layer cross-check — flagged, not changed

The paper's principle: *the fault side is the component that could have acted
correctly on the information it had.* Applied to AFR's `layer`:

| AF | AFR layer | paper's side | verdict |
|---|---|---|---|
| AF-0058 Unproductive repetition | harness | model (State Tracking) | **disagree** |
| AF-0049 Test failure loop | harness | model (State Tracking) | **disagree** |
| AF-0142 Stale context re-read | harness | model (State Tracking) | **disagree** |
| AF-0071 Delegation failure | harness | model (Delegation/Communication) | **disagree** |
| AF-0086 Insufficient sources | harness | model (Satisficing) | **disagree** |
| AF-0064 Context overflow truncation | harness | context/harness (when harness-driven) | agree |
| AF-0023 / 0011 / 0042 / 0077 / 0088 / 0125 | model | model | agree |
| AF-0118 / 0130 | environment | environment | agree |
| AF-0149 Tool defect | tool | tool (Mistranslation) | agree |

The five disagreements share a shape: AFR put "the harness should have caught
this" failures on the harness; the paper puts them on the model because *the
information to avoid them was in context*. The SCHEMA calls layer "the most
contested judgement in this space" and deliberately keeps it separate from
the id, so this is a maintainer decision. **Adopted 2026-08-23**: the five
moved to `model`, and the principle is now stated in SCHEMA.md — it is the
only principled rule either side has written down, and it makes AFR's
`by layer` profile line comparable with a published taxonomy.

## Gaps this paper records (single source, so recorded, not filled)

Memory family (8 modes — AFR has no memory edge at all); Unauthorized
Irreversible Action; Sycophancy; Contextual Sycophancy; Indirect Prompt
Injection; Specification Gaming; Goal Drift; Suboptimal Arguments;
Over-/Under-initiative; Stale State Delivery; Recovery Failure (named three
times across edges — the strongest single-source candidate). Evaluation
Awareness and Value Misalignment are left empty but *not* GAP: the first is
not trajectory-observable by the paper's own account, the second is outside a
symptom registry's scope.
