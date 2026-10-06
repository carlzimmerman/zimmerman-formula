/-
CFG353 certificates: the turnaround-density estimator rho_est = 3 g^2 / (4 pi G |Phi|).
Units in the obstruction lemmas: phi = Phi / (4 pi G rho_bar), lap phi = delta, rho_est / rho_bar = 3 |grad phi|^2 / |phi|.
-/
import Mathlib

open Real

namespace CFG353

/-- T1: point mass (and a uniform sphere outside): rho_est equals the enclosed mean density. -/
theorem pointmass_identity (G M r : ℝ) (hG : 0 < G) (hM : 0 < M) (hr : 0 < r) :
    3 * (G * M / r ^ 2) ^ 2 / (4 * π * G * |-(G * M / r)|) = 3 * M / (4 * π * r ^ 3) := by
  have h1 : 0 < G * M / r := by positivity
  rw [abs_neg, abs_of_pos h1]
  field_simp

/-- T2: uniform sphere inside: rho_est = rho_bar_sphere * 2 r^2 / (3 R^2 - r^2). -/
theorem sphere_inside_identity (G M R r : ℝ) (hG : 0 < G) (hM : 0 < M) (hR : 0 < R) (hr : 0 ≤ r) (hrR : r ≤ R) :
    3 * (G * M * r / R ^ 3) ^ 2 / (4 * π * G * |-(G * M * (3 * R ^ 2 - r ^ 2) / (2 * R ^ 3))|)
      = (3 * M / (4 * π * R ^ 3)) * (2 * r ^ 2 / (3 * R ^ 2 - r ^ 2)) := by
  have hq : 0 < 3 * R ^ 2 - r ^ 2 := by nlinarith
  have h1 : 0 < G * M * (3 * R ^ 2 - r ^ 2) / (2 * R ^ 3) := by positivity
  rw [abs_neg, abs_of_pos h1]
  field_simp

/-- T3: inside the sphere the estimator never exceeds the true mean (ratio <= 1). -/
theorem sphere_inside_ratio_le_one (R r : ℝ) (hR : 0 < R) (hr : 0 ≤ r) (hrR : r ≤ R) :
    2 * r ^ 2 / (3 * R ^ 2 - r ^ 2) ≤ 1 := by
  have hq : 0 < 3 * R ^ 2 - r ^ 2 := by nlinarith
  rw [div_le_one hq]; nlinarith

/-- T4: the EdS turnaround contrast 9 pi^2/16 exceeds 1 (the overdensity threshold is positive). -/
theorem delta_ta_gt_one : (1 : ℝ) < 9 * π ^ 2 / 16 := by
  have := pi_gt_three; nlinarith

/-- T5: a 3D isotropic void never fires (2 |delta_v| <= 2 < 9 pi^2/16 - 1). -/
theorem void3d_never_fires (dv : ℝ) (_h0 : 0 ≤ dv) (h1 : dv ≤ 1) : 2 * dv < 9 * π ^ 2 / 16 - 1 := by
  have := pi_gt_three; nlinarith

/-- T6: a planar void with |delta_v| = 0.8 fires (6 |delta_v| > 9 pi^2/16 - 1): an E1 false positive. -/
theorem planar_void_fires : 9 * π ^ 2 / 16 - 1 < 6 * (4 / 5 : ℝ) := by
  have h := pi_lt_d2
  have h0 := pi_pos
  nlinarith

/-- T7: near a nondegenerate maximum phi = -k x^2/2, rho_est/rho_bar = 6 k (= 6 |delta|/d when d k = |delta|). -/
theorem near_max_value (k x : ℝ) (hk : 0 < k) (hx : x ≠ 0) :
    3 * (k * x) ^ 2 / |-(k * x ^ 2 / 2)| = 6 * k := by
  have h1 : 0 < k * x ^ 2 / 2 := by positivity
  rw [abs_neg, abs_of_pos h1]
  field_simp
  ring

/-- T8: FRW (phi = 0, grad phi = 0) is OFF under the strict, division-free switch. -/
theorem frw_off (c : ℝ) : ¬ (3 * (0 : ℝ) ^ 2 > c * |(0 : ℝ)|) := by simp

/-- T9 (E0 obstruction): at a regular zero of phi (phi = a x, a != 0) the estimator is unbounded:
for every threshold T there is a point x != 0 where 3 a^2 / |a x| > T. -/
theorem e0_unbounded (a : ℝ) (ha : a ≠ 0) (T : ℝ) : ∃ x : ℝ, x ≠ 0 ∧ T < 3 * a ^ 2 / |a * x| := by
  have hpa : 0 < |a| := abs_pos.mpr ha
  have hT : 0 < |T| + 1 := by positivity
  refine ⟨3 * |a| / (|T| + 1), by positivity, ?_⟩
  have hx : 0 < 3 * |a| / (|T| + 1) := by positivity
  rw [abs_mul, abs_of_pos hx]
  have e : 3 * a ^ 2 / (|a| * (3 * |a| / (|T| + 1))) = |T| + 1 := by
    have : a ^ 2 = |a| ^ 2 := (sq_abs a).symm
    rw [this]; field_simp
  rw [e]; linarith [le_abs_self T]

/-- T10: eta = (G dM/r) / (G dM/r + exterior) <= 1 when the exterior overdensity is non-negative. -/
theorem eta_le_one (a p : ℝ) (ha : 0 < a) (hp : 0 ≤ p) : a / (a + p) ≤ 1 := by
  rw [div_le_one (by linarith)]; linarith

/-- T11: a large-scale potential offset L only suppresses the estimator: 3 g2/(h + L) <= 3 g2 / L. -/
theorem offset_suppression (g2 h L : ℝ) (hg : 0 ≤ g2) (hh : 0 ≤ h) (hL : 0 < L) :
    3 * g2 / (h + L) ≤ 3 * g2 / L := by
  apply div_le_div_of_nonneg_left (by linarith) hL (by linarith)

/-- T12: MUTATE (threshold 0): any nonzero gradient turns the switch ON, whatever phi is. -/
theorem mutate_any_gradient_on (g phi : ℝ) (hg : g ≠ 0) : 0 * |phi| < 3 * g ^ 2 := by
  have : 0 < g ^ 2 := by positivity
  linarith

end CFG353
#print axioms CFG353.pointmass_identity
#print axioms CFG353.sphere_inside_identity
#print axioms CFG353.sphere_inside_ratio_le_one
#print axioms CFG353.delta_ta_gt_one
#print axioms CFG353.void3d_never_fires
#print axioms CFG353.planar_void_fires
#print axioms CFG353.near_max_value
#print axioms CFG353.frw_off
#print axioms CFG353.e0_unbounded
#print axioms CFG353.eta_le_one
#print axioms CFG353.offset_suppression
#print axioms CFG353.mutate_any_gradient_on
