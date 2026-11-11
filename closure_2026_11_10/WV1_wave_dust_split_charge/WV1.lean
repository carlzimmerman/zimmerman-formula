/-
WV1 (criteria 174870d2fe): Lean statements for the structural claims. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  dispersion_zero_charge : QG1's closed form omega^2 = G k^2 (b - a)/(a b) vanishes at every k when the frame's charge G
                           is 0 (V2 on FRW: no frame dust, P_bar = 0).
  v1_offbranch_negative  : V1's dispersion with J = 4 pi G rho > 0 and t = q^4 >= 0, at screening factor cY = 1:
                           J t/(1 + t) - J < 0 for every q (no Jeans scale on the off branch).
  v1_screen0_is_C5       : at cY = 0 the same form is X14's C5 dispersion J q^4 - J (= nu^2 k^4/4 - 4 pi G rho).
  v1_rate_bound          : for 0 <= cY <= 1 the growth rate squared -(omega^2) never exceeds the Jeans rate J.
  density_negative       : V1's U(1) charge C = m n + D with m > 0: a phantom charge D above C forces n < 0.
  advected_zero          : a quantity carried unchanged along a flow line that starts at 0 stays 0 (V2's frame charge).
  regular_centre_zero    : spherical div P = 0 means r^2 P_r = c; regularity at the centre (c = 0) gives P_r = 0 at r > 0.
  mu_identity            : the static law's algebra: g - a0 g/(a0 + g) = mu(g/a0) g with mu(x) = x/(1 + x).
  window_empty           : nu_min > nu_max leaves no nu with nu_min <= nu <= nu_max.
-/
import Mathlib.Tactic

namespace WV1

theorem dispersion_zero_charge (G k a b : ℝ) (hG : G = 0) :
    G * k ^ 2 * (b - a) / (a * b) = 0 := by
  subst hG; ring

theorem v1_offbranch_negative (J t : ℝ) (hJ : 0 < J) (ht : 0 ≤ t) :
    J * t / (1 + 1 * t) - J < 0 := by
  have hd : 0 < 1 + 1 * t := by linarith
  have h : J * t / (1 + 1 * t) - J = -J / (1 + 1 * t) := by
    field_simp; ring
  rw [h]
  exact div_neg_of_neg_of_pos (by linarith) hd

theorem v1_screen0_is_C5 (J t : ℝ) : J * t / (1 + 0 * t) - J = J * t - J := by
  simp

theorem v1_rate_bound (J t c : ℝ) (hJ : 0 < J) (ht : 0 ≤ t) (hc0 : 0 ≤ c) (hc1 : c ≤ 1) :
    -(J * t / (1 + c * t) - J) ≤ J := by
  have hd : 0 < 1 + c * t := by nlinarith
  have hnum : 0 ≤ J * t := by positivity
  have : 0 ≤ J * t / (1 + c * t) := div_nonneg hnum hd.le
  linarith

theorem density_negative (m n C D : ℝ) (hm : 0 < m) (hC : C = m * n + D) (hD : D > C) : n < 0 := by
  have : m * n < 0 := by linarith
  by_contra hn
  push_neg at hn
  have : 0 ≤ m * n := mul_nonneg hm.le hn
  linarith

theorem advected_zero (Y : ℕ → ℝ) (h : ∀ k, Y (k + 1) = Y k) (h0 : Y 0 = 0) : ∀ n, Y n = 0 := by
  intro n
  induction n with
  | zero => exact h0
  | succ k ih => rw [h k, ih]

theorem regular_centre_zero (r P c : ℝ) (hr : 0 < r) (hdiv : r ^ 2 * P = c) (hc : c = 0) : P = 0 := by
  subst hc
  have hr2 : r ^ 2 ≠ 0 := by positivity
  rcases mul_eq_zero.mp hdiv with h | h
  · exact absurd h hr2
  · exact h

theorem mu_identity (g a0 : ℝ) (ha : 0 < a0) (hg : 0 ≤ g) :
    g - a0 * g / (a0 + g) = ((g / a0) / (1 + g / a0)) * g := by
  have h1 : a0 + g ≠ 0 := by linarith
  have h2 : 1 + g / a0 ≠ 0 := by
    have : 0 ≤ g / a0 := div_nonneg hg ha.le
    linarith
  have h3 : a0 ≠ 0 := ha.ne'
  field_simp
  ring

theorem window_empty (numin numax : ℝ) (h : numax < numin) :
    ¬ ∃ nu : ℝ, numin ≤ nu ∧ nu ≤ numax := by
  rintro ⟨nu, h1, h2⟩
  linarith

end WV1

#print axioms WV1.dispersion_zero_charge
#print axioms WV1.v1_offbranch_negative
#print axioms WV1.v1_screen0_is_C5
#print axioms WV1.v1_rate_bound
#print axioms WV1.density_negative
#print axioms WV1.advected_zero
#print axioms WV1.regular_centre_zero
#print axioms WV1.mu_identity
#print axioms WV1.window_empty
