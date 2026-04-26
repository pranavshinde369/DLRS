"""Text cleaning + sensitive-info redaction pipeline.

v0.5 stub. Full implementation tracked by issue #32.
"""
from __future__ import annotations

import argparse
import sys

from pipelines import PipelineSpec


def _register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--record", required=False, help="Path to the record directory.")
    parser.add_argument("--input", required=False, help="Path to the input text file.")
    parser.add_argument(
        "--mode",
        choices=["normalize", "redact", "both"],
        default="both",
        help="What to run: 'normalize' (NFKC+whitespace), 'redact' (sensitive info), or 'both'.",
    )


def _run(args: argparse.Namespace) -> int:
    print(
        "[text] stub: text cleaning pipeline scaffold from v0.5 issue #30. "
        "Real normalisation + redaction arrives in issue #32.",
        file=sys.stderr,
    )
    return 0


SPEC = PipelineSpec(
    name="text",
    description="Deterministic text normalisation and conservative sensitive-info redaction (offline).",
    inputs=["text/plain", "transcript.json"],
    outputs=["text.clean.txt", "text.redactions.json"],
    dependencies=[],
    output_pointer_template="derived/text/{stem}.clean.txt",
    register=_register,
    run=_run,
)
