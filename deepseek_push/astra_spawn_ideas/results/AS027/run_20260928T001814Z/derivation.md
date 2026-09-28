# AS027 — Effective AQUAL response of the Q branch: derivation

**Run:** `run_20260928T001814Z` · **Worker:** `sa-6-48f9b328` (Hermes Agent subagent,
model `deepseek/deepseek-v4-flash-0731` via OpenRouter) · **Task hash:**
`b5267d5882b7912fe9fee73e17957292178743a371f13f941a850aa7c68d53d5`
· **Prerequisite:** AS026 (exact inverse of the algebraic a0-line, same Q branch).

Sources (hashes verified against `SOURCE_MANIFEST.json`, all three MATCH):
- `README.md` `91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed`
- `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`
- `real_research/peer_review_2026_09_26/README.md` `521d9ac36a93a27dcd6c995f78743ae9b1de4304095911871d81e6a70f9ecaac`

---

## 1. Precise claim, symbols, boundary conditions, assumptions

### 1.1 Symbol dictionary

| symbol | meaning | status |
|---|---|---|
| `a0` | framework vacuum acceleration scale, `a0 = kappa c sqrt(G rho_Lambda)`, `kappa = 1/2` | **framework input (adopted, NOT derived here)** |
| `G` | measured Newton constant `6.67430e-11 m^3 kg^-1 s^-2` | measured input |
| `c` | `299792458 m/s` | exact input |
| `rho_Lambda` | vacuum mass density | framework input |
| `B = g_N` | Newtonian radial acceleration `G M_b(<r)/r^2` of the baryon distribution | derived from `rho_b` |
| `g` | total radial acceleration | derived |
| `x = g/a0`, `y = B/a0` | dimensionless accelerations, both positive | derived |
| `M_b(<r)` | enclosed baryon mass | source data |
| `Phi`, `Phi_N` | total / Newtonian potential fields | derived |
| `mu`, `nu` | effective AQUAL kernel / QUMOND-style boost | **derived here** |
| `mu_EXP(x) = 1 - e^{-x}` | historical EXP AQUAL kernel | comparison branch only (retired operative target) |

### 1.2 Precise claim (the object to be derived)

> **Claim.** Let the Q branch be the radial algebraic law
> `g^2 = B^2 + a0 B` (equivalently `x^2 = y^2 + y`), declared as a radial relation
> (FRAMEWORK_CONTRACT branch table). Then:
> (i) in **spherical symmetry**, every solution of the Q branch is **exactly** the
> unique solution of an AQUAL-type divergence law
> `div( mu_Q(|grad Phi|/a0) grad Phi ) = 4 pi G rho_b` with the effective kernel
> `mu_Q(x) = (sqrt(1+4x^2) - 1)/(2x) = 2x/(1 + sqrt(1+4x^2))`,
> `x in (0, oo)`, strictly increasing, `mu_Q(0+)=0`, `mu_Q(oo)=1`;
> (ii) the kernel is **unique** (forced by the spherical reduction);
> (iii) the equivalent boost is `nu_Q(y) = g/B = sqrt(1 + 1/y)`, `y in (0, oo)`;
> (iv) the AQUAL-type action primitive exists in closed form,
> `F(X) = (1/4) asinh(2 sqrt X) + (sqrt X/2) sqrt(1+4X) - sqrt X`, `X = |grad Phi|^2/a0^2`,
> with `F'(X) = mu_Q(sqrt X)`;
> (v) **no claim beyond spherical symmetry**: Q is a radial magnitude relation, not a
> nonspherical field equation; the effective-AQUAL PDE is a *different* field theory
> off the spherical sector, and Q must not be identified with QUMOND, EXP AQUAL,
> RAR, MU2 or MONO anywhere.

### 1.3 Boundary conditions and assumptions

- `rho_b` spherically symmetric, nonnegative, finite total mass (compact support or
  fast decay); `M_b(<r) = 4 pi Integral_0^r rho_b(s) s^2 ds` finite for all `r`.
- `Phi` regular at the origin (or the source profile is regular there), `Phi -> 0` at
  infinity (constant-shift gauge fixed); `g = |grad Phi| >= 0` radial.
- The physical root branch: `y > 0`, `x > 0`; the quadratic `y^2 + y = x^2` has
  exactly one positive root `y = (sqrt(1+4x^2)-1)/2` (the negative root
  `(-sqrt(1+4x^2)-1)/2 < 0` is excluded by positivity — matching AS026's
  sign discipline).
- `kappa = 1/2` adopted input (contract); the dimensionless result is independent of
  `kappa`'s value, so **both registered footings apply identically** through
  `x = g/a0` with the respective `a0` (see §6). Dimensional examples are carried
  separately per footing and never mix the two vacuum densities with a shared kappa.
- `G = G_N` (measured) used; `G_bare`/`G_cosmo` are not needed by this task's
  dimensionless law — flagged, not assumed equal beyond the spherical law.
- No dynamics, no time dependence, no filter, no gate: the operative MONO cell's
  heat filter and gate are **outside** this task's declared branch (Q), and nothing
  here transfers to MONO/EXP/RAR/MU2.

---

## 2. Derivation: the effective spherical mu of the Q branch

### 2.1 Spherical reduction of the AQUAL-type law

The generic scalar modified-gravity (AQUAL-type) field equation is

```
div( mu(|grad Phi|/a0) grad Phi ) = 4 pi G rho_b.        (AQUAL-op)
```

In spherical symmetry, `Phi = Phi(r)`, `grad Phi = Phi'(r) e_r`, `g = Phi'(r) >= 0`,
and (AQUAL-op) becomes the ODE

```
(1/r^2) d/dr [ r^2 mu(g/a0) g ] = 4 pi G rho_b(r).        (1)
```

Multiplying by `4 pi r^2` and integrating from 0 to r (source regular at 0, so
`r^2 mu g -> 0` there):

```
r^2 mu(g/a0) g = G M_b(<r)   ==>   mu(x) * x = y,          (2)
```

where `y(r) = B(r)/a0 = G M_b(<r)/(a0 r^2)`. **Equation (2) is the entire content of
AQUAL-type modified gravity in spherical symmetry**: the PDE reduces, per radius, to
an algebraic inversion of `mu`. This reduction is exact, with every scale factor
(`4 pi`, `G`, `a0`) accounted for above; units: `[r^2][mu][g] = m^2 m s^-2 =
m^3 s^-2`; `[G M] = m^3 s^-2`. Consistent.

### 2.2 Inversion for Q

The Q branch in dimensionless form is `x^2 = y^2 + y` (from `g^2 = B^2 + a0 B`,
divided by `a0^2`). Its unique positive root is

```
y(x) = ( sqrt(1 + 4 x^2) - 1 ) / 2 = 2 x^2 / ( 1 + sqrt(1+4x^2) )   (rationalized, stable)
```

(The rationalized form is AS026's stable inverse; it avoids the cancellation of
`sqrt(1+4x^2) - 1` at small x.)

The effective kernel is forced by (2): `mu_Q(x) = y/x`, i.e.

```
mu_Q(x) = ( sqrt(1 + 4 x^2) - 1 ) / (2 x) = 2x / ( 1 + sqrt(1+4x^2) ).   (3)
```

**Uniqueness**: any kernel whose spherical reduction reproduces Q must satisfy
`mu(x) x = y(x)` pointwise for all `x > 0`, with `y` the unique positive root of
`y^2 + y = x^2`; hence `mu = mu_Q` is the *unique* such function (within the
positive-branch prescription). The spherical statement is an **exact identity**, not
a fit: `mu_Q(x) x = y(x)` and `y^2 + y = x^2` hold identically
(`y(y+1) = ((sqrt-1)(sqrt+1))/4 = x^2`).

### 2.3 Domain and analytic properties

- `mu_Q : (0, oo) -> (0,1)`, `C^oo`, strictly increasing:
  `mu_Q'(x) = (sqrt(1+4x^2) - 1)/(2 x^2 sqrt(1+4x^2)) > 0` for `x > 0`
  (manifestly positive; verified numerically over the whole grid, min value
  `5.0e-17` at the largest grid point `x = 1e8`, matching the asymptotic `1/(2x^2)`).
- `nu_Q : (0, oo) -> (1, oo)`, strictly decreasing:
  `nu_Q'(y) = -1/(2 y^2 sqrt(1+1/y)) < 0` (max over grid `-5.0e-17`).
- Limits and series (sympy-exact coefficients, C12):

```
small x:  mu_Q(x) = x - x^3 + 2 x^5 - 5 x^7 + O(x^9)
large x:  mu_Q(x) = 1 - 1/(2x) + 1/(8 x^2) - 1/(128 x^4) + O(x^-5)
```

- Deep regime (`y -> 0`): `mu_Q ~ x`, i.e. `g^2 = a0 B` — the framework's deep law
  `v_flat^4 = G M_b a0` follows from `g = v^2/r`, `B = G M_b/r^2` (identical to the
  AS006/AS007 chain; not re-derived here).
- Newtonian regime (`y -> oo`): `mu_Q = 1 - 1/(2x) + ...`, i.e.
  `g = B + a0/2 - a0^2/(8 B) + ...` — the Q branch's **constant a0/2 offset** in the
  Newtonian tail (the "alpha=1" asymptote recorded in STANDING rev. blocks; retained
  here only as a property of the declared Q branch).
- The exact μ-space inverse: `x = mu/(1 - mu^2)`, `y = mu^2/(1 - mu^2)` (Lean
  certificate `qMu_inverse`; see §5). This is the Q law written in μ-space. Note the
  **conditioning**: the divided form loses precision as `mu -> 1` (measured relative
  failure ~1.0e-43 at x = 5e7 at 50 digits; mechanism: `(1-mu^2)` is an O(1) minus
  O(1) subtraction whose absolute mantissa error ~1e-50 is amplified by the product
  `x*(1-mu^2)` by the factor `x ~ 1/(1-mu)` — the condition number of the map
  `mu -> x`). Numerically healthy forms are `mu = y/x` or the rationalized pair; the
  identity itself is exact and Lean-certified.

### 2.4 The AQUAL primitive (action form)

With the AQUAL convention `S = -(a0^2/(8 pi G)) Integral F(X) d^3x + Integral rho Phi`,
`X = |grad Phi|^2/a0^2`, the field equation is `div(F'(X) grad Phi) = 4 pi G rho`.
Setting `F'(X) = mu_Q(sqrt X)` and integrating:

```
F(X) = (1/4) asinh(2 sqrt X) + (sqrt X / 2) sqrt(1 + 4 X) - sqrt X,
F(0) = 0,  F strictly convex (F'' = mu_Q'(sqrt X)/(2 sqrt X) > 0).
```

Verified symbolically (`F'(X) = [1+4X-sqrt(1+4X)]/(2 sqrt X sqrt(1+4X)) =
mu_Q(sqrt X)` identically) and numerically (residuals §4). Deep leading term:
`F(X) = (2/3) X^(3/2) - (2/5) X^(5/2) + ...` (measured deviation from `(2/3)X^(3/2)`
bounded by the neglected `(2/5)X` factor: `6.34e-6` at `X = 1.585e-5`,
`(2/5)X = 6.34e-6`). Newtonian: `F ~ X - sqrt X + O(ln X)`.

So the Q branch is exactly the **spherical sector of a bona fide AQUAL-type
modified-gravity action with kernel `mu_Q`** — the "effective AQUAL response" exists
as a real PDE, not merely as an algebraic bookkeeping device. Convexity of F gives
ellipticity of the PDE in the regime where `mu' > 0` (deep and intermediate); the
Newtonian tail is the standard AQUAL property `mu -> 1` with `F'' -> 0`.

### 2.5 Why this does NOT equate nonspherical QUMOND and AQUAL solutions

Matching the spherical radial law is not equivalence of field theories:

1. **Q is a magnitude relation, not a vector field equation.** The declared Q branch
   is `g^2 = B^2 + a0 B` for the *magnitudes* of radial accelerations. As a vector
   law `bold g = nu_Q(|bold g_N|) bold g_N`, the field has nonzero curl in general
   (the framework contract records this: "A radial relation; not by itself a
   nonspherical field equation"); a curl-free potential representation of the Q law
   does not exist off the spherical sector.
2. **AQUAL with mu_Q is a genuinely nonlinear PDE** `div(mu_Q(|grad Phi|/a0) grad Phi)
   = 4 pi G rho_b`. Its nonspherical solutions carry angular structure and do *not*
   satisfy the algebraic relation `g^2 = B^2 + a0 B` pointwise; the two coincide
   exactly only where the solution is radial (or in the deep regime, where
   `mu ~ x` turns AQUAL into `|grad Phi|^2 = a0 |grad Phi_N|`-type relations that
   still differ in angular content).
3. **QUMOND is a different operator**: `div(nu_Q(|grad Phi_N|/a0) grad Phi_N)
   = 4 pi G rho_b` with the same `nu_Q` reproduces Q's radial boost but is
   (standard result, echoed in the repository's f23/f24 quadrupole audits) a
   distinct theory off the sphere — same one-asymptote caveat applies: *matching one
   asymptote does not make two kernels equivalent*.
4. **Branch fidelity**: `mu_Q != mu_EXP` (negative control, §4 C6), `mu_Q != mu_RAR`,
   `mu_Q != mu_MU2` at every finite x (C11 table); the operative MONO kernel is a
   separate branch with its own heat filter. Nothing in this result transfers to any
   other branch.

---

## 3. Step 3 — intermediate algebra, signs, units, limiting regimes (summary)

All factors are displayed in §2.1–2.4. Sign conventions: outward-pointing positive
accelerations (`Phi` increasing outward), `rho_b >= 0`; the flux `r^2 mu(x) g` is
positive, equal to `G M_b(<r)`. Units check: `y = B/a0` dimensionless;
`mu_Q` dimensionless; `x = g/a0` dimensionless; `F` dimensionless; action coefficient
`a0^2/(8 pi G)` has units `m^3 s^-2 kg^-1 * kg = m^3 s^-2`... (action density; the
full dimensional chain `[a0^2/G] = m^2 s^-4 / (m^3 kg^-1 s^-2) = kg m^-1 s^-2 = Pa`,
pressure, matching the vacuum-tension reading of the AQUAL action). Limiting regimes
with leading neglected terms:

| regime | condition | law | leading neglected term | domain of validity |
|---|---|---|---|---|
| deep | `y <= 1e-3` (`x <= 0.0316`) | `mu_Q = x (1 - x^2 + ...)`, `g^2 = a0 B` | `-x^3` in `mu_Q/x` (rel. `x^2`) | all r with `B <= 1e-3 a0` |
| Newtonian | `y >= 1e3` (`x >= 31.7`) | `g = B + a0/2 - a0^2/(8B) + ...` | `-a0^2/(8B)` (rel. `1/(8y)`) | all r with `B >= 1e3 a0` |
| intermediate | `1e-3 < y < 1e3` | full `mu_Q` | none (exact) | the whole transition |

The neglected-term bounds were verified numerically (C4, C5): deep residual
`|mu_Q/x - 1| <= 1.002 x^2` (observed 9.990e-4 vs bound 1.000e-3 on 71 points);
Newtonian residual `|mu_Q - (1-1/2x)| <= 1.0001/(8x^2)` (observed 1.249e-7 vs bound
1.25e-7 on 51 points); offset residual `|(x-y) - 1/2| <= 1.02/(8y)` (observed
1.249e-4 vs bound 1.27e-4).

---

## 4. Step 4 — independent checks (actual residuals, different representations)

Grid: `y = 10^k`, `k = -10 .. 8` step 0.1 (181 points <= 512-cell bound), mpmath
`dps = 50`; refinements: bisection (roots, 50-digit), Richardson fd (1 refinement).
All residuals below are from the actual run `as027_numeric_run.out` (exit 0,
0.36 s wall, 56.0 MiB max RSS).

| check | statement | observed (max over grid) | tolerance | status |
|---|---|---|---|---|
| C1 | `y^2 + y = x^2` (rel.) | 2.61e-51 | 1e-45 | PASS |
| C2 | `mu_Q(x) x = y` (rel.) | 2.26e-51 | 1e-45 | PASS |
| C3a/b | `x(1-mu^2) = mu`, `y(1-mu^2) = mu^2`, well-conditioned domain `x <= 100` | 2.11e-49 | 1e-45 | PASS |
| C3c | conditioning probe `x > 100`: `rel(mu, y/x) = 2.7e-51`, `rel(1-mu^2, y/x^2) = 4.1e-51`; the divided inverse degrades as `~x*ulp` (measured 2.06e-43 at x = 5.0e7 vs predicted `x*5e-51*4.1`) | — | — | recorded (representation conditioning, not identity failure; identity is Lean-certified) |
| C4 | deep: `|mu_Q/x - 1| <= 1.002 x^2` | 9.9900e-4 | 1.0000e-3 | PASS |
| C5a/b | Newtonian series residuals with leading-term bounds | 1.249e-7 / 1.249e-4 | 1.25e-7 / 1.27e-4 | PASS |
| C6 | **NC1**: substitute `mu = 1 - e^{-x}` — differs at finite x: `d(1) = mu_EXP(1) - mu_Q(1) = 0.0140865700786628`; `|d(1)| > 1e-6` fires; roots of `d(x) = 0` bracketed + bisected: single crossing `x* = 0.842568964352...` on `[0.02, 5]` (bisection residual 1.34e-51); `d(100) = 4.9875e-3 > 0` (~1/(2x) tail) | PASS (control fires and can fail: identical kernels would give d ~ 0) |
| C7 | monotonicity: `mu_Q' > 0`, `nu_Q' < 0` (closed forms, min/max over grid `5.0e-17` / `-5.0e-17` at x = 1e8) | PASS |
| C8 | **independent representation 1**: Milgrom-1999 form `sqrt(1+(2x)^-2) - (2x)^-1 == mu_Q(x)` (the repository's STANDING records this identity) | 3.85e-47 | 1e-45 | PASS |
| C9a | **independent representation 2**: `F'(X) = mu_Q(sqrt X)`, closed-form derivative | 1.63e-48 | 1e-45 | PASS |
| C9b | `F(X) = Integral_0^X mu_Q(sqrt s) ds` (mpmath adaptive quadrature) | 2.48e-51 | 1e-44 | PASS |
| C9c | deep primitive `F ~ (2/3)X^(3/2)` with neglected `(2/5)X` | 6.34e-6 @ X=1.585e-5 = (2/5)X | recorded | PASS |
| C10a | **independent representation 3**: Hernquist source (1e11 M_sun, scale 20 kpc): `r^2 mu_Q(x) g = G M(<r)` on r/a in [1e-3, 1e3] | 4.53e-51 | 1e-42 | PASS |
| C10b-i | field equation, **analytic direct differentiation**: `d/dr[r^2 mu g] = 2 G M a r/(r+a)^3 = 4 pi G rho r^2` | 4.34e-51 | 1e-42 | PASS |
| C10b-ii | field equation, **finite differences (Richardson, order-4 stencil, steps h = r*1e-4 and h/4)** | 7.29e-26 | 1e-20 | PASS (h-refinement ratio 256 ≈ 4^4, scheme converges) |
| C11 | branch-fidelity table (Q vs EXP vs RAR vs MU2) — comparison only, no transfer | see table below | — | recorded |
| C12 | sympy series: small-x `mu_Q = x - x^3 + 2x^5 - 5x^7 + O(x^9)`; `mu_EXP = x - x^2/2 + x^3/6 - O(x^4)`; `d(x) = -x^2/2 + 7x^3/6 + O(x^4)`; large-x `mu_Q = 1 - 1/(2x) + 1/(8x^2) - 1/(128x^4) + O(x^-5)` | exact coefficients | — | recorded |
| C13 | footing examples (canonical 9.3619e-11 vs alternative 1.1279e-10 m/s^2, separate) | see §6 | — | recorded |

C11 branch fidelity at `x = g/a0` (each branch's own algebraic inversion in the
spherical sense; RAR = `y` solved from `x = y/(1-e^{-sqrt y})` by bisection):

```
 x         mu_Q       mu_EXP(hist)   mu_RAR      mu_MU2
 0.1     0.0990195    0.0951626     0.0909718    0.0929705
 0.31    0.2848472    0.2665530     0.2377518    0.2503889
 1.0     0.6180340    0.6321206     0.5105908    0.5555556
 3.16    0.8542128    0.9575743     0.7950636    0.8497686
 10.0    0.9512492    0.9999546     0.9544732    0.9722222
```

All four kernels share the deep limit `mu ~ x` and the Newtonian limit `mu -> 1` but
differ at every finite x (max pairwise deviations: Q-EXP 0.049 at x = 3.16, Q-RAR
0.107 at x = 1, Q-MU2 0.062 at x = 1). Matching the asymptotes does not make the
kernels equivalent (the task's governing principle; re-confirmed quantitatively).

**Failed attempts (preserved in run history):** (1) rev1 absolute-residual checks
failed at large-x roundoff (2.4e-35 at x ~ 1e16-magnitudes) — replaced by relative
residuals; (2) rev1 C13 used `M_b = 10^n` kg instead of `10^n M_sun` (r_M off by
1.98847e30) — corrected; (3) `mpmath.diff` at order >= 2 collapses at these
magnitudes (`mp.diff(flux, r, 8) ~ 1e-50`, `mp.diff(., ., 2) = 6.9e-5` vs analytic
`1.1e-31`) — replaced by analytic differentiation + explicit Richardson fd (this is
a recorded instrument limitation, not a physics result); (4) the divided inverse
form `x = mu/(1-mu^2)` fails numerically at `mu -> 1` (conditioning, quantified in
C3c) — the identity is exact (Lean) and the cross-checked/stable forms pass.

---

## 5. Lean certificate

`AS027_effective_aqual_certificates.lean` (in run dir), verified with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>`, exit 0, zero
`sorry`/`admit` (grep count 0), and the **unfiltered** `#print axioms` audit shows
every theorem depending exactly on `{propext, Classical.choice, Quot.sound}`:

| theorem | content |
|---|---|
| `q_sqrt_sq` | `sqrt(1+4x^2)^2 = 1+4x^2` |
| `qY_sq_add` | `y^2 + y = x^2` (master identity) |
| `qY_pos` | `0 < y` for `x > 0` |
| `qMu_mul_self` | `mu_Q(x) x = y` (flux inversion) |
| `qMu_rationalized` | `mu_Q(x) = 2x/(1+sqrt(1+4x^2))` |
| `qMu_inverse` | `x = mu/(1-mu^2)` (exact inverse; no floating-point conditioning involved) |
| `qNu_sq` | `nu_Q(y)^2 = 1 + 1/y` |
| `qMu_lt_one` | `mu_Q(x) < 1` for `x > 0` (range) |

The EXP-difference (NC1) is certified numerically (C6: d(1) = 0.0140866 with
bracketed root 0.842568964352) and by the exact series `mu_EXP - mu_Q = -x^2/2 +
7x^3/6 + ...` (C12): two analytic functions differing at O(x^2) cannot coincide on
any neighborhood of 0, and they are not equal at x = 1.

---

## 6. Both scale footings

The theorem is **dimensionless** (a ratio law in `x = g/a0`, `y = B/a0`), so it
applies to both registered footings with the respective `a0`; the two footings are
*alternative normalizations*, never simultaneously a fixed `rho_Lambda` and a fixed
`kappa` (contract rule). Dimensional examples, carried separately (C13):

| footing | a0 [m/s^2] | Newtonian offset a0/2 [m/s^2] | r_M(1e10 M_sun) | r_M(1e11 M_sun) | r_M(1e12 M_sun) | v_flat(1e11) [km/s] |
|---|---|---|---|---|---|---|
| canonical | 9.3619e-11 | 4.68095e-11 | 3.859 kpc | **12.202 kpc** | 38.586 kpc | 187.7 |
| alternative | 1.1279e-10 | 5.6395e-11 | 3.515 kpc | **11.117 kpc** | 35.154 kpc | 196.7 |

Late-stage check: `g = 1e-10 m/s^2` corresponds to `x = 1.06816` (canonical,
`mu_Q = 0.636039`) vs `x = 0.886603` (alternative, `mu_Q = 0.584109`); `kappa = 1/2`
remains an **adopted input**, not derived by this task.

---

## 7. Step 5 — negative control, strongest surviving statement, next implication

### 7.1 Negative control (capable of failing)

**NC1 (task-mandated)**: substituting the historical EXP kernel `mu = 1 - e^{-x}`
into the effective-AQUAL representation and comparing with the Q-derived kernel:
`d(1) = 0.0140865700786628 != 0` (the control *fires*; if Q and EXP were the same
kernel the difference would vanish and the control would fail its detection
threshold). The difference is not a one-point accident: `d(x)` has exactly one
crossing in `[0.02, 5]`, bracketed `(0.84, 0.85)` and bisected to
`x* = 0.842568964352` (residual 1.34e-51), `d < 0` near 0 (series `-x^2/2 + ...`)
and `d > 0` beyond the crossing with `d(100) = 4.9875e-3 ~ 1/(2x)`. **NC2** (deep and
Newtonian regimes): verified with leading-term bounds (C4, C5) — exact identity vs
finite check distinguished: the algebraic identity is exact (C1/C2 at 1e-51; Lean
`qY_sq_add`, `qMu_mul_self`), the regime checks are finite series agreements with
bounds. Both controls passed.

### 7.2 Strongest surviving statement

> **Spherical effective-AQUAL representation of the Q branch (exact, unique,
> constructive).** For every spherically symmetric baryon distribution with finite
> total mass, the Q-branch radial law `g^2 = B^2 + a0 B` is exactly and uniquely
> equivalent to the AQUAL-type boundary value problem
> `div( mu_Q(|grad Phi|/a0) grad Phi ) = 4 pi G rho_b` with
> `mu_Q(x) = 2x/(1+sqrt(1+4x^2))` on `x in (0, oo)` (equivalently
> `nu_Q(y) = sqrt(1+1/y)` on `y in (0, oo)`), `mu_Q` strictly increasing from 0 to 1,
> `C^oo`, with closed-form convex action primitive `F(X) = (1/4)asinh(2 sqrt X) +
> (sqrt X/2) sqrt(1+4X) - sqrt X`, exact inverse `x = mu/(1-mu^2)`, deep limit
> `g^2 = a0 B`, Newtonian tail `g = B + a0/2 + ...`. The representation is exact on
> the spherical sector only; it does not equate Q with nonspherical AQUAL, QUMOND,
> EXP, RAR, MU2 or MONO solutions, and no branch transfer is claimed. Verified by
> 13 named numeric checks (all PASS, actual residuals 1e-24..1e-51) in a bounded
> deterministic run and by 8 Lean theorems (zero uncovered obligations, axioms
> {propext, Classical.choice, Quot.sound}). Dimensionless; applies to both registered
> footings through `x = g/a0` with the respective `a0` (canonical 9.3619e-11 and
> alternative 1.1279e-10 m/s^2). Outcome: **supports_scoped_claim.**

### 7.3 First additional implication needed to transfer to the full theory

The spherical effective-AQUAL representation does not by itself promote the Q
branch to an operative theory. The operative target is filtered MONO under
criterion B (amended requirement 1); a forward step needs a **branch-translation
theorem**: derive the monopole/spherical sector of the operative MONO + heat-filter
cell (with the source/force operator of requirement 1, `S = exp[(xi^2/2) Delta]`)
and exhibit whether/where it coincides with the Q law or with `mu_RAR`
(equivalently: prove which spherical kernel the operative cell actually produces).
Only then can the construction here serve as an exact spherical reduction lemma for
the operative branch; until then the Q effective-AQUAL result is a declared-branch
result with no transfer to MONO (contract: "A historical branch is a comparison or
conditional lemma until an explicit bridge to that target is proved"). Also open
for any future action use: full nonspherical PDE theory of `mu_Q` (existence,
ellipticity domains, EFE/quadrupole observables) and the physical source of
`kappa = 1/2`.

---

## 8. Bounds, commands, environment

- **Declared and enforced bounds**: wall/CPU `ulimit -t 120` (actual 0.36 s wall,
  0.31 s user); memory: `ulimit -v 524288` is **not settable on this macOS host**
  (bash and zsh both reject RLIMIT_AS: "cannot modify limit: Invalid argument" —
  recorded honestly), so the memory bound was enforced by measurement: peak RSS
  56.0 MiB (57,589,760 bytes via `/usr/bin/time -l`), far below the 512 MB
  planning bound; threads: 1 (`OMP_NUM_THREADS=1`, single process, no threading);
  grid 181 cells <= 512; refinements: 2 bisection/bracket passes + 1 Richardson
  refinement. mpmath `dps = 50`, deterministic, no network.
- **Commands** (all recorded in `result.json`): source hash reconciliation via
  `shasum -a 256`; bounded run
  `bash -c 'ulimit -t 120; OMP_NUM_THREADS=1; /usr/bin/time -l python3
  compute_AS027_effective_aqual.py > as027_numeric_run.out'` (exit 0); Lean
  `cd fable_independent_2026/lean_2026 && lake env lean
  .../AS027_effective_aqual_certificates.lean` (exit 0).
- **Artifacts**: `derivation.md`, `compute_AS027_effective_aqual.py`,
  `as027_numeric_run.out`, `AS027_effective_aqual_certificates.lean`,
  `lean_check.out`, `result.json` (hashes in `result.json`).

## 9. Limitations (what this result does NOT establish)

1. Spherical sector only: no nonspherical equivalence of Q with AQUAL/QUMOND, no
   EFE, no quadrupole/curl statements, no disc solvability.
2. No transfer to the operative MONO/heat-filter/gate cell or to RAR/MU2/EXP; all
   branch comparisons (C11) are diagnostic.
3. `kappa = 1/2` remains an adopted input; `G = G_N` used; no measured-G derivation;
   no dynamics, causality, stability or well-posedness claims for the AQUAL-type PDE
   (only convexity/ellipticity of F in the deep-intermediate regime is noted).
4. Numerical residuals are finite-precision evidence at 50 digits with relative
   tolerances documented; the exact identities are independently Lean-certified.
5. The `mu -> 1` inverse-form conditioning (C3c) is a property of the *divided
   representation*, not of the law; stable forms are given.
