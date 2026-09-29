# CFG44 — Gap 2: can a conserved fluid be the law's dark density? An exact target and a scoped no-go

Scripts (each with a MUTATE control that must exit 1): `B1_target_and_hydrostatics.py` (14 checks), `B2_barotropic_nogo.py` (9), `B3_local_closures.py` (9), `B4_actions_reciprocity.py` (8); shared `Bcommon.py`. Each runs in seconds. Written by a delegated agent and re-run here: all four main runs pass and all four controls fail as required. The point-mass identities of B1 are also certified in Lean (`ChainCert.PointMass`, 24 theorems, no discrepancy with the script). The extended-profile, barotropic and reciprocity results are numerical and were run, not re-derived.

## The target, exactly (B1)

Candidate B needs a cold fluid whose density is the law's phantom: **ρ_c g_tot = (a₀/3) ρ̄_b(<r) = a₀ M_b(<r)/(4π r³)** (CFG10's shell-theorem charge; a₀/4πG = 53.4 M☉/pc², half of CFG2's 106.9 ceiling).
- Point mass (x = r/r_M): ρ_c = a₀/(4πG r √(1+x²)); M_c = M(√(1+x²) − 1); g = √(g_N² + a₀ g_N) (P2); P = a₀M/(8π r²); σ² = V_c²/2.
- Extended baryons: ρ_c depends only on M_b(<r). Hydrostatic P = a₀ g_N/(8πG) + (a₀/2) Σ_out, and σ²/(V_c²/2) = 1 + 4πr²Σ_out/M_b (shape only). Equivalent: σ_r² = V_c²/2 with an anisotropy β = −(3/2) ρ_b/ρ̄_b. It is exact only for P2; ν_mono's phantom departs by up to 2% in the charge function.
- With the fluid feeling only the Newtonian potential of all mass, hydrostatics is an identity, so **the whole content of the target is the closure**.

## What was excluded (each with the exact hypothesis)

| mechanism | verdict | reason |
|---|---|---|
| a universal barotropic P(ρ) in g_tot | excluded | the required c_s² scales as M^e at fixed density, e = (2x⁴+4x²+1)/(4x⁴+4x²+1) ∈ [½, 1]; the spread over M_b = 10⁸–10¹⁴ is ≥ 10³; the effective index Γ runs from 2 to 1 |
| plus a symmetric second potential, or any fixed-kernel force linear in M_b | excluded | deep regime forces β = −1 and P ∝ ρ³; the Newtonian regime then forces g_felt = 0 |
| local closures (constant charge, P = a₀g_N/8πG, field-energy P, σ² = rνg_N/2) | excluded | far-shell theorem: identical local fields, yet P differs by (a₀/2) m/(4πR'²) (+65% for a 10 M_b shell at 40 kpc); off by 0.3–1.4 dex |
| adiabatic maintenance | excluded | adding baryons outside R' changes no force inside yet raises P |
| a Lagrange-constraint action | excluded under GR + real mass | redundant with the barotropic case or overshoots (M_λ/M_c up to 3.4) |
| the fluid feels the law's phantom potential | excluded (N11/N13) | reaction on the baryons 0.11–1.5 g_law |
| a density-slaved fluid | excluded by reciprocity | reaction −1.2 to −4.2 g_law |
| a state-independent "field-energy" stress | excluded | ω² = −igk: Hadamard ill-posed |
| **a temperature-slaved fluid, σ²(x) prescribed** | survives **as a restatement** | well-posed; the outer profile is an attractor; but it POSTULATES σ∞² = ½√(G a₀ M_b) (the BTFR), the cusp amplitude and the nonlocal Σ_out |
| **a locally virialised collisionless fluid with β = −(3/2) ρ_b/ρ̄_b** | survives **as an equilibrium** | Jeans identity derived; β postulated (equal to the target); f(E,L) ≥ 0 open |

An additive law (phantom + cosmic-share cold fluid) overshoots by +0.43 dex at x = 3 and +0.68 dex at x = 1.

## The sharpest statement of what is missing

One function of radius, **C(r) = ρ_c r³ g_tot = (a₀/4π) M_b(<r)**, has no dynamical origin. It is not an equation of state, a linear or Poisson coupling, a local function of the fields at r, a state-independent stress, a constraint under GR plus real mass, a coupling to the phantom potential, a density slaving (reciprocity costs 1–4 g_law), or adiabatically maintainable. What is left is a **non-adiabatic, nonlocal exchange of energy between the baryons and the fluid that depends on the enclosed baryonic mass**. That is Gap 1's ownership object, or a formation-history statement. The BTFR is the postulate σ∞² = ½√(G a₀ M_b). κ = ½ and Ω_c h² stay fitted.

Not tested: anisotropic f(E,L) positivity, non-spherical baryons beyond an estimate (a thin disc's tidal closure and enclosed-mass form differ 3–15×), and any relativistic completion. Hypotheses: spherical, static, Newtonian (GR correction ≤ 3 × 10⁻⁴ for M_b ≤ 10¹²).

Nothing here says the theory is closed.
