/-
AS034 -- Constructing the MONO continuation by integration (Lean 4 certificate).

Operative MONO branch (dimensionless, y = B/a0 > 0):

  h_RAR(y) = y / (exp(sqrt y) - 1),   nu_RAR(y) = 1/(1 - exp(-sqrt y))
  derivative rule:  h'_mono(y) = max(h'_RAR(y), P(y)),  P(y) = c/(y + y_p)
  with c = delta * h_p, delta = 0.05 fixed, y_p the phantom peak, h_p = h_RAR(y_p).

  Continuation (y >= y_star):
  h_mono(y) = h_RAR(y_star) + c * ln((y + y_p)/(y_star + y_p)),
  nu_mono(y) = 1 + h_mono(y)/y.

Certified here (exact algebraic statements only; the transcendental
crossing y_star is carried numerically in the companion Python run):

  A  antiderivative identity:  d/dy ln(y + y_p) = 1/(y + y_p)   (y + y_p > 0)
  B  ratio-form antiderivative: d/dy ln((y+y_p)/(y_star+y_p)) = 1/(y + y_p)
  C  operative rule: d/dy h_mono(y) = c/(y + y_p)      (the declared P(y) rule
     -- the integrated derivative equals the declared phantom slope)
  D  integrated-form continuity at the splice: h_mono(y_star) = h_RAR(y_star)

Axiom discipline: zero `sorry`; printed axioms must be a subset of
{propext, Classical.choice, Quot.sound}.
-/
import Mathlib
import Mathlib.Tactic

noncomputable section

open Real

namespace AS034

-- --------------------------------------------------------------------------
-- A. Antiderivative identity: (d/dy) ln(y + y_p) = 1/(y + y_p)
-- --------------------------------------------------------------------------
theorem antideriv_log (yp x : ℝ) (hx : 0 < x + yp) :
    deriv (fun y : ℝ => Real.log (y + yp)) x = 1 / (x + yp) := by
  have hlin : HasDerivAt (fun y : ℝ => y + yp) 1 x := by
    simpa using (hasDerivAt_id x).add_const yp
  have hid : deriv (fun y : ℝ => y + yp) x = 1 := hlin.deriv
  have hfun :
      (fun y : ℝ => Real.log (y + yp)) = Real.log ∘ (fun y : ℝ => y + yp) := by
    funext y
    rfl
  rw [hfun, deriv_comp]
  · rw [Real.deriv_log, hid]
    rw [mul_one]
    rw [one_div]
  · exact Real.differentiableAt_log (ne_of_gt hx)
  · fun_prop

-- --------------------------------------------------------------------------
-- B. Ratio-form antiderivative (the form used in the operative MONO
--    continuation): d/dy ln((y+y_p)/(y_star+y_p)) = 1/(y + y_p).
-- --------------------------------------------------------------------------
theorem antideriv_ratio (yp ys x : ℝ) (hys : 0 < ys + yp) (hx : 0 < x + yp) :
    deriv (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) x = 1 / (x + yp) := by
  have hlin : HasDerivAt (fun y : ℝ => y + yp) 1 x := by
    simpa using (hasDerivAt_id x).add_const yp
  have hid : deriv (fun y : ℝ => y + yp) x = 1 := hlin.deriv
  have hdiv : deriv (fun y : ℝ => (y + yp) / (ys + yp)) x = 1 / (ys + yp) := by
    rw [deriv_div_const]
    rw [hid]
  have hfun :
      (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) =
        Real.log ∘ (fun y : ℝ => (y + yp) / (ys + yp)) := by
    funext y
    rfl
  rw [hfun, deriv_comp]
  · rw [Real.deriv_log, hdiv]
    -- ((x + yp) / (ys + yp))⁻¹ * (1 / (ys + yp)) = 1 / (x + yp)
    rw [inv_div]
    field_simp [ne_of_gt hx, ne_of_gt hys]
  · exact Real.differentiableAt_log (ne_of_gt (div_pos hx hys))
  · fun_prop

-- --------------------------------------------------------------------------
-- C. Operative rule: h_mono(y) = h_RAR(y_star) + c*ln((y+y_p)/(y_star+y_p))
--    satisfies h_mono'(y) = c/(y + y_p)  -- the declared phantom slope.
-- --------------------------------------------------------------------------
def h_mono (c yp ys hRAR_ys : ℝ) (y : ℝ) : ℝ :=
  hRAR_ys + c * Real.log ((y + yp) / (ys + yp))

theorem mono_deriv_rule (c yp ys hRAR_ys x : ℝ)
    (hys : 0 < ys + yp) (hx : 0 < x + yp) :
    deriv (h_mono c yp ys hRAR_ys) x = c / (x + yp) := by
  unfold h_mono
  rw [deriv_const_add hRAR_ys]
  rw [deriv_const_mul c]
  · rw [antideriv_ratio yp ys x hys hx]
    ring
  · have hdlog : DifferentiableAt ℝ Real.log ((x + yp) / (ys + yp)) :=
      Real.differentiableAt_log (ne_of_gt (div_pos hx hys))
    have hdin : DifferentiableAt ℝ (fun y : ℝ => (y + yp) / (ys + yp)) x := by
      fun_prop
    exact hdlog.comp x hdin

-- --------------------------------------------------------------------------
-- D. Integrated-form continuity at the splice: h_mono(y_star) = h_RAR(y_star).
-- --------------------------------------------------------------------------
theorem mono_continuity_at_splice (c yp ys hRAR_ys : ℝ) (hys : 0 < ys + yp) :
    h_mono c yp ys hRAR_ys ys = hRAR_ys := by
  unfold h_mono
  rw [div_self (ne_of_gt hys), Real.log_one]
  ring

end AS034

-- axiom audit
#print axioms AS034.antideriv_log
#print axioms AS034.antideriv_ratio
#print axioms AS034.mono_deriv_rule
#print axioms AS034.mono_continuity_at_splice
