import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
AS651 -- four-form metric variation fixes the Legendre vacuum energy?
Algebraic core of the derivation, certified in Lean 4 (self-contained).

Sector:  S = ∫ sqrt(-g) P(q) d⁴x,   P(q) = (Z/2) q² + b β² q²   (k04 four-form promotion),
F = q ε four-form, energy density ε_vac = q P_q − P (Legendre form), κ² = a0²/(G ε_vac),
a0² = G β² q² (promotion).

Theorems:
  1. legendre_identity            : q P_q − P = (Z/2 + b β²) q²            [step 2]
  2. vacuum_positive              : ε_vac > 0 for q > 0 (B-iii sign, structural)
  3. eps_zero_at_zero             : ε_vac(0) = 0
  4. scalar_variation_kills_vacuum: altered premise P_q = 0 admits no q > 0 (negative control)
  5. kappa2_q_independent         : the flux amplitude q cancels from κ²   [B-iv input]
  6. kappa_half_iff_ratio         : κ = 1/2  ↔  Z/β² = 8 − 2b (equivalence, nothing else lurks)
  7. kappa_proj_distinct          : κ² is injective in the ratio Z/β² → κ-projection is a
                                    continuum, not a point (B-iv witness fails)
-/

noncomputable section
open scoped Real

namespace AS651

/-- Action density of the four-form sector, P(q) = (Z/2) q² + b β² q². -/
def P (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ := Z / 2 * q ^ 2 + b * beta ^ 2 * q ^ 2

/-- Formal derivative P_q = (Z + 2 b β²) q. -/
def Pq (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ := (Z + 2 * b * beta ^ 2) * q

/-- q P_q − P = (Z/2 + b β²) q² : the Legendre form of the energy density (step 2). -/
theorem legendre_identity (q Z b beta : ℝ) :
    q * Pq Z b beta q - P Z b beta q = (Z / 2 + b * beta ^ 2) * q ^ 2 := by
  unfold P Pq
  ring

/-- The vacuum energy density is strictly positive for q > 0 (B-iii, structural sign). -/
theorem vacuum_positive (q Z b beta : ℝ) (hq : 0 < q) (hZ : 0 < Z) (hb : 0 < b)
    (hbeta : beta ≠ 0) : 0 < q * Pq Z b beta q - P Z b beta q := by
  have hbz : 0 < beta ^ 2 := sq_pos_of_ne_zero hbeta
  have hA : 0 < Z / 2 + b * beta ^ 2 := by nlinarith
  have hq2 : 0 < q ^ 2 := sq_pos_of_ne_zero (ne_of_gt hq)
  rw [legendre_identity q Z b beta]
  exact mul_pos hA hq2

/-- At q = 0 the vacuum energy vanishes. -/
theorem eps_zero_at_zero (Z b beta : ℝ) : 0 * Pq Z b beta 0 - P Z b beta 0 = 0 := by
  unfold P Pq
  ring

/-- NEGATIVE CONTROL (altered premise: q varied as a metric-independent scalar):
P_q(q) = 0 with Z, b > 0 and q > 0 is impossible; the only stationary point is q = 0,
where the vacuum (and the scale, a0 = β√G |q|) vanish. -/
theorem scalar_variation_kills_vacuum (q Z b beta : ℝ) (hP : Pq Z b beta q = 0) (hq : 0 < q)
    (hZ : 0 < Z) (hb : 0 < b) (hbeta : beta ≠ 0) : False := by
  have hP' : (Z + 2 * b * beta ^ 2) * q = 0 := by simpa [Pq] using hP
  have hbz : 0 < beta ^ 2 := sq_pos_of_ne_zero hbeta
  have hpos : 0 < Z + 2 * b * beta ^ 2 := by nlinarith
  have hq0 : q = 0 := (mul_eq_zero.mp hP').resolve_left (ne_of_gt hpos)
  nlinarith

/-- The flux amplitude cancels from κ² = a0²/(G ε_vac) = β²q²/((Z/2+bβ²)q²):
κ² is independent of the boundary datum q (B-iv input). -/
theorem kappa2_q_independent (q Z b beta : ℝ) (hq : q ≠ 0) (hden : Z / 2 + b * beta ^ 2 ≠ 0) :
    (beta ^ 2 * q ^ 2) / ((Z / 2 + b * beta ^ 2) * q ^ 2) =
      beta ^ 2 / (Z / 2 + b * beta ^ 2) := by
  have hq2 : q ^ 2 ≠ 0 := pow_ne_zero 2 hq
  have hden2 : (Z / 2 + b * beta ^ 2) * q ^ 2 ≠ 0 := mul_ne_zero hden hq2
  field_simp [hden2]

/-- κ = 1/2  if and only if  Z/β² = 8 − 2b   (with s := β² > 0): the half is exactly the
coupling-ratio condition, an equivalence -- no hidden alternative. -/
theorem kappa_half_iff_ratio (s Z b : ℝ) (hden : Z / 2 + b * s ≠ 0) :
    s / (Z / 2 + b * s) = 1 / 4 ↔ Z = (8 - 2 * b) * s := by
  constructor
  · intro h
    have hM : s = 1 / 4 * (Z / 2 + b * s) := (div_eq_iff hden).mp h
    nlinarith
  · intro hZ
    have hM : s = 1 / 4 * (Z / 2 + b * s) := by nlinarith [hZ]
    exact (div_eq_iff hden).mpr hM

/-- κ² is strictly decreasing in r = Z/β² on the physical domain r > 0. -/
theorem kappa_strict_anti (b r1 r2 : ℝ) (hb : 0 < b) (hr1 : 0 < r1) (h12 : r1 < r2) :
    1 / (r1 / 2 + b) > 1 / (r2 / 2 + b) := by
  have h1 : 0 < r1 / 2 + b := by nlinarith
  have h2 : r1 / 2 + b < r2 / 2 + b := by nlinarith
  exact one_div_lt_one_div_of_lt h1 h2

/-- B-iv witness: the κ-projection of the candidate system is NOT a point --
two distinct ratios give two distinct κ-values (a continuum). -/
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
