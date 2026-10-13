# CFG724 FROZEN CRITERIA: Lean certificates for the cold-energy formula itself

Date: 2026-10-13. Written and committed ALONE, before the Lean file exists. Block CFG720–729. Nothing below may be edited after this commit.

κ = ½ is fitted (no theorem uses its value). The cold energy's mass is required. Not "theory closed". Certificates prove mathematics
from stated premises; they do not certify that the formula is physically true or that its constants are derived.

## Target (`fable_independent_2026/lean_2026/CFG724_formula_certificates.lean`, namespace `CFG724`)

The formula (COLD_ENERGY_FULL_FORMULA_2026-10-13.md): M_total = ν(g_N/a₀) M_b + k M_hot; the other chat's C* static law
g_N = g²/(g + a₀) with saturating polarization u = a₀g/(a₀ + g) and vacuum potential W(u) = −(a₀/K)[u + a₀ ln(1 − u/a₀)], K = 4πG.

| theorem | statement |
|---|---|
| F1 `law_inversion` | for g_N > 0, a₀ > 0: g > 0 ∧ g_N = g²/(g + a₀) ⇔ g = (g_N + √(g_N² + 4a₀g_N))/2 |
| F2 `saturation_bounds`, `saturation_mono` | for g > 0, a₀ > 0: 0 < a₀g/(a₀ + g) < a₀, and it is strictly increasing in g |
| F3 `W_deriv` | for 0 < u < a₀: HasDerivAt W at u with value (1/K)·u a₀/(a₀ − u) |
| F3b `static_law_from_W` | for 0 < u < a₀, g > 0: K·W′(u) = g ⇔ u = a₀g/(a₀ + g) |
| F3c `W_strictly_convex` | W′ is strictly increasing on (0, a₀) (positive second variation: stability) |
| F4 `btfr_limit` | for G, M, a₀ > 0: r·g(r) → √(G M a₀) as r → ∞, with g(r) = (g_N + √(g_N² + 4a₀g_N))/2, g_N = GM/r² |
| F5 `settled_mass_linear` | the settled cold mass M_c(<r) = r²g(r)/G − M satisfies M_c(<r)/r → √(M a₀/G) |
| F6 `supply_edge` | for S > 0, x real: 1/(eˣ − 1) = S ⇔ x = ln(1 + 1/S) (ν_mono edge: r_edge = r_M/ln(1 + f_ret f_b/(1 − f_b))) |
| F7 `sis_hydrostatic` | for σ, G > 0: with M(r) = 2σ²r/G and ρ(r) = σ²/(2πGr²), d(ρσ²)/dr = −ρ·G M/r² at every r > 0 |
| F7b `sis_btfr` | V² = 2σ² and V⁴ = G M a₀ imply σ⁴ = G M a₀/4 |
| F8 `clock_family_closed` (attempted) | for 1 < R ≤ 3.15, f = R^(−1/2): −ln(1 − f)·17.528 ≥ 13.8 (CFG666 canonical: the clock needs longer than the age of the universe). If the exp/log bounds cannot be certified, F8 is reported as NOT CERTIFIED and the rest stands. |

**Pass:** compiles with zero `sorry`; every theorem's `#print axioms` lists only [propext, Classical.choice, Quot.sound].
**MUTATE** (`CFG724_formula_certificates_MUTATE.lean`): F4 with limit 2√(GMa₀) and F6 with ln(1 + S) must each fail.
Statement-correspondence review in the lane README.

## Not certified (stated in advance)

That the law, k, κ or the C* action are physically correct; the hot-gas selector; any data verdict.
