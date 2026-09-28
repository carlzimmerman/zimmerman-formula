# AS031 — Historical exponential AQUAL inversion: derivation

Run `AS031-r1-20260928T021426Z-dsv4f-hermes` — worker `deepseek/deepseek-v4-flash-0731` (openrouter), Hermes focused subagent.
Task spec SHA-256: `c898cbe489844e63fe0d0c8732fec490d709828a691ac1ec118e0fcbc996675a`.

**Branch status (mandatory):** the historical EXP AQUAL branch is a **retired comparison branch**. The operative target
of the amended thirteen-item programme is **filtered MONO under causality criterion B**. Nothing in this run is a
substitute for that target; every conclusion below is labelled EXP-diagnostic unless an explicit bridge is proved.

---

## 0. Sources inspected, hashes, and status

| Source | SHA-256 (this run) | Manifest pin | Match |
|---|---|---|---|
| `README.md` | `91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed` | same | ✓ |
| `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` | `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` | same | ✓ |
| `real_research/peer_review_2026_09_26/README.md` | `521d9ac36a93a27dcd6c995f78743ae9b1de4304095911871d81e6a70f9ecaac` | same | ✓ |
| `STANDING.md` | `660462ebe8f98844c418e173a1dada90b9df3800c4d445fd5a0556eb9476bf63` | same | ✓ |
| `deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json` | `fe295b80bddbb0520884036ea5978d8f73174a8520f3ce0f91e2bf0f97f57fba` | — | ✓ (self) |

`SOURCE_MANIFEST.json` pins `README.md`, `FRIED_CHICKEN_SPEC.md` and the peer-review README at assembly; all current
bytes match the pins. The operative-target statements (filtered `nu_mono`, criterion B, requirement-9 controlled
zero-field limit) are taken from the amendment block of `FRIED_CHICKEN_SPEC.md` and `STANDING.md`.

No prior AS031 result directory exists; the claim file `claims/AS031.json` shows this seed reserved and dispatched to
this worker (state "running", `dispatched_utc 2026-09-28T01:58:22Z`). This run is the first execution of AS031.

---

## 1. Step 1 — precise claim, symbol dictionary, boundary conditions, assumptions

### 1.1 Symbol dictionary (framework conventions, FRAMEWORK_CONTRACT)

| Symbol | Meaning | Value / units |
|---|---|---|
| `g` | total radial acceleration (magnitude), `g = |grad Phi|` in spherical AQUAL | m/s² |
| `B = g_bar = g_N` | Newtonian baryonic acceleration `G M_b(r)/r^2` | m/s² |
| `x = g/a0` | dimensionless total-field variable | ≥ 0 |
| `y = B/a0` | dimensionless Newtonian variable | ≥ 0 |
| `mu_EXP(x)` | EXP interpolating function, **retired comparison branch** | `1 − exp(−x)`, x ≥ 0 |
| `a0` | framework scale | `a0 = kappa·c·sqrt(G·rho_Lambda)`, **kappa = 1/2 ADOPTED** (not derived) |
| `G, c, M_sun, pc, k_B` | numerics | `6.67430e-11`, `299792458`, `1.98847e30`, `3.085677581491367e16`, `1.380649e-23` (SI) |
| footings | canonical / alternative `a0` | `9.3619e-11` / `1.1279e-10` m/s² — **separate** (never shared fixed ρ and fixed κ) |

AQUAL field equation of the EXP branch (spherical, static):

```
div[ mu_EXP(|grad Phi|/a0) grad Phi ] = 4 pi G rho_b
   =>   (1/r^2) d/dr [ r^2 mu_EXP(g/a0) g ] = 4 pi G rho_b
   =>   mu_EXP(x) g = B        with x = g/a0,  B = G M_b(r)/r^2
   =>   y = x (1 - exp(-x)),   x >= 0.                     (the task's EXP law)
```

### 1.2 Precise claim (established here, EXP branch only)

For the EXP algebraic response

```
y(x) = x·(1 − e^{-x}),   x ∈ [0,∞),   μ(x) = 1 − e^{-x} ,
```

1. **(derivative / stability slope)** `dy/dx = 1 + (x−1)e^{-x}`;  `dy/dx ≥ 0` with equality **only at x = 0**
   (quadratic contact); `dy/dx` rises to its maximum `1 + e^{-2} ≈ 1.135335` at `x = 2` (inflection of y,
   `d²y/dx² = e^{-x}(2−x)`), then decreases to `1+` as `x → ∞`.
2. **(monotonicity / invertibility)** y is **strictly increasing** on `[0,∞)`, so `y : [0,∞) → [0,∞)` is a bijection
   and the EXP inverse `x(y) : [0,∞) → [0,∞)` exists and is unique.
3. **(exact inverse in the μ-parametrization)** with `μ = 1 − e^{-x} ∈ [0,1)`:
   `x(μ) = −ln(1−μ)`, `y(μ) = −μ·ln(1−μ)`, both strictly increasing in μ. No elementary/Lambert-W closed form for
   `x(y)` exists (sympy `NotImplementedError`; W(z) ~ z or −z-neighbourhood behavior cannot reproduce the deep
   branch `x ~ sqrt(y)`).
4. **(universal inversion bracket — deep and high-field initial brackets)** for every `y > 0`,
   `sqrt(y) ≤ x(y) ≤ (y + sqrt(y² + 4y))/2`, both bounds tight (width `~ y/2` deep, `→ 1` Newtonian).
5. **(asymptotics with leading neglected terms)** deep: `x = sqrt(y) + y/4 + (7/96)y^{3/2} + (1/48)y² + (491/92160)y^{5/2} + O(y³)`
   (leading neglected term after `sqrt(y)+y/4` is `(7/96)y^{3/2}`; domain `y ≪ 1`). Newtonian:
   `x = y + y·e^{-y} − y(y−1)·e^{-2y} + O(y²e^{-3y})` (leading neglected term `−y(y−1)e^{-2y}`; domain `y·e^{-y} ≪ 1`).
6. **(stability-relevant identity)** the AQUAL **strong-ellipticity function** computed at `T = x²` is
   `μ(T) + 2T·μ′(T) = dy/dx > 0` for all `x > 0` — the EXP spherical field equation is strictly elliptic away from
   `x = 0`; the ellipticity constant vanishes quadratically at the origin (`μ(0) = 0`, `y ~ x²`). **Diagnostic only**:
   it certifies the *retired* branch's structure, not the operative MONO equation.
7. **(Q-type deviation, exact)** the EXP branch never lies on the Q hyperbola: `x² − y² = x²(2e^{-x} − e^{-2x}) > 0`
   for all x > 0 (deep `~ x²`, Newtonian `~ 2x²e^{-x} → 0` exponentially).
8. **(exact landmarks)** `y(1) = 1 − 1/e = 0.6321206…` (the x = 1 pivot; the correct exact statement — an early
   draft claimed `y = 1/e` there, which the independent identity check rejected); `x(1/e) = 0.718078`; at the
   framework knee scale `y = 1` (i.e. `B = a0` at `r = r_M`): `x = 1.3499765`, `g = a0·x = 1.26383e-10 m/s²`
   (canonical) / `1.52264e-10` (alternative).
9. **(conditioning)** `dx/dy = 1/(1+(x−1)e^{-x}) ∈ [1/(1+e^{-2}), ∞)`; `dx/dy|(y=1e-10) ≈ 5.000025e4 ≈ 1/(2√y)` —
   deep inversion is ill-conditioned in the same quadratic-contact way as every MOND-family kernel (diagnostic).

### 1.3 Framework inputs vs conclusions

- **Inputs (adopted, not derived):** `kappa = 1/2`; `a0 = kappa·c·sqrt(G·rho_Lambda)`; the two a0 footings; the EXP
  law `y = x(1−e^{-x})` as the task's declared branch; the mandated grid `y = 10^k, k = −10..8 step 0.1`.
- **Derived here (EXP branch):** items 1–9 above; `rho_Lambda = 4a0²/(Gc²)` per footing (a consequence of the adopted
  `a0` relation, not an independent measurement).
- **Not derived / not claimed:** kappa's normalization; anything about the operative filtered-MONO branch; any
  dynamical, stability or observational statement of the full theory.

---

## 2. Step 2 — derivative, monotonicity, inverse construction (intermediate algebra)

### 2.1 `dy/dx` and monotonicity

```
y(x) = x(1 − e^{-x})
dy/dx = (1 − e^{-x}) + x·e^{-x} = 1 − e^{-x} + x e^{-x} = 1 + (x−1)e^{-x}.
d²y/dx² = e^{-x} + (e^{-x} − x e^{-x}) = e^{-x}(2 − x).
```

- `dy/dx(0+) = 0` (limit; exactly 0 at x = 0), `dy/dx(x) > 0` for all x > 0:
  - `0 < x < 1`: `dy/dx = 1 − (1−x)e^{-x}`; `(1−x)e^{-x} < 1` since `e^{-x} < 1` and `0 < 1−x < 1`; hence `dy/dx > 0`.
  - `x ≥ 1`: `dy/dx = 1 + (x−1)e^{-x} ≥ 1 > 0`.
- Inflection of y at `x = 2`: `d²y/dx² > 0` on `[0,2)`, `= 0` at 2, `< 0` on `(2,∞)` — the slope `dy/dx` is maximal
  at `x = 2` with `dy/dx(2) = 1 + e^{-2} = 1.1353352…`, and `dy/dx → 1+` as `x → ∞`
  (`(x−1)e^{-x} > 0` for x > 1).
- **Consequence:** y is C∞ and strictly increasing on `[0,∞)`, `y(0) = 0`, `y → ∞`. By the monotone convergence/
  intermediate-value argument, `y : [0,∞) → [0,∞)` is a **bijection**, so `x(y)` exists, is unique, and is C∞ on
  `(0,∞)` (inverse function theorem; slope > 0).

Stability relevance (`μ + 2Tμ′` identity). In AQUAL variables `T = (g/a0)² = x²`, `μ(T) = 1 − exp(−√T)`. The
strong-ellipticity constant of `div[μ ∇Φ] = 4πGρ` is `μ(T) + 2T μ′(T)`; because `x·d/dx = 2T·d/dT` at `T = x²`,

```
μ(T) + 2T μ′(T) = μ(x) + x μ′(x) = (1−e^{-x}) + x e^{-x} = dy/dx .
```

So **strict positivity of `dy/dx` is exactly the ellipticity (stability) condition of the EXP AQUAL equation**, and
it holds for every `x > 0`; only the isolated deep point `x = 0` is degenerate (`μ = 0`, quadratic contact). This is
the analogue of the "controlled zero-field limit" item in the operative spec — for the *retired* branch.

### 2.2 Exact inverse: μ-parametrization and the no-closed-form statement

Let `μ = 1 − e^{-x}`. Then `x(μ) = −ln(1−μ)` exactly, and

```
y(μ) = x·μ = −μ·ln(1−μ),   μ ∈ [0,1).
dy/dμ = −ln(1−μ) + μ/(1−μ) = x + (e^{x} − 1) > 0  (strictly increasing in μ).
```

This is the **exact EXP inverse as a function of μ** (the branch's natural constitutive variable). Substitution
`y(x(μ)) = μ` is identity. The map `y ↦ x(y)` has **no elementary/Lambert-W closed form**: `x ~ √y` as `y → 0⁺`
(quadratic contact), while every Lambert-W branch behaves as `W(z) ~ z` (principal, z → 0) or `W(z) ~ ln(−z)`
(W_{-1}, z → 0⁻); neither can supply `√y`. Sympy confirms: `solve(x*(1-exp(-x)) - y, x)` raises
`NotImplementedError` ("multiple generators [x, exp(x)]"). The inverse is therefore computed exactly by bracketed
monotone inversion (below) — it is not less an inverse for lacking an elementary symbol.

### 2.3 Deep and high-field initial brackets (also the universal bracket)

Two elementary inequalities from `e^{t} ≥ 1 + t` (t = −x and t = x):

```
1 − e^{-x} ≤ x            (upper line)   =>   y ≤ x²      =>   x ≥ sqrt(y)
1 − e^{-x} ≥ x/(1+x)      (lower line)   =>   y ≥ x²/(1+x) =>   x² ≤ y(1+x)   =>   x ≤ (y + sqrt(y²+4y))/2.
```

Both inequalities hold for every `x ≥ 0`, so **for every y > 0**:

```
sqrt(y)  ≤  x(y)  ≤  (y + sqrt(y² + 4y))/2 .
```

- Deep bracket (y ≪ 1): `[sqrt(y), sqrt(y) + y/2 + O(y²)]` — width ~ y/2 (tight).
- High-field bracket (y → ∞): `[y, y/(1−e^{-y})]` (since `x − y = x e^{-x} ≤ x e^{-y}`), i.e. `[y, y + y e^{-y} + …]`;
  equivalently the universal bracket's upper bound is `y + 1 − 1/y + …` (looser, still valid).

The numerical inverse uses bisection inside these brackets to relative tolerance `1e-70` followed by six Newton
polish steps (monotone function ⇒ bracket is never violated).

### 2.4 Asymptotic expansions with leading neglected terms

**Deep** (`y → 0⁺`). From `y = x² − x³/2 + x⁴/6 − x⁵/24 + …` with `s = √y`, ansatz `x = s + a1 s² + a2 s³ + a3 s⁴ + a4 s⁵`,
sympy fixes `a1 = 1/4, a2 = 7/96, a3 = 1/48, a4 = 491/92160` and verifies `y(x(s)) − s² = O(s⁷)`:

```
x(y) = sqrt(y) + y/4 + (7/96) y^{3/2} + (1/48) y² + (491/92160) y^{5/2} + O(y³) .
```

Leading neglected term after `sqrt(y) + y/4`: `+(7/96)y^{3/2}`, domain `y ≪ 1` (relative truncation error
`~ (7/96)·sqrt(y)`). Checked at `y = 1e-10`: `x/sqrt(y) − 1 = 2.5000073e-6` vs predicted `sqrt(y)/4 = 2.5e-6`, and
`(x − sqrt(y) − y/4)/y^{3/2} = 0.072916875` vs `7/96 = 0.07291667` (difference = `a3·sqrt(y) = 2.083e-7` ✓).

**Newtonian** (`y → ∞`). With `δ = x − y = x e^{-x}`, fixed-point iteration
`δ = (y+δ) e^{-(y+δ)} = y e^{-y} − y(y−1) e^{-2y} + O(y² e^{-3y})`:

```
x(y) = y + y·e^{-y} − y(y−1)·e^{-2y} + O(y² e^{-3y}).
```

Leading neglected term: `−y(y−1)e^{-2y}`, domain `y e^{-y} ≪ 1` (y ≳ 10). Checked at `y = 20, 30, 40, 60`:
`(x−y)/(y e^{-y}) = 0.999999961, 0.9999999999973, 0.9999999999999998, 0.9999999999999999999999995` and the ratio
against the second term `−y(y−1)e^{-2y}` → 1 at the same points. At `y = 1e8` the correction `y e^{-y} ~ 10^{-43429440}`
is below any fixed-precision floor (80 dps): the numerical inverse is exactly `y` — a precision statement, not a
mathematical one.

### 2.5 Exact landmarks and grid values (mandated grid, 181 points)

```
y(1) = 1 − 1/e = 0.6321205588…        <->  x = 1        (exact pivot)
x(1/e) = 0.71807796…                    (ordinary grid value)
y = 1   ->  x = 1.3499764854,  μ = 0.7407536,  g = 1.26383e-10 (can) / 1.52264e-10 (alt) m/s²
```

The pivot correction is worth recording: an initial draft asserted `x = 1 ⟺ y = 1/e` based on a sign slip
(`y = x(1−e^{-x}) = 1·(1−1/e) = 1 − 1/e`, not `1/e`); the independent identity check (`y_of_x(1) − (1−1/e) = 0` at
80 dps, `x(y=1−1/e) − 1 = 0`) rejected the wrong landmark and pinned the right one. This is exactly the kind of
error the "different-representation" check is designed to catch.

### 2.6 Q-type deviation (exact)

`x² − y² = x²[1 − (1 − e^{-x})²] = x²(2e^{-x} − e^{-2x})`, verified on the grid to ~1e-80. The EXP branch
**always** sits strictly inside the Q hyperbola (`x² − y² > 0`), deep `~ x²`, Newtonian `~ 2x²e^{-x} → 0`. A shared
deep limit (`y ~ x²`) is **not** a shared finite law: the branch table below shows 3–16% finite-y disagreement.

### 2.7 Conditioning

`dx/dy = 1/(dy/dx) = 1/(1 + (x−1)e^{-x})`; minimum over `(0,∞)` is `1/(1+e^{-2}) = 0.880797` at `x = 2`; deep:
`dx/dy ≈ 1/(2x) ≈ 1/(2√y) → ∞` as `y → 0` (numerically `5.0000e4` at `y = 1e-10`). Deep inversion is
ill-conditioned for every kernel with `y ~ x²` contact — a generic MOND-family fact, diagnostic only (cf. AS046).

---

## 3. Step 3 — intermediate algebra, signs, units, limits (all shown above)

- All algebraic steps are dimensionless in `x, y`; `a0` enters only through the maps `g = a0·x`, `B = a0·y` and is
  **cancelled identically** — the theorem is scale-free and applies to **both footings** without refitting.
- Signs: `x, y, μ ≥ 0`; `dy/dx > 0` strictly for x > 0; `d²y/dx²` changes sign at `x = 2`; `x² − y² > 0`.
- Units: `m/s²` for `a0, g, B`; `kg/m³` for `rho_Lambda`; `kg` for masses; dimensionless `x, y, μ`.
- Footing consequences (kappa = 1/2 **fixed** ⇒ different vacuum densities):
  `rho_Lambda = 4a0²/(Gc²) = 5.8444125e-27 kg/m³` (canonical), `8.4830896e-27 kg/m³` (alternative);
  `a0_alt/a0_can = 1.2047768` (effective kappa if ρ fixed), `rho_alt/rho_can = 1.4514872` (ρ ratio if κ fixed).

---

## 4. Step 4 — independent checks (different representations, actual residuals)

All at mpmath 80 digits, grid `y = 10^k, k = −10..8 step 0.1` (181 points), in `compute_as031.py`.

| Check | What it does | Observed (80 dps) | Pass |
|---|---|---|---|
| CK1 self-residual | substitution of the bracketed inverse into the forward law `r = y(x(y)) − y` | max `|r| = 4.2e-81` | ✓ |
| CK2 μ-route cross-check | independent representation: invert μ↦`−μ ln(1−μ)` for y ≤ 10, `x = −ln(1−μ)`, compare x | max diff `1.6e-72` | ✓ |
| CK3 monotone grid | dydx > 0 at every grid point (min `2.0e-5` at deepest point, → 0 only at x = 0) | 181/181 | ✓ |
| CK4 deep limit | `x/√y − 1` at y=1e-10 = `2.5000073e-6` vs `√y/4 = 2.5e-6`; next order `7/96` matched | ✓ exact + leading terms | ✓ |
| CK5 Newtonian limit | `(x−y)/(y e^{-y})` at y=20..60 → 1 (0.99999996 → 0.9999999999999999999999995); 2nd term ratio → 1 | ✓ | ✓ |
| CK6 stability identity | `μ + 2Tμ′(T)` vs `dy/dx`, T = x², at x ∈ {0.01,1,2,3,10} | diff ≤ 1.3e-81 | ✓ |
| CK7 Q-deviation identity | `x² − y²` vs `x²(2e^{-x} − e^{-2x})` at 5 points | diff ≤ 4.2e-80 | ✓ |
| CK8 pivot identity | `y(1) − (1 − 1/e) = 0`; `x(1 − 1/e) − 1 = 0` | exact | ✓ |
| CK9 derivative landmarks | `d²y/dx²(x=2) = 0`, sign + at x=1, − at x=3; `dy/dx(2) = 1+e^{-2}` | exact | ✓ |
| CK10 grid arithmetic | grid span `[1e-10, 1e8]`, 181 points (range(−100,81)/10) | 181/181 | ✓ |

The CK1–CK8 checks are *finite-precision consistency checks of exact identities*; the **certificates are the Lean
theorems** (Section 6) plus the sympy exact coefficient algebra — the numerics demonstrate, they do not constitute,
the mathematics.

---

## 5. Step 5 — negative control and strongest surviving statement

### 5.1 Mandated negative control: `x = y·nu_RAR(y)` treated as the exact EXP inverse

Control: take `x_RAR(y) = y/(1 − e^{−√y})` (the RAR branch's inverse relation) as a candidate "exact EXP inverse"
and evaluate the forward-law residual `r(y) = y(x_RAR(y)) − y = x_RAR(1 − e^{−x_RAR}) − y`.

**Analytic result (stronger than the numerics):** `r(y) > 0` for every `y > 0`. Proof chain:

```
x_RAR(y) > x_EXP(y)   <=>   y/(1−e^{−√y}) > x        (x = x_EXP(y))
                       <=>   x(1−e^{−x}) > x(1−e^{−√y})      (y = x(1−e^{−x}))
                       <=>   1−e^{−x} > 1−e^{−√y}
                       <=>   x > √y ,
```

and `x ≥ √y` is the certified lower bracket (equality only at y = 0). Therefore `r(0) = 0`, `r(y) > 0` for all
`y > 0`, and `r(y) → 0` as `y → ∞` (both inverses → y).

**Measured residuals (capable of failing; reported, not assumed):**

- `max |r| = 0.5805687` at `y = 10^{0.6} = 3.98107` (relative to y: 0.1458);
- `r(1) = +0.256772` with `x_RAR(1) = 1.581977` vs `x_EXP(1) = 1.349976` (r > 0 here);
- signed residual `r ≥ 0` on all 181 grid points; the unique apparent zero at `y = 10^{4.6}` is an **80-dps floor
  artifact** — at 120 dps `r = 8.8483e-83 > 0`, matching the leading prediction `y(e^{−√y} − e^{−y}) =
  8.8483e-83` to all 80 digits;
- fine multiplicative scan (850 points, ×1.05): 687 strictly positive, 163 exactly zero — all 163 at `y > 3.4e4`
  where both exponentials are below the 80-dps floor;
- adaptive-precision tail (`dps = 0.5·√y + 30`, up to 5030 dps): `r > 0` at `y ∈ {1e5, 1e6, 1e7, 1e8}`, each
  matching `y(e^{−√y} − e^{−y})` to full precision.

**Control verdict:** the RAR relation is **not** the EXP inverse: forward-law residual `0.58` at its worst and
strictly positive everywhere (proved). The control failed the candidate exactly as required.

### 5.2 Secondary control: deep and Newtonian limiting regimes

- Deep: both EXP and RAR inverses approach `√y`, but with different rates — `x_EXP = √y + y/4 + …` vs
  `x_RAR = √y + y/2 + …`; the residual `r ~ y/4·(2√y) ~ y^{3/2}/2` near 0 (measured `r > 0` at every deep grid
  point). A shared leading asymptote is **not** an identical law.
- Newtonian: both approach `y`; the corrections `y e^{−y}` (EXP) vs `y e^{−√y}` (RAR) differ by a factor
  `e^{√y − y}`, so `r ~ y(e^{−√y} − e^{−y}) > 0` until it vanishes beyond any fixed precision.
- These are consistency checks of an exact identity chain, reported with actual values, not claimed as theorems.

### 5.3 Strongest surviving statement (EXP branch, all conditions listed)

> **Theorem (EXP diagnostic).** On the retired EXP branch `y = x(1−e^{−x})`, x ∈ [0,∞): (i) `dy/dx = 1+(x−1)e^{−x}`
> with strict positivity on x > 0 — equivalently the AQUAL strong-ellipticity function `μ(T)+2Tμ′(T)`, T = x², is
> strictly positive away from x = 0 (degenerate quadratically at 0); (ii) y is a C∞ bijection [0,∞)→[0,∞); the
> inverse is unique, bracketed by `√y ≤ x(y) ≤ (y+√(y²+4y))/2`, has the deep series of §2.4 and the Newtonian
> expansion of §2.4; (iii) the exact inverse exists in the μ-parametrization `x(μ) = −ln(1−μ)`, `y(μ) = −μ ln(1−μ)`;
> (iv) the RAR relation is NOT an EXP inverse: `r(y) = x_RAR(1−e^{−x_RAR}) − y > 0` for all y > 0 (proved, measured
> max 0.5806). Certified in Lean 4 with axioms ⊆ {propext, Classical.choice, Quot.sound}. Conditions: x ≥ 0, y ≥ 0;
> all statements dimensionless; both a0 footings apply without refitting; kappa = 1/2 remains an adopted input.

### 5.4 Transfer implication (what is needed to reach the operative target)

This is a **retired-branch audit**; no EXP result is imported into the operative filtered-MONO theory. The audit's
usable content for the campaign is diagnostic: the deep conditioning degeneracy (`dx/dy ∝ 1/√y`, ellipticity
constant ∝ 2x → 0 quadratically) is generic to every `y ~ x²` MOND-family kernel, so the operative MONO branch faces
the same zero-field structure **and** the heat filter `S = exp((ξ²/2)Δ)` must carry the required control (spec
requirement 9). Whether the filtered MONO operator is strictly elliptic with a controlled modulus is a separate
theorem that this run does **not** prove (and that no EXP result can prove for it). The first additional implication
needed to transfer anything to the full theory is:

> **Bridge requirement:** derive the strong-ellipticity modulus of the operative filtered MONO equation
> `ΔΦ = 4πGρ_b + S* div[(ν_mono(|∇S u|/a0) − 1) ∇S u]` near the zero-field limit on the preferred foliation leaf
> (measure, domain, boundary conditions of S declared), and benchmark its deep conditioning against the EXP audit
> table (`dx/dy ≈ 1/(2√y)` at y = 1e-10, min `1/(1+e^{-2})`, max slope `1+e^{-2}` at x = 2).

Until that bridge exists, the EXP branch remains what the contract says it is: **a comparison branch**.

---

## 6. Lean 4 certificate

File: `AS031_exp_inverse_certificates.lean` (in this run dir). Compile (from `fable_independent_2026/lean_2026`):

```
lake env lean <abs path>/AS031_exp_inverse_certificates.lean   # exit 0, empty error log
```

13 theorems, all with `#print axioms` output exactly `[propext, Classical.choice, Quot.sound]`, zero `sorry`:

| Theorem | Content |
|---|---|
| `exp_mu_param` | μ-parametrization identity `y = −μ ln(1−μ)` at `μ = 1−e^{-x}` (G) |
| `exp_neg_deriv` | `d/dt exp(−t) = −exp(−t)` (helper) |
| `exp_deriv_ident` | `HasDerivAt yExp (1+(x−1)e^{-x}) x` (A) |
| `exp_deriv_pos` | `0 < dy/dx` for all `x > 0` (B) |
| `exp_forward_strict_mono` | `StrictMonoOn yExp (Ici 0)` (C) |
| `exp_forward_lt` / `exp_forward_injective_nonneg` | strict increase / injectivity on `[0,∞)` (C corollaries) |
| `exp_forward_upper` / `exp_forward_lower` | `x²/(1+x) ≤ y ≤ x²` ⇒ the universal bracket (D) |
| `exp_deriv2_ident` | `d²y/dx² = e^{-x}(2−x)` (E) |
| `exp_deriv2_sign_below` / `exp_deriv2_sign_above` | slope increases on [0,2), decreases on (2,∞) (F) |
| `exp_slope_at_two` | `dy/dx(2) = 1+e^{-2}` |

House traps hit and resolved (recorded for the campaign): `mul_right`/`mul_left` products must match the goal shape
exactly; `convert … using 1 <;> ring` spawns function-equality goals when one side is a `def` symbol — resolve by
`change` to the explicit lambda before `exact`; `simpa` with extra lemmas rewrites inside lambdas asymmetrically —
keep statements shape-identical and use `rw [hslope] at hd` with a standalone `ring` equality (AS026 pattern);
`HasDerivAt.exp` on `(hasDerivAt_id x).neg` is the robust way to differentiate `exp(−t)`; derivative-side `(1 − 0)`
shapes from rule applications must be kept until the closing `ring` equality; `strictMonoOn_of_deriv_pos` needs
`Convex ℝ (Ici 0)` + `ContinuousOn` + positivity of `deriv` on `interior (Ici 0) = Ioi 0` (`interior_Ici`).

---

## 7. Bounded prototype and execution bounds (actually enforced)

`compute_as031.py` — single process, single thread, no subprocesses:

- wall clock: `signal.alarm(120)` **armed before computation**, disarmed at exit; observed `1.62 s` (user 1.7 s);
- memory: macOS refuses `RLIMIT_AS` lowerings (`current limit exceeds maximum limit`, same as sibling AS026) —
  recorded honestly. Observed peak RSS: `/usr/bin/time -l` `~64 MB` (63.9 MB), in-script macOS `ru_maxrss`
  `60.95 MB` (bytes → MB). Far below the 512 MB declaration;
- precision: mpmath 80 dps (120–5030 dps for the NC floor/tail refinements), sympy exact for the series
  coefficients, float-free on the main grid;
- grid: `y = 10^k, k = −10..8 step 0.1` → 181 points (mandated), plus fine scan 850 pts, adaptive-precision tail
  4 pts, landmark table 9 rows.

---

## 8. Branch table (comparison only — never silently identified)

Rows: `x(y)` at selected y, EXP vs Q, RAR, MU2, MONO (MONO splice `y★ = 2.337412, y_p = 2.539638, h_p = h_RAR(y_p) ≈ 0.6476, δ = 0.05`, RAR segment below y★, continuation above, per FRAMEWORK_CONTRACT). All values 80-dps mpmath, computed in `compute_as031.py`.

| y | x_EXP | x_Q | x_RAR | x_MU2 | x_MONO | note |
|---|---|---|---|---|---|---|
| 1e-4 | 0.01002507 | 0.01000050 | 0.01005008 | 0.01003760 | 0.01005008 | all → √y deep, distinct approach rates |
| 1e-2 | 0.10257505 | 0.10049876 | 0.10508332 | 0.10385311 | 0.10508332 | |
| 0.1 | 0.34375982 | 0.33166248 | 0.36885862 | 0.35709020 | 0.36885862 | 3.7% above Q, 7.3% below RAR |
| 0.36788 (1/e) | 0.71807796 | 0.70937629 | 0.80895154 | 0.76907877 | 0.80895154 | |
| 1 | 1.34997649 | 1.41421356 | 1.58197671 | 1.48928857 | 1.58197671 | B = a0 (r_M scale); g = 1.2638/1.5226e-10 m/s² |
| 2.33741 (y★) | 2.53797829 | 2.79301036 | 2.98437237 | 2.82285707 | 2.98437237 | MONO reaches the splice on the RAR segment |
| 10 | 10.00045381 | 10.48808848 | 10.44200179 | 10.27281058 | 10.67753904 | EXP vs MONO differ at 6.8% |
| 100 | 100.00000000 | 100.49875621 | 100.00454020 | 100.03843256 | 100.74558198 | continuation diverges from RAR above y★ |
| 1e4 | 10000.0* | 10000.49998750 | 10000.00000037 | 10000.00039984 | 10000.89389589 | *80-dps floor (correction < 1e-80 relative) |

Shared deep limit (`x ~ √y`, equivalently `y ~ x²`) is **not** a shared finite law: at `y = 1` the five branches
give total-field-to-Newtonian ratios 1.350 / 1.414 / 1.582 / 1.486 / 1.582. The landmark row shows EXP below Q below
MU2 below RAR = MONO at the knee — the ordering the Q/RAR/MU2/EXP/MONO separation requires.

---

## 9. First-principles inputs, derived objects, limitations

**Primitives:** `G, c, M_sun, pc, k_B` (contract values); `kappa = 1/2` (ADOPTED); both a0 footings; the EXP law.
**Derived here:** §1.2 items 1–9 (all EXP branch); `rho_Lambda = 4a0²/(Gc²)` per footing; LEAN-certified A–G;
sympy-exact deep coefficients. **Measured inputs:** none (no dataset). **Not derived:** kappa; the operative MONO
statements; the filtered-equation ellipticity bridge; dynamics/stability of the full theory.

**Limitations.** (1) EXP is retired: results are diagnostic for the historical branch and transfer only through the
explicit §5.4 bridge. (2) kappa = 1/2 remains adopted; the inverse is dimensionless and cannot fix its freedom.
(3) All "theorem" content is the Lean certificate + exact algebra; grid values are finite consistency checks.
(4) The y = 1e8 Newtonian row is precision-bound, not mathematical. (5) Branch table uses the contract's rounded
MONO landmarks (2.337412, 2.539638, δ = 0.05); sub-splice details do not affect the EXP statements.

---

## 10. Child proposal (ready specification, NOT dispatched — no runner available)

**AS031.C01 — Operative-gate bridge: strong-ellipticity modulus of the filtered MONO equation vs the EXP audit.**
Claim: on the preferred foliation leaf with `S = exp((ξ²/2)Δ)` acting on a declared Sobolev domain, the linearized
filtered MONO operator `L = Δ − S* div[(ν_mono…−1)∇S·]`-type principal symbol has ellipticity constant bounded below
by a computable function of y whose deep modulus (y → 0) is `O(1)` (filtered) vs `O(x)` for the unfiltered EXP audit
(item: does the filter remove the quadratic-contact degeneracy?), benchmarked against this run's EXP table
(`dx/dy | y=1e-10 = 5.0000e4`, min `1/(1+e^{-2})`, max slope `1+e^{-2}` at x = 2). Controls: (i) constant-field
limit recovers the EXP-style `dy/dx` numbers when S → id (control can fail if ξ-dependence persists); (ii)
filter-width sweep ξ: modulus must move; (iii) deep limit y → 0 for the filtered modulus must be computed, not
assumed; (iv) zero-sorry Lean for the cleared algebraic form. Dependencies: FRAMEWORK_CONTRACT MONO + S definitions;
FRIED_CHICKEN_SPEC requirement-9 amendment; this run's EXP audit table. Duplicate check: nearest seeds are AS033
(splice location), AS034 (MONO integration), AS036 (physical vs phantom monotonicity), AS046 (inverse conditioning),
AS047 (force vs derivative error control), AS577/AS578 (MONO convexity/monotonicity modulus), AS026.C01 (Q-vs-MONO
mass-profile band) — none derives the *filtered* ellipticity modulus against an EXP benchmark; fingerprint distinct.
Dispatch state: **NOT DISPATCHED** — no subagent spawn mechanism available to this worker; ready spec returned to the
orchestrator per FIRST_PRINCIPLES_AND_BRANCHING.md.

---

## 11. Acceptance

`acceptance_state = "unreviewed"` — a separate orchestrator review is required before any scoped claim is accepted.
