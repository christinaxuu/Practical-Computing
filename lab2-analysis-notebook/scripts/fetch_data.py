"""Fetch the Framingham Heart Study teaching subset from its public source.

This is the same public mirror cited in the course's SOURCE.md for this
dataset option (the official BioLINCC Framingham data is restricted-access;
this is the widely-circulated de-identified teaching subset, ~4,000 rows).

Usage:
    python scripts/fetch_data.py
"""

from pathlib import Path
import pandas as pd

SOURCE_URL = (
    "https://raw.githubusercontent.com/GauravPadawe/Framingham-Heart-Study"
    "/master/framingham.csv"
)

OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "framingham.csv"


def fetch() -> pd.DataFrame:
    df = pd.read_csv(SOURCE_URL)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    return df


if __name__ == "__main__":
    df = fetch()
    print(f"Fetched {len(df)} rows, {len(df.columns)} columns -> {OUT_PATH}")
