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
