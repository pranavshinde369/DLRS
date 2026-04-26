#!/usr/bin/env python3
"""DLRS pipeline dispatcher.

Usage::

    python tools/run_pipeline.py --list                       # enumerate pipelines
    python tools/run_pipeline.py asr --help                   # help for one pipeline
    python tools/run_pipeline.py asr --record <path> [...]    # run a pipeline

Every pipeline is implemented as a sub-package under ``pipelines/`` that
exports a :class:`pipelines.PipelineSpec` named ``SPEC``. This script is
intentionally thin so future pipelines can be added without changing the CLI.

The ``--list`` mode is dependency-free: heavy optional libraries
(faster-whisper, sentence-transformers, qdrant-client, …) are NOT imported
when listing or printing help. They are only imported by each pipeline's
``run`` function when actually invoked.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines import PipelineSpec, load_specs  # noqa: E402


def _print_list(specs: list[PipelineSpec]) -> int:
    print(f"{'name':<16}{'inputs':<40}{'outputs':<40}description")
    print("-" * 120)
    for s in specs:
        inputs = ",".join(s.inputs)[:38]
        outputs = ",".join(s.outputs)[:38]
        print(f"{s.name:<16}{inputs:<40}{outputs:<40}{s.description}")
    return 0


def main() -> int:
    specs = load_specs()
    by_name = {s.name: s for s in specs}

    parser = argparse.ArgumentParser(
        prog="run_pipeline",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--list", action="store_true", help="List all registered pipelines and exit.")

    sub = parser.add_subparsers(dest="pipeline", help="Pipeline to run.")
    for spec in specs:
        sp = sub.add_parser(
            spec.name,
            help=spec.description,
            description=f"{spec.description}\n\n"
                        f"Inputs:  {', '.join(spec.inputs)}\n"
                        f"Outputs: {', '.join(spec.outputs)}\n"
                        f"Deps:    {', '.join(spec.dependencies) or '(none)'}\n"
                        f"Output:  {spec.output_pointer_template}",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        spec.register(sp)

    args = parser.parse_args()

    if args.list or args.pipeline is None:
        return _print_list(specs)

    spec = by_name[args.pipeline]
    return spec.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
