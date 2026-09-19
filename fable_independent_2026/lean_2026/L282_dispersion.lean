import Mathlib
/-!
L282 -- the algebraic core of the candidate's scalar dispersion (real_research/clock_2026/L282_scalar_dispersion_from_action.py).
With the pipeline's map c1 = -c3 = K_B, c4 = c14 - K_B, at Q0 = 0 and xi = 0, the machine-built determinant of the Fourier matrix
of the scalar sector (Psi, Phi, T, P) reduces to  A v^2 + B v + C = 0  (the slow root is -C/B to first order),  v = omega^2/k^2,  with the coefficients below (sympy output,
transcribed).  Certified here: (1) C factorises as c2 (2-K_B) [(2-K_B) - (2-c14) J_Y], so C = 0 iff J_Y = beta0 := (2-K_B)/(2-c14),
L279's backreaction coefficient -- the cold-dust theorem; (2) v = 0 is a root iff C = 0; (3) B is |K2| c2 (2-c14) plus the clock-mixing
inertia (2+3c2)(2-K_B)((2-K_B) + J_Y c14); (4) the fuzzy-dark-matter map hbar/(2m) = alpha c <-> m = hbar/(2 alpha c).
-/
namespace L282

def A (K2 c14 c2 : ℝ) : ℝ := K2 * c14 * (3 * c2 + 2)
def B (K2 KB c14 c2 β : ℝ) : ℝ :=
  K2 * c14 * c2 - 2 * K2 * c2 + 3 * KB ^ 2 * c2 + 2 * KB ^ 2 - 3 * KB * β * c14 * c2 - 2 * KB * β * c14
  - 12 * KB * c2 - 8 * KB + 6 * β * c14 * c2 + 4 * β * c14 + 12 * c2 + 8
def C (KB c14 c2 β : ℝ) : ℝ := -c2 * (KB - 2) * (-KB + β * c14 - 2 * β + 2)
noncomputable def β0 (KB c14 : ℝ) : ℝ := (2 - KB) / (2 - c14)

theorem C_factor (KB c14 c2 β : ℝ) :
    C KB c14 c2 β = c2 * (2 - KB) * ((2 - KB) - (2 - c14) * β) := by
  unfold C; ring

/-- the cold-dust theorem: the constant term vanishes exactly at L279's deep-MOND condition J_Y = beta0 -/
theorem C_eq_zero_iff (KB c14 c2 β : ℝ) (h2 : c14 ≠ 2) (hK : KB ≠ 2) (hc : c2 ≠ 0) :
    C KB c14 c2 β = 0 ↔ β = β0 KB c14 := by
  rw [C_factor]; unfold β0
  have h2' : (2 - c14) ≠ 0 := sub_ne_zero.mpr (Ne.symm h2)
  have hK' : (2 - KB) ≠ 0 := sub_ne_zero.mpr (Ne.symm hK)
  constructor
  · intro h
    have h3 : (2 - KB) - (2 - c14) * β = 0 := by
      rcases mul_eq_zero.mp h with h1 | h1
      · rcases mul_eq_zero.mp h1 with h4 | h4
        · exact absurd h4 hc
        · exact absurd h4 hK'
      · exact h1
    rw [eq_div_iff h2']
    linarith
  · intro h
    rw [h]
    have h3 : (2 - c14) * ((2 - KB) / (2 - c14)) = 2 - KB := by field_simp
    rw [h3]; ring

/-- v = 0 (no sound speed) is a root of the dispersion quadratic iff C = 0 -/
theorem zero_root_iff (K2 KB c14 c2 β : ℝ) :
    A K2 c14 c2 * 0 ^ 2 + B K2 KB c14 c2 β * 0 + C KB c14 c2 β = 0 ↔ C KB c14 c2 β = 0 := by
  simp

/-- the inertia: B = |K2| c2 (2 - c14) + (2 + 3 c2)(2 - K_B)((2 - K_B) + J_Y c14)   (for K2 < 0, -K2 = |K2|) -/
theorem B_structure (K2 KB c14 c2 β : ℝ) :
    B K2 KB c14 c2 β = -K2 * c2 * (2 - c14) + (2 + 3 * c2) * (2 - KB) * ((2 - KB) + β * c14) := by
  unfold B; ring

/-- the leading slow root -C/B in closed form: (2-K_B)(J_Y - beta0) over the clock-renormalised inertia -/
theorem slow_root_leading (K2 KB c14 c2 β : ℝ) (hB : B K2 KB c14 c2 β ≠ 0) (hc : c2 ≠ 0) (h2 : (2 - c14) ≠ 0)
    (hD : -K2 + (2 + 3 * c2) * (2 - KB) * ((2 - KB) + β * c14) / (c2 * (2 - c14)) ≠ 0) :
    -C KB c14 c2 β / B K2 KB c14 c2 β
      = (2 - KB) * (β - β0 KB c14)
        / (-K2 + (2 + 3 * c2) * (2 - KB) * ((2 - KB) + β * c14) / (c2 * (2 - c14))) := by
  rw [div_eq_div_iff hB hD, C_factor, B_structure]
  unfold β0
  field_simp
  ring

/-- fuzzy-dark-matter map: hbar/(2m) = alpha c  <->  m = hbar/(2 alpha c) -/
theorem fdm_map (ℏ α c m : ℝ) (hm : m ≠ 0) (hα : α ≠ 0) (hc : c ≠ 0) :
    ℏ / (2 * m) = α * c ↔ m = ℏ / (2 * α * c) := by
  constructor
  · intro h
    rw [div_eq_iff (mul_ne_zero two_ne_zero hm)] at h
    rw [eq_div_iff (mul_ne_zero (mul_ne_zero two_ne_zero hα) hc)]
    linear_combination -h
  · intro h
    rw [eq_div_iff (mul_ne_zero (mul_ne_zero two_ne_zero hα) hc)] at h
    rw [div_eq_iff (mul_ne_zero two_ne_zero hm)]
    linear_combination -h

end L282
#print axioms L282.C_eq_zero_iff
#print axioms L282.zero_root_iff
#print axioms L282.B_structure
#print axioms L282.slow_root_leading
#print axioms L282.fdm_map
