/-
AS050 (authoritative REDO) — "A branch-specific primitive cannot fix its zero".
Certificate of the core algebraic identities behind the seed claim
   "If F'(X) = mu(sqrt X), then F(X)+C has identical static constitutive response."

Certified here (X > 0, s = sqrt X, w = sqrt(1+4X)):
 1. shift_invariant_derivative:  (F + C)' = F'  — the additive constant is
    invisible to the constitutive response at the derivative level (generic).
 2. exp_primitive_deriv:  d/dX [ X + 2(1+s)e^{-s} ] = 1 - e^{-s} = mu_EXP(s)
    (historical AQUAL branch; the SPEC requirement-12 primitive G(y) with
    X = y^2 and C = -2 differs only by the constant).
 3. mu2_primitive_deriv: d/dX [ X - 8 ln(1+s/2) - 8/(1+s/2) ] = 1 - (1+s/2)^{-2}
    = mu_MU2(s)   (MU2 branch of the framework dictionary).
 4. q_primitive_deriv:  d/dX [ (s/2)w + (1/4) ln(2s+w) - s ] = (w-1)/(2s)
    = mu_Q(s)     (Q branch: g^2 = B^2 + a0 B).
 5. exp_zero_conventions_differ / exp_zero_conventions_same_derivative: the two
    normalizations (C = -2 vs C = 0) differ at X = 0 but share the derivative
    everywhere — the "zero" of the primitive is movable.

No `sorry`.  Axioms expected: {propext, Classical.choice, Quot.sound}.
Compile host only: file lives in the run dir; never written into lean_2026/.
-/
import Mathlib

noncomputable section
open scoped Real
namespace AS050

/-- pointwise add folded: d/dX (f U + g U) = f' + g' -/
lemma add_deriv_pw {f g : ℝ → ℝ} {f' g' x : ℝ}
    (hf : HasDerivAt f f' x) (hg : HasDerivAt g g' x) :
    HasDerivAt (fun U : ℝ => f U + g U) (f' + g') x := by
  have h := hf.add hg
  convert h using 1 <;> first | rfl | (funext U; rfl)

/-- pointwise sub folded: d/dX (f U - g U) = f' - g' -/
lemma sub_deriv_pw {f g : ℝ → ℝ} {f' g' x : ℝ}
    (hf : HasDerivAt f f' x) (hg : HasDerivAt g g' x) :
    HasDerivAt (fun U : ℝ => f U - g U) (f' - g') x := by
  have h := hf.sub hg
  convert h using 1 <;> first | rfl | (funext U; rfl)

/-- pointwise mul folded: d/dX (f U * g U) = f' * g x + f x * g' -/
lemma mul_deriv_pw {f g : ℝ → ℝ} {f' g' x : ℝ}
    (hf : HasDerivAt f f' x) (hg : HasDerivAt g g' x) :
    HasDerivAt (fun U : ℝ => f U * g U) (f' * g x + f x * g') x := by
  have h := hf.mul hg
  convert h using 1 <;> first | rfl | (funext U; rfl)

/-- (F + C)' = F' at X: the additive constant carries no constitutive content. -/
theorem shift_invariant_derivative {F : ℝ → ℝ} {d C : ℝ} {X : ℝ}
    (hF : HasDerivAt F d X) :
    HasDerivAt (fun U : ℝ => F U + C) d X := by
  have hc : HasDerivAt (fun _ : ℝ => C) (0 : ℝ) X := hasDerivAt_const X C
  have hsum := add_deriv_pw hF hc
  rw [add_zero] at hsum
  exact hsum

/-- EXP branch: F_EXP'(X) = 1 - e^{-sqrt X} = mu_EXP(sqrt X),  X > 0. -/
theorem exp_primitive_deriv {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => U + 2 * ((1 + Real.sqrt U) * Real.exp (-Real.sqrt U)))
      (1 - Real.exp (-Real.sqrt X)) X := by
  have hw : Real.sqrt X ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hX)
  have hwid : id X ≠ 0 := by simpa using (ne_of_gt hX)
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt X)) X :=
    (hasDerivAt_id X).sqrt hwid
  have hneg : HasDerivAt (fun U : ℝ => -Real.sqrt U) (-(1 / (2 * Real.sqrt X))) X := hsq.neg
  have hexp : HasDerivAt (fun U : ℝ => Real.exp (-Real.sqrt U))
      (Real.exp (-Real.sqrt X) * (-(1 / (2 * Real.sqrt X)))) X := by
    have hraw := (Real.hasDerivAt_exp (-Real.sqrt X)).comp X hneg
    convert hraw using 1 <;> first | rfl | (funext U; rfl)
  have honep : HasDerivAt (fun U : ℝ => 1 + Real.sqrt U) (1 / (2 * Real.sqrt X)) X := by
    have hh := add_deriv_pw (hasDerivAt_const X (1 : ℝ)) hsq
    rw [zero_add] at hh
    simpa using hh
  have hmul : HasDerivAt
      (fun U : ℝ => (1 + Real.sqrt U) * Real.exp (-Real.sqrt U))
      ((1 / (2 * Real.sqrt X)) * Real.exp (-Real.sqrt X)
        + (1 + Real.sqrt X) * (Real.exp (-Real.sqrt X) * (-(1 / (2 * Real.sqrt X))))) X := by
    simpa using (mul_deriv_pw honep hexp)
  have htwo : HasDerivAt
      (fun U : ℝ => 2 * ((1 + Real.sqrt U) * Real.exp (-Real.sqrt U)))
      (2 * ((1 / (2 * Real.sqrt X)) * Real.exp (-Real.sqrt X)
        + (1 + Real.sqrt X) * (Real.exp (-Real.sqrt X) * (-(1 / (2 * Real.sqrt X)))))) X := by
    simpa using (hmul.const_mul 2)
  have hid : HasDerivAt (fun U : ℝ => U) 1 X := hasDerivAt_id X
  have htot := add_deriv_pw hid htwo
  have hsimpl :
    1 + 2 * ((1 / (2 * Real.sqrt X)) * Real.exp (-Real.sqrt X)
        + (1 + Real.sqrt X) * (Real.exp (-Real.sqrt X) * (-(1 / (2 * Real.sqrt X)))))
      = 1 - Real.exp (-Real.sqrt X) := by
    field_simp [hw] <;> ring
  rw [hsimpl] at htot
  first | exact htot | (convert htot using 1 <;> first | rfl | (funext U; ring))

/-- MU2 branch: F_MU2'(X) = 1 - (1 + sqrt X / 2)^{-2} = mu_MU2(sqrt X),  X > 0. -/
theorem mu2_primitive_deriv {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => U + (-8) * Real.log (1 + Real.sqrt U / 2)
        - 8 * ((1 + Real.sqrt U / 2)⁻¹))
      (1 - 4 / (2 + Real.sqrt X) ^ 2) X := by
  have hw : Real.sqrt X ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hX)
  have hwid : id X ≠ 0 := by simpa using (ne_of_gt hX)
  have hu_pos : 0 < 1 + Real.sqrt X / 2 := by nlinarith [hX, Real.sqrt_nonneg X]
  have hu : 1 + Real.sqrt X / 2 ≠ 0 := ne_of_gt hu_pos
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt X)) X :=
    (hasDerivAt_id X).sqrt hwid
  have hdu : HasDerivAt (fun U : ℝ => 1 + Real.sqrt U / 2) (1 / (2 * Real.sqrt X) / 2) X := by
    have hh := add_deriv_pw (hasDerivAt_const X (1 : ℝ)) (hsq.div_const 2)
    rw [zero_add] at hh
    simpa using hh
  have hln : HasDerivAt (fun U : ℝ => Real.log (1 + Real.sqrt U / 2))
      (((1 + Real.sqrt X / 2)⁻¹) * (1 / (2 * Real.sqrt X) / 2)) X := by
    have hraw := (Real.hasDerivAt_log hu).comp X hdu
    convert hraw using 1 <;> first | rfl | (funext U; rfl)
  have hln8 : HasDerivAt
      (fun U : ℝ => (-8) * Real.log (1 + Real.sqrt U / 2))
      ((-8) * (((1 + Real.sqrt X / 2)⁻¹) * (1 / (2 * Real.sqrt X) / 2))) X := by
    simpa using (hln.const_mul (-8))
  have hinv : HasDerivAt (fun U : ℝ => (1 + Real.sqrt U / 2)⁻¹)
      (-(1 / (2 * Real.sqrt X) / 2) / (1 + Real.sqrt X / 2) ^ 2) X :=
    hdu.inv hu
  have hinv8 : HasDerivAt
      (fun U : ℝ => 8 * ((1 + Real.sqrt U / 2)⁻¹))
      (8 * (-(1 / (2 * Real.sqrt X) / 2) / (1 + Real.sqrt X / 2) ^ 2)) X := by
    simpa using (hinv.const_mul 8)
  have hid : HasDerivAt (fun U : ℝ => U) 1 X := hasDerivAt_id X
  have htot := sub_deriv_pw (add_deriv_pw hid hln8) hinv8
  have hden : 2 + Real.sqrt X ≠ 0 := by nlinarith [hX, Real.sqrt_nonneg X]
  have hsimpl :
    1 + (-8) * (((1 + Real.sqrt X / 2)⁻¹) * (1 / (2 * Real.sqrt X) / 2))
      - 8 * (-(1 / (2 * Real.sqrt X) / 2) / (1 + Real.sqrt X / 2) ^ 2)
      = 1 - 4 / (2 + Real.sqrt X) ^ 2 := by
    field_simp [hw, hu, hden] <;> ring
  rw [hsimpl] at htot
  first | exact htot | (convert htot using 1 <;> first | rfl | (funext U; ring))

/-- Q branch: F_Q'(X) = (sqrt(1+4X) - 1) / (2 sqrt X) = mu_Q(sqrt X),  X > 0. -/
theorem q_primitive_deriv {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => (Real.sqrt U / 2) * Real.sqrt (1 + 4 * U)
        + (Real.log (2 * Real.sqrt U + Real.sqrt (1 + 4 * U)) : ℝ) / 4
        - Real.sqrt U)
      ((Real.sqrt (1 + 4 * X) - 1) / (2 * Real.sqrt X)) X := by
  have hw : Real.sqrt X ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hX)
  have hwid : id X ≠ 0 := by simpa using (ne_of_gt hX)
  have harg : 0 < 1 + 4 * X := by nlinarith [sq_nonneg X]
  have hvpos : 0 < Real.sqrt (1 + 4 * X) := Real.sqrt_pos.2 harg
  have hv : Real.sqrt (1 + 4 * X) ≠ 0 := ne_of_gt hvpos
  have h2w : 0 ≤ 2 * Real.sqrt X := by
    apply mul_nonneg
    · norm_num
    · exact Real.sqrt_nonneg X
  have hpos : 0 < 2 * Real.sqrt X + Real.sqrt (1 + 4 * X) :=
    add_pos_of_nonneg_of_pos h2w hvpos
  have hden : 2 * Real.sqrt X + Real.sqrt (1 + 4 * X) ≠ 0 := ne_of_gt hpos
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt X)) X :=
    (hasDerivAt_id X).sqrt hwid
  have hd4 : HasDerivAt (fun U : ℝ => 1 + 4 * U) 4 X := by
    simpa using (((hasDerivAt_id X).const_mul 4).const_add (1 : ℝ))
  have hds : HasDerivAt (fun U : ℝ => Real.sqrt (1 + 4 * U))
      (4 / (2 * Real.sqrt (1 + 4 * X))) X :=
    hd4.sqrt (ne_of_gt harg)
  have h1 : HasDerivAt (fun U : ℝ => (Real.sqrt U / 2) * Real.sqrt (1 + 4 * U))
      ((1 / (2 * Real.sqrt X) / 2) * Real.sqrt (1 + 4 * X)
        + (Real.sqrt X / 2) * (4 / (2 * Real.sqrt (1 + 4 * X)))) X := by
    simpa using (mul_deriv_pw (hsq.div_const 2) hds)
  have htwo_s : HasDerivAt (fun U : ℝ => 2 * Real.sqrt U)
      (2 * (1 / (2 * Real.sqrt X))) X := by
    simpa using (hsq.const_mul 2)
  have hlin : HasDerivAt (fun U : ℝ => 2 * Real.sqrt U + Real.sqrt (1 + 4 * U))
      (2 * (1 / (2 * Real.sqrt X)) + 4 / (2 * Real.sqrt (1 + 4 * X))) X := by
    simpa using (add_deriv_pw htwo_s hds)
  have hlog : HasDerivAt
      (fun U : ℝ => Real.log (2 * Real.sqrt U + Real.sqrt (1 + 4 * U)))
      ((2 * Real.sqrt X + Real.sqrt (1 + 4 * X))⁻¹
        * (2 * (1 / (2 * Real.sqrt X)) + 4 / (2 * Real.sqrt (1 + 4 * X)))) X := by
    have hraw := (Real.hasDerivAt_log hden).comp X hlin
    convert hraw using 1 <;> first | rfl | (funext U; rfl)
  have hlog4 : HasDerivAt
      (fun U : ℝ => (Real.log (2 * Real.sqrt U + Real.sqrt (1 + 4 * U)) : ℝ) / 4)
      (((2 * Real.sqrt X + Real.sqrt (1 + 4 * X))⁻¹
        * (2 * (1 / (2 * Real.sqrt X)) + 4 / (2 * Real.sqrt (1 + 4 * X)))) / 4) X := by
    simpa using (hlog.div_const 4)
  have htot := sub_deriv_pw (add_deriv_pw h1 hlog4) hsq
  have hvv : Real.sqrt (1 + 4 * X) * Real.sqrt (1 + 4 * X) = 1 + 4 * X :=
    Real.mul_self_sqrt (le_of_lt harg)
  have hww : Real.sqrt X * Real.sqrt X = X := Real.mul_self_sqrt (le_of_lt hX)
  have hvv2 : (Real.sqrt (1 + 4 * X)) ^ 2 = 1 + 4 * X := by
    simpa [sq] using hvv
  have hww2 : (Real.sqrt X) ^ 2 = X := by
    simpa [sq] using hww
  have hsimpl :
    (1 / (2 * Real.sqrt X) / 2) * Real.sqrt (1 + 4 * X)
      + (Real.sqrt X / 2) * (4 / (2 * Real.sqrt (1 + 4 * X)))
      + ((2 * Real.sqrt X + Real.sqrt (1 + 4 * X))⁻¹
        * (2 * (1 / (2 * Real.sqrt X)) + 4 / (2 * Real.sqrt (1 + 4 * X)))) / 4
      - 1 / (2 * Real.sqrt X)
    = (Real.sqrt (1 + 4 * X) - 1) / (2 * Real.sqrt X) := by
    field_simp [hw, hv, hden]
    nlinarith [hvv2, hww2]
  rw [hsimpl] at htot
  first | exact htot | (convert htot using 1 <;> first | rfl | (funext U; ring))

/-- The two normalizations of the historical EXP primitive (C = -2, the SPEC
    requirement-12 convention G(0) = 0; and C = 0) differ at X = 0. -/
theorem exp_zero_conventions_differ :
    (0 : ℝ) - 2 + 2 * (1 + Real.sqrt (0 : ℝ)) * Real.exp (-Real.sqrt (0 : ℝ))
      ≠ (0 : ℝ) + 2 * (1 + Real.sqrt (0 : ℝ)) * Real.exp (-Real.sqrt (0 : ℝ)) := by
  norm_num

/-- ...but they share the constitutive derivative at every X > 0: the difference
    acts only through the constant, which the static response cannot see. -/
theorem exp_zero_conventions_same_derivative {X : ℝ} (hX : 0 < X) :
    HasDerivAt (fun U : ℝ => U + 2 * ((1 + Real.sqrt U) * Real.exp (-Real.sqrt U)) - 2)
      (1 - Real.exp (-Real.sqrt X)) X := by
  have hbase := exp_primitive_deriv hX
  have hshift := shift_invariant_derivative (C := -2) hbase
  first | exact hshift | (convert hshift using 1 <;> first | rfl | (funext U; ring))

end AS050