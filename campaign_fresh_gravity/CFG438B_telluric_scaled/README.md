# CFG438B: BX442 with Law+12's sky scaling and telluric. The graded run is VOID; the lane is CLOSED

**Bottom line.**
- **The graded run (S+T) is VOID.** The 2 s A0V standards fall short of the frozen validity gate: they reach per-channel S/N 12–31, against a required 50. The nod-pair scatter confirms this is real photon noise.
- **Telluric correction changes nothing,** as predicted: 27 → 27 spaxels.
- **Law's per-channel sky scaling (S-only)** recovers Law's kinematic PA, 166° (162–170) against 168°, and makes the two nights agree. But it passes fewer spaxels (19), and V1 still fails.
- **The split-half tests show the per-spaxel errors are understated:** flux by about 1.3×, velocity by 1.6–2.4×. So the frozen S/N ≥ 5 cut is really about S/N 3.8.
- **Even 52 frames would not reach 30 spaxels:** the forecast with corrected errors is 11 (CFG438 cubes) or 5 (S cubes).

Lane closed under the frozen stopping rule. CFG438's NOT VALIDATED stands. No a0 claim.

## What was run (FROZEN_CRITERIA.md, commit 83780fe078; build script 45cd36a51b)
- **Super-dark.** The DRP's Combine Frames (MEDIAN) over the five 900 s darks of 2011-08-23.
- **Science frames.** All 40 science frames were reduced with the super-dark subtracted, then the same chain as CFG438: channel levels, crosstalk, glitch, extract, cube, dispersion.
- **Standards.** 8 standard frames: HIP 111538 and HIP 16652, both A0V per SIMBAD, K = 9.41 and 8.63. Each nod-pair partner was subtracted.
- **S.** Each cube is A − s(λ)·B, with s = the per-channel ratio of the spaxel medians (Law's recipe; not a Davies-style OH line-group fit). The s values run 0.94–1.06 across channels (5–95%), with a median per pair of 0.97–1.03 (`cfg438b_S_scales.json`).
- **T.** The aperture spectrum of each standard (0.5"), divided by a 9700 K blackbody (A0V, Pecaut & Mamajek 2013, quoted from memory, provisional) and normalised. Each science frame uses the standard nearest in airmass. Using 9500 instead of 9700 K tilts the curve by 0.046% across Kn2 and 0.011% across the H-alpha window.
- **Mosaic and grading.** DRP Mosaic Frames (MEANCLIP, TEL), then CFG438's `cfg438_kinematics.py` run unchanged on each work tree.

## Results
| version | gate | S/N ≥ 5 spaxels | summed S/N | kinematic PA | σ_m (km/s) | verdict |
|---|---|---|---|---|---|---|
| CFG438 (no S, no T) | — | 27 | 11.9 | 203° (199–207), tanh fit at its bounds | 76.7 ± 11.2 | NOT VALIDATED (V1, V2 FAIL; V4 PASS) |
| T only (reported) | standards fail S/N ≥ 50 | 27 | 11.1 | 197° (192–202) | 75.6 ± 11.3 | ablation |
| S only (reported) | no standards needed | 19 | 11.8 | **166° (162–170)** | 80.8 ± 13.2 | ablation (V2 would PASS; V1 FAIL; V4 MARGINAL) |
| S+T (graded) | **VOID** (standards S/N 12–31) | — | — | — | — | no verdict |

- **Standards (`cfg438b_telluric.json`).** The per-channel S/N of the eight frames is 12–31. The scatter between the two frames of each nod pair gives 10–28 independently, so the noise is real photon noise, not telluric structure. Dividing by these curves adds 5–10% noise to every science channel. That is why T-only lowers the summed S/N slightly.
- **The pre-stated T-only prediction (count moves ≤ 10%) holds:** 27 → 27.
- **S-only fixes the rotation fit.** The tanh model behaves: V_t = 162 km/s projected, r_t = 0.56", χ²_r = 0.95. In CFG438 the same fit sat at its bounds, with V_t ≈ 1000 and χ²_r = 6.0.
  - V_t / sin 42° ≈ 242 km/s, near Law's 234. This is a fit parameter, not the frozen V3, and is reported only.
  - The frozen V3 reaches only R = 0.25" (2.1 kpc), so it cannot test Law's 8 kpc value.

## Split-half invariance (post-freeze diagnostic; DIAG_INVARIANCE_PLAN.md, 7160ba3b25)
The splits are by night (N1 = 22 cubes, N2 = 18) and by alternating AB sequences (HA = HB = 20). Spaxels are matched by sky position; the registration is exact (≤ 0.001"). Pulls are (x1 − x2)/√(e1² + e2²) over spaxels with S/N ≥ 3 in both halves (34–46 spaxels per split).

| test | CFG438 cubes | S cubes |
|---|---|---|
| I1 v pull, robust std (N1/N2, HA/HB) | 2.40, 1.95 | 1.56, 1.76 |
| I1 v pull, plain std (tails) | 6.3, 12.7 | 6.0, 2.6 |
| I1 σ pull, robust std | 1.41, 1.58 | 1.27, 1.78 |
| I1 flux pull, robust std | 1.31, 1.28 | 1.30, 1.34 |
| I2 summed S/N ratio, half / full (white noise predicts) | 0.68, 0.80, 0.67, 0.72 (0.74, 0.67, 0.71, 0.71) | 0.72, 0.76, 0.66, 0.75 (same) |
| I3 summed v, difference between halves (km/s) | −17 ± 18, −39 ± 21 | +2 ± 17, +3 ± 20 |
| I4 count at S/N ≥ 4.39 (52-frame white-noise forecast) | 49 | 35 |
| I4 same, with flux errors × 1.3 (S/N ≥ 5.70) | 11 | 5 |
| I4 passing count in each half: actual (white forecast) | 4, 2, 4, 4 (1, 0, 0, 0) | 2, 1, 3, 5 (0, 0, 0, 0) |
| I5 PA on halves | none has ≥ 10 passing spaxels | same |

What the diagnostic shows:
1. **The errors are understated.** The fit errors (curve_fit with absolute_sigma, noise taken as the per-channel MAD over off-source spaxels) are too small by about 1.3× in flux. They are too small by 1.6–2.4× in velocity, with heavy outlier tails, which S removes on the HA/HB split. The likely cause is that the MAD noise misses the extra variance in on-source spaxels.
2. **The summed spectrum averages down like white noise (I2).** The noise problem is per spaxel, not in the stack.
3. **Within the halves, more spaxels pass than white noise allows** (2–5 against a forecast of 0–1). Some passing spaxels in the stacks are therefore likely noise, and the S/N ≥ 5 count is not a stable statistic on this data.
4. **The 52-frame white-noise forecast (49, or 35 on S) is unreliable** by the plan's own rule, because the errors are not honest. With the measured 1.3× correction, 52 frames give 11 (base) or 5 (S) spaxels, well short of 30. Law's third night could not have rescued V1 under our frozen cut.
5. **The velocity offset is stable once S is applied** (I3: the halves agree to 2–3 km/s). So it is a property of the data or of how the systemic redshift is defined, not a one-night artefact. On the S cubes the tanh v_sys is −162 km/s, but with a mostly one-sided sample it is degenerate with the centre. That is not a measurement of the offset.

## What this closes
- With these 40 public frames, our reduction reproduces three things from Law+12:
  - the kinematic PA (S-only: 166° against 168°);
  - σ_m within about 1–2σ (76–81 against 66 ± 6 km/s);
  - the sense of the major-axis gradient (S-only projected range −77 to +127 km/s, against Law's ±150).
- It cannot reproduce Law's V_c at 8 kpc. The outer disc is below the noise once the errors are corrected, and neither the missing night nor any of Law's described reduction steps changes that.
- Per the frozen stopping rule, no further reduction knobs are tried on BX442. Any a0(z ≈ 2.2) use of BX442 rests on Law's published V_c (CFG437), not on our own cube.
- What would change this is a deeper data set, such as JWST NIRSpec IFU or ERIS. Re-reducing these frames will not.

## Files
- **Scripts:** `cfg438b_build.py` (all steps) and `cfg438b_diag_invariance.py`.
- **Results:**
  - `cfg438b_S_results.json` and `cfg438b_T_results.json` (copies of `out_S/`, `out_T/`, which also hold maps, slit and V(R) tables);
  - `cfg438b_S_scales.json`;
  - `cfg438b_telluric.json` and `cfg438b_telluric_curves.txt`;
  - `cfg438b_diag_invariance_{base,S}.json`.
- **The S+T graded run was not built.** It is VOID at its validity gate, and building it would add no information.
- **Cubes** are in ../_external_data/cfg438b_work/ (not in git).
