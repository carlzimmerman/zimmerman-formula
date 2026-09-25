import Mathlib

/-!
# L330 — the moving-source gate: algebraic certificates

SCOPE. Lean certifies the algebra `real_research/g03_audit_2026/L330_moving_source_momentum_gate.py` rests on,
not the physics (the reduction of C-H to these equations is in the Python lane, M1).

* `momentum_divergence`: for the linearised extrinsic curvature K_ij = (hdot_ij - k_i N_j - k_j N_i)/2 (Fourier
  symbols, any wavevector k, any shift N, any hdot), the divergence of the momentum constraint,
  -k_i k_j K_ij + |k|^2 K, equals half the time derivative of the leaf curvature symbol: every shift term cancels.
* `lambda_control`: with a K^2 coefficient lambda != 1 the same combination is NOT shift-free (explicit witness).
* `block_lapse`: in astra's truncated block the lapse is F (1 + C)/C, with no dependence on the source rho.
-/

theorem momentum_divergence (k N : Fin 3 → ℝ) (hd : Fin 3 → Fin 3 → ℝ) :
    (-(∑ i, ∑ j, k i * k j * ((hd i j - k i * N j - k j * N i) / 2))
        + (∑ i, k i ^ 2) * (∑ i, (hd i i - k i * N i - k i * N i) / 2))
      = (-(∑ i, ∑ j, k i * k j * hd i j) + (∑ i, k i ^ 2) * (∑ i, hd i i)) / 2 := by
  simp only [Fin.sum_univ_three]
  ring

/-- With lambda = 2 the lambda-weighted divergence keeps a shift term: k = N = e_1, hdot = 0. -/
theorem lambda_control :
    let k : Fin 3 → ℝ := ![1, 0, 0]
    let N : Fin 3 → ℝ := ![1, 0, 0]
    (-(∑ i, ∑ j, k i * k j * ((0 - k i * N j - k j * N i) / 2))
        + 2 * (∑ i, k i ^ 2) * (∑ i, (0 - k i * N i - k i * N i) / 2)) ≠ 0 := by
  simp [Fin.sum_univ_three]
  norm_num

/-- astra's truncated block (ACTION.md L_2): momentum constraint integrated, U equation, lapse equation. -/
theorem block_lapse {k C F rho psi phi U : ℝ} (hk : k ≠ 0)
    (hpsi : 4 * k ^ 2 * (psi - F) = -rho)
    (hU : 4 * k ^ 2 * (U - phi) + 4 * k ^ 2 * C * U = 0)
    (hphi : -4 * k ^ 2 * psi - 4 * k ^ 2 * (U - phi) - rho = 0) :
    phi * C = F * (1 + C) := by
  have hk4 : (4 * k ^ 2 : ℝ) ≠ 0 := mul_ne_zero (by norm_num) (pow_ne_zero 2 hk)
  have e1 : (1 + C) * U - phi = 0 := by
    have h : (4 * k ^ 2) * ((1 + C) * U - phi) = 0 := by linear_combination hU
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h hk4
    · exact h
  have e2 : phi - U - F = 0 := by
    have h : (4 * k ^ 2) * (phi - U - F) = 0 := by linear_combination hphi + hpsi
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h hk4
    · exact h
  linear_combination e1 + (1 + C) * e2

/-- The same, divided out: the lapse is set by the integration constant F alone. -/
theorem block_lapse_div {k C F rho psi phi U : ℝ} (hk : k ≠ 0) (hC : C ≠ 0)
    (hpsi : 4 * k ^ 2 * (psi - F) = -rho)
    (hU : 4 * k ^ 2 * (U - phi) + 4 * k ^ 2 * C * U = 0)
    (hphi : -4 * k ^ 2 * psi - 4 * k ^ 2 * (U - phi) - rho = 0) :
    phi = F * (1 + C) / C := by
  have h := block_lapse hk hpsi hU hphi
  field_simp
  linarith [h]

#print axioms momentum_divergence
#print axioms lambda_control
#print axioms block_lapse
#print axioms block_lapse_div
