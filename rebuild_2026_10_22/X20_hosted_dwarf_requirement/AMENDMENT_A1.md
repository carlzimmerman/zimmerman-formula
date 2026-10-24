# X20 AMENDMENT A1 (post-result; check code only; verdict logic untouched)

**What happened.** The first full run (exit 1) failed K2's separation clause: the oracle V = the E column of
`x1_per_system.csv` has ρ_S = +1.000 and z 18.0 / 17.8 (the z clause passes), but it does not SEPARATE the EXTRA and NONE
labels (4 / 3 offenders, canonical / alt).

**Why this is a check-design error, not a physics result.** The frozen labels are defined on Z_i = E_i / s_i (§1), and
s_i differs between systems. A system with small E and a small s_i can be EXTRA while a system with larger E and a large
s_i is NONE, so E itself cannot separate the labels by construction. The positive control for the separation scan must
use the label-generating variable.

**Change.** K2's separation clause now uses the oracle Z = (E from `x1_per_system.csv`) / s_i. The z clause still uses the
CSV E column. Nothing else changed: no variable, statistic, threshold, sample or verdict rule. Every correlation and
separation number of the lane is identical before and after A1 (the first run's verdict and tables are those reported).

**MUTATE.** The twin shuffles the analysis draws, so the CSV-E oracle no longer tracks the analysis E and K2 must still
FAIL.

**Second check-code change (same amendment, before the MUTATE run was committed).** In the first MUTATE run K2 failed only
as "not run (stop rule)". K2 is now computed even when K0/K1 stop the verdict, so the twin tests K2's content: under
MUTATE it fails on ρ −0.147 / −0.017 (z 1.3 / 0.1) and 25 / 26 offenders (`x20_hosted_dwarf_requirement_MUTATE.out`).
The normal run is unchanged (K2 PASS; verdict and every table identical).
