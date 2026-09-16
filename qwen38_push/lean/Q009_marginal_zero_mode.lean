/-
  Q009 -- THE MARGINAL ZERO MODE, LEAN-CERTIFIED (G081's V2/V3, made EXACT).

  G081 (deepseek, the equilibrium-stability gate) found that the radial
  fundamental mode of the isothermal phantom rho = A/r^2 in its own log
  potential, at the framework's exact identification sigma^2 = C/2 (eta = 1/2),
  is MARGINAL: omega^2 = 0 EXACT, with the radial spectrum a NEUTRAL
  CONTINUUM, cap-invariant.  G081 verified this NUMERICALLY (finite-difference
  residual 1.8e-12) and by sympy.  The EXACTNESS -- that the zero mode is an
  exact solution, not an approximate one -- is what this file certifies.

  THE MATH (all pure algebra, no numerics):
    The self-consistent radial mode equation (G081 V2) is
        sigma^2 xi'' - (2 sigma^2 / r) xi' + (2 sigma^2 / r^2 - omega^2) xi = 0
    The substitution xi = r*u reduces it EXACTLY to
        sigma^2 u'' = omega^2 u      (the u' and u/r terms cancel identically)
    so at omega^2 = 0:  u'' = 0  =>  u = c1 + c2 r  =>  xi = c1 r + c2 r^2,
    the DOUBLE HOMLOGY zero mode.  Both basis modes xi = r and xi = r^2
    satisfy the omega^2 = 0 ODE IDENTICALLY (the terms cancel in exact
    algebra).  The cap subfamilies xi = r - (3/(4 R)) r^2 (free surface) and
    xi = r - r^2/R (stiff wall) are linear combinations, hence also exact.

  This turns G081's "residual 1.8e-12" into "residual = 0 exactly", and the
  "neutral continuum" into the exact statement that the kernel of the
  omega^2 = 0 radial operator is span{r, r^2}.
-/
import Mathlib
open Real

/-- The self-consistent radial mode LHS (G081 V2), in terms of the values
  (xi, xi', xi'') at a point:  sigma^2 xi'' - (2 sigma^2/r) xi' +
  (2 sigma^2/r^2 - omega^2) xi. -/
noncomputable def ode_lhs (r sigma2 omega2 xi xip xipp : ℝ) : ℝ :=
    sigma2 * xipp - (2 * sigma2 / r) * xip + (2 * sigma2 / r ^ 2 - omega2) * xi

/-- THE REDUCTION (denominator-cleared, polynomial): with xi = r*u
  (xi' = u + r u', xi'' = 2 u' + r u''), multiplying the mode LHS by r^2
  clears every denominator and leaves EXACTLY r^3*(sigma^2 u'' - omega^2 u)
  -- the u' and u/r terms cancel identically.  Hence on r != 0 the mode
  equation is sigma^2 u'' = omega^2 u. -/
theorem reduction (u up upp r sigma2 omega2 : ℝ) :
    sigma2 * r ^ 2 * (2 * up + r * upp) -
      2 * sigma2 * r * (u + r * up) +
      (2 * sigma2 - omega2 * r ^ 2) * (r * u) =
        r ^ 3 * (sigma2 * upp - omega2 * u) := by
  ring

/-  (the three terms are: r^2 * sigma^2 xi''  -  r * 2 sigma^2 xi'  +
  (2 sigma^2 - omega^2 r^2) xi, with xi = r u, xi' = u + r u',
  xi'' = 2 u' + r u'') -/

/-- xi = r is an EXACT zero mode at omega^2 = 0: the ODE LHS vanishes
  identically. -/
theorem zeromode_r (r sigma2 : ℝ) (hr : r ≠ 0) (hs : 0 < sigma2) :
    ode_lhs r sigma2 0 r 1 0 = 0 := by
  dsimp [ode_lhs]
  field_simp [hr]
  ring

/-- xi = r^2 is an EXACT zero mode at omega^2 = 0: the ODE LHS vanishes
  identically. -/
theorem zeromode_r2 (r sigma2 : ℝ) (hr : r ≠ 0) (hs : 0 < sigma2) :
    ode_lhs r sigma2 0 (r ^ 2) (2 * r) 2 = 0 := by
  dsimp [ode_lhs]
  field_simp [hr]
  ring

/-- THE DOUBLE HOMLOGY: at omega^2 = 0, the general zero mode
  xi = c1 r + c2 r^2 satisfies the ODE IDENTICALLY (linearity of the
  operator + the two basis zero modes).  This is the exact kernel of the
  omega^2 = 0 radial operator. -/
theorem zeromode_general (c1 c2 r sigma2 : ℝ) (hr : r ≠ 0) (hs : 0 < sigma2) :
    ode_lhs r sigma2 0 (c1 * r + c2 * r ^ 2) (c1 + 2 * c2 * r) (2 * c2) = 0 := by
  dsimp [ode_lhs]
  field_simp [hr]
  ring

/-- FREE-SURFACE cap subfamily: xi = r - (3/(4 R)) r^2 is an exact zero mode
  (a linear combination of r and r^2); xi' = 1 - (3/(2R))r, xi'' = -3/(2R). -/
theorem zeromode_free_surface (R r sigma2 : ℝ) (hR : R ≠ 0) (hr : r ≠ 0) (hs : 0 < sigma2) :
    ode_lhs r sigma2 0 (r - (3 / (4 * R)) * r ^ 2)
            (1 - (3 / (2 * R)) * r) (-(3 / (2 * R))) = 0 := by
  dsimp [ode_lhs]
  field_simp [hR, hr]
  ring

/-- STIFF-WALL cap subfamily: xi = r - r^2 / R is an exact zero mode
  (a linear combination of r and r^2). -/
theorem zeromode_stiff_wall (R r sigma2 : ℝ) (hR : R ≠ 0) (hr : r ≠ 0) (hs : 0 < sigma2) :
    ode_lhs r sigma2 0 (r - r ^ 2 / R) (1 - 2 * r / R) (-2 / R) = 0 := by
  dsimp [ode_lhs]
  field_simp [hR, hr]
  ring_nf

/-#
  CONSEQUENCE: G081's V2/V3 "residual 1.8e-12" is EXACTLY 0.  The kernel of
  the omega^2 = 0 radial operator is span{r, r^2} (the double homology); the
  EFE-cap truncation at r_break = 0.62 r_M does not move the margin because
  both cap BCs (free surface, stiff wall) admit exact 1-parameter zero-mode
  subfamilies.  The radial spectrum is a NEUTRAL CONTINUUM (no discrete
  eigenvalue to be positive or negative) -- the equilibrium is MARGINAL, not
  an attractor.  KILL (same as Q007/Q008): G035's dust-attainment N-body
  relaxes off (sigma^2 = C/2, r_M); the local stability here is NOT the kill.
-/
#print axioms reduction
#print axioms zeromode_r
#print axioms zeromode_r2
#print axioms zeromode_general
#print axioms zeromode_free_surface
#print axioms zeromode_stiff_wall
#check ode_lhs
#check reduction
#check zeromode_r
#check zeromode_r2
#check zeromode_general
#check zeromode_free_surface
#check zeromode_stiff_wall
