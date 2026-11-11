/-
LSF1 false twin: each statement below is false and must fail to compile.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/

/-- FALSE: the k^6 candidate (d, z) = (3, 6) would give the deep-MOND exponent 3. -/
theorem lsf1_false_k6_mond : 3 + 6 = 3 := by decide

/-- FALSE: the EOS condition alone forces z = 6. -/
theorem lsf1_false_eos_forces_6 (d z : Nat) (heos : 2 * (d + z) = 3 * z) : z = 6 := by
  omega

/-- FALSE: 3-d Galilean fermions (d, z) = (3, 2) give BK's 3/2 EOS. -/
theorem lsf1_false_3d_galilean : 2 * (3 + 2) = 3 * 2 := by decide
