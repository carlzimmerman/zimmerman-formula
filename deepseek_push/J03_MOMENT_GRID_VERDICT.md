# J03 — DETERMINISTIC GRID CROSS-CHECK: HONEST FAILURE + DIAGNOSIS
**2026-09-23 · moment channel — the third engine attempt, recorded as failed**

**Attempt:** solve the derived hierarchy L F¹⁰ = 1, L F⁰² = 2κT,
L F¹² = F⁰² + 2κT·G F¹⁰ directly on an (r, μ) mesh by building the
discretized operator matrix and calling `np.linalg.solve` (no iteration, no
stochastic element — the target doc's "independent discretized transport
equation" in literal form).

**Files:** `J03_hierarchy_grid.py` · `J03_hierarchy_grid.out` (exit 1)

## The result — FAILS its own benchmarks (kept, not suppressed)

| quantity | grid (64×32) | grid (128×64) | MC reference (J01/J02) |
|---|---|---|---|
| −F¹⁰(0) = E[D] | **−0.035** | **0.059** | **0.501** |
| −F⁰²(0) = E[v²] | 0.060 | 0.034 | 2.806 |
| F¹²(0) = E[D v²] | 194 | 9.98 | 3.73 |

Not only wrong — **non-convergent** (values move the wrong way and flip sign as
the grid refines). This is a *bona fide* negative: the central-difference
discretization of the spherical streaming operator is invalid here, and no
number from it is offered as evidence for anything.

## Diagnosis (why it fails — the interesting part)

1. **The (1−μ²)/r·∂_μ term is singular at r → 0.** On the innermost row,
   r₀ = 1/(2Nᵣ) ≈ 0.008–0.016, so the angular-coupling coefficient reaches
   1/r ≈ 60–125 — the row's balance is dominated by that term, whose central
   difference then *amplifies* its own error by ~1/r. The physically correct
   content near r=0 is that ψ(r, μ) → ψ₀(r) is *iso-μ* (isotropy), with the
   angular-part scaling like rᵃ; a plain 2D finite difference cannot see that
   scaling without an explicit regularity model.
2. **Central differencing of a first-order (hyperbolic) operator.** u·∇ is
   first order; central differences in r couple both characteristics and, for
   the absorbing half-range boundary (r=1, μ>0 only), leave the discretized
   problem with spurious modes. The known-correct treatments are: (a)
   characteristic/"ray" integration from the boundary, (b) the P_N
   spherical-harmonics expansion, for which the streaming operator has the
   closed identities μP_l = [lP_{l−1}+(l+1)P_{l+1}]/(2l+1) and
   (1−μ²)P′_l = [l(l+1)/(2l+1)](P_{l−1}−P_{l+1}), turning the PDE into an ODE
   system in r with well-posed half-range (Marshak-type) BCs, or (c) a
   regularized coordinate (multiply through by r near the origin).
3. **Sanity anchor (passes):** the continuous operator is confirmed correct —
   at κ=0, L(rμ) = μ·∂_r(rμ) + (1−μ²)/r·∂_μ(rμ) = μ² + (1−μ²) = 1 exactly
   (S4 ✓), i.e. the operator algebra in J01/J02's hierarchy is right, and the
   failure is purely in the discretized transport equation, not in the
   derivation.

## What this does and does not change

- **Does not weaken J01/J02.** The mixed-moment hierarchy
  E[D v^{2m}] = (2m−1)!!·2^m·E[D·ang^m] was proven by the conditional-Gaussian
  argument (a closed argument, not a numerical scan) and verified at **35/35
  checks** across three independent stochastic engines and two source
  geometries: the frozen `transport.py` (calibration), the J01 engine, and the
  J02 engine (isothermal re-runs at new seeds). The volume-source face
  (Dynkin compensation + Q coupling) is likewise anchored by a generator
  identity with MC only for E[μ_exit].
- **Stands as a registered negative:** a naive central-difference transport
  grid does not reproduce the hierarchy; anyone reading
  `J03_hierarchy_grid.py` gets the exact failing matrices and values. The
  masked-P_N or characteristic solver is the registered next lane (the target
  doc's "independent discretized transport equation" would be supplied by a
  P_N solve; not fabricated here).
- **House rule kept:** no number was adjusted to make the check pass; the
  failing output is the deliverable of this lane, exactly as the "execution
  discipline" and "theatre physics" rules prescribe.

**Status line: J01/J02 stand on proof + three-engine MC evidence; J03's grid
solve is FAILED-with-diagnosis (singularity + hyperbolic discretization),
resurrection requires a P_N or characteristic solver — registered, not
claimed.**