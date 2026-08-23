**Open an ISSUE here, not a PR.** This repo accompanies a research effort and
has its own sharing mechanism; arriving with a diff would be presumptuous.
Ask first, contribute second.

**Title:** `Shared failure-mode ids across taxonomies — AF ids are derivable from Error Hub bundles today`

---

Thanks for AgentDebugX — the Diagnose → Rerun split is the clearest framing of
the debugging cycle I have read, and the opt-in Error Hub with scrubbed
bundles is the part I keep coming back to.

A question rather than a proposal — though I have done the homework first.

### The problem

I have been mapping the agent failure taxonomies against each other, and
there are now at least seven mutually incompatible ones — AgentRx's ten root
causes, Agent-Xray's 22 cascade categories, ToolFailBench's labels, AgentFail's
sixteen root causes, and the published taxonomies in 2607.28802 and
2603.06847. None shares vocabulary with any other. Your own seed taxonomy
quietly acknowledges this: its `source` fields cite AgentDebug, MAST,
Who&When, AgentRx and AgentSight — you are already crosswalking informally,
one citation at a time.

This is roughly the pre-CVE situation in vulnerability tooling: several good
taxonomies, no shared noun, so nothing aggregates across tools.

### What I have built

A vendor-neutral namespace — `AF-####` for permanent failure *modes*, plus
crosswalk tables mapping each taxonomy onto it with typed relations
(`exact` / `broader` / `narrower` / `overlaps`), borrowed from how medical
coding handles the same lossiness. It deliberately contains no classifier.
Mapping runs one way: the registry maps onto your taxonomy, never the reverse.

**Your 19 seed modes are already mapped** — from a full read of
`schema/taxonomy.py`, not the README — and published with the reasoning:

- crosswalk: https://github.com/canja006/agent-failure-registry/blob/main/registry/crosswalk/agentdebugx.yaml
- read notes: https://github.com/canja006/agent-failure-registry/blob/main/registry/crosswalk/notes/agentdebugx.md

Two things fell out of the read, which is the point of the exercise:

- `memory.retrieval_failure` was the second independent taxonomy to name a
  memory-read failure, so the registry now has a mode for it (`AF-0174`,
  "stored memory unused") — written because of you and cited as such.
- Three of your seed modes name things no taxonomy I have mapped can express
  (`reflection.causal_misattribution`, `multiagent.role_drift`, non-text
  `multimodal.perception_error`). They are recorded as open gaps with your
  categories as the source.

### The actual question

Because `BundleManifest` already carries `failure_mode_ids`, **nothing in
AgentDebugX needs to change for bundles to interoperate**: an AF id is
derivable from a bundle today via the crosswalk above. So the question is not
"would you add a field" but:

1. Would you *want* the mapping visible near the taxonomy — a data file in
   this repo, a doc link, or neither? Publishing it upstream only is fine;
   I would just rather the people reading `schema/taxonomy.py` know it exists.
2. The seed set says it is "designed to be extended by generated,
   project-specific taxonomy nodes." Is the *seed* list itself stable enough
   that a crosswalk against it will not rot within a release or two — or
   should I pin it to a version tag?
3. Is there a reason a neutral namespace is the wrong shape for this that I
   have not thought of? A real answer here is more useful to me than a merge.

Happy for the answer to be no on all three. The mapping stays published and
maintained upstream either way, and corrections are welcome as issues there.
