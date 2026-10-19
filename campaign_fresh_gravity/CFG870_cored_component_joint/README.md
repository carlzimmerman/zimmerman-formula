# CFG870 — the cored extra cold component: joint consistency across dwarfs and SPARC

Criteria: `FROZEN_CRITERIA.md` (976af111d, before the script; first ID of owner block 870–879). Run: `python3 cfg870.py`
(MUTATE `CFG870_MUTATE=1`). Seconds.

## Result — CLASS: **JOINT FIT HOLDS** (both footings)
Model: g_obs = g_law(g_bar) + G M_x(<r)/r², M_x(<r) = V_x² r³ / [G (r² + r_c²)], r_c = 104 pc (CFG859, post-hoc on 7 binary-corrected UFDs);
V_x re-fitted with the core on the 10 MW classical dSphs only.
| test | canonical | alt |
|---|---|---|
| V_x (MW classical, cored) | **10.65 km/s** (σ = 7.5 km/s) | 10.59 km/s |
| **T1 SPARC small rotating dwarfs (56)** | **D = +0.013 ± 0.022 ✓** | −0.021 ± 0.022 ✓ |
| **T2 M31 satellites + field dwarfs (17)** | **E = +0.025 ± 0.054 ✓** | +0.004 ± 0.055 ✓ |
| **T3 literature-σ MW UFDs (21; objects not used for r_c)** | **E = −0.085 ± 0.113 ✓** | −0.087 ± 0.113 ✓ |
| T4 MW classical rms ln-residual | 0.203 (law alone 0.568) | 0.210 (0.557) |
- MUTATE (r_c = 1 kpc): T3 fails on the canonical footing → BREAKS; the statistic responds to the core.
- The core also removes CFG857's MW/M31 amplitude offset (T2 passes).
- Physical scale: a cored isothermal component with σ ≈ 7.5 km/s, core ≈ 100 pc, central density ≈ 0.6 M_⊙/pc³.

## What this is, and is not
- **Is:** an empirical two-parameter description that, added to the law, fits MW classical dSphs (calibration), M31 and field dwarfs,
  ultra-faint dwarfs and SPARC's rotating dwarfs simultaneously, with both a0 footings, while leaving large rotating galaxies on the law
  (the component is a few % at 1–10 kpc in galaxies with V ≳ 30 km/s and negligible at V ~ 200 km/s).
- **Is not:** a mechanism. V_x is fitted (on MW classical dSphs) and r_c is fitted post-hoc (on 7 binary-corrected UFDs). The stiffened
  action cannot produce it (CFG858: stiffness only screens); expelled gas, tides, capture, early collapse, relaxation, friction transport,
  gas loss and binaries do not explain it (CFG822–853, CFG860/861). A framework-native origin for a universal σ ≈ 7.5 km/s, ρ0 ≈ 0.6 M_⊙/pc³
  cold core is the open target.
- Separate from the red/spheroidal lens excess (CFG851), which lives at 30–300 kpc around massive galaxies.

κ = ½ fitted; cold energy mass required; not theory closed.
