# Governance

The registry's only asset is neutrality. A namespace one vendor controls is one
every other vendor is right to ignore.

## Now

Maintained by a single maintainer (BDFL). Decisions in the open, on issues.

## The commitment

**When three independent tools map to this namespace, the registry moves to a
neutral foundation.** Publishing that exit ramp before it is needed is the only
credibility available to an unknown maintainer, and it is a promise, not an
aspiration.

Until then:

- Mode ids are **never** reused or renumbered. A withdrawn mode becomes
  `deprecated` with a `superseded_by` pointer, and its id stays burned.
- Crosswalks are additive. A mapping is corrected in place with the reason in
  the commit message; source-side taxonomy changes get a new `observed` date.
- No mapping is added for a taxonomy the maintainer has not read in full.
- Vendors may open PRs for their own taxonomy. Vendors do not get to define
  AF modes to match their categories — that is how a shared namespace becomes
  a house style.

## Adding a mode

A mode earns an id when it is **observable** (symptoms visible in a trajectory),
**discriminable** (distinguishable from every near neighbour), and **not already
covered** by an existing mode at a different granularity.

New modes land as `provisional`. Promotion to `stable` requires two independent
taxonomies mapping onto it, or documented examples from two independent sources.

## Licensing

Registry data is CC0 — a namespace with an attribution clause invites legal
review, and legal review is the friction that stops tools embedding it. The
library is Apache-2.0 for its patent grant.
