# Lab 3 — Parsing Messy Health Data

Regex-based and AI-assisted cleaning of a synthetic messy clinical dataset (60 records), plus a comparison of the two approaches and a failure-mode analysis.

## Project Structure

lab3-parsing-messy-data/
- clean_regex.py, deterministic regex-based cleaning script
- ai_clean.py, AI-assisted cleaning script (judgment calls documented in AI_USAGE.md)
- COMPARISON.md, comparison of the two approaches and failure-mode analysis
- AI_USAGE.md, documented AI interaction and prompts
- data/messy_samples.csv, raw input data
- data/clean_samples_regex.csv, output of the regex script
- data/clean_samples_ai.csv, output of the AI-assisted script

## Running the scripts

Both scripts read data/messy_samples.csv and write their output back into the data/ folder. Run from inside the lab3-parsing-messy-data folder:

```bash
python3 clean_regex.py
python3 ai_clean.py
```

## Comparing the outputs

```bash
python3 -c "
import csv
regex = {r['sample_id']: r for r in csv.DictReader(open('data/clean_samples_regex.csv'))}
ai = {r['sample_id']: r for r in csv.DictReader(open('data/clean_samples_ai.csv'))}
for sid in regex:
    r, a = regex[sid], ai[sid]
    if r['dob_clean'] != a['dob_clean'] or r['sex_clean'] != a['sex_clean'] or r['glucose_mgdl'] != a['glucose_mgdl']:
        print(sid, 'differs')
"
```

See COMPARISON.md for the full write-up of where and why the two methods disagreed, and for the failure-mode analysis of specific ambiguous or incorrect records.

## Data

data/messy_samples.csv is synthetic data generated for this course (see the course repo's data/raw/lab3-messy-data/SOURCE.md), not real patient data.
