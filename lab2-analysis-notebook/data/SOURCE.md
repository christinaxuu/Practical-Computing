# Data source

**Dataset:** Framingham Heart Study teaching subset (`framingham.csv`, ~4,240
rows, one row per participant, with a 10-year coronary heart disease (CHD)
outcome).

This is the widely-mirrored, de-identified teaching subset used across many
intro biostatistics/epidemiology courses — **not** the restricted-access
official NHLBI/BioLINCC Framingham data, which requires a formal
[BioLINCC](https://biolincc.nhlbi.nih.gov/) application.

**Loaded from:**
https://raw.githubusercontent.com/GauravPadawe/Framingham-Heart-Study/master/framingham.csv

The notebook (`notebook/framingham_analysis.ipynb`) loads this URL directly
at analysis time. `scripts/fetch_data.py` fetches the same file and writes it
to `data/framingham.csv` for convenience; that CSV is not committed to the
repo (see `.gitignore`) since the notebook and fetch script both pull fresh
from source.

**License / terms of use:** Circulates as an open teaching dataset with no
single consistent formal license across mirrors. Appropriate for classroom
use; not a citable primary source.

**PHI/PII status:** De-identified teaching subset, not linkable to real
participants.
