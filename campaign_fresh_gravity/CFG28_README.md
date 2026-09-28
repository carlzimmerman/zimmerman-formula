# CFG28 — adversarial referee of the largest standing failure: the Milky Way's ultra-faint dwarfs

Script: `CFG28_ufd_referee.py`, under a second.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every dispersion is halved, and H1 fails (rc = 1).
- The main run exits 0.

κ = ½ is fitted. Both footings are used.

## Question

Under ownership (FG001), an accreted satellite obeys the isolated law of its infall baryons. The ultra-faints were quenched by reionisation and hold no gas, so the law predicts their velocity dispersions from their stars alone. FG001 found the measured dispersions sit +0.355 / +0.334 dex above that: **7.97 / 7.52σ**, candidate B's largest scored failure.

Is the offset real, or did our analysis make it, or are the dispersions inflated?

**Our analysis had two weak points:**
- FG001 dropped every ultra-faint whose dispersion is only an upper limit: 9 of the 40 with a measurement, probably the slowest.
- It quoted a statistical error only, with no systematic floor.

**The data have three known inflation routes:**
- unresolved binary stars;
- Milky Way tides;
- small, noisy samples.

## Results (LVD Milky Way table; FG001's estimator exec'd read-only)

**C1 (control):** FG001's median and gate value are reproduced exactly.

| test | canonical | alt |
|---|---|---|
| FG001 (limits dropped, statistical error) | +0.355 ± 0.044 (7.97σ) | +0.334 ± 0.044 (7.52σ) |
| **T1:** the 9 upper limits included (Kaplan–Meier, bootstrap) | +0.325 ± 0.038 | +0.304 ± 0.038 |
| **T5:** systematic floor (Υ_V 1 / 2 / 4, and the pure deep-MOND estimator) | 0.077 dex | 0.077 dex |
| **T1 + T5: the honest significance** | **3.8σ** | **3.5σ** |
| **T2:** beyond 80 kpc (weak tides) / inside | +0.325 ± 0.029 / +0.322 ± 0.102 | +0.304 / +0.302 |
| T2: Spearman ρ(offset, distance) | −0.22 (p = 0.23) | −0.22 |
| **T4:** best-measured systems (error ≤ 25%, N = 13) | **+0.432 ± 0.056** | +0.412 ± 0.056 |
| **T3:** constant floor s (binaries) vs factor f (missing mass) | s = 2.83 km/s; f = 2.26; Δln L (floor − factor) = **−1.66** | s = 2.79; f = 2.16; −1.51 |

- **H1 passed:** the failure is robust to our analysis, but its significance is 3.5–3.8σ, not 7.5–8.0σ.
- **H2 passed:** the offset survives the tide and precision tests.

## Standing

**The failure is real but was overstated.**
- **Censoring:** putting the dropped upper limits back barely moves the offset (−0.03 dex).
- **Significance:** an honest systematic floor halves it, to 3.5–3.8σ. The floor is conservative: Υ_V = 1 and 4 are extreme for old populations.
- **Tides:** they do not explain it. Far and near ultra-faints show the same offset.
- **Noise:** it does not explain it. The best-measured systems show a larger offset.

**Binaries are the remaining escape.** A constant floor, the signature of unresolved binaries, fits slightly worse than a mass factor, and it would need about 2.8 km/s added in quadrature to every system. The decisive test is multi-epoch, binary-corrected dispersions. It needs a per-system audit of the LVD's dispersion references (`ref_vlos`) for their binary treatment.

Nothing here says the theory is closed.
