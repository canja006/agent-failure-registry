"""Mapping between third-party taxonomies and AF mode ids."""

from typing import Dict, Iterable, List, Union

from . import data
from .model import Label, Mapping, invert


def map(source_id: str, category: str, strict: bool = False) -> List[Mapping]:
    """Map one source category to AF modes.

    Returns an empty list for categories that are deliberately unmapped -
    residual labels like ``Inconclusive``, non-failures, and genuine registry
    gaps. Pass ``strict=True`` to raise on categories the source has never
    declared, rather than returning an empty list.
    """
    try:
        return data.edges(source_id, category)
    except KeyError:
        if strict:
            raise
        return []


def unmap(af_id: str, source_id: str) -> List[Mapping]:
    """Map an AF mode back to a source's categories.

    Relations are inverted on the way back: a source category that is *broader*
    than the AF mode means the AF mode is *narrower* than it.
    """
    data.mode(af_id)  # raises KeyError on unknown ids
    out = []
    for category in data.categories(source_id):
        for edge in data.edges(source_id, category):
            if edge.id == af_id:
                out.append(
                    Mapping(
                        id=af_id,
                        relation=invert(edge.relation),
                        title=category,
                        source=source_id,
                        category=category,
                        note=edge.note,
                    )
                )
    return out


def normalize(
    report: Union[Iterable[str], Dict[str, int]], source_id: str
) -> List[Label]:
    """Tag a source tool's output with AF ids.

    Accepts either an iterable of category strings (one per classified run or
    step) or a mapping of category -> count, which is what most tools' summary
    reports already look like.
    """
    if isinstance(report, dict):
        counts = dict(report)
    else:
        counts = {}
        for category in report:
            counts[category] = counts.get(category, 0) + 1

    labels = []
    for category, count in counts.items():
        labels.append(
            Label(
                category=category,
                source=source_id,
                af=map(source_id, category),
                count=count,
            )
        )
    labels.sort(key=lambda l: (-l.count, l.category))
    return labels


def coverage(source_id: str) -> dict:
    """How much of a source taxonomy the registry currently covers."""
    cats = data.categories(source_id)
    mapped = [c for c in cats if data.edges(source_id, c)]
    return {
        "source": source_id,
        "categories": len(cats),
        "mapped": len(mapped),
        "unmapped": sorted(set(cats) - set(mapped)),
        "ratio": (len(mapped) / len(cats)) if cats else 0.0,
    }
