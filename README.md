# hds-practical

A small reproducible analysis of toy patient data, built for Lab 1 of Applied Computing for Health Data Science (Undergraduate Version).

See [`lab2-analysis-notebook/`](lab2-analysis-notebook/) for Lab 2 (Framingham Heart Study analysis notebook).

## Project Structure

hds-practical/
├── README.md
├── .gitignore
├── environment.yml
├── scripts/
│   └── analyze.py
├── data/
│   ├── patients.csv
│   └── patients_by_age.csv
└── AI_USAGE.md

## Setup / Installation / Getting Started

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

## Running the Analysis

From the project root, run:

```bash
python scripts/analyze.py
```

This reads data/patients.csv and prints summary statistics (count, mean, std, etc.) plus mean age grouped by site.

## Data

data/patients.csv and data/patients_by_age.csv are small, fake/toy patient records (patient ID, age, site) created for practice — not real patient data.