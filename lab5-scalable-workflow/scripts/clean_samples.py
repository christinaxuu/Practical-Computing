#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

import pandas as pd

SITE_RE = re.compile(r"site[\s_-]*([abc])", re.IGNORECASE)
SEX_MAP = {
    "m": "M",
    "male": "M",
    "f": "F",
    "female": "F",
    "u": "U",
    "unknown": "U",
    "": "U",
}
MMOL_TO_MGDL = 18.0182


def clean_dob(raw):
    raw = str(raw).strip()
    if not raw:
        return "NA"
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", raw)
    if m:
        mm, dd, yyyy = m.groups()
        return f"{yyyy}-{mm}-{dd}"
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", raw)
    if m:
        return raw
    m = re.match(r"^(\d{2})-([A-Za-z]{3})-(\d{4})$", raw)
    if m:
        dd, mon, yyyy = m.groups()
        months = {
            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
            "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
        }
        return f"{yyyy}-{months[mon.title()]}-{dd}"
    m = re.match(r"^(\d{2})\.(\d{2})\.(\d{2})$", raw)
    if m:
        mm, dd, yy = m.groups()
        yyyy = f"20{yy}" if int(yy) <= 18 else f"19{yy}"
        return f"{yyyy}-{mm}-{dd}"
    return f"UNPARSED:{raw}"


def clean_sex(raw):
    return SEX_MAP.get(str(raw).strip().lower(), "U")


def clean_site(raw):
    m = SITE_RE.search(str(raw))
    if m:
        return f"Site {m.group(1).upper()}"
    return f"UNPARSED:{raw}"


def clean_glucose(raw_value, raw_unit):
    val = str(raw_value).strip()
    if val.upper() in {"N/A", ""}:
        return None, "mg/dL", "missing"
    m = re.match(r"^([\d.]+)(\*?)$", val)
    if not m:
        return None, "mg/dL", f"UNPARSED:{val}"
    num, star = m.groups()
    flag = "flagged(*)" if star else ""
    num = float(num)
    unit = str(raw_unit).strip().lower()
    if unit == "mmol/l":
        num = round(num * MMOL_TO_MGDL, 1)
    return num, "mg/dL", flag


def main():
    parser = argparse.ArgumentParser(description="Clean Lab 3 messy sample data.")
    parser.add_argument("--input", required=True, help="Raw messy samples CSV")
    parser.add_argument("--output", required=True, help="Cleaned samples TSV")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    cleaned = df.copy()
    cleaned["dob_clean"] = cleaned["dob"].map(clean_dob)
    cleaned["sex_clean"] = cleaned["sex"].map(clean_sex)
    cleaned["site_clean"] = cleaned["enrollment_site"].map(clean_site)

    glucose_values = cleaned.apply(
        lambda row: clean_glucose(row["glucose_value"], row["glucose_unit"]),
        axis=1,
    )
    cleaned["glucose_mgdl"] = [x[0] for x in glucose_values]
    cleaned["glucose_flag"] = [x[2] for x in glucose_values]

    cleaned["patient_key"] = range(1, len(cleaned) + 1)
    result = cleaned[
        [
            "sample_id",
            "patient_name",
            "dob_clean",
            "sex_clean",
            "site_clean",
            "glucose_mgdl",
            "glucose_flag",
            "patient_key",
        ]
    ]
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(out_path, sep="\t", index=False, na_rep="NA")


if __name__ == "__main__":
    main()
