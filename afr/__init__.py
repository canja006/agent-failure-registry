"""Agent Failure Registry - a neutral namespace for AI agent failure modes.

    >>> import afr
    >>> afr.map("agentrx", "Invalid Invocation")
    [AF-0023 (exact)]
    >>> afr.mode("AF-0023").layer
    'model'

Relations are recorded as *AF mode relative to source category*.
Data is CC0; this library is Apache-2.0.
"""

from .crosswalk import coverage, map, normalize, unmap
from .data import categories, mode, modes, reload, source, sources, version
from .model import LAYERS, RELATIONS, Label, Mapping, Mode, Source, invert
from .profile import Profile, profile

__version__ = "0.4.0"

__all__ = [
    "map", "unmap", "normalize", "coverage",
    "mode", "modes", "source", "sources", "categories", "version", "reload",
    "profile", "Profile",
    "Mode", "Mapping", "Source", "Label", "invert",
    "RELATIONS", "LAYERS",
]
