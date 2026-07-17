# Ladder-free, frame-free H0 from galaxy dynamics (E4 → E8)

**Date:** 2026-07-17 · **Script:** `ladder_free_h0.py` (exit 0) · **Log:** `run.out`
**Data:** real SPARC only (frozen repo, READ-ONLY): 131 galaxies (Q≤2, 30°≤inc≤85°, g_bar>0).

## Why this number is different (Sarkar context)
Every distance-ladder H0 inherits peculiar-velocity / frame corrections that (per
Sarkar) exceed the signal, with no observed convergence to the CMB frame. This H0
comes from **rotation-curve shapes** through Carl's dS-Unruh modified-inertia chain:
no ladder rung, no frame correction. In the E4 pair estimator the distance **D**,
inclination **sin i**, and (in the gas variant) **Υ\*** cancel *identically* — verified
here: a deliberate 20% distance error shifts every pair estimate by <1e-12 relative.

## The chain
- **E4** (pair estimator): `a0 = (g1² − R12 g2²)/(R12 g2 − g1)`, `R12=(v1/v2)⁴(θ2/θ1)²`.
  DERIVED conditioning fact: singular for deep-deep pairs (den→0); well-conditioned
  **only for pairs straddling y = g_bar/a0 = 1**. Fully-Υ-free gas variant ill-conditioned
  in practice → usable estimator = straddling pairs at fiducial Υ (D, i still cancel;
  **Υ is the one remaining nuisance**).
- **E8** (cosmo weld), Z = √(32π/3) = 5.7888, **both footings carried**:
  - **A canonical:** `H0 = Z a0 / (c √Ω_Λ)`, Ω_Λ = 0.6847 (Planck).
  - **B Pythagorean:** `H0 = √((Z a0/c)² + ω_m·(100 km/s/Mpc)²)`, ω_m = Ω_m h² = 0.1430
    (Planck physical matter density — a CMB shape number, **not** a ladder rung).

## The ladder-free path, made explicit (and the circularity it avoids)
Canonical `a0 = 9.36e-11` is **itself Planck-anchored** (`a0 = cH_Λ/Z`). Feeding *that*
a0 into E8 just re-recovers **H0 = 67.4** (both footings) — input recovery, circular.
The **only** ladder-free number is `a0_MEASURED` (E4 pair value from SPARC shapes) → E8.

## Step 1 — a0_MEASURED from E4 (straddling y=1)
| Sample | usable pairs / galaxies | a0_MEASURED median (Υ=0.5) | pair-scatter 16–84 band | boot err on median |
|---|---|---|---|---|
| All distances | 9827 / 40 | **1.59e-10** | 8.1e-11 – 3.3e-10 | ±20% |
| TRGB/Cepheid (fD∈{2,3}) | 1814 / **7** | **1.16e-10** | 8.1e-11 – 2.5e-10 | ±20% |
| Any primary (fD∈{2,3,4,5}) | 1922 / 13 | 1.16e-10 | 8.0e-11 – 2.5e-10 | ±19% |

- **Straddle-window robustness:** scanning the assumed a0_ref (canonical / alt / McGaugh)
  moves the median only within the band (1.59 → 1.74 → 1.76e-10) — not pinned by the window.
- **Υ sensitivity (dominant systematic on the central value):** across Υ=0.3–1.0 the
  central a0_MEASURED stays in **~1.0–2.2e-10**, consistently **above canonical 9.36e-11**
  and near the alt/McGaugh footing. Canonical is only touched by the small TRGB/Ceph subset
  at Υ=0.3 (9.7e-11). **The straddling-pair a0 does not reproduce 9.36e-11 at fiducial Υ** —
  this is the known Υ=0.50-vs-0.70 RAR-footing artifact (banked non-diagnostic), not a new
  result about a0's true value.

## Step 2/3 — a0_MEASURED → H0, confronted with Planck 67.4 / SH0ES 73.0
| Sample | Footing | H0 (km/s/Mpc) | 68% bootstrap | **pair-scatter band** | verdict |
|---|---|---|---|---|---|
| All | A canonical | 114.3 | 94.8–140.7 | **58.6–241.0** | spans BOTH |
| All | B Pythagorean | 101.9 | 87.1–122.4 | **61.5–203.0** | spans BOTH |
| TRGB/Ceph | A canonical | 83.2 | 74.9–108.8 | **58.3–176.8** | spans BOTH |
| TRGB/Ceph | B Pythagorean | 78.5 | 72.6–97.6 | **61.3–151.1** | spans BOTH |

## Honest bottom line
- **A ladder-free, frame-free galaxy-dynamics H0 is computable** from E4→E8, and it is a
  genuinely different systematics basis than any distance ladder (D, i cancel exactly).
- **The central value lands HIGH** — ~80 (TRGB/Cepheid) to ~110 (all) km/s/Mpc — because the
  E4 straddling-pair a0 lands at ~1.2–1.6e-10, *above* canonical 9.36e-11. That high-a0
  offset is the Υ=0.5 RAR-footing artifact, not a robust measurement of a0's value.
- **The honest error bar is enormous.** The E4 conditioning (few well-conditioned straddling
  pairs; only 7 galaxies in the clean TRGB/Cepheid subset) plus the un-cancelled Υ nuisance
  produce a pair-scatter band of **~58–240 km/s/Mpc**. Every footing/sample **spans both
  Planck and SH0ES**.
- **This does NOT resolve or arbitrate the Hubble tension.** The galaxy-dynamics H0 is
  consistent with both camps (and with values well above either) within its large
  uncertainty. Its value is as an *independent, frame-free cross-check*, not a decider.
- The E8 canonical path is circular unless a0 is the *measured* pair value; the a0_Planck→67.4
  recovery is printed only to expose that circularity. No "proves" language; the wide error
  bar is the result, verified as hard as any win would be.
