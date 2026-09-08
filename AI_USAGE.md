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

