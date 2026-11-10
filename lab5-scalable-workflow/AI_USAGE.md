# AI Usage — Lab 5

**GitHub Copilot (agent mode in VS Code):** it wrote the `Snakefile` and the Python scripts in `scripts/` for this workflow. The model used was **MAI-Code-1.1-Flash**.

**Claude (via Claude Code):** it explained Snakemake concepts to me in tutor mode, especially DAG design, rule dependencies, and the difference between a full clean run and a partial rerun. I used that explanation to understand the workflow logic, but I did not treat it as a final answer without checking it myself.

## What the AI generated

GitHub Copilot generated the following as a starting point for the lab:

- `lab5-scalable-workflow/Snakefile`
- `lab5-scalable-workflow/scripts/clean_samples.py`
- `lab5-scalable-workflow/scripts/build_patient_features.py`
- `lab5-scalable-workflow/scripts/build_combined_table.py`
- `lab5-scalable-workflow/scripts/summarize.py`

I used those drafts as a scaffold, then checked them against my own project files and the lab requirements.

## What I did myself

I did the following without relying on AI to decide the final result:

- I checked the Lab 3 and Lab 4 project outputs and reused the actual cleaning and feature-building logic from those labs.
- I confirmed the workflow target and the dependency chain: the cleaned data must be produced before the merged analytic table, and the summary report must depend on the merged table.
- I made sure each Snakemake rule declared explicit input and output files.
- I ran the workflow in my own terminal from a clean state and verified the outputs were produced.
- I reran the workflow in a dry-run after forcing the upstream cleaning rule to update, and I checked that only the downstream steps were scheduled.
- I saved the evidence files in `lab5-scalable-workflow/evidence/`.

## How I checked the work

I verified everything because I reran everything in my terminal.

- I ran the full workflow from a clean state with Snakemake and checked the job output reached 100% completion.
- I inspected the generated files in `results/` to make sure all expected outputs existed.
- I used a forced rerun of the upstream `clean_samples` rule and a dry run (`snakemake -n --forcerun clean_samples results/summary_report.md`) to confirm that only the downstream jobs reran.
- I checked that the workflow did not silently skip any required stage and that each rule had real input/output dependencies.
- I saved the clean-run and partial-rerun logs as evidence in the repository so the results are reproducible and reviewable.

## What I decided myself

I kept the pipeline structure simple and explicit rather than accepting AI-generated boilerplate without review. The main decisions I made on my own were:

- to use the Lab 3 cleaning step and the Lab 4 patient-base query as the real upstream dependencies,
- to keep the workflow output files under `results/`,
- to document the rerun evidence in `evidence/`,
- to verify all final outputs by running the workflow and checking the logs myself.

The final version is a workflow I checked, reran, and verified in my own project environment.
