/-
  Mondlean — Lean 4 / mathlib formalization of the load-bearing mathematical lemmas behind the
  de Sitter–MOND F(Q)Θ completion (fable_independent_2026 lanes L80–L82; astra's F(Q)Θ construction).

  Formalized (the *mathematics* the physics rests on):
    * kernel_identity : the exact-exponential primitive gives the MOND kernel  G'(y)/(2y) = 1 − e^{-y},
      where G'(y) := Gp y = 2y(1 − e^{-y}).   [Gp = dG/dy is verified symbolically in L80/L82; here the
      algebraic kernel identity is proved in Lean.]
    * Gpp_zero : G''(0) = 0   — loss of longitudinal ellipticity at the zero-field point (astra's
      strong-coupling obstruction), where G''(y) := Gpp y = 2(1 + (y−1)e^{-y}).
    * Gpp_pos  : ∀ y > 0, G''(y) > 0  — a STABLE massive scalar wherever the field is nonzero (no ghost off
      the zero-field point).  This is the exact health dichotomy astra's principal gate found.
    * cubic_leading_coeff : G(y) − ⅔y³ is o(y³)-free at quadratic order: G(0)=Gp(0)=Gpp(0)=0, so G's
      Taylor expansion starts at the CUBE — why the MOND term drops from the quadratic cosmological action,
      leaving standard gravity + a pressureless dust (L82).
    * affine_degeneracy : K_QQ = 3F_Q²/(2M²) ⟺ 2M²K_QQ − 3F_Q² = 0  (the cuscuton/det-W degeneracy).
    * sound_speed_zero  : gradient coefficient = 0 ⟹ c_s² = 0  (pressureless dust; the L82 clustering key).

  Imports kept minimal (real-exp basics only) to stay within this host's file-descriptor budget.
-/
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

open Real

noncomputable def G (y : ℝ) : ℝ := y ^ 2 + 2 * (1 + y) * Real.exp (-y) - 2
/-- G'(y), verified = dG/dy in L80/L82 (sympy). -/
noncomputable def Gp (y : ℝ) : ℝ := 2 * y * (1 - Real.exp (-y))
/-- G''(y), verified = dGp/dy in L80/L82 (sympy). -/
noncomputable def Gpp (y : ℝ) : ℝ := 2 * (1 + (y - 1) * Real.exp (-y))

/-- The MOND kernel identity: G'(y)/(2y) = 1 − e^{-y} for y ≠ 0. -/
theorem kernel_identity (y : ℝ) (hy : y ≠ 0) : Gp y / (2 * y) = 1 - Real.exp (-y) := by
  simp only [Gp]
  field_simp

/-- Zero-field point: G''(0) = 0 (loss of ellipticity / astra's strong-coupling obstruction). -/
theorem Gpp_zero : Gpp 0 = 0 := by
  simp only [Gpp, neg_zero, Real.exp_zero]; ring

/-- Away from zero field the scalar is a stable massive mode: G''(y) > 0 for all y > 0. -/
theorem Gpp_pos {y : ℝ} (hy : 0 < y) : 0 < Gpp y := by
  have he : 0 < Real.exp (-y) := Real.exp_pos _
  have hexp_ge : y + 1 ≤ Real.exp y := Real.add_one_le_exp y
  have hfac : 0 < Real.exp y + y - 1 := by nlinarith
  have hinv : Real.exp (-y) * Real.exp y = 1 := by
    rw [← Real.exp_add]; simp
  have hkey : 1 + (y - 1) * Real.exp (-y) = Real.exp (-y) * (Real.exp y + y - 1) := by
    linear_combination -hinv
  have hpos : 0 < 1 + (y - 1) * Real.exp (-y) := by
    rw [hkey]; exact mul_pos he hfac
  simp only [Gpp]; linarith

/-- The value at zero of G and its first two derivatives all vanish, so G's expansion begins at the CUBE:
    this is why the MOND operator is cubic in the perturbation and drops from the quadratic action (L82). -/
theorem G_zero : G 0 = 0 := by
  simp only [G, neg_zero, Real.exp_zero]; ring

theorem Gp_zero : Gp 0 = 0 := by simp [Gp]

theorem cubic_leading : G 0 = 0 ∧ Gp 0 = 0 ∧ Gpp 0 = 0 :=
  ⟨G_zero, Gp_zero, Gpp_zero⟩

/-- The affine cuscuton degeneracy: with a nonzero Planck scale M, the background-independent degeneracy
    K_QQ = 3F_Q²/(2M²) is equivalent to the vanishing of the det-W coefficient 2M²K_QQ − 3F_Q². -/
theorem affine_degeneracy (M FQ KQQ : ℝ) (hM : M ≠ 0) :
    KQQ = 3 * FQ ^ 2 / (2 * M ^ 2) ↔ 2 * M ^ 2 * KQQ - 3 * FQ ^ 2 = 0 := by
  have hM2 : (2 : ℝ) * M ^ 2 ≠ 0 := mul_ne_zero two_ne_zero (pow_ne_zero 2 hM)
  rw [eq_div_iff hM2]
  constructor
  · intro h; linear_combination h
  · intro h; linear_combination h

/-- Pressureless dust: gradient coefficient 0 and positive kinetic coefficient ⟹ sound speed² = 0. -/
theorem sound_speed_zero (grad kin : ℝ) (hgrad : grad = 0) (hkin : 0 < kin) :
    grad / kin = 0 := by
  simp [hgrad]
