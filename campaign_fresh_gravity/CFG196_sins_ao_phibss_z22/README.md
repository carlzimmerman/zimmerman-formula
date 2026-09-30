# CFG196 — a₀ at z ≈ 2.2 from SINS/zC-SINF AO Hα kinematics with PHIBSS CO gas (phase 1: frozen criteria and pre-flight)

- **Criteria:** `../CFG196_FROZEN_CRITERIA.md`.
  - Written before the pre-flight script existed and before any kinematic extraction.
  - Pre-extraction notes are appended at its end.
  - Not committed: the orchestrator reviews and commits it before any phase-2 work.
- **Script:** `CFG196_preflight.py`, about 1.5 s.
  - Its inputs are the PHIBSS table values, the cut-cube FITS headers and the PSF images.
  - It reads no cube spectrum and no velocity column.
- **Runs:**
  - The main run passes 6 of 7 checks and exits 0. The one miss is the reported H0.
  - The MUTATE run (the rival's E(z) → 1) collapses every separation to exactly 0, fails the headline S1, and exits 1.
  - The first run is kept as `*_firstrun*`. The final run adds a post-hoc diagnostic block; every frozen-set number is identical.

## Bottom line

**The pre-flight says the test CANNOT discriminate flat a₀ from a₀ ∝ H(z) on these data.**
- For the two primary discs, the declared profiled separation is **Z_prof = 0.91σ**, against a threshold of 2.
- No declared variant reaches 2. The largest is 1.54σ, and it assumes the curves reach 3 R_e, which the cut cubes do not.
- By the frozen D0, a phase-2 flat-against-rival verdict would therefore be NON-DIAGNOSTIC before any extraction, whatever FS2018's inclinations turn out to be. With the inclination error removed entirely, Z_prof is still 1.00.

**Why it fails:**
1. **The overlap is smaller than it looks.**
   - The names match in six galaxies, not five. The sixth, BX389, has only a CO upper limit.
   - Of the five CO detections, BX482's CO belongs to the companion BX482se, per Tacconi et al. 2013's Fig. 5 caption, so it is not the disc's gas.
   - The rule "measured whole-galaxy CO plus PHIBSS Disk(A)" leaves two primary discs: ZC406690 and Q2343-BX610. FS2018's class check (R3) is still pending.
2. **The accelerations are high.**
   - At 1 R_e, g_N/a₀ is 2.9 for ZC406690 and 17 for BX610.
   - There the laws differ by 31 and 15 km/s, i.e. 12% and 3% of V.
3. **The reach is short.**
   - The cut cubes' inscribed radius around the centre is 9.1 and 8.5 kpc. At FWHM spacing that is about 1.3–1.4 R_e.
   - 2 R_e, and BX610's 3 R_e, lie only in the cube corners; ZC406690's 3 R_e is outside the cube.
4. **Normalisation is degenerate.**
   - Both the inclination error (±5°) and the mass calibration (M* ±0.2 dex; α_CO ×/÷1.5) rescale V as a whole.
   - With P2 and the canonical footing, the two laws' mass bands overlap at every radius of every galaxy row. The only exception is BX482's gas-free main disc at 3 R_e.
   - Only the shape of ΔV(R) discriminates, and within 1.4 R_e that shape is small against the statistical errors.

## Pre-flight table: primary discs

Settings: P2 kernel, canonical footing, i = 45°. The error budget is the declared PS-B budget. Bands run over the 9 mass cells. A reach of "in" means inside the cut cube, "corner" the corners only, "out" beyond it.

| galaxy | R/R_e | R (kpc) | reach | g_N/a₀ | V_N | V_flat [band] | V_rival [band] | ΔV (km/s) | σ_V | ΔV/σ_V | PS-B − PS-K (km/s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ZC406690 (z 2.196, E 3.31) | 1 | 6.3 | in | 2.86 | 228 | 246 [205–297] | 277 [238–325] | 30.6 | 28.8 | 1.06 | 9.8 |
| | 2 | 12.6 | corner | 1.30 | 217 | 251 [214–298] | 298 [262–343] | 47.7 | 35.1 | 1.36 | 21.8 |
| | 3 | 18.9 | out | 0.61 | 182 | 232 [202–270] | 290 [258–329] | 58.0 | 47.5 | 1.22 | 39.8 |
| Q2343-BX610 (z 2.211, E 3.33) | 1 | 4.6 | in | 17.1 | 477 | 483 [395–594] | 498 [412–606] | 14.9 | 46.0 | 0.32 | 4.9 |
| | 2 | 9.2 | corner | 6.82 | 426 | 440 [363–538] | 470 [396–563] | 29.7 | 45.9 | 0.65 | 12.0 |
| | 3 | 13.8 | corner | 3.03 | 347 | 373 [311–451] | 418 [360–492] | 45.2 | 51.2 | 0.88 | 23.4 |

- **Other kernels and footings.** ν_mono and the alt footing enlarge ΔV by roughly 10–65%; ZC406690's ΔV/σ reaches at most 1.65 (ν_mono, alt). Every row is in `CFG196_preflight.out`, including the bands.
- **The prescription spread.** The last column is how much the PS-B and PS-K pressure corrections differ for the same observed rotation. It is one third to two thirds of the law separation, which is why the criteria require the two prescriptions to agree.

**Sample-level separation (H0).** Primary discs, dense FWHM sampling, reachable radii only:

| variant | Z_nom (masses exact) | Z_prof (masses profiled) |
|---|---|---|
| **declared: P2, canonical, i = 45°, PS-B budget** | **1.39** | **0.91** |
| i = 30° / 60° | 0.87 / 2.05 | 0.72 / 1.03 |
| ν_mono / alt footing / PS-K budget | 1.79 / 1.57 / 1.43 | 1.18 / 1.03 / 0.92 |
| 1, 2, 3 R_e, reachable only / all assumed reached | 1.11 / 1.85 | 0.70 / 1.54 |
| one shared (δ*, δ_CO) for both discs | — | 1.01 |

**Reported galaxies.** No reported row reaches Z_prof = 1.3. The largest is 1.22, for BX482's gas-free main disc under the PS-K budget, where Z_nom is 1.97.
- The only rows with g_N below about a₀ at 1–2 R_e are those without measured gas:
  - BX482's main disc, with FS2009's M* and no gas: g_N/a₀ = 0.89 at 1 R_e;
  - BX389 at gas = 0: 0.98 at 2 R_e.
- **In this overlap, measured gas and low acceleration do not coincide.**

## What limits it (post-hoc ablation; reported only; H0 unchanged)

Each row changes one term of the declared budget at a time. "Dense" is the declared set; "1–3 R_e" assumes those radii are reached.

| change | Z_prof, dense | Z_prof, 1–3 R_e |
|---|---|---|
| none (declared) | 0.91 | 1.54 |
| inclination error 0 | 1.00 | 1.64 |
| σ₀ error 0 | 0.93 | 1.67 |
| statistical error 0 | 1.36 | 2.54 |
| inclination and σ₀ exact | 1.02 | 1.79 |
| mass priors halved (0.1 dex; ×/÷1.22) | 1.19 | 1.73 |
| i and σ₀ exact, and mass priors halved | 1.69 | 2.37 |
| near-perfect kinematics (1 km/s), priors as declared | 11.0 | 30.8 |

- **No single realistic improvement lifts the declared set to 2σ.**
- The inclination and the mass calibration are interchangeable normalisation freedoms: removing one leaves the other.
- What is left is the shape of ΔV(R), which needs reach, beyond about 2 R_e, and precision.
- The near-perfect row shows that the shape information exists: the two laws are not degenerate in principle. It is not a forecast.

## Anticipated for BX610 (disclosed before freezing, criteria §0)

- **The prediction.** With PHIBSS's Galactic-α_CO gas (2.3 × 10¹¹ M☉ at R_CO = 3.8 kpc), the Newtonian baryonic V at 1 R_e is 477 km/s. With the ULIRG-like α_CO it is still 299 km/s.
- **The published values**, known to the analyst: V_c 324 ± 71 km/s (FS2009, seeing-limited) and vrot 216 km/s (PHIBSS).
- **The expected phase-2 outcome for BX610** is therefore the declared D5 BARYON OVERSHOOT. That is a statement about the gas calibration, not about a₀.
- This comparison uses published numbers, not the cubes. It is an expectation, not a result.

## Phase 2: what it would do, and whether to run it

**The frozen plan (criteria §3–§6):**
- per-spaxel Hα + [N II] fits of the cut cubes;
- a major-axis pseudo-slit, one FWHM wide;
- a thin-disc forward model through each galaxy's own PSF (moments, checked against a full cube);
- three pressure prescriptions: PS-B primary, PS-K and PS-0, never pooled;
- PHIBSS baryons over a 9-cell mass grid, 3 inclination cells, P2 and ν_mono, both footings;
- the statistic Δχ² = χ²_rival − χ²_flat;
- decision lines D0–D6, controls C1–C6, and MUTATE M1 (planted a₀ in mock cubes), M2 (shuffled gas), M3 (V × 10^0.15) and M4 (E → 1).

**Prerequisite:** the owner's go to fetch FS2018 (ApJS 238, 21; arXiv:1802.07276, the id recalled), for the published PA, inclination and AO kinematic class. Without it, phase 2 runs on the declared fallback geometry, and every statement is labelled that way.

**Effort and runtime (estimates):**
- About one working day of agent time for the fitter, the forward model and the controls.
- Under about 1 CPU-hour on one worker for all six galaxies:
  - line fits, about 10 s per galaxy;
  - the 972-cell grid with the moment forward model, about 2 min per galaxy;
  - M1's 2 × 20 mock realisations per primary, about 15 min in total.
- Light enough for the loaded machine.

**Recommendation.**
- **Do not run phase 2 as a flat-against-rival test.** By the frozen D0 it is NON-DIAGNOSTIC at every inclination before extraction.
- **It is worth running only for its reported rows.** These are:
  1. D5 and the gas break-evens (the gas scale f at which Newton, flat and the rival each fit best) at z ≈ 2.2 with directly measured CO. That speaks to the gas question the KURVS lanes turned on (CFG162/164), though it is not an a₀ result.
  2. A pipeline validated by M1, for future data.
- That is the orchestrator's and the owner's call.

**What a decisive z ≈ 2 test needs, from the ablation and consistent with CFG52:**
- discs with measured CO and g_N ≲ a₀ at the measured radii, i.e. lower-mass or more extended discs than these;
- curves to at least 3 R_e at useful S/N;
- inclinations to about 2°;
- mass calibration near 0.1 dex.

## Implementation notes and departures (disclosed)

- **The post-hoc block** (limits and ablation) was added after the first run. The first run is kept verbatim, and the frozen-set tables are byte-identical between the runs (checked by diff). A label in the first draft of the block ("mass-calibration floor alone") was wrong: the 1 km/s run shows that shape information survives the mass freedom. It was corrected before the final run.
- **Z_prof** is a grid minimum at 0.02-dex steps. For gas-free rows δ_CO is pinned at 0.
- **The PSF FWHM** comes from a circular Gaussian fit (0.18–0.29″). For BX389 the half-maximum-area estimate disagrees (0.11″ against 0.21″); the Gaussian value is used.
- **Inputs beyond PHIBSS,** all non-kinematic and declared in criteria §7:
  - FS2009 Hα r1/2 for the BX599 and BX513 size variants;
  - FS2009 M* and r1/2 for BX482's main disc;
  - FS2009 z_Hα for BX389, which has no z_CO.
  - The H0 set uses PHIBSS values only.
- **E(z):** E(2.2) = 3.32 with the record's Ω_m = 0.315. The brief's "≈ 3.2" corresponds to Ω_m = 0.3 (3.24).
- **Radius sources:** PHIBSS's rh_opt is the Hα radius for the BX galaxies. For zC406690 the table's note does not say which band.
- **Coverage:** Hα at z_CO falls inside every cut cube's wavelength range (C6). The cut cubes are 46 × 46 spaxels (2.3″), except BX482's 56 × 56 (2.8″). The full cubes are larger (for example 81 × 81 for ZC406690), but their S/N reach is unknown; the "1–3 R_e reached" rows are the optimistic bound on that.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
