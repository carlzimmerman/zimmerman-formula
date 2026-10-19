# CFG856 — a universal extra circular speed V_x on top of the law?

Criteria: `FROZEN_CRITERIA.md` (e7b1ea0e3, before the script). Run: `python3 cfg856.py` (MUTATE `CFG856_MUTATE=1`). Seconds.
Origin post-hoc (CFG854's simplest Pareto formula); SPARC is the genuine out-of-sample test.

## Result — CLASS: **SPARC-COMPATIBLE ONLY**
| | canonical | alt |
|---|---|---|
| V_x0 calibrated on MW dSphs (N) | **9.42 km/s** (10) | 9.24 km/s (9) |
| **P3 SPARC small dwarfs (56): D = obs − pred** | **+0.017 ± 0.022 → PASS** | −0.017 ± 0.022 → PASS |
| law alone (V_x = 0) | +0.032 | −0.004 |
| P1 M31 satellites mean V_x | 14.31 km/s (z +2.7) → FAIL | 13.50 (z +2.1) → FAIL |
| P2 slope of log V_x on log M★ | +0.089 ± 0.028 → pass (|slope| < 0.15) | +0.096 ± 0.035 |
| field dwarfs mean V_x | 8.67 km/s | 8.05 km/s |

- **The out-of-sample test passes:** an extra isothermal speed of 9.4 km/s on top of the law, calibrated only on MW dSphs, is
  consistent with SPARC's 56 small rotating dwarfs (it adds only a few % to their 30–60 km/s curves). MUTATE (V_x × 3) is excluded by
  SPARC (D −0.087 ± 0.025), so the test has teeth. This is the first dwarf-excess form in the record that does not break SPARC.
- **M31 satellites want more** (14 km/s, z 2.7 — though CFG843 found MW and M31 equal in Δ at matched g_bar; the V_x difference tracks
  M31's larger radii), and V_x rises weakly with stellar mass (3σ nonzero slope). So V_x is not strictly universal.
- **Not a force-law change:** a global V_x²/r term would be ~10% of the Sun's pull at 1 AU. The form only makes sense as an extra
  cored mass component inside each system (an isothermal cold population with σ ≈ V_x/√2 ≈ 7 km/s), negligible in large systems.
- **Dimensional curiosity (post-hoc, not claimed):** V_x0² = a0 × L with L ≈ 31 pc, at the bottom of the stiffness window
  (CFG820: L* ≥ 24 pc). Could indicate the stiffness length sets the extra speed; could be coincidence. Untested.

κ = ½ fitted; cold energy mass required; not theory closed.
