# CFG773 FROZEN CRITERIA: can the tether's field law be built on a bench?

Committed alone, before any script or number. 2026-10-14. Block CFG770–779.

## Question
The γ = 0 action's static field equation is AQUAL with the simple μ: ∇·(μ(|∇Φ|/a0)∇Φ) = 4πGρ, μ(x) = x/(1 + x) ∈ (0, 1).
- Which laboratory medium obeys the same equation?
- Can it be built from real materials?
- Over what range of x?

A web search (2026-10-14) found no MOND/AQUAL bench analogue in the literature.

## Declared steps
- **A1, electric no-go.** The analogue needs ε_r(E) = μ(E/E0) < 1 in a static field. For any passive medium in equilibrium,
  Kramers–Kronig gives ε(0) − 1 = (2/π)∫ε″(ω)/ω dω ≥ 0.
  - Numeric check: 10⁴ random passive Drude–Lorentz media (ε″ ≥ 0) all have ε(0) ≥ 1.
  - Class: ELECTRIC FORBIDDEN if no sample violates it. (Physical reason: gravity's polarization anti-screens, i.e. g > g_N.)
- **A2, magnetic mapping.** In a current-free region with magnetic pole density ρ_m (the ends of long thin magnets):
  H = −∇ψ, ∇·(μ_r(|H|)H) = ρ_m. Mapping: H ↔ g, B/μ0 ↔ the Newtonian flux, μ_r ↔ μ.
  - μ_r < 1 is allowed (diamagnets; superconductors have μ = 0).
  - Check: for a point pole, μ_r(H)H = Q/4πr² reproduces g_N = g²/(g + a0) to 1e-12.
- **A3, superconducting-grain composite (exact design).**
  - Effective medium: Maxwell-Garnett (MG) and Bruggeman (BR). The superconducting grains are μ = 0 spheres; normal grains
    and the matrix are μ = 1.
  - Derive the superconducting volume fraction f_s(x) that makes μ_eff = x/(1 + x):
    - MG: (1 − f_s)/(1 + f_s/2) = μ.
    - BR: μ = 1 − 3f_s/2.
  - From that, the required distribution of grain switching fields, and the lowest reachable x_min for total
    superconducting fraction f.
  - Monte-Carlo with N = 10⁵ grains drawn from the derived distribution. Gate K1: max |μ_eff − x/(1 + x)| ≤ 0.01 over
    x ∈ [x_min, 100].
- **A4, real materials.** Elemental switching fields at T → 0 (from memory, provisional): Al 10.5, In 28.1, Sn 30.5,
  Hg 41, Ta 83, Pb 80.3 mT (type I), and Nb H_c1 ≈ 180 mT.
  - Each grain transitions over its intermediate-state window, from (2/3)H_c to H_c for a sphere.
  - Fit non-negative weights over the 7 materials and a common scale H0 to the A3 target.
  - Report the achievable rms |Δμ| over x ∈ [x_min, 30], for MG at f = 0.5 and BR at f = 0.6.
  - This is an engineering fit, not physics. Class: BUILDABLE if rms ≤ 0.03; otherwise APPROXIMATE.
- **A5, analogue "rotation curve".** For a point pole in the A4 composite, compute H(r) and "V² ∝ rH".
  - Report the radius range over which rH is flat to ±10%, against the exact law.
  - MG has a floor μ_min, so the deep regime is cut off. BR reaches the deep regime only near percolation, which is
    disclosed as critical and model-dependent.

## Classes (the headline)
- **ELECTRIC FORBIDDEN** (A1).
- **MAGNETIC BUILDABLE / APPROXIMATE** (A4).
- **DEEP REGIME REACHABLE / NOT** (A5): reachable if BR gives a flat rH over ≥ 1 decade in r.

## MUTATE (CFG773_MUTATE=1)
- M1: grains with μ = 2 (paramagnetic) instead of 0. The required f_s becomes negative, i.e. impossible. The tooth must
  report no solution.
- M2: shuffle the A4 materials' critical fields by a factor of 10. The rms must worsen.

## Hand estimate (before any script)
- A1: forbidden.
- A3: MG f_s = 2/(2 + 3x) and BR f_s = (2/3)/(1 + x). Both need a shape-1 Lomax (Pareto II) distribution of switching
  fields. x_min(MG, f = 0.5) = 0.67.
- A4: 7 materials span about 17× in field. The fit is probably APPROXIMATE over 1.5 decades in x.
- A5: MG has no flat region (floor μ_min = 0.4, a boost of ≤ 2.5×). BR is flat only near percolation.

## Disclosures fixed now
- This is an analogue of the field equation only. It cannot reproduce cold energy, the tether's dynamics, or a0's tie to
  ρ_DE.
- Effective-medium theories are approximate; Bruggeman is unreliable near percolation.
- Critical fields are from memory (provisional).
- κ fitted; not theory closed.
