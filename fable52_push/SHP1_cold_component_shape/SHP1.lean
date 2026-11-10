/-
SHP1 (criteria db5f7da07b): Lean statements for Part A, the closed form of the cold component's shape under the
counted-once law. They certify the algebra, not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not
theory closed.

Units: x = r / r_M with r_M = sqrt(G M_b / a0); y = g_N / a0 = 1 / x^2. The law's field is g = a0 uin(y),
uin(y) = y/2 + sqrt(y^2/4 + y). The cold component's enclosed mass in units of M_b is X = g / g_N - 1.

  closed      uin(y)/y - 1 = (sqrt(1 + 4/y) - 1)/2                  (so X(x) = (sqrt(1 + 4 x^2) - 1)/2)
  X_le_x      X(x) <= x                                              (deep: about x, so rho ~ 1/r^2)
  X_ge        x - 1/2 <= X(x)
  X_le_sq     X(x) <= x^2                                            (inside r_M: about x^2, so rho ~ 1/r)
  X_strictMono   X strictly increasing on [0, inf)
  hasDerivAt_X   dX/dx = 2x / sqrt(1 + 4 x^2)
  D_strictAnti   the density shape D(x) = 1/(x sqrt(1 + 4x^2)) strictly decreases on (0, inf)
  D_inj          so a density level (rho_DE, say) is met at one radius at most
  law_identity   g = a0 (1 + sqrt(1 + 4x^2)) / (2x^2) solves g_N = g^2 / (g + a0) with g_N = a0 / x^2
-/
import Mathlib

namespace SHP1

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

end SHP1

#print axioms SHP1.closed
#print axioms SHP1.X_le_x
#print axioms SHP1.X_ge
#print axioms SHP1.X_le_sq
#print axioms SHP1.X_strictMono
#print axioms SHP1.hasDerivAt_X
#print axioms SHP1.D_strictAnti
#print axioms SHP1.D_inj
#print axioms SHP1.law_identity
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
