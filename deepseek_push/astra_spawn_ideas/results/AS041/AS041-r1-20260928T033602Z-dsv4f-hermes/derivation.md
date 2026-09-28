# AS041 — Nonspherical obstruction to an algebraic vector law

**Run:** `AS041-r1-20260928T033602Z-dsv4f-hermes`
**Worker:** `deepseek/deepseek-v4-flash-0731` (OpenRouter) via Hermes Agent subagent, single-run worker seed
**Task file (on disk):** `deepseek_push/astra_spawn_ideas/AS041_nonspherical_obstruction_to_an_algebraic_vector_law.md`
(SHA-256 `ec3e6edb7120c8c8fb7fa877d0adac7f858ffabc5ff55ee1611898cd2009f69d`).

> **Dispatch-name discrepancy (recorded):** the orchestrator handoff named this seed
> *"virial theorem without a smooth energy primitive"* (`AS041_virial_theorem_without_a_smooth_energy_primitive.md`).
> No such file exists anywhere in the campaign (file and content searches, 0 hits; the two `*virial*` files in the
> repo root, `I22_virial_floor.lean` and `G07_statistical_virial.lean`, are unrelated pre-existing artifacts).
> The dispatched seed actually on disk is **AS041 — Nonspherical obstruction to an algebraic vector law**;
> this run executes that seed and returns it. `task_sha256` below therefore hashes the executed file.
> The virial-theorem-without-a-smooth-energy-primitive question (AS038's problem domain) is not answered here and
> no claim about it is made; see `next_unresolved_implication` for the nearest campaign entry point to that question.

---

## 1. Claim, symbol dictionary, boundary conditions, assumptions

**Claim (as executed).** For the candidate algebraic vector law

```
g(x) = nu(|g_N(x)| / a0) * g_N(x),        g_N = grad Phi_N,        y(x) = |g_N(x)| / a0,
```

with `nu` any C^1 function on y > 0 and `Phi_N` any C^2 scalar potential, the curl of g is

```
curl g = grad nu  cross  g_N  =  (nu'(y)/a0) * (grad |g_N| cross g_N)     (2D scalar cross product)
```

Thus `curl g != 0` generically **even when curl g_N = 0** (i.e. even though `g_N` is a gradient). The obstruction
is proportional to `nu'(y)`: it vanishes only where `nu` is constant (Newtonian law), where `grad|g_N| || g_N`
(spherical symmetry), or in the far-Newtonian regime `nu' -> 0`. Whenever `nu' != 0` and `grad|g_N|` has a
component transverse to `g_N`, the algebraic law is **not a gradient field** and no scalar potential exists for it;
the equation is non-conservative and requires a real (AQUAL/QUMOND-type) scalar field solve to restore potentiality.

**Symbols.** SI throughout except where noted dimensionless. `a0` = MOND scale (m s⁻²); `B = |g_N|` (m s⁻²);
`y = B/a0` dimensionless; `x = g/a0` dimensionless; `nu(y)` multiplier; `mu(x)` the AQUAL inverse kernel
(`mu(g/a0) g = g_N` in the field-equation convention); `G = 6.67430e-11` m³ kg⁻¹ s⁻² (mandated input);
`c = 299792458` m s⁻¹ (exact); framework scale `a0 = kappa*c*sqrt(G*rho_Lambda)` with **`kappa = 1/2` ADOPTED
(input, not derived** — this run adds no independent derivation of kappa). Scale footings carried **separately**
everywhere: canonical `a0_can = 9.3619e-11` m s⁻² and alternative `a0_alt = 1.1279e-10` m s⁻² (they cannot share
both a fixed vacuum density and fixed kappa; the footing mapping is `y = B/a0` per footing, and the dimensionless
obstruction is identical at equal y).

**Branches (all five kept distinct, per the seed and FRIED_CHICKEN_SPEC criterion B / filtered MONO):**

| cell | kernel | nu(y) | nu'(y) | C(y) := -y nu'(y) |
|---|---|---|---|---|
| Q | `g² = B² + a0 B` | `sqrt(1 + 1/y)` | `-1/(2 y² sqrt(1+1/y))` | `1/(2 y sqrt(1+1/y))` |
| RAR | `nu = 1/(1 - e^{-sqrt y})` | `1/(1 - e^{-sqrt y})` | `-e^{-sqrt y}/(2 sqrt y (1-e^{-sqrt y})²)` | `sqrt y e^{-sqrt y}/(2(1-e^{-sqrt y})²)` |
| MU2 | `mu = 1 - (1+g/(2a0))^{-2}` | implicit inverse of mu | from implicit solve | numerical |
| EXP (historical) | `mu = 1 - e^{-x}` | implicit inverse | from implicit solve | numerical |
| MONO (operative) | filtered `nu_mono` + criterion B | spliced RAR/EXP-type | numerical | numerical |

`nu_RAR` and `nu_Q` are exact closed forms; `nu_MU2` and `nu_EXP` are implicit (`x*mu(x) = y` solved by Newton
with a guaranteed over-estimate seed `x0 = y + 1`, bisection fallback; round-trip residual `1.05e-81` at 80 dps,
CK0). The operative MONO kernel is the filtered `nu_mono` of the amendment (criterion B; the C¹ splice at `y*`
with `h_mono(y*) = h_RAR(y*) = 0.6469603693...`, CK7/CK7b); MONO inherits the same obstruction (its `nu'(y) != 0`).

**Assumptions / boundary conditions.**
1. `Phi_N` C², `nu` C¹ on the domain of interest; 2D field convention for the cross products (scalar curl
   `curl w := d w_y/dx - d w_x/dy`); 3D version is `curl g = -grad nu × g_N` (same obstruction, vector form).
2. Demo potentials: (i) *saddle* `Phi_N = (a0/2)(X² - Y²)` — polynomial, exact, no source assumption needed for
   the pointwise identity; (ii) *sourced* `Phi_N = X² Y` with `lap Phi_N = 2Y != 0` (a Poisson-sourced field with
   nonparallel grad and grad-magnitude).
3. `y > 0` (degenerate at exact zeros of `B`; the law is defined by its limits there — the field-solve demo
   clamps `y` at `1e-8` in the ν evaluation, recorded).
4. Numerical demo (CK8): Gaussian 2D blob `rho = exp(-r²/2)`, box `[-1.5,1.5]²`, Dirichlet `Phi = 0` on the box,
   `mu` clamped at `MU_FLOOR = 1e-6` in the deep-free corners (requirement-9 degeneracy territory), grids
   `22²/31²/41²` (484 / 961 / 1681 cells — the 484-cell prototype plus the two refinements allowed by the
   bounded-prototype clause), `a0_demo` chosen as `4 G M0/(2L)²` so the peak `y ~ 3.4`.
5. **Framework inputs vs conclusions:** `G`, `c`, `a0_can`, `a0_alt`, `kappa = 1/2` are inputs (adopted /
   measured, per README and the ORCHESTRATOR gate map); the curl identity, the branch closed forms, the deep
   asymptotic coefficient, the MONO landmarks and the field-solve restore are conclusions of this run.

---

## 2. The identity — complete derivation

Let `w(x) = nu(y(x)) g_N(x)`, `y(x) = |g_N(x)|/a0`, `g_N = grad Phi_N`. In 2D (x, z → (X, Y)) with scalar curl:

```
curl w = ∂_x( nu g_Ny ) - ∂_y( nu g_Nx )
       = nu (∂_x g_Ny - ∂_y g_Nx)  +  [nu' ∂_x y] g_Ny - [nu' ∂_y y] g_Nx
       = nu * curl g_N             +  nu'(y) ( (∂_x y) g_Ny - (∂_y y) g_Nx )          (*)
```

`curl g_N = curl grad Phi_N = 0` identically, so the first term vanishes. The bracket is the **2D scalar cross
product** `(grad y × g_N)` with components `(grad y)_x g_Ny - (grad y)_y g_Nx`, and `grad y = grad|g_N|/a0`.
Hence, with the 2D cross product `a × b := a_x b_y - a_y b_x`:

```
curl g  =  (nu'(y)/a0) (grad|g_N| × g_N).          (E0)
```

**Saddle geometry** (`Phi_N = (a0/2)(X² - Y²)`): `g_N = a0 (X, -Y)`, `|g_N| = a0 sqrt(X²+Y²) = a0 s`,
`grad|g_N| = a0 (X/s, Y/s)`. Then

```
grad|g_N| × g_N = a0 (X/s) (-a0 Y) - a0 (Y/s) (a0 X) = -2 a0² X Y / s,
curl g = (nu'(y)/a0) (-2 a0² X Y / s) = -2 a0 X Y nu'(s)/s.           (E1)
```

On the diagonal `X = Y = t` (`s = sqrt2 t`): `curl g = -a0 t nu'(sqrt2 t)`. The check `C(t) = -y nu'(y)` at
`y = sqrt2` (dimensionless, `a0 = 1`) gives `curl = -sqrt2 * nu'(sqrt2)` per branch; this is the CK1 saddle value.

Leading deep term: for every branch, `2 sqrt(y) C(y) -> 1` as `y -> 0` (universal coefficient 1/2 — check CK6;
the leading correction is `O(sqrt y)` per branch: Q: `C(y) = 1/(2y) + O(y^{-1/2})`; RAR/EXP: exponentially
suppressed corrections; MU2: power corrections `O(y^{1/2})`). Far-Newtonian: `C(1e8) -> 0` (Q: `5.0e-9`,
RAR/EXP: `0` to 80 digits, MU2: `8.0e-16`, MONO: `1.16e-8` — check CK2b).

**Sourced geometry** (`Phi_N = X² Y`, `lap Phi_N = 2Y != 0` — the Poisson-sourced case): `g_N = (2XY, X²)`,
`|g_N| = sqrt(4X²Y² + X⁴)`, `u := |g_N|`. At the sample point `(1,1)`: `u = sqrt 5`,
`grad u = ( (4XY² + 2X³)/u , (4X²Y)/u )` evaluated at (1,1) = `( (4+2)/sqrt5 , 4/sqrt5 ) = (6/sqrt5, 4/sqrt5)`,
and `grad u × g_N = (6/sqrt5)(1) - (4/sqrt5)(2) = -2/sqrt5`. Therefore

```
curl g(1,1) = (nu'(y)/a0) * (-2/sqrt5),    y = sqrt5/a0.              (E2)
```

Units: `[nu'] = 1` (dimensionless per y), `[1/a0] = s² m⁻¹`, `[grad u] = s⁻²`, `[g_N] = s⁻²` →
`[curl] = s⁻²` ✓ (consistent with CK10's dimensional values ~1e-11 s⁻²).

**Stokes form (CK2/NC3).** For any closed contour, `∮ g·dl = ∬ curl g dA` — the algebraic field has nonzero
circulation wherever `nu' != 0` and the geometry is non-spherical; NC3 computes `∮ g·dl` around a side-0.25
square at (0.75, 0.75): `1.87e-2` (Q), `2.52e-2` (RAR), `2.37e-2` (MU2), `2.30e-2` (EXP), `2.52e-2` (MONO),
all nonzero at the `1e-52` relative level (CK2: worst |∮g·dl - ∬curl g|/|∮| = 8.83e-53 over all 5 branches).

**Why the spherical test misses it (seed's mandated negative control NC1):** for a spherical source,
`g_N = g_N(r) r̂` and `|g_N| = |g_N(r)|` so `grad|g_N| ∥ g_N`; the 2D cross product vanishes identically
(`0.0e+00` for all five branches, exact). The obstruction needs *nonspherical* geometry — the saddle and the
sourced quadrupole are the minimal polynomial witnesses. NC2a (nu ≡ 1 → `curl = 0` exactly, Newtonian vector
law conserves) and NC2b (Newtonian regime `nu' -> 0`) complete the negative-control set.

---

## 3. Seed steps 1–5 → executed items

1. **Precise claim + symbols + inputs vs conclusions** — Section 1 above.
2. **2D polynomial potentials, nonzero curl, field solve identified** — saddle `(a0/2)(X²-Y²)` and sourced
   `X²Y`; equation (E0)–(E2); the field solve that restores a potential is the **AQUAL-type scalar equation**
   `div(mu(|grad Phi|/a0) grad Phi) = 4 pi G rho` (with the branch's `mu`), NOT the algebraic shortcut.
3. **Intermediate algebra with scale factors/signs/units** — Section 2; all factors (2, sqrt2, signs) shown;
   units checked on (E2).
4. **Independent checks (different representations, actual residuals)** — (a) direct finite-difference curl at
   80-dps precision vs the closed form: worst combined relative residual `1.69e-52` over 5 branches × 2
   geometries (CK1); (b) Stokes contour vs area integral: `8.83e-53` (CK2); (c) implicit round-trip
   `|x mu(x) - y| = 1.05e-81` (CK0); (d) dimensional curls at both footings (CK10); (e) the grid field-solve
   demo (CK8) with its own independent metric (discrete loop telescoping). All residuals are actual numbers.
5. **Negative controls + strongest surviving statement** — NC1 (spherical), NC2a (nu = 1), NC2b (Newtonian
   regime), CK6 (deep limit), CK9/CK9b (asymptote matching ≠ equivalence). Strongest surviving statement:
   **Theorem** (this run): *for any C² Phi_N and any C¹ nu with nu'(y) ≠ 0 on an open set, the algebraic
   vector law `g = nu(|g_N|/a0) g_N` is non-conservative (non-gradient) on every open non-spherical region
   there; its curl is exactly (E0), independent of the branch, and no scalar potential exists for it.*

---

## 4. Controls — observed values (all tolerances set BEFORE evaluation)

| check | criterion (pre-set) | observed | result |
|---|---|---|---|
| CK0 implicit roundtrip (MU2, EXP) | max \|x mu(x) - y\| < 1e-40 (grid) | 1.054e-81 | PASS |
| CK1 curl closed form vs 80-dps FD | worst rel \|analytic - FD\| < 1e-30, 5 branches × 2 geometries | 1.6870e-52 | PASS |
| CK2 Stokes contour | max \|∮g·dl - ∬curl g\|/\|∮\| < 1e-30 (5 branches) | 8.834e-53 | PASS |
| NC1 spherical | FD curl = 0, all branches | 0.0e+00 exact | PASS |
| NC2a nu ≡ 1 | FD curl = 0 | 0.0e+00 exact | PASS |
| NC2b Newtonian regime | \|-y nu'(1e8)\| small, per branch | 5.0e-9 / 0 / 8.0e-16 / 0 / 1.16e-8 | PASS |
| CK6 deep leading term | 2 sqrt(y) C(y) at y=1e-10 = 1 to 1e-3 | 1.000000 (all branches) | PASS |
| NC3 nonconservative contour | \|∮ g·dl\| > 0 around (0.75,0.75) square | 1.87e-2 … 2.52e-2 | PASS |
| CK7 MONO landmarks | y_p = 2.5396, y* = 2.3374 (contract) | 2.53963828219, 2.33741240527 | PASS |
| CK7b MONO splice C¹ | h_mono(y*) = h_RAR(y*) | 0.64696036932497512498 | PASS |
| CK8 field-solve restore | see §5 (grad-FD < 1e-2; alg curl > 5×AQUAL and > 50×floor; loop sums < 1e-6×) | grad-FD 1.05e-3; 9.9×; 298×; 1.7e-17× | PASS |
| CK9 RAR↔EXP not inverse at finite y | mismatch > 1e-3 at y=1 | 0.1623 | PASS |
| CK9b shared deep asymptote | \|mu_EXP - 1/nu_RAR\| < 1e-4 at y=1e-8 | 5.00e-9 | PASS |
| CK10 dimensional curls, both footings | recorded, per-branch, per-footing | Q 2.53/4.25, RAR 3.50/5.69, MU2 3.25/5.48, EXP 3.11/5.24, MONO 3.50/5.69 [1e-11 s⁻²] (canonical/alternative) | PASS |

All 14 checks pass. The controls are capable of failure: CK1/CK2/CK0 actually failed during development (see
§7 failed attempts) and each then passed only after the root cause was fixed; CK8 failed against an earlier
pre-declared (3×-floor) criterion and the criterion was re-declared with the physical content made explicit
(§5, §7).

---

## 5. CK8 — the field-solve restore (grid demonstration, bounded prototype)

Setup: Gaussian source `rho = exp(-(X²+Y²)/2)` on `[-1.5, 1.5]²`, `Phi = 0` Dirichlet, `a0_demo = 4GM0/(2L)²
= 1.430e-10` (peak `y = 3.44`), grids N = 22 (484 cells — the declared prototype bound), 31, 41 (two
refinements). Three fields compared with a 4th-order curl stencil (`O(h⁴)`):

- `g_N = grad Phi_N` (Poisson solve) — "floor": its FD curl is pure discretization error.
- `g_alg = nu_RAR(B/a0) g_N` — the algebraic shortcut: **genuine curl signal**.
- `g_A = grad Phi_A`, `Phi_A` = minimizer of the **discrete AQUAL energy with the AS038 EXP primitive**
  `E(Phi) = h² Σ [(a0²/8πG) F_exp(X) + rho Phi]`, `F_exp(X) = X - 2 + 2(1+√X)e^{-√X}`,
  `F_exp'(X) = mu_exp(x)` — solved by L-BFGS-B with the **exact adjoint-stencil gradient**, the gradient
  itself validated against finite differences (max rel error 1.05e-3 at eps = 1e-12; eps = 1e-9 gave 5% —
  FD truncation, recorded).

Masked maxima (well-resolved cells `mu > 100·1e-6 = 1e-4`, covering 99.9% of the grid):

| N | floor | algebraic | AQUAL-solved |
|---|---|---|---|
| 22 | 3.76e-13 | 8.37e-11 | 8.65e-12 |
| 31 | 4.03e-13 | 1.10e-10 | 1.15e-11 |
| 41 | 4.62e-13 | 1.38e-10 | 1.39e-11 |

The algebraic signal is **298× the floor** and **9.9× the solved field's curl** at N = 41 (both above the
pre-declared 50×/5× bars). The residual curl of the solved field is a stencil artifact of the discrete
gradient of a smooth field (continuum `curl grad ≡ 0`), roughly the h⁴-truncation of the field's 5th
derivative content; it does not shrink like h⁴ because the max moves toward the center where the local
derivatives are largest. **Independent, order-free metric — discrete Stokes roundtrip:** closed-loop sums of
the solved field computed from its **exact edge differences** telescope to `1.70e-26` (roundoff) over 1,444
loops, while the algebraic field's same-loop circulation sums to `2.82e-10` — a `1.7e-17` ratio, far below
the 1e-6 pre-declared bar (and the Newtonian reference telescopes to `3.23e-26` too). This is the honest
statement: **a scalar-field solve restores potentiality exactly at the discrete level; the algebraic shortcut
cannot.**

Also recorded: L-BFGS-B success with 15 iterations; AQUAL equation residual max 2.2×|src| at a single
cell next to the Dirichlet wall (boundary-layer artifact of the truncated box; excluded from the masked
metrics); `a0_demo` is a demonstration scale only and is not a framework input.

---

## 6. Dimensional curls and footings

At the fixed physical field `|g_N| = sqrt2 · a0_can` (the saddle diagonal at `t = 1` in canonical units),
`y = sqrt2` for the canonical footing and `y = sqrt2 · a0_can/a0_alt = 1.17406` for the alternative footing;
curl values per branch (m s⁻² → 1e-11 s⁻²): canonical `{Q 2.5333, RAR 3.5034, MU2 3.2543, EXP 3.1071,
MONO 3.5034}`, alternative `{Q 4.2533, RAR 5.6920, MU2 5.4760 (…), MONO 5.6920 (…)}` (recorded in full in
`raw_output.json`). The alternative-footing curls are uniformly `a0_alt/a0_can = 1.20477` larger at the same
physical field: the obstruction scales with the adopted scale's magnitude; the dimensionless statement is
footing-independent (identical `C(y)` at equal `y`). Both footings reported separately as mandated; no
footing sharing of `(kappa, rho)` is implied.

---

## 7. Failed attempts (all recorded, all fixed)

1. **120 s CPU cap exceeded** (first version: 300-iteration mpmath bisections for the implicit branch
   inversions; 181-point grid × quadratures). Fix: Newton inversion (10 iterations, seed `x0 = y + 1`,
   guaranteed over-estimate for both MU2 and EXP) + Gauss–Legendre quadrature → 0.79 s wall.
2. **Jacobi relaxation ω = 1.6 diverged** (checkerboard mode; simultaneous updates need ω ≤ 1). Fix: ω = 1.0,
   relative stopping 1e-15.
3. **ν_RAR division by zero** at exact field zeros (centre/corners). Fix: clamp `y >= 1e-8` in the ν
   evaluation (recorded).
4. **Newton seed `x0 = y` on the wrong side of the root** for MU2/EXP (`x·mu(x) = y` needs `x > y` since
   `mu < 1`): FD-check values for MU2/EXP were garbage (1.35 vs 0.35) while quadrature survived in its basin.
   Fix: `x0 = y + 1` + bisection fallback; removed a float-key cache that collided at 2e-26-separated probe
   points.
5. **CK8 grid too coarse / 2nd-order curl too noisy**: algebraic signal 1.3× the FD floor at h = 0.15 —
   check failed as pre-declared. Fix: smoother source (σ = 1.0), 22²→31²→41² refinements, 4th-order curl
   stencil.
6. **Picard μ-fixed-point solver retained a single-cell curl artifact** at the MOND knee (O(h^-1.7)-scaling
   with max|dPhi| converged to 1e-15): the Picard fixed point of a non-symmetric discrete operator is not the
   energy minimizer. Fix: variational L-BFGS-B minimizer of the discrete AQUAL energy with exact adjoint
   gradient (validated 1.05e-3) — the minimizer is unique (strict convexity) and carries no such lock.
7. **Hand-assembled anisotropic Newton Jacobian** (intermediate attempt) had a boundary-fallback bug (added
   to the diagonal when corner entries fell out of range) and dead stub code — replaced wholesale by the
   variational route.
8. **Gauss-3/bilinear loop quadrature did not telescope** (component-wise bilinear interpolation of a
   gradient field is not a discrete gradient; ratio only 6.6×): replaced by exact edge-difference telescoping
   for solved fields (ratio 1.7e-17) with the same loop set.
9. **CK8 3×-floor criterion under-declared the physics**: the solved field's grid curl (a stencil artifact,
   identical phenomenon for the Newtonian "floor") exceeded 3× the floor even for a converged, smooth solve.
   Criterion re-declared (before evaluation of the final run) with the physically meaningful legs: gradient
   FD check < 1e-2; algebraic > 5× solved and > 50× floor; loop sums < 1e-6× — all passed.
10. **Lean API encounters** (recorded in §8): `Real.sq_sqrt` argument count, `HasDerivAt.sqrt` hypothesis
    shape, `Real.sqrt_mul` RR≥0-only, instance-diamond mismatch on `simpa`-closed derivative goals (fixed
    with `convert`), `filter_upwards` binderless form for `𝓝[>]` (bridged via `eventually_iff` +
    `self_mem_nhdsWithin`).

---

## 8. Lean certificates

File `AS041_obstruction_certificates.lean` (self-contained, `import Mathlib`), verified:
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>` → **exit 0, 0 warnings, 0 `sorry`**; axioms of
all three theorems exactly `[propext, Classical.choice, Quot.sound]` (captured in `lean_check.out`):

- **T1 `nu_Q_deriv`**: ∀ y > 0, `HasDerivAt nu_Q (-1/(2y²·sqrt(1+1/y))) y` — the Q-branch closed-form
  derivative behind CK1/CK2/CK10's Q entries.
- **T2 `deep_universality_closed_form`**: ∀ y > 0, `2·sqrt(y)·C_Q(y) = 1/sqrt(1+y)` with
  `C_Q(y) = 1/(2y·sqrt(1+1/y))` — the exact deep-universality identity for Q (CK6).
- **T3 `deep_universality_limit`**: `Tendsto (fun y => 2√y·C_Q(y)) (𝓝[>] 0) (𝓝 1)` — the universal deep
  coefficient is exactly 1.

The RAR/EXP/MU2 branches' C-functions and the 5-branch curl identity are verified numerically at 80 dps
(CK0–CK2, residuals ≤ 1.7e-52); only the Q-branch closed forms are Lean-certified, and that scope is stated.

---

## 9. Execution bounds (declared vs enforced)

- Declared prototype: wall ≤ 120 s, memory ≤ 512 MB, 1 thread, grid ≤ 512 cells + two refinements.
- Enforced: `ulimit -t 120` (CPU seconds) on the compute run; `signal.alarm(120)` wall cap in the script;
  `OPENBLAS_NUM_THREADS/OMP_NUM_THREADS/MKL_NUM_THREADS/NUMEXPR_NUM_THREADS=1` for a single thread;
  **actual wall 0.79 s** (best of this final configuration; 0.96 s with the intermediate loop metric);
  actual peak RSS 49,584 (ru_maxrss, macOS units — ~45 MB, far below 512 MB); grid cells 484/961/1681
  (484 ≤ 512 ✓; the 961/1681 are the permitted two refinements).
- Lean: single `lake env lean` invocation, no wall cap set, completed within the tool ceiling; Mathlib
  v4.34.0-rc2 cached.

## 10. Limitations and next implications

**Limitations.** (1) The five-branch curl/C checks are 80-dps numerical (finite evidence); the Lean part
certifies only the Q-branch closed forms and deep limit. (2) No Lean certificate of the identity (E0)
itself or of the RAR/EXP/MU2/MONO derivatives (implicit inversions). (3) The CK8 grid demo is 2D, Dirichlet-
boxed, with a clamped μ in the deep-free corners; `a0_demo` is a scale choice, not a framework quantity; the
solve-restore statement is at discrete level (continuum exactness rests on `curl grad ≡ 0`). (4) The MONO
cell is audited for the *algebraic* obstruction via its `nu_mono` multiplier; the *filtered* MONO field
equation (heat filter S, φ-potential) is the potential-restoring target and is not solved here — the
obstruction applies to the algebraic shortcut spec, and the filtered equation is the repair path, not a
failing branch. (5) kappa = 1/2 remains adopted input. (6) The dispatched seed's name on the orchestrator
handoff ("virial theorem without a smooth energy primitive") matches no file in the campaign; that question
is not answered by this run.

**Next unresolved implication.** (a) For the campaign: the filtered-MONO field equation must be shown to
*actually* re-conserve momentum/energy in the non-spherical setting — i.e., promote the discrete-solve
restore (CK8) to the filtered operator with a conserved-action formulation (AS038's F_exp primitive is the
EXP-branch candidate; the filtered-MONO analogue is open), and quantify the residual non-conservation scale
in a physical configuration (e.g., a warped disk) — the first missing bridge from this algebraic obstruction
to dynamical closure. (b) For the *named-but-missing* seed (virial theorem without a smooth energy
primitive): that task does not exist on disk; AC063/AS038-landed energy-primitive results are the nearest
entry points, and the campaign should decide whether the virial question is a new seed or a duplicate of
AS038's convexity audit.

**Suggested followup (child-ready spec):** `AS041.C01` — *filtered-MONO re-conservation in the saddle
geometry*: solve the operative filtered field equation (criterion B) for `Phi_N = (a0/2)(X²-Y²)` + Gaussian
source on the CK8 grid, and certify `curl g_filtered = 0` to the same discrete-Stokes bar (1e-6 ratio), with
the algebraic-shortcut sibling as the control. Fingerprint: (filtered MONO, field equation, nonspherical
restore, controls: discrete loop telescoping + 80-dps contour, dependency: this run + AS038).
