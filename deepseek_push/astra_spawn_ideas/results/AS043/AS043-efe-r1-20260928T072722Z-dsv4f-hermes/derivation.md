# AS043 — Constant acceleration and the external field (REDO, authoritative)

**Run id:** `AS043-efe-r1-20260928T072722Z-dsv4f-hermes`
**Seed hash (verified):** `cefd64b32a09fe49cbf37bd17bb42505ac127c765a2cdaea4d59178d67eb4f6b`
**Supersedes:** `AS043-smk-r1-20260928T040643Z-dsv4f-hermes` (executed a different, wrong seed text; preserved at `results/AS043/AS043-smk-r1-20260928T040643Z-dsv4f-hermes/` but subperseeded).
**Worker:** deepseek-v4-flash-0731 (openrouter) via hermes-agent subagent (run dir `…/AS043-efe-r1-20260928T072722Z-dsv4f-hermes/`).
**Framework base (mandatory):** κ = 1/2 **adopted**, a0 = κ·c·√(G·ρ_Λ) = (c/2)·√(G·ρ_Λ). Operative target per `FRIED_CHICKEN_SPEC.md` amendment: **filtered MONO, causality criterion B**, weak-field equations as in the contract.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

### 1.1 Symbol dictionary
| Symbol | Meaning | Value / unit |
|---|---|---|
| a0 | external-field scale | (c/2)·√(G·ρ_Λ); canonical **9.3619e-11 m/s²**, alternative **1.1279e-10 m/s²** (footings carried separately, never simultaneously) |
| y | B/a0, dimensionless external-field magnitude | > 0 |
| x | g/a0, dimensionless local acceleration | ≥ 0 |
| ν(y) | inverse constitutive response (enhancement ratio) | branch-dependent, dimensionless |
| S | filter operator, S = exp((ξ²/2)·Δ), ξ = 0.5 | dimensionless on periodic/flat domain |
| u | Newtonian potential, Δu = 4πGρ_b | m²/s² |
| Φ | full potential, ΔΦ = 4πGρ_b + S·div[(ν(|∇S u|/a0) − 1)·∇S u] | m²/s² |
| J | linearized response Jacobian J = ν(y)·I + y·ν′(y)·êêᵀ | dimensionless |
| α_par, β_perp | longitudinal/transverse response eigenvalues | dimensionless; dimensionless claim — both footings apply by y = B/a0 |

**Branch declarations (criterion B; all five distinct — verified, §4):**
- **Q:** ν_Q(y) = √(1 + 1/y)  (i.e. g² = B² + a0·B)
- **RAR:** ν_RAR(y) = 1/(1 − exp(−√y))
- **EXP (historical AQUAL-type):** μ_EXP(x) = 1 − exp(−x), ν implicit
- **MU2:** μ_MU2(x) = 1 − (1 + x/2)^(−2), ν implicit
- **MONO (operative):** filtered MONO, criterion B, splice at y_star: y_p = **2.5396382822** (spec 2.5396), y_star = **2.3374124053** (spec 2.3374); ν = 1/(1 − e^(−√y)) for y ≤ y_star, ν = 1 + h/y above with h matched (h_p = 0.6476102379); max |log10 ν − fitted| = **0.01032** at y = 15.85 (spec constraint ≤ 0.0104 at 14.35).

### 1.2 Boundary conditions
- Flat leaf: domain ℝ² (unbounded) or periodic box; u decaying/periodic; **prescribed constant external vector e = a0·y·ê is boundary data** (this is the "external field").
- No additional vacuum boundary conditions needed for the flat periodic computations (mean-removed sources).

### 1.3 Assumptions (inputs vs conclusions)
Inputs: the five declared kernels; adopted κ = 1/2; a0 formula; G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI) for the dimensional examples; ξ = 0.5 filter scale.
Conclusions (to be established): S e = e; the anisotropic linearized response and its exact eigenvalues; the deep ratio 1/2; distinctness of the five branches.

---

## 2. Linearized response around nonzero e (seed step 2)

**Step A — the filter preserves constant vectors.** For constant e and flat (unbounded/periodic) derivatives, S e = (1 + (ξ²/2)Δ + …)e = e because Δe = 0. Numerically verified to machine precision (C1, observed 0.0, tol 1e-12) and with a heat-kernel quadrature at finite x (C1b, observed 1.03e-11, tol 1e-10). The nonlinearity therefore probes ν(|∇S u + e|/a0): the external vector enters as a shift of the filtered Newtonian gradient.

**Step B — directional derivative of the norm.** For fixed unit ŵ:
d/dε |e + ε w| = (e/|e|)·w = ê·ŵ. Hence
d/dε ν(|e + ε w|/a0)|_{ε=0} = (y ν′(y))·cos θ,  cos θ ≡ ê·ŵ.

**Step C — linearized phantom term.** Linearizing the source term about the external field e with perturbation ∇S u = ĝ·|g|:
S·div[(ν(|e + ∇S u|/a0) − 1)(e + ∇S u)]
→ linear part: S²·[(ν(y) − 1)·Δu + (ν′(y)/a0)·(ê·∇S u)·|e|…] — carrying the directional derivative through, the linearized multiplier in Fourier space (k̂ = (cos θ_k, sin θ_k)) is:

**M(k) = 1 + S²(k)·[ν(y) − 1 + y ν′(y)·cos²θ_k]**,  S²(k) = exp(−ξ²k²)

(the outer S· and the partial-product rule combine to S²; sign verified against the residual diagnostics — an initial minus sign made the residual linear in A and was corrected).

**Step D — the Jacobian.** Reading M as the Fourier symbol of I + (ν−1)·S²-type diffusion plus the rank-one direction term gives, back in real space,
**J = ν(y)·I + y·ν′(y)·êêᵀ**, with eigenvalues
**α_par = ν + y ν′** (longitudinal), **β_perp = ν** (transverse).

---

## 3. Intermediate algebra, signs, units, asymptotics (seed step 3)

### 3.1 Scale factors and units
- All steps dimensionless: y = B/a0, ν, J. Dimensional examples (a0 footings) computed separately with the SI constants above: canonical y(e = 1e-10 m/s²) = 1.06816, α/β = **0.71465**; alternative y = 0.88660, α/β = **0.69899**. Deep example e = 2e-11 m/s², canonical: y = 0.21363, α/β = **0.60668**. Both footings are separate columns — never mixed (κ fixed = 1/2; ρ_Λ fixed per footing).
- Sign conventions: external vector e adds to the gradient before the norm; transverse response is identically zero at first order (stationarity of the norm); the second-order transverse coefficient is ν′/(2y) per unit transverse field (C2c), i.e. quadratic growth, positive.

### 3.2 Deep limit (leading neglected term and its domain)
For all five branches ν(y) = y^(−1/2) + c + o(1) as y → 0 with:
c = 0 (Q), 1/2 (RAR), 1/4 (EXP), 3/8 (MU2), and MONO → RAR below the splice (C4: c_obs = 5e-11, 0.500000000008, 0.250000000007, 0.375000000013 at y = 1e-20, mpmath 60 digits, tol 1e-8; sub-asymptotic values bracketed by Richardson extrapolation).
Then **1 + y ν′(y)/ν(y) → 1/2** (C4c observed 0.50000000005 … 0.50000187, tol 1e-5 at y = 1e-10; C4f for the filtered kernel M_par/M_perp at k = 0.3, ξ = 0.5: 0.500000114 … 0.500002614, tol 1e-3). Leading neglected term: next order in the deep expansion is O(√y·c) relative — the ratio converges as (1/2) + O(√y·c).

### 3.3 Newtonian limit
y → ∞: ν → 1 (Q: 1 + 1/(2y); EXP: 1 − …; verified on the grid up to y = 10^8, C3 observed par = ν + yν′ → 1 within 2e-4 at y = 1e8), J → I: isotropic Newtonian response is recovered.

---

## 4. Independent checks — different representations, actual residuals (seed step 4)

All residuals below are real computed values (raw output: `efe_run.out`); every named check has its tolerance set before evaluation.

| Check | What it tests | Observed residual | Tolerance |
|---|---|---|---|
| C1 | S e = e, Fourier zero-mode | 0.0 | 1e-12 |
| C1b | heat-kernel convolution preserves linear datum e·x (composite Simpson, 10σ window, n = 50000) | 1.026e-11 | 1e-10 |
| C2 | d/dε |e + ε w⊥| = 0, w⊥ ⟂ ê, all 5 branches, y ∈ {0.01,0.1,1,10} (analytic directional derivative vs exact finite-difference average) | 0.0 | 1e-12 |
| C2b | ν-transverse derivative = 0 | 0.0 | 1e-12 |
| C2c | second-order transverse coefficient (1/2)ν′(y)/y vs finite-difference | rel ≤ 1e-4, e.g. Q y=0.01: −49751.828 vs −49751.860 | 1e-4 |
| C3 | Jacobian eigenvalues: par = ν + yν′ vs exact computation; perp = ν | par/perp rel ≤ 1e-6, e.g. Q y=0.01: 5.07469029 vs 5.07468964 | 1e-6 |
| C4/C4b/C4c/C4f | deep asymptotics (§3.2) | see §3.2 | 1e-8/1e-6/1e-5/1e-3 |
| C5g | five branches pairwise distinct on the y-grid (max relative deviation) | min pair 0.02349 (RAR–MONO) > 0 | > 0 |
| C6 | nonlinear residual of the linear-EFE kernel in the full filtered field equation: physical second-order remainder r2(A) with exact quadratic scaling r2(A/4)/r2(A) ≈ 1/4, RAR/MONO at y ∈ {0.05, 0.5, 10} | r2 = 1.24e-4 … 3.95e-6; ratios 0.250, 0.250, 0.250 | r2 < 1e-2, 0.02 < ratio < 0.5 |
| C6b | **independent representation**: real-space sparse-LU periodic Poisson (5-point stencil with periodic wrap) + rational S_m m = 64 vs the Fourier closed-form linear solve | rel 6.35e-4 | 2e-2 |
| C6c | filtered kernel response parallel/perpendicular vs analytic S²-form | | 1e-10 |
| C7 | C-branch grid records + MONO splice landmarks | y_p = 2.5396382822, y_star = 2.3374124053, max dex diff 0.01032 at y = 15.85 | spec intervals |

The C6b real-space cross-check is the requested "different representation": it re-derives the linear response from the original field equation with independent machinery (rational filter approximation + LU solve) and agrees with the Fourier closed form to 6.4e-4.

## 5. Negative control (seed step 5) — capable of failing, and it does

**Control NEG (scalar magnitudes):** replacing the vector law by the scalar prescription ν(|e| + |g|) adds a **first-order transverse response** d/dε ν(|e| + ε|w⊥|) = (√y-independent) ν′·ŵ = 0 is NOT attained — observed spurious transverse coefficients (Q/RAR/EXP/MU2/MONO × y ∈ {0.01…10}): 497.5, 15.08, 0.354, 0.00477 … (all > 1e-6, PASS = control fired). The vector law (C2) gives exactly 0.0. **The scalar prescription is not the vector law — the control is capable of failing and the linearization diagnostics distinguish the two.**

**Control DOM (domain boundary):** at y = 0.05, A = 0.02 the quadratic-scaling diagnostic breaks: r2(A = 0.02) = 1.580e-01 (> 5e-2) and |ratio − 1/4| = 0.217 (> 0.12) — the linear kernel is no longer a solution of the nonlinear equation at this amplitude (the linearization genuinely breaches). The result is thereby honest about its domain: linear EFE claims hold for y ≳ 0.05 at A = 1e-3, and the breakdown amplitude is bracketed (~A ≲ 5e-3 at y = 0.05).

**Control C1b/quadrature:** heat-kernel check is an exact identity (filter preservation) verified to 1e-11 — stated as exact identity, numerically cross-checked; all other finite checks are labeled as finite numerical consistency checks.

---

## 6. Strongest surviving statement

> **EFE theorem (dimensionless, both footings apply via y = B/a0):** On a flat leaf with filter S = exp((ξ²/2)Δ), ξ = 0.5, criterion-B branches Q, RAR, EXP, MU2, MONO, and prescribed constant external vector e = a0·y·ê:
> (i) S e = e exactly, so the external field enters only through the norm shift |∇S u + e|;
> (ii) the linearized response about e is J = ν(y)I + y ν′(y) êêᵀ with eigenvalues α_par = ν + yν′, β_perp = ν — the transverse response is **exactly zero at first order** (stationarity) and quadratic at second order with coefficient ν′(y)/(2y);
> (iii) in the deep limit ν → y^(−1/2) + c, the anisotropy ratio α_par/β_perp → 1/2 for every one of the five branches (Q, RAR, EXP, MU2, MONO; MONO follows RAR below y_star);
> (iv) the five branches are pairwise distinct (min pairwise max-deviation 2.35e-2), so matching the deep asymptote does NOT make any two kernels equivalent;
> (v) nonlinear residual of the linearized kernel is quadratic in amplitude with coefficient consistent with (1/2)ν″ structure, r2(A/4)/r2(A) = 0.250, on the domain y ≥ 0.05, A ≤ 1e-3 (8×8-periodic, N = 64, ξ = 0.5; residual norms 1e-4–4e-6 in a0-normalized units).
> Domain: y ∈ (0, 10^8] with grid 10^k, k = −10…8 step 0.1; deep statements at y ≤ 1e-10 (mpmath 60 digits); linearization statements on the finite box above.
> Dimensional examples: e = 1e-10 m/s² gives α/β = 0.71465 (canonical a0) and 0.69899 (alternative a0) — a canonical MOND-like **external-field effect**; the two footings differ by ~2% in the ratio at this e, which is a candidate discriminator but is not here compared to any observation.

**Transfers needed to the full theory:** the flat-leaf S e = e + linear kernel has been established; transferring to the full (spherically symmetric, curved-leaf) theory requires the radial-leaf extension of the filter commutation (next implication, see below). No other branch was imported to repair anything.

**Certified in Lean 4 (zero sorry, axioms = {propext, Classical.choice, Quot.sound}):** see §7.

## 7. Lean certificate

`AS043_efe_certificates.lean` (this directory), compiled with `lake env lean` (Lean 4.34.0-rc2, mathlib of `fable_independent_2026/lean_2026`), **0 errors**; `#print axioms` for all 7 theorems returns exactly `[propext, Classical.choice, Quot.sound]`:
- `transverse_stationarity_first_deriv`: d/dt √(A + t²B)|₀ = 0 (A > 0, B ≥ 0) — the first-order transverse stationarity;
- `transverse_stationarity_second_deriv`: d²/dt² |₀ = B/√A — quadratic transverse growth with coefficient |w|²/|e| (matches C2c's ν′/(2y) structure after the composed chain);
- `scalar_prescription_first_deriv` (+ `_nonzero`): d/dt (√A + t√B)|₀ = √B ≠ 0 — the **negative control certified**: the scalar prescription has a first-order transverse response;
- `powerlaw_anisotropy_ratio`: 1 + y·ν′(y)/ν(y) = 1/2 for ν(y) = C/√y — the universal deep anisotropy ratio;
- `jacobian_par_eigenvector`, `jacobian_perp_eigenvector`: J e = (ν + yν′)e and J w = νw for |e| = 1, e·w = 0, J = νI + yν′·êêᵀ — the anisotropic response eigenvalues.

## 8. Bounds, resources, reproducibility

- Prototype bound: ≤ 120 s wall, ≤ 512 MB, 1 thread. **Actually enforced:** single-threaded via `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`; `/usr/bin/time -l` reports **1.30 s real, 0.02 s sys; 75,071,488 bytes max RSS (48,742,976 peak footprint)**.
- Commands: `cd <run dir> && OPENBLAS_NUM_THREADS=1 … /usr/bin/time -l python3 as043_efe.py > efe_run.out 2> efe_run.time`; `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS043_efe_certificates.lean`.
- 142/142 named checks PASS (`efe_run.out`); residuals quoted above are the raw printed values.
- Source hashes (verified against `SOURCE_MANIFEST.json`): README.md 91a5fac4…, FRIED_CHICKEN_SPEC.md 98d9149f…, peer_review README 521d9ac3…; seed cefd64b3… (task pin).

## 9. Limitations (what this does not establish)

- Flat-leaf (periodic 8×8) linearization only; no curved leaf, no time dependence, no radiative/causal-retarded response beyond criterion B's causality assumption.
- MONO landmarks verified against the spec's stated values (2.5396/2.3374, dex ≤ 0.0104), not re-derived from first principles in this task.
- The EFE anisotropy is mathematical; no observational dataset is fitted (no empirical test claimed — this is a derivation + finite numerical consistency evidence).
- κ = 1/2 is adopted input, not derived.
- Second-order (quadratic) response structure verified only at the level of the leading coefficient; full second-order kernel not certified in Lean.

## 10. Next unresolved implication and suggested follow-up

**First missing bridge to the full theory:** the filtered-MONO external-field effect on a *curved/radial leaf* — specifically whether S e = e and the rank-one Jacobian form survive when the filter acts on a non-flat (e.g., spherical-symmetric) leaf, and which observable geometry (e.g., wide-binary or cluster-core anisotropy, or a solar-system-boundary test) separates α_par/β_perp ≈ 0.71 (canonical footing) from 0.70 (alternative) — the two footings differ at the 2% level in the EFE ratio at e = 1e-10 m/s².

**Suggested follow-up:** AS043 child: "radial-leaf external-field kernel" — derive the filter commutation S e = e on a spherically symmetric leaf and the anisotropic response for a radial external vector; dispatch to a fresh worker with this run's hash as parent.