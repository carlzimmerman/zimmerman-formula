# The single-metric action (L169) — written, reduced, and certified where Lean can reach

**Status in one line:** the action below passes the static galaxy, Solar-System (γ, β) and health reductions, its
smoothing sector carries no propagating degree of freedom, and it is **certified to fail the CMB–galaxy dark-fraction pincer**
because its only dark component is uniform in host mass. It is therefore NOT a complete theory. This is the derivation
target that all lanes pointed to, written out so that its failure is exact rather than presumed.

## The action

S = ∫ d⁴x √−g [ R/(16πG) + L_clock + L_φ + L_mix + L_smooth ] + S_m[g, ψ]        (matter and gravitons on ONE metric g)

- **Clock (cuscuton, 0 DOF):** L_clock = μ_c² √(−∇_μτ∇^μτ) − V(τ). Leaf normal n_μ = −∇_μτ/√(−(∇τ)²), induced metric
  h_μν = g_μν + n_μn_ν, leaf derivative D_μ = h_μ^ν∇_ν, normal acceleration A_μ = n^ν∇_νn_μ (static limit: A_i = ∂_iΦ).
- **MOND scalar:** L_φ = −(a₀²/8πG) 𝒥(Y/a₀²), Y = g^{μν}∇_μφ∇_νφ, with 𝒥'(y) ≡ μ(y): μ → √y (deep MOND), μ → μ_∞ (y → ∞).
- **Kinetic mixing (linear entry of MOND):** L_mix = (c/4πG) χ^μ ∇_μφ.
- **Coherence-length smoothing (elliptic constraint, 0 DOF):** L_smooth = λ^μ ( χ_μ − ξ² D²χ_μ − A_μ ), with χ_μ, λ_μ
  leaf-tangent. No time derivatives enter, so the sector is fully second-class (Lean: `smoothing_sector_zero_dof`).

## Static weak-field reduction (L169 script, sympy Euler–Lagrange; all four equations verified)

δλ: (1 − ξ²∇²)χ = ∇Φ  δχ: λ = −(c/4πG)(1 − ξ²∇²)⁻¹∇φ  δφ: ∇·(μ∇φ) = c ∇·χ  δΦ: ∇²Φ = 4πGρ + c ∇·(1 − ξ²∇²)⁻¹∇φ

So matter feels **Φ = Φ_N + c (1 − ξ²∇²)⁻¹ φ** and φ is sourced by the **smoothed** Newtonian field: the T-B double filter
of the f-lanes/G02, now derived from an action instead of imposed. Fourier space (Newtonian regime μ = μ_∞, u = ξ²k²):
Φ̂ = Φ̂_N / (1 − c²/(μ_∞(1+u)²)). Deep MOND (r ≫ ξ): AQUAL for φ with source cρ, g → √(ã₀ g_N), **ã₀ = c³ a₀**.

## What is certified (Lean, Mondlean.lean 93 theorems, zero sorry)

- `double_filter_kernel`: 1/(k²(1+u)²) = 1/k² − ξ²/(1+u) − ξ²/(1+u)², whose inverse transform gives the point-source
  transmission **T(x) = 1 − e^{−x}(1 + x + x²/2)**, x = r/ξ (script checks the closed form against numerics).
- `double_filter_uv_suppression`: the scalar channel is suppressed by (ξk)⁻⁴ at k ≫ 1/ξ — the k⁴ "coherent stiffening" G02 needed.
- `double_filter_transmission_cubic`: 0 ≤ T(x) ≤ x³ on [0, 1] (from the mathlib Taylor bound on exp).
- `screened_gamma_cassini`: |γ − 1| = 2 f_eff with f_eff ≤ T(r/ξ) ⇒ at r/ξ ≤ 1/100, |γ − 1| ≤ 2×10⁻⁶ < 2.3×10⁻⁵ (Cassini).
  Cassini floor from the f-lanes (sunward force, ephemerides) remains ξ ≥ 0.03 pc; γ alone would allow 0.002 pc.
- `single_metric_uniform_dark_fraction_fails`: the action's dark fraction is host-independent (cuscuton dust does not
  cluster, φ's background is stiff, no other sector) ⇒ by `dark_fraction_forces_mass_dependence` it cannot satisfy
  f ≤ 0.105 in galaxies and f ≥ 0.988 at recombination. **This is the certified failure.**

## What is derived but not Lean-certifiable, with numbers (script)

- Newtonian-regime G in galaxies is G/(1 − c²/μ_∞); SPARC Υ_* tolerance (≤ 30%) ⇒ μ_∞ ≥ 4.3 c². With c = 1 (so that
  ã₀ = a₀ and the framework's derived κ survives) the transition function must stiffen to μ_∞ ≥ 4.3 at high acceleration.
- Health: 𝒥'' > 0 in the transition (existing `aqual_hessian_transition_healthy`), c_s² = 1/2 in deep MOND (existing `csSq_aqual`).
- CMB: the clock's dust is smooth (existing `cuscuton_pressureless_iff`, no clustering); L129/L165 give third-to-second peak
  ratio 0.55 against 0.99 observed for smooth dust. Adding CDM fixes the CMB and fails galaxies (L145–L151); every temporal
  escape is closed (L159–L168).
- NOT run for this exact action: the boosted-frame PPN (α₁, α₂). At leading order they scale with the same screened
  fraction f_eff ~ T(r/ξ) ~ 10⁻⁹, and the k⁴ structure passed G02's boosted test in the AeST host, but that is an argument, not a run.

## Consequence

The single-metric kinetic-mixing action is the right static theory and the wrong cosmology. Nothing in this family supplies
a clustering component that is present at recombination and absent from galaxies; that requirement is L166 clause (i), and
it is exactly what the entire dark-sector programme (condensates, relics, decays, kicks) failed to produce. A derived theory
on these equations needs a NEW mechanism type for clause (i), not another parameter.
