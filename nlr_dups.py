#!/usr/bin/env python3
# Extract NLRs that overlap segmental duplications.
# Usage: python3 nlr_dups.py <workdir> <sample>

import sys
import pandas as pd

workdir = sys.argv[1]
sample = sys.argv[2]

nlrs = pd.read_csv(f"{workdir}/{sample}.nlrs.bed", sep="\t", header=None,
                   names=["chr", "start", "end", "genename"])

dups = pd.read_csv(f"{workdir}/{sample}.nlrs_in_duplications.bed", sep="\t", header=None,
                   names=["chr", "start", "end", "genename", "dup_chr", "dup_start", "dup_end"])

dup_nlrs = nlrs[nlrs["genename"].isin(dups["genename"])]
dup_nlrs.to_csv(f"{workdir}/{sample}.duplicated_nlrs.bed", sep="\t", index=False, header=False)
