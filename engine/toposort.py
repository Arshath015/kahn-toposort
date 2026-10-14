"""Implementation of Kahn's algorithm for topological sorting.

The engine reads a dependency map from a configuration file and
produces a deterministic ordering of nodes.  It raises a
DependencyCycleError when the input graph contains a cycle.
"""

from __future__ import annotations

import collections
from pathlib import Path
from typing import Dict, List, Iterable
import yaml


class DependencyCycleError(RuntimeError):
    """Raised when the dependency graph contains a cycle."""

    def __init__(self, remaining: Iterable[str]):
        nodes = ", ".join(sorted(remaining))
        super().__init__(f"Cycle detected among nodes: {nodes}")
        self.remaining = set(remaining)


class TopoSorter:
    """Core class that performs topological sorting using Kahn's algorithm.

    Parameters
    ----------
    config_path: str or Path
        Path to a YAML file that defines a mapping ``node -> [dependencies]``.
    """

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.graph: Dict[str, List[str]] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load the YAML configuration into ``self.graph``.

        The YAML must be a mapping where each key is a node identifier and the
        value is a list of identifiers that the key depends on.  Missing nodes
        are added automatically with an empty dependency list.
        """
        with self.config_path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        if not isinstance(raw, dict):
            raise ValueError("Configuration must be a mapping of node -> dependencies")
        # Normalise to list of strings
        for node, deps in raw.items():
            if deps is None:
                deps = []
            if not isinstance(deps, list):
                raise ValueError(f"Dependencies for node '{node}' must be a list")
            self.graph[str(node)] = [str(d) for d in deps]
        # Ensure all referenced nodes exist in the graph
        for deps in self.graph.values():
            for d in deps:
                self.graph.setdefault(d, [])

    def sort(self) -> List[str]:
        """Return a topological ordering of the nodes.

        Implements Kahn's algorithm:
        1. Compute in‑degree for each node.
        2. Repeatedly remove nodes with in‑degree 0 and update neighbours.
        3. If nodes remain, a cycle exists.
        """
        # Compute in‑degree
        in_degree = collections.Counter()
        for node in self.graph:
            in_degree[node] = 0
        for node, deps in self.graph.items():
            for dep in deps:
                in_degree[dep] += 1
        # Initialise queue with zero in‑degree nodes (sorted for determinism)
        zero_queue = collections.deque(sorted([n for n, deg in in_degree.items() if deg == 0]))
        order: List[str] = []
        while zero_queue:
            n = zero_queue.popleft()
            order.append(n)
            for m in self.graph[n]:
                in_degree[m] -= 1
                if in_degree[m] == 0:
                    zero_queue.append(m)
        if len(order) != len(self.graph):
            remaining = [n for n, deg in in_degree.items() if deg > 0]
            raise DependencyCycleError(remaining)
        return order

    def __call__(self) -> List[str]:
        """Convenient shortcut so the instance can be called directly."""
        return self.sort()
