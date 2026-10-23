# C7_aest_class: AeST's own linear CMB and P(k), from a patched CLASS v3.3.4

## Verdict (milestone 5 of 5): CRISP FINDING (numbers only; the frozen criteria define no χ² verdict)

**1. Every BBN-compatible small-K_B configuration runs away at linear order.** That covers v4 (λ_s = ∞, λ_c = 0,
K_B ∈ {0.01, 0.05, 0.078}), N1 and N2.
- At SZ21's caption parameters the computed P(k)/P_ΛCDM reaches 10²–10⁴¹ by k ≤ 10 h/Mpc, and χ² is 1.2×10³ to infinite.
- The result is gauge-consistent to ≤ 7.8×10⁻⁴ and converged to ≤ 5.3×10⁻⁶ (tol 10⁻⁹ vs 10⁻⁷). It is a solution of the
  derived equations, not a numerical artefact.

**2. SZ21's own benchmarks (K_B = 0.5 Cosh, 0.1 Exp) do not run away.** With the dust abundance (FITTED) and the six
standard parameters refitted to plik-lite + low-ℓ:
- at g = 1 (the paper's convention) they match the ΛCDM refit (Δχ² = +0.16 and −0.09);
- at the physical g = 1 − K_B/2 (λ_s = ∞) the Cosh benchmark gives Δχ² = +118.7 and H₀ = 55.6.

This tests AeST's dust and gravity sectors only. The a₀ sector is absent at linear order on FRW. Ω_aest is a FITTED
initial condition. Never "the framework fits the CMB".

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

## Milestone 5: native spectra and fits (`c7_native.py`, 7/7 checks; MUTATE 1/2)

Criteria are step N plus three amendments:
- A2: high precision.
- A3 (pre-result): v4 runs, C2's Gauss–Newton fitter, H₀/σ₈/S₈ reporting.
- A4 (**post-result**): RUNAWAY models are not fitted; K5/K6 added.

All numbers are in `c7_native_results.json`. The run took 134 CLASS runs in 20 min at nice 19, one process at a time,
with the Python process at most 0.11 GB.

**Likelihood check.** K1: C2's ΛCDM refit point gives χ² = 1003.48 with the pristine binary, against C2's 1003.20.

**Fits** (plik-lite TTTEEE + low-ℓ TT + low-ℓ EE + A_planck prior; free: ω_b, ω_dm (FITTED), 100θ_s, ln10¹⁰A_s, n_s, τ, A).
- The optimiser resolves χ² to about 0.1: B-Exp is ΛCDM to 8e-5 in the spectra, yet lands 0.09 below it.
- ω_b and ω_dm are in G̃ units (P-g).

| model | Δχ² vs ΛCDM refit | H₀ | σ₈ | S₈ | P/P_ΛCDM (best fits) at k = 0.1, 0.3, 1, 3, 10 h/Mpc |
|---|---|---|---|---|---|
| ΛCDM (pristine) | 0 (χ² 1003.48, plik 582.40) | 67.55 | 0.8280 | 0.8460 | — |
| B-Cosh, g = 1 | +0.16 | 67.56 | 0.8272 | 0.8452 | 1.001, 0.995, 0.936, 0.603, 0.098 |
| B-Exp, g = 1 | −0.09 | 67.56 | 0.8274 | 0.8453 | 0.999, 0.999, 0.999, 0.999, 0.976 |
| B-Cosh-g (g = 0.75) | +118.69 | 55.62 | 0.7950 | 0.8551 | 0.954, 0.907, 0.812, 0.517, 0.082 |
| B-Exp-g (g = 0.95) | +3.11 | 65.21 | 0.8220 | 0.8483 | 0.992, 0.982, 0.973, 0.962, 0.928 |

**RUNAWAY, not fitted.** Values are P/P_ΛCDM at the caption parameters, k = 0.1, 0.3, 1, 3, 10 h/Mpc. g = 1 − K_B/2 (N2: × 400/401).

| model | μ_eff(z=0) (Mpc⁻¹) | P/P_ΛCDM | χ² at caption |
|---|---|---|---|
| N1 (SZ21 Cosh shape, K_B = 0.05) | 8.8 | 1.02, 0.96, 54, 6.3e5, 1.9e9 | 3.7e5 |
| N2 (K_B = 0.07, λ_s = 400) | 8.8 | 1.03, 1.04, 0.72, 146, 5.0e5 | 1205 |
| v4 K_B = 0.01, μ⁻¹ = 1 Mpc | 1.00 | 4.9e26 … 2.8e41 | ∞ |
| v4 K_B = 0.05, μ⁻¹ = 1 Mpc | 1.00 | 0.89, 128, 4.3e6, 6.1e9, 1.8e12 | ∞ |
| v4 K_B = 0.078, μ⁻¹ = 1 Mpc | 1.00 | 1.01, 0.74, 136, 1.9e5, 9.8e7 | 2.2e5 |
| v4 K_B = 0.05, μ⁻¹ = 10 Mpc | 0.10 | 1.1e5 … 7.5e19 | ∞ |

Linear theory has plainly left its range in these runs; the numbers say the linear system is unstable, nothing more.

**λ_s → ∞ (K3).**
- For the stable B-Cosh shape the spectra converge as 1/λ_s: 2.1e-2, 2.2e-3, 3.2e-4 at λ_s = 10², 10³, 10⁴.
- For v4 (K_B = 0.05) the differences do not converge (TT 64, 6.5, 1010). A runaway amplifies the ~10⁻⁴ change in g.

**Question 2: does v4 show enhanced linear growth at k ≳ μ?**
- **Yes, and without bound.** At K_B = 0.078, P/P_ΛCDM is 1.01 at 0.1 h/Mpc, 0.74 at 0.3, then 136 at 1, 1.9e5 at 3 and
  9.8e7 at 10 h/Mpc.
- H1's Jeans-swindle ratio predicts suppression at the same k (0.69 at 1 h/Mpc, 0.022 at 10).
- γ_L is not in the patch. Its weight at 10 h/Mpc is (k/k_c)⁴ ≈ 6e-7 (H1's k_c), so it cannot stop this.

**Mechanism.** This is an ESTIMATE read off the derived equations (D2/D6); it was not isolated numerically.
- With c_ad² → 0 the vector pair obeys χ̈ ≈ (Q̄/K_B)[K′ − (2−K_B)Q̄]χ (cosmic time).
- Early on, K′ = I₀/a³ exceeds (2−K_B)Q̄. The pair is then tachyonic with rate² ≈ 8πG̃ρ̄(1+w)/K_B. That is 2/K_B times
  H3's bound 4πG̃ρ̄, which H3 derived in the opposite regime K′ ≪ (2−K_B)Q₀.
- The window closes at a_c³ = I₀/((2−K_B)Q₀): z_c ≈ 71–78 for Q₀ = 0.1 Mpc⁻¹.
- In the matter era χ ∝ τ^p with p(p−1) ≈ 12f/K_B: p ≈ 5 (K_B = 0.5), 15 (0.05), 32 (0.01).
- The pair feeds δ through δp ∝ c_ad²(k/a)²[K_B E + (2−K_B)χ]. That is why it scales with k and is harmless only when
  c_ad² is tiny (Exp, ~10⁻¹⁴) or K_B is large.
- **Consequence (estimate).** A small-K_B AeST cosmology needs a K-shape with negligible early c_ad², or Q₀ large enough
  that a_c < a_eq (roughly Q₀ ≳ 30 Mpc⁻¹). Neither is fixed by v4. The BBN route via K_B < 0.078 pushes straight into
  this regime.

**Process notes.**
- The first step-N attempts read stale CLASS output: CLASS v3 numbers output files `_00_`, `_01_`, … unless
  `overwrite_root = yes`. The scripts now set it, wipe the run directory and check each file's timestamp.
- Re-running `c7_validate.py` cleanly reproduced every committed validation number exactly (7/7; MUTATE 1/7).
- The first, aborted step-N run showed the runaway before any fit. That is why A4 is marked post-result.

## What this does not show

- **No statement that AeST, v4 or the framework fits or fails the CMB.** The χ² are numbers only.
- **The v4 K-shape (Cosh, Q₀ = 0.1, s = 0.1) is POSTULATED.** A different early K might remove the runaway. That was not
  scanned (no knob scans).
- **The mechanism is an estimate.** The runaway itself is computed and checked.
- **P-g is a premise.** It puts G̃ in the Friedmann equation and keeps T_cmb and the baryon number physical.
- **Not covered:** Higgs-like K (not run); λ_c ≠ 0 (H1's floor door, not run); γ_L (not in the patch). This lane tests AeST's dust sector and G_cosmo/G_N, not the galactic law: the a₀
term is absent at linear order on FRW. κ = ½ is FITTED and does not enter. Neither a₀ footing enters.
