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

### Why here rather than only in our repo

The mapping is published on our side regardless. Having it sit alongside the
taxonomy it describes means it stays visible to the people it helps, and it
gets noticed when the taxonomy changes. If you would rather it live only
upstream, say so and I will close this — the mapping is useful either way.

### Mapping decisions worth flagging

Three needed judgement, and I would rather surface them than have them found
later:

- **`System Failure` → three `narrower` mappings** (`AF-0064` context overflow,
  `AF-0130` rate-limit cascade, `AF-0136` timeout). Read as a deliberate
  catch-all for infrastructure faults; AFR splits it by mechanism. If you
  intend it more narrowly, this is wrong and I will fix it.
- **`Invention of New Information` → `AF-0011` (`narrower`)**. `AF-0011` covers
  fabricated *tool and parameter schemas* specifically. Your category also
  covers fabricated facts, which AFR has no mode for yet — a gap on our side,
  recorded as such.
- **`Instruction/Plan Adherence Failure`** splits across `AF-0077` (stopping
  early, `narrower`) and `AF-0088` (planning wrong, `overlaps`).

`Inconclusive` is deliberately left unmapped as a residual label rather than
forced onto a mode.

### On the category count

The README lists ten labels; the paper (arXiv 2602.02475) describes nine
root-cause categories with `Inconclusive` as the residual. The file follows the
README's ten and treats `Inconclusive` as unmapped, which I believe matches the
intent. Correct me if not.

### Not an endorsement

AFR does not ask AgentRx to adopt its ids, change its taxonomy, or depend on
anything. Mapping runs one way — the registry maps onto you. Merging this
implies no endorsement of the registry, and I have made that explicit in the
file header.

Happy to sign whatever CLA applies.
