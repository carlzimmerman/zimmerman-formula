import Mathlib

/-!
# QX4_udg -- algebra behind QX4 (closure_2026_11_06/QX4_udg)

1. `mu_nu_inverse`: the action's AQUAL function mu(x) = x/(1+x) inverts the law's nu(y) = 1/2 + sqrt(1/4 + 1/y).
   If x = y nu(y), then x mu(x) = y. So the exact AQUAL solve (iteration 1) and the algebraic law use the same
   function, and in spherical symmetry they agree exactly (K1).
2. `host_mass_lower`: the EFE host bound of iteration 2. A host of baryonic mass M at distance d, in its deep-MOND
   region (g_e = sqrt(G M a0)/d), whose tidal pull across radius R stays below the disc's own g_int
   (g_e R / d < g_int), must have M > g_e^4 R^2 / (G a0 g_int^2).
3. `nu_ge_one`: nu(y) >= 1, so the law can only raise V above Newton (the sign used in iteration 3).

Kappa = 1/2 FITTED; not theory closed.
-/

namespace QX4

noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)

theorem mu_nu_inverse (y : ℝ) (hy : 0 < y) :
    let x := y * nu y
    x * (x / (1 + x)) = y := by
  intro x
  have hs2 : Real.sqrt (1 / 4 + 1 / y) ^ 2 = 1 / 4 + 1 / y := Real.sq_sqrt (by positivity)
  have hs0 : 0 ≤ Real.sqrt (1 / 4 + 1 / y) := Real.sqrt_nonneg _
  have key : y * Real.sqrt (1 / 4 + 1 / y) ^ 2 = y / 4 + 1 := by
    rw [hs2]; field_simp
  have hx : 0 < 1 + x := by
    have : 0 ≤ x := by
      show 0 ≤ y * nu y
      unfold nu; positivity
    linarith
  rw [mul_div_assoc', div_eq_iff (ne_of_gt hx)]
  show y * nu y * (y * nu y) = y * (1 + y * nu y)
  unfold nu
  linear_combination y * key

theorem host_mass_lower (ge d R gint G a0 M : ℝ) (hge : 0 < ge) (hd : 0 < d) (hR : 0 < R) (hgint : 0 < gint)
    (hG : 0 < G) (ha0 : 0 < a0) (hM : 0 < M)
    (hfield : ge = Real.sqrt (G * M * a0) / d) (htidal : ge * R / d < gint) :
    ge ^ 4 * R ^ 2 / (G * a0 * gint ^ 2) < M := by
  have h1 : (ge * d) ^ 2 = G * M * a0 := by
    rw [hfield, div_mul_cancel₀ _ (ne_of_gt hd)]; exact Real.sq_sqrt (by positivity)
  have h2 : ge * R < gint * d := (div_lt_iff₀ hd).mp htidal
  have h3 : (ge * R) ^ 2 < (gint * d) ^ 2 := by
    have : 0 < ge * R := by positivity
    nlinarith
  have h4 : ge ^ 2 * (ge * R) ^ 2 < ge ^ 2 * (gint * d) ^ 2 :=
    mul_lt_mul_of_pos_left h3 (by positivity)
  rw [div_lt_iff₀ (by positivity)]
  have e1 : ge ^ 4 * R ^ 2 = ge ^ 2 * (ge * R) ^ 2 := by ring
  have e2 : ge ^ 2 * (gint * d) ^ 2 = gint ^ 2 * (ge * d) ^ 2 := by ring
  rw [e1]
  calc ge ^ 2 * (ge * R) ^ 2 < ge ^ 2 * (gint * d) ^ 2 := h4
    _ = gint ^ 2 * (ge * d) ^ 2 := e2
    _ = M * (G * a0 * gint ^ 2) := by rw [h1]; ring

theorem nu_ge_one (y : ℝ) (hy : 0 < y) : 1 ≤ nu y := by
  unfold nu
  have h : (1 / 2 : ℝ) ≤ Real.sqrt (1 / 4 + 1 / y) := by
    rw [show (1 / 2 : ℝ) = Real.sqrt (1 / 4) by
      rw [show (1 / 4 : ℝ) = (1 / 2) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    exact Real.sqrt_le_sqrt (by have : 0 < 1 / y := by positivity
                                linarith)
  linarith

end QX4

#print axioms QX4.mu_nu_inverse
#print axioms QX4.host_mass_lower
#print axioms QX4.nu_ge_one
