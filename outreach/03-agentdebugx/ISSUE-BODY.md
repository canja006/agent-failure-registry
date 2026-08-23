**Open an ISSUE here, not a PR.** This repo accompanies a paper and already has
its own sharing mechanism; arriving with a diff would be presumptuous. Ask
first, contribute second.

**Title:** `Shared failure-mode ids across taxonomies — would Error Hub bundles carry them?`

---

Thanks for AgentDebugX — the Detect → Attribute → Recover → Rerun loop is the
clearest framing of the debugging cycle I have read, and the opt-in Error Hub
with scrubbed bundles is the part I keep coming back to.

A question rather than a proposal.

### The problem

I have been mapping the agent failure taxonomies against each other, and there
are now at least seven mutually incompatible ones — AgentRx's ten root causes,
Agent-Xray's 22 cascade categories, and the published taxonomies in 2603.06847,
2607.28802, 2509.23735 and 2607.04686. None shares vocabulary with any other.
Agent-Xray's `tool_selection_bug` and AgentRx's `Invalid Invocation` describe
overlapping reality under names with nothing in common.

This is roughly the pre-CVE situation in vulnerability tooling: several good
taxonomies, no shared noun, so nothing aggregates across tools.

### What I have built

A vendor-neutral namespace — `AF-####` for permanent failure *modes*, plus
crosswalk tables mapping each existing taxonomy onto it, with typed relations
(`exact` / `broader` / `narrower` / `overlaps`) borrowed from how medical coding
handles the same lossiness. It deliberately contains no classifier. Mapping runs
one way: the registry maps onto your taxonomy, never the reverse.

### The actual question

Error Hub bundles look like the closest thing anyone has to a shared corpus of
real failures. If a bundle carried an optional `af_id` alongside your own
diagnosis label, bundles from AgentDebugX would aggregate with output from tools
that never used AgentDebugX — and the question *"did this model regress on this
failure mode between versions?"* becomes answerable across the ecosystem rather
than within one tool.

So:

1. Would an optional shared id field in a bundle be of interest, or does it cut
   against how you intend Error Hub to work?
2. Is your taxonomy stable enough to be worth crosswalking now, or should I wait
   for a later revision? I would rather map from the source than from the paper.
3. Is there a reason a neutral namespace is the wrong shape for this that I have
   not thought of? A real answer here is more useful to me than a merge.

Happy for the answer to be no. I am mapping your taxonomy either way and will
publish it upstream with corrections welcome.
