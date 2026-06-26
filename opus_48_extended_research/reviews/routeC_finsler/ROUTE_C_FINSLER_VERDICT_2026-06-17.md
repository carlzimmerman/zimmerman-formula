# Route C — Finsler / acceleration-dependent geometry for dS-Unruh modified inertia: VERDICT (2026-06-17)

**Charge:** write the Finsler free-particle action whose geodesics are the MI trajectories
`m·a·μ_fw(|a|/a0)=F`, and ask whether it lifts to a covariant field theory with a consistent
lensing sector. Honest: Finsler MI may be only a reformulation — say so if it yields no new
field content. All load-bearing claims sympy-verified (c7: 9/9 PASS); primaries read verbatim
via pdftotext.

## VERDICT: **OBSTRUCTED** (as a covariant MI action) — Finsler is a REFORMULATION that REPRODUCES the Milgrom-1994 no-go, and the only healthy Finsler theory is the velocity-keyed MODIFIED-GRAVITY sibling (AeST/AQUAL), not the framework's acceleration-keyed MI.

The route splits into two honest readings, and **neither is a covariant MI action:**

### Reading (I) — acceleration-keyed Finsler (the framework's actual TARGET): **GHOST / NO LOCAL ACTION**
- The MI law is the 2nd-order ODE `a·μ_fw(a/a0) = −Φ'(x)`, with `a·μ_fw(a/a0) = −a0/2 + √(4a²+a0²)/2` a **transcendental (non-polynomial) function of the acceleration ALONE** (c7 check 5).
- **No ordinary Finsler structure F(x,y) can produce it.** F(x,y) is homogeneous degree-1 in the tangent vector y=dx/dτ; its inertia tensor `g_μν=½∂²F²/∂yᵘ∂yᵛ` depends on position+velocity only — never on the 2nd-jet acceleration a (c2, c5B). This is Step-2/Milgrom-1994 in Finsler language: a velocity-Hessian cannot carry μ_fw(|a|/a0).
- **The acceleration-jet (Lagrange/Kawaguchi) Finsler structure that genuinely sees `a` is a higher-derivative Lagrangian → Ostrogradski ghost.** I constructed the natural Finsler-2 kinetic scalar `T(a)=∫a·μ_fw da = −a·a0/2 + a√(4a²+a0²)/4 + (a0²/8)asinh(2a/a0)` (c3/c7 check 4, dT/da=a·μ_fw exactly). Its `T''(a)=2a/√(4a²+a0²) ≠ 0` for all a>0 (c7 check 5) ⇒ **nondegenerate in xddot ⇒ Ostrogradski Hamiltonian H = P1·Q2 + [Legendre(T)] + Φ(Q1), linear in P1, unbounded below → linear ghost.**
- **A clean dichotomy theorem (c4, sympy-grounded):** any local `L(x,ẋ,ẍ,…)` whose EL is the 2nd-order MI law must have either (i) `L_aa=0` ⇒ a-dependence only LINEAR ⇒ cannot match the nonlinear μ_fw; or (ii) `L_aa≠0` ⇒ 4th-order EL + Ostrogradski ghost (and the EL is then the 2nd time-derivative of the force-law, not the force-law). **No healthy local Finsler/Lagrange action for the MI exists.** Finsler ADDS NO NEW FIELD CONTENT for Reading (I) — it re-derives the no-go.

### Reading (II) — the PUBLISHED "Finsler MOND" (Chang-Li 0806.2184; Finslerian-lensing 1309.1343; Pfeifer-Wohlfarth): **velocity-keyed MODIFIED GRAVITY — the AeST/AQUAL sibling, not the MI**
- Chang-Li get MOND from the **weak-field of the Berwald-Finsler FIELD EQUATION** → `∇²φ = 4πGρ·f(v)`, a **modified Poisson** (modified GRAVITY); the geodesic equation keeps its standard form. The law is `a = (GM/r²)·ν(GM/r²a0)`.
- **sympy (c5/c7 check 6): Chang-Li's law equals the framework's `g_obs=√(g_bar²+g_bar·a0)` EXACTLY** — but as a function of `g_bar` (position/field), i.e. modified GRAVITY, the AQUAL/AeST family. This is the **static-RAR degeneracy** the session already established: MI and MG agree on circular orbits, diverge on Cassini/EFE/plunge. The Finsler structure is **velocity-keyed**, which on circular orbits (v=v(r)) MIMICS a position-keyed gravity law — exactly how it lands the MG ν.
- a0 enters **by hand** ("deformation parameter"); Λ only NOTED (`2πa0≈c√(Λ/3)`), never derived; the rotation-curve fit uses a0=1.2e-10 — NOT the framework's 9.36e-11 nor κ.

## TARGET-PROPERTY SCORECARD
- **Reproduces MI law (test limit):** Reading I — NO healthy action (ghost/no-go); Reading II — reproduces the static `g_obs` but as MG, not MI (PARTIAL, wrong key).
- **Four limits (on the shared static law, c6/c7):** Newtonian `g_obs→g_bar` PASS; deep-MOND `g_obs→√(g_bar a0)`, `v⁴=GMa0` BTFR PASS; cosmological CMB-safe (a≫a0⇒GR at high z) PASS-at-background but INHERITED from a host, not from Finsler; GW `c_T=c` PASS-CONDITIONAL (Berwald/near-Riemann corner only; generic Finsler anisotropy is a Lorentz-violation/birefringence risk).
- **Ghost-free:** Reading I — NO (Ostrogradski, c3); Reading II — yes in the Berwald corner (it is AeST-class).
- **Lensing/metric sector (Bullet Cluster):** Reading II DOES supply one (modified h00; light-deflection = GR-angle × "Finslerian rescaling factor"; fits early-type lenses and, with ad-hoc dipole+quadrupole, the Bullet Cluster without DM) — **BUT underived:** verbatim "we cannot solve the field equations to derive the Finslerian rescaling factor … the factor is just a HYPOTHESIS"; 3 free params (a0, rc, vc); "one can choose the parameters such that the gravitational mass exactly matches." Reading I (the MI) leaves the metric UNDETERMINED — Finsler does not close the framework's known lensing gap.

## NOGO STATUS vs Milgrom-1994
Finsler **OBEYS** the no-go, does not evade it. Ordinary Finsler F(x,y) is a local Galilei-covariant velocity-Lagrangian → foreclosed by the same theorem. The acceleration-jet Finsler is the higher-derivative route the no-go warns about → Ostrogradski. The established time-NONLOCAL Galley worldline functional remains the only licensed MI home, and it is **not a finite-order Finsler structure** at all.

## HONEST ONE-LINE
Route C is **OBSTRUCTED**: the Finsler reformulation of dS-Unruh modified inertia reproduces the Milgrom-1994 no-go rather than evading it — an ordinary Finsler F(x,y) is velocity-keyed and cannot carry μ_fw(|a|/a0) (acceleration is a 2nd-jet object it never sees), and the acceleration-jet (Lagrange/Kawaguchi) Finsler that does see a is a nondegenerate higher-derivative Lagrangian with an Ostrogradski ghost (T''=2a/√(4a²+a0²)≠0 everywhere); the only healthy Finsler theory in the literature (Chang-Li/Pfeifer) is the velocity-keyed MODIFIED-GRAVITY sibling whose static law equals √(g_bar²+g_bar·a0) EXACTLY but as a function of the field (= AeST/AQUAL, the very sibling the session already identified), with a0 by hand and an UNDERIVED 3-parameter "Finslerian rescaling factor" lensing sector — so Finsler supplies **no new covariant MI field content**: it is a reformulation that re-lands the no-go on one branch and the MG host on the other.

## CAN / MUST NOT
- **CAN:** Finsler cleanly RE-DERIVES the Milgrom-1994 no-go (ordinary F(x,y) is velocity-keyed, can't see a); the acceleration-jet Finsler T(a) is constructible in closed form but Ostrogradski-ghosted; the published Finsler-MOND is the MG/AeST sibling (its static law = framework g_obs exactly) with a real but underived lensing sector — useful as confirmation of the MI-vs-MG split.
- **MUST NOT:** "Finsler gives the covariant MI action" (no — ghost or no-go); "Finsler MOND is the framework" (it's velocity-keyed modified GRAVITY, a0 by hand); "Finsler closes the lensing gap" (the rescaling factor is an admitted hypothesis with 3 free params); "Finsler evades the no-go" (it obeys it).

*Both ways: the closed-form T(a) + the exact Chang-Li=g_obs identity + the real (if underived) lensing sector are credited at full weight; the Ostrogradski ghost, the velocity-vs-acceleration key mismatch, the by-hand a0, and the hypothesis-only rescaling factor are conceded at full weight. No manufactured action. 9/9 sympy checks PASS. Files: c1–c7 in reviews/routeC_finsler/.*
