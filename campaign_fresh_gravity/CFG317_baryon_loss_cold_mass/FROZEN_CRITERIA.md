# CFG317 — FROZEN CRITERIA: does the cold component keep the collapse mass of the baryons a system ORIGINALLY had?

Written and committed before any new score. One plumbing prototype was run before freezing; it is disclosed in section 9 with every number it printed.

κ = ½ is FITTED (it sets a₀ on both footings: 9.3603e-11 / 1.1312e-10 m s⁻²). The cold component is collisionless and its mass is still required; no dark-matter particle is added. Nothing here says the theory is closed.

## 1. Why, and the hypothesis

CFG313 replaced the ΛCDM collapse masses in candidate B's cold-mass rule with the framework-native M_c = M_b,now / f_b (f_b = 0.157126, CFG35's `FB`). With that mass the rule never switches on: the leftover f_ex = max(0, 1 − M_ph,edge / [(1 − f_b) M_c]) is zero for every object, so B is the bare law. B then fails two tiles: the MW ultra-faints (+0.325 dex, z +3.77 | +3.55) and SLUGGS (z +3.28 | +2.67 with h50 masses, +3.99 | +3.65 with JAM masses, +3.60 | +3.22 with literature slopes, +2.75 | +2.23 with SLUGGS masses).

**Hypothesis under test (framework-native, collisionless retention).** The cold component keeps its collapse mass (PAPER36, CFG35–39). That mass is set by the system's ORIGINAL baryons, M_c = M_b,init / f_b, not by the baryons it has today. Systems that later lost most of their baryons keep their cold mass, while the law sees only the baryons that remain:
- ultra-faints lost their gas to reionization at z ≳ 6;
- massive ellipticals lost theirs to quasar/AGN outflows;
- M31 and Local Volume dwarfs, with extended star formation, lost relatively little.

Define the retention factor **R ≡ M_b,init / M_b,now**, so M_c = R M_b,now / f_b. CFG313 is R = 1. The hypothesis predicts that the R the data need tracks an INDEPENDENT, non-dynamical measure of baryon loss.

Record hint read (CFG34): over 20 groups and 12 X-COP clusters, log(M_HSE/M_B) falls with log f_b (ρ = −0.958). Caveat, declared here: in the branch where the cosmic share wins, M_B ∝ M_b, so part of that correlation is built in (M_HSE / M_B ∝ 1/f_b at fixed M_HSE). It motivates this lane but is not evidence for it.

**Correction to the request's premise, declared from CFG313's committed numbers.** "About 7× more" is CFG313's inertness margin k* = 7.0, the MINIMUM over every scored object, attained at M_b ≈ 9.5e11 (a massive elliptical). The switch-on factor grows towards low mass (section 7): about 700–1250 for the ultra-faints. So the two red tiles need very different R.

## 2. The machinery (no new physics, no new knob)

- The harness is CFG313's, exec'd read-only up to its run section (`cfg313_native_rescore.py`, everything before `MODES = {}`): CFG45 (satellites, SPARC classes, UGC 2487, Di Teodoro, SLUGGS h50, X-ray, Ogle), CFG58 (d2) (LV field dwarfs), CFG55 (SLUGGS JAM γ = 3 and SLUGGS masses), CFG111 (SLUGGS literature γ), CFG39 (SPARC rms). Same estimators, errors, data, kernels (each lane's own), both footings, and both profiles: V1 = h48's Dutton–Macciò NFW with M_200c = M_c, and V2 = an isothermal truncated at the law's own r_ta.
- The ONLY change: CFG313's native hook `mc_native(M_b)` returns R × M_b / f_b instead of M_b / f_b. The (1 − f_b) factor and f_b itself are unchanged. CFG313's native collapse-floor error term (factors ×0.1 … ×10 on the native M_c) applies to R × M_b / f_b as it stands.
- R enters in two ways.
  - **(A) Global scans:** one scalar R for every object. Each population's statistic depends only on the R of its own objects, so a global scan equals a per-population scan.
  - **(D) Per-object R:** a lookup keyed on the satellite's committed M★ = Υ_V L_V (Υ_V = 2; the hook receives this value in every Υ_V and floor variant). The floor hook reuses the R of the M_c call that precedes it in `sigma_read`. Objects not in the lookup get R = 1. Any key collision between two different objects is detected and reported; colliding objects get the mean of their R values.

## 3. (A) The needed retention factor R_need

- **Grid:** log₁₀ R = 0.00, 0.05, …, 6.00 (121 values). Every population statistic and z is evaluated for V1 and V2, at both footings. R_need is read by linear interpolation in log R between grid points.
- **Populations and their statistics** (as committed; ids as CFG313):

| ID | population | statistic and error | gate |
|---|---|---|---|
| P1 | MW ultra-faints, 31 + 9 limits | Kaplan–Meier median of log σ_obs/σ_pred; bootstrap ⊕ Υ_V floor ⊕ native collapse floor | \|z\| < 2 |
| P2a | MW classical (14) | median | z > −2 |
| P2b | M31 Collins+13 (14) | median | z > −2 |
| P2c | M31 LVD (34) | median | z > −2 |
| P2d | LV field dwarfs (13) | median | \|z\| < 2 |
| P5 | SLUGGS h50 masses (19) | mean outer-bin offset | \|z\| < 2 |
| P5J | SLUGGS JAM, γ = 3 (16) | mean | \|z\| < 2 |
| P5S | SLUGGS SLUGGS masses (16) | mean | \|z\| < 2 |
| P5L | SLUGGS JAM, literature γ (16) | mean | \|z\| < 2 |
| P6 | X-ray ellipticals (7) | mean | \|z\| < 2 |
| P3 / P8 | SPARC control | A3 fraction (both classes) and rms change | A3 ≥ 90% in both classes and rms change < 0.005 dex |

  UGC 2487, Di Teodoro and Ogle are carried through as in CFG313 and reported.
- **Per population, footing and profile:**
  - **R_need,0:** the smallest R at which the statistic crosses zero. If the statistic at R = 1 is ≤ 0, R_need,0 = 1 (cold mass only adds, and no extra mass is needed). If it never crosses by R = 1e6, R_need,0 is reported as "> 1e6" and censored at 1e6.
  - **The 1σ interval** {R : |z(R)| ≤ 1}.
  - **The gate interval** {R : gate passes}.
  - **R_switch:** the switch-on factor, min over the population's objects of M_ph,edge / [(1 − f_b) M_b / f_b]. Below it the rule is the bare law.
  - **SPARC:** R_max, the largest grid R at which both SPARC clauses still hold.
  - **Monotonicity** of each statistic in R is reported. If a statistic is not monotone, the first crossing is used.
- **Per object (satellites, resolved dispersions):** R_need,0 per object from the object's own offset log σ_obs/σ_pred(R), with the same rules: 1 if the offset at R = 1 is ≤ 0, censored at 1e6.
- **Reported beside these:** the R implied by the committed ΛCDM collapse masses, R_ΛCDM = M_c,committed f_b / M_b (Moster for the satellites; Mandelbaum red for SLUGGS and the X-ray ellipticals). Population medians.

## 4. (B) Independent baryon-loss estimators: data on disk only

### B1: dwarfs, the leaky-box effective yield from stellar [Fe/H] (the only estimator that exists on disk)

**Data.**
- **[Fe/H]:** `real_research/data/dsph/lvd_dwarf_mw.csv`, `lvd_dwarf_m31.csv` and `lvd_dwarf_local_field.csv` (Pace 2024 LVD), column `metallicity` (mean stellar [Fe/H], spectroscopic where available), with its error the mean of `metallicity_em` and `metallicity_ep`. For Collins+13 objects: the `[Fe/H]` and `e_[Fe/H]` columns of `collins2013_m31_dsph.tsv`.
- **Gas now:** M_g = 1.33 × 10^`mass_HI` from the same LVD rows. M_g = 0 if only an upper limit exists. The CFG18 infall gas is a model, not a measurement, and is not used by the estimator.
- **M★ = Υ_V L_V,** with Υ_V = 2 and L_V from M_V as the lanes use.
- **Missing values:** a missing [Fe/H] error is set to 0.2 dex. For M31 LVD objects with no LVD metallicity, the Collins+13 [Fe/H] of the same galaxy is used (matched by name, "Andromeda N" = "And N", "Cassiopeia II" = "And XXX"). Objects still missing take their population's median R_ind in (D), and are excluded from the per-object statistics.

**Model (declared; standard textbook leaky box).**
- Instantaneous recycling. One-zone. No inflow after collapse.
- Outflow rate = η × SFR (mass loading η ≥ 0, constant).
- True iron yield y. All baryons start as gas, M_g0.
- Then Z = p ln(M_g0/M_g) with p = y/(1 + η), and stars formed = (M_g0 − M_g)/(1 + η).
- The stellar metallicity distribution is a truncated exponential, dN/dZ ∝ e^(−Z/p) for 0 < Z < p ln(1/μ'), where μ' = M_g,now / M_g0 and M_g0 = M_g,now + (1 + η) M★.
- The observable is the mean of the stellar log metallicity, <[Fe/H]> = E[log₁₀ Z] − log₁₀ Z_Fe,⊙. For a gas-exhausted system (μ' = 0) this is log₁₀ p − γ_E/ln 10 = log₁₀ p − 0.2507, exactly.
- **η is solved per object** (Brent root on η ∈ [0, 1e7]) so that the model's E[log₁₀ Z] equals the observed mean. If even the closed box (η = 0) is more metal-poor than observed, then η = 0.
- **R_ind = M_b,init / M_b,now = [(1 + η) M★ + M_g] / (M★ + M_g).**

**The yield (declared, not fitted).** log₁₀(y_Fe / Z_Fe,⊙) = −0.2, with a systematic bracket [−0.5, +0.1]. This is a core-collapse-dominated iron yield: an oxygen yield of about 1–1.5 Z_O,⊙ for a Kroupa/Chabrier IMF, and the [α/Fe] ≈ +0.3–0.4 plateau of old metal-poor populations. These are textbook values, recalled and not re-verified here. The bracket is common to all objects: it moves every log R_ind by about the same amount, so it cannot change a rank correlation, but it does shift the ratio test and the re-score. The re-score is also run at the +0.1 end, the end that favours the hypothesis.

**Per-object error on log R_ind:** the [Fe/H] error ⊕ 0.1 dex (the MDF-shape allowance), propagated through the model by finite differences. Population value: the median of log R_ind over objects with [Fe/H]; error from a bootstrap of the median (2000, seed 317).

**What B1 can and cannot see (declared).** The metallicity records gas that was processed through star formation and then lost (the outflow). Gas removed WITHOUT forming stars is invisible to it: unprocessed gas photo-evaporated at reionization, or stripped wholesale. So in the scenario the hypothesis names for the ultra-faints, **R_ind is a LOWER BOUND** on M_b,init/M_b,now. This is reported beside every comparison ("R_need ≥ R_ind" is a consistency statement, not a prediction).

### B2: star-formation-history quench epoch — NOT ON DISK, branch stopped

The LVD `age` column is empty for every satellite with a dispersion. Needed: Weisz et al. 2014, ApJ 789, 147 (Table 2, τ₅₀/τ₉₀ for about 40 LG dwarfs; VizieR J/ApJ/789/147, about 20 kB), and Brown et al. 2014, ApJ 796, 91 (UFD ages, about 2 kB). Not downloaded.

### B3: ellipticals — NO ESTIMATOR ON DISK, branch stopped

- **Hot-gas deficit, X-ray ellipticals:** the repository has no gas-density profiles. `humphrey2006_ellipticals.tsv` carries only the NFW + stars fits, and CFG32 says so. Needed: the gas-density and temperature profile fits of Humphrey et al. 2006, ApJ 646, 899 (the arXiv source astro-ph/0601301, about 1 MB, the same source the repository's table was transcribed from); or Babyk et al. 2018, ApJ 857, 32 (hot-gas masses of about 94 ETGs, about 20 kB).
- **SLUGGS:** no hot-gas masses and no stellar metallicities on disk. `sluggs_forbes2017_galaxies.tsv` has M★, R_e, σ and environment only. Needed for B1-type metallicities: McDermid et al. 2015, MNRAS 448, 3484 (ATLAS3D XXX, [Z/H] and [α/Fe] within R_e/8, R_e/2 and R_e for 260 ETGs; VizieR J/MNRAS/448/3484, about 100 kB). It covers most SLUGGS galaxies.
- **The stellar-mass-to-cosmic-baryon shortfall** needs a halo mass. The only halo masses on disk are the Mandelbaum+16 lensing masses (ΛCDM-interpreted, and gravitational, so dynamical in this framework) and the h10/Humphrey NFW fits (dynamical). Both are excluded as R_ind: R must come from non-dynamical data. R_ΛCDM is reported in section 3 for orientation only.
- **Expectation, NOT used in any score:** published central [Z/H] of massive ellipticals is about 0 to +0.3 (recalled, not verified). By B1's own logic that would give R_ind ≈ 1–2 for the ellipticals, i.e. LOW loss: the opposite of what the hypothesis needs. Testing this requires the McDermid+15 table above.

### SPARC (control)

No metallicities on disk, so no R_ind. The hypothesis labels it low-loss. In (D) it keeps R = 1, and its R_max is reported.

## 5. (C) The test (frozen statistics)

All on V1 at the canonical footing as primary. The same statistics are reported for V1 alt, V2 canonical and V2 alt.

- **T1 — the sign test.**
  - **Hypothesis labels:**
    - HIGH-loss: P1 (ultra-faints), P5, P5J, P5S, P5L (SLUGGS, every mass route) and P6 (X-ray ellipticals).
    - LOW-loss: P2b (Collins), P2c (M31 LVD), P2d (LV field) and SPARC.
    - P2a (MW classical) is not labelled by the hypothesis; it is reported only.
  - **The data's need:** a population "needs large R" iff z(R = 1) > +1, i.e. the data lie above the bare law by more than 1σ. Any R that moves a statistic must exceed R_switch ≥ 7 > 10^0.5, so "needs large R" means "needs R > R_switch". Otherwise it "needs R ≈ 1".
  - **The estimator's class:** "large" iff the population's median log R_ind > 0.5. Otherwise "≈ 1".
  - **Pass condition:** T1 passes iff, for EVERY labelled population, both the need class and the R_ind class equal the label. A labelled population with no R_ind (SLUGGS, X-ray, SPARC) cannot satisfy the condition, so T1 cannot pass while those estimators are missing. This is declared now, before any number.
  - **Reported:** T1 restricted to the populations that have an R_ind (T1′), and a relative-order variant (the HIGH-labelled populations' median R_ind exceeds every LOW-labelled one's).
- **T2 — the correlation.**
  - **Primary:** the Spearman rank correlation between per-object log R_need,0 and log R_ind, over every satellite with a resolved dispersion and a measured [Fe/H]. P1, P2a, P2b, P2c and P2d are concatenated; an object that appears in two samples counts in each. One-sided permutation p (10,000 permutations, seed 317) for ρ > 0. Censored R_need is set to its cap: a rank statistic needs nothing more.
  - **Condition:** T2 passes iff p < 0.01 AND the population-level Spearman ρ over the populations with both R_need,0 and R_ind is > 0.
  - **Reported:** within the ultra-faints only (per object, same p method); the population-level ρ with its exact one-sided permutation p. With n = 5 populations, p < 0.01 is reachable only by a perfect, untied order; that is why the population-level value is a sign condition, not the significance test.
- **T3 — the ratio.**
  - **Statistic:** the median over populations (those with both values) of log₁₀(R_need,0 / R_ind), with its scatter: the std over populations, and the per-object std of the same ratio.
  - **Condition:** T3 passes iff |median| ≤ 0.3 dex.
  - **Reported:** the same at the yield bracket ends (−0.5 and +0.1).
- **Decision (per footing × profile):**
  - **SUPPORTED** iff T1 and T2 and T3 all pass.
  - **PARTIAL** iff it is not SUPPORTED, AND T1′ holds (the sign test over the populations that have an R_ind), AND either T2's per-object p < 0.05 with ρ > 0, or T3 passes.
  - **NOT SUPPORTED** otherwise.
  - **Headline:** SUPPORTED only if SUPPORTED in all four combinations; NOT SUPPORTED only if NOT SUPPORTED in all four; otherwise the four are reported as split.

## 6. (D) The re-score with M_c = R_ind × M_b,now / f_b (no fitting)

- **R per object:**
  - satellites: their own R_ind; objects with no [Fe/H] take the population median;
  - SLUGGS, X-ray ellipticals, SPARC, UGC 2487, Di Teodoro, Ogle: R = 1 (no estimator on disk, so CFG313 unchanged).
- **Runs:** V1 and V2, both footings, at the nominal yield and at the yield bracket ends −0.5 and +0.1 (+0.1 favours the hypothesis).
- **Report:** every CFG313 tile (the ROWS list, P3 and P8) with its gate under R = 1 (CFG313 native) and under R_ind, and the moves: red → green and green → red.

## 7. Hand pre-flight (before freezing; no harness statistic used)

**Switch-on factor R_switch = (M_ph,edge / M_b) / 5.364**, from CFG313's frozen pre-flight phantoms (canonical; alt about 15% higher):

| M_b [M☉] | 1e3 | 1e4 | 1e6 | 1e7 | 1e8 | 1e10 | 5e10 | 10^11.5 |
|---|---|---|---|---|---|---|---|---|
| R_switch | 1250 | 710 | 224 | 125 | 71 | 22 | 15 | 9.3 |

**Ultra-faint baryons against a collapse halo.**
- A typical ultra-faint has M_V ≈ −4, so L_V ≈ 3.4e3 L☉ and M★ ≈ 7e3 M☉ (Υ_V = 2).
- The committed rule's collapse mass, 1e9 M☉ (Moster, clamped), would have carried f_b × 1e9 = 1.6e8 M☉ of baryons. So the ΛCDM rule effectively assumed R_ΛCDM ≈ 1.6e8 / 7e3 ≈ 2e4 (range 1e4–1e5 over the ultra-faints).
- The committed rule with that mass took the ultra-faint offset to −0.059 dex, a slight overshoot. So R_need for the ultra-faints should lie below about 2e4 but above R_switch ≈ 700–1250.
- **Expected log R_need(UFD) ≈ 3–4.**

**Expected R_ind from B1** (gas-exhausted form, log R ≈ log y − <[Fe/H]> − 0.25 with log y = −0.2):

| population | typical [Fe/H] (LVD/Collins values seen while checking columns) | expected log R_ind | expected R_ind | R_switch at their mass |
|---|---|---|---|---|
| ultra-faints | ≈ −2.5 (range −2.2 to −3.0) | ≈ 2.05 | ≈ 110 (55–350) | 700–1250 |
| MW classical | ≈ −2.0 (Fornax −1.07, Sgr −0.53) | ≈ 1.5 | ≈ 30 (Sgr ≈ 1.2) | 70–225 |
| M31 dwarfs | ≈ −1.8 | ≈ 1.35 | ≈ 20 | 70–225 |
| LV field (gas-rich) | ≈ −1.45, with HI present | ≲ 1.0 | ≲ 10 | 70–125 |
| SLUGGS / X-ray | none on disk | — | — | 7–15 |

**Predictions from the pre-flight (each can fail):**
- **PF1.** R_ind < R_switch for every satellite population's median, so the (D) re-score moves no satellite tile. The ultra-faints stay red. SLUGGS stays red, because its R = 1.
- **PF2.** log(R_need/R_ind) for the ultra-faints is about +1 to +2 dex. T3 fails.
- **PF3.** The LOW-labelled dwarfs (M31, LV field) get R_ind ≈ 10–20: "large" by the 0.5 dex threshold. T1 fails on the R_ind side as well as on the missing elliptical estimators.
- **PF4.** The per-object correlation is weak. B1's R_ind follows the mass–metallicity relation smoothly, while R_need is ≈ 1 for about half of the classical and M31 objects.
- **Expected decision: NOT SUPPORTED.** Any of these predictions failing is reported as such.

## 8. Controls (each can fail) and checks

- **C1 (R = 1).** Every population statistic and z at R = 1, V1 and V2, both footings, reproduces CFG313's committed native table (`cfg313_native_rescore_results.json`, TABLE: native_V1, native_V2, P3, P8) to 1e-9.
- **C2 (identity).** For every population with 1 < R_need,0 < 1e6 (V1 canonical), the harness re-run at exactly R = R_need,0 gives |statistic| < 0.005 dex: the inversion reproduces the data by construction.
- **C3 (the estimator).**
  - The numerical E[log₁₀ Z] at μ' = 0 equals log₁₀ p − 0.2507 to 1e-6.
  - Every root residual is < 1e-8 dex.
  - R_ind ≥ 1 for every object.
  - At solar metallicity with no gas and y = Z☉, η = 0 and R = 1 to 1e-9.
- **C4 (positive control for the test machinery; synthetic, separate from data).**
  - Set R_need,syn = R_ind × 10^N(0, 0.15) per object (seed 317), and the population values to the medians of R_need,syn. T2 must pass (p < 0.01) and T3 must pass.
  - With R_need,syn shuffled across objects (seed 318), T2 must fail.
- **MUTATE (separate outputs `_MUTATE`).** R_ind is shuffled across all satellite objects (seed 317), and the population medians are recomputed from the shuffled values. T1, T2 and T3 are recomputed and the (D) re-score is re-run with the shuffled R. **Declared MUTATE check:** the correlation test T2 fails, AND the sign test T1′ or T1 fails.
  - Caveat, declared now: if the main run already fails T1/T2, the MUTATE fail is uninformative about discriminating power. C4 is the control that shows the machinery can say SUPPORTED.
- **Main-run checks:**
  - C1–C4;
  - PF1 (prediction);
  - T1, T2, T3 (the frozen tests; load-bearing);
  - DECISION (reported);
  - the R_need and R_ind tables (reported);
  - the (D) moves (reported).
- The run ends with an "N/M checks pass" line and exits 1 if any load-bearing check fails. A FAIL is a valid result.

**Outputs:** `cfg317_baryon_loss.py` writes `cfg317_baryon_loss.out` and `_results.json`; `MUTATE=1` writes the `_MUTATE` pair.

## 9. Disclosure: one plumbing prototype before freezing

To time the harness, a scratch script exec'd CFG313's prefix, scaled `mc_native` by a global R and called its `run_mode("native", "nfw")` at R = 1, 100 and 1e4. It printed the following canonical-footing values:

| R | UFD KM median | SLUGGS h50 mean | CFG55 JAM rule mean | M31 LVD median | X-ray mean | SPARC rms |
|---|---|---|---|---|---|---|
| 1 | +0.3245 | +0.0795 | +0.0970 | +0.0435 | +0.2802 | 0.1003 |
| 100 | +0.3245 | −0.1631 | −0.0909 | +0.0435 | −0.0943 | 0.3674 |
| 1e4 | −0.0434 | −0.3938 | −0.2423 | −0.3301 | −0.4272 | 0.7248 |

Each run took about 1 s. These values informed the hand pre-flight's expectation that log R_need(UFD) lies between 2 and 4, and they show that a single global R cannot serve SPARC and SLUGGS at once. No criterion, threshold, yield or label was chosen after seeing them in a way that changes a verdict: the labels come from the request, and the yield is a textbook value.

## 10. Rules

No fitting of R to make tiles pass: R_ind comes only from [Fe/H] and HI. No knob scans beyond the declared R_need inversion grid, which is a measurement of what the data require, not a tuning. No downloads; missing estimators are named with paper, table and size. Other lanes' files are read, never edited; the CFG316 folders are not touched. No personal names or absolute home paths in files.
