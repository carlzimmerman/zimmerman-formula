import Mathlib

/-! # AS142 — carrier Legendre transform without freezing t_c (Lean certificate)

Branch CA5-GNC-R (ACTION.md R1) with inherited CA4-GNC host (FINAL_ACTION (4)),
perspective/reciprocal-barrier carrier (PERSPECTIVE_VARIANT P1–P7 + vacuum/ACTION R1–R3):

  t_c = 1 + Z − ⟨Z⟩_h ∈ (0, ∞)   (varied, NOT frozen)
  L_d = t_c·K_d − W_exc/t_c − V0·F(t_c),   F(t) = 1 + (t−1)⁴/t²
  K_d = (1/2)·Σ_A n(φ_A)²,   W_exc = (1/2)Σ_A|Dφ_A|² + Vmix
  Π_A = sqrt(h)·p_A,   p_A = Π_A/sqrt(h) = t_c·n(φ_A)
  φ̇_A = N·n(φ_A) + Nⁱ∂ᵢφ_A   (shift retained)

Certified algebraic identities (ℝ, per unit sqrt(h); the common factor N·sqrt(h) and the
spatial integral are factored out — every identity below is homogeneous in those factors):

  1. `legendre_carrier`  :  Σ_A Π_A·φ̇_A − N·sqrt(h)·L_d = N·sqrt(h)·[(Σ_A p_A²/2 + W_exc)/t_c
                           + V0·F(t_c)] + Σ_A sqrt(h)·p_A·Nⁱ∂ᵢφ_A, i.e. the displayed H_R plus
                           the shift term — the Legendre transform at FIXED (parametric) t_c.
  2. `source_identity`   :  ∂/∂t_c[(Σ_A p_A²/2 + W_exc)/t_c + V0·F(t_c)] at fixed p_A, evaluated
                           at the Legendre image p_A = t_c·n_A, equals −σ_R, where
                           σ_R = K_d + W_exc/t_c² − V0·F'(t_c) is the velocity-form source (R3):
                           σ_R matches (R4)'s source after substitution (σ_H + σ_R = 0).
  3. `neg_control_mismatch` : NEGATIVE CONTROL. Differentiating the transformed Hamiltonian at
                           FIXED VELOCITIES n_A gives K_d − W/t_c² + V0·F'(t_c), while the correct
                           fixed-momentum derivative at the same point is −K_d − W/t_c² + V0·F'(t_c).
                           The mismatch is exactly 2·K_d = Σ_A n_A² ≠ 0 for any moving carrier:
                           the forbidden procedure is DETECTED, never silently zero.
  4. `floor_identity`    :  ρ_R − t_c·σ_R = V0·(F(t_c) + t_c·F'(t_c))  (R3 bookkeeping),
                           and at the inactive branch t_c = 1: F(1) = 1 (so ρ_R = K + W + V0).
-/

noncomputable section

open BigOperators

namespace AS142

/- Single-field certificates first (the per-A algebra). -/

/-- Legendre identity, single field, INCLUDING the shift term (φ̇ = N·n + sh):
    (t·n)·(N·n + sh) − N·(t·(n²/2) − W/t − V0·F) = N·(((t·n)²/2 + W)/t + V0·F) + (t·n)·sh
    for t ≠ 0.  (Π = sqrt(h)·p with p = t·n; sqrt(h) factored on both sides.) -/
theorem legendre_carrier (t n W V0 F N sh : ℝ) (ht : t ≠ 0) :
    (t * n) * (N * n + sh) - N * (t * (n ^ 2 / 2) - W / t - V0 * F)
      = N * (((t * n) ^ 2 / 2 + W) / t + V0 * F) + (t * n) * sh := by
  field_simp [ht]
  ring

/-- Canonical (fixed-momentum) Z-source after substitution p = t·n, plus the velocity-form
    source σ_R = n²/2 + W/t² − V0·F', vanish identically: σ_H + σ_R = 0. -/
theorem source_identity (t n W V0 F' : ℝ) (ht : t ≠ 0) :
    (-(((t * n) ^ 2 / 2 + W) / t ^ 2) + V0 * F') + (n ^ 2 / 2 + W / t ^ 2 - V0 * F') = 0 := by
  field_simp [ht]
  ring

/-- NEGATIVE CONTROL: fixed-velocity derivative minus fixed-momentum derivative of the
    transformed Hamiltonian, at the same phase point, equals n² = 2·K_d ≠ 0 for n ≠ 0.
    The two procedures are distinct by exactly the kinetic density — the mismatch is detected. -/
theorem neg_control_mismatch (t n W V0 F' : ℝ) (ht : t ≠ 0) :
    (n ^ 2 / 2 - W / t ^ 2 + V0 * F')
      - (-(((t * n) ^ 2 / 2 + W) / t ^ 2) + V0 * F') = n ^ 2 := by
  field_simp [ht]
  ring

/-- R3 bookkeeping: ρ_R − t·σ_R = V0·(F + t·F'). -/
theorem floor_identity (t n W V0 F F' : ℝ) (ht : t ≠ 0) :
    (t * (n ^ 2 / 2) + W / t + V0 * F) - t * (n ^ 2 / 2 + W / t ^ 2 - V0 * F')
      = V0 * (F + t * F') := by
  field_simp [ht]
  ring

/-- Inactive branch: F(1) = 1 + (1−1)⁴/1² = 1. -/
theorem F_at_one : 1 + (1 - 1 : ℝ) ^ 4 / 1 ^ 2 = 1 := by
  norm_num

/- Field-sum certificates: the above per-A algebra summed over a finite field index set. -/

/-- Legendre identity over a finite field index set (shift retained). -/
theorem legendre_carrier_sum {ι : Type} [Fintype ι] (n sh : ι → ℝ)
    (t W V0 F N : ℝ) (ht : t ≠ 0) :
    (∑ i, (t * n i) * (N * n i + sh i)) - N * (t * (∑ i, (n i) ^ 2 / 2) - W / t - V0 * F)
      = N * (((∑ i, (t * n i) ^ 2) / 2 + W) / t + V0 * F) + ∑ i, (t * n i) * sh i := by
  -- distribute inside the first sum, split it
  simp_rw [mul_add]
  rw [Finset.sum_add_distrib]
  -- hpart: the kinetic and potential parts coincide (squares summed)
  have hpart : (∑ i, (t * n i) * (N * n i)) - N * (t * (∑ i, (n i) ^ 2 / 2) - W / t - V0 * F)
      = N * (((∑ i, (t * n i) ^ 2) / 2 + W) / t + V0 * F) := by
    -- pull N out of the first sum; relate both sums of squares
    have hlin : (∑ i, (t * n i) * (N * n i)) = N * (t * ∑ i, (n i) ^ 2) := by
      calc
        (∑ i, (t * n i) * (N * n i)) = ∑ i, N * ((t * n i) * n i) := by
          refine Finset.sum_congr rfl ?_
          intro i hi
          ring
        _ = N * (∑ i, (t * n i) * n i) := by rw [Finset.mul_sum]
        _ = N * (t * ∑ i, (n i) ^ 2) := by
          congr 1
          calc
            (∑ i, (t * n i) * n i) = ∑ i, (t * (n i) ^ 2) := by
              refine Finset.sum_congr rfl ?_
              intro i hi
              ring
            _ = t * ∑ i, (n i) ^ 2 := by rw [Finset.mul_sum]
    have hsq : (∑ i, (t * n i) ^ 2) = t ^ 2 * ∑ i, (n i) ^ 2 := by
      calc
        (∑ i, (t * n i) ^ 2) = ∑ i, (t ^ 2 * (n i) ^ 2) := by
          refine Finset.sum_congr rfl ?_
          intro i hi
          ring
        _ = t ^ 2 * ∑ i, (n i) ^ 2 := by rw [Finset.mul_sum]
    rw [hlin, hsq]
    rw [← Finset.sum_div]
    field_simp [ht]
    ring
  -- split off the shift sums: cancel the common sum by linearity of nlinarith
  nlinarith [hpart]

/-- Negative-control mismatch over a finite field index set: mismatch = Σ_i n_i². -/
theorem neg_control_mismatch_sum {ι : Type} [Fintype ι] (n : ι → ℝ)
    (t W V0 F' : ℝ) (ht : t ≠ 0) :
    (∑ i, (n i) ^ 2 / 2 - W / t ^ 2 + V0 * F')
      - (-(((∑ i, (t * n i) ^ 2) / 2 + W) / t ^ 2) + V0 * F') = ∑ i, (n i) ^ 2 := by
  have hsq : (∑ i, (t * n i) ^ 2) = t ^ 2 * ∑ i, (n i) ^ 2 := by
    calc
      (∑ i, (t * n i) ^ 2) = ∑ i, (t ^ 2 * (n i) ^ 2) := by
        refine Finset.sum_congr rfl ?_
        intro i hi
        ring
      _ = t ^ 2 * ∑ i, (n i) ^ 2 := by rw [Finset.mul_sum]
  rw [hsq]
  rw [← Finset.sum_div]
  field_simp [ht]
  ring

end AS142

/- Axiom audit (hard bar: subseteq {propext, Classical.choice, Quot.sound}). -/
#print axioms AS142.legendre_carrier
#print axioms AS142.source_identity
#print axioms AS142.neg_control_mismatch
#print axioms AS142.floor_identity
#print axioms AS142.F_at_one
#print axioms AS142.legendre_carrier_sum
#print axioms AS142.neg_control_mismatch_sum

end
