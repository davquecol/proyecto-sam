# proyecto-sam

Command-line tool to compute MAPQ mapping quality statistics from SAM files.
Parses aligned reads, counts those with MAPQ = 60, and reports the percentage.

## Requirements

- [uv](https://docs.astral.sh/uv/) >= 0.4
- [Nextflow](https://nextflow.io) >= 23.10
- Java 17–25 (required by Nextflow)

## Installation

```bash
git clone https://github.com/davquecol/proyecto-sam.git
cd proyecto-sam
uv sync
```

## Usage

### Directly with uv

```bash
uv run main.py /path/to/file.sam
```

With machine-readable output:

```bash
uv run main.py /path/to/file.sam --tsv results.tsv
```

### Via the Nextflow pipeline

```bash
nextflow run main.nf --sam /path/to/file.sam
```

## Project structure

| File | Description |
|---|---|
| `main.py` | Main analysis script |
| `main.nf` | Nextflow pipeline |
| `pyproject.toml` | Project metadata and dependencies |
| `uv.lock` | Reproducible dependency lockfile |
| `LICENSE` | MIT licence |
| `CITATION.cff` | Citation metadata |

## Expected output

```
    SAM Analysis · Col0.1.sam
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Metric               ┃   Value ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ Total aligned reads  │ 203,807 │
│ Reads with MAPQ = 60 │ 196,184 │
│ Percentage           │   96.3% │
└──────────────────────┴─────────┘
```

## Licence

MIT — see [LICENSE](LICENSE) for details.
