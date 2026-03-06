#!/usr/bin/env python3
# Parse NLR-Annotator/NLR-Tracker output into BED format.
# Usage: python3 parse_nlrs.py <nlr_tracker.tsv> <output.bed>

import sys
import pandas as pd

nlr_tracker = sys.argv[1]
output_bed = sys.argv[2]

df = pd.read_csv(nlr_tracker, sep="\t", dtype=str)
df_nlr = df[df["Status"] == "NLR"]
df_nlr_unique = df_nlr.drop_duplicates(subset="genename")
bed = df_nlr_unique[["chrom", "start", "end", "genename"]]
bed.to_csv(output_bed, sep="\t", index=False, header=False)
