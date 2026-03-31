# Final Project Report
## Curso de Competencias Básicas para Biología Computacional — CSIC

**Author:** David Quevedo  
**Repository:** https://github.com/davquecol/proyecto-sam  
**Date:** March 2026

---

## 1. What the program does

`main.py` is a command-line tool that parses a SAM (Sequence Alignment/Map) file and reports basic mapping quality statistics. The script reads the file line by line, skips all header lines (those starting with `@`), and extracts the MAPQ value from column 5 of each alignment record. It then computes three values: total number of aligned reads, number of reads with MAPQ = 60 — which in most short-read aligners indicates a uniquely and confidently mapped read — and the corresponding percentage.

Output is displayed as a formatted table using the `rich` library:

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

The script also accepts a `--tsv` flag to write the same results to a tab-separated file, which allows downstream tools or scripts to parse the output programmatically without depending on terminal formatting.

---

## 2. How to use it

### Requirements

- `uv` — Python package and environment manager
- `nextflow` — pipeline runner
- Java 17–25 — required by Nextflow

### Installation

```bash
git clone https://github.com/davquecol/proyecto-sam.git
cd proyecto-sam
uv sync
```

`uv sync` reads `uv.lock` and recreates the exact environment used during development. No further configuration is needed.

### Running directly

```bash
uv run main.py /path/to/file.sam
```

With TSV output:

```bash
uv run main.py /path/to/file.sam --tsv results.tsv
```

### Running via the Nextflow pipeline

```bash
nextflow run main.nf --sam /path/to/file.sam
```

The `--sam` parameter is mandatory. If not provided, the pipeline exits immediately with an explicit error message.

---

## 3. Project organisation

```
proyecto-sam/
├── main.py           # Analysis script
├── main.nf           # Nextflow pipeline
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # Pinned dependency lockfile
├── .python-version   # Python version pin
├── LICENSE           # MIT licence
├── CITATION.cff      # Citation metadata
├── README.md         # Usage documentation
└── .gitignore
```

`main.py` is divided into four functions with clearly separated responsibilities: `parse_args()` handles the command-line interface, `analyze_sam()` contains the core logic with no side effects beyond file reading, `print_results()` handles all terminal output via `rich`, and `write_tsv()` handles machine-readable output. `main()` orchestrates the three, validates the input file, and exits with a non-zero status code on error. This separation makes the analysis logic straightforward to test independently.

The only configurable constant, `MAPQ_THRESHOLD`, is defined at the top of the file rather than inline, so changing the threshold does not require reading through the logic.

---

## 4. Git usage

The repository history reflects the actual development sequence:

```
540752d  chore: FAIR compliance
5eb2d59  docs: fill README with installation and usage instructions
24ba208  docs: add README with usage examples
dd4335a  feat: add Nextflow pipeline with analyze_sam process
822b9eb  feat: add SAM parser with MAPQ=60 stats and rich output
eb95852  chore: init project with uv, add rich dependency
```

Commit messages follow the conventional commits convention (`feat:`, `chore:`, `docs:`). Each commit represents a stable, self-contained state of the project rather than a snapshot of work in progress.

Version control has been part of my regular workflow before this course. I currently maintain private GitHub repositories for the analysis scripts associated with unpublished manuscripts, where branches and commit history are used to track analytical decisions across revisions and to share reproducible code with co-authors before submission.

---

## 5. Environment — uv

All dependencies are managed with `uv`. The project was initialised and the only external dependency added as follows:

```bash
uv init proyecto-sam
uv add rich
```

This produced `pyproject.toml`, which declares the project metadata and dependencies, and `uv.lock`, a pinned dependency tree that guarantees reproducibility across machines and time. Both files are committed to the repository. Anyone cloning the repo can recreate the exact environment with `uv sync` and run the script with `uv run`, with no manual activation of virtual environments required.

The `pyproject.toml` was also enriched with project-level metadata — description, author, keywords, licence reference, and repository URL — following FAIR software principles to make the project findable and reusable beyond its immediate context.

---

## 6. FAIR principles

The project was developed with FAIR software principles in mind from the start, as these are directly relevant to reproducible research in computational biology.

**Findable.** The repository includes a `CITATION.cff` file, which GitHub renders as a "Cite this repository" button. The `pyproject.toml` contains structured metadata including description, keywords, and repository URL, making the project indexable by software registries.

**Accessible.** The repository is public on GitHub and accessible via standard HTTPS. The pinned `uv.lock` ensures that the software can be retrieved and installed in a reproducible state at any point in the future.

**Interoperable.** In addition to the terminal output formatted with `rich`, the `--tsv` flag writes results to a plain tab-separated file with a header row. This format can be read directly by R, Python, or any spreadsheet application without parsing terminal escape codes or table borders.

**Reusable.** The project includes an explicit MIT licence, which grants unrestricted reuse, modification, and redistribution. The README documents all commands needed to install and run the tool from scratch. The code itself avoids hardcoded paths or assumptions about the execution environment.

---

## 7. Problems encountered

### Java version incompatible with Nextflow

The shared research server (`salvia`, Ubuntu 22.04) had Java 11 installed by default. Nextflow requires Java 17–25. Since the server is a shared computing cluster with multiple concurrent users, installing system packages via `sudo` was not appropriate. I installed Java 21 (Temurin LTS) in my home directory using SDKMAN, which requires no elevated privileges:

```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 21.0.4-tem
```

### uv and Nextflow not available on the server

Neither `uv` nor `nextflow` were installed on the server, and the system package manager required administrator rights. Both were installed in the user home directory without `sudo`:

```bash
# uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# nextflow
curl -s https://get.nextflow.io | bash
mkdir -p ~/bin && mv nextflow ~/bin/
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
```

This is a common situation in shared HPC environments and it is useful to know that both tools support user-level installation cleanly.

### SAM file not found inside the Nextflow work directory

Nextflow runs each process in an isolated temporary subdirectory under `work/`, staging input files as symbolic links. When `uv run --directory <project_dir>` was used inside the process script, it changed the working directory to the project root, making the symlinked SAM file unreachable by its relative name. The fix was to resolve the symlink to its absolute path using `realpath` before passing it to the Python script:

```groovy
script:
"""
uv run --directory ${projectDir} main.py \$(realpath ${sam_file})
"""
```

`realpath` resolves the symlink at execution time regardless of where Nextflow runs the process, which is the correct approach whenever a tool changes the working directory internally.
