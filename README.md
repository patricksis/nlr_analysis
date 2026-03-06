# NLR Analysis Pipeline

A pipeline for characterizing NLR (nucleotide-binding leucine-rich repeat) immune genes in plant genomes, analyzing their association with transposable elements (TEs) and segmental duplications.

## Overview

NLR genes are identified from NLR-Annotator/NLR-Tracker output, then intersected with TE annotations and segmental duplications to classify NLRs by genomic context. Outputs include per-NLR summary tables and BED files for TE-rich and duplicated NLR subsets.

## Dependencies

- [samtools](http://www.htslib.org/)
- [bedtools](https://bedtools.readthedocs.io/)
- Python: `pandas`

## Usage

```bash
bash all_commands.sh \
    -f genome.fasta \
    -g TE_intact.gff3 \
    -b segdups.bedpe \
    -n nlrtracker-merged-with-gene-coordinates.tsv \
    -r neighborhoods_final_renamed.bed \
    -w output_dir \
    -s sample_name
```

All flags are optional — defaults are shown with `bash all_commands.sh -h`.

## Pipeline Steps

| Step | Script | Description |
|------|--------|-------------|
| 1 | `all_commands.sh` | Index genome, extract `.genome` file |
| 2 | `parse_nlrs.py` | Parse NLR-Tracker TSV → NLR BED file |
| 3 | `all_commands.sh` | Extract segmental duplications from BEDPE |
| 4 | `all_commands.sh` | Clean TE GFF3 → BED format |
| 5 | `all_commands.sh` | Intersect TEs with NLR neighborhoods |
| 6 | `all_commands.sh` | Intersect NLRs with segmental duplications |
| 7 | `te_summary.py` | Count TEs per neighborhood + TE class breakdown |
| 8 | `seqdub_in_nlrs.py` | Count duplication hits per NLR |
| 9 | `summary_table.py` | Build per-NLR summary table |
| 10 | `nlr_dups.py` | Extract duplicated NLRs to BED |
| 11 | `nlr_rich_tes.py` | Extract TE-rich NLRs to BED |

## Input Files

| File | Description |
|------|-------------|
| `genome.fasta` | Reference genome |
| `TE_intact.gff3` | TE annotations (e.g. from EDTA or RepeatModeler) |
| `segdups.bedpe` | Segmental duplications (e.g. from BISER) |
| `nlrtracker-merged-with-gene-coordinates.tsv` | NLR-Tracker output with gene coordinates |
| `neighborhoods_final_renamed.bed` | NLR neighborhood regions |

## Output Files

All outputs are written to `<workdir>/` with `<sample>` prefix:

| File | Description |
|------|-------------|
| `<sample>.nlrs.bed` | NLR gene coordinates |
| `<sample>.segdups.bed` | Segmental duplication regions |
| `<sample>.tes.clean.bed` | Cleaned TE annotations |
| `<sample>.tes_in_neighborhoods.bed` | TEs overlapping NLR neighborhoods |
| `<sample>.nlrs_in_duplications.bed` | NLRs overlapping segmental duplications |
| `<sample>.te_counts_per_neighborhood.tsv` | TE count per neighborhood |
| `<sample>.te_class_counts.tsv` | TE class breakdown per neighborhood |
| `<sample>.duplication_counts_per_nlr.tsv` | Duplication hits per NLR |
| `<sample>.nlr_summary_table.tsv` | Full NLR summary with TE and duplication info |
| `<sample>.duplicated_nlrs.bed` | NLRs in segmental duplications |
| `<sample>.te_rich_nlrs.bed` | NLRs in TE-rich neighborhoods |
