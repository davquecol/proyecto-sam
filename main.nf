#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

// ── Parameters ────────────────────────────────────────────────
// --sam is mandatory; the pipeline fails explicitly if omitted
params.sam = null

// ── Process ───────────────────────────────────────────────────
process analyze_sam {

    tag "${sam_file.name}"

    publishDir "${launchDir}/results", mode: 'copy', overwrite: true

    input:
    path sam_file

    output:
    stdout

    script:
    // realpath resolves the Nextflow work/ symlink to an absolute path
    // so that uv --directory does not lose track of the input file
    """
    uv run --directory ${projectDir} main.py \$(realpath ${sam_file})
    """
}

// ── Workflow ──────────────────────────────────────────────────
workflow {

    if ( !params.sam ) {
        error "ERROR: please provide a SAM file with --sam <path>"
    }

    sam_ch = Channel.fromPath( params.sam, checkIfExists: true )

    analyze_sam( sam_ch ) | view
}
