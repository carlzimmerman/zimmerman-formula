# AS046 — Numerical inverse conditioning (derivation and audit)

**Run:** `AS046_sa2_20260928T0508Z` · **Seed:** `deepseek_push/astra_spawn_ideas/AS046_numerical_inverse_conditioning.md`
**task_sha256:** `70c19062028c3f3b09fbe4728e629dee1a01a18ad4bc7b172669aa8ed54f4a9d`
**Worker:** deepseek-v4-flash-0731 (openrouter) via Hermes subagent `sa-2-0197cc40`.

> **Dispatch note.** The brief that reached this worker referenced a file name
> `AS046_mu2_matching_nu_and_derivative_at_one.md` that does not exist in the
> catalog. The authoritative on-disk seed is
> `AS046_numerical_inverse_conditioning.md` (pinned by the manifest and the
> claims ledger; `shasum -a 256` = `70c19062…f4a9d`, verified against
> `SOURCE_MANIFEST.json`). All work below was executed against that real seed,
> whose step 1–5 protocol is followed. The MU2-at-one matching question named
> in the dispatch is *the* content of this seed's audit (see §3.5, §4).

---

## 1. Precise claim, symbol dictionary, boundary conditions (seed step 1)

**Claim under audit** (seed, "Mathematics and principal test"):

> For `B = F⁻¹(g)`, `dB/dg = 1/F'(B)`; the relative condition number is
> `κ = g/(B·F'(B))`.

**Symbols** (framework contract, §Mandatory scale and units):

| symbol | meaning | value / domain |
|---|---|---|
| `g` | total radial acceleration | `g > 0` |
| `B` | Newtonian/barred acceleration `g_bar = g_N` | `B > 0` |
| `a0` | framework acceleration scale | `a0 = κ c √(G ρ_Λ)`, **κ = 1/2 adopted** |
| `x` | `g/a0` | `x > 0` |
| `y` | `B/a0` | `y > 0` |
| `G` | Newton coupling in SI | `6.67430e-11 m³ kg⁻¹ s⁻²` |
| `c` | speed of light | `299792458 m/s` |
| `F` | branch map `F(y) = x` (dimensionless) | branch-specific, below |

**Branch dictionary** (framework contract; branches kept distinct — never
silently identified):

| label | dimensionless law | inverse used |
|---|---|---|
| Q | `x² = y² + y` (algebraic a0-line) | `y_Q(x) = (√(1+4x²)−1)/2` |
| RAR | `x = y·ν_RAR(y)`, `ν_RAR = 1/(1−exp(−√y))` | bisection on `(10⁻⁶⁰, 10²⁰)` |
| MU2 | `y = x·mu2(x)`, `mu2(x) = 1−(1+x/2)^(−2)` (contract cell) | explicit `y_MU2(x) = x·mu2(x)` |
| EXP | `y = x·mu_EXP(x)`, `mu_EXP(x) = 1−exp(−x)` (historical AQUAL, comparison only) | explicit `y_EXP(x) = x·(1−e^(−x))` |
| MONO | `x = y·ν_mono(y)`, `ν_mono = 1 + h_mono(y)/y`, heat-filter splice of RAR (operative) | bisection on `(10⁻⁶⁰, 10²⁰)` |

MONO splice (framework contract): `h_RAR(y) = y(ν_RAR(y)−1)`, peak `y_p` with
`h_p = h_RAR(y_p)`, `δ = 0.05`,
`h'_mono(y) = max(h'_RAR(y), δ·h_p/(y+y_p))`, and on the continuation
`h_mono(y) = h_RAR(y*) + δ·h_p·log[(y+y_p)/(y*+y_p)]` with the actual crossing
`y* ≈ 2.3374`, `y_p ≈ 2.5396` (rounded landmarks; solved numerically here:
`y* = 2.3374124052663294`, `y_p = 2.5396382821881653`).

**Framework inputs vs conclusions.** Inputs: the five branch laws, `κ = 1/2`
(adopted, not derived), `G`, `c`. Conclusions to be established: the
differentiation identity `dB/dg = 1/F'(B)` on each branch, the closed forms of
`κ`, the exact MU2 cell values at `x = 1`, and the behavior of `κ` across the
transition region. `G_N`, `G_bare`, `G_cosmo` are kept separate symbols; this
task never equates them.

**Boundary conditions / domain.** `y > 0`, `x > 0` on every branch. Deep
regime `y → 0⁺` (κ → 2), Newtonian regime `y → ∞` (κ → 1). The grid
`y = 10^k`, `k = −10 … 8` step `0.1` (181 points) is a diagnostic grid, not a
proof; roots are bracketed explicitly (bisection with tolerance `10⁻⁴⁰`,
bounds `10⁻⁶⁰ … 10²⁰`), and the exact statements are certified symbolically
(Lean, §5) or analytically (§2).

---

## 2. Analytic derivation for Q (seed step 2, 3)

On Q: `F(y) = √(y²+y)`, so `F'(y) = (2y+1)/(2√(y²+y)) = (2y+1)/(2x)`.
With `B = a0·y`, `g = a0·x`:

```
dB/dg = (a0 dy)/(a0 dx) = 1/(dx/dy) = 2x/(2y+1) = 1/F'(y)   ✓ (chain rule, exact)
κ_Q    = g/(B·F'(B)) = x/(y·dx/dy) = 2x²/(y(2y+1)) = 2(y²+y)/(y(2y+1)) = 2(y+1)/(2y+1)
```

Exact identities (all certified in Lean, §5):

```
κ_Q(y) = 2(y+1)/(2y+1) = 1 + 1/(2y+1) = 2 − 2y/(2y+1),   κ_Q(1) = 4/3,
1 < κ_Q(y) < 2  for all y > 0,
κ_Q → 2 as y → 0⁺ (deep),  κ_Q → 1 as y → ∞ (Newtonian).
```

**Amplification statement.** A relative error in the measured/inferred `g`
propagates to `B` amplified by at most a factor 2 on Q; the amplification is
maximal at `y → 0⁺` (deep-MOND regime), where the a0-line is most ill
conditioned, and vanishes in the Newtonian limit. The inverse-relative
conditioning is the exact reciprocal of the forward-relative conditioning
(`κ_inv · κ_fwd = 1`, certified), so `κ` is dimensionless and unit-free — it
depends only on the ratio `y = B/a0`.

**RAR (bounded bracket, analytic form).** `ν_RAR(y) = 1/(1−e^(−s))`, `s = √y`:

```
dν/dy = −e^(−s)·(1/(2s))·(1−e^(−s))⁻² · (−1) = e^(−s)/(2s(1−e^(−s))²)
κ_RAR = ν/(ν + y·ν') = 1/(1 − (s/2)·e^(−s)/(1−e^(−s)))     (exact algebra, certified)
```

`κ_RAR` is evaluated on the grid with mpmath at 60 dps and bracketed by
bisection; the identity `κ = ν/(ν+y ν')` is checked independently by
finite differences (§4).

**MU2 (contract cell).** `mu2(x) = 1−(1+x/2)^(−2)`, `y = x·mu2(x)`:

```
mu2(1) = 1 − (3/2)^(−2) = 1 − 4/9 = 5/9
mu2'(x) = −(−2)·(1/2)·(1+x/2)^(−3) = (1+x/2)^(−3)      ⇒  mu2'(1) = (3/2)^(−3) = 8/27
x·mu2'(1) = 8/27
κ_MU2(x) = 1/(1 + x·mu2'(x)/mu2(x))      (from κ = g/(B F'(B)) with F'(B) = d(x·mu2)/dx)
```

**EXP (comparison).** `mu_EXP(x) = 1−e^(−x)`, `mu_EXP'(x) = e^(−x)`,
`mu_EXP(1) = 1−1/e ≈ 0.6321205588285577`, `mu_EXP'(1) = 1/e ≈ 0.36787944117144233`.

**MONO.** `κ_MONO` evaluated numerically from `h_mono` and its derivative
(`h'_mono = max(h'_RAR, δ h_p/(y+y_p))`), spliced continuously at `y*`.

---

## 3. The at-x=1 matching audit (dispatch question)

The dispatch asked to verify "mu_MU2(1) = 1/√2, derivative at 1, etc." and the
role of `x·dmu/dx` in branch ordering. The audit separates the **contract MU2
cell** from the **dispatch-mentioned interpolant** `mu_s(x) = x/√(1+x²)`:

| quantity | contract MU2 cell `1−(1+x/2)^(−2)` | interpolant `x/√(1+x²)` |
|---|---|---|
| value at x=1 | **5/9 = 0.5555555555555556** | **1/√2 = 0.7071067811865476** |
| derivative at x=1 | **(3/2)^(−3) = 8/27 = 0.2962962962962963** | **2^(−3/2) = 0.3535533905932738** |
| x·dmu/dx at x=1 | 8/27 | 2^(−3/2) |

**Finding.** The claim "mu_MU2(1) = 1/√2" is **false for the contract MU2
cell** (which evaluates to 5/9) and holds **only for the different interpolant
`mu_s(x) = x/√(1+x²)`** — which is not the contract cell the seed compares.
The derivative claim `2^(−3/2)` likewise belongs to `mu_s`; the contract cell
derivative is `8/27`. Both sets of exact values are certified in Lean (§5),
and both are reproduced by the mpmath audit to full precision
(`claim_1_over_sqrt2 = 0.7071067811865476`, `claim_deriv = 0.3535533905932738`).

**Branch ordering at fixed x** (mpmath, 60 dps; also the "one" of the identity
`x·dmu/dx` terms — the derivative factor that governs first-order branch
separation):

| x | y_Q | y_RAR = y_MONO | y_MU2 | y_EXP |
|---|---|---|---|---|
| 0.1 | 0.009901951359278483 | 0.009097175831683107 | 0.009297052154195011 | 0.009516258196404042 |
| 0.5 | 0.20710678118654752 | 0.16822574683571648 | 0.18 | 0.1967346701436833 |
| 1.0 | 0.6180339887498949 | 0.5105908269770001 | 0.5555555555555556 | 0.6321205588285577 |
| 2.0 | 1.5615528128088303 | 1.3829805683095102 | 1.5 | 1.7293294335267746 |
| 10 | 9.512492197250394 | 9.544732419074734 | 9.722222222222221 | 9.999546000702376 |

Ordering at small x: `y_RAR = y_MONO < y_MU2 < y_EXP < y_Q`; at large x the
branches converge to `y ≈ x` with Q lagging by the Newtonian offset
`y − x → −1/2` (verified: `y_Q − x = −0.49999999875` at `y = 10⁸`, residual to
−1/2 is `1.25e-9`), MU2 by `y − x → −4/x²·…` (numerically `−4.0e-8` at
`y=10⁸`), EXP exactly `y = x` for `x ≫ 1` (residual 0). Matching one asymptote
does not make kernels equivalent: the five branches remain distinct across the
whole grid (criterion: distinct Q, RAR, MU2, EXP, MONO).

---

## 4. Independent checks (seed step 4) — actual residuals

All numerics: mpmath at `mp.dps = 60`, single thread, wall time 0.50 s,
peak RSS 18.5 MB (both actually enforced; see `as046_raw.json` → `bounds`).
Finite-difference step `d = 10⁻⁴⁵·max(1,y)`; empirical perturbation `ε = 0.001`
in `g`.

**Check 1 — finite differences of κ (independent representation).**
`κ_fd = (x(y+d)−x(y−d))/(2d) · x/y`-style differentiation of the *forward*
map (for MU2/EXP the explicit `y(x)` map; for Q/RAR/MONO the solved inverse),
compared against the analytic/bracketed `κ`. Absolute residuals:

| branch | y = 10⁻⁴ | y = 1 | y = 10⁴ | y = 10⁸ |
|---|---|---|---|---|
| Q | 3.4e-21 | 4.9e-17 | 3.7e-17 | 1.6e-18 |
| RAR | 1.1e-18 | 2.9e-17 | 5.8e-18 | 3.8e-17 |
| MONO | 3.9e-19 | 2.9e-17 | 1.1e-17 | 1.7e-17 |
| MU2 | — | 2.8e-32 | 4.3e-33 | 2.2e-32 |
| EXP | — | 7.3e-33 | 4.6e-32 | 4.6e-32 |

Max FD residual over all checks: **4.92e-17** (ν-form branches, bisection
tolerance limited) and **4.63e-32** (explicit-map branches).

**Check 2 — empirical inversion (perturb-and-invert).** Perturb `g` by
`ε = 0.001` (relative), invert on the branch, measure
`κ_emp = (ΔB/B)/(Δg/g)`. Max relative residual vs analytic κ:
**1.19e-7** (at EXP, y=1) — dominated by the finite ε step (expected
`O(ε)`), not by the identity.

**Check 3 — substitution into the original equation.** The bisection solves
residual `|F(y) − x| < 10⁻⁴⁰`; the explicit inverses reproduce the forward
laws to 60 digits (e.g. `y_Q(1) = (√5−1)/2 = 0.6180339887498949`,
`x_Q² − (y_Q² + y_Q) = 0` at 60 dps).

**Check 4 — MONO splice continuity.** `h_mono(y*±ε) − h_RAR(y*)`:
jump `6.6e-33` (continuity); `h'_mono(y*+ε) = h'_RAR(y*) = 0.006639363412377466`
(derivative continuity at the splice).

---

## 5. Negative controls (seed step 5) — capable of failing, and observed

**NC1 — absolute conditioning used as relative (unit dependence).**
`κ_abs = |dB/dg| = 1/F'(B)` is dimensionful and unit-dependent. At `y = 1`
(Q): `κ_rel = 4/3`, `κ_abs_as_rel = 0.9428`, ratio `0.7071 = y/x ≠ 1` — the
absolute quantity fails as a relative measure and its value changes with the
acceleration unit (canonical vs alternative footing give different
`κ_abs`-derived quotients: `0.0021363` vs `0.0017732` at y=10⁻⁶). **Control
fires** (NC1 fails as required): absolute conditioning is not a surrogate for
relative conditioning.

**NC2 — limiting regimes.** Deep (`y → 0⁺`): κ → 2 for all branches
(residuals vs 2: Q `2.0e-10` at y=10⁻¹⁰, RAR/MONO `1.0e-5`, MU2 `7.5e-6`,
EXP `5.0e-6`). Newtonian (`y → ∞`): κ → 1 for all branches (residuals vs 1:
Q `5.0e-9` at y=10⁸, RAR/EXP exactly 0, MU2 `8.0e-16`, MONO `1.2e-8`).
Exact identities (κ_Q closed form, κ_RAR algebra, bounds `1 < κ_Q < 2`) are
distinguished from finite numerical consistency (grid residuals) in §2/§5.

**NC3 (implicit) — branch identity.** The audit never imports one branch to
repair another: each κ is computed from its own declared law, and the five
branch curves remain distinct on the whole grid (ordering table, §3).

---

## 6. Strongest surviving statement

> **On the declared Q branch, for every `y > 0`: `dB/dg = 1/F'(B)` exactly and
> the relative condition number is `κ_Q(y) = 2(y+1)/(2y+1)`, with exact
> bounds `1 < κ_Q < 2`, `κ_Q(1) = 4/3`, deep limit 2, Newtonian limit 1. The
> same differentiation identity is verified numerically (FD residual
> ≤ 4.9e-17, empirical residual ≤ 1.2e-7) on RAR, MU2, EXP and MONO across
> `y ∈ [10⁻¹⁰, 10⁸]`. The contract MU2 cell satisfies `mu2(1) = 5/9`,
> `mu2'(1) = 8/27`; the dispatch's `1/√2` (and `2^(−3/2)`) values belong to
> the different interpolant `x/√(1+x²)`, not to the contract cell. All exact
> statements are Lean-certified with axioms ⊆ {propext, Classical.choice,
> Quot.sound} and zero `sorry`.**

**Domain.** Exact statements: all `x, y ∈ ℝ` with the stated nonzero
conditions (Lean). Numerical statements: `y ∈ [10⁻¹⁰, 10⁸]` (grid), plus
bracketed extrapolation to the limits above; `x = g/a0 > 0`.

---

## 7. First unresolved implication and suggested follow-up

**Next unresolved implication.** The audit establishes conditioning of the
*static* branch maps `B = F⁻¹(g)`. It does **not** establish how inferred
source uncertainty in `B` (e.g. baryonic mass-to-light or distance errors)
propagates through the *filtered* MONO field equation
`ΔΦ = 4πGρ_b + S*[div((ν_mono−1)∇Su)]` — the operative gate. The bridge needed:
a bound on `‖δu‖/‖u‖` in terms of `κ_MONO` and the filter `S`'s operator norm,
i.e. `κ` for the *field* problem, not just the pointwise map.

**Suggested follow-up (child).** "AS046.C01 — filtered-MONO field conditioning":
derive `κ_field = ‖(I − S*∘div((ν_mono−1)∇S·))⁻¹‖`-style bound on the
spliced MONO operator, using the certified `κ_MONO(y)` here as the pointwise
input, with the same negative controls (absolute-as-relative; deep/Newtonian
limits). Dependency: this result (pointwise κ) + the filter `S` definition
with metric/measure/boundary conditions from the framework contract.

---

## 8. Reproducibility

- Code: `as046_inverse_conditioning.py` (sha256 `719b668e…f2aef2`)
- Raw data: `as046_raw.json` (sha256 `cb14c797…b3ab3b`), stdout
  `as046_stdout.txt` (sha256 `46e68f4e…d64480`)
- Lean certificate: `AS046_mu2_certificates.lean` (sha256 `8cefe0d5…825b7`),
  compile log `lean_compile.out` (sha256 `a93c2e50…aa9109`)
- Commands:
  - `cd fable_independent_2026/lean_2026 && timeout 550 lake env lean <abs>/AS046_mu2_certificates.lean` → exit 0, 0 errors
  - `cd <run dir> && /usr/bin/time -p timeout 300 python3 as046_inverse_conditioning.py as046_raw.json` → exit 0
- Bounds actually enforced: wall 0.50 s (limit 120 s), RSS 18.5 MB (limit
  512 MB), 1 thread (`threads: 1`); Lean: timeout 550 s.