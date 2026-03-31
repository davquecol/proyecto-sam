#!/usr/bin/env python3
"""Mapping quality statistics from SAM files."""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

MAPQ_THRESHOLD = 60


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse a SAM file and report MAPQ statistics.",
    )
    parser.add_argument("sam_file", type=Path, help="Path to the SAM file")
    parser.add_argument(
        "--tsv",
        type=Path,
        default=None,
        metavar="FILE",
        help="Write results to a TSV file (FAIR interoperability)",
    )
    return parser.parse_args()


def analyze_sam(sam_path: Path, threshold: int) -> tuple[int, int]:
    """Read a SAM file and return (total_reads, mapq_hits).

    Header lines starting with '@' are skipped.
    MAPQ is in column 5 of the SAM format (0-indexed column 4).
    """
    total = 0
    mapq_hits = 0
    with open(sam_path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("@"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 5:
                continue
            total += 1
            try:
                if int(fields[4]) == threshold:
                    mapq_hits += 1
            except ValueError:
                pass
    return total, mapq_hits


def print_results(sam_name: str, total: int, hits: int, threshold: int) -> None:
    """Format and display results using rich."""
    pct = (hits / total * 100) if total > 0 else 0.0
    console = Console()
    table = Table(title=f"SAM Analysis · {sam_name}", header_style="bold magenta")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="green", justify="right")
    table.add_row("Total aligned reads", f"{total:,}")
    table.add_row(f"Reads with MAPQ = {threshold}", f"{hits:,}")
    table.add_row("Percentage", f"{pct:.1f}%")
    console.print(table)


def write_tsv(output_path: Path, total: int, hits: int, threshold: int) -> None:
    """Write results to a TSV file for machine readability (FAIR)."""
    pct = (hits / total * 100) if total > 0 else 0.0
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("metric\tvalue\n")
        fh.write(f"total_aligned_reads\t{total}\n")
        fh.write(f"reads_mapq_{threshold}\t{hits}\n")
        fh.write(f"percentage_mapq_{threshold}\t{pct:.1f}\n")


def main() -> None:
    args = parse_args()
    if not args.sam_file.exists():
        Console().print(f"[bold red]ERROR:[/bold red] File not found: {args.sam_file}")
        sys.exit(1)
    total, hits = analyze_sam(args.sam_file, MAPQ_THRESHOLD)
    print_results(args.sam_file.name, total, hits, MAPQ_THRESHOLD)
    if args.tsv:
        write_tsv(args.tsv, total, hits, MAPQ_THRESHOLD)
        Console().print(f"[dim]TSV written to: {args.tsv}[/dim]")


if __name__ == "__main__":
    main()
