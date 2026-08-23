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
'model'
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
by layer: model=49
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

Pre-v0. **25 modes** — 14 `stable`, 11 `provisional`; **7 source taxonomies**, every one
mapped from a full read of its operative definitions (classifier code, judge
prompts, paper text, ground-truth annotations), with the evidence in
[`registry/crosswalk/notes/`](registry/crosswalk/notes/):

| source | kind | mapped |
|---|---|---|
| [AgentRx](https://github.com/microsoft/AgentRx) | LLM judge, 10 labels | 9/10 |
| [Agent-Xray](https://github.com/GeeIHadAGoodTime/Agent-Xray) | rule classifier, 22 labels | 19/22 |
| [ToolFailBench](https://arxiv.org/abs/2607.04686) | benchmark, 5 labels | 4/5 |
| [AgentFail](https://arxiv.org/abs/2509.23735) | 307 annotated failures, 16 root causes | 15/16 |
| [Model or Harness?](https://arxiv.org/abs/2607.28802) | 41 modes with fault side | 27/41 |
| [Characterizing Faults](https://arxiv.org/abs/2603.06847) | 385 framework defects, 14 categories | 5/14 — mostly out of scope by design |
| [AgentDebugX](https://github.com/AgentDebugX/AgentDebugX) | debugger, 19 seed modes | 16/19 |

No mode is an orphan: every AF id has at least one source, and the six
newest (`AF-0153` required step omitted, `AF-0157` wrong tool selected,
`AF-0161` fabricated content, `AF-0166` unnecessary action, `AF-0170`
external service failure, `AF-0174` stored memory unused) each have two or
more. The rule that produced them:
**a gap becomes a mode only when a second independent taxonomy names the same
thing** — one mode per vendor category is how a shared namespace becomes a
house style.

`afr gaps` lists what is still unnamed. The ones with more than one source
behind them are the next candidates; the single-source ones (most of the memory
family, recovery failure, sycophancy, prompt injection, external access
blocks, role drift, non-text perception) wait for a second.

Layer attribution follows a stated principle (SCHEMA.md, adopted from
[Model or Harness?](https://arxiv.org/abs/2607.28802)): the fault lies with
the component that could have acted correctly on the information it had.
Promotion to `stable` required two independent sources, at least one `exact`
mapping, and a definition that survived the full-read pass unchanged.

## Repo layout

```
registry/modes/AF-####.yaml     canonical mode records (CC0)
registry/crosswalk/*.yaml       one file per third-party taxonomy (CC0)
registry/crosswalk/notes/       the full-read evidence behind each crosswalk
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
