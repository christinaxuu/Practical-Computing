import re
import csv

SITE_RE = re.compile(r"site[\s_-]*([abc])", re.IGNORECASE)
SEX_MAP = {
    "m": "M", "male": "M",
    "f": "F", "female": "F",
    "u": "U", "unknown": "U", "": "U",
}
MMOL_TO_MGDL = 18.0182

def clean_dob(raw):
    raw = raw.strip()
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", raw)          # MM/DD/YYYY
    if m:
        mm, dd, yyyy = m.groups()
        return f"{yyyy}-{mm}-{dd}"
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", raw)           # YYYY-MM-DD
    if m:
        return raw
    m = re.match(r"^(\d{2})-([A-Za-z]{3})-(\d{4})$", raw)     # DD-Mon-YYYY
    if m:
        dd, mon, yyyy = m.groups()
        months = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
                  "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
        return f"{yyyy}-{months[mon.title()]}-{dd}"
    m = re.match(r"^(\d{2})\.(\d{2})\.(\d{2})$", raw)         # MM.DD.YY (ambiguous century)
    if m:
        mm, dd, yy = m.groups()
        yyyy = f"20{yy}" if int(yy) <= 18 else f"19{yy}"      # heuristic, see AI_USAGE / comparison notes
        return f"{yyyy}-{mm}-{dd}"
    return f"UNPARSED:{raw}"

def clean_sex(raw):
    return SEX_MAP.get(raw.strip().lower(), "U")

def clean_site(raw):
    m = SITE_RE.search(raw)
    if m:
        return f"Site {m.group(1).upper()}"
    return f"UNPARSED:{raw}"

def clean_glucose(raw_value, raw_unit):
    val = raw_value.strip()
    flag = ""
    if val.upper() == "N/A" or val == "":
        return None, "mg/dL", "missing"
    m = re.match(r"^([\d.]+)(\*?)$", val)
    if not m:
        return None, "mg/dL", f"UNPARSED:{val}"
    num, star = m.groups()
    if star:
        flag = "flagged(*)"
    num = float(num)
    unit = raw_unit.strip().lower()
    if unit == "mmol/l":
        num = round(num * MMOL_TO_MGDL, 1)
    return num, "mg/dL", flag

def main():
    with open("data/messy_samples.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open("data/clean_samples_regex.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "patient_name", "dob_clean", "sex_clean",
                          "site_clean", "glucose_mgdl", "glucose_flag", "notes"])
        for row in rows:
            dob = clean_dob(row["dob"])
            sex = clean_sex(row["sex"])
            site = clean_site(row["enrollment_site"])
            glucose, unit, flag = clean_glucose(row["glucose_value"], row["glucose_unit"])
            writer.writerow([row["sample_id"], row["patient_name"], dob, sex,
                              site, glucose, flag, row["notes"]])

if __name__ == "__main__":
    main()
    print("Wrote data/clean_samples_regex.csv")
