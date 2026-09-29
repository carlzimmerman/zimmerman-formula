# CFG80 — a ΛCDM comparator for CFG33 (SLACS lensing against ATLAS3D dynamics): FROZEN CRITERIA

Written 2026-09-29, **before any CFG80 script exists and before any ΛCDM prediction for these data has been computed**. This file is committed on its own, before any scoring.

What was done before writing it (disclosed): CFG33's script, README and `.out`, CFG69's docstring, model block and `jam_mass_lcdm`, CFG45's prefix and h53's prefix were read. As a plumbing test, CFG33's pipeline (up to its reported rows) and CFG45's prefix were exec'd read-only. That printed B's committed numbers, f_b, ρ_c and the range of the Moster grid. The SLACS table's stellar-mass range was also looked at: log M_Salp runs 10.67–12.03, above the top of the Moster grid at 11.97. **No halo mass, projected mass, α or gap was evaluated for any lens or galaxy under ΛCDM.**

## Question

CFG33 tests B's lensing against B's dynamics. Under B's law (ν_mono) the SLACS lenses need α_lens = 1.20–1.27 × Salpeter. ATLAS3D's JAM masses, fitted in log σ and evaluated at the lenses' dispersions, need α_dyn = 0.85–0.86 ×. The gap is +0.15–0.17 dex: 1.5–1.7σ with the declared 0.10-dex floor, and 7–8σ statistically.

**Through CFG33's identical pipeline, does a standard ΛCDM halo show the same lensing–dynamics gap?** "Identical" means the same 70 lenses and Einstein radii, the same ATLAS3D Q ≥ 1 JAM calibration set, the same linear fit in log σ, the same median statistic and bootstrap, and the same 0.10-dex floor. Is B's gap SPECIFIC-TO-B, SHARED, ΛCDM-WORSE, or NON-DISCRIMINATING?

## Identical to CFG33 (exec'd read-only; its MUTATE forced off)

- **The pipeline:** `CFG33_slacs_lensing_vs_dynamics.py` is exec'd up to its reported rows, using CFG69's `exec_prefix` pattern with a read-only `open`. Through it come h53's 70 lenses and h9's ATLAS3D sample: 258 galaxies, 187 with JAM quality ≥ 1.
- **Lens quantities:** h53's lens quantities, all in Auger's cosmology (Ω_m = 0.3, Ω_Λ = 0.7, h = 0.7), as tabulated and as h53 recomputes them:
  - R_E in kpc;
  - M_E = π R_E² Σ_crit, as h53 recomputes it; its validation A matches Auger's tabulated Einstein masses;
  - Auger's Salpeter f_* and M_Salp;
  - the SDSS dispersion.
- **ATLAS3D quantities:** M_JAM = (M/L)_JAM L, M_Salp = (M/L)_Salp L, r_1/2 in kpc, σ_e.
- **B's side:** CFG33's four cells (canonical/alt × V/I), exactly as its exec computes them.

## The ΛCDM model (declared once; CFG69's "base"; no tuning)

- **Stars:** α × the lane's own Salpeter stellar mass, with the lane's own stellar profile.
  - Lens: the projected stellar mass inside R_E is α f_*,Salp M_E. This is Auger's measured fraction, taken exactly as CFG33 / h53 take it.
  - ATLAS3D: half the stars lie inside r_1/2.
- **Dark halo:** adds (1 − f_b) M_NFW, with f_b = Ω_b/Ω_m = 0.02237/(0.02237 + 0.1200) = 0.1571.
- **Halo mass:** M_h = `halo_mass(M_*)`, h48's Moster+2013 z = 0 relation. `halo_mass`, `FB` and `RHO_C` are obtained exactly as CFG69 obtains them: its `exec_prefix` of `CFG45_rule_readings.py` up to the "P3 SPARC" marker, with the same `READ` replacement.
  - M_h is evaluated at the stellar mass the model solves for, M_* = α M_Salp. This ties the halo to α exactly as CFG69's `jam_mass_lcdm` ties it to the solved M_*.
  - The Moster grid spans M_h = 10⁹–10^15.5 (M_* = 10^4.28–10^11.97). Above M_* = 10^11.97, `np.interp` clamps M_h at 10^15.5. This is counted and reported.
- **Concentration:** Duffy+2008 full sample, 200c: c = 5.71 (M_h / (2 × 10¹² / h))^−0.084, h = 0.674, with no (1+z) term.
  - The NFW profile is m(t) = ln(1+t) − t/(1+t), with x = r/R_200 clipped to [10⁻⁴, 5] and the mass normalised to M_h at R_200.
  - `c_duffy_full`, `c_duffy_relaxed`, `c_dm`, `_m_nfw` and `make_nfw` are **copied verbatim from CFG69**.
- **Critical density: z = 0, declared once and not scanned.** R_200c is defined against ρ_c(z = 0) = 3H₀²/(8πG) with H₀ = 67.4: h48's `RHO_C` via CFG45, 1.2605 × 10¹¹ M☉ Mpc⁻³, as CFG69 uses it. The reasons:
  - It is CFG69's declared model.
  - The Moster row (h48) and the Duffy row are z = 0 relations. Moving only ρ_c to each lens's redshift would mix epochs.
  - The JAM calibration set is local.
  - The lenses sit at z ≈ 0.06–0.5 (median 0.19). A redshift-consistent halo would need ρ_c(z), Duffy's (1+z)^−0.47 and Moster's z-evolution. That is **untested here** and is a caveat, not a variant.
- **Lensing, the projected halo:** the standard analytic untruncated NFW cylinder mass (Bartelmann 1996; Wright & Brainerd 2000): M_2D(<R) = M_h h(X)/m(c), with X = c R/R_200.
  - h(X) = ln(X/2) + 2/√(1−X²) · artanh√((1−X)/(1+X)) for X < 1;
  - h(X) = ln(X/2) + 2/√(X²−1) · arctan√((X−1)/(X+1)) for X > 1;
  - h(1) = 1 + ln ½.
  - The 3D profile's saturation at 5 R_200 is **not** applied to the projection. Its size is reported (R7).
- **Dynamics:** Newtonian (ν = 1), with no phantom. **No adiabatic contraction and no SHMR scatter; both are declared untested.**
- **Cosmology conventions, kept as the committed machineries have them:** the lensing geometry uses Auger's h = 0.7 (h53), and the halo's ρ_c uses h = 0.674 (h48). The ~4% length-unit mismatch is disclosed, not corrected.
- **Consequences of the model:**
  - ΛCDM has no a₀, so its numbers are **identical on both footings**.
  - Without adiabatic contraction the stellar profile does not enter ΛCDM's lens prediction, so **its V and I rows are identical by construction.**

**The solves.** m is the halo-mass multiplier: 1 for the base model, 1/3 or 3 for V3/V4, and × 100 under MUTATE.
- **Lens:** κ̄(α) = α f_*,Salp + (1 − f_b) M_2D,NFW(<R_E; m · M_h(α M_Salp)) / M_E = 1. It is solved in log M_* ∈ [8, 13.5] (CFG69's bracket; brentq, xtol 10⁻¹²), and α_lens,ΛCDM = M_*/M_Salp.
- **ATLAS3D:** CFG69's `jam_mass_lcdm`, copied verbatim, solves 0.5 M_* + (1 − f_b) M_NFW(<r_1/2; m · M_h(M_*)) = M_JAM/2 on the same bracket. Then α_dyn,ΛCDM = M_*/M_Salp.
- **Exclusions:** a system with no root in the bracket is **excluded and counted**, as CFG69 does for SLUGGS. Either its halo alone exceeds the target at M_* = 10⁸, or the target is out of reach at 10^13.5.

**The statistic (CFG33's, identical).**
- log α_dyn is fitted linearly in (log σ_e − 2.3) over the Q ≥ 1 ATLAS3D galaxies that calibrate, and evaluated at each lens's SDSS dispersion.
- Δ = the median over the solved lenses of log α_lens − fit.
- **Error:** the standard deviation of 2000 bootstrap resamples, with the lenses and the calibration set resampled and the fit redone. The draws come from a fresh `numpy.random.default_rng(33)` in CFG33's draw order, so with no exclusions they are exactly the resamples of CFG33's first cell.
- σ_tot = √(err² + 0.10²); z = Δ/σ_tot (floor-inclusive); z_stat = Δ/err.

## Circularity (stated plainly)

**No CFG33 input is derived from a halo mass.**
- **Auger's inputs:** M_E comes from the lens models (θ_E and the two redshifts); f_* and M_Salp come from stellar-population fits to the photometry.
- **ATLAS3D's inputs:** (M/L)_Salp comes from stellar populations. (M/L)_JAM is ATLAS3D XV's JAM total M/L, with M_JAM ≈ 2 M_1/2. h9 and CFG33 read it as the self-consistent, mass-follows-light value, which uses no halo mass; this was **not re-verified against the paper here**. The ATLAS3D XX columns that come from halo models (fDM_Re, logML_stars) are loaded by the table reader but **not used** by CFG33.

Two shared ingredients are disclosed. They are not circular:
- M_JAM is a total mass, so any halo inside r_1/2 is part of the measured target that both models must reproduce.
- The Moster SHMR is ΛCDM's own abundance-matching ingredient. It is calibrated on Chabrier-like stellar masses, while here it takes α × Salpeter masses. That is CFG69's tie, kept unchanged, and it is a caveat: at the high-mass slope (~2.5), 0.25 dex in M_* is ~0.6 dex in M_h, which V3 (× 1/3) roughly spans.

## Classes (CFG69's), for B's gap

B's gap is positive in all four cells: the lenses need more stellar mass than the dynamics. B is MARGINAL with the floor (1.5–1.7σ) and FAILS statistically (7–8σ).

**ΛCDM's gate outcome** is one of:
- **PASS:** |z| ≤ 2;
- **FAIL+:** z > 2;
- **FAIL−:** z < −2;
- **UNFIT:** fewer than 35 of the 70 lenses solved, or fewer than 94 of the 187 calibration galaxies calibrated.

The classes:
- **SHARED:** FAIL+ (B's sign, |z| > 2).
- **SPECIFIC-TO-B:** PASS (ΛCDM within 2σ).
- **ΛCDM-WORSE:** FAIL− (the opposite sign at > 2σ).
- **NON-DISCRIMINATING:** the outcome with every M_h × 100 equals the base outcome. This overrides the three-way class, which is still reported.
- **UNFIT:** no class is drawn.

The class uses the **floor-inclusive** z. The statistical-only z, and the class it would give, are reported (R1) and never used for the classification.

## Pre-declared checks

**Controls (load-bearing)**
- **C1 CONTROL:** CFG33's committed B numbers are reproduced through this script's exec of its pipeline, **to CFG33's printed precision**. This covers α_lens (median log), α_dyn at the lenses' dispersions, the difference ± its statistical error, and z with and without the floor, in all four cells.
  - The four H2 lines rebuilt from the exec must appear verbatim in the committed `.out`.
  - Every exec'd number must agree with the committed JSON within half a printed unit. The maximum JSON deviation is also printed.
  - **And** the generic estimator this script uses for ΛCDM, fed B's per-object α's with CFG33's seed and draw order, must reproduce the four differences and bootstrap errors to 10⁻¹².
- **C2 CONTROL:** the NFW enclosed mass at R_200c equals M_h to 10⁻¹², using `make_nfw` with Duffy full, Duffy relaxed and Dutton–Macciò c, for M_h = 10⁹–10^17.5, monotone in r.
  - The copied functions are verbatim CFG69: the source text is identical.
  - `RHO_C` equals 3H₀²/(8πG) with H₀ = 67.4 in h48's constants (z = 0) to 10⁻¹².
- **C3 CONTROL:** the analytic projected NFW mass equals a **direct numerical projection of the 3D NFW density** to **10⁻⁴**, as the maximum relative deviation. Two projections are used:
  - (a) spherical shells projected into the cylinder: ∫ 4πr²ρ(r) w(r, R) dr, with w = 1 inside R and w = 1 − √(1 − R²/r²) outside, normalised by the numerically integrated ∫₀^c;
  - (b) the line-of-sight Σ(R) integrated over the disc.

  The grid spans masses 10¹⁰–10¹⁷, radii 0.3–100 kpc, all three c relations, X < 1 and X > 1, and X = 1 exactly.
- **C4 CONTROL:** the solves.
  - κ̄_ΛCDM(α_lens) = 1 to 10⁻⁹ at every solved lens.
  - The ΛCDM mass inside r_1/2 equals M_JAM/2 to 10⁻⁹ at every calibrated galaxy.
  - With the halo switched off (M_h × 10⁻³⁰), the solvers return α_lens = 1/f_* and α_dyn = M_JAM/M_Salp to 10⁻⁹.
  - The halo only adds mass: α_lens,ΛCDM ≤ 1/f_* and α_dyn,ΛCDM ≤ M_JAM/M_Salp everywhere.
- **C5 MUTATE WITNESS:** the halo mass entering every base-model solve (lens and JAM) equals the Moster value of that solve's stellar mass, M_h / `halo_mass`(M_*) = 1, to 10⁻¹².
  - It **passes in the main run by construction** and **fails under MUTATE by construction** (ratio 100).
  - It guarantees that the MUTATE run exits 1 and that its failing set differs from the main run's. **It says nothing about whether the science responds**; that is C6's job.

**Headline**
- **H1 [HEADLINE] ΛCDM PASSES CFG33's GATE through the identical pipeline.** Checkable lines, all required:
  - H1a: at least 35 of the 70 lenses are solved.
  - H1b: at least 94 of the 187 Q ≥ 1 ATLAS3D galaxies are calibrated.
  - H1c: |Δ_ΛCDM| ≤ 2 σ_tot (bootstrap ⊕ 0.10 dex).

  PASS gives SPECIFIC-TO-B, unless NON-DISCRIMINATING. FAIL gives SHARED (z > +2), ΛCDM-WORSE (z < −2) or UNFIT (H1a or H1b).
- **C6 (MUTATE run only; load-bearing there):** the ΛCDM gate outcome with every M_h × 100 differs from its outcome at × 1. Both are computed in-process in every run; the main run's JSON is also read, if present, as a cross-check.
  - If C6 fails, the comparison is NON-DISCRIMINATING and the MUTATE control is uninformative for the headline.
  - In the main run the same comparison is a reported row (R6).

**Reported (never load-bearing)**
- **Class:** the classification line: the class, B's four cells beside ΛCDM, and B − ΛCDM.
- **R1:** ΛCDM's statistical-only z, and the class it would give. This is reported, not the classification.
- **R2:** B − ΛCDM per B cell (dex), with a paired bootstrap error: the same resamples for both models, statistical only. The floor's zero-point shift moves both α's almost equally and is not added.
- **R3:** the variants, declared here and not tuned. For each: Δ, z, z_stat, outcome and exclusions.
  - V1: Dutton–Macciò c (h48's).
  - V2: Duffy relaxed 200c (6.71, −0.091).
  - V3 / V4: every M_h × ⅓ and × 3.
- **R4:** ΛCDM's α_lens and α_dyn in CFG33's three dispersion bins. Also ΛCDM's dynamics slope d log α_dyn / d log σ_e (the analogue of CFG33's H3, with a bootstrap error) and the lenses' own slope.
- **R5:** diagnostics at the base solution:
  - the median log M_h for the lenses and for the calibration set;
  - the median projected dark fraction inside R_E, (1 − f_b) M_2D/M_E = 1 − α f_*;
  - the median 3D dark fraction inside r_1/2;
  - how many solved stellar masses lie above the Moster grid (M_* > 10^11.97, M_h clamped);
  - how many calibrated galaxies have r_1/2 < 10⁻⁴ R_200 (`make_nfw`'s inner clip active);
  - the exclusions on each side.
- **R6 (main run):** the ΛCDM gate with every M_h × 100, computed in-process. This decides NON-DISCRIMINATING. The shifts in Δ and z are given.
- **R7:** the projected halo with the line of sight saturated at 5 R_200 (`make_nfw`'s outer clip), against the untruncated analytic form, at each lens's R_E and base solution. The maximum relative difference and the maximum |Δκ̄| are given.

## MUTATE

MUTATE=1 multiplies **every ΛCDM halo mass by 100**: base and variants, lenses and ATLAS3D. B's side is not mutated, because CFG33 is exec'd with its own MUTATE off.

**Design:**
- The run **must exit 1**, and its failing set **must differ from the main run's**. C5 guarantees both in every case.
- H1 is then scored on the × 100 halos.
- C6 requires the gate outcome to change.

The README will say whether the control is informative:
- **informative for the headline** only if C6 holds (the outcome changes under × 100);
- if C6 fails, the exit code is informative only about the plumbing (C5).

**Run order:** the main run first, then MUTATE=1. The MUTATE run's C6 does not depend on the order, since both multipliers are computed in-process.

## Readings (declared)

- **SPECIFIC-TO-B** (H1 PASS, the × 100 outcome differs). A standard NFW halo shows no lensing–dynamics gap at > 2σ (with the floor) through CFG33's pipeline.
  - B's statistical gap is then a property of B's law: its projected phantom at R_E is small relative to what the law supplies inside r_1/2. It is not an artefact of the pipeline, of the two surveys' zero points, of the aperture or of the redshift difference.
  - B itself is within 2σ with the floor, so this is a statement about the statistical gap. R1 and R2 say how much of it ΛCDM shares.
- **SHARED** (H1 FAIL, z > +2, the × 100 outcome differs). A standard halo shows the same-sign gap. It is generic to the pipeline and data: the two surveys' zero points, the apertures, the local calibration set against lenses at z ≈ 0.2. B7's residual is then not evidence against B specifically.
- **ΛCDM-WORSE** (H1 FAIL, z < −2, the × 100 outcome differs). In this pipeline a standard halo's lenses need less stellar mass than its dynamics at the same dispersion, at > 2σ. B's gap has the opposite sign; R2 gives the difference.
- **NON-DISCRIMINATING** (the × 100 outcome equals the base outcome). The gate cannot tell the Moster halo from one 100 times heavier, so in this pipeline it carries no information about the dark halo. The three-way reading is reported but not used.
- **UNFIT** (H1a or H1b fails). The declared ΛCDM model cannot be run through the pipeline for most systems; no class.

None of these readings says the data favour either model.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
