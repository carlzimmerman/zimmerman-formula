# CFG917 FROZEN CRITERIA: the CMB-lensing gate on the theory-v2 1024³ runs (CFG649 checklist item 2 + a raw Planck PR4 bandpower statistic)

- **Written:** 2026-10-20, committed ALONE, before any CFG917 number was computed (no CFG917 script exists at this commit).
- **Block:** CFG910–919 (orchestrator reservation; CFG917 = "CMB-lensing gate" in the LEDGER reservation row, 376c629c7).
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻² are never pooled; each pair is scored on its own footing. "Cold
  energy" throughout; its MASS is required; no particle species. Not "theory closed". A CONSISTENT class never means the data favour the
  framework. Raw data, framework-native verdicts only: no ΛCDM fit result, no CAMB/CLASS nonlinear spectrum, no halofit / HMcode /
  BAHAMAS / halo model, and no "within X% of ΛCDM" yardstick enters any model or verdict.
- **Compute rule (a 1024³ job, chain7 NC2x, is live):** one process at a time, `OMP_NUM_THREADS=1`, `nice -n 10`, each process < 1 GB
  (measured with `/usr/bin/time -l` on the first call of each script; stop if > 2 GB). No running process is touched. Nothing is downloaded.
  The engine file names of CFG596/650/654 never appear on a command line (they gate the chain); Part A therefore scans byte-identical
  copies (sha256 checked) placed outside the repo in `_external_data/cfg917_work/`.

## 0. Disclosure: what was seen before this file was written

- CFG649 FROZEN_CRITERIA, README and `cfg649_cmb_safety.py` (read in full), including its published P1-vs-P0 numbers (canonical ΔA
  +0.0133 on Planck 2018 8–400 weights, bracket +0.0088…+0.0794, CONDITIONAL; coverage of the box ≈ 10% (z ≤ 1 and k in the box) and
  ≈ 15% (k in the box, any z) of the 8–400 band-weighted kernel).
- CFG654 FROZEN_CRITERIA, addenda A1–A3, README RESULT (NC1x vs NCS0: KiDS Δχ² −10.08, CONSISTENT; benchmark P_grav,NC1x/P_NCS0 at
  k = 0.3 / 0.5 / 1 h/Mpc = 0.972 / 0.961 / 0.949 at z = 0, 0.966 / 0.944 / 0.921 at z = 0.5, 0.964 / 0.932 / 0.891 at z = 1), and
  `cfg654_native.py` (native background, z > 1 growth continuation, k < k_lo continuation). CFG650 README (T1x −7.70, T2x −7.18,
  T2x benchmark 0.974 / 0.965 / 0.949 at z = 0). CFG592's `cfg592_native.py` library (node_P / Pmat continuation rules).
- Engine code read (Read tool): the IC routine (Gaussian random field: white noise × √P_lin0, Zel'dovich at z_i = 49, NOT fixed
  amplitude), `measure_pk` (CIC-deconvolved, linear bins of width k_f = 2π/L, bin n = [(n−½)k_f, (n+½)k_f), no shot-noise subtraction),
  and the CFG654 native-input switch (P_lin0 = the IC table's Plin0, D from the native ODE, E(a) with radiation + CFG630 trickle).
- Run JSONs (NC1x, NCS0, T1x, T2x, P0): keys, the `cosmo` dicts, the stored growth factors D at each snapshot, the k grid (first bins
  0.0802, 0.1402, 0.1969, 0.2551 h/Mpc). **No P(k) value of any run was printed or looked at.**
- The Planck PR4 lensing package on disk (README, .yaml, .dataset files, the 9 bandpowers with their Error and Ahat columns, both 9×9
  covariances, both linear-correction fiducial files, window formats, the package's unit test with its reference values −2 ln L = 8.368
  (CMB-marginalised) and 8.705 (with CMB spectra)). The typed Planck 2018 VIII MV band table in the committed XR26 script.
- System state at freezing: chain7 started NC2x at 10:33:47 (2026-10-20); `_external_data/cfg654_work/NC2x/` holds no run JSON.
  **NC2x is scored blind.**

## Part A. CFG649 checklist item 2, executed UNCHANGED

- Script: `campaign_fresh_gravity/CFG649_cmb_safety/cfg649_cmb_safety.py` (sha256 3ce5feb8b3086c9b…, not edited, not copied), its statistic
  ΔA = A_F/A_S0 − 1 on Planck 2018 MV 8–400 band weights, its 12-member bracket {base-1, base-2} × {Z-a, Z-b, Z-c} × {K-a, K-b},
  canonical (base-1, Z-b, K-a), labels SAFE / CONDITIONAL / UNSAFE(-ROBUST) at 2σ = 0.056 exactly as CFG649 froze them. The script also
  prints its Part A (A1 switch-off at z_i, A2 engine scan, A3 estimate); those are reported as its output.
- Order per pair: `CFG649_MUTATE=1` FIRST (outputs `cfg917_partA_<PAIR>_MUTATE.out/json`), then the normal run
  (`cfg917_partA_<PAIR>.out/json`), via the script's own `--f --s0 --tag --engine --out` options. Outputs go to this directory only.
- Pairs:
  - **NC1x vs NCS0** (`_external_data/cfg654_work/`; engine scanned = copy of `CFG654_independent_inputs/cfg654_pm.py`, sha256 7058f4333b8d4597…);
  - **T1x vs CFG596 P0** (engine copy of `CFG650_theory_v2_combined_pm/cfg650_pm.py`, sha256 8e2e477aeb0c670d…);
  - **T2x vs CFG596 P0** (same engine copy);
  - **NC2x vs NCS0**, DEFERRED: run only after chain7 writes `_external_data/overnight_chain/chain7_state/NC2x.ok`; commands left in the README.
- Known mismatches, reported as-is (the script is not edited): the script's background and linear spectrum are the inherited engine's
  (h 0.6736, Ω_m 0.3138, flat, no radiation; EH σ8 = 0.811). For the native pairs they enter only as weights of the measured F/S0 ratio
  (base-1/base-2, z > 1 and k > k_hi continuations) and in A3; the ratio itself is the native runs' own. The support top πN/(4L) is the
  runs' own (same N, L). A2's regex patterns were written for cfg596_pm.py; a NOT FOUND in the module engines is reported as printed
  and, per checklist 1(c), the README names the equivalent line by hand.

## Part B. A NEW raw-data statistic: each run's own C_L^φφ against the Planck PR4 lensing bandpowers

### B1. Data (primary, conservative range)

The package's `PlanckPR4LensingMarged` likelihood (Carron, Mirmelstein & Lewis 2022), files in
`_external_data/cmb_lensing_raw/planck_PR4_lensing/planckpr4lensing/data_pr4/` (sha256 prefixes in brackets):
- dataset `pp_consext8_npipe_smicaed_TiPi_jTP_pre30T_kfilt_rdn0cov_PS1_CMBmarged.dataset` [83d2c438…] (DEFAULT → `…_PS1.dataset` [64b318fc…]);
- bandpowers `…_PS1_bandpowers.dat` [712ffa48…], column PP = [L(L+1)]² C_L^φφ/2π, 9 bins, **L 8–400** (the conservative range; the
  only PR4 range on disk);
- covariance `…_PS1_CMBmarged_cov.dat` [f4db1c9f…] (CMB-spectra uncertainty marginalised; no calibration parameter);
- bin windows `…_PS1_window/window{1..9}.dat` [concatenated 0b528c0a…];
- linear N1/normalisation correction: windows `…_PS1_CMBmarged_lens_delta_window/window{1..9}.dat` [377cf288…] and fiducial values
  `…_PS1_CMBmarged_lensing_fiducial_correction.dat` [df4fe3c9…] — Planck's published linear fiducial correction, APPLIED.
- Binned theory (the package's CMBlikes rule): B_b = Σ_L W_b(L) X_L + Σ_L M_b(L) X_L − F_b, X_L = [L(L+1)]² C_L^φφ/2π, L = 2…2500.
- χ² = (B − d)ᵀ C⁻¹ (B − d), 9 bandpowers, no free parameter in either model → p from χ² with 9 dof.

**Aggressive range (robustness member AGG).** No PR4 aggressive file is on disk. AGG uses the Planck 2018 VIII Table 1 MV 8–2048
bandpowers as typed in the committed `real_research/cross_thread_review_2026_09_26/XR26_cmb.py` (14 bands, amplitudes A_b relative to
FFP10 and σ_A,b): A_b^model = ⟨X^model⟩_b / ⟨X^FFP10⟩_b (uniform averages over integer L in the band; FFP10 = the on-disk
`FFP10_wdipole_lenspotentialCls.dat` [a8410ac5…] PP column), χ² = Σ_b ((A_b^model − A_b)/σ_A,b)², diagonal (no covariance on disk),
no linear correction (none on disk for 2018), 14 dof. Disclosed as an approximate, older-release member.

### B2. Model: C_L^φφ from each run's MEASURED gravitating P(k, z)

- **Limber**, both arms identically: C_L = 4/(L+½)⁴ ∫₀^{χ*} dχ [1.5 Ω_m,X (H0/c)² (1+z)(χ* − χ)/χ*]² P̂_X((L+½)/χ, z), χ in Mpc/h,
  H0/c = 1/2997.92458 h/Mpc, z* = 1090, z ∈ [1e-3, 1089]; z grid = 400 log nodes on [1e-3, 1] and 600 log nodes on [1, 1089]
  (z = 1 shared); trapezoid in χ.
- **Run's own background, growth and linear spectrum.**
  - Native runs (NC1x, NCS0, NC2x): flat, Ω_cb 0.310403, Ω_r 9.106e-5, Ω_Λ (1 − CFG630 trickle), h 0.677698 (`cfg654_scorer_tables_cmb.npz`,
    = the engine's E(a)); D from the native lnD table; P_lin0 = the IC table's Plin0 (`cfg654_ics_tables_cmb.npz`), the engine's own
    log-log interpolation; Ω_m,X = Ω_cb.
  - Inherited runs (T1x, T2x, P0, P1): the engine's flat Ω_m 0.3138, h 0.6736, Λ, NO radiation; the engine's D(a) integral; EH σ8 = 0.811
    P_lin0 (engine code verbatim). Flagged inherited, as everywhere.
- **Measured nodes.** The five late snapshots a = 0.5, 0.5698, 0.6667, 0.7961, 1 (z = 1, 0.7548, 0.5, 0.2562, 0); field = the
  gravitating field P_grav (CFG555 definition) for BOTH arms (verdict); support = bins with k_b ≤ πN/(4L) (127 bins, 0.0802–7.98 h/Mpc,
  CFG649's rule).
- **Realisation-variance correction (declared, k ≤ 1 h/Mpc only).** The 1024³ box carries one Gaussian realisation (the first bin has
  9 independent modes). On support bins with k_b ≤ 1.0 h/Mpc the node spectra are P̂_X(k_b, a_n) = C_b P_grav,X(k_b, a_n) with
  C_b = P̄_lin0,X(b) D_X(a_i)² / P_grav,S0(k_b, z_i), where P̄_lin0,X(b) is the engine's P_lin0 averaged over the lattice modes of bin b
  (exact enumeration with the engine's binning) and D_X(a_i) the stored z_i growth factor; C_b = 1 above 1 h/Mpc. C_b comes from the S0
  arm and multiplies both arms (identical z_i fields, K4b), so P̂_F/P̂_S0 = P_grav,F/P_grav,S0 exactly. Fallback: if K5 fails for a pair,
  C_b ≡ 1 for that pair, flagged; the verdict proceeds.
- **Interpolation.** ln P̂ log-log in k between support bins; ln P̂ linear in a between adjacent snapshots.
- **k < k_lo = 0.0802 (primary K rule):** both arms = the run's own linear spectrum P_lin0,X(k) D_X(a)² (below the box's first bin the
  source is compensated and linear; F/S0 ≡ 1 there).
- **k > k_top = 7.98:** power law from the support top, slope fitted to ln P̂ vs ln k over bins k_b ∈ [k_top/2, k_top] at each node
  (CFG592/CFG649 rule).
- **z > 1 (above the last snapshot), primary:** each arm continues from its own z = 1 node with its own background linear growth,
  P̂_X(k, z) = P̂_X(k, 1) [D_X(z)/D_X(z = 1)]² — the shear scorers' rule (`cfg592_native.py` Pmat; native growth for the native runs as in
  `cfg654_native.py`). This holds each arm's z = 1 nonlinear shape and therefore holds F/S0 at its z = 1 value.

### B3. Statistic and classes

- **Δχ² = χ²(F) − χ²(S0)** on the primary data, per pair (positive = framework worse). Also reported: χ²(F), χ²(S0) and p (9 dof);
  per-band residuals; best-fit amplitude Â of each arm (context, no class role); coverage fractions of the S0 bandpowers from
  (i) z ≤ 1 and k in the support, (ii) z > 1 and k in the support, (iii) k < k_lo, (iv) k > k_top; the particle-field F (context: the
  lensing-vs-stability fork); the raw variant with C_b ≡ 1 (context).
- **Robustness set (declared now; each changes ONE thing; Δχ² of each = χ²_member(F) − χ²_member(S0)):**
  - **AGG** the aggressive range (B1).
  - **ZHOLD** the alternative z > 1 continuation holding the last-snapshot F/S0 ratio fixed: the S0 arm's nonlinear factor relaxes,
    P̂_S0(k, z) = P_lin0(k) D(z)² [1 + (T_S0,1(k) − 1) w(a)], T_X,1(k) ≡ P̂_X(k, 1)/(P_lin0(k) D(0.5)²), w(a) = clip((a − a_i)/(0.5 − a_i), 0, 1),
    a_i = 0.02; P̂_F = P̂_S0 × T_F,1/T_S0,1 (ratio fixed at z = 1). (Distinct from the primary, which already holds the ratio but keeps the
    full z = 1 nonlinear shape.)
  - **ZREL** both arms relax: P̂_X(k, z) = P_lin0(k) D(z)² [1 + (T_X,1(k) − 1) w(a)], so F/S0 → 1 at z_i (CFG649 Z-b analogue).
  - **KCUT** the k-support cut: measured spectra used only up to πN/(8L) = 4.02 h/Mpc, power law above (slope over [2.01, 4.02]).
    (The shear-type "≥ 90% of the integrand inside the support" cut cannot be applied: CFG649 found ≈ 15% of the 8–400 kernel inside the
    box support at any z, so it would keep no band.)
  - **KLOW** below k_lo the F arm carries the mean F/S0 ratio of the three lowest support bins at each snapshot (CFG649 K-b analogue);
    S0 stays linear.
  - **BG** the background variant: the distances χ(z) and χ* from the OTHER input set's background (native ↔ inherited); P̂_X, its
    growth and Ω_m,X in the potential stay the run's own.
- **Classes (as the shear scorer's):** EXCLUDED if Δχ² ≥ 9 and min(Δχ², robustness) ≥ 9; TENSION if Δχ² ≥ 4 (and not EXCLUDED);
  CONSISTENT if Δχ² < 4 and max(robustness) < 9; NOT DIAGNOSTIC otherwise, or if any gating K test fails, or if MUTATE does not bite.
  An absolute p(F) < 0.01 is flagged "ABSOLUTE MISFIT" next to the class (label only).

### B4. K identity tests (gating unless marked; each must PASS before any verdict)

- **K1** F ≡ S0 (the S0 JSON passed as both arms): Δχ² = 0 to ≤ 1e-12 on the primary and every robustness member.
- **K2** CFG649 reproduction through this code path: an emulation mode of this integrator (CFG649's base-1, Z-b, K-a; inherited
  background; z ∈ [1e-3, 50]; integer L 8–2048; uniform band averages; Planck 2018 8–400 weights 1/σ_A²) on CFG596 P1 vs P0 reproduces
  the stored canonical ΔA(8–400) in `CFG649_cmb_safety/cfg649_cfg596_P1_canonical.json` to ≤ 5e-4 absolute.
- **K3 likelihood and normalisation.**
  - K3a (reported): the PR4 windows applied to FFP10 PP vs PP_b/Ahat_b (Ahat printed to 3 decimals).
  - K3b: the fiducial-correction values equal Σ_L M_b(L) X_L^FFP10 to ≤ 2% per band.
  - K3c: no published χ² exists for the on-disk fiducial model file (FFP10), so the requested fiducial-χ² identity is N/A; K3e substitutes.
  - K3d: Limber normalisation — this code with the native linear spectrum (Plin0 × D², native background) reproduces CAMB 1.6.6's
    linear C_L^φφ at the native parameters (ω_b 0.02236, ω_c 0.1202, ln 10¹⁰A_s 3.045, n_s 0.9649, H0 67.770, massless ν N_eff 3.044,
    NonLinear off) binned with the PR4 windows to ≤ 3% in every band. (Linear CAMB is the framework-native IC generator of CFG654 §1;
    used here only as a normalisation check.)
  - K3e: the package's own unit-test value −2 ln L = 8.368 (`PlanckPR4LensingMarged`) is reproduced by this likelihood code from
    CAMB 1.6.6 at the unit-test parameters with lens_potential_accuracy 1 and halofit "mead", exactly as the package's test, to ≤ 0.15.
    This CAMB/halofit spectrum is a code-test input only; it enters no model, no Δχ² and no verdict.
  - K3d/K3e run in a separate script (`cfg917_camb_ktests.py`, one process) whose JSON the main script reads.
- **K4** (a) this code's D_X at every stored snapshot equals the stored D to ≤ 1e-5 relative; (b) P_grav,F(z_i) = P_grav,S0(z_i) to ≤ 1e-6
  relative in every bin; (c) the lattice mode-averaged |k| equals the stored k_b to ≤ 1e-5 relative on the variance-corrected bins;
  (d, reported) S0 max|P_grav/P − 1| per snapshot.
- **K5** (with the B2 fallback): x_b = P_grav,S0(k_b, z_i)/(P̄_lin0(b) D_i²) over the variance-corrected bins: reduced
  χ²_sv = (1/n) Σ_b (x_b − 1)² / (2/W_b) ∈ [0.2, 3.0] (W_b = the engine's mode weight sum of bin b) and |mode-weighted mean(x) − 1| ≤ 3 √(2/Σ W_b).
- **K6** grid convergence: doubling both z-node counts changes every reported χ² by ≤ 0.01.

### B5. MUTATE (`CFG917_MUTATE=1`, run FIRST, separate outputs `cfg917_<PAIR>_MUTATE.out/json`)

- **M1** F ≡ S0: Δχ² = 0 (≤ 1e-12), primary and every member.
- **M2** injected amplitude change on the P grid, P̂_F = (1 ± 0.10) P̂_S0 at all k, z: the pipeline's Δχ²± equal the independent
  binned-vector computation B± = (1 ± 0.10)(W + M)X_S0 − F to ≤ 1e-8 relative, AND (Δχ²₊ + Δχ²₋)/2 ≥ 9 (detection at ≥ 9, independent
  of where S0 sits relative to the data).
- **M3** (context, no bite requirement): CFG596 P1 vs P0 (the KiDS-EXCLUDED candidate B) through the Part B primary and members.
- MUTATE bites iff M1 is exact and both M2 conditions hold.

## ΛCDM dependence (disclosed as shared inputs; they do not cancel in a same-pipeline comparison)

- The PR4 reconstruction's normalisation (response), N1 bias, MC correction and covariance are computed at the FFP10 fiducial ΛCDM.
  Planck's published linear fiducial correction (B1) is applied; it corrects N1/normalisation to first order in C^φφ − C^φφ_FFP10 only.
  The CMB-marginalised covariance carries the CMB-spectra uncertainty of the package's construction.
- AGG's 2018 bands are amplitudes relative to FFP10 with no linear correction.
- Inherited runs: EH σ8 = 0.811 linear spectrum and a matter + Λ background without radiation (inherited ΛCDM-shaped inputs, flagged).
  Native runs: CFG654 §6 (the Planck TT,TE,EE+lowE base-ΛCDM-chain column; H0 from θ*; massless ν).
- The linear continuation below k_lo and the growth continuation above z = 1 ignore any framework nonlinear effect at z > 1 and on
  scales larger than the box. Bounded, not removed: ZHOLD and ZREL bracket the z > 1 rule; KLOW the large-scale rule; coverage
  fractions (ii) and (iii) state how much of each bandpower rests on these rules.
- No CAMB/CLASS nonlinear spectrum, halofit, HMcode or BAHAMAS enters any model or verdict (K3e's code test excepted, as stated).
- Limber at L ≥ 8 (shared by both arms).

## Scope and reading

- CFG917 has its own classes. It is NOT a CFG654 verdict input: CFG654 §5's CMB clause required a CFG649 raw-data statistic committed
  before the run was launched; that time has passed for NC12/NC1x, and the clause names CFG649, not this lane. CFG917 is reported next to
  CFG654 and CFG650. The NC2x pair is scored blind (B and A criteria frozen before its output exists).
- **Gate reading per pair:** PASS if Part B is CONSISTENT and Part A's canonical label is SAFE or CONDITIONAL; FAIL if Part B is EXCLUDED
  or Part A is UNSAFE(-ROBUST) (CFG649's committed rule); otherwise Part B's class (TENSION / NOT DIAGNOSTIC) as is. Never pooled across
  footings; a pass on one footing says nothing about the other.
- A PASS means only that this box's gravitating-field change is not detected by the PR4 8–400 bandpowers against the same-pipeline
  control; most of the CMB-lensing kernel lies outside the box (coverage reported) and rests on the declared continuations.

## Outputs

`cfg917_partA_<PAIR>[_MUTATE].out/json` (Part A), `cfg917_camb_ktests.out/json` (K3d/K3e), `cfg917_<PAIR>[_MUTATE].out/json` (Part B),
`README.md`. Every quoted number comes from a JSON. Any post-hoc change is a dated, labelled amendment; this file is never edited.

Commit rule: explicit paths only; no push. κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
