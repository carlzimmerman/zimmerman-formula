# QX4: can the action, not the plain law, rescue AGC 114905 and Malin 1? Malin 1: NO (class no-go). AGC 114905: only via the external field (CONDITIONAL, environment data needed)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. One galaxy excludes nothing. Footings never pooled. Criteria:
FROZEN_CRITERIA.md (c0d7f31b1e), committed before any script. AMENDMENTS.md A1 (d891f0e28a), made before any graded
galaxy number. A2 (abe74b7df7), POST-RESULT and labelled. Data, errors and baryons come from UD1/UD2: their
committed code is executed read-only, and their files are not written.

## Labels

| Mechanism (from the action / the data) | AGC 114905 | Malin 1 |
|---|---|---|
| 1. Exact static field: full AQUAL solve of v3s/AC2q's static sector, not the algebraic law | **NOT RESCUED**: chi2 700 / 830 (alg. 844 / 996) | **NOT RESCUED**: chi2 54.7 / 42.9 (A1), 56.7 / 91.3 (A2), against alg. 69 / 132 |
| 2. External field effect (1D estimator) | **CONDITIONAL**: needs g_e = 0.076-0.29 a0 (both footings) | **NOT RESCUED** for any g_e in [0, 3 a0] (best chi2 26.5 / 21.5) |
| 3a. Action terms beyond AQUAL (v3s stiffness, AC2q s^2) | **NOT RESCUED**: <= 3.9e-4 / 4.3e-4, against a needed -0.81 / -0.83 in g | **NOT RESCUED**: <= 3e-6 against -0.28 / -0.34 |
| 3b. Distance | **NOT RESCUED**: needs D x 0.17-0.27 (13-22 Mpc against 78.7) | **NOT RESCUED**: no factor works (shape) |
| 3c. Baryon mass | **NOT RESCUED**: needs x 0.03-0.08 | **NOT RESCUED**: no factor works |
| 3d. Asymmetric drift / beam smearing | wrong sign (raises V_c) / affects inner rings only | n/a |
| 3e. Non-equilibrium | requirement: a disc younger than 150-156 Myr (0.07 orbital periods) | requirement: younger than 326-340 Myr (0.13 orbits) |

Both footings are given as canonical / alt. Inclination, from UD1/UD3, still does not rescue either galaxy.

- **Malin 1: class no-go.** No mechanism in the v3s/AC2q action rescues it at its measured inclination, and neither do
  distance, mass or the external field. The exact field narrows the miss (canonical 69 -> 55, alt 132 -> 43). The
  shape (a dip at 62.5 kpc, then a rise) stays.
- **AGC 114905: rescued only by an external field of 0.08-0.29 a0.** A regular disc needs the tidal pull across
  its 10 kpc to stay below its own g_int (0.021-0.025 a0). So the field must come from a host of baryonic mass
  >= 3.4e9 Msun (canonical) or >= 6.4e9 Msun (alt) at d >= 30-37 kpc, with the required mass growing as d^2.
  A Milky-Way-mass host would have to be within about 130 kpc; a large-scale field of that size would also work.
  No environment data are on disk, so the label is CONDITIONAL; NEEDS_OWNER.md lists the download. The only other
  open requirement is a disc 0.07 orbits old, which is not plausible for a regular, symmetric rotating disc.
  Everything else is NOT RESCUED.

## Iteration 1 in detail (exact AQUAL, aqual.py)

Axisymmetric finite volume in (ln r, theta), Picard iteration, Dirichlet sphere at r_max >= 300 x the outer ring.
The exact field lies BELOW the in-plane algebraic law wherever the disc's vertical Newtonian field is comparable to
the radial one (Brada & Milgrom 1995). Exact/algebraic V:
- AGC 114905: 0.82-0.98. A good share of the miss, but nowhere near the factor 2.3.
- Malin 1: 0.90-0.98 (A1), 0.96-1.01 (A2).

The convergence ladder (240x72 vs 480x144) agrees to 5e-4 (AGC) and 4.5e-3 (Malin), against a 1 % line.

Known answers:
- K1 Plummer: 1.0e-4 (line 1e-3). PASS.
- K2 Kuzmin vs the BM95 form: 0.46 % (line 2 %). PASS. The comparison uses |g_N| just above the disc, as BM95
  states it; against the in-plane RAR form the same exact field is 15 % lower at R = a/2 (reported).
- K3 Newton vs UD baryons: 0.09 % (AGC), 0.6 % (Malin). PASS.
- K4 Malin Sigma reconstruction: 0.7-1.6 %. PASS.

MUTATE (mu = 1) reproduces UD's Newtonian chi2: 55.0 vs 55.0 and 1758 vs 1753. PASS.

Tags:
- K1's fine-grid run and both A2 runs stopped at the 400-iteration cap with residual 1.4-1.9e-8, against the frozen
  1e-8 line. Their V values pass the ladder line.
- Malin 1's label stands because A1 (residual met) and A2 agree.
- A1's NNLS places 3.4e11 Msun of gas between 98 and 200 kpc, which the plot does not constrain. A2 removes it
  (gas 7.8e10 Msun).

### Side finding outside QX4's scope: the record's SPARC pass is the algebraic law, not the action's exact field

The frozen recheck (exponential discs, Sigma_0 10-1000 Msun/pc^2) gives |log10(g_exact/g_alg)| up to **0.097 dex
at R = R_d** (Sigma_0 = 10), falling to <= 0.006 by 6 R_d. That is above the 0.057 dex line. By the frozen rule no
RESCUED label may be given (none was earned anyway). It also means v3s's SPARC/RAR pass, which was graded with the
algebraic law, still owes an exact-field regrade. The exact field lowers inner-disc accelerations, most of all in
low-surface-density discs.

## Iterations 2 and 3

- Iteration 2's MUTATE (nu = 1) bites: with Newton, no g_e rescues AGC 114905.
- Iteration 3's MUTATE bites: with Newton the distance requirement moves to x 1.5-2.3.
- Lean: fable_independent_2026/lean_2026/QX4_udg.lean certifies three theorems, with 0 sorry and standard axioms only:
  - mu = x/(1+x) inverts the law's nu exactly;
  - the EFE host bound M > g_e^4 R^2/(G a0 g_int^2);
  - nu >= 1.
  The MUTATE twin fails on all three planted false claims.

## What this does not show

- Only one inclination per galaxy, as UD1/UD2/UD3 used.
- A 1D EFE estimator, not an exact EFE solve.
- No environment data; Malin 1's baryons are reconstructed from figures.
- No new data were downloaded.
