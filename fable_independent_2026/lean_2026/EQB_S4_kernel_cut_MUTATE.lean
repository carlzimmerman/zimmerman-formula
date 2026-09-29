import Mathlib

/-!
# EQB_S4a -- the framework kernel on its cut: unitarity circle, phase lag, spectral dichotomy (Lean 4 certificate)

Source (committed): `prep_2026/equation_book/s4_kernel_spectral.py`, checks E-S4-2 / E-S4-3 (lines 165-205:
boundary value, |K| = 1, Im K = 1/(2W), Re K, drift identity, below-edge dissipative branch); write-up `MINE_M2.md` item 8.

PREMISES (declared, NOT certified as physics):
  * the kernel K(z) = (sqrt(1 + 4z) - 1)/(2 sqrt z) of the published action;
  * the frequency map z = -W^2 (W = c omega/a0 > 0) approached from the upper half plane, z = -W^2 + i0.  The principal square
    roots at that boundary point are
        sqrt(1 + 4z) -> i sqrt(4 W^2 - 1)   (W > 1/2, since 1 + 4z = 1 - 4W^2 < 0 with Im > 0)
        sqrt(1 + 4z) ->   sqrt(1 - 4 W^2)   (W < 1/2, real)
        sqrt(z)      -> i W
    These branch values are taken as the DEFINITION of the boundary value (the script derives them by a sympy limit; that limit is not
    re-proved in Lean).  The reading of K as an operator on worldlines ("Reading B") is the script's, and the script flags it as excluded
    in the drift channel: these are exact consequences of the operator, not endorsed phenomenology.

CERTIFIED (premises => conclusions):
  * `cut_above_eq`     : for W > 1/2, K(-W^2 + i0) = (sqrt(4W^2 - 1) + i)/(2W)
  * `cut_above_normSq` : |K|^2 = 1 exactly (the unitarity circle);  `cut_above_re`, `cut_above_im`: Re K = sqrt(4W^2-1)/(2W), Im K = 1/(2W)
  * `phase_lag`        : Re K = cos phi, Im K = sin phi with phi = arcsin(1/(2W)) (= arcsin(a0/(2 c omega)))
  * `drift_identity`   : 2 omega Im K = a0/c  with W = c omega/a0
  * `cut_below_eq`     : for 0 < W < 1/2, K = i (1 - sqrt(1 - 4W^2))/(2W): purely imaginary (Re K = 0), and 0 < Im K < 1, so |K| < 1
  * `cut_edge`         : at W = 1/2 both formulas give K = i
NOT certified: the branch values themselves (premises), that the boundary value is the physically relevant response, the time-domain
memory function and Bessel/Struve closed form (E-S4-1: numerical mpmath checks only), the inverse-moment family (E-S4-4), the wide-binary
numbers (E-S4-5).  kappa = 1/2 (FITTED) does not enter.
-/

open Real Complex

noncomputable section

/-- boundary value of K above the edge, from the declared branch values. -/
def Kabove (W : ℝ) : ℂ := (Complex.I * (Real.sqrt (4 * W ^ 2 - 1) : ℝ) - 1) / (2 * (Complex.I * (W : ℂ)))

/-- boundary value of K below the edge. -/
def Kbelow (W : ℝ) : ℂ := ((Real.sqrt (1 - 4 * W ^ 2) : ℝ) - 1) / (2 * (Complex.I * (W : ℂ)))

theorem re_mk (p q : ℝ) : (((p : ℝ) : ℂ) + ((q : ℝ) : ℂ) * Complex.I).re = p := by simp
theorem im_mk (p q : ℝ) : (((p : ℝ) : ℂ) + ((q : ℝ) : ℂ) * Complex.I).im = q := by simp

theorem cut_above_eq {W : ℝ} (hW : 0 < W) :
    Kabove W = ((Real.sqrt (4 * W ^ 2 - 1) / (2 * W) : ℝ) : ℂ) + ((1 / (2 * W) : ℝ) : ℂ) * Complex.I := by
  unfold Kabove
  have hW0 : (W : ℂ) ≠ 0 := by exact_mod_cast hW.ne'
  push_cast
  field_simp
  ring_nf
  simp [Complex.I_sq]
  ring

theorem cut_above_re {W : ℝ} (hW : 0 < W) : (Kabove W).re = Real.sqrt (4 * W ^ 2 - 1) / (2 * W) := by
  rw [cut_above_eq hW]; exact re_mk _ _

theorem cut_above_im {W : ℝ} (hW : 0 < W) : (Kabove W).im = 1 / W := by
  rw [cut_above_eq hW]; exact im_mk _ _

/-- the unitarity circle: |K|^2 = 1 for W > 1/2. -/
theorem cut_above_normSq {W : ℝ} (hW : 1 / 2 < W) : Complex.normSq (Kabove W) = 1 := by
  have hW0 : 0 < W := by linarith
  rw [Complex.normSq_apply, cut_above_re hW0, cut_above_im hW0]
  have h4 : 0 ≤ 4 * W ^ 2 - 1 := by nlinarith
  have hs := Real.sq_sqrt h4
  have hne : W ≠ 0 := hW0.ne'
  field_simp
  nlinarith [hs]

theorem cut_above_norm {W : ℝ} (hW : 1 / 2 < W) : ‖Kabove W‖ = 1 := by
  have h := cut_above_normSq hW
  have h2 : ‖Kabove W‖ ^ 2 = 1 := by rw [Complex.sq_norm]; exact h
  have h0 : 0 ≤ ‖Kabove W‖ := norm_nonneg _
  nlinarith [h2, h0]

/-- phase-lag law: K = cos phi + i sin phi with sin phi = 1/(2W), phi = arcsin(1/(2W)). -/
theorem phase_lag {W : ℝ} (hW : 1 / 2 < W) :
    (Kabove W).im = Real.sin (Real.arcsin (1 / (2 * W))) ∧
    (Kabove W).re = Real.cos (Real.arcsin (1 / (2 * W))) := by
  have hW0 : 0 < W := by linarith
  have hle : 1 / (2 * W) ≤ 1 := by
    rw [div_le_one (by positivity)]; linarith
  have hge : -1 ≤ 1 / (2 * W) := by
    have : 0 < 1 / (2 * W) := by positivity
    linarith
  constructor
  · rw [Real.sin_arcsin hge hle, cut_above_im hW0]
  · rw [Real.cos_arcsin, cut_above_re hW0]
    have h4 : 0 ≤ 4 * W ^ 2 - 1 := by nlinarith
    have hne : W ≠ 0 := hW0.ne'
    have : 1 - (1 / (2 * W)) ^ 2 = (4 * W ^ 2 - 1) / (2 * W) ^ 2 := by field_simp; ring
    rw [this, Real.sqrt_div h4, Real.sqrt_sq (by positivity)]

theorem drift_identity {a0 c ω : ℝ} (ha : 0 < a0) (hc : 0 < c) (hω : 0 < ω) :
    2 * ω * (1 / (2 * (c * ω / a0))) = a0 / c := by
  field_simp

theorem cut_below_eq {W : ℝ} (hW : 0 < W) :
    Kbelow W = ((0 : ℝ) : ℂ) + (((1 - Real.sqrt (1 - 4 * W ^ 2)) / (2 * W) : ℝ) : ℂ) * Complex.I := by
  unfold Kbelow
  have hW0 : (W : ℂ) ≠ 0 := by exact_mod_cast hW.ne'
  push_cast
  field_simp
  ring_nf
  simp [Complex.I_sq]
  ring

theorem cut_below_re {W : ℝ} (hW : 0 < W) : (Kbelow W).re = 0 := by
  rw [cut_below_eq hW]; exact re_mk _ _

theorem cut_below_im_bounds {W : ℝ} (hW : 0 < W) (hW2 : W < 1 / 2) :
    0 < (Kbelow W).im ∧ (Kbelow W).im < 1 := by
  rw [cut_below_eq hW, im_mk]
  have h1 : 0 < 1 - 4 * W ^ 2 := by nlinarith
  have hs0 : 0 < Real.sqrt (1 - 4 * W ^ 2) := Real.sqrt_pos.mpr h1
  have hs2 := Real.sq_sqrt h1.le
  have hs1 : Real.sqrt (1 - 4 * W ^ 2) < 1 := by nlinarith
  constructor
  · apply div_pos (by linarith) (by positivity)
  · rw [div_lt_one (by positivity)]
    nlinarith

theorem cut_edge : Kabove (1 / 2) = Complex.I ∧ Kbelow (1 / 2) = Complex.I := by
  have h1 : Real.sqrt (4 * (1 / 2 : ℝ) ^ 2 - 1) = 0 := by norm_num
  have h2 : Real.sqrt (1 - 4 * (1 / 2 : ℝ) ^ 2) = 0 := by norm_num
  constructor
  · unfold Kabove; rw [h1]; push_cast; field_simp; ring_nf; simp [Complex.I_sq]
  · unfold Kbelow; rw [h2]; push_cast; field_simp; ring_nf; simp [Complex.I_sq]

end

#print axioms cut_above_eq
#print axioms cut_above_normSq
#print axioms cut_above_norm
#print axioms phase_lag
#print axioms drift_identity
#print axioms cut_below_eq
#print axioms cut_below_im_bounds
#print axioms cut_edge
