import Mathlib

/-!
AS042 Lean certificate (run AS042-r1-20260928T033112Z-dsv4f-hermes).
Algebraic skeleton of the filter-order lemma for the operative MONO equation:

    S = exp[(xi^2/2) Delta]   (Dirichlet/periodic heat semigroup, Fourier basis)
    M[u] = div[(nu(y)-1) grad u],  y = |grad u|/a0.

Certified here (real-number algebra, Mathlib axioms only):
  1. The Fourier-mode action of S on the constant mode k = 0 is the identity
     (S(1) = 1):  exp(-(xi^2/2) * 0^2) = 1.
  2. Composition rule of the semigroup in a single mode:
     S o S = exp(xi^2 Delta) modewise:
     exp(-(xi^2/2)k^2) * exp(-(xi^2/2)k^2) = exp(-xi^2 k^2).
  3. EXACT linear-cell remainder, per Fourier mode k with x = xi^2 k^2:
       S* M[S u] - M[u]  (per mode: c k^2 (1 - e^{-x}))
       minus the leading prediction (xi^2/2)(Delta M + DM(Delta u))
                                    (per mode: xi^2 c k^4)
       equals exactly  c k^2 (1 - x - e^{-x}) .
     This makes the piece that is O(xi^4) fully explicit: it is the second-order
     Taylor remainder of the semigroup in the mode, c k^2 (1 - xi^2 k^2 - e^{...})
     -- zero to O(xi^2) and O(xi^4)-suppressed pointwise when xi^2 k^2 stays small.
Not certified here (out of scope for a pure-algebra certificate): analysis
(asymptotic bounds), the PDE action on nonsmooth fields, and the physics.

Axioms: whatever Mathlib imports (subseteq {propext, Classical.choice, Quot.sound}
per the campaign bar; `lake env lean` reports the actual axiom set).
-/

-- 1) action on constants: exp(-(xi^2/2)*0^2) = 1
theorem as042_S_action_on_constant (xi : ℝ) :
    Real.exp (-(xi^2 / 2) * (0 : ℝ)^2) = 1 := by
  ring_nf
  rw [Real.exp_zero]

-- 2) semigroup composition in a mode: S o S = exp(xi^2 Delta)
theorem as042_S_compose_S (xi k : ℝ) :
    Real.exp (-(xi^2 / 2) * k^2) * Real.exp (-(xi^2 / 2) * k^2) =
      Real.exp (-(xi^2) * k^2) := by
  rw [← Real.exp_add]
  ring_nf

-- 3) exact modewise remainder of the linear-cell identity
theorem as042_exact_linear_cell_remainder (c k xi : ℝ) :
    c * k^2 * (1 - Real.exp (-(xi^2 * k^2))) - (xi^2 / 2) * (2 * c * k^4) =
      c * k^2 * (1 - xi^2 * k^2 - Real.exp (-(xi^2 * k^2))) := by
  ring_nf