# Lab 2: Analysis Notebook — Framingham Heart Study (Epidemiology)

Reproducible analysis notebook for Lab 2 of Applied Computing for Health
Data Science, using the epidemiology/population-health dataset option
(Framingham Heart Study teaching subset).

## Project structure

```
lab2-analysis-notebook/
├── README.md
├── environment.yml
├── scripts/
│   └── fetch_data.py
├── notebook/
│   ├── framingham_analysis.ipynb
│   ├── framingham_analysis.html   (rendered export)
│   └── chd_by_age_sex.png
└── data/
    └── SOURCE.md
```

## Setup

This uses conda/mamba to manage a reproducible Python environment.

```bash
mamba env create -f environment.yml
conda activate hds-lab2
```

## Running the analysis

The notebook loads data directly from its original public source (see
`data/SOURCE.md`) — no manual download needed. From the `notebook/`
directory, open `framingham_analysis.ipynb` in Jupyter and choose
**Kernel → Restart & Run All**, or run headlessly:

```bash
cd notebook
jupyter nbconvert --to notebook --execute --inplace framingham_analysis.ipynb
jupyter nbconvert --to html framingham_analysis.ipynb
```

Alternatively, `scripts/fetch_data.py` fetches the same source data to
`data/framingham.csv` as a standalone check:

```bash
python scripts/fetch_data.py
```

## Analysis summary

The notebook computes 10-year coronary heart disease (CHD) incidence rates
by age group and sex, visualizes them, and compares systolic blood pressure
between participants aged 60+ who did and did not develop CHD within 10
years. See the notebook's final markdown cell for the written
interpretation of results.

## AI usage

See the repository-level `AI_USAGE.md` for documentation of AI assistance
used on this lab, including specific models and use cases.
