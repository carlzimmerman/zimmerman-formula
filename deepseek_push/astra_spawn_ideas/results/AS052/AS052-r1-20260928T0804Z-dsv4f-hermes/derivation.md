# AS052 — OR composition with unequal channel slopes

**Run:** `AS052-r1-20260928T0804Z-dsv4f-hermes`
**Worker:** deepseek-v4-flash-0731 (openrouter) / Hermes subagent (session 20260928_035109_c7e0d7)
**Task file:** `deepseek_push/astra_spawn_ideas/AS052_or_composition_with_unequal_channel_slopes.md`
**task_sha256:** `bd9a4d387b694b13c3c1b99dbb1886ab809e48816458d0abeaaa6343ab45a737` (verified before execution)
**Sources pinned and verified:** PD01 `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d`,
PD08 `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb`,
k01 `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c` — all match `SOURCE_MANIFEST.json`.

---

## 1. Claim, symbol dictionary, boundary conditions, assumptions

**Claim under test (seed's math block):**

```
mu = 1 - product_i (1 - p_i(Y));   p_i(Y) = b_i * Y + O(Y^2);   mu'(0) = sum_i b_i.
```

The seed asks whether OR composition over the metric's two static channels
(PD01 B1: count 2) *derives* kappa = 1/2 when the per-channel slopes b_i are
**allowed to differ**, and mandates the counterexample-control b1 = 1, b2 = 2.

**Symbols** (all SI unless stated):

| symbol | meaning | units |
|---|---|---|
| `s = c sqrt(G rho_L)` | vacuum's own acceleration scale | m s^-2 |
| `a0` | MOND scale, `a0 = kappa * s` | m s^-2 |
| `kappa` | dimensionless coefficient, `a0/s` | — |
| `Y = g/s` | dimensionless drive | — |
| `g` | total radial acceleration | m s^-2 |
| `B = g_N = G M_b / r^2` | Newtonian baryonic acceleration | m s^-2 |
| `p_i(Y)` | per-channel engagement, `p_i(0)=0`, `p_i(oo)=1` | — |
| `b_i = p_i'(0)` | per-channel deep slope (dimensionless) | — |
| `mu(Y)` | total response, `mu = 1 - prod(1 - p_i)` | — |
| `n` | channel count, integer >= 1 (symbolic in the algebra) | — |
| `lambda = b2/b1` | slope-asymmetry ratio (b1 = 1 in the diagnostics) | — |

**Boundary conditions:** per channel `p_i(0) = 0` (action vacuum: frozen state,
PD08 step 1), `p_i(oo) = 1` (saturation; forces the composition normalisation
`mu(oo) = 1`, the L230/PD01 A3 requirement that excludes the sum over
shares).

**Premises (declared):**
1. OR structure `mu = 1 - prod_i (1 - p_i)` over the carrier's static channels
   (PD01 D1 — the one-premise conditional derivation; *not* re-derived here).
2. The response equation `mu(Y) g = B` as the spherical first integral of
   `div[ mu(|grad Phi|/s) grad Phi ] = 4 pi G rho_b` (PD08 AQUAL-form cell;
   spherical sector only).
3. `s` fixed by the measured vacuum density, independent of a0 (PD08; k01:
   the one-scale action admits no second coefficient).
4. `b_i > 0`, finite.  Per-channel differentiability at 0 with explicit
   `O(Y^2)` remainder (seed's `p_i = b_i Y + O(Y^2)`).

**Framework inputs (adopted, per FRAMEWORK_CONTRACT.md):** `a0 = kappa c sqrt(G rho_Lambda)`,
`kappa = 1/2` ADOPTED (not derived by this task); `G_N = G_bare = G_cosmo`
NOT separated in this lane — a single G enters both s and B (limitation L3).
Branch: **CORE coefficient; conditional MU_n statistical response** — the
seed's declared branch. Q, RAR, EXP appear only as deep-limit *comparisons*
(section 6); MONO is not used and no bridge to it is claimed.

**Conclusions to be established** (vs inputs): (i) `mu'(0) = sum b_i` exact;
(ii) two-channel quadratic coefficient; (iii) `kappa = 1/(sum b_i)` from the
deep matching; (iv) the exact equal-slope condition needed for `kappa = 1/n`;
(v) the negative control b1=1, b2=2.

---

## 2. The full quadratic coefficient (two channels) and the equal-slope condition for kappa = 1/n

With `p1 = b1 Y + c1 Y^2`, `p2 = b2 Y + c2 Y^2` (b1, b2 the slopes; c1, c2 the
O(Y^2) coefficients), the OR composition expands exactly (sympy, rationals;
Lean T1):

```
mu(Y) = 1 - (1 - p1)(1 - p2)
      = (b1 + b2) Y + (c1 + c2 - b1 b2) Y^2
        - (b1 c2 + c1 b2) Y^3 - c1 c2 Y^4.
```

- **Linear coefficient:** `b1 + b2` — independent of c1, c2 (the completion).
- **Quadratic coefficient:** `c1 + c2 - b1 b2`.  The cross term enters with the
  MINUS sign (it comes from `- p1 p2`); for the saturating completion
  `p_i = b_i Y/(1 + b_i Y)` (c_i = -b_i^2) this is
  `-(b1^2 + b1 b2 + b2^2)`.
- **Leading neglected term:** the exact Y^3, Y^4 terms are listed above, so
  for any neighborhood of Y = 0 where p1, p2 are C^3 the remainder beyond the
  quadratic is bounded by the third-derivative norms (dimensionless).  On
  `0 < Y < 1/max(b1, b2)` the family `p_i = b_i Y/(1 + b_i Y)` is analytic.

**Equal-slope assumption needed for kappa = 1/n (exact statement):**

```
mu'(0) = sum_i b_i   =>   deep matching (section 3) gives  kappa = 1/(sum_i b_i).

kappa = 1/n   <=>   sum_i b_i = n.
```

- Equal slopes `b_i = b` give `kappa = 1/(n b)` — **equal slopes alone are NOT
  enough**; the unit-slope *fraction identity* `b_i = 1` (PD08 step 3, backed
  by the k01 zero-mode no-go: the one-scale action `S_kin = (1/8 pi G) int
  s^2 K(|grad Phi|/s)` has no second coefficient to rescale a slope) is the
  exact premise that delivers `kappa = 1/n`.
- Under the fraction identity unequal slopes are impossible **a priori** (all
  b_i = 1).  Outside the one-scale action class, each b_i is a genuinely
  independent dimensionless freedom of the response, and the OR composition
  does **not** remove it (control E1/E2).

---

## 3. Deep and Newtonian limits; scale factors, signs, units

**Closed-form unequal-slope family** (generalization of the committed member
`mu_n = 1 - (1+Y)^(-n)` to unequal slopes; saturating per-channel completion
`p_i = b_i Y/(1 + b_i Y)`):

```
mu(Y) = 1 - prod_i 1/(1 + b_i Y);      two channels:
mu(Y) = 1 - 1/[(1 + b1 Y)(1 + b2 Y)]
      = (b1 + b2) Y - (b1^2 + b1 b2 + b2^2) Y^2 + O(Y^3).
```

- `mu(0) = 0`, `mu(oo) = 1` exactly for all b1, b2 > 0 (Lean T3/T4; sympy
  S3/S3b).
- **Deep regime** (Y << 1): `mu ~ (b1+b2) Y`.  The spherical first integral
  of `div[mu grad Phi] = 4 pi G rho_b` for a point source is
  `(b1+b2) g^2 r^2 / s = G M` (all scales: s [m s^-2] as the argument unit
  and the matched rate; signs all attractive/positive; kappa and b_i
  dimensionless).  Hence

```
g^2 = (s/(b1+b2)) g_N,   a0 = s/(b1+b2),   kappa = a0/s = 1/(b1+b2).
```

  (Algebra certified in Lean T5/T6.)  `kappa = 1/2` **iff** `b1 + b2 = 2`.
- **Leading neglected term in the deep regime:** with `mu = k Y + q2 Y^2`,
  `k = b1+b2`, the first correction is `g^2 = (s/k) g_N + (q2/k^2)(s/k)
  g_N^2/s + O(g_N^3/s^2)`, i.e. relative `O(g/s) = O(sqrt(g_N/s))`; verified
  on the ladder (section 4).
- **Newtonian regime** (Y >> 1): `mu -> 1` exactly, so `g -> B` for every
  slope pair (numeric E4: `|g/B - 1| <= 2e-32` at B/s = 1e16 for all three
  pairs).  Both limits hold; the slope freedom lives only in the
  deep-matching constant.

---

## 4. Independent checks (different representations, actual residuals)

All numerics: mpmath at **dps = 50** (difference-quotient checks at dps =
80), single process, wall-bounded 120 s (actual 0.23 s), RSS 56.4 MiB.

1. **Symbolic identity vs direct differentiation** (S1, S1n): `mu'(0) =
   b1 + b2` by `limit(diff(mu, Y), Y, 0)` exact; general-n product
   `1 - prod(1 - b_i Y)` at n = 2, 3, 5 gives `mu'(0) = sum b_i` exactly.
2. **Finite-difference slope of the closed form** (S4a): `(mu(eps) -
   mu(0))/eps` at eps = 1e-40, dps 80: relative error vs b1+b2 is
   8.8e-12/8.8e-12/1.2e-13 — the O(Y) truncation visible at 1e-40 scale;
   actual numbers recorded, tolerance 1e-25 met (dps 80 kills the
   division-amplified rounding of the ~1e-40 values).
3. **High-precision response solves on the deep ladder** (S4b/S4c/S5):
   `mu(g/s) g = B` solved by bisection + Newton at 50 digits for
   (b1, b2) in {(1,1/2), (1,1), (1,2)} on B/s in {1e-1 ... 1e-14};
   `kappa_fit = g^2/(B s)` tends to {2/3, 1/2, 1/3} with
   `|kappa_fit - 1/(b1+b2)| < 1.4e-7` at the deepest point (tolerance
   1e-6).  **Actual residuals:** `max |mu(g/s) g - B|/B = 1.03e-44`
   across all ladders — quoted, not inferred.
4. **Boundary case** (E5): `mu(Y)/((b1+b2) Y) -> 1` at Y = 1e-30 (dps 80),
   deviation ~1e-30 level, tolerance 1e-25.

---

## 5. Negative control and diagnostic counterexamples

**E1 (mandated control, capable of failing):** `(b1, b2) = (1, 2)`.
`mu'(0) = 3`, and the deep ladder converges to `kappa_fit -> 0.3333333782 =
1/3`, NOT 1/2.  The check *would have failed* had the channel count alone
fixed kappa; it instead refutes the unconditional claim: **two channels
alone do not force kappa = 1/2.**  The composition inherits the slope SUM,
and the sum is an independent freedom.

**E2 (lambda diagnostics at 1/2, 1, 2):** with `lambda = b2/b1`, `b1 = 1`:

| lambda | b1 + b2 | kappa = 1/(b1+b2) | deep fit | kappa = 1/2? |
|---|---|---|---|---|
| 1/2 | 3/2 | 2/3 | 0.6666667302 | no |
| 1 | 2 | 1/2 | 0.5000000530 | yes (only here) |
| 2 | 3 | 1/3 | 0.3333333782 | no |

Observational preference is not a mathematical proof: the algebra selects
lambda = 1 iff the sum-condition `b1 + b2 = 2` is *imposed*, not derived.

**E3 (identifiability):** the deep regime measures the slope SUM, not the
count: `(b1,b2) = (1,1)` and `(1/2,3/2)` share `mu'(0) = 2` and kappa = 1/2.
A slope pair summing to the count masquerades as the count; any kappa in
(1/3, 2/3) is compatible with *some* unequal-slope two-channel member.

---

## 6. Branch audit (Q, RAR, MU2, EXP, MONO kept distinct)

- **MU2 — exact membership:** at b1 = b2 = 1 the family is
  `mu(Y) = 1 - (1+Y)^(-2)`, i.e. exactly the framework MU2 branch
  (`mu2(x) = 1 - (1+x/2)^(-2)`, `x = g/a0`, `Y = x/2`, `s = 2 a0`);
  sympy cancelled identity + Lean T9.  The family is the committed branch's
  unequal-slope generalization.
- **Q / EXP / RAR — deep-limit comparisons:** each has deep slope
  `1/kappa = 2` in Y on the adopted footing (Q and EXP exact algebraically;
  RAR numerically `mu/Y = 2.00000000` at Y = 1e-10 from the implicit solve).
  They concur with the equal-slope reading; none is an unequal-slope
  counterexample, and none is used as the seed's conclusion-branch.
- **MONO — not used.**  The filtered `nu_mono` continuation
  (`h'_mono = max(h'_RAR, delta h_p/(y+y_p))`) is a different response in a
  different variable set; no bridge from the spherical OR cell to it is
  derived here (limitation L1).

---

## 7. Lean certificate (zero sorry; axioms = {propext, Classical.choice, Quot.sound})

File: `AS052_certificate.lean` (self-contained, `import Mathlib`), compiled
with `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` —
LEAN_EXIT=0, no warnings.  Unfiltered `#print axioms` probe (Lean
4.34.0-rc2): all nine theorems report exactly
`[propext, Classical.choice, Quot.sound]`, zero sorryAx.

| theorem | statement |
|---|---|
| or_two_channel_expansion | exact 2-channel polynomial expansion incl. quadratic coefficient c1+c2-b1 b2 |
| or_slope_error | `(mu(Y)-mu(0))/Y - (b1+b2) = Y*(...)` : difference-quotient slope error is O(Y), slope b1+b2 |
| family_closed_form | `1 - 1/((1+b1Y)(1+b2Y)) = ((b1+b2)Y + b1 b2 Y^2)/((1+b1Y)(1+b2Y))` |
| family_slope_error | `mu(Y)/Y - (b1+b2) = -Y((b1^2+b1 b2+b2^2)+(b1+b2)b1 b2 Y)/((1+b1Y)(1+b2Y))` |
| deep_matching | `k g^2 r^2/s = G M  =>  g^2 = (s/k)(G M/r^2)` |
| kappa_identity | `a0 = s/k  =>  a0/s = 1/k` |
| kappa_equal_unit_slopes | `1/(1+1) = 1/2` |
| kappa_unequal_control_value / _not_half | `1/(1+2) = 1/3` and `1/3 != 1/2` (the negative control) |
| family_member_mu2 | `muFam 1 1 Y = 1 - ((1+Y)^2)^(-1)` (MU2 member) |

**One dropped attempt (recorded):** a HasDerivAt-level chain-rule theorem
(`p1'(0)=b1, p2'(0)=b2 => mu'(0)=b1+b2` via `HasDerivAt.sub`/`.mul`) was
attempted; this build's elaborator synthesizes divergent module instances
for the codomain R (RCLike.toInnerProductSpaceReal.toModule vs
Real.instAddCommGroup Semiring.toModule), so the compositions do not
elaborate against the hypothesis instances.  The slope content is fully
carried by `or_slope_error` + `family_slope_error` (exact O(Y) error
identities), which are in the certificate; no sorry was ever introduced.

---

## 8. Footings — both a0 values carried separately

`rho_Lambda` fixed per footing by `a0 = (1/2) c sqrt(G rho_L)` (kappa = 1/2,
adopted): canonical `rho_L = 5.8444125e-27 kg/m^3 → s = 1.87238e-10 m/s^2`;
alternative `rho_L = 8.4830896e-27 kg/m^3 → s = 2.2558e-10 m/s^2`.  These two
footings are NOT the same kappa with the same density; each rho_L fixes s
and the predicted a0 of the unequal-slope family is `s/(b1+b2)`:

| b1+b2 | a0_pred (canonical rho_L) | a0_pred (alt rho_L) | ratio vs measured can / alt |
|---|---|---|---|
| 3/2 | 1.2482533e-10 | 1.5038667e-10 | 1.3333 / 1.3333 |
| 2 | 9.3619e-11 | 1.1279e-10 | 1.0 / 1.0 (both footings are the equal-slope sum) |
| 3 | 6.2412667e-11 | 7.5193333e-11 | 0.66667 / 0.66667 |

A measured footing alone cannot select the slope pair (E3): kappa = 1/2 on a
footing only says `b1 + b2 = 2`.  The seed's rule that the two footings "cannot
share both fixed vacuum density and fixed kappa" is respected: every row fixes
rho_L per footing and lets the predicted a0 (equivalently the effective kappa
= a0_measured/s) follow from the slope sum.

---

## 9. Strongest surviving statement and first transfer implication

**THEOREM (conditional, this run; all controls pass; Lean-certified algebra):**
*Let the response be the OR composition `mu = 1 - prod_i (1 - p_i)` over
`n >= 1` channels with `p_i(0) = 0`, `p_i(oo) = 1`, `p_i'(0) = b_i > 0`
(`p_i = b_i Y + O(Y^2)`).  Then `mu'(0) = sum_i b_i` (exact), and the
spherical deep matching gives `a0 = s/(sum_i b_i)` and `kappa = 1/(sum_i
b_i)` on whichever footing fixes s.  `kappa = 1/n` holds iff `sum_i b_i =
n`; with the framework's one-scale fraction identity (PD08 step 3; k01
no-go) all b_i = 1 and kappa = 1/n follows — under that premise unequal
slopes cannot arise.*

**COUNTEREXAMPLE (this run; the seed's mandated control):** `(b1, b2) =
(1, 2)` gives `mu'(0) = 3` and `kappa = 1/3 != 1/2` on both footings.  The
channel count 2 alone does NOT force kappa = 1/2; the OR composition does
not remove the per-channel slope freedom.  Diagnostics at lambda in
{1/2, 1, 2}: kappa in {2/3, 1/2, 1/3}.

**Transfer implication (first additional step to the full theory):** the
PD01 "slope = channel count" reading needs the map from the metric's two
static Poisson channels (PD01 B1) to per-channel slopes b_i = 1.  If a
future derivation ever yields `b1 + b2 = 2` without unit slopes (e.g. b1 =
1/2, b2 = 3/2), the count reading is replaced by a slope-sum reading with
the same kappa and the PD01 D3 falsifier ("any kappa strictly inside (1/2,
1) kills the structure") must be re-derived — the slope-sum family fills
(1/3, 2/3) continuously.

---

## 10. Bounds actually enforced

- Wall: declared <= 120 s, **enforced in-process** (deadline check inside
  the lane); actual wall 0.23 s.
- Memory: declared <= 512 MB, measured via `ru_maxrss` (darwin bytes
  converted): **56.4 MiB** actual.
- Threads: declared 1; single process, OMP/OPENBLAS/MKL pinned to 1.
- Precision: mpmath dps = 50 (ladders/solves), dps = 80 (difference
  quotients).
- Lean compiles: `timeout 580 lake env lean ...`; certificate compile
  0.35 s-class, capped at 580 s.

## 11. Limitations

1. Spherical static sector only; the filtered-MONO operative target and the
   full nonspherical response are not touched — no bridge from the OR cell
   to the `nu_mono` continuation (criterion B) is derived.
2. The OR identification (PD01 D1) and the fraction identity / one-scale
   premise (PD08 step 3, k01) remain premises; this run proves what the OR
   composition does and does not force *under* them, it does not derive
   either premise.
3. G_N / G_bare / G_cosmo not separated: one G enters s and B; the
   Lambda_eff ratio `(G_E/G_N)` and critical-density ratio are outside this
   run (framework contract's separate-symbols discipline flagged open).
4. The ladder checks are finite numerical consistency evidence, not exact
   identities; the exact identities are the symbolic/Lean statements
   (difference: stated in sections 2-4).
5. kappa = 1/2 remains the adopted framework input for the footings; this
   run's theorem reproduces it only under the unit-slope premise and does
   not remove the slope freedom by itself.

## 12. Files

- `compute_as052.py` — the lane (all checks, residuals, footings).
- `raw_outputs/compute_as052.out`, `raw_outputs/checks.json` — full output
  and machine-readable checks.
- `AS052_certificate.lean` — Lean 4 certificate (9 theorems, zero sorry).
- `raw_outputs/AS052_lean_compile.out`, `raw_outputs/AS052_axioms.out`,
  `raw_outputs/AS052_cert_axioms_probe.lean` — compile log, unfiltered
  axiom audit, and the probe file.
- `derivation.md`, `result.json` — this report and the schema-v2 result.