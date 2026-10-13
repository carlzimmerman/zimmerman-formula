# CFG722: bridge from the unsolved cold-energy kinetic equation to the P-field action. FROZEN CRITERIA

Committed alone, before any CFG722 script exists and before any CFG722 number is computed. Date 2026-10-13.
Lane number: CFG720 (merger window) and CFG721 (two lanes: excess carrier 94c4b06b3, supply overflow 93d53f7345) are taken.
CFG722 had no directory, commit or LEDGER row. Block CFG720–729.

**Settings.** κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. Static law: CFG695's
saturating vacuum, ν_s(y) = ½ + √(¼ + 1/y). "Cold energy" throughout; its mass is still required (CFG624). No ΛCDM or
standard-MOND yardstick enters any verdict. Not "theory closed". No PM, no merger simulation, no download. One process,
≤ 1 GB, nice 10. The Lean chat's lanes (CFG690–699) and astra's files (sol61_push/**) are read only.

**Disclosure before freezing.** While writing these criteria I made back-of-envelope estimates of B3 (the P response time can
reach ~0.1 Gyr at the slow corner of the window) and of the B8 sign. These lines are frozen knowing that.

## The two objects being bridged
- astra (MASTER_COLD_ENERGY_EQUATIONS, Supplement E):
  ∂_t f_c + v·∇_x f_c − ∇Φ_g·∇_v f_c = C_sel[f_c, ρ_b, χ].
  Requirements: derive C_sel (or the target from a collisionless history), its reciprocal energy–momentum exchange, its
  source/phase dependence and its metric coupling. Benchmarks: IC-C (target density, σ = 0.05 V_f) needs energy IMPORT
  0.50–0.64 M V_f²; IC-B (diffuse reservoir) needs EXPORT 0.27–0.39 (static baryons, gravity only).
- Lean chat (CFG694/695): L = −|∇Φ − 4πG P|²/8πG − ρ_bΦ − W(P) − (γ/2)|∇P|² + (I/2)|Ṗ|², W from CFG695.

## Two bridge couplings (the only ones examined; declared now)
- **Coupling G (gravitational only).** A carrier f_c enters as −ρ_cΦ, like baryons. P stays an independent field.
- **Coupling ID (identification).** The carrier IS the polarizable medium: ∂_t P_L = −j_c (carrier mass current), ∇·P = ρ_c − ρ̄_c,
  kinetic term ½ρ_c v² replacing (I/2)|Ṗ|² (CFG698/743). The carrier then feels the tether force derived from W.
A parameter λ multiplies the P–Φ coupling (and therefore the ID tether). λ = 1 is the action; λ = 0 is the decoupling control.

## Tests (script cfg722.py; all numbers from it)
- **B1 (Q1, neutrality).** Hernquist baryons M_b = 10¹¹ M☉, a = 3 kpc; static CFG695 polarization out to r_e = 300 kpc, tapered
  linearly to zero over [r_e, 1.1 r_e]. Integrate ∇·P over r ≤ 1.2 r_e numerically. Structural PASS iff |net| / M_c(<r_e) ≤ 1e-6.
- **B2 (Q1, inertia; sympy).** The P field's Noether momentum density and its dispersion relation. Reported: whether a
  bound-charge lump has ballistic (particle-like) transport, i.e. whether ω = k·v for some v.
- **B3 (Q1, merger response).** Longitudinal gap frequency at fixed baryons, ω₀² = 2c_P² x(2 − x)/(L*²(1 − x)²), x = u/a₀ from
  ν_s, at y ∈ {0.1, 0.3, 1, 3}; L* ∈ {5.75, 100, 1000} pc with c_P at CFG659's double-pulsar floor (1.7e-3, 2.6e-4, 5.6e-5 c),
  and c_P = c. t_resp = 2π/ω₀.
  Rule: if max t_resp < 0.1 Gyr (the start of CFG623's Harvey window) at every allowed corner, the bound charge tracks the
  instantaneous all-baryon field through the merger (DERIVED: CFG623/624's α = ∞ class). Otherwise CONDITIONAL on (L*, c_P),
  with the response time handed to CFG720.
- **B4 (Q2, static limit = control K1).** Coupling ID, cold carrier at rest: solve the equilibrium for u on y ∈ [1e-4, 1e3]
  (200 log points). PASS iff g_N + u = ν_s g_N to ≤ 1e-10 relative everywhere. Coupling G: report the net force on a cold
  carrier at rest (no equilibrium iff ≠ 0).
- **B5 (Q2, sign of the required exchange).** Coupling ID, spherical, point-mass baryons M_b ∈ {10¹⁰, 10¹²} M☉, both footings.
  Static energy U[u] = (1/4πG) ∫ dV [∫₀ᵘ s²/(a₀ − s) ds − g_N u], with u = G M_c(<r)/r² (ρ̄_c neglected inside the halo; disclosed).
  Carrier mass fixed at M_c = M_law(<r_e), r_e = 10 r_M. Family at rest: M_s(<r) = M_eq(<r/s), s ∈ {0.5, 0.8, 1.25, 2, 4},
  integrated to 4.5 r_e. ΔU(s) = U[s] − U[1] in M_c V_f².
  Rule: DERIVED "the law profile is the unique static minimum; the required exchange is EXPORT (≥ 0) for every initial state"
  iff ΔU(s) > 0 for every s, M_b and footing. Then IC-C's required exchange is its own kinetic energy, 1.5 σ² = 0.00375 M V_f²
  (export), not import. If any ΔU(s) < 0: OBSTRUCTED (the identification does not select the law).
- **B6 (Q2, momentum receiver).** Coupling ID with the anchor in the cosmic frame: a halo moving at v_pec = 300 km/s for 1 Gyr is
  displaced d = v_pec t relative to its anchor; uniform P = ρ_c d with ρ_c the law's local cold density at y = 0.1 for
  M_b = 10¹¹ M☉. Rule: if 4πGρ_c d ≥ a₀ (beyond saturation) on both footings, a cosmic-frame anchor is excluded and the anchor
  must be the basin frame (reciprocal with the baryons; CONDITIONAL on B1 of CFG678, the switch as an action term).
- **B7 (Q3, phase dependence without a new constant).** Candidate routes and their fractional effect on the hot-gas source
  relative to the condensed source:
  (a) relativistic pressure, p/ρc² for kT = 1 and 8 keV, μ = 0.6;
  (b) stiffness, (ℓ_γ/h)² with ℓ_γ = L*²/(2 r_M), for disc gas (M_b 6e10 M☉, h 100 pc) and an ICM core (M_b 1e14 M☉,
      r_c 200 kpc), L* ∈ {5.75, 1000} pc;
  (c) granularity: a star's screened self-phantom, 0.0352 of its mass (CFG658 E3), and its sign.
  Rule: a route supplies A5 iff it suppresses the hot source relative to the condensed one by ≥ 0.5 with the right sign.
  None ⇒ OBSTRUCTED. (d) the carrier's own dispersion is reported separately; it is a carrier phase, not a baryon phase.
- **B8 (Q4, capacity).** (i) Hard wall u < a₀ ⇒ M_c(<r) < a₀r²/G; control: Σ̄ ≤ a₀/πG must reproduce CFG695 S4 (214 / 258 M☉ pc⁻²)
  within 1%. (ii) Coupling ID: net outward acceleration on the carrier f(u) = u²/(a₀ − u) − g_N at u = u_eq × {0.5, 0.9, 1.1, 1.5,
  min(2, 0.999 a₀/u_eq)}, y ∈ {0.1, 1, 10}. Rule: DERIVED "the tethered medium expels any excess over the law (no overflow can
  sit in its core) and a warm carrier can sit only at or below the law" iff f > 0 for every excess and f < 0 for every deficit.

## MUTATE (`CFG722_MUTATE=1`, writes `_MUTATE` outputs; exit 1 iff every tooth bites)
- **M1 (λ → 0).** The bound charge's contribution to the acceleration of matter must be exactly 0, and coupling ID must have no
  cold static equilibrium (residual net force = g_N).
- **M2 (saturation at 2a₀).** B4 must fail (deep coefficient ≠ a₀).
- **M3 (sign of the tether).** Flipping the sign of W must make B5's ΔU negative somewhere.

## Verdicts per question
- **Q1 ontology/merger.** DERIVED if B1 passes and B3 is adiabatic everywhere; CONDITIONAL if B3 depends on the window.
  Whether a carrier is forced is read from B1 together with CFG624 (the required cold mass); stated plainly.
- **Q2 selector.** DERIVED only if a C_sel follows from the action that is an attractor from both benchmark classes with the
  right exchange signs and no added receiver. CONDITIONAL if B4 and B5 pass (equilibrium selection) but the dynamics needs an
  export channel or anchor the action does not supply (assumptions named). OBSTRUCTED if B4 or B5 fails.
- **Q3 phase.** By B7's rule.
- **Q4 capacity.** DERIVED if B8 passes, with its implication for CFG721's supply-overflow hypothesis stated.
