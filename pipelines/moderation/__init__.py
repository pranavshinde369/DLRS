"""Content moderation pipeline.

v0.5 stub. Full implementation tracked by issue #34.
"""
from __future__ import annotations

import argparse
import sys

from pipelines import PipelineSpec


def _register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--record", required=False, help="Path to the record directory.")
    parser.add_argument("--input", required=False, help="Path to a cleaned text file.")
    parser.add_argument(
        "--lexicon",
        default=None,
        help="Optional YAML lexicon. Defaults to pipelines/moderation/lexicon.default.yaml.",
    )


def _run(args: argparse.Namespace) -> int:
    print(
        "[moderation] stub: moderation pipeline scaffold from v0.5 issue #30. "
        "Real lexicon scan + cross-border block arrives in issue #34.",
        file=sys.stderr,
    )
    return 0


SPEC = PipelineSpec(
    name="moderation",
    description="Offline keyword scan + cross-border-transfer enforcement.",
    inputs=["text.clean.txt"],
    outputs=["moderation_report.json"],
    dependencies=["pyyaml>=6.0"],
    output_pointer_template="derived/moderation/{stem}.report.json",
    register=_register,
    run=_run,
)
