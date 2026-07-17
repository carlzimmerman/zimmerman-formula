# VERIFY — Ladder-free, frame-free H0 (E4 → E8) — independent adversarial audit

**Date:** 2026-07-17 · **Auditor:** independent re-implementation (no reuse of target functions)
**Target:** `ladder_free_h0.py` (exit 0) · reproduces `run.out` **byte-identical**.

## Verdict: UPHELD, with one central-value caveat. The computation is honest.
A ladder-free, frame-free galaxy-dynamics H0 **is** computable via the genuinely
non-circular path (a0_MEASURED from E4 pair shapes → E8). D and inclination cancel
**exactly**. The central lands **high** and the honest error bar is **enormous** —
this is **NOT** a Hubble-tension resolution, and the script never claims one. A
manufactured resolution and a manufactured null were hunted equally; neither is present.

## What was re-checked, and the result

**(0) Reproduction.** Re-ran the committed script: exit 0, output byte-identical to
`run.out`. An independent from-scratch re-implementation reproduces every headline
number (a0 = 1.588e-10 ALL / 1.155e-10 TRGB·Ceph; H0 114.3/101.9 and 83.2/78.5).

**(1) E4 algebra — EXACT.** sympy confirms the estimator inverts the framework
relation g_obs² = g_bar² + g_bar·a0 identically:
`a0 = (g1² − R g2²)/(R g2 − g1)` with `R = (g_obs1/g_obs2)²`. The denominator at the
true a0 reduces to `g1(g1−g2)/(a0+g2)` — it vanishes at **g1=g2** (no lever), the
correct singular locus.

**(2) STRADDLING selection — genuinely well-conditioned, NOT false precision.**
The clean conditioning diagnostic is the sensitivity of R to a0:
`dlnR/dlna0 = a0(g2−g1)/[(g1+a0)(g2+a0)]`. Measured over real SPARC pairs by regime:

| regime | median a0 | per-pair MAD/med | median \|dlnR/dlna0\| |
|---|---|---|---|
| **straddle (kept)** | 1.59e-10 | 0.50 | **0.565** |
| deep-deep (excluded) | 6.9e-11 | 0.62 | 0.266 |
| high-high (excluded) | 3.3e-10 | 0.59 | 0.214 |

Straddling is the **best-conditioned** class (2× the a0-sensitivity of deep-deep,
where a0 provably drops out of R to leading order → singular). The selection is
principled and matches the derived conditioning fact. **However:** even the best class
has |dlnR/dlna0|≈0.57 (not ≫1) and a **50% per-pair scatter** — this is an intrinsically
noisy estimator, correctly reflected in the wide pair-scatter band, not hidden.

**(3) THE CIRCULARITY — correctly exposed; the ladder-free number is the measured one.**
Canonical a0 = c·H_Λ/Z is **Planck-anchored** (verified: c·H_Λ/Z with H_Λ=67.4·√Ω_L
reproduces 9.36e-11). Feeding it through E8 recovers **67.4 on both footings** — input
recovery, printed only to expose the circularity. The ladder-free H0 uses **only
a0_MEASURED** (rotation-curve shapes) → E8. Confirmed: the measured path is not secretly
Planck-anchored. Note honestly: E8 still uses Planck Ω_L (footing A) / ω_m (footing B) —
these are **CMB shape numbers, not distance-ladder rungs**; "ladder-free & frame-free"
is accurate, "cosmology-free" is not, and the script labels them as such.

**(4) DISTANCE-QUALITY split — honest; D cancels exactly.** The script's own numerical
D-test is *tautological* (r enters R only as a ratio, g_bar uses unscaled rm). Re-did it
the **physically correct** way — perturb the catalog distance and rescale the Newtonian
velocity components (M∝D², r∝D) **and** rm together: **+20% D → 0.00% shift in a0.**
D-cancellation is genuine. The TRGB/Cepheid subset (1.16e-10) differs from ALL (1.59e-10)
purely by **sample composition** (7 galaxies), not distance leverage — as claimed.

**(5) Error bar — NOT understated.** The ±20% is the bootstrap error on the *median*
(resampled over galaxies, correctly — pairs within a galaxy are correlated). The honest
*total* uncertainty is the pair-scatter band → **H0 ≈ 58–240 km/s/Mpc**, which the script
foregrounds and maps to every footing. Not understated.

**(6) NEW caveat — pooled central is weighting-sensitive (~28% high).**
The headline 1.588e-10 is the pooled median; **48% of pairs come from just 3 galaxies.**
A galaxy-democratic estimator (median of per-galaxy medians, 36 galaxies) gives
**1.235e-10** → H0 ≈ **89** (footing A, ALL), vs 114 pooled. The high all-distances H0=114
is partly a pair-concentration artifact; the galaxy-democratic and TRGB/Cepheid values
(1.16–1.24e-10, H0 ≈ 78–89) are the more robust central. Still above canonical, still
inside the huge band — a refinement, not a reversal.

## Both footings (verified, internally consistent)
- **A canonical:** H0 = Z a0/(c√Ω_Λ) — linear in a0, H0 = 67.4·(a0/9.36e-11).
- **B Pythagorean:** H0² = (Z a0/c)² + ω_m·(100)² — reduces to 67.4 at a0_canon (Ω_L+Ω_m
  partition checks out). Adds a matter floor → less sensitive to high a0.

## Manufactured-result hunt (both directions)
- **No manufactured Hubble-tension resolution.** Every footing/sample spans BOTH Planck
  67.4 and SH0ES 73.0 within the 58–240 band; the script explicitly declines to arbitrate.
- **No manufactured null.** The a0 detection at ~1.1–1.6e-10 (best-conditioned pairs) is
  real and is NOT suppressed to force canonical 9.36e-11. The high value is honestly
  attributed to the Υ=0.5 RAR-footing artifact (banked non-diagnostic), not a clean
  measurement of a0's true value.

## The honest ladder-free H0
**H0 ≈ 79–114 km/s/Mpc** (central, sample/footing/weighting-dependent: TRGB·Cepheid and
galaxy-democratic at the low end ~78–89, pooled-all-canonical at the high end 114), with
an honest systematic band of **~58–240 km/s/Mpc**. It is a genuinely different systematics
basis than any distance ladder (D, i cancel exactly) but its uncertainty is too large to
arbitrate Planck vs SH0ES. It sits above canonical because the straddling-pair a0 at Υ=0.5
lands high — a footing artifact, not a resolution. No "proves" language; win verified as
hard as a null.
