# NL1_native_level_L: FROZEN CRITERIA (committed alone, before any ng 64 zoom has finished)

Written 2026-10-28, at the owner's request ("run it"): derive the concentration level L from the framework's own
converged zooms, instead of locating it from data.

**Status when frozen.**
- X48 AMENDMENT A3 (54c45e963e) is running nine ng 64 seeds at 10^12 M☉. They are 55–70 % through
  (t = 3.3–4.3 of 6.08 Gyr), and no `snap_zf.npz` exists.
- The ng 48 nine-seed medians (A2, c218c10add) are c_nat = 11.63 / 8.22 / 7.31 at 10^12 / 10^13 / 10^14.
- CL2 and CL3 pass every canonical line only at L ≈ 3.75–4 with the S9 shape.
- LEE1's passing region is about L 3.64–4.17 for T ≳ 12.19.

So L = 4 is about 1.8× below the ng 48 native level at cluster mass.

**The question.** Does resolution bring the native level down to where the data put L?

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads. X48's files are not edited.

## 1. The native level (frozen)

1. **Measure.** Each finished ng 64 run (`runs/M1e12_s{1..9}_ng64/snap_zf.npz`) is measured with X48's own `measure()`
   (imported read-only from `x48_analyze.py`), with A2's settings. Only runs with flag "ok" are used.
   c64 is the median over ok seeds.
2. **Convergence ratio.** R = c64 / 11.63, where 11.63 is the A2 ng 48 median at 10^12.
   - **Disclosed:** the ng 64 runs are not the same physical realisations as the ng 48 seeds. The historical seed
     convention changes the field with grid size (`COMMON_MODES_CORRECTION_2026_10_27.md`), so R compares ensemble
     medians, not paired runs.
3. **Native level.** L_nat = 7.31 × R. This assumes the 10^12 convergence ratio also holds at 10^14 (disclosed; the S9
   mass shape is kept). The 68 % interval comes from 2000 bootstrap resamples of the ok seeds (seed 20261028).
4. **Readiness rule.** If fewer than 7 of the 9 runs are ok, the lane stops with **NOT READY**. Nothing is graded.

## 2. Grade (CL2's harness via LEE1's executed copy, read-only)

- **PRIMARY:** S9 shape, L = L_nat, T = 10^12.3, the measured cluster budget, and the full line set on both footings:
  SPARC A/B, 63 groups, 15 cluster keys × 2 h cells, five dwarf classes, and KiDS lensing.
- **Reported:**
  - T from CL3's crossover, linearly interpolated or extrapolated in L from CL3's committed pairs (canonical: L 3.75 →
    12.2357, 3.9 → 12.149);
  - the L_nat 68 % ends;
  - the uncorrected reference L = 7.31 (R = 1).

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **L DERIVED: THE NATIVE LEVEL PASSES** | every canonical line passes at L_nat |
| **NATIVE LEVEL FAILS: <lines>** | otherwise; the failing lines are listed |
| **CONVERGENCE INCONCLUSIVE** | added to either verdict when the L_nat 68 % interval straddles LEE1's passing band (3.64–4.17) |

## 3. Checks and twin

- **K0 (Step 0).** LEE1's executed copy reproduces its own Step-0 checks (K0a/b/c, K2a/b).
  `measure()` on X48's synthetic NFW (c = 4) passes X48's K3 (within 15 %).
- **K1.** The ng 48 A2 medians are re-read from `x48_analyze_results_ng48_A2.json` and must equal 11.63 / 8.22 / 7.31 to
  0.01.
- **K2.** Peak RSS < 1 GB for the grading process. It runs only after the zooms have finished.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`NL1_MUTATE=1`, separate outputs).** The A2 reference is read as 1.1 × 11.63, so K1 must fail and the run
  must exit 1.

**Run** (after the zooms finish): `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I nl1_native_level.py`
