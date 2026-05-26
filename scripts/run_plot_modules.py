#!/usr/bin/env python3
"""Run plot modules for specific CSV paths or all plots."""

import argparse
import subprocess
import sys

from src.plotting.plot_mapping import CSV_TO_PLOT_MODULES, plot_modules_for_csvs


def _run_module(module_name: str) -> None:
    subprocess.run(
        [sys.executable, "-m", f"src.plotting.{module_name}"],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run plot generation modules.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Run all plot modules (equivalent to make plots)",
    )
    group.add_argument(
        "--csv",
        nargs="+",
        metavar="CSV_PATH",
        help="Run plot modules affected by the given CSV paths",
    )
    args = parser.parse_args()

    if args.all:
        modules: set[str] = set()
        for csv_modules in CSV_TO_PLOT_MODULES.values():
            modules.update(csv_modules)
        module_list = sorted(modules)
    else:
        module_list = plot_modules_for_csvs(args.csv)

    for module_name in module_list:
        _run_module(module_name)


if __name__ == "__main__":
    main()
