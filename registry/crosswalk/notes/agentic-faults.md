# Characterizing Faults in Agentic AI — full read, 2026-08-23

Read in full: §3.1.1–3.1.3 of arXiv 2603.06847 v1 (fault-type, symptom and
root-cause taxonomies).

**What it is — and what it is not.** 385 faults stratified-sampled from
13,602 GitHub issues and PRs across 40 agent *framework* repositories
(autogen, langflow, haystack, crewAI, letta, MetaGPT, …). The unit is a
**software defect in a framework**, classified by grounded theory into 34
fault types / 14 categories / 4 dimensions, plus 12 developer-facing
symptoms and 12 root causes. The largest category is Dependency &
Environment Management (72); others include Platform Compatibility, UI
Defects, Documentation Issues.

This is not a taxonomy of trajectory-observable agent failures, and the
registry must not treat it as one. Mapping it wholesale would either invent
modes for "documentation bug" or force framework defects onto behavioural
modes. The file therefore:

- maps only the **five categories with a runtime manifestation** — LLM
  Interaction Faults (context overflow, redundant invocation), Agent Lifecycle
  & State (skipped tasks, loops, termination), Tool Invocation, External
  Access, Failure Handling & Robustness — all `overlaps`, none `exact`;
- leaves the other nine empty with an *out-of-scope* note, **not** `GAP`.

Coverage for this source (36%) is therefore low by design; it is a scoping
statement, not a to-do list.

**Worth keeping from it.** The "Agent Behaviour Anomalies" symptom — repeated
reasoning steps, role violations, loss of conversational context,
coordination breakdowns — is a good developer-facing description of the
cluster AF-0058 / AF-0064 / AF-0071 form. And "Data Schema Mismatch" (its
largest root cause, 28%) is the same shape as AgentFail F1.2 Response Format
Error: two sources for *malformed structured output between components*,
which AFR does not name — recorded here, not as a GAP, because both sources
describe it at the framework/pipeline level rather than as agent behaviour.
