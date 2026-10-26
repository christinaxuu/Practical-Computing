"""Build the Lab 4 per-patient feature table from data/cohort.db.

Runs the named queries in queries.sql, reshapes the long per-gene counts
to wide format with pandas, checks row counts at every step, and writes
output/feature_table.tsv (plus output/site_stage_counts.tsv).

Run from anywhere:
    python3 build_feature_table.py
"""
import re
import sqlite3
from pathlib import Path

import pandas as pd

LAB_DIR = Path(__file__).resolve().parent
DB_PATH = LAB_DIR / "data" / "cohort.db"
SQL_PATH = LAB_DIR / "queries.sql"
OUT_DIR = LAB_DIR / "output"

GENES = ["TP53", "KRAS", "EGFR", "STK11", "KEAP1"]
EXPECTED_PATIENTS = 566


def load_queries(path):
    """Split queries.sql into {name: sql} on its '-- name: <name>' lines."""
    parts = re.split(r"^-- name: (\w+)\s*$", path.read_text(), flags=re.MULTILINE)
    # parts = [header, name1, sql1, name2, sql2, ...]
    return {name: sql.strip() for name, sql in zip(parts[1::2], parts[2::2])}


def run(con, sql):
    return pd.read_sql_query(sql, con)


def main():
    queries = load_queries(SQL_PATH)
    # Read-only, so running the script can never modify the database.
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)

    n_patients = con.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    samples_per_patient = con.execute(
        "SELECT MAX(n) FROM (SELECT COUNT(*) AS n FROM samples GROUP BY patient_id)"
    ).fetchone()[0]
    print(f"patients table: {n_patients} patients")
    print(f"max samples per patient: {samples_per_patient}")
    assert n_patients == EXPECTED_PATIENTS
    # If a patient ever had two samples, patients LEFT JOIN samples would
    # duplicate them and every per-patient count below would be wrong.
    assert samples_per_patient == 1, "a patient has >1 sample; pick one before joining"

    # Patient-level columns (patients LEFT JOIN samples).
    base = run(con, queries["patient_base"])
    print(f"after patients LEFT JOIN samples: {len(base)} rows, "
          f"{base.patient_id.nunique()} unique patients")
    assert len(base) == base.patient_id.nunique() == EXPECTED_PATIENTS

    # Long gene counts: one row per (patient, gene).
    long_counts = run(con, queries["gene_counts"])
    print(f"gene_counts query: {len(long_counts)} rows "
          f"(expected {EXPECTED_PATIENTS} x {len(GENES)} = {EXPECTED_PATIENTS * len(GENES)})")
    assert len(long_counts) == EXPECTED_PATIENTS * len(GENES)
    assert not long_counts.duplicated(["patient_id", "gene_symbol"]).any()

    # Reshape long -> wide: one row per patient, one column per gene. The
    # grain is already (patient, gene) with mutations summed in SQL, so a
    # patient with several TP53 mutations is one cell, not several rows.
    wide = (long_counts
            .pivot(index="patient_id", columns="gene_symbol", values="n_protein_altering")
            .reindex(columns=GENES)
            .add_suffix("_count")
            .reset_index())
    wide.columns.name = None
    assert len(wide) == EXPECTED_PATIENTS

    features = base.merge(wide, on="patient_id", how="left", validate="one_to_one")
    print(f"after merging gene counts: {len(features)} rows")
    assert len(features) == EXPECTED_PATIENTS

    # A tumor with zero mutation calls of any type (not even Silent) has no
    # evidence it was successfully profiled, so "0 mutations in TP53" can't
    # be claimed for it. Its gene counts and its TMB (which cBioPortal derives
    # from those same calls) are recoded from 0 to NA.
    no_calls = features.has_mutation_calls == 0
    gene_cols = [f"{g}_count" for g in GENES]
    features[gene_cols] = features[gene_cols].astype("Int64")
    features.loc[no_calls, gene_cols] = pd.NA
    features.loc[no_calls, "tmb_nonsynonymous"] = pd.NA
    features["has_mutation_calls"] = features.has_mutation_calls.astype(bool)
    print(f"tumors with no mutation calls (gene counts + TMB set to NA): "
          f"{no_calls.sum()} -> {', '.join(features.loc[no_calls, 'patient_id'])}")

    print("missing values per column:")
    for col, n in features.isna().sum().items():
        print(f"  {col}: {n}")

    OUT_DIR.mkdir(exist_ok=True)
    features.to_csv(OUT_DIR / "feature_table.tsv", sep="\t", index=False, na_rep="NA")
    print(f"wrote {OUT_DIR / 'feature_table.tsv'} ({len(features)} rows)")

    site_stage = run(con, queries["site_stage_counts"])
    print(f"site_stage_counts query: {len(site_stage)} rows, "
          f"{site_stage.n_patients.sum()} patients total")
    assert site_stage.n_patients.sum() == EXPECTED_PATIENTS
    site_stage.to_csv(OUT_DIR / "site_stage_counts.tsv", sep="\t", index=False, na_rep="NA")
    print(f"wrote {OUT_DIR / 'site_stage_counts.tsv'}")

    con.close()


if __name__ == "__main__":
    main()
