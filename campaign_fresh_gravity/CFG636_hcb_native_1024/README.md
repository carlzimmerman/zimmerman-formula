# CFG636: framework-native 1024³ shear test of the condensed-baryon source (H-CB). Status: QUEUED (validation PASS; production C1 starts automatically after CFG596 P2)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (89aeaae12), 2026-10-12. CFG596's canonical RESULT and CFG634's
  results were seen before freezing (disclosed there).
- **Settings:** κ = ½ is FITTED. Footings canonical / alt, never pooled. "Cold energy" throughout; its mass is still required.
  No particle species. Not "theory closed". No ΛCDM or standard-MOND yardstick in any verdict.

## What is tested
CFG596 EXCLUDED candidate B (phantom sourced by all retained baryons) on raw KiDS-1000 (canonical Δχ² +68.7; own boost
1.19–1.25 at k 0.3–1). CFG634 proposed H-CB: only condensed baryons (stars + cold gas) source the phantom. CFG636 runs CFG634's
"decisive native test" exactly as specified there.

- **Engine** `cfg636_pm.py` = `cfg596_pm.py` at the production freeze 6323b630f plus the two named changes:
  per-catchment source weight `tab` = `min(fret_of(lM), 0.10)` (was `fret_of(lM)`), and the census edge in `x_supply` uses the
  same retention. Rule source: CFG634 FROZEN_CRITERIA T5 (HC-1: condensed = max(M*, 0.10 f_b M_ta) capped at the retained baryons;
  the PM has no stellar model, so its form is the cap alone, as CFG634's README spec writes). Since fret_of ≥ 0.10 everywhere,
  f_c = 0.10 in every catchment. `CFG636_SOURCE=b` restores the old weight; `none` is a control.
- **Scope note (stated, not changed):** cells outside every catchment keep weight 1.0, exactly as in cfg596_pm.py, because the
  spec changes only the per-catchment weight. Diffuse field baryons therefore still source the phantom in this test.
- **Runs:** C1 (canonical) then C2 (alt), L100 N1024 NSEED 1024 RMIN 0.78125, lean, spill, 14 threads, nice 10, launched by
  `run_636.py` (copy of `run_596.py`, same guards) into `../_external_data/cfg636_work/<JOB>/`. S0 = CFG596 P0, shared.
- **Scorer** `cfg636_native.py` = `cfg596_native.py` pointed at C1/C2 + CFG596 P0, plus the growth gate (z = 0, k ≤ 1:
  max|P_grav/P_S0 − 1| ≤ 0.10, deficit fails like an excess) and the per-footing verdict of criteria §6.

## Validation (256³, L100, NSEED 512, one process, nice 10; `cfg636_validate.py` → `.out/.json`)
Every number from `cfg636_validate.json`.

| gate | result |
|---|---|
| **V-R** VBr (cfg636_pm.py, `CFG636_SOURCE=b`) vs CFG596 VLr | **bit for bit**: 144 stored quantities (P, σ8, P_grav, σ8_grav, diagnostics) over all six snapshots, difference exactly 0 → PASS. Peak RSS 2.04 GB, swap growth 0 |
| **V-H** VHr (`hcb`) | completed; max\|P_grav(H-CB)/P_grav(B) − 1\| at z = 0 = 0.37 → PASS (differs). Peak RSS 2.13 GB, swap growth 0 |

**256³ PREVIEW, NOT a verdict** (resolution 256³ at L100; S0 = CFG596 VLs; the old weight's boost at 256³ is larger than at
1024³, 1.25–1.57 vs 1.19–1.25, so the size does not transfer):

| z | H-CB P_grav/P_S0 at k 0.3 / 0.5 / 1 | old weight B | max\|P/P_S0 − 1\| (k ≤ 1) H-CB / B | σ8_grav/σ8_S0 H-CB / B |
|---|---|---|---|---|
| 1 | 1.012 / 1.019 / 1.021 | 1.197 / 1.362 / 1.409 | 0.023 / 0.438 | 1.004 / 1.062 |
| 0.5 | 1.039 / 1.061 / 1.051 | 1.289 / 1.555 / 1.495 | 0.066 / 0.626 | 1.014 / 1.092 |
| 0 | 1.058 / 1.100 / 1.091 | 1.253 / 1.567 / 1.507 | 0.112 / 0.661 | 1.020 / 1.083 |

Reading of the preview only: on the PM, H-CB removes most of candidate B's excess but does NOT flip it to a deficit (unlike
CFG634's halo-model context number); at z = 0 it sits at the edge of the growth gate (0.112 at 256³). The 1024³ run decides.

**Scorer pipeline check** (`python3 cfg636_native.py --test530` → `cfg636_native_test530.out/json`): on CFG530 L100 N512 every
Δχ² and robustness value equals `cfg596_native_test530.out` exactly; only the T-OWN labels differ (no MUTATE pass was run for
the test, so T-OWN is "missing" and the verdict line is marked PROVISIONAL, by design).

## Queue
`../_external_data/cfg636_work/cfg636_waiter.sh` (copy of `cfg636_waiter.sh` here) polls every 2 min. It starts
`run_636.py serial C1` (nohup, nice 10) once no `cfg596_pm.py` and no `cfg636_pm.py` process is running and free + inactive
memory is ≥ 42 GB. It kills nothing. Log: `cfg636_waiter.log` in the work folder. Expected C1 runtime about 12 h (CFG596 P1).

## Finishing commands (from the repository root)
1. After C1 ends (check `../_external_data/cfg636_work/C1/watch.log` for `exit 0` and the JSON for a `z0` snapshot):
   - `cd campaign_fresh_gravity/CFG636_hcb_native_1024`
   - `CFG596_MUTATE=1 nice -n 10 python3 cfg636_native.py`   (MUTATE first: NZ1 + T-OWN; exit 1 = NZ1 bites everywhere)
   - `nice -n 10 python3 cfg636_native.py`                   (main pass: Δχ², classes, growth gate, verdict per footing)
2. Alt: `nohup nice -n 10 python3 run_636.py serial C2 > ../../../_external_data/cfg636_work/run_636_C2_nohup.log 2>&1 &`
   (only when the machine is free), then repeat step 1.
3. Optional MUTATE production run `CM` (old weight, canonical) must reproduce CFG596 P1; no verdict role.

## RESULT (2026-10-12): canonical 1024³ L100, C1 (H-CB census cap) vs CFG596 P0

Scored with `cfg636_native.py` as frozen (89aeaae12); MUTATE first (NZ1 bites). Outputs: `cfg636_native.out/json`,
`cfg636_native_MUTATE.out/json`.
- Own boost B(z=0) at k 0.3/0.5/1/2/4: 1.058 / 1.056 / 1.056 / 1.025 / 1.003 (CFG596: 1.186 / 1.252 / 1.206 / 1.103 / 1.035).
- **KiDS: Δχ² +13.97** (CFG596 +68.73); robustness min +9.19 (widen2), noIA +17.8, held-out +12.3, DESI +11.1; T-OWN passes →
  **EXCLUDED, narrowly** (every variant ≥ 9; widen2 at 9.19).
- **DES: Δχ² +7.01** (robust 4.0–13.3), T-OWN fails → NOT DIAGNOSTIC.
- Growth benchmark (NOT an observational gate — see astra audit 5c31fcad4): G = 0.089 → "PASS" as frozen.
- Verdict as frozen: canonical FAIL (EXCLUDED); alt PENDING.

Reading: capping the settling source cuts the raw-KiDS tension by ~80% (Δχ² 68.7 → 14.0) but leaves it just above the
exclusion line. Scope: this is a uniform census cap (f_c = 0.10 in every catchment; field baryons still source), not a
phase law (astra bd8981d3d); the framework's own gas expulsion (CFG646, ~¼ of Δχ²) and per-host supply (CFG647, ~⅓ of the
excess) are NOT included; verdicts are conditional on the inherited ΛCDM ICs/background (astra 5c31fcad4).
κ = ½ fitted; cold energy mass required; not theory closed.
