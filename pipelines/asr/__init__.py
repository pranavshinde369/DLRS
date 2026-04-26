"""ASR (automatic speech recognition) pipeline.

This is a v0.5 stub. The full implementation arrives in a follow-up PR
tracked by issue #31. The stub exists so that:

- ``python tools/run_pipeline.py --list`` can enumerate the pipeline.
- ``python tools/run_pipeline.py asr --help`` works without faster-whisper
  installed.
- Future PRs only need to fill in the body of :func:`run`, not change the
  CLI contract.
"""
from __future__ import annotations

import argparse
import sys

from pipelines import PipelineSpec


def _register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--record",
        required=False,
        help="Path to the record directory (the folder that holds manifest.json).",
    )
    parser.add_argument(
        "--input",
        required=False,
        help="Path to the input audio file. Defaults to the manifest's first audio pointer.",
    )
    parser.add_argument(
        "--model",
        default="small",
        help="faster-whisper model id (tiny, base, small, medium, large-v3). Default: small.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="ISO-639-1 language hint (e.g. 'zh', 'en'). Auto-detect when omitted.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda"],
        help="Compute device. Default: cpu (offline-first).",
    )


def _run(args: argparse.Namespace) -> int:
    print(
        "[asr] stub: ASR pipeline scaffold from v0.5 issue #30. "
        "Real transcription arrives in issue #31.",
        file=sys.stderr,
    )
    print(
        "[asr] would transcribe: "
        f"record={args.record!r} input={args.input!r} model={args.model!r}",
        file=sys.stderr,
    )
    return 0


SPEC = PipelineSpec(
    name="asr",
    description="Speech-to-text transcription with timestamps (default: faster-whisper, offline).",
    inputs=["audio/wav", "audio/mp3", "audio/m4a", "audio/flac"],
    outputs=["transcript.json"],
    dependencies=["faster-whisper>=1.0"],
    output_pointer_template="derived/asr/{stem}.transcript.json",
    register=_register,
    run=_run,
)
