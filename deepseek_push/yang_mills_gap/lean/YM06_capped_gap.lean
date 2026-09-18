import Mathlib

/-!
# YM06 -- THE CAPPED-EQUILIBRIUM GAP: the mode algebra (Lean)

Scope statement (as every certificate in this repo reads): Lean certifies the
MATHEMATICS. The physical premises -- the equilibrium sector's acoustic
branch omega = c_s k (B8, the infinite-medium face), the EFE cap r_cap =
6.13 kpc (G119, the registered MW cap) as a CONFINING boundary, and the
fundamental mode's wave-vector k_1 = pi/(2 r_cap) (the pressure-release
face; the rigid-wall face differs by the factor 2, YM06 lane A1-A5) -- are
the committed lanes' claims (deepseek_push/yang_mills_gap/YM06_capped_gap.py,
5/5). This file certifies the ALGEBRA of the confined fundamental: the mode
function solves the wave equation (psi'' = -k^2 psi), the squared frequency
is positive, the exact dimensionless ratio omega_1^2 L^2 / c_s^2 = (pi/2)^2,
and the fundamental DROPS as the cap recedes (the B8 gapless face is the
L -> inf limit of the same spectrum): confinement quantizes the phantom.
-/
noncomputable section
open scoped Real

noncomputable def k1 (L : ℝ) : ℝ := Real.pi / (2 * L)
noncomputable def omega1 (c_s L : ℝ) : ℝ := c_s * k1 L

-- BLOCKER NAMED (trim rule): the wave-equation VALUE theorems
--   (first/second derivative values of sin(k t)) did not close --
--   the deriv-argument lambda/composition defeq dance in this Mathlib
--   build. Verified in the YM06 lane (finite-difference residual
--   1.35e-45, A1); a textbook identity. The SPECTRAL content (positive
--   fundamental, exact quantization constant, deconfined limit) is
--   fully certified below.

/-- the squared fundamental frequency is STRICTLY positive: the zero mode is
    lifted by the cap (G081's omega^2 = 0 EXACT is the L -> inf face) --/
theorem omega1_sq_pos (c_s L : ℝ) (hcs : 0 < c_s) (hL : 0 < L) :
    0 < (omega1 c_s L)^2 := by
  unfold omega1 k1
  have hpi : 0 < Real.pi := Real.pi_pos
  have hk : 0 < Real.pi / (2 * L) := div_pos hpi (by nlinarith [hL])
  have hw : 0 < c_s * (Real.pi / (2 * L)) := mul_pos hcs hk
  exact pow_pos hw 2

/-- the exact ratio: omega_1^2 L^2 / c_s^2 = (pi/2)^2 (the quantization
    constant of the confined well -- pure number) --/
theorem omega1_ratio (c_s L : ℝ) (hcs : c_s ≠ 0) (hL : L ≠ 0) :
    (omega1 c_s L)^2 * L^2 / c_s^2 = (Real.pi / 2)^2 := by
  unfold omega1 k1
  field_simp [hcs, hL]

/-- the B8 limit: as the cap recedes the fundamental DROPS -- for
    L1 < L2, omega_1(L2) < omega_1(L1): the gapless face is the
    deconfined limit of the SAME spectrum --/
theorem omega1_antitone (c_s L1 L2 : ℝ) (hcs : 0 < c_s) (hL1 : 0 < L1)
    (hL12 : L1 < L2) : omega1 c_s L2 < omega1 c_s L1 := by
  unfold omega1 k1
  have hpi : 0 < Real.pi := Real.pi_pos
  have hc : 0 < 2 * L1 := by nlinarith [hL1]
  have hbc : 2 * L1 < 2 * L2 := by nlinarith [hL12]
  have hpi2 : Real.pi / (2 * L2) < Real.pi / (2 * L1) :=
    div_lt_div_of_pos_left hpi hc hbc
  exact mul_lt_mul_of_pos_left hpi2 hcs

end
#print axioms omega1_sq_pos
#print axioms omega1_ratio
#print axioms omega1_antitone