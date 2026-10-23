# C7_aest_class: AeST's own linear CMB and P(k), from a patched CLASS v3.3.4

## Verdict (milestone 4 of 5)

**RUNNABLE NOW.** The patched CLASS reproduces pristine ΛCDM CLASS in AeST's exact dust limit to 2.2×10⁻⁶. It passes the
convergence, gauge and initial-condition checks. The MUTATE build breaks it. So the frozen "native prediction ready"
conditions hold.

No native spectrum has been confronted with data yet: that is step N. The numbers in §Milestone 4 are code validation,
not a test of the theory.

This lane tests AeST's dust sector and G_cosmo/G_N, not the galactic law: the a₀ term is absent at linear order on FRW.
Ω_aest (the Ω_c-like density) is a FITTED initial condition.

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

## Milestone 3: the patch (`c7_make_patch.py` → `aest.patch`, 346 added lines)

- **Where things live.**
  - The extra sector's equations are in one C function, `perturbations_aest_rhs()`.
  - Its background is in one function, `background_aest_K()`.
  - A Khronon-dust variant (C5: c_s² = (Q̄−1)/Q̄) would replace these two functions and nothing else.
- **Background.**
  - Q̄(a) comes from K′(Q̄) = I₀/a³ for the dust, Cosh, Exp and quadratic K.
  - 8πG̃ρ = Q̄K′ − K and 8πG̃P = K.
  - I₀ is solved by Newton so that Ω_aest is the input, which makes it FITTED.
  - The constant −2Λ goes to Ω_Λ (premise P-Λ).
- **Perturbations.**
  - δ, θ, E, χ evolve as in D5/D6.
  - The sector enters δρ, (ρ+p)θ and δp (no shear) and δ_m (for P(k)).
  - The adiabatic IC is IC_cform in synchronous gauge; the D3 map gives the Newtonian IC.
- **Premise P-g conversions.** Ω_γ (and so Ω_ur) × g; n_H ÷ g; the BBN table is read at ω_b/g and ΔN_eff + (43/7)(g−1).
  All runs here have g = 1.
- **Build.** `make -j2 class` on a copy of the pristine tree (`PROVENANCE.md`).
  - `c7_validate.py` checks that the built tree equals pristine + `aest.patch`, byte for byte.
  - A separate build of `aest_MUTATE.patch` flips the metric-source term in δ′.

## Milestone 4: validation (`c7_validate.py`, 7/7 PASS; MUTATE 1/7)

All numbers are in `c7_validate_results.json`.

**What was compared.**
- Spectra: lensed TT, TE, EE and φφ for ℓ = 2–2500, and P(k, z = 0) for k = 10⁻⁴–1 Mpc⁻¹.
- Metric: the maximum relative difference. For TE it is |ΔTE|/√(TT·EE).

| check | result | line |
|---|---|---|
| V0 patched code, sector off, vs pristine (extra) | bit-identical | identical |
| **V1 exact dust limit vs pristine, synchronous** | TT 2.2e-6, EE 1.6e-6, TE 1.0e-6, φφ 1.7e-6, P(k) 5.3e-7; 100θ_s, r_drag identical | ≤ 1e-4; ≤ 1e-6 |
| **V1 exact dust limit vs pristine, Newtonian** | TT 2.2e-6, EE 1.2e-6, TE 9.8e-7, φφ 1.7e-6, P(k) 1.3e-6 | ≤ 1e-4 |
| V1 at default tolerance (reported) | ≤ 1.8e-5 (sync), ≤ 5.9e-5 (Newtonian) | — |
| V2 convergence, Cosh, default → high precision | TT 8.5e-4, EE 1.9e-3, TE 7.0e-4, φφ 6.1e-3, P(k) 2.2e-4; vanilla ΛCDM moves the same (P(k) 9.4e-5) | ≤ max(2e-3, 2× vanilla) |
| **V3 gauge consistency, Cosh** | TT 2.3e-5, EE 8.1e-5, TE 2.3e-5, φφ 1.6e-4 (vanilla: 2.5e-5, 8.1e-5, 2.3e-5, 1.3e-4) | ≤ max(1e-3, 3× vanilla) |
| **V3 gauge consistency, Exp** | TT 2.5e-5, EE 8.0e-5, TE 2.3e-5, φφ 1.6e-4 | same |
| V5 IC attractor (start ×0.5), Cosh | equal to vanilla's own change (largest EE 1.9e-4 in both) | ≤ vanilla + 1e-4 |
| V4 MUTATE (sign of the metric source in δ′) | V1 fails in both gauges (up to 1e5), V2, V3 and V5 fail: 1/7, exit 1 | must break V1 or V3 |

**What the validation shows.**
- **The dust limit is exact.** With w = c_ad² = 0 the sector is CDM, and the code agrees with pristine CLASS to the
  integrator tolerance in both gauges. This tests the background plumbing, the stress-energy coupling, δ_m and the dust
  IC.
- **The non-dust terms are gauge-consistent.**
  - V3 is the only test of the terms that vanish in the dust limit (Π, E, χ). It passes at CLASS's own gauge-agreement
    level.
  - That rests on derivation D3: the synchronous and Newtonian systems are the same theory.
  - A wrong sign or factor in a metric-coupled term would show up as a gauge mismatch. A wrong *gauge-invariant* term
    (in E′ or χ′) would not. Those terms rest on D2 (SZ21's E equation reproduced exactly), D5 and D6.
- **The IC choice does not matter** (V5). Starting earlier changes nothing beyond vanilla's own change. So the two
  homogeneous pieces set to zero (constant δ, constant α) are not driving the result.

**Diagnostics (reported, not gating).**
- **V6: deviation from the dust limit as Z₀ shrinks** (Cosh, SZ21 parameters otherwise).
  - At high precision (V6hi) it falls about linearly with Z₀, i.e. with w and c_ad², as SZ21 say ("Π → 0").

    | Z₀ factor | TT | φφ | P(k) |
    |---|---|---|---|
    | ×1 | 2.2e-4 | 2.0e-2 | 6.2e-2 |
    | ×0.1 | 2.8e-5 | 2.5e-3 | 9.8e-3 |
    | ×0.01 | 3.0e-6 | 2.6e-4 | 1.1e-3 |

  - At default precision the Z₀×0.1 row is not monotone (EE 2.1e-3). That is CLASS default-precision noise: the same
    pair at high precision gives 1.0e-5.
  - Hence AMENDMENT A2: every step-N run uses the high-precision settings.
- **Benchmarks vs pristine ΛCDM at SZ21's caption parameters** (g = 1, default precision).
  - **Cosh:** TT 2.2e-4, EE 8.3e-5, TE 4.4e-5, but **φφ 2.0 %** and **P(k) 5.3 %** (maximum |Δ| over the ranges) at
    k ≤ 1 Mpc⁻¹.
    - In exploratory scratch runs this was a suppression of small scales that grows with k. Step N will tabulate it.
    - It comes from the sector's pressure term c_ad²(k/a)²[K_B E + (2−K_B)χ]/ρ̂, set by K₂ (SZ21's mass μ).
  - **Exp:** ≤ 8e-5 everywhere (c_ad² ~ 1e-14 today).
  - These are properties of the computed theory at fixed parameters, not a confrontation with data.
- **Compute.**
  - The whole validation takes 79 s and 26 CLASS runs.
  - One CLASS run takes 2–3 s at default precision (0.21 GB) and 7.9 s at high precision (0.30 GB).
  - All on one thread, nice 15, while the CFG960 job ran. No run came near 1 GB.
- **Exploratory runs.** A few CLASS smoke runs were made in a scratch directory before `c7_validate.py` existed, to check
  that the build ran. They are not scored, and the thresholds were frozen before them (08daade3f8).

## What this does not show (yet)

No comparison with data and no χ² yet: that is step N. It is frozen (FROZEN_CRITERIA step N plus A2) and reports numbers only, no verdict.

The g ≠ 1 runs, which use the P-g conversions, have not been made yet. P-g itself is a premise: it puts G̃ in the
Friedmann equation and keeps T_cmb and the baryon number physical.

The Higgs-like K is not coded for running: SZ21 say it is not a MOND model. This lane tests AeST's dust sector and G_cosmo/G_N, not the galactic law: the a₀
term is absent at linear order on FRW. κ = ½ is FITTED and does not enter. Neither a₀ footing enters.
