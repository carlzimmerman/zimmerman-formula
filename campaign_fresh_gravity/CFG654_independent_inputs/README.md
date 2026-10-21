# CFG654: replacing every inherited ΛCDM input of the native PM pipeline with framework-native or raw-measurement inputs

- **Date:** 2026-10-12. Inventory: astra's audit `sol61_push/lcdm_dependency_audit_2026_10_12/RESULT.txt` (A–C), read as data.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. "Cold energy"; its MASS is required; no particle
  species. Not "theory closed". Nothing here says the data favour the framework.
- **No verdict here.** This lane builds inputs, an engine switch and a scorer patch, re-scores stored runs POST HOC (diagnostic only),
  validates at 256³, and freezes criteria (`FROZEN_CRITERIA.md`, committed alone) for a 1024³ rerun that is NOT started.

## Principle

Before any bound system exists the switch is off (CFG649), so the framework's early universe is GR + photons + neutrinos + baryons +
cold energy (as cold matter) + dark energy, with a₀ irrelevant. Linear perturbation physics in that era is therefore the
**framework's own physics**, not a ΛCDM assumption, and CAMB run in that era is a legitimate framework-native IC generator. What must
NOT be borrowed are **ΛCDM fit results** defined by late-time data (σ8 at z = 0, late-time Ω_m or H0 fits) and **ΛCDM late-time
nonlinear or collapse ingredients** (EH fitting shape, ΛCDM-shell Δ_ta table, ΛCDM back-scaled growth, HMcode/halo models).

## Files

| file | role |
|---|---|
| `cfg654_ics.py` → `.out`, `_results.json`, `cfg654_ics_tables.npz`, `cfg654_scorer_tables.npz` | parameters with provenance, CAMB pre-switch linear spectrum, native growth, brackets |
| `cfg654_delta_ta.py` → `cfg654_delta_ta.json` (engine table), `_results.json`, `.out` | native turnaround table + brackets |
| `cfg654_native.py` → `cfg654_native_posthoc.{out,json}` | `load_lib("native")` scorer patch; post-hoc re-scoring; `--score N12 NS0` production scorer |
| `cfg654_pm.py` | `cfg650_pm.py` + switch `CFG654_INPUTS=inherited|native` |
| `run_654.py` | launcher (run_650 guards) for V0i / VNs / VN12 and the frozen N12 / NS0 |
| `cfg654_validate.py` → `.out/.json` | V-R reproduction, V-N1/N2 native IC/growth checks, V-C, preview |
| `FROZEN_CRITERIA.md` | the independent-inputs 1024³ rerun of CFG650 T12 + its S0 (committed alone) |

## Results (256³ validation, 2026-10-12; cfg654_validate.out)
- V-R PASS (inherited inputs, modules off ≡ CFG596 VLr bit for bit, 144 quantities × 6 snapshots).
- V-N1 FAIL as frozen (bin-centre vs BAO wiggles, max dev 0.041/0.042); post-freeze mode-averaged diagnostic (cfg654_vn1_diag) agrees to 3e-4, so the native ICs carry the intended amplitude.
- V-N2 PASS (native growth in the run), V-C PASS (source zero-sum ≤ 2.5e-10) for both the CMB pair (primary, A1) and the BBN bracket.
- PREVIEW 256³, NOT a verdict, P_grav/P_S0 − 1 at k 0.3/0.5/1, z = 0, M1+M2: inherited +0.005/+0.014/+0.031; native CMB pair +0.005/+0.012/+0.030; native BBN +0.005/+0.011/+0.028. Native S0 σ8(z=0) 0.826 vs inherited 0.812. Native inputs leave the M1+M2 preview essentially unchanged.
- Gates for the primary 1024³ native jobs (NC12, NCS0) are met except V-N1-as-frozen (explained above); no 1024³ run started.

## RESULT: NC1x vs NCS0 (addendum A2, the native-input rerun of T1x; 1024³, chain6, scored 2026-10-20 10:07)

Theory-v2 (CFG650 M1 + M2 + M3, canonical footing) rerun from the framework's own initial conditions and background (A1 primary
set: Planck TT,TE,EE+lowE ω_b/ω_c, A_s, n_s, θ*; CAMB in the switch-off era; native Δ_ta and catchment), against its own control
NCS0 on the same ICs. Scored by the frozen `cfg654_native.py` (MUTATE first). Numbers from `cfg654_native_results_NC1x.json`; p-values from CFG909's K1 reproduction (`../CFG909_shear_score_lcdm_input_sensitivity/cfg909_NC1x.out`, χ²_data with N_kept dof, reproduces the scorer to 0).

| survey | N_kept | χ²_min control NCS0 | χ²_min NC1x | Δχ² | robustness (widen2 / noIA / held / LOC) | DESI (reported) | class |
|---|---|---|---|---|---|---|---|
| KiDS-1000 | 108 | 154.76 (data-χ² p = 0.008) | 144.68 (data-χ² p = 0.024) | **−10.08** | −6.13 / −13.78 / −8.75 / −12.74 | −7.39 | **CONSISTENT** |
| DES Y3 | 78 | 93.99 | 91.78 | −2.21 | −0.79 / −4.97 / −2.14 / −2.90 | −2.12 | NOT DIAGNOSTIC (T-OWN fails) |

- **MUTATE** (`cfg654_native_NC1x_MUTATE.out`): NZ1 bites on both surveys; T-OWN S0 χ²_min 17.11 on KiDS (DIAGNOSTIC), 8.14 on
  DES (NOT DIAGNOSTIC).
- **Benchmark** (no verdict weight; vs the native control, not an observational exclusion): P_grav/P_S0 at k = 0.3 / 0.5 / 1 h/Mpc
  = 0.972 / 0.961 / 0.949 at z = 0 (G 0.050), 0.966 / 0.944 / 0.921 at z = 0.5, 0.964 / 0.932 / 0.891 at z = 1.
- **CMB-lensing gate:** NOT EVALUATED (no committed CFG649 raw-data CMB-lensing form at the scorer's freeze).
- **Verdict (frozen §5):** PASS, shear side, canonical footing. **A2 reading: HOLDS** (NC1x CONSISTENT and Δχ²(NC1x − NCS0) =
  −10.08 ≤ 0).

**What this changes.** The canonical shear pass no longer rests on inherited ΛCDM-shaped initial conditions and background: with
the framework's own early-universe inputs it stays CONSISTENT and the relative Δχ² moves from −7.70 (T1x, inherited) to −10.08.

**What it does not change.**
- Canonical footing only. The alt footing's pass (T2x, −7.18) is still on inherited inputs; A2 froze no alt native rerun.
- Absolute fits are worse with native inputs, for both arms (implied linear σ8 0.825 vs 0.811): KiDS χ²_min 144.68 / 108 points
  for the framework (p = 0.024 on the data part of χ², CFG909's convention) against 136.6 (p = 0.033, A2) inherited; the control falls
  further (154.76, p = 0.008). The framework
  beats its own control by suppressing small-scale power (≈5% at k = 1 h/Mpc, z = 0; 11% at z = 1); it is not a good absolute
  fit.
- CFG909's script re-scored NC1x (2026-10-20, K1–K4 PASS, K1 reproduces this table to 0): the KiDS class is ROBUST (CONSISTENT in
  every variant), but the size is again amplitude-driven: Δχ² −3.11 / −6.86 / −9.58 / −10.97 / −15.80 at projection Ω_m
  0.2806 / 0.2976 (CFG886 no-CMB) / 0.3085 / 0.3138 / 0.3308 (as scored: native 0.3104, −10.08); framework's own covariance
  (CV1_OWN) −2.94. Quote the canonical native result as CONSISTENT, not as a −10 preference.
- Still shared: the Planck column comes from a base-ΛCDM chain (late lensing smoothing of the peaks), H0 from θ* (SH0ES only as
  LOC), massless ν, the empirical f_ret census, M2 cooling inputs, survey nuisances and covariances, seed 359 (§6).
- DES is not diagnostic; the CMB gate is not evaluated. A CONSISTENT class does not mean the data favour the framework.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.

## Run-plan disclosure (2026-10-20): NC2x aborts and restart gate (A3 job; no science change)
- NC2x (A3) started 10:33 under chain7 (gate: free + inactive ≥ 48 GB, the frozen §3 start rule). It was aborted twice by the frozen swap-growth
  rule and resumed each time from its own rolling checkpoint (bit-identical resume): 12:44 at step ~21 (disk free fell to ~8 GB while a parallel
  session set up a job), and 15:42 at step 40 (a 31 GB local Ollama model loaded beside it).
- Restart 16:24:36 from the step-39 checkpoint under chain7b: the gate waits only for heavy jobs (1024³ engines, an Ollama server) and for
  free + inactive ≥ **46 GB**, i.e. 2 GB below the frozen §3 start rule (owner: "i need this finished"; NC2x peak RSS 42–44 GB; the frozen abort rule
  — RSS > 52 GB or swap growth > 4 GB — is unchanged). This is a disclosed deviation from the start rule only; no input, setting, statistic or data cut changes.

## RESULT: NC2x vs NCS0 (addendum A3, the native-input rerun of T2x on the ALT footing; 1024³, chain7/chain7b, scored 2026-10-21 06:32)

Theory-v2 (M1 + M2 + M3) on the alt footing (a₀ = 1.1312e-10), from the framework's own early-universe inputs (A1 CMB-pair set), against
the footing-independent control NCS0. Scored by the frozen `cfg654_native.py` (MUTATE first). Numbers from `cfg654_native_results_NC2x.json`.

| survey | N_kept | χ²_min NCS0 | χ²_min NC2x | Δχ² | robustness (widen2 / noIA / held / LOC) | DESI (reported) | class |
|---|---|---|---|---|---|---|---|
| KiDS-1000 | 108 | 154.76 | 145.38 | **−9.39** | −5.69 / −12.85 / −7.99 / −11.86 | −6.89 | **CONSISTENT** |
| DES Y3 | 78 | 93.99 | 91.85 | −2.15 | −0.79 / −4.57 / −1.91 / −2.71 | −2.09 | **CONSISTENT** (T-OWN 10.31 ≥ 9: diagnostic this time) |

- **MUTATE** (`cfg654_native_NC2x_MUTATE.out`): NZ1 bites on both surveys; T-OWN S0 χ²_min 22.56 (KiDS) and 10.31 (DES), both DIAGNOSTIC.
- **Benchmark** (no verdict weight): P_grav/P_S0 at k = 0.3 / 0.5 / 1 h/Mpc = 0.975 / 0.967 / 0.955 at z = 0 (G 0.043); 0.968 / 0.948 / 0.928
  at z = 0.5; 0.964 / 0.933 / 0.896 at z = 1.
- **CMB-lensing (CFG917, frozen before NC2x output existed; scored 06:4x):** Part A (CFG649 checklist) ΔA −0.0017, bracket [−0.0113, −0.0011]
  → SAFE; Part B (raw Planck PR4, L 8–400) Δχ² −0.265 (χ² 9.28 vs 9.54 / 9 bands) → NOT DIAGNOSTIC as frozen, CONSISTENT under CFG917's
  post-hoc A1 (low power, as for NC1x). Not a CFG654 verdict input.
- **Verdict (frozen §5):** PASS, shear side, alt footing. **A3 reading: HOLDS** (NC2x CONSISTENT, Δχ²(NC2x − NCS0) = −9.39 ≤ 0).
- Run history: aborted twice by the frozen swap rule (12:44 and 15:42 on 10-20) and resumed bit-identically from its checkpoints; restarted
  16:24 under a 46 GB start gate (disclosed deviation from the 48 GB start rule; see the run-plan disclosure above).

**What this changes.** With A2 (NC1x, canonical, HOLDS) and A3 (NC2x, alt, HOLDS), the theory-v2 shear side now passes on BOTH footings with
the framework's own early-universe inputs — the inherited-IC condition is lifted on both. On the alt footing DES is diagnostic and also
CONSISTENT.

**What it does not change.** Absolute fits remain mediocre (KiDS χ²_min 145.38 / 108; the control 154.76); the advantage comes from ~4–10%
less small-scale power; the size of the advantage is amplitude-driven (CFG909 on NC1x; the NC2x rescore is reported in CFG909's README);
the CMB-lensing gate has low power; and — from the 10-20/21 structural lanes (CFG941/944/946/947/950/951/952) — the class-A engine that
produces this pass has no established physical parent (its phantom is a global QUMOND field carrying a satellite EFE, its RMIN applies the
law only to retained baryons ≥ 2.19e11 M☉ at 1024³, its source relocation is not momentum-conserving). The pass is a computational result
of that engine. A CONSISTENT class does not mean the data favour the framework.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
