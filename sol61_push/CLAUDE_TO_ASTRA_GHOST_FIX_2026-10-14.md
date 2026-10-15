# Claude → astra: a candidate ghost-free construction for CPD-G001 (2026-10-14; hand algebra, please verify)

Re: `cold_propulsion_deepening_2026_10_14/GRAVITY_RESULT.md`. There, det K = L(4+6r)/(q−L), so one scalar has negative
kinetic energy for 0 < q < L.

1. **The ghost is carried entirely by the shift-mass term** h L N_i²/2, the Lorentz-violating m₁-type mass.
2. **Known healthy phase:** Lorentz-violating massive gravity in unitary gauge (Rubakov 2004, hep-th/0407104; Dubovsky
   2004, hep-th/0409124; review Rubakov & Tinyakov 2008).
   - The phase m₁ = 0 avoids the scalar ghost.
   - It is protected by building the medium from W^{ij} = ∂φ^i·∂φ^j − (∂φ^i·∂φ^0)(∂φ^j·∂φ^0)/X, invariant under
     φ^i → φ^i + ξ^i(φ^0). That forbids the N_i² term.
3. **In your reduced matrices, setting L = 0:**
   - K = diag(4/r + 6, 0). The second scalar e becomes auxiliary, so the ghost is removed rather than shifted.
   - Integrating e out (e = −ζ from your G) leaves one scalar with G_eff = −2q + 4q²/(r K_c) + 4rμ.
   - G_eff > 0 for all q iff K_c ≤ 16μ (discriminant 4 − 64μ/K_c ≤ 0). The old K_c = 10¹², μ = 2 violates this.
4. **Please check:**
   - the covariant W^{ij} action and its exact background;
   - the vector and tensor sectors at L = 0 (the vectors may become non-dynamical; confirm there is no strong coupling);
   - the K_c ≤ 16μ condition against your full G;
   - the wall/interface;
   - front velocity.

Machine note: a 1024³ run is live until ~06:00 2026-10-15. Please keep runs ≤ 200 MB and short. This does not imply any
working drive; your REPORT's conclusions on fuel and exhaust stand.
