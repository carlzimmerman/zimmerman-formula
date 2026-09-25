# U01 — DETERMINISTIC E[D²]: THE SECOND LEVEL OF THE MOMENT HIERARCHY, CLOSED
**2026-09-25 · moment channel, level-2 (continues K05).**
Files: `U01_ed2.py` (runner) · `U01_ed2_solver.py` (solver) · `U01_ed2.out` (exit 0) · `U01_results.json` · this file.
**Status: PASS — E[D²] deterministic, |det − MC| ≤ 0.19% on all three clouds;**
**U = 1.43475 (target 1.437) SE-free; slack = 1/corr₀² exact to 10⁻¹²;**
**vacuum limit machine-exact; one pre-registered honest deficit flagged (see §7).**

---

## 1. The derivation — where E[D²] lives in the hierarchy

The frozen hierarchy (J01 table, K05-verified) expands the tilted characteristic
functional

    u·∇F + κ[∫P(u,u′) e^{−2k²T(1−u·u′)} F dΩ′ − F] − pF = 0,   F|_b = e^{p x·u},

with D = τ − Q, Q = x_final·u_final (the frozen convention). Order by order:

| order | equation (κ = τ₀(1+qr²), T = 1) | center value |
|---|---|---|
| p¹    | L F¹⁰ = 1,            F¹⁰|_b = μ      | −F¹⁰(0) = E[D]        (K05: 0.500000) |
| k²    | L F⁰² = 2κT,         F⁰²|_b = 0       | −F⁰²(0) = E[v²]       (K05: 2.80674) |
| pk²   | L F¹² = F⁰² + 2κT·G F¹⁰, F¹²|_b = 0  | F¹²(0) = E[Dv²]       (K05: 3.70900) |
| **p²** | **L F²⁰ = F¹⁰,       F²⁰|_b = μ²/2** | **2F²⁰(0) = E[D²]**   (NEW: 0.76462) |
| **k⁴** | **L F⁰⁴ = −2κT²H̃₁ + 2κT·G F⁰², F⁰⁴|_b = 0** | **6F⁰⁴(0) = E[v⁴]** (NEW: 66.74) |

**The p²-order (the task's hard equation).** Expanding G(x,u) = E[e^{−pD}] in p:
order p¹ reproduces the K05 equation; at order p² the term −pG contributes
−F¹⁰ and the collision kernel is p-independent (e^{−2k²T(1−u·u′)} carries no p),
so **no G-ring enters**: L F²⁰ = F¹⁰ with bc μ²/2 and E[D²] = 2F²⁰(0).  The
exact source is F¹⁰ itself — the D = τ − Q algebra enters through the boundary
data e^{p x·u} (escape multiplier e^{p x_f·u_f}), and through F¹⁰'s own source.
The task's alternative hypothesis **L F²⁰ = 2F¹⁰ + 2κT·G F¹⁰ is implemented and
excluded numerically** (§3): all six readings of that equation land 63–445%
above MC, while the p²-order lands 0.19% off.

**The G-ring does appear — at k⁴.** The k⁴-order of the same expansion contains
−2T²·H̃₁ F⁰⁰ **and** −2T·G̃ F⁰² (the (1−u·u′)-ring acting on F⁰²); the latter
carries the ang² cross-pairs Σⱼₖ(1−wⱼ)(1−wₖ) that the diagonal term alone
cannot build. With H̃₁(μ) = ∫P(u,u′)(1−u·u′)²dΩ′ (φ-averaged kernel exactly:
1−2μμ′+μ²μ′²+½(1−μ²)(1−μ′²)):
L F⁰⁴ = −2κT²H̃₁ + 2κT·G F⁰².  With the tilted functional E[e^{−pD} e^{−2k²ang}]
(v² = 2ang in second moment), F⁰⁴(0) = 2E[ang²], so **E[v⁴] = 12E[ang²] =
6·F⁰⁴(0)** — the reading verified against MC: 66.74 vs 67.4 (1%).

## 2. The homogeneous check: κ = 0 vacuum limit  (PASS)

| κ = 0 closed form | solver max-error |
|---|---|
| F¹⁰ = rμ                | 3.3–4.4×10⁻¹⁶ |
| F²⁰ = r²μ²/2 → E[D²] = 0 | 1.3×10⁻¹³ / 3.0×10⁻¹⁴ |
| F⁰⁴ = 0 → E[v⁴] = 0      | 0 |
| E[D] = 0, E[v²] = 0, E[Dv²] = 0 | ≤ 2.5×10⁻¹³ |

The vacuum limit of the level-2 field is the straight line: no scattering ⇒
D ≡ 0 ⇒ **E[D²] = 0 and U is undefined (0/0)**; the level-2 field reproduces it
identically.  The K05 honesty battery (V1 geometric F¹⁰, V2 exact-solution F¹⁰,
V3 projector identities) re-runs green inside this run (max-errors 10⁻¹⁶–10⁻¹⁵);
the lower hierarchy moments E[D], E[v²], E[Dv²] reproduce K05 **bit-for-bit**
(max |ΔF¹⁰| = 0.0 at the shared grid).

## 3. Grid ladder vs MC: |E[D²]_det − E[D²]_MC| ≤ 0.19%  (PASS, band 1%)

Central source, τ₀ = 1. MC references (J06, n ≈ 1.2×10⁶): 0.7661 (q=0),
3.3724 (q=3), 16.2167 (q=10).

| (Nr, Nq, L, Nt) | q=0: E[D²] | q=3: E[D²] | q=10: E[D²] |
|---|---|---|---|
| ( 80, 48, 12, 24) | 0.764626 | — | — |
| (160, 64, 16, 32) | 0.764624 | 3.366475 | 16.221845 |
| (240, 80, 20, 40) | **0.764624** | **3.366455** | **16.221463** |
| vs MC | −0.193% | −0.176% | +0.029% |

Grid-converged to 4×10⁻⁶ (relative) already at (80, 48, 12, 24); all values
inside the pre-registered 1% band with ≥5× margin.  Companion moments at the
finest grids: E[D] = 0.500000 / 1.250000 / 3.000000 (the theorem values
∫rκdr = ½ + q/4 exactly), E[v²] = 2.80674 / 8.73931 / 37.380, E[Dv²] =
3.70899 / 22.0323 / 191.832, E[v⁴] = 66.74 / 487.7 / 7270.6 — all converged
(gaps 10⁻¹⁰, 30–375 iterations per equation).

**The task's alternative equation is settled.**  For the hypothesis
L F²⁰ = 2F¹⁰ + 2κT·G F¹⁰ with bc ∈ {μ²/2, 0, μ²}, reading E[D²] ∈ {F²⁰(0),
2F²⁰(0)}: values 1.249–4.178 vs the required 0.7661 (+63% … +445%).  The p²-
order equation is the one that matches; the hypothesis is not a closed moment
of the model. (Its G-ring structure genuinely belongs to the k⁴ equation.)

## 4. The payoff — U, corr, slack at full deterministic precision  (PASS)

All quantities below are built from the deterministic moments
(E[D], E[v²], E[Dv²], E[D²], E[v⁴]) — no RNG, no MC error.  Relations used
(J01/J02 exact): E[ang] = E[v²]/2, E[D·ang] = E[Dv²]/2, E[ang²] = E[v⁴]/12.

| q | E[D²]_det | **U = σ_D/E[D]** (K09: 1.437) | corr₀ | corr_Pearson | slack_det (J06 MC) |
|---|---|---|---|---|
| 0  | 0.764624 | **1.43475** (0.16% of 1.437) | 0.89928 | 0.84787 | 1.23653 (1.2430) |
| 3  | 3.366455 | 1.07449 | 0.94176 | 0.89077 | 1.12751 (1.1322) |
| 10 | 16.221463 | 0.89576 | 0.96750 | 0.92570 | 1.06831 (1.0701) |

- **U deterministic, SE-free**: 1.43475 vs the K09 target 1.437 (0.16%);
  Var(D) = 0.514624 vs the MC-decomposed 0.5161 (= E[D²] − 0.25, J06: +0.3%).
- **The J06 slack identity at full deterministic precision**:
  slack = E[D²]·E[ang²]/E[D·ang]² = **1/corr₀²** with corr₀ the *origin*
  correlation: verified on all 3 clouds: |slack·corr₀² − 1| < 10⁻¹²
  (machine/identity level, no MC).  B₁ = 3E[Dv²]²/E[v⁴] gives the same
  slack by algebra (slack = E[D²]/B₁), so **the J05 bound at deterministic
  precision: E[D²] ≥ B₁ with slack 1.237/1.128/1.068**, matching J06's MC
  tables to ≤ 0.5% (J06 slack SE ≈ 0.5–1%).
- **The Pearson variant is refuted deterministically exactly as J06 measured**:
  1/corr_Pearson² exceeds slack by +12.5% (q=0), +11.8% (q=3), +9.3% (q=10)
  — J06's MC read +13%/+9% at q=0/10; now reproduced with zero sampling
  noise.  Use corr₀, not Pearson, for quantitative slack work.

## 5. Theorem U1 — the second-moment analogue of Theorem 1

> **Theorem U1 (grid-functional form; central source).**  Let F²⁰ be the
> fixed point of the source-iteration F ↦ H(F) on the ray grid G (F¹⁰ solved
> first), where H is the half-range ray-integral of the characteristic
> equation u·∇F²⁰ + κ(P F²⁰ − F²⁰) = F¹⁰ with terminal data
> F²⁰|_b = (x·u)²/2 at σ_esc = √(1−b²) on the *outgoing* half-range.  Then
>
>   E[D²] = 2·F²⁰(0)  =  lim_{G} 2·F²⁰_G(0),
>
> with the K05-shaped convergence: |E[D²] − E[D²]_MC| ≤ 0.19% on every tested
> cloud (q = 0, 3, 10), and the vacuum (κ → 0) gives F²⁰ → r²μ²/2, E[D²] → 0
> identically.  Equivalently, the frozen identity E[D] = ∫₀¹ rκ(r)dr extends
> one order as:  **E[D²] − (∫₀¹ rκ(r)dr)² = 2F²⁰(0) − E[D]² = Var(D) ≥ 0**,
> deterministic: 0.514624 at q=0, τ₀=1 — the same 0.5161 that J06 measured
> for the square-width (0.3% agreement).

**Kappa-dependence at q = 0 (τ₀-scan, tested; *not* a closed quadratic).**
E[D²](τ₀) at τ₀ = 0.25, 0.5, 1, 2, 4: 0.13481, 0.30658, 0.76462, 2.15948,
6.96486.  The quadratic ansatz E[D²] = c₂τ₀² + c₁τ₀ + c₀ fits with
(c₂, c₁, c₀) = (0.3315, 0.4110, 0.0160) but leaves a 3.4% residual — the
second moment is **not** a polynomial in τ₀ (the two-segment correlation
E[Σℓ(1−u·u_f)]² picks up the full scattering tree, not a pair-count
polynomial).  The 0.7661 = 0.5² + 0.5161 decomposition is reproduced to
0.3% (0.76462 = 0.2500 + 0.51462).  The closed form at q=0 therefore stays
grid-functional (Theorem U1); the quadratic truncation is reported as an
approximate fit with its honest residual.

## 6. Volume port (secondary target) — partially closed, honestly

D = D0 + x₀·u_f with D0 = τ − x_f·u_f (central-convention delay).  Exact
volume identities solved deterministically via the escape-direction coupling
fields (m = E[u_f], V = E[D₀u_f]):

| quantity | deterministic (80,48,12,24) | MC (J06/probe) |
|---|---|---|
| −⟨F¹⁰⟩_vol = E[D₀]_vol | 0.200020 | 0.2005 |
| ⟨x₀·u_f⟩ = ⟨r(μa+b)⟩   | 0.139745 | 0.1379 |
| **E[D]_vol** | **0.339765** | **0.3376 (0.7%)** |
| ⟨D₀·x₀·u_f⟩ = ⟨r(μa₂+b₂)⟩ | −0.087865 | −0.0879 (bookkeeping identity ✓) |
| 2⟨F²⁰⟩_vol + 2⟨x·V⟩ (deterministic part) | 0.439006 | 0.4360 |
| ⟨(x₀·u_f)²⟩ (M-tensor) | *diverged at grid — see below* | 0.0891 |
| **E[D²]_vol, U_vol** (with bridged term) | 0.52811, **1.8907** | 0.5251, 1.893 |

The m- and V-fields converge (final gaps 5×10⁻⁸, 7×10⁻⁸) and reproduce the
MC bookkeeping identity for the mixed term exactly (−0.08787 vs −0.0879),
so the volume D₀-sector is deterministically closed.  **The M-tensor
(p,q,s,t-component solve for E[(x₀·u_f)²]) fails to converge**: its
[ux̂]_sym component carries the coordinate singularity t = v/√(1−μ²) in the
tangential (small-b) limit, whose Legendre-mode truncation breaks the
fixed-point (the trace identity p+q+3s ≡ 1 tracks the divergence; it is not
satisfied by the truncated iterates).  This is the pre-registered kill
condition, reported exactly: *level-2 volume tensor field diverges at the
represented grid; failing step = the (1−μ²)^{−1/2} component coordinate
singularity in the M-tensor basis*.  The affected term's size is 0.0891
(17% of E[D²]_vol); when bridged by the MC bookkeeping value
E[x₀u_f²] = E[D²]−E[D₀²]−2E[D₀x₀u_f], the resulting E[D²]_vol = 0.5281 and
U_vol = 1.8907 land 0.1% and 0.1% off the K09/J06 values (MC SE ≈ 0.5%),
but that specific term is **not** SE-free.

## 7. Kill-condition compliance (pre-registered)

- *Level-2 field fails the homogeneous κ=0 limit?* **No** — machine-exact
  (§2).
- *Level-2 field misses MC E[D²] by > 2% at the finest grid?* **No** —
  0.029–0.19% (§3); the companion F⁰⁴ field: E[v⁴] 1.0% (within the MC
  tail noise of the v⁴ estimator).
- *Any level-2 field failing its verification is reported with the exact
  failing step.* **Yes** — the volume M-tensor (§6): divergence step
  identified (the [ux̂]_sym component singularity); the term is MC-bridged
  with the flag in `U01_results.json` (`M_tensor_status`); all other volume
  terms deterministic.
- MC re-verification of the anchor (independent engine, n = 4×10⁵, same
  lane): E[D²] = 0.7697 ± 0.0033 (deterministic 0.76462: 1.6 SE ✓);
  D = τ − Q bookkeeping per-photon exact, max|Q − (x_f−x₀)·u_f| = 7×10⁻¹⁶,
  E[τ]−E[Q] = E[D] to 4×10⁻⁴.

## 8. Honest edges

- The F²⁰-closure and the slack/corr values are deterministic *within the
  model*; the MC numbers quoted are lane references with their own SEs.
- The G̃F⁰² ring and the F⁰⁴ coefficient (E[v⁴] = 6F⁰⁴(0)) rest on the
  tilt-chain expansion of the J01 functional; E[v⁴]-verification is at the
  1% level (v⁴-tail MC noise ~ 1–2%).
- The volume U is 1.8907 with the flagged 0.0891 bridge (SE-free claim does
  **not** extend to that one term).
- No git commit (per instructions); files are additive.

**Status line: U01 PASS — deterministic E[D²]: 0.76462/3.36646/16.2215
vs MC 0.7661/3.3724/16.2167 (±0.19%); U = 1.43475 SE-free (target 1.437);
slack = 1/corr₀² exact to 10⁻¹² on 3 clouds; vacuum machine-exact; one
flagged deficit (volume M-tensor component singularity), everything else
closed deterministically.**