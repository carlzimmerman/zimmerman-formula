import Mathlib

/-!
# AS056 -- Static Einstein channel count versus propagating DOF

Lean 4 certificate of the algebraic core of the channel-count chain
(PD01/PD08, re-derived independently in as056_derive.py):

  1. `or_slope`   -- the OR-composition slope identity: for ANY completion
      polynomial p with p(0)=0 and p'(0)=1, the n-channel OR response
      mu = 1 - (1-p)^n has origin slope exactly n.  Because the slope is the
      channel count for every completion, kappa = 1/n never waits on the
      unknown shape of the completion.  (This is the algebraic heart of
      "the deep-MOND slope is the channel count".)
  2. `trace_reversal` -- the seed's two-channel bookkeeping at the level of
      the traced linearized Einstein tensor: with a = Delta Psi, b = Delta Phi
      (the exact Poisson loads computed in as056_derive.py part 1),
      the trace-reversal combination G_mn = R_mn - (1/2) eta_mn R delivers
      G00 = 2 a  and  sum_i Gii = 2 (b - a), i.e. exactly the factors 2 and
      the Phi - Psi difference of the seed's principal equations.
  3. `kappa_half` -- the spherical deep-MOND matching tail: a0 = s/2 with
      s = c sqrt(G rho_Lambda) implies kappa = a0/s = 1/2 (adopted in this
      task as a framework input; the Lean statement certifies the algebra,
      not that the premises hold of the world).

These are DEPENDENCY statements, not physical claims: the physical reading
(the OR identification, the one-scale action, the two-potential static
sector) is held in the premises listed in derivation.md.
-/

open scoped Polynomial

noncomputable section

namespace As056

/-- OR-composition slope at the origin, arbitrary channel count `n` and
arbitrary completion polynomial `p` with the engagement boundary conditions
p(0) = 0 and p'(0) = 1. -/
lemma or_slope (p : Polynomial ℝ) (n : ℕ)
    (hp0 : p.eval 0 = 0) (hp1 : (Polynomial.derivative p).eval 0 = 1) :
    (Polynomial.derivative (Polynomial.C 1 - (Polynomial.C 1 - p) ^ n)).eval 0 = (n : ℝ) := by
  have hder : (Polynomial.derivative (Polynomial.C 1 - p)).eval 0 = -1 := by
    rw [Polynomial.derivative_sub, Polynomial.derivative_C, zero_sub]
    simp [hp1]
  rw [Polynomial.derivative_sub, Polynomial.derivative_C, zero_sub, Polynomial.eval_neg]
  rw [Polynomial.derivative_pow]
  rw [Polynomial.eval_mul, Polynomial.eval_mul, Polynomial.eval_C]
  rw [Polynomial.eval_pow, Polynomial.eval_sub, Polynomial.eval_C]
  rw [hp0]
  simp only [sub_zero, one_pow]
  rw [hder]
  ring

/-- The trace-reversal algebra of the two static channels: with
a = Delta Psi and b = Delta Phi the linearized Einstein tensor combination
G_mn = R_mn - (1/2) eta_mn R (eta = diag(-1,1,1,1), R_trace = -R00 + sum Rii,
R00 = b, sum Rii = 4a - b) gives exactly G00 = 2a and sum_i Gii = 2(b-a). -/
lemma trace_reversal (a b : ℝ) :
    (b - (1 / 2 : ℝ) * (-1 : ℝ) * (4 * a - 2 * b) = 2 * a) ∧
    ((4 * a - b) - (3 / 2 : ℝ) * (4 * a - 2 * b) = 2 * (b - a)) := by
  constructor <;> ring

/-- Deep-MOND spherical matching: the scale a0 = s/2 (from the slope-2 OR
composition, PD08 step 5) implies kappa = a0/s = 1/2. -/
lemma kappa_half (s a0 : ℝ) (hs : s ≠ 0) (ha0 : a0 = s / 2) :
    a0 / s = (1 / 2 : ℝ) := by
  rw [ha0]
  field_simp [hs]

end As056

#print axioms As056.or_slope
#print axioms As056.trace_reversal
#print axioms As056.kappa_half