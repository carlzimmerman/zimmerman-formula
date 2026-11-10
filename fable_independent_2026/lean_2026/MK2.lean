import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Tactic

/-!
# MK2: the exponential dust term and the trade-off (2026-11-10)

Lane `fable52_push/MK2_exponential_dust_term/` (criteria 3b4f515ff8). n(x) = K L_K'(1 + x), x = Q − 1.

1. The trade-off (DT1 section 2, criteria section 2), for any n differentiable on [x_a, x_b]:
   * `width_le`: if k² ≤ n' on the stretch, then k² (x_b − x_a) ≤ n(x_b) − n(x_a).
   * `well_floods`: if n is monotone, a well whose offset x̄₀ + φ is at least x_b holds n ≥ n(x_b).
   * `flood_threshold`: together, every well with φ ≥ (x_a − x̄₀) + (n_b − n_a)/k² holds at least n_b.
2. The exponential n(x) = n* e^{x/x_T} (x_T > 0):
   * `exp_deriv`: n' = n / x_T, so the Jeans wavenumber² n' is proportional to the density and c_s² = n/n' = x_T.
   * `exp_static_ratio`: a well of depth φ holds n(x̄ + φ) = n(x̄) e^{φ/x_T} (Boltzmann).
   * `exp_dust_mono`: the static dust rises with φ and falls as x_T rises (for φ > 0).
   * `w_exp`: w = x_T / (1 + x − x_T) from ρ = n(1 + x − x_T), p = x_T n (units K = 1).
3. The singular isothermal sphere: ρ = c²/(2π G r²), M = 2c² r/G satisfies hydrostatic balance with Poisson:
   `sis_poisson` (dM/dr = 4π r² ρ) and `sis_hydrostatic` (c² dρ/dr = −ρ G M / r²).

κ = ½ FITTED; footings never pooled; the cold component is cold dark energy, no particle; not theory closed. Adopts nothing.
-/

open Real

namespace MK2

theorem width_le {n n' : ℝ → ℝ} {xa xb k : ℝ} (hab : xa ≤ xb)
    (hd : ∀ x ∈ Set.Icc xa xb, HasDerivAt n (n' x) x) (hk : ∀ x ∈ Set.Icc xa xb, k ^ 2 ≤ n' x) :
    k ^ 2 * (xb - xa) ≤ n xb - n xa := by
  have hcont : ContinuousOn n (Set.Icc xa xb) := fun x hx => (hd x hx).continuousAt.continuousWithinAt
  have hdiff : DifferentiableOn ℝ n (interior (Set.Icc xa xb)) :=
    fun x hx => (hd x (interior_subset hx)).differentiableAt.differentiableWithinAt
  have hle : ∀ x ∈ interior (Set.Icc xa xb), k ^ 2 ≤ deriv n x := by
    intro x hx
    rw [(hd x (interior_subset hx)).deriv]
    exact hk x (interior_subset hx)
  exact Convex.mul_sub_le_image_sub_of_le_deriv (convex_Icc xa xb) hcont hdiff hle xa
    (Set.left_mem_Icc.mpr hab) xb (Set.right_mem_Icc.mpr hab) hab

theorem well_floods {n : ℝ → ℝ} (hmono : Monotone n) {x0 φ xb : ℝ} (h : xb ≤ x0 + φ) : n xb ≤ n (x0 + φ) :=
  hmono h

theorem flood_threshold {n n' : ℝ → ℝ} (hmono : Monotone n) {xa xb x0 k φ : ℝ} (hk0 : 0 < k) (hab : xa ≤ xb)
    (hd : ∀ x ∈ Set.Icc xa xb, HasDerivAt n (n' x) x) (hk : ∀ x ∈ Set.Icc xa xb, k ^ 2 ≤ n' x)
    (hφ : (xa - x0) + (n xb - n xa) / k ^ 2 ≤ φ) : n xb ≤ n (x0 + φ) := by
  have hw := width_le hab hd hk
  have hk2 : 0 < k ^ 2 := by positivity
  have hwidth : xb - xa ≤ (n xb - n xa) / k ^ 2 := by
    rw [le_div_iff₀ hk2]; linarith
  exact well_floods hmono (by linarith)

/-! ## The exponential term -/

noncomputable def nE (ns xT x : ℝ) : ℝ := ns * exp (x / xT)

theorem exp_deriv (ns xT x : ℝ) (hT : xT ≠ 0) : HasDerivAt (nE ns xT) (nE ns xT x / xT) x := by
  have h1 : HasDerivAt (fun y : ℝ => y / xT) (1 / xT) x := by
    simpa using (hasDerivAt_id x).div_const xT
  have key : HasDerivAt (fun y : ℝ => ns * exp (y / xT)) (ns * (exp (x / xT) * (1 / xT))) x :=
    (h1.exp).const_mul ns
  have hf : nE ns xT = fun y : ℝ => ns * exp (y / xT) := by funext y; rfl
  rw [hf]
  convert key using 1
  simp only []
  ring

theorem exp_static_ratio (ns xT xb φ : ℝ) : nE ns xT (xb + φ) = nE ns xT xb * exp (φ / xT) := by
  unfold nE
  rw [add_div, exp_add]; ring

theorem exp_dust_mono {ns xT φ1 φ2 xb : ℝ} (hns : 0 < ns) (hT : 0 < xT) (h : φ1 ≤ φ2) :
    nE ns xT (xb + φ1) ≤ nE ns xT (xb + φ2) := by
  unfold nE
  apply mul_le_mul_of_nonneg_left _ hns.le
  apply exp_le_exp.mpr
  apply div_le_div_of_nonneg_right (by linarith) hT.le

theorem exp_dust_falls_with_xT {φ T1 T2 : ℝ} (hφ : 0 < φ) (h1 : 0 < T1) (h12 : T1 ≤ T2) :
    exp (φ / T2) ≤ exp (φ / T1) := by
  apply exp_le_exp.mpr
  exact div_le_div_of_nonneg_left hφ.le h1 h12

theorem w_exp (n x xT : ℝ) (hden : n * (1 + x - xT) ≠ 0) :
    (xT * n) / (n * (1 + x - xT)) = xT / (1 + x - xT) := by
  have hn : n ≠ 0 := by intro h; apply hden; rw [h]; ring
  have h2 : (1 + x - xT) ≠ 0 := by intro h; apply hden; rw [h]; ring
  field_simp

/-! ## The singular isothermal sphere -/

noncomputable def rhoS (c G r : ℝ) : ℝ := c ^ 2 / (2 * π * G * r ^ 2)
noncomputable def MS (c G r : ℝ) : ℝ := 2 * c ^ 2 * r / G

theorem sis_poisson (c G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    HasDerivAt (MS c G) (4 * π * r ^ 2 * rhoS c G r) r := by
  have h : HasDerivAt (fun y : ℝ => 2 * c ^ 2 * y / G) (2 * c ^ 2 * 1 / G) r :=
    ((hasDerivAt_id r).const_mul (2 * c ^ 2)).div_const G
  unfold MS rhoS
  convert h using 1
  have hpi : π ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

theorem sis_hydrostatic (c G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    HasDerivAt (fun y => c ^ 2 * rhoS c G y) (-(rhoS c G r) * G * MS c G r / r ^ 2) r := by
  have hpi : π ≠ 0 := Real.pi_ne_zero
  have hd : HasDerivAt (fun y : ℝ => y ^ 2) (2 * r) r := by simpa using hasDerivAt_pow 2 r
  have hne : (2 * π * G * r ^ 2) ≠ 0 := by
    have : r ^ 2 ≠ 0 := pow_ne_zero 2 hr
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero two_ne_zero hpi) hG) this
  have h2 : HasDerivAt (fun y : ℝ => 2 * π * G * y ^ 2) (2 * π * G * (2 * r)) r := hd.const_mul (2 * π * G)
  have key : HasDerivAt (fun y : ℝ => c ^ 2 * c ^ 2 * (2 * π * G * y ^ 2)⁻¹)
      (c ^ 2 * c ^ 2 * (-(2 * π * G * (2 * r)) / (2 * π * G * r ^ 2) ^ 2)) r := (h2.inv hne).const_mul (c ^ 2 * c ^ 2)
  have hf : (fun y => c ^ 2 * rhoS c G y) = fun y : ℝ => c ^ 2 * c ^ 2 * (2 * π * G * y ^ 2)⁻¹ := by
    funext y; unfold rhoS; rw [div_eq_mul_inv]; ring
  rw [hf]
  convert key using 1
  unfold rhoS MS
  field_simp

end MK2

#print axioms MK2.width_le
#print axioms MK2.well_floods
#print axioms MK2.flood_threshold
#print axioms MK2.exp_deriv
#print axioms MK2.exp_static_ratio
#print axioms MK2.exp_dust_mono
#print axioms MK2.exp_dust_falls_with_xT
#print axioms MK2.w_exp
#print axioms MK2.sis_poisson
#print axioms MK2.sis_hydrostatic
-- κ = ½ FITTED; not theory closed. Adopts nothing.
