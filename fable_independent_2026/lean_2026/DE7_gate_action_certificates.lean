/-
DE7 -- the vacuum gate varied as an action term: certificates for the algebra and calculus the lane rests on.

real_research/dark_energy_2026/DE7_gate_action_term_mond_normalised.py computes the numbers; these theorems certify
the structural steps:
  * any C^2 gate with an off-plateau (f = 0, f' = 0 at t = 0) and an on-plateau (f = 1, f' = 0 at t = 1) has
    f'' > 0 somewhere AND f'' < 0 somewhere on (0, 1) -- the mean value theorem, twice (T1);
  * on the no-ghost branch Delta < 0 the effective k^4 coefficient obeys E_* = E - D^2/Delta >= E (T1 ii);
  * so B f'' t_R^2 > 0 somewhere forces E_* > 0 there, and with F > 0 the k^4 dispersion coefficient
    d4 = -16 E_*/(9F) is negative: growth ~ k^2, Hadamard ill-posed without a repair term;
  * the Lambda-scaled repair keeps Delta < 0 in voids iff eta <= 3 c2/(2 pi) (arctan < pi/2);
  * any repair concave by at least m on an interval loses at least m x (length) of C_R across it (the slip floor);
  * the static trace-free equation (M^2/2)(phi - psi) + G_R = 0 gives psi - phi = 2 G_R/M^2 (S4);
  * the gate's half activation is u = x_c0; the contrast door's FRW background (u = 0) is off-plateau for 0 < w <= 1;
    the absolute door's is off-plateau iff u_FRW <= x_c0 (1 - w); p = 1 reduces to 27 Lambda R/(8 x_c K^4).
Standard axioms only, no sorry.
-/
import Mathlib

open Set

namespace DE7

/-- T1 (i): a C^2 plateau gate is convex somewhere and concave somewhere on its transition. -/
theorem plateau_gate_both_signs (f : ℝ → ℝ) (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f))
    (h0 : f 0 = 0) (h1 : f 1 = 1) (hd0 : deriv f 0 = 0) (hd1 : deriv f 1 = 0) :
    (∃ t ∈ Ioo (0 : ℝ) 1, 0 < deriv (deriv f) t) ∧ (∃ t ∈ Ioo (0 : ℝ) 1, deriv (deriv f) t < 0) := by
  obtain ⟨c, hc, hfc⟩ := exists_deriv_eq_slope f (by norm_num : (0 : ℝ) < 1)
    hf.continuous.continuousOn hf.differentiableOn
  rw [h1, h0] at hfc
  norm_num at hfc
  obtain ⟨hc0, hc1⟩ := hc
  constructor
  · obtain ⟨t, ht, hft⟩ := exists_deriv_eq_slope (deriv f) hc0 hf'.continuous.continuousOn hf'.differentiableOn
    refine ⟨t, ⟨ht.1, lt_trans ht.2 hc1⟩, ?_⟩
    rw [hft, hfc, hd0]
    exact div_pos (by norm_num) (by linarith)
  · obtain ⟨t, ht, hft⟩ := exists_deriv_eq_slope (deriv f) hc1 hf'.continuous.continuousOn hf'.differentiableOn
    refine ⟨t, ⟨lt_trans hc0 ht.1, ht.2⟩, ?_⟩
    rw [hft, hfc, hd1]
    exact div_neg_of_neg_of_pos (by norm_num) (by linarith)

/-- T1 (ii): on the no-ghost branch the mixing term only raises the k^4 coefficient. -/
theorem estar_ge_E (E D Δ : ℝ) (hΔ : Δ < 0) : E ≤ E - D ^ 2 / Δ := by
  have : D ^ 2 / Δ ≤ 0 := div_nonpos_of_nonneg_of_nonpos (sq_nonneg D) hΔ.le
  linarith

/-- where B f'' > 0 (t_R ≠ 0) the unrepaired k^4 coefficient is positive. -/
theorem estar_pos_where_convex (B fpp tR D Δ : ℝ) (hB : 0 < B) (hf : 0 < fpp) (ht : tR ≠ 0) (hΔ : Δ < 0) :
    0 < B * fpp * tR ^ 2 - D ^ 2 / Δ := by
  have hE : 0 < B * fpp * tR ^ 2 := mul_pos (mul_pos hB hf) (by positivity)
  have := estar_ge_E (B * fpp * tR ^ 2) D Δ hΔ
  linarith

/-- the same for B < 0 where f'' < 0 (the gate's concave half). -/
theorem estar_pos_where_concave_negB (B fpp tR D Δ : ℝ) (hB : B < 0) (hf : fpp < 0) (ht : tR ≠ 0) (hΔ : Δ < 0) :
    0 < B * fpp * tR ^ 2 - D ^ 2 / Δ := by
  have hE : 0 < B * fpp * tR ^ 2 := mul_pos (mul_pos_of_neg_of_neg hB hf) (by positivity)
  have := estar_ge_E (B * fpp * tR ^ 2) D Δ hΔ
  linarith

/-- with a healthy kinetic sign F > 0, E_* > 0 makes the k^4 dispersion coefficient negative (ill-posed). -/
theorem d4_negative (Es F : ℝ) (hE : 0 < Es) (hF : 0 < F) : -16 * Es / (9 * F) < 0 := by
  have : 0 < 16 * Es / (9 * F) := div_pos (by linarith) (by linarith)
  have h : -16 * Es / (9 * F) = -(16 * Es / (9 * F)) := by ring
  rw [h]; linarith

/-- the Lambda-scaled repair's void ceiling: Delta_void = -c2 + (4/3) eta arctan|R| < 0 whenever eta <= 3 c2/(2 pi). -/
theorem void_ceiling (c2 η x : ℝ) (hc : 0 < c2) (hη0 : 0 ≤ η) (hη : η ≤ 3 * c2 / (2 * Real.pi)) :
    -c2 + 4 / 3 * η * Real.arctan x < 0 := by
  have ha : Real.arctan x < Real.pi / 2 := Real.arctan_lt_pi_div_two x
  have hpi : 0 < Real.pi := Real.pi_pos
  rcases hη0.lt_or_eq with hpos | hzero
  · have h1 : 4 / 3 * η * Real.arctan x < 4 / 3 * η * (Real.pi / 2) := by
      have : 0 < 4 / 3 * η := by positivity
      exact mul_lt_mul_of_pos_left ha this
    have h2 : 4 / 3 * η * (Real.pi / 2) ≤ c2 := by
      have := mul_le_mul_of_nonneg_left hη (by positivity : (0 : ℝ) ≤ 2 * Real.pi / 3)
      have e : 2 * Real.pi / 3 * (3 * c2 / (2 * Real.pi)) = c2 := by field_simp
      calc 4 / 3 * η * (Real.pi / 2) = 2 * Real.pi / 3 * η := by ring
        _ ≤ 2 * Real.pi / 3 * (3 * c2 / (2 * Real.pi)) := this
        _ = c2 := e
    linarith
  · subst hzero; simp; linarith

/-- the repair's slip floor: C concave by at least m on [a, b] loses at least m (b - a) of C_R across it. -/
theorem repair_slope_drop (C : ℝ → ℝ) (a b m : ℝ) (hab : a < b) (hC : Differentiable ℝ (deriv C))
    (hconc : ∀ t ∈ Ioo a b, deriv (deriv C) t ≤ -m) :
    deriv C b - deriv C a ≤ -m * (b - a) := by
  obtain ⟨c, hc, hfc⟩ := exists_deriv_eq_slope (deriv C) hab hC.continuous.continuousOn hC.differentiableOn
  have hba : 0 < b - a := by linarith
  have h := hconc c hc
  rw [hfc] at h
  have := (div_le_iff₀ hba).mp h
  linarith

/-- S4: the static trace-free metric equation gives the slip psi - phi = 2 G_R/M^2. -/
theorem slip_from_tracefree (M2 φ ψ GR : ℝ) (hM : M2 ≠ 0) (h : M2 / 2 * (φ - ψ) + GR = 0) :
    ψ - φ = 2 * GR / M2 := by
  field_simp
  linarith

/-- the gate's half activation: t = (u/x_c0 - 1)/(2w) + 1/2 equals 1/2 exactly at u = x_c0. -/
theorem half_activation (u xc0 w : ℝ) (hx : 0 < xc0) (hw : 0 < w) :
    (u / xc0 - 1) / (2 * w) + 1 / 2 = 1 / 2 ↔ u = xc0 := by
  constructor
  · intro h
    have h2 : (u / xc0 - 1) / (2 * w) = 0 := by linarith
    rcases div_eq_zero_iff.mp h2 with h3 | h3
    · have : u / xc0 = 1 := by linarith
      field_simp at this; linarith
    · linarith
  · intro h; subst h; field_simp; ring

/-- the contrast door: on flat FRW u = 0, so t = (w - 1)/(2w) <= 0 for 0 < w <= 1 (off-plateau). -/
theorem contrast_door_frw (xc0 w : ℝ) (hx : 0 < xc0) (hw : 0 < w) (hw1 : w ≤ 1) :
    (0 / xc0 - 1) / (2 * w) + 1 / 2 ≤ 0 := by
  have : (0 / xc0 - 1) / (2 * w) + 1 / 2 = (w - 1) / (2 * w) := by field_simp; ring
  rw [this]
  exact div_nonpos_of_nonpos_of_nonneg (by linarith) (by linarith)

/-- the absolute door: t <= 0 on its FRW value u iff u <= x_c0 (1 - w). -/
theorem absolute_door_frw (u xc0 w : ℝ) (hx : 0 < xc0) (hw : 0 < w) :
    (u / xc0 - 1) / (2 * w) + 1 / 2 ≤ 0 ↔ u ≤ xc0 * (1 - w) := by
  have e : (u / xc0 - 1) / (2 * w) + 1 / 2 = (u - xc0 * (1 - w)) / (2 * w * xc0) := by field_simp; ring
  rw [e]
  constructor
  · intro h
    have hpos : 0 < 2 * w * xc0 := by positivity
    have := (div_nonpos_iff.mp h)
    rcases this with ⟨h1, _⟩ | ⟨h1, h2⟩
    · linarith
    · linarith
  · intro h
    exact div_nonpos_of_nonpos_of_nonneg (by linarith) (by positivity)

/-- p = 1, w = 1: the general gate argument is the lead track's t = 27 Lambda R/(8 x_c K^4), x_c = Omega_L0 x_c0. -/
theorem p1_reduction (Λ R K Ω xc0 : ℝ) (hK : K ≠ 0) (hΩ : Ω ≠ 0) (hx : xc0 ≠ 0) :
    ((9 / 4 * (3 * Λ) * R / (Ω * xc0 * K ^ 4)) - 1) / (2 * 1) + 1 / 2 = 27 * Λ * R / (8 * (Ω * xc0) * K ^ 4) := by
  field_simp
  ring

end DE7

#print axioms DE7.plateau_gate_both_signs
#print axioms DE7.estar_ge_E
#print axioms DE7.estar_pos_where_convex
#print axioms DE7.estar_pos_where_concave_negB
#print axioms DE7.d4_negative
#print axioms DE7.void_ceiling
#print axioms DE7.repair_slope_drop
#print axioms DE7.slip_from_tracefree
#print axioms DE7.half_activation
#print axioms DE7.contrast_door_frw
#print axioms DE7.absolute_door_frw
#print axioms DE7.p1_reduction
