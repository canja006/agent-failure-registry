"""Registry loading.

The canonical registry is YAML under ``registry/`` for human editing. At build
time it is compiled to a single JSON index shipped inside the package, so the
runtime has zero third-party dependencies. Run ``make build`` after editing
any YAML.
"""

import json
import os
from typing import Dict, List

from .model import Mapping, Mode, Source

_INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_index.json")

_cache = None


def _load() -> dict:
    global _cache
    if _cache is None:
        if not os.path.exists(_INDEX_PATH):
            raise RuntimeError(
                "registry index missing at %s - run `make build`" % _INDEX_PATH
            )
        with open(_INDEX_PATH, "r") as fh:
            _cache = json.load(fh)
    return _cache


def reload() -> None:
    """Drop the cached index. Useful in tests and after a rebuild."""
    global _cache
    _cache = None


def version() -> str:
    return _load().get("version", "0")


def modes() -> List[Mode]:
    """Every mode in the registry, ordered by id."""
    return [Mode(**m) for m in _load()["modes"]]


def mode(af_id: str) -> Mode:
    """Look up a single mode. Raises KeyError if unknown."""
    for m in _load()["modes"]:
        if m["id"] == af_id:
            return Mode(**m)
    raise KeyError("unknown mode: %s" % af_id)


def sources() -> List[Source]:
    return [Source(**s) for s in _load()["sources"]]


def source(source_id: str) -> Source:
    for s in _load()["sources"]:
        if s["id"] == source_id:
            return Source(**s)
    raise KeyError("unknown source: %s" % source_id)


def categories(source_id: str) -> List[str]:
    """Every category name declared by a source taxonomy."""
    edges = _load()["edges"].get(source_id)
    if edges is None:
        raise KeyError("unknown source: %s" % source_id)
    return sorted(edges.keys())


def _titles() -> Dict[str, str]:
    return {m["id"]: m["title"] for m in _load()["modes"]}


def edges(source_id: str, category: str) -> List[Mapping]:
    """Raw mappings for one category of one source."""
    src = _load()["edges"].get(source_id)
    if src is None:
        raise KeyError("unknown source: %s" % source_id)
    entry = src.get(category)
    if entry is None:
        raise KeyError("unknown category %r in source %r" % (category, source_id))
    titles = _titles()
    return [
        Mapping(
            id=e["id"],
            relation=e["relation"],
            title=titles.get(e["id"], ""),
            source=source_id,
            category=category,
            note=entry.get("note", ""),
        )
        for e in entry["af"]
    ]
