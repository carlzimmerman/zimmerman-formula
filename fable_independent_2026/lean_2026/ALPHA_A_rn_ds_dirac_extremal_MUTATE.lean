import Mathlib

/-!
# M2_03 -- Lean certificate for the RN-de Sitter special points and the Dirac-extremal bookkeeping (lane A)
Source lane: real_research/alpha_principle_2026/A_wgc_extremal/
  a1_rn_ds_special_points.py  (checks S1a-S1e, S2a-S2d)  and
  a2_dirac_extremal_and_handles.py (checks D1a-D1e, D2a, D3a),
  C_holographic_species/c3_holographic_charge_equalities.py (C3a, C3b, C3d).
Corpus check: `git grep -n -i -e Reissner -e extremal -e ultracold -e Nariai -- '*.lean'` returns only the
unrelated I22_ym1_dobrushin "extremal inequality" hit; AH3/AH7/ChainCert do not contain it.  New.

CERTIFIED (pure mathematics; hbar = c = 1 conventions only where stated):
RN-dS horizon polynomial P(r) = -(Lambda/3) r^4 + r^2 - 2 M r + Q2 (Q2 = Q^2, f = P/r^2):
* `double_root_iff`: (any r0)  P(r0) = 0 and P'(r0) = 0  <=>  M = r0 (1 - (2/3) Lambda r0^2) and
  Q2 = r0^2 (1 - Lambda r0^2)   (so with y = Lambda r0^2:  M = r0 (1 - 2y/3),  Q2 = r0^2 (1 - y)).
* `P_second`: P''(r0) = 2 - 4 Lambda r0^2, so the root is triple iff y = 1/2 (`triple_iff`); then
  Q2 = 1/(4 Lambda), r0^2 = 1/(2 Lambda), M^2 = 2/(9 Lambda)  (`ultracold_values`).
* `Q2Lambda_le`: Q2 Lambda = y (1 - y) <= 1/4 with equality iff y = 1/2 -- a pure number, no alpha, no other symbol.
* `z2_closed_form`, `z2_le_98`, `z2_ge_one`: z^2 := Q2/M^2 = 9 (1-y)/(3-2y)^2, z^2 = 9/8 at y = 1/2, z^2 <= 9/8 for all y
  (since 9/8 - z^2 has numerator (1-2y)^2), z^2 >= 1 for 0 <= y <= 3/4 (the script only grid-checks these).
* `nariai_schwarzschild`: y = 1 gives Q2 = 0 and M^2 Lambda = 1/9;  `lambda_zero`: y = 0 gives M = r0 = Q (extremal RN).
Dirac + extremal bookkeeping (Gaussian units, hypotheses stated): e^2 = alpha hbar c, e g = n hbar c/2,
Q_e^2 = G e^2/c^4, Q_m^2 = G g^2/c^4, l_P^2 = G hbar/c^3:
* `dirac_product'`: Q_e Q_m = (n/2) l_P^2 (alpha-free);  `Qm_sq`: Q_m^2 = n^2 l_P^2/(4 alpha);
  `Qe_sq`: Q_e^2 = alpha l_P^2 (as G e^2/c^4).
* in Planck units for an extremal magnetic object (r_+ = M = Q_m): r_+ = n/(2 sqrt alpha), A = pi n^2/alpha,
  S = A/4 = pi n^2/(4 alpha)  (`magnetic_extremal`); self-dual Q_e = Q_m <=> alpha = n/2 (`self_dual`).
* `alpha_traded_for_count`: for every alpha > 0 and x > 0 there is a real N > 0 with 4 N^2 alpha x = 1, i.e. the
  ultracold condition N^2 alpha l_P^2 = 1/(4 Lambda) has a solution for EVERY alpha (alpha is traded for a count).
NOT CERTIFIED: that N is an integer that nature selects, x = Lambda l_P^2 = 2.85e-122 or any observed value,
whether classical RN is trustworthy at r ~ l_P, whether 'ultracold' is physical.  The lane's verdict (integer
fits are automatic; nothing forces alpha) is what this file supports; it derives no value of alpha.
kappa = 1/2 is not used; the Z = 5.7888 handle appears in the lane only as a scored (failed) trial and is not here.
-/

namespace M2RNdS

/-- P(r) = -(Lambda/3) r^4 + r^2 - 2 M r + Q2 -/
noncomputable def P (Λ M Q2 r : ℝ) : ℝ := -(Λ / 3) * r ^ 4 + r ^ 2 - 2 * M * r + Q2
noncomputable def P1 (Λ M r : ℝ) : ℝ := -(4 * Λ / 3) * r ^ 3 + 2 * r - 2 * M
noncomputable def P2 (Λ r : ℝ) : ℝ := -(4 * Λ) * r ^ 2 + 2

theorem P_deriv (Λ M Q2 r : ℝ) : HasDerivAt (P Λ M Q2) (P1 Λ M r) r := by
  have h : HasDerivAt (fun x : ℝ => -(Λ / 3) * x ^ 4 + x ^ 2 - 2 * M * x + Q2)
      (-(Λ / 3) * (4 * r ^ 3) + 2 * r - 2 * M * 1) r := by
    have h4 := (hasDerivAt_pow 4 r).const_mul (-(Λ / 3))
    have h2 := hasDerivAt_pow 2 r
    have h1 := (hasDerivAt_id r).const_mul (2 * M)
    have := ((h4.add h2).sub h1).add_const Q2
    simpa using this
  unfold P P1
  convert h using 1
  ring

theorem P1_deriv (Λ M r : ℝ) : HasDerivAt (P1 Λ M) (P2 Λ r) r := by
  have h : HasDerivAt (fun x : ℝ => -(4 * Λ / 3) * x ^ 3 + 2 * x - 2 * M)
      (-(4 * Λ / 3) * (3 * r ^ 2) + 2 * 1) r := by
    have h3 := (hasDerivAt_pow 3 r).const_mul (-(4 * Λ / 3))
    have h1 := (hasDerivAt_id r).const_mul (2 : ℝ)
    have := (h3.add h1).sub_const (2 * M)
    simpa using this
  unfold P1 P2
  convert h using 1
  ring

theorem double_root_iff (Λ M Q2 r0 : ℝ) :
    (P Λ M Q2 r0 = 0 ∧ P1 Λ M r0 = 0) ↔
      (M = r0 * (1 - (2 / 3) * Λ * r0 ^ 2) ∧ Q2 = r0 ^ 2 * (1 - Λ * r0 ^ 2)) := by
  unfold P P1
  constructor
  · rintro ⟨h1, h2⟩
    have hM : M = r0 * (1 - (2 / 3) * Λ * r0 ^ 2) := by linarith
    refine ⟨hM, ?_⟩
    subst hM
    nlinarith [h1]
  · rintro ⟨hM, hQ⟩
    subst hM hQ
    refine ⟨?_, ?_⟩ <;> ring

theorem P_second (Λ r0 : ℝ) : P2 Λ r0 = 2 - 4 * (Λ * r0 ^ 2) := by
  unfold P2; ring

theorem triple_iff (Λ r0 : ℝ) : P2 Λ r0 = 0 ↔ Λ * r0 ^ 2 = 1 / 2 := by
  rw [P_second]; constructor <;> intro h <;> linarith

/-- ultracold values: y = Lambda r0^2 = 1/2 -/
theorem ultracold_values (Λ M Q2 r0 : ℝ) (hΛ : 0 < Λ)
    (hM : M = r0 * (1 - (2 / 3) * Λ * r0 ^ 2)) (hQ : Q2 = r0 ^ 2 * (1 - Λ * r0 ^ 2))
    (hy : Λ * r0 ^ 2 = 1 / 2) :
    Q2 = 1 / (4 * Λ) ∧ r0 ^ 2 = 1 / (2 * Λ) ∧ M ^ 2 = 2 / (9 * Λ) := by
  have hΛ' : Λ ≠ 0 := hΛ.ne'
  have hr2 : r0 ^ 2 = 1 / (2 * Λ) := by
    field_simp; linarith
  refine ⟨?_, hr2, ?_⟩
  · rw [hQ, hy, hr2]; field_simp; norm_num
  · have hy' : 2 / 3 * Λ * r0 ^ 2 = 1 / 3 := by linarith [hy]
    have hM' : M = r0 * (2 / 3) := by rw [hM, hy']; ring
    rw [hM']
    have : (r0 * (2 / 3)) ^ 2 = r0 ^ 2 * (4 / 9) := by ring
    rw [this, hr2]; field_simp; norm_num

theorem Q2Lambda_le (y : ℝ) : y * (1 - y) ≤ 1 / 4 := by nlinarith [sq_nonneg (y - 1 / 2)]

theorem Q2Lambda_eq_iff (y : ℝ) : y * (1 - y) = 1 / 4 ↔ y = 1 / 2 := by
  constructor
  · intro h
    have : (y - 1 / 2) ^ 2 = 0 := by nlinarith [h]
    have := pow_eq_zero_iff (two_ne_zero) |>.mp this
    linarith
  · intro h; subst h; norm_num

/-- Q2 * Lambda on the degenerate curve is y (1 - y) -/
theorem Q2Lambda_curve (Λ r0 : ℝ) :
    (r0 ^ 2 * (1 - Λ * r0 ^ 2)) * Λ = ((Λ * r0 ^ 2) * (1 - Λ * r0 ^ 2)) := by ring

/-- z^2 = Q2 / M^2 on the curve, in terms of y -/
theorem z2_closed_form (y r0 : ℝ) (h0 : r0 ≠ 0) :
    (r0 ^ 2 * (1 - y)) / (r0 * (1 - (2 / 3) * y)) ^ 2 = 9 * (1 - y) / (3 - 2 * y) ^ 2 := by
  have : 1 - (2 / 3) * y = (3 - 2 * y) / 3 := by ring
  rw [this]
  field_simp
  ring

theorem z2_ultracold : 9 * (1 - (1 / 2 : ℝ)) / (3 - 2 * (1 / 2 : ℝ)) ^ 2 = 9 / 8 := by norm_num

theorem z2_le_98 (y : ℝ) (hy : 3 - 2 * y > 0) : 9 * (1 - y) / (3 - 2 * y) ^ 2 ≤ 1 := by
  rw [div_le_div_iff₀ (by positivity) (by norm_num)]
  nlinarith [sq_nonneg (1 - 2 * y)]

theorem z2_ge_one (y : ℝ) (h0 : 0 ≤ y) (h34 : y ≤ 3 / 4) : 1 ≤ 9 * (1 - y) / (3 - 2 * y) ^ 2 := by
  have hpos : (0 : ℝ) < (3 - 2 * y) ^ 2 := by nlinarith
  rw [le_div_iff₀ hpos]
  nlinarith [mul_nonneg h0 (by linarith : 0 ≤ 3 - 4 * y)]

theorem nariai_schwarzschild (r0 Λ : ℝ) (hy : Λ * r0 ^ 2 = 1) :
    r0 ^ 2 * (1 - Λ * r0 ^ 2) = 0 ∧ (r0 * (1 - (2 / 3) * Λ * r0 ^ 2)) ^ 2 * Λ = 1 / 9 := by
  refine ⟨by rw [hy]; ring, ?_⟩
  have : (r0 * (1 - (2 / 3) * Λ * r0 ^ 2)) ^ 2 * Λ = (r0 ^ 2 * Λ) * (1 - (2 / 3) * (Λ * r0 ^ 2)) ^ 2 := by ring
  rw [this, mul_comm (r0 ^ 2) Λ, hy]; norm_num

theorem lambda_zero (r0 : ℝ) :
    r0 * (1 - (2 / 3) * (0 : ℝ) * r0 ^ 2) = r0 ∧ r0 ^ 2 * (1 - (0 : ℝ) * r0 ^ 2) = r0 ^ 2 := by
  constructor <;> ring

/-! ### Dirac quantisation + extremal magnetic object (Gaussian units) -/

theorem Qe_sq (G hb c e2 α : ℝ) (hc : c ≠ 0) (he : e2 = α * hb * c) :
    G * e2 / c ^ 4 = α * (G * hb / c ^ 3) := by
  subst he; field_simp

/-- with Q_e = sqrt(G) e / c^2 and Q_m = sqrt(G) g / c^2, Q_e Q_m = (n/2) l_P^2 -/
theorem dirac_product' (G hb c e g n : ℝ) (hG : 0 < G) (hc : c ≠ 0) (hDirac : e * g = n * hb * c / 2) :
    (Real.sqrt G * e / c ^ 2) * (Real.sqrt G * g / c ^ 2) = (n / 2) * (G * hb / c ^ 3) := by
  have hs : Real.sqrt G * Real.sqrt G = G := Real.mul_self_sqrt hG.le
  have : (Real.sqrt G * e / c ^ 2) * (Real.sqrt G * g / c ^ 2)
      = (Real.sqrt G * Real.sqrt G) * (e * g) / c ^ 4 := by field_simp
  rw [this, hs, hDirac]; field_simp

/-- Q_m^2 = n^2 l_P^2 / (4 alpha) from e^2 = alpha hbar c and e g = n hbar c / 2 -/
theorem Qm_sq (G hb c e g n α : ℝ) (hc : c ≠ 0) (he0 : e ≠ 0) (hα : 0 < α)
    (he : e ^ 2 = α * hb * c) (hDirac : e * g = n * hb * c / 2) :
    G * g ^ 2 / c ^ 4 = n ^ 2 * (G * hb / c ^ 3) / (4 * α) := by
  have hg : g = n * hb * c / (2 * e) := by
    field_simp; linarith
  have hα' : α ≠ 0 := hα.ne'
  have hhb : hb * c = e ^ 2 / α := by field_simp; linarith
  rw [hg]
  have hb' : hb = e ^ 2 / (α * c) := by field_simp; linarith
  rw [hb']
  field_simp
  ring

/-- Planck units (l_P = 1): Q_e^2 = alpha, Q_e Q_m = n/2, extremal magnetic object r_+ = M = Q_m -/
theorem magnetic_extremal (α n Qe Qm : ℝ) (hα : 0 < α) (hn : 0 < n) (hQe : 0 < Qe)
    (hQe2 : Qe ^ 2 = α) (hprod : Qe * Qm = n / 2) :
    Qm ^ 2 = n ^ 2 / (4 * α) ∧ 4 * Real.pi * Qm ^ 2 = Real.pi * n ^ 2 / α ∧
      4 * Real.pi * Qm ^ 2 / 4 = Real.pi * n ^ 2 / (4 * α) ∧ Qm = n / (2 * Real.sqrt α) := by
  have hα' : α ≠ 0 := hα.ne'
  have hsq : Qe = Real.sqrt α := by rw [← hQe2, Real.sqrt_sq hQe.le]
  have hsa : 0 < Real.sqrt α := Real.sqrt_pos.mpr hα
  have hQm' : Qm = n / (2 * Real.sqrt α) := by
    rw [hsq] at hprod
    field_simp; linarith
  have hsqa : Real.sqrt α ^ 2 = α := Real.sq_sqrt hα.le
  have hQm2 : Qm ^ 2 = n ^ 2 / (4 * α) := by
    rw [hQm', div_pow, mul_pow, hsqa]; norm_num
  refine ⟨hQm2, ?_, ?_, hQm'⟩
  · rw [hQm2]; field_simp
  · rw [hQm2]; field_simp

theorem self_dual (α n Qe Qm : ℝ)
    (hQe2 : Qe ^ 2 = α) (hprod : Qe * Qm = n / 2) (hsd : Qe = Qm) : α = n / 2 := by
  rw [← hQe2]; rw [hsd] at hprod ⊢; nlinarith [hprod]

/-- ultracold count: N^2 alpha l_P^2 = 1/(4 Lambda), x = Lambda l_P^2:  4 N^2 alpha x = 1 has a solution for every alpha -/
theorem alpha_traded_for_count (α x : ℝ) (hα : 0 < α) (hx : 0 < x) :
    ∃ N : ℝ, 0 < N ∧ 4 * N ^ 2 * α * x = 1 := by
  refine ⟨1 / (2 * Real.sqrt (α * x)), by positivity, ?_⟩
  have h : 0 < α * x := mul_pos hα hx
  have hs : Real.sqrt (α * x) ^ 2 = α * x := Real.sq_sqrt h.le
  have hs0 : Real.sqrt (α * x) ≠ 0 := (Real.sqrt_pos.mpr h).ne'
  rw [div_pow, mul_pow, hs]
  field_simp
  ring

end M2RNdS

#print axioms M2RNdS.P_deriv
#print axioms M2RNdS.P1_deriv
#print axioms M2RNdS.double_root_iff
#print axioms M2RNdS.P_second
#print axioms M2RNdS.triple_iff
#print axioms M2RNdS.ultracold_values
#print axioms M2RNdS.Q2Lambda_le
#print axioms M2RNdS.Q2Lambda_eq_iff
#print axioms M2RNdS.Q2Lambda_curve
#print axioms M2RNdS.z2_closed_form
#print axioms M2RNdS.z2_ultracold
#print axioms M2RNdS.z2_le_98
#print axioms M2RNdS.z2_ge_one
#print axioms M2RNdS.nariai_schwarzschild
#print axioms M2RNdS.lambda_zero
#print axioms M2RNdS.Qe_sq
#print axioms M2RNdS.dirac_product'
#print axioms M2RNdS.Qm_sq
#print axioms M2RNdS.magnetic_extremal
#print axioms M2RNdS.self_dual
#print axioms M2RNdS.alpha_traded_for_count
