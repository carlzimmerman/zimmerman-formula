/-
  PD18 -- THE WIDE-BINARY FACE: a NEW falsifiable prediction, derived
  from the a0-line's deep branch as algebra, with the Newtonian control
  as the discriminator.

  THE SYSTEM.  A wide binary: total baryonic mass M, separation r, in
  the deep-MOND regime (g << a0, r > r_M = sqrt(G M / a0)).  The
  a0-line's deep branch: g = sqrt(a0 g_N), g_N = G M / r^2.

  T1 wide_binary_plateau  -- the relative velocity is INDEPENDENT of
      separation: v^4 = a0 G M.  The two-body analog of the BTFR: the
      VELOCITY PLATEAU.
  T2 newtonian_control    -- without the a0-line: v^2 r = G M: the
      Newtonian r^{-1/2} decline.
  THE DISCRIMINATOR: the plateau vs the decline -- the relative
  velocity's SCALING with separation discriminates the frameworks
  inside one system, with no mass modeling and no distance ladder
  (the Gaia-class wide-binary samples measure v_rel and r directly).
  SCOPE, refereed: T1 certifies the SCALING EXPONENT (the r-independence)
  -- the falsifier rests on the exponent, which is normalization-
  independent. The two-body AMPLITUDE normalization (vs the test-
  particle convention) is a registered subtlety: flagged, not claimed.

  THE NUMBERS (the Python lane computes; the machine-checked algebra
  certifies the SCALING): for M = 1 M_sun: the crossover
  r_M = sqrt(G M / a0) = 7.95 kAU; the velocity at the crossover
  v = sqrt(a0 r_M) = 0.335 km/s; beyond it the plateau HOLDS while the
  Newtonian prediction declines as r^{-1/2}: at 2 r_M the boost is
  1.41x, at 4 r_M it is 2x.
-/

import Mathlib

set_option linter.unusedVariables false

/-- **T1** -- the wide-binary velocity plateau: from the a0-line's deep
branch, the relative velocity's fourth power is a0 G M -- INDEPENDENT
of the separation. -/
theorem wide_binary_plateau {v g g_N a0 G M r : ℝ}
    (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) (hr : 0 < r)
    (hgN : g_N = G * M / r ^ 2)
    (hdeep : g = Real.sqrt (a0 * g_N))
    (hv : v ^ 2 = g * r) :
    v ^ 4 = a0 * G * M := by
  have hgNpos : 0 < g_N := by
    rw [hgN]
    exact div_pos (mul_pos hG hM) (pow_pos (by linarith) 2)
  have hgsq : g ^ 2 = a0 * g_N := by
    rw [hdeep, pow_two, Real.mul_self_sqrt (le_of_lt (mul_pos ha0 hgNpos))]
  have h5 : v ^ 4 = (v ^ 2) ^ 2 := by ring
  have h6 : (v ^ 2) ^ 2 = g ^ 2 * r ^ 2 := by
    rw [hv, mul_pow]
  rw [h5, h6, hgsq, hgN]
  field_simp [hr.ne]

/-- **T2** -- the Newtonian control: without the a0-line, the relative
velocity DECLINES as r^{-1/2}: the scaling invariant v^2 r = G M. -/
theorem newtonian_control {v g G M r : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hr : 0 < r)
    (hg : g = G * M / r ^ 2)
    (hv : v ^ 2 = g * r) :
    v ^ 2 * r = G * M := by
  rw [hv, hg]
  field_simp [hr.ne]
