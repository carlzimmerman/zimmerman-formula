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
