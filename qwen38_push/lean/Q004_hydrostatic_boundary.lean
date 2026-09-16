/-
  Q004 -- THE HYDROSTATIC FAMILY AND THE gamma = 2 SELECTION -- the Lean
  certificate that TURNS FALE'S L258 B1 AUDIT INTO A LEMMA.

  FALE'S L258 B1 (correct): hydrostatic balance in a 1/r force admits
      rho(r) = A r^(-gamma),   sigma^2 = C/gamma,
  for EVERY gamma > 0 with the amplitude A FREE. So the balance condition
  fixes NOTHING about sigma^2; "sigma^2 = C/2" (rung 4) is the gamma = 2
  SELECTION, which is the IDENTIFICATION (dust IS the phantom), not a
  consequence of the balance. This file certifies that boundary exactly:

   1. balance_law          sigma^2 * rho' = -rho * C/r  holds identically for
                           rho = A r^(-gamma) with sigma^2 = C/gamma, every
                           gamma > 0 (exact derivative identity)
   2. gamma_sigma_relation gamma = C / sigma^2   (the family parameterization)
   3. family_surjective    the balance leaves sigma^2 FREE: every positive
                           sigma^2 is a valid balance solution
   4. selection_iff        sigma^2 = C/2  <->  gamma = 2
                           (the "dust is the phantom" selection, certified
                           as an EQUIVALENCE, not a balance consequence)

  HONEST SCOPE (stated, not smoothed): the balance law is proven; the
  SELECTION (gamma = 2) is the external identification input. Fable's audit
  is CORRECT and is hereby part of the certified record: rung 4 is
  POSTULATED-by-identification, and the balance contributes the family it
  lives in. Axioms: {propext, Classical.choice, Quot.sound}. Zero sorry.
-/
import Mathlib

open Real

namespace Q004

/-! ## 1. The balance law (for every gamma) -/

/-- The hydrostatic balance sigma^2 * rho' = -rho * C/r holds IDENTICALLY for
    rho = A r^(-gamma) with sigma^2 = C/gamma, for every gamma > 0 and every
    free amplitude A.  Exact derivative identity. -/
theorem balance_law (C A : ℝ) (hC : 0 < C) (hA : 0 < A)
    (gamma : ℝ) (hgam : 0 < gamma) (r : ℝ) (hr : 0 < r) :
    (C / gamma) * (deriv (fun x : ℝ => A * x ^ (-gamma)) r) =
        -(A * r ^ (-gamma)) * (C / r) := by
  have h : HasDerivAt (fun x : ℝ => A * x ^ (-gamma))
      (A * (-gamma * r ^ (-gamma - 1))) r := by
    have hd : HasStrictDerivAt (fun x : ℝ => x ^ (-gamma))
        ((-gamma) * r ^ (-gamma - 1)) r :=
      hasStrictDerivAt_rpow_const_of_ne hr.ne' (-gamma)
    refine HasDerivAt.const_mul A hd.hasDerivAt
  have hderiv : deriv (fun x : ℝ => A * x ^ (-gamma)) r =
      A * (-gamma * r ^ (-gamma - 1)) := by
    exact h.deriv
  have hrpow : r ^ (-gamma - 1) = r ^ (-gamma) / r := by
    have hexp : (-gamma : ℝ) - 1 = -gamma + (-1 : ℝ) := by ring
    rw [hexp, rpow_add (by positivity), rpow_neg_one r]
    field_simp
  rw [hderiv, hrpow]
  field_simp [hgam.ne, hr.ne]

/-! ## 2. The family parameterization -/

/-- gamma = C / sigma^2: the family is parameterized by sigma^2 (equivalently
    gamma), with the amplitude A free. -/
theorem gamma_sigma_relation (C gamma sigma2 : ℝ) (hC : 0 < C)
    (hgam : 0 < gamma) (hs2 : 0 < sigma2) (h : sigma2 = C / gamma) :
    gamma = C / sigma2 := by
  rw [h]
  field_simp [hgam.ne]

/-! ## 3. The balance does NOT select sigma^2 -/

/-- For every gamma > 0, sigma^2 := C/gamma > 0 is a valid balance solution:
    the balance condition leaves sigma^2 free. -/
theorem family_surjective (C : ℝ) (hC : 0 < C) :
    ∀ sigma2 : ℝ, 0 < sigma2 → ∃ gamma : ℝ, 0 < gamma ∧ C / gamma = sigma2 := by
  intro sigma2 hs2
  refine ⟨C / sigma2, ?_, ?_⟩
  · exact div_pos hC hs2
  · field_simp [hs2]

/-! ## 4. The selection (the identification input) -/

/-- sigma^2 = C/2 <-> gamma = 2: the "dust is the phantom" selection is
    certified as an EQUIVALENCE. It is NOT a consequence of the balance law
    (which holds for every gamma); it is the external identification input
    that fixes the amplitude-free family at gamma = 2. -/
theorem selection_iff (C sigma2 gamma : ℝ) (hC : 0 < C)
    (hgam : 0 < gamma) (hs2 : 0 < sigma2) (h : sigma2 = C / gamma) :
    sigma2 = C / 2 ↔ gamma = 2 := by
  constructor
  · intro hsel
    have hnum : (C / 2) * gamma = C := by
      rw [← hsel, h]
      field_simp [hgam.ne]
    nlinarith [hnum]
  · intro hsel
    rw [h, hsel]

/-! ## THE SPINE -/

/-- The boundary in one theorem: the balance holds for every gamma (1), the
    family is parameterized by sigma2 (2), the balance does NOT select
    sigma2 (3), and gamma = 2 is an external EQUIVALENCE (4) -- fable's L258
    B1 audit, certified. -/
theorem the_boundary (C A : ℝ) (hC : 0 < C) (hA : 0 < A)
    (gamma sigma2 : ℝ) (hgam : 0 < gamma) (hs2 : 0 < sigma2)
    (h : sigma2 = C / gamma) :
    ((C / gamma) * (deriv (fun x : ℝ => A * x ^ (-gamma)) 1) =
        -(A * (1 : ℝ) ^ (-gamma)) * C) ∧
    (gamma = C / sigma2) ∧
    (∀ sigma2' : ℝ, 0 < sigma2' → ∃ gamma' : ℝ, 0 < gamma' ∧ C / gamma' = sigma2') ∧
    (sigma2 = C / 2 ↔ gamma = 2) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · have hr : (0 : ℝ) < 1 := by norm_num
    have hb : (C / gamma) * (deriv (fun x : ℝ => A * x ^ (-gamma)) 1) =
        -(A * (1 : ℝ) ^ (-gamma)) * (C / 1) :=
      balance_law C A hC hA gamma hgam 1 hr
    simpa [one_div] using hb
  · exact gamma_sigma_relation C gamma sigma2 hC hgam hs2 h
  · exact family_surjective C hC
  · exact selection_iff C sigma2 gamma hC hgam hs2 h

end Q004

#print axioms Q004.the_boundary
#print axioms Q004.balance_law
#print axioms Q004.gamma_sigma_relation
#print axioms Q004.family_surjective
#print axioms Q004.selection_iff
