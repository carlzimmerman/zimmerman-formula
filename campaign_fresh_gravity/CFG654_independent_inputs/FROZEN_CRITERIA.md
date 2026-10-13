# CFG654 FROZEN CRITERIA: the "independent-inputs" 1024³ rerun of CFG650 T12 and its S0

Date: 2026-10-12. Committed ALONE, before any CFG654 native-input PM number at any resolution was seen (the 256³ native
validation runs VNs / VN12 start only after this commit) and before any 1024³ run. This file is never edited; dated
disclosures go in the README. κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. "Cold energy" throughout;
its MASS is still required; no particle species. Not "theory closed". Nothing here may say the data favour the framework. No
ΛCDM fit result (σ8 at z = 0, late-time Ω_m or H0 fits) and no ΛCDM nonlinear/collapse machinery (HMcode, BAHAMAS, mass functions,
EH fitting shape, the ΛCDM-shell Δ_ta table, ΛCDM back-scaled growth) enters the verdict.

## 0. Disclosure: what was seen before this file was written

- astra's audit `sol61_push/lcdm_dependency_audit_2026_10_12/RESULT.txt` (items A–E), read as data; CFG596 RESULT (canonical KiDS
  Δχ² +68.73, EXCLUDED; DES NOT DIAGNOSTIC); CFG636 RESULT (+13.97, EXCLUDED); CFG650's 256³ previews and its T12 addendum (A1).
- This lane's input products (all committed next to this file in the build commit): `cfg654_ics.out` (native parameters; IC
  amplitude vs the σ8 = 0.811 normalisation: σ_R(z_i) ratio 1.030 / 1.041 / 1.044 at R = 8 / 2 / 0.5 Mpc/h; implied LINEAR σ8 0.827),
  `cfg654_delta_ta.out` (native Δ_ta within +0.07% to +0.74% of cfg361), and the scorer-only POST-HOC re-scoring of the stored
  CFG596 P1 / CFG636 C1 runs (`cfg654_native_posthoc.out`). None of these is an outcome of the runs frozen here.
- Smoke tests of the native engine path at 64³ (3 steps; numbers not used).

## 1. The principle

The framework's early universe (before any bound system; switch off, CFG649) is GR + photons + neutrinos + baryons + cold energy
(cold matter) + dark energy, with a₀ irrelevant. Linear perturbation physics in that era is the framework's OWN physics; CAMB run in
that era with independently measured early-universe numbers is therefore a framework-native IC generator, not a ΛCDM assumption.

## 2. Inputs (frozen; `cfg654_ics_tables.npz` sha256 58a0e0a4…ab8d, `cfg654_delta_ta.json` sha256 462a7c14…fbf7)

| input | value | provenance |
|---|---|---|
| T_CMB | 2.7255 K | FIRAS (Fixsen 2009) |
| ω_b | 0.021932 | BBN: Cooke+18 D/H inverted with CAMB 1.6.6's PRIMAT 2024 table (CFG642 d1) |
| ω_c | 0.1202 | Planck 2018 VI (1807.06209) Table 2, TT,TE,EE+lowE (no lensing reconstruction, no BAO) |
| A_s, n_s | ln(10¹⁰A_s) = 3.045, n_s = 0.9649 (pivot 0.05 Mpc⁻¹) | same column |
| H0 | 67.403 (h = 0.674027), DERIVED from 100θ* = 1.04109 (same column) in the framework background | flat, radiation (N_eff 3.044 massless), Λ + CFG630 trickle |
| Ω_cb, Ω_r, Ω_Λ | 0.31285, 9.21e-5, 0.68706 | derived |
| linear spectrum at z_i = 49 | CAMB 1.6.6 linear δ_cb, A_s-normalised; P_lin0 = P(k, z_i)/D(a_i)², D, f from the native growth ODE | no σ8, no EH |
| Δ_ta(z) | native shell in the native background, law off until turnaround (the engine switches the law on at this threshold) | cfg654_delta_ta.py N0 |
| catchment conversion | Ω_m, h native (OM_TA = Ω_cb, H_TA = h) | replaces 0.315 / 0.674 |

## 3. Runs (DEFINED, NOT STARTED by this lane; the orchestrator decides queue order)

- **N12** = CFG650 T12 module set (M1 + M2, M3/M4 off), RES canonical; **NS0** = S0 canonical. Both: `cfg654_pm.py`
  (sha256 e425f837…af89, = cfg650_pm.py 771d556c… + the CFG654_INPUTS switch) with `CFG654_INPUTS=native`, L = 100 Mpc/h, N = 1024,
  NSEED 1024, seed 359, RMIN 0.78125, lean, spill, 14 threads, nice 10, CFG596's 150-step grid and snapshots. Launcher `run_654.py`
  (sha256 4518ada7…0bde): `python3 run_654.py serial NS0 N12`. NS0 SHARES the native ICs (same seed, same tables): the S0 for N12 is
  NS0, never CFG596 P0.
- **Start condition:** no cfg596/636/640/650/654 engine process running; free + inactive memory ≥ 48 GB; free disk ≥ 18 GB. Nothing
  is killed. **Abort:** RSS > 52 GB or swap growth > 4 GB (run_654.py guards, = run_650.py).
- **Gate before production:** the 256³ reproduction control V-R (section 4) must PASS.

## 4. Validation (256³, ONE process ≤ 3 GB, nice 10; `cfg654_validate.py`)

- **V-R (must pass):** CFG654_INPUTS=inherited, all modules OFF equals CFG596 VLr bit for bit (every stored snapshot quantity).
- **V-N1 (must pass):** VNs z_i particle P(k)/VLs z_i P(k) equals the predicted native/inherited ratio to ≤ 3% at k ≤ 1 h/Mpc.
- **V-N2 (must pass):** fundamental-mode growth of VNs over the native linear D² within 5% at z = 1, 0.5, 0.
- **V-C (must pass):** VN12 finite; |src_sum|/e_sum ≤ 1e-5 at z = 1, 0.5, 0.
- **Preview (reported, NOT a verdict):** VN12/VNs and CFG650 VM12/CFG596 VLs, P_grav/P_S0 − 1 at k 0.3/0.5/1. Never used to choose.

## 5. Statistic, data and verdict (`cfg654_native.py --score N12 NS0`, sha256 c3218d7b…2b14)

- **Scorer:** CFG592's library exec'd with the NATIVE patch (`load_lib("native")`): distances and dχ/dz from the framework background
  (section 2), lensing-kernel and IA Ω_m = Ω_cb native, P(k) continuation above z = 1 with the native linear growth, k < k_lo
  continuation with the native CAMB z = 0 linear shape matched at k_lo. Data, covariances, n(z), published cuts, support cut (≥ 90%
  of the integrand in [k_lo, πN/(4L)]; N_kept < 10 → NOT DIAGNOSTIC), nuisances, fit and classes are CFG592/596's, unchanged.
- **Models:** framework = N12's measured gravitating P(k, z) at z = 0, 0.5, 1; S0 = NS0's particle P. Δχ² = χ²_min(N12) − χ²_min(NS0),
  IA marginalised, per survey; positive = framework worse.
- **Robustness set:** widen2, noIA, held, **LOC** (distances of the same background with H0 = 73.04, ω_m fixed — the SH0ES bracket).
  The DESI+CMB+DES-Y5 CPL-chain distance variant is REPORTED ONLY (it is a fit including late-time data).
- **Classes:** EXCLUDED (Δχ² ≥ 9 and robustness minimum ≥ 9); TENSION (Δχ² ≥ 4); CONSISTENT (Δχ² < 4 and robustness maximum < 9);
  NOT DIAGNOSTIC otherwise, or N_kept < 10, or failed T-OWN.
- **T-OWN tooth and NZ1:** unchanged in form (S0 best-fit mock × CFG530 L100 N512 own boost must refit to χ²_min ≥ 9; source-zero path
  reproduces S0 to |Δχ²| ≤ 1e-9); `CFG596_MUTATE=1 … --score` runs FIRST.
- **CMB-lensing gate:** if CFG649 commits a raw-data CMB-lensing statistic (e.g. on the Planck PR4 bandpowers now on disk) before N12
  is launched, it is executed unchanged on N12's P_grav(k, z) and its class enters like a survey class; otherwise NOT EVALUATED (stated).
- **Benchmark (no verdict weight):** G = max_{k ≤ 1}|P_grav,N12/P_NS0 − 1| at z = 0 (0.5, 1 reported), labelled "benchmark vs the
  native-input S0 control, not an observational exclusion".
- **Verdict (canonical footing only; raw data only):** FAILS if any diagnostic survey (or the evaluated CMB gate) is EXCLUDED; PASSES
  the shear side on this footing only if CONSISTENT on ≥ 1 diagnostic survey and none EXCLUDED or in TENSION; otherwise TENSION /
  NOT DIAGNOSTIC. A shear-side pass of the theory needs the alt footing too (not frozen here). T12 is a post-preview selection
  (CFG650 addendum A1) and is labelled so; T1 stays CFG650's primary.
- **Reported, no verdict weight:** N12 − CFG650 T12 and NS0 − CFG596 P0 differences (input sensitivity), if those runs exist.

## 6. What remains shared or inherited (the verdict is conditional on these, stated with it)

Shared with every theory: GR in the early universe; the measured BBN and CMB-primary numbers of section 2. Residual model
dependence: the Planck TT,TE,EE+lowE column comes from a base-ΛCDM chain (Λ-constant late background = the framework's own; but the
late-time lensing smoothing of the peaks is computed with ΛCDM clustering); H0 inferred from θ* in the framework background (the
framework does not predict H0; the SH0ES value enters only as the LOC robustness variant); massless neutrinos in the PM (0.06 eV
bracket reported in cfg654_ics.out); the census f_ret law and floor (CFG515, empirical); M2's cooling inputs (Tozzi & Norman Λ(T),
μ, n_e/n_H); the footings (not rebuilt; rebuilt canonical value 9.372e-11 reported); survey nuisance priors and covariances; the
CFG530 boost used by the T-OWN tooth (a sensitivity tooth, not a model input); seed 359. A same-pipeline S0 does not cancel shared
inputs (astra, exact check).

## 7. Outputs

`cfg654_native_N12[_MUTATE].out`, `cfg654_native_results_N12[_MUTATE].json`; runs in `../_external_data/cfg654_work/{NS0,N12}/`.
Every quoted number comes from a JSON.
