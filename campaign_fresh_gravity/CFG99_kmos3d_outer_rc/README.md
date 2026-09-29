# CFG99 (run as CFG89) — KMOS3D cubes: how far out is Hα rotation measured, and how many z ≥ 1.9 discs reach g_bar < a₀ there?

**Renumbered (bookkeeping only).** This lane was frozen and run as CFG89: criteria 6eb7ae539 at 07:13, lane 029968534. Another session had committed its own CFG89 (8a9541d3a, a super-spirals re-derivation) at 06:55, so this lane moved to CFG99. Its files keep their working names (`cfg89_*`), and the script's docstring still shows the old path. The script's paths are relative to its own file, so it runs unchanged from here. Nothing else changed.

**This is a feasibility count, not a test of B.** No law is scored, and no velocity is compared with any prediction.

**Files:**
- Criteria, frozen and committed before any extraction: `FROZEN_CRITERIA.md` (commit 6eb7ae539).
- Script: `cfg89_kmos3d_outer_rc.py`. It takes about 1 minute on 14 processes. It reads the 739 cubes at `../_external_data/kmos3d/cubes` (relative to the repo root; nothing is copied into the repo).
- Outputs: `.out` and `_results.json`; the per-object table `cfg89_per_object.csv`; the per-aperture curves `cfg89_curves.csv`; the per-injection table `cfg89_c1_injections.csv`. Each has a `_MUTATE` twin.

**Exit codes:**
- Main run: exit 1. C1c, H1-can and H1-alt fail. Failing H1 on both footings is the declared, valid NOT FEASIBLE result, as in CFG54.
- MUTATE run (`MUTATE=1 python3 cfg89_kmos3d_outer_rc.py`): exit 1. It fails C1c, **D1**, H1-can and H1-alt.

## Bottom line

**NOT FEASIBLE on either footing.**

**How far out Hα rotation is measured at z ≥ 1.9.**
- The extraction measures Hα rotation on both sides of 150 of the 168 discs.
- The outermost reliable radius r_out has a median of **0.6″ (4.9 kpc), 1.5 R_e and 1.3 PSF FWHM**. The 84th percentile is 0.8″ (2.6 R_e).

**The count at r_out.**
- 74 are clean rotating discs.
- Of these, only **2 (canonical a₀) and 3 (alt a₀)** have g_bar < a₀ at r_out, against CFG54's gate of 5.
- Only **1 and 1** reach g_bar < 0.3 a₀.
- The median clean disc still sits at **g_bar ≈ 4 a₀** at its last measured radius.

**The count is marginal, not robust.**
- Lower-g brackets raise it: half the model gas gives 6 and 8 (canonical, alt); the enclosed-mass form gives 4 and 7.
- Higher-g readings lower it: twice the gas gives 1 and 1; the 0.2-dex mass floor gives 1 and 2.

**The velocity at r_out is not the circular velocity.** Synthetic discs injected into the real cubes come back a median **28% slow** at r_out, so control C1c fails (beam smearing plus aperture averaging).

**At z ≈ 0.6–1.1 the same pipeline does reach the regime.**
- **53 (canonical) and 65 (alt)** of 114 clean discs have g_bar < a₀ at r_out, and 9 and 16 are below 0.3 a₀.
- At z ≥ 1.9, the model baryonic acceleration at the last measured Hα radius is still above a₀ for almost every disc.

## Results

**Stages** (FLAG_ZQUALITY = 0):

| window | selected | E0 | r_out > 0 | K1 coherent | K2 V/σ₀ ≥ 1 | not K3 | gate σ_V/V ≤ 0.25 = clean |
|---|---|---|---|---|---|---|---|
| HIGH, z ≥ 1.9 (all K band) | 168 | 156 | 150 | 112 | 79 | 75 | **74** |
| LOW, 0.6 ≤ z ≤ 1.1 (YJ) | 215 (213 in window) | 188 | 185 | 157 | 121 | 116 | **114** |
| MID, 1.1 < z < 1.9 (H; reported row R8) | 145 | 136 | 135 | 110 | 81 | 74 | 74 |

The FLAG_ZQUALITY = 1 rows (8, 21 and 12 objects) add 0, 1 and 1 clean discs. None is at z ≥ 1.9, so the headline is unchanged (R7).

**Counts at r_out** (clean discs; N(< a₀) / N(< 0.3 a₀)):

| row | canonical 9.3603e-11 | alt 1.1312e-10 |
|---|---|---|
| **HIGH, declared model (Freeman disc, Tacconi gas) — headline** | **2 / 1** | **3 / 1** |
| HIGH, gas × 0.5 (R3) | 6 / 1 | 8 / 1 |
| HIGH, gas × 2 (R3) | 1 / 0 | 1 / 0 |
| HIGH, enclosed-mass form, the lower-g bracket (R4) | 4 / 1 | 7 / 1 |
| HIGH, either-side r_out (R6) | 4 / 1 | 6 / 1 |
| HIGH, robust to the 0.2-dex mass floor (R9) | 1 / 0 | 2 / 0 |
| HIGH, only r_out ≥ PSF FWHM (R5; 68 of 74) | 2 / 1 | 3 / 1 |
| LOW comparison | 53 / 9 | 65 / 16 |
| MID (reported, R8) | 14 / 2 | 23 / 3 |

**Distributions at r_out.** Each cell gives the median, then the 16th–84th percentile range in brackets.

| set | r_out [″] | r_out [kpc] | r_out / R_e | r_out / PSF | g_bar/a₀ (canonical) |
|---|---|---|---|---|---|
| HIGH, measured (N = 150) | 0.6 (0.4–0.8) | 4.9 (3.2–6.6) | 1.46 (0.96–2.60) | 1.28 (0.87–1.92) | 4.2 (1.9–9.7) |
| HIGH, clean (N = 74) | 0.6 (0.4–0.8) | 5.0 (3.3–6.6) | 1.43 (1.04–2.09) | 1.61 (1.08–2.02) | 4.0 (1.8–9.3) |
| LOW, measured (N = 185) | 0.8 (0.4–1.0) | 6.0 (3.1–7.8) | 1.48 (0.93–2.44) | 1.42 (0.88–2.11) | 1.02 (0.39–3.47) |
| LOW, clean (N = 114) | 0.8 (0.6–1.0) | 6.3 (4.6–7.9) | 1.52 (1.14–2.39) | 1.62 (1.12–2.21) | 1.03 (0.41–2.87) |

- **Extremes:** the largest r_out/R_e is 7.6 at HIGH and 6.4 at LOW. The lowest g_bar/a₀ is 0.24 at HIGH and 0.12 at LOW.
- **Field-of-view limit:** 1 of 74 clean HIGH discs is FOV-limited, against 16 of 114 at LOW, so some LOW r_out values are lower limits.

**The three HIGH discs below a₀ (R14):**
- **U3_10584:** z 2.246, log M* 8.99, μ_gas 6.7. g_bar/a₀ = 0.24 (canonical) and 0.20 (alt).
- **COS4_08515:** z 2.454, log M* 9.88, μ_gas 2.0. g_bar/a₀ = 0.75 and 0.62.
- **U4_22581:** z 2.166, log M* 10.19, μ_gas 1.0. g_bar/a₀ = 1.11 and 0.92, so it counts on the alt footing only.

All three have:
- r_out = 0.8″ ≈ 6.5 kpc, which is 1.4–1.7 R_e and 1.7–1.9 PSF FWHM;
- σ_V/V = 0.07–0.10;
- V_rot/σ₀ = 1.4–2.2.

The first one owes its low g_bar to an extrapolated gas fraction (Tacconi+2018 at log M* ≈ 9).

## Controls

| check | result | verdict |
|---|---|---|
| C1a: honest velocity errors | pull robust std 1.08 over 343 reliable apertures of 40 rotating injections | PASS |
| C1b: r_out not inflated by noise | median r_out − r_exp = 0.00″; 97% within 0.4″ (N = 39) | PASS |
| **C1c: V at r_out** | only 12 of 33 within 25% (70% needed). V_rot/V_true median 0.72 (16th–84th percentile 0.59–0.78), at r_out ≈ 1.5 PSF FWHM | **FAIL** |
| C1d: rotation detection | 31/33 rotating discs pass K1; 1/20 non-rotating discs pass K1 | PASS |
| C2: integrated Hα flux vs HAFIT_FLUX_HA | median −0.024 dex, scatter 0.061 dex (N = 347; the 7 failed fits entered as −inf). Against the aperture-corrected flux: +0.006 and 0.082 | PASS |
| C3: centroid redshift vs Z | median +9.8 km/s, scatter 11.7 km/s (N = 340). The vacuum convention holds: no 83 km/s air/vacuum offset | PASS |
| D1: coherent rotation in the real sample | 269/381 = 71% pass K1 | PASS |
| H1-can / H1-alt | 2 and 3 objects (5 needed) | **FAIL: NOT FEASIBLE** |

- **C2 and C3** also support the inferred readings of the catalogue: fluxes in 1e-17 erg s⁻¹ cm⁻² in a 1.5″-radius aperture, and vacuum wavelengths.
- **C1c is a real finding, not a bug.**
  - PA recovery is good (median error 3.3°).
  - The loss comes from beam smearing and aperture averaging off the major axis at 1–2 beams.
  - It does not change the count, which uses g_bar at r_out only. It does mean that no g_obs could be taken from these pseudo-slit velocities without forward modelling.

**MUTATE:**
- The spaxels of every real cube were spatially scrambled before the kinematic extraction. K1 then passes in **8/381 = 2.1%** of objects, D1 fails, and the run exits 1.
- The failing set {C1c, D1, H1-can, H1-alt} differs from the main run's {C1c, H1-can, H1-alt}.
- **The control is informative for rotation detection.** Scrambling takes K1 from 71% to 2% and E0 at HIGH from 156 to 19, so K1 responds to spatial coherence and not to line S/N alone.
- **It is not informative for the headline.** The main run already fails H1, and the scrambled run gives 0 and 0.
- C1, C2 and C3 are identical in both runs by design.

## Caveats (the ones that matter most first)

1. **Beam smearing.**
   - r_out is only about 1.3–1.6 PSF FWHM (median), and the three counted objects are at 1.7–1.9 PSF.
   - The light at r_out includes smeared light from further in, so the radius the velocity really samples is smaller than r_out. That makes the count, if anything, optimistic.
   - The velocity there is about 28% low (C1c).
2. **Model gas.**
   - μ_gas comes from the Tacconi+2018 scaling, with δMS from the catalogue SFR. It is not measured.
   - The factor-2 bracket moves the headline from 1 to 6 (canonical) and from 1 to 8 (alt).
   - The only object below 0.3 a₀ depends on the relation extrapolated to log M* ≈ 9 (μ_gas = 6.7).
3. **Pressure support.**
   - No asymmetric-drift correction is applied. The counted discs have V/σ₀ = 1.4–2.2.
   - It does not enter g_bar, but it enters any future g_obs.
   - K2 uses the beam-smeared V, which is biased low. Post-hoc row P1 shows that none of the 17 objects rejected by K2 alone would have counted.
4. **Stellar masses and RHALF come from the catalogue.**
   - M* comes from SED fits and RHALF from the H-band catalogue. RHALF is read as the semi-major-axis radius in arcsec, as CFG52 read it.
   - The catalogue column meanings (flags, units) are not on disk and were inferred. C2 and C3 support them.
   - The model is one exponential disc with no bulge.
   - Only 1 (canonical) and 2 (alt) objects survive a 0.2-dex mass shift.
5. **Inclination** comes from Q with q0 = 0.2. It enters only K2, not r_out or g_bar.

## Disclosed departures and post-hoc rows

- **P1 (reported only; added after the first full run, in response to C1c).** It counts the HIGH objects that pass K1, pass the gate and are not K3, but fail K2. There are 17 such objects, with V_rot/σ₀ of 0.40–0.92. None has g_bar < a₀, so the headline does not depend on K2.
- **Code edits before the first full run** (at that point no real galaxy's kinematics had been computed):
  - The FOV-limited flag counts only a side whose run ends exactly at r_out. This is my reading of "the limiting side".
  - Failed or non-positive integrated fits enter C2 as −inf. The frozen text was silent on them; −inf is the conservative choice.
- **Smoke tests before that run** used synthetic injections only, on four hosts. One of them, COS4_01966, has FLAG_ADDGALDET = 1 and is not a C1 host. They also used one S/N map of an empty injection window. That map showed spaxel-to-spaxel scatter somewhat above the noise extension over multi-channel sums; C1a then measured a pull width of 1.08.
- **After the first run**, the injection results are sorted before printing. This is cosmetic. The rerun reproduces the first run's tables byte for byte, and no check changed.
- **Implementation guards** not spelled out in the frozen text:
  - a 1e-12 ridge on the grid normal equations;
  - f = 1 if fewer than 60 line-free channels are valid.
- **Spurious warnings:** numpy on this machine raises spurious floating-point warnings from BLAS `matmul`. Its output agrees with `einsum` to 1.5e-15, and the workers suppress the warnings.
- **No subsample fallback** was needed: the projected runtime was 0.9 minutes.

## What this means for the a₀(z) test

- **At z ≥ 1.9 the flat-a₀ versus a₀ ∝ H(z) test cannot be run on the KMOS3D cubes with this extraction.**
  - There are 2–3 candidates.
  - All sit near two beams, where the pseudo-slit velocity is biased low.
  - This agrees with CFG52 and CFG54.
  - CFG63's cap of about 2.3σ from the correlated mass scale would apply even if usable discs existed.
- **At z ≈ 0.6–1.9 the g_bar < a₀ regime is reached for tens of discs.** Using them would still need a beam-smearing forward model (C1c) and measured gas.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.


## Notes after the independent re-run (appended 2026-09-29; no result changed)

- **Not verified by LEDGER_VERIFICATION Part 5 (84910a506, at HEAD 4fa9f54e3):** the KMOS3D cubes are git-ignored and outside the repo. Without them the script gives 16/25 checks against the committed 22/25, and it still exits 1.
- **Data requirements (not in git):** the 739 KMOS3D cubes (about 3.8 GB) at `../_external_data/kmos3d/cubes` relative to the repo root, with their hashes in `data_assembly/kmos3d_phibss/manifest.json`. The catalogue `data_assembly/kmos3d_phibss/kmos3d_catalog.csv` is in git.
