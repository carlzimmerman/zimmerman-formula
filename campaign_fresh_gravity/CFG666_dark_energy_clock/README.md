# CFG666: the dark-energy clock — SHAPE DISFAVOURED; the clock family is closed

**Label as frozen: SHAPE DISFAVOURED.** Diluting a de Sitter-scale law (a_true = cH_Λ) by a cosmic-clock settled fraction leaves too
much phantom where gravity is strong. **Post-hoc family diagnostic:** any uniform-dilution clock settling at the rate H_Λ needs more
time than the age of the universe on both footings. The κ = ½ coincidence that motivated the lane is not physical in this form.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (9dc52f46b), 2026-10-12. Block CFG660–669. The motivating coincidence
  and the shape risk were disclosed there before any code.
- **Settings:** κ fitted on the record; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed"; nothing here says the data favour the framework. Raw SPARC (CFG4 harness, Υ = 0.61).
- **Scripts:** `cfg666.py` → `cfg666.out`, `cfg666_results.json` (exit 0); MUTATE `CFG666_M=M1` / `M2` each exit 1 (both bite).
  `cfg666_family_diag.py` → `cfg666_family_diag.json` (post hoc, no verdict weight).

## Results

| item | canonical | alt |
|---|---|---|
| C1: f = √(a₀/a_true), implied t_b | 0.4156, 9.42 Gyr | 0.4569, 10.70 Gyr |
| D1 rms law / clock (Δ) | 0.1003 / 0.1088 (+0.0085) | 0.1013 / 0.1174 (+0.0161) |
| D1 mean residual law / clock | +0.004 / **−0.042** | −0.022 / **−0.063** |
| g_bar > 1e-10 (905 points): bias law / clock | −0.022 / −0.076 | −0.038 / −0.089 |
| 1e-11..1e-10 (1355): bias law / clock | +0.029 / −0.018 | −0.001 / −0.042 |
| < 1e-11 (1129): bias law / clock | −0.015 / −0.039 | −0.051 / −0.073 |
| frozen class | TENSION (bias > 0.03) | **DISFAVOURED** (bias > 0.06) |

- C2 (mergers): α_eff = H_Λ τ_ff = 0.006 / 0.017 / 0.029 for τ_ff = 0.1 / 0.3 / 0.5 Gyr, below CFG623's first excluded node: the
  clock would have been consistent with the merger result.
- D2 (sign only): outer residual vs the law, early (T ≤ 2; 10 galaxies, 43 points) −0.047 / −0.083, late (T ≥ 7; 87 galaxies)
  −0.015 / −0.052. The early types sit *lower*, not higher, on these points: no support for the clock's sign here (small early
  sample).
- MUTATE: M1 (f = 1, the excluded κ = 2.894 directly) and M2 (f × 2) both move the scores by ≥ 0.1 dex.

## Family diagnostic (post hoc)

For a uniform-dilution clock with true scale a_true = R·a₀ and f = R^(−1/2) (fixed by the measured deep amplitude), the frozen shape
gates pass only up to **R = 3.15 (canonical, κ_true ≤ 1.58)** and **R = 1.26 (alt, κ_true ≤ 0.76)**. A clock at the cosmic rate H_Λ
then needs t_b = −ln(1 − f)/H_Λ = **14.5 Gyr (canonical)** and **38.9 Gyr (alt)**, both longer than the age of the universe
(13.8 Gyr). A faster rate is a free constant and removes the coincidence. **The clock family is closed** in its uniform-dilution form.

## Reading

- The coincidence (κ = ½ from the de Sitter surface gravity times a 9.4 Gyr settling at H_Λ) is arithmetic, not physics: the dilution
  it needs spoils the strong-field shape, the same failure class as the Verlinde linear sum (CFG117). Selector row S5 is the binding
  constraint.
- What stays open: the raw-data age anomaly (CFG700, ×1.46 old/young) and the SPARC early-type outer excess (CFG534) are still
  unexplained; this lane shows they are not produced by a uniform cosmic-clock dilution of a larger scale.
