import Mathlib
import Mathlib.Tactic

/-!
AS055 -- Correlation freedom in the two-channel response.  Lean 4 certificate.

Framework (dimensionless; both a0 footings 9.3619e-11 and 1.1279e-10 m/s^2 carry the
same dimensionless statements, per the framework contract):
  two channel-engagement events A, B with common marginal p = P(A) = P(B) in [0,1];
  union response U(p) = P(A ∪ B) = 2p - P(A ∩ B) = 2p - p^2 - C(p),
  correlation correction C(p) = P(A ∩ B) - p^2 (deviation from stochastic independence);
  admissible (Frechet) interval  max(0, 2p-1) - p^2 <= C(p) <= p - p^2   (in particular
  -p^2 <= C <= p - p^2);
  drive scale  Y = g/s >= 0,  per-channel engagement p(Y) = Y/(1+Y);
  alpha-family  C_alpha(p) = alpha*(p - p^2),  alpha in [0,1].

Certified content:
 1 as055_independent_union_mu2       : union of two INDEPENDENT channels equals MU2:
                                       1 - (1+Y)^(-2) = 2p - p^2.
 2 as055_alpha_family                : exact closed form of the correlated family:
                                       U_alpha(Y) = (Y^2 + (2-alpha)Y)/(1+Y)^2.
 3 as055_union_bounds                : ANY admissible C forces p <= U <= 2p.
 4 as055_perfect_correlation         : perfect correlation (C = p - p^2) collapses the
                                       response to one channel: U = p.
 5 as055_alpha_family_admissible     : alpha-family stays inside the Frechet box:
                                       p^2 <= p^2 + alpha(p-p^2) <= p.
 6 as055_deep_slope_family           : deep slope of the family = 2 - alpha (limit of
                                       the difference quotient at the punctured origin);
                                       kappa = 1/(2-alpha) in [1/2, 1] at fixed vacuum
                                       density: the correlation freedom IS the
                                       kappa-normalization freedom.
 7 as055_perfect_corr_slope          : NEGATIVE CONTROL -- perfect correlation gives
                                       deep slope ONE, not TWO.
-/

noncomputable section
open Set Filter Topology

/-- 1. Independent two-channel OR equals MU2: 1 - (1+Y)^(-2) = 2p - p^2, p = Y/(1+Y). -/
theorem as055_independent_union_mu2 (y : ℝ) (hy : 1 + y ≠ 0) :
    1 - ((1 + y)⁻¹) ^ 2 = 2 * (y / (1 + y)) - (y / (1 + y)) ^ 2 := by
  field_simp [hy]
  ring

/-- 2. Correlated family closed form: U_alpha(Y) = (Y^2 + (2-alpha)Y)/(1+Y)^2. -/
theorem as055_alpha_family (α y : ℝ) (hy : 1 + y ≠ 0) :
    (2 - α) * (y / (1 + y)) - (1 - α) * (y / (1 + y)) ^ 2 =
      (y ^ 2 + (2 - α) * y) / (1 + y) ^ 2 := by
  field_simp [hy]
  ring

/-- 3. Sharp union bounds for ANY admissible C in the Frechet box (-p^2 <= C <= p - p^2):
       p <= P(A ∪ B) = 2p - p^2 - C <= 2p. -/
theorem as055_union_bounds (p C : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (hC0 : -p ^ 2 ≤ C) (hC1 : C ≤ p - p ^ 2) :
    p ≤ 2 * p - p ^ 2 - C ∧ 2 * p - p ^ 2 - C ≤ 2 * p := by
  constructor
  · nlinarith [hC1]
  · nlinarith [hC0]

/-- 4. Perfect correlation: P(A ∩ B) = p (A = B a.s.), C = p - p^2, collapses U to p. -/
theorem as055_perfect_correlation (p : ℝ) :
    2 * p - p ^ 2 - (p - p ^ 2) = p := by
  ring

/-- 5. The alpha-family intersection P(A ∩ B) = p^2 + alpha(p-p^2) stays inside the
       Frechet box: p^2 <= ... <= p for 0 <= alpha <= 1 and 0 <= p <= 1. -/
theorem as055_alpha_family_admissible (α p : ℝ) (hα0 : 0 ≤ α) (hα1 : α ≤ 1)
    (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    p ^ 2 ≤ p ^ 2 + α * (p - p ^ 2) ∧ p ^ 2 + α * (p - p ^ 2) ≤ p := by
  constructor
  · have h1mp : 0 ≤ 1 - p := by linarith
    have hpm : 0 ≤ p * (1 - p) := mul_nonneg hp0 h1mp
    have hprod : 0 ≤ α * (p * (1 - p)) := mul_nonneg hα0 hpm
    nlinarith [hprod]
  · have h1ma : 0 ≤ 1 - α := by linarith
    have h1mp : 0 ≤ 1 - p := by linarith
    have hpm : 0 ≤ p * (1 - p) := mul_nonneg hp0 h1mp
    have hprod : 0 ≤ (1 - α) * (p * (1 - p)) := mul_nonneg h1ma hpm
    nlinarith [hprod]

/-- Quotient identity used in the slope limit (on the punctured neighborhood). -/
theorem as055_family_slope_quotient (α ε : ℝ) (hε : ε ≠ 0) :
    ((2 - α) * ε - (1 - α) * ε ^ 2) / ε = (2 - α) - (1 - α) * ε := by
  field_simp [hε]

/-- 6. Deep slope of the alpha-family response (in the per-channel drive p) is exactly
       2 - alpha:  lim_{eps -> 0, eps != 0} U_alpha(eps)/eps = 2 - alpha. -/
theorem as055_deep_slope_family (α : ℝ) :
    Tendsto (fun ε : ℝ => ((2 - α) * ε - (1 - α) * ε ^ 2) / ε)
        (nhdsWithin (0 : ℝ) {x : ℝ | x ≠ 0}) (𝓝 (2 - α)) := by
  have hEq : (fun ε : ℝ => ((2 - α) * ε - (1 - α) * ε ^ 2) / ε) =ᶠ[nhdsWithin (0 : ℝ) {x : ℝ | x ≠ 0}]
      (fun ε : ℝ => (2 - α) - (1 - α) * ε) := by
    filter_upwards [self_mem_nhdsWithin] with ε hε
    exact as055_family_slope_quotient α ε hε
  have hcont : ContinuousAt (fun ε : ℝ => (2 - α) - (1 - α) * ε) 0 := by
    fun_prop
  have hlim := (hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' hEq.symm
  simpa using hlim

/-- 7. NEGATIVE CONTROL: perfectly correlated channels (U(p) = p, slope one). -/
theorem as055_perfect_corr_slope :
    Tendsto (fun ε : ℝ => ε / ε) (nhdsWithin (0 : ℝ) {x : ℝ | x ≠ 0}) (𝓝 (1 : ℝ)) := by
  have hEq : (fun ε : ℝ => ε / ε) =ᶠ[nhdsWithin (0 : ℝ) {x : ℝ | x ≠ 0}]
      (fun _ : ℝ => (1 : ℝ)) := by
    filter_upwards [self_mem_nhdsWithin] with ε hε
    field_simp [hε]
  have hcont : ContinuousAt (fun _ : ℝ => (1 : ℝ)) 0 := by
    fun_prop
  have hlim := (hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' hEq.symm
  simpa using hlim

#print axioms as055_independent_union_mu2
#print axioms as055_alpha_family
#print axioms as055_union_bounds
#print axioms as055_perfect_correlation
#print axioms as055_alpha_family_admissible
#print axioms as055_deep_slope_family
#print axioms as055_perfect_corr_slope

end
