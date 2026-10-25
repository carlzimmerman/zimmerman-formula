# X44_self_similar_cf — FROZEN CRITERIA (committed alone, before any script or number of this lane; paper estimate disclosed)

**Question.** X43's rule, Σ_core = max(a₀/(2πG), η Σ_coll), needed one external number: the formation concentration
c_f = 4, which is simulation-calibrated. Can c_f come from the self-similar infall solution itself? If so, does X43's rule
pass when regraded with the derived value?

Standing rules: κ = ½ FITTED. Footings never pooled. Route E, Newtonian, cold dark energy not matter. No simulation
calibration. Not "theory closed". Nothing here may say the data favour the framework.

## 1. The derivation (frozen definition)

- Self-similar secondary infall (Fillmore & Goldreich 1984; Bertschinger 1985), with an initial excess δM/M ∝ M^(−ε).
  Shells turn around at t_ta(M), with M_ta ∝ t^{2/(3ε)}. Spherical collapse gives t_coll = 2 t_ta. The interior profile is
  ρ ∝ r^(−γ), with γ = 9ε/(1 + 3ε) for ε ≥ 2/3 (γ = 9/4 at ε = 1). M(<r) ∝ r^{3−γ}.
- **Core (frozen):** the mass that had already collapsed when the formation object's outermost shell turned around, at
  t_f/2. Self-similarity then gives M_c / M_f = 2^{−2/(3ε)}, so
  x_c = r_c / r_f = 2^{−2/(3ε(3−γ))} and **c_f,SS = 1/x_c**.
- **Primary: ε = 1** (Bertschinger's point-mass infall, γ = 9/4). This is the same profile X43's η uses, so
  η = (4/(3B(1))) c_f,SS^{γ−1} is self-consistent.
- Paper estimate (disclosed): c_f,SS = 2^{8/9} = 1.85, so η = 5.66, well below X43's 14.83.

## 2. Regrade

X43's script, executed with c_f = c_f,SS and nothing else changed: SPARC, X30's cluster keys, and P4's 63 groups, with
X43's verdict rule. The label is **SS PASSES** or **SS FAILS: <keys>**. There is no external tag, since nothing external
is used.

Reported, no verdict weight:
- ε from the local EPS slope, ε = (n_eff + 3)/6 at the cluster median (the Fillmore–Goldreich branch with γ = 2 if ε < 2/3),
  and its c_f;
- the structural ratios of the infall solution (r_vir / r_ta = 1/2 from spherical collapse; Bertschinger's first caustic
  r₁/r_ta = 0.364, a literature value) as alternative "c" readings;
- the c_f needed for X43's two binding keys (from X43's c_f = 3 / 4 / 5 sensitivity, interpolated).

## 3. Checks

- **K0:** with c_f forced to 4, X43's numbers are reproduced exactly (groups Z +2.05, MGAS T3 OUTER Z +2.41).
- **K1:** c_f,SS from the closed form equals a direct numerical solution of M_c / M_f = 2^{−2/(3ε)} on the M ∝ r^{3−γ}
  profile, to 1e-12.
- **K2:** at ε = 1, γ = 9/4 exactly.
- **MUTATE:** t_coll = t_ta, dropping the factor 2. Then c_f,SS = 1, and K1's check against 2^{8/9} must fail.
