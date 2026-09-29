import Mathlib

open Real Polynomial

/-- p09: S = (1/16 pi) int sqrt(-g) [R - 2 a0^2 U(phi) + ...]:  on a constant-field vacuum Lambda_eff = a0^2 U_v, rho = Lambda_eff/(8 pi) -/
theorem vac_friedmann {a0 Uv : ℝ} : (8 * π / 3) * ((a0 ^ 2 * Uv) / (8 * π)) = (a0 ^ 2 * Uv) / 3 := by
  have hp := Real.pi_pos
  field_simp

/-- the puzzle G rho = 4 a0^2  <->  U_v = 32 pi   (a0 != 0) -/
theorem selfconsistency_iff {a0 Uv : ℝ} (ha : a0 ≠ 0) : (a0 ^ 2 * Uv) / (8 * π) = 4 * a0 ^ 2 ↔ Uv = 32 * π := by
  have hp := Real.pi_pos
  have h8 : (8 * π) ≠ 0 := by positivity
  have h2 : a0 ^ 2 ≠ 0 := by positivity
  rw [div_eq_iff h8]
  constructor
  · intro h
    have : a0 ^ 2 * (Uv - 32 * π) = 0 := by linarith
    rcases mul_eq_zero.mp this with h3 | h3
    · exact absurd h3 h2
    · linarith
  · intro h; rw [h]; ring

/-- 32 pi is irrational (Mathlib: irrational_pi); transcendence of pi is NOT in Mathlib -/
theorem Uv_irrational : Irrational (32 * π) := by
  have h : Irrational π := irrational_pi
  have := h.ratCast_mul (q := 32) (by norm_num)
  simpa using this

/-- so no rational U_v solves the puzzle self-consistency -/
theorem Uv_not_rational (q : ℚ) : (q : ℝ) ≠ 32 * π := by
  intro h
  exact Uv_irrational ⟨q, h⟩

/-- scoped no-go (certified part): a QUADRATIC potential with rational coefficients has a RATIONAL stationary value,
so it can never give U_v = 32 pi. -/
theorem quadratic_potential_no_32pi (α β γ : ℚ) (hα : α ≠ 0) (u : ℝ)
    (hcrit : 2 * (α : ℝ) * u + β = 0) : (α : ℝ) * u ^ 2 + β * u + γ ≠ 32 * π := by
  have hα' : (α : ℝ) ≠ 0 := by exact_mod_cast hα
  have hu : u = -(β : ℝ) / (2 * α) := by
    field_simp; linarith
  have : (α : ℝ) * u ^ 2 + β * u + γ = ((γ - β ^ 2 / (4 * α) : ℚ) : ℝ) := by
    rw [hu]; push_cast; field_simp; ring
  rw [this]
  exact Uv_not_rational _

/-- general local (polynomial, rational-coefficient) potentials: CONDITIONAL on Lindemann's theorem (transcendence of pi),
which is stated here as an explicit hypothesis because Mathlib does not contain it.  A stationary value of V is algebraic. -/
theorem polynomial_potential_no_32pi (hπ : Transcendental ℚ π) (V : ℚ[X]) (u : ℝ)
    (hV' : derivative V ≠ 0) (hcrit : aeval u (derivative V) = 0) : aeval u V ≠ 32 * π := by
  intro h
  have hu : IsAlgebraic ℚ u := ⟨derivative V, hV', hcrit⟩
  have hmem : u ∈ algebraicClosure ℚ ℝ := (mem_algebraicClosure_iff).mpr hu
  have hsub : Algebra.adjoin ℚ {u} ≤ (algebraicClosure ℚ ℝ).toSubalgebra :=
    Algebra.adjoin_le (by simpa using hmem)
  have hval : aeval u V ∈ algebraicClosure ℚ ℝ := hsub (Polynomial.aeval_mem_adjoin_singleton ℚ u)
  rw [h] at hval
  have hpi : π ∈ algebraicClosure ℚ ℝ := by
    have h32 : ((1 / 32 : ℚ) : ℝ) ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).algebraMap_mem _
    have := (algebraicClosure ℚ ℝ).mul_mem h32 hval
    have e : ((1 / 32 : ℚ) : ℝ) * (32 * π) = π := by push_cast; ring
    rwa [e] at this
  exact hπ ((mem_algebraicClosure_iff).mp hpi)

#print axioms vac_friedmann
#print axioms selfconsistency_iff
#print axioms Uv_irrational
#print axioms Uv_not_rational
#print axioms quadratic_potential_no_32pi
#print axioms polynomial_potential_no_32pi
