import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

set_option autoImplicit false
namespace TrackingBalance
noncomputable section

/-!
Audit of L194's ASSUMED variance-rate closure, not of an action-derived
nonlinear evolution. k is physical wavenumber/H, NOT Zimmerman's fitted
acceleration coefficient. u is the positive imaginary sound-speed magnitude.
The drag equation is an approximation control, not a new gravity model.
-/

def varianceRate (k u : ℝ) := -2+2*k*u

theorem balance_sets_hubble_rate (k u : ℝ)
    (h : varianceRate k u = 0) : k*u = 1 := by
  unfold varianceRate at h
  linarith

theorem balance_has_negative_sound_squared (k u c2 : ℝ)
    (hk : 0 < k) (hc : c2 = -u^2) (h : varianceRate k u = 0) :
    c2*k^2 = -1 ∧ c2 < 0 := by
  have hku := balance_sets_hubble_rate k u h
  have hid : c2*k^2 = -1 := by
    calc
      c2*k^2 = -(k*u)^2 := by rw [hc]; ring
      _ = -1 := by rw [hku]; ring
  have hksq := sq_pos_of_pos hk
  constructor
  · exact hid
  · nlinarith

theorem shorter_mode_invades (k larger u : ℝ)
    (hk : 0 < k) (hlarge : k < larger) (h : varianceRate k u = 0) :
    0 < varianceRate larger u := by
  have hku := balance_sets_hubble_rate k u h
  have hu : 0 < u := by nlinarith
  have hprod := mul_pos (sub_pos.mpr hlarge) hu
  unfold varianceRate
  nlinarith

theorem retained_drag_changes_balance (k u drag growth : ℝ)
    (hmode : growth^2+drag*growth-k^2*u^2 = 0)
    (hvariance : -2+2*growth = 0) :
    k^2*u^2 = 1+drag := by
  have hg : growth = 1 := by linarith
  rw [hg] at hmode
  nlinarith

#print axioms balance_sets_hubble_rate
#print axioms balance_has_negative_sound_squared
#print axioms shorter_mode_invades
#print axioms retained_drag_changes_balance
end
end TrackingBalance
