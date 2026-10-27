import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring

/-!
  Kernel-checked algebra for the Hamiltonian-envelope completion.  This file
  formalizes only the scalar-sector identities proved by the executable gate;
  it is not a certificate of the full covariant metric theory.
-/

namespace RMMGEnvelope

theorem envelope_hda_identity (p s m : ℝ) (hm : m ≠ 0) :
    (p / m) * (s * m) = p * s := by
  field_simp

theorem envelope_stationarity_factorization
    (m mp p s chi : ℝ) (hm : m ≠ 0) :
    (m * chi + mp * (s ^ 2 / 2 - chi ^ 2 / 2)
      - m * chi - p ^ 2 * mp / (2 * m ^ 2)) =
      mp * (s ^ 2 / 2 - chi ^ 2 / 2 - p ^ 2 / (2 * m ^ 2)) := by
  field_simp [hm]
  ring

theorem exponential_mu_positive (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) := by
  have hlt : Real.exp (-y) < (1 : ℝ) := by
    rw [← Real.exp_zero]
    exact Real.exp_lt_exp.mpr (neg_lt_zero.mpr hy)
  exact sub_pos.mpr hlt

theorem static_relay_flux (s m : ℝ) :
    s * m = m * s := by
  ring

end RMMGEnvelope
