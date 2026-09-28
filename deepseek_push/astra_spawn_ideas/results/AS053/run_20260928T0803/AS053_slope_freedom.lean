import Mathlib

/-!
# AS053 — Dimensionless slope freedom in a single-scale action

Algebraic certificate for the family

    p_lam(Y) = lam·Y / (1 + lam·Y),        lam > 0,
    mu_lam(Y) = 1 − (1 − p_lam(Y))²   =   1 − ((1 + lam·Y)²)⁻¹,
    K_lam(Y) = lam·Y² / (1 + lam·Y)    (  K_lam' = mu_lam  ).

Certified facts (all for real lam > 0, Y ≥ 0 where stated):
  1. p_lam(0) = 0, p_lam'(0) = lam                       (slope is a free parameter)
  2. mu_lam(0) = 0, mu_lam'(0) = 2·lam                   (two-channel slope = 2·lam)
  3. K_lam' = mu_lam                                    (static energy primitive)
  4. p_lam → 1 and mu_lam → 1 as Y → +∞                 (saturation/normalization)
  5. deep spherical matching: r²·(2lam/s)·g² = G·M  ⇒  g² = (s/(2lam))·(G·M/r²),
     i.e. the a0-line holds with a0 = s/(2lam) ⇒ κ = a0/s = 1/(2lam).

Proved with zero `sorry`; axioms are checked below via #print axioms.
-/

noncomputable section
open scoped Topology
open Filter

namespace AS053

-- pfun lam Y = lam·Y/(1+lam·Y)
def pfun (lam Y : ℝ) : ℝ := lam * Y / (1 + lam * Y)

-- mu_lam = 1 − (1 − p)²  (OR composition over two equal channels)
def mufun (lam Y : ℝ) : ℝ := 1 - (1 - pfun lam Y) ^ 2

-- K_lam = lam·Y²/(1+lam·Y), the static energy primitive
def kfun (lam Y : ℝ) : ℝ := lam * Y ^ 2 / (1 + lam * Y)

lemma pfun_zero (lam : ℝ) : pfun lam 0 = 0 := by
  simp [pfun]

theorem pfun_hasDerivAt_zero (lam : ℝ) :
    HasDerivAt (fun Y : ℝ => pfun lam Y) lam 0 := by
  unfold pfun
  have hnum : HasDerivAt (fun Y : ℝ => lam * Y) lam 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).const_mul lam
  have hden : HasDerivAt (fun Y : ℝ => 1 + lam * Y) lam 0 := by
    simpa [add_comm] using ((hasDerivAt_id (0 : ℝ)).const_mul lam).add_const 1
  have hd := hnum.div hden (by simp)
  have hval : (lam * (1 + lam * 0) - lam * 0 * lam) / (1 + lam * 0) ^ 2 = lam := by
    ring
  have hfunex : (fun Y : ℝ => lam * Y) / (fun Y : ℝ => 1 + lam * Y) =
      fun Y : ℝ => lam * Y / (1 + lam * Y) := by
    funext Y
    rfl
  rwa [hfunex, hval] at hd

lemma one_sub_pfun (lam Y : ℝ) (h : 1 + lam * Y ≠ 0) :
    1 - pfun lam Y = (1 + lam * Y)⁻¹ := by
  unfold pfun
  field_simp [h]
  ring

lemma mufun_eq_inv (lam Y : ℝ) (h : 1 + lam * Y ≠ 0) :
    mufun lam Y = 1 - ((1 + lam * Y) ^ 2)⁻¹ := by
  unfold mufun
  rw [one_sub_pfun lam Y h]
  rw [← inv_pow]

theorem mufun_zero (lam : ℝ) : mufun lam 0 = 0 := by
  simp [mufun, pfun]

theorem mufun_hasDerivAt_zero (lam : ℝ) :
    HasDerivAt (fun Y : ℝ => mufun lam Y) (2 * lam) 0 := by
  unfold mufun
  have hp := pfun_hasDerivAt_zero lam
  have h1p : HasDerivAt (fun Y : ℝ => 1 - pfun lam Y) (-lam) 0 := by
    simpa [sub_eq_add_neg] using (hp.neg.add_const 1)
  have hsq : HasDerivAt (fun Y : ℝ => (1 - pfun lam Y) ^ 2) (-2 * lam) 0 := by
    have h := h1p.pow 2
    have hval : (2 : ℝ) * (1 - pfun lam 0) ^ (2 - 1) * -lam = -2 * lam := by
      have hzp : pfun lam 0 = 0 := pfun_zero lam
      rw [hzp]
      norm_num
    exact hval ▸ h
  have hres : HasDerivAt (fun Y : ℝ => 1 - (1 - pfun lam Y) ^ 2) (2 * lam) 0 := by
    have h := hsq.neg.add_const 1
    simpa [sub_eq_add_neg] using h
  simpa using hres

-- --------------------------------------------------------------------------
-- K_lam' = mu_lam : the varied static energy primitive
-- --------------------------------------------------------------------------

lemma kfun_deriv_value (lam Y : ℝ) (h : 1 + lam * Y ≠ 0) :
    (2 * lam * Y * (1 + lam * Y) - lam * Y ^ 2 * lam) / (1 + lam * Y) ^ 2
      = mufun lam Y := by
  unfold mufun pfun
  field_simp [h]
  ring

theorem kfun_hasDerivAt (lam : ℝ) (hlam : 0 < lam) (Y : ℝ) (hY : 0 ≤ Y) :
    HasDerivAt (fun t : ℝ => kfun lam t) (mufun lam Y) Y := by
  unfold kfun
  have hp2 : HasDerivAt (fun t : ℝ => t ^ 2) (2 * Y) Y := by
    simpa [pow_succ, pow_one] using (hasDerivAt_pow 2 Y)
  have hnum : HasDerivAt (fun t : ℝ => lam * t ^ 2) (2 * lam * Y) Y := by
    simpa [mul_assoc, mul_comm, mul_left_comm] using hp2.const_mul lam
  have hden : HasDerivAt (fun t : ℝ => 1 + lam * t) lam Y := by
    simpa [add_comm] using ((hasDerivAt_id Y).const_mul lam).add_const 1
  have hdenN : 1 + lam * Y ≠ 0 := by nlinarith [hlam, hY]
  have hd := hnum.div hden hdenN
  have hval : (2 * lam * Y * (1 + lam * Y) - lam * Y ^ 2 * lam) / (1 + lam * Y) ^ 2
      = mufun lam Y := kfun_deriv_value lam Y hdenN
  have hfunex : (fun t : ℝ => lam * t ^ 2) / (fun t : ℝ => 1 + lam * t) =
      fun t : ℝ => lam * t ^ 2 / (1 + lam * t) := by
    funext t
    rfl
  rwa [hfunex, hval] at hd

-- --------------------------------------------------------------------------
-- Saturation: p_lam → 1 and mu_lam → 1 as Y → +∞
-- --------------------------------------------------------------------------

lemma one_add_lam_tendsto_atTop (lam : ℝ) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => 1 + lam * Y) atTop atTop := by
  have hlamY : Tendsto (fun Y : ℝ => lam * Y) atTop atTop := by
    simpa [mul_comm] using (tendsto_id.atTop_mul_const hlam)
  have hle : (fun Y : ℝ => lam * Y) ≤ᶠ[atTop] (fun Y : ℝ => 1 + lam * Y) := by
    filter_upwards with Y
    nlinarith
  exact tendsto_atTop_mono' atTop hle hlamY

lemma inv_tendsto_zero (lam : ℝ) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => (1 + lam * Y)⁻¹) atTop (𝓝 0) := by
  exact (one_add_lam_tendsto_atTop lam hlam).inv_tendsto_atTop

lemma inv_sq_tendsto_zero (lam : ℝ) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => ((1 + lam * Y) ^ 2)⁻¹) atTop (𝓝 0) := by
  have htop := one_add_lam_tendsto_atTop lam hlam
  have hsq : Tendsto (fun Y : ℝ => (1 + lam * Y) ^ 2) atTop atTop := by
    have hcomp : Tendsto ((fun x : ℝ => x ^ 2) ∘ (fun Y : ℝ => 1 + lam * Y))
        atTop atTop := (tendsto_pow_atTop (by norm_num : (2 : ℕ) ≠ 0)).comp htop
    have hfunex : (fun x : ℝ => x ^ 2) ∘ (fun Y : ℝ => 1 + lam * Y) =
        fun Y : ℝ => (1 + lam * Y) ^ 2 := by
      funext Y
      rfl
    exact hfunex ▸ hcomp
  exact hsq.inv_tendsto_atTop

theorem pfun_tendsto_one (lam : ℝ) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => pfun lam Y) atTop (𝓝 1) := by
  have hzew : EventuallyEq atTop (fun Y : ℝ => pfun lam Y)
      (fun Y : ℝ => 1 - (1 + lam * Y)⁻¹) := by
    rw [EventuallyEq]
    rw [eventually_atTop]
    refine ⟨0, ?_⟩
    intro Y hY
    have hden : 1 + lam * Y ≠ 0 := by nlinarith [hlam, hY]
    have hm : 1 - pfun lam Y = (1 + lam * Y)⁻¹ := one_sub_pfun lam Y hden
    nlinarith
  refine Tendsto.congr' hzew.symm ?_
  simpa using tendsto_const_nhds.sub (inv_tendsto_zero lam hlam)

theorem mufun_tendsto_one (lam : ℝ) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => mufun lam Y) atTop (𝓝 1) := by
  have hzew : EventuallyEq atTop (fun Y : ℝ => mufun lam Y)
      (fun Y : ℝ => 1 - ((1 + lam * Y) ^ 2)⁻¹) := by
    rw [EventuallyEq]
    rw [eventually_atTop]
    refine ⟨0, ?_⟩
    intro Y hY
    exact mufun_eq_inv lam Y (by nlinarith [hlam, hY])
  refine Tendsto.congr' hzew.symm ?_
  simpa using tendsto_const_nhds.sub (inv_sq_tendsto_zero lam hlam)

-- --------------------------------------------------------------------------
-- Deep spherical matching: κ = a0/s = 1/(2lam)
--    r²·(2lam/s)·g² = G·M   ⇒   g² = s·G·M/(2·lam·r²) = (s/(2lam))·(G·M/r²)
-- --------------------------------------------------------------------------

theorem deep_matching_kappa (lam s G M r g : ℝ)
    (hlam : 0 < lam) (hs : 0 < s) (hr : 0 < r)
    (h : r ^ 2 * (2 * lam / s) * g ^ 2 = G * M) :
    g ^ 2 = s * G * M / (2 * lam * r ^ 2) := by
  have hlam' : 2 * lam ≠ 0 := by nlinarith
  field_simp [ne_of_gt hlam, ne_of_gt hs, ne_of_gt hr, hlam'] at h ⊢
  nlinarith [h]

theorem deep_matching_a0_line (lam s G M r g : ℝ)
    (hlam : 0 < lam) (hs : 0 < s) (hr : 0 < r)
    (h : r ^ 2 * (2 * lam / s) * g ^ 2 = G * M) :
    g ^ 2 = (s / (2 * lam)) * (G * M / r ^ 2) := by
  have hlam' : 2 * lam ≠ 0 := by nlinarith
  field_simp [ne_of_gt hlam, ne_of_gt hs, ne_of_gt hr, hlam'] at h ⊢
  nlinarith [h]

-- κ = a0/s = 1/(2lam) with a0 := s/(2lam)  (the a0-line g² = a0·g_N)
theorem kappa_from_matching (lam : ℝ) (hlam : 0 < lam) (s : ℝ) (hs : s ≠ 0) :
    (s / (2 * lam)) / s = 1 / (2 * lam) := by
  have hlam' : 2 * lam ≠ 0 := by nlinarith
  field_simp [hs, hlam', ne_of_gt hlam]

end AS053

#print axioms AS053.pfun_zero
#print axioms AS053.pfun_hasDerivAt_zero
#print axioms AS053.mufun_zero
#print axioms AS053.mufun_hasDerivAt_zero
#print axioms AS053.kfun_hasDerivAt
#print axioms AS053.pfun_tendsto_one
#print axioms AS053.mufun_tendsto_one
#print axioms AS053.deep_matching_kappa
#print axioms AS053.deep_matching_a0_line
#print axioms AS053.kappa_from_matching