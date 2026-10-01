# CFG240 FROZEN CRITERIA (phase 1): the BARYON-CALIBRATION WALL as a Lean theorem, plus a numeric Fisher companion

> **Status: criteria frozen BEFORE any proof of the new theorems is written and BEFORE any Fisher table exists.** Lane CFG240, phase 1. Nothing in the repo was edited or created by phase 1; this file is the only deliverable. kappa = 1/2 is FITTED. Lean certifies an IMPLICATION from stated premises, not any empirical fact (section 0). No sentence here says any data favour any law: this lane has no data.

## Reading order / what was decided in phase 1
1. The orchestrator's hand derivation for P2 is **CHECKED and CONFIRMED** (algebra by hand, by sympy, and by a scratch Lean proof of T2a that compiles, see section 1.6). Exact injectivity of (f, a0) -> (g_obs(g1), g_obs(g2)) holds for exact P2 for ANY two distinct positive g_bar values; no "not deep" requirement appears in the exact statement. The practical transition requirement is a CONDITIONING statement (T2c, T4), and it is sharper than the brief anticipated: the Jacobian determinant is exactly `b(y2) - b(y1)` for every kernel (rows `(1-b, b)`, section 1.4), and no sample of N points at sigma dex can beat `sigma(log a0) >= 3 sigma/sqrt(N)` with f free (T4, proved by hand, one line in Lean).
2. nu_mono: injectivity from two points is **formalisable via one kernel-general theorem (T2e)** whose single premise is strict convexity of `L(u) = log(e^u nu(e^u))` (equivalently a strictly increasing log-slope of `y nu(y)`). For P2 the direct algebraic proof (T2a) suffices. For nu_mono the premise reduces to "s/(e^s - 1) is strictly decreasing" (section 2). Attempted in phase 2 as a stretch item; the fallback is frozen in section 2.
3. All 36 statements below elaborate (scratch typecheck, Lean 4.34.0-rc2, Mathlib in the repo's lake project): 0 errors, 36 `declaration uses sorry` warnings (phase 1 only).

## 0. What Lean does and does not certify here (this paragraph goes verbatim into CalibrationWall.lean's header)
CERTIFIED (premises => conclusions, in Lean): for the declared law `g_obs = (f g) nu((f g)/a0)` (f > 0 a single multiplicative calibration of g_bar, the same f and a0 at every point), (T1) the deep-regime law, its dependence on (f, a0) only through f*a0, and the exact P2 identity g_obs^2 = f^2 g^2 + (f a0) g with the exact relative-difference bound between equal-product pairs; (T2) exact two-point injectivity for P2 and its failure at one point and for the deep kernel; the closed-form Jacobian and its degeneration; (T3) the Newtonian limit; (T4) a design bound on the Fisher matrix.
NOT CERTIFIED: that a calibration factor f exists in any survey, its size, its redshift dependence, that a0 is the same for all points, that nature follows P2 or nu_mono, any statistical statement (Fisher information is a numeric companion, not a Lean theorem), any other systematic (selection, mass-to-light, gas, non-circular motion), non-multiplicative calibrations (offsets, g-dependent f), and kappa (FITTED at 1/2). Lean has no data and says nothing about whether the wall is binding in the real data; the wall is a statement about what the declared law CAN identify.

## 1. Statements

### 1.1 Setting (declared, not decided)
`gObs nu f a0 g := (f*g) * nu((f*g)/a0)`: the kernel law g_obs = g_bar nu(g_bar/a0) with g_bar replaced by f g_bar. Kernels (declared choices): `nuP2 y = sqrt(1 + 1/y)` (the record's P2; equals `nuBeta 1 y` for y > 0, `nuP2_eq_nuBeta`, reusing `C2_nuBeta_one`), `nuDeep y = 1/sqrt y` (deep-MOND form), `nuMono y = 1/(1 - exp(-sqrt y))` (Kernel.lean, existing). `yOf s t g = exp s * g / exp t` is y at the TRUE (f, a0) with s = log f, t = log a0.

**Which y?** y = f g_bar / a0 at the TRUE (f, a0): this is the argument actually fed to nu, so the local sensitivity of log g_obs to (log f, log a0) is a function of this y alone (section 1.4), and the Fisher matrix of a sample depends on the sample only through the multiset of these y. The nominal ratio y_nom = g_bar/a0 equals y/f; they coincide only at f = 1. The numeric companion samples y_true, and reports y_nom = y/f0 for f0 != 1 (section 3).

### 1.2 T1: the deep-regime wall (all with f, a0, f', a0', g > 0)
* **T1a (exact deep law).** For nu(y) = 1/sqrt y: `g_obs = sqrt(f a0 g)`. (`T1_deep_law`)
* **T1b (equal products).** f a0 = f' a0' => g_obs(f, a0; g) = g_obs(f', a0'; g) for every g > 0, deep kernel. (`T1_deep_equal_products`) And the converse, so the dependence is ONLY through f a0: `(for all g > 0, equal g_obs) <=> f a0 = f' a0'`. (`T1_deep_iff`)
* **T1c (drift mimicry).** For c > 0: g_obs(c f, a0) = g_obs(f, c a0) = sqrt(c) g_obs(f, a0) and log g_obs shifts by (log c)/2 in both cases. This is exactly CFG255's "delta in log f moves log g_obs by delta/2, as a delta in log a0 does". (`T1_deep_drift`)
* **T1d (P2 exact, the quantitative statement).** `g_obs^2 = f^2 g^2 + (f a0) g = (f a0) g (1 + y)`, y = f g/a0 (`P2_sq`, `P2_sq_y`). For f a0 = f' a0' = p, with rho = f'/f and y = f g/a0 of the FIRST pair: the second pair has y' = rho^2 y and the EXACT ratio is
  `g_obs'^2 / g_obs^2 = (1 + rho^2 y)/(1 + y)`, equivalently `(g_obs'^2 - g_obs^2)/g_obs^2 = (rho^2 - 1) y/(1 + y)`.
  Lean (division-free): `g_obs'^2 (f^2 g + f a0) = g_obs^2 (f'^2 g + f a0)` (`T1_P2_ratio`) and the bound `|g_obs'^2 - g_obs^2| (f a0) <= |f'^2 - f^2| g g_obs^2` (`T1_P2_bound`), i.e. relative difference `<= |1 - rho^2| y`, which vanishes linearly as y -> 0; and `g_obs'/g_obs -> 1` as g -> 0+ (`T1_P2_limit`). [Hand check: (g'^2 - g^2) = (f'^2 - f^2) g^2 and g^2 >= f a0 g give the bound; y' = f' g/a0' = rho^2 y because a0' = f a0/f'.]
* **T1e (any kernel with C2's deep premise).** If nu(y) sqrt(y) -> 1 as y -> 0+ (the premise of C2, proved for nu_mono in Kernel.lean and for P2) then `g_obs/sqrt(f a0 g) -> 1` as g -> 0+ (`T1_general_limit`), hence for equal products `g_obs'/g_obs -> 1` (`T1_general_equal_products_limit`). So the wall is a property of the deep-limit premise, not of P2 or nu_mono specifically. (Rate: not stated in general; P2's rate is T1d.)

### 1.3 T2: identifiability
* **T2a (exact injectivity, P2).** f, f', a0, a0' > 0; g1, g2 > 0; g1 != g2; g_obs(f, a0; g_i) = g_obs(f', a0'; g_i) for i = 1, 2 => f = f' and a0 = a0'. (`T2a_P2_injective`.) Inversion (`T2a_inversion`): with A_i = g_obs(g_i)^2, `A1/g1 - A2/g2 = f^2 (g1 - g2)`, so `f^2 = (A1/g1 - A2/g2)/(g1 - g2)` and `f a0 = A1/g1 - f^2 g1`. **Minimal hypotheses:** positivity of f, f' (so g_obs^2 = f^2 g^2 + f a0 g holds and the sign of f is fixed by f^2 = f'^2), a0, a0' > 0 (so the square root is of a positive number and P2_sq holds), g1, g2 > 0, and g1 != g2. No "not deep" hypothesis is needed. **Orchestrator's derivation: confirmed.**
* **T2a' (one point is not enough, even for P2).** For every f, a0, g > 0 there are f' != f, a0' > 0 with the same g_obs at that g (`T2a_one_point_fails`; witness f' = f/2, a0' = (3/2) f g + 2 a0).
* **T2b (deep kernel: not injective).** There exist (f, a0) != (f', a0') (e.g. (1, 1) and (2, 1/2)), all positive, with g_obs equal at EVERY g > 0 (`T2b_deep_not_injective`); with T1b the full statement is T1_deep_iff. Two points do not help: the map factors through f a0.
* **T2c (conditioning, closed form; P2).** With s = log f, t = log a0, y = f g/a0 (true), d(log g_obs)/ds = `(1 + 2y)/(2(1 + y))`, d(log g_obs)/dt = `1/(2(1 + y))` (`T2c_dlogf`, `T2c_dloga`, `HasDerivAt`; they are the same numbers for log10 g_obs and (log10 f, log10 a0): the ln 10 factors cancel). The rows are `(1 - b, b)` with `b(y) = 1/(2(1 + y))` (`T2c_rows`). Hence for two points y1, y2 > 0 the Jacobian determinant of (log f, log a0) -> (log g_obs(g1), log g_obs(g2)) is
  `det = (y1 - y2)/(2 (1 + y1)(1 + y2)) = (1/(1 + y2) - 1/(1 + y1))/2 = b(y2) - b(y1)` (`T2c_det`, kernel-general form `T2c_det_general`: `(1-b1) b2 - b1 (1-b2) = b2 - b1`).
  It is nonzero iff y1 != y2 iff g1 != g2 (`T2c_det_ne_zero_iff`, using `T2c_yratio`: y1/y2 = g1/g2), and
  `|det| <= |y1 - y2|/2`, `|det| <= 1/(2(1 + min(y1, y2)))`, `|det| < 1/2` (`T2c_det_bounds`).
  So det -> 0 when BOTH points go deep (|det| <= max(y)/2) AND when both go Newtonian (|det| <= 1/(2(1 + min y))); it approaches its supremum 1/2 only for one point deep and one point Newtonian. For N points the Fisher determinant is `det F = (1/sigma^4) * (1/2) sum_{i,j} (b_i - b_j)^2` (`T2c_fisher_det`), zero iff all b_i are equal (`T2c_fisher_singular_iff`), i.e. iff all y_i are equal for P2 (b strictly monotone in y).
* **T2e (kernel-general two-point injectivity).** Let nu > 0 on (0, inf) and suppose `L(u) = log(e^u nu(e^u))` is STRICTLY CONVEX on R. Then for g1 != g2, g_i > 0, equality of g_obs at both points forces (f, a0) = (f', a0'). (`T2e_injective_of_strictConvex`.) Proof sketch (frozen): g_obs = a0 psi(f g/a0), psi(y) = y nu(y); log g_obs = t + L(s - t + u), u = log g; equality at u1 != u2 gives `L(m + u1) - L(m + u2) = L(m' + u1) - L(m' + u2)` with m = s - t; strict convexity makes `m -> L(m + u2) - L(m + u1)` strictly monotone (two uses of `StrictConvexOn.secant_strict_mono`), so m = m', then t = t', s = s'. Equivalent local statement: the log-slope eta = L' = d log(y nu)/d log y is strictly monotone, and det = b(y2) - b(y1) with b = 1 - eta.
* **T2f (nu_mono instance; STRETCH, section 2).** `nuMono_logslope_strictConvex` and `T2e_nuMono_injective`. P2 instance of convexity (`nuP2_logslope_strictConvex`) is OPTIONAL (T2a already proves P2 directly).

### 1.4 The unified Fisher structure (derived here; used by the numeric companion)
For ANY kernel with `psi(y) = y nu(y)` and log-slope `eta(y) = d log psi / d log y`: `log g_obs = t + L(s - t + log g)` so `d/ds = eta(y)`, `d/dt = 1 - eta(y)`. With `b := 1 - eta`: row `J_i = (1 - b_i, b_i)`.
* P2: `b(y) = 1/(2(1 + y))` (b: 1/2 deep -> 0 Newtonian; ~1/(2y) at large y, 1/2 - y/2 at small y).
* nu_mono: with s = sqrt(y), `b(y) = s/(2(e^s - 1))` (sympy-verified: L'(u) = 1 - s/(2(e^s - 1)), s = e^{u/2}); b = 1/2 - s/4 + ... at small y, ~ (s/2) e^{-s} at large y.
Deep: b = 1/2 (rows (1/2, 1/2): only f a0 measured). Newtonian: b = 0 (rows (1, 0): only f measured). Fisher (parameters theta = (log10 f, log10 a0), data log10 g_obs, i.i.d. Gaussian error sigma dex): `F = sigma^-2 [[sum A_i^2, sum A_i B_i],[sum A_i B_i, sum B_i^2]]`, A = 1 - b, B = b. With D := (1/2) sum_{i,j} (b_i - b_j)^2 = N sum (b_i - bbar)^2:
`det F = D/sigma^4`; `Cov = F^-1`: `var(log a0) = sigma^2 sum A^2 / D`, `var(log f) = sigma^2 sum B^2 / D`, `cov = -sigma^2 sum A B / D`, `rho = -sum AB / sqrt(sum A^2 sum B^2) < 0`. Conditional (other parameter known): `sigma(log a0 | f) = sigma / sqrt(sum B^2)`, `sigma(log f | a0) = sigma/sqrt(sum A^2)`. With a Gaussian prior sigma_f on log f (tau): `var'(log a0) = sigma^2 (sum A^2 + sigma^2/tau^2)/(D + (sigma^2/tau^2) sum B^2)`. (Hand derivation; the script re-derives it with sympy, section 3.)
**T4 (design bound, new).** For b_i in [0, 1/2] (true for P2 and nu_mono for all y > 0): `9 sum_{ij}(b_i - b_j)^2 <= 2 N sum (1 - b_i)^2` (`T4_design_bound`), i.e. `var(log a0) >= 9 sigma^2/N`, i.e. **sigma(log a0) >= 3 sigma/sqrt(N) for EVERY sample of N points with f free**, equality iff all b_i in {0, 1/2} with 2/3 of the points at b = 1/2 (deep) and 1/3 at b = 0 (Newtonian). Hand proof: with B = sum b, Q = sum b^2 <= B/2: `N^2 - 2NB + 9B^2 - 8NQ >= (N - 3B)^2 >= 0`. (A scratch Lean proof of T4 and T2c_fisher_det compiled with only "no goals" lint errors, section 1.6.) Consequence: to reach sigma(log a0) < 0.1 dex at sigma = 0.1 dex needs N > 9; at sigma = 0.2, N > 36; at 0.05, N > 2.25. No y-range helps below this floor.

### 1.5 T3 (optional in the brief, included: cheap)
For any kernel with nu(y) -> 1 as y -> infinity: `g_obs/g -> f` as g -> infinity (`T3_newton_limit`), and the dependence on a0 disappears: `g_obs(f, a0)/g_obs(f, a0') -> 1` (`T3_newton_limit_a0`). Instances: `nuP2_tendsto_one`, `nuMono_tendsto_one`. So the Newtonian end measures f alone, the deep end measures f*a0, the pair identifies both (T2a), and the information is bounded by T4.

### 1.6 The Lean statements (scratch typecheck PASS, phase 1 only; `sorry` is phase-1 scaffolding)
Scratch file: `CalibrationWall_stmts.lean` (kept in the scratch dir; the final module in phase 2 is `ChainCert/CalibrationWall.lean`, namespace `CalibrationWall`, imports `Mathlib`, `ChainCert.Certificates`, `ChainCert.Kernel`). Typecheck command: `cd fable_independent_2026/lean_2026 && lake env lean <scratch>/CalibrationWall_stmts.lean`. Result: **0 errors; 36 `declaration uses sorry` warnings (one per theorem); 36 theorems.** De-risking proofs run in scratch (NOT the deliverable): `P2_sq` and `T2a_P2_injective` compile with no errors; `T4_design_bound` and `T2c_fisher_det` compile (the only messages are two "No goals to be solved" lines from a redundant trailing `ring`); the Mathlib names `StrictConvexOn.secant_strict_mono`, `StrictConvexOn.slope_strict_mono_adjacent`, `StrictMonoOn.strictConvexOn_of_deriv`, `strictConvexOn_exp`, `Real.exp_half` all exist in this Mathlib. sympy residuals (script `sympy_check.py`, not committed): d/ds and d/dt of log g_obs vs the closed forms 0, det identities 0, equal-product ratio `(1 + rho^2 y)/(1 + y)` residual 0, nu_mono L' residual 0.

```lean
import Mathlib
import ChainCert.Certificates
import ChainCert.Kernel

open Filter Topology

namespace CalibrationWall

/-- the P2 kernel (the record's kernel; = nuBeta 1 for y > 0) -/
noncomputable def nuP2 (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)
/-- the deep-MOND kernel nu y = 1/sqrt y -/
noncomputable def nuDeep (y : ℝ) : ℝ := 1 / Real.sqrt y
/-- observed acceleration when g_bar is mis-calibrated by f: g_obs = (f g) nu(f g / a0) -/
noncomputable def gObs (ν : ℝ → ℝ) (f a0 g : ℝ) : ℝ := (f * g) * ν (f * g / a0)
/-- y at the TRUE (f, a0): the argument actually fed to nu -/
noncomputable def yOf (s t g : ℝ) : ℝ := Real.exp s * g / Real.exp t

theorem nuP2_eq_nuBeta {y : ℝ} (hy : 0 < y) : nuP2 y = nuBeta 1 y := by sorry

/-! T1 -/
theorem T1_deep_law {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    gObs nuDeep f a0 g = Real.sqrt (f * a0 * g) := by sorry
theorem T1_deep_equal_products {f a0 f' a0' g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg : 0 < g) (hp : f * a0 = f' * a0') :
    gObs nuDeep f a0 g = gObs nuDeep f' a0' g := by sorry
theorem T1_deep_iff {f a0 f' a0' : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f') (ha' : 0 < a0') :
    (∀ g : ℝ, 0 < g → gObs nuDeep f a0 g = gObs nuDeep f' a0' g) ↔ f * a0 = f' * a0' := by sorry
theorem T1_deep_drift {f a0 c g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hc : 0 < c) (hg : 0 < g) :
    gObs nuDeep (c * f) a0 g = Real.sqrt c * gObs nuDeep f a0 g ∧
    gObs nuDeep f (c * a0) g = Real.sqrt c * gObs nuDeep f a0 g ∧
    Real.log (gObs nuDeep (c * f) a0 g) = Real.log (gObs nuDeep f a0 g) + Real.log c / 2 ∧
    Real.log (gObs nuDeep f (c * a0) g) = Real.log (gObs nuDeep f a0 g) + Real.log c / 2 := by sorry

/-- (ii) P2 exact -/
theorem P2_sq {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    gObs nuP2 f a0 g ^ 2 = f ^ 2 * g ^ 2 + (f * a0) * g := by sorry
theorem P2_sq_y {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    gObs nuP2 f a0 g ^ 2 = (f * a0) * g * (1 + f * g / a0) := by sorry
theorem T1_P2_ratio {f a0 f' a0' g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg : 0 < g) (hp : f * a0 = f' * a0') :
    gObs nuP2 f' a0' g ^ 2 * (f ^ 2 * g + f * a0) = gObs nuP2 f a0 g ^ 2 * (f' ^ 2 * g + f * a0) := by sorry
theorem T1_P2_bound {f a0 f' a0' g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg : 0 < g) (hp : f * a0 = f' * a0') :
    |gObs nuP2 f' a0' g ^ 2 - gObs nuP2 f a0 g ^ 2| * (f * a0) ≤
      |f' ^ 2 - f ^ 2| * g * gObs nuP2 f a0 g ^ 2 := by sorry
theorem T1_P2_limit {f a0 f' a0' : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hp : f * a0 = f' * a0') :
    Tendsto (fun g : ℝ => gObs nuP2 f' a0' g / gObs nuP2 f a0 g) (𝓝[>] 0) (𝓝 1) := by sorry

/-! T2a -/
theorem T2a_inversion {f a0 g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg1 : 0 < g1) (hg2 : 0 < g2) :
    gObs nuP2 f a0 g1 ^ 2 / g1 - gObs nuP2 f a0 g2 ^ 2 / g2 = f ^ 2 * (g1 - g2) := by sorry
theorem T2a_P2_injective {f a0 f' a0' g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg1 : 0 < g1) (hg2 : 0 < g2) (hne : g1 ≠ g2)
    (h1 : gObs nuP2 f a0 g1 = gObs nuP2 f' a0' g1) (h2 : gObs nuP2 f a0 g2 = gObs nuP2 f' a0' g2) :
    f = f' ∧ a0 = a0' := by sorry
theorem T2a_one_point_fails {f a0 g : ℝ} (hf : 0 < f) (ha : 0 < a0) (hg : 0 < g) :
    ∃ f' a0' : ℝ, 0 < f' ∧ 0 < a0' ∧ f' ≠ f ∧ gObs nuP2 f' a0' g = gObs nuP2 f a0 g := by sorry

/-! T2b -/
theorem T2b_deep_not_injective :
    ∃ f a0 f' a0' : ℝ, 0 < f ∧ 0 < a0 ∧ 0 < f' ∧ 0 < a0' ∧ f ≠ f' ∧
      ∀ g : ℝ, 0 < g → gObs nuDeep f a0 g = gObs nuDeep f' a0' g := by sorry

/-! T2c -/
noncomputable def dlogf (y : ℝ) : ℝ := (1 + 2 * y) / (2 * (1 + y))
noncomputable def dloga (y : ℝ) : ℝ := 1 / (2 * (1 + y))
theorem T2c_dlogf (s t g : ℝ) (hg : 0 < g) :
    HasDerivAt (fun s' : ℝ => Real.log (gObs nuP2 (Real.exp s') (Real.exp t) g))
      (dlogf (yOf s t g)) s := by sorry
theorem T2c_dloga (s t g : ℝ) (hg : 0 < g) :
    HasDerivAt (fun t' : ℝ => Real.log (gObs nuP2 (Real.exp s) (Real.exp t') g))
      (dloga (yOf s t g)) t := by sorry
theorem T2c_rows {y : ℝ} (hy : 0 < y) : dlogf y = 1 - dloga y := by sorry
theorem T2c_det {y1 y2 : ℝ} (h1 : 0 < y1) (h2 : 0 < y2) :
    dlogf y1 * dloga y2 - dloga y1 * dlogf y2 = (y1 - y2) / (2 * (1 + y1) * (1 + y2)) ∧
    dlogf y1 * dloga y2 - dloga y1 * dlogf y2 = (1 / (1 + y2) - 1 / (1 + y1)) / 2 := by sorry
theorem T2c_det_ne_zero_iff {y1 y2 : ℝ} (h1 : 0 < y1) (h2 : 0 < y2) :
    dlogf y1 * dloga y2 - dloga y1 * dlogf y2 ≠ 0 ↔ y1 ≠ y2 := by sorry
theorem T2c_det_bounds {y1 y2 : ℝ} (h1 : 0 < y1) (h2 : 0 < y2) :
    |dlogf y1 * dloga y2 - dloga y1 * dlogf y2| ≤ |y1 - y2| / 2 ∧
    |dlogf y1 * dloga y2 - dloga y1 * dlogf y2| ≤ 1 / (2 * (1 + min y1 y2)) ∧
    |dlogf y1 * dloga y2 - dloga y1 * dlogf y2| < 1 / 2 := by sorry
theorem T2c_yratio {s t g1 g2 : ℝ} (hg2 : 0 < g2) : yOf s t g1 / yOf s t g2 = g1 / g2 := by sorry
/-- Fisher determinant identity -/
theorem T2c_fisher_det {n : ℕ} (b : Fin n → ℝ) :
    (∑ i, (1 - b i) ^ 2) * (∑ i, b i ^ 2) - (∑ i, (1 - b i) * b i) ^ 2
      = (1 / 2) * ∑ i, ∑ j, (b i - b j) ^ 2 := by sorry
theorem T2c_fisher_singular_iff {n : ℕ} (b : Fin n → ℝ) :
    (∑ i, (1 - b i) ^ 2) * (∑ i, b i ^ 2) - (∑ i, (1 - b i) * b i) ^ 2 = 0 ↔ ∀ i j, b i = b j := by sorry

/-! T3 -/
theorem T3_newton_limit (ν : ℝ → ℝ) (hν : Tendsto ν atTop (𝓝 1)) {f a0 : ℝ} (hf : 0 < f) (ha : 0 < a0) :
    Tendsto (fun g : ℝ => gObs ν f a0 g / g) atTop (𝓝 f) := by sorry
theorem T3_newton_limit_a0 (ν : ℝ → ℝ) (hν : Tendsto ν atTop (𝓝 1)) {f a0 a0' : ℝ} (hf : 0 < f)
    (ha : 0 < a0) (ha' : 0 < a0') :
    Tendsto (fun g : ℝ => gObs ν f a0 g / gObs ν f a0' g) atTop (𝓝 1) := by sorry
theorem nuP2_tendsto_one : Tendsto nuP2 atTop (𝓝 1) := by sorry
theorem nuMono_tendsto_one : Tendsto nuMono atTop (𝓝 1) := by sorry

/-! T1 general kernel: the deep-limit premise of C2 gives the product-only dependence asymptotically -/
theorem T1_general_limit (ν : ℝ → ℝ) (hν : Tendsto (fun y : ℝ => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1))
    {f a0 : ℝ} (hf : 0 < f) (ha : 0 < a0) :
    Tendsto (fun g : ℝ => gObs ν f a0 g / Real.sqrt (f * a0 * g)) (𝓝[>] 0) (𝓝 1) := by sorry
theorem T1_general_equal_products_limit (ν : ℝ → ℝ)
    (hν : Tendsto (fun y : ℝ => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1))
    {f a0 f' a0' : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f') (ha' : 0 < a0') (hp : f * a0 = f' * a0') :
    Tendsto (fun g : ℝ => gObs ν f' a0' g / gObs ν f a0 g) (𝓝[>] 0) (𝓝 1) := by sorry

/-! kernel-general Jacobian: rows (1 - b, b) -/
theorem T2c_det_general (b1 b2 : ℝ) : (1 - b1) * b2 - b1 * (1 - b2) = b2 - b1 := by sorry
/-- T4: design bound; any N points with b_i in [0, 1/2]: C22 >= 9 sigma^2 / N -/
theorem T4_design_bound {n : ℕ} (b : Fin n → ℝ) (h0 : ∀ i, 0 ≤ b i) (h1 : ∀ i, b i ≤ 1 / 2) :
    9 * ∑ i, ∑ j, (b i - b j) ^ 2 ≤ 2 * n * ∑ i, (1 - b i) ^ 2 := by sorry

/-! T2e: general two-point injectivity from strict convexity of L(u) = log(e^u nu(e^u)) -/
theorem T2e_injective_of_strictConvex (ν : ℝ → ℝ) (hν : ∀ y : ℝ, 0 < y → 0 < ν y)
    (hL : StrictConvexOn ℝ Set.univ (fun u : ℝ => Real.log (Real.exp u * ν (Real.exp u))))
    {f a0 f' a0' g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f') (ha' : 0 < a0')
    (hg1 : 0 < g1) (hg2 : 0 < g2) (hne : g1 ≠ g2)
    (h1 : gObs ν f a0 g1 = gObs ν f' a0' g1) (h2 : gObs ν f a0 g2 = gObs ν f' a0' g2) :
    f = f' ∧ a0 = a0' := by sorry
theorem nuMono_pos {y : ℝ} (hy : 0 < y) : 0 < nuMono y := by sorry
theorem nuMono_logslope_strictConvex :
    StrictConvexOn ℝ Set.univ (fun u : ℝ => Real.log (Real.exp u * nuMono (Real.exp u))) := by sorry
theorem T2e_nuMono_injective {f a0 f' a0' g1 g2 : ℝ} (hf : 0 < f) (ha : 0 < a0) (hf' : 0 < f')
    (ha' : 0 < a0') (hg1 : 0 < g1) (hg2 : 0 < g2) (hne : g1 ≠ g2)
    (h1 : gObs nuMono f a0 g1 = gObs nuMono f' a0' g1) (h2 : gObs nuMono f a0 g2 = gObs nuMono f' a0' g2) :
    f = f' ∧ a0 = a0' := by sorry
theorem nuP2_logslope_strictConvex :
    StrictConvexOn ℝ Set.univ (fun u : ℝ => Real.log (Real.exp u * nuP2 (Real.exp u))) := by sorry

end CalibrationWall
```

**Mathlib facts expected (phase 2):** `Real.sq_sqrt`, `Real.sqrt_eq_iff`/`Real.sqrt_sq`, `Real.sqrt_mul`, `Real.log_mul`, `Real.log_sqrt`, `Real.sqrt_inj`/`Real.sqrt_lt_sqrt`, `Real.exp_log`, `Real.add_one_lt_exp`/`Real.one_sub_lt_exp_neg` (for the nu_mono step), `Real.exp_half`, `Tendsto.comp` with `tendsto_nhdsWithin_iff` (as in `Kernel.nuMono_deep`), `Filter.Tendsto.div`, `HasDerivAt.log`, `HasDerivAt.exp`, `HasDerivAt.sqrt` (or rewrite `log g_obs = (s + log g + log(e^s g + e^t))/2` by `funext` and differentiate), `Finset.sum_comm`, `Finset.sum_sub_distrib`, `Finset.sum_div`, `StrictConvexOn.secant_strict_mono`, `StrictMonoOn.strictConvexOn_of_deriv`, `strictConvexOn_exp`.

### 1.7 Premises: decided vs declared
| item | status | note |
|---|---|---|
| positivity of f, f', a0, a0', g, g1, g2 | **decided (hypotheses of each theorem)** | f > 0 is needed: it makes f g > 0 and f^2 = f'^2 pin f; a0 > 0 for P2_sq |
| g1 != g2 | **decided (hypothesis of T2a, T2e)** | needed; with g1 = g2 T2a' says injectivity fails |
| the law `g_obs = (f g) nu((f g)/a0)`: f multiplies g_bar only, one f and one a0 for all points | **declared** | a pure multiplicative calibration; offsets, g-dependent f, per-point scatter in f are outside |
| kernel = P2 (record's) / nu_mono (Kernel.lean) / nuDeep | **declared** | not a claim about nature; T1e extends T1 to any kernel with C2's deep premise |
| T2e premise: L strictly convex | **declared in T2e; a theorem for P2 (via T2a) and, in the stretch, for nu_mono** | |
| T4: b_i in [0, 1/2] | **decided for P2 and nu_mono (b = 1 - eta, eta in [1/2, 1])** for the numeric statement; Lean takes it as hypothesis | |
| statistical model (i.i.d. Gaussian log10 errors sigma, flat y-design) | **declared, numeric only** | |

## 2. nu_mono
**Attempt (phase 2, in this order):** (i) `nuMono_pos` (1 - exp(-sqrt y) > 0 for y > 0). (ii) `nuMono_logslope_strictConvex`: rewrite `L(u) = u - log(1 - exp(-exp(u/2)))` using `Real.exp_half` and `Real.sqrt_exp`-type rewriting (`sqrt(e^u) = e^(u/2)`); `HasDerivAt` gives `L'(u) = 1 - (s/2)/(e^s - 1)`, s = e^{u/2} (sympy-verified); strict monotonicity of `s -> s/(e^s - 1)` on (0, inf) via `s (e^{s'} - 1) > s' (e^s - 1)` for s < s', which is the strict secant-slope monotonicity of exp at 0 (`strictConvexOn_exp.secant_strict_mono`); then `StrictMonoOn.strictConvexOn_of_deriv`. (iii) `T2e_nuMono_injective` is T2e applied to (i), (ii). (iv) the numeric check that eta = 1 - b is strictly increasing from 1/2 to 1 (done in the numeric script as a sanity line, NOT a proof).
**What counts as "not formalisable cleanly" (frozen):** the nu_mono convexity step exceeds about 120 lines, or needs anything other than the three standard axioms (no `native_decide`, no numerical interval arithmetic standing in for a proof, no extra `axiom`), or I cannot close it without a `sorry` after a bounded effort. Then: ship T2e (kernel-general, conditional on the convexity premise) and the numeric nu_mono Fisher/degeneracy results, drop `nuMono_logslope_strictConvex` and `T2e_nuMono_injective` from the module, and say in the README, in these words, that "nu_mono injectivity is conditional on the strict convexity of log(e^u nu(e^u)), which is not proved; the local Jacobian det = b(y2) - b(y1) is non-zero wherever b is strictly monotone". Do not force it.
**Answer to the brief:** injectivity for nu_mono holds in the same exact sense as for P2 IF eta is strictly monotone; it is not a regime-only statement, and it is NOT trivially algebraic as P2's is (nu_mono has no polynomial g_obs^2). The honest odds that phase 2 closes it cleanly: about 0.7 (estimate).
**Counts:** core target 33 theorems (items 1-33 of the statement list: everything except `nuMono_logslope_strictConvex`, `T2e_nuMono_injective`, `nuP2_logslope_strictConvex`); with nu_mono 35; with the optional P2 convexity 36.

## 3. Numeric companion spec (to be implemented in phase 2; NOT written now)
**Directory/files:** `campaign_fresh_gravity/CFG240_calibration_wall/`: `cfg240_fisher.py` (single script, standard library + numpy + sympy; deterministic, no RNG except the seeded design-bound sweep, seed 240), `cfg240_fisher.out`, `cfg240_fisher_results.json`, `cfg240_fisher_MUTATE<k>.out` / `_MUTATE<k>_results.json` (k = 1..6; mutation runs write separate outputs), `README.md`. The script prints repo-relative names only (no absolute home path; derive names from `Path(__file__).name`).
**Definitions.** Parameters theta = (log10 f, log10 a0); data d_i = log10 g_obs(g_i), i = 1..N, independent Gaussian errors sigma dex (same for all i). `g_obs = (f g) nu((f g)/a0)`. Fiducial (f0, a0) with a0 = 1 (units drop out), f0 = 1 for the grid and f0 in {0.5, 1.7} for the y-definition check. **y is y_true = f0 g/a0** (the argument of nu), sampled log-uniform with ENDPOINTS INCLUDED: `y_i = y_min (y_max/y_min)^((i-1)/(N-1))`, i = 1..N (N >= 2; deterministic). g_i = y_i a0/f0. Reported alongside: y_nom = g/a0 = y/f0. Why y_true: the Fisher matrix is a function of y_true alone (section 1.4); y_nom changes the regime label by the unknown f.
**Grid.** kernels {P2, nu_mono}; y_min in {1e-3, 1e-2, 1e-1}; y_max on the geometric grid y_min 10^(k/50), k = 1..(50 log10(1e4/y_min)); N in {5, 10, 20, 50, 100}; sigma in {0.05, 0.1, 0.2} dex; prior tau (sigma of log10 f) in {none, 0.15, 0.3}.
**Outputs per cell:** the 2x2 F; rho = corr(log f, log a0) of the estimates, computed as -F12/sqrt(F11 F22) (equal to the F^-1 correlation whenever F is invertible, and defined also at the singular single-y design); sigma_marg(log a0) = sqrt((F^-1)_22); sigma_cond(log a0 | f) = 1/sqrt(F_22); sigma_marg(log f); the condition number of F (ratio of eigenvalues, raw) and of the correlation-normalised F; det F; with prior: sigma'(log a0). **Break-even table:** for each (kernel, y_min, N, sigma, tau) and target 0.1 dex (also 0.2): `ymax_first` = smallest grid y_max with sigma_marg(log a0) < target; `ymax_stable` = smallest y_max such that it holds for ALL larger grid y_max up to 1e4; `sigma_min`, `ymax_argmin` (sigma_marg is NOT monotone in y_max: past the optimum extra Newtonian points hurt); `NONE` if the target is never reached on the grid. The paper line is "a sample must reach y >~ ymax_stable to break the degeneracy at 0.1 dex", quoted with the cell. Also the two-point table det = b(y2) - b(y1) on a (y1, y2) grid, and the T4 floor 3 sigma/sqrt(N) next to each sigma_min.
**Closed-form Fisher entries (to be recorded twice: by hand, by sympy).** By hand (section 1.4): with A = 1 - b, B = b, P2 b = 1/(2(1+y)); nu_mono b = sqrt(y)/(2(exp(sqrt y) - 1)); F11 = sum A^2/sigma^2, F12 = sum AB/sigma^2, F22 = sum B^2/sigma^2 (in log10 parameters and log10 data). By sympy: differentiate `log g_obs(s, t, g)` symbolically from the DEFINITION `gObs` (not from the closed form) for each kernel, substitute y, and simplify the difference to 0; also verify `det = b(y2) - b(y1)`, `var(log a0) = sigma^2 sum A^2 / D`, and the prior formula by symbolic 2x2 inversion. Both are printed.
**Pass lines (main run exit 0 iff all hold):**
- PL1: analytic J (closed forms) Fisher equals a finite-difference Fisher of the DEFINITION gObs (4-point central stencil, step 1e-3 in log10, parameters (log10 f, log10 a0)) to 1e-8 relative on every F entry, for both kernels, at f0 in {0.5, 1, 1.7}, on 12 sample designs.
- PL2: closed form equals sympy at 20 test y per kernel to 1e-12 relative (dlogf, dloga, det, marginal sigma, prior formula).
- PL3: T1 reproduced: for nuDeep, pairs (1, 1), (2, 0.5), (0.25, 4) give g_obs equal to 1e-14 relative at 30 g values; for P2, the equal-product relative difference of g_obs^2 equals `(rho^2 - 1) y/(1 + y)` to 1e-12 and decays linearly: log-log slope in y over [1e-6, 1e-3] is 1 within 0.01; for nu_mono the equal-product relative difference in g_obs tends to 0 as y -> 0 (its value at y = 1e-6 is below 0.05 of its value at y = 1e-2 for rho = 2; the expected ratio is ~ 1e-2 because nu_mono's deep correction is O(sqrt y)) [this is T1e].
- PL4: sign and limit of rho: rho < 0 in EVERY cell; rho -> -1 as the sample collapses to one y (y_max = y_min gives |rho| = 1 to 1e-12 when F is singular; for y_max = 1.0001 y_min, rho < -0.999 in the deep corner y_min = 1e-3, P2, nu_mono). **Sign: NEGATIVE.** Reason: both log f and log a0 raise log g_obs (J has positive entries), so the nearly degenerate direction is (d log f, d log a0) = (+delta, -delta) (deep: f a0 fixed); estimates of log f and log a0 are therefore anti-correlated. At fixed y the rank is 1 for any kernel and rho = -1 exactly.
- PL5: design bound: for 20000 seeded random designs (b_i drawn uniform in [0, 1/2] and y-draws log-uniform, N in 2..200, both kernels) sigma_marg(log a0) >= 3 sigma/sqrt(N) (1 - 1e-12); equality (to 1e-12) at the two-cluster design 2N/3 points at b = 1/2 and N/3 at b = 0 (N a multiple of 3).
- PL6: det identity: two-point numeric det equals b(y2) - b(y1) to 1e-14 and |det| < 1/2 over a 200x200 y grid; for P2 additionally equals (y1 - y2)/(2(1+y1)(1+y2)).
- PL7: scalings: sigma_marg(log a0) is exactly linear in sigma (ratio 2 when sigma doubles to 1e-12) and a replicated design (each y_i repeated k times) scales as 1/sqrt(k) to 1e-12.
- PL8: nu_mono sanity: eta = 1 - b strictly increasing on a 4000-point grid of log y in [-20, 3.5] (grid check; a numerical line, not the proof). Also T3: b -> 0 at y = 1e4 (P2: 5e-5; nu_mono < 1e-30).
- PL9: the break-even logic: `ymax_first <= ymax_stable`; at the reported ymax_first sigma_marg < target and at the grid point just below it >= target; N = 5, sigma = 0.1 returns NONE (its floor 0.134 > 0.1) for every y_min and both kernels; sigma = 0.2, N = 20 returns NONE (floor 0.134).

## 4. MUTATE controls (frozen)
**Numeric convention:** main run exits 0 iff all pass lines hold; `MUTATE=k python3 cfg240_fisher.py` runs ONE mutated computation and exits 1 iff the pass lines detect it ("CONTROL BITES"), exits 0 (and prints "CONTROL DID NOT BITE") otherwise, each writing its own `_MUTATE<k>` outputs.
- M1 wrong kernel in the analytic J (nuDeep's b = 1/2 used for the P2 rows): PL1 and PL2 must fail.
- M2 sigma-scaling: F built without the 1/sigma^2: PL7 must fail (and the break-even table moves).
- M3 y definition swapped: sample y_nom = g/a0 as if it were the argument of nu at f0 = 1.7 (closed-form J evaluated at y_nom): PL1 must fail for f0 != 1.
- M4 sign flip of the F12 term in rho: PL4 (sign) must fail.
- M5 break-even computed from sigma_cond instead of sigma_marg: PL9's NONE assertions (N = 5, sigma = 0.1; N = 20, sigma = 0.2) must fail because the conditional sigma is below the T4 floor.
- M6 design-bound constant 3 replaced by 3.1 in PL5: the two-cluster equality case must fail.
**Lean convention:** `ChainCert/CalibrationWallMutate.lean.txt` holds one FALSE variant per theorem, each "proved" by the ORIGINAL proof term; the verifier copies it to `ChainCert/CalibrationWallMutate.lean`, compiles it with `lake env lean`, expects exactly one error per variant (message `Type mismatch` or an unknown/ill-typed hypothesis), and removes the copy; `CalibrationWallMutate.out` records the output (as `DimensionMutate.out`). Frozen variants (each must be rejected):
1. `T1_deep_law` with `sqrt(f*g)` in place of `sqrt(f*a0*g)`.
2. `T1_deep_equal_products` with the WRONG equal-products hypothesis `f / a0 = f' / a0'` (and variant `f + a0 = f' + a0'`).
3. `T1_deep_iff` with conclusion `f = f' /\ a0 = a0'` (the injectivity claim in the deep regime).
4. `T1_deep_drift`: `Real.log c / 2` replaced by `Real.log c`.
5. `P2_sq`: the cross term `(f*a0)*g` replaced by `(f*a0)*g^2`.
6. `T1_P2_ratio`: `f'^2*g + f*a0` replaced by `f^2*g + f*a0` (i.e. claiming exact equality for unequal-f pairs).
7. `T1_P2_bound`: `|f'^2 - f^2|` replaced by `|f' - f|`.
8. `T1_P2_limit`: limit 1 replaced by 2.
9. `T2a_P2_injective` with `nuP2` replaced by `nuDeep` (the injectivity claim for the deep kernel; it must FAIL, and T2b is its refutation).
10. `T2a_P2_injective` with the hypothesis `g1 != g2` DROPPED (proof term applied to a missing `hne`).
11. `T2a_P2_injective` with `f > 0` DROPPED for f' (hypothesis missing).
12. `T2a_P2_injective` with only ONE point (h2 dropped).
13. `T2a_one_point_fails` reversed into the injectivity-at-one-point claim: `forall f' a0' > 0, gObs nuP2 f' a0' g = gObs nuP2 f a0 g -> f' = f` (must be rejected: the original proof term proves the opposite).
14. `T2a_inversion`: RHS `f^2 * (g1 - g2)` replaced by `f * (g1 - g2)`.
15. `T2b_deep_not_injective` negated (injectivity asserted for nuDeep).
16. `T2c_det`: `(y1 - y2)` replaced by `(y1 + y2)`.
17. `T2c_det_general`: `b2 - b1` replaced by `b1 - b2`.
18. `T2c_det_bounds`: `< 1/2` replaced by `< 1/4`.
19. `T2c_dlogf` with the derivative `dloga` (swapped partials).
20. `T2c_fisher_det`: the factor `1/2` replaced by `1`.
21. `T3_newton_limit`: limit `f` replaced by `a0`.
22. `T4_design_bound`: constant `9` replaced by `10` (false: the equality design attains 9).
23. `T2e_injective_of_strictConvex` with `StrictConvexOn` replaced by `ConvexOn` (non-strict: injectivity claim is false for a linear L; Lean must reject the original proof term).
24. `T1_general_limit` with the hypothesis `nu y * sqrt y -> 1` replaced by `nu y -> 1` (wrong deep premise).
Expected: 24+ errors, exactly one per variant (variants 2 and others with two spellings count by spelling). Phase 2 records the actual count in README.

## 5. Build / verify checklist (phase 2)
1. Registration: the lib `ChainCert` has default roots, so a new module is built only if reachable from `fable_independent_2026/lean_2026/ChainCert.lean`: add `import ChainCert.CalibrationWall` there; add `import ChainCert.CalibrationWall` and one `#print axioms CalibrationWall.<name>` per theorem at the end of `ChainCert/Axioms.lean` (verify_chain.sh counts `#print axioms` lines against results); `Chain.lean` is a content module, NOT an index, and is not edited. README: append a section (no edits to existing text) with the statement table, the "NOT certified" list and the nu_mono outcome.
2. `lake build ChainCert` succeeds (before: "Build completed successfully (8782 jobs)").
3. `ChainCert/verify_chain.sh`: before = **281** theorems (current `Axioms.lean` has 281 `#print axioms` lines; `verify_chain.out`: PASS, 0 non-standard, 0 sorry mentions). After = 281 + 33 = **314** (core), 316 with nu_mono, 317 with the optional P2 convexity; the phase-2 report states which. 0 non-standard axiom lists (each must be exactly `[propext, Classical.choice, Quot.sound]`), 0 `sorry` anywhere (`grep -n sorry ChainCert/CalibrationWall.lean` empty; the module has no `axiom`, no `native_decide`).
4. `MUTATE=1 ChainCert/verify_chain.sh` still fails (exit 1) as before ("theorems checked: 2; with non-standard axioms: 1; sorry mentions: 2").
5. `CalibrationWallMutate.lean.txt` compiled as in section 4: every variant errors; output saved as `CalibrationWallMutate.out`; no variant compiles.
6. No edits to other sessions' modules beyond the import list, `Axioms.lean`, and the README append; `git status` shows only the new/edited files named in section 6; commit after build AND verify pass.

## 6. File plan
Lean (in `fable_independent_2026/lean_2026/`): `ChainCert/CalibrationWall.lean`, `ChainCert/CalibrationWallMutate.lean.txt`, `ChainCert/CalibrationWallMutate.out`; edits: `ChainCert.lean` (one import), `ChainCert/Axioms.lean` (import + `#print axioms` lines), `ChainCert/Axioms.out` (regenerated), `ChainCert/verify_chain.out` and `verify_chain_MUTATE.out` (regenerated), `ChainCert/README.md` (append). Campaign (in `campaign_fresh_gravity/`): `CFG240_FROZEN_CRITERIA.md` (this file), `CFG240_calibration_wall/{cfg240_fisher.py, cfg240_fisher.out, cfg240_fisher_results.json, cfg240_fisher_MUTATE1..6 outputs, README.md}`. No absolute home path in any committed file; no personal name.

## 7. Hand ESTIMATES (labelled; made BEFORE any run of the numeric script; computed with the closed forms of section 1.4 by hand and continuum approximations of the log-uniform sample, not from any table)
Setting: P2, N = 20, sigma = 0.1 dex, no prior, endpoints-inclusive log-uniform y. Formula: `sigma_a0^2 = sigma^2 mean(A^2)/(N Var(b))`.
- E1 (y_min = 0.01): sigma(log a0) ~ 0.105 dex at y_max = 10, ~ 0.097 at y_max = 30; first break-even `ymax_first` ~ 17 (80% interval 8 to 40). P(8 <= ymax_first <= 40) = 0.8; P(< 8) = 0.1; P(> 40 or NONE) = 0.1. Stable break-even within a factor 1.5 of the first (P = 0.7).
- E2 (y_min = 1e-3, more deep points): ymax_first ~ 10 (5 to 25); lower than E1's with P = 0.75.
- E3 (y_min = 0.1, no deep points): NONE; minimum sigma(log a0) ~ 0.12 to 0.13 near y_max ~ 20 and rising again (~ 0.14) at y_max = 1e3. P(NONE) = 0.75; P(sigma_min < 0.1) = 0.15.
- E4 (T4 floor, proved): 3 sigma/sqrt(N) = 0.067 dex at (20, 0.1). N = 5 and N = 10 at sigma = 0.1: NONE for the log-uniform design (floors 0.134 and 0.095; P(NONE at N = 10) = 0.97, P(NONE at N = 5) = 0.99); N = 20 at sigma = 0.2: NONE with certainty (floor 0.134). N = 100, sigma = 0.1: ymax_first ~ 1 (0.3 to 3). N = 20, sigma = 0.05: ~ 1 (0.5 to 3).
- E5 (rho): ~ -0.8 at y_max = 10 and ~ -0.7 at y_max = 30 (y_min = 0.01): the correlation is still strong at break-even; sigma_marg < 0.1 does not require |rho| small. Deep corner (y_max <= 0.1): rho < -0.99 (P = 0.95).
- E6 (conditioning at break-even): cond(F) ~ 15 (10 to 25) at (y_max = 10, y_min = 0.01, N = 20, sigma = 0.1); > 1e3 for y_max <= 0.1.
- E7 (prior on log f): a deep-only sample cannot reach 0.1 dex with any prior tau >= 0.1: sigma'(log a0) ~ sqrt(tau^2 + (2 sigma/sqrt(N))^2) ~ 0.156 at tau = 0.15 (P = 0.95). tau = 0.15 lowers ymax_first by at most a factor ~1.5 (to ~ 12); tau = 0.3 by < 1.15 (P = 0.7 for both).
- E8 (nu_mono): same floor (b in [0, 1/2]); ymax_first within a factor 2 of P2's (P = 0.65); direction not estimated (nu_mono's b is lower at y ~ 0.01 (0.475 against 0.495) but higher at y ~ 10 (0.07 against 0.045)).
- E9 (Lean): P(core 33 theorems proved with standard axioms) = 0.85; P(nu_mono convexity closed cleanly) = 0.7; P(`T2c_dlogf`/`T2c_dloga` need a rewrite of log g_obs as a sum before differentiating) = 0.8.
These are to be compared with the run, and misses reported as misses.

## 8. What is NOT covered
- Non-P2, non-nu_mono kernels except through T1e (deep premise), T2e (convexity premise) and T3 (Newtonian limit premise); the rate in T1 is stated only for P2.
- Other systematics: a stellar-mass-to-light or gas calibration that is not a single multiplicative f on g_bar; offsets; g-dependent calibration (f varying with g_bar or with the galaxy: this breaks the "same f" premise and can restore or destroy identifiability); per-galaxy scatter in f (an error-in-variables effect on g_bar not in the Fisher model); selection effects and Malmquist-type bias; the external-field effect; non-circular motion; correlated errors among points (the Fisher matrix assumes independent Gaussian errors); non-Gaussian errors.
- Redshift evolution: a0 constant per sample is assumed; the lane says what a single-epoch sample can identify, not how to separate drifts (T1c shows a drift in log f mimics one in log a0 in the deep regime, and that is all).
- Real data: no real sample's y distribution is used; the table is a design statement ("a sample must reach y >~ X"), not an assertion that any existing survey does or does not.
- That the wall binds the framework more than its rival: it binds any law with a deep limit of the same form (T1e).
- kappa = 1/2 is FITTED and is not touched.
