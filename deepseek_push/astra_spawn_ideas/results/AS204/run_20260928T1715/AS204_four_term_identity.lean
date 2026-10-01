import Mathlib

/-!
AS204 -- algebraic certificate: the four-term Jacobian norm identity.

Curved-leaf derivative bound (derivation.md, eq. 5): for a field A on the round
3-sphere with ambient Jacobian J at x (|x| = 1) and tangent frame {u_a}:
   sum_a ||Proj_T (J u_a)||^2  =  Tr(J^T J) - ||J x||^2 - ||J^T x||^2 + (x^T J x)^2

The projective identity below is the pure-algebraic content (here in the 2x2 case
with the single tangent direction u = (-q, p) orthogonal to x = (p, q)); the S^3
computation in the prototype evaluates the same identity with the recursion-built J.
-/

namespace AS204

open scoped Real

theorem four_term_factored (a b c d p q : ℝ) :
    (((b * p - a * q) ^ 2 + (d * p - c * q) ^ 2)
        - (p * (b * p - a * q) + q * (d * p - c * q)) ^ 2)
    - (((a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2)
        - ((a * p + b * q) ^ 2 + (c * p + d * q) ^ 2)
        - ((a * p + c * q) ^ 2 + (b * p + d * q) ^ 2)
        + (p * (a * p + b * q) + q * (c * p + d * q)) ^ 2))
    = -(p ^ 2 + q ^ 2 - 1)
        * (a ^ 2 * p ^ 2 - a ^ 2 + 2 * a * c * p * q
          + b ^ 2 * p ^ 2 - b ^ 2 + 2 * b * d * p * q
          + c ^ 2 * q ^ 2 - c ^ 2 + d ^ 2 * q ^ 2 - d ^ 2) := by
  ring

/-- Under |x| = 1 the four-term identity holds (frame {x, u} orthonormal). -/
theorem four_term_unit (a b c d p q : ℝ)
    (hunit : p ^ 2 + q ^ 2 = 1) :
    ((b * p - a * q) ^ 2 + (d * p - c * q) ^ 2)
        - (p * (b * p - a * q) + q * (d * p - c * q)) ^ 2
    = (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2)
        - ((a * p + b * q) ^ 2 + (c * p + d * q) ^ 2)
        - ((a * p + c * q) ^ 2 + (b * p + d * q) ^ 2)
        + (p * (a * p + b * q) + q * (c * p + d * q)) ^ 2 := by
  rw [← sub_eq_zero]
  rw [four_term_factored]
  have hf : (p ^ 2 + q ^ 2 - 1 : ℝ) = 0 := by
    nlinarith [hunit]
  rw [hf]
  ring

end AS204