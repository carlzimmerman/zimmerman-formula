import Mathlib.Data.Real.Basic
import Mathlib.Topology.Algebra.Ring.Real
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
  Kernel-checked existence and uniqueness for the homogeneous DBI clock branch.

  The minisuperspace current in the companion executable gate is

      z^3 / (1 - z^2) = L * (C / (A * a^3))^2,

  with A,L,C,a positive and 0 < z < 1.  This file proves that the equation
  has exactly one admissible speed z for every positive scale factor a.

  Scope boundary: this is a theorem about the homogeneous clock equation only.
  It does not prove the full covariant metric variation, nonlinear Dirac/HDA
  closure, PPN parameters, or the requested two-tensor-DOF gravity theory.
  No `sorry`, `axiom`, or numerical rank assumption is used.
-/

open Set

noncomputable section

def chargeShape (z : ℝ) : ℝ := z ^ 3 / (1 - z ^ 2)

def chargePoly (q z : ℝ) : ℝ := z ^ 3 + q * z ^ 2 - q

theorem charge_shape_strictMono_on :
    StrictMonoOn chargeShape (Ioo (0 : ℝ) 1) := by
  intro x hx y hy hxy
  have hx0 : 0 < x := hx.1
  have hx1 : x < 1 := hx.2
  have hy0 : 0 < y := hy.1
  have hy1 : y < 1 := hy.2
  have hdx : 0 < 1 - x ^ 2 := by
    nlinarith [mul_pos (sub_pos.mpr hx1) (by nlinarith : 0 < 1 + x)]
  have hdy : 0 < 1 - y ^ 2 := by
    nlinarith [mul_pos (sub_pos.mpr hy1) (by nlinarith : 0 < 1 + y)]
  have hfac : 0 < x ^ 2 + x * y + y ^ 2 - x ^ 2 * y ^ 2 := by
    have hxx : 0 < x ^ 2 * (1 - y ^ 2) := mul_pos (sq_pos_of_pos hx0) hdy
    have hxypos : 0 < x * y := mul_pos hx0 hy0
    have hyy : 0 < y ^ 2 := sq_pos_of_pos hy0
    nlinarith
  have hid : y ^ 3 * (1 - x ^ 2) - x ^ 3 * (1 - y ^ 2) =
      (y - x) * (x ^ 2 + x * y + y ^ 2 - x ^ 2 * y ^ 2) := by
    ring
  have hprod : 0 < (y - x) * (x ^ 2 + x * y + y ^ 2 - x ^ 2 * y ^ 2) :=
    mul_pos (sub_pos.mpr hxy) hfac
  unfold chargeShape
  apply (div_lt_div_iff₀ hdx hdy).2
  nlinarith [hprod]

theorem charge_shape_exists (q : ℝ) (hq : 0 < q) :
    ∃ z, z ∈ Ioo (0 : ℝ) 1 ∧ chargeShape z = q := by
  have hcont : ContinuousOn (chargePoly q) (Icc (0 : ℝ) 1) := by
    unfold chargePoly
    fun_prop
  have hsubset : Icc (chargePoly q 0) (chargePoly q 1) ⊆
      chargePoly q '' Icc (0 : ℝ) 1 :=
    intermediate_value_Icc (show (0 : ℝ) ≤ 1 by norm_num) hcont
  have hzero : (0 : ℝ) ∈ Icc (chargePoly q 0) (chargePoly q 1) := by
    constructor <;> dsimp [chargePoly] <;> nlinarith
  obtain ⟨z, hz, hp⟩ := hsubset hzero
  have hz0 : 0 < z := by
    have hzle : 0 ≤ z := hz.1
    by_contra hn
    have hzeq : z = 0 := le_antisymm (le_of_not_gt hn) hzle
    subst z
    dsimp [chargePoly] at hp
    nlinarith
  have hz1 : z < 1 := by
    have hzl : z ≤ 1 := hz.2
    by_contra hn
    have hzeq : z = 1 := le_antisymm hzl (le_of_not_gt hn)
    subst z
    dsimp [chargePoly] at hp
    nlinarith
  have hden : 1 - z ^ 2 ≠ 0 := by
    have hdenpos : 0 < 1 - z ^ 2 := by
      nlinarith [mul_pos (sub_pos.mpr hz1) (by nlinarith : 0 < 1 + z)]
    exact ne_of_gt hdenpos
  refine ⟨z, ⟨hz0, hz1⟩, ?_⟩
  unfold chargeShape
  field_simp [hden]
  dsimp [chargePoly] at hp
  nlinarith [hp]

theorem charge_shape_unique_positive_root (q : ℝ) (hq : 0 < q) :
    ∃! z, z ∈ Ioo (0 : ℝ) 1 ∧ chargeShape z = q := by
  obtain ⟨z, hz, hqz⟩ := charge_shape_exists q hq
  refine ⟨z, ⟨hz, hqz⟩, ?_⟩
  intro y hy
  exact charge_shape_strictMono_on.injOn hy.1 hz (by simp [hy.2, hqz])

theorem dbi_clock_unique_speed
    (A L C a : ℝ) (hA : 0 < A) (hL : 0 < L) (hC : 0 < C) (ha : 0 < a) :
    ∃! z, z ∈ Ioo (0 : ℝ) 1 ∧
      chargeShape z = L * (C / (A * a ^ 3)) ^ 2 := by
  have hAa : 0 < A * a ^ 3 := mul_pos hA (pow_pos ha 3)
  have hfrac : 0 < C / (A * a ^ 3) := div_pos hC hAa
  have hq : 0 < L * (C / (A * a ^ 3)) ^ 2 :=
    mul_pos hL (sq_pos_of_pos hfrac)
  exact charge_shape_unique_positive_root _ hq
