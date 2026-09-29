import Mathlib

/-!
# M3F -- (i) the chord bound for a concave local gate; (ii) York time ticks on dust FRW while Lambda is conserved

(i) Source: `real_research/derivation_chain_2026/FP3_cosmology_linear.py`, check C3 (lines 391-434) and
CHAIN_STATUS row G1i: "a concave W >= 0 with W(0) >= 0 has W(rho)/rho non-increasing, so W(rho) <=
(rho/rho_bar) W(rho_bar)".  NOTE: the script does NOT prove this; it tests 4000 random concave gates
numerically.  The mathematics is the elementary theorem certified here.  Lean corpus check: DE7's
`concave` lemmas concern the plateau-gate / slip floor, not the chord bound.

  * `chord_slope_antitone` : ConcaveOn R (Ici 0) W and W 0 >= 0  =>  for 0 < a <= b, W b / b <= W a / a.
  * `chord_bound`          : hence W(rho) <= (rho/rho_bar) W(rho_bar) for rho >= rho_bar > 0, and if
                             W(rho_bar) <= f then W(rho) <= (rho/rho_bar) f (the FP3 "half-on radius" input).
  * `linear_gate_saturates`: the bound is attained by the concave linear gate W(u) = u (equality for all r, rb).

(ii) Source: `real_research/cross_thread_review_2026_09_26/XR30_one_clock.py`, check M2 (lines 377-394):
"on dust FRW dK/dt = -12 pi G rho_m ... Q = K^2/3 - 8 pi G rho_m = Lambda_0".  Here K = 3H, dust obeys
rho' = -3 H rho, and Friedmann H^2 = (8 pi G/3) rho + Lambda/3 holds at all times with Lambda constant.
  * `York_time_ticks`      : H' = -4 pi G rho and K' = -12 pi G rho  (H != 0);
  * `Q_conserved`          : Q = K^2/3 - 8 pi G rho = Lambda at every time (so Q' = 0);
  * `K_frozen_iff`         : K' = 0 iff rho = 0 (G > 0), i.e. an identification Lambda == F(K) with F' != 0 freezes
                             K only on empty space (the script's "MB" no-merge argument, algebraic part only);
  * `K_sq_floor`           : K^2 = 3 Lambda + 24 pi G rho >= 3 Lambda.
NOT CERTIFIED: the action-level derivation of Friedmann/Raychaudhuri from the unimodular + khronon action,
the merger-candidate analysis (M3, MA, MC, SQ), the Dirac counts, E(z) numbers.  No physical claim is an axiom;
kappa = 1/2 is not involved.
-/

noncomputable section
namespace M3F

/-! ### (i) chord bound -/

theorem chord_slope_antitone (W : ℝ → ℝ) (hW : ConcaveOn ℝ (Set.Ici (0 : ℝ)) W) (h0 : 0 ≤ W 0)
    {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) : W b / b ≤ W a / a := by
  have hb : 0 < b := lt_of_lt_of_le ha hab
  have hmem0 : (0 : ℝ) ∈ Set.Ici (0 : ℝ) := Set.mem_Ici.mpr le_rfl
  have hmemb : b ∈ Set.Ici (0 : ℝ) := Set.mem_Ici.mpr hb.le
  have hl0 : 0 ≤ a / b := by positivity
  have hl1 : 0 ≤ 1 - a / b := by
    have : a / b ≤ 1 := (div_le_one hb).mpr hab
    linarith
  have hcomb : (a / b) • b + (1 - a / b) • (0 : ℝ) = a := by
    simp only [smul_eq_mul]; field_simp; ring
  have h := hW.2 hmemb hmem0 hl0 hl1 (by ring)
  rw [hcomb] at h
  simp only [smul_eq_mul] at h
  -- (a/b) W b + (1-a/b) W 0 <= W a
  have h2 : a / b * W b ≤ W a := by
    have : 0 ≤ (1 - a / b) * W 0 := mul_nonneg hl1 h0
    linarith
  rw [div_le_div_iff₀ hb ha]
  have := mul_le_mul_of_nonneg_left h2 hb.le
  have e : b * (a / b * W b) = a * W b := by field_simp
  rw [e] at this
  linarith

theorem chord_bound (W : ℝ → ℝ) (hW : ConcaveOn ℝ (Set.Ici (0 : ℝ)) W) (h0 : 0 ≤ W 0)
    {rb r f : ℝ} (hrb : 0 < rb) (hle : rb ≤ r) (hf : W rb ≤ f) :
    W r ≤ (r / rb) * W rb ∧ W r ≤ (r / rb) * f := by
  have hr : 0 < r := lt_of_lt_of_le hrb hle
  have h := chord_slope_antitone W hW h0 hrb hle
  have h1 : W r ≤ (r / rb) * W rb := by
    rw [div_le_div_iff₀ hr hrb] at h
    have : W r ≤ r * W rb / rb := by
      rw [le_div_iff₀ hrb]; linarith
    calc W r ≤ r * W rb / rb := this
      _ = (r / rb) * W rb := by ring
  refine ⟨h1, ?_⟩
  have : 0 ≤ r / rb := by positivity
  calc W r ≤ (r / rb) * W rb := h1
    _ ≤ (r / rb) * f := mul_le_mul_of_nonneg_left hf this

/-- the bound is attained by a concave linear gate: W(u) = u (so W(r) = (r/rb) W(rb)). -/
theorem linear_gate_saturates (rb r : ℝ) (hrb : 0 < rb) :
    (fun u : ℝ => u) r = (r / rb) * (fun u : ℝ => u) rb := by
  simp only
  field_simp

/-! ### (ii) York time -/

theorem York_time_ticks (G Λ : ℝ) (H ρ : ℝ → ℝ) (t h' : ℝ)
    (hH : HasDerivAt H h' t) (hρ : HasDerivAt ρ (-3 * H t * ρ t) t)
    (hF : ∀ s, H s ^ 2 = 8 * Real.pi * G / 3 * ρ s + Λ / 3) (hne : H t ≠ 0) :
    h' = -4 * Real.pi * G * ρ t ∧
    HasDerivAt (fun s => 3 * H s) (-12 * Real.pi * G * ρ t) t := by
  have h1 : HasDerivAt (fun s => H s ^ 2) (2 * H t * h') t := by
    have := hH.pow 2
    refine this.congr_deriv ?_
    simp
  have h2 : HasDerivAt (fun s => 8 * Real.pi * G / 3 * ρ s + Λ / 3)
      (8 * Real.pi * G / 3 * (-3 * H t * ρ t)) t := by
    have := (hρ.const_mul (8 * Real.pi * G / 3)).add_const (Λ / 3)
    exact this
  have hfun : (fun s => H s ^ 2) = fun s => 8 * Real.pi * G / 3 * ρ s + Λ / 3 := funext hF
  rw [hfun] at h1
  have huniq := h1.unique h2
  have hh : h' = -4 * Real.pi * G * ρ t := by
    have : H t * (2 * h') = H t * (-8 * Real.pi * G * ρ t) := by linarith
    have h3 := mul_left_cancel₀ hne this
    linarith
  refine ⟨hh, ?_⟩
  have := hH.const_mul 3
  refine this.congr_deriv ?_
  rw [hh]; ring

theorem Q_conserved (G Λ H ρ : ℝ) (hF : H ^ 2 = 8 * Real.pi * G / 3 * ρ + Λ / 3) :
    (3 * H) ^ 2 / 3 - 8 * Real.pi * G * ρ = Λ := by
  nlinarith

theorem K_frozen_iff (G ρ : ℝ) (hG : 0 < G) :
    -12 * Real.pi * G * ρ = 0 ↔ ρ = 0 := by
  have hp : 0 < Real.pi := Real.pi_pos
  have hn : -12 * Real.pi * G ≠ 0 := by
    have : 0 < 12 * Real.pi * G := by positivity
    intro h; linarith
  constructor
  · intro h
    have : (-12 * Real.pi * G) * ρ = 0 := h
    rcases mul_eq_zero.mp this with h1 | h1
    · exact absurd h1 hn
    · exact h1
  · intro h; rw [h]; ring

theorem K_sq_floor (G Λ H ρ : ℝ) (hG : 0 < G) (hρ : 0 ≤ ρ)
    (hF : H ^ 2 = 8 * Real.pi * G / 3 * ρ + Λ / 3) :
    (3 * H) ^ 2 = 3 * Λ + 24 * Real.pi * G * ρ ∧ 3 * Λ ≤ (3 * H) ^ 2 := by
  have hp : 0 < Real.pi := Real.pi_pos
  have e : (3 * H) ^ 2 = 3 * Λ + 24 * Real.pi * G * ρ := by nlinarith
  refine ⟨e, ?_⟩
  have : 0 ≤ 24 * Real.pi * G * ρ := by positivity
  linarith

end M3F

#print axioms M3F.chord_slope_antitone
#print axioms M3F.chord_bound
#print axioms M3F.linear_gate_saturates
#print axioms M3F.York_time_ticks
#print axioms M3F.Q_conserved
#print axioms M3F.K_frozen_iff
#print axioms M3F.K_sq_floor
