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
| FL2 | clearing it from galaxies while clusters keep it | next |

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

**Still open:**
- (a) **Clearing it from galaxies while clusters keep it.** This is what the kick does now. XR7 puts the retention
  transition at v_c ≈ 700–850 km/s for v_k = 575–650 km/s. A within-one-field mechanism has to leave free-streaming
  products, not a pressure-supported normal fluid (X-COP, Harvey, the Bullet).
- (b) **The amount.** It is the field's conserved U(1) charge, set by initial conditions, and free, as the record's I₀.
- (c) **The shell-crossing test at a finite radial mass.** XR8 is running it.
