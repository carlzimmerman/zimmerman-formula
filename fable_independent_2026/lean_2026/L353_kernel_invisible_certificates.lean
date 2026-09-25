import Mathlib

open Matrix

/-!
# L353 — a kernel-invisible dark component in C-H/K: algebraic certificates

SCOPE. Lean certifies the algebra of `real_research/g03_audit_2026/L353_kernel_invisible_dark_component.py`: the
reciprocity theorem behind the force law, the asymmetry of L321's "additive" law, the on-shell identities of the
subtraction pair, and the static solution of L340's block with the pair at alpha_c = 0.  The Euler–Lagrange derivation,
the relativistic block's moving-source and mode checks, and the X-COP numbers are symbolic/numeric in the lane, not here.

* `response_symmetric`: for any symmetric field Hessian H and source couplings B, the static species-response matrix
  Gamma = Bᵀ H⁻¹ B is symmetric (potential felt by species s per unit source of species t = the reverse).
* `additive_not_symmetric`: L321's additive law, Gamma = [[1 + C, 1], [1 + C, 1]] (rows: felt by baryons, by the carrier;
  columns: source baryons, carrier), is not symmetric for C ≠ 0, so no Lagrangian produces it.
* `kernel_argument_baryonic`: Lap u = 4 pi G (rho_b + rho_d) and Lap v = 4 pi G rho_d give Lap (u - v) = 4 pi G rho_b.
* `dark_potential_newtonian`: Lap Phi = Lap u + X and 4 pi G Lap lambda = -X give Lap (Phi + 4 pi G lambda) = Lap u.
* `static_block_alpha0`: in L340's static block with the pair and alpha_c = 0, the lapse is
  phi = (1 + C) psi_N,b + psi_N,d with psi_N = -R/(4k^2): baryons boosted, the dark component Newtonian.
* `two_body_imbalance`: under L321's law the force on a carrier particle over the force on the baryons is nu (> 1 in the
  MOND regime); under the construction it is 1.
-/

theorem response_symmetric {n : ℕ} (H : Matrix (Fin n) (Fin n) ℝ) (B : Matrix (Fin n) (Fin 2) ℝ) (hH : Hᵀ = H) :
    (Bᵀ * H⁻¹ * B)ᵀ = Bᵀ * H⁻¹ * B := by
  rw [Matrix.transpose_mul, Matrix.transpose_mul, Matrix.transpose_transpose, Matrix.transpose_nonsing_inv, hH,
    Matrix.mul_assoc]

theorem additive_not_symmetric {C : ℝ} (hC : C ≠ 0) :
    (!![1 + C, 1; 1 + C, 1] : Matrix (Fin 2) (Fin 2) ℝ)ᵀ ≠ !![1 + C, 1; 1 + C, 1] := by
  intro h
  have h01 := congrFun (congrFun h 0) 1
  simp [Matrix.transpose_apply] at h01
  exact hC (by linarith)

theorem kernel_argument_baryonic {G rb rd u2 v2 : ℝ} (hu : u2 = 4 * Real.pi * G * (rb + rd))
    (hv : v2 = 4 * Real.pi * G * rd) : u2 - v2 = 4 * Real.pi * G * rb := by
  rw [hu, hv]; ring

theorem dark_potential_newtonian {G Phi2 u2 lam2 X : ℝ} (hPhi : Phi2 = u2 + X)
    (hlam : 4 * Real.pi * G * lam2 = -X) : Phi2 + 4 * Real.pi * G * lam2 = u2 := by
  rw [hPhi, hlam]; ring

theorem static_block_alpha0 {k C psi phi U v Rb Rd : ℝ} (hk : k ≠ 0)
    (h1 : psi = phi)
    (h2 : -4 * k ^ 2 * psi - 4 * k ^ 2 * (U - phi) - (Rb + Rd) = 0)
    (h4 : 4 * k ^ 2 * (U - phi) + 4 * k ^ 2 * C * (U - v) = 0)
    (h6 : 4 * k ^ 2 * v + Rd = 0) :
    phi = (1 + C) * (-Rb / (4 * k ^ 2)) + (-Rd / (4 * k ^ 2)) := by
  have hk2 : (4 * k ^ 2) ≠ 0 := by positivity
  have hU : U = -(Rb + Rd) / (4 * k ^ 2) := by
    rw [h1] at h2
    field_simp
    linarith
  have hv : v = -Rd / (4 * k ^ 2) := by
    field_simp
    linarith
  have hphi : phi = U + C * (U - v) := by
    have h4' : 4 * k ^ 2 * ((U - phi) + C * (U - v)) = 0 := by linarith
    have : (U - phi) + C * (U - v) = 0 := by
      rcases mul_eq_zero.mp h4' with h | h
      · exact absurd h hk2
      · exact h
    linarith
  rw [hphi, hU, hv]
  field_simp
  ring

theorem two_body_imbalance {nu gN m : ℝ} (hnu : 1 < nu) (hg : 0 < gN) (hm : 0 < m) :
    (nu * gN * m) / (gN * m) = nu ∧ (nu * gN * m) / (gN * m) ≠ 1 := by
  have hpos : gN * m ≠ 0 := by positivity
  constructor
  · field_simp
  · rw [show (nu * gN * m) / (gN * m) = nu by field_simp]
    linarith

#print axioms response_symmetric
#print axioms additive_not_symmetric
#print axioms kernel_argument_baryonic
#print axioms dark_potential_newtonian
#print axioms static_block_alpha0
#print axioms two_body_imbalance
