# CFG678-G2 FROZEN CRITERIA: the cheapest well-posed cold-energy sector (gate B3/A2)

Sub-lane of CFG678 (no new id; owner: "you try it", 2026-10-13). Committed alone before any script exists. This is a derivation
lane: no data, apart from the SPARC harness already used by CFG660 (read-only). Astra's files are not touched.

## Starting point (record)
- CFG660: the law is an exact equilibrium of a field-aligned stress P∥(g), P⊥ − P∥ (S1). As an independent-density medium it is
  ILL-POSED: WKB growth ∝ √k (S5). The cause is the term i k g₀ δρ (background weight on a density perturbation, through
  continuity), with no k² restoring term, because the stress does not respond to compression.
- CFG661: P(ρ_c, ρ_b, g) keeping the law exact for every spherical baryon profile has the form P_A(g) + Ψ(u/h), with
  u = ρ_c − (F′ − 1)ρ_b (u ≡ 0 on the law) and u/h of dimension 1/length. With {G, a₀} alone, Ψ is constant (ill-posed).

## Candidate (stated before computing)
P∥ = P_A(g) + (g²/4πG) Ψ(ℓ · 4πG u / g), with Ψ(0) = 0 and Ψ′(0) = ψ > 0. Two choices of ℓ:
- **(C) c-built:** ℓ = c²/a₀, with ψ = O(1). No new constant.
- **(K) new constant:** ψ ℓ treated as one free constant, declared as +1.

## Gates (PASS lines frozen here)
- **G2-1 equilibrium (S1 kept):** on u ≡ 0 the equilibrium residual is identically zero for general F and ρ_b (sympy). Also
  N1/D1: the SPARC rms equals the law's to ≤ 1e-6 dex (it must, since u ≡ 0; checked numerically by re-using CFG660's harness only
  if cheap, otherwise by the sympy identity alone, stated).
- **G2-2 well-posed:** with c_s² = ∂P∥/∂ρ_c|_{u=0} > 0, the WKB max Im ω (CFG660's S5 system, same deep SIS point
  g = 0.1 a₀, τ_ff = 1) is bounded as k → ∞. PASS iff Im ω(k = 1e5) ≤ 1.1 × Im ω(k = 1e3) for both (C) and (K) at the values
  below. The analytic high-k limit Im ω → g₀/(2 c_s) is checked to 5%.
- **G2-3 independence (the cost):** cold energy must stay an independent, collisionless-like component on cluster scales (the
  record needs it for clusters, the Bullet and lensing; CFG624, CFG660 reading 4a). Proxy declared here: the u-sound speed at
  g = a₀ may not exceed a rich cluster's velocity dispersion, c_s(g = a₀) ≤ 1000 km/s; otherwise u relaxes to 0 faster than a
  crossing time and ρ_c is slaved to the baryons (option (a) of CFG660, which gives up independent cold energy).
  - (C) PASS iff c_s(a₀) ≤ 1000 km/s at ψ = 1.
  - (K) report the largest ψℓ allowed, and also the smallest ψℓ that keeps the high-k growth Im ω ≤ 10/τ_ff at the deep SIS
    point (well-posed AND not violently unstable). (K) PASSES iff that window is non-empty, at the cost of +1 constant.
- **G2-4 lensing / one metric:** cold energy is mass, so it lenses (CFG663) and uses the one metric (CFG670). Stated, not
  computed; the relativistic completion is OUT OF SCOPE and stays open (it blocks a full B3 PASS).

## Verdict wording (frozen)
- If (C) passes G2-1..3: "c-built compression sector: well-posed and independent at zero new constants".
- If (C) fails G2-3 and (K) passes: "well-posedness costs exactly +1 constant (window [lo, hi]); with c alone the cold energy is
  slaved".
- If both fail: "door closed at this order".
Either way B3 stays OPEN until a relativistic completion exists.

## MUTATE
ψ = 0 (no compression response): G2-2 must FAIL (√k growth returns).

κ = ½ fitted; cold energy mass required; no particle; not theory closed.
