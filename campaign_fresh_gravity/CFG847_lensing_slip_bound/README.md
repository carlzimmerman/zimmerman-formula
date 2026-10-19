# CFG847 — how far can lensing differ from dynamics in the framework? (gravitational-slip bound)

Criteria: `FROZEN_CRITERIA.md` (8e554a296, before the script). Run: `python3 cfg847.py` (MUTATE `CFG847_MUTATE=1`). Seconds.
Source: path 2 of the 2026-10-19 review of Codex's work.

## Result — CLASS: **LENSING = DYNAMICS AT TEST PRECISION** (conditional on a well-posed covariant parent of the CFG43 type)
| system (canonical) | v_c (km/s) | s from cold dispersion | s from field energy W | s from stiffness (L* 1 kpc) | total s |
|---|---|---|---|---|---|
| dwarf (1e7 M_⊙, 0.3 kpc) | 21 | 3.8e-9 | 6.4e-10 | 1.7e-8 | 2.2e-8 |
| MW disc (10 kpc) | 208 | 2.7e-7 | 5.8e-8 | 7.9e-10 | 3.3e-7 |
| MW outer (100 kpc) | 169 | 3.0e-7 | 1.7e-8 | 1.4e-11 | 3.2e-7 |
| group (1e12, 300 kpc) | 345 | 1.2e-6 | 9.0e-8 | 6.4e-12 | 1.3e-6 |
| cluster (1.5e14, 1 Mpc) | 1314 | 1.5e-5 | 2.6e-6 | 5.7e-12 | 1.7e-5 |
(alt footing: same to ~10%; largest s = 1.9e-5.)

- s = |Φ − Ψ|/v_c², the lensing–dynamics mismatch. Lensing tests reach ~5–10%; the framework's own non-dust stresses give at most
  2e-5 (clusters) and ~1e-7 in galaxies, i.e. lensing traces the dynamical mass to far better than any test can see.
- **By construction (disclosed):** the dominant term is the cold energy's own dispersion (σ²/c²); the result mostly restates that
  cold energy is dust-like mass. The non-trivial content is that the P-field's potential energy W (which grows only
  logarithmically toward its wall) and its stiffness energy are both smaller still, for any L* in the CFG820 window.
- **MUTATE did not bite (disclosed):** a TeVeS-like anisotropic stress of 1e-3 of the cold rest-energy density gives s ≤ 1.9e-3,
  still below test precision. So the conclusion holds for any parent whose anisotropic stress stays below ~5e-3 ρ_c c²; only a
  parent with relativistic-scale anisotropic stress could produce a testable slip.
- **Run-1 bug (disclosed):** the stiffness term carried an extra factor 4πG (units error) in run 1 (`*_run1_unitbug.*`); fixed to
  Π₃ = πG L*² ρ_c² before recording. It is negligible in both runs; no class changed.
- **Criteria typo (disclosed):** the frozen file's parenthetical formula for u is garbled; the script uses the law's own field value
  u = g a0/(g + a0), checked against the identity K W′(u) = u²/(a0 − u) = g_N to 1e-9.
- **What stays open:** existence of a well-posed covariant parent (CE-075 shows one vector parent is ill-posed); this lane removes the
  quantitative side of "predict lensing", not the construction side.

κ = ½ fitted; cold energy mass required; not theory closed.
