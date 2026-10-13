# CFG697: the CFG691–696 construction against the record's hard gates

**Label: GALAXY MECHANISM.** The construction passes every galaxy-scale gate it was run on. It fails the cluster and cosmology
gates exactly as CFG624's "no cold energy" model does, because once relaxed it *is* that model with simple μ. It also supplies
no mean cold density (⟨∇·P⟩ = 0). It is a mechanism for the law's phantom, not for the cold energy.

- **Criteria:** `FROZEN_CRITERIA.md` (5c5d22bd5), committed alone before any cell.
- **Script:** `python3 cfg697.py` (seconds) → `cfg697.out`, `cfg697_results.json`.
- **Settings:** κ = ½ FITTED; the cold energy's mass is required; no particle species; not "theory closed".

## How much the interpolation moves the inherited gates (`cfg697.out`)

| range | ν_simple / ν_mono |
|---|---|
| X-COP clusters (y 0.3–3) | 1.009–1.038 |
| deep regime: Local Group, C3, satellites (y 10⁻³–0.1) | 1.000–1.004 |
| SPARC (y 0.01–30) | 1.000–1.038 |

## Scorecard

| gate | status | source |
|---|---|---|
| lensing = dynamics (Newtonian limit) | PASS (structural) | CFG692, CFG694 |
| mass/energy ledger | PASS | CFG692 T3; CFG696 A2 |
| attractor from non-law states | PASS (spherical, fixed baryons) | CFG696 |
| SPARC (C2) | PASS 0.1009 @ 0.60 / 0.0994 @ 0.55 | CFG695 |
| Solar System / Cassini | PASS (L* ≥ 5.75 pc) | CFG691, CFG693 |
| stars carry no halos | PASS (3.5%) | CFG694 |
| satellites, no EFE (PAPER44) | PASS (basin edge = aperture; unscreened) | CFG693, CFG694 |
| groups (Tian+26 BFJR) | INHERITED PASS | CFG624 G4b |
| **X-COP clusters** | **INHERITED FAIL**: NCE gives 0.55 / 0.60 of the measured mass; simple μ adds ≤ 3.8%, so at most 0.57 / 0.62 | CFG624 G2 |
| **Bullet** | UNTESTED: the static identity puts the lensing on the gas (NCE +7.9σ); a slow c_P could make it lag, not run | CFG624 G3 |
| **Local Group timing** | **INHERITED FAIL** (too fast, z +4.9 / +6.4); deep regime, ratio ≤ 1.004 | CFG624 G4a |
| **cosmic shear / growth (D2)** | **INHERITED FAIL**: no basins in linear cosmology, so Newtonian baryons; σ₈ ≈ 0.01 | CFG624 G5 |
| **CMB / background cold mass** | **FAIL**: ⟨∇·P⟩ = 0, no mean cold density | theorem (this lane) |
| early types (C3) | INHERITED FAIL (deep amplitude, ratio ≤ 1.004) | CFG529, CFG678 |
| wide binaries | prediction: Newtonian (Gaia DR4) | CFG691, CFG694 |

## Reading
1. **What has been found.** A worked, testable mechanism for the *galaxy-scale* part. The law's phantom is the bound charge of a
   critical, saturating vacuum polarization field. It reaches the law's profile by radiating, conserves mass and energy, lenses,
   hides the Solar System, and ignores external fields.
2. **What has not been found.** The cold energy that clusters, the Bullet, Local Group timing, cosmic growth and the CMB need.
   Here the cold mass is only *displaced*, never added: on cosmic average it is zero. This is the same wall CFG624 found for
   "no cold energy", now with a mechanism attached.
3. **The obvious next step (named, not tested).** Make P the displacement of a real cold medium with mean density ρ̄_c,
   P = ρ̄_c ξ.
   - Then ⟨ρ_c⟩ = ρ̄_c ≠ 0 (background and CMB), and the bound charge −∇·(ρ̄_c ξ) is literally cold mass *moved* toward the
     baryons.
   - The kinetic constant is fixed: I = 1/ρ̄_c.
   - The tether W(P) resists displacement relative to the cosmic (dark-energy) frame.
   - Algebra in the scored action suggests the critical quadratic then exactly cancels the medium's own Jeans instability. This
     needs checking, because it decides whether the medium can also cluster like a cold component on large scales (clusters,
     D2). That is the next lane.
