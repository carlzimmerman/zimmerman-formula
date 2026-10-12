# CFG666 FROZEN CRITERIA: do the "dark" strong-lens perturbers need mass with no baryons?

Date: 2026-10-12. Committed ALONE before any CFG666 script or scored number. Block CFG660–669. Later changes go in dated README
disclosures. κ = ½ FITTED; footings separate; cold energy mass required; no particle species; not "theory closed"; nothing will be
phrased as "the data favour the framework".

## 0. What has been seen (before scoring)

The record's L99 (fable_independent_2026/L99_no_dark_subhalos.py) states the structural prediction (every perturber is baryonic,
M_dyn a functional of M_b) but never confronted a measured perturber. The record calls substructure the referee's first objection
(memory: particle-vs-mode LIABILITY 2). Published values read from the papers' own text 10-12 (arXiv HTML/TeX, not a summariser):

| object | z_lens | mass | light |
|---|---|---|---|
| J0946 dark model (Vegetti+2010, 0910.0760) | 0.222 | M3D(<0.3 kpc) = 5.8±0.3e8, M3D(<0.6 kpc) = 1.1±0.05e9 M☉ | L_V < 5.0e6 L☉ (3σ); M/L > 120 |
| J0946 luminous model (2506.07978) | 0.222 | projected M(<1 kpc) = 10^8.9 (+1.1/−0.8, 95%) | L = 10^8.4 (+0.1/−0.2) L☉, R_half = 0.74–0.77 kpc; luminous model fits better |
| B1938 A (Vegetti+2012, 1201.3643) | 0.881 | M3D(<0.6 kpc) = 1.13±0.06e8; projected(<600 pc) ≈ 1.7e8 | L_V < 5.4e7 L☉ (3σ); M/L > 3.5 |
| B1938 V (Powell+2025, 2510.07382) | 0.881 | projected m80 = 1.13±0.04e6 M☉ (80 pc) | no luminosity limit published |

Rough chat estimates already made by the author (disclosed): J0946 dark model at 0.3 kpc sits at g ≈ 10 a0 (the law adds ~10%);
J0946 luminous model ⇒ law-predicted ~10^8.7 vs measured 10^8.9; V needs ~0.4–1.1e6 M☉ of baryons (far below any z=0.88 imaging).
Expectation: dark-model J0946 EXCLUDED, luminous J0946 CONSISTENT, B1938 A and V NOT DIAGNOSTIC.

## 1. Framework prediction (no halo model)

For each object and reading, the baryonic mass the law needs to reproduce the measured mass M_obs at radius r:
- **R-iso** (cold mass settled while the satellite was isolated, EFE-blind; the record's surviving reading 1812f594a): solve
  M_obs = M_b(<r)·ν_mono(g_N/a0), g_N = G M_b(<r)/r², spherical, ν_mono = the record's kernel.
- **R-EFE** (law acts with the host's external field ≫ a0): Newtonian, M_b(<r) = M_obs. This bounds the requirement from above.
Required stellar light: L_req = M_b,req / Υ_max with Υ_max = 8 (a generous old-population ceiling in V/I; gas-free satellite of an
elliptical). Projected masses are treated as spherical masses at the same radius (a projected mass ≥ the 3D mass, so this
overstates M_obs only mildly and is stated).
For the J0946 luminous model the prediction is the forward one: M_b(<1 kpc) = L·Υ·f_in, Υ ∈ [1, 4], f_in = fraction of a projected
exponential (Sérsic n=1) with R_half = 0.75 kpc inside 1 kpc, L ∈ [10^8.2, 10^8.5]; law (R-iso) and Newtonian (R-EFE) masses.

## 2. Classes (per object, per footing)

- **EXCLUDED** (that published solution cannot be baryonic under the law): L_req > 10 × the 3σ light limit under BOTH readings.
- **CONSISTENT** (luminous J0946): the predicted M(<1 kpc) band [R-EFE low, R-iso high] overlaps the measured 95% interval.
- **NOT DIAGNOSTIC**: no light limit, or L_req ≤ the light limit.
- Lane label: the J0946 verdict is decided by which published solution is adopted; if the dark solution is EXCLUDED and the
  luminous one CONSISTENT, the lane label is **NOT DIAGNOSTIC (model-selection-limited)** and the deciding observation is named.

## 3. MUTATE (`CFG666_MUTATE=1`, exit 1 iff bite)

M1: a0 → 0 (pure Newton) must make R-iso = R-EFE exactly. M2: Υ_max → 1e4 must turn J0946-dark from EXCLUDED to NOT DIAGNOSTIC.

## 4. Limits named now

Lens masses come from lens models (profile choices; tNFW/PJ/SIS); distances use the papers' cosmology (the framework's background
is the same at percent level, far below the factors tested); Υ ceiling; spherical treatment; perturbers may lie off the lens plane.
