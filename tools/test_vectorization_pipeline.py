#!/usr/bin/env python3
"""Tests for ``pipelines.vectorization``.

Layers:

1. Unit tests for ``chunk_text`` (paragraph splitting, sliding window,
   absolute char offsets) and the ``hash`` embedding backend
   (determinism, dim, normalisation).
2. End-to-end CLI test that runs ``run_pipeline.py vectorization
   --backend hash`` against a synthetic record produced by
   ``pipelines.text`` and validates the descriptor against
   ``schemas/derived-asset.schema.json``.

We do NOT exercise the real ``sentence-transformers`` backend in CI:
loading the model would either require a network call or a multi-hundred-MB
local cache. The real backend is covered by manual smoke tests
(documented in PIPELINE_GUIDE.md, issue #38) and is structurally
identical to ``hash`` — both go through the same ``embed()`` dispatcher.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.vectorization.embed import (  # noqa: E402
    HASH_BACKEND_DIM,
    chunk_text,
    embed,
)

SCHEMA_PATH = ROOT / "schemas" / "derived-asset.schema.json"


def _assert(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def _unit_tests_chunk(errors: list[str]) -> None:
    # Two paragraphs separated by a blank line.
    text = "Hello world.\nThis is line two.\n\nA second paragraph here."
    chunks = chunk_text(text, max_chars=600, overlap_chars=80)
    _assert(len(chunks) == 2, f"expected 2 chunks, got {len(chunks)}", errors)
    if len(chunks) >= 2:
        _assert(
            chunks[0].text == "Hello world.\nThis is line two.",
            f"chunk[0].text wrong: {chunks[0].text!r}",
            errors,
        )
        _assert(
            text[chunks[0].char_start : chunks[0].char_end] == chunks[0].text,
            "chunk[0] char offsets do not slice back to chunk text",
            errors,
        )
        _assert(
            chunks[1].text == "A second paragraph here.",
            f"chunk[1].text wrong: {chunks[1].text!r}",
            errors,
        )

    # A long paragraph forces sliding windows.
    long_text = "x" * 1500
    long_chunks = chunk_text(long_text, max_chars=600, overlap_chars=100)
    _assert(len(long_chunks) >= 3, f"long paragraph should slide >=3 chunks, got {len(long_chunks)}", errors)
    if long_chunks:
        for i, c in enumerate(long_chunks):
            _assert(
                c.text == long_text[c.char_start : c.char_end],
                f"long_chunks[{i}] offsets do not slice back to chunk text",
                errors,
            )

    # Empty / whitespace-only paragraphs are dropped.
    sparse = "\n\n\n  \n\n\nactual content\n\n   \n"
    sparse_chunks = chunk_text(sparse, max_chars=600, overlap_chars=80)
    _assert(len(sparse_chunks) == 1, f"sparse should yield 1 chunk, got {len(sparse_chunks)}", errors)
    if sparse_chunks:
        _assert(sparse_chunks[0].text == "actual content", f"sparse text wrong: {sparse_chunks[0].text!r}", errors)


def _unit_tests_hash_backend(errors: list[str]) -> None:
    # Build chunks deterministically and embed twice; results must match.
    chunks = chunk_text("alpha bravo charlie\n\ndelta echo", max_chars=600, overlap_chars=80)
    a = embed(chunks, backend="hash")
    b = embed(chunks, backend="hash")
    _assert(a.dim == HASH_BACKEND_DIM, f"hash dim {a.dim} != {HASH_BACKEND_DIM}", errors)
    _assert(a.vectors == b.vectors, "hash backend not deterministic across calls", errors)

    # Different text -> different vectors (almost surely).
    other_chunks = chunk_text("zulu yankee xray\n\nwhiskey", max_chars=600, overlap_chars=80)
    c = embed(other_chunks, backend="hash")
    _assert(a.vectors[0] != c.vectors[0], "hash backend collided on distinct inputs", errors)

    # All vectors are unit-normalised (||v||_2 ~= 1) so cosine distance works.
    for i, v in enumerate(a.vectors):
        norm = math.sqrt(sum(x * x for x in v))
        if not (0.999 < norm < 1.001):
            errors.append(f"hash backend vector {i} not unit-normalised: ||v||={norm:.6f}")


def _make_synthetic_record(root: Path) -> Path:
    record = root / "dlrs_test_vec_001"
    derived_text = record / "derived" / "text"
    derived_text.mkdir(parents=True, exist_ok=True)
    (derived_text / "voice_master.clean.txt").write_text(
        "First paragraph about life.\n\n"
        "Second paragraph about memory and continuity.\n\n"
        "A third short closing paragraph.\n",
        encoding="utf-8",
    )
    (record / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "dlrs-manifest/1.0",
                "record_id": "dlrs_test_vec_001",
                "created_at": "2026-04-26T08:00:00Z",
                "artifacts": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return record


def _e2e_test(errors: list[str]) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        errors.append("jsonschema not installed; install via tools/requirements.txt")
        return

    with tempfile.TemporaryDirectory() as tmp:
        record = _make_synthetic_record(Path(tmp))
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "run_pipeline.py"),
            "vectorization",
            "--record",
            str(record),
            "--backend",
            "hash",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            errors.append(f"run_pipeline.py vectorization exited {proc.returncode}: {proc.stderr.strip()}")
            return

        derived = record / "derived" / "vectorization"
        index_path = derived / "voice_master.index.json"
        desc_path = derived / "voice_master.index.descriptor.json"

        for p in (index_path, desc_path):
            _assert(p.exists(), f"missing output {p}", errors)

        if index_path.exists():
            payload = json.loads(index_path.read_text(encoding="utf-8"))
            _assert(payload.get("backend") == "hash", "index.backend != hash", errors)
            _assert(payload.get("dim") == HASH_BACKEND_DIM, f"index.dim != {HASH_BACKEND_DIM}", errors)
            entries = payload.get("entries", [])
            _assert(len(entries) >= 3, f"expected >=3 entries, got {len(entries)}", errors)
            if entries:
                _assert(
                    "vector" in entries[0] and len(entries[0]["vector"]) == HASH_BACKEND_DIM,
                    "index entry missing vector or wrong dim",
                    errors,
                )
                _assert(
                    entries[0].get("text_sha256", "").startswith("sha256:"),
                    "index entry text_sha256 not sha256:",
                    errors,
                )

        if desc_path.exists():
            d = json.loads(desc_path.read_text(encoding="utf-8"))
            schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
            schema_errors = sorted(Draft202012Validator(schema).iter_errors(d), key=lambda e: e.path)
            for se in schema_errors:
                errors.append(
                    f"vec descriptor schema error at {'/'.join(map(str, se.path)) or '<root>'}: {se.message}"
                )
            _assert(d.get("pipeline") == "vectorization", "descriptor.pipeline != vectorization", errors)
            _assert(
                d.get("output", {}).get("path", "").startswith("derived/vectorization/"),
                "descriptor.output.path doesn't start with derived/vectorization/",
                errors,
            )
            _assert(
                d.get("model", {}).get("online_api_used") is False,
                "descriptor.model.online_api_used is not False",
                errors,
            )


def main() -> int:
    errors: list[str] = []
    _unit_tests_chunk(errors)
    _unit_tests_hash_backend(errors)
    _e2e_test(errors)

    if errors:
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(f"test_vectorization_pipeline: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("test_vectorization_pipeline: chunk + hash backend + end-to-end OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
