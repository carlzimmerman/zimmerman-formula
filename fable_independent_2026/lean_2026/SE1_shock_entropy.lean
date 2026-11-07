/-
SE1 (closure_2026_11_06/SE1_shock_entropy_sector, criteria bf53473414): algebra behind the shock-entropy sector
L_x = F(Q, s) + zeta n.ds in the khronon sector.

1. `jeans_mono` (arm a): with g monotone and Sigma >= 0 (s >= s0), mu_K^2 g(s) >= mu_K^2 g(s0): the Jeans
   wavenumber of any shocked host is at least the primordial (CMB) one.
2. `secular` (Theorem K core): if (a t + b) d = 0 for every t and a != 0, then d = 0. With zeta = N F_s t + zeta_0
   and T_tx = zeta N s', a static metric forces s' = 0 wherever F_s != 0.
3. `crocco_static`: dh = T ds + dP/rho, hydrostatics dP/rho = -dPhi and the khronon's h + Phi = const give T ds = 0.
4. `shock_enthalpy`: strong shock (rho2 = 4 rho1, p2 = (3/4) rho1 v^2): h2 = (5/2) p2/rho2 = (15/32) v^2.
5. `jeans_adiabatic` (arm b): rho = A a^-3, c_s = c0 / a give k_J^2 = (A / c0^2) / a.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SE1

theorem jeans_mono (g : ℝ → ℝ) (hg : Monotone g) {s s0 μ : ℝ} (h : s0 ≤ s) :
    μ ^ 2 * g s0 ≤ μ ^ 2 * g s :=
  mul_le_mul_of_nonneg_left (hg h) (sq_nonneg μ)

theorem secular {a b d : ℝ} (ha : a ≠ 0) (h : ∀ t : ℝ, (a * t + b) * d = 0) : d = 0 := by
  have e0 := h 0
  have e1 := h 1
  have hd : a * d = 0 := by
    have : (a * 1 + b) * d - (a * 0 + b) * d = a * d := by ring
    rw [← this, e0, e1]; ring
  rcases mul_eq_zero.mp hd with h' | h'
  · exact absurd h' ha
  · exact h'

theorem crocco_static {T ds dP dPhi dh ρ : ℝ} (h1 : dh = T * ds + dP / ρ) (h2 : dP / ρ = -dPhi)
    (h3 : dh + dPhi = 0) : T * ds = 0 := by
  linarith

theorem shock_enthalpy {ρ₁ v2 : ℝ} (hρ : 0 < ρ₁) :
    (5 / 2) * ((3 / 4) * ρ₁ * v2) / (4 * ρ₁) = (15 / 32) * v2 := by
  rw [div_eq_iff (by positivity)]; ring

theorem jeans_adiabatic {A c0 a : ℝ} (ha : 0 < a) (hc : c0 ≠ 0) :
    A * (a⁻¹) ^ 3 / (c0 * a⁻¹) ^ 2 = (A / c0 ^ 2) / a := by
  have : a ≠ 0 := ne_of_gt ha
  field_simp

end SE1

#print axioms SE1.jeans_mono
#print axioms SE1.secular
#print axioms SE1.crocco_static
#print axioms SE1.shock_enthalpy
#print axioms SE1.jeans_adiabatic
