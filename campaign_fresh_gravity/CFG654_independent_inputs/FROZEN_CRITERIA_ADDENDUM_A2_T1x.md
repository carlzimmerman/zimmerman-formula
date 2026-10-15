# CFG654 ADDENDUM A2 (2026-10-15): native-input rerun of T1x (committed alone, before any job is added or started)

**Why.** T1x (CFG650, M1+M2+M3, canonical) is the primary pre-declared run, and it is CONSISTENT on raw KiDS-1000 (Δχ² −7.70
against the same-pipeline control; absolute χ² 136.6, p = 0.033). It inherited ΛCDM initial conditions and background. This
addendum extends the frozen CFG654 rerun from T12 to T1x, with nothing else changed.

**Jobs** (run_654.py; same _P production settings, same guards):
- `NC1x`: native_cmb inputs, MODS "123", RES, canonical.
- `NCS0`: already defined (native_cmb control, shares the native ICs).
- Order: NCS0, then NC1x.

**Score.** `CFG596_MUTATE=1 cfg654_native.py --score NC1x NCS0` (MUTATE first), then without MUTATE. Same statistic, data, cuts,
robustness set and classes as FROZEN_CRITERIA.md + A1 (relative Δχ² vs the native control, plus absolute χ² and p).

**Pre-declared reading:**
- **HOLDS** if NC1x is CONSISTENT under the A1 classes AND Δχ²(NC1x vs NCS0) ≤ 0.
- **WEAKENED** if CONSISTENT but Δχ² > 0.
- **FAILS** otherwise.

Whichever happens is reported. No other job, setting or data cut is added after this commit.

**Alt footing (separate, already pre-declared).** CFG650's `T2x` (M1+M2+M3, alt, inherited inputs) runs first and is scored by
`cfg650_native.py`, which picks T2x automatically. That is CFG650's own frozen job; this addendum does not change it.

κ = ½ fitted; footings never pooled; not theory closed.
