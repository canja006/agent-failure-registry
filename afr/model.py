"""Core types for the Agent Failure Registry."""

from dataclasses import dataclass, field
from typing import List, Optional

RELATIONS = ("exact", "broader", "narrower", "overlaps")

# Strength order for picking a label's strongest mapping. Lower is stronger.
RELATION_STRENGTH = {"exact": 0, "narrower": 1, "broader": 2, "overlaps": 3}

#: Inverting a mapping swaps containment but preserves identity and overlap.
_INVERSE = {
    "exact": "exact",
    "broader": "narrower",
    "narrower": "broader",
    "overlaps": "overlaps",
}

LAYERS = ("model", "harness", "tool", "environment", "user-intent")


def invert(relation: str) -> str:
    """Flip a relation's direction.

    Relations are recorded as *AF mode relative to source category*. Reading a
    mapping backwards (AF -> source) therefore requires swapping broader and
    narrower; getting this wrong silently corrupts the crosswalk.
    """
    try:
        return _INVERSE[relation]
    except KeyError:
        raise ValueError("unknown relation: %r" % (relation,))


@dataclass(frozen=True)
class Mapping:
    """One edge between a source taxonomy category and an AF mode."""

    id: str
    relation: str
    title: str = ""
    source: str = ""
    category: str = ""
    note: str = ""

    def __post_init__(self):
        if self.relation not in RELATIONS:
            raise ValueError("unknown relation: %r" % (self.relation,))

    def __str__(self):
        return "%s (%s)" % (self.id, self.relation)

    # The README's first example is `afr.map(...)` at a REPL; the dataclass
    # repr would drown the two fields that matter in five that do not.
    __repr__ = __str__


@dataclass(frozen=True)
class Mode:
    """A failure mode. Permanent, versionless, citable."""

    id: str
    title: str
    status: str
    layer: str
    description: str = ""
    symptoms: List[str] = field(default_factory=list)
    discriminators: List[str] = field(default_factory=list)
    near_neighbors: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)

    def __str__(self):
        return "%s  %s" % (self.id, self.title)


@dataclass(frozen=True)
class Source:
    """A third-party taxonomy the registry maps onto."""

    id: str
    name: str
    vendor: str = ""
    url: str = ""
    license: str = ""
    taxonomy_size: int = 0
    observed: str = ""


@dataclass
class Label:
    """One classified step or run, after normalisation."""

    category: str
    source: str
    af: List[Mapping] = field(default_factory=list)
    count: int = 1

    @property
    def mapped(self) -> bool:
        return bool(self.af)

    @property
    def strongest(self) -> List[Mapping]:
        """Every mapping sharing the strongest relation this label carries.

        More than one when the crosswalk records genuine lossiness: four
        `narrower` edges mean the source category splits four ways, and the
        registry has no basis for calling one of them the answer.
        """
        if not self.af:
            return []
        rank = min(RELATION_STRENGTH.get(m.relation, 9) for m in self.af)
        return [m for m in self.af if RELATION_STRENGTH.get(m.relation, 9) == rank]

    @property
    def ambiguous(self) -> bool:
        """True when several mappings tie for strongest."""
        return len(self.strongest) > 1

    @property
    def best(self) -> Optional[Mapping]:
        """The single strongest mapping, or None when several tie.

        Returning None on a tie is deliberate. Which of several equally
        ranked modes happens to be listed first in a crosswalk file is not a
        fact about the failure, and letting file order decide meant a profile
        could change because a file was reordered - reported by the
        AgentDebugX maintainers, 2026-09-12. A tie is a statement that the
        source category is coarser than the registry, and callers should see
        it rather than be handed an arbitrary winner.
        """
        strongest = self.strongest
        return strongest[0] if len(strongest) == 1 else None
