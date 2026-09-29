# CFG79 — a ΛCDM comparator for the X-ray ellipticals (CFG32): FROZEN CRITERIA

Written 2026-09-29, **before any CFG79 script exists and before any ΛCDM prediction for these seven galaxies has been computed**. This file is committed on its own, before any scoring. It follows CFG69's comparator pattern (a standard halo run through a lane's identical pipeline) and CFG67's order (freeze, then score).

## Question

CFG32 scored candidate B's law on seven X-ray-bright ellipticals (Humphrey+2006, ApJ 646, 899: NGC 720, 1407, 4125, 4261, 4472, 4649, 6482). B falls short of the hydrostatic masses:
- by +0.280 / +0.254 dex (a factor 1.91 / 1.79, canonical / alt);
- at 1.70 / 1.58σ;
- with the shortfall growing outward in 7 of 7.

**Run through CFG32's identical pipeline (same data, same statistic, same error model and floors), does a standard ΛCDM halo also fall short?** Is B's shortfall SPECIFIC-TO-B, SHARED, ΛCDM-WORSE, or NON-DISCRIMINATING?

## Identical to CFG32

CFG32 is executed read-only from `CFG32_xray_ellipticals_under_b.py`, with its MUTATE forced off.

- **Data and g_obs:** h10's Humphrey+2006 table and its fitted model, exactly as CFG32 uses them:
  - g_obs(r) = G [M_Hern(r; Υ_fit L_K) + M_NFW(r; M_vir − Υ_fit L_K, R_vir, c)] / r²;
  - Hernquist stars with a = R_e / 1.8153.
- **Baryons:** CFG32's, unchanged. Stars only, Hernquist, at the Kroupa population M/L (Υ_K L_K). There is no hot gas: CFG32 has none, and the repository has no gas profiles.
- **Radii:** 5, 10, 20, 40, 70 kpc.
- **Statistic:**
  - A point's offset is log10(g_obs / g_model). Positive means the model falls short.
  - A galaxy's offset is the median over its five radii.
  - The sample offset is the mean of the seven galaxies.
- **Error model:** the galaxy-to-galaxy error std(ddof = 1) / √7, plus a floor in quadrature.
  - IMF term: |offset with Salpeter stars (Humphrey's Υ_S) − offset with Kroupa stars|.
  - Radial term: |offset over r ≤ 40 kpc − offset over all five radii|.
  - floor = √(IMF² + radial²); σ = √(err² + floor²); z = offset / σ.
  - For ΛCDM the floor is recomputed by the same method, through the ΛCDM pipeline. CFG69 did the same when it recomputed each lane's floors for its halo.
  - B's committed floor values (IMF 0.126, radial 0.065, floor 0.142, canonical) are applied to ΛCDM only as a reported row (R4b).
- **B:** CFG32's own numbers, computed by CFG32's own code inside the exec: ν_mono, no external field, both footings. κ = ½ is fitted.

## The ΛCDM model (declared once; no tuning)

- **Acceleration:** g_Λ(r) = G [M_Hern(r; Υ_K L_K) + (1 − f_b) M_NFW(<r)] / r².
  - Newtonian (ν = 1).
  - The galaxy's own stars (CFG32's baryons) plus a dark halo.
- **Halo mass:** M_h is the Moster+2013 stellar-to-halo relation `halo_mass` (h48's), evaluated at M_* = Υ_K L_K.
  - `halo_mass`, `FB` (f_b = Ω_b/Ω_m, from CFG35) and `RHO_C` are obtained exactly as CFG69 obtains them.
  - That is: its `exec_prefix` of `CFG45_rule_readings.py` up to the "P3 SPARC" marker, with the same READ replacement.
- **Concentration:** Duffy+2008 full sample, 200c: c = 5.71 (M_h / [2×10¹² / h])^−0.084, with h = 0.674 and z = 0.
- **Profile:** `c_duffy_full`, `c_duffy_relaxed`, `c_dm` and `make_nfw` are copied verbatim from CFG69.
  - m(t) = ln(1+t) − t/(1+t).
  - R_200c = (3 M_h / (4π · 200 ρ_c))^(1/3).
  - x = r / R_200c, clipped to [10⁻⁴, 5].
  - M_NFW(<r) = M_h m(cx) / m(c): normalised to M_h at R_200c.
- **Declared untested:** no adiabatic contraction and no scatter in the stellar-to-halo relation.
- **Footings:** ΛCDM has no a₀, so its numbers are identical on both footings. B keeps both: canonical 9.36 × 10⁻¹¹ and alt 1.13 × 10⁻¹⁰ m s⁻².
- **The IMF floor for ΛCDM:** the Salpeter row changes only the stars, and the halo stays at the Moster M_h of the Kroupa M_*.
  - This is CFG69's convention: its Υ floors vary the baryons, with the halo tied to the declared stellar mass.
  - Keeping it is also consistent: the SHMR is calibrated on a Chabrier/Kroupa-type population mass.
  - The other mapping, with M_h re-derived from the Salpeter M_*, is a reported row (R4a).

## Circularity, stated plainly

**CFG32's g_obs is derived from a halo mass.** It is Humphrey's best-fit NFW + stars model (their M_vir, R_vir, c and fitted M/L), not the deprojected data.

- **Not circular in value.** No ΛCDM input is taken from that fit. M_h comes from Moster at a stellar-population M_* (Υ_K L_K, which is not derived from any halo mass), and c comes from Duffy.
- **But form-matched.** ΛCDM is scored against data expressed in ΛCDM's own functional form (NFW + stars).
  - ΛCDM's radial shape therefore matches the data's by construction. B's does not.
  - The test reduces to one question: does a Moster/Duffy halo match Humphrey's fitted halo at 5–70 kpc?
  - A ΛCDM pass is partly built in; a ΛCDM failure is not.
- **Different mass definition.** Humphrey's M_vir uses their virial overdensity, not 200c. It is printed beside M_h for context (R2) and enters no score.

## Caveat, stated

- **Central-galaxy halos.** These are group- or cluster-central ellipticals (e.g. NGC 4472, 4649, 720; NGC 4472 and 4649 are Virgo members), so a Moster halo from the central galaxy's M_* may be smaller than the group halo.
- **A steep relation.** The Moster relation is steep at these masses, so M_h is sensitive to M_*.
- **Not fixed.** This is stated, not fixed: no halo mass is adjusted.
- **Other lanes on these galaxies.** CFG35, CFG36 and CFG45 (P6) score B's sum rule on these galaxies: the law plus a collapse-mass NFW, a different model. Their outputs were not read before this file was written.

## Classes (CFG69's rule)

B's status on each footing:
- FAIL if |z_B| > 2;
- MARGINAL if 1 < |z_B| ≤ 2;
- OK if |z_B| ≤ 1 (then "B-ok", and no class is given).

CFG32 committed MARGINAL on both footings, with a positive sign.

For a FAIL or MARGINAL B:
- **SPECIFIC-TO-B:** |z_Λ| ≤ 2.
- **SHARED:** z_Λ has B's sign and |z_Λ| > 2.
- **ΛCDM-WORSE:** z_Λ has the opposite sign and |z_Λ| > 2.
- If the two footings give different classes, the row reads MIXED.

**NON-DISCRIMINATING:** the gate cannot see the halo. With every M_h × 100 (the MUTATE), ΛCDM's class is unchanged.
- The "gate outcome" is the three-way class, not only pass/fail: a move from SHARED to ΛCDM-WORSE counts as a change.
- NON-DISCRIMINATING overrides the base class. The base class is still printed.
- If the base class is ΛCDM-WORSE, × 100 moves ΛCDM further in the same direction and cannot change the class. The label is then NON-DISCRIMINATING by the rule as written. The mirror (× 1/100, R6) is reported only and does not change the label.

## Pre-declared checks

### Controls (load-bearing in both runs)

- **C1 CONTROL:** CFG32's committed B numbers are reproduced through the exec of its pipeline, on both footings.
  - (a) At its printed precision, as strings against its committed `.out`: the per-galaxy Kroupa offsets; the mean, galaxy-to-galaxy error, floor, and IMF and radial terms; z; the factor; and the Salpeter, fitted-M/L, r ≤ 40 kpc and P2 means.
  - (b) To 1e-9 against its committed JSON.
  - (c) The generic estimator used for ΛCDM, run with B's law, reproduces the exec'd numbers to 1e-12.
- **C2 CONTROL:** the NFW profile.
  - For every halo used (base, V1–V4 and the R6 ladder), the NFW enclosed mass at R_200c equals M_h to 1e-12.
  - Analytic check: `make_nfw` equals the numerical integral of the NFW density to 1e-7 at the five radii, for every base, V1 and V2 halo, and it is monotone in r.
- **C3 CONTROL:** the limits of the ΛCDM engine.
  - With M_h → 0, ΛCDM's per-point ratio equals CFG32's g_obs / g_bar (Newtonian, stars only) to 1e-12.
  - ΛCDM's numbers are identical whether the call carries the canonical or the alt a₀.
  - The halo only adds mass: g_Λ ≥ g_bar at every point.
- **C4 CONTROL:** every M_* fed to `halo_mass` (Kroupa, plus Salpeter and fitted for R4) lies inside h48's Moster grid, so nothing is clamped. `moster_mstar(halo_mass(M_*))` returns M_* to 1e-6.

### Headline H1: the classification on the base model, as pass/fail lines

- **H1a [HEADLINE] NOT SHARED:** ΛCDM (base) is not off in B's direction at more than 2σ.
- **H1b [HEADLINE] NOT ΛCDM-WORSE:** ΛCDM (base) is not off in the opposite direction at more than 2σ.
- H1a and H1b both pass exactly when the class is SPECIFIC-TO-B.
- **H1c [HEADLINE; the NON-DISCRIMINATING test] THE GATE SEES THE HALO:** ΛCDM's class with every declared M_h × 100 differs from its class with the declared M_h.
  - Both classes are computed in every run, so the label does not depend on the order the runs are made in (CFG69's run-order lesson).
- **M1 [MUTATE detector] THE SCORED CLASS IS THE DECLARED CLASS:** the class on the halos scored in H1a/H1b equals the class on the declared halos.
  - In the main run it passes by construction.
  - Under MUTATE it fails exactly when H1c passes.
- **H1 (reported):** the final label, per footing and combined, with B − ΛCDM in dex.

### Reported rows (never enter a class)

- **R1:** per galaxy, B's offsets (both footings) and ΛCDM's (base), with ΛCDM's five per-radius values; B − ΛCDM on the sample means.
- **R2:** the halo of each galaxy (M_*, M_h, c, R_200c), beside Humphrey's fitted M_vir, R_vir and c and the overdensity they imply. Context only.
- **R3:** the variants.
  - V1: Dutton–Macciò c (CFG69's `c_dm`).
  - V2: Duffy relaxed 200c (6.71, −0.091).
  - V3 / V4: every M_h × 1/3 and × 3.
  - Each runs through the identical pipeline with its own recomputed floor, and reports offset, σ, z and class.
- **R4:** the floor readings.
  - (a) The IMF term with M_h re-derived from the Salpeter M_*.
  - (b) B's committed floor on each footing, combined with ΛCDM's galaxy-to-galaxy error.
  - (c) CFG32's R1 row for ΛCDM: Salpeter; Humphrey's fitted M/L, with the halo from the Kroupa M_*; r ≤ 40 kpc.
- **R5:** ΛCDM's residual shape. The slope of log(g_obs / g_Λ) against log g_bar for each galaxy (CFG32's H2 statistic), and how many are negative.
- **R6:** the halo ladder. Every declared M_h × 1/100, × 1 and × 100, with offset, σ, z and class, computed in every run.

## MUTATE

**MUTATE=1** multiplies every ΛCDM M_h by 100 (base and V1–V4). B is untouched. The R6 ladder and the H1c comparison stay relative to the declared halos.

In the MUTATE run, H1a and H1b are scored on the × 100 halos, H1c is the same comparison as in the main run, and M1 fails exactly when the class changed. So:
- **The MUTATE run always exits 1:** either H1c or M1 fails.
- **Its failing set differs from the main run's exactly when H1c passes.** M1 then fails under MUTATE and never fails in the main run.
- **If H1c fails, the control is uninformative.** Both runs then fail the same set of checks, H1c included, and the label is NON-DISCRIMINATING.
- The README states which case occurred.

## Readings (declared)

- **SPECIFIC-TO-B** (H1a, H1b and H1c pass):
  - A standard Moster/Duffy halo, run through CFG32's identical pipeline, stays within 2σ of the hydrostatic masses while B's law falls short.
  - B's shortfall is itself only marginal (CFG32's H1 still fails at 2σ). The label says ΛCDM is inside 2σ; it does not make B's shortfall a failure.
  - It does say the shortfall is not an artefact of the pipeline.
  - A ΛCDM pass is partly form-matched (see Circularity).
- **SHARED** (H1a fails, H1c passes):
  - The standard halo also falls short at more than 2σ, so B's shortfall is not specific to B.
  - It is, at least in part, a property of the data or the pipeline: Humphrey's fitted halos hold more mass at 5–70 kpc than a Moster/Duffy halo of the central galaxy's M_*.
  - The candidate reasons (group halos, concentration, adiabatic contraction, hot gas) are named, not fitted.
- **ΛCDM-WORSE** (H1b fails, H1c passes): the standard halo over-predicts at more than 2σ, the opposite of B.
- **NON-DISCRIMINATING** (H1c fails): M_h × 100 leaves the class unchanged. The gate cannot see the halo here, so the base class says nothing about ΛCDM.
- **Either way:**
  - CFG32's reading stands as run: B's shortfall is not an established failure.
  - The definitive test needs the deprojected gas density and temperature profiles.
  - Nothing here says the data favour either model.

## Process

- A failed declared control is kept as a FAIL and disclosed.
- No criterion is changed after a result is seen.
- Anything added after the first run is a disclosed, reported-only row.
- Outputs: `CFG79_lcdm_xray_ellipticals.out` and `_results.json`, and the `_MUTATE` pair. The README is `CFG79_README.md`.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
