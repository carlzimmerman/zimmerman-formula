# QX7 iter_1: cold sector switched by potential depth. Frozen label NO VERDICT; the numbers read FAIL

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: ../FROZEN_CRITERIA.md and FROZEN_CRITERIA.md (d9d76d87a2).
Script: qx7_iter1.py (one thread, about 1 min). Outputs: qx7_iter1.json/.out, MUTATE qx7_iter1_MUTATE.json/.out.

## Which scalar reads potential depth

- The K(Q) sector's own Q reads its own density, not the depth. In the cold regime Q - 1 = rho_d/(2A), and c_s^2(Q) is
  barotropic, so it falls in QX3 iter3's no-go class.
- AC2q's clock does read depth: X = s^2/(2N^2) gives delta X/X = -2 Phi. That includes every subhorizon long-wavelength mode,
  so a galaxy's key is its own depth plus the large-scale potential at its site.

## Result

- Large-scale potential today, on the QX3 G1 background (fitted A_s 2.04e-9, no Planck values):
  sigma_Phi = 4.5e-5 (k_min = H0/c), 2.7e-5 (k_min = 10 H0/c).
- Known answer K1: the large-scale Phi equals (3/5)^2 Delta_R^2 x 0.61. That is the expected growth/transfer suppression
  from the late vacuum term.
- These numbers are the same size as the cluster depths (X-COP keys 4.5e-5 to 1.2e-4) and about 10x the galaxies'
  (SPARC per-galaxy maximum: median 4.4e-7, max 5.4e-6).
- At the largest threshold that keeps every X-COP point cold (t = 4.53e-5 canonical, 4.66e-5 alt), the fraction of SPARC
  galaxies sitting at cold sites is:

| k_min | switch | canonical | alt | line |
|---|---|---|---|---|
| H0/c (graded) | one-sided | 0.164 | 0.157 | 0.05 |
| H0/c | two-sided | 0.315 | 0.301 | 0.05 |
| 10 H0/c (conservative) | one-sided | 0.052 | 0.047 | 0.05 |
| 10 H0/c | two-sided | 0.095 | 0.086 | 0.05 |

- Under the frozen window definition (every k_min and every switch shape), there is no window on either footing. The one
  near-window (alt, k_min = 10 H0/c, one-sided) is 1 % wide in t. It also assumes galaxies are unbiased tracers, which is
  generous: real galaxies sit preferentially in large-scale wells, and that would close it.
- What kills the depth key: Phi_LSS ~ 1e-5 sets the CMB anisotropy and cluster depths alike, so on this key a galaxy in a
  large-scale well looks like a cluster.

## Controls

- MUTATE A (t = 1e-7): cold fraction 0.51-1.00 on every case. **BITES.**
- MUTATE B (flipped switch must fail C1 for every t in [1e-7, 1e-3]): **DOES NOT BITE as frozen.** The design was wrong: a flipped
  switch with t > 1.2e-4 makes every X-COP point cold, so C1 alone can be met. Its full window (C1 and C2) is empty in every
  case (reported), but that is not the frozen statistic.
- By the frozen rule a control that does not bite gives NO VERDICT. The FAIL reading above rests on the numbers, not on that control.

## Also

- The superhorizon cut is stated in the criteria: an adiabatic superhorizon mode is a local time shift, so delta X/X is about 0.
- White dwarfs and neutron stars are cold sites, but the dust inside them at rho_d0 is 1e-36 / 1e-45 of the star. Not graded.
