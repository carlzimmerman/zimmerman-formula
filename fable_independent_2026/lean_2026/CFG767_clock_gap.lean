import Mathlib

/-!
# CFG767: Lean certificates for the formation clock (CFG763/764) and the P-wave gap algebra (CFG760/761)

Criteria: campaign_fresh_gravity/CFG767_lean_clock_gap/FROZEN_CRITERIA.md (5dc0650d4), committed before this file.
Formation fraction f(t, τ) = 1 − e^{−t/τ}. Certified: monotonicity in t and τ, bounds, the prediction window, the SPARC upper bound
τ ≤ t/ln 10, evanescence below the gap, and the deep-limit c_P,max. Algebra/analysis only: no physics or data verdict is certified.
κ = ½ is FITTED (unused); nothing here says the theory is closed.
-/

open Real

namespace CFG767

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
theorem frac_anti_tau {t τ₁ τ₂ : ℝ} (ht : 0 < t) (h1 : 0 < τ₁) (h12 : τ₁ < τ₂) : frac t τ₂ < frac t τ₁ := by
  simp only [frac]
  have h2 : 0 < τ₂ := by linarith
  have hd : t / τ₂ < t / τ₁ := by rw [div_lt_div_iff₀ h2 h1]; nlinarith
  have h : -t / τ₁ < -t / τ₂ := by rw [neg_div, neg_div]; linarith
  have := Real.exp_lt_exp.mpr h
  linarith

/-- non-strict version used for the window -/
lemma frac_anti_tau_le {t τ₁ τ₂ : ℝ} (ht : 0 ≤ t) (h1 : 0 < τ₁) (h12 : τ₁ ≤ τ₂) : frac t τ₂ ≤ frac t τ₁ := by
  simp only [frac]
  have h2 : 0 < τ₂ := by linarith
  have hd : t / τ₂ ≤ t / τ₁ := by rw [div_le_div_iff₀ h2 h1]; nlinarith
  have h : -t / τ₁ ≤ -t / τ₂ := by rw [neg_div, neg_div]; linarith
  have := Real.exp_le_exp.mpr h
  linarith

/-- C3: the fraction lies in [0, 1). -/
theorem frac_bounds {t τ : ℝ} (ht : 0 ≤ t) (hτ : 0 < τ) : 0 ≤ frac t τ ∧ frac t τ < 1 := by
  simp only [frac]
  have hn : -t / τ ≤ 0 := by rw [neg_div]; exact neg_nonpos.mpr (div_nonneg ht hτ.le)
  have h1 := Real.exp_le_one_iff.mpr hn
  have h0 := Real.exp_pos (-t / τ)
  constructor <;> linarith

/-- C4: CFG763's prediction band. -/
theorem window {t τ τmin τmax : ℝ} (ht : 0 < t) (hmin : 0 < τmin) (h1 : τmin ≤ τ) (h2 : τ ≤ τmax) :
    frac t τmax ≤ frac t τ ∧ frac t τ ≤ frac t τmin :=
  ⟨frac_anti_tau_le ht.le (by linarith) h2, frac_anti_tau_le ht.le hmin h1⟩

/-- C5: f ≥ 9/10 after time t iff τ ≤ t / ln 10 (the SPARC upper bound). -/
theorem sparc_upper {t τ : ℝ} (ht : 0 < t) (hτ : 0 < τ) : 9 / 10 ≤ frac t τ ↔ τ ≤ t / Real.log 10 := by
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

/-- C6: below the local gap the perturbation does not propagate (k² < 0). -/
theorem below_gap_evanescent {ω s v : ℝ} (hgap : ω ^ 2 < 2 * v / s + 2 / s ^ 2) : ω ^ 2 - 2 / s ^ 2 - 2 * v / s < 0 := by
  linarith

/-- C7: the deep-limit c_P,max = V/(x ω_g s₀) with ω_g = √(2/s₀) equals V/(x √(2 s₀)). -/
theorem deep_gap_cp {V x s0 : ℝ} (hs : 0 < s0) :
    V / (x * √(2 / s0) * s0) = V / (x * √(2 * s0)) := by
  have h2 : 2 * s0 = (2 / s0) * s0 ^ 2 := by field_simp
  have hk : √(2 / s0) * s0 = √(2 * s0) := by
    rw [h2, Real.sqrt_mul (by positivity), Real.sqrt_sq hs.le]
  rw [mul_assoc, hk]

end CFG767

open CFG767 in
#print axioms frac_mono_t
open CFG767 in
#print axioms frac_anti_tau
open CFG767 in
#print axioms frac_bounds
open CFG767 in
#print axioms window
open CFG767 in
#print axioms sparc_upper
open CFG767 in
#print axioms below_gap_evanescent
open CFG767 in
#print axioms deep_gap_cp
