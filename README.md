# Applied Computing for Health Data Science — Labs

Coursework for Applied Computing for Health Data Science (PUBH 4201).

## Labs

| Lab | Description | Link |
|---|---|---|
| Lab 1 | Reproducible analysis of toy patient data | [root of this repo](#lab-1-toy-patient-data-analysis) (below) |
| Lab 2 | Framingham Heart Study analysis notebook | [`lab2-analysis-notebook/`](lab2-analysis-notebook/) |
| Lab 3 | Regex vs. AI-assisted cleaning of messy clinical data | [`lab3-parsing-messy-data/`](lab3-parsing-messy-data/) |

---

## Lab 3: Parsing Messy Health Data

**Start here:** [`lab3-parsing-messy-data/README.md`](lab3-parsing-messy-data/README.md)

**Regex script:** [`lab3-parsing-messy-data/clean_regex.py`](lab3-parsing-messy-data/clean_regex.py)
**AI-assisted script:** [`lab3-parsing-messy-data/ai_clean.py`](lab3-parsing-messy-data/ai_clean.py)
**Comparison & failure-mode analysis:** [`lab3-parsing-messy-data/COMPARISON.md`](lab3-parsing-messy-data/COMPARISON.md)

Cleans a synthetic messy clinical dataset (60 records) two ways: a deterministic regex script and an AI-assisted pass making explicit judgment calls on ambiguous cases (date format ambiguity, blank vs. explicit "unknown" values, unit conversion precision). Compares where the two methods agreed and disagreed, referencing specific records, and documents concrete failure modes. See the lab's own README for setup and run instructions.

---

## Lab 2: Framingham Heart Study Analysis Notebook

**Start here:** [`lab2-analysis-notebook/README.md`](lab2-analysis-notebook/README.md)

**Notebook:** [`lab2-analysis-notebook/notebook/framingham_analysis.ipynb`](lab2-analysis-notebook/notebook/framingham_analysis.ipynb)
**Rendered export:** [`lab2-analysis-notebook/notebook/framingham_analysis.html`](lab2-analysis-notebook/notebook/framingham_analysis.html)

Analyzes 10-year coronary heart disease (CHD) risk by age and sex using the
Framingham Heart Study teaching dataset, loaded directly from its public
source. See the lab's own README for setup and run instructions.

---

## Lab 1: Toy Patient Data Analysis

A small reproducible analysis of toy patient data.

### Project Structure

```
.
├── README.md
├── .gitignore
├── environment.yml
├── scripts/
│   └── analyze.py
├── data/
│   ├── patients.csv
│   └── patients_by_age.csv
├── AI_USAGE.md
├── lab2-analysis-notebook/   (see Lab 2 above)
└── lab3-parsing-messy-data/  (see Lab 3 above)
```

### Setup / Installation / Getting Started

This project uses conda/mamba to manage a reproducible Python environment.

**Prerequisites:** conda or mamba installed (e.g. via Miniforge: https://github.com/conda-forge/miniforge).

1. Clone this repository:

```bash
git clone https://github.com/christinaxuu/Practical-Computing.git
cd Practical-Computing
```

2. Create the environment from environment.yml:

```bash
mamba env create -f environment.yml
```

3. Activate the environment:

```bash
conda activate hds-practical
```

### Running the Analysis

From the project root, run:

```bash
python scripts/analyze.py
```

This reads data/patients.csv and prints summary statistics (count, mean, std, etc.) plus mean age grouped by site.

### Data

data/patients.csv and data/patients_by_age.csv are small, fake/toy patient records (patient ID, age, site) created for practice — not real patient data.
