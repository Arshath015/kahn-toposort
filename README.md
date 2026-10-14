# Kahn's Algorithm Topological Sort Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

Fast, config‑driven dependency resolver for DAGs.

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Theoretical Background](#theoretical-background)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Analysis Document](#analysis-document)
- [Testing](#testing)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

## Overview
This submodule provides a deterministic topological sort based on Kahn's
algorithm.  Behaviour is entirely driven by a YAML configuration that maps each
node to its list of prerequisites.

## Tech Stack
- Python 3.9+
- PyYAML for configuration parsing
- Standard library collections, pathlib, typing

## Architecture
```text
kahn-toposort/
├─ engine/
│  ├─ __init__.py
│  └─ toposort.py   # Core implementation
├─ config/
│  └─ example_config.yaml
├─ tests/
│  ├─ test_toposort.py
│  └─ test_edge_cases.py
├─ examples/
│  └─ run_demo.py   # Generates results/output.txt
├─ docs/
│  └─ analysis.md   # Internal analysis of config‑driven design
└─ README.md
```

## Theoretical Background
Kahn's algorithm solves the topological ordering problem for directed acyclic
graphs (DAGs) in O(V + E) time.  It works by repeatedly removing nodes with zero
in‑degree and updating the in‑degree of their outgoing neighbours.  If at the
end any nodes remain, the graph contains a cycle and no valid ordering exists.

The algorithm is well suited for build systems, package managers, and any
scenario where a static dependency graph must be linearised.  Our implementation
adds two practical enhancements:
1. **Deterministic tie‑breaking** – When multiple nodes have zero in‑degree we
   process them in lexical order, ensuring repeatable results across runs.
2. **Implicit node handling** – Dependencies that are not explicitly declared
   become leaf nodes, mirroring real‑world tools that allow transitive
   dependencies without redundant configuration.

## Installation
```bash
git clone https://github.com/yourorg/kahn-toposort.git
cd kahn-toposort
pip install -r requirements.txt
```

## Usage
```python
from pathlib import Path
from engine.toposort import TopoSorter

config = Path('config/example_config.yaml')
order = TopoSorter(config)()
print(order)  # ['A', 'B', 'C', 'D', 'E']
```

Or run the bundled demo:
```bash
python examples/run_demo.py
```
The script writes the ordering to ``examples/results/output.txt``.

## API Reference
### class TopoSorter
- ``__init__(config_path: str | Path)`` – Load a YAML dependency map.
- ``sort() -> List[str]`` – Return a topological ordering or raise ``DependencyCycleError``.
- ``__call__() -> List[str]`` – Shortcut to ``sort``.

### class DependencyCycleError(RuntimeError)
- ``remaining: Set[str]`` – Nodes that participate in the detected cycle.

## Analysis Document
Further discussion of design decisions and edge‑case handling is available in
[`docs/analysis.md`](docs/analysis.md).

## Testing
Run the test suite with:
```bash
pytest -q
```
All tests validate correct ordering, cycle detection, and implicit node
creation.

## Limitations
- Only YAML configuration is supported; JSON would require a separate loader.
- The engine assumes the input graph fits in memory.

## Roadmap
- Add optional JSON config support.
- Provide a CLI wrapper for quick command‑line usage.
- Benchmark against other topological sort libraries.

## License
MIT License


---
**Last updated:** 2026-10-14
