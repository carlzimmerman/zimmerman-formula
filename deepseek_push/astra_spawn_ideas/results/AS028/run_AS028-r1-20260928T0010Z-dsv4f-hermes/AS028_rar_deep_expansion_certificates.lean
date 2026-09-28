import Mathlib

/-!
# AS028 — RAR deep expansion with stable evaluation (certificate)

Framework base (adopted inputs, NOT derived here): a0 = kappa*c*sqrt(G*rho_Lambda),
kappa = 1/2 adopted; G, c measured inputs.  This certificate covers EXACT ALGEBRAIC
statements only.  The exponential series, its radius of convergence, the Bernoulli
coefficients and all truncation-error estimates are analytic facts validated
numerically in the run artifacts; they are not Lean statements here.

Certified statements (all exact, real arithmetic):

1. `nu_stable_rearrangement` — the two evaluation forms of the RAR kernel agree:
       1 / (1 - exp(-s)) = exp(s) / (exp(s) - 1)        (s != 0)
   This is the algebra behind the numerically stable evaluation
   (float: -1/expm1(-s) = 1/(1 - exp(-s)) = exp(s)/(exp(s)-1) by the defining
   identity expm1(x) = exp(x) - 1).  The naive form loses ~eps/s digits for
   small s (validated numerically); the rearrangement does not.

2. `h_RAR_rearrangement` — the phantom-boost function used in the MONO splice:
       h_RAR(y) = y*(1/(1 - exp(-s)) - 1) = y/(exp(s) - 1)        (s != 0, s = sqrt y)

3. `deep_series_expansion_terms` / `deep_series_expansion_in_y` — the deep series
   truncation is an exact algebraic identity:
       (1 + s/2 + s^2/12 - s^4/720 + s^6/30240)/s
         = 1/s + 1/2 + s/12 - s^3/720 + s^5/30240
   i.e. nu_RAR(y) = 1/sqrt(y) + 1/2 + sqrt(y)/12 - y^(3/2)/720 + y^(5/2)/30240 + ...,
   displayed through the five explicit deep terms (three nonzero terms beyond the
   leading 1/sqrt(y): 1/2, sqrt(y)/12, -y^(3/2)/720, plus y^(5/2)/30240).
   This is the algebraic core of the deep expansion; the remainder estimate
   (first neglected term -s^7/1209600, absolute; -y^4/1209600 relative to 1/s;
   series radius |s| < 2 pi  <=>  y < 4 pi^2) is analytic and numerically validated.

4. `series_core_algebraic_core` — the eight-term Taylor polynomial of
   (1 - exp(-s))/s and the seven-term deep series are mutual inverses through
   order 7:
       (sum_{k=0}^{7} (-1)^k s^k/(k+1)!) * (1 + s/2 + s^2/12 - s^4/720 + s^6/30240)
         = 1 + s^8*(-1/518400 - 11/7257600 s - 1/87091200 s^3
                    + 1/152409600 s^4 - 1/1219276800 s^5)
   This certifies the coefficient set {1/2, 1/12, -1/720, 1/30240} as the correct
   reciprocal-series coefficients through that order (the inversion step being the
   algebraic content; the Taylor coefficients of the exponential are analytic input).

These do NOT derive kappa = 1/2, do NOT prove convergence of the infinite series,
and do NOT transfer any statement to the filtered MONO branch.  Branch comparison
(RAR vs MONO on the splice neighbourhood) is dimensional/numerical evidence in the
run artifacts, not a Lean theorem.
-/

open Real

namespace AS028

lemma exp_neg_ne_one {s : ℝ} (hs : s ≠ 0) : Real.exp (-s) ≠ 1 := by
  intro h
  rw [Real.exp_eq_one_iff] at h
  exact hs (by linarith)

lemma exp_ne_one {s : ℝ} (hs : s ≠ 0) : Real.exp s ≠ 1 := by
  intro h
  rw [Real.exp_eq_one_iff] at h
  exact hs h

-- 1. stable rearrangement of nu_RAR
theorem nu_stable_rearrangement {s : ℝ} (hs : s ≠ 0) :
    1 / (1 - Real.exp (-s)) = Real.exp s / (Real.exp s - 1) := by
  have h1 : 1 - Real.exp (-s) ≠ 0 := sub_ne_zero.mpr (Ne.symm (exp_neg_ne_one hs))
  have h2 : Real.exp s - 1 ≠ 0 := sub_ne_zero.mpr (exp_ne_one hs)
  have hmul : Real.exp s * (1 - Real.exp (-s)) = Real.exp s - 1 := by
    rw [mul_sub, Real.exp_neg]
    rw [mul_one, mul_inv_cancel₀ (ne_of_gt (Real.exp_pos s))]
  have hmul' : (1 - Real.exp (-s)) * Real.exp s = Real.exp s - 1 := by
    rw [mul_comm, hmul]
  field_simp [h1, h2]
  rw [hmul']

-- 2. h_RAR rearrangement (identically the MONO-splice boost function)
lemma inv_stable_rearrangement {s : ℝ} (hs : s ≠ 0) :
    1 / (1 - Real.exp (-s)) - 1 = 1 / (Real.exp s - 1) := by
  have T1 := nu_stable_rearrangement (s := s) hs
  have h2 : Real.exp s - 1 ≠ 0 := sub_ne_zero.mpr (exp_ne_one hs)
  rw [T1]
  field_simp [h2]
  try ring

theorem h_RAR_rearrangement {s y : ℝ} (hs : s ≠ 0) :
    y * (1 / (1 - Real.exp (-s)) - 1) = y / (Real.exp s - 1) := by
  rw [inv_stable_rearrangement hs]
  ring

-- 3. deep series expansion terms (exact algebraic identity of the truncated form)
theorem deep_series_expansion_terms {s : ℝ} (hs : s ≠ 0) :
    (1 + s / 2 + s ^ 2 / 12 - s ^ 4 / 720 + s ^ 6 / 30240) / s
      = 1 / s + 1 / 2 + s / 12 - s ^ 3 / 720 + s ^ 5 / 30240 := by
  field_simp [hs]
  try ring

theorem deep_series_expansion_in_y {y : ℝ} (hy : 0 < y) :
    (1 + Real.sqrt y / 2 + Real.sqrt y ^ 2 / 12 - Real.sqrt y ^ 4 / 720
        + Real.sqrt y ^ 6 / 30240) / Real.sqrt y
      = 1 / Real.sqrt y + 1 / 2 + Real.sqrt y / 12 - Real.sqrt y ^ 3 / 720
        + Real.sqrt y ^ 5 / 30240 := by
  exact deep_series_expansion_terms (s := Real.sqrt y) (ne_of_gt (Real.sqrt_pos.mpr hy))

-- 4. algebraic core of the reciprocal-series inversion (through order 7)
theorem series_core_algebraic_core {s : ℝ} :
    (1 - s / 2 + s ^ 2 / 6 - s ^ 3 / 24 + s ^ 4 / 120 - s ^ 5 / 720 + s ^ 6 / 5040
        - s ^ 7 / 40320)
        * (1 + s / 2 + s ^ 2 / 12 - s ^ 4 / 720 + s ^ 6 / 30240)
      = 1 + s ^ 8 *
          (-1 / 518400 - 11 / 7257600 * s - 1 / 87091200 * s ^ 3
            + 1 / 152409600 * s ^ 4 - 1 / 1219276800 * s ^ 5) := by
  ring

#check exp_ne_one
#print axioms nu_stable_rearrangement
#print axioms inv_stable_rearrangement
#print axioms h_RAR_rearrangement
#print axioms deep_series_expansion_terms
#print axioms deep_series_expansion_in_y
#print axioms series_core_algebraic_core

end AS028
