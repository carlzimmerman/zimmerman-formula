/-
SHP1 MUTATE twin (criteria db5f7da07b): the true statements of SHP1.lean (namespace SHP1M) followed by six false
versions. This file must FAIL to compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SHP1M

open Real

noncomputable def uin (y : ℝ) : ℝ := y / 2 + Real.sqrt (y ^ 2 / 4 + y)
noncomputable def X (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
noncomputable def D (x : ℝ) : ℝ := 1 / (x * Real.sqrt (1 + 4 * x ^ 2))

theorem closed (y : ℝ) (hy : 0 < y) : uin y / y - 1 = (Real.sqrt (1 + 4 / y) - 1) / 2 := by
  unfold uin
  have h1 : y ^ 2 / 4 + y = (y / 2) ^ 2 * (1 + 4 / y) := by field_simp; ring
  have h2 : Real.sqrt (y ^ 2 / 4 + y) = y / 2 * Real.sqrt (1 + 4 / y) := by
    rw [h1, Real.sqrt_mul (by positivity), Real.sqrt_sq (by positivity)]
  rw [h2]; field_simp; ring

theorem X_le_x (x : ℝ) (hx : 0 ≤ x) : X x ≤ x := by
  unfold X
  have : Real.sqrt (1 + 4 * x ^ 2) ≤ 1 + 2 * x := by
    rw [Real.sqrt_le_left (by positivity)]; nlinarith
  linarith

theorem X_ge (x : ℝ) (_hx : 0 ≤ x) : x - 1 / 2 ≤ X x := by
  unfold X
  have : 2 * x ≤ Real.sqrt (1 + 4 * x ^ 2) := by
    apply Real.le_sqrt_of_sq_le; nlinarith
  linarith

theorem X_le_sq (x : ℝ) : X x ≤ x ^ 2 := by
  unfold X
  have : Real.sqrt (1 + 4 * x ^ 2) ≤ 1 + 2 * x ^ 2 := by
    rw [Real.sqrt_le_left (by positivity)]; nlinarith [sq_nonneg (x ^ 2)]
  linarith

theorem X_strictMono : StrictMonoOn X (Set.Ici 0) := by
  intro a ha b hb hab
  simp only [Set.mem_Ici] at ha hb
  unfold X
  have h : 1 + 4 * a ^ 2 < 1 + 4 * b ^ 2 := by nlinarith
  have := Real.sqrt_lt_sqrt (by positivity) h
  linarith

theorem hasDerivAt_X (x : ℝ) : HasDerivAt X (2 * x / Real.sqrt (1 + 4 * x ^ 2)) x := by
  have hpos : (0 : ℝ) < 1 + 4 * x ^ 2 := by positivity
  have h2 : HasDerivAt (fun v : ℝ => v ^ 2) (2 * x) x := by simpa using hasDerivAt_pow 2 x
  have hin : HasDerivAt (fun v : ℝ => 1 + 4 * v ^ 2) (8 * x) x := by
    exact ((h2.const_mul 4).const_add 1).congr_deriv (by ring)
  have h : HasDerivAt (fun v : ℝ => (Real.sqrt (1 + 4 * v ^ 2) - 1) / 2)
      ((8 * x / (2 * Real.sqrt (1 + 4 * x ^ 2))) / 2) x :=
    ((hin.sqrt hpos.ne').sub_const 1).div_const 2
  have hne : Real.sqrt (1 + 4 * x ^ 2) ≠ 0 := (Real.sqrt_pos.mpr hpos).ne'
  have he : 2 * x / Real.sqrt (1 + 4 * x ^ 2) = (8 * x / (2 * Real.sqrt (1 + 4 * x ^ 2))) / 2 := by
    field_simp; ring
  rw [he]; exact h

theorem D_strictAnti : StrictAntiOn D (Set.Ioi 0) := by
  intro a ha b hb hab
  simp only [Set.mem_Ioi] at ha hb
  unfold D
  have hsa : 0 < Real.sqrt (1 + 4 * a ^ 2) := Real.sqrt_pos.mpr (by positivity)
  have hsab : Real.sqrt (1 + 4 * a ^ 2) < Real.sqrt (1 + 4 * b ^ 2) :=
    Real.sqrt_lt_sqrt (by positivity) (by nlinarith)
  apply one_div_lt_one_div_of_lt (by positivity)
  calc a * Real.sqrt (1 + 4 * a ^ 2) < b * Real.sqrt (1 + 4 * a ^ 2) := by nlinarith
    _ < b * Real.sqrt (1 + 4 * b ^ 2) := by nlinarith

theorem D_inj (a b : ℝ) (ha : 0 < a) (hb : 0 < b) (h : D a = D b) : a = b :=
  D_strictAnti.injOn ha hb h

theorem law_identity (a0 x : ℝ) (ha : 0 < a0) (hx : 0 < x) :
    let g := a0 * (1 + Real.sqrt (1 + 4 * x ^ 2)) / (2 * x ^ 2)
    a0 / x ^ 2 = g ^ 2 / (g + a0) := by
  intro g
  have hs : Real.sqrt (1 + 4 * x ^ 2) ^ 2 = 1 + 4 * x ^ 2 := Real.sq_sqrt (by positivity)
  have hg : 0 < g := by positivity
  have hga : g + a0 ≠ 0 := by positivity
  have hx2 : x ^ 2 ≠ 0 := by positivity
  have hdiff : g ^ 2 - a0 / x ^ 2 * (g + a0) =
      a0 ^ 2 / (4 * x ^ 4) * (Real.sqrt (1 + 4 * x ^ 2) ^ 2 - (1 + 4 * x ^ 2)) := by
    show (a0 * (1 + Real.sqrt (1 + 4 * x ^ 2)) / (2 * x ^ 2)) ^ 2
        - a0 / x ^ 2 * (a0 * (1 + Real.sqrt (1 + 4 * x ^ 2)) / (2 * x ^ 2) + a0) = _
    field_simp; ring
  rw [hs, sub_self, mul_zero, sub_eq_zero] at hdiff
  rw [eq_div_iff hga]; exact hdiff.symm


-- ===== false versions (each must fail) =====
theorem X_le_x_M (x : ℝ) (hx : 0 ≤ x) : X x ≤ x / 2 := by
  unfold X
  have : Real.sqrt (1 + 4 * x ^ 2) ≤ 1 + x := by
    rw [Real.sqrt_le_left (by positivity)]; nlinarith
  linarith

theorem X_ge_M (x : ℝ) (hx : 0 ≤ x) : x ≤ X x := by
  unfold X
  have : 2 * x + 1 ≤ Real.sqrt (1 + 4 * x ^ 2) := by
    apply Real.le_sqrt_of_sq_le; nlinarith
  linarith

theorem X_le_sq_M (x : ℝ) : X x ≤ x ^ 2 / 2 := by
  unfold X
  have : Real.sqrt (1 + 4 * x ^ 2) ≤ 1 + x ^ 2 := by
    rw [Real.sqrt_le_left (by positivity)]; nlinarith [sq_nonneg (x ^ 2)]
  linarith

theorem hasDerivAt_X_M (x : ℝ) : HasDerivAt X (2 * x / (1 + 4 * x ^ 2)) x := by
  have h := hasDerivAt_X x
  have hpos : (0 : ℝ) < 1 + 4 * x ^ 2 := by positivity
  convert h using 1
  field_simp

theorem D_strictMono_M : StrictMonoOn D (Set.Ioi 0) := by
  intro a ha b hb hab
  simp only [Set.mem_Ioi] at ha hb
  unfold D
  apply one_div_lt_one_div_of_lt (by positivity)
  nlinarith [Real.sqrt_nonneg (1 + 4 * a ^ 2)]

theorem law_identity_M (a0 x : ℝ) (ha : 0 < a0) (hx : 0 < x) :
    let g := a0 * (1 - Real.sqrt (1 + 4 * x ^ 2)) / (2 * x ^ 2)
    a0 / x ^ 2 = g ^ 2 / (g + a0) := by
  intro g
  have hs : Real.sqrt (1 + 4 * x ^ 2) ^ 2 = 1 + 4 * x ^ 2 := Real.sq_sqrt (by positivity)
  have hga : g + a0 ≠ 0 := by positivity
  rw [eq_div_iff hga]
  show a0 / x ^ 2 * (a0 * (1 - Real.sqrt (1 + 4 * x ^ 2)) / (2 * x ^ 2) + a0) =
    (a0 * (1 - Real.sqrt (1 + 4 * x ^ 2)) / (2 * x ^ 2)) ^ 2
  field_simp
  nlinarith [hs]

end SHP1M
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
