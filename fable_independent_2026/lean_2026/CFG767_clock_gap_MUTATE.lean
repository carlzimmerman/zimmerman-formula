import Mathlib

/-! CFG767 MUTATE twin (criteria 5dc0650d4): C2 reversed and C5 with ln 9; both must FAIL. -/

open Real

namespace CFG767M
/-- the formation fraction -/
noncomputable def frac (t τ : ℝ) : ℝ := 1 - Real.exp (-t / τ)

/-- C1: more time, more cold energy. -/
theorem frac_mono_t {τ : ℝ} (hτ : 0 < τ) : StrictMono (fun t => frac t τ) := by
  intro a b hab
  simp only [frac]
  have h : -b / τ < -a / τ := (div_lt_div_iff_of_pos_right hτ).mpr (by linarith)
  have := Real.exp_lt_exp.mpr h
  linarith

/-- C2: slower formation, less cold energy. -/
theorem frac_anti_tau_MUTATE {t τ₁ τ₂ : ℝ} (ht : 0 < t) (h1 : 0 < τ₁) (h12 : τ₁ < τ₂) : frac t τ₁ < frac t τ₂ := by
  simp only [frac]
  have h2 : 0 < τ₂ := by linarith
  have hd : t / τ₂ < t / τ₁ := by rw [div_lt_div_iff₀ h2 h1]; nlinarith
  have h : -t / τ₁ < -t / τ₂ := by rw [neg_div, neg_div]; linarith
  have := Real.exp_lt_exp.mpr h
  linarith

/-- C5: f ≥ 9/10 after time t iff τ ≤ t / ln 10 (the SPARC upper bound). -/
theorem sparc_upper_MUTATE {t τ : ℝ} (ht : 0 < t) (hτ : 0 < τ) : 9 / 10 ≤ frac t τ ↔ τ ≤ t / Real.log 9 := by
  simp only [frac]
  have h10 : 0 < Real.log 10 := Real.log_pos (by norm_num)
  have he : Real.exp (-Real.log 10) = 1 / 10 := by rw [Real.exp_neg, Real.exp_log (by norm_num)]; norm_num
  rw [le_div_iff₀ h10]
  constructor
  · intro h
    have h' : Real.exp (-t / τ) ≤ Real.exp (-Real.log 10) := by rw [he]; linarith
    have hl := Real.exp_le_exp.mp h'
    rw [neg_div] at hl
    have : Real.log 10 ≤ t / τ := by linarith
    rw [le_div_iff₀ hτ] at this
    linarith
  · intro h
    have : Real.log 10 ≤ t / τ := by rw [le_div_iff₀ hτ]; linarith
    have hl : -t / τ ≤ -Real.log 10 := by rw [neg_div]; linarith
    have := Real.exp_le_exp.mpr hl
    rw [he] at this
    linarith

end CFG767M
