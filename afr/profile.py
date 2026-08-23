"""Failure profiles - the report that replaces a single pass rate."""

from dataclasses import dataclass, field
from typing import Dict, List

from . import data
from .model import Label


@dataclass
class Profile:
    total: int = 0
    by_mode: Dict[str, int] = field(default_factory=dict)
    by_layer: Dict[str, int] = field(default_factory=dict)
    unmapped: Dict[str, int] = field(default_factory=dict)
    source: str = ""

    @property
    def unmapped_total(self) -> int:
        return sum(self.unmapped.values())

    def top(self, n: int = 5) -> List[tuple]:
        ranked = sorted(self.by_mode.items(), key=lambda kv: (-kv[1], kv[0]))
        return ranked[:n]

    def render(self, width: int = 34) -> str:
        """A plain-text failure profile, safe for CI logs."""
        if not self.total:
            return "no labels"
        lines = []
        head = "failure profile"
        if self.source:
            head += "  (source: %s, n=%d)" % (self.source, self.total)
        lines.append(head)
        lines.append("-" * (width + 34))
        for af_id, count in sorted(self.by_mode.items(), key=lambda kv: (-kv[1], kv[0])):
            pct = 100.0 * count / self.total
            bar = "#" * max(1, int(round(pct / 100.0 * width)))
            try:
                title = data.mode(af_id).title
            except KeyError:
                title = "?"
            lines.append(
                "%-9s %5.1f%%  %-*s  %s" % (af_id, pct, width, bar, title)
            )
        if self.unmapped:
            lines.append("-" * (width + 34))
            for cat, count in sorted(
                self.unmapped.items(), key=lambda kv: (-kv[1], kv[0])
            ):
                pct = 100.0 * count / self.total
                lines.append("%-9s %5.1f%%  %s" % ("unmapped", pct, cat))
        lines.append("-" * (width + 34))
        lines.append(
            "by layer: "
            + ", ".join(
                "%s=%d" % (k, v)
                for k, v in sorted(self.by_layer.items(), key=lambda kv: -kv[1])
            )
        )
        return "\n".join(lines)


def profile(labels: List[Label]) -> Profile:
    """Aggregate normalised labels into a failure profile.

    Only the strongest mapping per label is counted, so a category that maps to
    three AF modes does not inflate the totals.
    """
    p = Profile()
    for label in labels:
        p.total += label.count
        if not p.source:
            p.source = label.source
        best = label.best
        if best is None:
            p.unmapped[label.category] = p.unmapped.get(label.category, 0) + label.count
            continue
        p.by_mode[best.id] = p.by_mode.get(best.id, 0) + label.count
        try:
            layer = data.mode(best.id).layer
        except KeyError:
            layer = "unknown"
        p.by_layer[layer] = p.by_layer.get(layer, 0) + label.count
    return p
