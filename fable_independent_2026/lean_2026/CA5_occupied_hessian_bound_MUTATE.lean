import Mathlib

/-!
# M3C -- occupied-FRW velocity Hessian: the exact eigen-bound G >= (D/F_d) G0, the shift completion of the
#        square, D_R > 0 for all 0 < alpha < 2, and the UV host-speed identity

Source: `real_research/breakthrough_review_2026_09_26/occupied/RESULT.md` ("The decisive relation" and
"UV") and `occupied/check.py` (checks `occupied_shift_stationarity`, `occupied_shift_reduction`,
`parallel_kinetic_determinant`, `carrier_occupation_control_identity`, `flat_vacuum_positive_decomposition`,
`occupied_FRW_UV_host_speed`).  RESULT.md asserts "G >= (D/F_d) G0 > 0 whenever D > 0" and that the
normalised matrix has one eigenvalue D/F_d; the committed `OccupiedBridge20260926.lean` proves the
determinant identity and the positivity of pieces, NOT this quadratic-form bound, NOT the shift
completion, and only alpha <= 1 is covered for alpha_e by `PQBridge20260926.lean`.

CERTIFIED (real algebra; hypotheses explicit):
  * `hessian_bound_identity` : in the host/parallel block with kinetic form
        q(p, c) = M K p^2 + c^2 - (M K H p - Q s c)^2 / (M F),   F = K H^2 + D + Q^2 s^2 / M  (M, F > 0)
    one has the EXACT identity   q(p,c) - (D/F)(M K p^2 + c^2) = K (H c + Q s p)^2 / F  (>= 0).
    (s = |v| the carrier speed, so s^2 = 2T;  c = the carrier velocity component along v.)
  * `hessian_bound`   : hence q >= (D/F)(M K p^2 + c^2), and q > 0 whenever D > 0 and (p,c) != 0.
  * `D_flat_pos`      : D_R = alpha_e q^2 + 2 r (1-r) rho_exc / M > 0 for every 0 < alpha < 2,
                        0 <= r < 1, rho_exc >= 0, M > 0, q^2 > 0 (alpha_e = 2 - (2-alpha)(1-r)^2 > 0).
  * `shift_completion`: the shift block S(b) (b = x beta) satisfies
        S(b) = R - (M c2 / 2)(b - b*)^2  with b* = (3 + 2/c2) ss - v chi / (M c2),
        R = M K ss^2/2 - (3+2/c2) ss v chi + (v chi)^2 / (2 M c2), K = 2 (2 + 3 c2) / c2;
    so b* is the unique maximiser and the reduced value is R (c2 > 0, M > 0).
  * `UV_host_speed`   : 2 (2-alpha) / (K alpha) = c2 (2-alpha) / ((2 + 3 c2) alpha).

NOT CERTIFIED: the ADM/Dirac derivation of the block (its coefficients are hypotheses), finite-q restoring
matrix, nonlinear evolution, the homogeneous constraint, any observational claim.  No physical claim is an
axiom; no empirical premise; kappa = 1/2 is not involved.
-/

noncomputable section
namespace M3C

theorem hessian_bound_identity (M K H Q s D F p c : ℝ)
    (hM : M ≠ 0) (hF : F ≠ 0)
    (hFdef : F = K * H ^ 2 + D + Q ^ 2 * s ^ 2 / M) :
    (M * K * p ^ 2 + c ^ 2 - (M * K * H * p - Q * s * c) ^ 2 / (M * F))
      - D / F * (M * K * p ^ 2 + c ^ 2)
    = K * (H * c + Q * s * p) ^ 2 / F := by
  have hD : D = F - K * H ^ 2 - Q ^ 2 * s ^ 2 / M := by rw [hFdef]; ring
  rw [hD]
  field_simp
  ring

theorem hessian_bound (M K H Q s D F p c : ℝ)
    (hM : 0 < M) (hK : 0 < K) (hF : 0 < F)
    (hFdef : F = K * H ^ 2 + D + Q ^ 2 * s ^ 2 / M) :
    D / F * (M * K * p ^ 2 + c ^ 2)
      ≤ M * K * p ^ 2 + c ^ 2 - (M * K * H * p - Q * s * c) ^ 2 / (M * F) := by
  have h := hessian_bound_identity M K H Q s D F p c hM.ne' hF.ne' hFdef
  have hnn : 0 ≤ K * (H * c + Q * s * p) ^ 2 / F := by positivity
  linarith

theorem hessian_pos (M K H Q s D F p c : ℝ)
    (hM : 0 < M) (hK : 0 < K) (hF : 0 < F) (hD : 0 < D)
    (hFdef : F = K * H ^ 2 + D + Q ^ 2 * s ^ 2 / M) (hpc : p ≠ 0 ∨ c ≠ 0) :
    0 < M * K * p ^ 2 + c ^ 2 - (M * K * H * p - Q * s * c) ^ 2 / (M * F) := by
  have h := hessian_bound M K H Q s D F p c hM hK hF hFdef
  have hW : 0 < M * K * p ^ 2 + c ^ 2 := by
    rcases hpc with hp | hc
    · have : 0 < p ^ 2 := by positivity
      have : 0 < M * K * p ^ 2 := by positivity
      nlinarith [sq_nonneg c]
    · have : 0 < c ^ 2 := by positivity
      have : 0 ≤ M * K * p ^ 2 := by positivity
      linarith
  have : 0 < D / F * (M * K * p ^ 2 + c ^ 2) := by positivity
  linarith

/-- D_R > 0 for the whole range 0 < alpha < 2 (PQBridge covers only alpha <= 1). -/
theorem D_flat_pos (alpha r x M rho : ℝ) (ha0 : 0 < alpha) (ha2 : alpha < 2)
    (hr0 : 0 ≤ r) (hr1 : r < 1) (hx : 0 < x) (hM : 0 < M) (hrho : 0 ≤ rho) :
    0 < (2 - (2 - alpha) * (1 - r) ^ 2) * x - 2 * r * (1 - r) * rho / M := by
  have hb : 0 < 2 - alpha := by linarith
  have hq0 : 0 < 1 - r := by linarith
  have hq1 : 1 - r ≤ 1 := by linarith
  have hsq : (1 - r) ^ 2 ≤ 1 := by nlinarith
  have hsqp : 0 < (1 - r) ^ 2 := by positivity
  have hae : 0 < 2 - (2 - alpha) * (1 - r) ^ 2 := by nlinarith
  have h1 : 0 < (2 - (2 - alpha) * (1 - r) ^ 2) * x := mul_pos hae hx
  have h2 : 0 ≤ 2 * r * (1 - r) * rho / M := by positivity
  linarith

/-- the occupation control identity in the flat-vacuum case, assembled with D_R > 0:
    Delta - Q^2 v^2 / M = alpha_e x + 2 r (1-r)(T+V)/M with T = v^2/2. -/
theorem D_flat_decomposition (alpha r x M v V : ℝ) :
    ((2 - (2 - alpha) * (1 - r) ^ 2) * x
        + 2 * ((v ^ 2 / 2) + (V - v ^ 2 / 2) * r - V * r ^ 2) / M)
      - (1 - r) ^ 2 * v ^ 2 / M
    = (2 - (2 - alpha) * (1 - r) ^ 2) * x + 2 * r * (1 - r) * (v ^ 2 / 2 + V) / M := by
  ring

theorem shift_completion (M c2 v chi ss b : ℝ) (hM : M ≠ 0) (hc : c2 ≠ 0) :
    M / 2 * (-6 * ss ^ 2 + 4 * b * ss - c2 * (3 * ss - b) ^ 2) - b * v * chi
    = (M * (2 * (2 + 3 * c2) / c2) * ss ^ 2 / 2 - (3 + 2 / c2) * ss * v * chi
          + (v * chi) ^ 2 / (2 * M * c2))
      - M * c2 / 2 * (b - ((3 + 2 / c2) * ss - v * chi / (M * c2))) ^ 2 := by
  field_simp
  ring

theorem shift_unique_max (M c2 v chi ss b : ℝ) (hM : 0 < M) (hc : 0 < c2) :
    M / 2 * (-6 * ss ^ 2 + 4 * b * ss - c2 * (3 * ss - b) ^ 2) - b * v * chi
      ≤ (M * (2 * (2 + 3 * c2) / c2) * ss ^ 2 / 2 - (3 + 2 / c2) * ss * v * chi
          + (v * chi) ^ 2 / (2 * M * c2)) := by
  rw [shift_completion M c2 v chi ss b hM.ne' hc.ne']
  have : 0 ≤ M * c2 / 2 * (b - ((3 + 2 / c2) * ss - v * chi / (M * c2))) ^ 2 := by positivity
  linarith

theorem UV_host_speed (alpha c2 : ℝ) (halpha : alpha ≠ 0) (hc : c2 ≠ 0)
    (h2 : 2 + 3 * c2 ≠ 0) :
    2 * (2 - alpha) / ((2 * (2 + 3 * c2) / c2) * alpha)
      = c2 * (2 - alpha) / ((2 + 3 * c2) * alpha) := by
  field_simp

end M3C

#print axioms M3C.hessian_bound_identity
#print axioms M3C.hessian_bound
#print axioms M3C.hessian_pos
#print axioms M3C.D_flat_pos
#print axioms M3C.D_flat_decomposition
#print axioms M3C.shift_completion
#print axioms M3C.shift_unique_max
#print axioms M3C.UV_host_speed
