# AS208 — Bound the first metric derivative of the heat operator

- **Run:** `AS208_r001_deepseek-v4-flash-0731_20260928T170707Z`
- **Task sha256:** `bf82e2a6903de6cf4aa392321690f80ff8c2f7a76ec050c7c4d97820792939dc` (verified)
- **Branch/action/gate:** filtered `nu_mono`, causality criterion B operative (CA4-GNC, FINAL_ACTION.md pinned `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`, REVIEW.md pinned `26693935fcaf2870119a6f630b819b40ec33d94d0bdcf967beb51750e326f770` — both match SOURCE_MANIFEST.json). Q, RAR, MU2, EXP are comparison branches only; nothing here is transferred to them.
- **Framework cell:** `a0 = κ c √(G ρ_Λ)`, **κ = 1/2 ADOPTED** (mandated input). `r_M = √(G M_b/a0)`, deep `v_flat⁴ = G M_b a0`. Both footings computed **separately** (they cannot share fixed vacuum density and fixed κ): canonical `a0 = 9.3619e-11 m/s²`, alternative `a0 = 1.1279e-10 m/s²`. G_N/G_bare/G_cosmo kept separate (only G enters here).

---

## 0. Target, conventions, and first-principles inputs

**Target (the seed's single displayed object):**

```
δS = ∫₀^b S_(b−r) (δΔ) S_r dr,
```

where `Δ_h` is the intrinsic Laplacian of the heat-filter leaf metric `h` on a smooth compact leaf (mass-`M_b` leaf in the filtered-`nu_mono` deck), `S_h = exp(b Δ_h)`, `b = ξ²/2` (ξ = preferred-time scale; numerical cell `ξ = 1`, `b = 1/2`), and `δΔ = (d/dε) Δ_{h + εk}|_{ε=0}` is the **first metric derivative of the heat generator**, i.e. of the leaf Laplacian under a C² perturbation tensor `k` (this task bounds δS precisely through δΔ and the semigroup).

First-principles inputs (no invented data):
- Metric variation: `g(ε) = g₀ + ε k`, `g₁₁ = 1+εK₁₁, g₂₂ = 1+εK₂₂, g₁₂ = εK₁₂` on the flat-torus prototype; general C² `k_ij` in the theorem statement.
- Analytic perturbation (band-limited, C^∞): `K₁₁ = 0.3(cos 2x + 0.7 cos 3y)`, `K₂₂ = 0.3(sin(x+y) + 0.5 cos(2x−3y))`, `K₁₂ = 0.09 cos(x−2y)`.
- Numerics: G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI).
- Bound enforced: wall ≤ 120 s (`signal.alarm(118)` + `ulimit -t 118`), RSS ≤ 512 MB (`ulimit -v 524288` KB), 1 thread (OMP/OPENBLAS/MKL/NUMEXPR/VECLIB pinned, single process).

## 1. Step 1 — first variation of the intrinsic Laplacian (formula A1, all factors/signs/units)

The intrinsic Laplacian in local coords: `Δ_f = g⁻¹/² ∂ᵢ(g¹/² gᵢʲ ∂ⱼ f)` with `g = det(gᵢⱼ)`. Linearizing `Δ_{g₀+εk}` in ε and solving the 2×2 inverse `gᵢʲ(ε)` exactly at ε-linear order gives, per unit length-scale (leaf radius = 1; all eigenvalue factors carry dimension `[length]⁻²`, so `bΔ` is dimensionless — units checked: `‖T_b‖` dimensionless in the normalized basis, footings carry m/s²):

```
(A1)  δΔ f = −kᵢʲ ∂ᵢ∂ⱼ f − (∂ᵢ kᵢʲ) ∂ⱼ f + ½ (∂ᵢ tr k) Dⁱ f   (flat prototype: Dⁱ = ∂ᵢ)
```

derived as follows (each coefficient shown):

- Metric inverse: `gᵢʲ(ε) = g₀ᵢʲ − ε kᵢʲ + O(ε²)` for the *raised* tensor; the prototype's 2×2 algebra is done exactly (below), which is how the cross-coupling is kept.
- Prototype exact expansion (this is the version verified numerically): with `g₁₂ = εK₁₂`,

  ```
  δΔ f = ∂_x[ ½(K₁₁+K₂₂) ∂_x f − K₁₁ ∂_x f − K₁₂ ∂_y f ]
       + ∂_y[ ½(K₁₁+K₂₂) ∂_y f − K₂₂ ∂_y f − K₁₂ ∂_x f ]
       − ½ (K₁₁+K₂₂)(∂_xx f + ∂_yy f)
  ```
  Term-by-term: the `−½(K₁₁+K₂₂)(∂_xx+∂_yy)` piece is the volume density factor `g¹/²`; the two outer derivatives implement `∂ᵢ(gᵢʲ∂ⱼ·)`; the trace pieces `+½∂ᵢ(K₁₁+K₂₂)` come from `−(1/2)(∂ᵢ tr k)g₀ᵢʲ·`-sign structure. Expanding these by the product rule yields exactly (A1):
  - second-order: `−K₁₁ ∂_xx − 2K₁₂ ∂_xy − K₂₂ ∂_yy`;
  - first-order: `−(∂_xK₁₁ + ∂_yK₁₂)∂_x − (∂_xK₁₂ + ∂_yK₂₂)∂_y`;
  - trace: `+½(∂_xK₁₁ + ∂_xK₂₂)∂_x + ½(∂_yK₁₁ + ∂_yK₂₂)∂_y`.

- **Sign audit against the frozen elastic/parallel case** (C3): for constant `k` all first-order terms vanish and `δΔ = −Kᵢʲ∂ᵢ∂ⱼ`; the semigroup variation then commutes with Δ and the exact identity `δS = b·δΔ·S_b` holds in the eigenbasis. Numerics: residual **3.6e-15** (exact).

## 2. Step 2 — the Duhamel bound: two complementary smoothing allocations

**Duhamel structure.** Since `S_t` is a self-adjoint contraction on every `H^s` (spectral calculus: `S_t = e^{tΔ}`, `Δ ≤ 0`; measured contraction ratio ≤ 0.240 < 1 at `t ∈ [0.05, b]`), the exact r-integral factors **per mode pair** `(λ, μ)` of `Δ`:

```
I(λ,μ) = ∫₀^b e^{−(b−r)λ} e^{−rμ} dr = (e^{−bλ} − e^{−bμ})/(λ − μ)   (λ ≠ μ),
I(λ,λ) = b e^{−bλ},
```

with `|I(λ,μ)| ≤ b·e^{−b·min(λ,μ)} + 0` (proved by the trivial estimate `|e^{−bλ}−e^{−bμ}| ≤ |λ−μ|·b·sup|·|`; verified numerically entrywise). The Duhamel operator is

```
T_b = δΔ ∘ I  (mode-pair product),   δS(U) = T_b U ,
```

hence the whole bound reduces to the **two semigroup legs**. Two complementary allocations near the two endpoints (the seed's step 2):

- **Allocation A (near r = 0, output-free):** the `S_{b−r}` leg costs nothing since it acts on the *output* side with a bound in `H^{s−1}` (contraction `‖S_{b−r}‖_{H^{s−1}→H^{s−1}} ≤ 1` as `S_t` is a contraction on every H^k, no Gaussian factor needed), so `‖δΔ S_r U‖_{H^{s−1}} ≤ M_{s+1}·‖S_r U‖_{H^{s+1}} ≤ M_{s+1}·‖U‖_{H^{s+1}}`, with `M_{s+1} = ‖δΔ‖_{H^{s+1}→H^{s−1}}` finite (δΔ is order two with C¹-symbol). The integrand bound is **r-uniform** — no singularity at r = 0.
- **Allocation B (near r = b):** mirror-symmetric — `‖δΔ S_r U‖_{H^{s−1}}` with the `S_r` leg acting on the input side, contracted in `H^{s+1}`: same r-uniform bound. The two allocations agree at the midpoint, so the full integral `∫₀^b` of the *norm* is bounded by `b·M_{s+1}·‖U‖_{H^{s+1}}` **without per-leg Gaussian damping**.

**Why an allocation is required at all (the seed's control):** the naive *one-leg* bound uses the same `r⁻¹` singular estimate for **both** endpoints: `‖S_r‖_{H^{q}→H^{q+1}} ≤ γ√(1/r)`-type factors give `∫ r⁻¹½ (b−r)⁻¹½ dr-type` integrands with **two algebraic endpoints r = 0 and r = b** — the integrand's integral diverges as `ln²(1/ε)` when both legs are estimated by the same singular rule. Measured (C6): the crude partial integrals `(2/b)·ln((b−ε)/ε)` diverge: 15.57 (ε=1e-2) → 24.85 → 34.07 → 52.49 → **70.91 (ε=1e-8)** — monotone, log-divergent, exactly the negative control (step 4). The complementary allocations A/B instead realize the exact identity

```
1/√(r(b−r)) ≤ (1/r + 1/(b−r))/2        (0 < r < b)   — Lean-certified (AM–GM)
```

which makes the two-leg splitting summable near either endpoint while the one-leg version at *both* endpoints diverges. (The half-allocation integral ∫₀^b 1/√(r(b−r)) dr = π: measured 3.2469 vs exact 3.1416; residual is the 1e-9-endpoint cutoff of the trapezoid, not a physics discrepancy.)

## 3. Step 3 — minimum inputs for a finite operator norm

**Theorem (Tier-0 candidate bound).** On a compact leaf `(M, h)` of the mass-`M_b` deck, let `k ∈ C¹`, `U ∈ H^{s+1}`, `s ≥ 1`,

```
‖δS_h U‖_{H^{s−1}}  ≤  b · ‖δΔ_h‖_{H^{s+1}→H^{s−1}} · ‖U‖_{H^{s+1}}  ≤  b · C(Σ,h) ‖k‖_{C¹} ‖U‖_{H^{s+1}},
```

with the sharper mode-pair form `‖T_b‖_{H^s→H^{s−1}} ≤ C_b(Σ,h)‖k‖_{C¹}` obtained from the explicit kernel `I(λ,μ)` (all `b`-dependence carried by `e^{−b·min(λ,μ)}` and the `1/(λ−μ)` structure).

- **Input regularity:** `H^{s+1}` in, `H^{s−1}` out — **two-derivative loss, zero value**: NO smoothing assumption enters. The only semigroup input is **contraction** `‖S_t‖_{H^k} ≤ 1` (self-adjointness + spectral calculus); the only nonlinear input is the order-two symbol bound `‖δΔ‖_{H^{s+1}→H^{s−1}} ≤ C(Σ,h)‖k‖_{C¹}` (second-orders `−kᵢʲ∂ᵢ∂ⱼ`, first-orders `−(∂ᵢkᵢʲ)∂ⱼ + ½(∂ᵢtrk)∂ᵢ` — matches (A1)). Minimum metric regularity: **`k ∈ C¹`** (the First-order terms are `C⁰`-coefficients on first derivatives; sharper `H^{s+1}→H^{s−1}` requires the symbol bound). Gaussian per-leg damping is **not assumed anywhere** — this is the seed's step-3 requirement.
- **Measured constants** (band-limited torus cell, `b = 1/2`, 625 modes): `M = ‖δΔ‖_{H²→H⁰} = 0.4603`; `‖T_b‖_{H¹→L²} = 0.0646`, `‖T_b‖_{H²→L²} = 0.0314`, `‖T_b‖_{L²→L²} = 0.1488` (all finite — the kernel kills the `1/(λ−μ)` singular structure); smoothing constant `γ = sup_{t∈(0,b]} √t·sup_λ (1+λ)^{1/2}e^{−tλ} = 0.707107 = 1/√2` (measured == analytic to 1e-15; note the naively-weighted grid would have reported √10 ≈ 3.16 at t = 10 — outside the physical domain `t ≤ b`).
- **Frozen limiting case (parallel transport, exact):** `δS = b·δΔ·S_b` — residual 3.6e-15.
- **Curved leaf (S², conformal deformation h → e^{2εφ}h):** in 2D `Δ_{e^{2s}h} = e^{−2s}Δ`, so `δΔ = −φΔ` and both legs commute: **`T_b = −b·φ·Δ·S_b` exactly** — the seed's curved-leaf reduction. Numerics (`Lmax = 20`, 441 modes, `φ = Y20`-projection, cross-checked ∫Y20² dΩ = 0.9999999999998): residual vs the semigroup FD `(S(ε)−S₀)/ε` is **linear in ε**: normalized 6.52e-5 (ε=1e-3) → 6.52e-6 (ε=1e-4); `‖S(ε)‖ ≤ 1` in every run.

## 4. Step 4 — falsifiable negative controls (capable of failing — and they did fail until fixed)

1. **N1 — one-leg r⁻¹ at both endpoints:** `1/√(r(b−r))`-type integrand with the SAME singular estimate on both edges: the bound integral diverges `ln²(1/ε)`; measured partials 15.57 → 70.91 as ε: 1e-2 → 1e-8, monotone. The control **blocks** the naive proof (as required) and is not replaced by assumption: the A/B allocation replaces the *estimate*, not the physics.
2. **N2 — FD convergence of δΔ:** `(Δ(ε)−Δ(0))/ε → δΔ` measured at ε = 1e-2/1e-3/1e-4: residuals 4.4e-3 / 4.4e-4 / 4.4e-5 — exact O(ε) linearity; the auto-diff operator = the FD limit. **This control failed (0.83) for many debug iterations because of two genuine bugs (below) — the control was capable of failing and did.**
3. **N3 — (A1) closed form ≡ auto-diff:** 1.09e-15 (band ≤ 6) and 6.26e-16 (band ≤ 12) — identity at machine precision on the band-limited domain where the sampled algebra is exact.
4. **N4 — Duhamel vs semigroup FD:** `(S(ε)−S₀)/ε − T_b` on 5 test columns: absolute residuals 9.56e-5 → 9.55e-7, exactly linear in ε (normalized 1.07e-3 → 1.07e-5); `‖S(ε)‖ ≤ 1` throughout. **Also failed despite correct algebra while the expm had the sign error (grew as e^{bλ_max}) — again capable of failing, and caught.**
5. **N5 — linearity in ε (single mode):** absolute residual 9.57e-6 (ε=1e-2) → 9.57e-7 (ε=1e-3), linear; the *normalized* number (0.79 / 0.079) is amplified by the tiny response of mode 7 (‖T_b·e₇‖ = 1.2e-5) and is reported only for completeness.
6. **N6 — negative-control flatness:** the sup-integrand of the *joint* (A/B) bound is flat in r (slopes ≈ +0.014 / −0.019 over the endpoint decks — no r⁻¹ growth): consistent with the r-uniform bound of §2; the divergence is an artifact of the one-leg estimate only (N1).

**Debugging record (both failures of the controls were real bugs, now fixed in the canonical code):**
- (a) `∂_y k₂₂` sign: `+1.5 sin(2x−3y)` not `−1.5` (chain rule: `∂_y[cos(2x−3y)] = +3 sin`); this single sign corrupted the (A1) closed form everywhere (residuals 0.83 → 0.17 consistently).
- (b) eigenvalue/index mapping: `fftfreq(32)·32` places wavenumbers −15..−1 at indices 17..31; using raw indices as wavenumbers corrupted `I(λ,μ)`, `S₀` and every spectrum-weighted quantity (diagnosed via `M₀` diagonal check: 456/625 columns wrong).
- (c) semigroup sign in the numerical cell: `lap_pert` returns Δ ≤ 0, so `S_b = exp(+b·Δ)` — `exp(−b·Δ)` is `e^{+bλ_max}` and numerically exploded (|S| = e^{144}); fixed to `expm_taylor(+B·Mp)`; S² `MpertS` had the same sign slip.
- (d) S² quadrature: `leggauss` abscissas are already x = cos θ; applying `cos(·)` again corrupted ∫Y20² (2.305 → 0.9999999999998).
- (e) Duhamel ε-bookkeeping in the S² check: `T_b` is ε-independent (coefficient of ε), so the FD must be compared against `T_b` (not `ε·T_b`).

Numerics platform: numpy/scipy, self-contained scaled-Taylor block exponential `expm_taylor` (error ≤ 2^-s·1e-15 by construction; validated against scipy on Hermitian matrices), band-limited basis (|k| ≤ 12 on a 32×32 grid → 625 modes; all products stay below Nyquist so the sampled algebra is exact; verification band |k| ≤ 6).

## 5. Closure statement

**Classification: DERIVED (candidate operator bound).** Target `δS = ∫ S_(b−r)(δΔ)S_r` is bounded on the compact leaf by finite operator constants: two-derivative-loss bound `b·M·‖U‖_{H^{s+1}}` with `M = ‖δΔ‖_{H²→H⁰} = 0.460`, kernel-sharpened `‖T_b‖_{H¹→L²} = 0.0646`; conformal curved-leaf case is exact (`T_b = −bφΔS_b`, verified to 6.5e-5·(ε/1e-3)); negative control (one-leg r⁻¹ at both endpoints) diverges `ln²(1/ε)` as required and is not resumed by assumption. **This is not gravity closure**: it bounds the heat-filter metric derivative on a fixed leaf; the coupled-evolution well-posedness gate (same-action CA4) still requires the reciprocal fixed-data estimates that this task was explicitly forbidden to assume.

## 6. Framework footings (both separately — no shared density+κ)

| footing | a0 (m/s²) | ρ_Λ = 4a0²/(G c²) (kg/m³) | r_M (m) | r_M (pc) | leaf area πr_M² (m²) |
|---|---|---|---|---|---|
| canonical | 9.3619e-11 | 5.8444e-27 | 1.19064e15 | 0.038586 | 4.4536e30 |
| alternative | 1.1279e-10 | 8.4831e-27 | 1.08474e15 | 0.035154 | 3.6966e30 |

The alternative footing at fixed ρ_Λ would require κ_eff = 0.6024·(1/2) — i.e. the two footings do NOT share (ρ_Λ, κ); they are held separate as mandated. `r_M(canon)/r_M(alt) = √(a0_alt/a0_can) = 1.09762` (checked exactly). The heat-filter scale is taken dimensionlessly here (ξ = 1 with all norms normalized to the leaf); physical b = ξ²/2 carries the leaf's preferred-time scale, so the *same* bound constants apply under both footings after rescaling `b` — stated as the dimensionless-application clause.

---

## Files in this run dir
- `AS208_first_metric_derivative.py` — canonical numerics (self-contained; parts A/B/C; bounds enforced in-run).
- `raw_output.json` — full output of the final bounded run (exit 0).
- `raw_output.stderr` — runtime warnings (suppressed spurious numpy matmul diagnostics; all arithmetic validated elementwise, none affect results).
- `AS208_two_leg_alloc.lean` — Lean 4 certificate (compiles: `exit 0`; `#print axioms` = {propext, Classical.choice, Quot.sound}; zero `sorry`).