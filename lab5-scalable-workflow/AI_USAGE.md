# AI Usage — Lab 5

## Tools used
- **GitHub Copilot (agent mode in VS Code), model MAI-Code-1.1-Flash:**
  wrote the `Snakefile`, all four scripts in `scripts/`, the Lab 5
  `README.md`, and the first draft of this file. It also chose how to
  reuse the Lab 3 cleaning logic and the Lab 4 query, and how to
  structure the rules.
- **Claude (via Claude Code):** explained Snakemake concepts (rules,
  inputs/outputs, how Snakemake decides what to re-run) and walked me
  through running commands in the terminal. After my first push, Claude
  reviewed the repo and pointed out that my evidence logs were not
  committed (blocked by `*.log` in `.gitignore`), that the `.snakemake/`
  cache folder had been committed, that my logs said "Nothing to be
  done", and that the first draft of this file credited me with work
  Copilot had done.

## What I did myself
- Asked Copilot to build the Lab 5 workflow and accepted its changes.
- Ran the pipeline in my own terminal: a clean run after deleting
  `results/`, and a partial re-run after changing an input file.
- Looked over the output files in `results/`.
- Fixed the repo problems Claude pointed out: force-added the evidence
  logs, untracked `.snakemake/` and added it to `.gitignore`, added
  Lab 5 to the root README, and replaced this file with an accurate one.

## Key prompts
- To Copilot: asked it to build the Lab 5 workflow in my
  Practical-Computing repo following the lab instructions.
- To Claude: asked for help with Lab 5 in "tutor mode", then for help
  saving files, pushing to GitHub, checking my repo, and fixing the
  partial re-run.

## What went wrong
- My first evidence logs were a dry run (`-n --forcerun`) and runs that
  said "Nothing to be done", so they didn't show the pipeline running.
- Using `touch` on `messy_samples.csv` did not trigger a re-run in
  Snakemake 9, because only the timestamp changed, not the contents.
- The first AI_USAGE draft (written by Copilot) overstated what I did
  myself, so I replaced it.

## How I checked the work
- In `evidence/clean_run.log`, I deleted `results/` and reran; all 5
  steps ran (clean_samples, patient_features, combine_tables,
  summary_report, all).
- In `evidence/partial_rerun.log`, I added a comment line to
  `../lab4-database-feature-table/queries.sql`. Only patient_features,
  combine_tables, and summary_report reran (4 jobs); clean_samples was
  skipped because its input didn't change.
