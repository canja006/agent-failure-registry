# Agent-Xray — full read, 2026-08-23

Read in full: `src/agent_xray/root_cause.py` (1,425 lines) and the
`ERROR_PATTERNS` / `_max_consecutive_repeat` / `analyze_task` sections of
`src/agent_xray/analyzer.py`, at `main` (last push 2026-04-05). This is the
evidence behind `registry/crosswalk/agent-xray.yaml`; the README table alone
was not enough, because several categories' *descriptions* and *detectors*
diverge. `taxonomy_size: 22` confirmed against `ROOT_CAUSES`.

## How the classifier works (matters for profiles)

Every classifier runs; the **primary** root cause is the first match in a
fixed order, the rest go to `also_matched`. Order:

```
routing_bug, approval_block, spin, delegation_failure, test_failure_loop,
tool_rejection_mismatch, error_dominance (-> environment_drift | tool_bug),
rate_limit_cascade, insufficient_sources, valid_alternative_path,
consultative_success, tool_selection_bug (search bias), memory_overload,
context_overflow, prompt_bug, model_limit, stuck_loop, early_abort,
reasoning_bug, tool_selection_bug (low diversity), timeout
```

Consequences: `spin` beats `stuck_loop` whenever both fire; `model_limit`
(>50 steps, <2 URLs) beats `stuck_loop` (>=5 steps, <=1 URL) — the two are the
same signal at different thresholds, so an Agent-Xray profile's AF-0125 vs
AF-0058 split is partly a step-count artefact. `prompt_bug` is also the
fallback when nothing else matches but a prompt-section pattern does.

## Per-category: detector, current mapping, verdict

| category | what actually fires | current | verdict |
|---|---|---|---|
| `spin` | longest **consecutive** streak of the same `tool_name` >= 5 (args not compared) | AF-0058 overlaps | **→ exact.** This is AF-0058's first symptom almost verbatim. |
| `stuck_loop` | `unique_urls <= 1 and step_count >= 5`; "stayed on one page while continuing to act" | AF-0058 exact | **→ overlaps.** No repetition required — it is absence of navigation progress. Matches AF-0058's "step count grows while state unchanged" but is equally close to `model_limit` as detected. |
| `timeout` | outcome `failed`/`incomplete` **and** `step_count >= 40` **and** last 5 steps on <=1 URL with <=2 tools | AF-0136 exact | **→ overlaps**, or broaden AF-0136 to "time *or step* budget exhausted". No elapsed-time signal at all; the classifier ignores the analyzer's `timed_out` flag. |
| `tool_bug` | error rate > 0.5 and `unknown_tool + validation + other` errors outnumber `timeout + click_fail + not_found` | `[]` GAP | **Gap is real but smaller than stated.** As detected, `tool_bug` is mostly **`unknown tool`** (= AF-0011) and **`validation error / field required`** (= AF-0023) — agent-side call errors, not tool defects. Honest mapping: AF-0011 overlaps + AF-0023 overlaps, GAP note retained for the intended tool-layer concept. |
| `routing_bug` | `no_tools_steps > 0` — steps where the exposed tool list was **empty** | AF-0088 overlaps | **Wrong.** Nothing to do with the agent's plan; it is the harness not exposing tools. Shares AF-0007's symptom "no available tool covers the capability" but at the harness layer. → AF-0007 overlaps + **GAP: tool not exposed (harness)**. |
| `tool_selection_bug` | (a) browser tools available, never used, only search/read used; (b) <=1 unique tool across >1 URLs | AF-0088 overlaps + AF-0023 overlaps | **Drop AF-0023.** No invocation error is involved; the calls are valid, the *choice* is wrong. Keep AF-0088 overlaps; candidate new mode "wrong tool selected" (model layer). |
| `context_overflow` | first step whose text matches context-pressure regex, then later reasoning shrinks >=40% or late errors rise | AF-0064 exact | **→ overlaps.** Concept is *degradation under pressure*, not *content dropped and acted on as if present*. |
| `memory_overload` | context usage >= 85% plus any of: pressure text, late confusion, late errors, **compaction/trim/eviction counters > 0**, short final answer | AF-0064 overlaps | Hold. Note: this is the category that actually carries AF-0064's eviction-event symptom, not `context_overflow`. The two are near-synonyms by design. |
| `environment_drift` | error rate > 0.5 and `timeout + click_fail + not_found` >= tool errors | AF-0118 exact | Hold, add note: detector is "environment-style errors dominate", a proxy for the described "page changed underneath the runner". |
| `model_limit` | `step_count > 50 and unique_urls < 2` | AF-0125 exact | Hold, add note: same test as `stuck_loop` at a higher threshold. |
| `delegation_failure` | a delegation-marker tool returned an error-like result | AF-0071 exact | Minor: AF-0071 also covers brief distortion and discarded results; `broader` is more precise than `exact`. |
| `early_abort` | `0 < step_count < 3` | AF-0077 exact | Hold. AF-0077's "claims completion" symptom is not required, but the concept matches. |
| `prompt_bug` | confusion/uncertainty regex in reasoning; also the residual when a prompt-section pattern hits | AF-0103 overlaps | Hold; note its quasi-residual role. |
| `reasoning_bug` | `errors == 0 and unique_tools > 1 and unique_urls > 1` — progressed cleanly, still failed | AF-0042 + AF-0125 overlaps | Hold; AF-0088 overlaps would also be defensible. Effectively "failed with no hard signal". |
| `approval_block` | `error_kinds["approval_block"]` or `approval_path` contains block/denied | AF-0095 exact | Hold. |
| `tool_rejection_mismatch` | non-expected rejected tools on >= 30% of steps | AF-0095 overlaps | Hold. |
| `test_failure_loop` | same normalised failure signature >= 2 runs; bonus evidence if no file edit between | AF-0049 exact | Hold — matches AF-0049 symptoms line for line. |
| `rate_limit_cascade` | >= 3 steps with 429 / rate-limit text | AF-0130 exact | Hold. |
| `insufficient_sources` | research task with < 2 searches and < 2 source diversity | AF-0086 exact | Hold. |
| `valid_alternative_path`, `consultative_success` | completed; non-browser path / long final answer | `[]` | Hold — not failures. |
| `unclassified` | nothing matched, no prompt pattern | `[]` | Hold — residual. |

## Gaps Agent-Xray surfaces (for the PR)

1. **Tool-layer defect** — still no AF mode; `tool_bug`'s *intended* meaning.
2. **Tool not exposed by the harness** (`routing_bug`) — no AF mode; AF-0007 is
   the user-intent-layer cousin.
3. **Wrong tool selected** (`tool_selection_bug`) — no AF mode; AF-0088 is the
   nearest.
4. **Context-pressure degradation** (`context_overflow` / `memory_overload`) —
   AF-0064 is about loss, not degradation. Candidate, not yet convinced it is
   distinct enough.
