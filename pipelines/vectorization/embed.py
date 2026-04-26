"""Chunking + embedding backends.

Two backends:

- ``hash`` — deterministic, dependency-free. Produces a fixed-dim vector
  by deriving floats from ``sha256(chunk_index || chunk_text)``. Used for
  tests, examples, and CI; offline-first.
- ``sentence-transformers`` — real semantic embeddings. The library is
  imported lazily so the rest of the module (and the CLI's ``--help``)
  works on machines without it installed.

Chunking is paragraph-aware: text is split on blank-line boundaries, and
any paragraph longer than ``max_chars`` is sliced into overlapping
windows so a single huge wall of text still produces multiple embeddable
units.
"""
from __future__ import annotations

import hashlib
import re
import struct
from dataclasses import dataclass, field
from typing import List, Optional

CHUNKER_VERSION = "1.0"
HASH_BACKEND_DIM = 64
HASH_BACKEND_VERSION = "1.0"


@dataclass(frozen=True)
class Chunk:
    """A single embeddable unit with absolute character offsets."""

    chunk_id: int
    text: str
    char_start: int
    char_end: int

    def text_sha256(self) -> str:
        return "sha256:" + hashlib.sha256(self.text.encode("utf-8")).hexdigest()


@dataclass
class EmbeddingResult:
    backend: str
    model_id: str
    dim: int
    chunks: List[Chunk] = field(default_factory=list)
    vectors: List[List[float]] = field(default_factory=list)


_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")


def chunk_text(text: str, max_chars: int = 600, overlap_chars: int = 80) -> List[Chunk]:
    """Split text into paragraph-aware chunks with absolute char offsets.

    Empty / whitespace-only paragraphs are dropped. The returned offsets
    point into the *input* string so downstream tooling can highlight
    matches without re-finding them.
    """
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if overlap_chars < 0 or overlap_chars >= max_chars:
        raise ValueError("overlap_chars must be in [0, max_chars)")

    chunks: List[Chunk] = []
    cursor = 0
    chunk_id = 0
    for paragraph_match in _split_with_offsets(text, _PARAGRAPH_BREAK):
        para = paragraph_match[0]
        para_start = paragraph_match[1]
        stripped = para.strip()
        if not stripped:
            continue
        leading = len(para) - len(para.lstrip())
        absolute_start = para_start + leading
        for sub_start, sub_end in _windowed_offsets(len(stripped), max_chars, overlap_chars):
            sub_text = stripped[sub_start:sub_end]
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    text=sub_text,
                    char_start=absolute_start + sub_start,
                    char_end=absolute_start + sub_end,
                )
            )
            chunk_id += 1
        cursor = para_start + len(para)
    _ = cursor  # keep flake happy; cursor is implicit via paragraph offsets
    return chunks


def _split_with_offsets(text: str, sep: re.Pattern[str]):
    """Yield (substring, start_offset) pairs split by ``sep``."""
    last = 0
    for m in sep.finditer(text):
        yield text[last:m.start()], last
        last = m.end()
    yield text[last:], last


def _windowed_offsets(length: int, window: int, overlap: int):
    """Yield (start, end) windows over [0, length) with overlap."""
    if length <= window:
        yield 0, length
        return
    stride = window - overlap
    start = 0
    while start < length:
        end = min(start + window, length)
        yield start, end
        if end == length:
            break
        start += stride


def embed(
    chunks: List[Chunk],
    *,
    backend: str,
    model: Optional[str] = None,
    device: str = "cpu",
) -> EmbeddingResult:
    """Dispatch to the chosen backend."""
    if backend == "hash":
        return _embed_hash(chunks)
    if backend == "sentence-transformers":
        return _embed_sentence_transformers(chunks, model=model, device=device)
    raise ValueError(f"unknown embedding backend: {backend!r}")


def _embed_hash(chunks: List[Chunk]) -> EmbeddingResult:
    """Deterministic 64-D float vectors derived from sha256 of (id || text)."""
    dim = HASH_BACKEND_DIM
    vectors: List[List[float]] = []
    for chunk in chunks:
        seed = f"{chunk.chunk_id}\x00{chunk.text}".encode("utf-8")
        # Need 4 bytes per float, so dim*4 bytes total. Each sha256 is 32
        # bytes, so we walk multiple sha256 rounds with a counter.
        bytes_needed = dim * 4
        buf = bytearray()
        counter = 0
        while len(buf) < bytes_needed:
            buf.extend(hashlib.sha256(seed + counter.to_bytes(2, "big")).digest())
            counter += 1
        floats: List[float] = []
        for i in range(dim):
            (raw,) = struct.unpack("<I", bytes(buf[i * 4 : i * 4 + 4]))
            # Map to [-1, 1] without trig functions for full determinism.
            floats.append((raw / 0xFFFFFFFF) * 2.0 - 1.0)
        norm = sum(f * f for f in floats) ** 0.5
        if norm > 0:
            floats = [f / norm for f in floats]
        vectors.append(floats)
    return EmbeddingResult(
        backend="hash",
        model_id=f"hash:sha256:dim={dim}",
        dim=dim,
        chunks=list(chunks),
        vectors=vectors,
    )


def _embed_sentence_transformers(
    chunks: List[Chunk],
    *,
    model: Optional[str],
    device: str,
) -> EmbeddingResult:
    from sentence_transformers import SentenceTransformer  # type: ignore

    model_id = model or "sentence-transformers/all-MiniLM-L6-v2"
    encoder = SentenceTransformer(model_id, device=device)
    texts = [c.text for c in chunks]
    raw_vecs = encoder.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    dim = int(raw_vecs.shape[1]) if len(raw_vecs) else 0
    vectors = [list(map(float, vec)) for vec in raw_vecs]
    return EmbeddingResult(
        backend="sentence-transformers",
        model_id=model_id,
        dim=dim,
        chunks=list(chunks),
        vectors=vectors,
    )
