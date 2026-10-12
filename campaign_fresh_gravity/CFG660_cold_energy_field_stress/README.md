# CFG660: the law as the hydrostatic equilibrium of cold energy's own stress

**Lane label:** LAW = EQUILIBRIUM OF A FIELD-ALIGNED STRESS (spherical): S1 ✓, N1 ✓, D1-A ✓; ISOTROPIC: **EXCLUDED** on raw
SPARC; KINETIC: **NOT KINETIC**; DYNAMICS: **ILL-POSED**.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (7eff02fa3), 2026-10-12, with the owner's reservation of CFG660–669.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed";
  nothing here says the data favour the framework.
- **Script:** `cfg660.py`. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg660.py`: one process, under 2 GB, a few minutes, exit 0
  → `cfg660.out`, `cfg660_results.json`. `CFG660_MUTATE=1` exits 1 as designed (M1 and M2 bite) → `cfg660_MUTATE.out`,
  `cfg660_results_MUTATE.json`. Reads `CFG4_common`, `CFG7_common` and `CFG4_galaxy_law.py` read-only (the record's SPARC
  harness, Υ = 0.61). Nothing downloaded.

## Why this lane

Every cold-energy equation of motion on the record (CFG539–554, CFG638) puts the law in by hand: the drift relaxes ρ_c toward
ρ_ph, which is copied from the law. CFG539 killed the only fluid version (class B) because an ideal-gas pressure P = ρσ² needs a
per-system temperature σ⁴ = G M_b a₀/4. This lane asks whether a pressure that depends on the local field instead makes the law
cold energy's own equilibrium, with no constant beyond a₀ and G.

## Results

| check | result |
|---|---|
| **S1** sympy, general F and any spherical ρ_b(r) | (A) equilibrium residual along the law: **identically 0**. The law is an exact equilibrium of the field-aligned stress Π = P⊥I + (P∥ − P⊥)ĝĝ, dP∥/dg = (g/4πG)(1/F′ − 1), P⊥ − P∥ = g(g − F⁻¹(g))/4πG |
| **S2** isotropic residual | (r g_N′ + 2g_N)(F − g_N)F/(4πG r g_N) = ρ_b g (ν − 1): zero only where there are no baryons or the field is Newtonian |
| **S3** deep limit | P∥ = −g²/8πG + g³/6πGa₀, P⊥ − P∥ = g²/4πG − g³/4πGa₀: to leading order **minus the gravitational Maxwell stress** (tension along field lines) |
| **S4** kinetic realizability (P∥(0) = 0) | P∥ < 0 for every g > 0; β = 1 − P⊥/P∥ = 2.0 (g = 0.01 a₀) … 11 (g = 10 a₀). **NOT KINETIC**: no particle gas has P∥ < 0 or β > 1 |
| **S5** local WKB along the field (deep SIS point, g = 0.1 a₀) | max Im ω = 2.5 / 21 / 214 per τ_ff at k = 10 / 10³ / 10⁵: growth ∝ √k, **ILL-POSED**. Across the field: ω² = −4πGρ₀ (bounded). With an added kinetic pressure c_s² = V²/2 the growth is bounded at 1.36/τ_ff |
| **N1** Hernquist a/r_M 0.05–10, both kernels | (A) ≤ 7e-7 dex from the law (PASS); (I) +0.26 to +0.59 dex |
| **D1** raw SPARC, 175 galaxies, the record's harness | law 0.1003 / 0.1013; **isotropic 0.1766 / 0.1870 (Δ +0.076 / +0.086): EXCLUDED** on both footings; anisotropic 0.1003 / 0.1013 (Δ ≤ 1.5e-8) |
| MUTATE | M1 (anisotropy removed) breaks S1: residual F(F − g_N)/(2πG r); M2 reproduces the isotropic rms exactly |

## Reading

1. **The law is exactly the hydrostatic equilibrium of a universal, local stress** that depends only on |g|, a₀ and G
   (spherical symmetry, the round rule). No per-system constant, no target density, no catchment needed for the profile.
2. **The stress must be anisotropic and field-aligned.** Any isotropic equation of state is excluded by raw rotation curves
   (+0.08 dex rms). In the deep regime the stress is the gravitational field's own Maxwell stress, with sign reversed.
3. **No gas of particles can carry it** (S4). Cold energy, if the law is its equilibrium, is a field-like medium. That is
   consistent with the no-particle rule.
4. **But a medium with its own independent density and this stress is ill-posed** (S5). The stress does not respond to
   compression, so an overdensity's extra weight is unopposed and short waves grow without bound. Read plainly, the consistent
   options are:
   - (a) ρ_c is **slaved to the field** (no independent cold-energy dynamics). That is the law as modified gravity; it gives up
     cold energy as independent matter, which the record needs for clusters, the Bullet, lensing and the CMB (CFG624).
   - (b) The total stress also responds to compression (for example a kinetic part). The local growth is then bounded (about
     1.4/τ_ff here), but the total stress is no longer a function of g alone. Whether a two-variable law Π(ρ_c, g) can keep the
     law as an exact equilibrium for every baryon profile is **not answered here**: that is the next door.
   - (c) The law is not cold energy's equilibrium but a target it relaxes to (the record's class A + FIX-2), which is where the
     record already stands, with the per-system temperature question open.
5. **Not claimed:** anything beyond spherical symmetry (no exact field-built stress was found for general 3-D shapes in the
   exploratory work); relativistic completion; stability beyond local WKB; the cold energy's amount.

## Disclosures (2026-10-12)

- The exploratory scratchpad versions (disclosed in the criteria) gave the same Hernquist numbers; `cfg660.py` was written fresh.
- The criteria's S2 line guessed the residual's algebraic form; the computed form is ρ_b g (ν − 1), which has the frozen property
  (nonzero wherever ρ_b > 0 and ν > 1).
- S5 uses one representative deep point (g = 0.1 a₀) and 1-D WKB along and across the field; the √k growth is structural
  (the ik·(g/F′) term), not specific to that point.
- The table's smallest g is about 1e-5 a₀, so "P∥(0) = 0" holds to O(1e-10) a₀²/G.
