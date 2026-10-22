# D1_skew_preflight: the n = 1 vs n = 2 occupancy-noise skew test

## Verdict: SCOPED NO-GO (on any rotation-curve data, not only on what is on disk)

The skew sign cannot decide n = 1 vs n = 2 on RAR residuals. There are two obstructions, and either
one alone is enough.

1. **In log g the two laws have the same sign.** The record's skew formula (A63 eq. 17) is the skew of
   δg in linear g. Taking the log adds a term −3σ_rel. Both terms scale as N_s^{-1/2}, so the
   log-space sign does not depend on N_s either. Across the whole window g/a₀ ∈ (0.375, 1), **both laws
   predict a negative skew in log g** (√N_s·skew at g = a₀/2: n = 1 −4.38, n = 2 −2.44; neither law
   changes sign in log g on 0.3–1.5 a₀). Exact binomial sums at N_s = 93 confirm the signs (K5).
   In log g the test becomes a magnitude test, and magnitudes carry systematics.
2. **In linear g the background skew is far larger than the signal.** The signs do differ in linear g.
   But RAR errors (distance, Υ, inclination) are symmetric in *log* g, not in g. A log-symmetric
   background of 0.06 dex has a linear skew of +0.42 (K7, analytic and Monte Carlo). On SPARC the
   measured linear skew outside the window is 2.9 (canonical) and 3.2 (alt). The best-case predicted
   linear signal is +0.062 (n = 1) and −0.165 (n = 2), so the background is 17–50× larger.

The record says "an odd moment is blind to any symmetric error"
(`deepseek_push/DS_FINAL_2026_10_21/A63_saturating_medium/report.md:373-374`). That holds only for
errors symmetric in the variable you use. Here the errors are symmetric in log g, and in log g the
signal has no sign difference.

## Numbers (all in `d1_skew_preflight_results.json`)

**Point (a): the dilution error is real.** K30 combines the N_s = 1 skew (0.7071) with A2's
normalisation, and that normalisation means N_s = 93.1 (K3). The true occupancy skew at a₀/2 is then
+0.0733 (n = 1). For n = 2 it is −0.0361 at the same N_s, or −0.101 at n = 2's own N_s = 11.8 for 0.03 dex.
Correcting only s_true at φ = 0.447 multiplies N(3σ) by 93 (n = 1: 1.26e6) and by 384 (n = 2 at
N_s = 93: 5.2e6). K30 also takes φ at g = a₀ but s at g = a₀/2. Evaluated consistently at a₀/2
(σ_occ = 0.076 dex, φ = 0.786), the linear-g price is N(3σ) = 4.3e4 (n = 1) and 1.6e4 to 4.2e6 (n = 2).
That is 3× to 300× the record's "7,000–13,500", and it counts only Gaussian statistics.

**Best case allowed by SPARC.** This case puts all of the intrinsic window scatter into occupancy noise:
σ_tot = 0.167 dex, measurement 0.093 dex, intrinsic 0.139 dex, φ_max = 0.83, so N_s ≈ 19 (n = 1) or
≈ 5 (n = 2). The predicted signals are:

| footing | n=1 lin | n=2 lin | n=1 log | n=2 log | N(3σ) to separate, lin / log (Gaussian) | × design effect |
|---|---|---|---|---|---|---|
| canonical 9.36e-11 | +0.062 | −0.165 | −0.490 | −0.715 | 1.05e3 / 1.06e3 | 3.3e5 / 1.2e5 |
| alt 1.13e-10 | +0.063 | −0.170 | −0.496 | −0.729 | 9.9e2 / 1.0e3 | 3.6e5 / 1.6e5 |

**Systematic-skew floor measured on SPARC.** Sample: Q ≤ 2, Υ 0.5/0.7, residuals demeaned in 0.1 dex
g_bar bins, so no law is assumed.

| footing | var | out-of-window skew (floor) | per-bin range out | galaxy-demeaned out | SE_boot (window) | design effect | N_window / galaxies / N_eff |
|---|---|---|---|---|---|---|---|
| canonical | log | −1.20 | −4.1 … +1.2 | −1.68 | 0.84 | 111 | 958 / 118 / 9 |
| canonical | lin | +2.86 | −1.1 … +3.2 | +4.38 | 1.40 | 315 | 958 / 118 / 3 |
| alt | log | −1.12 | −3.4 … +0.7 | −1.63 | 1.04 | 163 | 906 / 106 / 6 |
| alt | lin | +3.18 | −1.2 … +3.5 | +5.20 | 1.55 | 361 | 906 / 106 / 3 |

Removing each galaxy's mean does not remove the skew, so the tails come from points within galaxies,
not from galaxy offsets. The bootstrap SE of the window skew is 10–20× the Gaussian √(6/N). This
reflects heavy tails as well as correlation between points; N_eff folds in both.

**Reported-only diagnostic (NOT a test of n):** the SPARC window skew is −1.25 (log) and +3.16 (lin)
on the canonical footing, and −1.39 / +3.68 on the alt footing. These are the same size and sign as
outside the window.

**Data on disk.** Only SPARC and LITTLE THINGS have per-point baryons.
- **SPARC:** 958 (canonical) and 906 (alt) window points, from 118 / 106 galaxies; median error
  0.034 / 0.032 dex (rms 0.093 / 0.087, because the tail has large errors).
- **LITTLE THINGS (Oh+2015):** g_bar = V_tot² − V_DM² with the authors' M/L. 542 matched points, but
  only 40 / 33 in the window, from 3 galaxies, with median error 0.18 dex.
- **WALLABY DR2:** 303 models and 2116 ring points. There are no resolved stellar profiles, and the
  30″ rings are strongly correlated.
- **Di Teodoro 2023:** 216 points in 15 galaxies, with no per-point baryons; these are massive and
  mostly g_N ≳ a₀.
- **Not point-level:** McQuinn 2022 has one point per galaxy. MIGHTEE-HI has a catalogue and cubes,
  with integrated widths and no curves. The KiDS RAR is a lensing stack, which averages the per-galaxy
  noise away.

## Errors found in the record

- `deepseek_push/DS_FINAL_2026_10_21/A63_saturating_medium/a63_checks.py:644,647` (K30) and
  `report.md:331-333` use s_true = 0.7071, the N_s = 1 value, with the N_s = 93 normalisation. The
  relative error in s_true is 8.6. The φ (at g = a₀) and the s (at g = a₀/2) are also taken at different g.
- `report.md:293-294`, `A2_medium/report.md:183` ("N_s-free"), and `report.md:362-374` ("no
  normalisation budget", "blind to any symmetric error") are true only for linear g. In log g both laws
  are negative throughout the window.
- `report.md:438` (K18 row) prints −0.348327. The computed value is −0.3483107; this is a typo.

## What this does not show

- It does not test n. No data result here favours either law, and neither is ruled out.
- It does not rule out higher-moment tests on non-RAR data, for example a lab medium (A63 §6.3) or a
  skew estimator that models the log-normal background explicitly. Such an estimator would need a
  forward model of the distance, Υ and inclination skew good to ≲ 0.05. That is ~8× tighter than the
  +0.42 a 0.06 dex log-symmetric background already produces, and ~50× below SPARC's measured 2.9–3.2.
- N_s is not predicted. The "best case" is an upper bound on the signal, not a forecast.

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 d1_skew_preflight.py` gives 10/10 PASS. The `--mutate` run
gives 9/10, with K4 failing as required.
