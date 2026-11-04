# V3X_v3s_close_undecided: FROZEN CRITERIA (committed alone, before any script or number)

**Owner 11-04:** "Yes, close both", about V3W's two UNDECIDED items (W2 and W4c). Test lanes may reopen frozen items under
the 11-04 lift. **This lane adopts nothing.** The 10-24 v3s verdict
(`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`) stands unless the owner changes it in writing. No file under
`covariant_push_2026_10_22/` or `doors_push_2026_10_22/` is edited; their code is imported or executed read-only, with
bytecode writing off.

κ = ½ FITTED. Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. **Not blind**: V3W, C6, C6P, C5,
C8, X3 and V3_FULL_PICTURE were read first, including V3W's rung values and C5's H6/H7 numbers. Not theory closed. Nothing
here says the data favour the framework. The cold sector stays retired. CMB and clusters are out of scope and open. a0 is
put in by hand.

Lane id checked free (11-04): `ls rebuild_2026_10_22 | grep V3X` and `git log --all --oneline | grep V3X` both empty.

The action is V3W's (frozen 10-24 form, C4/C5/C6, X3 switch):

    S = (c⁴/16πG) ∫ √−g [ R − 2Λ + 2μ_K²(Q − 1)² ] + ∫ √−g [ P^i A_i − W(K|P|) − (γ_L/2)[max(D_iP^i, 0)]² ] + S_m

β = η = γ_F = 0, γ_L = K L★²/2, K = 4πG/c², W = (a0²/K)[−u/a0 − ln(1 − u/a0)], u = K|P|.

## Compute rules (all parts)
- Every job one thread (`OMP_NUM_THREADS=1` and the BLAS equivalents), nice 15, **< 1 GB RSS**. Another search is running.
  Any job seen past 1 GB is killed and rewritten, and that is disclosed. No downloads, no web look-ups.
- RSS is measured per job (forked child, `ru_maxrss`) and written to a side file so the main JSON and `.out` are
  byte-comparable. Timing goes to stderr only.

## W2. C6's in-window ladder, closed with a lower-memory solver

**Unchanged from V3W (not widened):** Route N (r_F = 0, C6's `build` and Newton loop logic), E2 field (D7b `ge_total`,
x_e = ge/a0 at the exact footing), both footings at the exact footing a0, Λ = L★/r_M with L★ = 24 pc (622 / 684), C6's
grid rule (r_in = 1e-4, r_out = 300Λ, in r_M), Q2 from C6/D7d's `q2_raw` at r_x = 1, 10, 100 r_Saturn with **100 r_Saturn
graded**, Newton tolerance 1e-9 on the scaled residual, Route F from C6's `routeF_Q2`.

**New: the linear solver inside Newton.** Only the linear solve of each Newton step changes. The Jacobian, residual,
scaling and line search are C6's (re-implemented line by line from `c6_solver.solve_v`, with the solve swapped).
- **Method A (primary): block-tridiagonal direct LU.** Unknowns are ordered shell-interleaved (C6's `interleave`).
  The operator couples shells i ± 2 (grad-div), so shells are grouped in pairs into super-blocks of size 6 N_θ and the
  matrix is block-tridiagonal. Block Thomas elimination with dense LAPACK LU per super-block (partial pivoting inside
  the block). The eliminated upper blocks are streamed to a scratch file outside the repo and read back in reverse
  (out-of-core), so RSS holds O(1) blocks.
- **Method B (cross-check): SuperLU with a fill-reducing column ordering** (`MMD_AT_PLUS_A`, then `COLAMD`) on the same
  scaled Jacobian, run at every rung where its peak RSS stays < 1 GB (probed in a forked child that is killed at 1 GB;
  a rung where B would exceed 1 GB is not run with B and that is disclosed).
- **Known answer (W2-K1):** Method A at V3W's rungs (30, 48) and (40, 64) reproduces V3W's committed Q2 values
  (`V3W_v3s_weak_spots/w2_c6_rerun.json`, `C6prime`, all three radii) to ≤ 1e-6 relative. **W2-K2:** where A and B both
  run, they agree on Q2 at the graded radius to ≤ 1e-6 relative.

**Ladder (frozen):** (points per decade, N_θ) = (40, 64), (50, 80), (60, 96), (70, 112): V3W's finest plus **three rungs
past it**, all at the same aspect ratio as V3W's ladder (h ∝ 1/n). Each rung solved in its own forked process from a zero
start (as V3W).

**Pass line, per (footing) cell, at 100 r_Saturn (V3W's line, unchanged):**
- (a) every rung converged, scaled residual < 1e-9;
- (b) the ladder converges: on the last three rungs the change d₂₃ (rungs 60 → 70) is smaller than d₁₂ (50 → 60), and the
  order-2 Richardson value from the last two rungs, R = q₃ + (q₃ − q₂)/((70/60)² − 1), differs from the finest rung by
  **< 2e-2 relative**;
- (c) R agrees with Route F at the same L★ within 5e-2, same sign (C5's line);
- (d) every job < 1 GB RSS.
- **Observed order (guard):** p_obs is solved from d₂₃/d₁₂ = (h₂^p − h₃^p)/(h₁^p − h₂^p) on (50, 60, 70). If p_obs lies
  outside [1.5, 2.5], the order-2 Richardson is not trusted and the cell is UNDECIDED. The Richardson value at p_obs and
  its distance from the finest rung are reported beside the graded one.

**Label per footing (C6's check C6, in window):** PASS iff (a)–(d) hold and the guard holds, W2-K1 holds, and W2-K2 holds
wherever B ran; FAIL iff (a), (b) and the guard hold but (c) fails (the in-window Q2 disagrees with Route F); UNDECIDED iff
a rung fails to converge, the memory line is crossed, the guard fails, (b) fails, or K1/K2 fails. The overall W2 label
is then V3W's W2 rule with C6′ replaced by this result (C1, C3–C5, C7, C8 as V3W reproduced them; C6P's 24-cell Q2 band
read from C6P).

**MUTATE twin (W2):** `V3X_MUTATE=noscreen`: screening removed (Λ → 0, AQUAL), as V3W. Q2 must return to the AQUAL value
outside the Hees band and the label must not be PASS (exit 1).

## W4c. Health on the Solar-System background, β = η = 0

### Background (frozen)
- **The Sun's screened background is C6's Route N solution** at L★ = 24 pc (Λ 622 / 684), exact footing a0, E2 field,
  rung (30, 48) solved with Method A. From it: Δp = p(v_e + w) − p(v_e) (C6/D7d's `dP`, no cancellation), the total
  p = p_e + Δp, and ρ̄_τ = D·P̄ = ∇·Δp / K by second-order finite differences on the (ln r, θ) grid (D7d's θ operators).
- **Galactic phantom** from X3 D2's committed json: ρ_gal,min = 0.0055 / 0.0062 M☉/pc³ (box minimum, canonical / alt) for the
  lower bracket, ρ_gal,Sun = 0.0447 / 0.0514 for the upper bracket. **Dust ρ_d = 0** (X3's knife edge, worst case; ρ_d ≥ 0
  only raises ρ̄_τ). μ_K = 0 at these scales (μ_K L★ ≤ 2.4e-6; modes with k < μ_K do not fit in the domain).
- **Domain** r ∈ [r_in, r_out] with r_in = 1e-4 r_M (0.80 / 0.73 AU, C6's inner radius) and **r_out = L★ (graded)**;
  r_out = 10 L★ is reported. Baryons (the Sun) are a fixed external source; their own perturbations are not included.
- **Background known answer (W4c-K4):** the monopole of ρ̄_τ from Route N equals the analytic hedgehog
  ρ_h = −2Φ_N/(K L★²) = M☉/(2π L★² r) to ≤ 1e-2 relative for r ≤ 0.1 L★, excluding the three innermost shells. If K4
  fails, (b) is UNDECIDED.
- Brackets: ρ_lo(r) = min_θ ρ̄_τ(r, θ) + ρ_gal,min, ρ_hi(r) = max_θ ρ̄_τ(r, θ) + ρ_gal,Sun; M_lo = min M_T, M_hi = max M_L
  over the domain (M_T = 1 + x, M_L = (1 + x)², x = |v|, from the solution).

### (a) Quadratic action
- **PN quadratic action (sympy, 3D, general background).** Start from the weak-field Lagrangian of the action above
  (BS24's PN system, as in X3 B2-S, here in 3D): L = −|∇φ|²/2K − ρ_bφ + P·∇Ξ − W(K|P|) − (γ_L/2)F(∇·P) + μ_K²Ξ²/2K,
  Ξ = φ − ∂_tσ + |∇σ|²/2, with arbitrary background functions φ̄(x), P̄(x), Ξ̄ = φ̄ + C, σ̄ = 0 (held, static), general W
  and F(s) = s² on the stiff side (Θ = 1, D·P̄ > 0). Expand to second order in (δφ, δσ, δP).
  - **(a1)** the Euler–Lagrange equations of L₂ equal the linearised Euler–Lagrange equations of L (residual 0);
  - **(a2)** L₂ equals the reduced form L₂* = −|∇δφ|²/2K − δΞ₁∇·δP − ρ̄_τ|∇δσ|²/2 − ½δP·H·δP − (γ_L/2)Θ(∇·δP)²
    + μ_K²δΞ₁²/2K, δΞ₁ = δφ − ∂_tδσ, ρ̄_τ = ∇·P̄ − μ_K²Ξ̄/K, H the Hessian of W, up to a null Lagrangian (the EL operator
    of L₂ − L₂* vanishes identically);
  - **(a3) GR limit (known answer):** with the P sector removed (P ≡ 0, W ≡ 0, γ_L = μ_K = 0) L₂ is GR's Newtonian quadratic
    action −|∇δφ|²/2K exactly and δσ drops out (no scalar mode: GR's scalar sector).
- **Relativistic local quadratic matrix.** C5's 10-field builder (`build_local`: n, N_i, ζ, h₊, h×, δP_i on a frozen
  background with uniform P̄, lapse gradient g ∥ P̄, wave angle θ to P̄), executed read-only from C5's source by AST
  extraction (nothing edited), at β = η = γ_F = μ_K = 0. **(a4)** the matrix is Hermitian, and at P̄ = g = 0 (the law's
  background off, Minkowski) its non-zero roots are GR's two tensor modes ω² = k² exactly, with the remaining roots at
  ω = 0, reproducing C5 H4's C4-literal Minkowski row (mode and zero-root counts from C5's json).
- **Label (a):** PASS iff (a1)–(a4) all hold; FAIL iff a residual is non-zero for a reason in the action; UNDECIDED if a
  derivation cannot be completed (say where).

### (b) Kinetic and gradient matrices, eigenvalues, full non-WKB spectrum
- **Reduction (from (a), μ_K = 0).** Eliminating δφ and δP (both constrained) gives, per unit volume,
  L = ½⟨δρ̇, 𝒜⁻¹δρ̇⟩ − ½⟨δρ, 𝒱δρ⟩, with δρ = ∇·δP, 𝒜 = −∇·(ρ̄_τ∇) (kinetic matrix 𝒜⁻¹), and the gradient (potential)
  operator 𝒱 = γ_LΘ + L_W⁻¹ − K L₀⁻¹, L_W = −∇·H⁻¹∇, L₀ = −∇². Equivalently, in δσ: kinetic 𝒱⁻¹, gradient 𝒜. ω² is
  the spectrum of 𝒜𝒱. This reduction is checked symbolically (uniform background: ω² = Kρ̄(M_θ − 1) + ρ̄γ_Lk², X3/H4's
  dispersion, residual 0).
- **Radial non-WKB spectrum (the graded numbers).** Finite-volume discretisation on a log-r grid over [r_in, r_out], per
  spherical harmonic l = 0…4, with the same discrete gradient for 𝒜, L_W and L₀ (so the discrete 𝒱 ≥ γ_L exactly when
  M ≥ 1). Lower bracket (ρ_lo, M_lo) and upper bracket (ρ_hi, M_hi): by operator monotonicity (𝒜 and 𝒱 enter monotonically,
  Courant–Fischer), the 3D anisotropic spectrum lies between them. BCs: outer Dirichlet (δσ = δφ = 0); inner Neumann
  (graded) and inner Dirichlet (reported at the finest rung).
  - Ladder: 8, 12, 16 cells per decade. Each rung: the minimum eigenvalues of the kinetic and gradient matrices (Â and V̂),
    and the lowest five ω² per (l, bracket), from the symmetric form C = RᵀV̂R, Â = RRᵀ (Cholesky).
  - **Precision.** Built and diagonalised in mpmath (40 digits, graded; 30 and 60 digits at the finest rung, l = 0, as a
    precision ladder: lowest ω² agree to ≤ 1e-12 relative). A float64 diagonalisation is reported beside it to show the
    conditioning.
  - **Known answer W4c-K3 (uniform background, W4b reproduced):** on a uniform ρ̄, M ball the code returns
    ω² = Kρ̄(M − 1) + ρ̄γ_Lλ_h exactly (λ_h the discrete L₀ eigenvalues; ≤ 1e-25 relative at 40 digits) and λ_h → the Bessel
    zeros j²_{l+1/2,n}/R² on the ladder; galaxy parameters x = 1 (M_T 2, M_L 4) used. V3W's W4-K6 value (min of
    M_θ − 1 + L★²k²/2 over V3W's grid, `w4_health_gw.json`) is recomputed identically.
- **Label (b), per footing:** PASS iff at every rung, l, bracket and BC: Â and V̂ are positive definite (min eigenvalue
  > 0 by more than 1e-20 of the max), min eig V̂ ≥ γ_L(1 − 1e-12), every ω² > 0, the lowest three ω² per (l, bracket)
  change by < 5e-2 between the last two rungs, the precision ladder holds, K3 and K4 hold, **and** the relativistic local
  check below passes. FAIL iff any ω² < 0 beyond precision, or ρ̄_τ < 0 on the solution grid beyond its discretisation
  error (then 𝒜 is indefinite on an open set and, with 𝒱 positive definite, negative ω² exist by inertia), or the
  relativistic check finds ω² < 0 or a negative Krein norm. UNDECIDED iff a ladder or precision line fails, or K3/K4
  fails.
- **Relativistic local check (C5's matrix, β = η = γ_F = 0).** Solar-System background as C5's `bg_named("Solar System")`:
  u₀ = a0L x_e/(1 + x_e) with x_e = max of D7d's scan (C5's choice), g = GM☉/AU² in L★ units, both footings,
  L★ ∈ {21.7 / 22.9 (floors), 24, 90} pc, θ ∈ 13 values on [0, π], k = L★/r for r ∈ {1, 10, 100, 1000} AU (g/k ≤ 1e-5,
  WKB valid). C5's `modes`/`summarize` at C5's precision (120 digits). Pass: no ω² < 0, no negative Krein norm, and the
  non-zero roots are the two tensor modes with |ω²/k² − 1| ≤ 1e-10.

### (c) 3D hyperbolicity
- **Principal symbol in all directions (sympy).** The nonlinear PN khronon system (continuity for ρ_τ with v = −∇σ,
  Bernoulli/Euler, the P equation with the switched stiffness, Poisson) linearised with frozen coefficients about an
  arbitrary state (ρ̄_τ, v̄, P̄, H symmetric positive, Θ), for an arbitrary direction ξ ∈ ℝ³ (three free components). Pass:
  the characteristic roots are ω = v̄·ξ ± c|ξ| with c² = γ_LΘ(D·P̄ + ρ_d) for every ξ (residual 0), the P equation's
  symbol H + γ_LΘξξᵀ is positive definite for every ξ, and the remaining roots are ω = v̄·ξ (the curl part, absent for
  v = −∇σ). This is the 3D version of X3 B2-S's 1D result.
- **Numerical 3D symbol on the actual background.** At every (r, θ) node of the background in the domain and 2000 Fibonacci
  directions ξ̂, the exact frozen-coefficient roots of the full linear system (with H and the order −2 terms) at
  |ξ| = 10³/r and 10⁶/r: ω²/(c²|ξ|²) → 1, deviation reported.
- **Cones.** c_s,max/c over the domain (c_s² = γ_Lρ̄_τ), the tensor speed from the relativistic check (c_T = c in every θ),
  and |v̄| + c_s with |v̄| ≤ 370 km/s if the Sun moves through the khronon frame (reported bound; the background itself is
  C6's Sun at rest, as C6/C8).
- **Label (c), per footing:** PASS iff the symbolic symbol holds for all ξ, c² > 0 at every background node in the domain
  (ρ_lo > 0, Θ = 1), the propagating speeds are ≤ c (c_s,max/c < 1, c_T = c), and a positive conserved energy exists
  (Â and V̂ positive definite from (b)). FAIL iff c² < 0 at a node or a speed exceeds c. UNDECIDED iff c² = 0 somewhere
  in the domain (degenerate) or a check fails. **Stated with the label, not graded here:** P, δφ and the lapse obey
  elliptic constraints that act instantaneously on the khronon leaves. That is C5's structural finding (criterion B,
  global time, passes; criterion A, v ≤ c in the cone sense, fails) and is carried as recorded.

### W4c checks and twins
- **Byte-identical rerun** of each main script (SHA-256 of JSON and `.out`).
- **MUTATE twins, each must bite (exit 1, label not PASS):**
  - `V3X_MUTATE=eta`: η = γ_L put back (β = 0) in the relativistic local check: ω² < 0 must return on the Solar-System
    background (C5 H7's rate at k = 1/AU, 83 / 95 per yr, reproduced to ≤ 1e-3 relative).
  - `V3X_MUTATE=noscreen`: screening removed (γ_L → 0): the background is C6's Route N at Λ = 0 (AQUAL), and the PN
    part must find ρ̄_τ < 0 inside the domain (Â indefinite, negative ω²) and c² = 0 (no strict hyperbolicity).
- Ladders: W2 resolution ladder; W4c background rung, spectral resolution ladder, mpmath precision ladder.

## Output
`README.md` leads with a one-line verdict and a table W2 / W4c(a, b, c) × canonical / alt. It states: not blind;
κ = ½ FITTED; footings never pooled; not theory closed; nothing here says the data favour the framework; adopts nothing;
the cold sector stays retired; CMB and clusters are out of scope and open; a0 is put in by hand. Anything still resting on
the record without a passing check is marked **ASSERTED**. One pointer line under the v3s row of
`rebuild_2026_10_22/AX1_action_for_law/README.md` and one in `rebuild_2026_10_22/V3W_v3s_weak_spots/README.md`.
