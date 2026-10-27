# The stiffened saturating tether: exact results, no-gos, and numerical findings

Status: working note, `argon_clues/`, 2026-10-14. κ = ½ is FITTED. Nothing here says the theory is closed or that the data favour it.
Evidence labels: **[Lean]** exact statement checked in `lean/ArgonClues.lean` (compiles, no `sorry`, axioms propext/Classical.choice/Quot.sound only; `lean/ArgonClues_MUTATE.lean` with three false variants is rejected, 3 errors). **[script]** committed numerical script (named). **[record]** quoted from an existing lane. The Lean file certifies mathematics, not physics.

## 1. The law and its exact structure  [Lean]
With u = K|P|, K = 4πG, K W_rem'(u) = u²/(a₀−u), the static field equations give
 g_N = g²/(g+a₀), u = g − g_N = g a₀/(g+a₀).
Exact consequences (theorems `split`, `geom_mean`, `harmonic`, `nu_quadratic`, `golden`, `Wcurvature`, `Wrem_deriv`):
- g_N a₀ = g u (geometric-mean invariant); 1/u = 1/g + 1/a₀ (harmonic form; the variant 1/g_N − 1/g = 1/a₀ is false, `wrong_harmonic_false`);
- y ν(ν−1) = 1 with y = g_N/a₀, ν = g/g_N; at y = 1, g/a₀ = (1+√5)/2;
- d/du[a₀²(−ln(1−u/a₀) − u/a₀ − u²/2a₀²)] = u²/(a₀−u) (the remainder potential has the stated derivative), and on the law K W_rem'' = g(g+2a₀)/a₀², K W_full'' = (1+g/a₀)².
These are properties of the chosen W_rem (the "simple" interpolation), not derivations of a₀, κ or R₀.

## 2. No-go: κ is not fixed inside the static action class  [Lean]
`scale_gN`, `scale_tether`, `scale_nu`: (g, a₀) → (λg, λa₀) rescales g_N and u by λ and leaves ν = g/g_N invariant. a₀ enters only as a unit, so the static field equations are isomorphic for every a₀ > 0; no static variation, conservation law or stability condition in this class can fix a₀/(c√(Gρ_DE)). Every "derivation" of κ = ½ audited in this folder (hemisphere average, 4π division, Komar, Galileo drift, S² orientation measure, thermodynamic/horizon/instanton routes) inserted the number through a typed step; the choices are enumerated in `swing_ten_routes.py`, `audit_s2_orientation.py`, `audit_galileo_drift_claim.py` [script].

## 3. The π in Z is Friedmann's  [Lean + script]
`friedmann_units`: H² = 8πGρ/3 and a₀² = c²Gρ/4 imply a₀² (32π/3) = c²H², i.e. a₀ = cH/Z with Z² = 32π/3, and `Z_factor`: Z = 2√(8π/3). In (c, G, ρ_DE) units a₀ = ½ c√(Gρ_DE) is π-free; the open number is the rational ½ and why the scale is √(Gρ_DE) rather than H.
The gate: `gate_solves` (μ_fw solves μ² + μ/x − 1 = 0), `gate_is_DL` (μ_fw(x) equals the Deser–Levin form at y = 2x, i.e. the quadrature floor is a₀/2, not 2a₀), `complete_square`, `floor_ratio`: if the floor were κ_dS = cH then a₀ = 2cH and κ_dS/a_floor = 2Z = 11.58, not √(8π/3).

## 4. The stiffened point-mass solution  [Lean for the inner solution; numerics for the rest]
For the vector stiffness term −(γ/2)|∇P|² with healing length L* (CFG691: L* ≥ 5.75 pc from the Solar System), radial u(r) r̂ obeys
 −L*²(u'' + 2u'/r − 2u/r²) + u²/(a₀−u) = GM/r².
- **[Lean]** `inner_solution`: the constant profile u₀ balances the point-mass field exactly iff u₀ = GM/(2L*²); `M_crit_iff`: it reaches saturation u₀ = a₀ iff M = M_crit = 2a₀L*²/G; `phantom_cap`: inner phantom mass inside L* is M/2, so no source holds more than a₀L*²/G = M_crit/2 of tether inside L*; `M_crit_value`: for a₀ = 9.36×10⁻¹¹, L* = 5.75 pc, M_crit ∈ (4.43, 4.45)×10⁴ M☉ (`M_crit_not_paste`: the 4.46×10⁷ that was circulated is impossible; `sigma_star_not_139`: √(a₀L*) = 4.1 km/s, not 139).
- **[Lean]** `screening_radius`: r_s = L*²/r_M with r_M = √(GM/a₀) satisfies r_s r_M = L*².
- **[script]** `stiffness_point_mass.py`: for m = 2M/M_crit < 2 the BVP solution has u(0) = a₀m/2 (checked) and approaches the algebraic law beyond r_s; the saturated branch (m > 2, 1−u/a₀ = x²/(m−2)) did not converge numerically and rests on the inner expansion. r_s = 857 pc (1 M☉), 16 pc (3×10³ M☉), 2.7 pc (10⁵), 0.27 pc (10⁷), 0.003 pc (10¹¹): stars and wide binaries are Newtonian, galaxies untouched. **There is no decoherence trigger in this equation:** nothing switches cold energy from tethered to free.

## 5. Virial fraction of a power-law tether  [Lean + script]
`free_fraction`: for W ∝ u^(n+1), 1 − W/(uW') = n/(n+1); the cubic tether gives 2/3 (`free_fraction_cubic`). Against X-COP (12 clusters) the level 2/3·R₀·f_hot matches the fitted missing mass (median |Δlog| 0.05–0.08 dex at R₀ = 4.80) but fails the rank test (Spearman 0.46–0.48, p 0.12–0.13; `FROZEN_snap_fraction_test.md`). The mechanism that would make the tether "snap" is not derived.

## 6. Numerical findings (not Lean-certified)  [script]
- **UFDs** (`ufd_stiffness_correction.py`, CFG46's eight, Plummer baryons): the stiffened tether lowers σ and raises the offset: median +0.295 → +0.324 at L* = 5.75 pc, +0.376 at 10, +0.457 at 15, +0.591 at 25; the faintest three (Ret II, Seg 1, Wil 1) rise to +0.70/+0.95/+0.85. L* = 0.05 pc returns the bare law.
- **Outer-halo globulars** (CFG332's data, Υ_V = 1.6, no EFE): X² = 8.53 (alt 9.18) at L* = 5.75 pc against 4.57 for Newton and 11.87/13.12 for the isolated law (frozen rule fails: stiffened must be within 1 of Newton); 5.49/5.76 at 10 pc, 3.75/3.86 at 15, 3.07/3.09 at 25, 3.46 at 40, 4.16 at 80. Globulars prefer L* ≈ 15–40 pc, UFDs prefer small L*, the Solar System requires ≥ 5.75 pc: a quantitative tension window L* ≈ 10–15 pc (UFD cost +0.08 to +0.16 dex).
- **Wide binaries:** the stiffness screens them (r_s ≈ 850 pc ≫ 0.1 pc), so the prediction depends on L*, not on the basin definition; larger L* only shrinks the sealed CFG740 boost.

## 7. Constraints and negative results
- "No external-field effect" is an added basin definition (CFG693 says so), not an outcome; eliminating P gives dF/dg = g_N/K, an AQUAL-like static sector with an EFE; satellite lensing prefers no EFE (χ² 0.7 vs 99.5, PAPER44), so the rule is data-forced and underived. No local Stueckelberg shift or transport operator derived it (`audit_memory_kernel.py`, Stueckelberg audit in `README_closure.md`).
- Cold-energy → dark energy through black holes needs ≈ 8×10³ M_BH per hole and fails the DESI CPL bands as parametrised (`desi_conversion_test.py`); cold energy → baryons is limited by the FRB census to ≤ 12.2% of Ω_b (≤ 2.3% of the cold energy), R(0) ≥ 4.67 (`cold_to_baryon.py`; [Lean] `census_fraction`, `census_R_today_upper`, `census_R_today_central`).
- A free pool that tracks the gas is excluded at 6–8σ (CFG432); containment of a free pool is not parameter-free (`containment_test.py`). SLUGGS cannot separate merger history from hot gas (slow rotators 3, `rotator_test.py`, `tb_hotgas_test.py`).

## 8. What would decide things
Sealed releases: ALMA U4_27928 (2026-11-06) and GS4_24110 (11-28) (CFG571/778: separates a₀ ∝ H and L-fb from the rest, not flat from DESI-tracking); Gaia DR4 (2026-12-02) (CFG740 envelope ½(s/5.754 pc)²; sensitive to L*). Open: κ and the √(Gρ_DE) scale; the basin rule; the free-component origin and trigger.
