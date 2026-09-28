import Mathlib
import Mathlib.Tactic

def epsU (mu s : Fin 4) : ℤ :=
  match mu, s with
  | 0, 0 => -1
  | 1, 1 => 1
  | 2, 2 => -1
  | 3, 3 => 1
  | _, _ => 0

def eomComp (v : Fin 4 → ℤ) (s : Fin 4) : ℤ :=
  epsU 0 s * v 0 + epsU 1 s * v 1 + epsU 2 s * v 2 + epsU 3 s * v 3

example (v : Fin 4 → ℤ) (h : ∀ s : Fin 4, eomComp v s = 0) : ∀ mu : Fin 4, v mu = 0 := by
  intro mu
  fin_cases mu
  · have h0 := h 0
    simp [eomComp, epsU] at h0
    trace_state
    exact h0
  · have h1 := h 1
    simp [eomComp, epsU] at h1
    trace_state
    exact h1
  · have h2 := h 2
    simp [eomComp, epsU] at h2
    trace_state
    exact h2
  · have h3 := h 3
    simp [eomComp, epsU] at h3
    trace_state
    exact h3