# ChainCert — the composable Lean core of the chain

`lake build ChainCert` builds it; `ChainCert/verify_chain.sh` checks that it builds, has no `sorry`, and that all 52 theorems depend only on `propext`, `Classical.choice` and `Quot.sound` (`MUTATE=1` adds an unproved theorem and must fail). Outputs: `verify_chain.out`, `verify_chain_MUTATE.out`, `Axioms.out`.

**What Lean certifies here is that the conclusions follow from the stated premises. It certifies no empirical fact.** κ = ½ is fitted; Ω_c is fitted; ρ_Λ constant is a premise; the kernel is declared.

## The chain, link by link

| link | statement | status | where |
|---|---|---|---|
| (a) form of a₀ | the monomial c^α G^β ρ^γ has units of an acceleration iff (α, β, γ) = (1, ½, ½) (`C1_a0_form_iff`, both directions; all three unit equations are needed); the exponent matrix has det −2 | **certified, conditional** on the monomial family in (c, G, ρ_Λ) | `Certificates` C1 |
| (b) BTFR zero point | any kernel with ν(y)√y → 1 gives v⁴ → G M a₀ (point mass) | **certified** | `Certificates` C2 |
| (c) kernel family | the premise holds for ν_β (β = 1 is P2) and for **ν_mono** | **certified** | `Certificates` C2, `Kernel` |
| (a)+(b)+(c) composed | v⁴ → G M κ c √(G ρ_Λ) for ν_mono and ν_β | **certified** | `Kernel`, `Certificates` C2 |
| tie + flat a₀(z) | given ρ_Λ(z) constant, the BTFR limit is the same at every redshift; a₀(z) constant ⇔ ρ_Λ(z) constant | **certified, conditional**: flatness is the premise `hflat` (ρ_Λ constant, empirical), propagated; Lean adds nothing beyond "ρ_Λ constant ⇒ a₀ constant", and without `hflat` the conclusion is false | `Chain`, `Certificates` C4 |
| rival a₀ ∝ H(z) | E(z) > 1 for z > 0, strictly increasing; E(2.5) ∈ (3.76, 3.761) at Ω_m = 0.3138 | **certified** | `Certificates` C4 |
| (d) cold-mass rule | f_ex = max(0, 1 − M_ph/M_c) gives M_ph + f_ex M_c = max(M_ph, M_c), monotone in M_c | **certified as algebra of the rule as stated**; the rule is a declared law, not derived from an action | `Certificates` C3 |
| fluid cap (CFG43) | the saturating cap's pressure is P = P_cap x²/(1+x²) ∈ [0, P_cap); with P_cap = (κ²/8π) M_P² Λ the cap's acceleration satisfies a₀² = κ²Λ/8π, the kernel's α(Λ)c² | **certified as algebra inside the fluid module** (`cap_a0_tie` is an identity; it is not linked to the kernel's `ChainPremises.a0` in Lean, which would need Λ = 8πGρ_Λ and c = 1); the cap's entry FORM is a postulate of the CFG43 action; the field equations and the obstruction are numerical (CFG43 scripts). **The P2 point-mass pressure of `PointMass` exceeds this cap for r < r_M (P/P_cap = g_N/a₀), so the two rows are not one fluid** | `Fluid` |
| fluid = phantom, point mass (CFG44) | for the P2 point-mass law with x² = a₀r²/GM: M_c = M(√(1+x²) − 1), ρ_c = a₀/(4πG r √(1+x²)) = (1/4πr²) dM_c/dr; the shell-theorem charge ρ_c g_tot = a₀M/(4πr³); P = a₀M/(8πr²) is hydrostatic in g_tot; σ² = V_c²/2; the effective polytropic index Γ = 2(1+x²)/(1+2x²) is strictly decreasing from 2 to 1 (`no_single_polytrope` is stated for Γ(x); the `GammaEff` form needs one extra step), so no single polytrope for this point mass. `PointMass` uses the explicit-√ P2 law; Lean does not connect it to `nuBeta 1` | **certified as exact real-analysis identities**; the target ρ_c g = a₀M_b/(4πr³) is CFG10's declared law, not derived; extended baryon profiles and the general barotropic no-go are numerical (CFG44 scripts) | `PointMass` |
| κ | the BTFR zero point is linear in κ as a closed-form ratio, by cancellation (`zero_point_linear_in_kappa`; it does not mention the limit); the stated relation κ² = 2β²/(Z_q + 2bβ²) is onto (0, 1/√b) | **certified: the stated relation is onto; that Z_q is free is a premise**, so κ = ½ is a tuned value, not a derived one | `Chain`, `Certificates` C5 |

## Not certified (open)

- Ownership (hierarchical) and the bound-only switch: no formal statement exists without a written specification.
- The action itself: no committed action produces candidate B (see the closure map); nothing in the library formalises one.
- The relativistic sector: lensing slip, PPN, Shapiro, vacuum lensing (the astra lane's certificates live under `deepseek_push/astra_spawn_ideas` and were not audited here), stability and hyperbolicity beyond the scoped certificates in `Mondlean` and the per-file corpus.
- The det = 2 uniqueness of a₀ as a statement about ALL dimensionally allowed forms (C1 covers the monomial family only).
- Every empirical claim (SPARC fits, CFG lanes): they are numerical scripts, not Lean.

## Context

The 116 compiling files in this directory (audit, 2026-09-28) are islands: no file imports another, and `lake build` compiled only `Mondlean` before this library was added. `ChainCert` is the first library whose theorems import each other and compose into a conclusion.
