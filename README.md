# proyecto-sam

Análisis de calidad de mapeo para ficheros SAM.
Cuenta lecturas totales y lecturas con MAPQ = 60.

## Requisitos

- [uv](https://docs.astral.sh/uv/) >= 0.4
- [Nextflow](https://nextflow.io) >= 23.10
- Java 17–25

## Instalación
```bash
git clone https://github.com/davquecol/proyecto-sam.git
cd proyecto-sam
uv sync
```

## Uso

### Directo con uv
```bash
uv run main.py /ruta/al/fichero.sam
```

### Con Nextflow
```bash
nextflow run main.nf --sam /ruta/al/fichero.sam
```

## Estructura

| Archivo | Descripción |
|---|---|
| `main.py` | Script principal de análisis |
| `main.nf` | Pipeline Nextflow |
| `pyproject.toml` | Metadatos y dependencias (uv) |
| `uv.lock` | Lockfile reproducible |

## Salida esperada
```
        Análisis SAM · Col0.1.sam
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Métrica                     ┃   Valor ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ Total de lecturas alineadas │ 203,807 │
│ Lecturas con MAPQ = 60      │ 196,184 │
│ Porcentaje                  │   96.3% │
└─────────────────────────────┴─────────┘
```
