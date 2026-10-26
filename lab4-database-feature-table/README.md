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
