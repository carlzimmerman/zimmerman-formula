# CE1_converged_eta_grade: CONVERGED NATIVE FAIL (both footings, both f★, median and 68 % ends)

Criteria: `FROZEN_CRITERIA.md` (38e1a28c55), committed before any script or number. Script `ce1_grade.py` runs X74's
grader unchanged with a c_f-equivalent table. Log: `ce1_run.log` / `ce1.out`; results: `ce1_results.json`; per-run
grader outputs `CE1_*`.

## Converged-cusp η (X81's cusp fit at x_c 0.001, each run's own c_nfw)
| mass | grid | η_conv (median, 68 %) | X77 at the ε cut | c_f-equivalent |
|---|---|---|---|---|
| 10¹² | ng 64 | **25.94** [23.89, 26.53] | 20.83 | 8.05 |
| 10¹³ | ng 48 | **17.67** [16.73, 19.86] | 13.79 | 5.92 |
| 10¹⁴ | ng 48 | **16.91** [15.68, 18.39] | 14.39 | 5.72 |

Removing the resolution cut raises η by 18–28 % at every mass.

## Full grade (X74 lines unchanged)
| configuration | SPARC | groups Z | cluster keys failing (canonical, h 0.672) |
|---|---|---|---|
| canonical, f★ 0.034, median | **FAIL**: Υ 0.48 / 0.47, rms 0.0701 | +1.51 | G-MID-T3 Z −2.30, G-IN-Mall Z −2.55 (both OVER) |
| canonical, 16th | FAIL: Υ 0.48 | +1.55 | the same two |
| canonical, 84th | FAIL: Υ 0.46 | +1.44 | the same two, plus G-IN-all |
| f★ 0.0615 | identical classes | | |
| alt | FAIL: Υ 0.41–0.42, as at every c_f (X78: the a₀ law's) | | the same keys |

- **Labels:** CONVERGED NATIVE FAIL at f★ 0.034 and 0.0615, canonical and alt. The cluster masses carry [ng 48].
- **What X43 / X77 had:** G-MID-T3 Z +0.30, G-IN-Mall −1.18 (X43, c_f 4). With converged η they are −2.30 / −2.55.
  So the cusp is too dense in **both** places, bright galaxies and cluster cores.
- **Checks:**
  - K1: X77's table reproduces X77's committed grade exactly (max |d| 0).
  - K2: X81's 25.94 reproduced (25.937).
  - MUTATE (η × 0.5): canonical SPARC Υ +0.080, as required.

## Reading
With the resolution cut removed, route E's native collapse branch fails SPARC and two cluster-core keys, on both
footings. The knife-edge passes (X77) came from the ε cut. Native cold collapse over-concentrates by about 20–30 % at
every mass. The only route E configuration that passes is still the external c_f = 4 (η 10.82).

**Post-A4 (automatic, reported):** `watch_A4_then_CE1.sh` waits for X77's A4 rerun, then runs `ce1_grade.py --A4`
with 10¹³ and 10¹⁴ at ng 64 (outputs CE1_A4_*).

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. The converged η
extrapolates each halo's fitted NFW inward of r_conv (X81 T2: every halo is NFW-shaped down to the cut).
