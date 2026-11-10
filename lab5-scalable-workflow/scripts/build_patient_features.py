#!/usr/bin/env python3
import argparse
import re
import sqlite3
from pathlib import Path

import pandas as pd


def load_queries(path):
    parts = re.split(r"^-- name: (\w+)\s*$", path.read_text(), flags=re.MULTILINE)
    return {name: sql.strip() for name, sql in zip(parts[1::2], parts[2::2])}


def main():
    parser = argparse.ArgumentParser(description="Extract patient features from Lab 4 cohort db.")
    parser.add_argument("--db", required=True, help="Path to cohort.db")
    parser.add_argument("--sql", required=True, help="Path to queries.sql")
    parser.add_argument("--output", required=True, help="Output TSV for patient features")
    args = parser.parse_args()

    queries = load_queries(Path(args.sql))
    with sqlite3.connect(f"file:{Path(args.db)}?mode=ro", uri=True) as con:
        df = pd.read_sql_query(queries["patient_base"], con)

    df = df.copy()
    df["patient_key"] = range(1, len(df) + 1)
    df = df[
        [
            "patient_id",
            "patient_key",
            "sex",
            "age_at_diagnosis",
            "stage",
            "tissue_source_site",
            "tmb_nonsynonymous",
            "has_mutation_calls",
        ]
    ]

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, sep="\t", index=False, na_rep="NA")


if __name__ == "__main__":
    main()
