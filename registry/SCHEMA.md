# Registry schema

Two record types. Getting the distinction right is the whole design.

## Modes — `registry/modes/AF-####.yaml`

A **mode** is a permanent, versionless class of failure. Modes are what
classifiers map onto and what people cite in issues. They are never
year-stamped: "stale context re-read" is not a failure *of 2026*.

| field | required | notes |
|---|---|---|
| `id` | yes | `AF-` + four digits. Never reused, never renumbered. |
| `title` | yes | Short noun phrase. |
| `status` | yes | `provisional` \| `stable` \| `deprecated` |
| `layer` | yes | `model` \| `harness` \| `tool` \| `environment` \| `user-intent` |
| `description` | yes | 2–4 sentences. What happens, not who is at fault. |
| `symptoms` | yes | **Observable** signals only. Never causes. |
| `discriminators` | strongly | `vs AF-####: …` — how to tell it from a neighbour. |
| `near_neighbors` | strongly | The confusion set. Every mode cited in a discriminator belongs here. |
| `references` | no | Papers, issues, postmortems. |
| `examples` | no | Minimal reproducing trajectory fragments. |

### Why `layer` is separate

Attribution — model vs. harness vs. tool — is the most contested judgement in
this space, and there is [a whole paper](https://arxiv.org/abs/2607.28802) on
localising it. Keeping layer as its own axis means a mode can be recorded from
its **symptoms** without first resolving blame. The id stays stable even while
attribution is argued about.

### Why `symptoms` must be observable

Causes are contested; observations are not. A symptom you cannot see in a
trajectory cannot be classified from one, and a mode nobody can apply
consistently is worse than no mode at all.

### Why `discriminators` exist

Most taxonomies fail not because their categories are wrong but because they
overlap and nobody knows which to pick. Explicit confusion sets are what make a
taxonomy usable — and what you measure inter-rater agreement against.

## Crosswalks — `registry/crosswalk/<source>.yaml`

One file per third-party taxonomy.

```yaml
source:
  id: agentrx
  name: AgentRx
  vendor: Microsoft Research
  url: https://github.com/microsoft/AgentRx
  license: MIT
  taxonomy_size: 10        # validated against the mapping count
  observed: "2026-08-23"   # taxonomies drift; record when you read it

mappings:
  - category: "Invalid Invocation"
    af: [{id: AF-0023, relation: exact}]
  - category: "System Failure"
    af:
      - {id: AF-0064, relation: narrower}
      - {id: AF-0130, relation: narrower}
      - {id: AF-0136, relation: narrower}
    note: "Catch-all infrastructure bucket; AF splits it by mechanism."
```

### Relation direction — read this twice

`relation` describes **the AF mode relative to the source category**.

| relation | meaning |
|---|---|
| `exact` | same concept |
| `narrower` | the AF mode is *narrower* than the source category |
| `broader` | the AF mode is *broader* than the source category |
| `overlaps` | partial; neither contains the other |

Reading a mapping backwards inverts it: `afr.unmap()` swaps `broader` and
`narrower` for you. Hand-authoring the reverse direction is how crosswalks
silently corrupt.

**At most one `exact` per source category.** Two exact mappings means at least
one is really `overlaps`, and one wrong `exact` discredits the whole table.

### Empty `af:` is meaningful

Three different things, all legitimate, distinguished by `note`:

- **Residual labels** — `Inconclusive`, `unclassified`. Not failures.
- **Non-failures** — `valid_alternative_path`, `consultative_success`.
- **Genuine gaps** — prefix the note with `GAP:`. `afr gaps` surfaces these,
  and they are the registry's roadmap for the classifiers.

## Instances — not yet

`AFI-YYYY-MM-####` records one observed occurrence pinned to a model version,
harness version and tool set. They are what make *"did Opus 5.2 regress on
AF-0142?"* answerable.

Deliberately not implemented. Open instance collection only once three
independent tools emit AF ids — a corpus with no shared vocabulary feeding it
is a pile of logs.
