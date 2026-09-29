import Mathlib
import H1_bpst

open MeasureTheory Set Real

/-! ### Vol(S^4_L) from the sine-power integrals -/

/-- Vol(S^4_L) as the iterated integral of the round volume element
L^4 sin^3 th1 sin^2 th2 sin th3 (dth1 dth2 dth3 dphi). -/
noncomputable def volS4 (L : ℝ) : ℝ :=
  L ^ 4 * (∫ x in (0:ℝ)..π, Real.sin x ^ 3) * (∫ x in (0:ℝ)..π, Real.sin x ^ 2) *
    (∫ x in (0:ℝ)..π, Real.sin x) * (2 * π)

theorem volS4_eq (L : ℝ) : volS4 L = 8 * π ^ 2 * L ^ 4 / 3 := by
  unfold volS4; rw [int_sin_cube, int_sin_sq, int_sin]; ring

/-! ### Euler density of the round S^4_L from the constant-curvature Riemann tensor (orthonormal frame, 4 dimensions) -/

def dl (a b : Fin 4) : ℝ := if a = b then 1 else 0
/-- R_{abcd} = k (delta_ac delta_bd - delta_ad delta_bc), k = 1/L^2 -/
def riem (k : ℝ) (a b c d : Fin 4) : ℝ := k * (dl a c * dl b d - dl a d * dl b c)
def ric (k : ℝ) (b d : Fin 4) : ℝ := ∑ a, riem k a b a d
def scal (k : ℝ) : ℝ := ∑ b, ric k b b
def ric2 (k : ℝ) : ℝ := ∑ b, ∑ d, ric k b d ^ 2
def riem2 (k : ℝ) : ℝ := ∑ a, ∑ b, ∑ c, ∑ d, riem k a b c d ^ 2
/-- Gauss-Bonnet (Euler) density E4 = R^2 - 4 Ric^2 + Riem^2 -/
def E4 (k : ℝ) : ℝ := scal k ^ 2 - 4 * ric2 k + riem2 k

theorem scal_eq (k : ℝ) : scal k = 12 * k := by
  simp [scal, ric, riem, dl, Fin.sum_univ_four]; ring
theorem ric2_eq (k : ℝ) : ric2 k = 36 * k ^ 2 := by
  simp [ric2, ric, riem, dl, Fin.sum_univ_four]; ring
theorem riem2_eq (k : ℝ) : riem2 k = 24 * k ^ 2 := by
  simp [riem2, riem, dl, Fin.sum_univ_four]; ring
theorem E4_eq (k : ℝ) : E4 k = 24 * k ^ 2 := by
  unfold E4; rw [scal_eq, ric2_eq, riem2_eq]; ring

/-- the same polynomial identity in general dimension n: n^2(n-1)^2 - 4 n (n-1)^2 + 2 n (n-1) = n(n-1)(n-2)(n-3) -/
theorem E4_general_dim (n : ℝ) :
    (n * (n - 1)) ^ 2 - 4 * (n * (n - 1) ^ 2) + 2 * (n * (n - 1)) = n * (n - 1) * (n - 2) * (n - 3) := by ring

/-! ### The bridge: int_{S^4_L} E4 = 32 pi^2 chi with chi = 2, for EVERY L -/

theorem s4_euler_integral {L : ℝ} (hL : L ≠ 0) : E4 (1 / L ^ 2) * volS4 L = 64 * π ^ 2 := by
  rw [E4_eq, volS4_eq]; field_simp; ring

theorem s4_euler_number {L : ℝ} (hL : L ≠ 0) : E4 (1 / L ^ 2) * volS4 L = 32 * π ^ 2 * 2 := by
  rw [s4_euler_integral hL]; ring

/-- scale-freeness: two different radii give the same integral -/
theorem s4_euler_scale_free {L₁ L₂ : ℝ} (h₁ : L₁ ≠ 0) (h₂ : L₂ ≠ 0) :
    E4 (1 / L₁ ^ 2) * volS4 L₁ = E4 (1 / L₂ ^ 2) * volS4 L₂ := by
  rw [s4_euler_integral h₁, s4_euler_integral h₂]

/-- 32 pi^2 = int_{S^4(1)} R dV (12 Vol(S^4_1)), and the two elementary factorisations -/
theorem gb_unit_is_scalar_curvature_integral : scal 1 * volS4 1 = 32 * π ^ 2 := by
  rw [scal_eq, volS4_eq]; ring

theorem gb_constant_factorisation :
    (32 * π ^ 2 = (8 * π) * (4 * π)) ∧ (32 * π ^ 2 = 2 * (4 * π) ^ 2) ∧ (32 * π ^ 2 = 12 * (8 * π ^ 2 / 3)) := by
  refine ⟨by ring, by ring, by ring⟩

#print axioms volS4_eq
#print axioms scal_eq
#print axioms ric2_eq
#print axioms riem2_eq
#print axioms E4_eq
#print axioms E4_general_dim
#print axioms s4_euler_integral
#print axioms s4_euler_number
#print axioms s4_euler_scale_free
#print axioms gb_unit_is_scalar_curvature_integral
#print axioms gb_constant_factorisation
