/-
LSF1 (TOE0 follow-up, 2026-11-10): the dimensional rule of reading F.

A Fermi gas with dispersion c k^z in d space dimensions and no other scale has
  * EOS exponent  P_0 ~ mu^((d+z)/z)      (free Fermi sea), and
  * gradient-dominated (formal) Lagrangian L ~ c q^(d+z).
Deep MOND needs L ~ |grad theta|^3 (d + z = 3); BK's EOS needs P_0 ~ mu^(3/2), i.e. 2(d+z) = 3z.
Both together force (d, z) = (1, 2): one-dimensional Galilean fermions. The k^6 candidate (d, z) = (3, 6)
meets the EOS (2*9 = 3*6) but gives q^9.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/

/-- Both conditions force d = 1, z = 2 (with z > 0). -/
theorem lsf1_only_1d_galilean (d z : Nat) (_hz : 0 < z)
    (hmond : d + z = 3) (heos : 2 * (d + z) = 3 * z) : d = 1 ∧ z = 2 := by
  omega

/-- The EOS condition alone is z = 2d. -/
theorem lsf1_eos_iff (d z : Nat) : 2 * (d + z) = 3 * z ↔ z = 2 * d := by
  omega

/-- The k^6 candidate satisfies the EOS condition ... -/
theorem lsf1_k6_eos : 2 * (3 + 6) = 3 * 6 := by decide

/-- ... and its gradient exponent is 9, not 3. -/
theorem lsf1_k6_gradient : 3 + 6 = 9 ∧ 3 + 6 ≠ 3 := by decide

/-- The crossover k^2 + k^6 in d = 3 has gradient exponents 5 (k^2) and 9 (k^6): neither is 3. -/
theorem lsf1_crossover_ends : 3 + 2 ≠ 3 ∧ 3 + 6 ≠ 3 := by decide
