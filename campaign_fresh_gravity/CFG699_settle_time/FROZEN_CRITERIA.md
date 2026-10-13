# CFG699 — can the cold medium settle in time? (CFG679 M1b for CFG698's identification; frozen criteria, committed alone)

Block CFG690–699 (last ID). Written 2026-10-13, before any CFG699 number. κ = ½ fitted; both footings, never pooled; the cold
energy's mass is required; no particle species; not theory closed.

## Why
CFG698 identified P = −ρ̄_c ξ, which fixes the inertia I = 1/ρ̄_c. About the static (law) profile, a medium element then
oscillates with

ω² = ρ̄_c [W″(P) − 4πG] + ρ̄_c γ k², with W″ − 4πG = 4πG[(1 − x)⁻² − 1], x = u/a₀ (CFG695),

and γ = 2πG L*² (from L*² = 2r_M ℓ_γ and ℓ_γ = γ√a₀/(4πG√(GM)); derived in the script). That timescale is ~1/√(Gρ̄_c), i.e.
cosmological. CFG696's attractor took about 30 local periods with radiation; without radiation it did not relax at all.

## Inputs (framework-native)
- ρ_Λ from each footing: a₀ = κc√(Gρ_Λ), κ = ½.
- ρ̄_c = (Ω_c/Ω_Λ) ρ_Λ, with Ω_c = 0.26 and Ω_Λ = 0.686 (the record's CMB pair).
- Static u from simple μ at y = g_N/a₀ ∈ {0.01, 0.1, 1, 10}.
- Gradient term at k = 1/r, for r = 10 kpc and L* = 5.75 pc.

## Test
- **T1. Element period** T(y) = 2π/ω at those y, both footings.
- **PASS iff T ≤ 1.38 Gyr at y = 0.1 and y = 1 on both footings**, i.e. at least 10 periods within 13.8 Gyr. This is a generous
  bar: CFG696 needed about 30.
- **FAIL** otherwise: CFG698's identification cannot settle halos within the age of the universe, and M1b fails for it.
- Reported: the factor by which T exceeds the bar, and what the inertia would have to be (I_req/I) to pass.

## Reading rule (frozen)
- If T1 FAILS, the radiative mechanism (CFG696) survives only with P an independent field whose inertia is not the cold
  medium's mass. That reopens the two-sector problem (CFG663: cold matter + response; the record needs g_cold ≈ 0 inside
  galaxies), and the cosmic cold mass must come from elsewhere.
- If T1 PASSES, CFG698 stands.

## MUTATE (`CFG699_MUTATE=1`, exit 1 iff it bites)
- ρ̄_c × 10⁴ (a halo-like local density instead of the cosmic mean): T must drop by 100× (ω ∝ √ρ).
