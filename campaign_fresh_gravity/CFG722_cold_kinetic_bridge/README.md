# CFG722: the cold-energy kinetic equation bridged to the P-field action

**Label.**
- **Q1 ontology:** DERIVED that the bound charge is a field quantity with zero net mass. **Merger: CONDITIONAL.** A collisionless
  carrier is FORCED, and it is a new particle species with a free mass.
- **Q2 selector:** CONDITIONAL. Under the identification coupling the action gives an explicit C_sel. It selects the law's profile
  as the unique static minimum, but it is conservative, so it is not an attractor.
- **Q3 phase dependence:** OBSTRUCTED.
- **Q4 capacity:** CONDITIONAL, on a disclosed criteria correction. The capacity wall is DERIVED, and a tethered core cannot hold
  overflow.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (cb2aac21f), 2026-10-13, before any CFG722 script or number.
- **Script:** `nice -n 10 python3 cfg722.py`, ~10 s, 0.27 GB, exit 0 → `cfg722.out`, `cfg722_results.json`.
  `CFG722_MUTATE=1` writes `_MUTATE` outputs and exits **0**: M1 and M2 bite, M3 does not (see Disclosures).
- **Settings:** κ = ½ FITTED; footings never pooled; static law ν_s (CFG695); the cold energy's mass is required (CFG624); not
  "theory closed". No PM, no merger simulation, no download. CFG690–699 and sol61_push/** were read only.
- **Inputs bridged:**
  - astra, MASTER_COLD_ENERGY_EQUATIONS Supplement E: ∂_t f_c + v·∇f_c − ∇Φ_g·∇_v f_c = C_sel[f_c, ρ_b, χ], with the
    collective_energy_lower / collective_energy_gate benchmarks.
  - Lean chat, CFG694/695: L = −|∇Φ − 4πG P|²/8πG − ρ_bΦ − W(P) − (γ/2)|∇P|² + (I/2)|Ṗ|².
  - This chat: CFG658, CFG659, CFG699/743.

## Two couplings (declared in the criteria)
- **G (gravity only).** The carrier enters as −ρ_cΦ and P stays an independent field.
- **ID (identification).** The carrier *is* the polarizable medium: ∂_t P_L = −j_c, ∇·P = ρ_c − ρ̄_c, and the carrier's kinetic
  energy ½ρ_c v² replaces (I/2)|Ṗ|² (CFG698/743).

## Results (canonical / alt where they differ)

| test | result |
|---|---|
| B1 neutrality (Hernquist 10¹¹ M☉, r_e 300 kpc) | inside +23.9 / +26.3 M_b, edge shell −the same; **net 2.7e-12 / 2.9e-12 of M_c**. PASS |
| B2 inertia (sympy) | ω² = (K + γk²)/I; momentum density −I Ṗ ∂P, which is not ρ_c v. A gapped field has **no translating lump at any v**: no ballistic transport |
| B3 response time 2π/ω₀ | L* 5.75 pc (c_P at the double-pulsar floor): ≤ 5e-5 Gyr; 100 pc: ≤ 6e-3 Gyr; **1000 pc: 0.06–0.28 Gyr** (y 3 → 0.1); c_P = c: ≤ 2e-5 Gyr. Max 0.276 > 0.1 Gyr → **CONDITIONAL** |
| B4 static limit (control K1) | ID, cold carrier at rest: λW′_rem(u) = g_N reproduces ν_s to **3e-16** on y ∈ [1e-4, 1e3]. PASS. G: no static cold equilibrium |
| B5 required exchange | ΔU/(M_c V_f²) at s = 1.25 / 2 / 4: **+0.031 / +0.118 / +0.208** (identical for both masses and footings: scale invariance); s < 1 hits the wall u ≥ a₀ (+∞). The integrand's curvature is σu(2a₀ − u)/(a₀ − u)² > 0. **The law is the unique static minimum, and the required exchange is EXPORT for every initial state** |
| B6 anchor | a halo moved 307 kpc (300 km/s × 1 Gyr) from a cosmic-frame anchor: u_shift = **2.48 / 2.73 a₀**, beyond saturation → cosmic anchor EXCLUDED |
| B7 phase routes | pressure 5e-6 to 4e-5 (and it adds to the hot source); stiffness ≤ 0.28, and it suppresses *thin cold* components, so the sign is wrong; granularity 0.035, sign wrong → **OBSTRUCTED** |
| B8 capacity | (i) Σ̄_c ≤ a₀/πG = **213.8 / 258.3** M☉ pc⁻² (= CFG695 S4). PASS. (ii) As frozen: **FAIL**, from 2 cells beyond the wall (u/a₀ 1.008, 1.374). Every admissible cell passes: excess over the law → net outward, deficit → net inward |
| MUTATE | M1 (λ = 0): P pulls on matter with exactly 0 and the ID residual force is g_N. Bites. M2 (saturation 2a₀): deep coefficient 1.99, dev 0.41. Bites. M3 (tether sign): **does not bite** on the frozen s-family |

## Answers

### Q1. Field or carrier? What does the bound charge do in a merger?
- **It is a field quantity. It adds no mass and has no inertia of its own (DERIVED).**
  - The bound charge ∇·P only moves mass from the edge of the polarized region to its interior. Seen from outside the basin, the
    system weighs M_b (B1).
  - Its dynamics belongs to P (inertia I, gap K), not to ρ_c. A gapped field cannot carry a lump ballistically (B2).
- **So the bound charge cannot be the cold energy that CFG624 requires.** CFG624 needs real added mass: X-COP is missing
  3.1 / 2.8 M_b, plus Local Group timing, the cosmic web and the mean density (CFG697: ⟨∇·P⟩ = 0).
- **A collisionless carrier f_c is therefore forced** by the action together with CFG624's data. Stated plainly: in kinetic terms
  this is **a new particle species** (a dark-sector carrier). Its particle mass is free: the Vlasov equation does not fix it,
  provided the species is cold and collisionless.
  - Under coupling G it also has no selector (Q2).
  - Under coupling ID its coupling is fixed by W (no new constant), but the identification and its anchor are new structure.
- **Merger (CONDITIONAL).** The pure field follows the instantaneous field of *all* baryons on the gap time (B3). In the Bullet
  those baryons are mostly the stripped gas, so the field sits in CFG623/624's excluded α = ∞ class (lensing on the gas, Z +7.9).
  - The only exception is the slow corner (L* ≈ 1 kpc, c_P at the double-pulsar floor), where t_resp reaches 0.06–0.28 Gyr. That
    response time is handed to CFG720.
  - Even there the field lags or rings (B2). **It never follows the galaxies**, which is what CFG623/641 want.
  - Under ID the carrier itself moves with its galaxies (it is collisionless). The tether then pulls it back onto the law of the
    instantaneous all-baryon field, on CFG743's oscillation period (0.05–2.4 Gyr for M_b ≤ 10¹²; longer for clusters by
    T ∝ M_b^{1/4}, scaling only, not computed here). That is a finite-α merger whose α is set by the action rather than chosen.

### Q2. The selector
- **Coupling G:** C_sel ≡ 0 exactly. The carrier is ordinary collisionless matter in the total potential. P responds to the carrier's
  mass too, so the phantom would be sourced by M_b + M_c (two-sector double counting).
  - In the adiabatic limit (CFG659), f(J) is conserved and P's energy is a functional of the instantaneous density. astra's closed
    bounds therefore carry over (her proof needs only a static potential and conserved energy): IC-C still needs IMPORT 0.50–0.64 and IC-B EXPORT 0.27–0.39 M V_f². **No selector.**
- **Coupling ID: the derived C_sel.** Vary a carrier path in the action with P[f_c] defined by ∂_t P_L = −∫ m v f_c d³v and
  ∇·P = ρ_c − ρ̄_c. The result is

  ∂_t f_c + v·∇_x f_c − ∇Φ_g·∇_v f_c = C_sel ≡ −∇_v·(**a_T** f_c),  **a_T** = W′₆₉₅(u) P̂,  W′₆₉₅(u) = u/(1 − u/a₀),  u = 4πG|P[f_c]|.

  Here Φ_g is the total potential (baryons + carrier). In the square form, the critical quadratic cancels the carrier's
  self-gravity. The carrier then sees ∇Φ_N[ρ_b] plus the residual tether W′_rem(u) = u²/(a₀ − u).
  - **What it is:** a velocity-independent mean-field (Vlasov) force, **not a collision operator**. It conserves N, phase-space
    volume and every Casimir. It has no H-theorem, and f(J) is invariant under slow change.
  - **Selection by equilibrium (DERIVED under ID):** a cold carrier at rest has its unique static minimum exactly on the law's
    profile (B4 to 3e-16; B5 by convexity). The tether, not velocity dispersion, holds the cold energy up.
  - **Exchange signs:** the required exchange is always **EXPORT ≥ 0**.
    - IC-C: astra's IMPORT 0.50–0.64 disappears, because the tether supplies the missing support. What remains is IC-C's own
      kinetic energy, 1.5σ² = 0.00375 M V_f², to be exported.
    - IC-B-like diffuse states: export 0.03–0.21 M_c V_f² at s = 1.25–4. That is the same order as astra's 0.27–0.39 (different
      benchmark).
  - **Reciprocity:**
    - Energy: carrier kinetic ↔ vacuum polarization energy ∫W, exactly conserved by the action.
    - Momentum: reciprocal only if the tether is anchored to the basin's free-fall frame, so that it exchanges with that basin's
      baryons. A cosmic-frame anchor is excluded (B6: a moving halo would be driven past saturation).
  - **Why CONDITIONAL, not DERIVED.** Assumptions: (a) the identification (the carrier is the medium); (b) a basin-frame anchor,
    i.e. CFG678's B1 switch as an action term (not built); (c) an export channel. The action supplies none of (c):
    - P radiation is trapped at ≤ 1e-195 (CFG659);
    - phase mixing keeps the energy as dispersion, and a warm carrier sits *below* the law (B8).
  - So it selects the profile but does not drive arbitrary states onto it. Metric coupling is Newtonian only (one Poisson
    equation); Φ = Ψ is open.

### Q3. Hot vs condensed without a new constant
**OBSTRUCTED.** The tether reads g_N of all baryons, because the coupling is gravitational and universal. Every candidate route is
too small or has the wrong sign:
- relativistic pressure: ≤ 4e-5, and it *adds* to the hot source;
- stiffness: it screens components thinner than ℓ_γ, so it suppresses cold discs (up to 0.28 at L* = 1000 pc) and leaves extended
  hot gas alone;
- granularity: star self-phantoms are screened to 3.5%, again suppressing the condensed source.

The only phase the bridge has is the *carrier's* dispersion, which is a matter of formation history. Its sign (warm ⇒ less settled
mass) is opposite to the cluster-core excess. CFG658's A5 tension stands.

### Q4. Capacity and overflow
- **The capacity is finite (DERIVED).** The hard wall u < a₀ gives M_c(<r) < a₀r²/G and Σ̄_c ≤ 214 / 258 M☉ pc⁻².
- **Inside a tethered basin the capacity is exactly the law's amount.** Excess over the law feels a net outward force; deficits
  feel a net inward force (B8 on every admissible cell).
- **Implication for CFG721's supply-overflow hypothesis.** Under ID, overflow **cannot sit in the core**. The tether pushes it out to
  the basin edge, which is the opposite of H-OF.
  - Core overflow needs a second, untethered population of the carrier: a phase label on the carrier, which is new structure.
  - A static warm carrier sits at or below the law. An excess above the law can only be transient (infall overshoot, the sign
    CFG743 named), and it is pushed back out on the oscillation period.

## Disclosures
1. **B8(ii) criteria error.** The frozen factor list put two y = 10 cells beyond the wall (u/a₀ 1.008, 1.374). The tether energy
   there is infinite and the formula's sign flips, so the frozen line FAILS on inadmissible states. The frozen text is unchanged.
   Q4 is CONDITIONAL on reading the rule over admissible states only, and every admissible cell passes.
2. **M3 does not bite.** With the tether sign flipped, stretched states (s > 1) still cost energy, because −g_N u dominates. The
   compressed states (s < 1) are beyond the wall in either sign. The flip *is* caught elsewhere: B4 finds no equilibrium root, and
   the integrand becomes pointwise concave. That catch is post-hoc and carries no verdict weight. MUTATE therefore exits 0, not 1.
3. **B5's s < 1 cells are +∞ trivially.** A point mass's strong-field core puts any compression past the wall. They carry no
   information beyond the wall itself.
4. **Approximations.**
   - ρ̄_c is neglected inside halos in B5 (the local density is 10³–10⁶ × the mean, CFG743).
   - B3 uses the k → 0 gap at fixed baryons.
   - The ID merger timescale for clusters is a scaling from CFG743, not computed.
5. **A back-of-envelope estimate of B3 and of B8's sign was made before freezing** (stated in the criteria).
