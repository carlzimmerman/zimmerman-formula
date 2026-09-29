import Mathlib
/-!
# AH3 MUTATE control -- the certificates must have power.
(1)-(3): deliberately FALSE variants of AH3's statements, closed with the same tactics; each must FAIL to compile.
(4): positive control -- an observable that depends on e alone (not only through lambda) CAN recover e, so the no-go is not vacuous.
Expected: errors at (1), (2), (3); (4) compiles.  Run: lake env lean AH3_alpha_nogo_MUTATE.lean
-/
noncomputable section
open Real

def rPlus (a b : ℝ) : ℝ := Real.exp (-2 * b) * Real.cosh (a + b) / Real.cosh (a - b)
def rMinus (a b : ℝ) : ℝ := Real.exp (-2 * b) * Real.cosh (a - b) / Real.cosh (a + b)
def Jclosed (l ρ : ℝ) : ℝ := ρ * Real.sinh (2 * π * l) / (π * Real.sinh (2 * π * ρ))

-- (1) FALSE: swap sinh(2a) for sinh(2b) on the right of the pair identity
theorem mutate1 (a b : ℝ) :
    (rPlus a b * (1 - rMinus a b) - rMinus a b * (1 - rPlus a b)) * Real.sinh (2 * b)
      = Real.sinh (2 * b) * ((1 - rPlus a b) * (1 - rMinus a b)) := by
  have hc1 : Real.cosh (a + b) ≠ 0 := (Real.cosh_pos _).ne'
  have hc2 : Real.cosh (a - b) ≠ 0 := (Real.cosh_pos _).ne'
  unfold rPlus rMinus
  field_simp
  ring

-- (2) FALSE: the m^2 = H^2/4 response is lambda/pi, not lambda/(2 pi)
theorem mutate2 (l : ℝ) (hl : l ≠ 0) : Jclosed l l = l / (2 * π) := by
  unfold Jclosed
  have hpi : π ≠ 0 := Real.pi_ne_zero
  have hs : Real.sinh (2 * π * l) ≠ 0 := by
    intro h
    have := Real.sinh_eq_zero.mp h
    have : 2 * π * l = 0 := this
    rcases mul_eq_zero.mp this with h1 | h1
    · exact hpi (by linarith [h1])
    · exact hl h1
  field_simp

-- (3) FALSE: the current is EVEN in lambda
theorem mutate3 (l ρ : ℝ) : Jclosed (-l) ρ = Jclosed l ρ := by
  unfold Jclosed
  rw [show 2 * π * -l = -(2 * π * l) by ring, Real.sinh_neg]
  ring

-- (4) POSITIVE CONTROL: an observable that sees e directly (not only through lambda) recovers e -> compiles
def obsDirect (e _E _m _H : ℝ) : ℝ := e
theorem control_direct_recovers_e (m H : ℝ) :
    ∃ f : ℝ → ℝ, ∀ e E : ℝ, 0 < e → f (obsDirect e E m H) = e :=
  ⟨id, fun _ _ _ => rfl⟩
