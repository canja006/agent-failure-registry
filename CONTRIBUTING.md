# Contributing

```bash
pip install pyyaml            # build-time only; the library has no runtime deps
make build                    # registry/*.yaml -> afr/_index.json
make check                    # validate + tests
```

`afr/_index.json` is generated and **committed** — that is what lets the
runtime stay dependency-free. Always rebuild before committing YAML changes;
CI fails if the index is stale.

## Adding a mode

1. `registry/modes/AF-####.yaml`, any unused id above the current maximum —
   the numbering is sparse on purpose, so ids do not read as a ranking. Never
   reuse a retired one.
2. Symptoms must be observable in a trajectory. If you cannot say what a
   classifier would look at, the mode is not ready.
3. Every near neighbour gets a `vs AF-####:` discriminator, and vice versa.
4. `make check` — the validator flags one-sided neighbour links and
   discriminators citing modes you forgot to declare.

## Adding a crosswalk

Read the taxonomy in full first. Mapping from an abstract or a blog summary
produces exactly the false precision this project exists to remove.

- Set `observed` to the date you read it, and `taxonomy_size` to the real count.
  The validator checks the count against your mappings.
- One `exact` per category, at most. When tempted by a second, it is `overlaps`.
- Leave `af: []` with a `GAP:` note when the source names something the registry
  does not. Those notes are the roadmap.

Honest lossiness is survivable. False precision is not.
