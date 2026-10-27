#!/usr/bin/env bash
# NLR and TE analysis pipeline.
# Usage: bash all_commands.sh [-f fasta] [-g gff3] [-b bedpe] [-n nlr_tracker] [-r neighborhoods] [-w workdir] [-s sample]

set -euo pipefail

# --- Defaults ---
FASTA="genome.fasta"
GFF="TE_intact.gff3"
BEDPE="segdups.bedpe"
NLR_TRACKER="nlrtracker-merged-with-gene-coordinates.tsv"
NEIGHBORHOODS="neighborhoods_final_renamed.bed"
WORKDIR="."
SAMPLE=$(basename "$FASTA" .fasta)

# --- Help menu ---
usage() {
  echo "Usage: $0 [-f fasta] [-g gff3] [-b bedpe] [-n nlr_tracker] [-r neighborhoods] [-w workdir] [-s sample]"
  exit 1
}

while getopts ":f:g:b:n:r:w:s:" opt; do
  case $opt in
    f) FASTA="$OPTARG" ;;
    g) GFF="$OPTARG" ;;
    b) BEDPE="$OPTARG" ;;
    n) NLR_TRACKER="$OPTARG" ;;
    r) NEIGHBORHOODS="$OPTARG" ;;
    w) WORKDIR="$OPTARG" ;;
    s) SAMPLE="$OPTARG" ;;
    *) usage ;;
  esac
done

echo "=== NLR & TE ANALYSIS PIPELINE ==="
echo "FASTA:         $FASTA"
echo "GFF:           $GFF"
echo "BEDPE:         $BEDPE"
echo "NLR TRACKER:   $NLR_TRACKER"
echo "NEIGHBORHOODS: $NEIGHBORHOODS"
echo "WORKDIR:       $WORKDIR"
echo "SAMPLE:        $SAMPLE"

mkdir -p "$WORKDIR"
cp "$NEIGHBORHOODS" "${WORKDIR}/${SAMPLE}.neighborhoods_final_renamed.bed"

# --- 1. Index genome and extract .genome file ---
echo "[1] Indexing genome..."
samtools faidx "$FASTA"
cut -f1,2 "${FASTA}.fai" > "${WORKDIR}/${SAMPLE}.genome"

# --- 2. Parse NLR tracker into BED ---
echo "[2] Generating NLR BED file..."
python3 parse_nlrs.py "$NLR_TRACKER" "${WORKDIR}/${SAMPLE}.nlrs.bed"

# --- 3. Extract segmental duplications from BEDPE ---
echo "[3] Extracting segmental duplications..."
cut -f1-3 "$BEDPE" > "${WORKDIR}/${SAMPLE}.segdups.bed"

# --- 4. Clean TE GFF3 to BED ---
echo "[4] Filtering TE GFF3 to BED format..."
awk -F'\t' '$3 == "repeat_region" || $9 !~ /Parent=/' "$GFF" | \
awk -F'\t' '{OFS="\t"; print $1, $4-1, $5, $9}' > "${WORKDIR}/${SAMPLE}.tes.clean.bed"

# --- 5. Intersect TEs with NLR neighborhoods ---
echo "[5] Finding TEs in neighborhoods..."
bedtools intersect -a "$NEIGHBORHOODS" -b "${WORKDIR}/${SAMPLE}.tes.clean.bed" -wa -wb \
    > "${WORKDIR}/${SAMPLE}.tes_in_neighborhoods.bed"

# --- 6. Intersect NLRs with segmental duplications ---
echo "[6] Finding duplicated NLRs..."
bedtools intersect -a "${WORKDIR}/${SAMPLE}.nlrs.bed" -b "${WORKDIR}/${SAMPLE}.segdups.bed" -wa -wb \
    > "${WORKDIR}/${SAMPLE}.nlrs_in_duplications.bed"

# --- 7. TE summary ---
echo "[7] Running TE summary..."
python3 te_summary.py "$WORKDIR" "$SAMPLE"

# --- 8. Duplication summary ---
echo "[8] Running duplication summary..."
python3 seqdub_in_nlrs.py "$WORKDIR" "$SAMPLE"

# --- 9. NLR summary table ---
echo "[9] Creating NLR summary table..."
python3 summary_table.py "$WORKDIR" "$SAMPLE"

# --- 10. Extract duplicated NLRs ---
echo "[10] Extracting duplicated NLRs..."
python3 nlr_dups.py "$WORKDIR" "$SAMPLE"

# --- 11. Extract TE-rich NLRs ---
echo "[11] Extracting TE-rich NLRs..."
python3 nlr_rich_tes.py "$WORKDIR" "$SAMPLE"

echo "Pipeline complete! Output files are in: $WORKDIR"
