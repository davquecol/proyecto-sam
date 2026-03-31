#!/usr/bin/env python3
"""Análisis de calidad de mapeo en ficheros SAM."""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

MAPQ_THRESHOLD = 60


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analiza un fichero SAM y reporta estadísticas de MAPQ.",
    )
    parser.add_argument("sam_file", type=Path, help="Ruta al fichero SAM")
    return parser.parse_args()


def analyze_sam(sam_path: Path, threshold: int) -> tuple[int, int]:
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
    pct = (hits / total * 100) if total > 0 else 0.0
    console = Console()
    table = Table(title=f"Análisis SAM · {sam_name}", header_style="bold magenta")
    table.add_column("Métrica", style="cyan", no_wrap=True)
    table.add_column("Valor", style="green", justify="right")
    table.add_row("Total de lecturas alineadas", f"{total:,}")
    table.add_row(f"Lecturas con MAPQ = {threshold}", f"{hits:,}")
    table.add_row("Porcentaje", f"{pct:.1f}%")
    console.print(table)


def main() -> None:
    args = parse_args()
    if not args.sam_file.exists():
        Console().print(f"[bold red]ERROR:[/bold red] Fichero no encontrado: {args.sam_file}")
        sys.exit(1)
    total, hits = analyze_sam(args.sam_file, MAPQ_THRESHOLD)
    print_results(args.sam_file.name, total, hits, MAPQ_THRESHOLD)


if __name__ == "__main__":
    main()
