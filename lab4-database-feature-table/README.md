# Lab 4 — Database-Driven Feature Table

Builds a one-row-per-patient feature table from a SQLite database of real
tumor sequencing data (TCGA Lung Adenocarcinoma, PanCancer Atlas, 566
patients; see `data/SOURCE.md`).

## Task 1: Schema

Checked by inspecting `data/cohort.db` (`.schema`, row counts, and join
checks), not guessed from column names.

| Table | Rows | Primary key | Foreign keys | Grain: one row is... |
|---|---|---|---|---|
| `patients` | 566 | `patient_id` | none | one patient |
| `samples` | 566 | `sample_id` | `patient_id` → `patients.patient_id` | one tumor sample |
| `mutations` | 200,789 | `mutation_id` | `sample_id` → `samples.sample_id`; `gene_symbol` → `genes.gene_symbol` | one somatic mutation in one sample |
| `genes` | 17,756 | `gene_symbol` | none | one gene |

**Columns**

- `patients`: `patient_id`, `sex`, `age_at_diagnosis`, `stage`, `vital_status`, `followup_months`
- `samples`: `sample_id`, `patient_id`, `tissue_source_site`, `tmb_nonsynonymous`, `aneuploidy_score`, `msi_mantis_score`
- `mutations`: `mutation_id`, `sample_id`, `gene_symbol`, `variant_classification`, `variant_type`, `protein_change`, `chromosome`, `start_pos`, `end_pos`, `t_ref_count`, `t_alt_count`
- `genes`: `gene_symbol`, `entrez_gene_id`, `chromosome`

**Relationships**

    patients 1 --- 1 samples 1 --- 0..many mutations many --- 1 genes

- **patients → samples:** the schema allows one-to-many, but in this data it
  is one-to-one. Every one of the 566 patients has exactly 1 sample (checked
  with `GROUP BY patient_id`).
- **samples → mutations:** one-to-many. 4 samples have no mutations at all.
- **genes → mutations:** one-to-many. Each mutation is in exactly one gene.
- `PRAGMA foreign_key_check` returns nothing, so there are no orphan rows.

## Task 2: SQL queries and row counts

Both queries are in `queries.sql`.

| Query | Expected rows | Actual rows | Match? |
|---|---|---|---|
| `gene_counts`: protein-altering mutations per patient per gene | 2,830 (566 patients × 5 genes; every patient gets a row for every gene, including zero counts) | 2,830 | yes |
| `site_stage_counts`: patients per tissue source site per stage | At most 340 (34 sites × 10 stage values, counting missing stage as one). Fewer in practice, since most sites don't see every stage. Counts must add up to 566 | 142 rows, adding up to 566 patients | yes |

**Why the filters in `gene_counts` go in `ON`, not `WHERE` (Week 8, habit 2).**
The query builds the full patient × gene grid first, then LEFT JOINs
mutations with the gene match and `variant_classification <> 'Silent'` in
the `ON` clause. I also ran the same query with those filters in `WHERE`
instead: it returned **700** rows instead of 2,830. The `WHERE` version
throws away every patient–gene pair with zero mutations, which is most of
them.

**Missing stage in `site_stage_counts`.** Nothing filters on stage, so
patients with no recorded stage stay in the result as their own NULL-stage
group. `COUNT(DISTINCT patient_id)` counts each patient once.

## Task 3: Building the feature table

`build_feature_table.py` combines SQL and Python:

1. SQL (`patient_base` in `queries.sql`): patients LEFT JOIN samples gives
   sex, age, stage, site, and TMB for all 566 patients.
2. SQL (`gene_counts`): the long per-patient, per-gene counts (2,830 rows).
   The grain is fixed in SQL before reshaping: `GROUP BY patient_id,
   gene_symbol` adds up several mutations in one gene into a single count,
   so a patient with 3 EGFR mutations still ends up as one row.
3. Python (pandas `pivot`): reshapes long to wide, one column per gene.
   Done in Python, not by pivoting in SQL.
4. Python: merges the two on `patient_id` (`validate="one_to_one"`), applies
   the missing-data rule below, and writes `output/feature_table.tsv`.

The script asserts the patient count at every step. Output from my run:

    patients table: 566 patients
    max samples per patient: 1
    after patients LEFT JOIN samples: 566 rows, 566 unique patients
    gene_counts query: 2830 rows (expected 566 x 5 = 2830)
    after merging gene counts: 566 rows

566 patients went in and 566 came out, so no one was lost in the joins.

## Task 4: Missing data

| Gap | How many | What I did | Why |
|---|---|---|---|
| Missing `sex` | 52 | Kept the patient, left as `NA` | No basis for guessing. These 52 are missing sex, age, and stage together, so their clinical record is absent. Dropping them would also drop their real sequencing data |
| Missing `age_at_diagnosis` | 71 (the 52 above + 19 more) | Kept, left as `NA` | Filling in a mean or median would invent values that look real |
| Missing `stage` | 54 (the 52 above + 2 more) | Kept, left as `NA` | Same reason. Query 2 also keeps them as their own group |
| No mutation in a given gene | most patients (e.g. 275 of the 562 tumors with mutation calls have no protein-altering TP53 mutation) | `0` | The tumor was sequenced and has mutation calls, but none are protein-altering in that gene. That is a real, observed zero |
| Tumor with no mutation calls at all | 4 (TCGA-64-1678, TCGA-69-8453, TCGA-78-7143, TCGA-86-A4D0) | Gene counts set to `NA`, TMB recoded from 0.0 to `NA`, and flagged with `has_mutation_calls = False` | A lung adenocarcinoma with zero mutations of any kind, not even Silent, more likely means the calls are missing than that the tumor is mutation-free. A 0 would claim "sequenced, nothing found," which the data can't support. TMB is calculated from those same calls, so it is NA too. The patients themselves are kept |

**Zero vs. missing.** `0` means "we looked and found no protein-altering
mutation in this gene." `NA` means "not recorded, or can't be determined."
The gene count columns use 0 for the first case and NA only for the 4 tumors
with no calls. The clinical columns only use NA. No NA was replaced with 0
or with a made-up value.

## How to run

**Needs:** the conda environment from the repo's root `environment.yml`
(Python 3.12 + pandas). `sqlite3` comes with Python.

    conda activate hds-practical
    python3 lab4-database-feature-table/build_feature_table.py

Works from the repo root or from inside this folder.

- **Expects:** `data/cohort.db` and `queries.sql` next to the script. The
  database is opened read-only.
- **Produces:** `output/feature_table.tsv` (566 rows, one per patient) and
  `output/site_stage_counts.tsv` (Task 2, query 2). Prints the patient count
  after every join and stops with an error if any count is wrong.
- **SQL only:** `sqlite3 data/cohort.db < queries.sql` runs the queries
  directly.

## Files

- `queries.sql`: all SQL queries, each labeled with `-- name:`
- `build_feature_table.py`: runs the queries, reshapes to wide format, checks row counts, writes the outputs
- `output/feature_table.tsv`: the final feature table
- `output/site_stage_counts.tsv`: patients per tissue source site per stage
- `DATA_DICTIONARY.md`: every column in the feature table
- `AI_USAGE.md`: how AI was used and how I checked its SQL
- `data/cohort.db`, `data/SOURCE.md`: the course-provided database and where it came from
