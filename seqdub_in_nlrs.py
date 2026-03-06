#!/usr/bin/env python3
# Summarize segmental duplications overlapping NLRs.
# Usage: python3 seqdub_in_nlrs.py <workdir> <sample>

import sys
import pandas as pd

workdir = sys.argv[1]
sample = sys.argv[2]

df = pd.read_csv(f"{workdir}/{sample}.nlrs_in_duplications.bed", sep="\t", header=None)
df.columns = ["chr", "start", "end", "genename", "dup_chr", "dup_start", "dup_end"]

duplicated_nlrs = df["genename"].unique()
print(f"Duplicated NLRs: {len(duplicated_nlrs)}")

dup_counts = df["genename"].value_counts().reset_index()
dup_counts.columns = ["genename", "duplication_hits"]
dup_counts.to_csv(f"{workdir}/{sample}.duplication_counts_per_nlr.tsv", sep="\t", index=False)
