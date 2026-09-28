import Mathlib
open Real

/-!
# AS033 — MONO splice continuity join (certified part)

Scope statement (read before over-reading this certificate):

This file certifies PURE MATHEMATICS about the MONO continuation formula

    h_mono(y) = h_RAR(y_star) + delta * h_p * log((y + y_p) / (y_star + y_p))

for y >= y_star as defined in FRAMEWORK_CONTRACT.md (MONO branch):

  T1  the value join at the splice: h_mono(y_star) = h_RAR(y_star) + delta*h_p*log 1
      = h_RAR(y_star)  (algebraic identity: log 1 = 0);
  T2  real-continuity of the continuation function at the splice point (y_star is an
      arbitrary parameter in these theorems — the TRANSCENDENTAL value
      y_star = 2.337412405266329455558123303201198860792... is carried numerically
      in the companion Python lane, NOT certified here);
  T3  the continuation derivative rule: d/dy h_mono = delta*h_p / (y + y_p) at every
      y with y + y_p ≠ 0 — the exact RHS of the operative max rule
      h'_mono = max(h'_RAR, delta*h_p/(y+y_p)) on the continuation branch.

No claim here asserts or denies any law of nature, any measured value of a0,
kappa, or the physical status of the MONO branch. The splice LOCATION y_star
(transcendental crossing) and the landmarks y_p, h_p are numerical data verified
to 60 digits in as033_splice.py; this file certifies the algebraic/analytic join
that holds for ANY positive parameters.

Bounded prototype: this file compiles with `lake env lean` in ~1-2 min, 1 thread.
-/

noncomputable section

/-- The log-argument at the splice collapses to 1. -/
theorem mono_arg_at_splice (ys yp : ℝ) (hden : ys + yp ≠ 0) :
    (ys + yp) / (ys + yp) = 1 :=
  div_self hden

/-- T1: value continuity at the splice — h_mono(y_star) = h_RAR(y_star) + delta*h_p*ln 1
    = h_RAR(y_star) for any parameters, by log 1 = 0. -/
theorem mono_join_value (hR hp δ ys yp : ℝ) (hden : ys + yp ≠ 0) :
    hR + δ * hp * Real.log ((ys + yp) / (ys + yp)) = hR := by
  have harg : (ys + yp) / (ys + yp) = 1 := div_self hden
  rw [harg, Real.log_one]
  ring

/-- T2: the continuation branch is continuous AT the splice point (joined
    continuously from the RAR segment). -/
theorem mono_continuation_continuousAt (hR hp δ ys yp : ℝ) (hden : ys + yp ≠ 0) :
    ContinuousAt (fun y : ℝ => hR + δ * hp * Real.log ((y + yp) / (ys + yp))) ys := by
  have hphi : ContinuousAt (fun y : ℝ => (y + yp) / (ys + yp)) ys := by
    refine ContinuousAt.div ?hf ?hg ?h0
    · exact (continuous_id.add continuous_const).continuousAt
    · exact continuous_const.continuousAt
    · simpa using hden
  have hlog : ContinuousAt Real.log 1 := Real.continuousAt_log (by norm_num : (1 : ℝ) ≠ 0)
  have hval1 : (ys + yp) / (ys + yp) = 1 := div_self hden
  have hlog' : ContinuousAt Real.log ((ys + yp) / (ys + yp)) := by
    simpa only [hval1] using hlog
  have hcomp0 : ContinuousAt (Real.log ∘ (fun y : ℝ => (y + yp) / (ys + yp))) ys :=
    ContinuousAt.comp (g := Real.log) (f := fun y : ℝ => (y + yp) / (ys + yp)) (x := ys) hlog' hphi
  have hcomp : ContinuousAt (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) ys := by
    convert hcomp0 using 1
    funext y
    rfl
  have hmul : ContinuousAt (fun y : ℝ => (δ * hp) * Real.log ((y + yp) / (ys + yp))) ys :=
    hcomp.const_mul (δ * hp)
  have hcst : ContinuousAt (fun _ : ℝ => hR) ys := continuousAt_const
  exact hcst.add hmul

/-- T3: the continuation derivative rule — on the continuation branch
    h'_mono(y) = delta*h_p / (y + y_p) exactly (the max-rule RHS). -/
theorem mono_continuation_deriv (hR hp δ ys yp y : ℝ) (hden : ys + yp ≠ 0) (hyy : y + yp ≠ 0) :
    HasDerivAt (fun t : ℝ => hR + δ * hp * Real.log ((t + yp) / (ys + yp))) (δ * hp / (y + yp)) y := by
  have hlin : HasDerivAt (fun t : ℝ => t + yp) 1 y := (hasDerivAt_id y).add_const yp
  have hdenc : HasDerivAt (fun _ : ℝ => ys + yp) 0 y := hasDerivAt_const y (ys + yp)
  have hdiv : HasDerivAt (fun t : ℝ => (t + yp) / (ys + yp))
      ((1 * (ys + yp) - (y + yp) * 0) / (ys + yp) ^ 2) y := hlin.div hdenc hden
  have harg_ne : (y + yp) / (ys + yp) ≠ 0 := div_ne_zero hyy hden
  have hlog : HasDerivAt (fun t : ℝ => Real.log ((t + yp) / (ys + yp)))
      (((y + yp) / (ys + yp))⁻¹ * ((1 * (ys + yp) - (y + yp) * 0) / (ys + yp) ^ 2)) y := by
    convert (HasDerivAt.comp (x := y) (h₂ := Real.log)
        (h := fun t : ℝ => (t + yp) / (ys + yp)) (Real.hasDerivAt_log harg_ne) hdiv) using 1
    · rfl
    · rfl
    · funext t; rfl
  have hmul : HasDerivAt (fun t : ℝ => δ * hp * Real.log ((t + yp) / (ys + yp)))
      (δ * hp * (((y + yp) / (ys + yp))⁻¹ * ((1 * (ys + yp) - (y + yp) * 0) / (ys + yp) ^ 2))) y :=
    hlog.const_mul (δ * hp)
  have hcst : HasDerivAt (fun _ : ℝ => hR) 0 y := hasDerivAt_const y hR
  have htot : HasDerivAt (fun t : ℝ => hR + δ * hp * Real.log ((t + yp) / (ys + yp)))
      (0 + δ * hp * (((y + yp) / (ys + yp))⁻¹ * ((1 * (ys + yp) - (y + yp) * 0) / (ys + yp) ^ 2))) y :=
    hcst.add hmul
  have hval : δ * hp * ((ys + yp) / (y + yp) * ((ys + yp) / (ys + yp) ^ 2)) =
      δ * hp / (y + yp) := by
    field_simp [hyy, hden]
  simpa [hval] using htot

end

#print axioms mono_join_value
#print axioms mono_continuation_continuousAt
#print axioms mono_continuation_deriv
