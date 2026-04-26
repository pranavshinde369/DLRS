# DLRS build pipelines (v0.5, offline-first)

This directory hosts every pipeline that turns **raw artefacts** referenced
by `manifest.json` (audio, images, text, …) into **derived artefacts** that
runtime layers can consume (transcripts, cleaned text, embeddings,
moderation reports).

## Hard rules

1. **Offline-first.** No pipeline may call a hosted API. Heavy local
   dependencies (faster-whisper, sentence-transformers, qdrant-client,
   PyYAML, …) are *optional* — they are imported lazily inside `run()` so
   `python tools/run_pipeline.py --help` works on a bare Python install.
2. **Contract-driven.** Every sub-package exposes a module-level
   `SPEC: pipelines.PipelineSpec` so the dispatcher and the static
   validator (`tools/validate_pipelines.py`) can introspect the pipeline
   without importing those heavy dependencies.
3. **Append-only outputs.** Derived artefacts go under
   `<record>/derived/<pipeline>/` and SHOULD be paired with a
   derived-asset descriptor (schema added in issue #35).

## Running

```bash
# enumerate registered pipelines
python tools/run_pipeline.py --list

# read the pipeline-specific flags
python tools/run_pipeline.py asr --help

# run a pipeline (currently the v0.5 #30 stubs print TODO and exit 0)
python tools/run_pipeline.py asr --record humans/asia/cn/dlrs_94f1c9b8_lin-example
```

## Sub-packages

| Pipeline       | Issue | Status                          |
|----------------|-------|---------------------------------|
| `asr`          | #31   | scaffold only (this PR)         |
| `text`         | #32   | scaffold only (this PR)         |
| `vectorization`| #33   | scaffold only (this PR)         |
| `moderation`   | #34   | scaffold only (this PR)         |

The full implementations land in their own follow-up PRs to keep the
review surface small. This PR (#30 / #40) only ships the directory layout,
the `PipelineSpec` contract, the dispatcher, and the static validator.

## Validation

`tools/validate_pipelines.py` runs in CI (via `tools/batch_validate.py`)
and enforces:

- every `SPEC` declares `name`, `inputs`, `outputs`, `output_pointer_template`;
- `output_pointer_template` lives under `derived/`;
- no pipeline declares hosted-API dependencies via `online_apis_used`;
- `python tools/run_pipeline.py <name> --help` exits cleanly.
