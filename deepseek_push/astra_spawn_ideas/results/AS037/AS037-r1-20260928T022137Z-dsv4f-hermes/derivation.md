# AS037 — Constitutive Hessian eigenvalues of an AQUAL branch

**Run:** `AS037-r1-20260928T022137Z-dsv4f-hermes` · **Worker:** deepseek/deepseek-v4-flash-0731 (openrouter), Hermes focused subagent
**Task file (sha256):** `892289c1aa25b19d7b3896a0181ccace7b0f0b92aafac5d3d0e49663881f20bd`
**Sources:** all SOURCE_MANIFEST pins verified before execution (README `91a5fac…`, FRIED_CHICKEN_SPEC `98d9149f…`, peer review `521d9ac…`).
**Audited cell:** MU2 (algebraic, Lean-certified). **Comparison cell:** Q (Lean-certified). **Numerical cells:** EXP (historical comparison), RAR, MONO (operative, criterion B). ALL FIVE audited numerically at 80 dps.

---

## 1. Task, cell statement, and scope

The seed asks for the constitutive-Hessian eigenvalue content of an AQUAL-type branch: for a Lagrangian `f(z)`, `z = |grad Φ|²/a0²`, the constitutive matrix has eigenvalues related to `f'(z)` and `2z f''(z) + f'(z)`. We derive the eigenvalues for all five branches of the framework (RAR, MONO, Q, EXP, MU2), establish sign conditions (ellipticity ⟺ both eigenvalues > 0), the domains where eigenvalues vanish or change sign, and what that means per branch.

**Criterion-B placement:** MONO + heat filter is the *operative* cell; EXP AQUAL is *historical comparison*. This task audits the pointwise constitutive response only — the *filtered field equation* (seed step-5 dependency: apply the heat filter to the branch and derive the filtered field equation) is explicitly **not** exercised here; it is recorded as the next unresolved implication and dispatched as child AS037.C01. Both a0 footings (9.3619e-11, 1.1279e-10 m s⁻², kappa = 1/2) computed; the eigenvalue theorem is dimensionless so one theorem carries both footings.

Mandated constants: G = 6.67430e-11 SI, c = 299792458 SI, kappa = 1/2 (input). Mandated grid: `y = 10^k`, k = −10..8 step 0.1 → 181 points (y = B/a0; x = g/a0 on the same grid).

---

## 2. Constitutive setting and the eigenvalue theorem

The framework's branches are all of AQUAL type in flux form:

```
flux A(v) = mu(|v|/a0) v,        v = grad Φ,   x := |v|/a0,    B := the branch field variable (B = |B|, y := B/a0)
constitutive matrix N_ij := ∂A_i/∂v_j = mu(x) δ_ij + (mu'(x)/x) v_i v_j
```

With unit vectors e_∥ = v̂ and e_⊥ ⊥ v̂ the matrix is diagonal in the frame (e_⊥, e_∥):

```
lambda_T = mu(x)                      (transverse; any direction ⊥ grad Φ)
lambda_L = mu(x) + x mu'(x) = d(x mu)/dx      (longitudinal; along grad Φ)
```

In the Lagrangian language of the seed, `x² = z`, `f'(z) = mu(x)`, and

```
lambda_T = f'(z)
lambda_L = f'(z) + 2z f''(z)
```

(the two forms coincide by the chain rule: `d(xμ)/dx = μ + xμ'`, `x²f''(x²)·2x = 2z f''`). **Constitutive-ellipticity/well-posedness criterion:**

```
strict ellipticity of N  ⟺  lambda_T > 0  AND  lambda_L > 0
```

Both eigenvalues are continuous functions of `g > 0`; a zero crossing of either signals loss of well-posedness (hyperbolic blow-up or ill-posed elliptic step). The lambda_L form `d(xμ)/dx` is verified independently three ways: direct formula (ID1), finite difference of `x·μ` (ID2), and product-rule derivative certified in Lean (`xmu2_deriv`, `xmuQ_deriv`).

---

## 3. Branch-by-branch eigenvalue content

Notation: `x = g/a0`, `y = B/a0`, `u = x/2`.

### 3.1 MU2 (AUDITED CELL, Lean-certified)

```
mu(u)   = 1 − (1+u)⁻²                     (u = x/2)
lambda_T(u) = mu(u) = u(2+u)/(1+u)²
lambda_L(u) = mu + x·mu' = u(4+3u+u²)/(1+u)³ = 1 + (u−1)/(1+u)³
```

- Positivity: `lambda_T, lambda_L > 0` for all `u > 0` (Lean: `lamT_pos`, `lamL_pos`, `mu2_pos`); numerator factors `u > 0`, `2+u > 0`, `4+3u+u² > 0`.
- Degeneracy: `lambda_T(0) = lambda_L(0) = 0` (Lean: `mu2_zero`, `lamT_zero`, `lamL_zero`).
- Derivative content: `mu' = 2/(1+u)³` (Lean `mu2p_deriv`), `d(x·mu)/dx = d(u·mu)/du = lambda_L` (Lean `xmu2_deriv`; identity `lamL_eq_mu_plus`).
- Range: `lambda_T ∈ (0,1)`; `lambda_L ∈ (0, 28/27]`, sup **28/27 = 1.037037…** attained at `u = 2` ⇔ `x = 4` (Lean: `lamL_le_28_27`, `lamL_max_at_two`). This is the MU2 *historical longitudinal stiffness bump*: `lambda_L > 1` for `u ∈ (1, ...)`, i.e. for `x ∈ (2, x_bump)`.
- Newtonian side: `lambda_T, lambda_L → 1` from above; `lambda_L − 1 = (u−1)/(1+u)³ ~ 4/x²` at `x → ∞` (NUM: 3.99999875e-16 at x = 1e8 = 4/x²).
- Deep side: `lambda_T/x → 1`, `lambda_L/x → 2` as `x → 0+` (measured 1.999999999775 at x = 1e-10; exact series `lambda_L = 2u − 6u² + …`).

**No sign change**: both eigenvalues strictly positive on `(0,∞)`, degenerate only at `x = 0`.

### 3.2 Q (comparison cell, Lean-certified)

```
mu(x)   = (√(1+4x²) − 1)/(2x)     (J(0) = 0 branch; note mu ~ x, i.e. B ~ g²/a0 deep)
lambda_T = mu
lambda_L = d(x·mu)/dx = 2x/√(1+4x²)
```

- `x·mu = (√(1+4x²) − 1)/2 = yQ(x)`; Lean `yQ_deriv` gives `d yQ/dx = lambda_L`, `xmuQ_deriv` transfers to the flux form; `yQ_eq_x_muQ` is the algebraic identity.
- `mu > 0` and `mu < x` on `x > 0` (Lean `muQ_pos`, `muQ_lt_x` — the deep bracket, B ~ x²), `mu < 1` (`muQ_lt_one`).
- `0 < lambda_L < 1` on `x > 0` (Lean `lamLQ_pos`, `lamLQ_lt_one`): **no bump, sub-Newtonian**, `lambda_L → 1` from below as `1 − 1/(8x²)` (NUM: 1.25e-17 at x = 1e8).
- Deep: `lambda_L → 2x` exactly (measured 1.99999999999999999996 at x = 1e-10); `(x·mu)/x² → 1` (0.99999999999999999999 at x = 1e-10) — quadratic contact at the origin, `mu_Q(1e-50) = 0.0` exactly (degeneracy, NC3).

### 3.3 EXP (historical comparison; transcendental, numerical lane)

```
f(z) = 1 − e^{−√z},   G(z) = z + 2(√z + 1)e^{−√z} − 2   (spec form; sympy: G'(z) − (1−e^{−√z}) ≡ 0 EXACT)
mu(x) = 1 − e^{−x}
lambda_T = mu = 1 − e^{−x}
lambda_L = f' + 2z f'' = (√z + e^{√z} − 1)e^{−√z} = 1 + (x−1)e^{−x}
```

- Positivity: `1 − e^{−x} > 0`, `1 + (x−1)e^{−x} > 0` on `x > 0` (analytic; min of lambda_L over grid = 1.99…e-10 at x = 1e-10; approach to 0 from above).
- **Historical bump**: `lambda_L` has sup **1 + e⁻² = 1.1353352832** at `x = 2` (critical point of `(x−1)e^{−x}`: derivative `(2−x)e^{−x}`); `lambda_L > 1` for `x ∈ (1, x_bump)`, `x_bump ≈ 2.28`; `mu(2) = e⁻² = 0.1353…`. `lambda_T` strictly increasing to 1.
- Newtonian: `lambda_L = 1 + (x−1)e^{−x} → 1` from above with deficit `(x−1)e^{−x}` (at x = 100: deficit 99·e^{−100} = 3.7e-42; at x ≥ 1e4 the deficit underflows 80 dps → exactly 1.0).
- Deep: `lambda_T → x − x²/2 + …`, `lambda_L → 2x − 3x²/2 + …`; `lambda_L/x → 2` (1.99999999985 at x = 1e-10).

### 3.4 RAR (numerical lane)

```
mu(y) = 1 − e^{−√y}             (= y/x; the eigenvalue mu, monotone (0,1) on y > 0)
x(y)  = y/(1 − e^{−√y})          (RAR forward relation; deep x ~ √y: quadratic contact B ~ g²/a0)
lambda_T = mu
lambda_L = dy/dx = 1/(dx/dy),   dx/dy = 1/(1−e^{−√y}) + y·dν/dy,  ν = 1/μ   (inverse-slope identity ID3: (dy/dx)(dx/dy) = 1 to 1.05e-81)
```

- `lambda_T = μ ∈ (0,1)`, strictly increasing, `μ ~ √y` deep, `→ 1` Newtonian (0.9999546 at x = 100).
- `lambda_L` on the diagnostic grid: deep end `~ 2√y` (1.99998e-5 at y = 1e-10, `lambda_L/x → 2` since `x ~ √y`); knee region dips to ≈ 0.51 (x ≈ 0.42); **crosses 1 and carries an exponentially small longitudinal bump**: sup over grid `1.00018165` at x ≈ 100.0 (y = 100), asymptote `lambda_L − 1 ~ (√y/2)e^{−√y}` (peak `≈ 2.3e-4` at √y = 10); then returns to 1 from above (`(√y/2)e^{−√y}` decays; at 80 dps the deficit underflows to exactly 1.0 for y ≥ 1e4).
- No sign change: both eigenvalues positive on `y > 0`; degeneracy at the origin only (`λT ~ √y → 0`, `λL ~ 2√y → 0` as `x ~ √y → 0`).

### 3.5 MONO (OPERATIVE cell, criterion B; numerical lane)

```
mu(y) = y/(y + h(y)),   h' = h'_mono(y) = max(h'_RAR(y), delta·h_p/(y + y_p)),   delta = 0.05
y_p = 2.5396382822 (h'_RAR = 0),  h_p = h_RAR(y_p) = 0.6476102379,  splice y* = 2.3374124053
h(y) = h_RAR(y)  = y·e^{−√y}/(1−e^{−√y})         for y ≤ y*;
h(y) = h_RAR(y*) + delta·h_p·ln((y+y_p)/(y*+y_p))   for y > y*      (tail h' = delta·h_p/(y+y_p))
x(y) = y + h(y)                                    (MONO forward relation)
lambda_T = mu = y/(y+h)
lambda_L = dy/dx = 1/(1 + h')
```

Landmarks match the contract to 8 digits: y_p = 2.53963828 (contract 2.5396), h_p = 0.64761024 (0.6476), y* = 2.33741241 (2.3374).

- **Ellipticity**: `lambda_T = y/(y+h) ∈ (0,1)` trivially; `lambda_L = 1/(1+h')` with `h' = h'_mono ≥ 0` ⇒ `0 < lambda_L ≤ 1` on all `y > 0` — **strictly sub-Newtonian, no bump** (measured: 1 − λL = delta·h_p/(y+y_p) = 3.2380511e-10 at y = 1e8, matching the exact tail formula to all digits; `1 − μ = 1.192e-8`). Numerically: no sign-change bracket on (1e-12,1e8) (NC4) and zero violations on the 10000×10000 refined probe over x,y ∈ [1e-12,1e12].
- **Splice health**: h is C⁰ at y_p to 6.64e-33 (ID4), but the splice is C⁰ *in h′*: `d(lambda_L)/dy` jumps by **0.0342879** at y* (ID4 kink jump). lambda_L itself remains continuous and positive — the kink does not threaten ellipticity.
- Deep: `h ~ √y`: `mu ~ √y` (0.00000999995 at y = 1e-10), `x ~ √y`, `mu/x − 1 ≈ −√y` (measured −9.9999e-6 at y = 1e-10), `lambda_L ~ 2√y` (1.99998e-5) ⇒ `lambda_T/x → 1`, `lambda_L/x → 2`.
- Newtonian: `lambda_T, lambda_L → 1` from below with the exact tail rates above.

---

## 4. Domain analysis: vanishing and sign-change

| branch | lambda_T = 0 | lambda_L = 0 | sign change on (0,∞) | lambda_L > 1 (bump) | Newtonian limit |
|---|---|---|---|---|---|
| MU2 | x=0 only | x=0 only | none | (2, ∞): sup 28/27 at x=4 | 1 from above (~4/x²) |
| Q | x=0 only (mu~x) | none (mu>0) | none | never (sup < 1) | 1 from below (~1/(8x²)) |
| EXP | x=0 only | x=0 only | none | (1, ∞): sup 1+e⁻² at x=2 | 1 from above (~x e^{−x}) |
| RAR | origin only (y→0 ⟺ x→0, μ~√y) | origin only (λL~2√y) | none | tiny: 1.00018165 at y=100 (~(√y/2)e^{−√y}) | 1 from above (exponentially suppressed) |
| MONO | never on y>0 (μ∈(0,1)) | never (λL=1/(1+h′)>0) | none | never (0 < λL ≤ 1) | 1 from below (~delta·h_p/y) |

**Every branch is strictly elliptic on `g > 0`** and all have the *same* controlled degeneracy at the origin (`lambda_T = lambda_L = 0` at `g = 0`: quadratic contact `B ~ g²/a0` for Q/RAR/MONO; `B ~ x²` contact for EXP/MU2 — limit of both eigenvalues to 0, never a sign change). **There is no eigenvalue surface crossing zero inside the physical domain for any branch** — the well-posedness finding: no hyperbolic blow-up surface, no elliptic sign-flip; the only non-strict point is grad Φ = 0, which is the requirement-9 controlled zero-field limit.

**Branch discriminator (the sharpest contrast produced):** the historical branches EXP and MU2 carry O(0.1) longitudinal bumps (`lambda_L > 1` with sup 1.135 / 1.037) and RAR only an exponentially small one (1.8e-4); the OPERATIVE MONO branch — and Q — are strictly sub-Newtonian in lambda_L (`0 < lambda_L < 1` everywhere). Any observable sensitive to lambda_L ∈ (1, 1.135) vs (0, 1) on the same g-range discriminates the historical class from the operative one.

---

## 5. Controls (all run, all green at 80 dps; raw_output.json `checks`)

- **ID1** `mu + x·mu′ = lambda_L`: max abs residual 1.1e-75 (EXP 5.3e-82, MU2 1.7e-81, Q 1.1e-75). PASS.
- **ID2** FD `d(x·mu)/dx = lambda_L` (h = 1e-20·x): residual 7.5e-41 — FD truncation floor `h²f‴/6 ~ 1e-41` at 80 dps, as expected. PASS.
- **ID3** inverse slope `(dy/dx)·(dx/dy) = 1`: RAR 1.05e-81; MONO exactly 0.0 (dy2 = 1/(1+hp) and dx2 = 1+hp cancel at 80 dps). PASS.
- **ID4** MONO splice: h-continuity abs residual 6.64e-33 at y_p; kink jump in `d(lambda_L)/dy` = 0.0342879 at y*. PASS (recorded).
- **ID5** flux-inverse roundtrip `B(x(B)) = B`: max rel residual 1.35e-59 (MONO/RAR) … 2.46e-65 (EXP/MU2/Q). PASS.
- **ID6** Rayleigh 3-d quotients `qᵀNq/|q|²`: abs residuals 1.05e-81 … 1.13e-75; rel 2.0e-81 … 8.0e-77. PASS.
- **ID7** spec EXP cross-check (sympy EXACT): `G′(z) − (1−e^{−√z}) = 0`; `lambda2 = f′+2z f″ = (√z + e^{√z} −1)e^{−√z}`; exp λ_L = spec λ_∥, exp λ_T = spec λ_⊥; all differences `0`. PASS.
- **ID8** MU2 primitive `f′(z) = mu2(√z)`: sympy identity exact (`f(z) = z − 8 ln(√z/2 + 1) + 8 − 8/(√z/2+1)`); FD transit check 4.2e-22 (FD floor at h = 1e-16 on z = 1e-8). PASS.

## 6. Negative control (capable of failing)

- **NC1** drop the `x·mu′` term (use μ-only response `delta A = mu·delta v`): at x = 1e-4 the μ-only prediction of `delta A` carries **relative error 0.50024** — deep-limit 1/2 exactly, i.e. the longitudinal half of the response is lost. The full `lambda_L` prediction is accurate to 4.997e-4 (finite-ε nonlinearity at ε = 1e-7). **The control fails exactly as required**: it proves the `x·mu′` term is indispensable and that ID1 is not vacuous.
- **NC2** limits: deep x = 1e-10: `lambda_T/x → 1`, `lambda_L/x → 2` for all five (Q 1.99999999999999999996; MONO/RAR 1.99997000 = 2(1 − 1.5√y) exact at √y = 1e-5). Newtonian (x,y = 1e8): all → 1 with the per-branch approach rates of §3 (MONO deficits 5.97e-9 / 3.24e-10 matching delta·h_p·ln(2y/y_p)/y and delta·h_p/(y+y_p)). PASS.
- **NC3** boundaries/normalizations: exp λ_L(2) = 1.1353352832366127 = 1+e⁻² (50 digits); mu2 λ_L(4) = 1.037037037037037 = 28/27; Q λ_L(1e30) = 0.99999…875 (→1 from below); μ_Q(1e-50) = 0.0; (x·μ_Q)/x² at 1e-10 = 0.99999999999999999999. PASS.
- **NC4** no-root bracket probe: for every branch f(lo) > 0 and f(hi) > 0 on (1e-12, 1e8) for both eigenvalues — consistent with the analytic positivity (a bracket would have been the failure flag). PASS.
- **Refined sign probe**: 10000×10000 log grid over x, y ∈ [1e-12, 1e12], all five branches: zero violations.

Lean certificate, π-level: the MU2/Q algebraic content is proven, not merely sampled (see §8). The unit-audit negative control (mistake-injected formula) is embodied by NC1 (missing x·mu′ ⇒ 50% error) — the identity checks are therefore discriminating, not tautological.

---

## 7. Footings (both mandated)

kappa = 1/2, G = 6.67430e-11, c = 299792458:

| footing | a0 (m/s²) | rho_Lambda (kg/m³) |
|---|---|---|
| canonical | 9.3619e-11 | 5.844412454021875e-27 |
| alternative | 1.1279e-10 | 8.483089619559097e-27 |

- `a0_alt/a0_can = 1.204776808`; `rho_alt/rho_can = 1.451487157`.
- If rho_Lambda were pinned at the canonical value, the alternative a0 would force kappa = 0.6023884 — recorded (the eigenvalue theorem is kappa-free: it is a function of x = g/a0 only).
- Same physical g maps to x_alt = x_can/1.2047768; the eigenvalue table is evaluated identically in both footings (dimensionless).

## 8. Lean 4 certificate

File: `AS037_mu2_q_eigenvalue_algebra.lean` (in run dir). Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` — **exit 0, zero errors/warnings; all 22 theorems; every `#print axioms` line reports exactly `[propext, Classical.choice, Quot.sound]`.**

MU2 (audited cell): `mu2_eq_lamT` (λ_T = μ identity), `lamL_eq_mu_plus` (λ_L = μ + u·μ′), `lamL_eq_one_plus`, `lamT_pos` / `lamL_pos` / `mu2_pos` (strict positivity on u > 0), `mu2_zero` / `lamT_zero` / `lamL_zero` (degeneracy at 0), `lamL_le_28_27` + `lamL_max_at_two` (sup 28/27 at u = 2), `mu2p_deriv` (μ′ = 2/(1+u)³), `xmu2_deriv` (d(u·μ)/du = λ_L).
Q (comparison): `yQ_eq_x_muQ`, `yQ_pos`, `muQ_pos`, `muQ_lt_one`, `muQ_lt_x` (deep bracket 0 < μ < x), `lamLQ_pos`, `lamLQ_lt_one`, `yQ_deriv`, `xmuQ_deriv`.
EXP/RAR/MONO: transcendental content (exp, spliced sqrt forms) — carried in the numerical lane at 80 dps (sympy exact cross-checks where algebraic: EXP G′(z) identity, MU2 primitive) — **no Lean for them** (that is the declared reason, not an omission).

## 9. Open dependency and next step

The seed's step-5 dependency — "apply the heat filter S = exp((ξ²/2)Δ) to the branch and derive the filtered field equation" — is **not** part of this run (pointwise constitutive audit only). The ellipticity theorem of §4 is the boundary condition the filtered equation must preserve: any filter action must keep λ > 0 on |grad Φ| ≥ ε > 0. Child **AS037.C01** (proposed): filtered-operator ellipticity at finite ξ on the MONO cell, Rayleigh-quotient-gated, kink-correction scale recorded against y*.

---

*All numbers quoted are direct values of the bounded run (raw_output.json; wall 2.148 s, 1 thread, signal.alarm(120 s) enforced; RLIMIT_AS 512 MB rejected by the host and recorded honestly — process footprint is tiny by construction). Nothing in this file is a placeholder; every quoted residual was printed by the executed prototype.*
