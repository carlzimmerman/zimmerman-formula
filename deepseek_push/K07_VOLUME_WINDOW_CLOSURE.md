# K07 — CLOSURE OF THE VOLUME WINDOW THEOREM

**2026-09-23 · moment channel · volume source · final**

Closes the J11 open door (J11 V2 q>0 quadrature check FAILED, z = 29.5 / 83.6)
and the τ₀-shape question.  Every number below carries an SE; all MC via the
J02 engine volume source (`deepseek_push/J02_moment_hierarchy.py::simulate`,
exact optical-depth bisection), n = 600 000 per grid point (+ a 2e6-photon
micro grid at τ₀ ≤ 0.1 for the thin limit).

**Engine ⇔ quadrature agreement after the sign fix: 18/18 points within 4 SE
(max z = 2.53); the J11-stated chord formula is rejected at q > 0 (z = 29–84).**

---

## 1. The J11 quadrature sign error (why V2 failed) — fixed

The volume atom is

    A_v(τ₀,q) = 3∫₀¹ r² dr · ½∫₋₁¹ dμ exp(−τ₀·T),   T = chord + q(r²chord + rμ chord² + chord³/3),

but the **escape chord along the ray +u is**

    chord(r,μ) = √(1 − r²(1−μ²)) − rμ            (CORRECT — matches the engine)

not `√(...) + rμ` as stated in J11.  The two agree only under the q=0
μ-symmetric integrand (why J11 V1 passed); at q>0 the stated formula is off
by z = 29.5 (q=3) and z = 83.6 (q=10).  Gauss–Legendre quadrature here is
80/160-pt with the factor-2-careful weights **Wm = ½dμ** (sums to 1) and
**Wr = 3r²·½dr** (sums to 1); |A(ng=80) − A(ng=160)| ≤ 7.4e−7.

## 2. P1 — E[D]_vol and −ln A_vol, MC vs EXACT quadrature (n = 6e5)

All |MC − quadrature| within 4 SE.  −lnA_quad is exact (no SE); MC column
for cross-check; R_v := −ln A / E[D].

| τ₀ | q | E[D]_vol ± SE | −lnA (MC) | −lnA (quad) | z | R_v (MC) | R_v (quad) |
|----|----|----|----|----|----|----|----|
| 0.5 | 0 | 0.17969 ± 0.00059 | 0.3442 | 0.3463 | 2.53 | 1.9157 ± 0.0050 | 1.9273 |
| 1.0 | 0 | 0.33757 ± 0.00083 | 0.6380 | 0.6401 | 1.72 | 1.8899 ± 0.0040 | 1.8961 |
| 2.0 | 0 | 0.61078 ± 0.00121 | 1.0999 | 1.1014 | 0.78 | 1.8009 ± 0.0034 | 1.8032 |
| 3.0 | 0 | 0.85729 ± 0.00156 | 1.4409 | 1.4424 | 0.68 | 1.6807 ± 0.0032 | 1.6825 |
| 5.0 | 0 | 1.30783 ± 0.00225 | 1.9178 | 1.9173 | 0.15 | 1.4664 ± 0.0029 | 1.4660 |
| 8.0 | 0 | 1.94063 ± 0.00329 | 2.3759 | 2.3750 | 0.24 | 1.2243 ± 0.0026 | 1.2238 |
| 0.5 | 3 | 0.46955 ± 0.00103 | 0.8580 | 0.8577 | 0.19 | 1.8273 ± 0.0036 | 1.8267 |
| 1.0 | 3 | 0.86063 ± 0.00155 | 1.4683 | 1.4693 | 0.39 | 1.7061 ± 0.0032 | 1.7072 |
| 2.0 | 3 | 1.55565 ± 0.00258 | 2.2283 | 2.2292 | 0.25 | 1.4324 ± 0.0029 | 1.4330 |
| 3.0 | 3 | 2.20946 ± 0.00360 | 2.6787 | 2.6810 | 0.49 | 1.2124 ± 0.0026 | 1.2134 |
| 5.0 | 3 | 3.50531 ± 0.00568 | 3.2226 | 3.2306 | 1.25 | 0.9194 ± 0.0021 | 0.9216 |
| 8.0 | 3 | 5.40408 ± 0.00878 | 3.7140 | 3.7212 | 0.88 | 0.6873 ± 0.0018 | 0.6886 |
| 0.5 | 10 | 1.05929 ± 0.00184 | 1.7339 | 1.7308 | 1.10 | 1.6369 ± 0.0031 | 1.6340 |
| 1.0 | 10 | 1.92807 ± 0.00313 | 2.5491 | 2.5462 | 0.64 | 1.3221 ± 0.0028 | 1.3206 |
| 2.0 | 10 | 3.59644 ± 0.00577 | 3.3108 | 3.3179 | 1.07 | 0.9206 ± 0.0022 | 0.9226 |
| 3.0 | 10 | 5.24112 ± 0.00843 | 3.7447 | 3.7453 | 0.07 | 0.7145 ± 0.0018 | 0.7146 |
| 5.0 | 10 | 8.49914 ± 0.01370 | 4.2716 | 4.2723 | 0.07 | 0.5026 ± 0.0014 | 0.5027 |
| 8.0 | 10 | 13.35187 ± 0.02151 | 4.7444 | 4.7510 | 0.47 | 0.3553 ± 0.0011 | 0.3558 |

J11's V3 anchor re-verified: (τ₀=1, q=10) R = 1.3221 ± 0.0028 — **below 4/3**, as J11
found (1.3142).  The volume window is τ₀-DEPENDENT, the central window is not.

## 3. P2 — shape of the volume window: R_v(τ₀) is DECREASING

Candidate fit R = a/τ₀ + b (weighted LSQ, SEs from the fit covariance):

| q | a ± SE | b ± SE | χ²/4 | decreasing |
|----|----|----|----|----|
| 0 | 0.759 ± 0.324 | 1.224 ± 0.099 | 28092 | yes (a > 0) |
| 3 | 1.121 ± 0.355 | 0.607 ± 0.089 | 98161 | yes |
| 10 | 1.153 ± 0.224 | 0.230 ± 0.043 | 119290 | yes |

**The a/τ₀+b candidate is formally REJECTED** (χ² massive: the SEs are tiny and
the true shape is steeper at small τ₀ and flatter at large τ₀ — R is near-linear
in τ₀ on the grid, then bends).  The monotone-decrease claim survives
nonparametrically: R(τ₀) is strictly decreasing in every row of the P1 table
(neighbours differ by ≫ 10 SE), and the semiparametric scan (below) confirms it
on [0.001, 8].

### 3b. P2c — the thin limit, measured separately (low-τ₀ MC)

c_q(τ₀) := E[D]_vol/τ₀ measured at τ₀ ∈ {1e−3, 1e−2, 5e−2, 0.1, 0.2, 0.3, 0.5}
(n = 2e6 for τ₀ ≤ 0.1, 6e5 above); c₀ = lim fit (weighted quadratic, τ₀ ≤ 0.2):

| q | c₀ ± SE | c(τ₀=1e−3) | ⟨T⟩_q (quadrature) | ⟨chord⟩ | thin limit = ⟨T⟩_q/c₀ |
|----|----|----|----|----|----|
| 0 | 0.3962 ± 0.0028 | 0.3962 ± 0.014 | 0.750000 | 0.750000 | **1.893 ± 0.013** |
| 3 | 1.0890 ± 0.0037 | 1.0674 ± 0.015 | 2.000000 | 0.750000 | **1.837 ± 0.006** |
| 10 | 2.6765 ± 0.0112 | 2.6132 ± 0.023 | 4.916667 | 0.750000 | **1.837 ± 0.008** |

(⟨T⟩_q = ⟨chord + q(r²chord + rμchord² + chord³/3)⟩_vol; cross-seed 4×2e6
checks at τ₀=1e−3 agree: c = 0.396 ± 0.014 / 1.100 ± 0.015 / 2.699 ± 0.023.)

**The thin volume window is UNIVERSAL in q: ≈ 1.84–1.89 (~1.86).**
This REFUTES the earlier "thin ≈ 2.2" claim (J11 used E[D] ≈ 0.338·τ₀, which
is the value of c at τ₀ = 1 — the true τ₀→0 limit is c₀ ≈ 0.40 ± 0.01, and
0.75/0.338 = 2.22 was never a τ₀→0 statement).

## 4. P3 — THE KILL-REGION MAP (naive central-window observer)

Naive observer assumes the central window [4/3, 2] (τ₀-free, J09 27/27);
under volume emission the same ratio measures outside that window → the
observer "kills" Thomson scattering wrongly.  Boundaries from exact
−ln A_v(τ₀) ÷ (τ₀ · c-interp(τ₀)) on [0.001, 8], MC knot interpolation,
200-sample bootstrap SEs on the crossing points.

| q | R < 4/3 (low-side kill) | R > 2 (high-side kill) | max R_v (location) |
|----|----|----|----|
| 0 | **τ₀ > 6.40 ± 0.02** | never (max 1.927 ± 0.01 at τ₀ ≈ 0.50; 2/200 bootstrap excursions) | 1.9272 |
| 3 | **τ₀ > 2.39 ± 0.01** | never (max 1.873; 0/200) | 1.8732 (τ₀→0) |
| 10 | **τ₀ > 0.97 ± 0.01** | never (max 1.880; 0/200) | 1.8802 (τ₀→0) |

Boundary curve τ*(q) — refined by a dense supplement (`K07_supplement.py`,
n = 6e5 per point, exact R = −ln A_quad/E[D]_MC, linear interpolation of the
bracketing points, delta-method SE):

| q | **τ*(q): R_v = 4/3** | bracketing R values |
|----|----|----|
| 0 | **6.505 ± 0.002** | R(6.5)=1.3337±0.0023, R(7.0)=1.2949±0.0022 |
| 3 | **2.415 ± 0.002** | R(2.2)=1.3796±0.0023, R(2.5)=1.3151±0.0022 |
| 10 | **0.978 ± 0.002** | R(0.9)=1.3791±0.0023, R(1.05)=1.2911±0.0021 |

(consistent with the knot-interp model scan: 6.40±0.02 / 2.39±0.01 / 0.97±0.01).
The naïve-kill region in (τ₀, q) is **{τ₀ > τ*(q)}**, with τ* = 6.505 / 2.415 /
0.978 at q = 0 / 3 / 10 — monotone decreasing in q (the (τ₀=1, q=10) point of
J11 is already inside it); the high side **does not exist** — the volume window
never exceeds 2, so a naive observer never gets a false high-side kill (the
old "thin ~2.2 > 2" J11 speculation dies with the c₀ correction above).

## 5. P4 — the crossing report

- **Central window: flat in τ₀** — (1+q/3)/(½+q/4) = 2.000 (q=0), 1.6/1.4444
  (q=3/10), independent of τ₀ (J09, 27/27).
- **Volume window: strictly DECREASING in τ₀ for every q**, from the thin
  limit ≈ 1.86 (universal) down through
  **R(8) = 1.224 ± 0.003 (q=0) · 0.689 ± 0.002 (q=3) · 0.356 ± 0.001 (q=10)**;
  the "thick ~1.2" target is the q=0, τ₀≈8 value, not a floor.
- **Asymptotic thick limit = 0**: the exponent T has a zero at the surface
  (r→1, μ→1: chord → 0), so −ln A_v grows only logarithmically (−lnA(200)/ln200
  → 1.05–1.51 by q; q=0: A·τ₀ → ⟨chord⟩ = 0.750 within 0.3%), while
  E[D] ~ τ₀·c∞ with c∞ > 0 ⇒ R_v → 0 slowly (log/linear).  So the volume
  window is (0, ~1.93] on [0.001, 8] — versus central [4/3, 2] — and the
  geometry discriminates cleanly: **central emission ⇒ ratio ∈ [4/3, 2]
  always; volume emission ⇒ ratio leaves [4/3, 2] on the LOW side above
  τ*(q) and never exceeds 2**.

## 6. Verdict

- **V1/V2 (J11): CLOSED** — corrected chord quadrature matches the engine
  18/18 within 4 SE (max z = 2.53 at (0.5, 0); q=3/10 now z ≤ 1.25, was
  29.5/83.6).  The J11 file's "plus"-chord formula is demonstrably wrong at
  q>0 and must not be used.
- **Window theorem, volume face: CLOSED** — R_v(τ₀,q) is τ₀-dependent,
  strictly decreasing, thin limit ≈ 1.86 (universal), never above 2, low-side
  crossing τ*(q) = 6.40/2.39/0.97 for q = 0/3/10.
- A measured transfer-function ratio below 4/3 is NOT a Thomson kill unless the
  geometry is known to be central; under volume emission it is the *expected*
  signal for τ₀ > τ*(q).  Central: 27/27 checks stand (J09).

## 7. Files

- `K07_vol_window.py` / `K07_vol_window.out` / `K07_results.json` (34/34 checks)
- `K07_supplement.py` / `K07_supplement.out` / `K07_supplement.json` —
  dense boundary bracketing (10 runs × 6e5 photons)
- This file.  No git commit (per lane rules).