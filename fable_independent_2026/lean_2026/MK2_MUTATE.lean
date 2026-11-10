import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Tactic

/-!
# MK2 MUTATE twin: false versions of MK2.lean's claims. Every theorem here must FAIL to compile.

1. `width_reversed_FALSE`: n(x_b) − n(x_a) ≤ k² (x_b − x_a) from k² ≤ n' (the bound reversed).
2. `floods_without_monotone_FALSE`: a deep well holds n ≥ n(x_b) for any n (monotonicity dropped).
3. `sis_wrong_norm_FALSE`: ρ = c²/(4π G r²) with M = 2c² r/G satisfies Poisson (wrong normalisation).
4. `w_without_xT_FALSE`: w = x_T n / (n (1 + x − x_T)) equals x_T exactly (the O(x) term dropped).

κ = ½ FITTED; not theory closed. Adopts nothing.
-/

open Real

namespace MK2M

theorem width_reversed_FALSE {n n' : ℝ → ℝ} {xa xb k : ℝ} (hab : xa ≤ xb)
    (hd : ∀ x ∈ Set.Icc xa xb, HasDerivAt n (n' x) x) (hk : ∀ x ∈ Set.Icc xa xb, k ^ 2 ≤ n' x) :
    n xb - n xa ≤ k ^ 2 * (xb - xa) := by
  have hcont : ContinuousOn n (Set.Icc xa xb) := fun x hx => (hd x hx).continuousAt.continuousWithinAt
  have hdiff : DifferentiableOn ℝ n (interior (Set.Icc xa xb)) :=
    fun x hx => (hd x (interior_subset hx)).differentiableAt.differentiableWithinAt
  have hle : ∀ x ∈ interior (Set.Icc xa xb), k ^ 2 ≤ deriv n x := by
    intro x hx; rw [(hd x (interior_subset hx)).deriv]; exact hk x (interior_subset hx)
  have := Convex.mul_sub_le_image_sub_of_le_deriv (convex_Icc xa xb) hcont hdiff hle xa
    (Set.left_mem_Icc.mpr hab) xb (Set.right_mem_Icc.mpr hab) hab
  linarith

theorem floods_without_monotone_FALSE {n : ℝ → ℝ} {x0 φ xb : ℝ} (h : xb ≤ x0 + φ) : n xb ≤ n (x0 + φ) := by
  linarith

noncomputable def rhoW (c G r : ℝ) : ℝ := c ^ 2 / (4 * π * G * r ^ 2)
noncomputable def MSW (c G r : ℝ) : ℝ := 2 * c ^ 2 * r / G

theorem sis_wrong_norm_FALSE (c G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) (hc : c ≠ 0) :
    HasDerivAt (MSW c G) (4 * π * r ^ 2 * rhoW c G r) r := by
  have h : HasDerivAt (fun y : ℝ => 2 * c ^ 2 * y / G) (2 * c ^ 2 * 1 / G) r :=
    ((hasDerivAt_id r).const_mul (2 * c ^ 2)).div_const G
  unfold MSW rhoW
  convert h using 1
  have hpi : π ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

theorem w_without_xT_FALSE (n x xT : ℝ) (hden : n * (1 + x - xT) ≠ 0) :
    (xT * n) / (n * (1 + x - xT)) = xT := by
  have hn : n ≠ 0 := by intro h; apply hden; rw [h]; ring
  field_simp
  ring

end MK2M
-- κ = ½ FITTED; not theory closed. Adopts nothing.
