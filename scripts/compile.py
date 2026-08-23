#!/usr/bin/env python3
"""Compile the YAML registry into the JSON index the library ships.

Maintainer-only: this is the single place PyYAML is required. The runtime
package reads only the compiled JSON, so `afr` itself has no dependencies.

    python3 scripts/compile.py
"""

import hashlib
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required to build the index: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODES = os.path.join(ROOT, "registry", "modes")
CROSS = os.path.join(ROOT, "registry", "crosswalk")
OUT = os.path.join(ROOT, "afr", "_index.json")

MODE_FIELDS = (
    "id", "title", "status", "layer", "description", "symptoms",
    "discriminators", "near_neighbors", "references", "examples",
)
SOURCE_FIELDS = (
    "id", "name", "vendor", "url", "license", "taxonomy_size", "observed",
)


def load_modes():
    modes = []
    for name in sorted(os.listdir(MODES)):
        if not name.endswith(".yaml"):
            continue
        with open(os.path.join(MODES, name)) as fh:
            raw = yaml.safe_load(fh)
        record = {k: raw.get(k) for k in MODE_FIELDS}
        record["description"] = (record.get("description") or "").strip()
        for key in ("symptoms", "discriminators", "near_neighbors", "references", "examples"):
            record[key] = list(record.get(key) or [])
        modes.append(record)
    return modes


def load_crosswalks():
    sources, edges = [], {}
    for name in sorted(os.listdir(CROSS)):
        if not name.endswith(".yaml"):
            continue
        with open(os.path.join(CROSS, name)) as fh:
            raw = yaml.safe_load(fh)
        src = raw["source"]
        sources.append({k: src.get(k) or ("" if k != "taxonomy_size" else 0)
                        for k in SOURCE_FIELDS})
        table = {}
        for m in raw.get("mappings") or []:
            table[m["category"]] = {
                "af": [{"id": e["id"], "relation": e["relation"]}
                       for e in (m.get("af") or [])],
                "note": (m.get("note") or "").strip(),
            }
        edges[src["id"]] = table
    return sources, edges


def main():
    modes = load_modes()
    sources, edges = load_crosswalks()
    payload = {"modes": modes, "sources": sources, "edges": edges}
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()[:12]
    payload["version"] = digest
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")
    edge_count = sum(len(e["af"]) for t in edges.values() for e in t.values())
    print("index %s -> %d modes, %d sources, %d categories, %d edges"
          % (digest, len(modes), len(sources),
             sum(len(t) for t in edges.values()), edge_count))


if __name__ == "__main__":
    main()
