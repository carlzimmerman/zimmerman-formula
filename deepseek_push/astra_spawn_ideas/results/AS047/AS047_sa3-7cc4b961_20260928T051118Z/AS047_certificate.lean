/-
AS047 -- Uniform force-error versus derivative-error control (Lean 4 certificate).

Registered seed: AS047_uniform_force_error_versus_derivative_error_control.md.
Certified here (exact real-arithmetic statements; the transcendental landmarks
y_p, h_p, y_star are carried numerically in the companion Python run):

  A  log-potential derivative: d/dr (C*ln r) = C/r                       (r > 0)
  B  radial 3-D Laplacian of the log potential:
       (1/r^2) d/dr (r^2 * d/dr C ln r) = C/r^2
       -- the Poisson-inversion identity behind rho_ph = C/(4 pi G r^2)
          for Phi_ph = C ln(r/r0)   [the 'log phantom' density law]
  C  MONO continuation slope rule (the operative derivative rule):
       d/dy [h* + c ln((y+yp)/(y*+yp))] = c/(y+yp)       (y+yp > 0)
       -- the exact derivative of the log-phantom continuation h_mono
          from FRAMEWORK_CONTRACT's MONO cell

The radial-chain profile identity d/dr [r^2 h(y(r))] = 2r h - 2r y h'(y),
y = (r_M/r)^2, is verified numerically (independent_derivative_residuals
~ 1e-21 in AS047_supplementary.py); it is not Lean-certified here.

Axiom discipline: zero `sorry`; printed axioms must be a subset of
{propext, Classical.choice, Quot.sound}.
-/
import Mathlib
import Mathlib.Tactic

noncomputable section

open Real
open scoped Topology Filter

namespace AS047

-- --------------------------------------------------------------------------
-- A. log-potential derivative: deriv (fun r => C * log r) r0 = C / r0
-- --------------------------------------------------------------------------
theorem log_potential_deriv (C r0 : ℝ) (hr : 0 < r0) :
    deriv (fun r : ℝ => C * Real.log r) r0 = C / r0 := by
  have hlog : deriv (fun r : ℝ => Real.log r) r0 = 1 / r0 := by
    simpa using Real.deriv_log (ne_of_gt hr)
  rw [deriv_const_mul C]
  · rw [hlog]
    ring
  · exact Real.differentiableAt_log (ne_of_gt hr)

-- --------------------------------------------------------------------------
-- B. radial 3-D Laplacian of the log potential (Poisson inversion):
--    (1/r^2) d/dr [r^2 * (C ln r)'] = C / r^2
-- --------------------------------------------------------------------------
-- helper: d/dr [r^2 * C/r] = C   (r^2 * Phi' = C r is C-linear)
theorem radial_flux_deriv (C r0 : ℝ) (hr : r0 ≠ 0) :
    deriv (fun r : ℝ => r ^ 2 * (C / r)) r0 = C := by
  have hmul : (fun r : ℝ => r ^ 2 * (C / r)) = fun r : ℝ => C * r := by
    funext r
    field_simp [pow_two, mul_comm, mul_left_comm, mul_assoc, hr]
  rw [hmul]
  simpa using (hasDerivAt_id r0).const_mul C |>.deriv

theorem log_laplacian (C r0 : ℝ) (hr : 0 < r0) :
    deriv (fun r : ℝ => r ^ 2 * deriv (fun s : ℝ => C * Real.log s) r) r0 = C := by
  have hpoint : (fun r : ℝ => deriv (fun s : ℝ => C * Real.log s) r) =ᶠ[𝓝 r0]
                (fun r : ℝ => C / r) := by
    filter_upwards [Ioi_mem_nhds hr] with r hr_pos
    exact log_potential_deriv C r hr_pos
  have hmain : (fun r : ℝ => r ^ 2 * deriv (fun s : ℝ => C * Real.log s) r) =ᶠ[𝓝 r0]
               (fun r : ℝ => r ^ 2 * (C / r)) := by
    filter_upwards [hpoint] with r hrp
    rw [hrp]
  rw [hmain.deriv_eq]
  exact radial_flux_deriv C r0 (ne_of_gt hr)

theorem log_poisson_density (C r0 : ℝ) (hr : 0 < r0) :
    (1 / r0 ^ 2) *
        deriv (fun r : ℝ => r ^ 2 * deriv (fun s : ℝ => C * Real.log s) r) r0
      = C / r0 ^ 2 := by
  rw [log_laplacian C r0 hr]
  field_simp [pow_two, ne_of_gt hr]

-- --------------------------------------------------------------------------
-- C. MONO continuation slope rule (operative derivative rule P(y)):
--    d/dy [h* + c ln((y+yp)/(y*+yp))] = c/(y+yp)          (y+yp > 0)
-- --------------------------------------------------------------------------
theorem mono_continuation_deriv (c yp ys hstar x : ℝ)
    (hys : 0 < ys + yp) (hx : 0 < x + yp) :
    deriv (fun y : ℝ => hstar + c * Real.log ((y + yp) / (ys + yp))) x = c / (x + yp) := by
  have hlin : HasDerivAt (fun y : ℝ => y + yp) 1 x := by
    simpa using (hasDerivAt_id x).add_const yp
  have hid : deriv (fun y : ℝ => y + yp) x = 1 := hlin.deriv
  have hdiv : deriv (fun y : ℝ => (y + yp) / (ys + yp)) x = 1 / (ys + yp) := by
    rw [deriv_div_const]
    rw [hid]
  have hfun :
      (fun y : ℝ => Real.log ((y + yp) / (ys + yp))) =
        Real.log ∘ (fun y : ℝ => (y + yp) / (ys + yp)) := by
    funext y; rfl
  rw [deriv_const_add hstar]
  rw [deriv_const_mul c]
  · rw [hfun, deriv_comp]
    · rw [Real.deriv_log, hdiv]
      rw [inv_div]
      field_simp [ne_of_gt hx, ne_of_gt hys]
    · exact Real.differentiableAt_log (ne_of_gt (div_pos hx hys))
    · fun_prop
  · have hdlog : DifferentiableAt ℝ Real.log ((x + yp) / (ys + yp)) :=
      Real.differentiableAt_log (ne_of_gt (div_pos hx hys))
    have hdin : DifferentiableAt ℝ (fun y : ℝ => (y + yp) / (ys + yp)) x := by
      fun_prop
    exact hdlog.comp x hdin

end AS047

#check AS047.log_potential_deriv
#check AS047.log_poisson_density
#check AS047.mono_continuation_deriv

-- axiom audit (zero sorry required)
#print axioms AS047.log_potential_deriv
#print axioms AS047.log_poisson_density
#print axioms AS047.mono_continuation_deriv
