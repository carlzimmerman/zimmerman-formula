# CFG640: a PM that carries condensed and hot baryons separately (H-CB as a phase law). Status: VALIDATED at 256³; 1024³ production QUEUED behind CFG636 (not started)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (71b2cc1c9), before any CFG640 run.
- **Settings:** κ = ½ is FITTED. Footings canonical / alt, never pooled. "Cold energy" throughout; its mass is still required.
  No particle species. Not "theory closed". No ΛCDM or standard-MOND yardstick in any verdict.

## Why
astra's review (bd8981d3d) showed that the CFG596/CFG636 PM maps a hot state and a condensed state with the same baryon density to
the same source, so CFG636 tests a uniform 10% census cap, not a phase law. CFG640 gives every particle a separate condensed
fraction, so the condensed-baryon-source hypothesis (H-CB) can be tested with phase information.

## The split rule (engine `cfg640_pm.py` = `cfg596_pm.py` @6323b630f + the split)
- **State:** each particle carries f_d, the condensed fraction of its baryon share (float16). Hot = 1 − f_d. f_d = 0 at z = 49.
- **Phase law:** at every dynamical census refresh (cfg596's existing every-10th-call catchment refresh; snapshots never change f_d),
  a particle whose nearest grid point is in catchment k gets f_d ← max(f_d, f_c,k). f_d is never lowered.
  f_c,k = 0.10 + (f_ret,k − 0.10) χ_k. Here 0.10 is the census floor (stars + cold gas, CFG515 / CFG634 HC-1) and χ_k = min(1, r_cool/R_k)
  is the share of the catchment's hot gas inside its cooling radius. The hot gas is isothermal at T = μ m_p V²/2k with V⁴ = G M_ret a0,
  ρ ∝ r⁻² out to the catchment radius, and the cooling radius is where t_cool = r/V.
- **Source:** the law's MOND input is f_b ρ_d/ρ̄, with ρ_d the CIC deposit of f_d, so only condensed baryons enter it.
  Ordinary gravity reads all mass, as before. The census edge uses f_c. Settling, R5, supply, cap, grid and outputs are cfg596 verbatim.
- **Switch:** `CFG640_SOURCE=b` restores cfg596's all-retained-baryon source on the original code path.
- **Inherited ingredients:**
  - Λ(T) is the record's Tozzi & Norman (2001) Z = 0.3 Z_sun fit (cm12 → CFG369/370), with CFG370's corrected 1e-22 normalisation.
  - μ = 0.6, n_e/n_H = 1.17, n/n_H = 2.3 (cm12).
  - t_dyn = r/V (CFG369 / CFG638 SIS).
  - Collisional cooling only, with no UV background. Every catchment holding hot gas has kT ≳ 0.09 keV.
  - The census f_ret and the Δ_ta table.
- **New tuned constants: 0.** Knob-like structural choices are declared and frozen, never varied:
  - K1, the hot-gas truncation radius: the catchment radius.
  - K2, t_dyn rather than the age.
  - K3, Z = 0.3 Z_sun.
  - K4, irreversibility (no reheating or feedback).
  - K5, haloes below RMIN carry no condensed baryons (a resolution bias, low).
- **What the rule gives** (`cfg640_split.py` → `.out/.json`, design table, no simulation): with K1 as frozen, f_c − 0.10 ≤ 5.9e-4
  for every mass ≤ 10^15 and z ≤ 2. Hot gas spread to the catchment radius barely cools, so **f_c is the census floor in practice.**
  K1 is the one real lever. Truncating at the census MOND radius r_M instead gives χ = 1 at lM 13 (f_c = 0.325) and χ = 0.03–0.32
  for lM 13.5–15. The age bracket gives χ ≤ 0.06 and the primordial bracket χ ≤ 5e-4. Neither bracket is run.
  The physics CFG640 adds over CFG636 is therefore mostly representational:
  - phase memory: condensed baryons stay condensed after they leave a catchment;
  - field baryons are hot or diffuse and source nothing (CFG636 kept field weight 1.0);
  - a separately carried condensed density.
- **Not implemented (stated):**
  - astra's Route-2 conversion-energy term −∫μ_d Γ dx. There is no W_int.
  - Any thermal evolution of the hot phase.
  - A pass would not establish a complete phase dynamics.

## Validation (256³, L100, NSEED 512, one process at a time, nice 10; `cfg640_validate.py` → `.out/.json`)
| gate | result |
|---|---|
| **V-R** VBr (`b`) vs CFG596 VLr | **bit for bit**: 144 stored quantities, 6 snapshots, difference 0. PASS. Peak RSS 1.91 GB, swap growth 0 |
| **V-P (b)** phase pair on VPh's z = 0 state | 4,272,195 of 8,974,818 condensed particles set hot (x < L/2), total density identical. Phase source differs: src_sum −1.106e-5 vs +3.412e-5, max\|Δφ\|/max\|φ\| 9.3e-3. The old representation gives bit-for-bit identical potentials for A and B. PASS |
| **V-P (i)** | 7,802,398 hot particles moved by up to 2 cells: condensed MOND input bit-for-bit unchanged, total density changed (max \|Δ\| 113). PASS |
| **V-P (iii)** | f_d ≡ 0: src_sum = e_sum = 0 exactly; potential equals pure Newtonian (difference 0). PASS |
| **V-H** VPh (`phase`) | completed. Peak RSS 2.31 GB, swap growth 0 |

The validation script itself (in-process V-P force evaluations) peaked at 3.16 GB RSS (2.22 GB footprint), slightly above the 3 GB
target; disclosed.

**256³ PREVIEW, NOT a verdict.** S0 is CFG596 VLs. The 256³ boosts are larger than at 1024³ for candidate B, so the size does not transfer.

| z | phase P_grav/P_S0 at k 0.3 / 0.5 / 1 | G (k ≤ 1) | CFG636 cap | CFG596 B | σ8_grav/S0 | f_d mean / nonzero fraction |
|---|---|---|---|---|---|---|
| 1 | 1.040 / 1.070 / 1.072 | 0.081 | 1.012 / 1.019 / 1.021 (G 0.023) | 1.197 / 1.362 / 1.409 | 1.014 | 0.037 / 0.371 |
| 0.5 | 1.076 / 1.119 / 1.098 | 0.133 | 1.039 / 1.061 / 1.051 (G 0.066) | 1.289 / 1.555 / 1.495 | 1.025 | 0.046 / 0.456 |
| 0 | 1.055 / 1.103 / 1.099 | 0.116 | 1.058 / 1.100 / 1.091 (G 0.112) | 1.253 / 1.567 / 1.507 | 1.019 | 0.054 / 0.535 |

Reading of the preview only:
- The phase law removes most of candidate B's excess, like the cap.
- At z = 0 it lands within 0.01 of the cap. At z = 1 and 0.5 it carries more power than the cap.
- It sits at the edge of the growth gate at 256³. The 1024³ run decides.

**Scorer pipeline check** (`python3 cfg640_native.py --test530`): output identical to `cfg636_native_test530.out` except the wall time.

## Production (NOT started; FROZEN_CRITERIA section 3)
- **Start condition:** CFG636 C1 finished and scored, no cfg596/636/640 engine running, and free + inactive memory ≥ 48 GB.
- **Memory estimate:** CFG636 C1 peaked at 40.3 GB. CFG640 adds 2.1 GB of float16 f_d and one float64 condensed deposit
  (8.6 GB, at the force stage, the same footprint as the normal deposit stage). The expected peak is about 43–46 GB, against the
  unchanged 50 GB abort rule. It has not been measured at 1024³; the first production steps measure it.
- Queue (from the repository root): `nohup bash campaign_fresh_gravity/CFG640_phase_source_pm/cfg640_waiter.sh > /dev/null 2>&1 &`
  The waiter starts `run_640.py serial H1` when the start condition holds; it kills nothing.
- Direct (only when the start condition holds): `cd campaign_fresh_gravity/CFG640_phase_source_pm && nohup nice -n 10 python3 run_640.py serial H1 > ../../../_external_data/cfg640_work/run_640_H1_nohup.log 2>&1 &`
- **After H1 ends** (watch.log `exit 0`, JSON has `z0`):
  1. `CFG596_MUTATE=1 nice -n 10 python3 cfg640_native.py` first.
  2. Then `nice -n 10 python3 cfg640_native.py`.
- H2 (alt) next, the same way. HM (`b`, canonical) is optional and must equal CFG596 P1.
- Arrays and logs go to `../_external_data/cfg640_work/<JOB>/`.
- CFG639 Part B is also queued behind the 1024³ runs. The owner orders the queue.

## Files
- `cfg640_pm.py`: the engine.
- `run_640.py`: the launcher.
- `cfg640_waiter.sh`: the production waiter.
- `cfg640_split.py` → `.out/.json`: the split-rule design table.
- `cfg640_validate.py` → `.out/.json`: the validation gates.
- `cfg640_native.py` → `cfg640_native_test530.out` and `cfg640_native_results_test530.json`: the scorer and its pipeline check.
