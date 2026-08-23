# AgentFail — full read, 2026-08-23

Read in full: §3–§4 of arXiv 2509.23735 v2 and the Figure 4 taxonomy image
(the only place all sixteen root causes are listed; the text names ten).
Dataset: https://github.com/Jenna-Ma/JaWs-AgentFail (not yet mined for
`examples`; it should be — 307 real failures with root location + cause).

**What it is.** 307 failures from platform-orchestrated multi-agent workflows
(Coze, Dify). Each is annotated with a *root location* (node) and a
*root cause* from a **repair-oriented** taxonomy: agent-level (7), structure-
level (7), platform-level (2). Attribution uses re-rollout counterfactuals
(replace a node's output with a corrected one; earliest node whose fix flips
the outcome is the root). 32% of failures surface at a different node than
their root.

**Because these are causes, not symptoms, almost everything maps `overlaps`.**
The exceptions: F1.4 Knowledge or Reasoning Limitation → AF-0125 `exact`
(repair = model upgrade/augmentation, AF-0125's third symptom); F3.1/F3.2 →
AF-0170 `broader`.

| code | name | n | mapping |
|---|---|---|---|
| F1.1 | Tool or Action Planning Error | 7 | AF-0157, AF-0088 overlaps |
| F1.2 | Response Format Error | 28 | AF-0023 overlaps (consumer-side invalid-invocation shape); no mode for malformed inter-node output |
| F1.3 | Response Content Deviation | 47 | AF-0153, AF-0088 overlaps |
| F1.4 | Knowledge or Reasoning Limitation | 55 | AF-0125 exact |
| F1.5 | Poor Prompt Design | 52 | AF-0103 overlaps + **GAP** (cause-level; same thing as Agent-Xray `prompt_bug`; may not belong in a symptom registry — flagged to decide) |
| F1.6 | Language or Encoding Issue | 15 | `[]` borderline scope |
| F1.7 | Tool Invocation or KB Retrieval Error | 9 | AF-0023, AF-0149 overlaps |
| F2.1 | Missing Input Verification | 15 | AF-0042 overlaps |
| F2.2 | Unreasonable Node Dependency | 17 | AF-0071, AF-0088 overlaps |
| F2.3 | Loops and Deadlocks | 3 | AF-0058 overlaps (orchestration-graph loop) |
| F2.4 | Faulty Conditional Judgment | 11 | AF-0088 overlaps |
| F2.5 | Improper Task Decomposition | 6 | AF-0071, AF-0088 overlaps |
| F2.6 | Context Conflict | 8 | AF-0071 overlaps |
| F2.7 | Cross-agent tool or interface mismatch | 11 | AF-0071, AF-0149 overlaps |
| F3.1 | Network and Resource Fluctuation | 13 | AF-0170 broader, AF-0136 overlaps |
| F3.2 | Service Unavailability | 10 | AF-0170 broader |

Third independent source for AF-0170 (with AgentRx System Failure and
Model-or-Harness Service Failure) and for AF-0157 (with Agent-Xray and
Model-or-Harness).
