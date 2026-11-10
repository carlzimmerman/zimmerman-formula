/-
SCS1 (criteria 5d2870617c): Lean statements for the closed forms of the coupled dispersion relation of the static clock.
They certify the algebra, not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Newtonian-order Fourier form (frozen coefficients): with X = mu^2 + K m k2 (k2 = k^2, m = khat.J''.khat > 0),
  L = -k2 phi^2/(2K) + (X/(2K)) (v - phi)^2 - (G/2) k2 pi^2,   v = pi_t,
G = n_d + D.P the clock's charge density.

  constraint_stationary, constraint_value : phi* = X v/(X - k2) is stationary and leaves the kinetic term X k2 v^2/(2K(k2 - X)).
  dispersion             : omega^2 = G k2 / K_eff = K G ((1 - K m) k2 - mu^2)/(mu^2 + K m k2).
  bounded_decomposition  : that equals G (1 - K m)/m - G mu^2/(m (mu^2 + K m k2)).
  bounded_abs            : |omega^2| <= |G| (2 - K m)/m for every k2 >= 0 (growth bounded in k).
  stable_mu0             : mu = 0, G > 0, 0 < K m < 1 gives omega^2 > 0 at every k.
  Km_lt_one              : c^2/(1+u)^2 + s^2/(1+u) < 1 for u > 0, c^2 + s^2 = 1 (K = 1).
  mixing_factor          : K_eff over the decoupled X/K is 1/(1 - K m - mu^2/k2); at mu = 0 it is 1/(1 - K m).
  dust_jeans             : law off (m = 0): omega^2 = K n (k2 - mu^2)/mu^2, and -K n at k2 = 0.
  stiffness_form         : with m -> m/(1 + g m k2) and mu = 0: omega^2 = G (1 + g m k2 - K m)/m, linear in k2.
  stiffness_unbounded    : if G < 0 and g m > 0, omega^2 falls below any bound as k2 grows.
  spherical_divergence   : (2 r p + r^2 p')/r^2 = p' + 2 p/r (TPA1's planar model keeps p' only).
-/
import Mathlib

namespace SCS1

theorem constraint_stationary (K X k2 v : ℝ) (hK : K ≠ 0) (hX : X - k2 ≠ 0) :
    -(k2 * (X * v / (X - k2))) / K - X * (v - X * v / (X - k2)) / K = 0 := by
  field_simp
  ring

theorem constraint_value (K X k2 v : ℝ) (hK : K ≠ 0) (hX : X - k2 ≠ 0) (hX' : k2 - X ≠ 0) :
    -k2 * (X * v / (X - k2)) ^ 2 / (2 * K) + X / (2 * K) * (v - X * v / (X - k2)) ^ 2
      = X * k2 * v ^ 2 / (2 * K * (k2 - X)) := by
  have h : X - k2 = -(k2 - X) := by ring
  rw [h]
  field_simp
  ring

/-- omega^2 = G k2 / K_eff with K_eff = X k2 / (K (k2 - X)), X = mu^2 + K m k2. -/
theorem dispersion (K G m mu k2 : ℝ) (hK : K ≠ 0) (hk : k2 ≠ 0) (hX : mu ^ 2 + K * m * k2 ≠ 0)
    (hd : k2 - (mu ^ 2 + K * m * k2) ≠ 0) :
    G * k2 / ((mu ^ 2 + K * m * k2) * k2 / (K * (k2 - (mu ^ 2 + K * m * k2))))
      = K * G * ((1 - K * m) * k2 - mu ^ 2) / (mu ^ 2 + K * m * k2) := by
  field_simp
  ring

theorem bounded_decomposition (K G m mu k2 : ℝ) (hm : m ≠ 0) (hX : mu ^ 2 + K * m * k2 ≠ 0) :
    K * G * ((1 - K * m) * k2 - mu ^ 2) / (mu ^ 2 + K * m * k2)
      = G * (1 - K * m) / m - G * mu ^ 2 / (m * (mu ^ 2 + K * m * k2)) := by
  field_simp
  ring

theorem bounded_abs (K G m mu k2 : ℝ) (hm : 0 < m) (hKm : 0 ≤ K * m) (hKm1 : K * m ≤ 1) (hk : 0 ≤ k2)
    (hX : 0 < mu ^ 2 + K * m * k2) :
    |K * G * ((1 - K * m) * k2 - mu ^ 2) / (mu ^ 2 + K * m * k2)| ≤ |G| * (2 - K * m) / m := by
  rw [bounded_decomposition K G m mu k2 hm.ne' hX.ne']
  have hfrac : mu ^ 2 / (mu ^ 2 + K * m * k2) ≤ 1 := by
    rw [div_le_one hX]; nlinarith [sq_nonneg mu, mul_nonneg hKm hk]
  have hfrac0 : 0 ≤ mu ^ 2 / (mu ^ 2 + K * m * k2) := div_nonneg (sq_nonneg mu) hX.le
  have e1 : G * (1 - K * m) / m - G * mu ^ 2 / (m * (mu ^ 2 + K * m * k2))
      = (G / m) * ((1 - K * m) - mu ^ 2 / (mu ^ 2 + K * m * k2)) := by
    field_simp
  rw [e1, abs_mul, abs_div, abs_of_pos hm]
  have hin : |(1 - K * m) - mu ^ 2 / (mu ^ 2 + K * m * k2)| ≤ 2 - K * m := by
    rw [abs_le]; constructor <;> nlinarith
  calc |G| / m * |(1 - K * m) - mu ^ 2 / (mu ^ 2 + K * m * k2)| ≤ |G| / m * (2 - K * m) :=
        mul_le_mul_of_nonneg_left hin (div_nonneg (abs_nonneg G) hm.le)
    _ = |G| * (2 - K * m) / m := by ring

theorem stable_mu0 (K G m k2 : ℝ) (hG : 0 < G) (hm : 0 < m) (hKm : 0 < K * m) (hKm1 : K * m < 1) (hk : 0 < k2) :
    0 < K * G * ((1 - K * m) * k2 - 0 ^ 2) / (0 ^ 2 + K * m * k2) := by
  have h1 : 0 < (1 - K * m) * k2 := mul_pos (by linarith) hk
  have h2 : 0 < K * m * k2 := mul_pos hKm hk
  have hK : 0 < K := by
    rcases lt_or_ge 0 K with h | h
    · exact h
    · nlinarith
  apply div_pos
  · have : (0 : ℝ) ^ 2 = 0 := by norm_num
    rw [this, sub_zero]; positivity
  · simpa using h2

theorem Km_lt_one (u c s : ℝ) (hu : 0 < u) (hcs : c ^ 2 + s ^ 2 = 1) :
    c ^ 2 / (1 + u) ^ 2 + s ^ 2 / (1 + u) < 1 := by
  have h1 : (0 : ℝ) < 1 + u := by linarith
  have hc : c ^ 2 / (1 + u) ^ 2 ≤ c ^ 2 / (1 + u) := by
    apply div_le_div_of_nonneg_left (sq_nonneg c) h1; nlinarith
  have hlt : (c ^ 2 + s ^ 2) / (1 + u) < 1 := by rw [hcs, div_lt_one h1]; linarith
  have : c ^ 2 / (1 + u) + s ^ 2 / (1 + u) = (c ^ 2 + s ^ 2) / (1 + u) := by ring
  linarith

/-- the coupled kinetic coefficient over the decoupled one X/K. -/
theorem mixing_factor (K m mu k2 : ℝ) (hK : K ≠ 0) (hk : k2 ≠ 0) (hX : mu ^ 2 + K * m * k2 ≠ 0)
    (hd : k2 - (mu ^ 2 + K * m * k2) ≠ 0) (hd' : 1 - K * m - mu ^ 2 / k2 ≠ 0) :
    ((mu ^ 2 + K * m * k2) * k2 / (K * (k2 - (mu ^ 2 + K * m * k2)))) / ((mu ^ 2 + K * m * k2) / K)
      = 1 / (1 - K * m - mu ^ 2 / k2) := by
  have hd2 : k2 - k2 * K * m - mu ^ 2 ≠ 0 := by intro h; apply hd; linarith
  rw [div_div_eq_mul_div, eq_div_iff hd']
  field_simp
  ring

theorem mixing_factor_mu0 (K m k2 : ℝ) (hK : K ≠ 0) (hk : k2 ≠ 0) (hX : K * m * k2 ≠ 0)
    (hd : k2 - K * m * k2 ≠ 0) (h1 : 1 - K * m ≠ 0) :
    (K * m * k2 * k2 / (K * (k2 - K * m * k2))) / (K * m * k2 / K) = 1 / (1 - K * m) := by
  have hm : m ≠ 0 := by intro h; apply hX; rw [h]; ring
  have e : k2 - K * m * k2 = k2 * (1 - K * m) := by ring
  rw [e]
  field_simp

theorem dust_jeans (K n mu k2 : ℝ) (hmu : mu ≠ 0) :
    K * n * ((1 - K * 0) * k2 - mu ^ 2) / (mu ^ 2 + K * 0 * k2) = K * n * (k2 - mu ^ 2) / mu ^ 2 ∧
    K * n * ((1 - K * 0) * 0 - mu ^ 2) / (mu ^ 2 + K * 0 * 0) = -(K * n) := by
  constructor
  · ring
  · have : mu ^ 2 ≠ 0 := pow_ne_zero 2 hmu
    field_simp
    ring

theorem stiffness_form (K G m g k2 : ℝ) (hm : m ≠ 0) (hd : 1 + g * m * k2 ≠ 0) :
    G * (1 - K * (m / (1 + g * m * k2))) / (m / (1 + g * m * k2)) = G * (1 + g * m * k2 - K * m) / m := by
  have hd' : 1 + m * g * k2 ≠ 0 := by rwa [show m * g * k2 = g * m * k2 by ring]
  field_simp

theorem stiffness_unbounded (K G m g : ℝ) (hG : G < 0) (hm : 0 < m) (hg : 0 < g * m) (B : ℝ) :
    ∃ k2 : ℝ, 0 ≤ k2 ∧ G * (1 + g * m * k2 - K * m) / m < B := by
  -- choose k2 large: the expression is linear in k2 with slope G g < 0
  set c := G * (1 - K * m) / m with hc
  have hslope : G * g < 0 := by
    have : 0 < g := by
      rcases lt_or_ge 0 g with h | h
      · exact h
      · nlinarith
    nlinarith
  refine ⟨max 0 ((B - c) / (G * g) + 1), le_max_left _ _, ?_⟩
  have hexp : G * (1 + g * m * (max 0 ((B - c) / (G * g) + 1)) - K * m) / m
      = c + G * g * (max 0 ((B - c) / (G * g) + 1)) := by
    rw [hc]; field_simp; ring
  rw [hexp]
  have hge : (B - c) / (G * g) + 1 ≤ max 0 ((B - c) / (G * g) + 1) := le_max_right _ _
  have h2 : G * g * (max 0 ((B - c) / (G * g) + 1)) ≤ G * g * ((B - c) / (G * g) + 1) :=
    mul_le_mul_of_nonpos_left hge hslope.le
  have hne : G * g ≠ 0 := hslope.ne
  have h3 : G * g * ((B - c) / (G * g) + 1) = (B - c) + G * g := by
    rw [mul_add, mul_div_cancel₀ _ hne, mul_one]
  linarith

theorem spherical_divergence (r p dp : ℝ) (hr : r ≠ 0) :
    (2 * r * p + r ^ 2 * dp) / r ^ 2 = dp + 2 * p / r := by
  field_simp
  ring

end SCS1

#print axioms SCS1.constraint_stationary
#print axioms SCS1.constraint_value
#print axioms SCS1.dispersion
#print axioms SCS1.bounded_decomposition
#print axioms SCS1.bounded_abs
#print axioms SCS1.stable_mu0
#print axioms SCS1.Km_lt_one
#print axioms SCS1.mixing_factor
#print axioms SCS1.mixing_factor_mu0
#print axioms SCS1.dust_jeans
#print axioms SCS1.stiffness_form
#print axioms SCS1.stiffness_unbounded
#print axioms SCS1.spherical_divergence

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
