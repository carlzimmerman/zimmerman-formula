# CFG909 FROZEN CRITERIA: how much do the ΛCDM-derived inputs in the cosmic-shear SCORING move the theory-v2 shear verdict? (committed alone, before any script)

**Why.** CFG650 scored the theory-v2 1024³ runs T1x (canonical) and T2x (alt) against raw KiDS-1000 and DES Y3 cosmic
shear with CFG592's native machinery: KiDS Δχ² (F − S0) −7.70 canonical / −7.18 alt, CONSISTENT on both footings; DES
NOT DIAGNOSTIC (T-OWN fails). An audit listed three ΛCDM-derived elements in that scoring:
1. inherited ΛCDM-shaped initial conditions and background (the native-input rerun NC1x addresses this; **not this lane**);
2. Ω_m fixed in the projection at the PM value (CFG592 README: "Ω_m is fixed (0.3138), whereas the papers marginalise it");
3. the published KiDS-1000 covariance, computed by the KiDS team at a fiducial ΛCDM cosmology.

This lane rescores the **existing, already-scored** T1x/T2x outputs with elements (2) and (3) varied, and reports whether the
CONSISTENT class survives. No simulation is started. NC1x is not read, run or touched.

## Inputs (read only)

- Runs: `_external_data/cfg650_work/T1x`, `T2x` (framework), `_external_data/cfg596_work/P0` (matched control S0), exactly as
  `cfg650_native.py`'s `runs_list()` selects them (asserted: the T1x/T2x RES files exist, so it picks T1x and T2x).
- Scorer: `CFG650_theory_v2_combined_pm/cfg650_native.py` (git blob 211b36aba3925588c5267b98cbf22f01548656f4) is read as
  text, checked against that blob hash, and its preamble is exec'd up to (not including) its single line `def strip(r)`.
  That preamble execs CFG592's library (`cfg592_native.py`, blob 437bc9524d358dd97c4e1990d7706869b8b03111) unchanged and
  defines `build`, `runs_list`, `Binj`. Nothing after that cut (scoring, file writes) is executed. Environment forced:
  `CFG596_MUTATE=0`, `CFG650_SCORE=T`, `CFG650_JOBSET` unset, no `--test530`.
- K1 targets: `cfg650_native_results.json` (blob c2802e71b278ad1b2fbad39dd2ee36f870d50153) and
  `cfg650_native_results_MUTATE.json` (blob 7504357698f81f49eaa0e4fe35d875e07ea6f32c).
- Data: only what CFG592's library reads (KiDS-1000 xipm FITS + covariance + SOM matrix, DES Y3 2pt FITS + scale cuts, DESI
  DR2 chain median). No downloads.
- Nothing in CFG592/650/654, LEDGER.md, THEORY_CANONICAL*.md or `_external_data/overnight_chain/` is edited. All outputs are
  written in this lane's directory.

## A. Projection Ω_m

**Definition (what "projection Ω_m" changes).** The library's global Ω_m (as scored: (ω_b + ω_c)/h² = 0.3137721…, used
as the exact float) is replaced by Ω_m,v in:
- A1 the PM background distances χ(z), dχ/dz (same flat w = −1 form, `background(Ω_m,v)`);
- A2 the lensing-efficiency prefactor (3/2) Ω_m (H0/c)²;
- A3 the NLA intrinsic-alignment factor C1 ρ_crit Ω_m / D(z), with D(z) recomputed at Ω_m,v by the library's own growth
  integral (exact for this background form).

**Not changed:** the simulated P(k, z) nodes (both arms were evolved at Ω_m = 0.3138; they cannot be re-evolved here), their
z > 1 growth continuation (it describes the simulated runs, so it keeps the as-run growth), the k < k_lo EH shape (the runs'
own IC shape, normalised to each run's lowest bin), the k-units (h/Mpc with χ in Mpc/h, so h drops out), and the 'DESI'
robustness member's own chain-median distances (its lensing/IA prefactor does follow Ω_m,v). The variant is applied
identically to the framework arm and the control arm.

**Grid:** Ω_m,v ∈ {0.2806, 0.2976, 0.3085, 0.3137721 (as scored), 0.3308}.
- 0.2976 = CFG886's no-CMB measurement (DESI DR2 BAO + BBN, flat a0), ± 0.0085;
- 0.3085 = CFG682's flat-a0 row (described by the audit as a forecast row; included as an intermediate value only);
- bracket: CFG886's ±2σ applied below the lowest and above the highest value: 0.2976 − 0.017 = 0.2806, 0.3138 + 0.017 = 0.3308.

**Kept data points.** PRIMARY: the as-scored kept set (support fraction ≥ 0.9 computed at the as-scored projection), so the
Δχ² shift isolates the projection. ALSO SCORED: the support cut re-derived at Ω_m,v (if the kept set is identical, the
primary numbers are reused). Both are class-weighted.

**Limitation (stated in the README):** changing Ω_m in the projection while keeping P(k, z) from runs evolved at 0.3138 is
not a self-consistent cosmology change; the papers' marginalisation varies P(k) too. This variant measures only how much
the projection's fixed Ω_m moves the relative statistic. A consistent change needs new runs (NC1x's native background is
the record's route for that).

## B. Covariance

**Facts about the published file (checked tonight, read only).** The KiDS-1000 xipm FITS contains ONE total covariance
(`COVMAT`, 270 × 270); the release (data_fits + chains_and_config_files/main_chains_iterative_covariance) contains no
Gaussian / non-Gaussian / super-sample split. The release's config names the data file `fits_iterative_covariance/...`,
i.e. the covariance was iterated toward the best fit of KiDS's own ΛCDM + HMcode chain; the release's xipm `maxpost` file
lists that chain's best fit as its start values (S8 0.768, Ω_m 0.206, σ8 0.928; read, not used in any computation). The
exact cosmology at which the released matrix was evaluated is not stated in the release. Therefore:
**GAUSS-ONLY (Gaussian term only) is NOT AVAILABLE** from the published products, and is not attempted. The DES Y3
covariance is likewise a single total matrix (the 400 × 400 cosmic-shear block is used as scored).

Notation: C = the published covariance restricted to the kept points; t_X = the best-fit theory vector (at the best-fit
nuisances, the `t` returned by CFG592's `fit`) of arm X; r = per-point signal ratio, clipped to [0.5, 2] (number clipped
reported; expected 0); R^p = diag(r^p). The reference signal t_ref is the control's best fit with the published C in the
same configuration — the in-pipeline stand-in for the published fiducial signal (the KiDS fiducial is itself a best fit to
the same data). No ΛCDM nonlinear model (HMcode etc.) is used to build any reference.

Leading-order cosmology dependence of a Gaussian covariance: the cosmic-variance term ∝ signal², the signal × shape-noise
term ∝ signal, the shape-noise term ∝ signal⁰. Because the file is not split, rescaling the whole matrix by R C R
(p = 1) is an UPPER bracket (it also scales the shape noise) and R^½ C R^½ (p = ½) a LOWER bracket of the signal-dependent
part.

- **B1 CV1-COMMON (class-weighted).** One covariance for BOTH arms, re-evaluated at the framework's predicted signal:
  r = t_F / t_S0,pub (main configuration), C' = R C R, iterated twice (r₁ from the published-C fits, r₂ from the F refit under
  C'₁; t_ref fixed). Final C'₂ is used for both arms and every robustness member. Convergence max|r₂ − r₁| reported.
- **B2 CVh-COMMON (class-weighted).** As B1 with p = ½.
- **B3 CV1-OWN (class-weighted).** Each arm scored with a covariance at its OWN predicted signal: in every configuration,
  C_X = R_X C R_X with r_X = t_X / t_ref, two iterations (KiDS-style iterative covariance). The control's r ≡ 1 exactly, so it
  keeps C. Because the two arms then use different covariances, Δχ² alone is not a likelihood ratio: the class uses
  **Δ(−2 ln L) = Δχ² + Δ ln det C** (Gaussian likelihood); Δχ² alone and the class it would give are reported.
- **B4 CVh-OWN (class-weighted).** As B3 with p = ½.
- **B5 COMBINED (class-weighted).** Ω_m,v = 0.2976 (primary kept set) together with B1 (r recomputed inside that projection).
- **B6 DIAG (reported only, no class weight).** Both arms with diag(C). It discards the real (mostly Gaussian) correlations of
  ξ±, so its χ² is not calibrated against the 4 / 9 thresholds; it removes all off-diagonal structure (including the
  fiducial-dependent non-Gaussian and super-sample parts) but its diagonal still carries the fiducial cosmic variance.
  If its class differs, that is stated in the README headline, but it does not set the lane class.
- Uniform rescaling C → s² C is not run: to first order it multiplies every Δχ² by 1/s² > 0, so it cannot change the sign
  of Δχ² or move a CONSISTENT class with Δχ² < 0 (stated in the README).

**Limitations (stated in the README):** the reference signal is the control's best fit, not the published fiducial's (which
needs a ΛCDM nonlinear model, excluded); the non-split file forces the p = 1 / p = ½ bracket; a model-dependent covariance in
a Gaussian likelihood adds information the data do not carry (stated, which is why B1/B2 keep one covariance for both arms).

## Statistic and classes (CFG650's, unchanged)

Per variant, footing and survey: Δχ² (F − S0) in the main configuration (IA marginalised) and the robustness set {widen2,
noIA, held, DESI} with CFG592's `klass` (EXCLUDED if Δχ² ≥ 9 and min(Δχ², robust) ≥ 9; TENSION if Δχ² ≥ 4; CONSISTENT if
Δχ² < 4 and max(robust) < 9; else NOT DIAGNOSTIC; N_kept ≥ 10). The robustness members are computed under the same variant.
**T-OWN is recomputed under each variant** (S0 best-fit mock × the footing's B_foot, refit S0 with the variant's control
covariance and projection; χ²_min ≥ 9 else NOT DIAGNOSTIC). Absolute χ² and p (N_kept dof) of both arms are reported.

**Lane class (KiDS, both footings, never pooled):**
- **ROBUST** — the KiDS class is CONSISTENT in every class-weighted variant (A: four Ω_m values × {primary kept set,
  re-derived kept set}; B1–B5) on both footings.
- **SENSITIVE** — the KiDS class changes in at least one class-weighted variant on either footing; each such variant, footing
  and new class is named.
Also reported: the largest class-driving Δχ² (or Δ(−2 ln L)) across variants and its margin to 4; DES classes per variant.

## Controls (frozen)

- **K1** (as scored, published C, the library's own objects): reproduce CFG650's committed numbers for both footings × both
  surveys — Δχ², Δχ²_noIA, the four robust values, the three no-IA robust values, χ²_S0, χ²_F, class and class_noIA — to
  |diff| ≤ 1e-6, and the MUTATE JSON's T-OWN χ² to ≤ 1e-6. If K1 fails, no variant is interpreted.
- **K2** the Ω_m override path evaluated at the as-scored Ω_m reproduces K1 (main + robust) to ≤ 1e-9.
- **K3** the common-covariance path with r ≡ 1 reproduces K1's main Δχ² to ≤ 1e-9.
- **K4** in B3/B4 the control's r equals 1 exactly at every iteration, so its χ² equals K1's.
- **K5 (native path, for the NC1x script)** the `--score` code path at its as-scored settings, run on the stored pair CFG636 C1
  vs CFG596 P0 with CFG654's `load_lib("native")`, reproduces `CFG654_independent_inputs/cfg654_native_posthoc.json`
  (blob b03696458adaf1c33904575220076e9a50eb7be7) native_all Δχ², Δχ²_noIA, χ²_S0, χ²_F and robust {widen2, noIA, held,
  DESI, LOC} for KiDS and DES to ≤ 1e-6; and its Ω_m override at the native as-scored Ω_m reproduces that to ≤ 1e-9.
  This is a pipeline check on a stored scorer-only diagnostic, no verdict.
- **MUTATE** (separate process, run first; exit 1 = bites): M1 Ω_m,v = 0.25 for the FRAMEWORK arm only (control as scored);
  M2 the framework arm's covariance × 0.5 (control as scored). Each must move the KiDS main Δχ² by ≥ 9 on both footings.

## NC1x applicability (written, NOT run)

The same script takes `--score <jobF> <jobS>` (e.g. `NC1x NCS0`) and then mirrors CFG654's production scorer
(`cfg654_native.py`, blob 450677f9e0ce8727020f2f81904f8848e7f95f6b, imported read only): the native library selected by
the runs' `cfg654_inputs`, robustness set {widen2, noIA, held, LOC}, DESI reported. In native mode the Ω_m override
replaces the native Ω_m in the PM and LOC distances (CFG654's own `native_E` form with Ω_Λ = 1 − Ω_m − Ω_r, trickle kept;
LOC with ω_m = Ω_m,v h_native²), the prefactor and the IA factor; the IA growth is the native table × D_ODE(Ω_m,v)/D_ODE(native
Ω_m) (linear growth ODE on the native E(z), exactly 1 at the as-scored value). The grid adds the native as-scored Ω_m. K1
there = reproduce `cfg654_native_results_<jobF>.json` when the chain has written it (else K1 PENDING, numbers provisional).
It is not run on NC1x in this lane.

## Compute

Single core (`OMP_NUM_THREADS=1 nice -n 10`), one process at a time, each < 2 GB peak (checked with `/usr/bin/time -l` on a
K1-only first call; if more, stop and report). Results are written incrementally. The 1024³ NC1x run is live and is not
touched.

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; raw data, framework-native; no HMcode / BAHAMAS in any
computation; a CONSISTENT class does not mean the data favour the framework; not theory closed.

## Commit provenance (appended; no criterion above is changed)

The text above (git blob 3bb5e5a479167b782994b32234d28a35d980a7ae) was staged alone for its own commit, but a parallel
session's commit 1049b615c ("CFG906 ledger row ...", 2026-10-20 02:40:42) landed between this lane's `git add` and
`git commit` and swept the staged file into it, together with that session's two ledger rows. The content is identical to
what was staged; no CFG909 script existed at that time. History is not rewritten; this provenance note is committed alone
(path-limited commit) as the forward fix, still before any CFG909 script.
