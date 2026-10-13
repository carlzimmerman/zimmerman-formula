# CFG723: Lean certificates for the derived cold-energy results — CERTIFIED (12 theorems, 0 sorry, standard axioms)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (4002e3dd7), 2026-10-13. Block CFG720–729.
- **Files** (in `fable_independent_2026/lean_2026/`): `CFG723_cold_energy_certificates.lean` → `.out` (compiles, exit 0, every theorem
  depends only on [propext, Classical.choice, Quot.sound]); `CFG723_cold_energy_certificates_MUTATE.lean` → `_MUTATE.out` (exit 1: T1
  with the anisotropy set to 0 leaves unsolved goals; T6b with (0, −1, 3) fails `linarith`). Lean v4.34.0-rc2, Mathlib per the project.
- Run: `cd fable_independent_2026/lean_2026 && lake env lean CFG723_cold_energy_certificates.lean` (about 30 s).
- **Settings:** κ = ½ is FITTED (no theorem uses its value). The cold energy's mass is required. Not "theory closed". Certificates prove
  algebra/calculus from stated premises only.

## Statement correspondence (English claim ↔ Lean statement), reviewed 2026-10-13

| theorem | English claim (lane) | Lean statement | match |
|---|---|---|---|
| `aniso_equilibrium` | CFG660 S1: the field-aligned stress makes the law an equilibrium | pointwise: with g′ = F′g_N′, dP∥/dr = (g/K)(1/F′ − 1)g′, P⊥ − P∥ = g(g − g_N)/K, the residual is 0 | MATCH, with the caveat stated in the docstring: pointwise it needs only the chain rule; that P⊥ − P∥ is a function of g alone holds on the law's shell (g_N = F⁻¹(g)), which is not certified |
| `iso_residual` | CFG660 S2: isotropic residual = ρ_b g (ν − 1) | residual = ρ_b·g·(g/g_N − 1) (ν = g/g_N) | MATCH |
| `iso_fails` | isotropic fails wherever baryons are present and the field is non-Newtonian | residual ≠ 0 given ρ_b ≠ 0, g ≠ 0, g ≠ g_N | MATCH |
| `deep_Ppar_deriv` | deep P∥ = −g²/8πG + g³/6πGa₀ | HasDerivAt of 2x³/(3Ka₀) − x²/(2K) is (x/K)(2x/a₀ − 1); with K = 4πG this is the claim | MATCH (the K = 4πG substitution is arithmetic, stated in the docstring) |
| `deep_anisotropy` | deep P⊥ − P∥ → g²/4πG (minus Maxwell stress) | g(g − g²/a₀)/K = g²/K − g³/(Ka₀) | MATCH (leading term; "Maxwell" is the reading, not a theorem) |
| `rhoc_coefficient_nogo`, `rhoc_nogo` | CFG661 T1: exactness for all profiles forces ∂P/∂ρ_c = 0 where F′ ≠ 1 | an affine-in-g_N″ residual vanishing at two different g_N″ forces P_ρ(F′ − 1) = 0, hence P_ρ = 0 if F′ ≠ 1 | MATCH; the affine form (that ρ_c′ carries g_N″ with coefficient (F′ − 1)/K) is a premise from the chain rule, verified symbolically in CFG661's sympy |
| `psi_terms_cancel` | CFG661 T2: the free function Ψ drops out on shell | −ψ′/r² + 2((u/2)ψ′/h)/r = 0 given u = h/r | MATCH (the cancellation step; the rest of T2 is `aniso_equilibrium`) |
| `no_dimensionless_group` | CFG661 T3: no group with {G, a₀} | no rational exponents solve the (kg, s, m) system | MATCH |
| `unique_group_with_c` | with c, the group is w c²/a₀ | exponents ⇔ (0, −1, 2) | MATCH |
| `lensing_difference` | CFG663: cold matter cancels in g_dyn − g_lens | algebra | MATCH |
| `edge_identity` | CFG665: the edge conditions give σ⁴ = G M_b a₀/4 identically | algebra | MATCH (and the identity's status as a coincidence is the lane's reading) |

## What this adds

The algebraic backbone of the session's structural results is now machine-checked: the law as an exact anisotropic-stress equilibrium,
the failure of any isotropic version, the deep Maxwell form, the compression no-go, the cancellation of the free function, the
dimensional obstruction (and the single group that c allows), the cold-matter cancellation behind the lensing test, and the edge identity.
Data verdicts (SPARC, KiDS, mergers), the WKB ill-posedness and the numerical S* failure remain script results, not certificates.
