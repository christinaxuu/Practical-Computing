# Regex vs. AI-Assisted Cleaning: Comparison

**Note:** This analysis uses the dataset posted by the instructor on 2026-09-30 (the real `messy_samples.csv`, previously blocked by an instructor-side `.gitignore`). An earlier version of this file was built against a self-generated substitute dataset while the real file was unavailable; that version has been replaced with this one, built against the actual posted data.

## Method summary

- **Regex approach** (`clean_regex.py`): deterministic pattern-matching rules for dates, sex, site, and glucose values/units. Same rule applied to every row, no judgment calls per-record.
- **AI-assisted approach** (`ai_clean.py`): same general strategy, but built by walking through the raw data and making explicit interpretive decisions on ambiguous cases, then encoding those decisions in code so they applied consistently. This is the "AI-assisted" step for this lab, since the choices below came from an AI (Claude) reasoning about the data directly rather than a fixed rule written in advance.

Out of 60 records, the two methods disagreed on at least one field in 24 places. The disagreements fall into four categories:

## 1. Unit conversion precision (13 records)

Example: **s-0006**, raw value `159.9 mmol/L`. Regex converted using the precise factor (159.9 × 18.0182 = 2881.1 mg/dL); the AI approach used the commonly-quoted rounded factor (159.9 × 18.0 = 2878.2 mg/dL). Same pattern in S0011, S0013, S0015, S0026, S0034, S0037, S0039, s-0047, S0048, S0053, S0055, S0059.

This isn't really a *disagreement about the data*. Both methods correctly identified the same raw value and correctly recognized it needed converting. It's a disagreement about which conversion factor is "right," which regex can't resolve on its own: a regex has no concept of a conversion factor being more or less precise, a human or an AI has to supply that judgment. For a real clinical pipeline, this is the kind of silent numeric drift that's dangerous: it doesn't throw an error, it quietly changes downstream values by about 0.1%.

## 2. Blank sex vs. explicitly-recorded "unknown" (5 records: S0012, S0016, S0017, S0022, s-0036)

The raw `sex` field was blank (empty string) for these five records, different from rows where sex was explicitly recorded as `unknown` or `U` (e.g. S0007, S0032). The regex script's `SEX_MAP` had no separate case for an empty string, so it fell through to the same `"U"` default as explicit unknowns. The AI-assisted version treated blank as meaningfully different (a field that was never filled in vs. one where "unknown" was actively chosen) and coded it as `MISSING` instead.

This matters in practice: "the clinician recorded that sex was unknown" and "this field was left empty" can have different causes (a data entry gap vs. a genuine clinical ambiguity) and arguably shouldn't be silently collapsed into one code without a decision being made about it.

## 3. Date day/month order ambiguity (6 records: S0011, S0012, S0014, S0015, S0033, S0039)

Raw dates like `07.09.61`, `06.07.96`, `09.12.58`, `02.11.98`, `06.07.12`, and `04.12.80` are genuinely ambiguous: both the first and second number are ≤12, so nothing in the string itself indicates whether it's `MM.DD.YY` or `DD.MM.YY`. The regex script assumed `MM.DD.YY` uniformly, since that matched the pattern used elsewhere in the dataset (e.g. `07/09/1962`-style slash dates). The AI-assisted pass flagged these six specifically as ambiguous and interpreted them as `DD.MM.YY` instead, a different but equally defensible guess.

Example: **S0011**, raw `07.09.61`. Regex reads it as `1961-07-09` (July 9); AI reads it as `1961-09-07` (Sep 7). Neither is verifiably correct from the data alone.

## 4. Name capitalization (2 records: S0032, S0046)

The raw `patient_name` field was in ALL CAPS for two records (`J. SMITH`, `S. DAVIS`). The regex script was scoped only to `dob`/`sex`/`site`/`glucose` and never touched names, so it passed these through unchanged. The AI-assisted pass normalized them to title case (`J. Smith`, `S. Davis`), an obvious cleanup step a human or AI would naturally think to do but that wasn't in the regex script's original scope.

## Time/effort comparison

The regex script took longer to write correctly (getting all 4 date formats, the site abbreviations, and the unit conversion right required iterating), but once written, it is fully deterministic and auditable: every decision is visible in the code. The AI-assisted pass was faster to produce the *judgment calls* (immediately noticing the blank-vs-unknown distinction, the day/month ambiguity, and the name-casing issue), but those judgment calls are the parts that would need a human to sign off on before trusting them at scale. They're guesses, not derivations.

## Which is more reliable for real datasets?

Neither alone. The regex script is reliable and reproducible but blind to ambiguity: it will confidently produce a wrong answer with no warning. The AI-assisted pass is better at *noticing* ambiguity, but its guesses aren't more likely to be correct than the regex's, they're differently arbitrary. The practical takeaway is that AI is most useful here as an ambiguity-detector (flagging S0011, S0012, S0014, S0015, S0033, S0039 as genuinely uncertain, and flagging the blank/unknown distinction as a real modeling decision), while regex is more useful as the deterministic, auditable execution layer, once a human has decided how to handle the ambiguous cases.

## Failure mode analysis

At least 2 concrete records where results were incorrect or ambiguous, as required:

**Record s-0003** (`dob` raw: `11.24.53`): Two-digit year ambiguity. Both regex and AI resolved this to `1953` using the same heuristic (two-digit years ≤18 → 20xx, else 19xx), which happens to be correct for this synthetic dataset (all DOBs fall between 1950 and 2018) but is not a generally valid assumption. A record with a true DOB after 2018, or a truly ambiguous edge year, would break this heuristic silently, with no error raised. This is a **latent failure mode**: it looks correct here only because of an assumption about the dataset's range that isn't stated anywhere in the data itself.

**Record S0011** (`dob` raw: `07.09.61`): As discussed above, regex and AI produced two different, equally plausible dates (`1961-07-09` vs `1961-09-07`) with no way to determine which is correct from the raw string alone. This is an **irreducible ambiguity**: no amount of better regex or a smarter AI prompt can resolve it without an external source of truth, such as a data dictionary specifying the original format, or cross-referencing another field. Neither method should be trusted on this record without manual review. Five other records (S0012, S0014, S0015, S0033, S0039) have the exact same problem.

**Records S0039 and S0042** (`glucose_value` raw: `241.2*` and `209.0*`): Both methods got these right, correctly stripping the trailing `*` and flagging the record (`flagged(*)`) rather than either silently dropping the annotation or failing to parse the number at all. Worth flagging anyway: a less careful regex (one not expecting a stray character at the end of a numeric field) could easily have failed to match at all here and silently produced a missing value, or worse, parsed `241.2*` as a string and let it pass through unflagged into downstream analysis. Not a failure in this case, but the kind of mistake that's easy to make and easy to miss.
