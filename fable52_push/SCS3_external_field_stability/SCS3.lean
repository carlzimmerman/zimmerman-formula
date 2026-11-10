/-
SCS3 (criteria eff0ae1861, amendment A1 f51866c8d4): Lean statements for the closed forms the external-field lane uses.
They certify algebra and inequalities, not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  growth_par         : with K m = 1/(1+u)^2 (along the field), (1 - K m)/m = K u (2 + u).
  growth_perp        : with K m = 1/(1+u) (across the field), (1 - K m)/m = K u.
  par_beats_perp     : u (2 + u) > u for u > 0: the fastest direction is along the field.
  growth_sign        : Gamma^2 = -(K D.P) u (2 + u) is positive iff D.P < 0 (u > 0).
  growth_zero_at_null: at u = 0 (the total field's null) the local rate vanishes, whatever D.P is.
  farfield_plane_KDP : SCS2's far-field phantom K D.P = -L A [r_perp^2 - 2 x_par^2/(1+L)]/((1+L) s^5) at x_par = 0
                       (s = r) is -L A/((1+L) r^3).
  farfield_plane_rate: with L = 1/(1+x), s^2 = 1 + L, A = G M (1+x)/(x s): L A x (2+x)/((1+L) r^3) = G M (2+x)/(s^3 r^3).
  farfield_decreasing: that rate falls with r (Gamma^2 r^3 is constant).
  richardson_ratio / richardson_limit : three values Q + C, Q + C/t, Q + C/t^2 give (Q1-Q0)/(Q2-Q1) = t and
                       Q = Q2 + (Q2-Q1)/(t-1).
  route2_lower_bound : N >= c q, D >= q > 0, c < 0 give N/D >= c.
  mediant_ge_min     : (G1+G2)/(J1+J2) >= min(G1/J1, G2/J2) for J1, J2 > 0.
  inertia_ge_chi     : 0 < a < b gives 1/(1/a - 1/b) >= a (scalar form of H >= L_chi).
-/
import Mathlib

namespace SCS3

theorem growth_par (K u : ℝ) (hK : 0 < K) (hu : 0 ≤ u) :
    (1 - K * (1 / (K * (1 + u) ^ 2))) / (1 / (K * (1 + u) ^ 2)) = K * u * (2 + u) := by
  have h1 : (0 : ℝ) < 1 + u := by linarith
  have hK' : K ≠ 0 := ne_of_gt hK
  have h1' : (1 + u) ≠ 0 := ne_of_gt h1
  field_simp
  ring

theorem growth_perp (K u : ℝ) (hK : 0 < K) (hu : 0 ≤ u) :
    (1 - K * (1 / (K * (1 + u)))) / (1 / (K * (1 + u))) = K * u := by
  have h1 : (0 : ℝ) < 1 + u := by linarith
  have hK' : K ≠ 0 := ne_of_gt hK
  have h1' : (1 + u) ≠ 0 := ne_of_gt h1
  field_simp
  ring

theorem par_beats_perp (u : ℝ) (hu : 0 < u) : u < u * (2 + u) := by nlinarith

theorem growth_sign (KDP u : ℝ) (hu : 0 < u) : 0 < -KDP * (u * (2 + u)) ↔ KDP < 0 := by
  have hp : 0 < u * (2 + u) := by positivity
  constructor
  · intro h
    by_contra hc
    have hc' : 0 ≤ KDP := not_lt.mp hc
    have : -KDP * (u * (2 + u)) ≤ 0 := by nlinarith
    linarith
  · intro h
    have : 0 < -KDP := by linarith
    positivity

theorem growth_zero_at_null (KDP : ℝ) : -KDP * ((0 : ℝ) * (2 + 0)) = 0 := by ring

theorem farfield_plane_KDP (L A r : ℝ) (hL : 0 < L) (hr : 0 < r) :
    -L * A * (r ^ 2 - 2 * (0 : ℝ) ^ 2 / (1 + L)) / ((1 + L) * r ^ 5) = -L * A / ((1 + L) * r ^ 3) := by
  have h1 : (1 + L) ≠ 0 := by positivity
  have hr' : r ≠ 0 := ne_of_gt hr
  field_simp
  ring

theorem farfield_plane_rate (GM x s r : ℝ) (hx : 0 < x) (hs : 0 < s) (hr : 0 < r)
    (hs2 : s ^ 2 = 1 + 1 / (1 + x)) :
    (1 / (1 + x)) * (GM * (1 + x) / (x * s)) * (x * (2 + x)) / ((1 + 1 / (1 + x)) * r ^ 3)
      = GM * (2 + x) / (s ^ 3 * r ^ 3) := by
  have h1x : (0 : ℝ) < 1 + x := by linarith
  rw [← hs2]
  have hx' : x ≠ 0 := ne_of_gt hx
  have hs' : s ≠ 0 := ne_of_gt hs
  have hr' : r ≠ 0 := ne_of_gt hr
  have h1x' : (1 + x) ≠ 0 := ne_of_gt h1x
  field_simp

theorem farfield_decreasing (C r1 r2 : ℝ) (hC : 0 < C) (h1 : 0 < r1) (h12 : r1 < r2) :
    C / r2 ^ 3 < C / r1 ^ 3 := by
  apply div_lt_div_of_pos_left hC (by positivity)
  exact pow_lt_pow_left₀ h12 h1.le (by norm_num)

theorem richardson_ratio (Q C t : ℝ) (ht : 0 < t) (ht1 : t ≠ 1) (hC : C ≠ 0) :
    ((Q + C / t) - (Q + C)) / ((Q + C / t ^ 2) - (Q + C / t)) = t := by
  have ht' : t ≠ 0 := ne_of_gt ht
  have hden : (Q + C / t ^ 2) - (Q + C / t) ≠ 0 := by
    have : (Q + C / t ^ 2) - (Q + C / t) = C * (1 - t) / t ^ 2 := by field_simp; ring
    rw [this]
    have : (1 - t) ≠ 0 := fun h => ht1 (by linarith)
    exact div_ne_zero (mul_ne_zero hC this) (pow_ne_zero 2 ht')
  rw [div_eq_iff hden]
  field_simp
  ring

theorem richardson_limit (Q C t : ℝ) (ht : 0 < t) (ht1 : t ≠ 1) :
    Q = (Q + C / t ^ 2) + ((Q + C / t ^ 2) - (Q + C / t)) / (t - 1) := by
  have ht' : t ≠ 0 := ne_of_gt ht
  have ht1' : t - 1 ≠ 0 := sub_ne_zero.mpr ht1
  field_simp
  ring

theorem route2_lower_bound (N D q c : ℝ) (hq : 0 < q) (hc : c < 0) (hN : c * q ≤ N) (hD : q ≤ D) :
    c ≤ N / D := by
  have hD0 : 0 < D := lt_of_lt_of_le hq hD
  rw [le_div_iff₀ hD0]
  nlinarith

theorem mediant_ge_min (G1 G2 J1 J2 : ℝ) (h1 : 0 < J1) (h2 : 0 < J2) :
    min (G1 / J1) (G2 / J2) ≤ (G1 + G2) / (J1 + J2) := by
  rw [le_div_iff₀ (by linarith)]
  have a : min (G1 / J1) (G2 / J2) * J1 ≤ G1 := by
    have := min_le_left (G1 / J1) (G2 / J2)
    calc min (G1 / J1) (G2 / J2) * J1 ≤ G1 / J1 * J1 := by nlinarith
      _ = G1 := by field_simp
  have b : min (G1 / J1) (G2 / J2) * J2 ≤ G2 := by
    have := min_le_right (G1 / J1) (G2 / J2)
    calc min (G1 / J1) (G2 / J2) * J2 ≤ G2 / J2 * J2 := by nlinarith
      _ = G2 := by field_simp
  nlinarith

theorem inertia_ge_chi (a b : ℝ) (ha : 0 < a) (hab : a < b) : a ≤ 1 / (1 / a - 1 / b) := by
  have hb : 0 < b := lt_trans ha hab
  have hd : 0 < 1 / a - 1 / b := by
    rw [sub_pos]; exact one_div_lt_one_div_of_lt ha hab
  rw [le_div_iff₀ hd]
  have : a * (1 / a - 1 / b) = 1 - a / b := by field_simp
  rw [this]
  have : 0 < a / b := div_pos ha hb
  linarith

end SCS3
#print axioms SCS3.growth_par
#print axioms SCS3.growth_perp
#print axioms SCS3.par_beats_perp
#print axioms SCS3.growth_sign
#print axioms SCS3.growth_zero_at_null
#print axioms SCS3.farfield_plane_KDP
#print axioms SCS3.farfield_plane_rate
#print axioms SCS3.farfield_decreasing
#print axioms SCS3.richardson_ratio
#print axioms SCS3.richardson_limit
#print axioms SCS3.route2_lower_bound
#print axioms SCS3.mediant_ge_min
#print axioms SCS3.inertia_ge_chi
