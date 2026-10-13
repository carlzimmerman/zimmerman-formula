# CFG723 FROZEN CRITERIA: Lean certificates for this chat's derived cold-energy results

Date: 2026-10-13. Written and committed ALONE, before the Lean file exists. Block CFG720–729. Nothing below may be edited after this
commit.

κ = ½ is fitted (no theorem here uses its value). The cold energy's mass is required. Not "theory closed". A Lean certificate proves
the stated algebra/calculus from stated premises; it does not certify data verdicts, numerical integrations, or that any premise is
physically true.

## Target (file `fable_independent_2026/lean_2026/CFG723_cold_energy_certificates.lean`, namespace `CFG723`)

Pointwise spherical setting at one radius: K = 4πG > 0, r > 0, the law g = F(g_N) with F′ ≠ 0, the chain rule g′ = F′·g_N′ as a premise,
ρ_b = (g_N′ + 2g_N/r)/K and ρ_c = (g′ + 2g/r)/K − ρ_b (Poisson with G9).

| theorem | statement | source |
|---|---|---|
| T1 `aniso_equilibrium` | with dP∥/dr = (g/K)(1/F′ − 1)·g′ and P⊥ − P∥ = g(g − g_N)/K, the radial equilibrium residual dP∥/dr + 2(P∥ − P⊥)/r + ρ_c g = 0 | CFG660 S1 |
| T2 `iso_residual` | with isotropic dP/dr = (g/K)(1/s − 1)·g′, s = F′g_N/g, the residual equals ρ_b·g·(g/g_N − 1) | CFG660 S2 |
| T2b `iso_fails` | if ρ_b ≠ 0, g ≠ 0 and g ≠ g_N the isotropic residual is nonzero | CFG660 S2 |
| T3 `deep_Ppar_deriv` | HasDerivAt of 2x³/(3Ka₀) − x²/(2K) is (x/K)(2x/a₀ − 1) (the deep-law P∥′; = −x²/8πG + x³/6πGa₀ with K = 4πG) | CFG660 S3 |
| T3b `deep_anisotropy` | with g_N = g²/a₀: P⊥ − P∥ = g²/K − g³/(K a₀) | CFG660 S3 |
| T4 `rhoc_coefficient_nogo` | if the residual is affine in g_N″ with slope P_ρc(F′ − 1)/K and vanishes for two different g_N″, then P_ρc(F′ − 1) = 0; with F′ ≠ 1, P_ρc = 0 | CFG661 T1 |
| T5 `psi_terms_cancel` | on shell u = h/r (h ≠ 0, r ≠ 0): −ψ′/r² + 2·((u/2)·ψ′/h)/r = 0 (the free-function terms cancel) | CFG661 T2 |
| T6 `no_dimensionless_group` | no rational (a, b) makes (1/length)·G^a·a₀^b dimensionless | CFG661 T3 |
| T6b `unique_group_with_c` | with c, the unique exponent triple is (0, −1, 2), i.e. w c²/a₀ | CFG661 T3 |
| T7 `lensing_difference` | g_dyn = F + g_c and g_lens = g_b + g_c imply g_dyn − g_lens = F − g_b (cold matter cancels) | CFG663 |
| T8 `edge_identity` | σ⁴ = G M_tot g_e/4, M_tot = M_b/f_b, g_e = f_b a₀ (f_b ≠ 0) imply σ⁴ = G M_b a₀/4 | CFG665 (disclosed identity) |

**Pass:** the file compiles with zero `sorry` and every theorem's `#print axioms` lists only [propext, Classical.choice, Quot.sound].
**MUTATE** (`CFG723_cold_energy_certificates_MUTATE.lean`): T1 with the anisotropy set to 0 and T6b with (0, −1, 3) must each fail to
compile. Outputs: `.out` files beside each. A statement-correspondence note (English claim vs Lean statement, per theorem) goes in the
lane README.

## Not certified (stated in advance)

The sympy general-F identities beyond the pointwise algebra, the SPARC / KiDS / merger verdicts, the WKB ill-posedness (S5), the
numerical failure of S* (CFG665) and anything about physical truth of the premises.
