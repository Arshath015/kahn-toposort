"""Demo script that loads the example config and writes the sorted order.

The result is stored in ``results/output.txt`` so CI can verify the file
exists and contains a valid ordering.
"""

from pathlib import Path

from engine.toposort import TopoSorter


def main() -> None:
    config_path = Path(__file__).parents[1] / "config" / "example_config.yaml"
    sorter = TopoSorter(config_path)
    order = sorter.sort()
    result_dir = Path(__file__).parent / "results"
    result_dir.mkdir(exist_ok=True)
    out_file = result_dir / "output.txt"
    out_file.write_text(" -> ".join(order))
    print(f"Topological order written to {out_file}")


if __name__ == "__main__":
    main()
