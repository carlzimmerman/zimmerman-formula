# UD2: the a0 law on Malin 1: FAILS (shape), both footings; inclination escape NOT RESCUED

κ = ½ FITTED; not theory closed; footings never pooled; not blind; one galaxy excludes nothing (owner rule). Criteria:
FROZEN_CRITERIA.md (4b44046a2b), AMENDMENTS.md A1 (06545dab7d), committed before any baryon or law number. Run:
`python3 ud2.py law` and `python3 ud2.py MUTATE` (about 1 s); outputs ud2.{out,json}, ud2_MUTATE.{out,json}.

## Inputs

- **Rotation curve:** Lelli, Fraternali & Sancisi 2010 (arXiv:1003.1312) Table 3. Rings at 12.5, 37.5, 62.5 and
  87.5 kpc: V_c 236.9 ± 9.4, 216.2 ± 2.6, 197.4 ± 4.7 and 214.1 ± 11.8 km/s. i0 = 38° ± 3°. D_A = 322 Mpc is the
  paper's (H0 70 with a q0 term), an input of the paper, not of this lane.
- **Baryon components:** exact path coordinates from the authors' vector EPS figures (inputs/; gs -dSAFER -dEPSCrop).
  The primary is the HSB-LSB decomposition at the paper's table M/L (HSB 3.3, LSB 0.9).
  - V_bar = 193, 122, 112 and 112 km/s at the four radii.
  - g_N/a0 = 1.04, 0.14, 0.07 and 0.05: the outer three points are well below a0.

## Grade

| footing | V_law (km/s) | χ²/4 | label | inclination escape |
|---|---|---|---|---|
| canonical | 244.7, 219.2, 232.9, 251.4 | 69.0 | **FAIL** | no i in 5-90° reaches p ≥ 0.05: **NOT RESCUED** |
| alt | 251.3, 228.0, 242.7, 262.2 | 132.5 | **FAIL** | **NOT RESCUED** |

- **The miss is the shape.** The data dip to 197 km/s at 62.5 kpc and stay near 214 km/s. The law, driven by the
  massive gas disc (V_gas 65-78 km/s outside 60 kpc), rises again to 233-262 km/s. A single inclination rescales all
  points together, so it cannot fix a shape.
- **Outer-disc label: not formed.** The HSB component never falls below 10 % of V_b² at the tabulated radii (shares
  0.99, 0.82, 0.56, 0.40).
- **M/L ends:** χ² 110-867 with HSB × 0.5 or × 2 and LSB 0.5 or 0.9. The paper's MOND-fit components (HSB 3.7, LSB 0.5)
  give 84 and 164. All FAIL.
- **EFE** at an assumed g_e = 0.01 a0: χ² 56 and 32; at 0.03 a0: 178 and 140. All FAIL; reported, not graded.
- The paper's own MOND fit (fitted HSB M/L, a0 3000 (km/s)²/kpc, standard μ) scores χ² 43.5/4 against Table 3. That is
  the "12-13 %" discrepancy it reports.

## Checks

- K0a: the plotted rotation-curve dots in both figures match Table 3 to 0.39 and 0.06 km/s. PASS.
- K0b: the paper's plotted MOND fit is reproduced from its own plotted components to a median of 0.0001. PASS. The
  M/L-free gas curve agrees between the two figures to 0.17 km/s.
- K1: no optimiser. PASS. MUTATE (ν ≡ 1): χ² 1753, far worse than the law on both footings. PASS. Rerun:
  byte-identical.

All checks pass, so the label is clean: **FAIL, NOT RESCUED.**

## Context (not graded)

Malin 1's outer disc is warped. The authors note that dropping the outer inclination from 38° to 32° would bring the
curve into agreement with MOND. A radius-dependent inclination is outside this lane's frozen escape, which uses one
inclination for all points, and was not tried. With only four rings, the 62.5 kpc point carries much of the χ².
Nothing here is a verdict on a theory.
