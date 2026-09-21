# Regex vs. AI-Assisted Cleaning: Comparison

## Method summary

- **Regex approach** (`clean_regex.py`): deterministic pattern-matching rules for dates, sex, site, and glucose values/units. Same rule applied to every row, no judgment calls per-record.
- **AI-assisted approach** (`ai_clean.py`): same general strategy, but built by walking through the raw data and making explicit interpretive decisions on ambiguous cases, then encoding those decisions in code so they applied consistently. This is the "AI-assisted" step for this lab, since the choices below came from an AI (Claude) reasoning about the data directly rather than a fixed rule written in advance.

Out of 60 records, the two methods disagreed on at least one field in 20 places. The disagreements fall into three categories:

## 1. Unit conversion precision (11 records)

Example: **S0006**, raw value `141.2 mmol/L`. Regex converted using the precise factor (141.2 × 18.0182 = 2544.2 mg/dL); the AI approach used the commonly-quoted rounded factor (141.2 × 18.0 = 2541.6 mg/dL). Same pattern in S0014, S0015, s-0016, s-0017, S0024, S0033, S0035, s-0038, S0039, S0046.

This isn't really a *disagreement about the data*. Both methods correctly identified the same raw value and correctly recognized it needed converting. It's a disagreement about which conversion factor is "right," which regex can't resolve on its own: a regex has no concept of a conversion factor being more or less precise, a human or an AI has to supply that judgment. For a real clinical pipeline, this is the kind of silent numeric drift that's dangerous: it doesn't throw an error, it quietly changes downstream values by about 0.1%.

## 2. Blank sex vs. explicitly-recorded "unknown" (4 records: S0013, S0018, S0037, S0046)

The raw `sex` field was blank (empty string) for these four records, different from rows where sex was explicitly recorded as `unknown` or `U`. The regex script's `SEX_MAP` had no separate case for an empty string, so it fell through to the same `"U"` default as explicit unknowns. The AI-assisted version treated blank as meaningfully different (a field that was never filled in vs. one where "unknown" was actively chosen) and coded it as `MISSING` instead.

This matters in practice: "the clinician recorded that sex was unknown" and "this field was left empty" can have different causes (a data entry gap vs. a genuine clinical ambiguity) and arguably shouldn't be silently collapsed into one code without a decision being made about it.

## 3. Date day/month order ambiguity (4 records: s-0034, S0037, S0058, S0060)

Raw dates like `06.07.12`, `09.06.98`, `02.08.89`, and `02.09.06` are genuinely ambiguous: both the first and second number are ≤12, so nothing in the string itself indicates whether it's `MM.DD.YY` or `DD.MM.YY`. The regex script assumed `MM.DD.YY` uniformly, since that matched the pattern used elsewhere in the dataset (e.g. `07/09/1962`). The AI-assisted pass flagged these four specifically as ambiguous and interpreted them as `DD.MM.YY` instead, a different but equally defensible guess.

Example: **S0060**, raw `02.09.06`. Regex reads it as `2006-02-09` (Feb 9); AI reads it as `2006-09-02` (Sep 2). Neither is verifiably correct from the data alone.

## Time/effort comparison

The regex script took longer to write correctly (getting all 4 date formats, the site abbreviations, and the unit conversion right required iterating), but once written, it is fully deterministic and auditable: every decision is visible in the code. The AI-assisted pass was faster to produce the *judgment calls* (immediately noticing the blank-vs-unknown distinction and the day/month ambiguity), but those judgment calls are the parts that would need a human to sign off on before trusting them at scale. They're guesses, not derivations.

## Which is more reliable for real datasets?

Neither alone. The regex script is reliable and reproducible but blind to ambiguity: it will confidently produce a wrong answer with no warning. The AI-assisted pass is better at *noticing* ambiguity, but its guesses aren't more likely to be correct than the regex's, they're differently arbitrary. The practical takeaway is that AI is most useful here as an ambiguity-detector (flagging s-0034, S0037, S0058, S0060 as genuinely uncertain, and flagging the blank/unknown distinction as a real modeling decision), while regex is more useful as the deterministic, auditable execution layer, once a human has decided how to handle the ambiguous cases.

## Failure mode analysis

At least 2 concrete records where results were incorrect or ambiguous, as required:

**Record s-0003** (`dob` raw: `11.24.53`): Two-digit year ambiguity. Both regex and AI resolved this to `1953` using the same heuristic (two-digit years ≤18 → 20xx, else 19xx), which happens to be correct for this synthetic dataset (all DOBs fall between 1950 and 2018) but is not a generally valid assumption. A record with a true DOB after 2018, or a truly ambiguous edge year, would break this heuristic silently, with no error raised. This is a **latent failure mode**: it looks correct here only because of an assumption about the dataset's range that isn't stated anywhere in the data itself.

**Record S0060** (`dob` raw: `02.09.06`): As discussed above, regex and AI produced two different, equally plausible dates (`2006-02-09` vs `2006-09-02`) with no way to determine which is correct from the raw string alone. This is an **irreducible ambiguity**: no amount of better regex or a smarter AI prompt can resolve it without an external source of truth, such as a data dictionary specifying the original format, or cross-referencing another field. Neither method should be trusted on this record without manual review.

**Record S0012** (`glucose_value` raw: `N/A`): Both methods got this one right, treating it as missing instead of trying to force it into a number. Worth flagging anyway: if either script had instead treated `N/A` as `0`, the mean glucose calculation later on would come out wrong with no error thrown to warn anyone. Not a failure here, but the kind of mistake that's easy to make and easy to miss.
