# AI Usage

## Interaction 1: Diagnosing a conda dependency conflict

**Model used:** Claude (Sonnet 5), via Claude Code

**Task:** While completing the Week 2 practical, I intentionally broke my `environment.yml` by pinning `numpy=1.19` alongside `pandas=2.2`, then tried to rebuild the environment with `mamba env create -f environment.yml`.

**Exact error pasted to the AI:**
error libmamba Could not solve for environment specs
The following packages are incompatible
├─ numpy =1.19 * is requested and can be installed;
└─ pandas =2.2 * is not installable because there are no viable options
├─ pandas [2.2.0|2.2.1|2.2.2] would require
│ └─ numpy >=1.22.4,<2.0a0 *, which conflicts with any installable versions previously reported;
...
critical libmamba Could not solve for environment specs



**What I asked first:** I asked what the error meant before asking how to fix it. Claude explained that pandas 2.2 requires numpy >=1.22 (roughly, depending on the exact patch version) as a dependency, and that pinning numpy to 1.19 in the same file created a version requirement that no combination of installable packages could satisfy simultaneously — so the solver refused to install anything rather than produce a broken environment.

**Suggested fix:** Remove the `numpy=1.19` pin from `environment.yml` and let conda resolve a compatible numpy version automatically.

**How I verified the fix:** I did not apply it blindly. I re-read the error myself first to confirm the pandas/numpy version requirement it referenced actually matched what the fix proposed (i.e., that removing the pin, rather than pinning a different numpy version, was the correct fix given no other numpy version constraint existed in my file). I then removed the line and reran `mamba env create -f environment.yml`, which succeeded, installing numpy 2.5.2 and pandas 2.2.3 with no conflicts. I confirmed this by running `python analyze.py` again and checking the output matched my working environment from before the intentional break.

## Interaction 2: Building the Lab 2 analysis notebook (Framingham Heart Study)

**Model used:** Claude (Sonnet 5), via Claude Code

**Task:** For Lab 2, I asked Claude to help scaffold and build the analysis
notebook for the Framingham Heart Study dataset option: finding a working
public URL for the dataset (the course's `SOURCE.md` only had a placeholder
"stable URL — see open item below"), writing the data-loading/fetch code,
and drafting a transformation, visualization, and interpretation.

**What Claude did:** Claude fetched the course's `SOURCE.md` for this
dataset option, found it referenced a public mirror
(GauravPadawe/Framingham-Heart-Study on GitHub) but hadn't filled in the
actual stable URL, and verified that mirror's raw CSV URL actually resolved
(HTTP 200, correct columns) before using it. It then wrote a notebook that
bins age into decades, computes 10-year CHD incidence rate by age group and
sex, plots it, and compares systolic blood pressure between older
participants who did/didn't develop CHD.

**Where I checked its work:** Claude's first draft binned ages into 30s/40s/
50s/60s/70s, but I had it verify the data's actual age range — the dataset
only goes up to age 70, so the "70s" bin held just 2 rows (both from one
sex), making that group statistically meaningless. Claude caught this
itself by checking `age.describe()`, re-binned as 30s/40s/50s/60+, reran
the notebook, and rewrote the interpretation paragraph to cite the real
computed numbers (e.g. 25.3% vs 15.7% CHD rate in the 50s by sex; 152.9 vs
143.7 mmHg mean systolic BP) rather than placeholder estimates. I then
independently reviewed the printed groupby table and the rendered chart
myself to confirm the interpretation text matches the actual output before
accepting it.

**Reproducibility check:** I ran `jupyter nbconvert --to notebook --execute
--inplace` on the notebook (equivalent to Restart & Run All) to confirm it
executes cleanly end-to-end from a fresh kernel, then exported it to HTML.

