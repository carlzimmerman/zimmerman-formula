# FRZ5 RESULT: the forest row with the forest nuisance parameters refit

**Labels as frozen (FROZEN_CRITERIA.md 84ab155bc1):** cases A and C are **NO VERDICT (a twin does not bite)** on both
footings. Twin T3 was built so that the model could not absorb it exactly, and twin T4 missed its 1.25x factor.

**Labels under amendment A1 (04460600b2; post hoc, committed alone before its numbers; it redesigns only the two twins
and cannot move a refit number):**

| case | canonical | alt |
|---|---|---|
| **A, full layout at flux level (FRZ4 f = inf)** | **FOREST ROW FAILS AFTER REFIT** | **FOREST ROW FAILS AFTER REFIT** |
| B, settled f = 1, 2, 3 | NO VERDICT (inherited from FRZ4), ungraded | NO VERDICT (inherited from FRZ4), ungraded |
| C, FRZ1 matter-level ratio | FOREST ROW FAILS AFTER REFIT | FOREST ROW FAILS AFTER REFIT |

No frozen bracket flips the word, so neither label carries FRAGILE. THE RECORD'S GATE ALREADY REFITS does not apply:
the gate refits nothing, because it has nothing to refit (next section).

TEST lane: adopts nothing, relabels nothing (FRZ1, FRZ1R, FRZ3R and FRZ4 keep their labels), registers nothing.
Footings are never pooled. Cold dark energy is a gravitating field component; no particle is added. kappa = 1/2 is
FITTED. Nothing here says the data favour the framework.

## 1. What the record's gate does and does not refit

- **The gate** is `closure_2026_11_09/SS1_self_shielded_conversion/ss1_cosmo.py`:
  - `forest_setup` (lines 212 to 224) loads DESI DR1 QMLE P1D, 755 points, full covariance;
  - `forest_eval` (lines 228 to 238) returns **Delta chi^2 = d^T C^-1 d with d = (r - 1) x P_data** (line 237).
- **It is an Asimov Delta chi^2, not a fit.** No model is ever compared with the data. The reference forest model is
  assumed to equal the data, so its chi^2_min is 0 by construction. NC2's `nc2_g3.py` (line 4) names the convention:
  "Delta chi2_Asimov".
- **The model inside it has no forest nuisance parameter at all.** The ratio r is a ratio of linear-matter P1D
  integrals (`p1d_at`, lines 226 to 227). There is no T0, gamma, mean flux, pressure smoothing, resolution, amplitude
  or tilt. Nothing is free, nothing carries a prior, and nothing is refit.
- **"The fit it starts from"** is F1A's B2 cold fit, `closure_2026_11_07/F1A_primary_cmb_audit/parts/fit_B2_<footing>_cold.json`
  (loaded at `frz3r_grade.py` line 34 and `frz1_forest.py` line 50). It fits six cosmological parameters to the
  **Planck CMB** (its nuisances are CMB calibrations) and never sees the forest. It supplies only P_lin(k) and H(z).
- **How the ratio is applied:**
  - FRZ1 (`frz1_forest.py` lines 72 to 110) passes sqrt(R_cold) into `forest_eval`.
  - FRZ3R and FRZ4 (`frz3r_grade.py` lines 40 to 48; `frz4_grade.py` lines 55 to 68 and 89) use the same quadratic form
    on R_F from FGPA boxes.
  - FRZ4's gas inputs (T0 1e4 K, gamma 1.5, lambda_P 79 comoving kpc, tau_eff(z)) are held fixed. They are bracketed,
    never fitted.
- **In plain words:** the lead's worry is right in effect but not in letter. The gate does not hold fitted nuisance
  parameters at the rival's best fit. It has no such parameters, which is the same as treating all forest gas physics
  as exactly known.
- **Reading S (strict, from the brief's parameter rule):** the record's own refit set is empty, so the refit equals the
  fixed number (269.1 / 288.4; 9916 / 9009). That reading cannot answer the question.
- **The primary reading therefore uses the record's only forest nuisance model on these data:** P1D3
  (`rebuild_2026_10_22/P1D3_m6_desi_dr1_growth/p1d3_m6_desi.py` lines 179 to 245). Per bin it has:
  - an amplitude A_j > 0 (no prior);
  - a tilt alpha_j in [-1, 1];
  - a smoothing R_J,j in [0.02, 0.30] Mpc/h.

  That is 36 parameters. They are applied to the gate's own P1D with the base at A = 1, alpha = 0 and R0 = lambda_P =
  0.0533 Mpc/h. The statistic is the profiled Asimov Delta chi^2 (P1D3's own G1 convention) on the full covariance.

## 2. Table per case

The fixed number is the record's, reproduced exactly. The refit is the profiled number. Shifts are the largest over the
12 bins.

| case | footing | fixed | **refit** | max abs(A - 1) | max abs(alpha) | max abs(R - R0), Mpc/h (prior widths) | max shift, Fisher sigma | honesty |
|---|---|---|---|---|---|---|---|---|
| A f = inf | can | 269.14 | **23.04** | 0.040 | 0.013 | 0.031 (0.11) | 2.2 | OK |
| A f = inf | alt | 288.36 | **23.90** | 0.029 | 0.015 | 0.030 (0.11) | 2.1 | OK |
| B f = 1 | can / alt | 0.103 / 0.108 | 0.084 / 0.090 | 0.002 | < 0.001 | < 0.001 | 0.0 | OK |
| B f = 2 | can / alt | 0.503 / 0.413 | 0.228 / 0.209 | 0.003 | 0.001 | 0.001 | 0.1 | OK |
| B f = 3 | can / alt | 2.202 / 2.041 | 0.783 / 0.763 | 0.016 | 0.002 | 0.004 | 0.4 | OK |
| C FRZ1 matter | can | 9916.2 | **118.3** | 0.191 | 0.077 | 0.033 (0.12) | 4.9 | breaks: R_J at its 0.02 floor in most bins; A up to 1.19 |
| C FRZ1 matter | alt | 9008.7 | **107.4** | 0.174 | 0.069 | 0.033 (0.12) | 4.9 | breaks (18 violations) |

- **Case A per bin, canonical.**
  - A: 1.009, 1.037, 0.986, 1.040, 1.012, 0.997, 0.981, 0.983, 0.978, 0.981, 0.984, 0.986.
  - alpha: -0.007 to +0.013.
  - R: 0.079 at z 2.2, falling to 0.048 at z 4.4.
  - Every shift is small and inside its prior, and no parameter sits at a bound. The nuisance freedom removes 91 to 92 %
    of the Delta chi^2. What remains (23 / 24) is the part of the ratio's shape that an amplitude, a power-law tilt and a
    Gaussian smoothing cannot mimic: the rise and fall across k at low z, and the different shapes in neighbouring bins.
- **Case C:** the refit goes from 9916 to 118, but only by pushing R_J to its floor and the amplitudes beyond 15 %. It
  would count as FAILS even if it had come under 4.
- **Case B:** ungraded. Its numbers were already below the gate and fall by a further factor of 1.2 to 2.8.

## 3. Brackets (refit Delta chi^2; canonical / alt; an asterisk marks a broken honesty rule)

| bracket | A | C |
|---|---|---|
| A only | 134.4 / 105.5 | 3472* / 3110* |
| alpha only | 231.8 / 255.3 | 9815 / 8917 |
| R only | 47.5 / 57.9 | 2990* / 2499* |
| priors doubled | 23.04 / 23.90 (nothing near a bound) | 58.6* / 67.3* |
| R0 x 0.5 | 21.5* / 22.6* (R at the floor at z >= 3.4) | 307* / 264* |
| R0 x 2 | 25.5 / 26.0 | 94.6* / 107.6* |
| smooth in z (P1D3's V-smoothz) | 32.0 / 35.4 | 121* / 112* |
| reading G: FRZ4's own gas-bracket response (gamma, tau_eff, lambda_P; c in [-1, 1]) | 67.4 / 73.3 (c_gamma -0.65 / -0.73, c_tau -0.45 / -0.56, c_lambda -0.24 / -0.33) | 1812* / 1637 |
| reading G, c in [-2, 2] (reported only) | 67.4 / 73.3 | 1402 / 1316 |

- **The lowest value for case A is 21.5, from R0 x 0.5.** No bracket brings case A under 4. Reading G, which is FRZ4's
  physical gas response, absorbs less than P1D3's free template does (67 against 23).
- **The amplitude yardstick:** in FRZ4's base box, tau_eff x 0.9 / x 1.1 changes the reference flux power by 12 to 13 %
  at k_v 0.01 s/km. The frozen amplitude limit was 0.15. Case A uses at most 4 %.

## 4. Known answers and twins

**Known answers.**
- **K1 (pass):** the fixed numbers reproduce FRZ4 (269.1409, 288.3640; f = 1, 2, 3 to every digit) and FRZ1 (9916.246,
  9008.690) to relative 4e-16. A direct `forest_eval` call agrees as well.
- **K2 (pass), convention check:** the record's `cho_solve`, FRZ4's `dchi2_sel` and this lane's whitened form agree to
  1e-15. The record's Delta chi^2 convention and FRZ4's are the same quadratic form.
- **K3 (pass):** with r = 1, the refit gives 0 with every parameter at base.
- **K4 (pass):** the smoothing factor is 1 at R0, and raising R lowers it at the highest k in every bin.

**Twins (both footings).**
- **T1, doubled change: bites.**
  - Case A: 23.0 -> 79.5 (canonical), 23.9 -> 81.2 (alt).
  - Case C: 118 -> 3005 (canonical), 107 -> 2359 (alt).
- **T2, pure rescaling: bites.** The constant 1.05 goes from 574.5 fixed to 1e-26 refit; the version linear in z goes
  from 178.7 to 2e-26.
- **T3 as frozen: does not bite.** The fixed value 3895 refits to 0.093, against a limit of 1e-4. The twin was not
  exactly representable: P1D smoothing ratios do not compose after projection. **T3-A1 bites:** 5460 -> 4e-26.
- **T4 as frozen: does not bite.** With the amplitudes frozen, case A rises 23.0 -> 26.4 (canonical) and 23.9 -> 27.4
  (alt), factors 1.14 / 1.15 against the frozen 1.25. **T4-A1 bites:** on the constant twin with the amplitudes frozen,
  20.9 > 4.

## 5. What is left out

- **No hydrodynamics.** The ratios are FRZ4's FGPA boxes (case A/B) and FRZ1's halo model (case C), with all of FRZ4's
  caveats: real space, 20 Mpc/h box, one seed except z 2.2, six of twelve bins estimated by linear interpolation in z,
  and PROVISIONAL gas inputs.
- **The nuisance model is a template.** P1D3's amplitude, tilt and smoothing set is a linear proxy, and P1D3 itself
  found it fails the real data (chi^2 7017 / 719). It is used here only as a response template in the Asimov
  convention.
- **No forest emulator is on disk.** There are no T0 or gamma response tables at all twelve redshifts and no resolution
  or noise nuisances.
- **Reading G is limited.** It uses only the base box, only z 2.2 and 3.0 (held constant beyond), and it does not refit
  the framework ratio's own dependence on the gas parameters.
- **No independent measurement of the gas temperature** was found on disk. None was used.
- **The cosmological parameters were not refit.** F1A's cosmology is held, as in the record.

## 6. What this does to "the forest row fails"

The record's gate never fit the forest's gas physics. It treated it as exactly known, which inflates the forest
failure. Letting the record's own forest nuisance template float (a per-bin amplitude, a tilt and a smoothing, with
P1D3's bounds) and refitting removes about 91 % of the full layout's flux-level Delta chi^2: 269 / 288 falls to
23.0 / 23.9. The refit needs only small shifts: amplitudes within 4 %, tilts under 0.015, smoothing within 0.03 Mpc/h.
That is still about six times the gate of 4 on both footings, and no bracket brings it under 4 (lowest 21.5). The
physically tied gas response from FRZ4's own brackets absorbs less (67 / 73). So the forest row still fails for the
full layout at flux level, by a factor of about 6 rather than about 70. The matter-level number the record first used
(9916 / 9009) overstated the failure by more than a factor of 300. Even refit, it stays at 107 to 118, and only with
the smoothing pinned at its floor. The settled layout stays ungraded. Its numbers, already under the gate, fall further
(at most 0.78). This lane is post hoc in its twin amendment and is not a blind re-grade.

## Files and commits

- `FROZEN_CRITERIA.md` (84ab155bc1, alone).
- `frz5_refit.py` and the as-frozen outputs `frz5_<footing>.json/.out`, `frz5_<footing>_MUTATE.json/.out`
  (dcf2b304de).
- `AMENDMENT_A1.md` (04460600b2, alone).
- The `--A1` flag and outputs `frz5_<footing>_A1*.json/.out` (fa573ee430). The as-frozen path was re-run after the edit
  and reproduces its committed outputs; only the timing lines differ.
- Console logs are in `logs/` and are git-ignored.
- Machine: 23 s per run, 0.51 GB, one thread. Nothing was downloaded, nothing was written outside this folder, and
  nothing was pushed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
