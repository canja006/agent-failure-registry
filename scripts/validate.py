#!/usr/bin/env python3
"""Integrity checks for the registry. Run in CI; a crosswalk that lies is
worse than no crosswalk at all.

    python3 scripts/validate.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import afr
from afr import data
from afr.model import LAYERS, RELATIONS

ID_RE = re.compile(r"^AF-\d{4}$")
STATUSES = ("provisional", "stable", "deprecated")


def main():
    errors, warnings = [], []
    modes = afr.modes()
    ids = {m.id for m in modes}

    if len(ids) != len(modes):
        errors.append("duplicate mode ids present")

    for m in modes:
        where = m.id
        if not ID_RE.match(m.id):
            errors.append("%s: malformed id" % where)
        if m.status not in STATUSES:
            errors.append("%s: bad status %r" % (where, m.status))
        if m.layer not in LAYERS:
            errors.append("%s: bad layer %r" % (where, m.layer))
        if not m.description:
            errors.append("%s: empty description" % where)
        if not m.symptoms:
            errors.append("%s: no symptoms - modes must be observable" % where)
        if not m.discriminators:
            warnings.append("%s: no discriminators - overlap risk" % where)
        for nn in m.near_neighbors:
            if nn not in ids:
                errors.append("%s: near_neighbor %s does not exist" % (where, nn))
            if nn == m.id:
                errors.append("%s: lists itself as a near neighbor" % where)
        # A discriminator naming a mode should have it as a declared neighbour.
        cited = set()
        for disc in m.discriminators:
            for ref in re.findall(r"AF-\d{4}", disc):
                cited.add(ref)
                if ref not in m.near_neighbors:
                    warnings.append(
                        "%s: discriminator cites %s but it is not in near_neighbors"
                        % (where, ref)
                    )
        # ...and every declared neighbour should come with a discriminator.
        for nn in m.near_neighbors:
            if nn not in cited:
                warnings.append(
                    "%s: near_neighbor %s has no `vs %s:` discriminator" % (where, nn, nn)
                )

    # Confusion is symmetric: if A lists B, B must list A. One-sided links are
    # how a confusion set silently decays, so this is an error, not a warning.
    by_id = {m.id: m for m in modes}
    for m in modes:
        for nn in m.near_neighbors:
            if nn in by_id and m.id not in by_id[nn].near_neighbors:
                errors.append(
                    "%s: lists %s as a near neighbor, but %s does not list %s"
                    % (m.id, nn, nn, m.id)
                )

    for src in afr.sources():
        cats = data.categories(src.id)
        if src.taxonomy_size and len(cats) != src.taxonomy_size:
            errors.append(
                "%s: declares taxonomy_size %d but has %d categories"
                % (src.id, src.taxonomy_size, len(cats))
            )
        for cat in cats:
            for edge in data.edges(src.id, cat):
                if edge.id not in ids:
                    errors.append(
                        "%s/%s: maps to unknown mode %s" % (src.id, cat, edge.id)
                    )
                if edge.relation not in RELATIONS:
                    errors.append(
                        "%s/%s: bad relation %r" % (src.id, cat, edge.relation)
                    )
            seen = [e.id for e in data.edges(src.id, cat)]
            if len(seen) != len(set(seen)):
                errors.append("%s/%s: duplicate target modes" % (src.id, cat))
            exacts = [e for e in data.edges(src.id, cat) if e.relation == "exact"]
            if len(exacts) > 1:
                errors.append(
                    "%s/%s: %d exact mappings - exact must be one-to-one"
                    % (src.id, cat, len(exacts))
                )

    orphans = sorted(
        m.id for m in modes
        if not any(
            any(e.id == m.id for c in data.categories(s.id) for e in data.edges(s.id, c))
            for s in afr.sources()
        )
    )
    for o in orphans:
        warnings.append("%s: no source taxonomy maps to it (registry-only gap)" % o)

    for w in warnings:
        print("warn  %s" % w)
    for e in errors:
        print("ERROR %s" % e)
    print(
        "\n%d modes, %d sources, %d errors, %d warnings"
        % (len(modes), len(afr.sources()), len(errors), len(warnings))
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
