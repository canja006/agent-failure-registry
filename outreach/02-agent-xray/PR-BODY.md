**Title:** `docs: add optional cross-taxonomy mapping file (no code changes)`

---

### What this adds

One data file, `afr-mapping.yaml`. No code, no dependencies, nothing reads it
at runtime.

It maps Agent-Xray's 22 root-cause categories onto `AF-####` ids from the
Agent Failure Registry, a vendor-neutral namespace for agent failure modes.
The motivation is that someone running Agent-Xray and any other diagnostic
tool currently gets two reports with no shared vocabulary between them.

The mapping was made from a full read of `root_cause.py` and `analyzer.py`
(at `main`, 2026-08-23), not from the README table — several categories'
detectors are more specific than their one-line descriptions, and the mapping
follows the detectors. The read notes are public in the AFR repo.

### Your taxonomy changed ours

This is the mapping working in the direction I hoped it would. Three Agent-Xray
categories name things the registry could not name; one is already fixed and
two are recorded as open gaps:

- **`tool_bug`** — the *intended* meaning (right tool, bad result) is a
  tool-layer defect, and the registry had no `tool`-layer mode at all. It now
  has one, `AF-0149`, written because of this category and cited as such.
  `tool_bug` maps `overlaps` to it rather than `exact` because, as detected
  (`unknown_tool` + `validation` + `other` errors dominating), the category
  also catches fabricated tools and schema errors, which map to two other
  modes — the file lists all three.
- **`routing_bug`** — a step whose exposed tool list is empty. Tool-not-exposed
  is a harness failure no taxonomy I have mapped names; the nearest AF mode is
  the user-intent-layer cousin "intent not supported", mapped `overlaps`.
- **`tool_selection_bug`** — right tool available, something else used, no
  invocation error. Wrong-tool-selected is a distinct thing from
  plan/intent misalignment; mapped `overlaps` to that for now.

The 22-category cascade is the most granular taxonomy I have read, and
separating `spin` from `stuck_loop`, and `test_failure_loop` from both, is a
distinction the coarser taxonomies collapse.

### Judgement calls I would like checked

Surfaced rather than buried — the registry allows at most one `exact` per
category precisely so a single wrong `exact` cannot quietly discredit the rest
of the table.

- **`spin` → `exact`, `stuck_loop` → `overlaps`** (both to "unproductive
  repetition"). `spin` is a consecutive same-tool streak, which is that mode's
  first symptom almost verbatim; `stuck_loop` is one-URL-many-steps, which
  doesn't require repetition. If you read them the other way round, it is a
  one-line fix.
- **`timeout` → `exact`** to a mode that covers *time or step* budgets. Your
  detector is a step budget plus a stalled final window; the registry
  broadened its mode to match because the two present identically in a trace.
- **`context_overflow` and `memory_overload` → both `overlaps`**, not exact, to
  "context overflow truncation". Both detect degradation under context
  pressure; the AF mode is specifically about content being dropped and then
  acted on as if present. `memory_overload` is actually the one that can carry
  the eviction/compaction counters.
- **`model_limit` → `exact`** to "model capability limit", with a note that
  the detector (>50 steps, <2 URLs) is the `stuck_loop` test at a higher
  threshold, so AFR profiles from Agent-Xray will split those two by step
  count.
- `valid_alternative_path`, `consultative_success` and `unclassified` are left
  unmapped as non-failures / residual rather than forced onto a mode.

### No obligation either way

Nothing here asks Agent-Xray to adopt AF ids or change anything. The mapping is
published upstream regardless; having it beside the taxonomy it describes just
keeps it honest when the taxonomy changes. Close it without ceremony if you
would rather not carry the file.
