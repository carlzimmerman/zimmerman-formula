import Mathlib

open Polynomial

/- E2C1 -- Lean certificate of the E2(q) degree-2 structure (Z15 door).
   Context (loaded-not-transcribed): E2Q1 (exit 0, deepseek_push/E2Q1_results.json,
   commit 2e51b7e46) banked E2(q) = a + b q + c q^2 EXACTLY with measured
   a = 0.616696+-0.000230, b = 0.667788+-0.000560, c = 0.190069+-0.000119.

   Model context (W3 Amendment 1): the two-scatter integrand is
   (1 + q*a1) * (s1*(W2 + q*A2) + (c00f + q*c0qf)) with k1(s1) = 1 + q*a1(s1),
   K2tot = W2 + q*A2, c0f = c00f + q*c0qf, and W2, A2, c00f, c0qf q-free.

   HONEST SCOPE / K01 labeling: e2c1P and L1-L4 below are the algebra of the
   model's own integrand definition (consistency-family, A/B-class, same label
   E2Q1 carried); the certificate payload is that these identities are
   UNCONDITIONAL (arbitrary CommRing, no side hypotheses -- the LR4b
   conditional-vs-unconditional trap is respected). Degree EXACTLY 2
   (nonvanishing of the coefficients) is NOT provable over a general ring; it
   is carried at the MEASURED level by E2Q1 (a, b, c all nonzero at
   z = 2682 / 1193 / 1601 from the E2Q1 fit block). Exact closed forms of
   (a, b, c) are OUT of scope (asinh-class u1-dipole averages; barred without
   a pre-registered candidate). -/

section E2C1

variable {R : Type*} [CommRing R]

/-- The E2 two-scatter q-expansion polynomial: its three coefficients are
EXACTLY the q-free integrand expressions (s1*W2 + c00f),
a1*(s1*W2 + c00f) + s1*A2 + c0qf, and a1*(s1*A2 + c0qf). -/
noncomputable def e2c1P (a1 s1 W2 A2 c00f c0qf : R) : R[X] :=
  C (s1 * W2 + c00f)
    + C (a1 * (s1 * W2 + c00f) + s1 * A2 + c0qf) * X
    + C (a1 * (s1 * A2 + c0qf)) * X ^ 2

variable (a1 s1 W2 A2 c00f c0qf q : R)

/-- L1: the q-expansion of the two-scatter integrand is EXACTLY the degree-2
polynomial with q-free coefficients. Unconditional ring identity. -/
theorem e2c1_integrand_q_expansion :
    (1 + q * a1) * (s1 * (W2 + q * A2) + (c00f + q * c0qf))
      = (s1 * W2 + c00f)
        + q * (a1 * (s1 * W2 + c00f) + s1 * A2 + c0qf)
        + q ^ 2 * (a1 * (s1 * A2 + c0qf)) := by
  ring

/-- L2: the integrand equals the evaluation at q of e2c1P. -/
theorem e2c1_poly_eval :
    (e2c1P a1 s1 W2 A2 c00f c0qf).eval q
      = (1 + q * a1) * (s1 * (W2 + q * A2) + (c00f + q * c0qf)) := by
  simp only [e2c1P, eval_add, eval_mul, eval_C, eval_X_pow, eval_X]
  ring

/-- L3: every coefficient of degree k > 2 vanishes -- no higher terms. -/
theorem e2c1_coeff_gt2 (k : ℕ) (hk : 2 < k) :
    (e2c1P a1 s1 W2 A2 c00f c0qf).coeff k = 0 := by
  have hk0 : k ≠ 0 := by omega
  have hk1 : 1 ≠ k := by omega
  have hk2 : k ≠ 2 := by omega
  simp only [e2c1P, coeff_add, coeff_C, coeff_C_mul, coeff_X_pow, coeff_X,
    hk0, hk1, hk2]
  simp

/-- L4: the coefficient of q^2 is EXACTLY a1*(s1*A2 + c0qf) -- q-free by
construction (coefficients live in R; q is the polynomial variable). -/
theorem e2c1_coeff2 :
    (e2c1P a1 s1 W2 A2 c00f c0qf).coeff 2 = a1 * (s1 * A2 + c0qf) := by
  simp only [e2c1P, coeff_add, coeff_C, coeff_C_mul, coeff_X_pow, coeff_X]
  simp

end E2C1

/-- L5: the chain assembly -- with S(q) = 1/3 + (1/3)q + (46/525)q^2 (the
LR9-certified survival law), c1(q) = -S(q) + E2(q) = (a - 1/3) + (b - 1/3)q +
(c - 46/525)q^2. -/
theorem e2c1_c1_quadratic (a b c q : ℚ) :
    -((1:ℚ)/3 + (1:ℚ)/3 * q + (46:ℚ)/525 * q ^ 2) + (a + b * q + c * q ^ 2)
      = (a - 1/3) + (b - 1/3) * q + (c - 46/525) * q ^ 2 := by
  ring

#print axioms e2c1_integrand_q_expansion
#print axioms e2c1_poly_eval
#print axioms e2c1_coeff_gt2
#print axioms e2c1_coeff2
#print axioms e2c1_c1_quadratic
