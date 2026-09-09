import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
  A small, executable Lean core for the clock/constitutive gate.

  This file deliberately formalizes only identities that are actually
  established by the symbolic gate: the exponential constitutive law, the
  positivity of its two principal eigenvalues, the factored flat-space
  equation determinant, and the numerical witness for the clock cone.  It is
  not a certificate of the full covariant theory: York/Hodge pseudoinverse
  variation, nonlinear Dirac closure, boosted PPN, FLRW perturbations, and
  the y = 0 endpoint remain outside this file.
  -/

namespace ClockConstitutive

theorem exponential_primitive_mu (y : ℝ) (hy : 0 < y) :
  (2 * y - 2 * y * Real.exp (-y)) / (2 * y) =
      1 - Real.exp (-y) := by
  have hden : (2 * y : ℝ) ≠ 0 :=
    ne_of_gt (mul_pos (by exact zero_lt_two) hy)
  apply (div_eq_iff hden).2
  ring

theorem lambda_perp_pos (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) := by
  have hlt : Real.exp (-y) < (1 : ℝ) := by
    rw [← Real.exp_zero]
    exact Real.exp_lt_exp.mpr (neg_lt_zero.mpr hy)
  exact sub_pos.mpr hlt

theorem lambda_parallel_pos (y : ℝ) (hy : 0 < y) :
  0 < 1 + (y - 1) * Real.exp (-y) := by
  have hlt : Real.exp (-y) < (1 : ℝ) := by
    rw [← Real.exp_zero]
    exact Real.exp_lt_exp.mpr (neg_lt_zero.mpr hy)
  by_cases hle : y ≤ 1
  · have hnonneg : 0 ≤ Real.exp (-y) := le_of_lt (Real.exp_pos (-y))
    have hprod_le : (1 - y) * Real.exp (-y) ≤ Real.exp (-y) := by
      simpa using (mul_le_mul_of_nonneg_right
        (sub_le_self 1 (le_of_lt hy)) hnonneg)
    have hprod_lt : (1 - y) * Real.exp (-y) < (1 : ℝ) :=
      lt_of_le_of_lt hprod_le (by simpa using hlt)
    calc
      0 < 1 - (1 - y) * Real.exp (-y) := sub_pos.mpr hprod_lt
      _ = 1 + (y - 1) * Real.exp (-y) := by ring
  · have hy1 : 1 < y := lt_of_not_ge hle
    have hterm : 0 ≤ (y - 1) * Real.exp (-y) := by
      exact mul_nonneg (sub_nonneg.mpr (le_of_lt hy1))
        (le_of_lt (Real.exp_pos (-y)))
    exact add_pos_of_pos_of_nonneg zero_lt_one hterm

def waveK (kx kz : ℝ) : ℝ := kx ^ 2 + kz ^ 2

def determinant3 (a b c d e f g h i : ℝ) : ℝ :=
  a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

def equationDeterminant (C ell rate kx kz : ℝ) : ℝ :=
  let K := waveK kx kz
  determinant3
    (-4 * K) (-2 * (C - 2) * K) 0
    (2 * rate * (C + 3 * ell) * K) 0 (-2 * ell * K ^ 2)
    (-2 * (3 * C * rate ^ 2 + 9 * ell * rate ^ 2 + 2 * K))
    (4 * K) (2 * rate * (C + 3 * ell) * K)

theorem equation_determinant_factor (C ell rate kx kz : ℝ) :
    equationDeterminant C ell rate kx kz =
      8 * C * waveK kx kz ^ 3 *
        (C ^ 2 * rate ^ 2 + 3 * C * ell * rate ^ 2
          - 2 * C * rate ^ 2 - 2 * ell * waveK kx kz
          - 6 * ell * rate ^ 2) := by
  simp [equationDeterminant, determinant3, waveK]
  ring

theorem witness_clock_speed_squared :
    (2 * (1 / 100 : ℝ)) /
        ((2 - 5 / 3 : ℝ) * (5 / 3 + 3 * (1 / 100 : ℝ))) =
      18 / 509 := by
  norm_num

theorem witness_clock_is_subluminal :
    0 < (18 / 509 : ℝ) ∧ (18 / 509 : ℝ) < 1 := by
  norm_num

end ClockConstitutive
