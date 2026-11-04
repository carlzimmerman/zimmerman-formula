# V3X_v3s_close_undecided: neither item closes cleanly. In W2, the in-window C6 ladder now meets every one of V3W's lines on both footings (Richardson −0.70 % / −0.74 % against 2e-2, N/F 0.9999 / 0.9997), but my own known-answer check K1 fails at an ungraded radius. In W4c, (a) and (c) PASS. (b) shows no instability anywhere (every ω² > 0, both operators positive definite), but it is UNDECIDED: two of its own lines fail, the spectral ladder at l ≥ 1 and the 1e-10 tensor line

**Owner 11-04:** "Yes, close both", about V3W's UNDECIDED W2 and W4c. **This lane adopts nothing**, and the 10-24 v3s verdict
stands: v3s passes as a galaxy-scale law and fails as gravity plus cosmology.

**Standing statements.**
- **Not blind.** V3W, C6, C6P, C5, C8, X3 and V3_FULL_PICTURE were read first.
- κ = ½ FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled.
- Not theory closed. Nothing here says the data favour the framework.
- The cold sector stays retired. CMB and clusters are out of scope and open. a0 is put in by hand.
- No file under `covariant_push_2026_10_22/` or `doors_push_2026_10_22/` was edited. C6/D7d code is imported read-only,
  and C5's source is executed read-only by AST extraction.

**Files and compute.**
- Criteria: `FROZEN_CRITERIA.md` (859c76bec3), committed alone first. Amendments: `AMENDMENTS.md` (0f79edf051), committed
  alone before the production runs.
- Scripts: `v3x_solver.py`, `v3x_w2_ladder.py`, `v3x_w4c_health.py`. Outputs `*.{json,out}`; reruns `*_RERUN.*`; twins
  `*_MUTATE*.*`; RSS side files `*_rss.json`.
- Compute: one thread, nice 15, no downloads. The worst completed job used 0.85 GB. W2 takes about 12 min per run, W4c
  about 15 min.

## Table

| | canonical | alt |
|---|---|---|
| **W2** C6's check C6, in window (L★ = 24 pc) | **UNDECIDED (reading PASS).** The ladder at (40,64) / (50,80) / (60,96) / (70,112) meets every V3W line: all rungs converged (residual ≤ 1.5e-14); d₂₃/d₁₂ = 0.610 (order 2 expects 0.603), p_obs = 1.94; **Richardson − finest = −7.0e-3 against 2e-2**; N/F = 0.99994. The clean label fails on **K1**: Q2 at 1 r_Sat is 2.2e-3 off V3W's value, against a 1e-6 line | **UNDECIDED (reading PASS).** Richardson − finest = −7.4e-3; p_obs = 1.65; N/F = 0.99972. K1 fails at 1 r_Sat (7.5e-4) and at 10 r_Sat (1.0e-5) |
| **W4c (a)** quadratic action | **PASS.** The PN L₂ is derived in 3D for a general background and a general W. Its EL equations equal the linearised EL equations (residual 0); it reduces to L₂* up to a null Lagrangian (0); the GR limit is exact. C5's 10-field matrix is Hermitian, with GR's two tensor modes at Minkowski to 6e-61 | **PASS**, same |
| **W4c (b)** kinetic and gradient matrices, non-WKB spectrum | **UNDECIDED (no instability found).** Over 40 graded radial cases (l = 0–4, lower and upper brackets, 3 rungs), the kinetic and gradient matrices are positive definite (min eig Â = 1.0e-10; V̂ ≥ γ_L = 1.934e5) and **every ω² > 0**. The lowest is 2.82e-5 a0/r_M = 2.2e-30 s⁻², a period of about 134 Myr. C5's matrix at β = η = 0 finds 0 unstable and 0 ghost points out of 156. **Two lines fail:** the ladder change on the three lowest ω² is up to 14.6 % at l = 4 (line 5 %; only l = 0 passes), and the tensor roots sit 1.1e-10 below 1 (line 1e-10) | **UNDECIDED (no instability found).** Same; min eig Â = 7.1e-11, V̂ ≥ 2.337e5, lowest ω² 2.25e-5 a0/r_M (2.4e-30 s⁻²). The ladder misses by up to 14.7 % and the tensor line by 1.2e-10 |
| **W4c (c)** 3D hyperbolicity | **PASS.** The principal symbol is Ω² = γ_LΘ(D·P + ρ_d)\|ξ\|² in every direction ξ (sympy, 9-field system, residual 0). c² > 0 at all 544 background nodes. Characteristic speeds are c_s ≤ 33 km/s (1.1e-4 c) in the domain and c_T = c. A positive conserved energy exists. **The constraints are instantaneous** (C5's criterion A fails, carried, not graded here) | **PASS**, same; 560 nodes, c_s ≤ 35 km/s |

## W2. C6's in-window ladder

The pass lines are V3W's, unchanged and not widened: residual < 1e-9, d₂₃ < d₁₂, order-2 Richardson within 2e-2 of the
finest rung, N/F within 5e-2, RSS under 1 GB. This lane adds a guard that p_obs lies in [1.5, 2.5].

**Solver (`v3x_solver.py`).**
- It is C6's Newton loop with a different linear solve.
- **Method A**, Gaussian elimination with partial pivoting on two-shell super-blocks.
  - In the interleaved order the grad-div operator makes the matrix block-tridiagonal. Pivots are searched over block
    rows j and j + 1, which is banded LU's pivot set.
  - Factors are streamed to a scratch file outside the repo, so the peak at (70,112) is 0.76 GB, against about 1 GB that
    C6's NATURAL SuperLU already needed at (40,64).
- **Method B**, SuperLU with COLAMD, ran at (30,48) and (40,64). It matches A to ≤ 1.1e-7 (**K2 PASS**).
  - At (50,80) B was killed at the watchdog line (0.86 GB).
  - MMD_AT_PLUS_A was killed at (30,48), after it reached **1.01 / 1.05 GB**: over the 1 GB rule for well under a second
    before the kill. This is disclosed.
  - An earlier production run with a 0.98 GB, 1 s watchdog let the B probes reach 1.02–1.05 GB. The final runs use
    0.85 GB polled every 0.1 s.

**Amendment A1** (`AMENDMENTS.md`; made after smoke tests, before production).
- **Change.** Each Newton step adds a diagonal shift of 1e-12 on the w rows of C6's row-scaled Jacobian. After the
  residual first drops below 1e-9, three polish steps follow.
- **Why.** From (60,96) on, the law's r² entries fall below float64 ε against the grad-div stiffness at the inner shells.
  Unshifted Newton then stalled at (60,96) or failed at (70,112).
- **Effect.** The converged state still meets C6's residual test. Shift sensitivity (1e-10 against 1e-12) is ≤ 2.5e-7
  at the graded radius.

| Q2 at 100 r_Sat (s⁻²) | (40,64) | (50,80) | (60,96) | (70,112) | Richardson (60/70) | Route F |
|---|---|---|---|---|---|---|
| canonical | 1.64434e-34 | 1.63086e-34 | 1.62412e-34 | 1.62002e-34 | 1.60865e-34 (−0.70 %) | 1.60875e-34 |
| alt | 1.39996e-34 | 1.38834e-34 | 1.38255e-34 | 1.37885e-34 | 1.36859e-34 (−0.74 %) | 1.36898e-34 |

- **Why the clean label is UNDECIDED.** I froze K1, the reproduction of V3W's committed Q2 at all three radii, to 1e-6.
  - At the graded radius it reproduces to 4.6e-8 (canonical) and 1.0e-7 (alt).
  - At 1 r_Saturn it misses by 2.2e-3 and 7.5e-4. At 10 r_Saturn alt misses by 1.0e-5.
  - V3W recorded that at r_Saturn the l = 2 part is ~1e-18 of the monopole, beyond float64, so that radius is solver
    noise. That makes K1's wording my criteria error. It was not amended after the fact.
  - Under the frozen rule the label is UNDECIDED. The physics reading is a PASS.
- **C6′ is a PASS on both footings**: the C6′ check passes, the extrapolation agrees with Route F to 6e-5 / 3e-4, and
  C6P's 24-cell band is unaffected.
- **MUTATE** (screening removed): Q2 = 3.49e-26 / 3.91e-26, N/F about 2e8, and both labels **FAIL** (outside the Hees
  band); exit 1.
- **Reruns.** SHA-256 of json / out: 6285d19f8288 / 327af1399a1b, equal to the `_RERUN` copies. A further rerun of the
  final script file gave the same hashes.

## W4c. Solar-System background, β = η = 0

### (a) Quadratic action
In the PN limit, with δΞ₁ = δφ − ∂_tδσ, ρ̄_τ = D·P̄ − μ_K²Ξ̄/K and H the Hessian of W:

    L₂ = −|∇δφ|²/2K − δΞ₁ ∇·δP − ρ̄_τ|∇δσ|²/2 − ½ δP·H·δP − (γ_L/2)Θ(∇·δP)² + μ_K²δΞ₁²/2K

- **(a1).** Derived in 3D for an arbitrary static background and a general W. Its EL equations equal the linearised EL
  equations of the full PN Lagrangian (5 fields, residual 0).
- **(a2).** The difference from the expanded form is a null Lagrangian (residual 0). The negative control, which drops
  the integration by parts, fails.
- **(a3).** With the P sector removed, L₂ = −|∇δφ|²/2K exactly and δσ drops out: GR's scalar sector.
- **Uniform-background check (b0).** It reproduces H4/X3's ω² = ρ̄_τ(k²/χ − K) exactly.
- **Metric sector.** C5's relativistic 10-field matrix (lapse, shift, ζ, h₊, h×, δP) is used at β = η = γ_F = 0.
  - It is Hermitian.
  - At Minkowski it gives 2 modes plus 2 ω = 0 roots, equal to C5 H4's row, with ω² = k² to 6e-61.
  - Correction disclosed: the first execution compared with "== 0" at 120 digits and failed on 6e-61. The comparison was
    changed to the working precision (≤ 1e-50).

### (b) Kinetic and gradient operators, spectrum
- **The operators.** Eliminating the constraints δφ and δP gives
  L = ½⟨δρ̇, 𝒜⁻¹δρ̇⟩ − ½⟨δρ, 𝒱δρ⟩, where:
  - the kinetic operator is 𝒜⁻¹, with 𝒜 = −∇·(ρ̄_τ∇);
  - the gradient operator is 𝒱 = γ_LΘ + L_W⁻¹ − K L₀⁻¹.
- **Why 𝒱 ≥ γ_LΘ.** M_T, M_L ≥ 1 gives H ≥ K pointwise, so L_W⁻¹ ≥ K L₀⁻¹ by operator monotonicity. This needs no WKB.
  Stability on any background therefore reduces to ρ̄_τ ≥ 0.
- **The background is C6's Route N solution** at (30,48), with residual 2e-14 / 1e-14.
  - **K4 PASS.** The monopole of D·P equals the hedgehog M☉/(2πL★²r) to 2.5e-3 / 2.2e-3 at r ≤ 1e-3 L★ (amendment A2).
    Over the frozen range r ≤ 0.1 L★ the gap is 0.22 / 0.20, as A2 predicted before the run.
  - **Minimum ρ̄_τ** (Sun's response plus X3's minimum Galactic phantom, dust 0) is 3.98e-6 / 3.36e-6 in units of a0/(K r_M).
    That is the phantom: the Sun's own response stays ≥ +3e-10 inside L★.
  - M ranges over 3.20–10.24 (canonical) and 2.82–7.95 (alt).
- **The spectrum.** It is non-WKB and per l, with lower and upper brackets that enclose the 3D anisotropic spectrum by
  Courant–Fischer. It was diagonalised in mpmath at 40 digits.
- **Results:**
  - every one of the 40 graded cases has ω² > 0, and so do inner-Dirichlet BCs and r_out = 10 L★;
  - precision ladder 30 / 60 digits: identical to 20 digits;
  - float64 agrees here to 1e-15;
  - **K3 PASS**: the uniform ball is exact to 3e-29 and converges to the Bessel zeros; V3W's W4-K6 value 1.000e-4 is
    reproduced.
- **What fails.**
  - **The ladder line.** The 12 → 16 cells-per-decade change of the three lowest ω² is 4.6 % / 4.8 % at l = 0 and
    7–15 % at l = 1–4, against 5 %. The spectral grid is too coarse for the higher modes. No sign changes: all rungs are
    positive. A finer ladder would decide it.
  - **The relativistic tensor line.** C5's matrix on the Solar-System background (156 points per footing, 13 angles,
    r = 1–1000 AU) finds 0 unstable and 0 ghost points, and exactly 2 non-zero roots everywhere. Those roots sit up to
    1.1e-10 / 1.2e-10 below ω² = k², against my 1e-10 line. That is the frozen lapse gradient (g at 1 AU) applied at
    r = 1000 AU, which is subluminal.
- **Label.** Both failures are line misses, not instabilities, so the label is UNDECIDED, with no instability found.

### (c) 3D hyperbolicity
- **Symbol.** The 9-unknown frozen-coefficient system (sympy, H in its own frame, arbitrary ξ and v̄) has
  det = Ω²·[Ω² − ρ̄|ξ|²(γ_LΘ + 1/ξ·H⁻¹·ξ) + Kρ̄] × (a positive ω-free factor). Its principal part is
  Ω² = γ_LΘρ̄|ξ|² in every direction. That extends X3's 1D result to 3D.
- **The P symbol** H + γ_LΘξξᵀ is positive definite.
- **On the actual background** (544 / 560 nodes × 2000 directions):
  - c² > 0 everywhere;
  - the symbol tends to c²|ξ|² (7.7e-12 at |ξ| = 1e6/r);
  - the eliminated formula equals the exact 9 × 9 roots (50-digit elimination) to 7e-16.
  - Correction disclosed: two earlier executions mis-evaluated the 9 × 9 roots in float64 (conditioning).
- **Cones.**
  - In the hedgehog region c_s² = γ_L ρ̄_τ = |Φ_N| exactly. That gives 33 km/s at 0.8 AU, 437 km/s at the solar surface
    and 535 km/s at a uniform Sun's centre. With a 370 km/s khronon-frame speed this is still 3e-3 c.
  - c_T = c, with the roots at or below 1.
- **Correction disclosed: the (c) label code.** The first full execution gated (c) on (b)'s 1e-10 tensor line. It was
  regated to the frozen (c) criterion, propagating speeds ≤ c. Before the change: (c) UNDECIDED with no failing check
  named.
- **Stated with the label, not graded.** P, δφ and the lapse obey elliptic constraints that act instantaneously on the
  khronon leaves, as C5 recorded: criterion B (global time) passes, criterion A (v ≤ c in the cone sense) fails.

### Checks and twins
- **Known answers.** GR limit (a3, a4) exact. W4b reproduced (K3, and V3W's W4-K6). Background K4.
- **MUTATE `eta`** (η = γ_L, β = 0, C5's matrix on the Solar-System background): **bites.** 144 of 156 points are
  unstable on each footing, min ω² −1.3e11 / −1.7e11 (L★ units); labels FAIL; exit 1.
  - C5 H7's Solar-System rate is reproduced: 83.30 /yr canonical, 6.5e-5 from C5's ω².
  - Alt gives 95.19 /yr against C5's 95.09, a 2.1e-3 gap that **fails the 1e-3 line**. It is the footing: C5 ran at
    1.13e-10, and ω² ∝ u₀² moves by 2 × 0.106 %. This is disclosed.
- **MUTATE `noscreen`** (γ_L → 0, Route N at Λ = 0): **bites.**
  - The Sun's unscreened phantom has negative lobes, min ρ̄_τ −0.85 / −0.63 a0/(K r_M) at r ≈ 0.8–0.9 r_M.
  - Â is indefinite, and the lowest ω² is −0.135 / −0.057 (a bounded instability, as in H4).
  - c² = 0, so the system is not strictly hyperbolic.
  - Labels: (b) FAIL, (c) UNDECIDED; exit 1.
- **Byte-identical rerun.** SHA-256 of json / out: 180676d37014 / 81d76b6f672d, equal to the `_RERUN` copies.

## ASSERTED (still resting on the record without a check here)
- Post-Newtonian corrections to (a)'s coefficients, O(GM/c²r) ≤ 2e-6, are taken not to flip any sign. The tensor sector's
  principal part is W4a's and C5's.
- Inside the Sun the background is the hedgehog formula c_s² = |Φ_N|, with a uniform-density Sun (illustrative).
- The Sun is at rest in the khronon frame (C6/C8). X15 says a moving Sun does not carry its hedgehog at β = 0.
- Nonlinear well-posedness and the moving interface are open (X3).

## Unfinished
- **W2.** The clean label needs K1 restated at the graded radius. That is the owner's call; the physics reading is PASS.
- **W4c (b).** A finer spectral ladder (≥ 24 cells per decade) is needed to clear the 5 % line at l ≥ 1. Whether 1e-10
  was the right tensor line is a criteria question.
- **Still open, as in the 10-24 verdict:** clusters, growth/CMB, the radiation era, hosted dwarfs and the MW disc.
