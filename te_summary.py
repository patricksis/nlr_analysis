#!/usr/bin/env python3
# Summarize TE counts and classes per NLR neighborhood.
# Usage: python3 te_summary.py <workdir> <sample>

import sys
import pandas as pd

workdir = sys.argv[1]
sample = sys.argv[2]

cols = [
    "nbh_chr", "nbh_start", "nbh_end", "neighborhood_id",
    "te_chr", "te_start", "te_end", "te_info"
]
df = pd.read_csv(f"{workdir}/{sample}.tes_in_neighborhoods.bed", sep="\t", header=None, names=cols)

# Count TEs per neighborhood
counts = df.groupby("neighborhood_id").size().reset_index(name="TE_count")
counts.to_csv(f"{workdir}/{sample}.te_counts_per_neighborhood.tsv", sep="\t", index=False)

# TE class breakdown
def parse_class(info):
    for field in info.split(";"):
        if "Classification=" in field:
            return field.split("=")[1]
    return "Unknown"

df["TE_class"] = df["te_info"].apply(parse_class)
class_summary = df.groupby(["neighborhood_id", "TE_class"]).size().reset_index(name="count")
class_summary.to_csv(f"{workdir}/{sample}.te_class_counts.tsv", sep="\t", index=False)
