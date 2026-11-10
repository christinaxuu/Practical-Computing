#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Merge the cleaned samples and cohort feature tables.")
    parser.add_argument("--samples", required=True, help="Cleaned samples TSV")
    parser.add_argument("--features", required=True, help="Feature table TSV")
    parser.add_argument("--output", required=True, help="Merged analytic table TSV")
    args = parser.parse_args()

    samples = pd.read_csv(args.samples, sep="\t")
    features = pd.read_csv(args.features, sep="\t")

    samples["patient_key"] = pd.to_numeric(samples["patient_key"], errors="raise").astype(int)
    features["patient_key"] = pd.to_numeric(features["patient_key"], errors="raise").astype(int)

    combined = samples.merge(
        features,
        on="patient_key",
        how="left",
        validate="one_to_one",
        suffixes=("_sample", "_feature"),
    )

    keep = [
        "sample_id",
        "patient_name",
        "dob_clean",
        "sex_clean",
        "site_clean",
        "glucose_mgdl",
        "glucose_flag",
        "patient_id",
        "sex",
        "age_at_diagnosis",
        "stage",
        "tissue_source_site",
        "tmb_nonsynonymous",
        "has_mutation_calls",
    ]

    result = combined[keep].sort_values("sample_id").reset_index(drop=True)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(out_path, sep="\t", index=False, na_rep="NA")


if __name__ == "__main__":
    main()
