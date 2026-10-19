# CFG859 — does CFG856's extra isothermal speed survive the ultra-faint dwarfs?

Criteria: `FROZEN_CRITERIA.md` (a40dd5cd9, before the script; last ID of block 850–859). Run: `python3 cfg859.py` (MUTATE `CFG859_MUTATE=1`).

## Result — CLASS: **OVER-PREDICTS UFDs (needs a core)**
| sample | E = ln(σ_obs/σ_pred), uncored V_x | law alone |
|---|---|---|
| **binary-corrected UFDs (7), canonical** | **−0.683 ± 0.090** | +0.677 |
| literature-σ MW UFDs (21), canonical | −0.416 ± 0.103 | +0.905 |
| binary-corrected, alt | −0.669 ± 0.091 | +0.631 |

- An UNCORED extra component (V_x0 = 9.42 km/s from the MW classical dSphs) adds ≥ 5.4 km/s to every dwarf's dispersion and predicts the
  binary-corrected ultra-faints ~2× too hot; the law alone predicts them ~2× too cold. The data sit between.
- **Post-hoc (not a verdict):** a cored isothermal extra component, M_x(<r) = V_x0² r³ / [G (r² + r_c²)], with **r_c ≈ 104 pc** (both footings)
  brings the binary-corrected UFD mean to E = 0. With r_c ~ 100 pc the component is barely changed at classical-dSph radii (r_1/2 ~ 0.2–1 kpc)
  and at SPARC radii (1–10 kpc), so CFG856's SPARC pass should survive — to be re-tested with the cored form (named, not run).
- K1 reproduces CFG826's law-only UFD excess (+0.68). MUTATE (V_x × 0.3) moves E toward the law and classes SURVIVES — the statistic responds.
- **Reading:** the surviving empirical description of the faint-dwarf excess is a cored cold component with σ ≈ V_x/√2 ≈ 7 km/s and a core
  ≈ 100 pc. Two numbers, both fitted (V_x on classical dSphs, r_c post-hoc on UFDs); a mechanism must produce both.

κ = ½ fitted; cold energy mass required; not theory closed.
