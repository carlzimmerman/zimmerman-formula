# L01 — THE THIN-OPACITY EXPANSION OF THE CLOSURE RATIO
**2026-09-23 · moment channel (J01/J02/K04 lane) · the joint law Cov(D, ang) at τ₀ → 0**
Files: `L01_closure_expansion.py` (engine: `J02_moment_hierarchy.simulate`, n = 4·10⁶ per point; seeds pre-registered in-script) · `L01_closure_expansion.out` (exit 0 · 72/72 checks) · `L01_results.json` (every number ± SE).

**Bottom line up front.** The premised expansion *does not exist as stated*:

> E[D·ang] = τ₀²·r₁(q) + τ₀³·r₂(q) + …  ✗  (the O(τ₀) term does **not** vanish)
> R − 1 = O(τ₀)  ✗  (R − 1 **diverges** as τ₀⁻¹)

The first-flight + one-collision structure gives, exactly to O(τ₀²) (all coefficients machine-verified, SEs everywhere):

```
E[D·ang] = r1(q)·tau0 + r2(q)·tau0^2 + O(tau0^3),     r1(q) = (7/5)(1/2 + q/4)
E[ang]   = E[N] = (1+q/3) tau0 + c2(q) tau0^2 + O(tau0^3),   c2 = K04(6), analytic
E[D]     = (1/2 + q/4) tau0                               (exact, frozen Theorem 1)

R = E[D·ang]/(E[D] E[ang]) = (7/5)/[(1+q/3) tau0] · (1 + g(q) tau0) + O(tau0),
     g(q) = r2/r1 − c2/(1+q/3)
R − 1 = (7/5)/[(1+q/3) tau0] − 1 + O(1)           [NO O(tau0) expansion of R−1]
Cov(D,ang) = r1(q) tau0 + O(tau0^2),  r1(q) = 0.70 + 0.35 q      (linear in q)
```

The 1/τ₀ prefactor (7/5)/(1+q/3) = 1.40 / 0.70 / 0.323 at q = 0/3/10 matches MC at the deepest points (R = 281.15 ± 2.22 vs 1.4/0.005 at q=0, τ₀=0.005 — i.e. R−1 = 280.15 ± 2.2 vs 279). The **pre-registered kill condition is applied in both directions**: the premised form (no τ₀ term in E[D·ang]) is killed at 341–1078 SE; the corrected r₁(q) = (7/5)(1/2+q/4) passes its own 5-SE gate (z = 0.47/0.59/0.03).

---

## 1. Why the premise fails: the sector structure of the joint law

**Telescoping lemma (any source, exact).** D = L − (x_f − x₀)·u_f with L the total path length telescopes segment by segment:

```
D = Σ_{j=1}^N s_j (1 − u_j·u_f),   N = collisions, u_f = final direction.
```

- N = 0: (D, ang) = (0, 0) — the atom spike has *zero lag and zero width*, and contributes **nothing** to E[D·ang].
- N = 1: D = s₁(1−μ), ang = (1−μ) (T = 1), s₁ ⊥ μ (first flight radial, Thomson μ local), so D·ang = s₁(1−μ)².
- N ≥ 2: P = O(τ₀²) and contributes at O(τ₀²) to E[D·ang].

**Consequence.** E[D·ang] = P(N=1)·E[s₁(1−μ)²|N=1]·(1+O(τ₀)) = **O(τ₀)**, not O(τ₀²): the one-collision photon carries a finite angular-mean coupling s₁·E[(1−μ)²] per unit τ₀. Meanwhile E[D]·E[ang] = O(τ₀)·O(τ₀) = O(τ₀²). The covariance therefore does **not** start at second order in τ₀ — hence the ratio diverges and the "second-order" closure-expansion premise is void. *The only way the premise could hold is E[(1−μ)²] = E[1−μ]² = 1; the Thomson kernel gives 7/5.*

**The leading coefficient (exact, from the N=1 sector):**

```
r1(q) = ∫₀¹ s κ̃(s) ds · E[(1−μ)²],   κ̃ = 1+qs²,   E[(1−μ)²] = 7/5
      = (1/2 + q/4)·(7/5).
```

(The N=1 sector is computed **exactly in τ₀** — the full integrand κ(s₁)e^{−Λ₁−Λ₂}(1−μ)ᵐp(μ), m = 0,1,2, with both flight optical depths and the exact wall distance s₂ = −s₁μ+√(s₁²μ²+1−s₁²) — and verified against MC with masks per collision number, §3.)

**Second order.** r₂⁽¹⁾ (N=1 sector alone, from e^{−Λ} → 1−Λ) = −1.3223 / −7.3589 / −40.8341 at q = 0/3/10 — *negative* (backward-scattered photons escape through a longer Λ₂). The **measured total** r₂ = +0.886 ± 0.031 / +4.64 ± 0.22 / +26.5 ± 1.2 — *positive and N≥2-dominated*: the two-collision sector's D·ang growth (∝ s₁(1−μ₁)(1−μ₁...)+s₂(1−μ₂)…) exceeds the escape suppression. So E[D·ang] = r₁τ₀ + r₂τ₀² with r₂ measurable but not first-flight-analytic (N≥2 enters at exactly this order — "contributions vanish at second order" is false for E[D·ang]; it *is* true for E[D] in the stronger form E[D] = ∫rκ dr exactly).

---

## 2. Term-by-term measurement (n = 4·10⁶ per point; SEs quoted)

### 2a. E[D] (exact identity, no expansion needed)

| τ₀ | q=0 E[D] (±SE) | q=3 | q=10 | z_max |
|---|---|---|---|---|
| 0.02 | 0.009964 ± 4.8e-5 | 0.025041 ± 8.1e-5 | 0.060001 ± 1.3e-4 | 0.75 |
| 0.05 | 0.024983 ± 7.6e-5 | 0.062229 ± 1.3e-4 | 0.150158 ± 2.1e-4 | 2.12 |
| 0.1 | 0.049894 ± 1.1e-4 | 0.124820 ± 1.8e-4 | 0.299278 ± 3.0e-4 | 2.45 |
| 0.2 | 0.099957 ± 1.5e-4 | 0.249576 ± 2.6e-4 | 0.600217 ± 4.4e-4 | 1.62 |

vs τ₀(1/2+q/4): |z| ≤ 2.45 everywhere. ✓ (exact at all orders, again)

### 2b. E[ang] = E[N] = τ₀(1+q/3) + c₂(q)τ₀² + O(τ₀³), c₂ analytic (K04)

Weighted quadratic fit of E[ang]/τ₀ over 10-11 depths per q (τ₀ = 0.002…0.3):

| q | (1+q/3) fit ± SE (an) | c₂ fit ± SE | c₂ analytic (K04(6)) | z |
|---|---|---|---|---|
| 0 | 1.0017 ± 0.0030 (1.0000) | +0.3593 ± 0.0413 | 0.38145656 | 0.54 |
| 3 | 2.0043 ± 0.0076 (2.0000) | +1.9397 ± 0.1733 | 2.06895656 | 0.75 |
| 10 | 4.3278 ± 0.0130 (4.3333) | +11.7907 ± 0.3223 | 11.78957221 | 0.00 |

Per-point two-term z ≤ 4.2 at all grid depths except (τ₀=0.2, q=10) where the O(τ₀³) curvature (c₃·τ₀³ ≈ +5.6·0.008) legitimately breaks the two-term law (z=43.6) — the fit-based test is the registration. E[ang] = E[N] identity: |z| ≤ 0.54 at all 12 grid points. ✓

### 2c. E[D·ang] = r₁τ₀ + r₂τ₀² + O(τ₀³)

**The kill condition, squarely applied.** Weighted quadratic fit of E[D·ang]/τ₀ (11 depths per q, τ₀ = 0.002…0.5):

| q | r₁ fit ± SE | r₁ = (7/5)(1/2+q/4) | z | r₂ fit ± SE | χ² |
|---|---|---|---|---|---|
| 0 | 0.6982 ± 0.0038 | 0.7000 | **0.47** | +0.886 ± 0.031 | 11.4 |
| 3 | 1.7550 ± 0.0085 | 1.7500 | **0.59** | +4.636 ± 0.221 | 6.6 |
| 10 | 4.1989 ± 0.0379 | 4.2000 | **0.03** | +26.51 ± 1.21 | 16.8 |

✓ derived r₁ verified within 5 SE at all q. **Premised r₁ ≡ 0 (the τ₀²-form):** E[D·ang]/SE at the deepest points = z ≈ +0.5 (probe τ₀=0.002,q=0) is the *largest* it gets: at τ₀=0.005–0.02 the premised form misses by 6–480 SE and by **341–1078 SE in R−1** (§2e). Premise killed.

Single-term (r₁τ₀ only) agreement at the deepest probes: q=0: z=+1.33 (τ₀=0.002), +2.95 (0.005); q=3: −0.38, +3.73; q=10: +1.52 (τ₀=0.002; at 0.005 z=9.1 — the r₂τ₀² curvature is already 9 SE there, as the fit says r₂(10) ≈ +26.5).

### 2d. The N=1 sector, exact quadrature vs MC-with-masks (all orders in τ₀)

| (τ₀,q) | P(N=1) z | E[D·𝟙{N=1}] z | E[D·ang·𝟙{N=1}] z | N≥2 share of E[D·ang] |
|---|---|---|---|---|
| (0.02, 0) | −0.66 | −0.73 | −0.64 | 0.00092 |
| (0.02, 3) | −0.44 | −2.30 | −2.75 | 0.00471 |
| (0.02, 10) | +0.53 | +0.06 | −0.26 | 0.02637 |
| (0.05, 0) | −0.04 | −0.33 | −0.31 | 0.00530 |
| (0.05, 3) | +0.55 | −0.25 | −0.31 | 0.02869 |
| (0.05, 10) | +0.91 | +0.31 | +0.28 | 0.15473 |

The first-flight + one-collision integrand **is** the P(N=1) law and the (D, ang) joint law on that sector, exact in τ₀ (|z| ≤ 2.8). At (0.05, q=10) the N≥2 sector carries 15% of E[D·ang] — the sector that makes r₂ positive and that no two-moment marginal can close.

### 2e. The closure ratio itself

| τ₀ | R(q=0) ± SE | R(q=3) | R(q=10) | (7/5)/[(1+q/3)τ₀] leading |
|---|---|---|---|---|
| 0.002 | 694.5 ± 5.5 | 353.0 ± 2.8 | 162.7 ± 0.5 | 700 / 350 / 162 |
| 0.005 | 281.15 ± 2.22 | 140.24 ± 0.70 | 66.05 ± 0.23 | 280 / 140 / 64.6 |
| 0.01 | 140.04 ± 0.69 | 70.88 ± 0.16 | 33.45 ± 0.11 | 140 / 70 / 32.3 |
| 0.02 | 71.13 ± 0.25 | 36.25 ± 0.15 | 17.39 ± 0.03 | 70 / 35 / 16.2 |
| 0.05 | 29.18 ± 0.10 | 15.26 ± 0.03 | 7.70 ± 0.01 | 28 / 14 / 6.5 |
| 0.1 | 15.20 ± 0.03 | 8.24 ± 0.01 | 4.48 ± 0.001 | 14 / 7 / 3.2 |
| 0.2 | 8.21 ± 0.01 | 4.76 ± 0.003 | 2.90 ± 0.002 | 7 / 3.5 / 1.6 |

**Premised form R−1 = C·τ₀:** weighted-fit residuals |z| = **341 / 489 / 1078** (q = 0/3/10) — killed at every sampled depth (5-SE gate), i.e. the expansion "breaks" already at τ₀ = 0.02, the shallowest sampled depth. The **derived leading law** R·τ₀(1+q/3)·(5/7) → 1 + g(q)τ₀ (g from the r₂/c₂ fits: 0.88/1.61/3.59): measured 1.0018-target within |z| ≤ 3.2 at τ₀ = 0.002 and 0.005 for all q (§3c of `.out`; e.g. q=10, τ₀=0.005: 1.0183 ± 0.0013 vs 1.0180). ✓

---

## 3. Q-dependence of the leading coefficient of Cov(D, ang)

Cov(D,ang) = E[D·ang] − E[D]·E[ang] = **r₁(q)·τ₀** + O(τ₀²), with

```
r1(q) = (7/5)(1/2 + q/4) = 0.70 + 0.35q      (linear in q: slope 7/20, intercept 7/10)
```

verified at q ∈ {0, 3, 10} (fit z = 0.47/0.59/0.03). The higher-order piece of Cov is O(τ₀²) with coefficient r₂ − (1/2+q/4)(1+q/3) (measured r₂ above).

## 4. Break depths (first sampled depth with |residual| > 5 SE)

| law | q=0 | q=3 | q=10 |
|---|---|---|---|
| leading law r₁τ₀ for E[D·ang] | valid τ₀ < 0.05 (breaks at 0.05) | valid τ₀ < 0.02 (breaks at 0.02) | valid τ₀ < 0.02 (breaks at 0.02) |
| two-term r₁τ₀ + r₂τ₀² | valid through τ₀ = 0.2 | valid τ₀ < 0.1 | valid τ₀ < 0.05 |
| **premised R = 1 + τ₀C** | **breaks at τ₀ = 0.02 (smallest sampled)** | same | same |

The premised expansion is dead on arrival — its residual is 10²–10³ × its own 5-SE gate at *every* sampled depth; the correct leading law for R−1 = (7/5)/[(1+q/3)τ₀] − 1 + O(1) is validated at τ₀ ≤ 0.005–0.01 and the two-term E[D·ang] law through τ₀ ≈ 0.05–0.2 depending on q.

## 5. Corollary — the volume face (closes in closed form)

D telescopes identically for the volume source (D = Σ sⱼ(1−uⱼ·u_f); the source position cancels), so E[D]_vol = P(N=1)·E[s₁|N=1] + O(τ₀²):

```
E[D]_vol = A_v(q)·tau0 + O(tau0^2),   A_v(q) = 2/5 + (8/35) q
```

closed form (the q=0 part: E[s_w²]/2 with s_w the wall distance under the volume-uniform × isotropic measure; mean <s_w²> = 4/5 because the μ-odd chord terms drop). Verified: single-term z at τ₀=0.002: **+1.02 / +0.78 / +0.45** (q=0/3/10); intercept fit over six depths: A_fit = 0.4030±0.0032 / 1.0915±0.0028 / 2.6976±0.0031 vs 0.4 / 1.0857 / 2.6857 (z = 0.94 / 2.06 / 3.78). Companion thin law for the observed exposure: E[ang]_vol = τ₀·⟨Λ_wall⟩ + O(τ₀²), ⟨Λ_wall⟩ = 3/4, 2, 59/12 at q = 0/3/10 (verified at τ₀ = 0.002, z ≤ 1.7). (At τ₀ = 1, q = 0 the J02 volume value E[D]_vol = 0.3375 ± 0.0006 sits below the thin-law line A_v = 0.4 — the O(τ₀²) curvature b_fit ≈ −0.1…−2.5 is negative, as the fit shows.)

## 6. Kill-condition ruling and honest edges

- **Premised derivation (E[D·ang] ≈ τ₀²·r₁, R−1 = O(τ₀)): KILLED** — leading-coefficient mismatch 341–1078 SE (≫ 5 SE pre-registered limit) at every sampled depth; the "second-order" expansion of R does not exist. The reason is structural: the N=1 sector couples D to (1−μ)² at unit order in τ₀ (E[(1−μ)²] = 7/5 > E[1−μ]² = 1).
- **Corrected derivation (r₁(q) = (7/5)(1/2+q/4); R−1 = (7/5)/[(1+q/3)τ₀] − 1 + O(1); Cov leading 0.7+0.35q; E[D]_vol = (2/5 + 8q/35)τ₀): SURVIVES ITS OWN 5-SE GATE (72/72 checks).**
- Honest edges: r₂ (and g) are measured, not derived (N≥2 sector enters at that order); no git commit; append-only (J01–K04 untouched); all numbers are MC ± SE, the analytic claims are the squared-cosine constant 7/5, the telescoping lemma, the exact N=1 integrand, and the two wall-moment identities — no asymptotic machinery beyond the sector ordering P(N≥2) = O(τ₀²).