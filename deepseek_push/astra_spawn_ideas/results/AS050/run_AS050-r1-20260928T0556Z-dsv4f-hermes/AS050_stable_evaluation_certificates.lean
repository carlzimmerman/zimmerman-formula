import Mathlib

/-!
# AS050 — Stable evaluation of the RAR deep x (certificate)

Framework base (adopted inputs, NOT derived here): a0 = kappa*c*sqrt(G*rho_Lambda),
kappa = 1/2 adopted; G, c measured inputs; x = g/a0 = y*nu_RAR(y) = y/(1-exp(-sqrt(y))),
y = B/a0 > 0, s = sqrt(y).  This certificate covers EXACT ALGEBRAIC statements only.

The exponential's Taylor series, the radius of convergence |s| < 2 pi (pole of
s/(1-e^{-s}) at s = 2 pi i, i.e. y < 4 pi^2), the Bernoulli-coefficient identification
and all truncation-error estimates are analytic facts validated numerically in the run
artifacts; they are not Lean statements here.

Certified statements:

1. `nu_stable_rearrangement` — the two evaluation forms agree:
       1 / (1 - exp(-s)) = exp(s) / (exp(s) - 1)        (s != 0)
   This is the algebra behind the dispatch's "multiply by exp(+sqrt(y))" candidate form.
   (fp64 evaluation note, measured in the run: this identity is algebraically exact, but
   computing exp(s) - 1 by subtraction in fp64 re-introduces cancellation for small s;
   the numerically stable evaluation is -1/expm1(-s), definitionally expm1(x) = exp(x)-1,
   or the expm1-free Bernoulli series.  The identity itself is what is certified here.)

2. `x_stable_form_exp` — total-acceleration form of the same identity:
       y / (1 - exp(-s)) = y * exp(s) / (exp(s) - 1)    (s != 0)

3. `x_stable_form_exp_neg` — the expm1-defining rearrangement:
       y / (1 - exp(-s)) = -y / (exp(-s) - 1)           (s != 0)
   (expm1(-s) = exp(-s) - 1 by definition, so this is -y/expm1(-s).)

4. `x_deep_rearrangement` — the phantom-boost split of the total acceleration:
       y / (1 - exp(-s)) = y + y / (exp(s) - 1)         (s != 0)

5. `deep_x_series_terms` — the deep-x series through s^7 (ring identity):
       s * (1 + s/2 + s^2/12 - s^4/720 + s^6/30240)
         = s + s^2/2 + s^3/12 - s^5/720 + s^7/30240
   i.e. x(s) = s + s^2/2 + s^3/12 - s^5/720 + s^7/30240 + ... (odd powers >= 5 absent).

6. `deep_x_over_s_terms` / `deep_x_over_s_in_y` — the dispatch's claimed route
   x/sqrt(y) = 1 + s/2 + s^2/12 - s^4/720 + ... displayed through the five explicit
   terms, as an exact algebraic identity, in s and in the y-variable (s = sqrt y, y > 0).

7. `series_core_algebraic_core` — the six-term Taylor polynomial of (1-exp(-s))/s and
   the six-term deep-x series are mutual inverses through order 6:
       (sum_{k=0}^{6} (-1)^k s^k/(k+1)!) * (1 + s/2 + s^2/12 - s^4/720 + s^6/30240)
         = 1 + s^7*(1/40320 + 19/1814400*s + 1/1814400*s^2
                     - 1/21772800*s^4 + 1/152409600*s^5)
   This certifies the coefficient set {1/2, 1/12, -1/720, 1/30240, 0, ...} as the correct
   reciprocal-series coefficients through that order, i.e. exactly the algebra of the
   deep-series route; the Taylor coefficients of the exponential are analytic input.

These do NOT derive kappa = 1/2, do NOT prove convergence of the infinite series, and do
NOT transfer any statement to the filtered MONO branch (the MONO deep-inheritance
statement is identity-by-construction on (0, y*] plus measured fp64 residuals in the run
artifacts, not a Lean theorem).  Branch distinctness (Q, RAR, MU2, EXP, MONO, criterion B)
is dimensional/numerical evidence in the run artifacts.
-/


open Real

namespace AS050

lemma exp_neg_ne_one {s : ℝ} (hs : s ≠ 0) : Real.exp (-s) ≠ 1 := by
  intro h
  rw [Real.exp_eq_one_iff] at h
  exact hs (by linarith)

lemma exp_ne_one {s : ℝ} (hs : s ≠ 0) : Real.exp s ≠ 1 := by
  intro h
  rw [Real.exp_eq_one_iff] at h
  exact hs h

-- 1. stable rearrangement of nu_RAR (the exp-multiplied form, algebraically)
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

-- 2. total-acceleration (x) form of the exp-multiplied rearrangement
theorem x_stable_form_exp {y s : ℝ} (hs : s ≠ 0) :
    y / (1 - Real.exp (-s)) = y * Real.exp s / (Real.exp s - 1) := by
  have T := nu_stable_rearrangement (s := s) hs
  calc
    y / (1 - Real.exp (-s)) = y * (1 / (1 - Real.exp (-s))) := by ring
    _ = y * (Real.exp s / (Real.exp s - 1)) := by rw [T]
    _ = y * Real.exp s / (Real.exp s - 1) := by ring

-- 3. expm1-defining rearrangement: expm1(-s) = exp(-s) - 1
theorem x_stable_form_exp_neg {y s : ℝ} (hs : s ≠ 0) :
    y / (1 - Real.exp (-s)) = -y / (Real.exp (-s) - 1) := by
  have h1 : 1 - Real.exp (-s) ≠ 0 := sub_ne_zero.mpr (Ne.symm (exp_neg_ne_one hs))
  have h3 : Real.exp (-s) - 1 ≠ 0 := sub_ne_zero.mpr (exp_neg_ne_one hs)
  field_simp [h1, h3]
  ring

-- 4. phantom-boost split: x = y + y/(e^s - 1)
theorem x_deep_rearrangement {y s : ℝ} (hs : s ≠ 0) :
    y / (1 - Real.exp (-s)) = y + y / (Real.exp s - 1) := by
  have h2 : Real.exp s - 1 ≠ 0 := sub_ne_zero.mpr (exp_ne_one hs)
  rw [x_stable_form_exp (y := y) (s := s) hs]
  field_simp [h2]
  ring

-- 5. deep-x series terms (ring identity through s^7: x = s*Q(s), Q = 1 + s/2 + s^2/12 - s^4/720 + s^6/30240)
theorem deep_x_series_terms {s : ℝ} :
    s * (1 + s / 2 + s ^ 2 / 12 - s ^ 4 / 720 + s ^ 6 / 30240)
      = s + s ^ 2 / 2 + s ^ 3 / 12 - s ^ 5 / 720 + s ^ 7 / 30240 := by
  ring

-- 6. claimed route x/sqrt(y) = 1 + s/2 + s^2/12 - s^4/720 + ... (exact truncated identity)
theorem deep_x_over_s_terms {s : ℝ} (hs : s ≠ 0) :
    1 + s / 2 + s ^ 2 / 12 - s ^ 4 / 720 + s ^ 6 / 30240
      = (s + s ^ 2 / 2 + s ^ 3 / 12 - s ^ 5 / 720 + s ^ 7 / 30240) / s := by
  rw [← deep_x_series_terms]
  field_simp [hs]

theorem deep_x_series_in_y {y : ℝ} :
    Real.sqrt y * (1 + Real.sqrt y / 2 + Real.sqrt y ^ 2 / 12 - Real.sqrt y ^ 4 / 720
        + Real.sqrt y ^ 6 / 30240)
      = Real.sqrt y + Real.sqrt y ^ 2 / 2 + Real.sqrt y ^ 3 / 12 - Real.sqrt y ^ 5 / 720
        + Real.sqrt y ^ 7 / 30240 := by
  exact deep_x_series_terms (s := Real.sqrt y)

theorem deep_x_over_s_in_y {y : ℝ} (hy : 0 < y) :
    1 + Real.sqrt y / 2 + Real.sqrt y ^ 2 / 12 - Real.sqrt y ^ 4 / 720
        + Real.sqrt y ^ 6 / 30240
      = (Real.sqrt y + Real.sqrt y ^ 2 / 2 + Real.sqrt y ^ 3 / 12 - Real.sqrt y ^ 5 / 720
        + Real.sqrt y ^ 7 / 30240) / Real.sqrt y := by
  exact deep_x_over_s_terms (s := Real.sqrt y) (ne_of_gt (Real.sqrt_pos.mpr hy))

-- 7. algebraic core of the reciprocal-series inversion (through order 6)
theorem series_core_algebraic_core {s : ℝ} :
    (1 - s / 2 + s ^ 2 / 6 - s ^ 3 / 24 + s ^ 4 / 120 - s ^ 5 / 720 + s ^ 6 / 5040)
      * (1 + s / 2 + s ^ 2 / 12 - s ^ 4 / 720 + s ^ 6 / 30240)
      = 1 + s ^ 7 * (1 / 40320 + 19 / 1814400 * s + 1 / 1814400 * s ^ 2
          - 1 / 21772800 * s ^ 4 + 1 / 152409600 * s ^ 5) := by
  ring

#print axioms nu_stable_rearrangement
#print axioms x_stable_form_exp
#print axioms x_stable_form_exp_neg
#print axioms x_deep_rearrangement
#print axioms deep_x_series_terms
#print axioms deep_x_over_s_terms
#print axioms deep_x_series_in_y
#print axioms deep_x_over_s_in_y
#print axioms series_core_algebraic_core

end AS050
