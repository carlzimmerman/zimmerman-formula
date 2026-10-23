# DRAFT: PAPER57 v1.1 correction text (not applied; for the owner and orchestrator)

**Scope.** This file lives only in this lane. PAPER57 (DOI 10.5281/zenodo.23532885) and its .tex are not edited.

**Sources.**
- WT-02 (9b3d77382, criteria b85749d1c).
- CFG961: criteria 83b04219e and A1 f3cbd85e5. The result commit is in the LEDGER row.
- The sol61 cold-covariant audit (`sol61_push/cold_covariant_audit_2026_10_20/RESULT.md`, in the repo at a67f9ed9c). It derived the
  FRW tensor coefficient first.

**Placement.** Insert the block below after the abstract, before §1. Each replacement is listed with its v1.0 line.

---

## Block to insert (LaTeX-ready prose)

**Correction (v1.1), 2026-10-2x.** Two statements about the CFG938 covariant parent in v1.0 are wrong as stated. Both concern the
action exactly as printed in §2.

*(1) "Linear well-posedness" holds only on static backgrounds.*
- **Where CFG938 checked.** Static media in flat space, where the constraint fields χ and λ have no time derivatives. That result
  stands, including the dispersion relation and the inertia condition quoted in §2.
- **The operator.** CFG938's constraint uses D²χ = h^{μν}∇_μ∇_νχ = ³Δχ − θ u·∂χ, where θ is the medium's expansion. This is the
  term through which the background χ̄(t) absorbs the mean density: −3Hχ̄̇ = Kρ̄_c c².
- **On FRW.**
  - The same term makes λ the canonical momentum of χ.
  - χ obeys a forward and λ a backward heat-type equation: 3Hχ̇ = c²∇²χ/a² − c²Kδρ_c, and 3Hλ̇ = −c²∇²λ/a² + (sources).
  - The linear Cauchy problem then has modes growing at Re σ = c²k²/(3|H|), so it is Hadamard ill-posed.
  - For a contracting medium the growing mode is χ's. In general the rate is of order c²k²/|θ| wherever the medium expands or
    contracts, and it diverges as θ → 0.
- **The growing mode is physical, not a multiplier artefact.**
  - The gradient of λ is the force on the medium (−ρ_c K∇λ).
  - In the growing mode the medium accelerates at the full growth rate and the Bardeen potential responds.
  - In the full Einstein system the λ equation follows, through the contracted Bianchi identity (χ̄̇ ≠ 0), from the Hamiltonian
    constraint and the trace-ij equation.
- **Final data does not rescue it.** Posing λ with final data instead gives a non-causal two-point problem: the medium anticipates
  its future by 3|H|/(c²k²), which is 0.22 yr at 10 kpc and 2.2 × 10³ yr at 1 Mpc. That is a different theory, not linear
  well-posedness.
- **Repair.** Replacing D² by the intrinsic slice Laplacian removes the parabolic terms, but the mean density must then be
  subtracted explicitly. That repaired parent is not the action of v1.0, and it is under separate test.

*(2) "c_T = c (structural)" (gate A5) is wrong.*
- **The general result.** The tidal stiffness −(3γ/4K²)τ_μντ^μν is built from the four-dimensional Hessian of χ, so it contains
  Christoffel symbols. For a tensor wave in a medium where χ has a spatial gradient u and a rate ∂₀χ,
  δ(c_T²/c²) = (3/2)L*²[u_⊥² + (u_∥ + ∂₀χ)²]/c⁴ (superluminal).
- **Inside a static medium at the W wall (u = a₀).** c_T/c − 1 = 4.5 × 10⁻¹⁹ to 7.7 × 10⁻¹⁶ (canonical footing) and 6.5 × 10⁻¹⁹ to
  1.1 × 10⁻¹⁵ (alternative), for L* = 24 pc to 1 kpc.
- **On FRW.** The background clock ∂₀χ̄ = cΩ_cH/2 = 8.7 × 10⁻¹¹ m s⁻² (independent of the footing) gives the tensor kinetic
  coefficient Q_T = 1 − 3γχ̇²/K.
- **GW170817.** Averaged along its path, c_T/c − 1 = 3.9 × 10⁻¹⁹ to 6.8 × 10⁻¹⁶. That is inside the bound
  (−3 × 10⁻¹⁵, 7 × 10⁻¹⁶) but caps L* ≲ 1.0 kpc, at the top of the L* window.
- **Early universe.** If the medium is present early, Q_T < 0 before 1 + z ≈ 2.7 × 10⁵ (L* = 1 kpc) to 1.1 × 10⁷ (24 pc).

*Consequences for v1.0's text.*
- The parent remains a covariant completion of the static law (2.2 × 10⁻¹⁶ on NGC 3198), with the dust background, the derived
  field-aligned stress and the slip bound unchanged.
- It is not a well-posed covariant theory on cosmological backgrounds.
- On CFG678's contract, the support v1.0 gave for A2 (hyperbolicity) and B3 (cold sector, "linear well-posed") is withdrawn for
  non-static backgrounds.
- A5 is a computed bound, not a structural pass: CONDITIONAL on L* ≲ 1.0 kpc and on no medium at early times.
- Nothing else in the note depends on these two statements. Its no-go results (D-T, G, L-G/T-O2, S) are derived from the static
  equation.

---

## Line replacements

**Line 24 (abstract, item 1).**
- v1.0: "…and has an isotropic dust background, a derived field-aligned stress, linear well-posedness and slip $\le1.54\times10^{-5}$,
  under five conditions (CONDITIONAL)."
- v1.1: "…and has an isotropic dust background, a derived field-aligned stress, linear stability on static backgrounds and slip
  $\le1.54\times10^{-5}$, under five conditions (CONDITIONAL). On expanding or contracting backgrounds its constraint pair is
  Hadamard ill-posed, and its tensor speed is not exactly $c$ (Correction v1.1)."

**§2 "Results" (line 51), after the dispersion sentence**, add: "This is the static WKB result. On FRW the χ/λ pair is a
forward/backward heat pair and the linear Cauchy problem is ill-posed (Correction v1.1)."

**§2 "Scorecard" (line 54).** Replace "PASS A5, C2; CONDITIONAL A1, A2, B3, C1;" with "PASS C2; CONDITIONAL A1, C1, A5 (computed
bound, L* ≲ 1.0 kpc; v1.0 read PASS); A2 and B3: linear support withdrawn off static backgrounds (Correction v1.1);". Make the
same change in the CFG950 scorecard sentence (line 165), which quotes CFG938's.

**Line 206 ("Established, conditionally").**
- v1.0: "The record's static field equation has a covariant parent with an isotropic dust background, a derived field-aligned stress,
  linear well-posedness and negligible slip, under five stated conditions."
- v1.1: "The record's static field equation has a covariant parent with an isotropic dust background, a derived field-aligned
  stress, linear stability on static backgrounds and negligible slip, under five stated conditions. That parent is ill-posed on
  expanding backgrounds and its gravitational waves are not exactly at c (Correction v1.1)."

**Disclosures (line 213)**, append: "v1.1 corrects two statements about CFG938 (well-posedness off static backgrounds; A5 c_T = c),
following WT-02 and an independent check (CFG961), with the FRW tensor coefficient first derived by the sol61 audit."

**Header (line 18).** "v1.0" becomes "v1.1 (correction of 2026-10-2x; see the box after the abstract)".
