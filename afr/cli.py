"""Command line interface.

    afr modes                            list every mode
    afr show AF-0142                     full record for one mode
    afr map agentrx "Invalid Invocation" source category -> AF ids
    afr unmap AF-0064 agent-xray         AF id -> a source's categories
    afr coverage                         how much of each taxonomy is mapped
    afr gaps                             unmapped categories and orphan modes
    afr profile counts.json -s agent-xray
                                         failure profile from a counts file
"""

import argparse
import json
import sys

from . import coverage as _coverage
from . import crosswalk, data, profile as _profile


def _p(*a):
    print(*a)


def cmd_modes(args):
    for m in data.modes():
        _p("%-9s %-12s %s" % (m.id, m.layer, m.title))
    _p("\n%d modes  (index %s)" % (len(data.modes()), data.version()))


def cmd_show(args):
    try:
        m = data.mode(args.id)
    except KeyError as exc:
        sys.exit(str(exc))
    _p("%s  %s" % (m.id, m.title))
    _p("status: %s    layer: %s" % (m.status, m.layer))
    _p("\n%s" % m.description)
    for header, items in (
        ("symptoms", m.symptoms),
        ("discriminators", m.discriminators),
    ):
        if items:
            _p("\n%s:" % header)
            for i in items:
                _p("  - %s" % i)
    if m.near_neighbors:
        _p("\nnear neighbors: %s" % ", ".join(m.near_neighbors))
    _p("\nmapped from:")
    any_edge = False
    for src in data.sources():
        for edge in crosswalk.unmap(m.id, src.id):
            any_edge = True
            _p("  %-12s %-34s %s" % (src.id, edge.category, edge.relation))
    if not any_edge:
        _p("  (nothing - this mode is a registry-only gap)")


def cmd_map(args):
    hits = crosswalk.map(args.source, args.category)
    if not hits:
        known = args.category in data.categories(args.source)
        _p("no AF mapping" if known else "unknown category %r" % args.category)
        return
    for h in hits:
        _p("%-9s %-10s %s" % (h.id, h.relation, h.title))
        if h.note:
            _p("           note: %s" % h.note)


def cmd_unmap(args):
    try:
        hits = crosswalk.unmap(args.id, args.source)
    except KeyError as exc:
        sys.exit(str(exc))
    if not hits:
        _p("%s has no mapping in %s" % (args.id, args.source))
        return
    for h in hits:
        _p("%-34s %s" % (h.category, h.relation))


def cmd_coverage(args):
    for src in data.sources():
        c = _coverage(src.id)
        _p("%-12s %3d/%-3d categories mapped  (%.0f%%)"
           % (src.id, c["mapped"], c["categories"], 100 * c["ratio"]))


def cmd_gaps(args):
    _p("source categories with no AF mode:")
    found = False
    for src in data.sources():
        for cat in _coverage(src.id)["unmapped"]:
            note = data._load()["edges"][src.id][cat].get("note", "")
            if note.startswith("GAP"):
                found = True
                _p("  %-12s %-26s %s" % (src.id, cat, note))
    if not found:
        _p("  (none flagged)")
    _p("\nAF modes no taxonomy maps to:")
    orphans = [m for m in data.modes() if not any(
        crosswalk.unmap(m.id, s.id) for s in data.sources())]
    for m in orphans or []:
        _p("  %-9s %s" % (m.id, m.title))
    if not orphans:
        _p("  (none)")


def cmd_profile(args):
    with open(args.file) as fh:
        payload = json.load(fh)
    labels = crosswalk.normalize(payload, args.source)
    _p(_profile(labels).render())


def build_parser():
    p = argparse.ArgumentParser(prog="afr", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("modes").set_defaults(fn=cmd_modes)
    sub.add_parser("coverage").set_defaults(fn=cmd_coverage)
    sub.add_parser("gaps").set_defaults(fn=cmd_gaps)

    s = sub.add_parser("show"); s.add_argument("id"); s.set_defaults(fn=cmd_show)

    s = sub.add_parser("map")
    s.add_argument("source"); s.add_argument("category")
    s.set_defaults(fn=cmd_map)

    s = sub.add_parser("unmap")
    s.add_argument("id"); s.add_argument("source")
    s.set_defaults(fn=cmd_unmap)

    s = sub.add_parser("profile")
    s.add_argument("file"); s.add_argument("-s", "--source", required=True)
    s.set_defaults(fn=cmd_profile)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
