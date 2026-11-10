/-
COL1: Lean statements for the closed forms the lane uses. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  static_dust_newton     : M_d(r) = mu^2 M r^2 / 2 solves M_d' = (mu^2/G) r^2 (G M / r) (Newtonian static dust, Part 0).
  jeans_polytrope        : the n = 1 polytrope's sound speed c_s^2 = K n / mu^2 gives c_s^2 mu^2 = K n (Jeans wavenumber mu).
  lawon_response         : law on, linear: the clock's self-potential plus its h response is -K N mu^2 / (k^2 (mu^2 + k^2)).
  lawon_cancel_mu0       : at mu = 0 the clock's self-gravity is cancelled exactly at every k.
  shell_equilibrium      : -g_b - y + a0 y/(a0 - y) = 0  <->  y^2 = g_b (a0 - y)   (X14's shell equation at rest = the law).
  law_point              : y = a0 u/(1+u), g_b = a0 u^2/(1+u) satisfy it (u = g/a0).
  shell_frequency        : 2 a0 x^2 / (r (1 - x)^2) = 2 a0 u^2 / r at x = u/(1+u) (X14's small-x form made exact; = SCS1 high k).
  wkb_reduced_scs1       : the reduced system's WKB omega^2 equals SCS1's closed form (Qbar = 1).
  shell_energy           : v a + V' v = 0 when a = -V' (each thin shell conserves its energy at mu = 0).
  frw_half_stiff         : w(a) = w0/(w0 + a^3) <= 1/2  <->  mu^2 >= I0/(4 a^3)   (the brief's 3.71/Mpc puts w = 1/2 near z 1090).
  flux_cap               : K|P| = a0 A/(a0 + A) < a0 for A >= 0.
  pericentre_from_rest   : deep-MOND shell from rest far out: r_eq^2 = 3 r_p^2.
  legendre_flip          : the P.A sign flip leaves the Legendre value unchanged (MUTATE M2a cannot bite).
-/
import Mathlib

namespace COL1

theorem static_dust_newton (mu M G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    HasDerivAt (fun x : ℝ => mu ^ 2 * M * x ^ 2 / 2) (mu ^ 2 / G * r ^ 2 * (G * M / r)) r := by
  have h0 := ((hasDerivAt_pow 2 r).const_mul (mu ^ 2 * M)).div_const 2
  refine h0.congr_deriv ?_
  push_cast
  field_simp

theorem jeans_polytrope (K n mu : ℝ) (hmu : mu ≠ 0) : (K * n / mu ^ 2) * mu ^ 2 = K * n := by
  field_simp

theorem lawon_response (K N k mu : ℝ) (hk : k ≠ 0) (hd : mu ^ 2 + k ^ 2 ≠ 0) :
    -K * N / k ^ 2 + K * N / (mu ^ 2 + k ^ 2) = -K * N * mu ^ 2 / (k ^ 2 * (mu ^ 2 + k ^ 2)) := by
  field_simp
  ring

theorem lawon_cancel_mu0 (K N k : ℝ) (hk : k ≠ 0) :
    -K * N / k ^ 2 + K * N / ((0 : ℝ) ^ 2 + k ^ 2) = 0 := by
  have : (0 : ℝ) ^ 2 + k ^ 2 = k ^ 2 := by ring
  rw [this]
  ring

theorem shell_equilibrium (gb y a0 : ℝ) (h : a0 - y ≠ 0) :
    -gb - y + a0 * y / (a0 - y) = 0 ↔ y ^ 2 = gb * (a0 - y) := by
  have e : -gb - y + a0 * y / (a0 - y) = (y ^ 2 - gb * (a0 - y)) / (a0 - y) := by
    field_simp
    ring
  rw [e, div_eq_zero_iff]
  constructor
  · rintro (h1 | h1)
    · linarith
    · exact absurd h1 h
  · intro h1
    left
    linarith

theorem law_point (a0 u : ℝ) (hu : 1 + u ≠ 0) :
    (a0 * u / (1 + u)) ^ 2 = (a0 * u ^ 2 / (1 + u)) * (a0 - a0 * u / (1 + u)) := by
  field_simp
  ring

theorem shell_frequency (a0 u r : ℝ) (hu : 1 + u ≠ 0) (hr : r ≠ 0) :
    2 * a0 * (u / (1 + u)) ^ 2 / (r * (1 - u / (1 + u)) ^ 2) = 2 * a0 * u ^ 2 / r := by
  have h1 : 1 - u / (1 + u) = 1 / (1 + u) := by
    field_simp
    ring
  rw [h1]
  field_simp

theorem wkb_reduced_scs1 (K N0 k m mu : ℝ) (hK : K ≠ 0) (hk : k ≠ 0) (hd : mu ^ 2 + K * m * k ^ 2 ≠ 0) :
    N0 * k ^ 2 * (1 - K * m - mu ^ 2 / k ^ 2) / (mu ^ 2 / K + m * k ^ 2)
      = K * N0 * ((1 - K * m) * k ^ 2 - mu ^ 2) / (mu ^ 2 + K * m * k ^ 2) := by
  have h2 : mu ^ 2 / K + m * k ^ 2 = (mu ^ 2 + K * m * k ^ 2) / K := by
    field_simp
  rw [h2]
  field_simp

theorem shell_energy (v a Vp : ℝ) (h : a = -Vp) : v * a + Vp * v = 0 := by
  subst h
  ring

theorem frw_half_stiff (I0 a mu : ℝ) (hI : 0 < I0) (ha : 0 < a) (hmu : 0 < mu) :
    I0 / (4 * mu ^ 2) ≤ a ^ 3 ↔ I0 / (4 * a ^ 3) ≤ mu ^ 2 := by
  have h1 : 0 < 4 * mu ^ 2 := by positivity
  have h2 : 0 < 4 * a ^ 3 := by positivity
  rw [div_le_iff₀ h1, div_le_iff₀ h2]
  constructor <;> intro h <;> nlinarith

theorem flux_cap (a0 A : ℝ) (ha : 0 < a0) (hA : 0 ≤ A) : a0 * A / (a0 + A) < a0 := by
  have h : 0 < a0 + A := by linarith
  rw [div_lt_iff₀ h]
  nlinarith

theorem pericentre_from_rest (G m a0 M : ℝ) (ha : a0 ≠ 0) (hM : M ≠ 0) :
    G * m ^ 2 / (a0 * M) = 3 * (G * m ^ 2 / (3 * a0 * M)) := by
  field_simp

theorem legendre_flip (p A W : ℝ) : (-(-p)) * A - W = p * A - W := by
  ring

end COL1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
