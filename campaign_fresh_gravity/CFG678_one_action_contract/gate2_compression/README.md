# CFG678-G2: the cheapest well-posed cold-energy sector. VOID AS FROZEN (premise error); the question reduces to CFG661

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone (1147466be). No script was written and no number computed.

## Why VOID
The frozen candidate assumed u = ρ_c − (F′ − 1)ρ_b vanishes on the law, so that Ψ(0) = 0 would leave the equilibrium untouched.
That is false.
- On the law, spherical Poisson gives ρ_c = (F′ − 1)ρ_b + 2(F − F′g_N)/(4πG r). So u ≠ 0.
- CFG661 T2b (sympy, committed) gives the exact invariant: on shell, u/h = 1/r, with h = g(1 − s)/2πG.

With the correct form the frozen gates reduce to results already on the record:
- **G2-1 (equilibrium):** holds for arbitrary Ψ(u/h), provided P⊥ carries −(u/2)∂P∥/∂u (CFG661 T2b).
- **G2-2 (well-posed):** bounded growth iff Ψ′ > 0. Im ω is 4.7 and 1.36 per τ_ff at c_eff² = 0.01 and 0.5 (CFG661 T3(ii)).
- **G2-3 (the cost):**
  - With {G, a₀} there is no dimensionless group, so Ψ is constant and the sector is ill-posed (CFG661 T3(i)).
  - With c there is one group, c²(u/h)/a₀, which equals c²/(a₀ r) on shell (~10⁶ at kpc). Ψ is then an arbitrary function of it.
  - No universal Ψ reproduces even the Jeans-like c_eff² = V²/2 (CFG661 T4).
  - So **well-posedness costs a free function** (at least one new constant if Ψ is a power law). c alone does not fix it.

## Reading for gate B3/A2
The local, first-order door is closed: with {G, a₀} it is impossible, and with c it needs a free function. The remaining doors
are the ones CFG661 named:
- gradient stiffness (astra's sourced polarization, with its own γ);
- a declared new constant;
- target relaxation (giving up exactness).

**One lead not on the record** (a hypothesis, untested). CFG661's invariant gives a *local* inverse length w = u/h that equals
1/r on shell. A gradient-stiffness term written as (k/w)² is dimensionless, so it needs no new dimensional constant (only a pure
number). Whether such a term can keep the equilibrium exact and bound the growth is the next calculation. It is not claimed here.

κ = ½ fitted; cold energy mass required; no particle; not theory closed.
