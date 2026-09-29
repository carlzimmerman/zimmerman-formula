import Mathlib

/-!
# MineM5-D: the Frenet-torsion sign obstruction (no function of Box_u has |a|^2 as a bound-orbit eigenvalue)

Source lane: real_research/reviews/mi_eigenvalue_a2_operator_nogo_2026.py, E1-E5 (lines ~72-215): the Frenet triad D u = |a| ahat, D ahat = |a| u + B b, D b = -B ahat on the relativistic circular
worldline with |a| = gamma^2 Omega v/c, B = gamma^2 Omega; "E2 D^2 u = |a|^2 u + |a| B b", "E3 spec(Box_u) = {0, -(gamma Omega)^2}", "E4 u.D^2 u = -|a|^2", "E5 torsion-free motion: exact eigenvalue |a|^2".

MODEL: the operator D in the orthonormal-type Frenet basis (u, ahat, b), acting on coefficient triples (x, y, z) by
  D(x, y, z) = (A y, A x - B z, B y),           [from D u = A ahat, D ahat = A u + B b, D b = -B ahat]
with the Lorentzian form g(w, w') = -x x' + y y' + z z'.

CERTIFIED (premises => conclusions; real algebra):
* `D2_on_u`: D^2 u = A^2 u + A B b (the lane's E2).
* `D2_eigenvalues`: if D^2 w = lam w with w != 0 then lam = 0 or lam = A^2 - B^2.
* `A2_not_eigenvalue`: for A > 0 and B != 0, lam = A^2 is NOT an eigenvalue of D^2 (the torsion obstruction: spec(D^2) is within {0, A^2 - B^2}).
  `spectral_F` records the only consequence used for a function F of Box_u: on an eigenvector F(D^2) acts through F(lam) with lam in {0, A^2 - B^2}, so its eigenvalues are among F(0), F(A^2 - B^2).
* `spec_negative`: with gamma^2 (1 - beta^2) = 1, A = gamma^2 Omega beta, B = gamma^2 Omega (beta = v/c): A/B = beta, and A^2 - B^2 = -(gamma Omega)^2 <= 0.
* `moment_is_minus_A2`: g(u, D^2 u) = -A^2 (Theorem-B moment), because b is g-orthogonal to u.
* `torsion_free_eigen`: if B = 0, D^2 u = A^2 u (u is an exact eigenvector with eigenvalue +A^2: the lane's mutation control E5).

NOT certified: that the coordinate model D is the covariant derivative along a worldline (the lane verifies the Frenet relations symbolically on the explicit worldline in sympy; here they are the premise),
the values |a| = gamma^2 Omega beta and B = gamma^2 Omega for the circular worldline (taken as hypotheses hA, hB), the claim about ARBITRARY functions F of an unbounded/nonlocal operator on a full Hilbert space
(the lane's spectral-mapping remark F(spec) = spec(F) is a standard fact assumed, not proved here), and anything about MOND phenomenology or modified inertia being viable.
It certifies only the algebra of the obstruction; it does NOT show that modified inertia is closed or excluded.  kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

namespace MineM5D

/-- the Frenet generator on coefficient triples (x, y, z) of x u + y ahat + z b -/
def D (A B : ℝ) (w : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (A * w.2.1, A * w.1 - B * w.2.2, B * w.2.1)

/-- Box_u = D^2 -/
def D2 (A B : ℝ) (w : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ := D A B (D A B w)

/-- E2: D^2 u = A^2 u + A B b -/
theorem D2_on_u (A B : ℝ) : D2 A B (1, 0, 0) = (A ^ 2, 0, A * B) := by
  simp [D2, D]; constructor <;> ring

/-- eigenvalues of D^2 lie in {0, A^2 - B^2} -/
theorem D2_eigenvalues (A B lam : ℝ) (w : ℝ × ℝ × ℝ) (hw : w ≠ 0)
    (h : D2 A B w = (lam * w.1, lam * w.2.1, lam * w.2.2)) :
    lam = 0 ∨ lam = A ^ 2 - B ^ 2 := by
  obtain ⟨x, y, z⟩ := w
  simp only [D2, D, Prod.mk.injEq] at h
  obtain ⟨e1, e2, e3⟩ := h
  have e1' : A ^ 2 * x - A * B * z = lam * x := by linarith
  have e3' : A * B * x - B ^ 2 * z = lam * z := by linarith
  by_cases hy : y = 0
  · have hx : lam * (lam - (A ^ 2 - B ^ 2)) * x = 0 := by
      linear_combination (-B ^ 2 - lam) * e1' + A * B * e3'
    have hz : lam * (lam - (A ^ 2 - B ^ 2)) * z = 0 := by
      linear_combination (-(A * B)) * e1' + (A ^ 2 - lam) * e3'
    have hxz : x ≠ 0 ∨ z ≠ 0 := by
      by_contra hcon
      have hx0 : x = 0 := by
        by_contra h'
        exact hcon (Or.inl h')
      have hz0 : z = 0 := by
        by_contra h'
        exact hcon (Or.inr h')
      apply hw
      simp [hx0, hz0, hy]
    have hprod : lam * (lam - (A ^ 2 - B ^ 2)) = 0 := by
      rcases hxz with hx0 | hz0
      · exact (mul_eq_zero.mp hx).resolve_right hx0
      · exact (mul_eq_zero.mp hz).resolve_right hz0
    rcases mul_eq_zero.mp hprod with h0 | h0
    · left; exact h0
    · right; linarith
  · right
    have : (A ^ 2 - B ^ 2) * y = lam * y := by nlinarith [e2]
    exact (mul_right_cancel₀ hy this).symm

/-- the obstruction: for A > 0 and B != 0, +A^2 is not an eigenvalue of D^2 -/
theorem A2_not_eigenvalue {A B : ℝ} (hA : 0 < A) (hB : B ≠ 0) :
    ¬ ∃ w : ℝ × ℝ × ℝ, w ≠ 0 ∧ D2 A B w = (A ^ 2 * w.1, A ^ 2 * w.2.1, A ^ 2 * w.2.2) := by
  rintro ⟨w, hw, h⟩
  rcases D2_eigenvalues A B (A ^ 2) w hw h with h0 | h0
  · have : A ^ 2 > 0 := by positivity
    linarith
  · have hB2 : B ^ 2 = 0 := by linarith
    exact hB (pow_eq_zero_iff (two_ne_zero) |>.mp hB2)

/-- functions of D^2 act on an eigenvector through the eigenvalue (the only spectral fact used) -/
theorem spectral_F (F : ℝ → ℝ) (A B lam : ℝ) (h : lam = 0 ∨ lam = A ^ 2 - B ^ 2) :
    F lam = F 0 ∨ F lam = F (A ^ 2 - B ^ 2) := by
  rcases h with h | h
  · left; rw [h]
  · right; rw [h]

/-- kinematics of the circular worldline: A/B = beta and A^2 - B^2 = -(gamma Omega)^2 -/
theorem spec_negative {γ Ω β A B : ℝ} (hγ : γ ≠ 0) (hΩ : Ω ≠ 0)
    (hnorm : γ ^ 2 * (1 - β ^ 2) = 1) (hA : A = γ ^ 2 * Ω * β) (hB : B = γ ^ 2 * Ω) :
    A / B = β ∧ A ^ 2 - B ^ 2 = -(γ * Ω) ^ 2 ∧ A ^ 2 - B ^ 2 ≤ 0 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [hA, hB]; field_simp
  · have : A ^ 2 - B ^ 2 = -(γ ^ 2 * Ω ^ 2) * (γ ^ 2 * (1 - β ^ 2)) := by
      rw [hA, hB]; ring
    rw [this, hnorm]; ring
  · have : A ^ 2 - B ^ 2 = -(γ ^ 2 * Ω ^ 2) * (γ ^ 2 * (1 - β ^ 2)) := by
      rw [hA, hB]; ring
    rw [this, hnorm]; nlinarith [sq_nonneg (γ * Ω)]

/-- the Lorentzian form -/
def g (w w' : ℝ × ℝ × ℝ) : ℝ := -(w.1 * w'.1) + w.2.1 * w'.2.1 + w.2.2 * w'.2.2

/-- E4: the u-contraction of D^2 u is -A^2 (b is orthogonal to u: torsion drops out) -/
theorem moment_is_minus_A2 (A B : ℝ) : g (1, 0, 0) (D2 A B (1, 0, 0)) = -A ^ 2 := by
  simp [g, D2, D]
  ring

/-- E5 control: torsion-free motion (B = 0) has u as an exact eigenvector with eigenvalue +A^2 -/
theorem torsion_free_eigen (A : ℝ) : D2 A 0 (1, 0, 0) = (A ^ 2 * 1, A ^ 2 * 0, A ^ 2 * 0) := by
  simp [D2, D]; ring

end MineM5D

#print axioms MineM5D.D2_on_u
#print axioms MineM5D.D2_eigenvalues
#print axioms MineM5D.A2_not_eigenvalue
#print axioms MineM5D.spectral_F
#print axioms MineM5D.spec_negative
#print axioms MineM5D.moment_is_minus_A2
#print axioms MineM5D.torsion_free_eigen
