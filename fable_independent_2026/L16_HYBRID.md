# L16 — the inverse question: if cold dark matter exists, do galaxies still need a₀?

`L16_hybrid_inverse.py` + `L16_hybrid_inverse.out` (12 checks, 5 FAIL; the FAILs are the finding).

Every lane tonight assumed the framework's premise — no dark matter, the kernel does all the work — and that
premise is what makes clusters impossible (L2, L5, L6 closed every mechanism; L7 showed the required cluster
source **is** the cosmic dark-to-baryon ratio, 5.73 ± 0.68 against Ω_dm/Ω_b = 5.43, universal to 12%). This lane
inverts the premise and asks the question the programme had never asked:

> **Grant the cold component. Give every SPARC galaxy the halo ΛCDM actually predicts for it.
> Is the residual still organised by an acceleration?**

## The answer is NO, and it is decisive

**No acceleration scale survives.** Granting the abundance-matched halo, the residual
B(r) = g_obs/(g_bar + g_halo) is structureless: a curve in g_bar alone removes **−3.5%** of the variance a
constant leaves (74.0% with no halo — the RAR). The fit rails at the search floor; the bootstrap 95% upper limit
is **a_eff < 3.3×10⁻¹³ m/s²**, more than **3.4 dex below a₀** on either footing.

| | rms(log B) about 1 | about the best constant | about the best g_bar-only curve | variance acceleration removes | fitted a_eff |
|---|---|---|---|---|---|
| no halo (control) | 0.517 | 0.285 | 0.145 | **74.0%** | 1.08e-10 (= a₀) |
| abundance-matched halo | 0.171 | 0.165 | 0.168 | **−3.5%** | none (< 3.3e-13) |
| cosmic-ratio halo (lower bound) | 0.245 | 0.176 | 0.151 | 26.6% | 5.4e-12 (−1.24 dex) |

The same thing happens *inside* individual galaxies, so population scatter is not hiding it: the median
per-galaxy slope d log B / d log g_bar goes from **−0.324** with no halo (deep-MOND expects −0.5) to
**+0.020** with the halo — 6% of it retained.

## The controls, and why the null is a bound rather than a failure

- **Pipeline (H0, PASS ×2).** With no halo the machinery recovers the radial acceleration relation: fitted scale
  1.134e-10 m/s², **0.002 dex from the alt footing** (0.083 from canonical), scatter 0.142 dex against the
  published 0.11–0.13.
- **Injection–recovery (A2, PASS ×2).** A known boost is injected into the residual on top of the halo and the
  estimator recovers it: an injected a₀ comes back to **0.100 dex**. Scanning the injected scale gives the
  **detection floor, a₀ × 10^−0.50 = 2.96e-11 m/s²** — anything above that would have been seen. The null is a
  bound, not a lack of sensitivity.
- **Robustness (R4, PASS).** The verdict is **identical in all eleven halo rows**: log M₂₀₀ ± 0.6 dex (2× the
  abundance-matching uncertainty), log c ± 0.22 dex (2× Dutton & Macciò's scatter), the cosmic-ratio halo,
  dropping the massive end where Moster's relation is steepest, and the Lelli quality cuts. Both no-halo controls
  go the other way, so the scan is alive. The conclusion does not flip inside the halo uncertainty.
- **Margin (R4b, PASS).** a₀ returns only at **log M₂₀₀ − 1.80 dex** — a halo **63× smaller** than ΛCDM's, six
  times the 0.30 dex abundance-matching uncertainty below it.

## What the framework keeps, stated as carefully as the data allow

Three FAILs are the price ΛCDM pays here, and they are where an acceleration scale keeps content even though it
is no longer *required*:

- **H1 FAIL.** Baryons + the abundance-matched NFW halo with no boost do not reproduce the inner rotation curves
  to the RAR's own tightness: inner rms **0.167 dex, 1.5×**; 48% of galaxies are off by more than 0.1 dex, with a
  per-galaxy spread of 0.168 dex and a range −0.62 to +0.32 dex. That spread at a fixed prescription is the
  diversity problem (Oman+ 2015).
- **A1 PASS.** With **zero free parameters on each side**, the framework's kernel at fixed a₀ is the tighter
  description: **0.142 dex** (alt footing; 0.145 canonical) against the halo's **0.171 dex**, a factor 1.20.
- **A4 FAIL.** The halo above used *mean* relations. Switch on the scatter ΛCDM actually has (0.25 dex in M₂₀₀
  at fixed M\*, 0.11 dex in log c) and the halo's rms rises to **0.198 ± 0.008 dex**, 1.39× the fixed-a₀ kernel,
  with a galaxy-to-galaxy offset spread of 0.190 dex. This is the known halo-population-scatter problem
  (Desmond 2017; and this repository's own `rar_origin_detector_2026.py` V2, which finds the ΛCDM population
  predicts 0.449 dex of per-galaxy a₀ scatter against 0.275 observed).

So the honest summary is: **a₀ is not required by the galaxy data once a ΛCDM halo is granted, but it remains the
tighter and more economical description of them.** "Not required" and "not preferred" are different claims and
only the first is established here.

## Method

- **Data.** SPARC `*_rotmod.dat`, loaded exactly as `L6_screened_force.py` does — Υ_disk = 0.5, Υ_bulge = 0.7,
  r > 0, V_obs > 0, V_bar² > 0, eV/V_obs < 0.10, ≥ 3 surviving points: **155 galaxies, 2786 points**. The Lelli+
  2016/2017 cuts (Q ≤ 2, i ≥ 30°, 141 galaxies) are carried as a robustness row. Baryonic masses from
  `SPARC_Lelli2016c.mrt` (M\* = 0.5·L[3.6], M_gas = 1.33·M_HI), spanning log M_b = 7.69–11.43.
- **Halo, primary.** Moster, Naab & White 2013 (z = 0) stellar-to-halo mass, inverted for M₂₀₀ — *what ΛCDM
  actually predicts for a galaxy of this stellar mass*. Concentration from **Dutton & Macciò 2014** eq. 7 at
  z = 0, log₁₀ c₂₀₀ = 0.905 − 0.101 log₁₀(M₂₀₀h/10¹²), the same relation already used in this repository
  (`hunt_2026/h88_crispy_gap_concentrations.py`, which carries its full redshift form;
  `hunt_2026/h117_rar_intrinsic_scatter.py`; `hunt_2026/h48_h69_binary_galaxies.py`, which pairs it with the
  same Moster inversion; `prep_2026/rar_origin_2026/rar_origin_detector_2026.py`). NFW, with the baryons
  subtracted from M₂₀₀ so nothing is counted twice.
- **Halo, second prescription.** The cosmic ratio applied to the galaxy's own baryons, M₂₀₀ = (Ω_m/Ω_b)M_b — the
  L7 cluster reading transplanted to a galaxy. It is a **lower bound**, not the ΛCDM prediction: it sits 0.77 dex
  (6×) below abundance matching, and that gap is the missing-baryon problem. Median M₂₀₀/M_b is 38 for abundance
  matching against 6.43 for the cosmic ratio.
- **a₀ does not enter the measurement.** The surviving scale a_eff is fitted freely over 10⁻¹³·⁵–10⁻⁸ m/s²; a₀
  (9.3619e-11 canonical, 1.1279e-10 alt) enters only the comparisons, and both footings are carried in every one.
- **Statistics.** Variance explained by acceleration alone is a binned-median curve in log g_bar, **cross-validated
  by galaxy** so correlated per-galaxy errors cannot inflate it; a_eff is fitted with a free normalisation offset
  that absorbs a wrong halo *amplitude*, and bootstrapped over galaxies.

## Cross-lane consistency

The abundance-matched halo puts **0.97 M_b [0.59, 3.33]** inside 10 kpc — the same currency and the same range as
L1's cold-infall calculation (0.92–1.45 M_b), against the 0.25 M_b the RAR was said to tolerate. L16 is the
resolution of that tension: the mass is not too much, because the observed curves accommodate it. What the RAR
"tolerates" was computed *on top of* the kernel; once the kernel is not also acting, the halo is what the data
show.

## What this does not show

It does not measure dark matter. It does not by itself rescue clusters. The halo is the plain equilibrium NFW
population with no adiabatic contraction and no feedback, both of which move inner profiles — the leading
systematic on H1 and on the −0.044 dex normalisation offset. And it does not touch the programme's distinctive
prediction a₀ = κ c √(Gρ_Λ), which is a claim about the **value** of an acceleration scale and is tested by the
pre-registered measurements (Gaia DR4's two arms, the deep-MOND Tully–Fisher zero point at z ≈ 2.5), not by this
rotation-curve inversion.

## Consequence for the programme

The hybrid rescue that this lane went looking for **is not there**. Combined with L7 — clusters demand exactly
the cosmic dark-to-baryon share — the standing is now one-sided in a way it was not this morning: dark matter
accounts for clusters (L7) *and* is sufficient for galaxies (L16), while the kernel accounts for galaxies and
cannot account for clusters (L2, L5, L6). The framework's remaining distinctive content is not the galaxy
rotation curves, which are now shown to be reproducible without it. It is (i) the **tightness** of the relation,
which a halo population does not naturally deliver (A1, A4), and (ii) the **value** of the acceleration scale and
its tie to ρ_Λ, tested by the pre-registered measurements. Those two, not the rotation curves, are what the
programme should now be defended on.

## PASS/FAIL, verbatim

```
  [PASS] H0a [control] with no halo the fitted acceleration scale lands within 0.15 dex of a_0 on at least one footing   (closest footing is 0.002 dex away)
  [PASS] H0b [control] with no halo the residual scatter about the fitted acceleration relation is the RAR's known ~0.11 dex   (rms = 0.142 dex (published RAR scatter 0.11-0.13 dex))
  [FAIL] H1 [control] baryons + the abundance-matched NFW halo with NO boost reproduce the inner rotation curves to the RAR's own 0.11 dex   (inner rms 0.167 dex, 1.5x the relation the framework's kernel achieves; median offset -0.026 dex)
  [FAIL] T2 [THE TEST] after granting a LambdaCDM cold halo the residual boost is STILL organised by acceleration (a g_bar-only curve removes >= 50% of the variance a constant leaves, AND the fitted scale is not vanishing)   (variance removed -3.5% (< 50%); bootstrap 16th percentile of log10 a_eff = -13.500 vs the vanishing threshold log10(a_0/10) = -11.029 (below))
  [FAIL] T3 [scale] the acceleration scale surviving the abundance-matched halo agrees with a_0 to within 0.15 dex on at least one footing   (closest footing is 3.471 dex away (a factor 2960.49))
  [PASS] A1 [head-to-head] the framework's kernel with a_0 FIXED describes these rotation curves more tightly than the granted LambdaCDM halo does   (kernel 0.142 dex (best footing: alt) vs halo 0.171 dex, a factor 1.20 in scatter with the same number of free parameters (none))
  [PASS] A2a [injection] the estimator recovers an injected acceleration scale equal to a_0 to within 0.15 dex, so a surviving a_0 would have been found if it were there   (injected log -10.029, recovered -10.129 [-10.213, -10.054], variance removed 64.9%)
  [PASS] A2b [injection] the DETECTION FLOOR is at least 3x below a_0, so T2's null is a real bound on a surviving acceleration scale rather than a lack of sensitivity   (the smallest injected scale recovered is a_0 x 10^-0.50 = 2.96e-11 m/s^2)
  [FAIL] A3 [within-galaxy] the acceleration structure survives the halo INSIDE individual galaxies (the median per-galaxy slope keeps at least half its no-halo value)   (median slope -0.324 with no halo -> +0.020 with the abundance-matched halo, i.e. 6% of it retained)
  [FAIL] A4 [scatter] the LambdaCDM halo population still matches the rotation curves once its own scatter in M_200 and concentration is switched on, i.e. within the RAR's observed 0.13 dex   (0.198 dex, 1.39x the fixed-a_0 kernel; this is the known halo-population-scatter problem (Desmond 2017; this repository's rar_origin_detector_2026.py V2) and it is where an acceleration scale keeps content even though it is not REQUIRED)
  [PASS] R4 [robust] the T2 verdict is the SAME in every halo row above (log M_200 +- 0.6 dex = 2x the abundance-matching uncertainty, log c +- 0.22 dex = 2x Dutton-Maccio's scatter, the cosmic-ratio halo, the Lelli cuts), so the conclusion does not flip inside the halo uncertainty and the test IS decisive with current data   (all 11 halo rows agree with the primary (no scale survives); the two no-halo controls both go the other way, so the scan is alive)
  [PASS] R4b [margin] a_0 returns only if the halo is pushed more than 3x the abundance-matching uncertainty (0.90 dex) BELOW what LambdaCDM predicts, so the null has margin   (a_0 comes back only at log M_200 -1.80 dex, i.e. a halo 63x smaller than LambdaCDM's and 6.0 sigma below it)
```

## Verdict

Granting every SPARC galaxy the cold halo ΛCDM predicts for its stellar mass, the residual boost is
**not organised by acceleration at all** — 74% of the variance is acceleration-organised without a halo and
−3.5% with one, the surviving scale is bounded at a_eff < 3.3×10⁻¹³ m/s² (3.4 dex below a₀), and the same
collapse happens inside individual galaxies (slope −0.324 → +0.020), while an injected a₀ would have been
recovered to 0.100 dex. The conclusion holds identically across every halo assumption in a range twice the real
abundance-matching and concentration uncertainties, and a₀ returns only for a halo 63× below the ΛCDM value.
The hybrid rescue is therefore not available: a₀ is **not required** by the galaxy data once dark matter is
granted — though the fixed-a₀ kernel remains the tighter description (0.142 dex against the halo's 0.171, rising
to 0.198 once the halo population's own scatter is switched on), which is where the programme's galaxy claim now
has to live.
