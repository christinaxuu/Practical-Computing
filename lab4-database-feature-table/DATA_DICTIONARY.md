# Data dictionary: `output/feature_table.tsv`

One row per patient (566 rows), tab-separated. Missing values are written as
`NA`. Built by `build_feature_table.py` from `data/cohort.db`.

"Protein-altering" in the gene columns means every mutation type in the
database **except** `Silent`. Counted: `Missense_Mutation`,
`Nonsense_Mutation`, `Frame_Shift_Del`, `Frame_Shift_Ins`, `In_Frame_Del`,
`In_Frame_Ins`, `Splice_Site`, `Nonstop_Mutation`, `Translation_Start_Site`.
Excluded: `Silent`. UTR, intron, flank, RNA, and splice-region variants are
never counted because they were not loaded into `cohort.db` (see
`data/SOURCE.md`).

| Column | Meaning | Type / units | Source table (column) | Missing values |
|---|---|---|---|---|
| `patient_id` | TCGA patient barcode; the row key | text, e.g. `TCGA-05-4244` | `patients` (`patient_id`) | never missing; unique |
| `sex` | Patient sex as recorded | `female` / `male` | `patients` (`sex`) | `NA` for 52 patients with no clinical record; left as NA, not guessed |
| `age_at_diagnosis` | Age when the cancer was diagnosed | years (whole numbers, 33–88) | `patients` (`age_at_diagnosis`) | `NA` for 71 patients (the same 52 as `sex`, plus 19) |
| `stage` | AJCC pathologic tumor stage | `I`, `IA`, `IB`, `II`, `IIA`, `IIB`, `IIIA`, `IIIB`, `IV` | `patients` (`stage`) | `NA` for 54 patients (the same 52, plus 2) |
| `tissue_source_site` | Institution that contributed the tumor sample | text (34 sites) | `samples` (`tissue_source_site`) | never missing |
| `tmb_nonsynonymous` | Tumor mutation burden: non-synonymous mutations per megabase of sequenced exome | mutations per megabase | `samples` (`tmb_nonsynonymous`) | `NA` for the 4 tumors with `has_mutation_calls = False`. The database stores 0.0 for them, but that value comes from mutation calls that don't exist, so it is recoded to NA |
| `has_mutation_calls` | Whether the tumor has at least one mutation of any type, Silent included, in `mutations` | `True` / `False` | derived from `mutations` | never missing; `False` for 4 patients |
| `TP53_count` | Number of protein-altering TP53 mutations in the patient's tumor | count (integer ≥ 0) | `mutations` (`gene_symbol`, `variant_classification`), joined through `samples` | `0` = tumor has mutation calls but none are protein-altering in this gene. `NA` = tumor has no mutation calls at all (4 patients) |
| `KRAS_count` | Number of protein-altering KRAS mutations | count (integer ≥ 0) | same as `TP53_count` | same as `TP53_count` |
| `EGFR_count` | Number of protein-altering EGFR mutations | count (integer ≥ 0) | same as `TP53_count` | same as `TP53_count` |
| `STK11_count` | Number of protein-altering STK11 mutations | count (integer ≥ 0) | same as `TP53_count` | same as `TP53_count` |
| `KEAP1_count` | Number of protein-altering KEAP1 mutations | count (integer ≥ 0) | same as `TP53_count` | same as `TP53_count` |
