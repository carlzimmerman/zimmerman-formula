/-
QX13 (closure_2026_11_06/QX13_virial_floor, criteria 5584787fbd): algebra of the virial-shock sector with an entropy
floor (gamma = 5/3, p = K rho^(5/3), enthalpy h = (5/2) p / rho = (5/2) K rho^(2/3)).

1. `shock_enthalpy`: a strong shock (rho_2 = 4 rho_1, p_2 = (3/4) rho_1 v^2) leaves post-shock enthalpy
   h_2 = (15/32) v^2, independent of the upstream density rho_1.
2. `shock_identity`: with free fall from rest at r_ta (v^2 = 2 H_sh), h_2 = (15/16) H_sh (KA2).
3. `shock_h_le`: for any infall with v^2 <= 2 H_sh and H_sh >= 0, h_2 <= H_sh.
4. `base_mono`: the profile base 2 w / (5 K), with rho = base^(3/2), is monotone up in w and down in K.
5. `class_bound`: in an isentropic host with K >= K_0 > 0, any shock radius and any upstream density, the base
   2 (h_2 + H_in) / (5 K) never exceeds the open-contact floor atmosphere's base rho_sea^(2/3) + 2 H / (5 K_0),
   where H = H_sh + H_in. So M2 (K = K_0, heating off) bounds the class's retention from above.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace QX13

theorem shock_enthalpy {ρ₁ v2 : ℝ} (hρ : 0 < ρ₁) :
    (5 / 2) * ((3 / 4) * ρ₁ * v2) / (4 * ρ₁) = (15 / 32) * v2 := by
  field_simp; ring

theorem shock_identity {ρ₁ H : ℝ} (hρ : 0 < ρ₁) :
    (5 / 2) * ((3 / 4) * ρ₁ * (2 * H)) / (4 * ρ₁) = (15 / 16) * H := by
  field_simp; ring

theorem shock_h_le {v2 H : ℝ} (hv : v2 ≤ 2 * H) (hH : 0 ≤ H) : (15 / 32) * v2 ≤ H := by
  nlinarith

theorem base_mono {w₁ w₂ K₁ K₂ : ℝ} (hw : w₁ ≤ w₂) (hw1 : 0 ≤ w₁) (hK2 : 0 < K₂) (hK : K₂ ≤ K₁) :
    2 * w₁ / (5 * K₁) ≤ 2 * w₂ / (5 * K₂) := by
  have hK1 : 0 < K₁ := lt_of_lt_of_le hK2 hK
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  have h1 : 2 * w₁ * (5 * K₂) ≤ 2 * w₁ * (5 * K₁) := by nlinarith
  have h2 : 2 * w₁ * (5 * K₁) ≤ 2 * w₂ * (5 * K₁) := by nlinarith
  linarith

theorem class_bound {h2 Hsh Hin K K0 x : ℝ} (hK0 : 0 < K0) (hK : K0 ≤ K) (h2le : h2 ≤ Hsh)
    (h2nn : 0 ≤ h2) (hin : 0 ≤ Hin) (hx : 0 ≤ x) :
    2 * (h2 + Hin) / (5 * K) ≤ x + 2 * (Hsh + Hin) / (5 * K0) := by
  have hb := base_mono (w₁ := h2 + Hin) (w₂ := Hsh + Hin) (by linarith) (by linarith) hK0 hK
  linarith

end QX13

#print axioms QX13.shock_enthalpy
#print axioms QX13.shock_identity
#print axioms QX13.shock_h_le
#print axioms QX13.base_mono
#print axioms QX13.class_bound
