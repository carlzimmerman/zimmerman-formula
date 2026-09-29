import Mathlib

/-!
AS235 — alpha3-sensitive momentum balance (Tier-0b, run AS235-r1-20260928T223805Z-dsv4f-hermes).

Certified algebraic core used in the M1 / M3a coefficient extraction:
the exact remainder of the u-normalization series

    u0^2 = (1 - a*s - b*s^2)^(-1)  =  1 + a*s + (a^2 + b) * s^2 + O(s^3)

with the closed remainder used by the machine extraction (sympy coefficient
engine and the substitution-back control).  Physical instantiation for the
CT = 1 statement (M3a1): a = 2 Phi_t carries no v^2, b = v^2 + 2 (N.v) + 4 Phi_t^2
carries v^2 with coefficient 1, hence the v^2 coefficient of T^{00}/rho at
O(s^2) equals exactly 1.
-/

theorem inv_series_residue (x : ℝ) (hx : x ≠ 1) :
    (1 - x)⁻¹ = 1 + x + x^2 + x^3 * (1 - x)⁻¹ := by
  field_simp [hx]
  ring_nf

theorem norm_series_remainder (a b s : ℝ) (hs : 1 - a*s - b*s^2 ≠ 0) :
    (1 - a*s - b*s^2)⁻¹ =
      1 + a*s + (a^2 + b) * s^2 + s^3 * (2*a*b + b^2 * s + (a + b*s)^3 * (1 - a*s - b*s^2)⁻¹) := by
  have hqn : a*s + b*s^2 ≠ 1 := by
    intro h
    apply hs
    linarith
  have hsub : 1 - a*s - b*s^2 = 1 - (a*s + b*s^2) := by ring
  rw [hsub]
  convert inv_series_residue (a*s + b*s^2) hqn using 1
  ring_nf

theorem norm_series_s2_coefficient_kinetic (v2 s : ℝ) (hs : 1 - v2*s^2 ≠ 0) :
    (1 - v2*s^2)⁻¹ = 1 + v2*s^2 + s^4 * (v2^2 * (1 - v2*s^2)⁻¹) := by
  field_simp [hs]
  ring_nf

/-!
In the notation of the derivation: writing q = a*s + b*s^2, the first theorem
gives (1 - q)⁻¹ = (1 + q + q^2) + q^3 (1 - q)⁻¹; the second is the s^2-split
of that identity used to read off the s^2 coefficient a^2 + b (remainder
s^3 * r with r = 2*a*b + b^2*s + (a + b*s)^3 * (1 - q)⁻¹); the third is the
pure-kinetic specialization (a = 0, b = v2) giving the kinetic normalization
coefficient 1 at s^2 -- the CT = 1 content of M3a1.
-/

#print axioms inv_series_residue
#print axioms norm_series_remainder
#print axioms norm_series_s2_coefficient_kinetic