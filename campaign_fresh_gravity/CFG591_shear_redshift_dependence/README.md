# CFG591: CFG590's cosmic-shear test with a redshift-dependent framework/ΛCDM ratio R(k, z). Verdict (w = −1 primary): canonical NOT DIAGNOSTIC (M1 EXCLUDED, min Zmax 3.36; the M2 mapping reads CONSISTENT), alt EXCLUDED (min Zmax 6.22). Lane label: NO LABEL (control HZ1 failed; effect quantified below)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (455966295). **Addendum 1** (`FROZEN_CRITERIA_ADDENDUM_1.md`, 2026-10-10) adds the owner's DESI-tracking dark-energy variant. It was committed alone (see the commit log) before any R(k, z > 0), A_eff or class had been looked at. Date: 2026-10-10.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled. ν_mono, candidate B, G9. The cold energy's MASS is still required; no particle species. Not "theory closed"; nothing here says the data favour the framework. Nothing was downloaded; other lanes were read only.
- **Primary a0(z):** flat, the same at every z (w = −1, the framework's own prediction). The DESI-tracking variant is §5.
- All numbers come from `cfg591_halo_results.json`, `cfg591_results.json`, `cfg591_toy_results.json`, `cfg591_posthoc.json` and their `_DESI` versions. Pairs are canonical / alt.

## Scripts (all `nice -n 10`, ≤ 4 threads or processes)

| script | does | run time |
|---|---|---|
| `cfg591_lib.py` | the CFG556 namespace at epoch z: CFG556 exec'd read-only, epoch inputs overridden; CFG557/559 profile functions exec'd verbatim; s_c*(M_ta, z) via `cfg557_lib.s_catch` | — |
| `cfg591_toy.py` | CFG559's kinetic toy (`run_cell`, imported unchanged) rerun at z = 0.25–1.0. 72 cells, PRIMARY supply; the z = 0 tables are CFG559's, reused | 5.4 h |
| `cfg591_halo.py` | R(k, z) for PRIMARY, CFG557 TESTED, CFG556 cen / emg / r200scope at z = 0, 0.25, 0.5, 0.75, 1.0 | 1.5 min |
| `cfg591_shear.py` | `cfg590_shear.py` exec'd read-only with ONE function replaced (`R_of` → z-interpolated R(k, z)); CFG590's frozen rule. `CFG591_MUTATE=1` runs MZ1 / MZ2 (exit 1 = all teeth bite) | 2 min |
| `cfg591_desi.py` | Addendum 1: in-process patch of `cfg557_lib`'s background to flat w0waCDM; a0(z) tracking | — |
| `cfg591_posthoc.py` | post-hoc, not a verdict input: the effect of the HZ1 failure on R | 1.5 min |

Set `CFG591_DESI=1` to run any of the toy / halo / shear / posthoc scripts for the Addendum 1 variant (`_DESI` outputs).

## 1. R(k = 1 h/Mpc, z): the excess shrinks with redshift, but not fast enough on canonical

| z | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|---|---|---|---|---|
| PRIMARY canonical | 1.292 | 1.215 | 1.147 | 1.088 | 1.038 |
| PRIMARY alt | 1.378 | 1.302 | 1.228 | 1.161 | 1.104 |
| s(z) = (R(1, z) − 1)/(R(1, 0) − 1), canonical / alt | 1 / 1 | 0.736 / 0.800 | 0.504 / 0.604 | 0.300 / 0.427 | 0.131 / 0.275 |
| s_c* at log M_ta 14, canonical | 0.616 | 0.526 | 0.454 | 0.395 | 0.346 |
| emergent edge (CFG556 emg) can / alt | 0.988 / 1.086 | 0.925 / 1.031 | 0.876 / 0.987 | 0.834 / 0.946 | 0.798 / 0.906 |
| r200m scope can / alt | 0.918 / 0.952 | 0.922 / 0.929 | 0.955 / 0.950 | 0.974 / 0.972 | 0.986 / 0.984 |

- **Why it shrinks.** At earlier epochs the finite-age supply ceiling s_c* is smaller (the universe is younger: 0.62 → 0.35 at log M_ta 14 from z = 0 to 1), the concentrations are lower, and clusters (log M_ta 14–15, the CFG556 drivers) are rarer. The kinetic toy also spreads more at high z: r_99/r_ta at log M_ta 15 rises from 0.43 to 0.59 (canonical).
- **The emergent-edge excess turns into a DEFICIT at z > 0** (R(1) 0.80–0.93 on canonical, 0.91–0.99 on alt at z ≥ 0.5). Its edge moves outward with z (at log M_ta 15 from 0.53 to 0.74 r_ta, canonical), so the settled mass is spread wider than the reference NFW.

## 2. Effective A_mod and the frozen verdict (CFG590's rule, M1, feedback range log T_AGN 7.3–8.3)

| model | A_eff off (KiDS / DES) | A_eff at T 8.3 | Z at T 8.3 (KiDS / DES) | min Zmax | M1 class | systematics | **final class** |
|---|---|---|---|---|---|---|---|
| ΛCDM-DMO (R ≡ 1) | 1.000 / 1.000 | 0.783 / 0.782 | −1.45 / −0.94 | 0.58 (T 8.1) | CONSISTENT | all CONSISTENT | **CONSISTENT** |
| canonical PRIMARY, R(k, z) | 1.208 / 1.210 | 0.953 / 0.954 | +1.82 / +3.36 | 3.36 | EXCLUDED | M2 **CONSISTENT**, ℓ_max 3000 TENSION, ℓ_max 1000 and n(z) ±0.1 EXCLUDED | **NOT DIAGNOSTIC** |
| alt PRIMARY, R(k, z) | 1.352 / 1.354 | 1.067 / 1.069 | +4.02 / +6.22 | 6.22 | EXCLUDED | all EXCLUDED | **EXCLUDED** |
| (CFG590, fixed z = 0 R) canonical / alt | 1.305 / 1.455 (KiDS) | 1.033 / 1.152 | +5.27 (DES) / +8.24 | 5.27 / 8.24 | EXCLUDED | — | EXCLUDED / EXCLUDED |

- **The A_eff excess over ΛCDM** is ΔA = +0.208 / +0.352 (off), against CFG590's +0.305 / +0.455. In A_eff terms the redshift dependence keeps s_A = 0.68 (canonical) and 0.77 (alt) of the fixed-R excess (the same at every feedback setting). CFG590's crude post-hoc estimate was 0.78. The class thresholds from CFG590's scaled family were 0.64 (canonical) and 0.43 (alt). So canonical lands just above its exclusion boundary, and alt stays far above it.
- **canonical: NOT DIAGNOSTIC by the frozen rule.** Under the primary mapping M1 it is still EXCLUDED at every feedback setting: min Zmax is 3.36, set by DES at the strongest calibrated feedback, and KiDS alone would be +1.82. But the M2 mapping (the CFG526 k = 1, 2, 4 average at the single plane z = 0.5) reads CONSISTENT, and ℓ_max = 3000 reads TENSION. M2 sees only z = 0.5, where s = 0.50. The Limber M1 weights the lower-z lens planes, where the excess is larger. That is why the two mappings now disagree. In CFG590, with z-fixed R, they agreed. **Read plainly: canonical is excluded under the lensing-kernel mapping by a thin margin (3.36 against 3), and a cruder mapping does not exclude it.** No feedback setting in the search range 7.0–9.0 gives Z = 0 for either survey (Z = +2 is reached at T 8.26 on KiDS and 8.75 on DES).
- **alt: EXCLUDED**, robust to every declared mapping systematic.
- **The high-z tail does not matter.** With R ≡ 1 beyond z = 1 instead of R(k, 1) held, every class is unchanged (HIGH-Z-TAIL-SENSITIVE: no, all footings and survivors).
- **S8-equivalent (canonical PRIMARY):** 0.871 with feedback off and 0.850 at T 7.8 (CFG590 fixed R: 0.887 / 0.867; ΛCDM 0.829 / 0.811; KiDS / DES 0.759, recalled).
- **VARIANT-SENSITIVE (both footings).** CFG557 TESTED (sharp, s_c*(z)) and CFG556 cen stay EXCLUDED with R(k, z) on both footings (min Zmax 6.43 / 9.39 and 9.12 / 13.79). The emergent edge is TENSION (canonical; now too LOW: A_eff 0.71 with no feedback, Z −2.83 / −2.69) and CONSISTENT (alt) under M1. The CFG559 full-supply kinetic variant was not rerun at z > 0; at its fixed z = 0 R it is EXCLUDED (CFG590).

## 3. The survivors (emergent edge, r200m scope) with R(k, z)

| survivor | canonical M1 (min Zmax) | canonical final | alt M1 (min Zmax) | alt final |
|---|---|---|---|---|
| emergent edge (CFG556 emg) | TENSION (2.99, too LOW) | NOT DIAGNOSTIC | CONSISTENT (1.01; \|Z\| < 2 at T 7.3–7.7, inside the fiducial band) | NOT DIAGNOSTIC (M2 EXCLUDED) |
| r200m scope | CONSISTENT (1.50; \|Z\| < 2 at T 7.3–7.5 only, outside the fiducial band) | NOT DIAGNOSTIC (ℓ_max 3000 TENSION) | CONSISTENT (0.75; T 7.3–7.7) | NOT DIAGNOSTIC (M2 TENSION) |

- **Both survivors now sit on the LOW side.** Their A_eff with no feedback is already 0.71–0.83 (emergent) and 0.79–0.83 (r200m), so they tolerate only weak feedback. In CFG590 (fixed R) both were CONSISTENT under M1. With R(k, z) the canonical emergent edge slips to TENSION (too little power), and every survivor reading is NOT DIAGNOSTIC once the mapping systematics are included.

## 4. Controls and MUTATE

- **HZ0** (the z-generalised machinery at z = 0 reproduces the stored CFG559 PRIMARY_kin, CFG557 TESTED and CFG556 cen / emg / r200scope R): max |ΔR| = 0 on both footings. **PASS.**
- **HZ1: FAIL (mass conservation).**
  - σ8(P_lin, z) = 0.811 D(z) to 1.1e-4 at every z. I(k = 1e-3) = 1 to ≤ 4.3e-7.
  - Mass conservation of the PRIMARY is ≤ 4.6e-16 at z ≤ 0.75 but **0.33 at z = 1**.
  - The cause: 13 (canonical) / 3 (alt) halos at log M_ta ≥ 16.16 / 16.42 have a supply edge reaching r_ta (capped). CFG559's `frame_profile_kin` then adds M_set Δm(r/r_e) with r_e clamped to r_ta, so Δm(1) ≠ 0 at r_ta. That code path never triggered at z = 0.
  - **By the frozen §4 the lane is NO LABEL.**
  - Post-hoc (`cfg591_posthoc.py`, not a verdict input): switching the kinetic term off in exactly those halos changes R(k, z = 1) by at most 1.3e-11 / 2.2e-16 (canonical / alt; DESI variant 2.1e-11 / 2.2e-16). Halos at log M_ta > 16 have essentially zero abundance at z = 1, so the class reading above is unaffected.
- **Toy:** C6 (m_sharp(1) = 1) 2.2e-16 and C7 (mass exact) pass in all 72 new cells. **10 of 72 cells fail CFG544's steadiness gate:** log M_ta 15 at z = 0.5, and log M_ta 14.5 and 15 at z = 0.75 and 1.0, both footings. In each, |D| = 0.10–0.16: the settled density is still below the law's. As frozen, their Δm is used without substitution.
- **CFG590's controls** C1–C4 re-executed: PASS (σ8 0.81100, fit identity 0, ΛCDM A_eff monotone in T, R(1e-3) = 1).
- **MUTATE (all bite, exit 1):**
  - **MZ1:** R(k, z) := R(k, 0) at every node reproduces CFG590's stored A_eff table for the PRIMARY and all four variants with max |ΔA| = 0, and every M1 / final class.
  - **MZ2:** R ≡ 1 as a 2-D table reproduces ΛCDM exactly (|ΔA| = 0, CONSISTENT).

## 5. Addendum 1: a0(z) tracking DESI DR2 w0wa dark energy (declared variant; side by side; no verdict authority)

- **Setup** (Addendum 1):
  - Flat w0waCDM with (w0, wa) = (−0.752, −0.861), the DESI DR2 + CMB + DES-Y5 posterior mean, read from CFG549's JSON.
  - a0(z)/a0(0) = √(ρ_DE ratio) = 1.055 / 1.059 / 1.040 / 1.008 at z = 0.25 / 0.5 / 0.75 / 1.0 (0.861 at z = 2).
  - Ω_m, h, ω_b, n_s and σ8(0) are kept at CFG556's values. The background (H, age 13.70 Gyr, growth, spherical collapse, Δ_ta, EPS, s_c*, mass function, bias inputs) is recomputed in w0wa.
  - The toy was rerun at all 5 epochs (90 cells; 9 fail CFG544's steadiness gate, the same high-mass, high-z corner as the primary).
  - The projection uses CAMB HMcode-2020 DMO + BAHAMAS feedback in the same w0wa background (PPF).
- **For context only:** the other DR2 chains give a0(0.5)/a0(0) = 1.032 (Pantheon+), 1.089 (Union3) and 1.179 (CMB-only). They were not run.

| | w = −1 PRIMARY canonical | DESI-tracking canonical | w = −1 PRIMARY alt | DESI-tracking alt |
|---|---|---|---|---|
| R(k = 1) at z = 0 / 0.25 / 0.5 / 0.75 / 1.0 | 1.292 / 1.215 / 1.147 / 1.088 / 1.038 | 1.291 / 1.236 / 1.168 / 1.102 / 1.040 | 1.378 / 1.302 / 1.228 / 1.161 / 1.104 | 1.378 / 1.319 / 1.248 / 1.176 / 1.107 |
| ΔA_eff vs the comparison model, feedback off (KiDS) | +0.208 | +0.230 | +0.352 | +0.373 |
| min Zmax over T 7.3–8.3 (M1) | 3.36 | 3.80 | 6.22 | 6.64 |
| M1 class | EXCLUDED | EXCLUDED | EXCLUDED | EXCLUDED |
| final class (mapping systematics) | NOT DIAGNOSTIC (M2 CONSISTENT) | NOT DIAGNOSTIC (M2 CONSISTENT) | EXCLUDED | EXCLUDED |
| S8-equivalent, off / T 7.8 | 0.871 / 0.850 | 0.875 / 0.854 | 0.896 / 0.874 | 0.899 / 0.878 |
| emergent edge: M1 (min Zmax) → final | TENSION (2.99) → NOT DIAGNOSTIC | TENSION (2.64) → NOT DIAGNOSTIC | CONSISTENT (1.01) → NOT DIAGNOSTIC | CONSISTENT (0.65) → NOT DIAGNOSTIC |
| r200m scope: M1 (min Zmax) → final | CONSISTENT (1.50) → NOT DIAGNOSTIC | CONSISTENT (1.48) → NOT DIAGNOSTIC | CONSISTENT (0.75) → NOT DIAGNOSTIC | CONSISTENT (0.61) → NOT DIAGNOSTIC |
| comparison model (R ≡ 1) + feedback | CONSISTENT | CONSISTENT | — | — |

- **The DESI-tracking variant makes the framework slightly WORSE, not better.** a0 is 4–6% higher at z = 0.25–0.75. That raises the law's phantom at a given baryon mass. The w0wa growth also makes halos at z > 0 slightly more abundant at fixed σ8(0) (D(0.5) 0.774 against 0.769). R(k = 1) rises by +0.02 at z = 0.25–0.5.
- The classes are identical to the primary on both footings, so the result is **not DE-SENSITIVE**. canonical stays NOT DIAGNOSTIC (M1 EXCLUDED at 3.80) and alt stays EXCLUDED (6.64).
- **The comparison model in the same background** has A_eff and its CONSISTENT class essentially unchanged: A_eff is a ratio fit to that background's own DMO and linear spectra. The A_mod data were derived in ΛCDM; this is disclosed, not corrected.
- **Addendum MUTATE:**
  - **MD2 bites.** The DESI code path at (w0, wa) = (−1, 0) with R ≡ 1 reproduces CFG590's ΛCDM A_eff table, max |ΔA| = 0.
  - **MD1 FAILS its frozen tolerance.** At (−1, 0) and z = 0.5 the DESI background reproduces the w = −1 path to 8e-13 in D, 0 in age and 2.5e-12 in Δ_ODE, but the s_c* grid differs by up to 4.3e-6 relative against the frozen 1e-6. The cause is that `cfg557_lib.s_catch` itself converges only to |Δs_c| < 1e-6 and interpolates the crossing shell. A 1e-12 change in the trajectory tables therefore moves s_c* at the 1e-6 level. The tolerance was set below the solver's own precision. The failure is recorded and not re-thresholded. It is ~4e-6 in s_c and has no effect on any class.
- The DESI run has the same HZ1 mass-conservation failure at z = 1 (13 / 3 capped halos above log M_ta 16.16 / 16.42). Its effect on R is ≤ 2.1e-11 (`cfg591_posthoc_DESI.out`).
- Print artefacts (the frozen JSON is correct): `cfg591_halo_DESI.out` prints "HZ0 … nan -> FAIL" (HZ0 does not apply to the variant; the JSON records "n/a"), and its header and the toy header say "flat a0 (w = −1)". The DESI cells and spectra use the tracking a0 (`a0_ratio` and `desi` in the JSON).

## 6. Inherited ΛCDM-calibrated ingredients (stated as assumptions, owner's request 2026-10-10)

The halo model is built from ΛCDM N-body calibrations, applied unchanged to the framework and to the comparison model at every epoch:
- **Mass function:** Tinker et al. 2008 (Δ = 200m) and its z evolution, calibrated on ΛCDM dark-matter-only simulations. The framework's own halo abundance is not derived; R3 (mass conserved inside r_ta) and "outside B ∩ C cold energy is cold matter" are the arguments for using it (CFG557).
- **Linear bias:** Tinker et al. 2010, ΛCDM-calibrated.
- **Concentration–mass relation:** Duffy et al. 2008, (1 + z)^−1.01, ΛCDM-calibrated. It sets both the ΛCDM reference profile and the turnaround catchment (r_ta, M_ta) of the framework halo.
- Also inherited: the EPS main-progenitor form (Neistein+06, q = 2.2) behind s_c*; Moster+13 stellar masses with their z evolution; the CFG416 census retention f_ret (z-independent); CAMB HMcode-2020 (DMO and BAHAMAS feedback) for P_NL and S_fb.
- These are the same for both models, so they largely cancel in R. They do not cancel in the turnaround catchment. In the DESI variant they are evaluated on the w0wa background, but they are not recalibrated for it.

## 7. Disclosures (dated 2026-10-10; frozen text not edited)

1. **Recalled, PROVISIONAL inputs:** the Tinker08 z-evolution, Duffy08 (1 + z)^−1.01 and Moster13 z-evolution parameters; the A_mod data (KiDS-1000 0.858 ± 0.052, DES Y3 0.82 ± 0.04), the n(z) means and the survey noise, all as in CFG590.
2. **Toy age.** The toy is run to T = 10 Gyr at every epoch (the bench end state), although the universe is 8.6 / 7.1 / 5.9 Gyr old at z = 0.5 / 0.75 / 1. The finite age enters only through s_c*. The 10 non-steady cells (§4) are at the high-mass, high-z corner.
3. **Pickling fix before the first toy run completed.** The first toy launch failed at once (worker processes could not pickle `run_cell` from the spec-loaded module). `cfg559_toy` was registered in `sys.modules` and the run restarted. No cell had run.
4. **The toy's header line says "flat a0" also in the DESI run.** That is print text only; the DESI cells use the tracking a0 (`cfg591_toy_DESI_results.json`, settings.desi and the per-cell s_c*, r_*).
5. **Addendum 1 MD1 tolerance.** See §5.
6. **Addendum 1 code was added while the primary toy was running.** `cfg591_lib.py` (the `DE` hook) and `cfg591_toy.py` (the `CFG591_DESI` switch) were edited after the primary toy had started; the running process used the earlier in-memory code. With `DE = None` the added lines are identities (ρ_DE ratio 1, √1 = 1). `cfg591_halo.py` and `cfg591_shear.py` ran the primary with the final code, and HZ0 = 0 confirms the z = 0 path is unchanged.
7. **The emergent-edge s(z)** is not meaningful (R(1, 0) − 1 = −0.012 / +0.086 is near zero); its R(k, z) is used directly.

Commits: criteria 455966295; Addendum 1 ab84fd0b9; results in the commit that adds this README.
