/-
XJ1 MUTATE twin: the statements of XJ1.lean with a sign or a term changed. Every theorem is false and must fail
(expected: exit 1, one error per theorem). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace XJ1_MUTATE

theorem junction_total_flip (T CB CR t : ℝ) (ht : t * (T - CR) = T - CB) : CB + t * (T - CR) = T + CB := by
  linarith

theorem junction_factor_nonneg_flip (T CB CR : ℝ) (h1 : CB ≤ T) (h2 : CR < T) : 0 ≤ (CB - T) / (T - CR) - 1 := by
  apply div_nonneg <;> linarith

theorem junction_outside_monotone_flip (CB CRs CR1 CR2 t : ℝ) (ht : 0 ≤ t) (h12 : CR1 ≤ CR2) :
    CB + t * (CR2 - CRs) ≤ CB + t * (CR1 - CRs) - 1 := by
  have h : t * (CR1 - CRs) ≤ t * (CR2 - CRs) := mul_le_mul_of_nonneg_left (by linarith) ht
  linarith

theorem rescale_gap_flip (CB s : ℝ) : CB - s * CB = (1 + s) * CB := by
  ring

end XJ1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
