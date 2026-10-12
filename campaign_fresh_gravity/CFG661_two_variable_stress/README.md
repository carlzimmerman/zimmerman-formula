# CFG661: can a stress that responds to compression keep the law as cold energy's exact equilibrium?

**Label: NO-GO (local, first-order in derivatives, spherical, constants {G, a₀}); with c: NEEDS A FREE FUNCTION; no universal
Jeans mimic.**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (abd99a242), 2026-10-12. Block CFG660–669. The author's hand
  derivation was disclosed there before any code; sympy confirms every step.
- **Settings:** κ = ½ FITTED; the cold energy's mass is required; no particle species; not "theory closed".
- **Script:** `cfg661.py` (sympy + one WKB evaluation; seconds; exit 0) → `cfg661.out`, `cfg661_results.json`.
  `CFG661_MUTATE=1` exits 1 as designed (M1, M2 bite) → `_MUTATE` outputs.

## Results

| check | result |
|---|---|
| **T1** P∥(ρ_c, g), general law F | coefficient of g_N″ in the on-shell equilibrium = (∂P∥/∂ρ_c)(F′ − 1)/4πG exactly. Exactness for every spherical baryon profile forces ∂P∥/∂ρ_c = 0 wherever F′ ≠ 1: no compressional response |
| **T2a** P∥(ρ_c, ρ_b, g) | coefficient = [P,ρc (F′ − 1) + P,ρb]/4πG: cancellation forces dependence through u = ρ_c − (F′(g) − 1)ρ_b |
| **T2b** family P∥ = P_A(g) + Ψ(u/h(g)), h = g(1 − s)/2πG, P⊥ = P∥ − (u/2)∂P∥/∂u + g(g − g_N)/4πG | residual **identically zero for arbitrary Ψ** (explicit law g_N = g²/(g + a₀)). On-shell u/h = 1/r: the free function depends on a local quantity that equals 1/r in equilibrium |
| **T3(i)** dimensions | u/h has units 1/length; **no** dimensionless group with {G, a₀} ⇒ Ψ constant ⇒ ∂P∥/∂ρ_c ≡ 0. With c: one group, c²(u/h)/a₀ |
| **T3(ii)** WKB at CFG660's deep point | Ψ flat: Im ω 2.5 / 21 / 214 (√k, ill-posed). Ψ′ > 0 (c_eff² = 0.01, 0.5): bounded at 4.7 and 1.36 per τ_ff |
| **T4** with c, Jeans mimic c_eff² = V²/2 | needs Ψ′(1/r) = g² r(1 − s)/4πG, which depends on g at fixed r: no universal Ψ |
| MUTATE | M1 (no g_N″ in ρ_c′): the coefficient vanishes, so T1 rests on that term. M2 (u built with F′): residual nonzero |

## Reading

Together with CFG660: with only G and a₀, no local, first-order stress of cold energy can make the law both an exact equilibrium
and a well-posed dynamics. The escapes are named: **gradient (stiffness) terms**, which carry their own length scale; a
**new constant** (c enters only through a free function); or giving up exactness (the record's target relaxation). astra's
stable sourced-polarization construction (`sol61_push/cold_production_2026_10_11/mechanism_2026_10_12/STABLE_SOURCED_RESPONSE.md`)
is an instance of the first escape: a separate field with stiffness γ|∇P|², stable for fixed sources, with an onset length
ℓ_γ = γ/(βB) ∝ M^(−1/2). Out of scope here: gradient stresses, non-spherical systems, relativistic completion.
