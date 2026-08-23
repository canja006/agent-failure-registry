**Title:** `docs: add optional cross-taxonomy mapping file (no code changes)`

---

### What this adds

One data file, `afr-mapping.yaml`. No code, no dependencies, nothing reads it
at runtime.

It maps Agent-Xray's 22 cascade categories onto `AF-####` ids from the Agent
Failure Registry, a vendor-neutral namespace for agent failure modes. The
motivation is that someone running Agent-Xray and any other diagnostic tool
currently gets two reports with no shared vocabulary between them.

### Your taxonomy found a gap in ours

`tool_bug` — a defect in the tool itself rather than in the agent's use of it —
has **no AF mode**. Nothing in the registry covers the `tool` layer yet, and
none of the other taxonomies I mapped names it either. It is now recorded as an
open gap and is one of the next modes to be written.

That is the mapping working in the direction I hoped it would. The 22-category
cascade is the most granular taxonomy I have read, and separating
`stuck_loop` from `spin`, and `test_failure_loop` from both, is a distinction
the coarser taxonomies collapse.

### One judgement call I would like checked

**`tool_selection_bug`** is mapped as `overlaps` to *both* `AF-0088`
(plan/intent misalignment) and `AF-0023` (invalid tool invocation), rather than
`exact` to either. Choosing the wrong tool sits between planning and
invocation, and I could not honestly call it either one.

If you read it as unambiguously one of those, tell me and I will tighten it.
The registry allows at most one `exact` per category precisely so that a single
wrong `exact` cannot quietly discredit the rest of the table.

Also flagged for you rather than silently mapped:

- `spin` → `AF-0058` as `overlaps`, not `exact`, because `stuck_loop` takes the
  `exact`. If that ordering is backwards, it is a one-line fix.
- `valid_alternative_path`, `consultative_success` and `unclassified` are left
  unmapped as non-failures rather than forced onto a mode.

### No obligation either way

Nothing here asks Agent-Xray to adopt AF ids or change anything. The mapping is
published upstream regardless; having it beside the taxonomy it describes just
keeps it honest when the taxonomy changes. Close it without ceremony if you
would rather not carry the file.
