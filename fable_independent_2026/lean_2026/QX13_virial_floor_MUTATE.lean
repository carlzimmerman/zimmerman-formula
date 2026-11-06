/-
QX13 MUTATE twin: three planted false claims, each must fail.
M1: the post-shock enthalpy is (15/16) v^2 (wrong jump coefficient).
M2: the class bound holds for K BELOW the floor (K <= K_0) -- must fail.
M3: the profile base increases with K -- must fail.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace QX13M

theorem shock_enthalpy_wrong {ρ₁ v2 : ℝ} (hρ : 0 < ρ₁) :
    (5 / 2) * ((3 / 4) * ρ₁ * v2) / (4 * ρ₁) = (15 / 16) * v2 := by
  field_simp; ring

theorem class_bound_below_floor {h2 Hsh Hin K K0 : ℝ} (hK : 0 < K) (hK0p : 0 < K0) (hK0 : K ≤ K0) (h2le : h2 ≤ Hsh)
    (h2nn : 0 ≤ h2) (hin : 0 ≤ Hin) :
    2 * (h2 + Hin) / (5 * K) ≤ 2 * (Hsh + Hin) / (5 * K0) := by
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith

theorem base_up_in_K {w K₁ K₂ : ℝ} (hw : 0 < w) (hK1 : 0 < K₁) (hK2 : 0 < K₂) (hK : K₁ ≤ K₂) :
    2 * w / (5 * K₁) ≤ 2 * w / (5 * K₂) := by
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith

end QX13M

#print axioms QX13M.shock_enthalpy_wrong
#print axioms QX13M.class_bound_below_floor
#print axioms QX13M.base_up_in_K
