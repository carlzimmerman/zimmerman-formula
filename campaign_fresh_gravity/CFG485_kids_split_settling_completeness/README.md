# CFG485: does settling completeness produce the KiDS early/late split? NOT DIAGNOSTIC: the predicted difference is about 100 times too small

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone before any script (019eb965a).
- **Script:** `cfg485_settling_split.py`, about 1 min. It uses on-disk data only; nothing was downloaded.
- **Runs:**
  - Main run: 17 of 18 checks pass. The one failure is H1, the "SUPPORTED" headline, so the script exits 1, as CFG95 does when its headline fails.
  - MUTATE run (ages shuffled): also fails H1. So for the headline it is uninformative, as declared in advance. It does flip the sign of the settling increment (see Controls).
- **Post-hoc check:** `cfg485_verify.py`, written after the main run. It has no verdict weight.
- **Outputs:**
  - `cfg485_settling_split.out` and `_results.json`, plus the `_MUTATE` pair;
  - `cfg485_verify.out` and `cfg485_verify_results.json`.

## Bottom line

**Settling completeness, at the zero-constant rate (λ = 1) with the 5.85 r_M mass-conserving edge, cannot produce the KiDS early/late split.**
- **The prediction has the right sign but almost no size.** Early types come out fully settled. Late types are about 0.2% unsettled on average. That makes the predicted early-minus-late increment 0.003–0.085 Msun/pc² on K1, against a measured difference of 2–33 Msun/pc².
- **The increment is undetectable.** Its own signal-to-noise is 0.013–0.018 in every cell. It improves χ² over the colour-blind control by only 0.017–0.029.
- **What the data want.** Along the predicted direction, the data prefer about 160–200 times the predicted increment (ŝ ≈ 160–197 ± 108–143).
- **The verdict.** Every cell is N, so the frozen rule gives **NOT DIAGNOSTIC**. In plain terms, the reading fails to produce the split, but it is not contradicted on sign.

## Primary numbers

χ² with the free two-halo amplitude profiled, 6 dof.

| footing / data | S (settling) | B2 (uniform f) | B1 (CFG95 law) | Δχ² vs B1 | Δχ² vs B2 | ŝ/σ_s | SNR of increment | cell |
|---|---|---|---|---|---|---|---|---|
| canonical, released | 4.54 (p 0.60) | 4.56 | 5.51 (p 0.48) | +0.97 | +0.023 | +1.36 | 0.018 | N |
| canonical, re-measured | 6.57 (p 0.36) | 6.60 | 6.70 (p 0.35) | +0.13 | +0.029 | +1.59 | 0.016 | N |
| alt, released | 4.82 (p 0.57) | 4.84 | 5.40 (p 0.49) | +0.58 | +0.017 | +1.20 | 0.014 | N |
| alt, re-measured | 6.02 (p 0.42) | 6.05 | 6.59 (p 0.36) | +0.56 | +0.023 | +1.49 | 0.013 | N |

**Without the two-halo term** (CFG95's own statistic, 7 dof; row R7), the split stays a failure:

| | S (settling) | B1 (CFG95 law) |
|---|---|---|
| canonical, released | 18.66 (p 0.009) | 20.30 |
| canonical, re-measured | 25.99 (p 5e-4) | 26.68 |
| alt, released | 17.49 (p 0.015) | 18.59 |
| alt, re-measured | 23.91 (p 0.001) | 24.79 |

## Why the settled fractions are all near 1

- **Settling is fast compared with the ages.** The dynamical time inside the 5.85 r_M edge is short:
  - early types, median 0.20 Gyr (canonical) / 0.17 Gyr (alt);
  - late types, median 0.16 / 0.13 Gyr.
- **The proxy ages are much longer.** The median t_age is 10.0 Gyr for early types and 3.4 Gyr for late types.
- **The resulting unsettled fractions are tiny.**
  - Early types: M_gal-weighted mean q = 1 − f of 4.5e-11 (canonical) and 3.7e-12 (alt); no early lens has q > 1e-3.
  - Late types: mean q of 2.5e-3 / 1.9e-3. This comes entirely from the young tail of the proxy: 19% of late types have t_age < 1 Gyr, 4.5% have t_age < 0.3 Gyr, and 3,133 of 93,398 have q > 0.1.
- **The edge sets this.** At fixed g_bar the edge lies at g_bar = a0/34.2 for every lens, so in K1 the settled phantom acts almost as a point mass of 5.364 f M_b. At λ = 1 it is filled within a few dynamical times, whatever the colour.

## What it would take (post-hoc diagnostic, `cfg485_verify.py` V4; not a fit, no verdict weight)

- **The test.** Take the fully settled truncated model, keep early types fully settled, and let a single unsettled fraction c apply to all late types. c is fitted to the split.
- **The answer.**
  - With the free two-halo term: c = 0.33–0.44 ± 0.25–0.30.
  - Without it: c = 0.52–0.71 ± 0.14–0.16, at χ² 3.2–5.8/6.
  - The predicted value is 0.002–0.003.
- **What that would mean.** Reaching it at the median late-type age needs λ ≈ 0.016–0.044 instead of 1.
  - That is a new constant, against the zero-knob standard.
  - At such a λ the early types would not be fully settled either, so this is not a consistent settling model. It is shown only as the size of the gap.

## Reported brackets (rows declared in advance; no verdict weight)

| row | what changes | SNR of increment | Δχ² vs B2 | ŝ (times the predicted increment the data want) |
|---|---|---|---|---|
| R2 | density = local density at the edge (the slowest shell) | 0.03–0.05 | ≤ 0.08 | 59–71 |
| R3 | ages halved (mass-weighted age for constant SFR) | 0.04–0.06 | ≤ 0.10 | 46–55 |
| R4 | R2 and R3 together (the most favourable declared case at this edge) | 0.11–0.16 | ≤ 0.25 | 18–22 |
| R5 | census-retention edge (f_ret 0.10, 54 r_M) | 0.79–0.92 | ≤ 0.23 | 21–27 |
| R6 | CFG95's own 0.40 r_ta edge | 1.15–1.30 | ≤ 0.34 | 14–20 |

- In every bracket all four cells stay N, ŝ/σ_s stays positive (+1.2 to +1.8), and the improvement over B1 is ≤ 1.14.
- With the larger edges (R5, R6) the density inside the edge is lower, so late types are 9–14% unsettled. The increment then reaches 2.9–4.5 Msun/pc² in the innermost bin, but it is largely absorbed by the free two-halo amplitude.

## Two caveats that change how the χ² values above should be read

**1. The free two-halo term on the difference absorbs the split for every model, including B1.**
- The task required CFG413's free two-halo treatment. With it, CFG95's colour-blind law also fits the split on K1 (p 0.35–0.49).
- **Why that is not a rescue:**
  - The fitted differential amplitude is 0.94–1.21 in CFG377's template units. That is as large as the whole isolated-lens stack's two-halo amplitude in CFG413 (1.1–1.6).
  - Fitted class by class (R8, released), B1 needs +0.86 / +0.62 for early types and **−0.19 / −0.34 for late types**. A negative two-halo term is unphysical.
  - Inside 0.3 Mpc (K1 is the 1-halo range by construction), the free R^−0.8 term acts as a free colour-dependent profile, not as a two-halo term.
- **So** p_S > 0.05 is easy to meet here; the Δχ² conditions carry the test. Without the two-halo term (R7) the split persists at CFG95's level (2.4–3.5σ).

**2. The 5.85 r_M truncated model fails the absolute lensing levels (R8).**
- Against the released per-class blocks with the two-halo term:
  - early types: S 30.5 / 38.1 (6 dof), against B1 2.5 / 2.9;
  - late types: S 47.8 / 52.7, against B1 13.9 / 14.3.
- Without the two-halo term, early types are 110 / 115 against 23 / 14.
- **Where it misses.** The truncated model is too low at large R (about 4× low in the outermost K1 bin, both classes) and, for late types, too high in the innermost bin.
- This is CFG398's supply-edge tension in another form. The split test above is on the early-minus-late difference only.

## Controls

- **C1:** CFG95's machinery, run read-only, reproduces its committed χ² exactly: 20.3037 / 18.5935 released and 26.6775 / 24.7862 re-measured.
- **C2:** this lane's vectorised stack reproduces CFG95's model D to 1e-14 and its χ² to 3e-14.
- **C3:** the ν_mono phantom at r_M/ln(1/(1 − f_b)) equals 5.364 M_b to 5e-9, so the edge is mass-conserving under the kernel used.
- **C4:** the log-M_b interpolation of the truncated profiles matches direct profiles to 2e-3.
- **C5:** the class two-halo templates are proportional to 2e-16, so one amplitude on D is exact.
- **C6:** all 181,477 lenses match the LePhare rows by exact position; u − r > 2 reproduces typ; log M* = MASS_MED + 0.15.
- **C7:** the proxy orders the classes, with median t_age 10.0 Gyr for early types against 3.4 Gyr for late types.
- **MUTATE (ages shuffled across all lenses):**
  - The increment changes sign, to −0.004 to −0.080 Msun/pc². With shuffled ages, massive early types get young ages, and their lower density makes them settle more slowly.
  - Δχ² vs B2 goes from +0.017–0.029 to −0.018–0.027, and ŝ/σ_s from +1.2–1.6 to −1.2–1.6.
  - H1 fails in both runs, so the MUTATE is uninformative for the headline (declared). The machinery check is C2.
- **Post-hoc (`cfg485_verify.py`):**
  - V1 recomputes the class-mean unsettled fractions in SI units, with its own matching, cosmic-age quadrature and calibration constants read from CFG95's JSON. It agrees to 1.3e-4.
  - V2/V3 recompute every χ² by Cholesky whitening, with the two-halo shape built from the bin edges alone. They agree to 2e-14.
  - A first V1 run had a Gyr unit slip in the verification script itself. It was fixed before the outputs were written; the main script was not touched.

## Caveats

- **Ages are absent on disk.**
  - The proxy is the LePhare sSFR formation time, min(M*/SFR, t_U(z)), from MASS_BEST and SFR_BEST. LePhare SED-fit SFRs are known to be noisy.
  - Late-type log sSFR runs from −10.3 to −8.5 (5–95%), with median −9.5, somewhat high for z ≈ 0.25 discs.
  - 21 lenses use the fallback (t_U).
  - A younger or noisier proxy only moves the late-type tail. Even the most favourable declared case at the 5.85 r_M edge (R4: slowest shell and halved ages) leaves the increment about 20 times too small (ŝ 18–22).
- **Conditional on CFG95's calibration** (frozen in Step 0) and on CFG61's grid stack.
- **The 5.85 r_M edge is the PAPER45 undepleted-halo edge (f_ret = 1).** The census edge (R5) is reported, not scored.

κ = ½ is fitted. The two footings are reported separately and never pooled. The cold fluid's mass is still required, with no particle species. Nothing here says the data favour either model, and no front is closed.
