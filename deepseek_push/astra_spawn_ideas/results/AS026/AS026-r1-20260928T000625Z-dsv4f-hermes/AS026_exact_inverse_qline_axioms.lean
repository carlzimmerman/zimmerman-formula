import Mathlib
import Mathlib.Tactic

/-
  AS026 -- Exact inverse of the algebraic a0 line (Lean 4 certificate).

  Q branch:       g^2 = B^2 + a0*B ,   y = B/a0 > 0 ,  x = g/a0 .
  Exact inverse:  y(x) = (sqrt(1 + 4 x^2) - 1)/2 = 2x^2/(sqrt(1+4x^2)+1).

  Formalized content (all on the declared Q branch):
    A  yQ x >= 0 for every real x        (physical branch, y = B/a0 > 0)
    B  yQ satisfies the forward law: y^2 + y = x^2     (exact inversion)
    C  rationalized (numerically stable) form identity
    D  the OTHER quadratic root satisfies the same raw law (root discarding is
       NOT automatic: the forward equation alone cannot reject it)
    E  the other root is strictly negative (rejected by the physical domain
       y = B/a0 > 0, B = g_N > 0), and on x > 0 the physical root is positive
    F  boundary at g = 0: yQ(0) = 0 (physical), yNeg(0) = -1 (other)
    G  uniqueness on [0, oo): the physical root is the unique nonnegative root
    H  strict monotonicity on [0, oo) (the inverse is unique there)
    I  derivative: y'(x) = 2x/sqrt(1+4x^2)
    J  knee mapping: yQ x = 1 <-> x^2 = 2 ; x = sqrt 2 is the unique preimage
    K  inverse composition: yQ(sqrt(w^2+w)) = w for w >= 0 (surjectivity)
    L  injectivity on [0, oo) from strict monotonicity
    M  NEGATIVE CONTROL: the sign-perturbed inverse -yQ is rejected --
       (a) on x > 0 it violates the forward law, (b) it lies outside the
       physical branch (y > 0). The raw law accepts BOTH roots (D); the branch
       domain is the discriminating condition (E, M).
-/

noncomputable section
open Real

/-- Exact inverse of the algebraic a0 line, dimensionless: y = B/a0 as function of x = g/a0. -/
def yQ (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2

/-- The other algebraic root of w^2 + w = x^2. -/
def yNeg (x : ℝ) : ℝ := -(1 + Real.sqrt (1 + 4 * x ^ 2)) / 2

theorem sqrt_one_add_four_sq_sq (x : ℝ) : (Real.sqrt (1 + 4 * x ^ 2)) ^ 2 = 1 + 4 * x ^ 2 := by
  rw [Real.sq_sqrt]
  nlinarith [sq_nonneg x]

theorem sqrt_one_add_four_sq_pos (x : ℝ) : 0 < Real.sqrt (1 + 4 * x ^ 2) + 1 := by
  nlinarith [Real.sqrt_nonneg (1 + 4 * x ^ 2)]

/- A: physical branch: yQ x >= 0 for every real x. -/
theorem qline_yQ_nonneg (x : ℝ) : 0 ≤ yQ x := by
  unfold yQ
  have hge : 1 ≤ Real.sqrt (1 + 4 * x ^ 2) := by
    have hm : (1 : ℝ) ≤ 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
    calc
      1 = Real.sqrt 1 := by rw [Real.sqrt_one]
      _ ≤ Real.sqrt (1 + 4 * x ^ 2) := Real.sqrt_le_sqrt hm
  nlinarith

/- B: forward law: y(y+1) = x^2, i.e. y^2 + y = x^2. -/
theorem qline_yQ_identity (x : ℝ) : yQ x ^ 2 + yQ x = x ^ 2 := by
  unfold yQ
  have ht2 := sqrt_one_add_four_sq_sq x
  have hfac : ((Real.sqrt (1 + 4 * x ^ 2) - 1) / 2) ^ 2 + (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
      = (Real.sqrt (1 + 4 * x ^ 2) ^ 2 - 1) / 4 := by
    ring
  rw [hfac, ht2]
  ring

/- A': strictly positive for x > 0. -/
theorem qline_yQ_pos (x : ℝ) (hx : 0 < x) : 0 < yQ x := by
  have hnn := qline_yQ_nonneg x
  have hid := qline_yQ_identity x
  nlinarith [hnn, hid, pow_pos hx 2]

/- C: rationalized (numerically stable) form is the same function. -/
theorem rationalized_form (x : ℝ) : 2 * x ^ 2 / (Real.sqrt (1 + 4 * x ^ 2) + 1) = yQ x := by
  unfold yQ
  have ht2 := sqrt_one_add_four_sq_sq x
  have htpos := sqrt_one_add_four_sq_pos x
  rw [eq_comm, eq_div_iff (ne_of_gt htpos)]
  have hcross : (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2 * (Real.sqrt (1 + 4 * x ^ 2) + 1)
      = 2 * x ^ 2 := by
    have htmp : (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2 * (Real.sqrt (1 + 4 * x ^ 2) + 1)
        = (Real.sqrt (1 + 4 * x ^ 2) ^ 2 - 1) / 2 := by ring
    rw [htmp, ht2]
    ring
  exact hcross

/- D: the OTHER root satisfies the same raw law (root discarding is not automatic). -/
theorem other_root_satisfies_raw_law (x : ℝ) : yNeg x ^ 2 + yNeg x = x ^ 2 := by
  unfold yNeg
  have ht2 := sqrt_one_add_four_sq_sq x
  have hfac : (-(1 + Real.sqrt (1 + 4 * x ^ 2)) / 2) ^ 2
      + (-(1 + Real.sqrt (1 + 4 * x ^ 2))) / 2
      = (Real.sqrt (1 + 4 * x ^ 2) ^ 2 - 1) / 4 := by
    ring
  rw [hfac, ht2]
  ring

/- E: the other root is strictly negative for every real x (outside the physical
   domain y = B/a0 > 0, i.e. B = g_N > 0 of the framework contract). -/
theorem other_root_negative (x : ℝ) : yNeg x < 0 := by
  unfold yNeg
  have hnn : 0 ≤ Real.sqrt (1 + 4 * x ^ 2) := Real.sqrt_nonneg (1 + 4 * x ^ 2)
  field_simp
  nlinarith

/- F1: boundary at g = 0: the physical root vanishes. -/
theorem physical_root_at_zero : yQ 0 = 0 := by
  unfold yQ
  norm_num [Real.sqrt_one]

/- F2: boundary at g = 0: the other root sits at -1 (B = -a0). -/
theorem other_root_at_zero : yNeg 0 = -1 := by
  unfold yNeg
  norm_num [Real.sqrt_one]

/- G: uniqueness in [0, oo): any nonnegative solution of the raw law is yQ x. -/
theorem unique_nonneg_root (x : ℝ) {w : ℝ} (hw : 0 ≤ w)
    (hwq : w ^ 2 + w = x ^ 2) : w = yQ x := by
  have hw1 : 0 ≤ 2 * w + 1 := by nlinarith
  have hsq : (2 * w + 1) ^ 2 = 1 + 4 * x ^ 2 := by nlinarith [hwq]
  have hsqrt : Real.sqrt (1 + 4 * x ^ 2) = 2 * w + 1 := by
    rw [← hsq]
    rw [Real.sqrt_sq_eq_abs]
    exact abs_of_nonneg hw1
  unfold yQ
  rw [hsqrt]
  ring

/- H: strict monotonicity of the inverse on [0, oo). -/
theorem qline_inverse_strict_mono {x1 x2 : ℝ} (h1 : 0 ≤ x1) (_h2 : 0 ≤ x2)
    (h12 : x1 < x2) : yQ x1 < yQ x2 := by
  unfold yQ
  have hsum : 0 < x2 + x1 := by nlinarith [h12, h1]
  have hdif : 0 < x2 - x1 := by nlinarith [h12]
  have hsq : x1 ^ 2 < x2 ^ 2 := by
    nlinarith [mul_pos hdif hsum]
  have hs : 1 + 4 * x1 ^ 2 < 1 + 4 * x2 ^ 2 := by nlinarith
  have hsqrt : Real.sqrt (1 + 4 * x1 ^ 2) < Real.sqrt (1 + 4 * x2 ^ 2) := by
    exact Real.sqrt_lt_sqrt (by nlinarith [sq_nonneg x2]) hs
  nlinarith

/- I: derivative of the exact inverse: y'(x) = 2x / sqrt(1 + 4 x^2). -/
theorem qline_inverse_deriv (x : ℝ) : HasDerivAt yQ (2 * x / Real.sqrt (1 + 4 * x ^ 2)) x := by
  have harg : 0 < 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
  have hd : HasDerivAt (fun z : ℝ => 1 + 4 * z ^ 2) (4 * (2 * x)) x := by
    simpa using (((hasDerivAt_id x).pow (2 : ℕ)).const_mul (4 : ℝ)).const_add (1 : ℝ)
  have hds : HasDerivAt (fun z : ℝ => Real.sqrt (1 + 4 * z ^ 2))
      ((4 * (2 * x)) / (2 * Real.sqrt (1 + 4 * x ^ 2))) x :=
    hd.sqrt (ne_of_gt harg)
  have hdy : HasDerivAt (fun z : ℝ => (Real.sqrt (1 + 4 * z ^ 2) - 1) / 2)
      (((4 * (2 * x)) / (2 * Real.sqrt (1 + 4 * x ^ 2))) / 2) x :=
    (hds.sub_const 1).div_const 2
  have hslope : ((4 * (2 * x)) / (2 * Real.sqrt (1 + 4 * x ^ 2))) / 2 =
      2 * x / Real.sqrt (1 + 4 * x ^ 2) := by
    field_simp [ne_of_gt (Real.sqrt_pos.2 harg)]
    ring
  rw [hslope] at hdy
  exact hdy

/- J1: knee mapping -- y = 1 exactly at x^2 = 2. -/
theorem knee_iff (x : ℝ) : yQ x = 1 ↔ x ^ 2 = 2 := by
  constructor
  · intro hy
    have hid := qline_yQ_identity x
    nlinarith
  · intro hx2
    unfold yQ
    have hnine : 1 + 4 * x ^ 2 = 9 := by nlinarith [hx2]
    rw [hnine]
    norm_num

/- J2: knee uniqueness -- x = sqrt 2 is the unique nonnegative preimage of y = 1. -/
theorem knee_unique (x : ℝ) (hx : 0 ≤ x) (hy : yQ x = 1) : x = Real.sqrt 2 := by
  have hx2 : x ^ 2 = 2 := (knee_iff x).mp hy
  have hsq : Real.sqrt (x ^ 2) = Real.sqrt 2 := by rw [hx2]
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg hx] at hsq
  exact hsq

/- K: inverse composition -- for every w >= 0 the point x = sqrt(w^2 + w) is a
   preimage: yQ (sqrt (w^2+w)) = w. -/
theorem inverse_composition (w : ℝ) (hw : 0 ≤ w) : yQ (Real.sqrt (w ^ 2 + w)) = w := by
  unfold yQ
  have hin : 0 ≤ w ^ 2 + w := by nlinarith [hw, sq_nonneg w]
  rw [Real.sq_sqrt hin]
  have harg : 1 + 4 * (w ^ 2 + w) = (2 * w + 1) ^ 2 := by ring
  have hw1 : 0 ≤ 2 * w + 1 := by nlinarith
  have hsqrt : Real.sqrt (1 + 4 * (w ^ 2 + w)) = 2 * w + 1 := by
    rw [harg]
    rw [Real.sqrt_sq_eq_abs]
    exact abs_of_nonneg hw1
  rw [hsqrt]
  ring

/- K': existential form of surjectivity onto [0, oo). -/
theorem surjective_on_nonneg (w : ℝ) (hw : 0 ≤ w) : ∃ x ≥ 0, yQ x = w := by
  refine ⟨Real.sqrt (w ^ 2 + w), Real.sqrt_nonneg (w ^ 2 + w), inverse_composition w hw⟩

/- L: injectivity on [0, oo) (from strict monotonicity). -/
theorem injective_on_nonneg {x1 x2 : ℝ} (h1 : 0 ≤ x1) (h2 : 0 ≤ x2)
    (hy : yQ x1 = yQ x2) : x1 = x2 := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with h | h
  · have hlt := qline_inverse_strict_mono h1 h2 h
    nlinarith
  · have hlt := qline_inverse_strict_mono h2 h1 h
    nlinarith

/- M1 NEGATIVE CONTROL: the sign-perturbed inverse -yQ violates the forward law
   on x > 0 (the law rejects the mirror image). -/
theorem sign_perturbation_rejected {x : ℝ} (hx : 0 < x) :
    0 < yQ x ∧ (-(yQ x)) ^ 2 + (-(yQ x)) ≠ x ^ 2 := by
  constructor
  · exact qline_yQ_pos x hx
  · intro hc
    have hid := qline_yQ_identity x
    have hp := qline_yQ_pos x hx
    nlinarith

/- M2 NEGATIVE CONTROL: the sign-perturbed candidate lies outside the physical
   branch (y > 0); together with D and E this shows the discriminating condition
   for the physical root is the branch domain, not the raw equation. -/
theorem sign_perturbation_outside_domain {x : ℝ} (hx : 0 < x) : -(yQ x) < 0 := by
  nlinarith [qline_yQ_pos x hx]

end

/- Axiom audit: every theorem below must print an axiom list
   subseteq {propext, Classical.choice, Quot.sound}. -/
#print axioms qline_yQ_nonneg
#print axioms qline_yQ_identity
#print axioms qline_yQ_pos
#print axioms rationalized_form
#print axioms other_root_satisfies_raw_law
#print axioms other_root_negative
#print axioms physical_root_at_zero
#print axioms other_root_at_zero
#print axioms unique_nonneg_root
#print axioms qline_inverse_strict_mono
#print axioms qline_inverse_deriv
#print axioms knee_iff
#print axioms knee_unique
#print axioms inverse_composition
#print axioms surjective_on_nonneg
#print axioms injective_on_nonneg
#print axioms sign_perturbation_rejected
#print axioms sign_perturbation_outside_domain
