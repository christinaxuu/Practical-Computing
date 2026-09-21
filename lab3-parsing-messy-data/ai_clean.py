import re
import csv

SITE_RE = re.compile(r"site[\s_-]*([abc])", re.IGNORECASE)
SEX_MAP = {"m": "M", "male": "M", "f": "F", "female": "F", "u": "U", "unknown": "U"}
MMOL_TO_MGDL = 18.0  # AI used the common rounded factor, not the precise 18.0182
DDMM_AMBIGUOUS = {"06.07.12", "09.06.98", "02.08.89", "02.09.06"}  # AI's judgment call: interpret as DD.MM

MONTHS = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
          "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}

def clean_dob(raw):
    raw = raw.strip()
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
        return f"{yyyy}-{MONTHS[mon.title()]}-{dd}"
    m = re.match(r"^(\d{2})\.(\d{2})\.(\d{2})$", raw)
    if m:
        a, b, yy = m.groups()
        yyyy = f"20{yy}" if int(yy) <= 18 else f"19{yy}"
        if raw in DDMM_AMBIGUOUS:
            dd, mm = a, b          # AI's alternate reading: DD.MM
        else:
            mm, dd = a, b          # default MM.DD, same as regex script for unambiguous rows
        return f"{yyyy}-{mm}-{dd}"
    return f"UNPARSED:{raw}"

def clean_sex(raw):
    raw = raw.strip()
    if raw == "":
        return "MISSING"
    return SEX_MAP.get(raw.lower(), "U")

def clean_site(raw):
    m = SITE_RE.search(raw)
    return f"Site {m.group(1).upper()}" if m else f"UNPARSED:{raw}"

def clean_name(raw):
    return " ".join(w.title() if w.isupper() and len(w) > 2 else w for w in raw.split())

def clean_glucose(raw_value, raw_unit):
    val = raw_value.strip()
    if val.upper() == "N/A" or val == "":
        return None, "missing"
    m = re.match(r"^([\d.]+)(\*?)$", val)
    if not m:
        return None, f"UNPARSED:{val}"
    num, star = m.groups()
    flag = "flagged(*)" if star else ""
    num = float(num)
    if raw_unit.strip().lower() == "mmol/l":
        num = round(num * MMOL_TO_MGDL, 1)
    return num, flag

def main():
    with open("data/messy_samples.csv") as f:
        rows = list(csv.DictReader(f))

    with open("data/clean_samples_ai.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "patient_name_clean", "dob_clean", "sex_clean",
                          "site_clean", "glucose_mgdl", "glucose_flag", "notes"])
        for row in rows:
            writer.writerow([
                row["sample_id"],
                clean_name(row["patient_name"]),
                clean_dob(row["dob"]),
                clean_sex(row["sex"]),
                clean_site(row["enrollment_site"]),
                *clean_glucose(row["glucose_value"], row["glucose_unit"]),
                row["notes"],
            ])

if __name__ == "__main__":
    main()
    print("Wrote data/clean_samples_ai.csv")
