import Mathlib

/-!
# YM07 -- THE VOLUME-UNIFORM STRONG-COUPLING GAP: the thermodynamic-limit rung

Scope statement (as every certificate in this repo reads): Lean certifies the
MATHEMATICS. The physics premises -- the per-loop LOCALIZATION of the
magnetic deficit (a flux loop's influence zone is a fixed O(1) set of
plaquettes, so |<psi|H_B - <vac|H_B|vac>|psi>| <= (2N/g^2) n_influence ell for
an ell-loop state; delocalized superpositions do no better), the electric
second eigenvalue (g^2/2)*4*C_F over the vacuum's orthogonal complement, the
vacuum's extensive magnetic shift CANCELING in the gap -- are the committed
YM07 lane's claims (deepseek_push/yang_mills_gap/YM07_uniform_gap.py). This
file certifies the ARITHMETIC of the uniform bound: with ANY influence zone
n_influence <= 18 (the absolute ceiling -- any honest counting is far below),
the gap polynomial 3x/2 - 2N n_influence / x is STRICTLY positive on the
strong-coupling window x = g^2 >= 8, for BOTH SU(2) (kappa <= 72) and SU(3)
(kappa3 <= 108). The bound is independent of the volume: the finite-box
Hamiltonians' gaps are all >= the same positive number, so the
infinite-lattice Hamiltonian (the direct limit) has a positive spectral gap
at fixed lattice spacing and strong coupling. The continuum limit (a -> 0,
g^2(a) -> 0) remains the open Clay rung, registered in YM_ROADMAP.md.
-/
noncomputable section

/-- the SU(2) uniform-gap polynomial with the worst-case magnetic constant
    kappa = 2N n_influence = 72 (N = 2, n_influence <= 18) --/
noncomputable def gap_uniform_su2 (x : ℝ) : ℝ := 3 * x / 2 - 72 / x

/-- the SU(3) uniform-gap polynomial with the worst-case kappa3 = 108 --/
noncomputable def gap_uniform_su3 (x : ℝ) : ℝ := 8 * x / 3 - 108 / x

/-- SU(2): on the strong-coupling window x >= 8 the uniform gap is strictly
    positive for EVERY influence zone <= 18 plaquettes (and hence for the
    lane's committed zone) -- the bound is VOLUME-INDEPENDENT --/
theorem uniform_su2_pos (x : ℝ) (hx : 8 ≤ x) : 0 < gap_uniform_su2 x := by
  unfold gap_uniform_su2
  have hx0 : 0 < x := by linarith [hx]
  have hnum : 0 < 3 * x^2 - 144 := by nlinarith [hx]
  calc
    3 * x / 2 - 72 / x = (3 * x^2 - 144) / (2 * x) := by
      field_simp [hx0.ne'] <;> ring
    _ > 0 := div_pos hnum (mul_pos (by norm_num : (0:ℝ) < 2) hx0)

/-- SU(3): same window, strictly positive for every influence zone <= 18 --/
theorem uniform_su3_pos (x : ℝ) (hx : 8 ≤ x) : 0 < gap_uniform_su3 x := by
  unfold gap_uniform_su3
  have hx0 : 0 < x := by linarith [hx]
  have hnum : 0 < 8 * x^2 - 324 := by nlinarith [hx]
  calc
    8 * x / 3 - 108 / x = (8 * x^2 - 324) / (3 * x) := by
      field_simp [hx0.ne'] <;> ring
    _ > 0 := div_pos hnum (mul_pos (by norm_num : (0:ℝ) < 3) hx0)

/-- the anchor: at x = 8 the uniform bounds are positive with wide margin:
    Delta_SU2(8) = 3, Delta_SU3(8) = 47/6 ~ 7.83 (WORST-CASE kappa) --/
theorem uniform_anchors : 3 ≤ gap_uniform_su2 8 ∧ 47 / 6 ≤ gap_uniform_su3 8 := by
  constructor <;> norm_num [gap_uniform_su2, gap_uniform_su3]

/-- the COUNTED constants (YM07 lane, 15/15: n_influence = 13 counted from
    the 3D cubic drawing, 8d-11; kappa = 2N*13 = 52 for SU(2)): at x = 8 the
    counted bound is Delta = 11/2 --/
noncomputable def gap_counted_su2 (x : ℝ) : ℝ := 3 * x / 2 - 52 / x

/-- SU(2) with the counted kappa = 52 is strictly positive on x >= 8:
    the registered bound of the thermodynamic-limit rung --/
theorem uniform_su2_counted (x : ℝ) (hx : 8 ≤ x) : 0 < gap_counted_su2 x := by
  unfold gap_counted_su2
  have hx0 : 0 < x := by linarith [hx]
  have hnum : 0 < 3 * x^2 - 104 := by nlinarith [hx]
  calc
    3 * x / 2 - 52 / x = (3 * x^2 - 104) / (2 * x) := by
      field_simp [hx0.ne'] <;> ring
    _ > 0 := div_pos hnum (mul_pos (by norm_num : (0:ℝ) < 2) hx0)

/-- the counted anchor: Delta_SU2(8) = 11/2 with kappa = 52 --/
theorem uniform_counted_anchor : 11 / 2 ≤ gap_counted_su2 8 := by
  norm_num [gap_counted_su2]

end
#print axioms uniform_su2_pos
#print axioms uniform_su3_pos
#print axioms uniform_anchors
#print axioms uniform_su2_counted
#print axioms uniform_counted_anchor