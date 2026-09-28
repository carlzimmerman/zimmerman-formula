import Mathlib

/-!
# AS018 — Reference potential and gauge-independent force (certificate)

Framework base (adopted inputs): a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2,
C = sqrt(G*M_b*a0)  (so v_flat^4 = G*M_b*a0 = C^2), r_M = sqrt(G*M_b/a0).
Deep-MOND radial sector:  Phi(r) = C*ln(r/r_ref),  |g| = |d Phi/dr| = C/r.
Section D expansion (RAR segment of MONO, y = g_N/a0 = (r_M/r)^2, z = sqrt y):
    g = (C/r) * [1 + z/2 + y/12 - y^2/720 + y^3/30240 + O(y^5)]
with the z^3 coefficient EXACTLY zero (Bernoulli structure of z/(1-e^{-z})).

What is certified (real arithmetic; no physics is claimed by Lean):

1) `grad_gauge_invariance` — adding any constant c to a differentiable
   function leaves its derivative (the force) pointwise unchanged:
       HasDerivAt f f' x  =>  HasDerivAt (fun y => f y + c) f' x.

2) `log_potential_gradient_exact` — the task's principal test identity
   ("Phi = C*ln(r/r_ref); g = dPhi/dr = C/r"):
       HasDerivAt (fun s => C * log(s/r_ref)) (C/r) r      (r > 0, r_ref != 0).

3) `reference_shift_is_constant_shift` — re-referencing the logarithm shifts
   the potential by a constant independent of the evaluation point:
       C*log(s/r_ref2) = C*log(s/r_ref1) + C*log(r_ref1/r_ref2)   (positivity domain).

4) `gradient_reference_independent` — the force is the same function for
   every reference radius (statement 2 specialised with a second r_ref).

5) `well_energy_shift` — at FIXED mass distribution, the fixed-well energy
   E = ∫ ρ_b·Phi dV shifts by exactly c times the mass under the gauge
   Phi -> Phi + c:
       ∫ x in s, ρ x*(Phi x + c) = ∫ x in s, ρ x*Phi x + c * ∫ x in s, ρ x
   (integrable hypotheses). Consequence: E is convention-dependent; a
   boundary condition fixing the reference (box value / reference radius /
   vanishing at infinity where it exists) is REQUIRED to define E, while
   every gradient observable is gauge-invariant (1)-(4).

6) `deep_series_truncated_inverse` — the truncated inverse consistency of
   the deep series. With E = (1 - e^{-z})/z truncated at z^4 and
   F = z/(1-e^{-z}) truncated at z^4 (whose z^3 coefficient is 0 and whose
   z^4 coefficient is -1/720), the product is 1 up to order 5:
       E*F - 1 = z^5/720 + z^6/2160 + z^7/17280 - z^8/86400   (exact poly identity)
   certifying the formal-power-series statements used in section D of the
   derivation (zero coefficient at z^3, -1/720 at z^4).
-/

noncomputable section
open scoped Real
open scoped MeasureTheory
open scoped ENNReal
namespace AS018

-- (1) gradient gauge invariance ----------------------------------------------
theorem grad_gauge_invariance {f : ℝ → ℝ} {f' x c : ℝ}
    (hf : HasDerivAt f f' x) :
    HasDerivAt (fun y : ℝ => f y + c) f' x := by
  have h : HasDerivAt (fun y : ℝ => f y + c) (f' + 0) x := by
    exact hf.add (hasDerivAt_const x c)
  simpa [add_zero] using h

-- (2) principal test identity: d/dr [C ln(r/r_ref)] = C/r ---------------------
lemma log_scaled_deriv {r r_ref : ℝ} (hr : 0 < r) (hr0 : r_ref ≠ 0) :
    HasDerivAt (fun s : ℝ => Real.log (s / r_ref)) (1 / r) r := by
  have hx : r / r_ref ≠ 0 := div_ne_zero (ne_of_gt hr) hr0
  have hlog : HasDerivAt Real.log ((r / r_ref)⁻¹) (r / r_ref) := by
    exact Real.hasDerivAt_log hx
  have hdiv : HasDerivAt (fun s : ℝ => s / r_ref) (1 / r_ref) r := by
    simpa using (hasDerivAt_id r).div_const r_ref
  have hc : HasDerivAt (fun s : ℝ => Real.log (s / r_ref))
      ((r / r_ref)⁻¹ * (1 / r_ref)) r := by
    exact HasDerivAt.comp r hlog hdiv
  convert hc using 1
  field_simp [ne_of_gt hr, hr0]

theorem log_potential_gradient_exact {C r r_ref : ℝ} (hr : 0 < r) (hr0 : r_ref ≠ 0) :
    HasDerivAt (fun s : ℝ => C * Real.log (s / r_ref)) (C / r) r := by
  have hC : HasDerivAt (fun s : ℝ => C * Real.log (s / r_ref)) (C * (1 / r)) r := by
    exact (log_scaled_deriv hr hr0).const_mul C
  simpa [div_eq_mul_inv] using hC

-- (3) re-referencing = adding a constant --------------------------------------
theorem reference_shift_is_constant_shift {C s r_ref1 r_ref2 : ℝ}
    (hs : s ≠ 0) (h1 : r_ref1 ≠ 0) (h2 : r_ref2 ≠ 0) :
    C * Real.log (s / r_ref2) = C * Real.log (s / r_ref1) + C * Real.log (r_ref1 / r_ref2) := by
  rw [Real.log_div hs h2, Real.log_div hs h1, Real.log_div h1 h2]
  ring

-- (4) force independent of the reference radius --------------------------------
theorem gradient_reference_independent {C r r_ref1 r_ref2 : ℝ}
    (hr : 0 < r) (_h1 : r_ref1 ≠ 0) (h2 : r_ref2 ≠ 0) :
    HasDerivAt (fun s : ℝ => C * Real.log (s / r_ref2)) (C / r) r := by
  exact log_potential_gradient_exact hr h2

-- (5) fixed-well energy shift at fixed mass ------------------------------------
open MeasureTheory
theorem well_energy_shift {c : ℝ} {s : Set ℝ} {μ : Measure ℝ} {ρ Φ : ℝ → ℝ}
    (hs : MeasurableSet s)
    (hρ : IntegrableOn ρ s μ)
    (hρΦ : IntegrableOn (fun x : ℝ => ρ x * Φ x) s μ) :
    (∫ x in s, ρ x * (Φ x + c) ∂μ) =
      (∫ x in s, ρ x * Φ x ∂μ) + c * (∫ x in s, ρ x ∂μ) := by
  have hρc : IntegrableOn (fun x : ℝ => c * ρ x) s μ := by
    exact hρ.const_mul c
  calc
    (∫ x in s, ρ x * (Φ x + c) ∂μ) = (∫ x in s, (ρ x * Φ x) + (c * ρ x) ∂μ) := by
      apply setIntegral_congr_ae hs
      exact ae_of_all μ (fun x _ => by ring)
    _ = (∫ x in s, ρ x * Φ x ∂μ) + (∫ x in s, c * ρ x ∂μ) := by
      exact integral_add hρΦ hρc
    _ = (∫ x in s, ρ x * Φ x ∂μ) + c * (∫ x in s, ρ x ∂μ) := by
      congr 1
      exact integral_const_mul c ρ

-- (6) deep-series truncated inverse (certifies zero z^3 and -1/720 at z^4) -------
theorem deep_series_truncated_inverse (z : ℝ) :
    (1 - z / 2 + z ^ 2 / 6 - z ^ 3 / 24 + z ^ 4 / 120) *
      (1 + z / 2 + z ^ 2 / 12 - z ^ 4 / 720) - 1
      = z ^ 5 / 720 + z ^ 6 / 2160 + z ^ 7 / 17280 - z ^ 8 / 86400 := by
  ring

end AS018
-- axiom audit (unfiltered #print axioms); verified subset exactly
-- {propext, Classical.choice, Quot.sound} for all seven theorems above
#print axioms AS018.grad_gauge_invariance
#print axioms AS018.log_scaled_deriv
#print axioms AS018.log_potential_gradient_exact
#print axioms AS018.reference_shift_is_constant_shift
#print axioms AS018.gradient_reference_independent
#print axioms AS018.well_energy_shift
#print axioms AS018.deep_series_truncated_inverse
