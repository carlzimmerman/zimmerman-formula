# dark_fluid_2026 — what the dark fluid is

The author asked, on 2026-09-26, to find out what the dark "fluid" is, and said it is not particles. The record
fixes what the dark component must do:
- Clusters, the CMB and lensing need collisionless **mass**.
- The GDM theorem says linear cosmology sees only a cold a⁻³ fluid.
- L353's reciprocity makes a kernel-invisible component feel Newtonian gravity only.
- Criterion B forbids a fluid made of the clock's own dust, because stream crossing would fold the khronon's leaves
  (XR3 §2.5; CV4).

It also records what failed. The framework's no-particle condensate dust, the ghost-condensate "Q-mode" of one real
scalar, breaks down at the first stream crossing. A linear complex field passes (L374 and its MUTATE).

These lanes work inside V0, the C-H/K branch's one action (`real_research/chk_v0_2026/`). Each has a MUTATE control. The
continuum tests and the inverse specification are the cross-thread review's XR8.

| Lane | Content | Status |
|---|---|---|
| FL1 | the identification: a superfluid order parameter; the condensate dust as its limit | **6/6** (MUTATE rc = 1) |
| FL2 | FK1's kick potential in V0's dark slot: the field-side checks | **8/8** (MUTATE rc = 1) |
| FL3 | the swirl: a rotating halo's vortex lattice against the clock's slices | **4/4** (MUTATE rc = 1) |

The kick itself — clearing the fluid from galaxies while clusters keep it — is FK1, in its own folder
(`real_research/dark_fluid_kick_2026/`, c2e1fa119).

## FL1 — the dark fluid is a superfluid order parameter (6/6; MUTATE without L353's pair fails F2, rc = 1)

`FL1_order_parameter.py` (+ `.out`, `_MUTATE.out`, results JSON; about a second).

- **F1, V0 has no room for it.** V0's scalar block on a gate-on plateau (L340's, CV2 B2) has a determinant quadratic in
  ω: one propagating scalar, the khronon, besides the two tensor modes. Every other field of V0 is a constrained
  auxiliary. **So the dark fluid is new field content.**
- **F2, the order parameter in V0.** Take a complex field ψ, the non-relativistic envelope of a complex scalar, coupled
  exactly as V0's dark slot is (ρ_d = m|ψ|², through the metric potential and L353's pair). It obeys
  iψ_t = −∇²ψ/2m + m u ψ, where u is the Newtonian potential of all matter, baryons and the fluid. That is
  Schrödinger–Poisson, and it is kernel-invisible: the fluid neither feels nor sources the phantom.
- **F3, the record's condensate dust is its phase-only limit.** With ψ = √n e^{iθ} and a repulsive self-interaction, the
  Madelung form is exact. Dropping the quantum pressure and eliminating n (Thomas–Fermi) leaves P(μ) = μ²/2g. That is
  a quadratic P about the condensate: the record's ghost condensate, K(Q) = μ²(Q − 1)², in non-relativistic form.
  - Its "dust" density n = μ/g can run negative in the phase-only theory. That is L374's runaway.
  - The full field has n = |ψ|² ≥ 0 identically.
  - So the no-particle condensate and the wave field are **one field, in two limits**. L374's failure is the phonon
    EFT breaking down at stream crossing; the order parameter it is the EFT of passes.
- **F4, criterion B is safe.** Two crossing streams superpose (ψ = e^{ikx} + e^{−ikx}). A vortex (ψ = x + iy) has
  ∇θ → ∞ at its core. In both cases the field, its energy density and its momentum density Im(ψ*∇ψ) stay single-valued
  and finite: nodes, not singularities. The stress that the metric and the khronon see is smooth, so the khronon's
  leaves never fold. A fluid made of the clock's own dust would need two values of ∇τ at one point.
- **F5, cosmology.** For m ≥ 2×10⁻¹⁹ eV the free order parameter is GDM (0, 0, 0) to within 3×10⁻¹⁶ on the scales
  linear cosmology sees (c_s² = q²/(1 + q²), q = k/2ma; w ~ (H/m)²). The record's w₀ squeeze (CMB w₀ ≤ 2×10⁻¹⁴ against
  galaxy-MOND w₀ ≥ 1.4×10⁻⁸) came from one scalar carrying both MOND and the dust. In V0, MOND is C-H's U-sector, whose
  equations carry no parameter of the fluid. **So the squeeze's lower bound does not exist here.**
- **F6, classical, not particles.** The occupation number per de Broglie cell, N = (ρ/m)(2πħ/mv)³, is 9×10⁷⁶ in
  clusters and 4.5×10⁷⁶ at the cosmic mean for m = 2×10⁻¹⁹ eV. It reaches 1 only at m ≈ 3 eV (clusters: 3.46 eV;
  cosmic mean: 2.91 eV). So for 2–5×10⁻¹⁹ eV ≤ m ≲ 1 eV the dark fluid is a classical coherent field, a superfluid
  order parameter at enormous occupation. **Both halves, plainly:** it is a classical field and not a gas of particles,
  and its quanta, if quantised, would be bosons of mass m, as a classical light wave's quanta are photons.

**Still open after FL1** (status now):
- (a) **Clearing it from galaxies while clusters keep it.** FK1 builds this inside the field, and FL2 checks it against V0.
  - FK1: the field's two real components are split by ε. Heavy pairs convert to light pairs that leave back to back at
    v_k.
  - Retention, Harvey, X-COP and the flagship are not re-scored.
- (b) **The amount.** FL1 called it a conserved U(1) charge. FK1's ε breaks that U(1). The amount is now the
  non-relativistic number n_H + n_L: an adiabatic invariant that the conversion conserves, set by the initial
  misalignment's amplitude. It is still free, as the record's I₀.
- (c) **The shell-crossing test at a finite radial mass.** XR8 is running it.

## FL2 — FK1's kick potential in V0's dark slot (8/8; MUTATE gating the splitting fails V3, V4 and V7, rc = 1)

`FL2_dark_slot_with_the_kick.py` (+ `.out`, `_MUTATE.out`, results JSON; a few seconds). It reads FK1's committed JSON
(the trigger couplings G_t/mc², ε/m², q) and does not run FK1. Lean: `FL2_dark_slot_certificates.lean`, 6 theorems, zero
sorry.

FK1 writes the dark slot as one complex scalar, V = m²|Φ|² + ε Re(Φ²) + λ(K)(Im Φ²)², with λ ∝ K^(−2q) and q = 1.75. Its
hand-off to V0 had two checks: the khronon's equation with the λ′(K) source, and kernel invisibility. The review session
added CV3's rule, the fold condition and a plain statement of the field content.

- **V1, kernel invisibility holds.** Both non-relativistic components go into V0's static action exactly as FL1 F2's
  one did. Each obeys iψ_j,t = −∇²ψ_j/2m_j + m_j(Φ + λ/2)ψ_j + ∂U/∂ψ_j*, and ∇²u = 4πG(ρ_b + m_H n_H + m_L n_L).
  Neither the splitting nor the cross term contains a metric field. So on shell (CV3 `carrier_blind`) the fluid feels
  and sources only u, whatever its composition.
- **V2, the gated energy is non-negative and transient.** The fast-phase average of φ_H²φ_L² reproduces FK1 K5: cross
  coupling λ/m², pair coupling G/n = λ/2m².
  - Its value is g_c(6a² + 2b²) ≥ 0, with a + ib = ψ_Hψ_L*.
  - It vanishes in both pure states, so it lives only while the conversion runs.
- **V3, the K-gate stiffens the khronon.** Add −λ(K)E_int to CV4's quasi-static term, −(c₂S/2)(δK)², with
  SK² = 3ρ_c c².
  - The khronon's equation becomes ∇²[∂L/∂δK] = 0, so x = δK/K solves x(1 + x)^(2q+1) = 2qE_int/(3c₂ρ_c c²).
  - The second variation's coefficient is c₂S/2 + q(2q+1)E_int/K². That is positive because E_int ≥ 0.
  - A convex gate times a non-negative energy adds stiffness. It cannot destabilise the khronon.
- **V4, K stays CMC.** Take FK1's trigger couplings (G_t/mc² = 1.8 × 10⁻⁹ at 2 × 10⁻¹⁹ eV, less for heavier m),
  conversion at the trigger density (1 + δ_t)Ω_d ρ_c0 E⁴, and c₂ ≥ 10⁻⁴.
  - δK/K ≤ 1.0 × 10⁻² for z ≤ 4. The gate's force relative to gravity is ≤ 3 × 10⁻⁴. The leaves stay CMC to that
    accuracy, and the K-gate stays force-free.
  - At z = 10 with c₂ = 10⁻⁴ the shift reaches 0.12. It self-quenches the coupling by (1 + x)^(−2q) ≈ 0.67. That is
    reported, not a failure.
- **V5, CV3's rule holds.** Order the Hessian as (multipliers, constrained, khronon + fluid). Then
  det H = (−1)ⁿ det(M)² det(Z) for any constrained block X and any constrained–khronon block Y.
  - This is checked with the explicit block inverse, det A = −det(M)², a zero Schur correction, and five exact random
    8×8 matrices.
  - V0's instance (Φ, u, Ψ, w, τ) gives a²b²Z; Lean `gate_block_det` certifies it.
  - The gated term depends only on (τ, ψ). Its entries sit in Z, never in a multiplier row.
- **V6, criterion B holds.** Each component is a three-stream superposition, with its generic vortex lattice.
  - At a node the fluid velocity diverges: |v|r → constant, with one quantum of circulation.
  - The density, the stress and E_int stay finite and continuous through the node.
  - The khronon is sourced by that smooth stress and answers E_int algebraically (V3), so its leaves never fold. A dust
    khronon (∇τ = v) would inherit the 1/r singularity.
- **V7, only the conversion may carry a gate.** Suppose each piece were gated by the region gate instead. The gate force
  at a 10¹¹ M☉ edge (z = 0.25, w = 0.25, r_e = 1355 kpc) then gives:
  - the conversion: ≤ 1.5 × 10⁻² v_f²;
  - the splitting: 10 v_f², a wall.

  The splitting's rest energy (ε/2m² = v_k²/4c²) is 692× the conversion's at 2 × 10⁻¹⁹ eV, and 1.5 × 10⁷× at
  10⁻¹⁰ eV. It also changes sign, which Lean `splitting_energy_changes_sign` certifies. So it can carry neither gate,
  and FK1's K-gate on the conversion is the force-free choice.

**Said plainly.** The dark slot is one complex scalar: two real fields, φ_H and φ_L. It is new field content, and the
fluid's mass is still required. Each item is marked:
- m is declared (≥ 2–5 × 10⁻¹⁹ eV, L383);
- ε is fitted to L388's kick window: ε/m² = 1.84–2.35 × 10⁻⁶;
- λ₀ and q are declared, with q = 1.75 matched to the linear gate;
- the initial misalignment is declared: near φ_H, and its amplitude is the amount.

Z₂ × Z₂, kernel invisibility and pair-only conversion at v_k are derived from that potential. Its quanta, if quantised,
would be bosons of masses m_H and m_L. At occupations ~10⁷⁷ per de Broglie cell (FL1 F6) it is a classical field, not a
gas of particles.

**Scope.** The khronon response is CV4's quasi-static, linear equation, dominated by the λ-term. The conversion is taken
to happen at the trigger density. FK1's G_t is its z = 0 background estimate, with O(1) factors; the z-scaling G_t ∝ H^½
follows from FK1 K4.

## FL3 — can the dark fluid swirl without disturbing the clock's slices? (4/4; MUTATE dust clock fails S4, rc = 1)

`FL3_swirl_and_the_clock.py` (+ `.out`, `_MUTATE.out`, results JSON; a few seconds). It reads FL2's and CV4's committed
JSON. Lean: `FL3_swirl_certificates.lean`, 4 theorems, zero sorry.

The review session asked this as one of four readings of the author's idea that halos are like a fluid swirling down
between the bands. The fluid here is the dark fluid (FL1/FK1), not Λ. A superfluid holds angular momentum only in
quantised vortices: one circulation quantum h/m each, at Feynman's density n_v = mΩ/(πħ). At every core the field
vanishes.

- **S1, the gate's khronon source at the cores.**
  - It vanishes smoothly. The gated energy g_c(6a² + 2b²), with a + ib = ψ_Hψ_L*, goes as r² at a ψ_H core. The
    relativistic (Im Φ²)² goes as r⁴ at a common core.
  - On a rotating triangular lattice it is exactly zero at every one of the 37 cores, finite and smooth everywhere
    (|∇E_int| ≤ 8 E_max per lattice spacing), and identically zero before the conversion.
  - The swirl gives the source holes, never spikes.
- **S2, δK/K at the lattice scale.**
  - FL2's response is algebraic, so the lattice only modulates the conversion's own shift between 0 (at the cores) and
    FL2 V4's maximum. That maximum is 1.1 × 10⁻³ (c₂ = 10⁻³), 3.8 × 10⁻⁴ (2.9 × 10⁻³) and 1.5 × 10⁻⁴ (7.3 × 10⁻³),
    all below CV4's 4.8 × 10⁻³.
  - At the KM1 floor, c₂ = 10⁻⁴, it reaches 1.0 × 10⁻² at z = 4. That is a statement about the conversion, not the
    swirl.
  - The swirl's own moving-pattern channel is ≤ 2 × 10⁻¹³, taking CV4 K2's G₁ at C = 0 because the fluid is
    kernel-invisible (G₁ ∝ α_c/c₂). This covers the ordered lattice (l_v = 146–188 pc at 2 × 10⁻¹⁹ eV for spin
    0.03–0.05, 2–27 pc for heavier m) and the random tangle (one vortex per λ_dB²).
- **S3, no vorticity reaches τ at linear order.**
  - On a metric with a shift, the linear K and the lapse do not depend on a transverse (vortical) shift. A longitudinal
    shift enters K as −∇²χ, which is the built-in control.
  - The khronon's normal is twist-free, and V0's khronon terms are only a² and (K − ⟨K⟩)².
  - The second-order leak is ≤ 2 × 10⁻⁹.
- **S4, criterion B holds.**
  - The circulation lives in the order parameter's phase: 7 h/m around 7 cores, one quantum each.
  - The khronon's tilt, solved from the swirling fluid's own E_int, has a zero loop integral (relative 4 × 10⁻⁹).
  - The stress is continuous through every core.
  - So τ is single-valued and the leaves never fold. A clock made of the fluid's dust (the MUTATE) would carry that
    winding: a screw dislocation at every core.

**Answer.** Yes. The dark fluid can swirl without disturbing the clock's slices. Its swirl is the winding of its own
phase, which the twist-free clock does not see at linear order, and the only coupling, the conversion gate, has a hole at
every core. The baryons' swirl (the disk, spiral patterns) is CV4 K2's moving-source dipole, not this lane.
