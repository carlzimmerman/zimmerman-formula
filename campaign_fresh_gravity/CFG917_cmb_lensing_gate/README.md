# CFG917: the CMB-lensing gate on theory-v2. Not detected on any scored pair: Part A SAFE ×3; Part B NOT DIAGNOSTIC as frozen (a wrong premise in one of my K tests), CONSISTENT under post-hoc addendum A1. The test has little power at box scales.

- **Criteria:** `FROZEN_CRITERIA.md`, commit **0289e4ad4**, committed alone before any CFG917 number. **Addendum A1** (`ADDENDUM_A1_2026-10-20.md`,
  commit **187f895aa**) is POST HOC. It was committed after the NC1x Part B run and before any Part B number for T1x, T2x or NC2x. Date: 2026-10-20.
- **Settings:** κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 are never pooled, and each pair is read on its own footing. "Cold energy"
  throughout; its mass is required; no particle species. Not "theory closed". Raw data and framework-native verdicts only. No ΛCDM fit,
  CAMB/CLASS nonlinear spectrum, halofit, HMcode or BAHAMAS enters any model or verdict (K3e/K3b′ use a CAMB+halofit spectrum only as a
  code-test input, exactly as the Planck package's own unit test does).
- **Compute:** a 1024³ job (chain7, NC2x) was live throughout. Every process ran alone, single-threaded under `nice -n 10`, and peaked
  at ≤ 0.43 GB (measured). Nothing was downloaded or touched.
- **NC2x** (alt footing, native inputs) was **not scored**: its output does not exist yet. The criteria and A1 were frozen before it, so it will be
  scored blind. The commands are at the end of this file.

## Result

Quoted from `cfg917_A1_classes.json`, `cfg917_<PAIR>.json` and `cfg917_partA_<PAIR>.json`.

**Part A: CFG649 checklist item 2** (unchanged script). The statistic is ΔA on Planck 2018 8–400 band weights, with 2σ = 0.056.

| pair | footing / inputs | canonical ΔA | 12-member bracket | label |
|---|---|---|---|---|
| NC1x vs NCS0 | canonical / native | −0.0018 | [−0.0115, −0.0012] | SAFE |
| T1x vs P0 | canonical / inherited | −0.0017 | [−0.0107, −0.0011] | SAFE |
| T2x vs P0 | alt / inherited | −0.0016 | [−0.0105, −0.0011] | SAFE |
| NC2x vs NCS0 | alt / native | — | — | DEFERRED (blind) |

**Part B: raw Planck PR4 lensing** (CMB-marginalised, L 8–400, 9 bandpowers, published covariance and linear fiducial correction).
- Positive Δχ² means the framework fits worse.
- The robustness set is AGG, ZHOLD, ZREL, KCUT, KLOW and BG.

| pair | χ²(F) / 9 (p) | χ²(S0) / 9 (p) | **Δχ²** | robustness range | class as frozen | class under A1 |
|---|---|---|---|---|---|---|
| NC1x vs NCS0 | 9.265 (0.413) | 9.541 (0.389) | **−0.276** | −1.571 (AGG) … −0.236 (ZREL) | NOT DIAGNOSTIC (K3b) | **CONSISTENT** |
| T1x vs P0 | 9.555 (0.388) | 9.643 (0.380) | **−0.088** | −1.200 (AGG) … +0.292 (KLOW) | NOT DIAGNOSTIC (K3b) | **CONSISTENT** |
| T2x vs P0 | 9.558 (0.387) | 9.643 (0.380) | **−0.085** | −1.157 (AGG) … +0.285 (KLOW) | NOT DIAGNOSTIC (K3b) | **CONSISTENT** |

- **Gate reading** (frozen "Scope and reading" rule):
  - As frozen: NOT DIAGNOSTIC for all three pairs.
  - Under A1: **PASS** for all three: NC1x on the canonical footing, T1x on the canonical footing, and T2x on the alt footing.
  - The alt-footing native pair, NC2x, is pending.
- **Per-band effect of the framework** (B_F/B_S0, L 8–400): from 0.9998 to 0.9896 for NC1x, and from 0.9998 to 0.9901 for T1x. The deficit of 0.02% to 1% grows with L.
- **Robustness members:**
  - AGG: Planck 2018 MV 8–2048, 14 bands. χ²(F)/χ²(S0) is 17.87/19.44 for NC1x and 16.71/17.91 for T1x.
  - ZHOLD and ZREL: the two alternative z > 1 continuations.
  - KCUT: support cut at 4.02 h/Mpc.
  - KLOW: the low-bin F/S0 ratio (0.989–0.990) held below k = 0.08.
  - BG: distances from the other input set's background.
- **Best-fit amplitudes** (context only, data relative to model): A_S0 = 0.979 ± 0.024 (native) and 1.003 ± 0.024 (inherited); A_F = 0.982 (NC1x) and 1.005 (T1x, T2x). Both arms fit PR4 well in absolute terms.
- **Context, particle-field F** (the lensing-vs-stability fork): Δχ² is −0.046 for NC1x and −0.016 for T1x and T2x.
- **Context, without the realisation-variance correction:** Δχ² is −0.168 for NC1x and +0.014 / +0.013 for T1x / T2x.

## What the gate can see (coverage of the S0 bandpowers, inverse-variance band summary)

| region | share of the 8–400 signal |
|---|---|
| z ≤ 1, k inside the box support (0.080–7.98 h/Mpc) | 0.150 |
| z > 1, k inside the support (rests on the z > 1 continuation) | 0.154 |
| k < 0.0802 h/Mpc (both arms = the run's own linear spectrum) | 0.696 |
| k > 7.98 h/Mpc | 0.000 |

About 70% of every PR4 8–400 bandpower comes from scales larger than the 100 Mpc/h box. On those scales the two arms are identical by
construction, as the compensated-source rule requires. The framework's measured box-scale suppression of P_grav is 3–11% at k 0.3–1 h/Mpc (0.6–0.7% at k = 0.1).
It moves the bandpowers by ≤ 1%, against a PR4 amplitude error of ≈ 2.4%.

The statistic is not blind:
- MUTATE M2 detects a ±10% amplitude change at symmetric Δχ² ≈ 17–18.
- The KiDS-EXCLUDED CFG596 candidate B (P1 vs P0; KiDS Δχ² +68.7) reaches only Δχ² **+1.88** on the primary statistic. Under the frozen rule it is NOT DIAGNOSTIC, because AGG (+10.05) and KLOW (+10.40) exceed 9.

So CMB lensing at L ≤ 400 is much weaker than raw shear for box-scale changes. It cannot sink a run whose large-scale (k < 0.1) power is unchanged.

## K tests (gating unless marked)

| test | result |
|---|---|
| K1 F ≡ S0 → Δχ² = 0 on the primary and every member | PASS (exactly 0) |
| K2 CFG649 canonical P1-vs-P0 ΔA reproduced through this code path | PASS: +0.013254 vs stored +0.013254 (difference 3e-7) |
| K3a PR4 windows on FFP10 vs PP/Ahat (reported) | 4.5e-4 |
| **K3b (as frozen):** marginalised fiducial correction = M·X_FFP10 within 2% | **FAIL**: max deviation 0.40 (wrong premise; see A1) |
| K3b′ (A1): (i) PS1 fiducial correction = full windows × FFP10 lensed CMB + PP; (ii) PS1 package unit test 8.705 | PASS: (i) ≤ 1.3e-4; (ii) 8.7094 |
| K3c published fiducial-model χ² | N/A: no such value exists for the on-disk FFP10 file; K3e substitutes |
| K3d Limber normalisation vs CAMB linear (native), PR4-binned, within 3% | PASS: max 0.46% (band 1) |
| K3e package unit test −2 ln L = 8.368 (CMB-marginalised) | PASS: 8.3724 |
| K4a growth D at every stored snapshot | PASS (0) |
| K4b P_grav,F(z_i) = P_grav,S0(z_i) (shared realisation) | PASS (0) for all three pairs |
| K4c lattice mode-averaged \|k\| = stored k_b (15 corrected bins) | PASS (6e-8) |
| K5 z_i field = input spectrum × Gaussian realisation | PASS: χ²_sv/n = 2.10 (n = 15), mean 1.013 ± 0.011 |
| K6 doubled z grid | PASS: ≤ 3.8e-4 on every χ² |

On K5: bin 3 (k = 0.197 h/Mpc) of the shared seed-359 realisation sits at +47%, about 3σ for its 43 independent modes. This is the
realisation-variance correction's reason to exist, and the uncorrected variant is reported as context.

## MUTATE (run first for every pair)

- **Part B MUTATE bites for all three pairs.**
  - M1 (F ≡ S0) gives exactly 0.
  - M2 (pipeline vs independent binned vectors, agreement ≤ 7e-16):
    - NC1x: +25.53 at 1.10× and +10.50 at 0.90×, symmetric mean 18.01.
    - T1x and T2x: +16.24 and +18.10, symmetric mean 17.17.
  - M3 context: P1 vs P0, as above.
- **Part A (CFG649's MUTATE, unchanged): "bites: False" for all three.**
  - M1, M2a and M2b pass.
  - M2c fails only on its "dA > 0" clause. That clause assumed CFG596's boost, but the script injects the lane's own z = 0 ratio, which here is a suppression (dA −0.0013 to −0.0014).
  - M2c's quadrature identity passes at 1.4–1.5e-4, within its 1e-3 tolerance.
  - CFG649's label rule does not depend on MUTATE, so the SAFE labels stand as printed. The orchestrator should note the clause.

## Disclosures

1. **K3b failed as frozen; A1 is post hoc.**
   - K3b assumed that the CMB-marginalised PR4 constant is the PP-only correction at FFP10. In fact it also folds in the CMB-spectrum part of the linear correction, evaluated at a CMB reference spectrum of the package's construction.
   - Mechanism checks:
     - The non-marginalised PS1 constant equals the full correction applied to FFP10 to 1e-4.
     - F_PS1 − F_marged = M_CMB·C_ref, which is 0.3% below M_CMB·C_FFP10.
     - My likelihood code reproduces both package unit tests (8.3724 vs 8.368; 8.7094 vs 8.705).
   - A1 changes no model, statistic, class or other test. It replaces K3b by K3b′.
   - NC1x's Part B numbers were seen before A1. T1x's and T2x's were not.
   - Both classes are reported. The frozen class for every pair is NOT DIAGNOSTIC.
2. **The CMB-marginalised constant carries a ΛCDM-based CMB reference spectrum.** It is the same constant offset for both arms. It is added to the shared ΛCDM inputs:
   - the FFP10 fiducial for normalisation, N1, MC correction and covariance;
   - the inherited runs' EH σ8 = 0.811 spectrum and background without radiation;
   - the native runs' CFG654 §6 list.
3. **Part A for the native pair uses CFG649's inherited background and EH spectrum.** They enter as weights of the measured F/S0 ratio and in A3, and are reported as-is (the script was not edited).
   - A2 scanned byte-identical engine copies (`_external_data/cfg917_work/`, sha256 7058f4333b8d4597… for the CFG654 engine and 8e2e477aeb0c670d… for the CFG650 engine).
   - This was needed because the engine file names gate the running chain. A2 found every pattern (PASS) in both module engines.
4. The first normal Part A run on NC1x was cut off by a closed output pipe before it wrote any file. It was rerun unchanged; no number differs.
5. **The continuations are bounded, not removed.**
   - z > 1 and k < 0.08 rest on declared continuations (coverage above).
   - ZHOLD, ZREL and KLOW move Δχ² by ≤ 0.38 from the primary; AGG by ≤ 1.3.

## What this establishes, and what it does not

- **It establishes:**
  - On the three finished theory-v2 1024³ runs, the framework's own gravitating field is not distinguishable from its same-pipeline control on the raw PR4 8–400 bandpowers (Δχ² −0.28 to −0.09; every robustness member < 1.6 in magnitude).
  - CFG649's relative check is SAFE on all three.
  - Both arms fit PR4 acceptably in absolute terms (p ≈ 0.38–0.41).
  - The shear-side pass is therefore not contradicted by CMB lensing at L ≤ 400. That holds on the canonical footing (native and inherited inputs) and on the alt footing with inherited inputs.
- **It does not establish:**
  - That the data favour the framework. CONSISTENT does not mean that, and Δχ² ≈ −0.1 to −0.3 is noise-level.
  - Any statement about scales larger than the box. There both arms are the same linear spectrum by construction, and that is 70% of the signal.
  - Anything about the alt footing with native inputs (NC2x, pending, blind).
  - Anything beyond L 400, except the approximate AGG member.
  - Anything about the primary CMB beyond CFG649's switch-off argument.
- The frozen class is NOT DIAGNOSTIC everywhere. The PASS reading rests on post-hoc A1.
- CFG917 is not a CFG654 verdict input: that clause's time condition has passed, and the clause names CFG649.

## NC2x: run these when `_external_data/overnight_chain/chain7_state/NC2x.ok` exists and chain7 has logged "chain7 done"

Run them one at a time, from `campaign_fresh_gravity/CFG917_cmb_lensing_gate`.
- Do not pipe them into `head`: a closed pipe kills the CFG649 script before it writes its files.
- The outputs go to the `.out` and `.json` files.

```
E=../../../_external_data
ls $E/cfg654_work/NC2x/                       # expect cfg654cmb_cfg650_m1m2m3_RES_alt_N1024_L100_ns1024_lean.json
OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_engine_copy.py
F=$E/cfg654_work/NC2x/cfg654cmb_cfg650_m1m2m3_RES_alt_N1024_L100_ns1024_lean.json
S=$E/cfg654_work/NCS0/cfg654cmb_cfg650_na_S0_canonical_N1024_L100_ns1024_lean.json
CFG649_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 ../CFG649_cmb_safety/cfg649_cmb_safety.py --f $F --s0 $S --tag CFG917_NC2x --engine $E/cfg917_work/engine654_copy.py --out cfg917_partA_NC2x_MUTATE > /dev/null
OMP_NUM_THREADS=1 nice -n 10 python3 ../CFG649_cmb_safety/cfg649_cmb_safety.py --f $F --s0 $S --tag CFG917_NC2x --engine $E/cfg917_work/engine654_copy.py --out cfg917_partA_NC2x > /dev/null
CFG917_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_cmb_lensing.py --pair NC2x > /dev/null
OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_cmb_lensing.py --pair NC2x > /dev/null
OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_amendment_A1.py        # frozen and A1 classes + gate readings for all four pairs
```

Then read `cfg917_A1_classes.out`. As for the other pairs, report NC2x's frozen class (NOT DIAGNOSTIC via K3b) and its A1 class side by side.

## Files

| file | role |
|---|---|
| `FROZEN_CRITERIA.md` (0289e4ad4), `ADDENDUM_A1_2026-10-20.md` (187f895aa) | criteria; post-hoc amendment |
| `cfg917_lib.py` | PR4/2018 data, CMBlikes binning, backgrounds, growth, linear spectra, per-run P(k, z) model, Limber |
| `cfg917_cmb_lensing.py` → `cfg917_<PAIR>[_MUTATE].out/json` | Part B scorer (K1, K2, K3a/b, K4–K6, MUTATE M1–M3) |
| `cfg917_camb_ktests.py` → `cfg917_camb_ktests.out/json` | K3d, K3e |
| `cfg917_amendment_A1.py` → `cfg917_A1_classes.out/json` | K3b′; frozen and A1 classes; gate readings |
| `cfg917_engine_copy.py` | byte-identical engine copies for CFG649's A2 scan (outside the repo) |
| `cfg917_partA_<PAIR>[_MUTATE].out/json` | Part A: CFG649's unchanged script, its own output format |

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
