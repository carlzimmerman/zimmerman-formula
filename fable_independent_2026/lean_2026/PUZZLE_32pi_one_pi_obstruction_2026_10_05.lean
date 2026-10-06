import Mathlib

/-!
# PUZZLE_32pi_one_pi_obstruction_2026_10_05 -- why ~60 horizon/vacuum principles never give G rho r*^2 = c^2

Every standard condition linking a horizon of radius r to the vacuum density rho (escape speed, equal areas/entropies, Smarr, Komar, tidal matching,
holographic equipartition; sonnet55_push/puzzle_32pi/p17, p19, p51) produces  G rho r^2 / c^2 = q * pi^e  with q rational and e = +1 or -1,
because G enters through 4 pi G or 8 pi G while geometry contributes rational volume factors. The puzzle needs the value 1.

* `one_pi_obstruction`   : for every rational q and e in {+1, -1},  q * pi^e != 1   (pi is irrational: Mathlib `irrational_pi`).
* `p17_values_never_one` : the concrete values 3/(8 pi), 3/(16 pi), 1/(16 pi), 1/(32 pi), 1/(8 pi), 3 pi/32, 3/(64 pi) are all != 1.
* `gauss_shape_is_pi_free` : a whole-sphere flux balance g (4 pi r^2) = 4 pi G S cancels its pis exactly: g r^2 = G S.
(Not proved here: that NO combination with net pi-power != 0 equals 1 -- that needs pi's transcendence, not yet in Mathlib.)
So the missing principle must contain one factor of pi from geometry (a full solid angle 4 pi, or an area 4 pi r^2) for EACH factor from gravity's 4 pi G:
a Gauss-law-type balance (flux over a whole sphere = 4 pi G x enclosed source) with a pi-free enclosed source. That is the shape to look for.
-/

open Real

theorem one_pi_obstruction (q : ℚ) : ((q : ℝ) * π ≠ 1) ∧ ((q : ℝ) / π ≠ 1) := by
  have hpi := irrational_pi
  have hp : π ≠ 0 := Real.pi_ne_zero
  constructor
  · intro h
    have hq : (q : ℝ) ≠ 0 := by intro h0; rw [h0, zero_mul] at h; exact zero_ne_one h
    have : π = ((q⁻¹ : ℚ) : ℝ) := by
      rw [Rat.cast_inv]; field_simp; linarith [h]
    exact hpi ⟨q⁻¹, this.symm⟩
  · intro h
    have : π = (q : ℝ) := by field_simp at h; linarith [h]
    exact hpi ⟨q, this.symm⟩

theorem p17_values_never_one :
    (3 / (8 * π) ≠ 1) ∧ (3 / (16 * π) ≠ 1) ∧ (1 / (16 * π) ≠ 1) ∧ (1 / (32 * π) ≠ 1) ∧ (1 / (8 * π) ≠ 1) ∧ (3 * π / 32 ≠ 1) ∧ (3 / (64 * π) ≠ 1) := by
  have h1 := (one_pi_obstruction (3 / 8)).2
  have h2 := (one_pi_obstruction (3 / 16)).2
  have h3 := (one_pi_obstruction (1 / 16)).2
  have h4 := (one_pi_obstruction (1 / 32)).2
  have h5 := (one_pi_obstruction (1 / 8)).2
  have h6 := (one_pi_obstruction (3 / 32)).1
  have h7 := (one_pi_obstruction (3 / 64)).2
  push_cast at h1 h2 h3 h4 h5 h6 h7
  refine ⟨fun h => h1 (by rw [div_div]; exact h), fun h => h2 (by rw [div_div]; exact h), fun h => h3 (by rw [div_div]; exact h),
    fun h => h4 (by rw [div_div]; exact h), fun h => h5 (by rw [div_div]; exact h), fun h => h6 (by linarith [h]), fun h => h7 (by rw [div_div]; exact h)⟩

/-- the Gauss-law shape: flux of a field of strength g over a whole sphere equals 4 pi G times a pi-free source S; the pis cancel. -/
theorem gauss_shape_is_pi_free {g r G S : ℝ} (_hr : 0 < r) (h : g * (4 * π * r ^ 2) = 4 * π * G * S) : g * r ^ 2 = G * S := by
  have hp : (4 * π) ≠ 0 := by positivity
  have : 4 * π * (g * r ^ 2) = 4 * π * (G * S) := by linarith [h]
  exact mul_left_cancel₀ hp this

#print axioms one_pi_obstruction
#print axioms p17_values_never_one
#print axioms gauss_shape_is_pi_free
