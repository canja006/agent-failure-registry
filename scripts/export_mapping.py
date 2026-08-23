#!/usr/bin/env python3
"""Emit the vendor-facing mapping file we contribute to a source's own repo.

Generated, never hand-edited, so an upstream PR can never drift from the
registry it claims to reflect.

    python3 scripts/export_mapping.py agent-xray > afr-mapping.yaml
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import afr
from afr import data

REPO = "https://github.com/canja006/agent-failure-registry"


def render(source_id: str, date: str) -> str:
    src = afr.source(source_id)
    out = []
    w = out.append
    w("# Agent Failure Registry (AFR) mapping for %s" % src.name)
    w("# %s" % REPO)
    w("#")
    w("# Maps %s's categories onto AF-#### mode ids - a vendor-neutral" % src.name)
    w("# namespace shared across agent failure taxonomies, so a failure profile")
    w("# from this tool can be compared with one from any other.")
    w("#")
    w("# Informational only. Nothing in %s reads this file, and it adds" % src.name)
    w("# no dependency. AFR does not ask %s to change its taxonomy." % src.name)
    w("#")
    w("# `relation` describes the AF mode RELATIVE TO the %s category:" % src.name)
    w("#   exact    - same concept")
    w("#   narrower - the AF mode is narrower than this category")
    w("#   broader  - the AF mode is broader than this category")
    w("#   overlaps - partial; neither contains the other")
    w("#")
    w("# Generated from AFR index %s on %s." % (data.version(), date))
    w("# Corrections welcome as issues on the AFR repo.")
    w("")
    w('afr_index: "%s"' % data.version())
    w("source: %s" % source_id)
    w("")
    w("categories:")

    unmapped = []
    for cat in data.categories(source_id):
        edges = data.edges(source_id, cat)
        raw = data._load()["edges"][source_id][cat]
        if not edges:
            unmapped.append((cat, raw.get("note", "")))
            continue
        w("  %s:" % (cat if cat.replace("_", "").isalnum() else '"%s"' % cat))
        for e in edges:
            w("    - id: %s" % e.id)
            w("      relation: %s" % e.relation)
            w("      title: %s" % afr.mode(e.id).title)
        if raw.get("note"):
            w("    # %s" % raw["note"])

    if unmapped:
        w("")
        w("# Categories with no AF mode. Three different things:")
        w("#   - residual labels and non-failures (correct to leave empty)")
        w("#   - genuine registry gaps, marked GAP - these are AFR's roadmap")
        w("unmapped:")
        for cat, note in unmapped:
            w("  %s: \"%s\"" % (cat, note or "not a failure mode"))
    w("")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--date", default="2026-08-23")
    a = ap.parse_args()
    sys.stdout.write(render(a.source, a.date))
