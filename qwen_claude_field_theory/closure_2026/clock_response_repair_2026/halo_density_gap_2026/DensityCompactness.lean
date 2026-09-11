import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/- gamma=0 constrained zero-clock-gradient initial slice only.
   M is squared reduced Planck mass. The SymPy bridge, not Lean, connects
   densitySlope to the varied action. C=rho R^2/(3M) is a density-radius
   proxy, equal to 2G M_b/R only for a uniform-density ball in c=1 units. -/
namespace ClockDensityCompactness
noncomputable section

def densitySlope (M m : ℝ) : ℝ := (m+1)/(2*M*m)

def lapseGap (H M m v rho : ℝ) : ℝ := 9*H^2*(m+1)*(1-v)/(m*(m+2)) + (m+1)*rho/(2*M*m)

theorem positive_gap (H M m v rho : ℝ) (hH : 0 < H) (hM : 0 < M)
    (hm : 0 < m) (hv : v < 1) (hr : 0 ≤ rho) : 0 < lapseGap H M m v rho := by
  have h1 : 0 < 1-v := by linarith
  unfold lapseGap
  positivity

theorem selected_epoch_gap (H rho : ℝ) (hH : H^2=4/15) :
    lapseGap H 1 (1/10) (1/2) rho = 44/7+(11/2 : ℝ)*rho := by
  unfold lapseGap
  rw [hH]
  ring

theorem density_compactness_identity (M m rho R base C : ℝ)
    (hM : M ≠ 0) (hm : m ≠ 0) (hc : rho*R^2=3*M*C) :
    (base+densitySlope M m*rho)*R^2 = base*R^2+3*(m+1)/(2*m)*C := by
  unfold densitySlope
  have hterm : (m+1)/(2*M*m)*rho*R^2 = (m+1)/(2*m)*(rho*R^2/M) := by
    field_simp [hM,hm]
  rw [add_mul,hterm,hc]
  field_simp [hM,hm]

theorem fixed_epoch_coefficient (M : ℝ) :
    densitySlope M (1/10) = 11/(2*M) := by
  unfold densitySlope
  ring

theorem fixed_epoch_budget (B C : ℝ) :
    B+3*((1/10 : ℝ)+1)/(2*(1/10))*C = B+(33/2 : ℝ)*C := by
  ring

theorem required_compactness (B C eps : ℝ)
    (hbg : B ≤ eps) (hscreen : 1 ≤ B+(33/2 : ℝ)*C) :
    2*(1-eps)/33 ≤ C := by
  linarith

theorem weak_field_exclusion (B C : ℝ)
    (hbg : B ≤ 1/100) (hweak : C ≤ 1/100000) :
    B+(33/2 : ℝ)*C < 1 := by
  linarith

#print axioms density_compactness_identity
#print axioms fixed_epoch_coefficient
#print axioms fixed_epoch_budget
#print axioms required_compactness
#print axioms weak_field_exclusion
#print axioms positive_gap
#print axioms selected_epoch_gap
end
end ClockDensityCompactness
