# CFG81 — a ΛCDM comparator for CFG34's X-ray groups: FROZEN CRITERIA

Written 2026-09-29 (UTC), **before any CFG81 script exists and before any ΛCDM prediction for these groups has been computed**. This file is committed on its own. Any later deviation goes in the README as a disclosed departure. It follows the repo's control pattern (CFG67, CFG68, CFG69): a standard halo run through exactly the lane's own machinery.

**Known before freezing:**
- **CFG34's committed numbers for B** (README, script and `.out` read in full):
  - R500: M_HSE/M_B = **1.41** (+0.150 dex, **+1.80σ**) canonical; **1.33** (+0.124 dex, **+1.49σ**) alt. H1 PASS.
  - R2500: **1.88** (+0.275 dex, **+2.57σ**) canonical; **1.88** (+0.274 dex, **+2.63σ**) alt. H2 FAIL.
  - Floor terms: group-to-group 0.014–0.017 dex; stellar bracket 0.020–0.070 dex; hydrostatic allowance 0.079 dex. The phantom wins the max in 18/20 and 20/20 groups at R500 (canonical, alt) and in 1/20 and 5/20 at R2500. H3: ρ = −0.958 over 32 systems.
- **h7** (`hunt_2026/h7_groups_hot_gas.py`) was read in full, and the data table `real_research/data/lovisari2015_groups.tsv` was printed in full while reading. All 20 groups' R500, M500, M_gas,500, R2500, M2500 and M_gas,2500 were therefore seen. While the MUTATE was being chosen, five groups' tabulated M2500/M500 were glanced at (0.24–0.49).
- **CFG69** was read at lines 1–180 (the docstring, `exec_prefix`, `c_duffy_full`, `c_duffy_relaxed`, `c_dm`, `make_nfw`, the variant table). CFG68's frozen file was read as a format reference. CFG45 lines 95–130, h48's `halo_mass` / `nfw_enclosed`, CFG7_common's `Report` and CFG4_common's `exec_slices` / `_ro_open` were read.
- **Computations run before freezing** (none of them is a ΛCDM prediction for any group):
  - The critical density the data themselves imply. Per group, ρ̄(<R500)/500 and ρ̄(<R2500)/2500 agree to ≤ 0.8%. Against ρ_c(H₀ = 70, z) the ratio is 0.93–0.99 (median 0.976). Against CFG45's `RHO_C` (H₀ = 67.4, z = 0) it is 1.02–1.085 (median 1.078).
  - Feasibility execs. CFG45's prefix (as CFG69 execs it) gives FB = 0.15713 and RHO_C = 1.2605e11 M☉/Mpc³. CFG34's prefix, exec'd up to its H3 marker, reproduces its committed `RES` exactly (max |d| = 0). Its own in-namespace checks fall as committed: C1, C2 and H1 pass; H2 fails.
- **Hand estimates** (disclosed; neither is the comparator, and nothing below depends on them):
  - The top of h48's Moster grid (log M_h = 15.5) corresponds to a central M_* ≈ 9.3e11 M☉. The lane's total M_*,500 spans ≈ 6.5e11–2.1e12 M☉.
  - While the MUTATE was designed, the generic NFW ratio M(<0.3 R_200)/M(<0.65 R_200) was estimated for c ≈ 4.5 and c ≈ 0.45 (≈ 0.43 and ≈ 0.24). So a concentration × 0.1 should lower the predicted mass inside R2500 by roughly 0.25–0.3 dex.
  - The thresholds and classes are CFG34's and CFG69's. The MUTATE's exit 1 is guaranteed by C5, not by these estimates.

## Question

**Through CFG34's identical pipeline (the same 20 Lovisari+2015 groups, the same radii R2500 and R500, the same statistic — the median over groups of log₁₀(M_HSE / M_model) — and the same floor), does a standard ΛCDM halo show the same shortfall at R2500 and at R500? Is B's R2500 failure SPECIFIC-TO-B, SHARED, LCDM-WORSE, or NON-DISCRIMINATING?**

## The circularity finding (it decides the design)

**The lane's stars are assigned from the hydrostatic halo mass.**
- CFG34 line 109 calls h7's `mstar500(g["M500"])`, where `mstar500(M500) = 1.7e12 (M500 / 1e14)^0.60` M☉ (h7 lines 145–147). This is the Kravtsov, Vikhlinin & Meshcheryakov 2018 relation for the group's TOTAL stellar mass inside R500: BCG + ICL + satellites.
- `M500` is Lovisari's **hydrostatic** mass.
- Inside R2500 the stars are 0.65 M_*,500, the mean of h7's `FIN = (0.50, 0.80)`. The bracket × / ÷ 1.5 scales the normalisation.
- The gas is measured: M_gas at R500 and R2500 comes from Lovisari's double-β density profiles and is not derived from M_HSE. Only the radii themselves are defined by M_HSE.

**So CFG69's base cannot be used here.**
- **It is circular.** M_h = Moster `halo_mass(M_*)` would be a deterministic function of M500_HSE (Kravtsov forward, Moster inverse). Comparing its mass with M_HSE tests only whether two stellar-to-halo relations agree, not ΛCDM.
- **It is also a category mismatch.** Moster+2013 relates a CENTRAL galaxy's stellar mass to its halo, but the lane's M_* is the whole group's. The lane has no central-galaxy mass: Lovisari tabulates none, and h7 imports none. Fed the group total, h48's inversion sits at or near its grid ceiling of 10^15.5 M☉, where `np.interp` clamps, for groups of 2–14 × 10¹³ M☉.
- **The gas cannot supply a non-circular halo mass either.**
  - ΛCDM does not predict a group's baryon fraction without a feedback model.
  - Assuming the cosmic fraction (M = M_b / f_b) is B's own cosmic branch, not a ΛCDM prediction.
  - An M–T or f_gas–M relation would be external data calibrated on hydrostatic masses, and none is in the lane.

**Consequences.**
- **At R500 the lane's data permit no non-circular ΛCDM mass prediction.**
- **What the data do permit is the profile SHAPE.** Given the mass inside R500, ΛCDM's concentration–mass relation predicts the mass inside R2500. That is the design below. It is scored like-for-like with B's R2500 shortfall, which is CFG34's one failure.

## The ΛCDM comparator: the shape design (declared once; no tuning)

**M_Λ(<r) = M_b(<r) + (1 − f_b) · M_NFW(<r; M_h, c(M_h))** — CFG69's base structure. Only the source of M_h changes.

- **Baryons:** the lane's own, identical to B's in CFG34's `run`.
  - At R500: M_gas,500 + M_*,500.
  - At R2500: M_gas,2500 + 0.65 M_*,500.
  - The same stellar bracket applies (× 1.5 and ÷ 1.5).
- **f_b** = FB = Ω_b/Ω_m = 0.02237 / 0.14237 = 0.15713. It is obtained exactly as CFG69 obtains it: the CFG45 prefix up to "P3 SPARC", with `READ = ("L", "S")`.
- **M_h ≡ M_200c is solved per group** (brentq on [1e10, 1e18] M☉, with a sign change asserted) so that **M_Λ(<R500) = M500_HSE at the measured R500**.
  - This replaces CFG69's Moster step, which is circular here.
  - It is the only place the hydrostatic mass enters the ΛCDM side.
  - The halo carries (1 − f_b) of M_h while the group's actual baryons (f_b ≈ 0.08–0.10) are added. The normalisation absorbs the baryons the group has lost.
- **Concentration:** Duffy+2008 FULL-sample Δ = 200c, CFG69's `c_duffy_full` copied verbatim: 5.71 (M_200c / [2e12/h])^−0.084, h = 0.674, the z = 0 row.
  - c is evaluated at the solved M_h, so the solve is self-consistent. C5 verifies it.
- **Profile:** NFW, with m(t) = ln(1+t) − t/(1+t) and M_NFW(<r) = M_h m(c x)/m(c), where x = r / R_200c is clipped to [1e-4, 5].
  - This is CFG69's `make_nfw`, copied verbatim.
  - The lane uses the same code with ρ_c as an argument (`nfw_M`). C2 checks it equal to the verbatim `make_nfw` at ρ_c = RHO_C.
- **How 200c relates to 500c and 2500c (the ρ_c convention).** Every overdensity is taken with respect to ONE critical density per group: the one the data define,
  **ρ_c,g = 3 M500 / (4π · 500 · R500³)**.
  - The measured R500 is then exactly the 500c radius, and the measured R2500 is the 2500c radius of the same ρ_c within rounding (C3).
  - R_200c = (3 M_h / (4π · 200 · ρ_c,g))^{1/3}.
  - The NFW's 500c and 2500c radii solve m(c x)/m(c) = (Δ/200) x³, found by fixed-point iteration, with M_Δ = M_h m(c x_Δ)/m(c). C2 checks this against a direct brentq root solve of the mean enclosed density = Δ ρ_c,g.
  - The Duffy pivot keeps CFG69's h = 0.674 verbatim. The data are in h70 units, and the resulting (0.70/0.674)^0.084 = 1.003 in c is ignored (declared).
- **Prediction and comparison:** M_Λ(<R2500) at the **measured** R2500, against M2500_HSE.
  - This is a fixed-radius comparison, as CFG34 scores B, not a comparison of spherical-overdensity masses.
  - At R500 the comparison is identically 1 (see below).
- **Declared simplifications, untested:**
  - Newtonian throughout (ν = 1).
  - No adiabatic contraction. It would raise the central mass and move ΛCDM's R2500 offset down.
  - No concentration scatter: the mean relation only.
  - The z-dependence of c is ignored. With z ≤ 0.034 that is ≤ 1.6% in c.
- **ΛCDM has no a₀.** It gives one set of numbers for both footings. B keeps both footings: CFG34's numbers, reproduced in C1.

## Statistic and error (CFG34's, as coded; the same floor)

- **Per group:** log₁₀(M_HSE(<r) / M_Λ(<r)) at r = R2500 and r = R500. A positive value means ΛCDM is short, which is B's sign.
- **Median** over the 20 groups.
- **Error terms:**
  - err = std(ddof = 1) / √20;
  - star = ½ |median with stars × 1.5 − median with stars ÷ 1.5|, with the whole chain re-run, the R500 normalisation included;
  - HSE = log₁₀ 1.2 = 0.0792.
- **tot** = √(err² + star² + HSE²), and **z** = median / tot.
- **The same floor as CFG34's**, including the 0.079-dex hydrostatic allowance.
  - For the shape design that allowance is generous to ΛCDM. A hydrostatic bias that is uniform in radius cancels from the R2500 prediction, except through c(M) and the baryon term.
  - The differential and uniform versions are reported as variants V3/V4 and V3u/V4u.
- Printed like CFG34: ratios to 2 decimals, dex to 3, σ to 2.

## At R500 (declared now): NOT A TEST

- The comparator is normalised at R500, so ΛCDM's R500 offset is 0 by construction. C4 verifies it to 1e-9, and H2 records it. It cannot fail, including under the MUTATE.
- B's R500 standing is CFG34's: +1.80σ / +1.49σ. On CFG69's scale that is MARGINAL, and it is a CFG34 pass.
- **The R500 class is "NOT TESTED":** the lane's data contain no non-circular ΛCDM prediction at R500.

## Classes (CFG69's rule, applied at R2500, per footing)

- **B's status per footing:** FAIL if |z_B| > 2; MARGINAL if 1 < |z_B| ≤ 2; OK if |z_B| ≤ 1, in which case there is no class ("B-ok"). CFG34's R2500 is FAIL on both footings (+2.57 / +2.63).
- **For a FAIL or MARGINAL B:**
  - |z_Λ| ≤ 2 → **SPECIFIC-TO-B**;
  - z_Λ with B's sign and |z_Λ| > 2 → **SHARED**;
  - z_Λ with the opposite sign and |z_Λ| > 2 → **LCDM-WORSE**.
- If the two footings give different classes, the row reads **MIXED**.
- **NON-DISCRIMINATING:** applies if the MUTATE (every concentration × 0.1) leaves ΛCDM's R2500 gate outcome (H1 pass/fail) unchanged.
  - It is determined in the main run from row RM, which computes the MUTATE's model internally, and confirmed in the MUTATE run by C6.
  - When it applies, the headline class reads NON-DISCRIMINATING, with CFG69's underlying class printed beside it.
  - **Declared clarification:** if both the main and the mutated gates FAIL, with the mutated offset further from zero in the same direction, the label is still attached, as the rule is written. The README must then say that the gate did respond (the offset moved) and only its pass/fail did not.

## Pre-declared checks

- **C1 CONTROL:** CFG34's committed B numbers are reproduced through a read-only exec of its pipeline.
  - The exec uses CFG69's `exec_prefix` pattern: CFG34's source up to its `H3` banner marker, its own MUTATE forced off, `open` replaced by CFG4's read-only `_ro_open`, and its stdout captured. h7 is reached through it.
  - (i) Every `RES` entry (med, err, star, tot, z, n_phantom_wins, law_med, fb_med) for both footings and both radii equals `CFG34_groups_and_the_ladder_under_b_results.json` to 1e-12.
  - (ii) The four printed "median M_HSE/M_B = …" lines in the captured stdout equal the committed `.out` lines character for character. This is the printed precision.
  - (iii) CFG34's own in-namespace checks fall as committed: C1, C2 and H1 PASS; H2 FAIL.
- **C2 CONTROL:** the NFW engine.
  - (i) M_NFW(<R_200c) = M_h to 1e-12, for M_h = 1e12, 1e13, 1e14 and 1e15 and each of the three concentration relations.
  - (ii) The lane's `nfw_M` at ρ_c = RHO_C equals CFG69's verbatim `make_nfw` to 1e-12 (relative), for 4 masses × 30 radii (1–3000 kpc) × 3 relations.
  - (iii) The 200c → 500c and 2500c conversion (fixed point) equals a direct brentq root solve to 1e-9 in M_Δ and R_Δ. The grid is 7 masses (1e12–1e15) × the three relations, each also × 0.1 (so the MUTATE's regime is covered), at ρ_c = 1.36e11 M☉/Mpc³.
  - (iv) M_NFW(<r) equals a direct numerical integral of the NFW density to 1e-7, for 3 masses × 5 radii.
- **C3 CONTROL (the ρ_c convention):** for every group, the critical density implied by (M500, R500) and by (M2500, R2500) agree to 2%. The tabulated values carry 2–3 significant figures.
- **C4 CONTROL (the normalisation):** in every ΛCDM run, |M_Λ(<R500) / (target) − 1| < 1e-9 for all 20 groups. That covers the base, the stellar-bracket ends, every variant and RM. The target is M500 × the variant's factor.
- **C5 CONTROL (the declared concentration):** for every group in the base run, the c used equals `c_duffy_full(M_h)` at the solved M_h to 1e-12 (relative).
  - **Under the MUTATE it fails by construction.** It is the mutation detector, and it guarantees exit 1.
- **C6 CONTROL (MUTATE run only):** the MUTATE run's base R2500 median and z equal the main run's RM row to 1e-9, read from the main run's `_results.json`. The check fails if that file is absent.
  - The MUTATE run also prints whether its H1 outcome differs from the main run's H1 outcome, read from the same JSON. That is the NON-DISCRIMINATING confirmation.
- **H1 [HEADLINE]:** ΛCDM reproduces the groups inside R2500: **|z_Λ(R2500)| < 2** (CFG34's gate). There is one number for both footings.
  - The MUTATE is expected to fail H1, but this is **not guaranteed**. H1 survives the MUTATE if the main offset lies below about −0.1 dex (hand estimate).
- **H2 (reported, load_bearing = False; NOT A TEST):** ΛCDM at R500, |z_Λ(R500)| < 2. It passes by construction and is recorded so that the R500 row exists.

## Reported rows (they never change H1, H2 or the class)

- **R0 — the circularity diagnostic:**
  - (a) Each group's M_* divided by 1.7e12 (M500_HSE / 1e14)^0.6 equals 1: the stars are the relation evaluated at the hydrostatic mass.
  - (b) CFG45's `halo_mass` evaluated at the lane's M_*: its range, and the number of groups clamped at the grid ceiling 10^15.5.
  - No ΛCDM mass ratio is formed from it.
- **R1 — the class table:**
  - B (CFG34, both footings) beside ΛCDM at R2500 and at R500: the median ratio, dex, the σ components and z;
  - B − ΛCDM in dex;
  - B's status, the class per footing, the combined class and the NON-DISCRIMINATING flag.
- **R2 — the variants.** Each gets the full statistic at R2500 (R500 is set by construction, and its offset is printed).
  - **V1:** Dutton–Macciò c (CFG69's `c_dm`).
  - **V2:** Duffy RELAXED 200c (CFG69's `c_duffy_relaxed`).
  - **V3 / V4:** the R500 normalisation mass × 1.2 / × 0.8, with R2500 still compared with the measured M2500. This is a 20% DIFFERENTIAL hydrostatic bias between the radii, and it replaces CFG69's M_h × 3 and × 1/3 in this design.
  - **V3u / V4u:** both M500 and M2500 × 1.2 / × 0.8: the uniform bias.
  - **V5:** the total mass as ONE NFW, with no separate baryons and no (1 − f_b). Its M_500c = M500_HSE, and it predicts from the concentration alone. Its stellar term is zero.
  - **V6:** CFG45's `RHO_C` (H₀ = 67.4, z = 0) in CFG69's verbatim `make_nfw` instead of ρ_c,g: the ρ_c convention.
- **R3 — B's shape-only offset:** per group, log(M_HSE/M_B) at R2500 minus the same at R500, using CFG34's own per-group ratios.
  - Reported with its median, err, star (half the bracket spread of the median difference), the 0.079 allowance and z, on both footings.
  - It is the like-for-like shape comparison beside ΛCDM's R2500 offset, whose R500 offset is zero.
- **RM — the MUTATE's model inside the main run:** the base with every concentration × 0.1. Its R2500 median, z and gate outcome set the NON-DISCRIMINATING flag.
- **R4 — the per-group table:** name, M500, R2500/R500, ρ_c,g/RHO_C, M_h, c, M_Λ(<R2500), log(M_HSE/M_Λ) at R2500, and B's log(M_HSE/M_B) at R2500 on both footings.
- **R5 — the concentration each group's own profile implies:** the c for which a single total-mass NFW with M_500c = M500 (ρ_c,g) has M(<R2500)/M500 = M2500/M500. The search runs over c ∈ [0.3, 60], and groups without a solution are counted. It is set against `c_duffy_full` at the same M_200c, with the medians of both.

## MUTATE

**MUTATE=1: every ΛCDM concentration × 0.1.** It is applied inside the lane's concentration wrapper, so it covers the base, every variant, the stellar-bracket runs and V6. B is not mutated: CFG34 is exec'd with its own MUTATE off.

- **Expected effect:** a less concentrated halo puts less mass inside R2500, so ΛCDM's R2500 offset rises by about 0.25–0.3 dex (hand estimate). H1 is expected to fail, but it is not guaranteed to.
- **Exit 1 is guaranteed by C5,** which fails by construction. So the MUTATE's failing set always contains C5, and the main run's cannot (unless the engine is wrong, which would be a disclosed control failure). **The failing sets therefore differ.**
- **The MUTATE is INFORMATIVE about the gate if and only if H1's outcome flips between the two runs.** If it does not flip, the class carries NON-DISCRIMINATING, and the README says so.

## Outputs

- The script `CFG81_lcdm_xray_groups.py` is written after this file is committed.
- It uses CFG7_common's `Report`: `.out` and `_results.json`, plus the `_MUTATE` pair. It ends with `sys.exit(1 if failures else 0)`.

## Reading (declared)

- **H1 PASS (B FAIL at R2500) → SPECIFIC-TO-B.** Through the same groups, radii, statistic and floor, a standard NFW normalised at R500 reproduces the mass inside R2500, where B is 1.88× short (2.6σ).
  - B's R2500 shortfall is then B's own, not a feature of the data that any halo shares. That is CFG34's reading: a cosmic share tied to today's baryons.
  - It becomes NON-DISCRIMINATING if the concentration × 0.1 halo passes as well. The gate then cannot tell a standard concentration from a tenfold-lower one.
- **H1 FAIL with z_Λ > 0 → SHARED.** A standard ΛCDM halo is also short inside R2500: the groups' hydrostatic mass is more centrally concentrated than an NFW with Duffy's c plus the observed baryons.
  - The suspects are the shared inputs and physics both models omit: adiabatic contraction, cool-core or relaxed selection, a hydrostatic bias that varies with radius, and the imported stellar mass.
  - B's R2500 failure then does not single out B. R3 and R5 give the sizes.
- **H1 FAIL with z_Λ < 0 → LCDM-WORSE.** ΛCDM over-predicts the mass inside R2500 where B under-predicts. The data lie between the two models.
- **At R500: NOT TESTED** (declared above).
- **Variants:** if any of V1–V6, V3u or V4u gives a different class from the base, the standing line says the class depends on that choice. The declared class does not change.
- Nothing here says the data favour B or ΛCDM.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
