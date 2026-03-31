#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

params.sam = null

process analyze_sam {
    tag "${sam_file.name}"

    input:
    path sam_file

    output:
    stdout

    script:
    """
    uv run --directory ${projectDir} main.py \$(realpath ${sam_file})
    """
}

workflow {
    if ( !params.sam ) {
        error "ERROR: proporciona el fichero SAM con --sam <ruta>"
    }
    sam_ch = Channel.fromPath( params.sam, checkIfExists: true )
    analyze_sam( sam_ch ) | view
}
