/-
AS133: THE TERMINAL HEAT BOUNDARY CONDITION (Tier-0 certificate)
Seed: AS133_derive_the_terminal_heat_boundary_condition.md (sha256 1a03b8f0...30b, verified)
Result contract: RESULT_CONTRACT.json

Content certified (self-contained, no Sorry):
  T1  Nf_double_deriv        : (N*f)'' = N''*f + 2 N' f' + N f''          (analytic core)
  T2  measure_residual       : (Nf)''/N - f'' = 2 (N'/N) f' + (N''/N) f   (the
                               canonical-rel EXPONENT identity whose LHS is the
                               measure residue of the heat-flux lapse)
  T3  endpoint_closed        : L_b = -R_W  =>  L_b + R_W = 0              (terminal
                               closing condition)
  T4  terminal_control_residual : if R_W - R_W^naive = ell * measure (T2) and
                               L_b = -R_W, L_b^naive = -R_W^naive then
                               L_b - L_b^naive = -ell * measure: the NEGATIVE
                               CONTROL is exactly the lapse-residue term, so the
                               control is capable of failing (survives precisely
                               when the lapse identity T2 is non-trivial)
  T5  rw_forms_1d            : algebraic equivalence of the two R_W forms
                               (canonical vs 1d-expanded) used in check A

Runs at fable_independent_2026/lean_2026:   lake env lean <this file>
-/
import Mathlib
open scoped Real Topology

namespace AS133

/-- (N*f)'' = N''*f + 2 N' f' + N f'' (product rule, twice, at any x). -/
theorem Nf_double_deriv (N f : ℝ → ℝ) (x : ℝ)
    (hNd : ∀ y, DifferentiableAt ℝ N y)
    (hfd : ∀ y, DifferentiableAt ℝ f y)
    (hNdd : ∀ y, DifferentiableAt ℝ (deriv N) y)
    (hfdd : ∀ y, DifferentiableAt ℝ (deriv f) y) :
    deriv (fun y => deriv (fun z => N z * f z) y) x
      = deriv (deriv N) x * f x + 2 * deriv N x * deriv f x + N x * deriv (deriv f) x := by
  have hP : (fun y => deriv (fun z => N z * f z) y)
      = fun y => N y * deriv f y + deriv N y * f y := by
    funext y
    calc
      deriv (fun z => N z * f z) y = deriv N y * f y + N y * deriv f y :=
        deriv_mul (hNd y) (hfd y)
      _ = N y * deriv f y + deriv N y * f y := by
        ring
  rw [hP]
  have h1 : DifferentiableAt ℝ (fun y => N y * deriv f y) x :=
    DifferentiableAt.mul (hNd x) (hfdd x)
  have h2 : DifferentiableAt ℝ (fun y => deriv N y * f y) x :=
    DifferentiableAt.mul (hNdd x) (hfd x)
  change deriv ((fun y => N y * deriv f y) + fun y => deriv N y * f y) x
      = deriv (deriv N) x * f x + 2 * deriv N x * deriv f x + N x * deriv (deriv f) x
  rw [deriv_add h1 h2]
  change deriv (N * deriv f) x + deriv (deriv N * f) x
      = deriv (deriv N) x * f x + 2 * deriv N x * deriv f x + N x * deriv (deriv f) x
  rw [deriv_mul (hNd x) (hfdd x)]
  rw [deriv_mul (hNdd x) (hfd x)]
  ring

/-- Measure (canonical-relation exponent) residue identity:
    (Delta(Nf))/N - Delta f  ==  2 (N'/N) f' + (N''/N) f,  flat leaf, 1d. -/
theorem measure_residual (N f : ℝ → ℝ) (x : ℝ)
    (hNd : ∀ y, DifferentiableAt ℝ N y)
    (hfd : ∀ y, DifferentiableAt ℝ f y)
    (hNdd : ∀ y, DifferentiableAt ℝ (deriv N) y)
    (hfdd : ∀ y, DifferentiableAt ℝ (deriv f) y)
    (hN0 : N x ≠ 0) :
    deriv (fun y => deriv (fun z => N z * f z) y) x / N x - deriv (deriv f) x
      = 2 * (deriv N x / N x) * deriv f x + (deriv (deriv N) x / N x) * f x := by
  rw [Nf_double_deriv N f x hNd hfd hNdd hfdd]
  field_simp [hN0]
  ring

/-- Terminal closing condition: L_b = -R_W  iff  L_b + R_W = 0. -/
theorem endpoint_closed (Lb R : ℝ) (h : Lb = -R) : Lb + R = 0 := by
  rw [h]
  ring

/-- Negative control, algebraic core: with
    R_W - R_W^naive = ell * measure , L_b = -R_W , L_b^naive = -R_W^naive :
    L_b - L_b^naive = -ell * measure .  The control is capable of failing:
    it vanishes (naive == correct) exactly when the measure residue is zero. -/
theorem terminal_control_residual (R Rnaive Lb Lbnaive ell measure : ℝ)
    (hR : R - Rnaive = ell * measure)
    (hL : Lb = -R)
    (hLn : Lbnaive = -Rnaive) :
    Lb - Lbnaive = -(ell * measure) := by
  have hneg : -R - -Rnaive = -(R - Rnaive) := by
    ring
  rw [hL, hLn, hneg, hR]

/-- Negative control, analytic instance: measure = T2's residue, so
    L_b - L_b^naive = -ell * (2 (N'/N) f' + (N''/N) f). -/
theorem terminal_control_residual_deriv (N f : ℝ → ℝ) (x : ℝ) (ell : ℝ)
    (R Rnaive Lb Lbnaive : ℝ → ℝ)
    (hNd : ∀ y, DifferentiableAt ℝ N y)
    (hfd : ∀ y, DifferentiableAt ℝ f y)
    (hNdd : ∀ y, DifferentiableAt ℝ (deriv N) y)
    (hfdd : ∀ y, DifferentiableAt ℝ (deriv f) y)
    (hN0 : N x ≠ 0)
    (hR : R x - Rnaive x
        = ell * (deriv (fun y => deriv (fun z => N z * f z) y) x / N x - deriv (deriv f) x))
    (hL : Lb x = -R x)
    (hLn : Lbnaive x = -Rnaive x) :
    Lb x - Lbnaive x
      = -ell * (2 * (deriv N x / N x) * deriv f x + (deriv (deriv N) x / N x) * f x) := by
  have hneg : -R x - -Rnaive x = -(R x - Rnaive x) := by
    ring
  rw [hL, hLn, hneg, hR]
  rw [measure_residual N f x hNd hfd hNdd hfdd hN0]
  ring

/-- Check A core (1d, flat leaf): the two R_W forms agree exactly when
    (Na)'/N = N''/N  (a = N'/N, derivative of the lapse-weight) and the
    measure residual (T2) holds.  X = (N f J_p)'/N, A = (Na)'/N, B = (Nf)''/N,
    C = f'', a = N'/N, fp = f', G = N''/N. -/
theorem rw_forms_1d (X A B C ell a fp : ℝ) (f G : ℝ)
    (hNa : A = G)
    (hme : B - C = 2 * a * fp + f * G) :
    (-X - ell * A + ell * B) = (-X + ell * (f - 1) * A + 2 * ell * a * fp + ell * C) := by
  have hdiff : (-X - ell * A + ell * B) - (-X + ell * (f - 1) * A + 2 * ell * a * fp + ell * C)
      = 0 := by
    calc
      (-X - ell * A + ell * B) - (-X + ell * (f - 1) * A + 2 * ell * a * fp + ell * C)
          = ell * (B - C - 2 * a * fp - f * A) := by
            ring
      _ = ell * (f * G - f * A) := by
            rw [hme]
            ring
      _ = 0 := by
            rw [hNa]
            ring
  exact sub_eq_zero.mp hdiff

end AS133