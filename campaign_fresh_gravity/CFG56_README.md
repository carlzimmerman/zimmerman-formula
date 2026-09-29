# CFG56 — CFG40 redone with the bulge: the marginal fail survives

Script: `CFG56_super_spirals_bulge.py` (about 5 s). Data: `real_research/data/simard2011_ogle_bulge_disc.tsv` (Simard+2011 table 1, the bulge + exponential-disc fits Ogle used; a TAP cone search for the 23 galaxies, fetched with the owner's approval; every galaxy matched one row, and the row's redshift, R_d and inclination reproduce Ogle's). Outputs: `.out`, `_results.json`, and the MUTATE pair. The main run exits 1: **H2 failed as declared**.

## Why

CFG40's independent referee found that its marginal fail depended on the baryon structure model: the declared exponential disc gave the nine fastest +0.170, a point mass +0.113. CFG40 put all the baryons in a disc; massive spirals have bulges. Simard's bulge-to-total ratios (r band, 0.04–0.46, median 0.26) test whether the bulge removes the fail.

## Frozen method

CFG40's hypotheses, thresholds and error model exactly, with one change (declared before the first run): the stars split into a Hernquist bulge (fraction B/T_r, scale R_e,bulge/1.8153) and an exponential disc (R_d from Simard), the gas in the disc. The floor's model term is B/T ± 0.10 (B/T is a light fraction; a redder bulge carries more of the W1 mass), plus CFG40's stellar-mass and gas terms.

## Results

| statistic (canonical) | CFG40 (all-disc) | **CFG56 (bulge + disc)** |
|---|---|---|
| mean offset | +0.107 ± 0.075 (1.42σ) | **+0.105 ± 0.063 (1.67σ)** |
| slope against log M_b | +0.194 ± 0.100 (1.95σ) | **+0.166 ± 0.092 (1.80σ)** |
| the nine fastest | +0.170 (2.06σ) | **+0.164 (2.34σ)** |

Alt footing: +0.090, +0.165 (slope), +0.149 (nine fastest, 2.17σ). **H1 passed** (the bare law within 2σ); **H2 failed** on the nine-fastest clause. The controls pass: every Simard row reproduces Ogle's R_d and inclination, and with B/T = 0 the model reproduces CFG40's mean to 1e-6.

## Standing

**The bulge does not remove the marginal fail.** The offsets barely move (mean −0.002, nine fastest −0.006), because the measured bulge fractions are modest and the bulge scale is small. The model floor shrinks from 0.041 to 0.001 dex, so the nine-fastest significance rises from 2.06σ to **2.34σ**. **CFG40's referee point ("a point mass passes") is refuted by the measured structure:** a point mass is not a fair model of a disc-dominated spiral with B/T ≈ 0.26.

What limits the result is now the stellar-mass systematic (0.059 of the 0.063 floor), the missing HI, and the inclination and maximum-of-a-noisy-curve caveats CFG40 listed. On galaxy scatter alone the mean offset would be 5σ. **B fails its declared test on the most massive star-forming disks at 2.3σ (the nine fastest), 1.8σ (the mass trend) and 1.7σ (the mean).** That is still marginal, and the cold-mass rule still cannot cure it (f_ex = 0 in all 23).

Nothing here says the theory is closed.
