import Mathlib

/-!
# CFG487 -- certificates for the settled-fraction switch (FROZEN_CRITERIA.md section 3(e))

The settled fraction m obeys D m / Dt = Gamma L (1 - m), with the binding latch L in {0, 1}.
Exact step update over dt: m' = 1 - (1 - m) exp(-(Gamma dt L)).  The switch is f = m * Theta, Theta in [0, 1] (the edge).

* L1 step monotonicity (the label never decreases: no flicker).
* L2 [0, 1] invariance.
* L3 FRW-off: never latched (L = 0 at every step) and m0 = 0  =>  m = 0 at every step.
* L4 MUTATE: latched from the start with Gamma dt > 0  =>  m > 0 after one step (a nonzero background).
* L5 the mass-conserving edge: with R = r_M / ln(1/(1 - f_b)), 1/(exp(r_M/R) - 1) = (1 - f_b)/f_b (T9 closed form).
* L6 the switch f = m Theta lies in [0, 1].
* L7 the (d) bound: a root s >= 0 of s^2 (s + Gamma) = G2 (s + Gamma) + C with Gamma > 0, C >= 0 obeys s^2 <= G2 + C/Gamma.
* L8 uniform in k: with G2 = Gg2 - cs2 k^2, cs2 >= 0, C = Gph2 F (1 - m) Gamma chi / 2, the bound is <= Gg2 + Gph2 F (1-m) chi / 2.
* L9 exponent monotonicity: E1 <= E2 => 1 - exp(-E1) <= 1 - exp(-E2) (the conservative clock bracket is a lower bound).
* L10 extra growth: if Gph2 <= Gg2 and 0 <= F (1 - m) chi <= 1 then s^2 <= (3/2) Gg2, hence s <= (5/4) Gg.
-/

noncomputable def step (m G dt L : ℝ) : ℝ := 1 - (1 - m) * Real.exp (-(G * dt * L))

theorem L1_step_monotone (m G dt L : ℝ) (hm : m ≤ 1) (hx : 0 ≤ G * dt * L) :
    m ≤ step m G dt L := by
  unfold step
  have he : Real.exp (-(G * dt * L)) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
  have h1 : 0 ≤ 1 - m := by linarith
  nlinarith [mul_le_mul_of_nonneg_left he h1]

theorem L2_unit_interval (m G dt L : ℝ) (h0 : 0 ≤ m) (hm : m ≤ 1) (hx : 0 ≤ G * dt * L) :
    0 ≤ step m G dt L ∧ step m G dt L ≤ 1 := by
  unfold step
  have he : Real.exp (-(G * dt * L)) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
  have hp : 0 < Real.exp (-(G * dt * L)) := Real.exp_pos _
  have h1 : 0 ≤ 1 - m := by linarith
  constructor
  · nlinarith [mul_le_mul_of_nonneg_left he h1]
  · nlinarith [mul_nonneg h1 hp.le]

theorem L3_frw_off (mseq : ℕ → ℝ) (G dt : ℝ) (L : ℕ → ℝ)
    (hstep : ∀ n, mseq (n + 1) = step (mseq n) G dt (L n)) (hL : ∀ n, L n = 0) (h0 : mseq 0 = 0) :
    ∀ n, mseq n = 0 := by
  intro n
  induction n with
  | zero => exact h0
  | succ n ih => rw [hstep, ih, hL]; unfold step; simp

theorem L4_mutate_on (G dt : ℝ) (hx : 0 < G * dt) : 0 < step 0 G dt 1 := by
  unfold step
  have h : Real.exp (-(G * dt * 1)) < Real.exp 0 := Real.exp_lt_exp.mpr (by linarith)
  rw [Real.exp_zero] at h
  linarith

theorem L5_edge_identity (fb : ℝ) (_h0 : 0 < fb) (h1 : fb < 1) :
    1 / (Real.exp (Real.log (1 / (1 - fb))) - 1) = (1 - fb) / fb := by
  have hpos : 0 < 1 / (1 - fb) := by apply div_pos one_pos; linarith
  have h2 : (1 : ℝ) - fb ≠ 0 := sub_ne_zero.mpr (ne_of_gt h1)
  rw [Real.exp_log hpos, div_sub_one h2, one_div_div, sub_sub_cancel]

theorem L6_switch_unit (m θ : ℝ) (h0 : 0 ≤ m) (h1 : m ≤ 1) (t0 : 0 ≤ θ) (t1 : θ ≤ 1) :
    0 ≤ m * θ ∧ m * θ ≤ 1 := by
  constructor
  · exact mul_nonneg h0 t0
  · nlinarith

theorem L7_root_bound (s Γ G2 C : ℝ) (hs : 0 ≤ s) (hΓ : 0 < Γ) (hC : 0 ≤ C)
    (hroot : s ^ 2 * (s + Γ) = G2 * (s + Γ) + C) : s ^ 2 ≤ G2 + C / Γ := by
  have hsg : 0 < s + Γ := by linarith
  have key : s ^ 2 = G2 + C / (s + Γ) := by
    field_simp
    linarith [hroot]
  rw [key]
  have : C / (s + Γ) ≤ C / Γ := div_le_div_of_nonneg_left hC hΓ (by linarith)
  linarith

theorem L8_uniform_in_k (s Γ Gg2 cs2 k Gph2 F m χ : ℝ) (hs : 0 ≤ s) (hΓ : 0 < Γ) (hcs : 0 ≤ cs2)
    (hC : 0 ≤ Gph2 * F * (1 - m) * Γ * χ / 2)
    (hroot : s ^ 2 * (s + Γ) = (Gg2 - cs2 * k ^ 2) * (s + Γ) + Gph2 * F * (1 - m) * Γ * χ / 2) :
    s ^ 2 ≤ Gg2 + Gph2 * F * (1 - m) * χ / 2 := by
  have h := L7_root_bound s Γ (Gg2 - cs2 * k ^ 2) (Gph2 * F * (1 - m) * Γ * χ / 2) hs hΓ hC hroot
  have e : Gph2 * F * (1 - m) * Γ * χ / 2 / Γ = Gph2 * F * (1 - m) * χ / 2 := by
    field_simp
  have hk : 0 ≤ cs2 * k ^ 2 := mul_nonneg hcs (sq_nonneg k)
  rw [e] at h
  linarith

theorem L9_exponent_monotone (E1 E2 : ℝ) (h : E1 ≤ E2) : 1 - Real.exp (-E1) ≤ 1 - Real.exp (-E2) := by
  have : Real.exp (-E2) ≤ Real.exp (-E1) := Real.exp_le_exp.mpr (by linarith)
  linarith

theorem L10_extra_growth (s Gg Gph2 X : ℝ) (hs : 0 ≤ s) (hG : 0 ≤ Gg) (hph : 0 ≤ Gph2) (hph2 : Gph2 ≤ Gg ^ 2)
    (_hX0 : 0 ≤ X) (hX1 : X ≤ 1) (hb : s ^ 2 ≤ Gg ^ 2 + Gph2 * X / 2) :
    s ^ 2 ≤ (3 / 2) * Gg ^ 2 ∧ s ≤ (5 / 4) * Gg := by
  have h1 : Gph2 * X ≤ Gg ^ 2 := by nlinarith
  have hsq : s ^ 2 ≤ (3 / 2) * Gg ^ 2 := by nlinarith
  refine ⟨hsq, ?_⟩
  nlinarith [sq_nonneg (s - (5 / 4) * Gg), sq_nonneg (s + (5 / 4) * Gg)]

#print axioms L1_step_monotone
#print axioms L2_unit_interval
#print axioms L3_frw_off
#print axioms L4_mutate_on
#print axioms L5_edge_identity
#print axioms L6_switch_unit
#print axioms L7_root_bound
#print axioms L8_uniform_in_k
#print axioms L9_exponent_monotone
#print axioms L10_extra_growth
