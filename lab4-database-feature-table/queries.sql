-- Lab 4 SQL queries against data/cohort.db (SQLite).

-- name: gene_counts
-- Protein-altering (non-Silent) mutation count for every patient x gene.
-- Expected rows: 566 patients x 5 genes = 2,830.
-- The gene match and the Silent filter go in the LEFT JOIN's ON clause, not
-- WHERE; in WHERE they would drop every patient-gene pair with 0 mutations.
SELECT
    p.patient_id,
    g.gene_symbol,
    COUNT(m.mutation_id) AS n_protein_altering
FROM patients AS p
CROSS JOIN (
    SELECT gene_symbol FROM genes
    WHERE gene_symbol IN ('TP53', 'KRAS', 'EGFR', 'STK11', 'KEAP1')
) AS g
LEFT JOIN samples AS s
    ON s.patient_id = p.patient_id
LEFT JOIN mutations AS m
    ON  m.sample_id = s.sample_id
    AND m.gene_symbol = g.gene_symbol
    AND m.variant_classification <> 'Silent'
GROUP BY p.patient_id, g.gene_symbol
ORDER BY p.patient_id, g.gene_symbol;

-- name: site_stage_counts
-- Patients per tissue source site per tumor stage. Patients with no stage
-- are kept as their own NULL-stage group; each patient is counted once.
SELECT
    s.tissue_source_site,
    p.stage,
    COUNT(DISTINCT p.patient_id) AS n_patients
FROM patients AS p
LEFT JOIN samples AS s
    ON s.patient_id = p.patient_id
GROUP BY s.tissue_source_site, p.stage
ORDER BY s.tissue_source_site, p.stage;

-- name: patient_base
-- One row per patient: clinical columns plus the sample's site and TMB.
-- Only one row per patient because every patient has exactly one sample
-- (build_feature_table.py checks this). has_mutation_calls = 1 if the tumor
-- has at least one mutation of any type, Silent included.
SELECT
    p.patient_id,
    p.sex,
    p.age_at_diagnosis,
    p.stage,
    s.tissue_source_site,
    s.tmb_nonsynonymous,
    EXISTS (SELECT 1 FROM mutations AS m WHERE m.sample_id = s.sample_id) AS has_mutation_calls
FROM patients AS p
LEFT JOIN samples AS s
    ON s.patient_id = p.patient_id
ORDER BY p.patient_id;
