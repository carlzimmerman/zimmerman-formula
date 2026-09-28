import Mathlib.Data.Real.Basic
import Mathlib.Tactic
noncomputable section
open scoped Real
namespace AS651
def P (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ := Z / 2 * q ^ 2 + b * beta ^ 2 * q ^ 2
def Pq (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ := (Z + 2 * b * beta ^ 2) * q
theorem legendre_identity (q Z b beta : ℝ) :
    q * Pq Z b beta q - P Z b beta q = (Z / 2 + b * beta ^ 2) * q ^ 2 := by
  unfold P Pq; ring
theorem vacuum_positive (q Z b beta : ℝ) (hq : 0 < q) (hZ : 0 < Z) (hb : 0 < b)
    (hbeta : beta ≠ 0) : 0 < q * Pq Z b beta q - P Z b beta q := by
  have hbz : 0 < beta ^ 2 := sq_pos_of_ne_zero hbeta
  have hA : 0 < Z / 2 + b * beta ^ 2 := by nlinarith
  have hq2 : 0 < q ^ 2 := sq_pos_of_ne_zero (ne_of_gt hq)
  rw [legendre_identity q Z b beta]
  exact mul_pos hA hq2
theorem eps_zero_at_zero (Z b beta : ℝ) : 0 * Pq Z b beta 0 - P Z b beta 0 = 0 := by
  unfold P Pq; ring
theorem scalar_variation_kills_vacuum (q Z b beta : ℝ) (hP : Pq Z b beta q = 0) (hq : 0 < q)
    (hZ : 0 < Z) (hb : 0 < b) (hbeta : beta ≠ 0) : False := by
  have hP' : (Z + 2 * b * beta ^ 2) * q = 0 := by simpa [Pq] using hP
  have hbz : 0 < beta ^ 2 := sq_pos_of_ne_zero hbeta
  have hpos : 0 < Z + 2 * b * beta ^ 2 := by nlinarith
  have hq0 : q = 0 := (mul_eq_zero.mp hP').resolve_left (ne_of_gt hpos)
  nlinarith
theorem kappa2_q_independent (q Z b beta : ℝ) (hq : q ≠ 0) (hden : Z / 2 + b * beta ^ 2 ≠ 0) :
    (beta ^ 2 * q ^ 2) / ((Z / 2 + b * beta ^ 2) * q ^ 2) =
      beta ^ 2 / (Z / 2 + b * beta ^ 2) := by
  have hq2 : q ^ 2 ≠ 0 := pow_ne_zero 2 hq
  have hden2 : (Z / 2 + b * beta ^ 2) * q ^ 2 ≠ 0 := mul_ne_zero hden hq2
  field_simp [hden2]
theorem kappa_half_iff_ratio (s Z b : ℝ) (hden : Z / 2 + b * s ≠ 0) :
    s / (Z / 2 + b * s) = 1 / 4 ↔ Z = (8 - 2 * b) * s := by
  constructor
  · intro h
    have hM : s = 1 / 4 * (Z / 2 + b * s) := (div_eq_iff hden).mp h
    nlinarith
  · intro hZ
    have hM : s = 1 / 4 * (Z / 2 + b * s) := by nlinarith [hZ]
    exact (div_eq_iff hden).mpr hM
theorem kappa_strict_anti (b r1 r2 : ℝ) (hb : 0 < b) (hr1 : 0 < r1) (h12 : r1 < r2) :
    1 / (r1 / 2 + b) > 1 / (r2 / 2 + b) := by
  have h1 : 0 < r1 / 2 + b := by nlinarith
  have h2 : r1 / 2 + b < r2 / 2 + b := by nlinarith
  exact one_div_lt_one_div_of_lt h1 h2
theorem kappa_proj_distinct (b r1 r2 : ℝ) (hb : 0 < b) (hr1 : 0 < r1) (hr2 : 0 < r2)
    (h21 : r1 ≠ r2) : 1 / (r1 / 2 + b) ≠ 1 / (r2 / 2 + b) := by
  by_contra h
  rcases lt_or_gt_of_ne h21 with h12 | h21'
  · have hm : 1 / (r1 / 2 + b) > 1 / (r2 / 2 + b) := kappa_strict_anti b r1 r2 hb hr1 h12
    exact (ne_of_gt hm) h
  · have hm : 1 / (r2 / 2 + b) > 1 / (r1 / 2 + b) := kappa_strict_anti b r2 r1 hb hr2 h21'
    exact (ne_of_gt hm) h.symm
end AS651
end
#print axioms AS651.legendre_identity
#print axioms AS651.vacuum_positive
#print axioms AS651.eps_zero_at_zero
#print axioms AS651.scalar_variation_kills_vacuum
#print axioms AS651.kappa2_q_independent
#print axioms AS651.kappa_half_iff_ratio
#print axioms AS651.kappa_strict_anti
#print axioms AS651.kappa_proj_distinct
