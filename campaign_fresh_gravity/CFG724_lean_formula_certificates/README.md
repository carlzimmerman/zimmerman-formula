# CFG724 (dir CFG724_lean_formula_certificates): Lean certificates for the cold-energy formula — CERTIFIED (12 theorems, 0 sorry, standard axioms)

- **ID note:** a parallel session also used CFG724 (dir `CFG724_capacity_ceiling`) inside the same reserved block CFG720–729. Refer to this
  lane by its directory. Fixed forward; no history rewritten.
- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (7b2193b05), 2026-10-13.
- **Files** (in `fable_independent_2026/lean_2026/`): `CFG724_formula_certificates.lean` → `.out` (exit 0, no errors, no sorry; every
  theorem depends only on [propext, Classical.choice, Quot.sound]); `CFG724_formula_certificates_MUTATE.lean` → `_MUTATE.out` (exit 1:
  F4 with limit 2√(GMa₀) is a type mismatch; F6 with ln(1 + S) fails its rewrites). Lean v4.34.0-rc2, Mathlib per the project.
- Run: `cd fable_independent_2026/lean_2026 && lake env lean CFG724_formula_certificates.lean`.
- **Settings:** κ = ½ is FITTED (no theorem uses its value). The cold energy's mass is required. Not "theory closed". Certificates prove
  mathematics from stated premises only.

## Statement correspondence (English claim ↔ Lean statement), reviewed 2026-10-13

| theorem | English claim | Lean statement | match |
|---|---|---|---|
| F1 `law_inversion` | the C* static law inverts uniquely to the positive root | g_N, a₀ > 0: (0 < g ∧ g_N = g²/(g + a₀)) ↔ g = (g_N + √(g_N² + 4a₀g_N))/2 | MATCH |
| F2 `saturation_bounds` | polarization saturates below a₀ | 0 < a₀g/(a₀ + g) < a₀ for a₀, g > 0 | MATCH |
| F2 `saturation_mono` | and grows with the field | g₁ < g₂ ⇒ a₀g₁/(a₀ + g₁) < a₀g₂/(a₀ + g₂) | MATCH |
| F3 `W_deriv` | W′(u) = u a₀/(K(a₀ − u)) | HasDerivAt (W K a₀) (u a₀/(K(a₀ − u))) u on 0 < u < a₀ | MATCH (`hu0` unused: the derivative holds for all u < a₀) |
| F3b `static_law_from_W` | K W′(u) = g ⇔ u = a₀g/(a₀ + g) | stated with W′ written explicitly (its value from F3) | MATCH (F3 + F3b together give the claim) |
| F3c `W_strictly_convex` | W′ strictly increasing on (0, a₀): stable vacuum | StrictMonoOn of u a₀/(K(a₀ − u)) on Ioo 0 a₀, K > 0 | MATCH |
| F4 `btfr_limit` | r g(r) → √(GMa₀) (flat curve, Tully–Fisher) | Tendsto (r ↦ r·gpm G M a₀ r) atTop (𝓝 √(GMa₀)) | MATCH (the positivity premises turn out unused: the limit holds for any real G, M, a₀ with Real.sqrt's convention) |
| F5 `settled_mass_linear` | M_c(<r)/r → √(M a₀/G) | Tendsto ((r² g/G − M)/r) atTop (𝓝 √(M a₀/G)), G, M, a₀ > 0 | MATCH |
| F6 `supply_edge` | 1/(eˣ − 1) = S ⇔ x = ln(1 + 1/S) | as stated, S > 0 | MATCH (the r_edge formula follows by substituting S = f_ret f_b/(1 − f_b); that substitution is arithmetic, not certified) |
| F7 `sis_hydrostatic` | ρ = σ²/(2πGr²), M = 2σ²r/G balance | HasDerivAt of ρσ² equals −ρ G M/r² at every r ≠ 0 | MATCH |
| F7b `sis_btfr` | V² = 2σ², V⁴ = GMa₀ ⇒ σ⁴ = GMa₀/4 | algebra on V², σ² | MATCH |
| F8 `clock_family_closed` | CFG666 canonical: R ≤ 3.15 needs > 13.8 Gyr | 1 < R ≤ 3.15 ⇒ 13.8 ≤ −ln(1 − 1/√R)·17.528 | MATCH (17.528 Gyr = 1/H_Λ as used in CFG666 is an input, not certified) |

## What this adds

Together with CFG723 (dir `CFG723_lean_cold_energy_certificates`), the formula's mathematical spine is machine-checked: the law inverts
uniquely, the vacuum polarization saturates and is stable, its potential yields the law exactly, the point-mass field tends to the flat
Tully–Fisher speed, the settled cold mass grows linearly, the supply edge has a closed form, the isothermal halo is in exact balance with
σ⁴ = GM_b a₀/4, and the CFG666 dark-energy clock is closed on its canonical range. Not certified: that the law, k, κ or the C* action
are physically correct; the hot-gas selector; any data verdict.
