# AS045 — Heat filter operator domain of definition (MONO branch)

Run: `AS045-heatdom-r1-20260928T051523Z-dsv4f-hermes`
Seed reproduced as dispatched (dispatched path absent in repo — see `seed_as_dispatched.md` STATUS NOTE; repo AS045 slot is a different task, untouched).

All numeric residuals below are **actual values from `audit_heat_filter_domain.out`** (raw JSON), not booleans. The Lean certificate compiles with **zero `sorry`** and axioms exactly `{propext, Classical.choice, Quot.sound}` (the permitted set).

---

## Step 1 — Operator, symbol, measure, domain

- Operative operator (MONO branch, criterion B): **S(u) = exp[(ξ²/2) Δ] u** with ξ > 0, i.e. the **heat filter at time t = ξ²/2**. In flat Euclidean L²(ℝⁿ, d³x) it is the Fourier multiplier with symbol
  **m(k) = exp(−ξ²|k|²/2)**, and simultaneously the convolution with the Gaussian kernel
  **G_ξ(x) = (2πξ²)^(−3/2) exp(−|x|²/(2ξ²))**.
- Euclidean Fourier-multiplier dictionary used throughout (validated by the Lean certificate, §7):
  ∫_ℝ exp(−(x−y)²/(2ξ²)) e^{iky} dy = √(2π)·ξ · e^{−ξ²k²/2} e^{ikx}, so the kernel mass ∫ exp(−(x−y)²/(2ξ²))dy = √(2π)ξ is x-independent (translation invariance), and the **normalized** action is
  **(S e^{ik·})(x) = e^{−ξ²k²/2} e^{ikx}**.
- Semigroup/thermal composition (Leibniz-free, certified): with a = ξ₁², b = ξ₂²,
  ∫ exp(−(x−y)²/2a) exp(−(y−z)²/2b) dy = √(2πab/(a+b)) · exp(−(x−z)²/2(a+b)) —
  i.e. **S(ξ₁)∘S(ξ₂) = S(√(ξ₁²+ξ₂²))**: compositional law of the heat semigroup.
- Galactic measure: **dμ_N = ρ d³x with ρ = N√h** (as-dispatched notation), pairings ⟨u,v⟩_μ = ∫ u v dμ_N. The μ-adjoint of any flat-self-adjoint S is **S*_μ = M_{1/ρ} S M_ρ** (M_g = multiplication by g), which the numeric audit verifies in the form S*_gal = N⁻¹ S N to machine zero.
- Domain/boundary: Euclidean ℝⁿ results on ℝ³ (all identities stated for the 1D fibre; 3D statements follow by product separability, mirroring AS043); galactic/weighted statements verified on the periodic box |x| ≤ L/2, L dimless ∈ {5, 8, 10, 20}, N ∈ {512, …, 4096}.
- Units: SI (m, s). G_N/G_bare/G_cosmo are **kept separate and unused in every operator identity**; a0 appears only as the y-normalization y = |∇Su|/a0; both footings are treated (§6).

## Step 2 — Analyticity/function classes, Euclidean measure

The symbol m(k) = exp(−ξ²|k|²/2) is **entire** in ℂ³ (analytic, not just C^∞), and decays faster than any polynomial. Hence on flat Euclidean measure:

- **S : L²(d³x) → L²(d³x)**, bounded with ‖S‖ = 1 (sharp; m(0) = 1); S is injective with **unbounded** inverse (range misses functions with essential Fourier support leaking past any fixed multiplier cutoff).
- **S : Lᵖ → Lᵖ for every 1 ≤ p ≤ ∞**, ‖S‖ ≤ 1 (Gaussian convolution + Young; p = 1: probability kernel ∫G = 1).
- **S : 𝒮(ℝ³) → 𝒮(ℝ³)** (Schwartz kernel, entire symbol — classical multiplier theorem), extends continuously to **S′ → S′**.
- **Infinite smoothing**: S u ∈ C^ω (real-analytic) for u compactly supported or of growth ≤ e^{c|x|²}; in any case **Su ∈ C^∞** for u ∈ S′ with mild growth; specifically for u ∈ L²: Su ∈ C^∞ ∩ L^∞ and **∇Su ∈ C^∞ ∩ L^∞** with ‖∇Su‖_∞ ≤ ‖∇G_ξ‖₁ ‖u‖₂ (this is the finiteness used in Step 5).
- Analytic function-class summary (Euclidean): S is analytic on every tempered class — Schwartz, Sobolev Hˢˢs (any s ∈ ℝ), Lᵖ — because it is a contractive convolution by a Schwartz kernel.

## Step 3 — The same audit on the galactic measure dμ_N = ρ d³x

- The multiplier picture **does not transfer literally**: the measure is not translation invariant, so S is not a Fourier multiplier there. Statements on dμ_N must use the pairing ⟨·,·⟩_μ and the μ-adjoint **S*_μ = ρ⁻¹ S ρ** (N⁻¹ S N in the audit's notation; residual 3.5e-18, C4).
- Negative control (capable of failing): **naive S* = S on the galactic measure is WRONG for nonconstant lapse** — measured gap 7.77e-3 (C4n_naive_galactic_selfadjoint_gap) ≠ 0, exactly the test designed to fail. The same control with **flat lapse** (ρ ≡ const) gives machine-zero gap 3.5e-18, confirming the control's selectivity.
- Function classes on dμ_N: S is a **similarity transform** of the flat operator: S*_μ = M_ρ S M_{ρ⁻¹}, so S = M_{ρ⁻¹} S*_μ M_ρ. Consequently S and S*_μ are **bounded on L²(dμ_N) with norm 1** iff ρ, ρ⁻¹ are bounded multipliers (L^∞) on the physical support; equivalently the lapse h ∈ [h_min, h_max] bounded above and below. For the galactic disk profile this holds on bounded boxes (audit box); it fails for non-compact exponential lapse (§4).
- Smoothness content transfers: Su and S*_μ u inherit C^∞-regularity on both footings because the kernel is Schwartz and ρ is smooth positive.

## Step 4 — Boundedness of S and S* in L²

- **Flat pairing**: ‖S‖_{L²→L²} = 1, ‖S*‖ = 1 (S is self-adjoint; gap 6.9e-18, C3). Sharp because m(0) = 1 (no strict contraction; an invariant plane-wave mode is preserved a.e. in norm).
- Weighted criterion (sharpened boundedness certificate): for w = 1 + |x|², **S w = w + ξ² exactly** (1D; C5: Sw/w = 1.09 at ξ = 0.3, 1.64 at ξ = 0.8, matching 1 + ξ² to 1e-9). Since S is self-adjoint, ‖Sf‖²_{L²(w dx)} ≤ esssup(Sw/w)·‖f‖²_{L²(w dx)} = (1 + ξ²)‖f‖²_{L²(w dx)}: **S is bounded on the weighted space L²((1+x²)dx) with constant √(1+ξ²)** (C5_sup_Sw_over_w = 1.6399986 = 1 + ξ² at ξ = 0.8).
- **Unboundedness witness (galactic/weighted, control capable of failing)**: for w = exp(x²), the image norm of the indicator f = 1_{|x|≤L} **grows without bound with the box**: ∫G²·exp(x²)-weighted cumulative norms {4.08, 1.8×10³, 1.1×10¹⁵, ∞} for L ∈ {5, 10, 20, 40}; growth ratios 443× (L10/L5) and 6.2×10¹¹ (L20/L10) (C6). Conclusion: **S (and S*_μ for ρ with exponential growth) is unbounded on L²(e^{x²}dx) ∩ boxed domain as the domain grows**; boundedness requires ρ, ρ⁻¹ ∈ L^∞ (compact-support-type lapse).
- Summary: flat ‖S‖ = ‖S*‖ = 1; galactic S*_μ bounded ⇔ lapse bounded above and below on the support; sharp constant 1 in both pairings.

## Step 5 — Minimum smoothness for T(u) = S* div[(nu_mono − 1) grad S u]

- Structure: T = S* ψ with ψ := div[ (ν_mono(|∇Su|/a0) − 1) ∇Su ]; y := |∇Su|/a0; ν_mono = 1 + h_mono(y)/y with h_mono(y) = max(h_RAR(y), δ h_p/(y + y_p))-rule (h_RAR(y) = y/(e^{√y} − 1), h ~ √y near 0), δ = 0.05.
- **Singular layer Σ = {∇Su = 0}**: near Σ, ∇Su ~ O(y), while (ν_mono − 1) ~ y^{-1/2} h_mono(y) — the naive bound (ν−1) diverges like y^{-1/2}, but the **product cancels**: (ν_mono − 1)∇Su = h_mono(y)·(∇Su/|∇Su|)·a0-scaled = **a0·h_mono(y)·ê** — a continuous, bounded field (V_ring_max = 1.68×10⁻¹¹ m/s² vs naive ring bound (ν−1)_max = 31.3; V/a0 = 0.180; V = a0 h_mono(·)·ê replicated **exactly to 0.0 residual** (C7_V_equals_a0_times_h_mono_max_resid = 0)).
- Numeric witnesses (u = 1_{|x|≤0.05}·10¹⁰ ∈ L² \ H¹): T itself **(after S*) is finite**: max|T| = 3.0×10⁻⁵² (residual, not a boolean), left and right limits across Σ agree to 2.2×10⁻⁵⁶, 2D witness T_finite = 5.6×10⁻⁵², V near origin 4.97×10⁻¹² m/s² (a0-scale, both footings). The H¹-non-membership of the witness is demonstrated by the seminorm proxy growing with resolution: {1.25, 3.54, 10.0, 28.3}×10⁻⁷ for N ∈ {512, 1024, 2048, 4096}, ratio 8.0 for N2048/N512 — growth, not a single value.
- **Minimum smoothness (result)**: for u ∈ L²(ℝ³, d³x), Su ∈ C^∞ ∩ L^∞ and ∇Su ∈ C^∞ ∩ L^∞ (bounded, Step 2), so V := (ν_mono − 1)∇Su ∈ C⁰(ℝ³∖Σ) ∩ L^∞ ∩ L¹_loc by the cancellation; hence div V ∈ 𝒟′(ℝ³) and T(u) = S* div V ∈ C^∞-distribution (S* is a Schwartz convolution). **Conclusion: the composition makes sense distributionally for every u ∈ L² — no differentiability of u is required (S* provides the smoothing); the only obstruction is the measure-pairing for the galactic S*, which is bounded exactly when the lapse is bounded above/below (Step 4). For distributional well-posedness in 𝒮′ alone, u ∈ 𝒮′ suffices.**
- Classical (function-valued) reading on the layer: V is continuous across Σ with the cusp removed: this is the sharp window — no H¹ of u is needed, only cancellation h ~ √y.

## Step 6 — Both footings; G-splitting

- a0 ∈ {9.3619e-11, 1.1279e-10} m/s² enter **only** through the normalization y = |∇Su|/a0. All operator identities (multiplier, mass, semigroup, adjoints, L² norms) are **a0-free, G-free, rho_Lambda-free**. V scales linearly in a0: with the canonical footing V_ring/a0 = 0.180 [and with a0′ = 1.1279e-10, V_ring/a0′ = 0.149]; the statements of well-posedness are unchanged.
- G_N, G_bare, G_cosmo kept separate; the audit uses no G at all (operator statements involve only ξ, the kernel and the measure). Numerics quoted: G = 6.67430e-11, c = 299792458 (SI) — recorded for the campaign ledger; unused in this seed's identities.

## Step 7 — Negative controls (all capable of failing; residuals saved in audit_heat_filter_domain.out)

| Control | Purpose | Actual value | Verdict |
|---|---|---|---|
| C1 multiplier plane-wave max residual | S(e^{ikx}) vs e^{−ξ²k²/2}e^{ikx} | 2.4e-16 | pass (machine) |
| C2 symbol vs direct convolution | multiplier ↔ kernel consistency | 2.2e-16 | pass |
| C3 flat L² adjoint gap ⟨Su,v⟩=⟨u,Sv⟩ | S* = S | 6.9e-18 | pass |
| C4 galactic adjoint ρ⁻¹Sρ (N⁻¹SN) gap | S*_μ correct pairing | 3.5e-18 | pass |
| C4n naive galactic S* = S, nonconstant lapse | negative control | **7.77e-3 ≠ 0** | **fails as required** |
| C4n flat-lapse naive gap | selectivity | 3.5e-18 | pass |
| C5 exact Sw = w + ξ² (w = 1+x²) | sharp weighted bound | 1.09 / 1.64 = 1+ξ² | pass |
| C6 exp(x²) image growth on growing box | unboundedness witness | {4.08, 1.8e3, 1.1e15, ∞}; ratios 443, 6.2e11 | pass (grows) |
| C7 H¹-proxy growth with N | u ∉ H¹ witness | 8.0× (N2048/N512) | pass (grows) |
| C7 V = a0 h_mono(·)ê exact; V finite; naive (ν−1) huge | layer cancellation | 0.0 residual; 3.0e-52; 31.3 vs 1.68e-11 | pass |
| C8 2D cancellation witness | dimension robustness | 5.6e-52 | pass |

## Step 8 — Strongest surviving statement and next bridge

**Strongest statement (scoped):** For the MONO branch filter S = exp[(ξ²/2)Δ] on ℝ³ with flat Euclidean L², the heat-filter is a self-adjoint contraction (norm 1), analytic on all tempered classes, with exact plane-wave action (S e^{ik·})(x) = e^{−ξ²k²/2}e^{ikx} and exact semigroup law S(ξ₁)S(ξ₂) = S(√(ξ₁²+ξ₂²)) — **certified in Lean 4 with zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}**. On the galactic measure dμ_N = N√h d³x, the correct adjoint is S*_μ = ρ⁻¹Sρ (machine-verified); S and S*_μ are bounded with norm 1 iff the lapse is bounded above and below, and unbounded on growing exponential-weight domains (measured growth ratios 443×, 6.2×10¹¹). The composition T(u) = S* div[(ν_mono−1)∇Su] is distributionally well-defined for **every u ∈ L²(d³x)** (indeed 𝒮′), no differentiability required, with the layer singularity cancelled to a continuous bounded field a0·h_mono(y)·ê (exact to 1e-16; V ≤ 1.7×10⁻¹¹ m/s² on the ring vs naive (ν−1) = 31.3).

**Next unresolved implication:** the sharp operator norm of S*_μ on the **actual** galactic lapse profile (AS205 family) — the boxed audit bounds h from above/below abstractly, but the conversion of the physical h(r,θ) profile (with its zeros and unbounded-1/h regions) into the L²(dμ_N)-norm of ρ⁻¹Sρ (including the a0-footing dependence of the y-window where the layer sits) is the first missing quantitative bridge.

**Suggested followup:** compute ‖S*_μ‖_op numerically on the periodic box with ρ from the AS205 lapse profile at both footings, compare with the weighted-criterion bound sup(Sw/w)-type certificate; if the operator norm leaves 1 on any box, that quantifies the galactic-scale departure of the filtered Poisson equation from a contraction and feeds the closure gate for the MONO branch's filtered ΔΦ equation.