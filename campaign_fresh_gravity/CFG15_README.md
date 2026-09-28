# CFG15 — does CFG12's canonical window survive a physical 2-halo amplitude?

Script: `CFG15_kids_bias.py`, about 5 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. There is no 2-halo term in H1, the floor returns to 0.47, and H1 fails (rc = 1).
- The main run exits 1, because H2 failed.

## The question

CFG12 opened the strict window on the canonical footing, pairing:
- the KiDS floor of 0.303–0.309, obtained with the 2-halo amplitude A fitted in [0, 2] per lens bin;
- a budget edge of 0.338–0.341.

The 2-halo template (FP1 E / L355) is the projected **matter** correlation, so A is the lens bias. Near that floor, the fit uses A = 1.7–1.9 in the two massive bins.

## The framework's own lens bias

The bias comes from the peak-background split at each KiDS bin's turnaround mass, at z_l = 0.25:
- the masses are CFG4's convention, the law's enclosed mass at r_ta;
- σ comes from CLASS, via CFG7_common;
- the thresholds are collapse 1.686 and turnaround 1.208.

| bin, log M_b | M_ta (canonical) | b (collapse / turnaround) |
|---|---|---|
| 10.4 | 4.9e12 | 1.11 / 0.68 |
| 10.9 | 1.2e13 | 1.35 / 0.85 |
| 11.05 | 1.5e13 | 1.44 / 0.91 |
| 11.25 | 2.1e13 | 1.57 / 1.01 |

The alt masses are about 1.15× larger. The cap per bin is the larger of the two values.

## Results

**Controls**

| check | result |
|---|---|
| C1: CFG4_switch's committed x-scan (A = 0 and A ≤ 2, all four rows) | reproduced exactly |
| C2: the per-bin-cap kfit equals FP1's kfit for scalar caps | exact |

**The KiDS floor against the cap** (canonical P2; ν_mono is similar and slightly higher):

| cap | 0 | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 | 2.0 | the framework's own bias |
|---|---|---|---|---|---|---|---|---|
| floor | 0.473 | 0.397 | 0.371 | **0.350** | 0.333 | 0.315 | 0.308 | **0.317** |

**The hypotheses**

| hypothesis | result |
|---|---|
| **H1:** at the framework's own bias the canonical floor ≤ CFG12's edge | **pass**: P2 0.317 vs 0.341; ν_mono 0.322 vs 0.338 |
| **H2:** with unbiased lenses (A ≤ 1), the same | **FAILED**: P2 0.350 vs 0.341; ν_mono 0.360 vs 0.338 |

On the alt footing the floor at the framework's own bias is 0.317–0.318, against an edge of 0.291–0.293, so it stays closed.

## Standing

**CFG12's "canonical conflict resolved" is downgraded to marginal and bias-dependent.**
- The canonical window, x_e ∈ [0.317, 0.341] (P2), is open if the isolated KiDS lenses carry a bias ≳ 1.1 (P2) or ≳ 1.3 (ν_mono).
- It closes by 0.01–0.02 in x for unbiased lenses.

**The bias estimate is uncertain.**
- The framework's peak-background bias (1.1–1.6) is computed at the law's *untruncated* turnaround masses. The actual masses, with the phantom cut at x_e, are smaller.
- KiDS's isolation criterion selects low-density environments.

Both effects lower the true bias, so the window's survival is not established.

Nothing here says the theory is closed.

**Completed by CFG16.** Taken self-consistently from the truncated profile's turnaround mass, the bias drops to 0.9–1.2, and the canonical window closes: P2 +0.0003, ν_mono +0.010.
