#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Create a plain-language summary from the merged table.")
    parser.add_argument("--input", required=True, help="Combined analytic TSV")
    parser.add_argument("--output", required=True, help="Markdown summary report")
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t")
    mean_glucose = df["glucose_mgdl"].mean()
    mean_age = df["age_at_diagnosis"].mean()
    site_counts = df["site_clean"].value_counts().sort_index()
    stage_counts = df["stage"].fillna("Missing").value_counts().sort_index()

    lines = [
        "# Summary Report",
        "",
        f"- Total merged records: {len(df)}",
        f"- Mean sample glucose: {mean_glucose:.1f} mg/dL",
        f"- Mean age at diagnosis: {mean_age:.1f} years",
        "",
        "## Enrollment site distribution",
    ]
    for site, count in site_counts.items():
        lines.append(f"- {site}: {count} samples")

    lines.extend(["", "## Stage distribution"])
    for stage, count in stage_counts.items():
        lines.append(f"- {stage}: {count} patients")

    output = "\n".join(lines) + "\n"
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output)


if __name__ == "__main__":
    main()
