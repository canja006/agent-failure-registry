**Title:** `docs: add optional cross-taxonomy mapping file (no code changes)`

---

### What this adds

One data file, `afr-mapping.yaml`. No code changes, no dependencies, nothing in
AgentRx reads it.

It maps AgentRx's ten root-cause labels onto `AF-####` ids from the Agent
Failure Registry — a vendor-neutral namespace for agent failure modes. The
point is comparability: a practitioner running AgentRx and a second diagnostic
tool currently gets two reports with no shared vocabulary, and no way to tell
whether the two tools found the same thing.

The mapping was made from the judge's operative definitions and checklists in
`agentrx/judge/judge.py`, the paper (§2.2), and the ground-truth annotations —
not from the README table. The checklists are more precise than the one-line
descriptions, and the mapping follows them. The read notes are public in the
AFR repo.

### Why here rather than only in our repo

The mapping is published on our side regardless. Having it sit alongside the
taxonomy it describes means it stays visible to the people it helps, and it
gets noticed when the taxonomy changes. If you would rather it live only
upstream, say so and I will close this — the mapping is useful either way.

### Your taxonomy changed ours

This is the mapping working in the direction I hoped it would. Four AgentRx
categories named things the registry could not name exactly. Three of them are
now modes — written because AgentRx and at least one other independent
taxonomy named the same thing, and cited as such — and one is still an open
gap:

- **`Instruction/Plan Adherence Failure`** — your checklist defines this as
  *goal correct, required step skipped / reordered / padded*, and your own
  annotations make it the most common failure event in the corpus. The
  registry had only "premature termination" for it. It now has `AF-0153`
  (required step omitted) and `AF-0166` (unnecessary action), with premature
  termination as the third slice; the category maps `narrower` to all three.
- **`Invention of New Information`** — the registry's only mode was fabricated
  *tool and parameter schemas*. It now has `AF-0161` (fabricated content) for
  invented facts and hallucinated state. Your category also covers
  unjustified *omission*, which neither mode does, so both map `narrower`.
- **`System Failure`** — the connectivity half (DNS / refused / unreachable /
  service unavailable) had no mode; it is now `AF-0170` (external service
  failure), alongside the existing time/step budget, rate-limit cascade and
  tool-internal error modes.
- **`Guardrails Triggered`** — your definition spans RAI/safety refusals *and*
  external site access restrictions (CAPTCHA, 403, paywall, robots.txt). The
  registry's "guardrail block" is the harness's own policy gate, so it maps
  `narrower`; the external-access half is an environment-layer block nobody
  else has named yet, so it stays a recorded gap.

### Mapping decisions worth flagging

Surfaced rather than buried — the registry allows at most one `exact` per
category precisely so a single wrong `exact` cannot quietly discredit the rest
of the table.

- **`Misinterpretation of Tool Output`** is `narrower` to "tool output
  misread", not `exact`, because the judge's name for it is
  "… / Handoff Failure" and the checklist covers *another agent's* output. The
  handoff half also maps `overlaps` to "delegation failure". 15 of 44 Magentic
  root causes are Orchestrator-misreads-WebSurfer, so this matters for profiles.
- **`Instruction/Plan Adherence Failure`** no longer maps to "plan/intent
  misalignment" at all — checklist question 1 requires the goal to be correct,
  which makes the two categories disjoint by construction.
- `Inconclusive` is left unmapped as a residual; the file notes that the judge
  emits a free-text `custom_category` with it.

### On the category count

The README lists ten labels; the paper (§2.2) describes nine with
`Inconclusive` as the residual. The file follows the README's ten and treats
`Inconclusive` as unmapped, which I believe matches the intent. Correct me if
not.

### Not an endorsement

AFR does not ask AgentRx to adopt its ids, change its taxonomy, or depend on
anything. Mapping runs one way — the registry maps onto you. Merging this
implies no endorsement of the registry, and I have made that explicit in the
file header.

Happy to sign whatever CLA applies.
