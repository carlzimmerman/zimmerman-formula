# RH11 -- THE ZERO-FREE REGION ROUTE: THE 3-4-1 TRICK WITH THE FRAMEWORK'S KERNEL
(deepseek lane; subagent RH11, 2026-09-17. Files: RH11_kerZeroFree.py / .out /
_results.json; lean/RH11L_ker34one.lean; this summary.)

## THE ENTRY (never tried before this lane)
The classical 3-4-1 (Hadamard / de la Vallée Poussin 1899) proves
ζ has no zeros in σ > 1 − c/(log|t|) from
    k(θ) = 3 + 4cosθ + cos2θ = 2(1+cosθ)² ≥ 0   (sum of squares) + Euler product.
The Euler-product identity is LINEAR in the weights, so it holds for any
(A,B,C):  A·log|ζ(σ)| + B·log|ζ(σ+it)| + C·log|ζ(σ+2it)| = Σ_p Σ_m p^(−mσ)·k(mθ_p)/m
with k(θ) = A + Bcosθ + Ccos2θ.  THE FRAMEWORK ENTRY: take the amplitudes from
the Lomax kernel f_l(u) = (1+u)^(−l):
    A = w0·f_l(u),  B = w1·f_l(2u),  C = w2·f_l(3u)   ("w0 f(u) + w1 f(2u) + w2 f(3u)"
    with the classical trig factors attached — the only reading under which the
    Euler-product identity survives).
Nonnegativity certificate (the framework analogue of 2(1+cosθ)², Lean-certified):
    vertex regime (B ≤ 4C):  k(θ) = [A − C − B²/8C] + 2C(cosθ + B/4C)² ,  margin ≥ 0 ⇒ k ≥ 0;
    corner regime (B ≥ 4C, −1 ≤ cosθ):  k(θ) − (A−B+C) = (1+cosθ)(B − 2C + 2C·cosθ) ≥ 0.

## RESULTS (real numerics, mpmath-free numpy; grid pre-registered)
- **Scan**: l ∈ {1.5, 2, 2.4824, 3} × u ∈ [0.02, 10] (256-pt log grid ∪ 5000-pt
  rational linear grid) × w ∈ {(3,4,1), (1,2,1), (5,6,1)}; θ ∈ [0,2π] verified.
  **61,678 of 63,060 candidates pass** (k ≥ 0 for ALL θ AND leading Fourier
  coefficient B > 0).  Closed-form min vs θ-grid min: max |diff| = 2.8e-6.
- **Closest-to-0 minimum over the grid** = **4.4872e-4** at (l, u, w) = (1.5,
  0.355395, (1,2,1)) [vertex regime].
- **Scheme constant** (Stechkin-normalized): c = c_class·B/(A+C) = c_class/α
  with α = (A+C)/B, c_class = 1/9.646 ≈ 0.10367 (Stechkin's classical explicit
  dVdP constant; the task's "1/(9.6...)" family; modern explicit: Kadiri
  1/5.69693, MTY 2022 1/5.558691).
  - best (closest-to-0) candidate: α = 1.08575, **c = 0.09548** (ratio 0.921 to classical);
  - family best on grid: α = 1.01512, c = 0.10213 (ratio 0.985);
  - pipeline-sharpened c_pipe(T): between 0.855·c_class (T=100) and 0.898·c_class (T→∞-limit 0.921) at the same height.
- **Family-optimality theorem (Lean-certified, `alpha_ge_one`)**: margin ≥ 0 ∧
  C > 0 ⟹ (A+C)/B ≥ 1, with equality only at (A,B,C) ∝ (3,4,1), i.e. u → 0,
  f ≡ 1 — **the classical kernel is the unique optimum of the Lomax-modulated
  family; every framework rung (l > 0, u > 0) is strictly weaker**.  On the
  grid, min α among passing = 1.0151 (not 1: the classical point lies at the
  u = 0 boundary, outside the framework's u ≥ 0.02 domain).
- **Literal reading (Family A)**: k(θ) = Σ w_j·f_l(j·tan²(θ/2)) is ≥ 0 (trivial)
  with positive leading Fourier coefficient, but touches 0 at θ = π (f(∞)=0)
  and is NOT a trig polynomial — the Euler-product identity fails, so no scheme
  constant exists: **the 3-4-1 scheme refuses the literal substitution**.

## KILLS (pre-registered)
- **K1** (no (l,u,w) found): **UNFIRED** — 61,678 candidates pass.
- **K2** (c < c_class/10): **UNFIRED** — c_best/c_class = 0.921 ≥ 0.1.
- **Registered weaker-than-known**: c_best = 0.09548 < c_class = 0.10367 (and
  far below the modern explicit best 1/5.558691).  The framework kernel enters
  the 3-4-1 scheme but cannot improve it; the route's framework entry is a
  dead end (strictly weaker, family-optimality certified).

## LEAN CERTIFICATE (lean/RH11L_ker34one.lean — exit 0, zero warnings, ZERO sorry, 4.1 s)
1. `classical_identity_c`, `cos_double_angle`, `classical_kernel_trig`, `classical_kernel_nonneg`:
   3+4c+(2c²−1) = 2(c+1)², cos(2t) = 2cos²t−1, 3+4cos t+cos2t = 2(1+cos t)² ≥ 0.
2. `sos_decomposition` (general weights), `vertex_scheme_nonneg`,
   `corner_decomposition`, `corner_scheme_nonneg`: the nonnegativity test's
   algebra in BOTH regimes (SOS and factor certificates, symbolic (A,B,C)).
3. `alpha_ge_one`: the family-optimality algebra (margin ≥ 0 ⇒ α ≥ 1).
4. **Exact instantiation at the best integer-l candidate** (l = 3, w = (1,2,1),
   u = 10 — the framework's equilibrium rung): A = 1/1331, B = 2/9261,
   C = 1/29791, min_θ k = **208917200/367215514281 ≈ 5.6892e-4** (exact, > 0);
   `best_kernel_trig_nonneg`: for ALL t, 1/1331 + (2/9261)cos t + (1/29791)cos(2t) ≥ 0
   [independently re-verified: grid min matches the exact value to all digits].
The overall grid best (l = 1.5, min = 4.4872e-4) is not Lean-exact (non-integer
rung); it is an instance of the symbolically-certified vertex algebra.  The
certified statements are PURE ALGEBRA of the kernel test; the standard 1899
analytic pipeline (identity + lower bound ⇒ region) is not formalized.  NO RH
claim, in whole or in part.

## VERDICT
**[FAIL]** as a framework improvement: the 3-4-1 scheme accepts the framework
kernels (K1 unfired) but every framework kernel yields a STRICTLY weaker region
constant (c_best = 0.09548 < c_class = 0.10367; α ≥ 1 certified, equality only
at the classical u → 0 point); K2 unfired; registered weaker-than-known.  The
classical 3+4cosθ+cos2θ = 2(1+cosθ)² remains the optimum of the whole
Lomax-modulated family.  No RH claim; nothing committed.