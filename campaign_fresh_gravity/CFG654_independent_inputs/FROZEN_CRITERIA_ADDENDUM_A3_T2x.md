# CFG654 ADDENDUM A3 (2026-10-20): native-input rerun of T2x, the ALT footing (committed alone, before the job is added or started)

**Why.** The theory-v2 shear side needs both footings (FROZEN_CRITERIA.md §5). On the canonical footing the native-input rerun
NC1x HOLDS (A2). The alt footing's pass (CFG650 T2x, KiDS Δχ² −7.18, CONSISTENT) still rests on inherited ΛCDM-shaped initial
conditions and background. This addendum adds the alt-footing native rerun, with nothing else changed.

**Seen before this file (disclosed):** NC1x vs NCS0 (A2): KiDS Δχ² −10.08, robustness −6.13 to −13.78, CONSISTENT; absolute χ²
144.68 / 108 (p = 0.011), NCS0 154.76 (p = 0.002); DES NOT DIAGNOSTIC; A2 reading HOLDS. CFG650 T2x (inherited): −7.18. CFG909
on T1x (advantage size amplitude-driven via projection Ω_m). No alt-footing native-input PM number at any resolution.

**Job** (run_654.py; same _P production settings, guards, start condition and abort rule as A1/A2):
- `NC2x`: native_cmb inputs, MODS "123", RES, **alt** footing (a₀ 1.1312e-10 m s⁻², the law's declared alt input).
- Control: **NCS0** (already run). The S0 switch never reads the footing (`cfg654_pm.py` `forces()`: S0 returns the plain
  Poisson field before any footing-dependent code), so one S0 serves both footings, as CFG596 P0 does for CFG650 T1x and T2x.

**Score.** `CFG596_MUTATE=1 cfg654_native.py --score NC2x NCS0` (MUTATE first; exit 1 = control bites), then without MUTATE.
Same statistic, data, cuts, robustness set {widen2, noIA, held, LOC}, DESI reported only, T-OWN (with the alt CFG530 boost the
scorer already selects by the framework run's footing), NZ1, classes and CMB-gate rule as FROZEN_CRITERIA.md + A1.

**Pre-declared reading (as A2):**
- **HOLDS** if NC2x is CONSISTENT under the A1 classes AND Δχ²(NC2x vs NCS0) ≤ 0.
- **WEAKENED** if CONSISTENT but Δχ² > 0.
- **FAILS** otherwise.

**Theory-level reading.** If NC1x and NC2x both HOLD, the theory-v2 shear side passes on both footings with the framework's own
early-universe inputs (still conditional on §6's shared inputs; CMB gate not evaluated; DES not diagnostic). If NC2x does not
HOLD, the two-footing native pass is not established and that is reported as such. Absolute χ² and p are reported next to Δχ².

Whichever happens is reported. No other job, setting or data cut is added after this commit. CFG909's script may re-score NC2x
afterwards as a reported sensitivity (no verdict weight), as it did for NC1x.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
