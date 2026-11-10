/-
SCS3 MUTATE (M4): false versions of SCS3.lean's statements, each with the true file's proof. Every one must fail to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SCS3_MUTATE

-- false: the along-field factor taken as u (the across-field one)
theorem growth_par (K u : ℝ) (hK : 0 < K) (hu : 0 ≤ u) :
    (1 - K * (1 / (K * (1 + u) ^ 2))) / (1 / (K * (1 + u) ^ 2)) = K * u := by
  have h1 : (0 : ℝ) < 1 + u := by linarith
  have hK' : K ≠ 0 := ne_of_gt hK
  have h1' : (1 + u) ≠ 0 := ne_of_gt h1
  field_simp
  ring

-- false: sign reversed
theorem growth_sign (KDP u : ℝ) (hu : 0 < u) : 0 < -KDP * (u * (2 + u)) ↔ 0 < KDP := by
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

-- false: s^2 in place of s^3
theorem farfield_plane_rate (GM x s r : ℝ) (hx : 0 < x) (hs : 0 < s) (hr : 0 < r)
    (hs2 : s ^ 2 = 1 + 1 / (1 + x)) :
    (1 / (1 + x)) * (GM * (1 + x) / (x * s)) * (x * (2 + x)) / ((1 + 1 / (1 + x)) * r ^ 3)
      = GM * (2 + x) / (s ^ 2 * r ^ 3) := by
  have h1x : (0 : ℝ) < 1 + x := by linarith
  rw [← hs2]
  have hx' : x ≠ 0 := ne_of_gt hx
  have hs' : s ≠ 0 := ne_of_gt hs
  have hr' : r ≠ 0 := ne_of_gt hr
  have h1x' : (1 + x) ≠ 0 := ne_of_gt h1x
  field_simp

-- false: t + 1 in place of t - 1
theorem richardson_limit (Q C t : ℝ) (ht : 0 < t) (ht1 : t ≠ 1) :
    Q = (Q + C / t ^ 2) + ((Q + C / t ^ 2) - (Q + C / t)) / (t + 1) := by
  have ht' : t ≠ 0 := ne_of_gt ht
  have ht1' : t - 1 ≠ 0 := sub_ne_zero.mpr ht1
  field_simp
  ring

-- false: the bound claimed at 0
theorem route2_lower_bound (N D q c : ℝ) (hq : 0 < q) (hc : c < 0) (hN : c * q ≤ N) (hD : q ≤ D) :
    0 ≤ N / D := by
  have hD0 : 0 < D := lt_of_lt_of_le hq hD
  rw [le_div_iff₀ hD0]
  nlinarith

-- false: max in place of min
theorem mediant_ge_min (G1 G2 J1 J2 : ℝ) (h1 : 0 < J1) (h2 : 0 < J2) :
    max (G1 / J1) (G2 / J2) ≤ (G1 + G2) / (J1 + J2) := by
  rw [le_div_iff₀ (by linarith)]
  have a : max (G1 / J1) (G2 / J2) * J1 ≤ G1 := by
    have := le_max_left (G1 / J1) (G2 / J2)
    calc max (G1 / J1) (G2 / J2) * J1 ≤ G1 / J1 * J1 := by nlinarith
      _ = G1 := by field_simp
  have b : max (G1 / J1) (G2 / J2) * J2 ≤ G2 := by
    have := le_max_right (G1 / J1) (G2 / J2)
    calc max (G1 / J1) (G2 / J2) * J2 ≤ G2 / J2 * J2 := by nlinarith
      _ = G2 := by field_simp
  nlinarith

-- false: the inequality reversed
theorem inertia_ge_chi (a b : ℝ) (ha : 0 < a) (hab : a < b) : 1 / (1 / a - 1 / b) ≤ a := by
  have hb : 0 < b := lt_trans ha hab
  have hd : 0 < 1 / a - 1 / b := by
    rw [sub_pos]; exact one_div_lt_one_div_of_lt ha hab
  rw [div_le_iff₀ hd]
  have : a * (1 / a - 1 / b) = 1 - a / b := by field_simp
  rw [this]
  have : 0 < a / b := div_pos ha hb
  linarith

end SCS3_MUTATE
