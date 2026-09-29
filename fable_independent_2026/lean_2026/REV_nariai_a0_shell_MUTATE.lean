import Mathlib

/-!
# MineM5-A: the Nariai a0-shell identity r_a0(M_Nariai)/L = sqrt(Z/(3 sqrt 3)) and what imposing it forces

Source lane: real_research/reviews/mi_nariai_forcing_2026.py, S1 (lines ~62-72: "r_a0(M_Nariai)/L = sqrt(Z/(3 sqrt 3)) EXACTLY"),
  S2 (lines ~74-90: "requiring r_a0(M_Nariai) = L => Z = 3 sqrt 3", "kappa_forced = 2 sqrt(2 pi)/9").

CERTIFIED (premises => conclusions; pure real algebra):
* `nariai_shell_ratio`: for G, H, c, Z > 0, with a0 := c H / Z, M_N := c^3/(3 sqrt 3 G H) and L := c/H,
  sqrt(G M_N / a0) / L = sqrt(Z/(3 sqrt 3)).
* `nariai_ratio_eq_one_iff`: that ratio equals 1 iff Z = 3 sqrt 3.
* `kappa_forced`: sqrt(8 pi/3)/(3 sqrt 3) = 2 sqrt(2 pi)/9 (kappa := sqrt(8 pi/3)/Z, i.e. a0 = kappa c sqrt(G rho_Lambda) with H^2 = 8 pi G rho/3).
* `forced_differs_from_canonical`: the forced Z = 3 sqrt 3 is strictly below the canonical Z = sqrt(32 pi/3) (because pi > 3), so the forced a0 is larger by the
  factor sqrt(32 pi/3)/(3 sqrt 3) > 1 (`a0_forced_over_canonical`).

NOT certified: that the shell of the maximal de Sitter black hole SHOULD coincide with the horizon (the lane's condition is POSTULATED, and the lane itself
states it is the ninth principle tried against the same target, so no evidential weight); that M_Nariai = c^3/(3 sqrt 3 G H) is the Schwarzschild-de Sitter
maximum (taken as the definition of M_N here; the Lean corpus only has the M^2 Lambda = 1/9 form in ALPHA_A_rn_ds_dirac_extremal); the empirical a0 box
[0.84, 1.36]e-10 m/s^2 and its "viable" verdict (empirical, not certified); any numerical a0.  kappa = 1/2 is FITTED and is NOT derived here; nothing says the theory is closed.
-/

open Real

namespace MineM5

/-- the Nariai a0-shell identity: r_a0(M_N)/L = sqrt(Z/(3 sqrt 3)) -/
theorem nariai_shell_ratio {G H c Z : ℝ} (hG : 0 < G) (hH : 0 < H) (hc : 0 < c) (_hZ : 0 < Z) :
    Real.sqrt (G * (c ^ 3 / (3 * Real.sqrt 3 * G * H)) / (c * H / Z)) / (c / H)
      = Real.sqrt (Z / (2 * Real.sqrt 3)) := by
  have h3 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have hin : G * (c ^ 3 / (3 * Real.sqrt 3 * G * H)) / (c * H / Z) = (c / H) ^ 2 * (Z / (3 * Real.sqrt 3)) := by
    field_simp
  rw [hin, Real.sqrt_mul (by positivity), Real.sqrt_sq (by positivity)]
  field_simp

/-- the ratio is 1 iff Z = 3 sqrt 3 (Z > 0) -/
theorem nariai_ratio_eq_one_iff {Z : ℝ} (_hZ : 0 < Z) :
    Real.sqrt (Z / (3 * Real.sqrt 3)) = 1 ↔ Z = 3 * Real.sqrt 3 := by
  have h3 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  rw [Real.sqrt_eq_one, div_eq_one_iff_eq (by positivity)]

/-- kappa := sqrt(8 pi/3)/Z at the forced Z = 3 sqrt 3 is 2 sqrt(2 pi)/9 -/
theorem kappa_forced :
    Real.sqrt (8 * π / 3) / (3 * Real.sqrt 3) = 2 * Real.sqrt (2 * π) / 9 := by
  have hp := Real.pi_pos
  have h3 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have hs : 0 < Real.sqrt (8 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hs2 : 0 < Real.sqrt (2 * π) := Real.sqrt_pos.mpr (by positivity)
  have hL : 0 ≤ Real.sqrt (8 * π / 3) / (3 * Real.sqrt 3) := by positivity
  have hR : 0 ≤ 2 * Real.sqrt (2 * π) / 9 := by positivity
  have e1 : (Real.sqrt (8 * π / 3) / (3 * Real.sqrt 3)) ^ 2 = 8 * π / 81 := by
    rw [div_pow, Real.sq_sqrt (by positivity), mul_pow, Real.sq_sqrt (by norm_num)]
    ring
  have e2 : (2 * Real.sqrt (2 * π) / 9) ^ 2 = 8 * π / 81 := by
    rw [div_pow, mul_pow, Real.sq_sqrt (by positivity)]
    ring
  exact (sq_eq_sq₀ hL hR).mp (e1.trans e2.symm)

/-- the forced Z is strictly below the canonical Z = sqrt(32 pi/3) -/
theorem forced_differs_from_canonical :
    3 * Real.sqrt 3 < Real.sqrt (32 * π / 3) := by
  have hp := Real.pi_gt_three
  have h3 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have e : (3 * Real.sqrt 3) ^ 2 = 27 := by
    rw [mul_pow, Real.sq_sqrt (by norm_num)]; norm_num
  apply Real.lt_sqrt_of_sq_lt
  rw [e]; nlinarith

/-- the a0 ratio forced / canonical equals Z_canonical / Z_forced and exceeds 1 (a0 = c H / Z) -/
theorem a0_forced_over_canonical {c H : ℝ} (hc : 0 < c) (hH : 0 < H) :
    1 < (c * H / (3 * Real.sqrt 3)) / (c * H / Real.sqrt (32 * π / 3)) := by
  have h3 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  have hlt := forced_differs_from_canonical
  have hpos : 0 < 3 * Real.sqrt 3 := by positivity
  have hch : 0 < c * H := mul_pos hc hH
  have hZ : 0 < Real.sqrt (32 * π / 3) := lt_trans hpos hlt
  have : (c * H / (3 * Real.sqrt 3)) / (c * H / Real.sqrt (32 * π / 3))
      = Real.sqrt (32 * π / 3) / (3 * Real.sqrt 3) := by
    field_simp
  rw [this, one_lt_div hpos]
  exact hlt

end MineM5

#print axioms MineM5.nariai_shell_ratio
#print axioms MineM5.nariai_ratio_eq_one_iff
#print axioms MineM5.kappa_forced
#print axioms MineM5.forced_differs_from_canonical
#print axioms MineM5.a0_forced_over_canonical
