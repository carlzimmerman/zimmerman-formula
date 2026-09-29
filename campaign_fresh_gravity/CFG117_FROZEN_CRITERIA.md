# CFG117 — Door 2: Verlinde's emergent gravity mapped onto the CFG44 target. FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. The menu of ten doors (closure_map/TEN_DOORS_GATES_2026-09-29.md, 5ef77ea09) was written knowing the target. The shared gates G1–G5 there are binding; this file adds lines but weakens none. A scoped no-go is a valid result.

## The question

Verlinde (2016, "Emergent Gravity and the Dark Universe", SciPost Phys. 2, 016 (2017)) gives an apparent dark mass for a spherical baryon distribution:

M_D²(r) = (a_V r² / G) · d(M_B(r) r)/dr, with a_V = cH/6.

1. **G1:** does it reproduce CFG44's target C(r) ≡ ρ_c r³ g_tot = (a₀/4π) M_b(<r)?
   - Here ρ_D = M_D′/(4πr²) plays ρ_c, and g_tot = G(M_B + M_D)/r².
   - The pass line is within 10% over x = r/r_M in [0.1, 30], with r_M = √(GM_b/a₀).
   - It is checked for a point mass and for CFG44's exponential spheres, at M_b = 10⁹, 10¹⁰, 10¹¹, 10¹² M☉ (h = 2, 3, 4, 5 kpc, as CFG44/CFG50), with the same constants at every mass.
2. **The a₀ mapping:** what κ does a_V correspond to?

## Declared choices

- **H in a_V, both carried:** H₀ (Verlinde's text) and H_Λ = H₀√Ω_Λ (the asymptotic de Sitter rate). Planck18: H₀ = 67.4, Ω_Λ = 0.685.
- **The κ identity:** with H_Λ, a_V = κ_V c√(Gρ_Λ) gives κ_V = √(8π/3)/6. With H₀, κ_V′ = √(8π/3)/(6√Ω_Λ).
- **The target's a₀:** κ = ½ on both footings (canonical 9.36e-11, alt 1.13e-10).
  - **G1 is scored with a₀ = a_V,** so the comparison is of the shape, not the normalisation.
  - **R2 reports the normalisation mismatch separately.**
- **The target itself** comes from CFG44's `Bcommon` (exp_sphere, target_fields), imported read-only.

## Checks

- **C1 CONTROL (point mass, analytic):** Verlinde gives M_D = M x, so the ratio is C_V/C_target = (1 + x)/x at every x. The code must reproduce this to 1e-9. It is 1.033 at x = 30.
- **C2 CONTROL:** the exponential-sphere target from Bcommon reproduces CFG44's committed C(r) = (a₀/4π) M_b(<r) to 1e-9.
- **H1 [HEADLINE; MUTATE must change it]:** G1 holds: C_V/C_target lies in [0.9, 1.1] over x in [0.1, 30], for every mass and both geometries.

## Reported rows

- **R1:** the ratio curves; the largest deviation; the x range where the ratio is within 10%; the ratio at x = 0.1, 1, 3 and 10.
- **R2:** the normalisation: a_V/a₀ for both H choices and both footings, and κ_V and κ_V′ against the fitted κ windows, 0.465 ± 0.076 (BTFR) and 0.55 ± 0.17 (distance-free).
- **R3, G2–G5 as statements** (no computation; sources read from arXiv abstract or HTML pages, no downloads):
  - G2: are cosmological perturbation equations defined in Verlinde 2016?
  - G3: does an action exist that makes reciprocity well defined?
  - G4: is the 1/6 derived in the framework or a new constant?
  - G5: field equations, ghosts and the Solar System; for example Hees et al. 2017 on planetary ephemerides, and Lelli et al. 2017 on the radial acceleration relation.
  - Each gate is marked PASS, FAIL or UNDEFINED (no equations to test).

## MUTATE

MUTATE=1 replaces Verlinde's M_D by the target's own point-mass cold mass, M(√(1 + x²) − 1). H1 must then pass (ratio 1 everywhere), so the MUTATE changes the headline. This checks that the G1 evaluator can pass.

## Readings (declared)

- **H1 PASS:** Verlinde's formula lands on the target's shape. G2–G5 are then assessed.
- **H1 FAIL:** a scoped no-go on G1.
  - The reading says where the formula fails, by how much, and why. A likely cause is the linear sum M_B + M_D, against the target's √(1 + x²) structure.
  - R2 says whether Verlinde's a₀ normalisation is consistent with the fitted κ in any case.
- **Untested hypotheses (declared):**
  - Verlinde's covariant or later formulations, for example Hossenfelder's covariant version, and non-spherical systems.
  - The formula's domain of validity (Verlinde states it is for quasi-static, spherical, isolated systems).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
