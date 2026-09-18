# SW03 — a covariant action for the mesoscopic switch (proposal, 2026-09-17)

**Status: PROPOSAL.** The action below reduces to SW02's equations in the static weak-field limit (verified in
`SW03_covariant_action.py`, sympy). Which gates it passes by structure, which it inherits from published results, and
which are unverified are listed in §4. Nothing here derives κ; a₀ = ½ c√(Gρ_Λ) enters through u₀ as before.

## 1. Fields and the action

Einstein-frame metric g_μν; a unit timelike vector u^μ (the æther, g_μν u^μ u^ν = −1, Lagrange multiplier λ); the MOND
scalar φ (dimensionless); the switch field ψ (dimensionless, 0 ≤ ψ < 1). Matter couples to the physical metric

    g̃_μν = e^{−2φ} g_μν − 2 sinh(2φ) u_μ u_ν                                   (TeVeS's disformal coupling)

which is what makes lensing = dynamics in the MOND regime (Bekenstein 2004: the static weak-field potentials of g̃ are
Φ̃ = Ψ̃ = Φ_E + φ). The action:

    S = ∫ d⁴x √−g { (R − 2Λ)/(16πG)
                    − (1/16πG) K^{αβ}_{μν} ∇_α u^μ ∇_β u^ν + λ (u_μ u^μ + 1)                 [Einstein-æther, c₁..c₄]
                    − (1/8πG) μ_s(ψ) g^{μν} ∂_μφ ∂_νφ                                        [the MOND scalar: LINEAR in φ]
                    − (u₀/2) [ ℓ² g^{μν} ∂_μψ ∂_νψ + ψ² ] + u₀ ψ H(𝒮)                        [the switch: a massive scalar, mass 1/ℓ]
                  } + S_m[g̃_μν, matter]

with
    u₀ = a₀²/(8πG),   a_μ = u^ν ∇_ν u_μ (the æther's proper acceleration),   Θ = ∇_μ u^μ (its expansion),
    𝒮 = [ a_μ a^μ + κ_Θ (cΘ)²/9 ] / (8πG u₀),        H(z) = z/(1+z)   (saturating, so the coupling energy is ≤ u₀),
    μ_s(ψ) = 1 / ( ν(y(ψ)) − 1 ),   y(ψ) = √(ψ/(1−ψ))   (the inverse of ψ = H(y²)),   ν the RAR kernel (or ν from μ₂).

The one new ingredient relative to the record: the nonlinearity of MOND lives entirely in the ψ-sector (a standard
massive scalar sourced by the æther's acceleration), and the MOND scalar φ has a kinetic coefficient that is a GIVEN
positive field μ_s(ψ), not a function of φ's own gradient. That is what removes the RAQUAL/AeST-class pathologies
(ghost from a wrong-sign f′, superluminal scalar), see §4.

## 2. The static weak-field limit (verified in the script)

Static æther u^μ = (1,0,0,0) in the rest frame: a_i = ∂_iΦ_E, Θ = 0. Then
    δψ:   (1 − ℓ²∇²) ψ = H( |∇Φ_E|² / (8πG u₀) )                                          (SW02's smoothed switch)
    δφ:   ∇·[ μ_s(ψ) ∇φ ] = 4πG ρ                                                          (linear in φ)
    matter: g = −∇(Φ_E + φ),  ∇²Φ_E = 4πG ρ.
Point mass, ℓ → 0: ψ = y²/(1+y²) with y = g_N/a₀, so μ_s = 1/(ν(y) − 1) and the scalar force is g_N/μ_s = (ν − 1) g_N:
    g_total = g_N + (ν(y) − 1) g_N = ν(y) g_N          — QUMOND exactly, with the RAR kernel.
Finite ℓ: ψ is the Yukawa-smoothed |∇Φ_E|²/(8πG u₀), which is SW02 with the Einstein-frame field as the switch variable.
Strong field (y ≫ 1): ψ → 1, μ_s → ∞, φ → const: the scalar switches OFF, g̃ → e^{−2φ₀} g up to a constant, and the
theory is Einstein-æther + Λ in the solar system. Uniform external field: ψ depends on |g_ext| only (the cross term
averages out over ℓ), so the external-field effect is isotropic — the framework's cap law from an equation.

## 3. The cosmological background

On FRW the æther is comoving: a_μ = 0, Θ = 3H, so 𝒮 = κ_Θ (cH)²/(8πG u₀) = κ_Θ (cH/a₀)² = 48.9 κ_Θ today, and
ψ_FRW = H(48.9 κ_Θ). With κ_Θ ≥ 1/48.9 the switch is ≥ half-on in the Hubble flow and μ_s ≥ 1/(ν(y_FRW) − 1) is large:
the MOND scalar is switched OFF on the background, the cosmology is GR + æther + Λ, and the deep-MOND strong-coupling
problem of TeVeS-class theories (μ_s → 0 at zero gradient) does not arise on FRW. Inside a virialised region the æther is
static, Θ = 0, and the switch reads the local acceleration alone. Consequence, new and testable: the modification turns
off where the æther congruence is still expanding — beyond turnaround, in the infall regions of clusters (2–5 R500) and in
voids — with a transition set by (cΘ/3)² against a₀². κ_Θ is a coefficient with a window, not a fitted number: κ_Θ ∈ [1/Z², 1]
keeps the background switched off; the framework's Deser–Levin reading suggests κ_Θ = 1/Z² (the cH_Λ ↔ a₀ tie).

## 4. Gate ledger

| gate | status | basis |
|---|---|---|
| deep limit g² = a₀ g_N, RAR transition | PASS by structure | §2, sympy |
| external field: isotropic, no vector-sum anisotropy | PASS by structure | §2; SW01/SW02 numbers |
| solar system: PPN = Einstein-æther's | PASS by structure, æther c_i on the Foster–Jacobson α₁ = α₂ = 0 subspace | the scalar is OFF (μ_s → ∞); the ψ-æther coupling energy ≤ u₀ ≈ ρ_Λc²/32π, negligible; NOT re-derived here |
| lensing = dynamics | INHERITED (Bekenstein 2004 static weak-field result for g̃) | not re-derived here |
| c_T = c | PASS by structure | the tensor sector is Einstein–æther's (c_T set by c₁₃; take c₁₃ → 0 to 1e-15) |
| no ghost in the scalar sectors | PASS by structure | μ_s(ψ) > 0; ψ has a standard-sign kinetic term; the æther health conditions on c_i (0 < c₁₄ < 2 etc.) as published |
| scalar sound speed | PASS by structure | principal symbol μ_s g^{μν}k_μk_ν: null cone of g (sympy) |
| deep-MOND strong coupling (μ_s → 0 as y → 0) | PRESENT inside galaxies' far outskirts, as in every TeVeS-class theory; ABSENT on FRW | §3 |
| the two-halo / cluster residual | NOT ADDRESSED | as before |
| κ | NOT DERIVED | a₀ enters through u₀ |
| full PPN with all couplings, cosmological perturbations, the infall-region switch-off | UNVERIFIED | the next computations (DE-series + a CLASS/hi_class implementation) |

## 5. What would kill it

Any field-aligned azimuthal asymmetry of outer rotation curves at the AQUAL level (DE05); wide binaries at γ_v ≥ 1.16
(DR4); a MOND-level boost persisting in cluster infall regions where Θ ≠ 0; a preferred-frame PPN parameter outside the
Einstein-æther subspace once the ψ-æther coupling is included; a failed CMB fit once ψ_FRW is implemented.
