import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
Algebraic certificates for the physical-action audit. The EH expansion,
Euler variations, Legendre transform and action-to-symbol identification
are supplied by the companion derivation, not axiomatized as physics here.
These are conditional mathematical statements, not proof of a law of nature.
-/
namespace PhysicalActionAudit

theorem static_matching_fixes_coefficients
    (eta sigma : ℝ)
    (h : ∀ b : ℝ, 0 < b → b < 1 → 1 - eta - sigma * b = b) :
    eta = 1 ∧ sigma = -1 := by
  have hq := h (1 / 4) (by norm_num) (by norm_num)
  have ht := h (3 / 4) (by norm_num) (by norm_num)
  constructor <;> linarith

theorem historical_source_coefficient_negative
    (mu : ℝ) (hmu : 0 < mu) : 1 - (1 : ℝ) - 2 * mu < 0 := by
  linarith

/-- The normalized, computed 4x4 scalar constraint bracket as a linear map. -/
def bracketMap (m k eta : ℝ) (v : Fin 4 → ℝ) : Fin 4 → ℝ :=
  ![-(2*m*k^2)*v 2, -eta*v 3, (2*m*k^2)*v 0-v 3, eta*v 1+v 2]

theorem bracket_has_no_null_vector
    (m k eta : ℝ) (hm : m ≠ 0) (hk : k ≠ 0) (he : eta ≠ 0)
    (v : Fin 4 → ℝ) (h : bracketMap m k eta v = 0) :
    v = 0 := by
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  have h2 := congrFun h 2
  have h3 := congrFun h 3
  simp [bracketMap] at h0 h1 h2 h3
  have hc : 2 * m * k ^ 2 ≠ 0 :=
    mul_ne_zero (mul_ne_zero (by norm_num) hm) (pow_ne_zero 2 hk)
  have hv2 : v 2 = 0 := by simpa [hm, hk] using h0
  have hv3 : v 3 = 0 := h1.resolve_left he
  have hv0 : v 0 = 0 := by
    rw [hv3, sub_zero] at h2
    exact (mul_eq_zero.mp h2).resolve_left hc
  have hv1 : v 1 = 0 := by
    rw [hv2, add_zero] at h3
    exact (mul_eq_zero.mp h3).resolve_left he
  funext i
  fin_cases i <;> simp [hv0, hv1, hv2, hv3]

/-- Positive prefactors 2 M^2/N are omitted; they do not affect the zero set. -/
noncomputable def lapseSymbol (y kpar kperp : ℝ) : ℝ :=
  Real.exp (-y) * (kperp^2 + (1-y)*kpar^2)

theorem lapse_radial_degeneracy :
    lapseSymbol 1 1 0 = 0 := by
  norm_num [lapseSymbol]

theorem lapse_mixed_signature (y : ℝ) (hy : 1 < y) :
    lapseSymbol y 1 0 < 0 ∧ 0 < lapseSymbol y 0 1 := by
  have he : 0 < Real.exp (-y) := Real.exp_pos _
  constructor
  · simp only [lapseSymbol, zero_pow (by decide : 2 ≠ 0), one_pow, zero_add, mul_one]
    exact mul_neg_of_pos_of_neg he (by linarith)
  · simpa [lapseSymbol] using he

theorem nonzero_characteristic_for_every_y_above_one
    (y : ℝ) (hy : 1 < y) :
    ∃ kpar kperp : ℝ, kpar ≠ 0 ∧ lapseSymbol y kpar kperp = 0 := by
  refine ⟨1, Real.sqrt (y-1), by norm_num, ?_⟩
  have hs : (Real.sqrt (y-1))^2 = y-1 := Real.sq_sqrt (by linarith)
  simp [lapseSymbol, hs]

theorem nonzero_clock_potential_cannot_be_stealth
    (rho V : ℝ) (henergy : rho = V) (hV : 0 < V) :
    rho ≠ 0 := by
  linarith

#print axioms static_matching_fixes_coefficients
#print axioms bracket_has_no_null_vector
#print axioms nonzero_characteristic_for_every_y_above_one

end PhysicalActionAudit
