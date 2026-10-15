# CFG790 FROZEN CRITERIA: a hypothetical "cold-energy haloscope". Could a lab device convert ambient cold energy to light, and how much?

Committed alone, before any script. 2026-10-15. Block CFG790–799 (reserved in LEDGER in this commit). Owner: "figure out a
hypothetical mechanism to [bottle cold energy] ... swing it".

## Idea
- Do not compress cold energy; Liouville forbids that without dissipation.
- Convert it in place to photons via a hypothetical portal, and store the energy. This is the axion-haloscope principle.
- The record allows cold energy to be particle-like with m ≤ 16–143 eV (CFG723/725).

## Two declared portal classes (natural units; provisional external bounds quoted from memory)
- **A, photon coupling g (axion-like, needs a magnetic field B).**
  - The spontaneous decay rate is Γ = g² m³/(64π). CFG789's sky limit τ ≥ 4.4 × 10¹⁵ yr caps g(m).
  - Literature bounds near 2–5 eV (MUSE dwarf spectroscopy, ~10⁻¹² GeV⁻¹) are also reported.
  - Device: a magnetised mirror (dish antenna), P/A = g² B² ρ / m². B = 10 T, A = 10 m².
- **B, kinetic mixing ε (dark-photon-like, converts at any conductor, no B needed).**
  - Spontaneous decay is negligible, so the sky bound is weak.
  - Bracket ε ∈ {10⁻¹², 10⁻¹⁴} (stellar/laboratory bounds near eV masses; provisional).
  - Device: a dish antenna, P/A = ε² ρ.
- Masses: m = 1, 2, 3, 10, 100 eV. ρ = 0.01 M☉ pc⁻³ (≈ 0.38 GeV cm⁻³).

## Outputs
- P per device and photon rate N = P/m.
- The factor short of 300 MW (1 N light drive) and of 1 W.
- Photon colour (λ = hc/m; 2–3 eV is visible).

## Classes
- **HARVEST CLOSED** if P < 1 μW for every class at its bound.
- **DETECTABLE** for a class if N ≥ 1 photon/day for a 10 m² device: a tabletop search is then viable.
- Report both.

## Controls
- K1: unit conversion 1 GeV⁴ = 6.26 × 10⁴⁵ W m⁻², and 1 T = 1.95 × 10⁻¹⁶ GeV², to 1%.
- K2: the class-A g bound reproduces Γ ≤ 7.2 × 10⁻²⁴ s⁻¹ (CFG789).
- MUTATE (CFG790_MUTATE=1): B → 0. Class A power must vanish; class B must be unchanged.

## Hand estimate
- A: g ≤ 3 × 10⁻¹⁰ GeV⁻¹ at 2 eV (sky). P(10 m², 10 T) ~ 10⁻²⁶ W, ~1 photon/yr.
- B: ε = 10⁻¹² gives P ~ 10⁻¹⁹ W, ~ 10⁻¹ photon/s.
- **HARVEST CLOSED by ≳ 30 orders. DETECTABLE for class B at ε ~ 10⁻¹².**

κ fitted; not theory closed. Hypothetical portals; no coupling is derived in the framework.
