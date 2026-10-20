module

public import Mathlib.Algebra.Order.Field.Basic
meta import Mathlib.Tactic.FieldSimp
meta import Mathlib.Tactic.Ring.Basic
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.NormNum

@[expose] public section

/-!
Exact energy algebra for a regular current interaction and a charged sextic.

The canonical-momentum relation and the fixed-charge energy are explicit
inputs. These statements do not derive a Gauss law, a field-theory state,
a microscopic charge source, or an operational MOND coefficient. The neutral
polynomial is defined at zero amplitude without interpreting a polar quotient.
-/

namespace Why4.CurrentEnergy

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def timeLagrangian (Q nu alpha z : K) : K :=
  Q * nu ^ 2 - 2 * alpha * Q * nu * z

def timeHamiltonian (Q p alpha z : K) : K :=
  (p + 2 * alpha * Q * z) ^ 2 / (4 * Q)

def neutralEnergy (Q lambda alpha z : K) : K :=
  alpha ^ 2 * Q * z ^ 2 + lambda * Q ^ 3 / 3

def chargedEnergy (n Q lambda : K) : K :=
  n ^ 2 / (4 * Q) + lambda * Q ^ 3 / 3

theorem exact_legendre_identity
    (Q nu alpha z p : K) (hQ : Q ≠ 0)
    (hp : p = 2 * Q * (nu - alpha * z)) :
    p * nu - timeLagrangian Q nu alpha z =
      timeHamiltonian Q p alpha z := by
  rw [hp]
  unfold timeLagrangian timeHamiltonian
  field_simp [hQ]
  ring1

theorem neutral_energy_nonnegative
    (Q lambda alpha z : K) (hQ : 0 ≤ Q) (hl : 0 < lambda) :
    0 ≤ neutralEnergy Q lambda alpha z := by
  unfold neutralEnergy
  exact add_nonneg
    (mul_nonneg (mul_nonneg (sq_nonneg alpha) hQ) (sq_nonneg z))
    (div_nonneg (mul_nonneg (le_of_lt hl) (pow_nonneg hQ 3)) (by norm_num))

theorem neutral_energy_zero_iff
    (Q lambda alpha z : K) (hQ : 0 ≤ Q) (hl : 0 < lambda) :
    neutralEnergy Q lambda alpha z = 0 ↔ Q = 0 := by
  constructor
  · intro he
    by_contra hne
    have hQp : 0 < Q := lt_of_le_of_ne hQ (Ne.symm hne)
    have hfirst : 0 ≤ alpha ^ 2 * Q * z ^ 2 :=
      mul_nonneg (mul_nonneg (sq_nonneg alpha) hQ) (sq_nonneg z)
    have hlast : 0 < lambda * Q ^ 3 / 3 :=
      div_pos (mul_pos hl (pow_pos hQp 3)) (by norm_num)
    unfold neutralEnergy at he
    linarith
  · intro he
    simp [neutralEnergy, he]

theorem charged_gap_factorization
    (n Q lambda a : K) (hQ : Q ≠ 0)
    (hn : n ^ 2 = 4 * lambda * a ^ 4) :
    chargedEnergy n Q lambda - 4 * lambda * a ^ 3 / 3 =
      lambda * (Q - a) ^ 2 * (Q ^ 2 + 2 * Q * a + 3 * a ^ 2) / (3 * Q) := by
  unfold chargedEnergy
  rw [hn]
  field_simp [hQ]
  ring1

theorem charged_global_lower_bound
    (n Q lambda a : K) (hQ : 0 < Q) (hl : 0 < lambda) (ha : 0 < a)
    (hn : n ^ 2 = 4 * lambda * a ^ 4) :
    4 * lambda * a ^ 3 / 3 ≤ chargedEnergy n Q lambda := by
  have hpoly : 0 < Q ^ 2 + 2 * Q * a + 3 * a ^ 2 := by
    nlinarith [sq_nonneg Q, sq_nonneg a, mul_pos hQ ha]
  have hgap : 0 ≤ chargedEnergy n Q lambda - 4 * lambda * a ^ 3 / 3 := by
    rw [charged_gap_factorization n Q lambda a (ne_of_gt hQ) hn]
    exact div_nonneg
      (mul_nonneg (mul_nonneg (le_of_lt hl) (sq_nonneg (Q - a)))
        (le_of_lt hpoly))
      (le_of_lt (mul_pos (by norm_num) hQ))
  exact sub_nonneg.mp hgap

theorem charged_equality_iff
    (n Q lambda a : K) (hQ : 0 < Q) (hl : 0 < lambda) (ha : 0 < a)
    (hn : n ^ 2 = 4 * lambda * a ^ 4) :
    chargedEnergy n Q lambda = 4 * lambda * a ^ 3 / 3 ↔ Q = a := by
  constructor
  · intro he
    by_contra hne
    have hsq : 0 < (Q - a) ^ 2 := sq_pos_of_ne_zero (sub_ne_zero.mpr hne)
    have hpoly : 0 < Q ^ 2 + 2 * Q * a + 3 * a ^ 2 := by
      nlinarith [sq_nonneg Q, sq_nonneg a, mul_pos hQ ha]
    have hgap : 0 < chargedEnergy n Q lambda - 4 * lambda * a ^ 3 / 3 := by
      rw [charged_gap_factorization n Q lambda a (ne_of_gt hQ) hn]
      exact div_pos (mul_pos (mul_pos hl hsq) hpoly)
        (mul_pos (by norm_num) hQ)
    rw [he, sub_self] at hgap
    exact (lt_irrefl (0 : K)) hgap
  · intro he
    have hgap : chargedEnergy n Q lambda - 4 * lambda * a ^ 3 / 3 = 0 := by
      rw [charged_gap_factorization n Q lambda a (ne_of_gt hQ) hn]
      simp [he]
    exact sub_eq_zero.mp hgap

#check @exact_legendre_identity
#check @neutral_energy_nonnegative
#check @neutral_energy_zero_iff
#check @charged_gap_factorization
#check @charged_global_lower_bound
#check @charged_equality_iff
#print axioms exact_legendre_identity
#print axioms neutral_energy_nonnegative
#print axioms neutral_energy_zero_iff
#print axioms charged_gap_factorization
#print axioms charged_global_lower_bound
#print axioms charged_equality_iff

end Why4.CurrentEnergy
