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
