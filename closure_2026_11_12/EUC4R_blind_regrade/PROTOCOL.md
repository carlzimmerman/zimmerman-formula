# EUC4R (BLIND RE-GRADE OF EUC4, PART A): PROTOCOL

Committed alone, before any EUC4R script exists and before any EUC4R number is computed. 2026-11-12.

kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s^2, graded separately, never pooled. Not
"theory closed". One-sided test: no outcome favours the framework. This lane is a blind re-grade; it does not relabel
EUC4.

## 1. What I read, what I do not

Read before my numbers are committed:
- `closure_2026_11_12/EUC4_wide_lenses/FROZEN_CRITERIA.md` (samples, statistic, words);
- `closure_2026_11_12/EUC1_eclipse_saturation_ceiling/FROZEN_CRITERIA.md` (the model EUC4 inherits);
- the archive's own data documentation, needed for units and the missing-value code: `README.txt` and
  `README_eclipse_dr1_catalogue_key_v20261103.md` in `_external_data/euclid_dr1_eclipse/`;
- value counts of five columns, read to write the loader: `lens_grade` (A 6,073 / B 8,999), `lens_model_success`,
  `final_sample`, `large_system_warning` (plain booleans, no blanks), and the identifier join (15,072 key rows, all
  matched in the object catalogue, no duplicates). No per-lens radius, mass, redshift, index or `b` has been read.

Not opened until my script and outputs are committed: everything else in `EUC4_wide_lenses/` and
`EUC1_eclipse_saturation_ceiling/` (`RESULT.md`, `euc4.py`, `euc1.py`, every output), A55's and A70's code (so the
Sersic deprojection and projection below are written from the criteria text, not from `M3D_star` / `M2D_from_g`),
the release review, and the EUC1 / EUC4 memory entries.

Seen by accident before this note (disclosed): the one-line commit subjects of EUC4's script and RESULT commits, shown
by `git log --oneline` (the brief asked for it to check the lane id) and in the session's start-up git status. They
state EUC4's word: WIDE LENSES BREAK THE CEILING on both footings. No EUC4 number was in them. The project memory
index loaded at start-up states EUC1's word (NO VERDICT / NO VERDICT). EUC4's criteria themselves disclose EUC1's
grade-A map (0.31 / 0.62 / 0.90 above 1.3 / 1.7 / 2.5 arcsec, 0.03-0.07 below 1 arcsec), EUC1's f25 on P (0.156 /
0.139) and on A+B (0.164 / 0.145). My word is therefore not blind to EUC4's word; my numbers are blind to EUC4's numbers.

## 2. What I compute (Part A only)

Samples W_B (theta_E >= 1.7"), secondary (1.3" <= theta_E < 1.7") and complement (theta_E < 1.0"), on grade B, as in
EUC4 §1. For each, per law (S, B) and footing: N, `f25` with a 95 % bootstrap interval, `f0`, median `b`. The word per
footing on W_B (and the secondary bin, labelled secondary) from law S. Check E2 and a mutation twin of my own.
Beside it, as a comparison of machinery only (section 4): my `f25` on EUC1's sample P.

Not done here: EUC4's robustness list (§3; cannot change the word), Part B, EUC1's checks K2-K6.

## 3. Ambiguities in the criteria and how I resolve them (fixed now)

1. **Prugniel-Simien form.** `p_n = 1 - 0.6097/n + 0.05463/n^2` (Lima Neto, Gerbal & Marquez 1999); `b_n` exact from
   `P(2n, b_n) = 1/2` (regularised lower incomplete gamma), not a series; enclosed mass
   `M(<r) = M* P(n(3 - p_n), b_n (r/R_e)^(1/n))`. If A55's `M3D_star` uses a series `b_n` or other `p_n` coefficients,
   differences are expected at the 1e-3 dex level, largest at n near 0.6.
2. **R_e** = `eclipse_effective_radius` (arcsec, not circularised) x D_A(z_l), as written; no circularisation.
3. **Constants.** G = 6.67430e-11, c = 299,792,458 m/s, M_sun = 1.98841e30 kg (IAU GM_sun / G), kpc =
   3.0856775814913673e19 m, arcsec = pi/648,000 rad.
4. **Distances.** Flat, E(z) = sqrt(Om (1+z)^3 + 1 - Om), Om = 0.3089, H0 = 67.74, no radiation (also at z_s = 1100,
   as written). Comoving distance by adaptive quadrature; D_ls = (chi_s - chi_l)/(1 + z_s).
5. **Source at infinity** = z_s = 1100 exactly. The convergence against z_s = 1e4 is printed.
6. **Projection.** `M_2D(<R) = (R^2/G) Int_0^U g(R cosh u) du`, U = arccosh(r_max/R), r_max = 1e6 kpc, Gauss-Legendre.
   The node count is mine (256 on [0, U] split at u = 4 into two 128-node panels); the change in `b` on doubling the
   nodes is printed and must be < 1e-4 dex.
7. **Root.** `b` by vectorised bisection on [-4, +4] dex, 60 halvings (`M_2D` is monotonic in the mass factor).
   Lenses at a bracket edge are counted and printed.
8. **Cuts.** Booleans as read; `large_system_warning == False` after the join on `unique_identifier` ==
   `Unique_Identifier`; the five validity conditions as written, so -99 fails them; counts of rows removed by each are
   printed. theta_E = `eclipse_effective_einstein_radius` (not the SIE value). Edges as written: W_B `>= 1.7`,
   secondary `>= 1.3` and `< 1.7`, complement `< 1.0`, on the stored values.
9. **f25** counts `b > 0.25` strictly; `f0` counts `b > 0`.
10. **Bootstrap.** `numpy.random.default_rng(20261112)`, 2,000 resamples of the sample's lenses with replacement; a fresh
    generator with that seed for each (sample, law, footing), so within a sample every statistic sees the same index
    sets; 95 % interval = 2.5th and 97.5th percentiles (numpy's default linear interpolation). Sensitivity, printed and
    not used for the word: the same with `numpy.random.RandomState(20261112)`. If the two generators put a bound on
    opposite sides of a threshold, RESULT says so.
11. **Words** (law S, per footing): BREAK if lower bound >= 0.25; NOT CONFIRMED if upper bound <= 0.10; NO VERDICT
    otherwise; NOT EVALUABLE if N < 30, E2 fails, or one of my machinery checks (section 4) fails.
12. **Mutation twin** (`EUC4R_MUTATE=newton`): a0 = 1e-30 on both footings; outputs carry `_mutate_newton`; the twin
    reads the main run's output and exits 1 if `f25` on W_B rises on both footings, exit 3 otherwise.

## 4. Checks

- **E2** (frozen in EUC4): identifiers with `lens_grade == 'A'` and with `lens_grade == 'B'` share none (count = 0).
  Also printed: agreement of the key catalogue's `lens_grade` with the object catalogue's `Expert_Grade`.
- **Machinery** (mine): point mass at a0 -> 0 returns M to 1e-6; a field g proportional to 1/r returns
  M_2D proportional to R to 1e-4; node doubling moves `b` by < 1e-4 dex; Sersic mass fraction inside r -> infinity is 1.
- **E1' (comparison, not a gate):** my `f25` on P beside EUC1's 0.156 / 0.139 quoted in EUC4 §2. A mismatch is a
  finding to trace after unblinding. I will not tune my code to it; any change after the first run is a bug fix,
  disclosed with its before and after numbers.
