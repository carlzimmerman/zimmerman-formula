/-
AS058 -- Field redefinition and the channel slope (Lean certificate).

Certifies the algebraic core of the lane result, on the framework's own
footing (n = 2 = the adopted channel count; kappa = 1/2 = a0/s = 1/n):

  T1  the OR-composition identity for the corpus member
      p(Y) = Y/(1+Y):  1-(1-p)^2 = 1-(1+Y)^(-2);
  T2  the channel-slope claim, generic completion: for ANY per-channel
      engagement p with p(0) = 0 and p'(0) = 1 the OR composition
      1-(1-p)^2 has slope exactly 2 at the origin (completion-independent);
  T3  the corpus member's slope: d/dY [1-(1+Y)^(-2)] at 0 is 2;
  T4  slope renormalization: measured against the primed field's gradient in
      fixed-s units, Z' = |grad Phi'|/s = lambda*Y, the same response has
      slope 2/lambda (the slope claim is normalization-free ONLY in the
      physical variable Y = g/s);
  T5  compensated redefinition invariance of the deep law (n = 2): from the
      primed-variable matching g'^2 = lambda^2*(s/2)*(G M/r^2) and the
      physical identification g = g'/lambda,
          g^2 = (s/2) (G M / r^2)   (a0 = s/2 invariant; kappa = 1/2);
  T6  the negative control algebra: the SAME deep-matching with the source
      coupling UNCHANGED gives g_c^2 = (lambda s/2)(G M/r^2) -- a0_c = lambda
      s/2 -- flagging the changed theory;
  T7  and that changed coefficient equals the original IFF lambda = 1.

All statements are pure algebra over the reals; no sqrt, no topology beyond
hasDerivAt at 0, no sorry.
-/
import Mathlib

/- T1: the OR-identity for the corpus member p = Y/(1+Y). -/
theorem or_identity_corpus (Y : ℝ) (hY : Y ≠ -1) :
    1 - (1 - Y / (1 + Y)) ^ 2 = 1 - ((1 + Y) ^ 2)⁻¹ := by
  have h1 : 1 + Y ≠ 0 := by
    intro h
    apply hY
    linarith
  have hm : (1 + Y) * (1 - Y / (1 + Y)) = 1 := by
    rw [mul_sub, div_eq_mul_inv]
    field_simp [h1] <;> ring
  have hA : 1 - Y / (1 + Y) = (1 + Y)⁻¹ := eq_inv_of_mul_eq_one_right hm
  rw [hA]
  rw [inv_pow]

/- T2: the channel slope 2 is completion-independent.
   Premises: p(0) = 0 and p'(0) = 1 (the fraction identity of the one-scale
   action, PD08 Step 3; k01 proves no second coefficient exists). -/
theorem or_slope_generic {p : ℝ → ℝ} (hp0 : p 0 = 0) (hpd : HasDerivAt p 1 0) :
    HasDerivAt (fun Y : ℝ => 1 - (1 - p Y) ^ 2) 2 0 := by
  -- g(Y) = 1 - p(Y),  g(0) = 1,  g'(0) = -1
  have hg : HasDerivAt (fun Y : ℝ => 1 - p Y) (-1) 0 := by
    simpa [sub_eq_add_neg] using ((hpd.neg).add_const 1)
  have hg0 : 1 - p 0 = 1 := by simp [hp0]
  -- (1 - p)^2 = g * g pointwise (the lemma's exact output form):
  have hgm : HasDerivAt ((fun Y : ℝ => 1 - p Y) * fun Y : ℝ => 1 - p Y)
      ((-1) * (1 - p 0) + (1 - p 0) * (-1)) 0 := hg.mul hg
  have hg2 : HasDerivAt (fun Y : ℝ => (1 - p Y) ^ 2) (-2) 0 := by
    have hf : (fun Y : ℝ => (1 - p Y) ^ 2) =
        (fun Y : ℝ => 1 - p Y) * (fun Y : ℝ => 1 - p Y) := by
      funext Y
      simp only [Pi.mul_apply]
      ring
    have hv : ((-1) * (1 - p 0) + (1 - p 0) * (-1)) = -2 := by
      rw [hg0]
      norm_num
    rw [hf, ← hv]
    exact hgm
  have hneg : HasDerivAt (-(fun Y : ℝ => (1 - p Y) ^ 2)) 2 0 :=
    (hg2.neg).congr_deriv (by norm_num)
  have hfinv : (fun Y : ℝ => 1 - (1 - p Y) ^ 2) =
      fun Y : ℝ => -((1 - p Y) ^ 2) + 1 := by
    funext Y
    ring
  rw [hfinv]
  exact (hneg.add_const 1)

/- T3: the corpus member mu_2(Y) = 1-(1+Y)^(-2) has slope 2 at the origin.
   (n = 2, the adopted count; the lane proves the same for general n.) -/
theorem corpus_slope_two :
    HasDerivAt (fun Y : ℝ => 1 - ((1 + Y) ^ 2)⁻¹) 2 0 := by
  have hlin : HasDerivAt (fun Y : ℝ => Y + 1) 1 0 := by
    exact (HasDerivAt.add_const (1 : ℝ) (hasDerivAt_id (x := (0 : ℝ))))
  have hlin3 : HasDerivAt (fun Y : ℝ => 1 + Y) 1 0 := by
    have hf : (fun Y : ℝ => 1 + Y) = fun Y : ℝ => Y + 1 := by
      funext Y
      ring
    rw [hf]
    exact hlin
  have hpow : HasDerivAt (fun x : ℝ => x ^ 2)
      ((2 : ℝ) * (1 + 0) ^ (2 - 1)) (1 + 0) :=
    hasDerivAt_pow (n := 2) (x := 1 + (0 : ℝ))
  have hcomp : HasDerivAt (fun Y : ℝ => (1 + Y) ^ 2)
      ((2 : ℝ) * (1 + 0) ^ (2 - 1) * 1) 0 := hpow.comp 0 hlin3
  have hsq : HasDerivAt (fun Y : ℝ => (1 + Y) ^ 2) 2 0 := by
    simpa [pow_one, mul_one] using hcomp
  have hsq0 : (1 + (0 : ℝ)) ^ 2 ≠ 0 := by norm_num
  have hinv : HasDerivAt (fun Y : ℝ => ((1 + Y) ^ 2)⁻¹)
      (-(2) / ((1 + (0 : ℝ)) ^ 2) ^ 2) 0 := by
    exact (HasDerivAt.inv hsq hsq0)
  have hneg : HasDerivAt (fun Y : ℝ => -(((1 + Y) ^ 2)⁻¹))
      (-(-(2) / ((1 + (0 : ℝ)) ^ 2) ^ 2)) 0 := hinv.neg
  have hfinv : (fun Y : ℝ => 1 - ((1 + Y) ^ 2)⁻¹) =
      fun Y : ℝ => -(((1 + Y) ^ 2)⁻¹) + 1 := by
    funext Y
    ring
  rw [hfinv]
  exact (hneg.add_const 1).congr_deriv (by norm_num)

/- T4: slope renormalization. In fixed-s units of the primed field,
   Z' = |grad Phi'|/s = lambda*Y, the same response 1-(1+Y)^(-2) has slope
   2/lambda at the origin. -/
theorem slope_renormalized (lam : ℝ) (_hlam : lam ≠ 0) :
    HasDerivAt (fun Z : ℝ => 1 - ((1 + Z / lam) ^ 2)⁻¹) (2 / lam) 0 := by
  have hd : HasDerivAt (fun Z : ℝ => Z / lam) (1 / lam) 0 := by
    simpa [one_div, div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using
      (hasDerivAt_const_mul (1 / lam))
  have hin : HasDerivAt (fun Z : ℝ => 1 + Z / lam) (1 / lam) 0 := by
    simpa [add_comm] using (hd.add_const 1)
  have hz : (0 : ℝ) / lam = 0 := by rw [zero_div]
  have hpow : HasDerivAt (fun x : ℝ => x ^ 2)
      ((2 : ℝ) * (1 + 0 / lam) ^ (2 - 1)) (1 + 0 / lam) :=
    hasDerivAt_pow (n := 2) (x := 1 + (0 : ℝ) / lam)
  have hcomp : HasDerivAt (fun Z : ℝ => (1 + Z / lam) ^ 2)
      ((2 : ℝ) * (1 + 0 / lam) ^ (2 - 1) * (1 / lam)) 0 := by
    exact hpow.comp (0 : ℝ) hin
  have hsq : HasDerivAt (fun Z : ℝ => (1 + Z / lam) ^ 2) (2 / lam) 0 := by
    simpa [pow_one, hz, one_div, div_eq_mul_inv] using hcomp
  have hsq0 : (1 + (0 : ℝ) / lam) ^ 2 ≠ 0 := by
    rw [hz]
    norm_num
  have hinv : HasDerivAt (fun Z : ℝ => ((1 + Z / lam) ^ 2)⁻¹)
      (-(2 / lam) / ((1 + (0 : ℝ) / lam) ^ 2) ^ 2) 0 := by
    exact (HasDerivAt.inv hsq hsq0)
  have hneg : HasDerivAt (fun Z : ℝ => -(((1 + Z / lam) ^ 2)⁻¹))
      (-(-(2 / lam) / ((1 + (0 : ℝ) / lam) ^ 2) ^ 2)) 0 := hinv.neg
  have hfinv : (fun Z : ℝ => 1 - ((1 + Z / lam) ^ 2)⁻¹) =
      fun Z : ℝ => -(((1 + Z / lam) ^ 2)⁻¹) + 1 := by
    funext Z
    ring
  rw [hfinv]
  exact (hneg.add_const 1).congr_deriv (by rw [hz]; simp)

/- T5: compensated redefinition leaves the physical deep law invariant.
   Primed deep matching (n = 2): g'^2 = lambda^2 * (s/2) * (G M / r^2);
   physical acceleration g = g'/lambda  =>  g^2 = (s/2) (G M / r^2). -/
theorem deep_law_invariance (lam s G M r g gp : ℝ) (hr : r ≠ 0)
    (hlam : lam ≠ 0) (hscale : gp = lam * g)
    (hdeep : gp ^ 2 = lam ^ 2 * (s / 2) * (G * M / r ^ 2)) :
    g ^ 2 = s / 2 * (G * M / r ^ 2) := by
  rw [hscale] at hdeep
  calc
    g ^ 2 = (lam * g) ^ 2 / lam ^ 2 := by field_simp [hlam]
    _ = (lam ^ 2 * (s / 2) * (G * M / r ^ 2)) / lam ^ 2 := by rw [hdeep]
    _ = s / 2 * (G * M / r ^ 2) := by field_simp [hlam]

/- T6: NEGATIVE CONTROL algebra. If the matter coupling is NOT rescaled, the
   rescaled-field theory's deep matching reads
   g_c * (2 g_c / (lam * s)) = G M / r^2  (mu = 2 g_c/(lam s) at n = 2),
   which solves to g_c^2 = (lam * s / 2) * (G M / r^2):
   a0_c = lam * (s/2) -- the changed theory. -/
theorem changed_theory_deep_law (lam s G M r : ℝ) (hc : lam ≠ 0) (hs : s ≠ 0)
    (hr : r ≠ 0) (g : ℝ) (hdeep : g * (2 * g / (lam * s)) = G * M / r ^ 2) :
    g ^ 2 = (lam * s / 2) * (G * M / r ^ 2) := by
  field_simp [hc, hs, hr] at hdeep ⊢
  ring_nf at hdeep ⊢
  exact hdeep

/- T7: the changed coefficient equals the original one iff lambda = 1. -/
theorem changed_coefficient_differs (lam s : ℝ) (hs : s ≠ 0) (hlam : lam ≠ 1) :
    lam * s / 2 ≠ s / 2 := by
  intro hz
  have hz2 : lam * s = s := by
    have hm2 : 2 * (lam * s / 2) = 2 * (s / 2) := congrArg (fun x : ℝ => 2 * x) hz
    have hleft : 2 * (lam * s / 2) = lam * s := by field_simp
    have hright : 2 * (s / 2) = s := by field_simp
    rw [hleft, hright] at hm2
    exact hm2
  have hEq : s * lam = s * (1 : ℝ) := by
    rw [mul_comm, mul_one]
    exact hz2
  exact hlam (mul_left_cancel₀ hs hEq)