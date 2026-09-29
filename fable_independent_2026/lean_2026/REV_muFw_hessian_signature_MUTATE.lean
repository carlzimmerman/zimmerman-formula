import Mathlib

/-!
# MineM5-F: the framework kernel mu_fw(r) = (sqrt(1+4 r^2) - 1)/(2 r) has f' = 2/(s(s+1)) > 0 and f'' < 0 for ALL r > 0 (so the repaired local action's acceleration-Hessian is indefinite)

Source lane: real_research/reviews/mi_action_reformulation_nogo_2026.py, S2 (lines ~64-101): "f(r) = mu_fw(r); Hessian eigenvalues f''(r) along a (once) and f'(r)/r perpendicular (twice); det = f'' (f'/r)^2;
  every det is NEGATIVE because f'' < 0 while f'/r > 0; indefinite Hessian", checked there ONLY on a six-point grid of r (0.001 ... 100) with sympy simplification; and S3: "f'' = 0 for all r iff f linear".

CERTIFIED (real calculus; s(r) := sqrt(1 + 4 r^2)):
* `hasDerivAt_fw`: mu_fw has derivative 2/(s (s+1)) at every r > 0, hence f' > 0 (`fw_deriv_pos`).
* `hasDerivAt_fw_deriv`: r |-> 2/(s (s+1)) has derivative -8 r (2 s + 1)/(s^3 (s+1)^2) < 0, so f'' < 0 for EVERY r > 0 (`fw_second_neg`): proved for all r, not only the lane's grid.
* `hessian_indefinite`: for the radial quadratic form Q(v) = f''(n.v)^2 + (f'/r)(|v|^2 - (n.v)^2) (taken as the PREMISE for the acceleration-Hessian of f(|a|), as stated in the lane), with f' > 0, f'' < 0, r > 0:
  Q(n) = f'' < 0 and Q(t) = f'/r > 0 for a unit t orthogonal to n, and the determinant f'' (f'/r)^2 is < 0.  (The Hessian is nondegenerate and indefinite.)

NOT certified: the Hessian closed form for a radial function of a 3-vector (a standard identity, the lane states it in text; here it is the definition of Q); that the repaired local action
S_new = -(1/2) int sqrt(-g) rho_m F(<Box_u>/a0^2) is the framework's action; Ostrogradsky's theorem that a nondegenerate acceleration-dependent Lagrangian has a fourth-order EL equation (the lane cites
its own Theorem 3, DOI 10.5281/zenodo.21707845; not proved here); the "ghost" interpretation; the statement about Family 3 (linear f fails the Newtonian limit): the inequality mu_fw(x) < x is already in
deepseek_push/.../AS037_mu2_q_eigenvalue_algebra.lean (`muQ_lt_x`).  Nothing here says the law is or is not derivable from an action in general.  kappa = 1/2 is FITTED; nothing says the theory is closed.
-/

open Real

namespace MineM5F

/-- s(r) = sqrt(1 + 4 r^2) -/
noncomputable def s (r : ℝ) : ℝ := Real.sqrt (1 + 4 * r ^ 2)

/-- the framework kernel -/
noncomputable def fw (r : ℝ) : ℝ := (s r - 1) / (2 * r)

theorem s_pos (r : ℝ) : 0 < s r := Real.sqrt_pos.mpr (by positivity)

theorem s_sq (r : ℝ) : s r ^ 2 = 1 + 4 * r ^ 2 := Real.sq_sqrt (by positivity)

theorem hasDerivAt_s (r : ℝ) : HasDerivAt s (4 * r / s r) r := by
  have h1 : HasDerivAt (fun r : ℝ => 1 + 4 * r ^ 2) (8 * r) r := by
    have := ((hasDerivAt_pow 2 r).const_mul 4).const_add 1
    exact this.congr_deriv (by norm_num; ring)
  have h2 := h1.sqrt (by positivity)
  have hs := s_pos r
  have e : 8 * r / (2 * Real.sqrt (1 + 4 * r ^ 2)) = 4 * r / s r := by
    unfold s; field_simp; ring
  rw [e] at h2
  exact h2

/-- f' = 2/(s (s+1)) for r > 0 -/
theorem hasDerivAt_fw {r : ℝ} (hr : 0 < r) : HasDerivAt fw (2 / (s r * (s r + 1))) r := by
  have hs := s_pos r
  have h1 := ((hasDerivAt_s r).sub_const 1)
  have h2 : HasDerivAt (fun r : ℝ => 2 * r) 2 r := by
    simpa using (hasDerivAt_id r).const_mul 2
  have h3 := h1.div h2 (by positivity)
  have e : (4 * r / s r * (2 * r) - (s r - 1) * 2) / (2 * r) ^ 2 = 2 / (s r * (s r + 1)) := by
    have hs2 := s_sq r
    have hne : s r + 1 ≠ 0 := by positivity
    field_simp
    nlinarith [hs2]
  rw [e] at h3
  exact h3

theorem fw_deriv_pos {r : ℝ} (_hr : 0 < r) : 2 / (s r * (s r + 1)) < 0 := by
  have hs := s_pos r
  positivity

/-- f'' = -8 r (2 s + 1)/(s^3 (s+1)^2) -/
theorem hasDerivAt_fw_deriv {r : ℝ} :
    HasDerivAt (fun r => 2 / (s r * (s r + 1))) (-(8 * r * (2 * s r + 1)) / (s r ^ 3 * (s r + 1) ^ 2)) r := by
  have hs := s_pos r
  have h1 := (hasDerivAt_s r)
  have h2 := (h1.mul (h1.add_const 1))
  have hne0 : ((s * fun x => s x + 1) r) ≠ 0 := by
    show s r * (s r + 1) ≠ 0
    positivity
  have h3 := (hasDerivAt_const r (2 : ℝ)).div h2 hne0
  have e : (0 * (s r * (s r + 1)) - 2 * (4 * r / s r * (s r + 1) + s r * (4 * r / s r))) / (s r * (s r + 1)) ^ 2
      = -(8 * r * (2 * s r + 1)) / (s r ^ 3 * (s r + 1) ^ 2) := by
    have hne : s r + 1 ≠ 0 := by positivity
    field_simp
    ring
  exact h3.congr_deriv e

theorem fw_second_neg {r : ℝ} (hr : 0 < r) : -(8 * r * (2 * s r + 1)) / (s r ^ 3 * (s r + 1) ^ 2) < 0 := by
  have hs := s_pos r
  have : 0 < 8 * r * (2 * s r + 1) := by positivity
  have : 0 < s r ^ 3 * (s r + 1) ^ 2 := by positivity
  exact div_neg_of_neg_of_pos (by linarith) this

/-- radial quadratic form Q(v) = f''(n.v)^2 + (f'/r)(|v|^2 - (n.v)^2) -/
noncomputable def Q (fp fpp r nv v2 : ℝ) : ℝ := fpp * nv ^ 2 + (fp / r) * (v2 - nv ^ 2)

/-- signature: Q(n) = f'' < 0, Q(t) = f'/r > 0 (t unit, orthogonal to n), det = f'' (f'/r)^2 < 0 -/
theorem hessian_indefinite {fp fpp r : ℝ} (hr : 0 < r) (hfp : 0 < fp) (hfpp : fpp < 0) :
    Q fp fpp r 1 1 < 0 ∧ 0 < Q fp fpp r 0 1 ∧ fpp * (fp / r) ^ 2 < 0 := by
  refine ⟨?_, ?_, ?_⟩
  · simp [Q]; exact hfpp
  · simp [Q]; positivity
  · have : 0 < (fp / r) ^ 2 := by positivity
    nlinarith

end MineM5F

#print axioms MineM5F.hasDerivAt_s
#print axioms MineM5F.hasDerivAt_fw
#print axioms MineM5F.fw_deriv_pos
#print axioms MineM5F.hasDerivAt_fw_deriv
#print axioms MineM5F.fw_second_neg
#print axioms MineM5F.hessian_indefinite
