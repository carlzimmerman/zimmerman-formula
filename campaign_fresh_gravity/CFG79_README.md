# CFG79 — a ΛCDM comparator for the X-ray ellipticals (CFG32)

## Bottom line

**The declared label is SPECIFIC-TO-B, reached through a weak gate.**

Through CFG32's identical pipeline:
- **A standard ΛCDM halo** (Moster+2013 halo mass, Duffy+2008 concentration, Newtonian) sits at **+0.060 ± 0.123 dex (+0.49σ)**. That is identical on both footings.
- **B's law falls short** by **+0.280 ± 0.165 dex (+1.70σ) canonical** and **+0.254 ± 0.161 dex (+1.58σ) alt**.
- **B minus ΛCDM** is **+0.22 / +0.19 dex**.

B's shortfall is itself only marginal. The label therefore says only that a standard halo stays within 2σ of the hydrostatic masses where B's law falls short at 1.6–1.7σ. So the shortfall is not an artefact of the pipeline, but the label does not make it an established failure: CFG32's reading stands.

Two things weaken the label:
- **The gate has little power over the halo mass.** In the committed rows ΛCDM stays inside 2σ at every halo mass × 0.01, × 1/3, × 1, × 3 and × 33 (the × 33 point is the MUTATE run's V3 row). It fails only at × 100 and × 300.
- **The data are an NFW fit.** CFG32's g_obs is Humphrey's best-fit NFW + stars model, which is ΛCDM's own functional form. ΛCDM's pass is therefore partly built in: its residual is flat, while B's grows outward.

## Files

Script: `CFG79_lcdm_xray_ellipticals.py` (about 5 s).
- Outputs: `.out` and `_results.json`, plus the `_MUTATE` pair.
- The first main run's log is kept as `CFG79_lcdm_xray_ellipticals_first_run.out`.
- The criteria were frozen and committed before any ΛCDM prediction was computed: `CFG79_FROZEN_CRITERIA.md` (commit 6cdfb9d8f).

**Both runs exit 1.** A declared control, C4, failed by a hair in both runs. It is kept as a FAIL and is immaterial (see Controls). This is a comparator: it is neither a model comparison nor a fit.

## Results

| model (CFG32's pipeline) | offset ± σ [dex] | z | class |
|---|---|---|---|
| B, law ν_mono, canonical | +0.280 ± 0.165 | +1.70 | B MARGINAL |
| B, law ν_mono, alt | +0.254 ± 0.161 | +1.58 | B MARGINAL |
| **ΛCDM base** (Moster + Duffy full 200c) | **+0.060 ± 0.123** | **+0.49** | **SPECIFIC-TO-B** |
| V1: Dutton–Macciò c | +0.006 ± 0.124 | +0.05 | SPECIFIC-TO-B |
| V2: Duffy relaxed 200c | +0.028 ± 0.125 | +0.22 | SPECIFIC-TO-B |
| V3: every M_h × 1/3 | +0.150 ± 0.127 | +1.18 | SPECIFIC-TO-B |
| V4: every M_h × 3 | −0.012 ± 0.132 | −0.09 | SPECIFIC-TO-B |

- **ΛCDM's error budget:** galaxy-to-galaxy 0.091, IMF 0.081, radial range 0.018 (recomputed through the ΛCDM pipeline).
- **Floor readings (R4, reported only):**
  - M_h re-derived from the Salpeter M_*: +0.31σ.
  - B's own floor applied to ΛCDM: +0.35σ (canonical) and +0.36σ (alt).
  - CFG32's R1 row for ΛCDM: Salpeter −0.021, Humphrey's fitted M/L +0.113, r ≤ 40 kpc +0.078.

**Per galaxy** (offset in dex, positive = the model falls short; halo masses in log M☉):

| galaxy | B canonical | B alt | ΛCDM | Moster log M_200c / Humphrey log M_vir | Duffy c / Humphrey c |
|---|---|---|---|---|---|
| NGC 720 | +0.572 | +0.539 | +0.494 | 12.47 / 12.82 | 5.7 / 18 |
| NGC 1407 | +0.270 | +0.246 | −0.010 | 14.39 / 13.20 | 3.9 / 18 |
| NGC 4125 | +0.043 | +0.016 | −0.149 | 13.78 / 12.79 | 4.4 / 10 |
| NGC 4261 | +0.034 | +0.009 | −0.162 | 14.19 / 13.83 | 4.1 / 3.7 |
| NGC 4472 | +0.341 | +0.315 | +0.069 | 14.11 / 13.52 | 4.2 / 13 |
| NGC 4649 | +0.551 | +0.525 | +0.263 | 14.15 / 13.54 | 4.1 / 21 |
| NGC 6482 | +0.151 | +0.126 | −0.087 | 14.37 / 12.85 | 4.0 / 18 |

- **B predicts less mass than ΛCDM in every galaxy,** by 0.08–0.29 dex (canonical).
- **ΛCDM is also short in two of B's three worst galaxies:** NGC 720 (+0.49) and NGC 4649 (+0.26). The third, NGC 4472, is +0.07.
- **The Moster halos are heavier than Humphrey's fitted halos in 6 of 7,** by 0.4–1.5 dex. The comparison is Moster's M_200c against Humphrey's M_vir at Δ ≈ 110 times critical, which is the larger mass for the same halo.
- **They are also far less concentrated:** c ≈ 4–6 against 10–21, in 6 of 7. Inside 70 kpc the two differences roughly compensate.
- **NGC 720 is the exception:** it is the one galaxy whose Moster halo is lighter than the fit, and it is where ΛCDM falls short most.
- **The shape differs (R5):** ΛCDM's residual slopes are small (−0.07 to +0.12; 3 of 7 negative), whereas B's are negative in 7 of 7 (CFG32 H2).

## Controls

- **C1 PASS.** CFG32's committed B numbers are reproduced through the exec of its pipeline:
  - at printed precision against its `.out`, with no mismatches;
  - against its JSON, with difference 0;
  - by the generic estimator used for ΛCDM, run with B's law, with difference 0.
- **C2 PASS.** NFW M(<R_200c) = M_h to 2 × 10⁻¹⁶ over 70 halos. The closed form matches the integral of the NFW density to 2 × 10⁻¹⁴, and the profile is monotone.
- **C3 PASS.** With zero halo mass, ΛCDM gives CFG32's g_obs/g_bar exactly. It is bitwise identical on both footings. g_Λ/g_bar ≥ 1.049 everywhere.
- **C4 FAILED (kept, disclosed).**
  - What passed: no M_* lies outside h48's Moster grid, so nothing is clamped.
  - What failed: the round trip `moster_mstar(halo_mass(M_*))` returns M_* to 1.1 × 10⁻⁶, not the declared 10⁻⁶.
  - Why: the tolerance came from a pre-run estimate of h48's interpolation error made at the high-mass end only. At NGC 720's lower mass the relation curves more.
  - The tolerance was not changed.
  - R7, added after the first run and reported only, shows the failure is immaterial. An exact inversion moves M_h by 1.1 × 10⁻⁶ dex and the ΛCDM offset by 6.5 × 10⁻⁸ dex; z and the class are unchanged.

## MUTATE (every M_h × 100) — informative

- **The class changes.** With every halo × 100, ΛCDM sits at −0.285 ± 0.116 (−2.46σ): ΛCDM-WORSE. H1c passes, so the label is not NON-DISCRIMINATING.
- **The failing sets differ.** The MUTATE run fails {C4, H1b, M1}; the main run fails {C4}. That difference is what makes the control informative.
- **The exit codes do not differ.** Both runs exit 1 because C4 fails in both, so the exit code alone carries no information.
- **Run order does not matter.** Both runs compute the × 1 and × 100 classes, so the label does not depend on which runs first.
- **The mirror is weaker (R6, reported only).** Every halo × 0.01 is still inside 2σ (+0.408 ± 0.207, +1.98σ). The gate sees a much heavier halo but only just fails to see a much lighter one.

## Caveats

- **Circularity (form-matching).**
  - CFG32's g_obs is derived from a halo mass: Humphrey's best-fit NFW + stars.
  - The test is not circular in value, because no ΛCDM input comes from that fit.
  - It is form-matched: ΛCDM is scored against data in its own functional form. A ΛCDM pass is partly built in, which the flat ΛCDM residual reflects.
- **Central-galaxy halos.** The frozen caveat was that a Moster halo from the central galaxy's M_* may be smaller than the group halo. That is not what was found in 6 of 7 galaxies: the Moster halos are heavier than Humphrey's fitted halos and less concentrated. NGC 720 matches the caveat.
  - Moster is steep at these masses, so M_h is sensitive to M_*.
  - Nothing was adjusted.
- **Concentration dependence.** Swapping to the Dutton–Macciò or the relaxed Duffy relation moves the offset by 0.03–0.05 dex. All of the declared c and M_h variants stay SPECIFIC-TO-B.
- **Untested.**
  - No adiabatic contraction. Contraction would raise ΛCDM's inner mass and lower its offset; by how much is untested.
  - No scatter in the stellar-to-halo relation. V3 and V4 stand in for it.
- **The IMF mapping.** The base keeps the halo at the Kroupa M_* (CFG69's convention). Re-deriving it from the Salpeter M_* gives +0.31σ.
- **Scope.**
  - Hot gas is omitted on both sides.
  - There are only seven galaxies.
  - The fitted models are extrapolated at 70 kpc for some galaxies.

## Disclosures

- **Before the first run.** C2's monotonicity is sampled over the profile's declared domain, x ∈ [2 × 10⁻⁴, 5] R_200c. CFG69's r-grid would start below its own declared clip at x = 10⁻⁴ for these group-mass halos, where the profile is flat by construction. This was an implementation choice made before any result existed; the frozen text says only "monotone in r".
- **After the first main run, before the MUTATE run.** Two things were added: R7, and a docstring note saying so. No hypothesis, gate, threshold, model choice or classification rule changed. The final main `.out` differs from the first run's log only by that note, R7 and the check count.
- **Other lanes' outputs.** The outputs of CFG35, CFG36 and CFG45 (P6) were not read. Those lanes score B's sum rule on these galaxies, which is a different model.

## Standing

**In CFG32's pipeline a standard halo does not share B's shortfall (SPECIFIC-TO-B).** But the gate is generous: σ ≈ 0.12 dex, and ΛCDM passes for halo masses from × 0.01 to × 33. The data are also in ΛCDM's own functional form. So this is not evidence for or against either model. What decides it is still the deprojected gas density and temperature profiles.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
