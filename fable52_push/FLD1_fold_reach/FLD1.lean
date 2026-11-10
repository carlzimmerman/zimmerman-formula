/-
FLD1: Lean statements for the closed forms the lane uses. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  share_of_radius     : x^2 = X (X + 1) inverts to X = [-1 + sqrt(1 + 4 x^2)]/2 (X >= 0): PD1's cap radius and X_fold.
  halo_mass_law       : the law's halo mass over M_b at x = r/r_M is [-1 + sqrt(1 + 4 x^2)]/2 (point mass).
  window_radius_mono  : R = sqrt(G M/g) falls as g rises (KiDS g_bar bins -> radii).
  kepler_energy       : the radial cycloid r = q (1 + cos e)/2, t = k (e + sin e), k^2 = q^3/(8 G M) has energy -G M/q (KA2).
-/
import Mathlib

namespace FLD1

theorem share_of_radius (X : ℝ) (hX : 0 ≤ X) : (-1 + Real.sqrt (1 + 4 * (X * (X + 1)))) / 2 = X := by
  have h : 1 + 4 * (X * (X + 1)) = (2 * X + 1) ^ 2 := by ring
  rw [h, Real.sqrt_sq (by linarith)]
  ring

theorem halo_mass_law (x : ℝ) (hx : 0 < x) :
    x ^ 2 * ((1 / x ^ 2 + Real.sqrt (1 / x ^ 4 + 4 / x ^ 2)) / 2 - 1 / x ^ 2) = (-1 + Real.sqrt (1 + 4 * x ^ 2)) / 2 := by
  have hx2 : 0 < x ^ 2 := by positivity
  have e : 1 / x ^ 4 + 4 / x ^ 2 = (1 + 4 * x ^ 2) / (x ^ 2) ^ 2 := by
    field_simp
  have hs : Real.sqrt (1 / x ^ 4 + 4 / x ^ 2) = Real.sqrt (1 + 4 * x ^ 2) / x ^ 2 := by
    rw [e, Real.sqrt_div (by positivity), Real.sqrt_sq hx2.le]
  rw [hs]
  field_simp
  ring

theorem window_radius_mono (GM g1 g2 : ℝ) (hGM : 0 < GM) (h1 : 0 < g1) (h12 : g1 < g2) :
    Real.sqrt (GM / g2) < Real.sqrt (GM / g1) := by
  have hg2 : 0 < g2 := by linarith
  apply Real.sqrt_lt_sqrt (div_nonneg hGM.le hg2.le)
  exact div_lt_div_of_pos_left hGM h1 h12

theorem kepler_energy (G M q k2 c s : ℝ) (hGM : G * M ≠ 0) (hq : q ≠ 0) (hc : 1 + c ≠ 0)
    (hk : k2 = q ^ 3 / (8 * (G * M))) (hs : s ^ 2 = 1 - c ^ 2) :
    (q ^ 2 * s ^ 2 / (4 * k2 * (1 + c) ^ 2)) / 2 - 2 * (G * M) / (q * (1 + c)) = -(G * M) / q := by
  subst hk
  rw [hs]
  have h1 : 1 - c ^ 2 = (1 - c) * (1 + c) := by ring
  rw [h1]
  field_simp
  ring

end FLD1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
