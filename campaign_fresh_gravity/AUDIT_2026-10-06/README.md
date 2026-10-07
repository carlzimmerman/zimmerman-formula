# AUDIT 2026-10-06: hostile referee pass on today's lanes

Scope: CFG361 / 366 / 372 / 374 (PM growth chain), CFG367 (superradiance), CFG368 (DESI flow), cold_mass cm12–cm15 (including cm13 energetics and the cm12 forward fix), the 10-06 STANDING entries and WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md.

Method:
- Nothing in any lane folder was edited.
- No PM simulation was started. PM numbers come from the lanes' work JSONs in `../_external_data/cfg3{59,61,66,72,74}_work/`.
- CFG367, cm12 (corrected) and cm13 were re-run from committed copies in a scratch directory. Their outputs are byte-identical to the committed `.out` files.

Audit scripts in this folder:
- `audit_pm_ratios.py`: S0 identity, plus σ₈ and P(k ≤ 1) ratios at z = 1, 0.5 and 0.
- `audit_kj_field.py`: imports CFG372's engine read-only and measures the size of the k_J error on a linear 128³ field. This is a field-level calculation, not a PM run.
- `audit_cfg368_bracket.py`: re-uses CFG368's own code with a wider initial-vacuum bracket.

## Ranked findings

### CRITICAL

**1. The gas Jeans wavenumber scales the wrong way with a (CFG372, CFG374, and inherited by CFG376 and CFG378). CFG372's lane verdict "GROWTH OK at 1e6 K" is not supported.**
- **Where:**
  - `CFG372_pressure_filtered_phantom/cfg372_pm.py:279`: `kJ = math.sqrt(1.5 * Om * a) * 100.0 / cs`;
  - the same line in `cfg374_pm.py:283`, `cfg376_pm.py` and `cfg378_pm.py`, and in the checkers `cfg372_checks.py` and `cfg374_checks.py`;
  - frozen as "k_J(a) = √(1.5 Ω_m a)·100/c_s" in CFG372/FROZEN_CRITERIA.md, citing Gnedin & Hui 1998.
- **What is wrong:**
  - Gnedin & Hui define the comoving k_J = (a/c_s)·√(4πG ρ̄), with ρ̄ ∝ a⁻³. That gives k_J = √(1.5 Ω_m / a)·H₀/c_s, which goes as a^(−1/2).
  - The code goes as a^(+1/2). It is right only at z = 0 and too small by a factor a before that: ×2 at z = 1, ×4 at z = 3, ×50 at z_i.
  - So the phantom is over-filtered at every earlier epoch.
- **Size (audit_kj_field.out, 1e6 K):** the phantom source near k ≈ 1 h/Mpc is too weak by ×1.7 at z = 0.5, ×2.5 at z = 1 and ×4.3 at z = 2.
- **Why the early epochs matter:** in CFG366 R_c = 3 with no filter, 58% of the z = 0 P(k = 1) excess (0.168 of 0.290) is already present at z = 1.
- **Expected effect:** scaling the CFG366 history by the correct filter ratios puts CFG372's 1e6 K max|P−1| at roughly 10–15%, against the 10% cut. The committed values are 7.6% / 8.9%. The verdict would therefore likely become TENSION, at least on alt.
  - This is an estimate. It needs an owner-approved re-run with k_J ∝ a^(−1/2).
- **Other runs:**
  - At 1e4 K the error is ≤ 6% at z ≤ 1. TENSION stands there.
  - CFG374's +12 / +16% are lower limits, so its TENSION stands and gets worse.
- **Why the controls missed it:** the C1/C2 controls and CFG374's C1c compare the code with the same wrong formula, so they cannot detect it.
- **What it changes:** the CFG372 verdict, the STANDING CFG372 and CFG374 lines ("σ₈ is solved"), and the "pure-WHIM pass" reading in CFG374's README. CFG376 and CFG378 inherit the bug.

### MAJOR

**2. CFG372's pass sits at an unconverged resolution (CFG366/372/374, all 256³ only).**
- CFG361 K4 FAILED: T5 gave 1.151 at 128³ and 1.205 at 256³, so the excess grows with resolution.
- The binding cut in CFG372 is P(k ≤ 1). A pass at a resolution where the excess is still rising is in the lenient direction.
- CFG372/README.md never mentions this.
- What it changes: GROWTH OK, even before finding 1, is not robust.

**3. Constant T and z ≈ 0 phase fractions are applied at all z (CFG372, CFG374).**
- WHIM forms at z ≲ 2. At z ≳ 2 the IGM is at about 1e4 K.
- Holding 1e6 K, or 54% hot gas, at all z suppresses the early phantom further, which compounds finding 1. Both biases point toward a pass.
- CFG374 discloses this in its scope. The STANDING growth summary and the working model do not carry it.

**4. CFG368's F2 and F4 forms were never tested: only p = 0 solved. The lane output (uncommitted, finished 20:16) presents them as NOT PREFERRED with Δχ² = 0.**
- **Where:** `CFG368_cold_de_flow_desi/cfg368_cold_de_flow.py:43`, the bracket `lo, hi = -5.0, 10.0` on the initial vacuum density at a = 1e-4.
- **Why it fails:** the ρ_c-tied flows need ρ_vac,ini of ~1e4 (F2) or ~1e9 (F4) ρ_crit0, which is still negligible against ~1e12 of matter. brentq therefore throws, and every |p| ≥ 0.025 is dropped.
- **With a wider bracket (audit_cfg368_bracket.out):**
  - F2 peaks at p ≈ −0.05 (vacuum → cold), with (w0, wa) = (−0.949, −0.332) and Δχ² PP/U3/DY5 = +4.22 / +2.97 / +3.97. That is NOT PREFERRED, because Union3 is below 4.
  - F4 at p = −0.025 gives +4.22 / +3.04 / +4.06, still rising at the last solvable point. Its peak is unresolved but probably similar. Ω_m,obs drifts to 0.38, which the declared scoring ignores.
- **What it changes:**
  - The lane verdict NOT SUPPORTED most likely survives.
  - The F2/F4 rows are wrong as written. The owner's question ("tied to dark energy or to the cold fluid?") is mis-answered: the cold-tied forms fit about as well as F1/F3 (+3.3 / +2.0 / +2.4 for F1).
  - F4 is also under-sampled by the 0.025 grid step.

**5. CFG374's README misstates the filter it compares against.**
- The README says "at k = 1 the census mix keeps 54% of the source, against 50% for pure WHIM".
- At z = 0 the pure 1e6 K filter at k = 1 is W = 0.17. It reaches 0.5 at k = k_J = 0.45.
- MIX-A keeps 3.2× more k = 1 source than pure WHIM, not 1.08×. That is the real reason CFG374 fails where CFG372 passed.

**6. STANDING (CFG374 entry) overstates the result: "σ₈ is solved (within 2%)".**
- The claim ignores findings 1–3.
- It is also only a ratio to the Newtonian S0 control at one resolution.

### MINOR

7. **CFG372 overdraw reported as null.** `cfg372_analysis.py:34` reads `overdraw_mass_frac`, but the engine writes `overdraw_mass`, so the overdraw in `cfg372_results.json` is null. The README says the overdraw is "not recomputed here", yet it was computed (audit_pm_ratios.out):
   - CFG372: 3.5% / 4.2% at 1e6 K, 18.8% / 21.3% at 1e4 K;
   - CFG374: MIX-A 9.8% / 11.9%, MIX-B 15.3% / 17.7%.
8. **CFG374 controls do not test the engine.**
   - The MUTATE is an algebraic identity (COLL1 gives W ≡ 1), not the frozen field-level test against T = 0. It cannot fail.
   - C1c compares the checker's own formula with itself.
9. **CFG368 K1 FAIL is a tolerance artefact.** dω_c = −1.18e-9 against a 1e-9 tolerance, with rtol 1e-10 over 9 e-folds. w0 and wa pass (8e-10, 6e-9). The script exits rc 1, and the outputs are uncommitted.
10. **CFG367 mass-error rule is inconsistent.** Masses quoted as "~" get ±50% (taken from Fig. 6 as 1σ), while measured masses get ±2σ.
    - Using [0.3c, 2c] for the "~" masses removes the 1.01–1.05e-19 sliver and opens 1.18–1.27e-17.
    - The light end (2.0–4.4e-20) is unchanged. It is set by PG0804+761, which has a measured mass.
11. **cm14b / cm15 EFE argument.** The EFE uses the total NFW host acceleration as the argument of ν.
    - A MOND EFE would use the Newtonian external field, i.e. 1/μ(g_e). With the simple μ that gives a boost of about 2.2, not 1.5.
    - Reading B (and SW01) is still excluded, at about 0.6 dex instead of 0.81.
    - r_bg is derived from m_bg itself (a weak circularity: the prediction goes as m_bg^(1/3)).
    - ν = √(1 + 1/y) is neither the simple nor the RAR form. This is negligible at y ~ 0.01.
12. **Working-model table cites a non-discriminating result.** It cites CFG361 CRIT ×1.50 / ×1.59 as evidence against a₀ ∝ H(z), but FLAT fails under the same bookkeeping (×1.205 / ×1.257). Its "decisive pending test: CFG372" section is stale; the forward note mentions CFG374 only.
13. **cold_mass IDs are reused.** cm12, cm13, cm14 and cm15 each label two or three different lanes, which makes citations ambiguous. The cm12 README header still reads "4 of 8"; this is superseded by its forward-fix section.

## Specific checks requested

- **(a) Is the filter consistent in time?** No; see findings 1 and 3. The comoving k_J has the wrong a-dependence, and the z ≈ 0 fractions are used at all z.
- **(b) Does the RES compensation conserve the k = 0 mode?** Yes, exactly.
  - In `cfg372_pm.py:310–312`, Wk(0) = 1 because k² is not regularised in that branch, so xk[0] = 0.
  - This is not a distinctive property: `ik2[0] = 0` drops the k = 0 mode of every PM source anyway.
  - Local positivity is violated wherever there is overdraw (finding 7).
- **(c) Is S0 identical?** Yes.
  - CFG359 S0 256³ uses the same IC code, seed 359, NSEED 256, z_i = 49, L = 200 and 150 steps.
  - The z_i P(k) is bitwise identical to S0 for all CFG366/372/374 runs, and for CFG361 too.
  - P(k) and σ₈ are measured identically: CIC-deconvolved, no shot-noise subtraction, which is negligible at k ≤ 1.
- **(d) CFG367 constants and rate.**
  - α constant: G M☉/c² / (ħc) = 1476.6 m / 1.9733e-7 eV·m = 7.483e9. The code's 7.49e9 is +0.09%, negligible.
  - Detweiler ×2: the code reduces to Γ = a α⁹/24 (C₂₁ = 1/48, g = 1 at small α). That is the occupation-number rate 2ω_I, with M ω_I = a α⁹/48 (the corrected Detweiler value). It matches a 200-e-fold occupation criterion. Near the superradiant edge the analytic rate underestimates the numerical one, which is conservative.
  - The validity fix is sound.
  - Table 1 transcription: all 32 mass-bearing objects match `r21.txt` (masses, asymmetric errors, spin lower edges).
- **(e) cm13 energetics: no error found.**
  - Units check out: a₀ in cgs; SN 1e49 erg per M☉ of stars; Kormendy & Ho 3.09e8 (σ/200)^4.38; σ = V/√2.
  - The log-potential with EFE cut-off is right: at r_e it equals G M/r_M = V².
  - At R = r_M the Newtonian term dominates the max rule. A hand recomputation of ε_need(MW), canonical R1 SN, gives 2.30, matching the output.
  - The STANDING phrases "38–250%" and "short by 4–250×" match the output: ε_need runs 0.377–2.53.
- **cm12 forward fix: verified.**
  - Tozzi & Norman's unit is 1e-22. Their T^0.5 term gives 5.8e-24 at 1 keV, against free-free emission of about 5.7e-24.
  - The n_e, n_H and μ bookkeeping is consistent.
  - The corrected output reproduces: PARTIAL 2/8, with the step at 10^12.3–12.7.

## Numbers in STANDING / WORKING_MODEL checked against JSON

These match: CFG366 (σ₈ 1.0095 / 1.0111, P 5.7% / 6.9%; R_c = 3: 1.034 / 1.040, P(k = 1) 1.29 / 1.35; overdraw 21–26%), CFG372 (1.009 / 1.011, 7.6% / 8.9%, 1e4 K 24% / 30%), CFG374 (1.015 / 1.019, 12% / 16%, MIX-B 19% / 24%), CFG361 (1.205 / 1.257, CRIT 1.50 / 1.59, K4 1.151), cm12 corrected and cm13.

There are no transcription errors. The problems are the physics and the overstatements above.

Rule kept: κ = ½ is fitted. The cold fluid is still required.
