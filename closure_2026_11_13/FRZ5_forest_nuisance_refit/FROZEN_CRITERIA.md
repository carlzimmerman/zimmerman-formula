# FRZ5 FROZEN CRITERIA (2026-11-13): the forest row with the forest nuisance parameters refit

Committed alone, before any script of this lane exists and before any number of this lane has been computed.
TEST lane: adopts nothing, relabels nothing (FRZ1, FRZ1R, FRZ3, FRZ3R, FRZ4, SRH1, SRF1 keep their labels), registers
nothing. Footings (canonical, alt) graded separately, never pooled. Cold dark energy is a gravitating field component; no
particle is added. kappa = 1/2 is FITTED. A HOLDS label is a hit that awaits an independent blind re-grade, not a pass
of the theory. Nothing here can say the data favour the framework.

## 1. What the record's gate does, read from the code (before any number)

- **The gate** is `forest_eval` in `closure_2026_11_09/SS1_self_shielded_conversion/ss1_cosmo.py`, lines 228 to 238
  (data loader `forest_setup`, lines 212 to 224: DESI DR1 QMLE P1D, `P1D_BLIND` table, 0.001 < k < 0.5 pi / R_z, 755
  points, full `COVARIANCE`, md5 33d7fc21...). It computes a ratio r(k, z) at the data points and returns
  **Delta chi^2 = d^T C^-1 d with d = (r - 1) x P_data** (line 237).
- **That is an Asimov Delta chi^2, not a fit.** No model is ever compared with the data. The data enter only as the scale
  P_data and through the covariance. The reference forest model is taken to equal the data exactly, so chi^2_min of the
  reference is 0 by construction. The record names this convention itself: NC2's `nc2_g3.py` header calls it
  "Delta chi2_Asimov = d^T C^-1 d, d = (r - 1) x PLYA".
- **The model inside the gate has no forest nuisance parameter at all.** The ratio is a ratio of linear-matter P1D
  integrals (`p1d_at`, line 226 to 227) with each model's H(z) for the k conversion. There is no gas temperature, no
  density slope gamma, no mean flux, no pressure smoothing, no resolution or noise term, no amplitude or tilt. None was
  free and none carries a prior, because none exists. The gate refits nothing.
- **"The fit it starts from"** is F1A's B2 cold fit, `closure_2026_11_07/F1A_primary_cmb_audit/parts/fit_B2_<footing>_cold.json`,
  loaded by FRZ3R's `frz3r_grade.py` line 34 and FRZ1's `frz1_forest.py` line 50. Its free parameters are h, omega_b,
  omega_cold, ln(10^10 A_s), n_s, tau_reio, fitted to the **Planck CMB** likelihood (its `nuis` entries are CMB
  calibration terms). It never saw the forest. It supplies the linear P(k) and H(z) of the reference only.
- **How the ratio is applied.** FRZ1 (`frz1_forest.py` lines 72 to 110): the matter-power ratio R_cold(k, z_bin) as an
  amplitude sqrt(R) on the CLASS grid, nearest DESI bin per grid redshift, into `forest_eval`. FRZ3R / FRZ4
  (`frz3r_grade.py` lines 40 to 48; `frz4_grade.py` lines 55 to 68 and 89): the flux-power ratio R_F(k_v, z) from FRZ4's
  FGPA boxes interpolated onto the data points, then `dchi2_sel(r, ALL)`, the same quadratic form with the covariance
  rebuilt from the Cholesky factor.
- **Where gas parameters do exist:** inside FRZ4's own flux build (T0 = 1e4 K, gamma 1.5, lambda_P = 79 comoving kpc,
  tau_eff(z) formula), all held fixed, with brackets (gamma 1.2 / 1.6, tau_eff x 0.9 / 1.1, lambda_P x 0.5 / x 2) run at
  z 2.2 and 3.0 only. They shape the ratio R_F, and they are never fitted to the data.
- **The only fit in the record of DESI DR1 P1D with forest nuisance parameters** is P1D3
  (`rebuild_2026_10_22/P1D3_m6_desi_dr1_growth/`, criteria d50412913d, result 40ae4d5c4c): per redshift bin a free
  amplitude b_z^2 > 0 (no prior), a pressure-smoothing scale R_J,z in [0.02, 0.30] Mpc/h (flat, filter exp(-k^2 R_J^2)
  on the 3D power), a tilt alpha_z in [-1, 1] (flat) on (k / k_p)^alpha with k_p = 0.01 s/km
  (`p1d3_m6_desi.py` lines 179 to 245: `shapes`, `chi`, `bounds`). P1D3's G1 (line 320) is a **profiled Asimov Delta chi^2**: exactly the statistic
  asked for here.

So the lead's description is right in effect and wrong in letter. The gate does not hold fitted nuisance parameters at
the rival's best fit. It has none: it is equivalent to holding every forest nuisance parameter fixed and known.

## 2. Readings

- **Reading S (strict, as the brief's parameter rule reads):** refit exactly the forest parameters free in the record's
  own fit. That set is empty, so the refit Delta chi^2 equals the fixed one. Reported as a statement, with the
  fixed-parameter numbers. It cannot answer the question.
- **Reading P (primary; gives the labels):** P1D3's nuisance set and priors, the record's only forest nuisance model on
  these data, nothing added and nothing widened. Per bin j (all 12 DESI bins, each its own parameters: 36 in all):

  N_j(k) = A_j x (k / 0.01 s/km)^alpha_j x S_j(k; R_j) / S_j(k; R0),

  S_j(k; R) = the gate's own P1D integral (`p1d_at`) of the gate's own linear P(k, z_j) (F1A CLASS) times
  exp(-K^2 R^2), K the 3D wavenumber, at the gate's own k_par = k_v H(z_j) / (1 + z_j) with the reference H.
  Bounds: A_j > 0 free (log A in [-3, 3], a numerical box only); alpha_j in [-1, 1]; R_j in [0.02, 0.30] Mpc/h
  (converted to Mpc with the F1A h).
  Base (the record's values, N = 1): A = 1, alpha = 0 (the gate's reference has no tilt), R0 = lambda_P = 79 comoving kpc
  = 0.079 x h Mpc/h (FRZ4's and FRZ3R's pressure-smoothing value; a power filter exp(-k^2 lambda_P^2) is FRZ4's density
  filter exp(-k^2 lambda_P^2 / 2) squared).
  **Statistic:** Delta chi^2_refit = min over theta of e^T C^-1 e, e = (r x N(theta) - 1) x P_data, full 755 x 755
  covariance, cross-z kept. In the Asimov convention the framework-free chi^2_min is 0 (theta = base), so this is the
  difference asked for. Beside it, the fixed number (theta = base), which must reproduce the record.
  Minimiser: bounded least squares on the whitened residual (scipy `least_squares`, trf), started from the base and
  from two further starts (R at 0.03 and 0.2 Mpc/h with A, alpha at base); the lowest is kept.

## 3. Cases (both footings, never pooled)

- **(A) Full layout at flux level:** FRZ4's case f = inf, R_F exactly as `frz4_grade.py` builds it (seed mean,
  stratified estimator, `r_points`): computed bins z 2.2, 2.6, 3.0, 3.4, 3.8, 4.4; estimated bins z 2.4, 2.8, 3.2, 3.6,
  4.0, 4.2 linear in z between computed neighbours, as FRZ4. GRADED.
- **(B) Settled layout f = 1, 2, 3** at flux level, FRZ4's same build. FRZ4 left them NO VERDICT (seed scatter e). Their
  numbers here are reported **UNGRADED**; no label beyond "NO VERDICT (inherited from FRZ4)".
- **(C) FRZ1's matter-level ratio as the record first applied it:** `frz1_hm.json` case "primary|<footing>", R_cold per
  DESI bin, through FRZ1's `Rkz_z` and the gate's ratio computation (`forest_eval`'s r). GRADED (comparison case).

## 4. Known answers (all must pass for a label)

- **K1 fixed number reproduces the record:** my r vector with theta = base gives FRZ4's flux Delta chi^2 (canonical
  269.1409 / alt 288.3640 at f = inf; f = 1, 2, 3: 0.10288 / 0.10756, 0.50301 / 0.41284, 2.20176 / 2.04113) and FRZ1's
  9916.246 / 9008.690, each to relative 1e-6.
- **K2 convention:** the record's `cho_solve` form (line 237) and FRZ4's rebuilt-covariance `dchi2_sel` agree on case A
  to relative 1e-8; the refit's whitened chi^2 at theta = base equals both to relative 1e-8.
- **K3 framework-free recovery:** r = 1 gives refit Delta chi^2 <= 1e-8 with every parameter at its base to 1e-4.
- **K4 nuisance response sane:** at R = R0 the smoothing factor is exactly 1; raising R lowers N at the highest data k
  in every bin.

## 5. Twins that must bite (`*_MUTATE*` outputs)

- **T1 doubled change:** r -> 1 + 2 (r - 1). Refit Delta chi^2 must rise (factor >= 1.25 if the primary refit is >= 0.1;
  otherwise must not fall). Per graded case and footing.
- **T2 pure rescaling the nuisance absorbs exactly:** r = 1.05 in every bin, and r = 1 + 0.05 (z - 3.3): the fixed
  number must be large (> 100) and the refit <= 1e-4.
- **T3 nuisance-shaped change:** r = (k / 0.01)^0.1 x S(k; R0 + 0.02 Mpc/h) / S(k; R0): refit <= 1e-4.
- **T4 mutation that must bite:** refit with every A_j frozen at 1 on case A: Delta chi^2 must not fall below the
  primary refit and must exceed it by >= 1.25x OR the primary amplitude shifts must all be below 1e-3 (then reported as
  "amplitude idle").
- A twin failing to bite gives NO VERDICT for that case and footing.

## 6. Honesty rule on the refit (frozen numbers)

A refit counts only if:
- no bounded parameter ends within 1 % of its range of a bound (alpha within 0.02 of +/-1; R within 0.0028 Mpc/h of
  0.02 or 0.30);
- no bounded parameter moves from base by more than **0.5 of its prior width** (alpha: 1.0; R: 0.14 Mpc/h);
- no amplitude moves by more than **|A_j - 1| = 0.15**. P1D3 gives b_z^2 no prior; 0.15 is frozen here as the outer
  edge of a mean-flux-driven amplitude change, and the amplitude change FRZ4's own tau_eff x 0.9 / x 1.1 bracket makes
  in the reference flux power at k_v = 0.01 s/km (z 2.2, 3.0, base box) is reported beside it as a yardstick, not
  used to move the line.
Report every shift in prior widths and in Asimov Fisher 1 sigma at the refit (from the Jacobian). A refit that reaches
Delta chi^2 <= 4 only by breaking this rule is labelled HOLDS ONLY WITH A PARAMETER AT ITS BOUND OR BEYOND THE FROZEN
SHIFT, which counts as FAILS, and names the parameter.

## 7. Brackets (reported; FRAGILE if one flips the word; word = FAILS if Delta chi^2 > 4 or the honesty rule breaks)

1. Each parameter family freed alone: A only; alpha only; R only.
2. Priors doubled in width: alpha in [-2, 2]; R in [0.001, 0.44] Mpc/h (width 0.28 -> ~0.56 about P1D3's centre
   0.16, floored); amplitude limit 0.30; honesty shifts doubled (alpha 2.0, R 0.28).
3. R0 x 0.5 and R0 x 2 (FRZ4's lambda_P bracket).
4. Smooth-in-z (P1D3's V-smoothz): R_j = r0 + r1 (z - 3.3), alpha_j = a0 + a1 (z - 3.3), clipped to the P1D3 bounds,
   r1 in [-0.2, 0.2], a1 in [-1, 1]; A_j free per bin.
5. **Reading G, gas response from FRZ4's own bracket boxes** (base box, seed 0, reference flux power): per parameter i
   in (gamma, tau_eff, lambda_P), L_i^+/-(k, z) = ln(P_F,R(bracket +/-) / P_F,R(primary)) at z 2.2 and 3.0;
   N = exp(sum_i c_i L_i^sign(c_i)), c_i in [-1, 1] (the record's own bracket range; -1 = gamma 1.2, tau x 0.9,
   lambda x 0.5; +1 = gamma 1.6, tau x 1.1, lambda x 2), three coefficients common to all bins; bins between 2.2 and
   3.0 linear in z, bins below 2.2 take 2.2, bins above 3.0 take 3.0 (held). The framework ratio r is held at the
   primary gas values (its own dependence on the gas parameters is not refit; disclosed). Honesty: no c_i at +/-1.
   Doubled-prior version c_i in [-2, 2] (log-linear extrapolation) reported, not part of FRAGILE.

## 8. Labels per graded case (A, C) and footing

- NO VERDICT if a known answer fails or a twin does not bite.
- FOREST ROW FAILS AFTER REFIT if Delta chi^2_refit > 4.
- FOREST ROW HOLDS AFTER REFIT if <= 4 and the honesty rule holds: a HIT awaiting an independent blind re-grade, not a
  pass of the theory; the shifts it needs are stated.
- HOLDS ONLY WITH A PARAMETER AT ITS BOUND OR BEYOND THE FROZEN SHIFT (counts as FAILS; names which).
- THE RECORD'S GATE ALREADY REFITS: not available. Section 1 shows the gate refits nothing.
- Append FRAGILE (bracket names) if a bracket of section 7 items 1 to 5 flips the word.
- Case B: numbers only, "NO VERDICT (inherited from FRZ4)".

## 9. Expectation and hand estimate (written before any number)

- FRZ4's case A ratio at z 2.2 runs 1.026 / 1.041 / 1.066 / 1.089 / 1.066 at k_v 0.003 / 0.005 / 0.01 / 0.02 / 0.03 s/km
  and is nearly flat (1.5 to 2 %) at z 3.0, turning down 2 to 3.5 % at the high-k end by z 4.4. A per-bin amplitude
  removes the mean (~5 % at z 2.2), a tilt removes the rise (alpha ~ 0.02 to 0.03, well inside the prior), and a larger
  R_J imitates the high-k downturn. What is left is the curvature of the rise-then-fall at z 2.2 to 2.6: roughly 1 % of
  the power over 20 to 40 points per bin at DESI's ~1 % low-z errors (strongly correlated). Hand estimate: case A refit
  Delta chi^2 about 5 to 40 per footing, central ~15, down from 269 / 288 by a factor 10 to 50. I expect FAILS AFTER
  REFIT, but a HOLDS is possible; amplitude shifts ~5 %, alpha shifts < 0.05, R shift < 0.05 Mpc/h.
- Case C (matter level, 9916 / 9009): the matter ratio dips 8 to 20 % at 3D k 3 to 5 h/Mpc; in P1D that is a smooth
  suppression rising with k, much of it smoothing-shaped. Expect a large fall but still FAILS: refit 100 to 2000.
- Case B: fixed numbers are already below 4, so the refit can only lower them: < 2.2 / 2.0.
- Reading G: the base-box gas responses are 10 to 40 % (looked at before freezing: three k values of each bracket at
  z 2.2, base box, to check the parts hold the reference power per bracket); I expect it to absorb more than P1D3's set at
  low z and less at high z, where it is held.

## 10. Outputs and rules

- `frz5_refit.py` (one script; footing as argument; MUTATE twins as a flag), `frz5_<footing>.json/.out`,
  `frz5_<footing>_MUTATE.json/.out`, `RESULT.md`. Paths relative to the script; no home paths; warnings suppressed; one
  or two threads; under 4 GB. Reads FRZ4, FRZ3R, FRZ1, F1A and the SS1 gate read-only; writes nothing outside this
  folder.
- Any change after this commit is a dated amendment committed alone, and RESULT.md reports the as-frozen reading first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
