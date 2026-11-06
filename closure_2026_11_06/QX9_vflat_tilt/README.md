# QX9: QX8's Vflat slope is not PAPER67's tilt; it is carried by galaxies at the Upsilon grid edges. NO VERDICT as frozen (control missed its line)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (0bd9b6c4b7), frozen before any
QX9 number. Script: qx9.py (about 9 s, 1 thread; QX8's loader, fitter and parts imported read-only). Both footings,
never pooled.

## The two numbers are different quantities

- PAPER67's "no tilt with speed" (+0.02 canonical / -0.02 alt, FG1 row Tl, line |t| <= 0.15) is the tilt of the
  FITTED MASS-TO-LIGHT RATIO: median refit Upsilon for Vflat < 100 minus that for Vflat > 150 (Q <= 2, Inc >= 30).
- QX8's "+0.21 to +0.26 per dex" is the partial coefficient of log Vflat (at fixed log SBeff) in a regression of
  each galaxy's weighted mean residual at its refit Upsilon, over all 135 galaxies with Vflat and SBeff, with no
  quality cut.
- So QX8's number does not contradict PAPER67's statement (Q1: NO). KA1: QX9 reproduces QX8's four slopes
  exactly (|diff| = 0).

## What drives the slope (b_V +- bootstrap sigma; canonical law shown, the rest in qx9.out)

| check | canonical law | canonical exact | alt law | alt exact |
|---|---|---|---|---|
| S0 joint, all (QX8's number) | +0.230 +- 0.088 (2.6 sigma) | +0.213 (2.5) | +0.259 (2.8) | +0.240 (2.7) |
| S1 simple, no SBeff | +0.159 (3.0) | +0.125 (2.6) | +0.192 (3.7) | +0.161 (3.2) |
| S2 FG1 quality cut | +0.038 (0.8) | +0.034 (0.7) | +0.063 (1.3) | +0.057 (1.2) |
| S3 fixed Upsilon 0.50 | +0.401 (3.4) | +0.411 (3.5) | +0.406 (3.5) | +0.417 (3.7) |
| S4 bulge-free | +0.285 (2.7) | +0.266 (2.7) | +0.316 (3.1) | +0.296 (2.9) |
| S5 gas-dominated (n 23) | +0.589 (2.9) | +0.575 (2.7) | +0.617 (3.1) | +0.598 (3.0) |
| S6 refit Upsilon off the grid edges (n 97-98) | -0.008 +- 0.017 (0.5) | -0.008 (0.7) | -0.021 (1.9) | -0.004 (0.3) |
| S2 + S6 | -0.005 (0.3) | -0.005 (0.5) | -0.018 (1.6) | +0.001 (0.0) |
| S7 law-mock null, median [95 %] | +0.011 [-0.001, +0.028] | +0.011 [-0.001, +0.025] (ex mocks) | +0.010 [+0.000, +0.025] | +0.011 [-0.001, +0.026] (ex mocks) |

- 62-66 of 175 galaxies have their refit Upsilon pinned at a grid edge (0.30 or 1.20; canonical law: 40 at 0.30,
  22 at 1.20). Their residual cannot be absorbed, so it leaks into the mean residual. Drop them (S6) and the
  slope is zero on every footing and both fields, with bootstrap errors 3-8 times smaller.
- At fixed Upsilon (S3) the slope is larger, +0.40 per dex. That is the ordinary Upsilon-Vflat degeneracy: the
  mass-to-light ratio the data want changes with speed, and a fixed value turns that into residuals.
- The pipeline itself makes no slope: law-drawn mocks give +0.01, with a 95 % band about 0.03 wide.
- Frozen reading: ARTEFACT on both footings, for the law and the exact field (the real slope is outside the mock
  band, but it loses significance under S3-or-S2+S6, which the frozen line counts as artefact).

## Label as frozen: NO VERDICT (the control missed its line)

MUTATE (planted 0.20 log10(Vflat/100) on mock g_obs before the refit) recovers only +0.100 (canonical) / +0.094
(alt) of the planted 0.20: the refit Upsilon absorbs about half of a multiplicative tilt. The frozen line was
0.20 +- 0.07, so the control does not bite as frozen (qx9_MUTATE.out, exit 1), and the frozen rule says no
verdict stands. Reading the shift against the null (0.10 vs a band about 0.03 wide), the pipeline does see a
planted tilt, at half strength. That reading is post-result and is not the label. The line was mis-set: it
assumed the refit would not absorb a multiplicative tilt.

What survives without the label: the slope is a different quantity from PAPER67's tilt, and it vanishes off the
grid edges. No erratum draft is written: Q1 is NO and the label is not REAL.

## Note for the owner (reported, not graded): the exact field moves PAPER67's own tilt

Q1 also recomputed FG1's Upsilon tilt on QX8's fits. On the law it reproduces PAPER67 (+0.020 / -0.020). On the
action's exact field it is **+0.170 canonical (above FG1's 0.15 line) and +0.090 alt**. The exact field lowers
predicted accelerations most in low-surface-brightness, slow discs, so their refit Upsilon rises (QX8). If the
flagship is regraded on the exact field (QX8), FG1's tilt row fails on the canonical footing. That needs its own
frozen lane before it changes any label.

## Checks

- KA1: QX8's four slopes reproduced exactly.
- Rerun: qx9.json byte-identical.
- MUTATE: does not bite as frozen (above).
