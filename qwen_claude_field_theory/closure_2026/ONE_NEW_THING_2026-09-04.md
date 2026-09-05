# One new thing (2026-09-04, late): the coherence length is a healing length, and the operator that realises the screened door is in hand

## The gap it fills
f31c found that the aether-scalar PPN lock (α₁ = −2(K_B + 2), untunable) is evaded only by a *coherent* stiffening of the scalar's whole quadratic form, J_Y → J_Y(1 + ξ²k²), mixings with the aether included; the two local fourth-order operators tried, (D²φ)² and |D_μD_νφ|², act on the χχ entry alone and make α₁ grow. The handoff to G03 said: "the operator that realises (A) from an action is not in hand."

## The operator
Inside the scalar function J, replace Y by

  Y → Y + ξ² q^{λσ} q^{μν} ∇_λV_μ ∇_σV_ν,   V_μ ≡ q_μ^ν ∂_νφ,   q_μν = g_μν + A_μA_ν,

i.e. add ξ² times the aether-projected gradient-squared of V, the aether-frame *spatial* gradient of the scalar (Y = V·V exactly, since q is a projector).

Why it does what the door needs: V's background vanishes (∂φ̄ = −Q₀A, and q kills A), so at quadratic order every Christoffel and background piece drops and (∇_⊥V)² = [k² + (A·k)²] V₁·V₁, while V₁·V₁ is the whole Y sector. The (1 + ξ²k²) factor therefore multiplies the scalar–scalar, scalar–aether and scalar–metric entries together, which is exactly (A).

## Verified (`hunt_2026/f32_ppn_k4_spatial_gradient_operator.py`, the repository's own boosted-aether PPN pipeline; checks can fail)
- α₁ of the operator equals α₁ of the coherent stiffening (A) **exactly**, at all 12 ladder points (K_B = 1/5, 1/2; J_Y = 1, 2; (ξk)² = 0, 1, 10², 10⁴): the propagator form −4(2 − K_B)/(J_Y(1 + ξ²k²) + 1) now comes from a Lagrangian term.
- α₂ (needs c₂ ≠ 0; the f31 ladder's c₂ = c₄ = 0 makes pure-aether α₂ singular): at c₂ = c₄ = 1/10, K_B = 1/5, the scalar's contribution to α₂ is 16.5 at ξ = 0 and 5.9×10⁻⁴ at (ξk)² = 10⁴, suppression 3.6×10⁻⁵ (variant (A): 4.2×10⁻⁵), scaling about (ξk)^(−2.2).
- At the Cassini floor, ξ ≥ 0.045 pc gives (ξk)² ≥ 8.6×10⁷ at 1 AU: the scalar's α₁ drag is about −8×10⁻⁸ and its α₂ drag about 3×10⁻⁸, under the bounds 10⁻⁴ and 4×10⁻⁷. The aether's own α₁, α₂ are Einstein-aether's (c₁₃ = 0 region, c₁₄ small and positive) and are not the scalar's problem.
- Documented residual: the pipeline's Y₂ differs from V₁·V₁ by Q₀² × (aether-normalisation pieces: Ψ = a₀, a₁, B_i − a_i) because the aether's unit-norm constraint is solved only at first order there; no χ, Φ or s₂₂ term; it does not enter α₁ and moves the α₂ drag by 15%.

## Health and meaning
The operator is purely spatial in the aether frame: no extra time derivatives, hence no Ostrogradsky mode and no new degree of freedom beyond the host's. The scalar's dispersion becomes ω² = c_s²k²(1 + ξ²k²), the Bogoliubov form of a superfluid: ξ is the healing length of the condensate the framework already carries (φ = Q₀t). ħ/(ξc) = 2×10⁻²² eV at ξ = 0.03 pc, the fuzzy-dark-matter mass scale; recorded as a coincidence, nothing more. The group velocity exceeds c in the aether frame for k > 1/ξ (Hořava-type, not instantaneous); the spec's causality gate (G03's screen, then G11) has to judge that.

## What it is not
- Not a derivation of ξ: a new scale in the action; ξ stays a constraint (0.02–0.05 pc from the Solar System, 15–20 kAU knee for wide binaries, 50–140 pc wanted by three outer-halo globulars, Pal 3 discordant).
- Not T-B literally: the static nonlinear limit is a fourth-order elliptic law, ∇·[J_Y(V − ξ²∇_⊥²V)]-type, not the double filter; its Solar-System gates (quadrupole, phantom monopole inside Saturn, sunward force) must be run as G02 ran T-B's.
- Not in the 2-DOF line: the host is an aether-scalar theory, which the spec's requirement 2 (N_grav = 2) excludes as it excludes AeST. This is the door of the AeST-host line; whether requirement 2 or this line gives way is the lead's call, not a calculation.
- Both footings do not enter (pure PPN algebra).

## First calculations for G03 (in order)
1. Write the term into the action with its boundary terms; confirm no new mode in the aether frame (Hamiltonian count unchanged from the host).
2. The static nonlinear limit and its three Solar-System gates, both footings, as in G02: does it need the same ξ ≥ 0.02–0.03 pc?
3. The causal screen on ω² = k²(1 + ξ²k²) against the spec.
4. Resolve the second-order aether normalisation in the PPN pipeline so the identity V·V = Y is exact there (removes f32's documented residual).
5. Binary pulsars: the scalar's dipole radiation at k ≫ 1/ξ with the modified dispersion, against the PSR J1738+0333 and J0348+0432 bounds.
