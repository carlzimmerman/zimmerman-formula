import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum

/-!
Pure algebra certificates conditional on positive-energy special-relativistic
mass shells. Units c=1. No dynamics, isotropic law, Poisson process, or clock
action is formalized. No user axioms or sorry are introduced.
-/
set_option autoImplicit false
namespace C003Recoil

theorem two_body_energy_sum (M m μ : ℝ) (hM : M ≠ 0) :
    (M^2 + m^2 - μ^2)/(2*M) + (M^2 - m^2 + μ^2)/(2*M) = M := by
  field_simp
  <;> ring

theorem massless_recoil_relation (M m E p β : ℝ)
    (energy : E + p = M) (momentum : p = β*E)
    (shell : E^2 - p^2 = m^2) :
    m^2*(1+β) = M^2*(1-β) := by
  rw [← energy, ← shell, momentum]
  ring

theorem rest_loss_partition (M m E p : ℝ) (energy : E + p = M) :
    M - m = (E-m) + p := by
  linarith

theorem nonzero_recoil_requires_lost_total_rest_mass
    (M m μ E F p : ℝ) (hm : 0 ≤ m) (hμ : 0 ≤ μ)
    (hE : 0 ≤ E) (hF : 0 ≤ F) (hp : 0 < p)
    (energy : M = E+F) (daughter : E^2-p^2=m^2)
    (scalar : F^2-p^2=μ^2) : m+μ < M := by
  have hpp : 0 < p^2 := sq_pos_of_pos hp
  have h1 : m < E := by nlinarith
  have h2 : μ < F := by nlinarith
  linarith

theorem exact_650kms_quadratic_split_incompatible (m : ℝ)
    (relation : m^2*(1+(650000:ℝ)/299792458) = 1-(650000:ℝ)/299792458) :
    1-m ≠ ((650000:ℝ)/299792458)^2/2 := by
  intro alleged
  have hm : m = 1-((650000:ℝ)/299792458)^2/2 := by linarith
  rw [hm] at relation
  norm_num at relation

#print axioms two_body_energy_sum
#print axioms massless_recoil_relation
#print axioms rest_loss_partition
#print axioms nonzero_recoil_requires_lost_total_rest_mass
#print axioms exact_650kms_quadratic_split_incompatible
end C003Recoil
