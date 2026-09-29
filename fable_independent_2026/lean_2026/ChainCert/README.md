# ChainCert — the composable Lean core of the chain

`lake build ChainCert` builds it; `ChainCert/verify_chain.sh` checks that it builds, has no `sorry`, and that all 161 theorems depend only on `propext`, `Classical.choice` and `Quot.sound` (`MUTATE=1` adds an unproved theorem and must fail). Outputs: `verify_chain.out`, `verify_chain_MUTATE.out`, `Axioms.out`.

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
| fluid = phantom, ARBITRARY spherical baryon profile (CFG44) | for any M_b(r) with M_b' = 4πr²ρ_b, Σ_out' = −ρ_b: d/dr[a₀g_N/8πG + (a₀/2)Σ_out] = −a₀M_b/(4πr³); given the target, dP/dr = −ρ_c g_tot (hydrostatic equilibrium for every profile); with Σ_out → 0 the pressure is unique and positive; σ²/(V_c²/2) = 1 + 4πr²Σ_out/M_b; the target is equivalent to the ODE G M_c' = a₀ r u_N/u; the point-mass case reduces to `PointMass` | **certified** (derivatives via `HasDerivAt` at r > 0); the target is CFG10's declared law; **no extended profile satisfying both the decay hypothesis and the target was constructed — only the point mass** (an isothermal profile witnesses the target without decay, an exponential profile witnesses the decay without a cold fluid); ODE solvability, ρ_c ≥ 0 on real profiles and Eddington positivity are numerical (CFG44) | `Profile` |
| NFW cusp scaling (CFG42, CFG65) | with m(x) = ln(1+x) − x/(1+x): m > 0, strictly increasing, x²/2 − 2x³/3 ≤ m ≤ x²/2; M(<r) ~ K r² as r → 0⁺ with K = M₂₀₀c²/(2m(c)R₂₀₀²) (the 2πρ_s r_s r² form); in the family R₂₀₀ = kM^{1/3}, c = c₀M^{−a}: K(M) = M^{1/3−2a} c₀²/(2k² m(c₀M^{−a})) exactly; the leading exponent 1/3 − 2a = 0.1313 for a = 0.101, **but the effective slope is about 0.178 at c ≈ 17** (the m(c) factor adds a c²/((1+c)²m(c)) ≈ 0.047): a factor 100 in halo mass changes the enclosed mass at fixed small radius by 2.27, not 1.83 | **certified** as mathematics; NOT certified: that real halos follow R₂₀₀ ∝ M^{1/3} and c = c₀M^{−a} (Dutton–Maccio is an empirical fit, used as a declared constant), that halos are NFW, or anything about the debris data | `Cusp` |
| κ | the BTFR zero point is linear in κ as a closed-form ratio, by cancellation (`zero_point_linear_in_kappa`; it does not mention the limit); the stated relation κ² = 2β²/(Z_q + 2bβ²) is onto (0, 1/√b) | **certified: the stated relation is onto; that Z_q is free is a premise**, so κ = ½ is a tuned value, not a derived one | `Chain`, `Certificates` C5 |

## Not certified (open)

- Ownership (hierarchical) and the bound-only switch: no formal statement exists without a written specification.
- The action itself: no committed action produces candidate B (see the closure map); nothing in the library formalises one.
- The relativistic sector: lensing slip, PPN, Shapiro, vacuum lensing (the astra lane's certificates live under `deepseek_push/astra_spawn_ideas` and were not audited here), stability and hyperbolicity beyond the scoped certificates in `Mondlean` and the per-file corpus.
- The det = 2 uniqueness of a₀ as a statement about ALL dimensionally allowed forms (C1 covers the monomial family only).
- Every empirical claim (SPARC fits, CFG lanes): they are numerical scripts, not Lean.

## Context

The 116 compiling files in this directory (audit, 2026-09-28) are islands: no file imports another, and `lake build` compiled only `Mondlean` before this library was added. `ChainCert` is the first library whose theorems import each other and compose into a conclusion.

## Added 2026-09-28 by the equations chat: `Gauss` (CFG48) and `Separation` (CFG63)

Two new modules, each theorem on standard axioms only (`verify_chain.sh`: PASS, 131 theorems checked; `MUTATE=1` fails as required; a false-statement mutation of each module is also rejected by Lean).

| link | statement | status | where |
|---|---|---|---|
| CFG48 Gauss lemma (G1, C1) | for `psi' = G M/r^2`, `Phi' = A psi'`: `r^2 Phi'/G = A M`; at the gate off (`W = 0`, `A = 1`) it equals `M`; `d/dr(r^2 psi') = 4 pi G r^2 rho`; the psi-momentum vanishes on `Phi' = A psi'`; a second real-mass source `M_c != 0` makes the `W = 0` mass `M + M_c`, not `M` | **certified: the algebra of the solution check.** NOT certified: the derivation of the Euler-Lagrange equations from the action (sympy in G1), the Helmholtz test (C3), the Noether budget (C4) | `Gauss` |
| CFG63 separation algebra | `S(N) = Delta/sqrt(v/N + f^2)` is strictly increasing in `N`, `< Delta/f` for `f > 0`, tends to `Delta/f`; if `f < Delta/k` then `N(k) = v/((Delta/k)^2 - f^2)` reaches `k` sigma and is the only `N` that does; if `Delta/k <= f` no `N` does; with `f = 0`, `N(k) = v k^2/Delta^2` | **certified as algebra.** NOT certified: any committed number (`Delta`, `v`, `f`, the citations) or the significance model itself, which is CFG63's declaration | `Separation` |

## Added 2026-09-28: `Exchange` (CFG72 algebra, 30 theorems; 161 in the library)

`verify_chain.sh`: PASS, 161 theorems checked, standard axioms only; `MUTATE=1` fails as required; 31 false variants of the statements (one per theorem, plus a weakened-hypothesis variant of `exch_fbb_gt_one`) are each rejected by Lean (`ExchangeMutate.lean.txt`, `ExchangeMutate.out`: 31 errors).

| link | statement | status | where |
|---|---|---|---|
| CFG72 characteristic speed (D5) | `beta = c_f vt^2/N > 0`, so `sqrt(1+beta) > 1`; `c_m sqrt(1+beta) = c` iff `c_m = c/sqrt(1+beta)`; the characteristic polynomial of the declared 3x3 symbol is `lam (lam^2 - c_m^2 (1+beta))`, with distinct roots `0, +-c_m sqrt(1+beta)` for `c_m > 0`, `beta > -1` | **certified as algebra** | `Exchange.lean` |
| CFG72 static structure (D3) | `theta = vartheta M - (1+beta) r_led/c_f`; the probe force `F/vartheta = r_led - 1/lam_t = (delta - 1)/lam_t`, never equal to `r_led`, negative for `delta < 1`; contamination `delta = lam_t r_led` and baryon-baryon ratio `f_bb = 1/(lam_t r_led)` satisfy `delta f_bb = 1` (for `lam_t r_led != 0`), so `0 < delta < 1` forces `f_bb > 1`, `delta <= eps` forces `f_bb >= 1/eps`, and `delta <= a`, `f_bb <= b` with `ab < 1` is impossible; in the open class `r_led = 0` gives `delta = 0` (the identity is not claimed there); `beta = eps_c lam_t`; `f_real = 1 - r/eps_c - delta` (1 in the open class, `< 1` for `r > 0`) | **certified as algebra.** The trade-off holds for any values of the free couplings `lam_t, beta, vt, c_f, N, g_b`; nothing ties them | `Exchange.lean` |
| CFG72 retardation and sigma-slaved / hydrostatic readings (D4, D6) | at value level, `E = E_qs + w` satisfies the wave equation iff `N (w_tt/c^2 - w_rr) = -(g_b M_tt + S_tt)/c^2`; `(3/8) a0 (2g + a0)/(g + a0)` is strictly increasing in `g` on `g > -a0`, lies in `((3/8) a0, (3/4) a0)` for `g > 0`, reduces to G4's `(3/8) a0 (2+x^2)/(1+x^2)` for `g = a0/x^2` and is strictly decreasing in `x`; `int_0^u r^2/u^2 dr = u/3`; the hydrostatic shell energy has reaction `a0/2` per unit mass | **certified as algebra.** D4's 'second-order retardation' implication is NOT certified (CFG72 records it as wrong for boundary-driven sources) | `Exchange.lean` |

NOT certified: the Schwinger-Keldysh action and its Euler-Lagrange derivation (D1, D2), the lattice causality and reciprocity checks, all numerics (Q1 simulations, the Q2 table), the Q3 stability result (nothing here says the operator is stable or unstable), the target law, the P1-P4 verdicts, and that the theory is closed. kappa = 1/2 is FITTED.
