# AS029 — MU2 Implicit Force Cubic: derivation

**Run:** `AS029_r1_dsv4flash_20260928T001410Z`
**Worker:** DeepSeek-V4-Flash-0731 via Hermes Agent subagent (platform: subagent, model `deepseek/deepseek-v4-flash-0731` on openrouter)
**Task:** `deepseek_push/astra_spawn_ideas/AS029_mu2_implicit_force_cubic.md` (task_sha256 `127783c7c036db5927e1c968b089102d1c67432d1a73b9fabbe01de88ff808b3`)
**Branch:** MU2 (comparison branch only; operative target is filtered `nu_mono` with causality criterion B — never identified with MU2).
**Framework input (adopted, not derived here):** `a0 = kappa * c * sqrt(G * rho_Lambda)`, `kappa = 1/2`.
**Status:** supports_scoped_claim — 29/29 checks PASS, exit 0; Lean certificate compiles with axioms ⊆ {propext, Classical.choice, Quot.sound}, zero `sorry`.

---

## 0. Symbol dictionary and claim

| Symbol | Meaning | Status |
|---|---|---|
| `x = g/a0` | normalized total radial acceleration | dimensionless |
| `y = B/a0` | normalized Newtonian/baryonic acceleration `B = g_bar` | dimensionless |
| `mu2(x) = 1 - (1 + x/2)^(-2)` | MU2 kernel (spec: `mu=1-(1+g/(2 a0))^-2`) | branch input |
| `B = mu2(x) * g` | implicit response relation | branch input |
| `a0` | `kappa c sqrt(G rho_Lambda)`, `kappa = 1/2` | adopted framework input |
| `G = 6.67430e-11 m^3 kg^-1 s^-2`, `c = 299792458 m/s` | numerics | framework convention |

**Claim (proved exactly, Lean-certified):** for every `y > 0` the implicit MU2 response `y = x*mu2(x)` on the physical domain `x > 0` is algebraically equivalent to the cubic
`P_y(x) = x^3 + (4 - y) x^2 - 4 y x - 4 y = 0`,
which has exactly three distinct real roots: exactly one positive root `x*(y)`, in the explicit bracket `y < x*(y) < y + 4`; the other two roots lie in `(-(y+4), -2)` and `(-2, 0)`. The discriminant is positive for all `y > 0`. The map `y ↦ x*(y)` is strictly increasing, `mu2` is strictly increasing on `x > 0` with range `(0, 1)`, and `B ↦ g` is therefore a bijection `(0,∞) → (0,∞)` (surjectivity lane: unbounded `yFwd` plus the exact inversion asymptotics below, verified numerically and algebraically on the diagnostic grid — the Lean side certifies strict monotonicity; surjectivity onto `(0,∞)` is carried by the Python lane data).

The claim is dimensionless; both footings apply by rescaling (see §8).

---

## 1. Step 1 — premises, boundary conditions, assumptions (task step 1)

- **Framework input:** `a0 = kappa c sqrt(G rho_Lambda)`, `kappa = 1/2` ADOPTED (never re-derived here; the task does not supply an independent derivation of `kappa`).
- **Branch equation (input):** `mu2(x) = 1 - (1 + x/2)^(-2)`; response `mu2(x) g = B`, i.e. `y = x * mu2(x)`.
- **Domain:** `x > 0`, `y > 0`. Boundary cases: `y → 0+` (deep MOND) and `y → ∞` (near-Newtonian) are limits of the same exact relation, not separate laws.
- **Distinctness assumption (criterion B MONO operative):** MU2 is a *comparison* branch. No conclusion in this file is transferred to MONO/RAR/Q/EXP; the deep asymptote of MU2 is explicitly **different** from RAR and Q (see §9), so branch monotonicity is maintained.
- **No extra assumptions:** the derivation introduces no free parameters; `kappa`, `G`, `c` fixed as above.

---

## 2. Step 2 — clearing denominators: the cubic (task step 2)

Start from the defining response:

```
y = x * mu2(x) = x * [1 - (1 + x/2)^(-2)]
```

Clear the negative power (`x ≠ -2`, automatic on `x > 0`):

```
(1 + x/2)^(-2) = [ (x+2)/2 ]^(-2) = 4/(x+2)^2
```

so

```
mu2(x) = 1 - 4/(x+2)^2 = [ (x+2)^2 - 4 ] / (x+2)^2 = x(x+4)/(x+2)^2
```

and the response becomes the exact rational identity

```
y = x*mu2(x) = x^2 (x+4) / (x+2)^2          (Eq. F, "forward map")
```

Multiplying by `(x+2)^2 ≠ 0`:

```
y (x+2)^2 = x^2 (x+4)
=> x^3 + (4 - y) x^2 - 4 y x - 4 y = 0     (Eq. C, the cubic)
```

**Dimensional form** (x = g/a0, y = B/a0, multiply by a0^3):

```
g^3 + 4 a0 g^2 - B g^2 - 4 B a0 g - 4 B a0^2 = 0
```

(sympy-verified: `-4*B*a0**2 - 4*B*a0*g - B*g**2 + 4*a0*g**2 + g**3`).

**Equivalence is exact on the physical domain:** for `x > 0, y > 0`,

```
y = x*mu2(x)   ⟺   P_y(x) = 0             (Lean: implicit_eq_cubic, cubic_iff_forward)
```

### Root structure — existence, bracketing, uniqueness

**Bracketing values (exact):**

| point | P_y value | sign for y > 0 |
|---|---|---|
| `x = y` | `-4y` | < 0 |
| `x = y+4` | `4y^2 + 44y + 128 = 4(y^2 + 11y + 32)` | > 0 |
| `x = -2` | `8` | > 0 |
| `x = 0` | `-4y` | < 0 |
| `x = -(y+4)` | `-2y(y^2 + 6y + 10)` | < 0 |

**Existence (IVT):** `P_y` is continuous; `P_y(y) < 0 < P_y(y+4)` ⇒ a root in `(y, y+4)`; `P_y(-(y+4)) < 0 < P_y(-2)` ⇒ a root in `(-(y+4), -2)`; `P_y(-2) > 0 > P_y(0)` ⇒ a root in `(-2, 0)`. (Lean: `exists_root_bracket`, `two_neg_roots`.)

**No positive root outside the bracket (sign bounds):**

```
P_y(x) = x(x+4)(x-y) - 4y
```

- `0 < x ≤ y`: `x(x+4)(x-y) ≤ 0` and `-4y < 0` ⇒ `P_y < 0`.
- `x ≥ y+4`: `x(x+4) ≥ 0`, `x - y ≥ 4` ⇒ `P_y ≥ 4x(x+4) - 4y = 4(x^2 + 3x + 4) + 4(x - y - 4) > 0`.

(Lean: `Pyl_lt_zero_low`, `Pyl_pos_high`, `pos_root_in_bracket`.)

**Uniqueness of the positive root (strict increase on the bracket):** for two points `x1 < x2` in `(y, y+4)`,

```
P_y(x2) - P_y(x1) = (x2 - x1) * Q,   Q = x1^2 + x1 x2 + x2^2 + (4-y)(x1+x2) - 4y
```

and on `x1, x2 > y > 0` the bracket `Q` factors into manifestly positive pieces:

```
Q = x1(x1 - y) + x2(x2 - y) + x1 x2 + 4(x1 + x2) - 4y > 0
```

so `P_y` is strictly increasing on `[y, y+4]`; at most one root there. (Lean: `Qbr_pos`, `Pyl_sub`, `unique_root_bracket`.)

**Exact count — exactly three distinct real roots.** Three distinct roots are exhibited (positive in `(y, y+4)`, two negative in `(-(y+4), -2)` and `(-2, 0)` — the intervals are disjoint, so all three are distinct). `deg P_y = 3` bounds `roots.card ≤ 3` (Lean: `Ppoly_coeff3`, `Ppoly_degree_le`, `Polynomial.card_roots`), hence `roots.card = 3` and every real root is one of the three (Lean: `roots_card_eq_three`, `root_iff_three`).

**Discriminant.** For `a x^3 + b x^2 + c x + d`, Δ = b²c² − 4ac³ − 4b³d − 27a²d² + 18abcd; with `(a,b,c,d) = (1, 4-y, -4y, -4y)`:

```
Δ_x = 16 y (2 y^2 + 13 y + 64) > 0   for all y > 0      (Lean: cubic_discriminant_identity, cubic_discriminant_pos)
```

**Dimensional discriminant:** `Δ_g = 16 B a0^3 (2 B^2 + 13 B a0 + 64 a0^2) > 0` (sympy-verified; units m¹²·s⁻⁶ — consistent with a cubic in g).

## 3. Step 3 — intermediate algebra, signs, units, limiting regimes (task step 3)

**All exact identities (sympy-verified, no floating point involved):**

```
mu2(x) = 1 - 4/(x+2)^2
y(x)   = x^2 (x+4)/(x+2)^2
x - y  = 4x/(x+2)^2          (exact bracketing identity: y < x < y+4)
dy/dx  = x (x^2 + 6x + 16)/(x+2)^3 > 0   on x > 0
dmu2/dx = 8/(x+2)^3 > 0
```

**Small-x (deep MOND) expansion of the forward map:**

```
y(x) = x^2 - (3/4) x^3 + (1/2) x^4 - (5/16) x^5 + O(x^6)
```

**Deep inversion (leading term + first correction):**

```
x(y) = sqrt(y) + (3/8) y + (3/16) y^(3/2) + O(y^2)      (x/y = 1/sqrt(y) + 3/8 + ...)
```

so in physical terms `g ≈ sqrt(B a0) + (3/8) B` deep — consistent with `v_flat^4 = G M_b a0` at leading order on the adopted footing (leading term only; the `3/8` is a branch-specific correction that does NOT transfer to other branches).

**Newtonian inversion:**

```
x(y) = y + 4/y + O(1/y)      (g ≈ B + 4 a0^2 / B)
```

The `4 a0^2/B` term is the exact leading near-Newtonian correction of the MU2 branch, derived from `x - y = 4x/(x+2)^2` with `x ≈ y`.

**Signs and units:** every factor above is dimensionless in `x,y`; `Δ_g` carries `m^12 s^-6`, `dy/dx` dimensionless; the dimensional cubic coefficients are `[1, 4a0, -B, -4B a0, -4B a0^2]` (mixed units force one unique positive root by Descartes-like sign structure — confirmed by the exact root count, which does not rely on Descartes).

## 4. Step 4 — independent checks, different representations (task step 4)

All tolerances were set before evaluation. 29/29 checks PASS (raw: `raw_outputs/run_stdout.log`, `raw_outputs/summary.json`).

| Check | Observed | Tolerance | Result |
|---|---|---|---|
| Symbolic clear to cubic, discriminant factorizations, derivatives, bracket values | exact | 0/exact | PASS (9 checks) |
| Grid `y = 10^k`, k = −10..8 step 0.1 (181 pts): exactly one positive real root | 181/181 | all | PASS |
| Negative roots: exactly 2 per case | 2/case | 2 | PASS |
| Rel. cubic residual `|P(x*)|/scale` | max 2.44e-14 | 1e-12 | PASS |
| Rel. implicit residual `|y − x*·mu2(x*)|/scale` (exact rational form) | max 4.88e-14 | 1e-12 | PASS |
| Bracket via exact identity `x−y = 4x/(x+2)^2` | min low margin 4.00e-8, min high margin 3.50 | 1e-14 | PASS |
| `mu2(x*) ∈ (0,1)` | [9.99996e-6, 1.0] | (0,1) | PASS |
| Root intervals `(-(y+4),-2)`, `(-2,0)`, `(y,y+4)` | 3/3 per case | all | PASS |
| Deep limit `x* ≈ sqrt(y)(1 + (3/8)sqrt(y))` at y=1e-10 | rel dev 1.01e-11 | 1e-5 | PASS |
| Near-Newtonian `x* − y* ≈ 4/y` at y=1e8 | 4.000000e-8 vs 4.000000e-8 | 1e-3 rel | PASS |
| mpmath dps=50 implicit residual | max 1.04e-52 | 1e-45 | PASS |
| hp vs numpy lane (float64 companion-root floor ~5eps·|x|) | max 2.51e-8 | 1e-7 | PASS |
| `dy/dx` identity vs central FD | 1.70e-10 | 1e-6 | PASS |
| `mu2' = (y'−mu2)/x = 8/(x+2)^3`, x ≤ 1e3 | 5.25e-6 | 1e-4 | PASS |
| hp FD of `dmu2/dx` (full range) | 2.00e-12 (truncation bound 2e-12) | 1e-10 | PASS |
| `dy/dx > 0` on grid | all positive | >0 | PASS |
| Footings: `g ≈ B + 4a0²/B` at B=1, both footings | 1.0 vs 1.0 | 1e-4 rel | PASS |

## 5. Step 5 — negative controls (task step 5; each is capable of failing)

- **NC1 (negative root):** run the physical-domain filter on the *most negative* real root `x ≈ -(y+4)`: `mu2` comes out negative (e.g. y=1e-10: `mu2(-3.99999999997) ≈ -2.5e-11 < 0`), `x < 0` — rejected. **0 wrong acceptances, 19/19 rejections.** The control would fail if the selector accepted it; it cannot pass vacuously because the wrong roots are real and exercised.
- **NC2 (complex root):** plant a complex candidate `imag = 1e-6·x` into the physical-domain check — rejected 19/19 (0 wrong acceptances). 
- **NC3 (wrong deep coefficient):** the leading-term check is run against a *fake* deep coefficient 6/8 instead of 3/8 at y = 1e-6: relative deviation **3.748e-4 ≫ 1e-5** — cleanly caught. (At y=1e-10 the deviation would be ≤ 3.75e-6 < 1e-5 and the control would hide the fake; the control is placed where it has power. Power analysis recorded in the script.)

## 6. Strongest surviving statement

**Theorem (dimensionless, exact; Lean-certified).** For all `y > 0`, the equation `y = x·mu2(x)` on `x > 0` is equivalent to the cubic `P_y(x) = 0`; `P_y` has exactly three distinct real roots; its unique positive root `x*(y)` satisfies `y < x*(y) < y + 4`; the other two roots lie in `(-(y+4), -2)` and `(-2, 0)`; `Δ_x = 16y(2y² + 13y + 64) > 0`; `mu2` is strictly increasing with range `(0,1)`; `yFwd(x) = x·mu2(x)` is strictly increasing on `x > 0`.

**Inverse.** The exact forward relation is `B = a0·x²(x+4)/(x+2)²` (rational, algebraic — no numerics needed). The exact inverse is *not* a single algebraic radical in closed manageable form (the cubic's roots are expressible by Cardano but the positive branch selection is a case split); the certified exact characterization is: `x*(y)` = the unique root of the cubic in `(y, y+4)`. Numerically it is obtained stably by bisection/Newton on `(y, y+4)` with the exact identity `x − y = 4x/(x+2)²` (margins ≥ 4e-8 on the entire grid); the hp lane confirms 1e-45-level residuals (max 1.04e-52 at dps=50).

## 7. First additional implication needed to transfer to the full theory

MU2 is a **comparison branch**. Transfer to the operative filtered-MONO target would require an explicit bridge: prove that replacing `nu_mono` by `mu2` changes the filtered field equation's static solutions, or prove a coupling/entry bound between the branches — such a bridge does not exist yet and is NOT established by this task. Also open (any branch): the three-dimensional field-equation inversion `div[mu2(|∇Φ|/a0)∇Φ] = 4πGρ_b` → actual `Φ`, which needs the kernel argument `g = |∇Φ|` handled as a field, not a scalar curve.

## 8. Both footings

Dimensionless theorem proved once; physical scaling per footing (framework contract: `a0 = κ c √(G ρ_Λ)`, κ = 1/2):

| | canonical | alternative |
|---|---|---|
| a0 = (c/2)√(G ρ_Λ) | **9.3619e-11 m/s²** | **1.1279e-10 m/s²** |
| implied ρ_Λ (κ=1/2 fixed) | 5.8444e-27 kg/m³ | 8.4831e-27 kg/m³ |
| κ_eff if ρ_Λ held at canonical | 1/2 (by construction) | 0.60239 |
| bracket B < g < B + 4a0 | width 3.74476e-10 | width 4.5116e-10 |
| deep galaxy B=1e-11 | g = 3.4695e-11 (= √(B a0) + (3/8)B + …) | g = 3.7650e-11 |
| transition B=1e-10 | g = 1.4610e-10 | g = 1.5442e-10 |
| near-Newtonian B=1 | g = 1.0000000000 = B + 4a0²/B (rel 1e-4 ✓) | same ✓ |

The alternatives do not share both fixed ρ_Λ and fixed κ (contract rule): they are two normalizations of the same dimensionless curve.

## 9. Branch distinctness (criterion B MONO operative)

Deep expansions (leading coefficient identical `1/√y` for all; first correction differs):

```
nu_MU2(y) = 1/√y + 3/8   + …
nu_RAR(y) = 1/√y + 1/2   + √y/12 + …
nu_Q(y)   = 1/√y + √y/2  - y^(3/2)/8 + …
```

MU2 is never identified with Q/RAR/EXP/MONO; the `3/8` vs `1/2` vs `√y/2` differences make the branches distinct (and NC3 shows the leading-term check has the power to catch a wrong coefficient).

## 10. Lean certificate

`AS029_mu2_implicit_cubic.lean` (compiles under `lake env lean` in `fable_independent_2026/lean_2026`, Lean 4.34.0-rc2 + mathlib4; output `lean_certificate.out`, exit 0):

- rational form of μ2; `y = x·μ2(x) ⟺ P_y(x)=0`; sign bounds; IVT existence in `(y, y+4)`; uniqueness via the positive bracket Q; two negative roots via IVT on `(-(y+4),-2)` and `(-2,0)`; **exactly three real roots** (`roots.card = 3` via `Polynomial.card_roots` + degree bound); no-other-roots enumeration; discriminant identity and positivity; `0 < μ2 < 1`, strict monotonicity of `μ2` and of `yFwd`; the main theorem `mu2_implicit_force_cubic`.
- **Hard bar met:** `#print axioms` on all 14 certified declarations gives exactly `[propext, Classical.choice, Quot.sound]`; zero `sorryAx`; zero `sorry`.
- Carried in the Python lane (not Lean): surjectivity of `B ↦ g` onto `(0,∞)` (unboundedness + continuity evidence), numeric residuals.
- The probes used to pin lemma names/signatures in this mathlib snapshot are preserved as `lean_probe1..7.lean`.

## 11. What this result does and does not establish

**Establishes (exactly, certified):** cubic structure, root count/selection and bracketing of the MU2 implicit force law; exact forward map; positive discriminant; monotone inverse; branch-distinct deep asymptotics; 29/29 reproducible numeric checks; both footings.

**Does not establish:** any result about the operative filtered-MONO branch (no bridge); the 3-D field equation for MU2; any empirical preference; `kappa = 1/2` from first principles; any claim about full-theory closure. `RLIMIT_AS` could not be lowered on this macOS host ("current limit exceeds maximum limit"); the 512 MB figure is declared, the enforced bounds are wall (120 s; actual 0.47 s) and thread pinning (1); peak RSS recorded 90.8 MB.
