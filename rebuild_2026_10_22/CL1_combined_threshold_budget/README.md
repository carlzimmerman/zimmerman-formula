# CL1_combined_threshold_budget: decoupled switch + measured cluster budget, on the full line set

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (947d12651f). CF2's higher-T points were not yet seen at write time (disclosed).
- **Harness:** CF2 (7881b642f8 / a2704b5c66) / X62 (8c7768d26d), plus GS1's cluster budget (01f6dd977d).
- **What this lane is:** a **consistency test**, not a derivation. T is located by CF2's map; the gas slope is measured
  (X-COP, s = 2.777).

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): **COMBINED PICTURE FAILS**

The binding lines are G-OUT-all and groups (canonical), plus the SPARC line and the MW ultra-faints (alt).

**Canonical footing.** At every grid point, KiDS lensing (Δχ² 0.0), SPARC, all five dwarf classes, G-OUT-M3 and 14 of
the 15 cluster keys pass. Exactly one line fails at each point, and which line depends on c_f:

| T | c_f | groups Z | G-OUT-all Z | failing |
|---|---|---|---|---|
| 12.2 | 4.0 | +2.20 | −1.93 | groups |
| 12.2 | 4.75 | +1.98 | −2.14 | G-OUT-all |
| 12.3 | 4.0 | +2.21 | (pass) | groups |
| 12.3 | 4.75 | (pass) | −2.14 | G-OUT-all |
| 12.4 | 4.0 | +2.12 | (pass) | groups |
| 12.4 | 4.25 | +2.05 | (OVER) | groups, G-OUT-all |
| 12.4 | 4.5 | (pass) | (OVER) | G-OUT-all |

The full per-point values are in `cl1_combined_results.json`.

- **The binding tension.** Groups pass only at c_f ≳ 4.5–4.75. The all-cluster outer band over-predicts at c_f ≳ 4.25.
  A single concentration misses by about 0.1–0.2σ on each side.
- **Alt footing.** It fails the SPARC line and the MW ultra-faints at every point, independently of T, c_f and the
  budget (as in CF1 and CF2). It also fails groups or G-OUT-all as on canonical.

## Reading

With a concentration-independent switch at about 10^12.2–10^12.4 M☉ and the measured cluster gas budget, the canonical
footing is one line from passing every graded line. The remaining tension is that groups want slightly higher
concentration than clusters. A concentration falling with mass, which is the direction X48's native zooms show, would
resolve it. That must be derived, not tuned.

## Checks: 10/10

- K0a/b/c and K2a/b (the X62 reproductions).
- S0a: always-halo plus the budget at c_f = 4 reproduces GS1's R4_meas exactly (max |ΔZ| 0.0000).
- K2: the budget is active on 4564/4564 cluster calls.
- S0b: reproduces CF2's T 12.2 / c_f 4.75 point.
- K1: the switch property holds at every point.
- K3: 0.70 GB.
- **Pending:** the twin and the rerun.

## Files

- `cl1_combined.py`
- `cl1_combined.out` and `cl1_combined_results.json`
- the per-run outputs
