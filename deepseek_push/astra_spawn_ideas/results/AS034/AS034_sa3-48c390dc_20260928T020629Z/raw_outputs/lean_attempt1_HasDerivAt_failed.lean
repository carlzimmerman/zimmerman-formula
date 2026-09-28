/-
FAILED ATTEMPT 1 (preserved, does NOT compile) — AS034_certificate.lean
initial version using HasDerivAt conclusions.

Failure mode: Mathlib elaborates two distinct ℝ-over-ℝ normed-module
instances at different declaration sites (Semiring.toModule vs
(NormedAlgebra.toNormedSpace ℝ).toModule, and the corresponding
AddCommGroup instances). `simpa using hcomp` / `convert hcomp` on the
*theorem statement's* HasDerivAt failed to unify the instance arguments
("Type mismatch: After simplification, term hcomp has type @HasDerivAt ...
NormedAlgebra.toNormedSpace ℝ.toModule ... but is expected to have type
@HasDerivAt ... Semiring.toModule ..."). A later attempt inside a single
tactic block also hit "typeclass instance problem is stuck:
NontriviallyNormedField ?m" when rw-ing `deriv_add_const`.

Resolution adopted in the final certificate: state theorems via
Mathlib's `deriv` (a single fixed constant whose instance arguments are
locked by the library), prove via `Real.deriv_log`, `deriv_div_const`,
`HasDerivAt.deriv` from tactic-local HasDerivAt facts, `deriv_comp`,
`deriv_const_add`, `deriv_const_mul`. Final file compiles, exit 0,
axioms {propext, Classical.choice, Quot.sound}.

This file is archived verbatim from the first write (with the header
comment trimmed) for the failed-attempts record.
-/
import Mathlib
import Mathlib.Tactic

noncomputable section

open Real

namespace AS034

theorem antideriv_log (yp x : ℝ) (hx : 0 < x + yp) :
    HasDerivAt (fun y : ℝ => Real.log (y + yp)) (1 / (x + yp)) x := by
  have hlin : HasDerivAt (fun y : ℝ => y + yp) 1 x := by
    simpa using (hasDerivAt_id x).add_const yp
  have hlog : HasDerivAt Real.log ((x + yp)⁻¹) (x + yp) := by
    apply Real.hasDerivAt_log
    exact ne_of_gt hx
  have hcomp := hlog.comp x hlin
  convert hcomp using 1
  · rfl
  · simp [one_mul, one_div]

theorem antideriv_ratio (yp ys x : ℝ) (hys : 0 < ys + yp) (hx : 0 < x + yp) :
    HasDerivAt (fun y : ℝ => Real.log ((y + yp) / (ys + yp)))
      (1 / (x + yp)) x := by
  have hinner : HasDerivAt (fun y : ℝ => (y + yp) / (ys + yp))
      (1 / (ys + yp)) x := by
    have hlin : HasDerivAt (fun y : ℝ => y + yp) 1 x := by
      simpa using (hasDerivAt_id x).add_const yp
    simpa using hlin.div_const (ys + yp)
  have hle : (x + yp) / (ys + yp) ≠ 0 := by
    exact ne_of_gt (div_pos hx hys)
  have hlog : HasDerivAt Real.log (((x + yp) / (ys + yp))⁻¹)
      ((x + yp) / (ys + yp)) := by
    apply Real.hasDerivAt_log
    exact hle
  have hcomp := hlog.comp x hinner
  convert hcomp using 1
  · rfl
  · field_simp [ne_of_gt hx, ne_of_gt hys]
    ring

end AS034
