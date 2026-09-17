# N07 — THE ACTION DOOR (registered 2026-09-17, after N00)

The campaigns N1–N6 treated the framework's fluid content as a static law
(N1 rheology, N2 drag-class, N3 completion, N5 window, N6 fingerprint). The
record's OWN action (THE_THEORY.md L5; G031 the GR fluid action) writes the
phantom as a MATTER SECTOR:

    S = ∫√(−g)[(c⁴/16πG)(R − 2Λ_geom) − Λ⁴f(K)] + S_fluid[J, φ, β, α] + S_baryons
    f(K) = K − 1/(1+K),  K = −½(∂φ)²/Λ⁴,  f(0) = −1            (L5)
    S_fluid = ∫√(−g)[−ε(n) + J^μ(∂_μφ + β∂_μα)],  n = √(−J^μJ_μ)  (G031)
    T^μν = (ε + p)u^μu^ν + p g^μν,  cold sector: barotropic dust ε = mn, p = 0

So the phantom is a **pressureless dust** carrying the conserved shift charge
(J^μ_{;μ} = 0 variationally — φ, β, α are Lagrange multipliers), whose
equilibrium is the isothermal sphere at the Zimmerman temperature:

    σ² = √(G M_b a₀)/2  ⇒  ρ_ph = √(G M_b a₀)/(4πG r²)  ⇒  g² = a₀ g_N  (the RAR as EOS)

## THE MISSED DOOR (this door, pre-registered)

The action-correct question for Navier–Stokes is NOT "what drag does the
phantom apply?" but **"what is the two-fluid system the action writes, and
where does its singular sector live?"** Three derived claims to execute (not
assume):

- **D1 (the cusp):** the equilibrium phantom ρ_ph ∝ 1/r² IS a stationary
  density singularity at every baryon centre — the framework's static dark
  sector already carries the axis cusp. (G031's isothermal chain re-verified
  here as the launch rung.)
- **D2 (the caustic channel):** the phantom is pressureless: its dynamics
  form caustics (density singularities) in finite time on the Jeans/free-fall
  scale τ_ff = 1/√(Gρ_ph) — the singular sector of the framework is the DARK
  dust, not the baryon fluid.
- **D3 (the transfer, the door's kill or its opening):** can the collapsing
  phantom drag the BARYON velocity to blowup through the action's coupling
  (the shared Newtonian potential, baryons feel −∇ψ)? Kill conditions:
  - K-1 (the transfer dies by measurement): IF the phantom's reaction follows
    the measured law (the response function that the RAR IS), its force on
    baryons is |g_ph| ≤ a₀/2 EXACTLY (Lean: `a0cap_bound`) — a bounded
    perturbation (N2's class): the caustic is CONFINED to the dark sector and
    the baryon Clay problem sits untouched on the Newtonian face.
  - K-2 (the transfer lives): IF the action's dynamical coupling can exceed
    the measured cap away from equilibrium (the G03 door: the action is NOT
    committed), the two-fluid system's baryon blowup is a DERIVED, novel
    prediction — and the constructive route is the OpenAI toolkit (N08).
- **D4 (the window consistency):** the phantom's Jeans time at 1 kpc:
  τ_ff = 1/√(Gρ_ph) ≲ 10⁸ yr — the deep sector responds on timescales far
  below galactic dynamics, consistent with its quasi-static equilibrium
  reading AND fast enough to mediate the a0-line in flows.

## The OpenAI record (N08 lane, status register)

2026-09-08: OpenAI announced + Lean-formalized (Lean 4.34.0-rc2, the SAME
toolchain as this repo) **finite-time blowup for forced 3D NSE at every
ν > 0**: smooth compactly-supported forcing, zero initial velocity, ‖u‖∞ → ∞
with energy bounded — the Clay answer (C)/(D), if the proof survives referee
scrutiny. Construction: self-similar slender vortex core (ℓ_r ≍ τ^½,
ℓ_z ≍ τ^{½−h}, |u| ≍ τ^{−½−h}) + oscillatory pulse families realizing the
annular stress (the Daneri–Székelyhidi oscillation toolkit + viscous shearing
waves); the N5-corollary consistency: the construction's material acceleration
→ ∞ ≫ 3.5·a₀ before the singular time — the blowup lives ABOVE the floor, on
the Newtonian face, exactly where the framework's law is silent. If the action
door's D3 dies (K-1), the framework's verdict converges: the visible-fluid
Clay problem is a Newtonian-face question; the framework's OWN singular sector
is the phantom dust, whose cusp the RAR already measures.

## Kill conditions (summary)

| Door | Opens if | Kills if |
|---|---|---|
| N7/D1 cusp derived | the static phantom is 1/r² (G031 chain holds) | — |
| N7/D2 caustic channel | pressureless dust singularities on τ_ff (cited class + numerics) | — |
| N7/D3 transfer | the action's coupling can exceed a₀/2 off-equilibrium (K-2) | the measured cap a₀/2 bounds it (K-1) — verification below |
| N7/D4 Jeans time | τ_ff at 1 kpc in [10⁶, 10⁹] yr | outside by >10× |

Lanes: N07_action_door.py (D1–D4, sympy-exact + 1D two-fluid numerics) ·
N08_openai.md (the OpenAI digest + consistency) · N09_phantom_cusp.py
(equilibrium cusp + Jeans numbers, the deep-sector clock).