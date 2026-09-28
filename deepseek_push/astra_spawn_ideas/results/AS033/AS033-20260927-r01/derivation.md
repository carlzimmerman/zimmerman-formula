# AS033 — MONO splice location from its derivative rule

**Run:** AS033-20260927-r01 · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter) via Hermes Agent subagent
**Started:** 2026-09-28T02:07:58Z (first command) · **Finished:** 2026-09-28T02:31:00Z (approx.; see result.json `finished_utc`)
**Task hash:** `41b34f5f2822b5b08abe33c43e9fcac45bce38e7f7eb7dd0978abe40b79bed2c`
**Branch:** operative MONO (filtered `nu_mono`); Q, RAR, MU2, EXP only as comparison branch in controls. No branch import was used to repair anything.

---

## 0. Precise claim, symbol dictionary, boundary conditions, assumptions

**Claim (quantified).** Let

```text
nu_RAR(y) = 1/(1 - exp(-sqrt(y))) ,          y = B/a0 > 0
h_RAR(y)  = y (nu_RAR(y) - 1) = y/(exp(sqrt(y)) - 1)
h'_mono(y) = max( h'_RAR(y),  delta*h_p/(y + y_p) ),   delta = 0.05
h_p = h_RAR(y_p),   y_p = argmax of h_RAR on (0, inf)
```

with the peak and the splice *defined* (not hard-coded) by

```text
h'_RAR(y_p) = 0                 (peak equation)
h'_RAR(y_star) = delta*h_p/(y_star + y_p)     (crossing / splice equation)
```

Then:

1. **Peak (exact).** `y_p = s_p^2` with `s_p` the unique root of `exp(s)(2 - s) = 2` on `(0,2)`;
   `h_p = s_p(2 - s_p)` exactly at the peak. Numerically
   `y_p = 2.53963828218816532499888178977436590236898…`,
   `h_p = 0.64761023789191485964720196197595458120902…`
   (landmarks 2.5396 / 0.647610 reproduced to 3.8e-5 / 2.4e-7).
2. **Splice (transcendental, unique).** The crossing equation has exactly one root on
   `(0, y_p)`; numerically
   `y_star = 2.33741240526632945555812330320119886079215…`
   (landmark 2.3374 reproduced to 1.2e-5). Residual of the crossing equation at the root:
   `F(y_star) = -3.89e-62` (60-digit mpmath).
3. **Continuity join.** With the exact continuation formula
   `h_mono(y) = h_RAR(y_star) + delta*h_p*ln[(y + y_p)/(y_star + y_p)]`  (y ≥ y_star),
   `h_mono(y_star) = h_RAR(y_star)` exactly (the `ln 1 = 0` term vanishes), and
   `h'_mono` is **continuous** at `y_star` (both sides equal `delta*h_p/(y_star + y_p)`;
   residual 3.9e-62). The join is C¹ but not C²: the second derivative jumps by
   `J = 0.0347447135548…` at the splice.
4. **Limits.** Deep (`y→0`): the max picks the RAR branch (`h'_RAR(y) → +∞` dominates),
   `nu_mono = nu_RAR`, `g ≈ sqrt(a0 B)` (leading deep law, same as Q); Newtonian
   (`y→∞`): `nu_mono(y) = 1 + h_mono(y)/y → 1`, i.e. `g → B` with a logarithmic correction
   `delta*h_p*ln(y)/(y)`.

**Symbol dictionary.** `B = g_bar = g_N > 0` (baryonic/Newtonian acceleration), `y = B/a0`,
`x = g/a0`, `g` total radial acceleration, `nu = g/B` (response), `h = g - B` (phantom excess
acceleration, units of acceleration, in dimensionless units of a0), `delta = 0.05` (declared
kernel parameter), `y_p, h_p` peak landmarks, `y_star` splice. Units: all equations are
dimensionless in `y`; the dimensional splice accelerations are `B_star = y_star * a0`
(§ 7). Boundary conditions: none beyond `y > 0`; `h_RAR(0+) = 0`, `h_RAR → 0` as `y→∞`.

**Framework inputs vs conclusions.** *Inputs (adopted, not derived):* `a0 = kappa*c*sqrt(G*rho_Lambda)`
with `kappa = 1/2`, `delta = 0.05`, the max rule, the two footings `a0 ∈ {9.3619e-11, 1.1279e-10} m/s²`,
`G = 6.67430e-11`, `c = 299792458` (SI). *Conclusions established here:* the peak location/value
in closed form, the splice as the unique crossing, the continuity join, the exact continuation
formula, and the derivative rule `d h_mono/dy = delta*h_p/(y+y_p)` on the continuation (Lean-certified).
`G_N`, `G_bare`, `G_cosmo` are kept separate; nothing in this task needs their ratio.

---

## 1. The peak: closed form

`h_RAR(y) = y/(e^s - 1)`, `s = sqrt(y)`. Direct differentiation gives the closed form

```text
h'_RAR(y) = 1/(e^s - 1) - (s/2) * e^s/(e^s - 1)^2 ,        s = sqrt(y)      (1)
```

(verified symbolically by sympy: `simplify(diff(h) - closed form) = 0`, and numerically by
central differences at y ∈ {0.2, 1.0, y_star, y_p, 5.0}, residuals ≤ 7.3e-32 at 60 digits).

Peak condition `h'_RAR(y_p) = 0` (and `e^s ≠ 1`) gives the exact equation

```text
e^s (2 - s) = 2 ,        s_p = sqrt(y_p) ,        h_p = s_p (2 - s_p)        (2)
```

(the second identity follows from `h_p = y_p/(e^{s_p}-1)` and `e^{s_p} = 2/(2-s_p)`:
`e^{s_p} - 1 = s_p/(2-s_p)`). The left side of (2) is strictly increasing on `(0, 1)` and
strictly decreasing on `(1, 2)` with values 2 at `s = 0` … >2 … and `→ 0` as `s → 2⁻`:
the unique root in `(0, 2)`. Newton iteration at 60 digits:

```text
s_p = 1.59362426004004009232304187587516024178900242…
y_p = 2.53963828218816532499888178977436590236898418…
h_p = 0.647610237891914859647201961975954581209020672…
```

`h'_RAR(y_p)` residual: 0.0 (machine exact at the root of the s-equation, then closed-form
evaluation). Landmark agreement: `|y_p − 2.5396| = 3.83e-5`, `|h_p − 0.647610| = 2.38e-7`
(the landmarks are rounded to 5/6 significant digits, so an exact match is not expected).

---

## 2. The splice as the crossing of the two derivative branches

The operative derivative rule is `h'_mono = max(h'_RAR, delta*h_p/(y+y_p))`; the splice is the
point where the two arguments are equal:

```text
F(y) := h'_RAR(y) - delta*h_p/(y + y_p) = 0 ,        delta = 0.05              (3)
```

**Uniqueness (bracket, not grid).** On `(0, y_p)`, `h''_RAR(y) < 0` because, with
`W = e^s/(e^s-1)^2 > 0`,

```text
h''_RAR(y) = W * [ s/(1 - e^{-s}) - (3 + s)/2 ] / (2 s) ,
```

and the bracket has the sign of `psi(s) = (3+s)(1 - e^{-s}) - 2 s`. `psi'(s) = (2+s)e^{-s} - 1`
has exactly one root `s0 = 1.1461932206205825852…` (bracketed, root of `e^s = 2+s`), so
`psi` increases to `psi(s0) = 0.53596235… > 0` and then decreases monotonically; since
`psi(s_p) = 0.47300701… > 0` (evaluated, not estimated), `psi > 0` on all of `(0, s_p]`, hence
`h''_RAR < 0` on `(0, y_p)`: `h'_RAR` strictly decreases from `+∞` (at `y→0+`, since
`h'_RAR ~ 1/(2 sqrt(y))`) to `0` at `y_p`. The RHS of (3) is strictly decreasing and positive on
`(0, y_p)`. Hence `F` is strictly decreasing on `(0, y_p)`; `F(0+) = +∞ > 0` and
`F(y_p) = -delta*h_p/(2 y_p) = -0.0063750244… < 0`; by IVT and strict monotonicity there is
**exactly one root `y_star ∈ (0, y_p)`** — the splice is defined by the equation, not hard-coded.

**Solve (60-digit mpmath, bracketed Newton; root bracketed in [1.5, 2.4]):**

```text
y_star = 2.33741240526632945555812330320119886079215277…
F(y_star) = -3.89e-62            (absolute residual of (3) at the root)
h'_RAR(y_star) = 0.0066393634123774664319402003748430201817060454…
delta*h_p/(y_star + y_p) = 0.0066393634123774664319402003748430201817060454…
```

Substitution into the *original* equation (independent check, different representation):
`|h'_RAR(y_star) − delta*h_p/(y_star+y_p)| = 3.89e-62`. Landmark agreement:
`|y_star − 2.3374| = 1.24e-5` (landmark is rounded to 5 digits).

**Branch structure around the splice.** For `y < y_star`, `h'_RAR(y) > delta*h_p/(y+y_p)`
(the max selects RAR); for `y > y_star` (up to `y_p` and beyond) the max selects the
continuation branch. This follows from strict monotonicity of `F` (single crossing, no grid).

---

## 3. Continuity join and the exact continuation formula

Define the continuation by integrating the active branch from the splice:

```text
h_mono(y) = h_RAR(y_star) + ∫_{y_star}^y delta*h_p/(t + y_p) dt
          = h_RAR(y_star) + delta*h_p * ln[ (y + y_p) / (y_star + y_p) ] ,   y ≥ y_star   (4)
```

- **Value join:** `h_mono(y_star) = h_RAR(y_star) + delta*h_p*ln(1) = h_RAR(y_star)` exactly
  (`ln 1 = 0`); numeric residual `0.0` (60 digits; the exact identity is Lean-certified, § 8).
- **Derivative continuity (C¹):** both one-sided derivatives at `y_star` equal
  `delta*h_p/(y_star + y_p)`; residual `3.89e-62`.
- **Not C²:** the second derivative jumps at the splice by
  `J = d/dy[delta*h_p/(y+y_p)] - h''_RAR(y_star) = -delta*h_p/(y_star+y_p)² - h''_RAR(y_star)
  = +0.0347447135548…` (with `h''_RAR(y_star) = -0.0361060619…`).
- **Response:** `nu_mono(y) = 1 + h_mono(y)/y`, continuous at `y_star`, `nu_mono(y_p) = 1.0006656… > nu_RAR(y_p)`
  — the continuation rises above the RAR peak (`h_mono(y_p) = 0.6482759304… > h_p`), the
  monotone-phantom growth that motivates the branch.
- **Derivative rule on the branch:** `d/dy h_mono = delta*h_p/(y+y_p)` at every
  `y > 0` with `y + y_p ≠ 0` (Lean-certified, § 8); verified numerically at `y_star`, `y_p`, 1e6.

The filter operators `S = exp[(xi²/2) Δ]` and the filtered field equation are the *operative*
context for this branch (framework contract); the filter acts on `nu_mono − 1 = h_mono/y` inside
the elliptic equation. The splice enters the filtered theory through the C¹-not-C² kink of
`h_mono` (§ 6 quantifies the kink and a model heat filter's action on it).

---

## 4. Independent checks (different representations, actual residuals)

| Check | Method | Observed | Tolerance | PASS |
|---|---|---|---|---|
| C1 | sympy symbolic derivative vs closed form (1) | `simplify(diff − closed) == 0` | exact 0 | ✓ |
| C2 | numeric central differences vs (1), y ∈ {0.2, 1.0, y_star, y_p, 5.0} | residuals ≤ 7.3e-32 | 1e-20 | ✓ |
| C3 | substitution into original crossing equation (3) | `\|F(y_star)\| = 3.89e-62` | 1e-45 | ✓ |
| C4 | landmarks vs task (rounded) | `Δy_p = 3.83e-5`, `Δh_p = 2.38e-7`, `Δy_star = 1.24e-5` | landmark quoted precision | ✓ |
| C5 | peak closed forms: `h_p = h_RAR(y_p)` | diff 0.0; `h'(y_p) = 0.0` | 1e-45 | ✓ |

---

## 5. Negative controls (capable of failing — all failed as designed, with numbers)

**NC1 — change the peak definition, retain the old splice → discontinuity of h′.**
Keeping `y_star = 2.33741240…` but using a different peak definition `(y_p′, h_p′)`:

| peak definition | `\|delta·h_p′/(y_star+y_p′) − h'_RAR(y_star)\|` | relative to true RHS |
|---|---|---|
| `y_p′ = y_p + 0.25` (mislocated peak) | 3.3217e-4 | 5.00% |
| `y_p′ = 2.0` (arbitrary peak) | 7.6615e-4 | 11.5% |
| `h_p′ = 0.5·h_p` (peak value halved) | 3.3197e-3 | 50.0% |

The derivative discontinuity is nonzero in every case (a maximum of ~0.05–0.5 of the true RHS):
the old splice location is *only* compatible with the true peak. Only the value join still holds
(any `ln 1 = 0`), so the failure is precisely in **C¹ continuity** — the control discriminates.

**NC2 — shifted splice (peak retained) → join condition violated.**
Re-solve nothing; evaluate the crossing residual at `y_star ± ε`:
`|F(2.3474124)| = 3.457e-4` (ε=+0.01), `|F(2.3874124)| = 1.695e-3` (ε=+0.05),
`|F(2.2874124)| = 1.781e-3` (ε=−0.05). All ≫ 1e-45: a shifted splice violates the
derivative-join condition by amounts growing ~linearly in the shift (F′ ≈ −0.0347 at y_star,
consistent with the measured ratios).

**NC3 — deep and Newtonian limits.**
- Deep `y = 1e-10`: `h'_RAR = 49999.5…` vs `delta·h_p/(y+y_p) = 0.012750049…` → the max
  selects RAR; `nu_mono·sqrt(y) − 1 = 5.0000083e-6 ≈ sqrt(y)/2` → `g = B·nu ≈ sqrt(a0·B)`
  (leading deep law, same leading term as Q; the `+B/2` subleading term reproduces the RAR
  expansion). Both values are actual, not asymptotics-by-fiat.
- Newtonian `y = 1e6`: `h_RAR(1e6) = 5.076e-429` (RAR tail is `y·e^{−sqrt y}`); the MONO branch
  instead gives `h_mono(1e6) = delta·h_p·ln(y/(y_star+y_p)) + h_RAR(y_star) = 1.0430055…`
  so `nu_mono − 1 = h_mono/y = 1.0430055e-6 → 0`; `g/B = 1 + 1.043e-6 → 1`. The Newtonian
  limit of MONO is `g → B` with a slowly decaying logarithmic correction
  `delta·h_p·ln(y/y_*)/y` — an exact statement about the branch, distinct from RAR's
  exponential tail.
- Normalization/peak check: `h'_RAR(y_p) = 0`, `h_p = h_RAR(y_p) = s_p(2−s_p)` exact identity.

**NC4 — kernel-parameter variation (δ′ ≠ δ).** New crossings for δ′ = 0.07 and 0.03:
`y_star′ = 2.262643737…` and `2.415579119…`; at the *old* `y_star` the residual
`|h'_RAR − δ′h_p/(y+y_p)| = 2.6557e-3 ≠ 0` both ways — i.e. `y_star` genuinely tracks the
declared `delta = 0.05`; the rule is not form-invariant under parameter substitution.

---

## 6. Heat-filter action on the splice (scoped model diagnostic — not part of the claim)

The framework's `S = exp[(xi²/2) Δ]` requires a metric, measure and domain that the campaign
has not committed for the lattice operator (open dependency, mirrored by AS042/AS047/AS048).
As an explicitly labeled **flat 1-D periodic model** (`S_xi = exp(−xi² k²/2)` in Fourier,
Lebesgue measure, domain [0,10] / splice window [1.5,3.5], N = 2^16, xi ∈ {0.01, 0.05}) the
action on the splice's `h''` kink is:

- Global: the y→0 singularity of `h''_RAR ~ −1/(4 y^{3/2})` (raw `‖h''‖_∞ = 3.75e5`) is
  regularized by the filter to `3.65e3` (xi=0.01) and `7.43e2` (xi=0.05).
- Splice-local (window |y − y_star| ≤ 0.5, seam-continuous baseline): the 0.03474 step in `h''`
  at `y_star` is smoothed: `max |S_xi g − g| = 1.49e-2` (xi=0.01), 1.54e-2 (xi=0.05); the raw
  curvature at the splice point `−0.00664` is shifted to `−0.0419…` (xi=0.01), i.e. the filter
  spreads the step over the heat width.

This diagnostic's numbers must NOT be transferred to the framework's metric-dependent `S`
(same-theory discipline); it quantifies the kink amplitude (§ 3) that a committed-cell filter
would smooth. The seed did not require this computation; it is reported as a scoped candidate
diagnostic only.

---

## 7. Both footings (dimensionless theorem, dimensional application)

The derivation is dimensionless in `y = B/a0`; it holds identically for both footings with the
correct `a0`. Dimensional splice locations `B_star = y_star·a0`:

| footing | a0 [m/s²] | rho_Lambda = 4 a0²/(G c²) [kg/m³] | B_star [m/s²] | kappa-implication |
|---|---|---|---|---|
| canonical | 9.3619e-11 | 5.84441245402e-27 | 2.18826212e-10 | kappa = 1/2 adopted |
| alternative | 1.1279e-10 | 8.48308961956e-27 | 2.636367452e-10 | rho_alt/rho_can = 1.451487157 at fixed kappa; equivalently kappa_eff = 0.6023884041 at fixed rho_can |

The two footings are NOT the same theory with two numbers: they differ in the physical
`rho_Lambda` (or in kappa if rho is pinned) by the quoted factors; the dimensionless splice is
transferable, the dimensional one is not.

---

## 8. Lean certificate

File: `AS033_MONO_SpliceJoin.lean` (this directory). Compile (exit 0):

```text
cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS033_MONO_SpliceJoin.lean
```

Theorems (all closed, zero `sorry`, `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}):

| theorem | meaning |
|---|---|
| `mono_join_value` | `h_RAR(ys) + delta·hp·log((ys+yp)/(ys+yp)) = h_RAR(ys)` — the value join at the splice (log 1 = 0), for any parameters with `ys + yp ≠ 0` |
| `mono_continuation_continuousAt` | the continuation `y ↦ h_RAR(ys) + delta·hp·log((y+yp)/(ys+yp))` is **continuous at the splice** |
| `mono_continuation_deriv` | `d/dy h_mono = delta·hp/(y+yp)` — the exact continuation derivative rule (the max-rule RHS) at every `y` with `y+yp ≠ 0` |

Scope declared in the file header: the certificate covers the algebraic/analytic join and
derivative rule for arbitrary positive parameters; the **transcendental crossing value**
`y_star = 2.3374124…` is carried numerically (60-digit lane, § 2), not certified in Lean.
Deliberately not certified: any law-of-nature statement, the landmark values themselves, and
the C² failure (routine calculus, numeric residual −J = −0.0347447135548… recorded here).

---

## 9. What survives and what does not

**Strongest surviving statement.** On the operative MONO branch with `delta = 0.05` and the
true peak `(y_p, h_p)`, the max rule `h'_mono = max(h'_RAR, delta·h_p/(y+y_p))` has a unique
splice at `y_star = 2.337412405266329455558123303201198860792…` solving the crossing equation
exactly (residual 3.9e-62), the continuation `h_mono(y) = h_RAR(y_star) + delta·h_p·ln[(y+y_p)/(y_star+y_p)]`
joins continuously (C¹, value residual 0.0, derivative residual 3.9e-62; Lean-certified), and
any change of peak definition or splice location produces a measured derivative discontinuity
(NC1/NC2, 0.03%–50% of the true branch scale). The splice is thereby *derived from the
derivative rule*, with `y_p`, `h_p` derived from first equations, not imported from AS032
(which has no result yet).

**Domain of validity.** `y > 0` real; the uniqueness argument is rigorous on `(0, y_p)` with
bracketed extrema values (ψ(s0), ψ(s_p)); the numeric values are 60-digit; the heat diagnostic
is a flat-1D model only.

**Limitations.** (i) Criterion-B/causality, stability and the full filtered field equation are
untouched — this result is a constitutive-kernel statement (gate 12 content), not a dynamics
statement. (ii) `delta = 0.05` and kappa = 1/2 remain adopted inputs; nothing here derives them.
(iii) The heat numbers do not transfer to the committed metric-dependent `S` (open dependency:
metric/measure/domain of `S` uncommitted). (iv) Landmark agreement is at the rounded precision
quoted (5–6 digits), as expected. (v) Numerical agreement at 60 digits is finite evidence, not
an empirical test.

**next_unresolved_implication.** The *filtered-field* consequence at the splice: evaluate the
operative equation `ΔΦ = 4πGρ_b + S* div[(nu_mono(|∇Su|/a0) − 1) ∇Su]` for a point mass with
the committed (metric, measure, domain, xi) for `S`, and show the splice kink of
`nu_mono − 1` produces no discontinuity in the filtered acceleration field — requires the
operator specification that the campaign has not committed (AS042/AS048 territory).

**Child proposals (recorded; not dispatched — no spawn mechanism in this slot).**

1. **AS033.C01 — committed-cell heat-filter action at the splice.** Target: with an explicitly
   declared metric/measure/domain for `S = exp[(xi²/2)Δ]` (self-adjoint in that measure),
   compute `S*(nu_mono − 1)` near `y_star` and the residual vs the flat-model diagnostic of § 6.
   Fingerprint: (MONO filtered kernel, committed S cell, splice neighborhood, operator-action
   residual, xi ∈ {0.01, 0.05, 0.1}). Closest seeds: AS042 (filter order as law), AS048
   (smoothing as candidate), AS599 (1-D splice transmission) — none computes the operator action
   with a committed cell. Blocking dependency: the operator cell (metric/measure/domain/xi) must
   be committed first; a no-go stating that dependency is a valid outcome.
2. **AS033.C02 — phantom profile of the log continuation.** Target: exact spherical phantom
   density `rho_ph(r) = (div[(nu_mono−1)∇Φ] source term for the MONO log branch)`, and its
   asymptotic `~ r^{-2} ln(r/r_*)` form; compare with RAR/EXP tails. Fingerprint: (MONO log
   branch, phantom density profile, spline-free closed form, r > r_star). Closest seeds:
   AS582/AS091/AS619 — none states the closed-form profile of THIS branch.

---

## 10. Reproducibility

- `as033_splice.py` — the full 60-digit lane; run:
  `cd <run_dir> && OMP_NUM_THREADS=1 python3 as033_splice.py > as033_splice.out 2> as033_splice.err`
  (wall 0.51 s, maxrss 114 MB, 1 thread, in-process alarm 120 s, RLIMIT_AS soft cap 512 MB;
  all bounds enforced and recorded).
- Raw output: `as033_splice.out`, `as033_splice.err`; exact digits: `landmarks.json`.
- `AS033_MONO_SpliceJoin.lean` — Lean certificate (compile + `#print axioms` as above).
