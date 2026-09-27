import Mathlib

/-!
# CV3 — V0's varied gate: the rule for what it may read

SCOPE. `real_research/chk_v0_2026/CV3_gate_varied.py` varies the gate in V0's static action. Its multipliers (Φ, Ψ, λ)
enter linearly, each paired with a constrained field (u, w, v). Lean certifies the algebra behind the rule. The
Euler–Lagrange equations and their identities are computed in the lane.

* `multiplier_block_det`: a multiplier's 2×2 block [[0, a], [a, X]] has determinant −a², whatever the gate puts in X —
  a gate that reads only the constrained field cannot make the constraint singular.
* `multiplier_rule_four`: the (Φ, u, Ψ, w) Hessian with gate entries only on the constrained fields has determinant
  a² b², independent of every gate entry (readings A and A+).
* `reading_B_singular`: when the gate also reads the multiplier Φ (reading B), the (Φ, u) symbol
  [[B W'' C² k⁴, −2k²/(8πG)], [−2k²/(8πG), 2k²/(8πG)]] is singular exactly at 4πG C² B W'' k² = 1.
* `carrier_blind`: with Φ = u + fΨ/2 − 4πG C B W' and λ = −fΨ + 8πG C B W' (reading A's integrated equations), the dark
  component's potential Φ + λ/2 is u.
-/

open Real Matrix

theorem multiplier_block_det (a X : ℝ) : det !![0, a; a, X] = -a ^ 2 := by
  rw [det_fin_two_of]
  ring

theorem multiplier_rule_four (a b Xuu Xuw Xww : ℝ) :
    det !![0, a, 0, 0; a, Xuu, 0, Xuw; 0, 0, 0, b; 0, Xuw, b, Xww] = a ^ 2 * b ^ 2 := by
  have e : Fin.succAbove (1 : Fin 4) (2 : Fin 3) = 3 := by decide
  simp [det_succ_row_zero, Fin.sum_univ_succ, e]
  ring

theorem reading_B_singular (G C BW2 k : ℝ) (hG : 0 < G) (h : 4 * π * G * BW2 * C ^ 2 * k ^ 2 = 1) :
    det !![BW2 * C ^ 2 * k ^ 4, -2 * k ^ 2 / (8 * π * G); -2 * k ^ 2 / (8 * π * G), 2 * k ^ 2 / (8 * π * G)] = 0 := by
  have hpi : 0 < π := pi_pos
  have h8 : (8 * π * G) ≠ 0 := by positivity
  have h4 : (4 * π * G) ≠ 0 := by positivity
  have hX : BW2 * C ^ 2 * k ^ 2 = 1 / (4 * π * G) := by
    rw [eq_div_iff h4]
    linarith
  have key : det !![BW2 * C ^ 2 * k ^ 4, -2 * k ^ 2 / (8 * π * G); -2 * k ^ 2 / (8 * π * G), 2 * k ^ 2 / (8 * π * G)]
      = 2 * k ^ 4 / (8 * π * G) * (BW2 * C ^ 2 * k ^ 2 - 1 / (4 * π * G)) := by
    rw [det_fin_two_of]
    field_simp
    ring
  rw [key, hX, sub_self, mul_zero]

theorem carrier_blind (u f Psi C B Wp G : ℝ) :
    (u + f * Psi / 2 - 4 * π * G * C * B * Wp) + (-f * Psi + 8 * π * G * C * B * Wp) / 2 = u := by
  ring

#print axioms multiplier_block_det
#print axioms multiplier_rule_four
#print axioms reading_B_singular
#print axioms carrier_blind
