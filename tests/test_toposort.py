import pathlib

from engine.toposort import TopoSorter


def test_basic_sort(tmp_path: pathlib.Path):
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text("""
X: []
Y: [X]
Z: [Y]
""")
    sorter = TopoSorter(cfg)
    assert sorter.sort() == ["X", "Y", "Z"]


def test_multiple_independent(tmp_path: pathlib.Path):
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text("""
A: []
B: []
C: [A, B]
""")
    sorter = TopoSorter(cfg)
    order = sorter.sort()
    # A and B can appear in any order before C
    assert order[-1] == "C"
    assert set(order[:2]) == {"A", "B"}
