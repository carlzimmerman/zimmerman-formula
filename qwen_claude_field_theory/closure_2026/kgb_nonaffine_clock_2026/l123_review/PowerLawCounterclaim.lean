import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/- Conditional arithmetic certificates for P=X^N after the separately derived
   shift-current and homogeneous-density identities. These lemmas contain no
   CMB transfer functions, action variation, clustering or health theorem. -/
namespace L123Counterclaim

theorem exponent_range (N : ℝ) (hN : 2 ≤ N) :
    3 < 6*N/(2*N-1) ∧ 6*N/(2*N-1) ≤ 4 := by
  have hd : 0 < 2*N-1 := by linarith
  constructor
  · apply (lt_div_iff₀ hd).2
    linarith
  · apply (div_le_iff₀ hd).2
    linarith

theorem exponent_sound_identity (N : ℝ) (hN : 2 ≤ N) :
    6*N/(2*N-1) = 3 + 3*(1/(2*N-1)) := by
  have hd : 2*N-1 ≠ 0 := by linarith
  have hcancel : (1/(2*N-1))*(2*N-1) = 1 := div_mul_cancel₀ 1 hd
  calc
    6*N/(2*N-1) = (6*N)*(1/(2*N-1)) := by ring
    _ = 3 + 3*(1/(2*N-1)) := by nlinarith

theorem sound_speed_small (N δ : ℝ) (hδ : 0 < δ)
    (hN : 2 + 1/(2*δ) ≤ N) :
    0 < 1/(2*N-1) ∧ 1/(2*N-1) < δ := by
  have hinv : 0 < 1/(2*δ) := div_pos zero_lt_one (by positivity)
  have hd : 0 < 2*N-1 := by linarith
  have hmul : (1/(2*δ))*(2*δ) = 1 := by
    field_simp
  have hbound : (2 + 1/(2*δ))*(2*δ) ≤ N*(2*δ) :=
    mul_le_mul_of_nonneg_right hN (by positivity)
  constructor
  · exact div_pos zero_lt_one hd
  · apply (div_lt_iff₀ hd).2
    nlinarith

end L123Counterclaim

#print axioms L123Counterclaim.exponent_range
#print axioms L123Counterclaim.exponent_sound_identity
#print axioms L123Counterclaim.sound_speed_small
