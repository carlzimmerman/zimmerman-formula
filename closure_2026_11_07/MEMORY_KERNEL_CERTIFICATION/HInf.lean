import Mathlib
open MeasureTheory Set
namespace HInf

/-- Analytic core of EW2 H-inf, normalized to R = 1: a potential whose secants
have slope at least s cannot have arbitrarily small weighted absolute area. -/
theorem weighted_abs_lower (f : ℝ → ℝ) (s : ℝ) (hs : 0 ≤ s)
    (hf : Continuous f)
    (hgrowth : ∀ x ∈ Icc (1/2 : ℝ) 1, ∀ y ∈ Icc (1/2 : ℝ) 1,
      x ≤ y → s * (y - x) ≤ f y - f x) :
    s / 128 ≤ ∫ x in (1/2 : ℝ)..1, |f x| * x ^ 2 := by
  have hi : IntervalIntegrable (fun x => |f x| * x ^ 2) volume (1/2) 1 :=
    (hf.abs.mul (continuous_id.pow 2)).intervalIntegrable _ _
  have hiL : IntervalIntegrable (fun x => |f x| * x ^ 2) volume (1/2) (3/4) :=
    (hf.abs.mul (continuous_id.pow 2)).intervalIntegrable _ _
  have hiR : IntervalIntegrable (fun x => |f x| * x ^ 2) volume (3/4) 1 :=
    (hf.abs.mul (continuous_id.pow 2)).intervalIntegrable _ _
  have ha := intervalIntegral.integral_add_adjacent_intervals hiL hiR
  have hnL : 0 ≤ ∫ x in (1/2 : ℝ)..(3/4), |f x| * x ^ 2 := by
    apply intervalIntegral.integral_nonneg (by norm_num)
    intro x hx; positivity
  have hnR : 0 ≤ ∫ x in (3/4 : ℝ)..1, |f x| * x ^ 2 := by
    apply intervalIntegral.integral_nonneg (by norm_num)
    intro x hx; positivity
  rcases le_total 0 (f (3/4)) with hmid | hmid
  · have hbound := intervalIntegral.integral_mono_on (μ := volume)
      (by norm_num : (3/4 : ℝ) ≤ 1)
      ((continuous_const.mul (continuous_id.sub continuous_const)).intervalIntegrable (3/4) 1)
      hiR (fun x hx => show (s/4) * (x - 3/4) ≤ |f x| * x^2 from by
        have h := hgrowth (3/4) (by norm_num) x ⟨by linarith [hx.1], hx.2⟩ hx.1
        have hfx : 0 ≤ f x := by nlinarith [hx.1, mul_nonneg hs (sub_nonneg.mpr hx.1)]
        rw [abs_of_nonneg hfx]
        have hx2 : (1/4 : ℝ) ≤ x^2 := by nlinarith [hx.1, sq_nonneg (x - 1/2)]
        nlinarith [mul_nonneg hfx (sub_nonneg.mpr hx2)])
    have heval : (∫ x in (3/4 : ℝ)..1, (s/4) * (x - 3/4)) = s/128 := by
      rw [intervalIntegral.integral_const_mul,
          intervalIntegral.integral_sub (f := fun x : ℝ => x) (g := fun _ : ℝ => (3/4 : ℝ)) (continuous_id.intervalIntegrable _ _)
            (continuous_const.intervalIntegrable _ _), integral_id,
          intervalIntegral.integral_const]
      norm_num
      ring
    simp only [Pi.mul_apply, Pi.sub_apply, id_eq] at hbound
    rw [heval] at hbound
    linarith
  · have hbound := intervalIntegral.integral_mono_on (μ := volume)
      (by norm_num : (1/2 : ℝ) ≤ 3/4)
      ((continuous_const.mul (continuous_const.sub continuous_id)).intervalIntegrable (1/2) (3/4))
      hiL (fun x hx => show (s/4) * (3/4 - x) ≤ |f x| * x^2 from by
        have h := hgrowth x ⟨hx.1, by linarith [hx.2]⟩ (3/4) (by norm_num) hx.2
        have hfx : f x ≤ 0 := by nlinarith [hx.2, mul_nonneg hs (sub_nonneg.mpr hx.2)]
        rw [abs_of_nonpos hfx]
        have hx2 : (1/4 : ℝ) ≤ x^2 := by nlinarith [hx.1, sq_nonneg (x - 1/2)]
        nlinarith [mul_nonneg (neg_nonneg.mpr hfx) (sub_nonneg.mpr hx2)])
    have heval : (∫ x in (1/2 : ℝ)..(3/4), (s/4) * (3/4 - x)) = s/128 := by
      rw [intervalIntegral.integral_const_mul,
          intervalIntegral.integral_sub (f := fun _ : ℝ => (3/4 : ℝ)) (g := fun x : ℝ => x) (continuous_const.intervalIntegrable _ _)
            (continuous_id.intervalIntegrable _ _), integral_id,
          intervalIntegral.integral_const]
      norm_num
      ring
    simp only [Pi.mul_apply, Pi.sub_apply, id_eq] at hbound
    rw [heval] at hbound
    linarith

/-- Combining the normalized integral lower bound with the separately supplied
mass-variation upper bound yields EW2's coefficient 512. -/
theorem scale_bound {muR delta eps area : ℝ}
    (heps : eps < 1) (hm : 0 ≤ muR ^ 2)
    (hlo : (1 - eps) / 128 ≤ area)
    (hhi : muR ^ 2 * area ≤ 4 * delta) :
    muR ^ 2 ≤ 512 * delta / (1 - eps) := by
  rw [le_div_iff₀ (by linarith : 0 < 1 - eps)]
  nlinarith [mul_le_mul_of_nonneg_left hlo hm]

/-- Derivative hypotheses imply the secant condition used above. -/
theorem weighted_abs_lower_of_deriv (f : ℝ → ℝ) (s : ℝ) (hs : 0 ≤ s)
    (hf : Continuous f)
    (hfd : DifferentiableOn ℝ f (interior (Icc (1/2 : ℝ) 1)))
    (hd : ∀ x ∈ interior (Icc (1/2 : ℝ) 1), s ≤ deriv f x) :
    s/128 ≤ ∫ x in (1/2 : ℝ)..1, |f x| * x^2 := by
  apply weighted_abs_lower f s hs hf
  exact (convex_Icc (1/2 : ℝ) 1).mul_sub_le_image_sub_of_le_deriv hf.continuousOn hfd hd

/-- The integral lower bound and the supplied mass-variation upper bound
compose to the claimed H-inf scale inequality. -/
theorem normalized_scale_bound (f : ℝ → ℝ) (muR delta eps : ℝ)
    (heps : eps < 1) (hf : Continuous f)
    (hfd : DifferentiableOn ℝ f (interior (Icc (1/2 : ℝ) 1)))
    (hd : ∀ x ∈ interior (Icc (1/2 : ℝ) 1), 1-eps ≤ deriv f x)
    (hmass : muR^2 * (∫ x in (1/2 : ℝ)..1, |f x| * x^2) ≤ 4*delta) :
    muR^2 ≤ 512*delta/(1-eps) := by
  exact scale_bound heps (sq_nonneg muR)
    (weighted_abs_lower_of_deriv f (1-eps) (by linarith) hf hfd hd) hmass


theorem bounded_increment (D : ℝ → ℝ) {δ x y : ℝ}
    (hx : |D x| ≤ δ) (hy : |D y| ≤ δ) : |D y - D x| ≤ 2*δ := by
  exact (abs_sub _ _).trans (by linarith)

/-- A monotone potential has at most one sign change. If its signed weighted
integrals are increments of a uniformly bounded mass function, its absolute
weighted integral is bounded by 4 delta, not merely its signed integral. -/
theorem absolute_mass_variation (f D : ℝ → ℝ) {a b δ : ℝ}
    (hab : a ≤ b) (hδ : 0 ≤ δ) (hf : Continuous f)
    (hmono : MonotoneOn f (Icc a b))
    (hD : ∀ x ∈ Icc a b, |D x| ≤ δ)
    (hprim : ∀ x ∈ Icc a b, ∀ y ∈ Icc a b,
      (∫ r in x..y, f r * r^2) = D y - D x) :
    (∫ r in a..b, |f r| * r^2) ≤ 4*δ := by
  have ha : a ∈ Icc a b := ⟨le_rfl,hab⟩
  have hb : b ∈ Icc a b := ⟨hab,le_rfl⟩
  have habD := bounded_increment D (hD a ha) (hD b hb)
  by_cases hfa : 0 ≤ f a
  · have heq : (∫ r in a..b, |f r| *r^2) = ∫ r in a..b, f r*r^2 := by
      apply intervalIntegral.integral_congr
      intro x hx
      rw [uIcc_of_le hab] at hx
      dsimp only
      rw [abs_of_nonneg (le_trans hfa (hmono ha hx hx.1))]
    rw [heq,hprim a ha b hb]
    have := le_abs_self (D b-D a)
    linarith
  by_cases hfb : f b ≤ 0
  · have heq : (∫ r in a..b, |f r| *r^2) = -(∫ r in a..b, f r*r^2) := by
      rw [← intervalIntegral.integral_neg]
      apply intervalIntegral.integral_congr
      intro x hx
      rw [uIcc_of_le hab] at hx
      dsimp only
      rw [abs_of_nonpos (le_trans (hmono hx hb hx.2) hfb)]
      ring
    rw [heq,hprim a ha b hb]
    have := neg_le_abs (D b-D a)
    linarith
  have hfa' : f a ≤ 0 := le_of_not_ge hfa
  have hfb' : 0 ≤ f b := le_of_not_ge hfb
  obtain ⟨c,hc,hfc⟩ := intermediate_value_Icc hab hf.continuousOn ⟨hfa',hfb'⟩
  have hL : (∫ r in a..c, |f r| *r^2) = -(∫ r in a..c, f r*r^2) := by
    rw [← intervalIntegral.integral_neg]
    apply intervalIntegral.integral_congr
    intro x hx
    rw [uIcc_of_le hc.1] at hx
    have hfx : f x ≤ 0 := by
      rw [← hfc]
      exact hmono ⟨hx.1,le_trans hx.2 hc.2⟩ hc hx.2
    dsimp only
    rw [abs_of_nonpos hfx]
    ring
  have hR : (∫ r in c..b, |f r| *r^2) = ∫ r in c..b, f r*r^2 := by
    apply intervalIntegral.integral_congr
    intro x hx
    rw [uIcc_of_le hc.2] at hx
    have hfx : 0 ≤ f x := by
      rw [← hfc]
      exact hmono hc ⟨le_trans hc.1 hx.1,hx.2⟩ hx.1
    dsimp only
    rw [abs_of_nonneg hfx]
  have hjoin := intervalIntegral.integral_add_adjacent_intervals (μ := volume)
    ((hf.abs.mul (continuous_id.pow 2)).intervalIntegrable a c)
    ((hf.abs.mul (continuous_id.pow 2)).intervalIntegrable c b)
  simp only [Pi.mul_apply, Pi.pow_apply, id_eq] at hjoin
  rw [hL,hR,hprim a ha c hc,hprim c hc b hb] at hjoin
  have hLD := bounded_increment D (hD a ha) (hD c hc)
  have hRD := bounded_increment D (hD c hc) (hD b hb)
  have := neg_le_abs (D c-D a)
  have := le_abs_self (D b-D c)
  linarith


/-- The mass primitive can include any nonnegative coupling q, in particular
q = (mu R)^2 after normalizing radius and potential. -/
theorem weighted_mass_variation (f D : ℝ → ℝ) {a b δ q : ℝ}
    (hab : a ≤ b) (hδ : 0 ≤ δ) (hq : 0 ≤ q) (hf : Continuous f)
    (hmono : MonotoneOn f (Icc a b))
    (hD : ∀ x ∈ Icc a b, |D x| ≤ δ)
    (hprim : ∀ x ∈ Icc a b, ∀ y ∈ Icc a b,
      (∫ r in x..y, (q * f r) * r^2) = D y - D x) :
    q * (∫ r in a..b, |f r| * r^2) ≤ 4*δ := by
  have hm : MonotoneOn (fun x => q * f x) (Icc a b) := by
    intro x hx y hy hxy
    exact mul_le_mul_of_nonneg_left (hmono hx hy hxy) hq
  have h := absolute_mass_variation (fun x => q * f x) D hab hδ
    (continuous_const.mul hf) hm hD hprim
  have heq : (∫ r in a..b, |q * f r| * r^2) = q * ∫ r in a..b, |f r| * r^2 := by
    rw [← intervalIntegral.integral_const_mul]
    apply intervalIntegral.integral_congr
    intro x hx
    dsimp only
    rw [abs_mul, abs_of_nonneg hq]
    ring
  rwa [heq] at h

/-- Closed normalized H-inf chain: derivative floor, bounded mass, and its
primitive relation together imply the 512 scale bound. No absolute-integral
estimate is assumed. The PDE and dimensional normalization remain inputs. -/
theorem normalized_Hinf (f D : ℝ → ℝ) (muR delta eps : ℝ)
    (heps : eps < 1) (hdelta : 0 ≤ delta) (hf : Continuous f)
    (hfd : DifferentiableOn ℝ f (interior (Icc (1/2 : ℝ) 1)))
    (hd : ∀ x ∈ interior (Icc (1/2 : ℝ) 1), 1-eps ≤ deriv f x)
    (hD : ∀ x ∈ Icc (1/2 : ℝ) 1, |D x| ≤ delta)
    (hprim : ∀ x ∈ Icc (1/2 : ℝ) 1, ∀ y ∈ Icc (1/2 : ℝ) 1,
      (∫ r in x..y, (muR^2 * f r) * r^2) = D y - D x) :
    muR^2 ≤ 512*delta/(1-eps) := by
  have hg := (convex_Icc (1/2 : ℝ) 1).mul_sub_le_image_sub_of_le_deriv hf.continuousOn hfd hd
  have hm : MonotoneOn f (Icc (1/2 : ℝ) 1) := by
    intro x hx y hy hxy
    have hsec := hg x hx y hy hxy
    have hnon : 0 ≤ (1-eps) * (y-x) := mul_nonneg (by linarith) (sub_nonneg.mpr hxy)
    linarith
  apply normalized_scale_bound f muR delta eps heps hf hfd hd
  exact weighted_mass_variation f D (by norm_num) hdelta (sq_nonneg muR) hf hm hD hprim

/-- The normalized first-order mass equation supplies the primitive relation
by the fundamental theorem of calculus. -/
theorem normalized_Hinf_of_mass_derivative (f D : ℝ → ℝ) (muR delta eps : ℝ)
    (heps : eps < 1) (hdelta : 0 ≤ delta) (hf : Continuous f)
    (hfd : DifferentiableOn ℝ f (interior (Icc (1/2 : ℝ) 1)))
    (hd : ∀ x ∈ interior (Icc (1/2 : ℝ) 1), 1-eps ≤ deriv f x)
    (hD : ∀ x ∈ Icc (1/2 : ℝ) 1, |D x| ≤ delta)
    (hDderiv : ∀ x ∈ Icc (1/2 : ℝ) 1,
      HasDerivAt D ((muR^2 * f x) * x^2) x) :
    muR^2 ≤ 512*delta/(1-eps) := by
  apply normalized_Hinf f D muR delta eps heps hdelta hf hfd hd hD
  intro x hx y hy
  apply intervalIntegral.integral_eq_sub_of_hasDerivAt
  · intro z hz
    exact hDderiv z ((uIcc_subset_Icc hx hy) hz)
  · exact ((continuous_const.mul hf).mul (continuous_id.pow 2)).intervalIntegrable x y

end HInf


#print axioms HInf.weighted_abs_lower
#print axioms HInf.scale_bound
#print axioms HInf.weighted_abs_lower_of_deriv
#print axioms HInf.normalized_scale_bound
#print axioms HInf.bounded_increment
#print axioms HInf.absolute_mass_variation
#print axioms HInf.weighted_mass_variation
#print axioms HInf.normalized_Hinf
#print axioms HInf.normalized_Hinf_of_mass_derivative
