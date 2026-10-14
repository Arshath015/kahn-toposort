# Configuration‑driven Topological Sort – Analysis

The engine demonstrates how a pure‑YAML configuration can drive a classic
algorithm without any code changes.  Two observations are noteworthy:

1. **Deterministic ordering** – By sorting the initial zero‑in‑degree queue we
   guarantee that runs on the same config produce identical results, even when
   the graph contains multiple independent components.
2. **Implicit node creation** – Nodes that appear only as dependencies are
   auto‑added with an empty dependency list.  This mirrors real‑world package
   managers where a package may depend on a library that is not otherwise
   listed as a top‑level entry.

When a cycle is introduced the ``DependencyCycleError`` reports the exact set
of offending nodes, allowing callers to surface a helpful diagnostic to the
user or to a CI pipeline.
