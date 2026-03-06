#!/usr/bin/env python3
# Extract NLRs located in TE-rich neighborhoods.
# Usage: python3 nlr_rich_tes.py <workdir> <sample>

import sys
import pandas as pd

workdir = sys.argv[1]
sample = sys.argv[2]

nlrs = pd.read_csv(f"{workdir}/{sample}.nlrs.bed", sep="\t", header=None,
                   names=["chr", "start", "end", "genename"])

summary = pd.read_csv(f"{workdir}/{sample}.nlr_summary_table.tsv", sep="\t")

te_rich = summary[summary["TE_count"] >= 1]
te_rich_nlrs = nlrs[nlrs["genename"].isin(te_rich["genename"])]
te_rich_nlrs.to_csv(f"{workdir}/{sample}.te_rich_nlrs.bed", sep="\t", index=False, header=False)
