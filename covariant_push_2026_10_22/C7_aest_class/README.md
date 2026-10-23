# C7_aest_class: AeST's own linear CMB and P(k), from a patched CLASS v3.3.4

## Status

Milestone 2 of 5 (derivation and initial conditions). No spectrum has been computed yet.

## Milestone 2: the linear equations and the adiabatic initial conditions (`c7_derive.py`, 18/18 PASS)

**What was done.** The linear equations were derived from SZ21's covariant action (arXiv:2007.00082, eq. NT_A_action)
with sympy, not copied from the paper. The setup is a general scalar metric, the scalar φ̄ + ϕ and the vector
A_x = ∂ₓα, with A₀ fixed by the unit constraint. The extra sector's stress tensor comes from the metric variation.

**Results (all DERIVED from SZ21's action plus premise P-F; `c7_derive_results.json`):**
- Background: 8πG̃ρ̄ = Q̄K′ − K, 8πG̃P̄ = K, a³K′ = I₀ (D1). I₀ is an initial condition, so Ω_aest is FITTED.
- In any gauge with g₀ₓ = 0, the sector has no anisotropic stress, and (D2_compact):
  - 8πG̃δρ = Q̄K″γ − (k/a)²[K_B E + (2−K_B)χ]
  - 8πG̃δp = K′γ
  - 8πG̃(ρ+p)θ = k²K′ϕ/a
  - with E = α′/a + h₀₀/2 = F₀ₓ/a and χ = ϕ + Q̄α. E and χ are gauge-invariant. γ = ϕ′/a − Q̄h₀₀/2.
- **SZ21's Newtonian-gauge system is reproduced term by term** (D2): the δ, θ and Π definitions, the fluid equations and
  the E equation. The E equation equals −1/(2a²k²) times the α Euler–Lagrange equation.
- **One caveat on SZ21.** Their E equation is the λ_c = 0 case. A nonzero F_Y at Y = 0 adds −(2−K_B)λ_c Q̄χ inside the
  bracket. All runs here use λ_c = 0 (premise P-F; SZ21 say F_Y vanishes in the MOND limit, and Y = 0 on FRW).
- **Conservation** ∇_μT^{μν} = 0 holds on the shell of the ϕ and α equations in both gauges (D4).
  - So δ and θ obey the standard fluid equations with δp = K′γ/8πG̃.
  - The two extra ODEs are α′ = a(E − h₀₀/2) and E′ = −ℋE + (a/K_B){K′χ − (2−K_B)[γ + (ℋ/a + Q̄)χ − 3c_ad²(ℋ/a)Q̄α]}.
- **Gauge map** (D3): synchronous system + map = Newtonian system, exactly. The map is δ_N = δ_S − 3ℋ(1+w)α_C,
  θ_N = θ_S + k²α_C, α_N = α_S − aα_C, E_N = E_S.
- **D5:** the compact forms that the C code will use equal the derived ones.

**Adiabatic initial conditions** (synchronous gauge, radiation era, leading order).
- CLASS normalisation: h = C(kτ)², C = curvature_ini/2.
- The background coefficients w, c_ad² and Q̄ are frozen at τ_ini, with w = c_ad².
  - That holds asymptotically early for both MOND K-functions (Cosh: w ≈ c_ad² ≈ Z₀/Q̄; Exp: ≈ Z₀/(2Q̄Z)).
- Leading terms:
  - δ = −(1+w)C(kτ)²/(2 + 3c_ad² − 3w), which is (1+w)·¾δ_γ at w = c_ad²;
  - θ = −c_ad² C k⁴τ³/((4−3c_ad²)(2+3c_ad²−3w)), which is CLASS's own fluid formula at c_s² = w;
  - E = −C c_ad² Q̄K′a²k²τ⁴/(4K_B(4−3c_ad²)(2+3c_ad²−3w));
  - α = the same with a³τ⁵/20 in place of a²τ⁴/4.
- Checks:
  - IC1: the leading-term IC satisfies the equations, with the residual one or more orders up.
  - IC2: the dust limit is CLASS's CDM IC (δ = ¾δ_γ, θ = E = α = 0).
  - IC3: the Newtonian IC from the D3 map satisfies the Newtonian equations.
  - IC_cform: the C-form formulas equal the series.
- **Ambiguity (stated, not resolved by the papers).** SZ21 cite their adiabatic ICs as "in preparation". Two homogeneous
  pieces are set to zero by choice:
  - the constant δ (CDM-like isocurvature);
  - the constant α (constant vector mode).
  
  Regularity removes the rest. Validation check V5 tests whether the spectra depend on this choice.

**Mutate** (`C7_MUTATE=1`): the sign of the δ term in the Newtonian E′ is flipped. D3, IC3 and D5 fail (15/18, exit 1).
Peak RSS 0.29 GB, about 2 min on one thread.

## What this does not show (yet)

No spectrum and no comparison with data. This lane tests AeST's dust sector and G_cosmo/G_N, not the galactic law: the a₀
term is absent at linear order on FRW. κ = ½ is FITTED and does not enter. Neither a₀ footing enters.
