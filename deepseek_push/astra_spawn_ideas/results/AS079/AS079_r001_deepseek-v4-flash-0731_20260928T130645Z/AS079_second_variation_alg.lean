/-
AS079 -- Entropy second variation on the constrained shell: Lean 4 certificate
of the algebraic core (all theorems over the reals, no sorry).

  A. log_le_sub_one      -- log x <= x - 1 for x > 0 (the tangent bound; the
     single lemma behind KL nonnegativity and the second-order bound).
  B. kl_nonneg           -- for z > 0: 0 <= z*log z - (z - 1): the POINTWISE
     Bregman/relative-entropy gap integrand is nonnegative.  Hence, on the
     tangent space (where the first variation vanishes), the global gap
     S(rho0) - S(rho0 + eps v) = int[ rho ln(rho/rho0) - (rho - rho0) ] dV >= 0,
     the global strict-concavity statement behind the unique maximum.
  C. kl_pos_of_ne        -- z /= 1 gives 0 < z*log z - (z - 1): equality of the
     gap happens only at the maximizer, i.e. the maximum is UNIQUE.
  D. exponent_two         -- with the thermal input beta = 1/sigma^2 and the
     virial input sigma^2 = C/2 (both declared by the task as adopted
     framework inputs), the profile exponent gamma = beta*C = 2 exactly.
  E. el_identity          -- the Euler-Lagrange identity of the second
     variation's stationarity core:
     log rho + 1 + alpha + beta*(3 sigma^2/2 + Phi) = 0 for the profile
     rho(r) = exp(K - beta*C*log r), K = -1 - alpha - 3 beta sigma^2 / 2.
     Pointwise it implies the first variation vanishes on the constraint
     tangent space (int v = int Phi v = 0), which is what makes the second
     variation the deciding object.
  F. second_order_exact   -- the exact pointwise central-difference
     decomposition at fixed potential, no truncation: for |eps u| < 1,
       (1+eps u) log(1+eps u) + (1-eps u) log(1-eps u)
         = log(1 - eps^2 u^2) + eps u * log((1+eps u)/(1-eps u)).
     With u = v/rho this is the integrand identity behind
       S(rho+eps v) + S(rho-eps v) - 2 S(rho)
         = -eps^2 int v^2/rho dV + O(eps^4)
     (the even O(eps^4,6,...) remainder comes only from the log(1-eps^2 u^2)
     side; the odd terms vanish as an exact algebraic cancellation).
  G. second_order_bound   -- for |eps u| < 1:
       eps^2 u^2 <= -( log(1+eps u) + log(1-eps u) ).
     Pointwise the symmetric part of the central-difference integrand
     dominates the analytic -eps^2 v^2/rho term; integrated this is one
     half of the sign statement delta^2 S = -int (v^2/rho) dV < 0.

Compiled host-side only from the run directory; no files under
fable_independent_2026/lean_2026 are created or modified.
-/
import Mathlib

noncomputable section
open Real
open scoped Real

namespace AS079

-- ============================================================ A. log <= x - 1
lemma log_le_sub_one {x : ℝ} (hx : 0 < x) : Real.log x ≤ x - 1 := by
  by_cases h1 : x = 1
  · rw [h1, Real.log_one]
    norm_num
  · exact le_of_lt (Real.log_lt_sub_one_of_pos hx h1)

-- ============================================================ B. KL nonneg
theorem kl_nonneg {z : ℝ} (hz : 0 < z) :
    0 ≤ z * Real.log z - (z - 1) := by
  have hw : 0 < 1 / z := by positivity
  have hl := log_le_sub_one hw
  have hld : Real.log (1 / z) = -Real.log z := by
    rw [Real.log_div (by norm_num) (ne_of_gt hz)]
    rw [Real.log_one]
    norm_num
  have hlin : -(Real.log z) ≤ 1 / z - 1 := by
    simpa [hld] using hl
  have hmul := mul_le_mul_of_nonneg_left hlin (le_of_lt hz)
  have hneg : z * (-Real.log z) = -(z * Real.log z) := by ring
  have hz1 : z * (1 / z - 1) = 1 - z := by
    field_simp [ne_of_gt hz]
  rw [hneg, hz1] at hmul
  nlinarith

-- ============================================================ C. KL > 0 off z = 1
theorem kl_pos_of_ne {z : ℝ} (hz : 0 < z) (hne : z ≠ 1) :
    0 < z * Real.log z - (z - 1) := by
  have hw : 0 < 1 / z := by positivity
  have hwne : 1 / z ≠ 1 := by
    intro h1
    have hzr : z * (1 / z) = 1 := by field_simp [ne_of_gt hz]
    have hm : z * (1 / z) = z * 1 := by
      rw [h1]
    rw [hzr] at hm
    -- hm : 1 = z * 1
    have : z = 1 := by simpa using hm.symm
    exact hne this
  have hl := Real.log_lt_sub_one_of_pos hw hwne
  have hld : Real.log (1 / z) = -Real.log z := by
    rw [Real.log_div (by norm_num) (ne_of_gt hz)]
    rw [Real.log_one]
    norm_num
  have hlin : -(Real.log z) < 1 / z - 1 := by
    simpa [hld] using hl
  have hmul := mul_lt_mul_of_pos_left hlin hz
  have hneg : z * (-Real.log z) = -(z * Real.log z) := by ring
  have hz1 : z * (1 / z - 1) = 1 - z := by
    field_simp [ne_of_gt hz]
  rw [hneg, hz1] at hmul
  nlinarith

-- ============================================================ D. gamma = 2
theorem exponent_two {C σ2 β : ℝ} (hC : C ≠ 0) (hσ2 : σ2 = C / 2)
    (hβ : β = 1 / σ2) :
    β * C = 2 := by
  rw [hβ, hσ2]
  field_simp [hC]

-- ============================================================ E. EL identity
theorem el_identity {K β C α σ2 : ℝ} (r : ℝ)
    (hK : K = -1 - α - 3 * β * σ2 / 2) :
    Real.log (Real.exp (K - β * C * Real.log r)) + 1 + α
      + β * (3 * σ2 / 2 + C * Real.log r) = 0 := by
  rw [hK]
  rw [Real.log_exp]
  ring

-- ============================================================ F. exact decomposition
theorem second_order_exact {u ε : ℝ} (h : |ε * u| < 1) :
    (1 + ε * u) * Real.log (1 + ε * u) + (1 - ε * u) * Real.log (1 - ε * u)
      = Real.log (1 - ε ^ 2 * u ^ 2)
        + ε * u * Real.log ((1 + ε * u) / (1 - ε * u)) := by
  have hpos1 : 0 < 1 + ε * u := by nlinarith [abs_lt.mp h]
  have hpos2 : 0 < 1 - ε * u := by nlinarith [abs_lt.mp h]
  have hm : Real.log ((1 + ε * u) * (1 - ε * u))
      = Real.log (1 + ε * u) + Real.log (1 - ε * u) :=
    Real.log_mul (ne_of_gt hpos1) (ne_of_gt hpos2)
  have hprod : (1 + ε * u) * (1 - ε * u) = 1 - ε ^ 2 * u ^ 2 := by ring
  have hlog_sum : Real.log (1 + ε * u) + Real.log (1 - ε * u)
      = Real.log (1 - ε ^ 2 * u ^ 2) := by
    rw [← hprod]
    exact hm.symm
  have hdiv : Real.log ((1 + ε * u) / (1 - ε * u))
      = Real.log (1 + ε * u) - Real.log (1 - ε * u) :=
    Real.log_div (ne_of_gt hpos1) (ne_of_gt hpos2)
  calc
    (1 + ε * u) * Real.log (1 + ε * u)
        + (1 - ε * u) * Real.log (1 - ε * u)
        = (Real.log (1 + ε * u) + Real.log (1 - ε * u))
          + ε * u * (Real.log (1 + ε * u) - Real.log (1 - ε * u)) := by ring
    _ = Real.log (1 - ε ^ 2 * u ^ 2)
          + ε * u * (Real.log (1 + ε * u) - Real.log (1 - ε * u)) := by
          rw [hlog_sum]
    _ = Real.log (1 - ε ^ 2 * u ^ 2)
          + ε * u * Real.log ((1 + ε * u) / (1 - ε * u)) := by
          rw [← hdiv]

-- ============================================================ G. eps^2 bound
theorem second_order_bound {u ε : ℝ} (h : |ε * u| < 1) :
    ε ^ 2 * u ^ 2 ≤ -(Real.log (1 + ε * u) + Real.log (1 - ε * u)) := by
  have hpos1 : 0 < 1 + ε * u := by nlinarith [abs_lt.mp h]
  have hpos2 : 0 < 1 - ε * u := by nlinarith [abs_lt.mp h]
  have hsq : (ε * u) ^ 2 < 1 := (sq_lt_one_iff_abs_lt_one (ε * u)).2 h
  have hmain : 0 < 1 - ε ^ 2 * u ^ 2 := by
    nlinarith [hsq]
  have hm : Real.log ((1 + ε * u) * (1 - ε * u))
      = Real.log (1 + ε * u) + Real.log (1 - ε * u) :=
    Real.log_mul (ne_of_gt hpos1) (ne_of_gt hpos2)
  have hprod : (1 + ε * u) * (1 - ε * u) = 1 - ε ^ 2 * u ^ 2 := by ring
  have hlog_sum : Real.log (1 + ε * u) + Real.log (1 - ε * u)
      = Real.log (1 - ε ^ 2 * u ^ 2) := by
    rw [← hprod]
    exact hm.symm
  have hl := log_le_sub_one hmain
  nlinarith [hl, hlog_sum]

-- ============================================================ axiom audit
#print axioms log_le_sub_one
#print axioms kl_nonneg
#print axioms kl_pos_of_ne
#print axioms exponent_two
#print axioms el_identity
#print axioms second_order_exact
#print axioms second_order_bound

end AS079

end
