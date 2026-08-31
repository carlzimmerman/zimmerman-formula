# CONVERGENCE.md

The decisive object is an **exact closed-form** dispersion `ω²=V(k)/A` (sympy, no discretization),
so "convergence" here means invariance under (a) independent derivation route, (b) k-range,
(c) grid refinement, (d) background inversion tolerance, plus the symbolic consistency limits.

## (a) Independent-route agreement — machine precision
Route I (Hermitian Schur complement, this run) vs Route II (EL-determinant `−D0/D1` from the
pre-existing `wf_adm_scalar_reduction.py`, `β_script=−β`): ω²(kx,kz) agrees to
**rel.diff ≤ 1.5e-16** at all sampled (kx,kz,y0,β,λ). (`phase5_numeric_dispersion.out`)

## (b) k-range (Phase 8, `phase78_robustness.out`)
`c²_par = ω²/kz²` at y0=2 over **15 decades** k∈[1e1,1e15] a0 is flat and negative,
converged to −4.188246e-3 by k~1e3 a0. The instability is a genuine k-independent gradient
`B2<0`, not a finite-k or numerical-band artifact.

## (c) Grid refinement (Phase 7)
`min_y c²_par` over the transition window with y0-grids at 1×/2×/4×/8× (N=200→1600):
identical to 6+ digits; fraction of the window that is unstable = 1.000 at every resolution.

## (d) Background inversion (Phase 3, `phase3_background.out`)
`μ_phys(y)·y = g_N/a0` inverted by bracketed root find; residual `max|μy−g_N/a0| = 1.15e-14`
over g_N∈[1e-3,1e3]a0. Point-mass and Plummer sources both traverse the unstable shell.

## (e) Symbolic consistency limits (guards against a spurious result)
- Pure-quadratic f=αa² ⇒ c²_par=c²_perp=**BB Eq.(14)** exactly, y0-independent, m²=0.
- High-a ⇒ BB c_s²; c_T²=1/(1−β). Deep-MOND (y0<1) ⇒ c²_par>0.
- Transverse c²_perp>0 for all y0. Flat machinery matches BB Eq.(14) exactly
  (`../khronometric_mond/wf_flat_validation.py`).
- Kinetic A=(1−β)(2+β+3λ)/(β+λ) matches the MISSION-seed shift-elimination formula.

## (f) Parameter-grid completeness (Phase 6, `PARAMETER_SCAN.*`)
42 points, β∈{1e-18…1e-12}×λ∈{1e-7…1e-1}, α=2β: `min_y c²_par<0` on **all 42**. The sign is
proven β,λ-independent analytically (sign c²_par = sign f''), so the grid is confirmatory, not
the basis of the claim.

## Angle robustness
At y0=2, c²(θ)<0 for a finite cone θ∈[0°,~44°) about the radial direction (the fastest-growing
modes are radial-wavevector); c²>0 for near-tangential θ. A pole (D_lapse=0) sits at θ≈45°.

## Not refined (honest scope)
- The frozen-local background is a leading-order (principal-symbol) treatment; background-gradient
  corrections are O(1/(k L_bg))≪1 in the validity band and do not affect the sign of the k²
  coefficient. A fully inhomogeneous mode solve on a global a(r) profile was not performed
  (unnecessary: the instability is a local function of y0 and every profile occupies the window).
- L4/L6 Hořava terms were treated analytically (they regulate only k≳M_*), not added to the
  action; they cannot cure a k-independent 2-derivative B2<0.
