# Agent Failure Registry

**A neutral namespace for AI agent failure modes, and a crosswalk between the
taxonomies that already exist.**

Not another classifier. There are at least seven of those, each with its own
private vocabulary: Agent-Xray's `tool_selection_bug`, AgentRx's
`Invalid Invocation`, and five more describing overlapping reality under names
that share nothing. This is the mapping layer between them.

```python
>>> import afr
>>> afr.map("agentrx", "Invalid Invocation")
[AF-0023 (exact)]
>>> afr.map("agent-xray", "spin")
[AF-0058 (exact)]
>>> afr.mode("AF-0058").layer
'harness'
```

The analogy is CVE, not CWE. Plenty of people have proposed taxonomies; nobody
has done the boring institutional work of assigning stable ids, accepting
mappings, and letting tools *reference* them. CVE's value was never
intellectual — it was giving the whole industry a shared noun.

## Why this and not a classifier

- **It gets stronger as rivals ship.** Every new classifier with a private
  taxonomy increases the need for the crosswalk. A classifier is threatened by
  the next classifier; a namespace is fed by it.
- **Incumbents structurally cannot build it.** A registry operated by one
  vendor is one every competitor is right to ignore. Microsoft declined the
  standards position for AgentRx explicitly.
- **Distribution runs through other repos.** You do not need an audience — you
  open a PR adding a mapping file to each classifier.

## Install

```bash
pip install agent-failure-registry     # zero runtime dependencies; imports as `afr`
```

## Use

```python
import afr

# One tool's report, tagged with shared ids
labels = afr.normalize({"stuck_loop": 31, "context_overflow": 18}, "agent-xray")
print(afr.profile(labels).render())
```

```
failure profile  (source: agent-xray, n=49)
--------------------------------------------------------------------
AF-0058    63.3%  ######################              Unproductive repetition
AF-0064    36.7%  ############                        Context overflow truncation
--------------------------------------------------------------------
by layer: harness=49
```

That is the pitch in one output. `67% pass` tells you nothing you can act on.

```bash
afr modes                              # every mode
afr show AF-0142                       # full record, plus who maps to it
afr map agentrx "System Failure"       # source category -> AF ids
afr unmap AF-0064 agent-xray           # and back, with relations inverted
afr coverage                           # how much of each taxonomy is mapped
afr gaps                               # what nobody has named yet
```

## Two levels of identifier

| | | |
|---|---|---|
| **`AF-0142`** | mode | Permanent, versionless, like CWE. What classifiers map onto and humans cite. |
| **`AFI-2026-08-0417`** | instance | One observation, pinned to model + harness version, like CVE. |

Conflating them breaks the query that justifies the whole project: *did Opus 5.2
regress on AF-0142 relative to 5.1?* That needs modes stable across time and
instances pinned to versions — so they cannot be the same identifier.

Instances are **deliberately not implemented yet**. Open collection only once
three independent tools emit AF ids.

## Relation direction

`relation` describes **the AF mode relative to the source category**: `exact`,
`broader`, `narrower`, `overlaps`. `afr.unmap()` inverts it for you — swapping
`broader` and `narrower` — because hand-authoring the reverse is how crosswalks
silently corrupt.

At most one `exact` per source category. One wrong `exact` discredits the table.

## Status

Pre-v0. 19 modes, all `provisional`; 3 source taxonomies; 90% of AgentRx and
86% of Agent-Xray mapped — Agent-Xray from a full read of its classifier, not
its README (see [`registry/crosswalk/notes/`](registry/crosswalk/notes/)). The
remaining modes are week-one reading, not coding — see
[`registry/crosswalk/academic.yaml`](registry/crosswalk/academic.yaml) for the
queue.

Findings are already falling out of the structure, which is the point. One
has already changed the registry: Agent-Xray's `tool_bug` exposed an empty
`tool` layer, and **`AF-0149`** (tool defect) now fills it. `afr gaps` surfaces
six more from the two tools, plus one orphan:

- **tool never exposed by the harness** (`agent-xray:routing_bug`)
- **wrong tool selected** (`agent-xray:tool_selection_bug`)
- **required step skipped with the goal correct** (`agentrx:Instruction/Plan
  Adherence Failure` — the most common failure event in AgentRx's own data)
- **fabricated fact or claim about state** (`agentrx:Invention of New Information`)
- **external access block** — CAPTCHA / 403 / paywall (`agentrx:Guardrails Triggered`)
- **connectivity failure** — DNS / refused / unreachable (`agentrx:System Failure`)
- **`AF-0142`** (stale context re-read) has **no source mapping** — a failure
  everyone has seen that no published taxonomy names.

Modes for these get written once a second independent source names the same
thing — one mode per vendor category is how a shared namespace becomes a house
style.

## Repo layout

```
registry/modes/AF-####.yaml     canonical mode records (CC0)
registry/crosswalk/*.yaml       one file per third-party taxonomy (CC0)
registry/SCHEMA.md              field semantics and relation direction
afr/                            the library (Apache-2.0), no dependencies
afr/_index.json                 compiled from YAML, committed, CI-enforced
scripts/compile.py              YAML -> index (the only place PyYAML is needed)
scripts/validate.py             integrity checks; a lying crosswalk is worse than none
```

## Development

```bash
make check      # build + validate + test
make demo       # coverage, gaps, and a sample profile
```

## Licensing

Registry data is **CC0**; the library is **Apache-2.0**. A namespace with an
attribution clause invites legal review, and legal review is the friction that
stops tools embedding it.

Governance, including the commitment to move to a neutral foundation once three
independent tools map to this namespace, is in [GOVERNANCE.md](GOVERNANCE.md).

## Outreach

Distribution runs through other projects' repos, not through this one. Drafted
mapping-file PRs for AgentRx and Agent-Xray, and an issue for AgentDebugX, are
in [`outreach/`](outreach/) — including the order to send them in, which
matters more than the speed.
