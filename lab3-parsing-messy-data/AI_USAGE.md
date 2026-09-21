# AI Usage — Lab 3

## Interaction: AI-assisted cleaning of messy_samples.csv

**Model used:** Claude (Sonnet 5), via Claude Code

**Task:** Produce a second, independent cleaning of the same raw data already handled by the deterministic regex script (`clean_regex.py`), so the two approaches could be compared on real disagreements rather than a hypothetical.

**What I asked:** I gave Claude the full raw contents of `messy_samples.csv` (all 60 rows) and asked it to reason through the ambiguous or judgment-dependent parts of cleaning the data, specifically: how to handle two-digit years, how to handle dates where both the day and month portions are ≤12 (genuinely ambiguous order), how to handle blank vs. explicitly-recorded "unknown" sex values, and what unit conversion factor to use for mmol/L to mg/dL.

**What the AI produced:** Rather than a single set of extracted values, Claude identified four specific judgment calls where a reasonable person (or AI) might differ from a fixed regex rule, then wrote those decisions into `ai_clean.py` so they applied consistently across the dataset:
1. Four specific rows (`06.07.12`, `09.06.98`, `02.08.89`, `02.09.06`) were flagged as day/month-order ambiguous and interpreted as DD.MM instead of the regex script's MM.DD assumption.
2. Blank `sex` values were coded separately as `MISSING`, distinct from explicitly-recorded `unknown`/`U`.
3. The mmol/L to mg/dL conversion used the commonly-quoted rounded factor (18.0) instead of the more precise 18.0182 the regex script used.
4. ALL-CAPS surnames (e.g. "J. KIM") were normalized to title case, something the regex script never attempted since it wasn't scoped to touch names.

**How I verified it:** I did not treat the AI output as automatically correct. I ran both scripts and diffed their outputs field-by-field, which surfaced exactly 20 disagreements across the 60 records, matching the four categories above. For each category I checked whether the disagreement reflected a genuine data ambiguity (the day/month order and two-digit year cases, where neither answer can be verified from the raw string alone) versus a straightforward difference in convention (the rounding factor). This distinction is the basis for COMPARISON.md's failure-mode analysis: some of these "disagreements" are really two different reasonable people making different but equally defensible calls, not evidence that one method is more correct than the other.
