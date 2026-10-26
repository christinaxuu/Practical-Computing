# AI Usage — Lab 4

**Model used:** Claude (Sonnet 5), via Claude Code

**What I used it for:** Claude walked me through the lab step by step. It
wrote the SQL in `queries.sql`, the `build_feature_table.py` script, and
drafts of the README sections and data dictionary. I ran every command
myself in my own terminal and committed each step.

**How I checked the SQL (not just that it ran):**
- **Expected vs. actual row counts:** I wrote down the expected count before
  running each query. `gene_counts`: expected 566 × 5 = 2,830, got 2,830.
  `site_stage_counts`: 142 rows adding up to 566 patients. The patient-level
  join: 566 rows.
- **Tested the ON vs. WHERE mistake:** the same gene-count query with the
  filters moved to `WHERE` returned 700 rows instead of 2,830, which showed
  the `ON` version is what keeps the zero counts.
- **Checked two patients by hand** against the raw `mutations` table:
  - TCGA-78-7155 has 3 EGFR missense mutations and 1 TP53 missense
    mutation, and the table shows EGFR_count = 3 and TP53_count = 1.
  - TCGA-17-Z023 has one TP53 Nonsense mutation and one TP53 Silent
    mutation, and the table shows TP53_count = 1, so Silent was excluded.
    This patient is also missing sex, age, and stage and is still in the
    table with NAs.
- **Checked the data dictionary against the table:** both list the same 12
  columns.

**Decisions I reviewed rather than accepted automatically:** Claude proposed
coding the gene counts and TMB as NA, not 0, for the 4 tumors with no
mutation calls at all. I kept that choice because a 0 would claim the tumor
was sequenced and nothing was found, which the data can't show. The database
itself stores 0.0 for their TMB, so I documented the recode in `README.md`
and `DATA_DICTIONARY.md`.
