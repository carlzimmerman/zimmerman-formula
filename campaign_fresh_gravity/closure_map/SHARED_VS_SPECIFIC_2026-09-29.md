<!-- A NEW documentary file. No new physics: every entry is read from a committed output and cites its lane and commit. -->
# Candidate B's failures: specific to B, shared with standard halos, or not discriminating?

**Scope.** Every row that `GATES_STATUS_2026-09-29.md` marks FAIL, MARGINAL or OPEN for candidate B (the law T1–T6 with FG001 ownership), plus the new KiDS colour-split failure. UNDECIDED and not-scored rows are left out. Each row asks one question: when a standard ΛCDM halo is run through the *same* data, estimator and error model, does it fail too?

**Classes.**
- **B-SPECIFIC:** ΛCDM passes in the same machinery where B fails.
- **SHARED:** ΛCDM fails in the same machinery with the same sign.
- **NON-DISCRIMINATING:** the machinery cannot make ΛCDM fail, or its spread for standard halos exceeds B's cost.
- **ΛCDM-WORSE:** ΛCDM fails with the opposite sign.
- **NOT COMPARED:** no ΛCDM run exists in the same machinery.
- **STRUCTURAL:** a property of the theory, not a data comparison.

A class describes the machinery, not the universe. Nothing here says the data favour either model. κ = ½ and Ω_c h² stay fitted, and nothing here says the theory is closed.

**Re-run status.**
- "Independent" means a re-derivation from separately written code.
- "Re-run" means the committed script was re-run and its output matched.
- **"NOT RE-RUN this round"** means the row is carried from `GATES.md` and nobody has re-run it since the freeze.

## Bottom line

- **Only one observational failure is cleanly B-specific in shared machinery: the KiDS early/late lensing split.** It holds for the *difference* between the two classes. In the same machinery ΛCDM's absolute profiles fail too.
- **Two are shared with standard halos:** the super spirals, and the Local Group / KiDS edge.
- **SLUGGS is mixed.**
  - It is B-specific under JAM calibration, but ΛCDM's pass there is largely built in by the calibration.
  - With population masses ΛCDM does worse than B.
  - All of it sits at a fixed GC density slope, γ = 3.
- **Two rows cannot discriminate in this machinery:**
  - the ultra-faints (ΛCDM's pass is nearly automatic, although B's law still fails on its own terms);
  - the budget against KiDS.
- **The rule's satellite failures depend on the concentration relation.** They are B-specific under Duffy and shared under Dutton–Macciò.
- **Four rows were never run against ΛCDM:** Chae's external-field signal, the X-ray ellipticals, SLACS and the X-ray groups.
- **The structural gaps are B's alone:** no action produces B.

## Rows

| Gate | B's failure | ΛCDM in the same machinery | Class | Lanes (commits) | Re-run |
|---|---|---|---|---|---|
| next to 3.05 | **KiDS early/late split:** χ² 28.1/7 (p = 2.1e-4, ~3.7σ) on the difference; the rule adds nothing at KiDS masses | colour-split halos 6.5/7; colour-blind Moster 6.9/7 | **B-SPECIFIC** (the difference) | CFG61 (3c03f9678; criteria d7aecf12b), CFG67 (f1df7889a) | re-run in place by the equations session and by the referee sweep (byte-identical) |
| 1.25 | **super spirals:** the nine fastest +0.164 dex (2.34σ); all 23 +0.105 (1.67σ) | Mandelbaum blue halos: the nine fastest +0.121 (z = 2.26) | **SHARED** | CFG40 (e773982cd; referee 071301aab), CFG56 (33e1af197), CFG68 (358564486; criteria 1808d8bee) | CFG56 re-run; CFG68 re-run by this session and the referee sweep |
| 2.04, 3.08 | **Local Group R₀** 3.0–4.8σ high; **one shared KiDS + LG edge** excluded at 5–7σ | every standard-halo variant has a KiDS–LG tension T = 24.5–72.5 (baseline 55.4) against B's 26–28; the KiDS side of FG016's kill is shared too | **SHARED** | CFG20 (a353f975f), CFG21 (d7093c210), CFG22 (132cba668), CFG23 (27a43a743), CFG25 (1f51ee1e3) | **NOT RE-RUN this round** |
| 1.20 | **SLUGGS GCs:** with JAM masses the law is +0.097 (4.0σ) and the rule +0.046 (2.6σ); with the h50 key fixed (17 galaxies) law +0.0996 (4.3σ), rule +0.0513 (2.9σ) | JAM row: +0.001 (0.0σ), largely by construction; population masses: −0.048 (−2.4σ; −4.1σ under Dutton–Macciò) | **mixed:** B-SPECIFIC (JAM), **ΛCDM-WORSE** (population masses) | CFG55 (791083f7f), CFG55 key-fix and corrections (4612c753a), CFG57 (9b071a024; data d409c19be), CFG69 (688c8f692), CFG76 (276c78784) | CFG55: independent (CFG76, exact) and re-run; **CFG57: this session only**; CFG69: its own lane |
| 1.09 | **MW ultra-faints:** law +0.325 (3.8σ; alt 3.5σ); binary-cleaned Boötes I +0.22 (2.5σ), Tucana II +0.47 (3.6σ) | +0.080 (0.6σ), but the gate passes for halo masses × 0.1 to × 100 | **NON-DISCRIMINATING** for ΛCDM; B's law fails on its own terms | CFG42 (67c170fe7), CFG46 (e6ecfd6ff), CFG51 (d7e6a6565), CFG66 (f385657c6), CFG69, CFG73 (815f635d3), CFG74 (72869a8aa), CFG78 (9e7f778bc) | CFG42/46/51 re-run; CFG69's numbers independent (CFG73, to 3 decimals); CFG46 independent (CFG78); **CFG66, CFG74: their own lanes only** |
| 3.07 | **budget against KiDS:** cost 29.4–49.3 | the same machinery's spread for standard halos S = 50.2 (B's cost is 0.59–0.98 of S) | **NON-DISCRIMINATING** | CFG24 (bf27d136c), CFG25, CFG27 (5aa9ad508) | **NOT RE-RUN this round** |
| 1.08 | **M31 LVD under the rule:** −2.67σ (the law is marginal, 1.2–1.6σ) | Duffy: −1.3σ; Dutton–Macciò: −2.2σ | **convention-dependent:** B-SPECIFIC (Duffy), SHARED (Dutton–Macciò) | CFG42, CFG45 (5518cfcd0), CFG69 | CFG42/45 re-run |
| 1.10 | **LV field dwarfs under the rule:** −3.47σ (alt −2.70σ) | Duffy: −0.5σ; Dutton–Macciò: −2.6σ | **convention-dependent:** as 1.08 | CFG58 (3371b14ac), CFG69 | CFG58 re-run |
| 1.15 | **Chae's external-field signal:** refit 1.7–3.0σ (FG001's cost) | none run | **NOT COMPARED** | CFG8 (302ff4bd9) | **NOT RE-RUN this round** |
| 1.18 | **X-ray ellipticals:** +0.280 dex (a factor 1.9) at 1.70σ (alt 1.58σ), growing outward | none run | **NOT COMPARED** | CFG32 (7dfe4a84b) | **NOT RE-RUN this round** |
| 1.19 | **SLACS lensing against dynamics:** a +0.15–0.17 dex gap; 1.5–1.7σ with the floor, 7–8σ statistically | none run | **NOT COMPARED** | CFG33 (682bed1b3) | **NOT RE-RUN this round** |
| 2.03 | **X-ray groups inside R2500:** 1.88× short (2.6σ); the shortfall tracks the baryon fraction (ρ = −0.96) | none run | **NOT COMPARED** | CFG34 (ac0d32b96) | **NOT RE-RUN this round** |
| 3.06 | **cold budget, strict reading** | ΛCDM fits Ω_c directly | **no ΛCDM counterpart** | CFG4_target, CFG39 (de70b7e7f) | **NOT RE-RUN this round** |
| 5.01, 5.02, 5.11 | **no action produces B;** the V0 region gate is unstable when varied; the dark mass is not yet a state of the field | ΛCDM has an explicit action (GR, a pressureless fluid, Λ) | **STRUCTURAL** (B's alone) | CFG43 (e42a98572), CFG44 (513ee4b28), CFG48 (0dba13349; referee 35eebbe99), CFG50 (bb2a7b680) | re-run; CFG48 G6 referee-reproduced |

## Caveats, row by row

**KiDS split.**
- What is B-specific is the early-minus-late difference. The same machinery's absolute profiles fail for ΛCDM too: early 29.6/7 and late 27.9/7, and 45.8/15 over all 15 bins (p = 5.7e-5).
- The 3.7σ is a χ² row reported after the first run; the frozen amplitude statistic was degenerate.
- The Sérsic replicate gives 2.9σ.
- A colour-blind dark mass survives if early-type lenses hold at least about 0.25–0.5 × their stellar plus cold mass in extra baryons (p > 0.0027 / 0.05). This is untested.

**Super spirals.**
- The verdict depends on the halo relation (Moster over-predicts) and on the lensing error at these masses: the +1σ halos pass.
- The stellar-mass floor (0.2 dex) is the limit.

**Local Group and edge.**
- The shared quantity is the KiDS–LG tension. CFG23 names the LG's spherical R₀ as the weak link.
- Duffy-c halos miss KiDS itself (χ² 173.7), and a ×0.7 concentration reaches 99.3. So KiDS does not prefer B either.

**SLUGGS.**
- Every number is at a fixed GC density slope, γ = 3. The law's offset is zero at γ ≈ 1.83 and the rule's at γ ≈ 2.45 (CFG76, post hoc).
- It leans on the group and cluster centrals: without M87, NGC 4365, NGC 4374 and NGC 5846, the law is at 2.7σ and the rule at 1.3σ.
- h50's name key had dropped NGC 720 and NGC 821. With the key corrected, the JAM sample of 17 gives the 4.3σ and 2.9σ quoted in the table.
- The measured hot gas is too small to matter (CFG57, non-diagnostic). M87's gas beyond 30 kpc is untested.
- The ΛCDM comparator has no adiabatic contraction and no SHMR scatter. Scaling its halos by 3 or 1/3 moves the JAM row to ∓2.5σ.
- ΛCDM at other γ was not run.

**Ultra-faints.**
- The ×0.1–×100 window is specific to Duffy's full concentration. Every concentration gives a window of 3.5–5 decades.
- Only an assumed cored Burkert halo discriminates (CFG74).
- The rule closes the ultra-faints (−0.06, −0.4σ) but fails the satellites (rows 1.08, 1.10).
- CFG78 flags two open points: the quadrature double-counts measurement scatter, and the offsets are luminosity-ordered (untested).

**Satellites under the rule.**
- CFG69's comparator floats a collapse-mass floor.
- Under Dutton–Macciò, both rows become SHARED for the rule.

**Rows with no ΛCDM comparison.**
- These classes are open, not favourable to either model.

## Not re-run by anyone this round

CFG8, CFG20–CFG25, CFG27, CFG32, CFG33, CFG34 and CFG39 are carried from `GATES.md`. CFG57, CFG66 and CFG74 have been run only by their own lanes.


## Addendum after CFG77 (appended 2026-09-29; the rows above are unchanged)

- **The KiDS row is B-specific for the early-minus-late difference only, and that result is fragile** (CFG77, a736715f8, an independent re-derivation that reproduces CFG61 and CFG67 exactly).
  - The law's χ² is the zero-model χ²: 28.085 against 28.074. So the split fails **every** colour-blind model equally and does not discriminate among them.
  - The released covariance is essentially diagonal and carries no systematic terms. Errors × 1.5 give 12.5/7 (p = 0.086). Dropping bin 11 or bin 12 leaves about 20/6.
  - ΛCDM's pass depends on the stellar-mass calibration (5.45–11.50/7). The law's χ² does not (a change of at most 0.03).
  - The bottom line's "only one observational failure is cleanly B-specific" should read: **the one observational failure specific to B in shared machinery is the KiDS early/late split. It is a failure of any colour-blind dark mass, at face value of a covariance without systematic terms.**
- **Re-run status of the KiDS row:** CFG61 and CFG67 have now also been independently re-derived (CFG77).


## Addendum after CFG79, CFG80 and CFG81, the ΛCDM comparators for the "NOT COMPARED" rows (appended 2026-09-29; the rows above are unchanged)

Each lane ran CFG69's base halo (Moster+2013 halo mass, Duffy+2008 full 200c concentration, (1 − f_b) NFW, Newtonian, no contraction, no scatter) through its source lane's own pipeline. Criteria were frozen before any ΛCDM number.

| Gate | B | ΛCDM, same pipeline | Class, after the independent re-derivations | Lanes (commits) | Re-run |
|---|---|---|---|---|---|
| 1.18 X-ray ellipticals | +0.280 dex (1.70σ; alt 1.58σ), marginal | +0.060 ± 0.123 (+0.49σ) | **COMPATIBILITY CHECK only, not a test of ΛCDM or of B** | CFG79 (criteria 6cdfb9d8f; lane b3141df7b; corrections c690392c1) | independent: CFG84 (68d166cea) |
| 1.19 SLACS, lensing against dynamics | gap +0.15–0.17 dex: 1.5–1.7σ with the floor, 7–8σ statistically | gap +0.037: +0.36σ with the floor, +1.5σ statistically | **SPECIFIC-TO-B for the statistical gap only;** both models pass with the floor | CFG80 (criteria fe0c1c040; lane 1af8de3ce) | **this lane only so far** |
| 2.03 X-ray groups | R2500: 1.88 (2.57σ; alt 2.63σ). Shape only, on equal footing: 1.37σ (alt 1.79σ) | R2500 shape test: 1.05 (+0.25σ). R500: normalised there, NOT TESTED | **NOT SEPARATED at 2σ on equal footing** (shape only); the halo-mass test is circular | CFG81 (criteria 27b4bf414; lane 698c35a33; corrections 5ab0919e4) | independent: CFG85 (8115c1189) |
| 1.15 Chae external field | refit 1.7–3.0σ | **ΛCDM has no external-field effect, so there is nothing to compare in this machinery** | **no ΛCDM counterpart** | CFG8 (302ff4bd9) | NOT RE-RUN this round |

**Caveats.**

- **X-ray ellipticals.** CFG32's "observed" masses are Humphrey's best-fit NFW + stars models, which are ΛCDM's own functional form. Humphrey's own fitted halo scores −0.031.
  - The Moster/Duffy pass is a cancellation: the halos are 0.4–1.5 dex too heavy, and the concentrations 0.2–0.4× too low in 6 of 7 galaxies.
  - With Moster's masses and Humphrey's concentrations, ΛCDM is at −2.58σ.
  - The gate passes at every halo mass from × 0.007 to × 60.8, about 3.9 dex.
- **SLACS.**
  - The gate sees the halo only weakly: halo mass × 100 fails at −2.61σ, while × 33 passes.
  - Moster's relation tied to α × Salpeter masses gives group- to cluster-scale halos, median 10^14.4 M☉. With every halo × 1/3, ΛCDM keeps about half of B's statistical gap (3.4σ).
  - The halos are defined at z = 0, while the lenses sit at a median z of 0.19.
- **Groups.** CFG34's stars are assigned from the hydrostatic M500, so a Moster halo would be circular. The frozen shape design hands ΛCDM each group's M500 and does not hand it to B.
  - ΛCDM's R2500 offset does not depend on the stellar level (+0.005 to +0.027 dex).
  - B's does. With +0.2 dex in stars, B is at 1.45σ; B closes at about 3.2× the Kravtsov relation (CFG85).

**Bottom line of this addendum.** None of the three comparators adds a clean B-specific failure.
- **The X-ray ellipticals** are a compatibility check.
- **SLACS** separates B from ΛCDM only statistically, where the 0.10-dex floor is not applied. With the floor, both pass.
- **The groups' shape test** does not separate them at 2σ.

The KiDS early/late split, B-specific for the difference only and fragile, remains the one B-specific observational failure in shared machinery. κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model or that the theory is closed.


## Addendum after CFG86 (appended 2026-09-29; the rows above are unchanged)

- **Row 1.19, SLACS.** "SPECIFIC-TO-B for the statistical gap only" is replaced by **B minus ΛCDM ≈ 0.12 dex, conditional on the halo and zero-point conventions. Both models pass with the floor.**
  - CFG86 (4d994bb28) independently re-derived ΛCDM's side exactly. B's side was not re-derived, so its B-minus-ΛCDM test is unpaired.
  - Over 54 declared convention cells, ΛCDM's statistical gap is inside 2σ in only 52%. B minus ΛCDM has a median of +0.118 dex (+0.023 to +0.266) and is never negative.
  - Lighter halos, a Chabrier-equivalent tie, a zero-point offset below −0.012 dex, or redshift-consistent halos (−0.020) each change ΛCDM's statistical verdict.
  - It is a difference between the models, not a failure of either.


## Addendum after CFG88 (appended 2026-09-29; the rows above are unchanged)

- **The KiDS row's fragility is partly answered.** CFG88 (ef7c1d303) scored the split in the seven 1-halo bins with a data-driven covariance.
  - **Data:** the repo's own KiDS-1000 re-measurement, 181,477 lenses.
  - **Covariance:** a 50-patch jackknife that passes a calibration null (mean null χ² 6.73 against 7).
  - **Result:** the colour-blind zero model is rejected at 35.0/7 (p = 1.1 × 10⁻⁵, 4.4σ), and the colour-split ΛCDM fits (7.4/7).
  - **Error size:** the jackknife errors match the released ones after scaling for sample size, so they show no 1.3–1.6× underestimate. The split would need errors 1.27× larger to fall to 3σ.
  - **Still open:** systematics common to all patches (shear calibration, photo-z), colour-class contamination and satellites, which a jackknife cannot see. It also remains a failure of every colour-blind dark mass, not of B specifically.


## Addendum after CFG95 and CFG96 (appended 2026-09-29; the rows above are unchanged)

**The KiDS row has now survived two more stress tests.**

- **CFG95 (7214b5c62), B's own stellar-mass calibration.**
  - B's ATLAS3D dynamics and SPARC fit make early-type lenses only 0.07 dex heavier than discs, relative to their catalogue masses. The split needs 0.18–0.5 dex.
  - With the calibration, the law's rejection falls from 3.7σ to 2.8σ on the released data (alt 2.6σ), and from 4.4σ to 3.6σ on the re-measurement (alt 3.3σ). Reduced, not removed.
- **CFG96 (d2e97eb53), satellites.**
  - A twice-stricter photo-z isolation keeps 51% of the lenses and leaves the 1-halo split undiminished: amplitude 0.97 ± 0.19, 4.1σ.
  - So satellites, as removed by this isolation, do not drive it.

**It remains B's one failure specific to B in shared machinery**, and it is shared by every colour-blind dark mass (CFG77). Still open: calibration common to all patches, colour-class contamination, and satellites that photo-z isolation cannot catch.


## Corrections at adoption (appended 2026-09-29; the rows and addenda above are unchanged; this addendum supersedes them where they differ)

**The current bottom line.** This supersedes the "Bottom line" block above and the wording of the later addenda.
- **The one B-specific failure:** the KiDS early/late lensing split is B-SPECIFIC relative to the ΛCDM comparator, for the early-minus-late difference only. It is shared by any model whose predicted difference at fixed g_bar is negligible, NOT by every colour-blind model (a colour-blind Moster halo fits it at 6.9/7, CFG67). It is robust to the repo's own jackknife covariance (4.4σ in the 1-halo bins, CFG88 ef7c1d303) and to a twice-stricter isolation (4.1σ, amplitude 0.97 ± 0.19, CFG96 d2e97eb53); reduced but not removed by B's own stellar-mass calibration (2.8σ released / 3.6σ jackknife, CFG95 7214b5c62); fragile only to systematics a jackknife cannot see. Every earlier "every colour-blind dark mass" or "any colour-blind model" in this file should read "any model with a negligible predicted difference at fixed g_bar".
- **Shared with standard halos:** the super spirals (CFG68), and the Local Group R₀ with the KiDS + LG edge (CFG23, CFG25).
- **Not B-only failures:**
  - SLACS is a conditional difference between the models. B − ΛCDM ≈ +0.12 dex (median +0.118 over 54 cells, never negative; paired base cell +0.115 to +0.135). The specificity holds in 28 of 54 cells (W = 0.52), and both models pass with the floor (CFG86 4d994bb28, CFG87 f7332204e).
  - The groups at R2500 do not separate the models on equal footing (CFG81, CFG85).
  - The super spirals are shared.
- **Non-discriminating:** the ultra-faints, and the cold budget against KiDS.
- **Mixed:** SLUGGS (at γ = 3; key-fix 17 galaxies).
- **A compatibility check:** the X-ray ellipticals.
- **Convention-dependent:** the rule's satellites. M31 LVD's −2.67σ also depends on the error recipe: −2.67 / −1.74 / −1.97 / −1.49σ (CFG91 abb698467).
- **No ΛCDM counterpart:** Chae's external-field signal.

**Line-level corrections.**
- **"Independent"** (the re-run definition at the top, the SLUGGS row's re-run cell, and the CFG77 addendum): an independent re-implementation checks the arithmetic and the shared inputs, not the model.
- **The ultra-faint caveat "luminosity-ordered (untested)".** CFG83 (b41ca5f55) tested it.
  - No trend on the 40-object sample: Kendall τ against M_V is +0.18 (p 0.09).
  - On the 8 binary-corrected systems, τ_b = +0.79 (p 0.0055). That is flagged but not detected against the declared Bonferroni bar of 3.3 × 10⁻⁴, and it is identical for the law, the rule and ΛCDM.
- **"Not re-run by anyone this round" is stale.**
  - CFG32's, CFG33's and CFG34's B numbers have been re-derived, through CFG84, CFG87 and CFG85 respectively.
  - CFG66 and CFG74 were re-run clean (LEDGER_VERIFICATION Parts 3–4).
- **The SLACS rows** ("SPECIFIC-TO-B for the statistical gap only"; "B's side was not re-derived … unpaired").
  - CFG87 re-derived B's side and paired it: B's gaps reproduce (+0.159 / +0.172 / +0.152 / +0.168).
  - The paired base cell gives B − ΛCDM = +0.115 to +0.135 (7.5–8.2σ statistical).
  - Across the cells it stays CONDITIONAL: a difference between the models.


## Addendum after CFG110 (appended 2026-09-29; the rows and addenda above are unchanged)

- **A second KiDS test in the same machinery: the within-class mass split at fixed g_bar** (CFG110, 2f05b5303). Within each colour class, the 1-halo lensing signal at fixed g_bar shows no detectable dependence on stellar mass.
  - **B's law** (mass-independence in the deep regime) is consistent: 22.2/14, p = 0.075.
  - **The colour-split ΛCDM** is consistent too: 25.2/14, p = 0.033. The power between these two is only 8.8, so the test is non-discriminating between them.
  - **The colour-blind ΛCDM (Moster) is rejected:** 105/14, p ≈ 4 × 10⁻¹⁶.
- **So the KiDS picture in shared machinery is:**
  - the signal depends on galaxy type, and not detectably on mass within a type;
  - B's law gets the mass-independence right and misses the type dependence;
  - the colour-blind halo matches the colour split only through mass, and fails the mass split;
  - colour-dependent halos fit both.
- **The KiDS row stays B-specific relative to the colour-split ΛCDM.** Relative to the colour-blind ΛCDM, the two models each fail one KiDS test.
- **The lens photo-z check:** the within-class redshift split is consistent with zero (19.2/14, p = 0.16).


## Wording note on the CFG110 addendum (appended 2026-09-29)

- "B's law gets the mass-independence right" rests on a non-detection in a power-limited test: the power between B and the colour-split ΛCDM is 8.8, below the declared 9.
- The result is at the re-measurement's jackknife errors; satellites and calibration systematics are not covered.


## Addendum after CFG111 (appended 2026-09-29; the rows above are unchanged)

- **Row 1.20, SLUGGS:** With each SLUGGS galaxy's published GC density slope in place of the fixed γ = 3, the law's JAM-calibrated deficit stays at 3.6σ (alt 3.2σ; 2.2σ without the four centrals). The slopes come from Alabi+2017's literature relation, γ 2.49–3.43, verified against its Table 1. The γ that would null the massive centrals is far below their published values: NGC 4365 needs 1.06 against 2.56, and no γ ≥ 1 nulls M87. So the γ caveat does not rescue the law. B's derived rule fits with the same slopes: 1.55σ (alt 1.64σ), and −0.66σ with population masses. Isotropic orbits are assumed (CFG111 6e1b04092). The ΛCDM comparison (CFG69) was not recomputed with these slopes.


## Correction after CFG100 (appended 2026-09-29; the addenda above are unchanged)

- **The CFG110 addendum above:** CFG100 (a51dfe756) is an independent re-derivation of CFG110 and reproduces every headline: B 22.20/14 (p 0.0746), colour-split ΛCDM 25.16, colour-blind Moster 105.04, power 8.77. It corrects the reading in three ways. (1) 'B gets the mass-independence right' is not supported; only a non-rejection is. The 14-dof test has power 0.41 against ΛCDM-size mass dependence and 0.11 against half of it. The sharper 1-dof amplitude is A = 0.33 ± 0.34, so ΛCDM-size dependence is disfavoured at about 2σ (statistical only) and half of it is not excluded. Read: B is not rejected, and ΛCDM-size mass dependence within a class is disfavoured at about 2σ. Likewise 'not on mass within a type' means no detectable dependence at this power. (2) B and the colour-split ΛCDM are not discriminated. B's p ranges from 0.005 to 0.08 across the mass-split edges, and the order flips: B is better at q25/q75, ΛCDM at q40/q60. Dropping late-class bin 9 makes ΛCDM beat B (p 0.88 vs 0.31). The power of 8.8 against the threshold of 9 is razor-thin (10.35 with pair weights). (3) Only the colour-blind Moster rejection is robust: it holds through the bin set and ×1.5 errors. Its size is not robust: χ² 49–230 for M* ± 0.1 dex, and 79 with M200m. It also rests on the Moster mapping as coded. The jackknife has no photo-z, intrinsic-alignment or satellite terms.


## Addendum after CFG112–CFG114 (appended 2026-09-29; the rows and addenda above are unchanged)

- **Row 1.20, SLUGGS, GC orbits and the joint degeneracy (CFG113 1db2d3a69, CFG114 2a83f369e). At the published slopes, any constant GC anisotropy in the measured range (β −0.5 to +0.5) leaves the law's deficit at 3.4σ or more (alt 2.9σ), and no β < 1 nulls it. But with slopes and orbits varied together, it falls below 2σ at the corner where both are favourable: every γ_i − 0.4 with β = +0.5 gives 0.6σ (alt 0.1σ). That corner is more radial than any measured GC system. The deficit exceeds 2σ in 23 of the 25 cells (alt 21). The rule is conditional in the opposite corner: it fits in 13 of 25 cells and fails wherever the slopes are 0.2 or more steeper than published (2.1–3.5σ). So SLUGGS alone cannot make either reading clean. Measured GC slopes and anisotropy for M87, NGC 4365, NGC 4374 and NGC 5846 would decide it.**
- **The derived rule's support:** CFG111–CFG113 qualify the line 'The derived rule has no clean support left'. With published GC slopes the rule fits SLUGGS on its own (1.55σ with JAM masses, −0.66σ with population masses), and it keeps fitting for isotropic or radial GC orbits (0.56σ at β = +0.5). But one debris fraction still does not fit all ten populations at 2σ: SLUGGS's window [0.77, 1] misses the other nine's [0.23, 0.71] by 0.06 in φ (alt 0.11), with the M31 LVD binding (CFG112 670356510). That NO is fragile. It opens if every γ_i is lowered by 0.2 or with SLUGGS's population masses, and radial orbits were not tested in it. The line's clause 'not with dynamical SLUGGS masses' therefore stands, narrowly. The 1σ NO and the satellite failures do not depend on SLUGGS.
- The ΛCDM comparison (CFG69) was not recomputed with these slopes or orbits.


## Addendum after CFG104–CFG106 (appended 2026-09-29; the rows and addenda above are unchanged)

- **SLUGGS (row 1.20 / E1) and the derived rule's support:** (1) **CFG104** (independent re-derivation of CFG112) reproduces it exactly. Its reading: the NO is a boundary, not a conflict. All ten populations share a φ at 2.07σ (alt 2.09σ) against the 2σ line, and at 2.62σ with γ = 3. Only SLUGGS and the M31 LVD are in tension. The result is a knife edge: every γ_i shifted by −0.1 opens the ten-set, and +0.1 empties SLUGGS's window. The other nine populations are CFG71's committed rows. Read 'not with dynamical SLUGGS masses' as 'only at 2.07σ with dynamical masses and the published slopes'.
- (2) **CFG105** (independent re-derivation of CFG113) reproduces it; the only difference is at β = 0.9 (0.036σ, the grid-edge bias R7 bounds). It adds that the constant-β result assumes the power-law tracer extends to infinity. With the tracer cut off at 50 or 20 R_e, radial orbits worsen the deficit: 3.38σ becomes 3.97σ and 4.98σ at β = +0.5. An Osipkov–Merritt profile with r_a = 3 R_e (β → 1 outside) on an infinite tracer removes it (−0.8σ). So the outer tracer slope matters as much as β. The rule's 2.06σ at β = −0.5 is fragile to leave-one-out.
- (3) **CFG106** (independent re-derivation of CFG114) reproduces it: 23/25 and 21/25 law cells above 2σ, 13/25 for the rule, the corner at 0.586σ. It checked against printed targets, not blind. h50's solver truncates the line-of-sight integral at u = 6, which biases σ_pred by up to 0.57% at the corner. The slopes are one relation shifted coherently, so the law's 2σ failure is only as firm as the unknown correlation of the relation's two coefficients. With 1000 draws, the fraction with the law below 2σ is 4.6% (β = 0) and 21% (β = +0.5) at ρ = −0.99, and about 43–47% at ρ = 0. The corner is a mean cancellation on the box boundary: six galaxies are still under-predicted by more than 0.05 dex, and M87 would need γ ≈ 1.6. A 20% error inflation takes 23/25 to about 21/25.
- (4) **The slopes are 3-D.** Alabi+2017 define γ as the slope of the de-projected GC number-density profile, as checked in the paper's arXiv HTML on 2026-09-29. So the Jeans solution's ρ ∝ r^−γ uses it as intended; the case of projected slopes, which would put SLUGGS at +5.6σ at φ = 1, does not arise. The 'published slopes' are one mass relation, γ = clip(−0.63 log M* + 9.81, 2, 4) (2.49–3.43), not per-galaxy measurements.


## Addendum after CFG115 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS rows (E2/E3; next to gate 3.05):** CFG115 (e469ab0b1; criteria e416f3bea) splits each class into colour tertiles (June LePhare u − r). At fixed g_bar the KiDS colour dependence is not a sharp step at the red/blue valley: the tertiles on either side of u − r = 2.0 are equal (−0.049 each). A step that is constant within each class is rejected (χ² 18.1/4, p 0.001), and a linear colour gradient fits (6.3/4). But the within-class variation sits in the boundary tertiles (outer contrasts p 0.20), which is what colour noise blurring a true step would produce. The power for a gradient of the class-difference size is 4.8, below 9, so by the frozen map the lane is non-discriminating between a blurred step and a gradient. B's null gives 36.3/5 with a free offset. The descriptive models, none of which include colour noise, give: colour-split ΛCDM's sharp class step 21.1/5, colour-blind Moster 12.2/5. The colour dependence remains B's specific failure; this changes its shape, not its existence.


## Addendum after CFG107 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS colour structure (CFG115):** CFG107 (a027a5fac; the Opus chat's independent re-derivation) reproduces CFG115's numbers. The step-vs-gradient result is weaker than 'step rejected' reads, for four reasons. (1) Fragile to error inflation: the jackknife has no photo-z, intrinsic-alignment or satellite terms. The step rejection reaches p = 0.05 with errors inflated ×1.38, and the gradient-over-step preference with ×1.82. B's null itself (36.3/5 with a free offset) reaches p = 0.05 at ×1.81. (2) A step blurred by at least 0.2 mag of colour noise fits about as well as the gradient (χ² 7.4/4 at σ = 0.20, p 0.12). The boundary equality L3 = E1 is equally a blurred step. (3) Signal versus a colour-dependent systematic is mostly undecidable with the staged product. The gradient survives mass and redshift matching (β_w 0.58 ± 0.18). It is not confined to large radii, and the two redshift halves differ by only 1σ. Mimicking it with mass-to-light alone would need a colour-dependent stellar-mass bias of about 0.9 dex, which is implausible for mass-to-light alone but not for combined mass-to-light, photo-z and satellite systematics. (4) Quote only free-offset χ² for the model rows. The zero-offset rows under the jackknifed reference (the frozen R1 and R5) measure normalisation against a near-null covariance direction, not physics. The power is 4.47 or 4.80 depending on which class-difference reading is used; both are below 9.
- Supplement (CFG107, exact): the colour-split ΛCDM zero-offset row under the jackknifed reference is 22.7 with an all-lens reference and 77.7 with CFG115's class-mix reference. A −0.006 dex normalisation shift spans that range, so no zero-offset row under the jackknifed reference should be quoted. The power row's 4.8 uses the class-level amplitudes, β_true = (A_E − A_L)/(u_E − u_L); the step-fit reading gives 4.465. After mass and redshift matching, the gradient slope is 0.46 ± 0.11 (β_w 0.58 ± 0.18). The LePhare colour errors are not in the staged files, so the blur cannot be measured. CFG107's independence stops at the sum level: the staged product is checked only against the June file, to 3.1e-11. One CFG107 control, K4a (BFGS vs the normal equations, 1.95e-6 against a frozen 1e-8), failed as frozen; it is an optimiser limit.


## Addendum after CFG116 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS rows (E2/E3; next to gate 3.05):** CFG116 (1ab67b216; criteria e4083bd4f): the KiDS early/late split passes both standard lensing systematics nulls. Cross shear (B-mode): the early−late cross difference over the 1-halo bins is 5.3/7 (p 0.63), and each class's cross profile is consistent with zero. A systematic carrying half of the split would have given χ² ≈ 9, so class-dependent B-mode systematics at about 50% or more are disfavoured. Source separation: near and far background sources give consistent splits (5.4/7, a weak test), and the split persists with far sources alone (23.2/7, p 0.0016). Near-source dilution (~0.1 dex) is similar for both classes. The 'fragile only to systematics a jackknife cannot see' caveat narrows to E-mode-only shape errors, lens photo-z beyond CFG110, satellites beyond CFG96, and unmodelled covariance (CFG107's ×1.8).


## Addendum after CFG108 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS nulls (CFG116):** CFG108 (6e7cbdec2; the Opus chat's independent re-derivation) reproduces CFG116's numbers. Its independence stops at the staged sums: the near/far assignment and WX's content inside the staging cannot be re-checked there. It makes four corrections. (1) R0's '9' and '2.2' are non-centralities λ, not expected χ²; the expected χ² is 7 + λ (16.0 and 9.25). (2) The power is overstated. The cross null has only 32% power at ε = 0.5 (α = 0.01); 80% power needs ε ≈ 0.74 (omnibus) or 0.57 (shape-matched). The near/far null is essentially blind to near-only systematics: power 0.07 at ε = 0.5, A_nf = +0.03 ± 0.29. So read 'excluded only for ε ≳ 0.6–0.75, and only for E~B-type leakage', not 'disfavoured at 50% or more'. (3) Calibrate p-values by permutation; the χ²₇ tails are anti-conservative (permuted 99th percentile ≈ 20.5, not 18.5). The far-only split's empirical p is 0.0055, not 0.0016. Random 51% lens subsamples of the all-source split reach χ² ≥ 23.2 with probability 0.39, so the far-only value is not merely a smaller-N fluctuation. The near and far splits are dependent, not independent confirmations. (4) The amplitudes use a pooled-ESD ratio per class, log10(Σ_K1 WG / Σ_K1 WW), early over late; a fixed-pair-weight reading misses the far amplitude by 0.007. Passing both nulls does NOT exclude: E-mode-only class-dependent errors (a multiplicative shear bias would need 51%; a class-dependent baryonic-mass or g_bar-assignment offset would need about 0.5 dex, the largest untested avenue); lens photo-z (a 0.24 offset would be needed through Σ_crit; class-dependent outlier fractions are untested); satellites (the isolation flags were not read); and covariance ×1.8 (the all-source split reaches p = 0.05 at ×1.58, and inflating it destroys the nulls' power too). CFG108's own frozen control K8c failed: a mis-specified 90% threshold, observed 64%.


## Addendum after CFG140 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** CFG140 (KURVS-CDFS, z ≈ 1.5; the first on-disk sample in the decisive regime, g_bar/a₀ = 0.06–0.67 at the outermost measured point): NON-DIAGNOSTIC over the declared brackets, because the answer turns on the unmeasured outer pressure support. With the observed rotation velocity, a strict lower bound on the circular speed, a₀ ∝ H(z) over-predicts the outer accelerations in every gas and stellar-mass cell (−3.2σ to −9.6σ, corrected by the SPARC anchor), and flat a₀ is never disfavoured. With the Burkert constant-σ asymmetric-drift correction, flat a₀ under-predicts in 21 of 24 cells and the rival is never disfavoured. A KROSS z ≈ 0.85 same-pipeline control suggests that correction over-corrects at these radii. What settles it: an outer dispersion profile or a pressure-free tracer, and measured gas. With both, the test has 3–5σ statistical power, subject to CFG52's correlated floor of about 2.3σ.


## Correction to the CFG140 addendum (appended 2026-09-29)

- CFG140 correction (logic; the orchestrator's check). The observed velocity is a lower bound on the circular speed, because pressure support only raises V_c. A lower bound can exclude only a model that predicts V_c below V_obs. Under P0 both readings predict at or above the observed accelerations in every cell (the largest P0 Δ′ is −0.035 for flat and −0.196 for the rival), so the bound excludes neither. The P0 rows are the NO-PRESSURE-SUPPORT SCENARIO (V_c = V_obs), not a bound in the excluding direction. 'a₀ ∝ H(z) over-predicts in all 24 cells' holds only if the outer pressure support is zero; it means the rival needs substantial outer pressure support to survive. 'Flat a₀ under-predicts in 21 of 24 cells' holds only in the constant-σ Burkert scenario (P1); it means flat a₀ needs the outer pressure support well below that level. Neither reading is excluded by the data alone. The frozen verdict (NON-DIAGNOSTIC), the anchor, the KROSS control, the power row and the MUTATE are unchanged.


## Addendum after CFG141 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** CFG141 (KURVS with each galaxy's MEASURED outer dispersion, read from the paper's plotted σ(R)): the outer σ does not fall (σ_out/σ₀ median 1.05, range 0.70–1.13), so the constant-σ pressure correction is supported by data. With it (the isothermal self-gravitating layer with the local σ), flat a₀ under-predicts the outer accelerations in 21 of 24 cells, and survives only if these z ≈ 1.5 discs hold about 4× their stellar mass in cold gas, which is unmeasured. At the paper's own 40% molecular fraction it under-predicts by 0.39 ± 0.07 dex. The rival a₀ ∝ H(z) needs nearly as much gas. The frozen reading is NON-DIAGNOSTIC. Its testable content: flat a₀ requires total cold gas of about 4 M* in KURVS-like discs, and a measured μ ≤ 1.5 would disfavour flat a₀ at z ≈ 1.5 under this correction. The fixed-scale-height variant softens this (flat disfavoured in 16 of 24).

## Correction to the CFG141 addendum (appended 2026-09-29)

- CFG141 wording correction (the orchestrator's check). (1) Under P2 BOTH readings under-predict at realistic gas: at the paper's 40% molecular fraction (μ = 0.67) Δ′_flat = +0.39 ± 0.07 and Δ′_H = +0.24 ± 0.06, and both survive only at μ = 4 (flat 3 cells, the rival 6). So the P2 excess is not evidence against flat a₀ in particular: either both readings need about 4 M* of cold gas, far above the paper's and PHIBSS-type molecular fractions (about 0.4–0.6), or the P2 dispersion model over-corrects. The rival sits 0.12–0.16 dex closer in every cell, about half the gas bracket; under P3 at the paper's gas flat is 3.5σ high and the rival 1.3σ. (2) The pressure term dominates V_c at R_max (V_c²/V_obs² 1.5–6.1), so the result rests on the dispersion model at 4–7 R_d (anisotropy, thickness, non-equilibrium untested), where beam smearing and pressure support are debated. (3) σ_out/σ₀ ≈ 1.05 shows σ does not fall; it does not validate the isotropic isothermal layer. (4) 'About 4 M* of cold gas' is a requirement of the P2 model, for either reading, not a prediction of the framework. (5) CFG140's KROSS caution is narrowed, not removed: a falling outer σ is ruled out as its cause, and the P1 differential (+0.27 ± 0.07) is unexplained. The verdict (NON-DIAGNOSTIC) and every number are unchanged.

## Addendum after CFG117 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The ten doors, door 2 (Verlinde):** CFG117 (door 2 of the ten doors, Verlinde's emergent gravity; criteria b09ca1480, gates 5ef77ea09; lane bb504274c): a scoped NO-GO on G1. Verlinde's apparent dark mass, M_D² = (a_V r²/G) d(M_B r)/dr with a_V = cH/6, misses the CFG44 target's shape in all 16 cases (4 masses × point mass or exponential sphere × H₀ or H_Λ), with the target evaluated at a₀ = a_V. For a point mass C_V/C_target = (1 + x)/x exactly: 11 at x = 0.1, 2 at x = 1, 1.10 at x = 10; the spheres give 10–16 at x = 0.1 and 1.8–8.6 at x = 1. The cause is structural: Verlinde's point-mass dark density is r⁻² all the way in (the linear sum g = g_N + √(a_V g_N)), the target's is r⁻¹ inside r_M (the quadrature sum g = √(g_N² + a₀ g_N)). They share only the deep limit and approach it as 1/x, and the total field differs by up to √2 (at x = 1), not only the dark density. The failure lies inside Verlinde's own onset regime (his eq. 1.3). The normalisation is not the problem: κ_V = √(8π/3)/6 = 0.482 with H_Λ (a_V/a₀ = Z/6 = 0.965) and 0.583 with H₀, both within 2σ of both fitted κ windows. Other gates: G2 and G3 UNDEFINED (no perturbation equations, no action); G4 PASS as a count only; G5 FAIL (Hees, Famaey & Bertone 2017: the weak-field formula misses the planets' perihelion advances by seven orders of magnitude). Untested: Hossenfelder's covariant Lagrangian, later formulations, non-spherical systems. MUTATE (the target's own cold mass) passes 16 of 16: informative.

## Corrections after the round-3 documentation audit (appended 2026-09-29; AUDIT-T 64084d046, a00ed3de1; append-only, no result changed)

- **Row 1.10 (LV field dwarfs under the rule):** the −3.47σ (alt −2.70σ) is in S's own shrunken error (a ddof = 0 scatter and a fixed-halo Υ floor). With Υ propagated into the halo it is −1.75 to −2.1σ at the declared Υ_V = 2, −1.37σ at Υ_V = 1 (S = −0.055 dex) and −4.64σ at Υ_V = 4 (S = −0.147 dex). In the law's own error the change is −1.4σ. The size of the S offset is robust only at Υ_V = 2. 'S switches off above M_b ≈ 2.3e7' holds only within a window: for M* = M_b/2, S is off from 2.3e7 to about 2.2e11 M☉ and f_ex turns on again above that (CFG35's massive-spiral failure); for M* = M_b the window is 5.6e7 to 8.4e10 M☉. CFG92 was written with CFG91's code in view (restructured), so its independence is partial.
- **Row 1.25 (super spirals, SHARED):** the failing clause, the nine fastest (+0.164, 2.34σ), is selected on v_obs, the offset's own numerator. Under a no-trend null the selected nine exceed the sample mean by +0.071 ± 0.016, against +0.059 observed (P = 0.77; CFG89, post hoc). So the clause adds almost nothing beyond the all-23 mean (1.67σ), and the unselected trend test is the slope clause, 1.80σ. A +0.1 dex stellar-mass shift alone passes H2 (nine fastest at 1.91σ). The ΛCDM comparator's nine (+0.121) are the same v_obs-selected galaxies, so the same caveat applies to that column (not computed); SHARED stands, weaker on both sides.
- **The addendum after CFG104–CFG106:** 'alt 2.09σ' should read 2.08σ: CFG104's alt value is 2.0846 (canonical 2.0667, i.e. 2.07σ, unchanged).

## Addendum after CFG119 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The ten doors, door 7 (a fuzzy-dark-matter soliton):** CFG119 (door 7 of the ten doors, a fuzzy-dark-matter soliton with the baryons in its potential; criteria b09ca1480, gates 5ef77ea09; lane 435cb43e9): a scoped NO-GO on G1, on both footings. The Schrödinger–Poisson ground state cannot reproduce the target for any boson mass on the grid (10⁻²³ to 10⁻²⁰ eV), even with the soliton mass free per galaxy. The closest single galaxy (m = 10⁻²³ eV, the 10⁹ M☉ exponential sphere) misses by 4.0 dex against a ±0.04 dex band; the best single m, 10⁻²³ eV (best for every mass), misses its worst galaxy by 1.2 × 10⁵ dex. The ground state is cored where the target rises as 1/r, and falls exponentially where the target falls as r⁻²; no core width can pass (an analytic remark; lighter m not run). Other gates: G2 FAIL for every m on the grid (growth within 5% to 30/Mpc needs m ≥ 1.28 × 10⁻²⁰ eV, from Hu, Barkana & Gruzinov's fit); G4 FAIL (m is a new constant); G3 and G5 pass as statements. Control C1 fails as frozen and is kept: the exact ground state departs from Schive's fitting formula by up to 6.3% at 2.7 r_c, the fit's tail accuracy, not the solver's (an independent referee shooting script reproduces the ground state to every printed digit). MUTATE (the target's own density) passes H1: informative. Untested: the excited-state envelope, which is NFW-like in simulations and behaves as cold dark matter (door 6's question).

## Correction after CFG109 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS split, satellites:** CFG96 (the isolation test), after CFG109 (b7d41c302; the Opus chat's independent re-derivation, which reproduces every printed number): read 'robust to a twice-stricter isolation' and 'satellites, as removed by this isolation, do not drive it' as: the split persists under stricter photo-z isolation (4.1σ, amplitude 0.97 ± 0.19), but it does not differ from the full split within errors (difference of splits 8.75/7, p 0.27, δ = +0.009 ± 0.350), and the test is not powered to exclude a satellite contribution below ε ≈ 0.3–0.45 of the split at complete removal (0.6–0.9 at 75% removal). The removal fraction is undetermined, because the windows are photo-z proxies. The split's significance is fragile to error inflation (W20 reaches p = 0.05 at errors × 1.51). CFG109's independence stops at the staged sums and the isolation flags; four of its controls failed as frozen, one of them (a biased group-permutation null) unresolved.

## Addendum after CFG118 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The ten doors, door 6 (secondary infall):** CFG118 (door 6 of the ten doors, spherical secondary infall of cold matter onto a baryon core with shell crossing; criteria b09ca1480, gates 5ef77ea09; lane d0baef700): a scoped NO-GO on G1, on both footings. In a 1-D shell code (20,000 shells, Planck18 from z = 100, a static core, three angular-momentum brackets), the infall profile's C/C_target falls with radius in all 24 runs: 4–360 at x ≈ 0.1 for the spheres, 0.8–5.6 at x ≈ 1, and 0.05–0.21 at x ≈ 28. Even the best bracket is off by a factor of about 30 somewhere. The cause: too much cold mass inside r_M and too little outside (the cumulative mass is 1.0–4.2× the target's at x ≈ 1 and 0.28–0.66× at x ≈ 28, stable to resolution). The infall's radial scale follows the turnaround (∝ M^0.33) rather than r_M ∝ M^(1/2), so no single set of constants serves every mass. C1 and C2 (Bertschinger's −9/4 slope, −2.238) pass. C3, the resolution check of the local bins, fails and is kept; the cumulative mass converges, and H1 fails at both resolutions. MUTATE (the target's own density) passes H1: informative. G2, G3 and G5 pass as statements (plain CDM and Newtonian gravity). Untested: non-spherical collapse, mergers, a growing core, feedback, other angular-momentum distributions.

## Addendum after CFG142 and CFG160 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** (1) CFG142 (c64865b33; GOODS-ALMA 2.0 1.1-mm dust continuum, criteria frozen before the cross-match): NON-DIAGNOSTIC for the sample. None of the ten KURVS discs is detected, and only KURVS-11 is powered at the survey's depth. It excludes the P2 gas requirement as an approximate point-source limit: dust-traced μ < 0.72 at the nominal calibration, < 1.44 with gas-to-dust × 2. That holds only if its dust is compact against the 0.45″ beam; the rms is the survey average. (2) CFG160 (ff3d9ea7d; the simulation-calibrated pressure-support factor of Kretschmer et al. 2021, VELA at z = 1–5, frozen before any number): at the pre-declared decision cell (μ = 0.67, the paper's molecular estimate; δ = 0; canonical) the rival a₀ ∝ H(z) fits (Δ′_H = −0.006 ± 0.044) and the framework's flat a₀ is 3.3σ high (Δ′_flat = +0.144 ± 0.044). By the frozen map that is a Kretschmer-conditional lean toward the rival, the first in-regime reading in this record whose central value favours it. It is not robust and not a kill. At μ = 1.5 it flips (flat +1.2σ, rival −2.1σ); at the calibration's α × 0.6 (its 40% scatter) and at R_e = 2 R_eff the cell is non-diagnostic; flat is disfavoured in 14 of 24 cells, not all. The KURVS a₀(z) test now turns on two measurable quantities: the outer pressure support at 2–4.5 R_e, and the total cold gas.

## CFG160 governing wording (appended 2026-09-29; the orchestrator's check; it governs the CFG142/CFG160 addendum above)

- Under the simulation-calibrated (Kretschmer+2021) pressure correction, the pre-declared decision cell (μ = 0.67) leans toward a₀ ∝ H(z) at 3.3σ. It is conditional, not robust and not a kill: it flips with gas (at μ = 1.5 flat is +1.2σ and the rival −2.1σ); it moves within the calibration's 40% scatter (α × 0.6 is non-diagnostic); and it rests on ONE published calibration, adopted after CFG141's P2 result was known (a forking-path risk). The GOODS-ALMA limit (μ < 0.72 nominal) is a point-source approximation, and no total gas is measured. The decisive quantities are the outer pressure support at 2–4.5 R_e and the total cold gas. The decision cell was fixed with the CFG141 grid already known. At that cell a confirming result for flat a₀ would have been Δ′_flat within 2σ with Δ′_H below −2σ (for example α × 0.6 gives +1.3σ / −2.0σ); a disconfirming result is Δ′_H within 2σ with Δ′_flat above +2σ, which is what occurred; anything else is non-diagnostic. Nothing here is evidence against flat a₀ beyond this statement. CFG140's and CFG141's rows are not superseded: they stand as the P1 and P2 results. An independent re-derivation (CFG165, the Opus chat) is pending, and this wording holds until it reports.

## CFG160 after CFG165 (appended 2026-09-29; the rows and addenda above are unchanged)

- **Headline: a weak, normalisation-dependent lean; not a detection.** CFG165 (33b446ef3), the Opus chat's independent re-derivation, reproduces CFG160's decision cell (flat +0.147 ± 0.044, rival −0.003 ± 0.045; the 0.003 gap is inc_sfr_deg against inc_star_deg) and every sensitivity row, and corrects how the lean reads. (a) 'The first in-regime reading favouring the rival' does not survive on CFG160's own map: P3 at the same cell already reads lean rival (CFG141's committed values: flat +3.5σ, rival +1.3σ), and P3 is lean rival in 12 of 24 cells against P4's 14 (both counts checked here from the committed JSONs). The accurate statement is that P4's rival central value sits at zero. (b) The lean depends on the normalisation, not the α shape: all 8 alternative shapes with median α within ×[0.75, 1.25] keep lean rival; flat's Δ′ drops below +2σ at s = 0.71, and the class flips to lean flat by R_e/R_eff = 3 (CFG165). (c) Break-even total gas: μ = 2.14 for flat and 0.65 for the rival. The lean holds only below about 1.2 M*, and at the repo's total-gas median (μ ~ 4) both laws over-predict (CFG165). (d) x runs from 1.04 to 3.54, inside the calibration range. The README's 'the three largest residuals (KURVS 13, 17, 21) have the largest x' is wrong: the largest x are KURVS 21, 8 and 17 (checked here), and KURVS-8 has the lowest residual. (e) With gas and α as nuisance parameters the likelihood ratio falls from about 130 to 0.5–1.7, and P(lean rival | flat true) is 0.31–0.45, against a frozen requirement below 0.05: weak evidence, not a detection (CFG165). (f) KROSS through the same P4 pipeline, anchor-corrected at μ = 0.67: flat −0.004, rival −0.082 (−4.1σ), the opposite of KURVS; KURVS − KROSS = +0.151 ± 0.045 (CFG165), reproduced by CFG161 (9ff8e369a: +0.148 ± 0.044, 3.3σ from flat, 1.7σ from the rival; CFG161's outcome was not blind). (g) CFG165's independence stops at CFG4_common, CFG140's set-up choices, and Kretschmer's α(x) as quoted (unverified literature); its MUTATE M6 (σ_out permuted) did not bite and is kept.

## Addendum after CFG161–CFG163 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** The headline is unchanged: a weak lean that depends on the normalisation and the gas; not a detection. (1) CFG161 (9ff8e369a; its criteria are blind, its outcome is not, as disclosed): under P4 the KURVS − KROSS differential lands on the rival by the frozen rule (+0.148 ± 0.044, 3.3σ from flat's 0 and 1.7σ from the rival's +0.072). P4 does not manufacture evolution; P1–P3 do. But at a common gas fraction, flat fits KROSS (z ≈ 0.85; rival −4.1σ) and the rival fits KURVS: neither law fits both, and the gas evolution between the two epochs is the untested lever. This is a consistency statement about P4, not an a₀ verdict. (2) CFG162 (250250ed3): a map, not a verdict. At the decision cell, flat is preferred for outer pressure support below s_mid = 0.67 × Kretschmer's α (bootstrap 0.51–0.85), and the rival above it. Every published prescription (Kretschmer 1.00, Dalcanton & Stilp 1.42, fixed height 1.62, Price n = 1 1.69, self-gravitating 3.00) sits above s_mid at the paper's molecular gas. The crossing moves with gas (1.11 at μ = 1.5, 2.39 at μ = 4). So, given the literature, the test reduces to the total cold gas: flat fits for μ ≈ 2.1–3.7 and the rival for μ ≈ 0.6–1.7. (3) CFG163 (5b7b4517c): KURVS-15 is not detected in the archival 1.32-mm dust continuum. Its dust-traced gas is below 1.90 M* at the nominal calibration (below 3.8 with gas-to-dust × 2). For this one disc that is below flat's P4 break-even at the nominal calibration, and it does not reach the rival's. It is a gas-prior statement, not an a₀ test.

## Addendum after CFG164 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the gas prior:** CFG164 (bf1e27b2e; a measured gas prior from PHIBSS, Tacconi+2013, the 17 z- and M*-matched rows, frozen before any gas value): NON-DIAGNOSTIC at Kretschmer's correction. The molecular-only prior puts the KURVS sample-median μ at 1.01 (0.60–1.69), 68% of it in the rival's window. The decision cell at s = 1 is lean rival 0.55, lean flat 0.21, both 0.24 (below the 68% bar); under the stronger published corrections (s = 1.42–1.69) it is lean rival 0.70–0.81. Not robust: HI equal to the molecular gas turns s = 1 into lean flat 0.59; extrapolating the gas–mass relation to KURVS's lower masses (8 of 10 discs lie below PHIBSS's range) splits it; the α_CO bracket spans it. Across the declared priors P(lean rival | s = 1) runs 0.11–1.00. The measured prior narrows the question but does not settle it; the decisive measurement remains the KURVS discs' own gas at a depth reaching μ ≈ 1, and HI at z ≈ 1.5.

## CFG164 after CFG166 (appended 2026-09-29; the rows and addenda above are unchanged)

- **Wording: the gas prior gives a weak lean toward the rival, uncertain by a factor of about 2 and reversible by HI; read with CFG165, it is weak evidence, not a detection.** CFG166 (ea66f9f17), the Opus chat's independent re-derivation, reproduces CFG164: 57 of 57 pass lines; counts 73/51/17/38; primary median μ 1.025 (0.604–1.719), 68% rival and 7.6% flat; at s = 1, lean flat 0.210, rival 0.540, both 0.245; the HI, mass-scaled (slope −0.219) and ULIRG rows. The largest class gap, 0.018, is Monte Carlo at N = 4000. (a) Extrapolating to lower mass: by the frozen rule the verdict is driven by the extrapolation, but only just (the P(lean rival) span is 0.202 against the 0.20 line). The mass slope is −0.22 ± 0.20 with a permutation p of 0.28, i.e. undetermined (checked here: −0.219 ± 0.196, p = 0.27). Carrying that uncertainty lowers lean rival from 0.54 to 0.34; a per-disc nearest-mass prior gives 0.52–0.55 (CFG166). (b) The redshift exponent implied by the data in the repo is 0.23 ± 0.52 (checked here, with the mass term, on all 51 clean rows), inconsistent with the 2.5 declared in Variant Z. The z ≈ 1.2 and z ≈ 2.2 PHIBSS samples are selected differently, so neither number is a clean evolution measure. The CO-detection bias cannot be tested, because no flagged row has z in the window; a bounding run moves lean rival to 0.43–0.62 (CFG166). (c) Window edges: the frozen stability line fails narrowly (5 of 105 near-frozen windows miss ±0.12, the worst by 0.199, all with z_hi = 2.5). There is no sign of tuning toward a class, and lean rival is the modal class in 97% of 317 windows (CFG166). (d) The marginalisation does not depend on its definition: bootstrap and lognormal draws differ by at most 0.013 (CFG166). CFG166's controls M1 and M3 did not bite, and are kept. Disclosed here: CFG164's HI rows (h = 0.5, 1) are not exact rescalings of the h = 0 draws, because one sequential random stream was used, so each HI row carries its own Monte Carlo noise (~0.01–0.02).

## Addendum after CFG170 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the two-epoch gas ratio:** CFG170 (fdbdcf323; criteria 1caae1adb frozen before any break-even): NON-DIAGNOSTIC. Both laws need the cold-gas fraction to rise about threefold between KROSS (z ≈ 0.85) and KURVS (z ≈ 1.5). At s = 1.42–3.00, flat needs 2.97–3.10 and the rival 2.60–3.57, only 0.01–0.06 dex apart; at s = 1, flat needs 3.3 [2.0, 5.7] and the rival 11.9 [1.6, open]. The in-repo PHIBSS bracket (1.00, 2σ [0.73, 1.39]) disfavours both laws, and the abstract-level literature bracket (2.02 [1.61, 2.42]) disfavours neither. Two epochs do not break CFG162's pressure–gas degeneracy.
