# CFG661 FROZEN CRITERIA: can a stress that responds to compression keep the law as cold energy's exact equilibrium?

Date: 2026-10-12. Written and committed ALONE, before any CFG661 code exists. Block CFG660–669 (owner reservation). Nothing below
may be edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is fitted. Footings never pooled (no check below depends on a footing). The cold energy's mass is required. No particle
species. Not "theory closed". Nothing will be phrased as "the data favour the framework". No knob scans.

## 0. What has been seen (stated before any choice below)

- CFG660 (53e9e6e56): the field-aligned stress Π_A(g) makes the law an exact equilibrium for any spherical baryon profile; it is
  NOT KINETIC and ILL-POSED as an independent-density medium (growth ∝ √k), because ∂Π/∂ρ_c = 0. With a kinetic pressure the
  growth is bounded (1.36/τ_ff at the test point).
- **Author's hand derivation, done before this commit (to be confirmed or refuted in sympy):**
  (a) a stress P∥(ρ_c, g) keeps the law exact for all spherical profiles only if ∂P∥/∂ρ_c = 0 where F′ ≠ 1, because ρ_c′
  carries g_N″, which nothing else cancels;
  (b) with the local baryon density allowed, P∥(ρ_c, ρ_b, g), cancellation of g_N″ forces dependence through
  u = ρ_c − (F′(g) − 1)ρ_b, and the general solution is P∥ = P_A(g) + Ψ(u/h(g)), h = g(1 − s)/2πG, with Ψ arbitrary and P⊥ fixed
  algebraically;
  (c) u/h has units of 1/length, so with only {G, a₀} Ψ is a constant: no compressional response;
  (d) with c allowed, Ψ = (a₀²/G) f(c² u/(a₀ h)) has a free function, and no universal Ψ reproduces a Jeans-like support
  c_eff² = V²/2 at every radius of every galaxy.
  Expected label: NO-GO (local, first-order in derivatives, spherical, constants {G, a₀}).

## 1. Scope (stated so the label cannot be over-read)

Newtonian, spherical symmetry (round rule), local stresses that are functions of (ρ_c, ρ_b, |g|) with no gradient terms,
field-aligned (Π = P⊥I + (P∥ − P⊥)ĝĝ). Gradient (Korteweg / quantum-pressure-like) stresses, non-spherical systems, and
relativistic completions are out of scope and stated as open. "Exact" means: the law g = F(g_N) (ν_mono, read-only) satisfies the
radial equilibrium dP∥/dr + 2(P∥ − P⊥)/r = −ρ_c g identically for every spherical ρ_b(r), with ρ_c the law's phantom
(Poisson with G9).

## 2. Checks

- **T1 (sympy):** for P∥(ρ_c, g), P⊥(ρ_c, g) arbitrary smooth functions, the coefficient of g_N″ in the on-shell equilibrium
  residual is P∥,ρc·(F′ − 1)/4πG. Confirmed iff sympy returns exactly that coefficient (so exactness forces P∥,ρc = 0 where
  F′ ≠ 1).
- **T2 (sympy):** for P∥(ρ_c, ρ_b, g): the g_N″ coefficient vanishes iff P∥,ρb = −(F′ − 1)P∥,ρc. With P∥ = P_A(g) + Ψ(u/h(g))
  and P⊥ = P∥ − (u/2)∂P∥/∂u + g(g − g_N)/4πG, the on-shell residual is identically zero for an ARBITRARY function Ψ. Confirmed iff
  both hold.
- **T3 (dimensions + WKB):** (i) list the dimensionless combinations of u/h with {G, a₀}: none (sympy nullspace of the dimension
  matrix), so Ψ is constant; (ii) local WKB along the field for the T2 family with Ψ linear, slope Ψ₁: max Im ω grows ∝ √k iff
  Ψ₁ = 0 and stays bounded for Ψ₁ > 0 (test point: CFG660's deep SIS point g = 0.1 a₀).
- **T4 (with c allowed):** the dimensionless group is c²u/(a₀h), so Ψ = (a₀²/G) f(·), f free. Test whether a universal Ψ can give
  c_eff² ≡ ∂P∥/∂ρ_c = V²/2 = g r/2 on-shell: requires Ψ′(1/r) = g² r(1 − s)/(4πG) for all (r, g), which depends on g at fixed r.
  Confirmed (no universal Ψ) iff sympy shows ∂/∂g of the required Ψ′ at fixed r is nonzero.
- **MUTATE (`CFG661_MUTATE=1`, exit 1 iff all bite):** M1, T1 with ρ_c′ replaced by an expression without g_N″ must make the
  coefficient vanish (the theorem relies on that term); M2, T2 with u built with F′ instead of F′ − 1 must leave a nonzero residual.

## 3. Label

- **NO-GO (local, first-order, spherical, {G, a₀})** iff T1, T2, T3(i) and T3(ii) are all confirmed.
- **DOOR OPEN** iff T3(i) finds a dimensionless combination (an error in the hand derivation), with the family stated.
- T4 is reported as the "with c" addendum: **NEEDS A FREE FUNCTION** if f is unconstrained, plus the Jeans-mimic result.

## 4. Machine rules

Light (sympy + one WKB evaluation): one process, `nice -n 10`, allowed while the 1024³ run is live.
