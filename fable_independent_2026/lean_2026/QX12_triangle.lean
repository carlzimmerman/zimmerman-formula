/-
QX12 (closure_2026_11_06/QX12_triangle, criteria 7a1afa9b6b): algebra behind the constraint triangle.
1. `law_inverse`: g_N = g^2/(g + a0) is the exact inverse of the law g = g_N/2 + sqrt(g_N^2/4 + a0 g_N).
2. `baro_order`: in hydrostatic equilibrium with the sea a barotropic sector has h(rho) = h_sea + D with h strictly
   increasing, so a deeper point never holds less sector: rho is a nondecreasing function of depth D alone.
3. `baro_nogo`: a galaxy point at depth D_A >= D_B allowed at most u, a hot point at D_B needing at least l > u:
   no nondecreasing H(D) serves both.
4. `iso_ratio`: an isothermal sector (h = c^2 ln rho) at depth D holds rho = rho_sea * exp(D/c^2); larger c^2
   gives less at every D > 0 (iter_3's monotone-in-c argument).
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace QX12

theorem law_inverse {g a0 : ℝ} (hg : 0 < g) (ha : 0 < a0) :
    g ^ 2 / (g + a0) / 2 + Real.sqrt ((g ^ 2 / (g + a0)) ^ 2 / 4 + a0 * (g ^ 2 / (g + a0))) = g := by
  set gN := g ^ 2 / (g + a0) with hgN
  have hpos : 0 < g + a0 := by linarith
  have hkey : gN * (g + a0) = g ^ 2 := by rw [hgN]; field_simp
  have hle : gN ≤ g := by
    rw [hgN, div_le_iff₀ hpos]; nlinarith
  have hsq : gN ^ 2 / 4 + a0 * gN = (g - gN / 2) ^ 2 := by nlinarith
  have hnn : 0 ≤ g - gN / 2 := by
    have : 0 ≤ gN := by rw [hgN]; positivity
    linarith
  rw [hsq, Real.sqrt_sq hnn]; ring

theorem baro_order {h : ℝ → ℝ} (hh : StrictMono h) {ρ₁ ρ₂ c D₁ D₂ : ℝ}
    (e1 : h ρ₁ = c + D₁) (e2 : h ρ₂ = c + D₂) (hD : D₁ ≤ D₂) : ρ₁ ≤ ρ₂ := by
  by_contra hc
  push_neg at hc
  have := hh hc
  linarith

theorem baro_nogo {H : ℝ → ℝ} (hH : Monotone H) {DA DB u l : ℝ}
    (hD : DB ≤ DA) (hA : H DA ≤ u) (hB : l ≤ H DB) (hlu : u < l) : False := by
  have := hH hD
  linarith

theorem iso_ratio {c₁ c₂ D : ℝ} (h1 : 0 < c₁) (h12 : c₁ ≤ c₂) (hD : 0 ≤ D) :
    Real.exp (D / c₂) ≤ Real.exp (D / c₁) := by
  apply Real.exp_le_exp.mpr
  exact div_le_div_of_nonneg_left hD h1 h12

theorem iso_profile {ρs c D : ℝ} (hρ : 0 < ρs) (hc : 0 < c) :
    c * Real.log (ρs * Real.exp (D / c)) = c * Real.log ρs + D := by
  rw [Real.log_mul hρ.ne' (Real.exp_pos _).ne', Real.log_exp]
  field_simp

end QX12

#print axioms QX12.law_inverse
#print axioms QX12.baro_order
#print axioms QX12.baro_nogo
#print axioms QX12.iso_ratio
#print axioms QX12.iso_profile
