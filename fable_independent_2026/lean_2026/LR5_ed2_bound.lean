import Mathlib

open MeasureTheory Real

/- LR5: Lean leg of the J06 bound chain E[D^2] >= 3 E[Dv^2]^2 / E[v^4]
   (register row 15, 'open (M01)').  Z7-wave.
   * T2lite (corrected per brief amendment 1): the m=1 chain coefficient algebra
     3*(2a)^2/(12b) = a^2/b -- pure algebra over the moment identities
     E[Dv^2] = 2*E[Dang], E[v^4] = 12*E[ang^2] (the identities themselves are
     the conditional-Gaussian leg, R0-audited numerically in LR5_ed2_bound.out;
     not probability-space-certified here -- labeled, not sorry'd).
   * T3: Cauchy-Schwarz in L2 for real-valued functions -- the probability-space
     leg of a^2/b <= E[D^2].  Proof: Q(t) = integral (f - t g)^2 >= 0 for all t,
     expanded mechanically; discriminant argument at t = C/A closes it; the
     circularity is broken by pointwise |fg| <= (f^2+g^2)/2 (AM-GM), so f*g is
     integrable without invoking CS. -/
theorem lr5_chain (a b : ℝ) (hb : b ≠ 0) :
    (3 : ℝ) * (2 * a) ^ 2 / (12 * b) = a ^ 2 / b := by
  field_simp
  ring

theorem lr5_l2_cs {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}
    (f g : Ω → ℝ) (hf : MemLp f 2 μ) (hg : MemLp g 2 μ) :
    (∫ x, f x * g x ∂μ) ^ 2 ≤ (∫ x, f x ^ 2 ∂μ) * (∫ x, g x ^ 2 ∂μ) := by
  classical
  have hf2 : Integrable (fun x => f x ^ 2) μ := hf.integrable_sq
  have hg2 : Integrable (fun x => g x ^ 2) μ := hg.integrable_sq
  have hfg : Integrable (fun x => f x * g x) μ := hf.integrable_mul hg
  have hDge : 0 ≤ ∫ x, f x ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg (f x))
  have hAge : 0 ≤ ∫ x, g x ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg (g x))
  have hexp : ∀ t : ℝ, ∫ x, (f x - t * g x) ^ 2 ∂μ
      = (∫ x, f x ^ 2 ∂μ) - 2 * t * (∫ x, f x * g x ∂μ) + t * t * (∫ x, g x ^ 2 ∂μ) := by
    intro t
    have i2 : Integrable (fun x => 2 * t * (f x * g x)) μ := hfg.const_mul (2 * t)
    have i3 : Integrable (fun x => t * t * (g x ^ 2)) μ := hg2.const_mul (t * t)
    have s1 : Integrable (fun x => f x ^ 2 - 2 * t * (f x * g x)) μ := hf2.sub i2
    have hcongr : (fun x => (f x - t * g x) ^ 2) =ᵐ[μ]
        (fun x => f x ^ 2 - 2 * t * (f x * g x) + t * t * (g x ^ 2)) :=
      Filter.Eventually.of_forall (fun x => by ring)
    rw [integral_congr_ae hcongr, integral_add s1 i3, integral_sub hf2 i2,
        integral_const_mul, integral_const_mul]
  set A : ℝ := ∫ x, g x ^ 2 ∂μ with hAdef
  set C : ℝ := ∫ x, f x * g x ∂μ with hCdef
  set D : ℝ := ∫ x, f x ^ 2 ∂μ with hDdef
  by_cases hA : A = 0
  · have hint0 : ∫ x, g x ^ 2 ∂μ = 0 := by rw [← hAdef]; exact hA
    have hg0 : (fun x => g x ^ 2) =ᵐ[μ] (fun _ : Ω => (0:ℝ)) :=
      (integral_eq_zero_iff_of_nonneg (fun x => sq_nonneg (g x)) hg2).mp hint0
    have hfg0 : (fun x => f x * g x) =ᵐ[μ] (fun _ : Ω => (0:ℝ)) := by
      filter_upwards [hg0] with x hx
      have hgx : g x = 0 := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp hx
      simp [hgx]
    have hC0 : C = 0 := by
      rw [hCdef, integral_congr_ae hfg0, integral_zero]
    rw [hC0, hA]
    simp
  · have hApos : 0 < A := lt_of_le_of_ne hAge (Ne.symm hA)
    have hq : 0 ≤ ∫ x, (f x - (C / A) * g x) ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg _)
    rw [hexp (C / A)] at hq
    have h2 : 0 ≤ A * (D - 2 * (C / A) * C + (C / A) * (C / A) * A) := by
      nlinarith [hq, hApos]
    have h3 : A * (D - 2 * (C / A) * C + (C / A) * (C / A) * A) = A * D - C * C := by
      have hne : A ≠ 0 := Ne.symm (hApos.ne)
      field_simp
      ring
    linarith [h2, h3]

#print axioms lr5_chain
#print axioms lr5_l2_cs
