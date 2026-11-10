# Lab 5 — Scalable Analysis Workflow

This lab turns the Lab 3 cleaning step and Lab 4 database query step into a small, reproducible DAG managed by Snakemake.

## Workflow goal

The pipeline does four explicit stages:

1. Clean the messy clinical sample table from Lab 3.
2. Query the cohort database from Lab 4 to extract patient-level features.
3. Merge the cleaned sample table and patient feature table into one analytic table.
4. Produce a short text summary report from the merged data.

## Project structure

```text
lab5-scalable-workflow/
├── README.md
├── AI_USAGE.md
├── Snakefile
├── scripts/
│   ├── clean_samples.py
│   ├── build_patient_features.py
│   ├── build_combined_table.py
│   └── summarize.py
├── results/
│   ├── clean_samples.tsv
│   ├── patient_features.tsv
│   ├── combined_table.tsv
│   └── summary_report.md
└── evidence/
    ├── clean_run.log
    └── partial_rerun.log
```

## Setup

From the repo root, create or activate the project environment and install Snakemake:

```bash
conda activate hds-practical
python -m pip install snakemake
```

## Clean run

From the repo root:

```bash
cd lab5-scalable-workflow
snakemake --cores 1 --printshellcmds results/summary_report.md
```

This executes the full DAG from a clean state and writes the final outputs under `results/`.

## Partial re-run check

After the pipeline has run, change a single upstream input and dry-run the workflow to confirm that only the affected downstream jobs rerun:

```bash
touch ../lab3-parsing-messy-data/data/messy_samples.csv
snakemake --cores 1 -n results/summary_report.md
```

The dry run should show only the rules downstream of the updated raw input being scheduled, rather than the whole workflow.

## Evidence

The project includes saved evidence in `evidence/` for:

- the clean run
- the partial rerun / dependency check

## AI usage

AI assistance was used to help draft the Snakemake workflow structure and the Python wrappers for data cleaning, SQL extraction, and reporting. The logic was reviewed line by line before execution, and the workflow definitions are explicit about every input and output.

## Notes

The original Lab 3 data are synthetic and the Lab 4 cohort is a separate real cohort table. For this workflow exercise, the two datasets are merged using an explicit `patient_key` generated from row order so the DAG demonstrates the dependency and merge logic cleanly without hiding any step.
