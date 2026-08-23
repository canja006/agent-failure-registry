# ToolFailBench — full read, 2026-08-23

Read in full: §3 (benchmark design, failure-mode taxonomy, metrics/detection)
and Appendices C–D of arXiv 2607.04686 v1.

**What it is.** 1,000 single-turn tasks in finance, medicine, law,
cybersecurity, real estate. 750 are tool-required *parametric traps* — the
mock tool return deliberately contradicts a plausible memorised value, so the
final answer reveals whether the model trusted the tool. 250 are control tasks
where no tool is needed. Each trace gets **one label within its task type**;
the label is a majority vote of a deterministic rule classifier and two LLM
judges (Qwen3.5-397B-A17B, GLM-4.7), ties to the rule classifier.

**Labels (taxonomy_size 5; "Correct" is not mapped).**

| label | set | operational definition | mapping |
|---|---|---|---|
| Tool-Skip | required | no valid executed tool call; includes tool-style answers ("Per <tool>…") with no call (App. D.1) | AF-0153 broader |
| Result-Ignore | required | called; final answer omits the returned value | AF-0042 broader |
| Output-Fabrication | required | called; answer adds invented structured information not in the return | AF-0161 broader |
| Unnecessary-Tool-Use | control | called a tool anyway | AF-0166 broader |
| Wrong-Answer | control | no tool, wrong answer — parametric knowledge error | `[]` not a tool-use failure |

Agreement (Table 8): TS κ .78, RI .53, OF .60, UTU .23 (rare; raw .95).

**Why it matters for AFR.** It is the second independent source for three of
the gaps recorded from AgentRx/Agent-Xray, which is what let AF-0153, AF-0161
and AF-0166 be written. Its labels are all `broader` from the AF side because
each is a tightly scoped single-turn slice of a general mode.

App. D.2 excludes an invalid-raw-token run as "a harness or formatting issue"
— not a category, but a reminder that harness defects are filtered out before
this taxonomy applies.
