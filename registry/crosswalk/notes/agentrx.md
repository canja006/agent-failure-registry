# AgentRx — full read, 2026-08-23

Read in full: `agentrx/judge/judge.py` `TAXONOMY_DATA` (the operative
definitions, with per-category checklists the judge is prompted with) and the
judge prompt templates, at `main` (last push 2026-06-22); the paper
(arXiv 2602.02475 v1) §2–2.2, §3.4, §6; and both ground-truth files
(`data/ground_truth/{magentic_one,tau}_ground_truth.json`, 44 + 29
trajectories). `taxonomy_size: 10` confirmed (9 categories + Inconclusive).

## How the label is assigned (matters for profiles)

One label per trajectory: the category of the **first unrecoverable** failure
("critical failure"), found by scanning forward and asking whether each
failure was later recovered from. Every failure event is also labelled in the
ground truth, but the reported root cause is one per run. The judge is an LLM
shown the definitions + checklists (+ optional invariant-violation log); there
is no detector code. `Inconclusive` requires a free-text `custom_category`, so
AgentRx output can carry labels outside the ten.

Ground-truth root-cause distribution (Magentic 44 / τ-bench 29):
Misinterpretation 15/7, Guardrails 9/0, Plan Adherence 8/3, Invention 4/0,
Intent-Plan 4/7, Underspecified 0/8, Intent Not Supported 3/2, System 1/1,
Invalid Invocation 0/1. Across *all* Magentic failure events Plan Adherence is
197 of ~295 — the workhorse bucket.

## Per-category: operative definition, current mapping, verdict

| category | what the checklist actually requires | was | verdict |
|---|---|---|---|
| Instruction/Plan Adherence Failure | **Goal is correct** (checklist Q1 excludes solving the wrong problem), info was available, and the agent skipped / reordered / added a step required by the plan, domain policy or orchestrator. Under- and over-execution. | AF-0077 narrower, AF-0088 overlaps | **Drop AF-0088** — the checklist defines this category as *not* intent misalignment. Keep AF-0077 narrower (stopping early is one kind of under-execution). **GAP:** "required step skipped / plan or policy deviated from with correct goal" — the most common failure event in AgentRx's own data — has no AF mode. |
| Invention of New Information | Pinpointable invented / altered / **omitted** claim, absent from all evidence, relied on for an action. Examples in GT: hallucinated file path, invented language operator, "hallucinated successful download". | AF-0011 narrower | Hold AF-0011 narrower; promote the existing note to **GAP:** fabricated facts / claims about state. |
| Invalid Invocation | Explicit parse / validation / schema / syntax error for a concrete call; NOT infra, NOT access block. | AF-0023 exact | Hold. |
| Misinterpretation of Tool Output (judge name: "… / Handoff Failure") | Reasoning derived from own **or another agent's** output contradicts it, omits a crucial part, or is a computation/logic error on it. 15/44 Magentic root causes are "Orchestrator misread WebSurfer's incomplete output". | AF-0042 exact | **AF-0042 → narrower** (category also covers handoff misreads) **+ AF-0071 overlaps** (parent misusing a sub-agent's result is AF-0071's third symptom). Category string kept as the README/GT spelling; judge alias noted. |
| Intent-Plan Misalignment | Optimises a different goal or violates a key constraint **because of misunderstanding** (not missing info, not a tool error). | AF-0088 exact | Hold. |
| Underspecified User Intent | A specific required piece of information is absent from all evidence; agent proceeded without it or failed to ask. | AF-0103 exact | Hold; note that AgentRx also counts "proceeded without it", AF-0103 emphasises "picked a reading silently" — same failure seen from two sides. |
| Intent Not Supported | Requested action needs a capability no available tool provides; not infra. In Magentic the requester is often the **Orchestrator** asking FileSurfer for audio/PDF. | AF-0007 exact | Hold; note the multi-agent reading (orchestrator-as-user) which brushes AF-0071. |
| Guardrails Triggered | Explicit refusal/block: **RAI/safety policy refusal** *or* **external site access restriction** (CAPTCHA, login wall, 403, paywall, robots.txt, automation forbidden); plan would be fine without the block. | AF-0095 exact | **AF-0095 → narrower.** AF-0095 is the harness's own policy / approval gate; the external-access half is an environment-layer block with **no AF mode — GAP**. 9/44 Magentic root causes sit here, a mix of Azure RAI filters and Cloudflare/CAPTCHA. |
| System Failure | Explicit infra / connectivity signal during a tool call: timeout, connection refused, DNS failure, endpoint unreachable, service unavailable, premature termination; NOT malformed args. GT: "Orchestrator did not respond … abrupt termination", "unexpected system error". | AF-0064, AF-0130, AF-0136 narrower | **Drop AF-0064** — context truncation is nowhere in the definition or checklist. Keep AF-0136 and AF-0130 narrower, **add AF-0149 narrower** (5xx / internal tool error is in its symptoms). **GAP:** pure connectivity failure (DNS / refused / unreachable) has no AF mode. |
| Inconclusive | None of 1–9; must supply a custom category. | `[]` | Hold — residual. |

## Gaps AgentRx surfaces

1. **Required step skipped / plan or policy deviation with correct goal** — the
   single most common failure event in the corpus. Distinct from AF-0088
   (wrong goal) and AF-0077 (stopped). Model layer.
2. **Fabricated fact or claim about state** — AF-0011 covers only fabricated
   tool/parameter schemas. Model layer.
3. **External access block** — CAPTCHA / 403 / paywall / robots.txt / login
   wall. Environment layer; sibling of AF-0095 (harness policy).
4. **Connectivity failure** — DNS / connection refused / endpoint unreachable.
   Environment layer; sibling of AF-0149 (tool's own defect) and AF-0136.

Together with Agent-Xray's two (tool-not-exposed, wrong-tool-selected) the
registry now has six recorded gaps. Several will recur in the academic
taxonomies; write the modes once two independent sources name the same thing
rather than one per vendor category.
