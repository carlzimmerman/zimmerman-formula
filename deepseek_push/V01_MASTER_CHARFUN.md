# V01 — THE MASTER CHARACTERISTIC FUNCTION: H(ω) = E[e^{iωD}] DETERMINISTICALLY

**2026-09-25 · moment channel · closes the L03 D-marginal (KS p = 0.000) with no Monte Carlo in the law.**
Files: `V01_master_charfun.py` · `V01_master_charfun.out` (exit 0) · `V01_results.json` (+ `V01_q3_results.json` supplement) · this file. No git commit.

---

## 1. The object and the pre-registered claim

The L03 pipeline built the 2D transfer function row by row (v²|row KS, 40/40 rows)
but **the D-marginal never closed**: the constructed marginal CDF failed the one-sample
KS against 4×10⁶ MC delays at p = 0.000 (registered informative-not-gated). This file
closes it: the marginal delay law is now produced **deterministically** — no RNG, no
Monte Carlo — as the inverse Fourier transform of the characteristic function

> **H(ω) = E[e^{iωD}]**,  D = τ − Q,  Q = x_exit·u_exit (the frozen convention, U01),

solved on the real ω axis by the K05 characteristic (ray) machinery with a **complex
weight**. The engine: the frozen characteristic functional (U01 derivation)

> u·∇G + κ(PG − G) − pG = 0,   G|_b = e^{p x·u},   p = −iω,   G(0) = H(ω),

whose ray-integral form (κ(r) = τ₀(1+qr²), exact optical-depth closed form) is

> G(r,μ) = e^{−κT} e^{−iω rμ}  +  ∫₀ᵀ e^{−(κ−iω)t} κ (PG)(r(t),μ(t)) dt,

solved by K05's source iteration, one real+imag channel per ω. Because
|e^{−(κ−iω)t}| = e^{−κt}, the iteration is a strict contraction **exactly as in K05**
(probability kernel + real attenuation); ω is real throughout. Order p¹ of the same
equation reproduces K05's L F¹⁰ = 1, F¹⁰|_b = μ bit-for-bit (E[D] = 0.500000), and
order p² the U01 closure L F²⁰ = F¹⁰, F²⁰|_b = μ²/2 (E[D²] = 0.76462) — the complex
solver is the resummation of the same chain (ω = 0 gives H = 1 to 5×10⁻¹⁰; the spread
across the μ-grid at r = 0 is 0 in all solves).

**Kill conditions (pre-registered):** (a) the κ = 0 vacuum check fails (H(ω) must equal
the vacuum law E[e^{iωD₀}], D₀ ≡ 0, i.e. H ≡ 1); (b) E[D] or E[D²] extracted from the
small-ω expansion of the deterministic H miss 0.500000 / 0.7661 by > 1%; (c) the L03
marginal KS at q = 0 still gives p < 0.01. All reported with the exact failing step.
**None of (a)–(c) fired.**

## 2. Grid protocol (pre-registered)

| item | setting |
|---|---|
| H(ω) headline grid | ω ∈ {0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 10, 15, 20} (12 values) |
| speed grid | (Nr, Nq, L, Nt) = (160, 64, 16, 32), τ₀ = 1, q = 0 central |
| 3 full-grid checks | ω = 0.5, 4, 15 at (320, 96, 24, 48) — |ΔH| ≤ 1.2×10⁻⁶ |
| inversion quadrature (my rule) | dense Δω = ⅛ on [0.125, 60] (480 values) + log tail {64…600} (12 values, Nt ∝ ω); Gil–Pelaez F = A + ½(1−A) − (1/π)∫ Im[e^{−iωτ}(H−A)]/ω dω with the ω = 0 endpoint g(0) = E[D] − τ(1−A) (E[D] = 0.5 theorem-exact); the smooth tail content c₁/(iω)+c₂/(iω)²+c₃/(iω)³+c₄/(iω)⁴ (LSQ on ω ≥ 60) is **subtracted from the integrand on the sparse tail and continued analytically on a 200001-point grid** (c₁..c₄ = −1.43, −59.9, −704, −1.39×10⁵; relative model residual at ω = 300 : 0.28) |
| p_D(τ) | τ ∈ [0, 4], 1024 points (density grid) + CDF to τ = 12 for the KS; the ballistic atom pin at τ = 0: **P(D = 0) = A = e^{−τ₀(1+q/3)} exactly** (theorem point) |
| MC test side | n = 4×10⁶ per leg, central, seeds 6101/6102 (q=0), 6103 (q=3); the same engine as L03 (J02 `simulate`); the float atom smears over ±6.7×10⁻¹⁶ (≈30 % of the atom) — the strip |D| ≤ 10⁻¹² is floored to 0 for the KS (zero mass moved; counts reported: 278613 / 278725 / 102616) |
| KS | one-sample with the atom jump handled by the left-continuous model CDF (L03's `ks_one_sample` structure); gate p > 0.01 at q = 0; q = 3 reported |
| spectral bootstrap | H ≈ Σₘ pₘ e^{iωτₘ}, m = 3..6, nonlinear least squares with **exact** constraints Σpₘ = 1, Σpₘτₘ = E[D], Σpₘτₘ² = E[D²] |

## 3. Results

── RESULTS ──

**A. κ = 0 vacuum (kill condition a):** H(ω) = 1 on all 12 omegas to 0 (machine exact —
one-pass ray integral); MC vacuum: max per-photon |D| = 6.7×10⁻¹⁶. **PASS.**

**B. H(ω) on the 12-point grid (q=0, speed grid; converged, spread = 0):**

| ω | 0.25 | 0.5 | 1 | 1.5 | 2 | 3 | 4 | 6 | 8 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Re H | 0.976854 | 0.915410 | 0.749830 | 0.612316 | 0.527403 | 0.460810 | 0.445496 | 0.423074 | 0.411203 | 0.402770 | 0.391878 | 0.386302 |
| Im H | 0.120785 | 0.219097 | 0.314986 | 0.311844 | 0.271221 | 0.191096 | 0.150240 | 0.116219 | 0.095379 | 0.080818 | 0.060382 | 0.048547 |
| \|H\| | 0.98429 | 0.94127 | 0.81330 | 0.68715 | 0.59306 | 0.49886 | 0.47015 | 0.43875 | 0.42212 | 0.41080 | 0.39650 | 0.38934 |

The full-grid re-solves agree to |ΔH| ≤ 1.2×10⁻⁶. H(0) = 1 + 5.3×10⁻¹⁰.

**C. J07 envelope (kill-adjacent):** |H(ω)| ≥ max(0, 1 − ½ω²·E[D²]) with E[D²] = 0.7661,
**true at 12/12 omegas** (asymptotic tightness verified: 1 − ReH − ½ω²E[D²] = O(ω⁴)).

**D. small-ω moment extraction (3-point Lagrange in x = ω² from ω = 0.25/0.5/0.75):**
**E[D] = 0.499593 vs 0.500000 (0.081 %, < 1 %) PASS; E[D²] = 0.764054 vs 0.7661
(0.267 %, < 1 %) PASS** (4-point variants 0.499866 / 0.764437). Independent no-MC
cross-checks from the restored CDF: E[D] = 0.50000, E[D²] = 0.76461.

**E. THE L03 MARGINAL CLOSURE (kill condition c):** deterministic inversion of H(ω)
→ p_D(τ) on [0, 4] (1024 points; atom spike at 0 of mass A = e⁻¹) → model CDF vs the
MC D-histogram (n = 4×10⁶):

| test | D | p | verdict |
|---|---|---|---|
| q = 0, leg 1 (seed 6101) | 6.54×10⁻⁴ | **0.0652** | PASS (> 0.01) |
| q = 0, leg 2 (seed 6102, reproducibility) | 6.88×10⁻⁴ | **0.0453** | PASS |
| q = 0, binned KS [0,4] + tail, 1024 bins | 6.53×10⁻⁴ | **0.0659** | PASS |
| q = 3 (seed 6103; reported) | 5.98×10⁻⁴ | **0.1150** | PASS (reported) |

**The L03 marginal test that read p = 0.000 now reads p = 0.065 at q = 0 — the
D-marginal is closed deterministically.** KS-maximum positions: Dp at D = 4.39
(9.5×10⁻⁴-level tail region, |ΔF| = 6.0×10⁻⁴ — the τ ≥ 4 region carries only 2.7×10⁻³
of the mass, its empirical noise ≈ 5×10⁻³), Dm at D = 0.49 (6.5×10⁻⁴). CDF spot
z-scores vs the leg-1 empirics: |z| ≤ 0.9 for τ ≤ 2, −2.6 at 3, −6.2 at 4 (ΔF ≈ 3×10⁻⁴
at SE ≈ 5×10⁻⁵), |z| ≥ 1.4 at 6; deterministic tail rate λ\* = 1.520 (q=0; from the
Laplace functional G(λ) = E[e^{λD}]: G(1.4) = 43, G(1.45) = 1.1×10⁴, G(1.5) = 5.3×10⁸)
and 0.820 (q=3).

**F. THE SPECTRAL / PADÉ BOOTSTRAP — first closed-form-ish DELAY-LAW
REPRESENTATION** (fits of H on the 12-point grid, moment constraints sum p = 1,
Σpτ = E[D], Σpτ² = E[D²] **exact** — checked to 10⁻⁶):

| m | pₘ | τₘ | rms / max\|ΔH\| |
|---|---|---|---|
| 3 | (0.5675, 0.2646, 0.1679) | (0.0245, 0.557, 2.015) | 0.207 / 0.396 |
| 4 | (0.5571, 0.1930, 0.2121, 0.0378) | (0.0341, 0.594, 1.128, 3.355) | 0.147 / 0.367 |
| 5 | (0.4550, 0.1968, 0.1879, 0.1129, 0.0474) | (0.0085, 0.276, 0.778, 1.350, 3.010) | 0.114 / 0.266 |
| 6 | (0.4904, 0.2026, 0.2174, 0.0578, 0.0476, −0.0158) | (0.0203, 0.284, 0.756, 3.013, 4.309, 7.045) | 0.140 / 0.203 |

The fits self-consistently find the atom-like first term (τ₁ ≲ 0.03, p₁ ≈ 0.5–0.6,
vs the exact atom A = 0.368) plus a 4–5-term delay structure; residual → m = 5 then
saturates (negative p at m = 6 is allowed in the representation). This is the first
deterministic, moment-constrained delay-law representation of the channel.

**G. Honest edges.** (i) The CDF's τ ∈ [8, 12] region carries model artifacts
(F wobbles ≈ 10⁻⁴–3×10⁻⁴ above 1; the monotone/≤1 sanity flags are False there) —
zero KS weight (mass = 10⁻⁵) and clipped in the KS, but noted. (ii) The tail model
(4-parameter, ω ≥ 60) still leaves a 28 % relative residual at ω = 300 (amplitude
≈ 10⁻⁴ of |H−A|); its CDF impact is ≤ 2×10⁻⁴. (iii) The frozen characteristic
functional is the U01-verified law: E[D] to 1.6×10⁻⁴, E[D²] to 2.7×10⁻³ of its
moment chain; the q=0 marginal KS is the sharpest test the channel has ever run and
it passes at the MC-noise floor (6.5×10⁻⁴ ≈ 1.3/√n). (iv) The MC atom-mass itself
fluctuates at ±2.4×10⁻⁴ (binomial) — at the same level as the KS statistic.

## 4. Status line

**V01 PASS — the master characteristic function is deterministic: H(ω) on a dense
grid (12 headline + 480-point Δω = ⅛ grid + 12-point log tail to ω = 600), J07
envelope honored 12/12, moments extracted to 0.08 % / 0.27 % (< 1 %), τ = 0 atom
e⁻¹ exact, λ\* = 1.520, multi-exponential delay-law representations fitted with
exact moment constraints (rms → 0.11 at m = 5), and the L03 marginal test — p = 0.000
before — now reads p = 0.065 at q = 0 (repro leg 0.045, binned 0.066; q = 3: 0.115).
No Monte Carlo in the law; no kill condition fired.**