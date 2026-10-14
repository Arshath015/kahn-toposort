import pathlib
import pytest

from engine.toposort import TopoSorter, DependencyCycleError


def test_cycle_detection(tmp_path: pathlib.Path):
    cfg = tmp_path / "cycle.yaml"
    cfg.write_text("""
A: [B]
B: [A]
""")
    sorter = TopoSorter(cfg)
    with pytest.raises(DependencyCycleError) as exc:
        sorter.sort()
    # Both nodes should be reported as part of the cycle
    assert exc.value.remaining == {"A", "B"}


def test_missing_node_auto_added(tmp_path: pathlib.Path):
    cfg = tmp_path / "missing.yaml"
    cfg.write_text("""
A: [B]
""")
    sorter = TopoSorter(cfg)
    # B is not defined explicitly but should be added with no deps
    assert sorter.sort() == ["B", "A"]
