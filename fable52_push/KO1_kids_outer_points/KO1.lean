/-
KO1 (criteria b1b91fae33): Lean statements for the two-phase exterior against the law. They certify the algebra and the
inequalities used by the lane's model, not the physics and not the data. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

Setting. By SWT1 T1 a law-on region shows exactly M_b from outside. With a swept share X M_b at the wall, the mass inside a
projected radius R beyond the wall is (1 + X) M_b, the surface density at R is zero, and the lensing estimator reads
4 G DeltaSigma = 4 G (1 + X) M_b / (pi R^2). The law's own field at the same radius is nu(y) g_N with g_N = G M_b / R^2 and
y = g_N / a0. Their ratio is c / nu(y) with c = (4 / pi)(1 + X).

  lens_point_mass      : 4 G M / (pi R^2) = (4 / pi) (G M / R^2).
  exterior_over_law    : the ratio of the two-phase exterior to the law is c / nu(y), c = (4 / pi)(1 + X).
  nu_strictAnti        : nu is strictly decreasing on y > 0.
  nu_gt_iff            : for c > 1, c < nu(y) iff y < 1 / (c (c - 1)).
  ratio_lt_one_iff     : for c > 1, c / nu(y) < 1 iff y < 1 / (c (c - 1)): below that acceleration the exterior is under the law.
  ratio_strictMono     : c / nu(y) increases with y: the exterior falls further under the law toward low acceleration.
  nu_mul_sqrt_ge_one   : nu(y) sqrt(y) >= 1.
  ratio_le_sqrt        : c / nu(y) <= c sqrt(y).
  corr_factor_ge_one   : the mass-scatter correction 10^(e/2) is at least 1 for e >= 0 (it can only raise the amplitude).
  u_scale_le, u_scale_ge : for enclosed mass k >= 1 times the model's, the law's field obeys sqrt(k) u(y) <= u(k y) <= k u(y):
                         the amplitude against a fixed-mass model lies between sqrt(k) and k (the law's floor for the shape ratio).
  shell_unsupported_iff: a shell of X M_b cannot rest on the wall inside (3/2) X (1 + X/2) r_M (deep regime).
-/
import Mathlib

namespace KO1

noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)

theorem nu_gt_one (y : ℝ) (hy : 0 < y) : 1 < nu y := by
  unfold nu
  have h1 : (1 / 2 : ℝ) = Real.sqrt (1 / 4) := by
    rw [show (1 / 4 : ℝ) = (1 / 2) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have h2 : Real.sqrt (1 / 4) < Real.sqrt (1 / 4 + 1 / y) := by
    apply Real.sqrt_lt_sqrt (by norm_num)
    have : 0 < 1 / y := by positivity
    linarith
  linarith

theorem nu_pos (y : ℝ) (hy : 0 < y) : 0 < nu y := lt_trans one_pos (nu_gt_one y hy)

/-- the lensing estimator of a mass M wholly inside the projected radius R. -/
theorem lens_point_mass (G M R : ℝ) (hR : 0 < R) :
    4 * G * (M / (Real.pi * R ^ 2)) = 4 / Real.pi * (G * M / R ^ 2) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  field_simp

/-- the two-phase exterior over the law's own field at the same radius. -/
theorem exterior_over_law (G Mb a0 R X : ℝ) (hG : 0 < G) (hM : 0 < Mb) (ha : 0 < a0) (hR : 0 < R) :
    4 * G * ((1 + X) * Mb / (Real.pi * R ^ 2)) / (nu (G * Mb / R ^ 2 / a0) * (G * Mb / R ^ 2))
      = 4 / Real.pi * (1 + X) / nu (G * Mb / R ^ 2 / a0) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hy : 0 < G * Mb / R ^ 2 / a0 := by positivity
  have hnu : 0 < nu (G * Mb / R ^ 2 / a0) := nu_pos _ hy
  field_simp

theorem nu_strictAnti (y₁ y₂ : ℝ) (h1 : 0 < y₁) (h12 : y₁ < y₂) : nu y₂ < nu y₁ := by
  unfold nu
  have h2 : 0 < y₂ := lt_trans h1 h12
  have hinv : 1 / y₂ < 1 / y₁ := one_div_lt_one_div_of_lt h1 h12
  have h0 : (0 : ℝ) ≤ 1 / 4 + 1 / y₂ := by positivity
  have hs : Real.sqrt (1 / 4 + 1 / y₂) < Real.sqrt (1 / 4 + 1 / y₁) :=
    Real.sqrt_lt_sqrt h0 (by linarith)
  linarith

theorem nu_gt_iff (c y : ℝ) (hc : 1 < c) (hy : 0 < y) : c < nu y ↔ y < 1 / (c * (c - 1)) := by
  unfold nu
  have hK : 0 < c * (c - 1) := mul_pos (by linarith) (by linarith)
  have hc2 : (0 : ℝ) ≤ c - 1 / 2 := by linarith
  have hstep : c < 1 / 2 + Real.sqrt (1 / 4 + 1 / y) ↔ (c - 1 / 2) ^ 2 < 1 / 4 + 1 / y := by
    rw [← Real.lt_sqrt hc2]
    constructor <;> intro h <;> linarith
  rw [hstep]
  have hyK : 0 < y * (c * (c - 1)) := mul_pos hy hK
  constructor
  · intro h
    have h1 : c * (c - 1) < 1 / y := by nlinarith
    have h2 : c * (c - 1) * y < 1 := by
      have h3 := mul_lt_mul_of_pos_right h1 hy
      have h4 : 1 / y * y = 1 := by field_simp
      linarith
    rw [lt_div_iff₀ hK]
    linarith
  · intro h
    have h2 : y * (c * (c - 1)) < 1 := by
      rw [lt_div_iff₀ hK] at h
      exact h
    have h1 : c * (c - 1) < 1 / y := by
      rw [lt_div_iff₀ hy]
      linarith
    nlinarith

theorem ratio_lt_one_iff (c y : ℝ) (hc : 1 < c) (hy : 0 < y) : c / nu y < 1 ↔ y < 1 / (c * (c - 1)) := by
  rw [div_lt_one (nu_pos y hy)]
  exact nu_gt_iff c y hc hy

theorem ratio_strictMono (c y₁ y₂ : ℝ) (hc : 0 < c) (h1 : 0 < y₁) (h12 : y₁ < y₂) : c / nu y₁ < c / nu y₂ := by
  have h2 : 0 < y₂ := lt_trans h1 h12
  exact div_lt_div_of_pos_left hc (nu_pos y₂ h2) (nu_strictAnti y₁ y₂ h1 h12)

theorem nu_mul_sqrt_ge_one (y : ℝ) (hy : 0 < y) : 1 ≤ nu y * Real.sqrt y := by
  unfold nu
  have hsy : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have h1 : Real.sqrt (1 / y) ≤ Real.sqrt (1 / 4 + 1 / y) := Real.sqrt_le_sqrt (by linarith)
  have h2 : Real.sqrt (1 / y) * Real.sqrt y = 1 := by
    rw [← Real.sqrt_mul (by positivity) y]
    have : 1 / y * y = 1 := by field_simp
    rw [this, Real.sqrt_one]
  have h3 : Real.sqrt (1 / y) * Real.sqrt y ≤ Real.sqrt (1 / 4 + 1 / y) * Real.sqrt y :=
    mul_le_mul_of_nonneg_right h1 hsy.le
  nlinarith

theorem ratio_le_sqrt (c y : ℝ) (hc : 0 ≤ c) (hy : 0 < y) : c / nu y ≤ c * Real.sqrt y := by
  have hnu : 0 < nu y := nu_pos y hy
  rw [div_le_iff₀ hnu]
  have h := nu_mul_sqrt_ge_one y hy
  nlinarith [mul_le_mul_of_nonneg_left h hc]

theorem corr_factor_ge_one (e : ℝ) (he : 0 ≤ e) : (1 : ℝ) ≤ (10 : ℝ) ^ (e / 2) :=
  Real.one_le_rpow (by norm_num) (by linarith)

/-- u(y) = nu(y) y, the law's field in units of a0 for a displacement y. -/
noncomputable def u (y : ℝ) : ℝ := y / 2 + Real.sqrt (y ^ 2 / 4 + y)

/-- enclosed mass k times larger raises the law's field by at most k ... -/
theorem u_scale_le (k y : ℝ) (hk : 1 ≤ k) (hy : 0 < y) : u (k * y) ≤ k * u y := by
  unfold u
  have hk0 : 0 ≤ k := by linarith
  have h1 : Real.sqrt ((k * y) ^ 2 / 4 + k * y) ≤ Real.sqrt (k ^ 2 * (y ^ 2 / 4 + y)) := by
    apply Real.sqrt_le_sqrt
    nlinarith [mul_nonneg (mul_nonneg hk0 (sub_nonneg.mpr hk)) hy.le]
  have h2 : Real.sqrt (k ^ 2 * (y ^ 2 / 4 + y)) = k * Real.sqrt (y ^ 2 / 4 + y) := by
    rw [Real.sqrt_mul (sq_nonneg k), Real.sqrt_sq hk0]
  rw [h2] at h1
  linarith

/-- ... and by at least sqrt(k): so against a fixed-mass model the law's amplitude lies between sqrt(k) and k. -/
theorem u_scale_ge (k y : ℝ) (hk : 1 ≤ k) (hy : 0 < y) : Real.sqrt k * u y ≤ u (k * y) := by
  unfold u
  have hk0 : 0 ≤ k := by linarith
  have hsk : Real.sqrt k ≤ k := by
    rw [Real.sqrt_le_left hk0]
    nlinarith
  have h1 : Real.sqrt (k * (y ^ 2 / 4 + y)) ≤ Real.sqrt ((k * y) ^ 2 / 4 + k * y) := by
    apply Real.sqrt_le_sqrt
    nlinarith [mul_nonneg (mul_nonneg hk0 (sub_nonneg.mpr hk)) (sq_nonneg y)]
  have h2 : Real.sqrt (k * (y ^ 2 / 4 + y)) = Real.sqrt k * Real.sqrt (y ^ 2 / 4 + y) := Real.sqrt_mul hk0 _
  rw [h2] at h1
  have h3 : Real.sqrt k * (y / 2) ≤ k * y / 2 := by nlinarith
  nlinarith

/-- A shell of mass X M_b at the wall. In units of a0 M_b its weight is y X (1 + X / 2) and, in the deep regime, the wall
force is at most (2/3) sqrt(y) (SWT1 W_le_deep). The wall cannot carry the shell exactly when sqrt(y) exceeds
2 / (3 X (1 + X / 2)), that is inside the radius (3/2) X (1 + X / 2) r_M. -/
theorem shell_unsupported_iff (X y : ℝ) (hX : 0 < X) (hy : 0 < y) :
    2 / 3 * Real.sqrt y < y * (X * (1 + X / 2)) ↔ 2 / (3 * (X * (1 + X / 2))) < Real.sqrt y := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have hK : 0 < X * (1 + X / 2) := by positivity
  have hsq : Real.sqrt y * Real.sqrt y = y := Real.mul_self_sqrt hy.le
  rw [div_lt_iff₀ (by positivity)]
  constructor
  · intro h
    have h1 : 2 / 3 * Real.sqrt y < Real.sqrt y * Real.sqrt y * (X * (1 + X / 2)) := by rw [hsq]; exact h
    have h2 : 2 / 3 < Real.sqrt y * (X * (1 + X / 2)) := by
      by_contra hc
      have hc' := not_lt.mp hc
      have := mul_le_mul_of_nonneg_left hc' hs.le
      nlinarith
    nlinarith
  · intro h
    have h2 : 2 / 3 < Real.sqrt y * (X * (1 + X / 2)) := by nlinarith
    have h3 := mul_lt_mul_of_pos_left h2 hs
    nlinarith

end KO1

#print axioms KO1.lens_point_mass
#print axioms KO1.exterior_over_law
#print axioms KO1.nu_strictAnti
#print axioms KO1.nu_gt_iff
#print axioms KO1.ratio_lt_one_iff
#print axioms KO1.ratio_strictMono
#print axioms KO1.nu_mul_sqrt_ge_one
#print axioms KO1.ratio_le_sqrt
#print axioms KO1.corr_factor_ge_one
#print axioms KO1.u_scale_le
#print axioms KO1.u_scale_ge
#print axioms KO1.shell_unsupported_iff
