# EST_GLS.md — the TRGB lever, GLS estimator lane

**Script:** `est_gls.py` (exit 0, model-based iterated GLS, both footings) · **Data:**
SPARC (Lelli-McGaugh-Schombert 2016), `sparc_master_clean.csv` + `*_rotmod.dat`, frozen
repo READ-ONLY · **Machinery:** reused `../a0_line/fire_common.py` (same cuts, same
estimator, `gls(..., biased=False)` — the guard that caught the fake 3.3e-11 deficit) ·
Comparison anchor: McGaugh+2016 g_dagger = 1.2e-10.

## What the lever does
The distance systematic `sysD` is the biggest single line in the gas a0 budget. TRGB/Cepheid
galaxies (`fD in {2,3}`) already carry a distance systematic 5× smaller than Hubble-flow
(`SIG_LND` 0.05 vs 0.25). Restricting to them **cuts the biggest budget line** and asks,
honestly both ways: does the tightened a0 STAY at the banked central or MOVE; does the error
shrink enough to DISCRIMINATE canonical (9.355e-11 = cH_Λ/Z) vs alt (1.1305e-10 = cH0/Z).

## Headline numbers (Ud = 0.7, the banked headline M/L)

| subsample | N pts / gals | a0_hat GLS | median | frac err | sysD frac | Occam canon | Occam alt |
|---|---|---|---|---|---|---|---|
| **full gas** | 310 / 49 | 1.181e-10 | 0.973e-10 | 16.1% | 6.5% | +0.60 ban | +1.04 ban |
| **TRGB gas** (fD 2,3) | 147 / 18 | **1.333e-10** | **1.273e-10** | **12.8%** | **2.8%** | **−0.49 ban** | **+0.80 ban** |

At the fiducial Ud = 0.5: full gas 1.363e-10 (16.0%), TRGB gas **1.490e-10** (12.4%),
Occam canon **−1.88 ban** / alt +0.10 ban. The central rises further at lower M/L.

## The four questions, answered

**(i) The lever WORKS mechanically.** Fractional `sysD` is cut by more than half
(6.5% → 2.8% at Ud=0.7; 6.0% → 2.7% at Ud=0.5); total fractional error 16.1% → 12.8%
(≈20% tighter). The biased-observed-weight control collapses to 6.3e-11 as expected,
confirming the model-based weights are doing the honest thing.

**(ii) The central MOVES — it does NOT stay.** The TRGB central rises to ~1.33e-10 (GLS) /
1.27e-10 (median) at Ud=0.7, ~13–15% ABOVE the banked full-gas central (1.18e-10 / 0.97e-10).
This is **robust across BOTH estimators** (GLS and median move together) and **not driven by
one galaxy**: the galaxy-level bootstrap gives 1.323e-10 [16–84%: 1.163, 1.470]e-10 over 18
galaxies, and the max leave-one-out leverage (NGC2915) shifts only 1.0e-11. It is **not a
y-segment artifact**: the TRGB y-window already spans the full-gas points (y-range-matched
full-gas is unchanged at 1.181e-10), and ybar is essentially identical (0.037 vs 0.041).

**(iii) It does NOT discriminate the footings — it TIGHTENS but stays NON-DIAGNOSTIC.**
Despite the tighter error, the TRGB 1σ band [1.16, 1.50]e-10 sits ABOVE *both* anchors:
canonical 9.36e-11 is 2.75σ low (Occam −0.49 ban, mildly disfavored) and alt 1.13e-10 is
1.28σ low (Occam +0.80 ban, mildly favored but the band still excludes it on the high side).
|Δbans| = 1.29 < the 2-ban discrimination threshold; footing likelihood-ratio +1.29 ban
toward alt. **This realizes the banked forecast concretely and CORRECTS it:** the forecast
assumed the central would STAY at 1.181e-10 (→ canonical −2.45 bans). The central instead
MOVED UP, so canonical lands at −0.49 ban (Ud=0.7) / −1.88 ban (Ud=0.5) at the *actual*
reduced error — disfavored, but not decisively, and the result now leans toward-but-above
alt rather than onto canonical.

**(iv) Λ inversion, tightened.** Λ = 3 Z² a0² / c⁴ (Z=5.789). TRGB gas gives
Λ = 2.03× Planck (GLS) / 1.85× (median) at Ud=0.7, +2.76σ — i.e. the tighter subsample sits
*further* from Planck (1.089e-52 m⁻²) than the banked 1.59×/1.08×, not closer. Across the
~52 a-priori orders the dwarf-rotation inversion still lands within a factor ~2 of the
cosmological Λ, but the high central pushes the tension to ~2.8σ.

## Honest caveats (both ways)
- **Deep-regime only.** Both subsamples are entirely y < ~0.2 (ybar ≈ 0.04, no points near
  y=1). The lever sharpens the a0 MAGNITUDE but **cannot discriminate the ν SHAPE**
  (framework vs McGaugh vs simple). Stated, not blurred.
- **The upward move has a distance-scale reading that cuts both ways.** For the a0-line,
  a0_measured ∝ 1/D per galaxy. TRGB dwarfs are the nearby population (D med 4.4 vs 12.5 Mpc).
  The rise could mean the Hubble-flow distances mildly SUPPRESSED the full-sample a0 (TRGB
  being the accurate anchor) — OR it could be a residual selection of the nearby low-mass
  dwarfs. N=18 galaxies cannot separate these. Not a claim either way.
- **M/L dependence.** The central and thus the bans depend on Ud (1.49e-10 at 0.5 →
  1.33e-10 at 0.7). This is the banked "estimator-/M/L-owned central, no clean footing lean"
  standing, inherited by the TRGB subsample.

## Verdict: TIGHTENS-BUT-NON-DIAGNOSTIC (both footings)
The TRGB lever fires — it robustly cuts the distance systematic and tightens the error ~20%.
But the tightened central MOVES UP to ~1.33e-10, landing ABOVE both footings, so the ~13%
band still cannot separate the 21%-apart anchors. Canonical is mildly disfavored (−0.5 to
−1.9 bans depending on M/L), alt mildly favored but not confirmed. No detection of either
footing is manufactured; the honest reading is a robust upward shift of uncertain origin
(framework a0 vs distance-scale) that **needs the full CCHP/EDD TRGB program or BIG-SPARC**
(more high-quality-distance dwarfs, and any that reach y~1) to become diagnostic. No "proof".
