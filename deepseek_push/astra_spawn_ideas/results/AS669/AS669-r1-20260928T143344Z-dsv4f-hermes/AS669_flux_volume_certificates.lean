import Mathlib

/-!
AS669 -- topological flux integral and metric-volume dependence (k04 branch).

Certified algebraic core (all statements in ℝ, no calculus, no integrals):

  T1 flux_identity_fixes_volume      Φ = q·V and q ≠ 0 ⇒ the volume is fixed by
                                     the flux; i.e. ΔΦ = 0 with Δq = 0 forces
                                     ΔV = 0 (the negative control's algebra).
  T2 simultaneous_fixing_inconsistent  q ≠ 0, V ≠ W ⇒ ¬ (q·V = q·W): q and the
                                     total flux cannot both stay fixed across a
                                     volume-changing metric variation.
  T3 dilution_ratio    fixed flux Φ = q1·V1 = q2·V2 ⇒ q2 = q1·V1/V2  (1/Vol law).
  T4 fixed_q_law       fixed local amplitude q ⇒ Φ2/Φ1 = V2/V1.
  T5 legendre_quadratic  ε = q·P'(q) − P(q) = P(q) for P(q) = Z q²/2 + b β² q²
                         (k04 F1 sign: the promoted primitive contributes
                          +b a0²/G --- reversed vs k01's −b a0²/G).
  T6 eps_positive      Z, b > 0, q ≠ 0, β ≠ 0 ⇒ ε > 0 (positive gravitating
                       vacuum energy of the quadratic four-form action).
  T7 kappa_raw_eq_simpl  κ²(q) = β²q²/ε(q) = 2β²/(Z + 2bβ²): q cancels.
  T8 kappa_volume_blind  κ²(q1) = κ²(q2) for all nonzero amplitudes: the
                         metric-volume channel cannot select κ = 1/2.
  T9 half_iff_ratio    κ² = 1/4 ⟺ Z/β² = 8 − 2b (k04 F2: one number, two
                         couplings; the flux does not fix it).
  T10 residual_nonzero  q ≠ 0, V1 ≠ V2 ⇒ q·V1 ≠ q·V2 (explicit violated
                         identity of the negative control).
-/

noncomputable section

open scoped BigOperators

-- T1
theorem flux_identity_fixes_volume {q V W : ℝ} (hq : q ≠ 0) (h : q * V = q * W) : V = W :=
  mul_left_cancel₀ hq h

-- T2
theorem simultaneous_fixing_inconsistent {q V W : ℝ} (hq : q ≠ 0) (hV : V ≠ W) :
    ¬ (q * V = q * W) := by
  intro h
  exact hV (flux_identity_fixes_volume hq h)

-- T3
theorem dilution_ratio {q1 q2 V1 V2 Φ : ℝ} (hq1 : q1 ≠ 0) (hV1 : V1 ≠ 0)
    (h1 : q1 * V1 = Φ) (h2 : q2 * V2 = Φ) : q2 = q1 * V1 / V2 := by
  have hV2 : V2 ≠ 0 := by
    intro hz
    have h : q2 * V2 = q1 * V1 := by
      rw [h2, ← h1]
    rw [hz, mul_zero] at h
    exact (mul_ne_zero hq1 hV1) h.symm
  have h : q2 * V2 = q1 * V1 := by
    rw [h2, ← h1]
  calc
    q2 = q2 * V2 / V2 := by field_simp [hV2]
    _ = q1 * V1 / V2 := by rw [h]

-- T4
theorem fixed_q_law {q V1 V2 : ℝ} (hq : q ≠ 0) (hV1 : V1 ≠ 0) :
    (q * V2) / (q * V1) = V2 / V1 := by
  field_simp [hq, hV1]

-- T5
theorem legendre_quadratic {Z b β q : ℝ} :
    q * (Z * q + 2 * (b * β ^ 2) * q) - ((Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2)
      = (Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2 := by
  ring

-- T6
theorem eps_positive {Z b β q : ℝ} (hZ : 0 < Z) (hb : 0 < b) (hβ : β ≠ 0) (hq : q ≠ 0) :
    0 < (Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2 := by
  have hq2 : 0 < q ^ 2 := sq_pos_of_ne_zero hq
  have hβ2 : 0 < β ^ 2 := sq_pos_of_ne_zero hβ
  have hz2 : 0 < (Z / 2 : ℝ) := by positivity
  have h1 : 0 < (Z / 2) * q ^ 2 := mul_pos hz2 hq2
  have h2 : 0 < (b * β ^ 2) * q ^ 2 := mul_pos (mul_pos hb hβ2) hq2
  exact add_pos h1 h2

-- T7
theorem kappa_raw_eq_simpl {Z b β q : ℝ} (hq : q ≠ 0) (_hden : Z + 2 * b * β ^ 2 ≠ 0) :
    β ^ 2 * q ^ 2 / ((Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2)
      = 2 * β ^ 2 / (Z + 2 * b * β ^ 2) := by
  field_simp [hq, _hden]

-- T8
theorem kappa_volume_blind {Z b β q1 q2 : ℝ} (hq1 : q1 ≠ 0) (hq2 : q2 ≠ 0)
    (hden : Z + 2 * b * β ^ 2 ≠ 0) :
    β ^ 2 * q1 ^ 2 / ((Z / 2) * q1 ^ 2 + (b * β ^ 2) * q1 ^ 2)
      = β ^ 2 * q2 ^ 2 / ((Z / 2) * q2 ^ 2 + (b * β ^ 2) * q2 ^ 2) := by
  rw [kappa_raw_eq_simpl hq1 hden, kappa_raw_eq_simpl hq2 hden]

-- T9
theorem half_iff_ratio {Z b β : ℝ} (hden : Z + 2 * b * β ^ 2 ≠ 0) :
    2 * β ^ 2 / (Z + 2 * b * β ^ 2) = (1 : ℝ) / 4 ↔ Z = (8 - 2 * b) * β ^ 2 := by
  constructor
  · intro h
    have hc : 2 * β ^ 2 = (1 / 4 : ℝ) * (Z + 2 * b * β ^ 2) := (div_eq_iff hden).mp h
    nlinarith
  · intro hZ
    apply (div_eq_iff hden).mpr
    rw [hZ]
    nlinarith

-- T10
theorem residual_nonzero {q V1 V2 : ℝ} (hq : q ≠ 0) (hV : V1 ≠ V2) : q * V1 ≠ q * V2 := by
  intro h
  exact hV (flux_identity_fixes_volume hq h)

end
