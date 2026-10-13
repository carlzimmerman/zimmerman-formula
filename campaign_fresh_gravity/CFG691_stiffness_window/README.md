# CFG691: can astra's stiffness hide the sector from the Sun and keep it in galaxies?

**Label: WINDOW OPEN (L* ≥ 5.75 pc from the Solar System; SPARC unaffected up to the grid edge, 1000 pc), CONDITIONAL on a
disclosed control-line error (K1 fails by 1e-6 at a line set equal to the analytic value). Never a C2 pass: the Υ-band failure
of CFG690 is inherited. Galactic external field not modelled.**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (9560a93c5), 2026-10-12. Block CFG690–699.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed"; nothing here says the data favour the framework. astra's sector is read only; no astra file is edited.
- **Script:** `cfg691.py`, one process, about 10 s → `cfg691.out`, `cfg691_results.json`.
  - It **exits 1** because K1 fails (see Disclosures).
  - `CFG691_MUTATE=1` exits 1 as designed (both teeth bite) → `_MUTATE` outputs.
  - Reads `CFG4_common` and `CFG690_cubic_origin/cfg690_results.json` read-only. Nothing downloaded.

## Results

**The universal profile.** For a point mass, astra's equation reduces exactly to −[q″ + 2q′/s − 2q/s²] + q² = 1/s²
(s = r/ℓ_γ). The reduction has no free parameter. solve_bvp converges with a relative ODE residual of 1.6e-10.

| s | 0.01 | 0.1 | 0.3 | 1 | 3 | 10 | 100 | 10³ |
|---|---|---|---|---|---|---|---|---|
| S = s q (screening factor) | 0.0050 | 0.048 | 0.134 | 0.358 | 0.663 | 0.894 | 0.990 | 0.998999 |

Inside ℓ_γ the anomaly is the constant pull **GM/L*²** (checked to 7.7e-6), with **L*² = 2 r_M ℓ_γ** one universal length.

| gate | canonical | alt |
|---|---|---|
| unscreened (γ = 0) Solar-System ratios, 1 AU / Saturn | 2.0e7 / 1.8e7 | 2.2e7 / 2.0e7 |
| **L*_min** (CFG3 gates; Saturn's mass bound binds, ratio 0.964) | **5.75 pc** | **5.75 pc** (the inner pull is a₀-free) |
| SPARC at L* = 0 (K2, = CFG690 T3) | 0.1012 @ Υ 0.46 | 0.1007 @ 0.42 |
| SPARC at L*_min | 0.1012 @ 0.46 | 0.1007 @ 0.42 |
| **L*_max** (rms ≤ 0.110) | **≥ 1000 pc** (grid edge; rms 0.1023) | **≥ 1000 pc** (0.1015) |
| verdict | WINDOW OPEN | WINDOW OPEN |

**MUTATE.**
- M1 (no stiffness): no L* passes the Solar-System gates. Bites.
- M2 (scalar Laplacian): q(10⁻³) = 6.8, not ½; the inner pull is 2e4 × off. Bites.

## Reported (no verdict weight), at L* = 5.75 pc
- **The Sun.** Constant inner pull 4.2e-15 m/s². ℓ_γ(Sun) = 430–470 pc, so the whole Solar System sits deep inside its
  screened core.
- **Wide binaries (2 M☉) are screened, so the anomaly is essentially Newtonian.** anomaly/Newton is 7e-7, 6e-6 and 7e-5 at
  10³, 3×10³ and 10⁴ AU. The unscreened law would give 0.09–0.98. This sector therefore predicts **no wide-binary boost**, unlike
  the law. Gaia DR4 decides. The frozen DR4 pre-registration is not edited.
- **Dwarfs.** ℓ_γ = 14 / 4.3 / 1.4 / 0.14 / 0.014 pc at M_b = 10³ / 10⁴ / 10⁵ / 10⁷ / 10⁹ M☉. The faintest UFDs (about 10³ M☉,
  r_h about 20–40 pc) sit near s ≈ 1–3, where S ≈ 0.4–0.7, so they are partially screened: a reduced boost. CFG259's tables
  carry no stellar masses, so this ladder is generic and disclosed, not a scored row.

## Reading
1. **One stiffness length screens the Solar System and leaves every SPARC galaxy alone.** The reason is that ℓ_γ ∝ M^{−1/2}: the
   lighter the system, the larger its screened core. The window is wide, from 5.75 pc to beyond 1 kpc. This removes the γ = 0
   form's 10⁷-fold Solar-System failure (S5) with the one new constant that CFG679 R1 allows.
2. **The price is a sharp, different prediction.** Wide binaries and the faintest dwarfs lose some or all of their boost. That
   distinguishes this sector from the law itself.
3. **Not settled here.**
   - The Galactic external field: the sector is nonlinear, so the Galaxy's own polarization at the Sun adds a mass term
     2βp_ext to the Sun's perturbation. That changes the screening, and is S2/Q2 territory.
   - C2: the Υ band (CFG690).
   - Lensing (M3a, still FAIL: the coupling is conformal).
   - The attractor and the energy ledger (M1a, M2b).

## Disclosures (2026-10-12)
- **K1 fails as frozen.** The frozen line S(10³) ≥ 0.999 equals the analytic asymptote 1 − 1/s at s = 10³. The solver gives
  0.998999, 1e-6 below. Every other K1 item passes (residual 1.6e-10; q(10⁻³) = 0.49981; inner pull within 7.7e-6). With the line
  read as "S(10³) within 1e-5 of 1 − 1/s", it passes. This is a criteria error, fixed forward here; the frozen file is unchanged.
  The verdict is therefore CONDITIONAL on this correction.
- **L*_max.** It lies at the grid edge (1000 pc), so it is a lower bound, not a measured edge.
- **M_b.** V_bar²R/G at each galaxy's last point (spherical, point-mass screening). This approximation is irrelevant at L*_min,
  where ℓ_γ ≲ 0.1 pc for SPARC masses.
