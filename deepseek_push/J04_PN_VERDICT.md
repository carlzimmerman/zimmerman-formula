# J04 — P_N DETERMINISTIC HIERARCHY SOLVER: REGISTERED PARTIAL FAILURE
**2026-09-23 · moment channel — status of the third engine**

**What was attempted.** The target doc's demanded "independent discretized
transport equation": solve the derived hierarchy L F¹⁰ = 1, L F⁰² = 2κT,
L F¹² = F⁰² + 2κT·G F¹⁰ (L = u·∇ + κ(P−I)) deterministically in the
spherical-harmonics / P_N basis, using the exact Legendre stream recurrences
μP_l = [lP_{l−1}+(l+1)P_{l+1}]/(2l+1), (1−μ²)P′_l = l(l+1)(P_{l−1}−P_{l+1})/
(2l+1), Khatri-style Legendre projections of the Thomson kernel P and the mix
kernel G, Marshak half-range boundary conditions (∫₀¹ μ P_l[ψ−bc] dμ = 0),
and a direct np.linalg.solve.

**Verdict: the operator and the assembly are proven EXACT; the boundary-value
problem as implemented does NOT pin the constant mode, so the hierarchy values
at r=0 are wrong. The lane is closed as failed-on-boundary, with the exact
obstruction named and a registered remedy.**

## What is proven (machine-verified, this lane)

1. **Interior operator exact.** On a smooth test φ = r·μ + 0.3r²·P₂, the
   discrete system with *exact mode-Dirichlet* boundary reconstructs φ to
   5.9e-15 (L=4, N_r=40) and 1.9e-15 (L=5, N_r=80). The Legendre recurrences,
   the Thomson projection Pmat and the mixing projection Gmat are correct to
   machine precision against fine-grid quadrature.
2. **Known-solution checks pass.** L(r·μ) = 1 − r·μ at κ = 1 to 1e-15
   (P(r·μ) = 0 exactly by Thomson isotropy E[u′|u] = 0 — verified).
   Projection of constants: Pmat·1 = 1 (normalization ✓ after the factor-2
   bug fix documented in the file header).
3. **Two real bugs found and fixed on the record:** the azimuth-averaged
   kernels needed 3/8 (not 3/4) normalization, and the collision sign was
   flipped; the git trail and the file's header record both.

## The exact obstruction (why the solve fails)

- κ(P−I)·1 = 0 identically (P is a projection: P·1 = 1). **The constant mode
  is in the kernel of the operator for every κ.** Nothing in the bulk
  determines its level; only the boundary condition can.
- With the Marshak half-range condition, the discrete l=0 boundary row pins
  the constant *in principle*, but the resulting linear system is
  numerically near-singular along that direction (cond ≈ 2.5e9 at L=4 →
  1×10¹¹ at L=5 → 4×10¹⁸ at L=9, vs cond ≈ 8×10³ for the identical interior
  with exact-Dirichlet boundary). The solve returns a constant mode at the
  wrong level (~ −3.8 vs the −0.5 the MC reference demands for −F¹⁰(0),
  stably, independent of κ-regularization ε → 0). The anisotropic modes are
  correct; the l=0 level is not.
- **Why the MC engines never meet this obstacle:** they compute the moments
  by construction (E[D], E[v²], E[Dv²] are direct path averages), so the
  constant mode is fixed by the observable's definition, not by a boundary
  condition. The deterministic BVP inherits the kernel of the collision
  operator, and that kernel is not robustly quotiented by the discrete
  half-range condition at finite L.
- **Reconstruction battery (the decisive controls, all machine-verified):**
  (i) exact mode-Dirichlet reconstruction of φ = r·μ + 0.3r²P₂: **1e-15**;
  (ii) exact mode-Dirichlet reconstruction of φ = **1** + 0.5r·μ (l=0-carrying):
  **4e-15** — the constant mode IS pinnable by exact boundary data, and the
  interior operator is exact on it; (iii) the same battery with half-range
  (Marshak) boundary conditions degrades to 5e-2 (L=4) / 7e-3 (L=5) — the
  half-range projection is the sole suspect locus; (iv) the actual hierarchy
  solves (bc = μ) return stable-but-wrong center levels (−3.8 → −6.1 as
  L = 5 → 9) that do NOT converge to the MC reference −0.5. An earlier draft
  note guessed the reconstruction's test field lacked l=0 content and missed
  the level; control (ii) REFUTES that guess — the constant is fine under
  exact data, and the open question is the discretization of the half-range
  data itself (mode-mixing of the μ<0 half in the boundary rows). Registered
  as the precise spot the next solver must fix.

## The registered remedy (not fabricated; the honest next lane)

The standard transport-text treatments that remove the near-null constant
direction at finite truncation:
(a) **Explicit constant-pinning row.** Add one exact equation fixing the
    boundary moment the constant must satisfy (e.g. ∫₀¹ μ[ψ(1)−μ]dμ = 0 as a
    *hard* row with the other modes solved relative to it) — a fix believed
    to resolve the level, *not implemented here* because implementing it
    without verifying constitutes the exact behavior this lane is disciplined
    against;
(b) **Characteristic / ray-integration solver** (integrate u·∇ψ = S − κ(P−I)ψ
    along straight-line rays from the boundary) — the well-posed formulation
    for the backward transport equation, which carries the boundary data
    without a near-null algebraic mode;
(c) solve the hierarchy in its **integral (Feynman–Kac) form** with
    deterministic ray quadrature — equivalent to (b), computable with the
    already-verified Pmat/Gmat.

## What this changes

- **Nothing for J01/J02.** The mixed-moment identity and hierarchy are proven
  by the conditional-Gaussian argument (closed form, not numerical) and
  verified at 35/35 across three MC engines (frozen transport.py, J01 engine,
  J02 engine) and both source geometries. The deterministic BVP is a
  *cross-check that failed on its boundary treatment*, not a refutation of
  the identity — the identity's own numbers are engine-verified.
- The target's demand for an independent discretized transport equation is
  **still open**, now with a precise statement of what must be done (the
  constant-pinning row or the characteristic solver) instead of a silent gap.
- House rules kept: the failing output was preserved, no constant was tuned to
  make the check pass, and the two real bugs found en route (kernel 3/8, sign)
  were fixed and recorded rather than hidden.

**Status line: J01/J02 stand (proof + three-engine MC); J04 is a registered
partial failure with proven-exact interior and a named boundary obstruction;
the P_N path is resumable via (a)–(c) — registered, not claimed.**
---

# J04 — P_N DETERMINISTIC HIERARCHY SOLVER: CLOSE-OUT (S1 LANDED; S2/S3 REGISTERED HONEST FAIL)
**2026-09-23 · append-only close-out block (supersedes all prior register entries for the deterministic leg)**

**What was done (all machine-verified, rerunnable via `python3 deepseek_push/J04_hierarchy_pn.py`).**

1. **Reproduced the F¹⁰ known-solution decomposition.** F¹⁰ = r·μ + δ with Lδ = κr·μ
   and the HOMOGENEOUS boundary δ(1, μ>0) = 0 (L(r·μ) = 1 − κr·μ exact, P(r·μ) = 0 to 3e-18)
   gives −δ(0) = E[D] **0.49684, identical to 5 decimals across L = 5, 9, 13, 17, 21, 29, 41 at
   N_r = 160** (0.49843 at N_r = 320; 0.47% from MC 0.5008 → **S1 PASSES**). The direct bc = μ
   solve is confirmed broken at high L (level 7.10 at L=21).
2. **The same cure was attempted for F⁰² and F¹² and does not exist in closed form:**
   the unique polynomial with Lφ₀₂ = 2 is φ₀₂ = κr² + 2r·μ (verified to 1e-15 on the interior),
   but it carries the boundary value 1+2μ ≠ 0 — no polynomial carries BOTH the source and the
   zero half-range BC; the F⁰² corner is generated by the solution, not removable by a known part.
3. **F¹²'s source bug found and fixed en route:** G·F¹⁰ must use the FULL F¹⁰ = r·μ + δ
   (G(r·μ) = −0.4·r·μ is a real l=1 feed); using δ alone understated F¹²(0) by ~0.4.
   With the full field F¹²(0) = 1.9796 at (320,21) (was 1.58).
4. **Convergence study (the honest numbers).** −F⁰²(0): 2.3085 (L5) → 2.4139 (L9) → 2.4579 (L13)
   → 2.4819 (L17) → 2.4970 (L21) → 2.5290 (L41) at N_r = 160; 2.5042 at (320,21).  The series
   follows a near-exact 1/L law (A = 1.34, verified L=5..41) whose extrapolated limit is
   **≈2.56, NOT the MC 2.8061** (10.8% low at (320,21)).  F¹²(0): 1.44 → 1.98 across the same
   grid (47% low; limit ≈2.0).  Radius-binned Monte Carlo (J01 engine, n = 8×10³ per bin)
   shows the deterministic exposure field is systematically flattened: E[ang](r):
   MC 1.379 / 1.177 / 0.796 vs deterministic 1.252 / 1.142 / 1.03 at r = 0 / 0.5 / 0.9 —
   center 9% low, edge 29% high.
5. **Cures tested, levels invariant (measured, no tuning):** ε = 1e-9 on the mode-0 diagonal
   only, Mark/Marshak-μ²/collocation half-range families: all give −F⁰²(0) = 2.50424 to 5 dp.
   "Exact-mean removal" (eps + source projection) DESTROYS the level (−F⁰²(0) → 0): the
   eps-diagonal regularization pins the near-null (constant) mode and forces its r-mean to ~0,
   which is not the physical level — the cure is rejected on measurement, not on opinion.
6. **What still passes:** the interior operator (V-checks 1e-13/1e-15: fast matrices == original
   double loop; L(r·μ) identity; P·1 = 1; P·μ = 0), S4 (κ=0 closed form), and the κ=3 Theorem-1
   anchor −F¹⁰(0) = 1.49528 vs ∫rκ dr = 1.5 (0.31%) — the hierarchy bookkeeping and the
   discretization are exact where a known value exists.

**Verdict: the deterministic P_N-Marshak leg now closes S1 (E[D], the Theorem-1 mean, to 0.5%)
and fails S2/S3 with the obstruction re-named precisely: at optical depth τ = κR = 1 the
μ = 0 half-range corner of the boundary layer (E[v²](1, μ<0) ≫ E[v²](1, μ>0) = 0) is not
representable in the P_N-Marshak angular truncation; the error is a 1/L angular tail whose
limit misses E[v²] by ~9% and E[Dv²] by ~47%.  This fires the J00-N1 kill condition ("the
truncation series stalls below the MC reference at the largest affordable L") exactly as
registered.  No number was tuned; the failing values above are the real ones.  Registered
remedy (unchanged): the characteristic/ray-integral solver (ND3), which carries the half-range
data exactly along chords, or a double-P_N treatment of the boundary layer.

**Status line: J04 deterministic leg = S1 LANDED (0.47%), S2/S3 OPEN with named obstruction
(half-range corner at τ=1), S5 fails on F⁰²/F¹²; J01/J02 stand (proof + three-engine MC).**
