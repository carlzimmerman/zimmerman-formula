import Mathlib

/-! MUTATE for MODULAR_S4_FIXED: FALSE, must fail. (M) Some conjugate of the modular S is the double transposition (0 1)(2 3).
False: conjugation preserves cycle type ({2} vs {2, 2}). -/

def T : Equiv.Perm (Fin 4) := finRotate 4
def S : Equiv.Perm (Fin 4) := Equiv.swap 2 3

theorem mutate_double_reachable : ∃ g : Equiv.Perm (Fin 4), g * S * g⁻¹ = Equiv.swap 0 1 * Equiv.swap 2 3 := by decide
