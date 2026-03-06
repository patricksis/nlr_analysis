#!/usr/bin/env python3
# Build a summary table of NLRs with duplication and TE annotation.
# Usage: python3 summary_table.py <workdir> <sample>

import sys
import pandas as pd

workdir = sys.argv[1]
sample = sys.argv[2]

# Load NLRs
nlr_bed = pd.read_csv(f"{workdir}/{sample}.nlrs.bed", sep="\t", header=None,
                      names=["chr", "start", "end", "genename"])

# Load duplicated NLRs
dup_bed = pd.read_csv(f"{workdir}/{sample}.nlrs_in_duplications.bed", sep="\t", header=None,
                      names=["chr", "start", "end", "genename", "dup_chr", "dup_start", "dup_end"])
duplicated_nlrs = set(dup_bed["genename"].unique())
nlr_bed["is_duplicated"] = nlr_bed["genename"].isin(duplicated_nlrs)

# Load neighborhoods and assign to each NLR
neighborhoods = pd.read_csv(f"{workdir}/{sample}.neighborhoods_final_renamed.bed", sep="\t", header=None,
                            names=["chr", "start", "end", "neighborhood_id"])

def assign_neighborhood(nlr_row):
    overlaps = neighborhoods[
        (neighborhoods["chr"] == nlr_row["chr"]) &
        (neighborhoods["start"] <= nlr_row["end"]) &
        (neighborhoods["end"] >= nlr_row["start"])
    ]
    return overlaps.iloc[0]["neighborhood_id"] if overlaps.shape[0] > 0 else "None"

nlr_bed["neighborhood_id"] = nlr_bed.apply(assign_neighborhood, axis=1)

# Merge TE counts
te_counts = pd.read_csv(f"{workdir}/{sample}.te_counts_per_neighborhood.tsv", sep="\t")
nlr_bed = nlr_bed.merge(te_counts, on="neighborhood_id", how="left")
nlr_bed["TE_count"] = nlr_bed["TE_count"].fillna(0).astype(int)

# Merge TE class summary
te_classes = pd.read_csv(f"{workdir}/{sample}.te_class_counts.tsv", sep="\t")
te_class_summary = te_classes.groupby("neighborhood_id")["TE_class"].apply(
    lambda x: ", ".join(sorted(set(x)))
).reset_index()
te_class_summary.columns = ["neighborhood_id", "TE_classes"]
nlr_bed = nlr_bed.merge(te_class_summary, on="neighborhood_id", how="left")
nlr_bed["TE_classes"] = nlr_bed["TE_classes"].fillna("None")

nlr_bed[["genename", "is_duplicated", "neighborhood_id", "TE_count", "TE_classes"]].to_csv(
    f"{workdir}/{sample}.nlr_summary_table.tsv", sep="\t", index=False
)
