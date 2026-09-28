import Mathlib

/-!
# AS020 — Scale-relation invariance under unit changes (machine certificate)

Framework base (adopted inputs, NOT derived here):
    a0  = kappa * c * sqrt(G * rho_Lambda)          (kappa = 1/2 adopted)
    rho_Lambda = 4 a0^2 / (G c^2)
    r_M  = sqrt(G*M_b/a0),  v_flat^4 = G*M_b*a0,  C = sqrt(G*M_b*a0),
    sigma^2 = C / 2
Consistent unit rescaling (task AS020): new base units (L_u m, M_u kg, T_u s):
    a0' = a0 * T_u^2 / L_u ;  G' = G * M_u * T_u^2 / L_u^3 ;
    rho' = rho * L_u^3 / M_u ;  c' = c * T_u / L_u ;  M' = M / M_u

What is certified here (real arithmetic; positivity hypotheses stated EXACTLY):

1. `pi_invariant`    — the dimensionless ratio a0/(c sqrt(G rho)) is IDENTICAL in
                       every consistently rescaled unit system.
2. `a0_relation_preserved` — the framework identity survives every consistent
                       rescaling: a0 = kappa c sqrt(G rho)  =>  a0' = kappa c' sqrt(G' rho').
3. `vflat4_covariant` — the deep-law object transforms covariantly:
                       G' M' a0' = (G M a0) * T_u^4 / L_u^4
                       (the flat speed v_flat' = v_flat * T_u/L_u).
4. `rM2_covariant`   — the MOND radius squared transforms as a length-squared:
                       G' M'/a0' = (G M/a0) / L_u^2.
5. `sigma_sq_preserved` — sigma^2 = C/2 is preserved: (sigma T_u/L_u)^2 = C'/2.
6. `hybrid_detector` — the negative control: convert LENGTHS (and masses) but
                       leave a0 at its old-unit number (T_u = 1); the ratio
                       changes by EXACTLY the length factor:
                       a0/((c/L_u) sqrt(G' rho')) = L_u * a0/(c sqrt(G rho)).
7. `footing_ratio_invariant` — the ratio of the two registered footings is
                       unit-invariant: a0_alt'/a0_can' = a0_alt/a0_can.
8. `rho_norm_covariant` — the normalization rho = 4 a0^2/(G c^2) survives:
                       rho' = 4 a0'^2/(G' c'^2).

Scope: these certify the unit algebra of the CORE scale cell only. They do NOT
derive kappa = 1/2, do not fix rho_Lambda physically, and do not transfer to
the interpolation branches Q/RAR/MU2/EXP/MONO (any statement there needs its
own proof).  `G_N`, `G_bare` and `G_cosmo` remain separate symbols; nothing
here identifies them.
-/

open Real

namespace AS020

-- transformed values under a consistent rescaling (new units of length L_u m,
-- mass M_u kg, time T_u s); division on ℝ is noncomputable in this mathlib
noncomputable def a0t (L_u T_u a0 : ℝ) : ℝ := a0 * T_u ^ 2 / L_u
noncomputable def ct (L_u T_u c : ℝ) : ℝ := c * T_u / L_u
noncomputable def Gt (L_u M_u T_u G : ℝ) : ℝ := G * M_u * T_u ^ 2 / L_u ^ 3
noncomputable def rhot (L_u M_u rho : ℝ) : ℝ := rho * L_u ^ 3 / M_u
noncomputable def Mt (M_u M : ℝ) : ℝ := M / M_u

-- |1| the dimensionless ratio is invariant under every consistent rescaling
theorem pi_invariant (L_u T_u M_u a0 c G rho : ℝ)
    (hL : 0 < L_u) (hT : 0 < T_u) (hM : 0 < M_u)
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0) :
    a0t L_u T_u a0 / (ct L_u T_u c *
      Real.sqrt (Gt L_u M_u T_u G * rhot L_u M_u rho)) = a0 / (c * Real.sqrt (G * rho)) := by
  unfold a0t ct Gt rhot
  have hprod : G * M_u * T_u ^ 2 / L_u ^ 3 * (rho * L_u ^ 3 / M_u) = (G * rho) * T_u ^ 2 := by
    field_simp [hL.ne', hM.ne']
  have hGrho : 0 ≤ G * rho := (mul_pos hG hrho).le
  have hT2 : 0 ≤ T_u ^ 2 := sq_nonneg T_u
  have hsqrtT2 : Real.sqrt (T_u ^ 2) = T_u := by
    rw [Real.sqrt_sq_eq_abs, abs_of_pos hT]
  have hsqrt : Real.sqrt (G * M_u * T_u ^ 2 / L_u ^ 3 * (rho * L_u ^ 3 / M_u))
      = Real.sqrt (G * rho) * T_u := by
    rw [hprod, Real.sqrt_mul hGrho (T_u ^ 2), hsqrtT2]
  have hsqrt_ne : Real.sqrt (G * rho) ≠ 0 := by
    rw [sqrt_ne_zero']
    exact mul_pos hG hrho
  rw [hsqrt]
  field_simp [hL.ne', hT.ne', hc, hsqrt_ne]

-- |2| the framework identity survives the rescaling
theorem a0_relation_preserved (L_u T_u M_u a0 c G rho kappa : ℝ)
    (hL : 0 < L_u) (hT : 0 < T_u) (hM : 0 < M_u)
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0)
    (hrel : a0 = kappa * c * Real.sqrt (G * rho)) :
    a0t L_u T_u a0
      = kappa * ct L_u T_u c * Real.sqrt (Gt L_u M_u T_u G * rhot L_u M_u rho) := by
  unfold a0t ct Gt rhot
  have hprod : G * M_u * T_u ^ 2 / L_u ^ 3 * (rho * L_u ^ 3 / M_u) = (G * rho) * T_u ^ 2 := by
    field_simp [hL.ne', hM.ne']
  have hGrho : 0 ≤ G * rho := (mul_pos hG hrho).le
  have hT2 : 0 ≤ T_u ^ 2 := sq_nonneg T_u
  have hsqrtT2 : Real.sqrt (T_u ^ 2) = T_u := by
    rw [Real.sqrt_sq_eq_abs, abs_of_pos hT]
  have hsqrt : Real.sqrt (G * M_u * T_u ^ 2 / L_u ^ 3 * (rho * L_u ^ 3 / M_u))
      = Real.sqrt (G * rho) * T_u := by
    rw [hprod, Real.sqrt_mul hGrho (T_u ^ 2), hsqrtT2]
  rw [hsqrt, hrel]
  field_simp [hL.ne', hT.ne']

-- |3| the deep-law product transforms covariantly (so v_flat' = v_flat * T_u/L_u)
theorem vflat4_covariant (L_u M_u T_u a0 G M : ℝ)
    (hL : L_u ≠ 0) (hT : T_u ≠ 0) (hM : M_u ≠ 0) :
    Gt L_u M_u T_u G * Mt M_u M * a0t L_u T_u a0
      = (G * M * a0) * T_u ^ 4 / L_u ^ 4 := by
  unfold Gt Mt a0t
  field_simp [hL, hT, hM]

-- |4| the MOND radius squared transforms as a length-squared (r_M' = r_M / L_u)
theorem rM2_covariant (L_u M_u T_u a0 G M : ℝ)
    (hL : L_u ≠ 0) (hT : T_u ≠ 0) (hM : M_u ≠ 0) (ha : a0 ≠ 0) :
    Gt L_u M_u T_u G * Mt M_u M / a0t L_u T_u a0 = (G * M / a0) / L_u ^ 2 := by
  unfold Gt Mt a0t
  field_simp [hL, hT, hM, ha]

-- |5| sigma^2 = C/2 is preserved under the rescaling
theorem sigma_sq_preserved (L_u T_u sigma C : ℝ)
    (hL : L_u ≠ 0) (hT : T_u ≠ 0)
    (hsig : sigma ^ 2 = C / 2) :
    (sigma * T_u / L_u) ^ 2 = (C * T_u ^ 2 / L_u ^ 2) / 2 := by
  rw [mul_div_assoc, mul_pow sigma (T_u / L_u), div_pow T_u L_u 2, hsig]
  field_simp [hL, hT]

-- |6| negative control: lengths converted, a0 left unconverted (T_u = 1):
--     the ratio changes by EXACTLY the length factor
theorem hybrid_detector (L_u M_u a0 c G rho : ℝ)
    (hL : L_u ≠ 0) (hM : M_u ≠ 0) (hc : c ≠ 0)
    (hG : 0 < G) (hrho : 0 < rho) :
    a0 / ((c / L_u) * Real.sqrt ((G * M_u / L_u ^ 3) * (rho * L_u ^ 3 / M_u)))
      = L_u * (a0 / (c * Real.sqrt (G * rho))) := by
  have hprod : G * M_u / L_u ^ 3 * (rho * L_u ^ 3 / M_u) = G * rho := by
    field_simp [hL, hM]
  have hsqrt : Real.sqrt (G * M_u / L_u ^ 3 * (rho * L_u ^ 3 / M_u))
      = Real.sqrt (G * rho) := by
    rw [hprod]
  have hsqrt_ne : Real.sqrt (G * rho) ≠ 0 := by
    rw [sqrt_ne_zero']
    exact mul_pos hG hrho
  rw [hsqrt]
  field_simp [hL, hc, hsqrt_ne]

-- |7| the footing ratio a0_alt/a0_can is unit-invariant
theorem footing_ratio_invariant (L_u T_u a0a a0b : ℝ)
    (hL : L_u ≠ 0) (hT : T_u ≠ 0) (ha : a0a ≠ 0) :
    a0t L_u T_u a0b / a0t L_u T_u a0a = a0b / a0a := by
  unfold a0t
  field_simp [hL, hT, ha]

-- |8| the normalization rho = 4 a0^2/(G c^2) survives the rescaling
theorem rho_norm_covariant (L_u M_u T_u a0 c G rho : ℝ)
    (hL : L_u ≠ 0) (hT : T_u ≠ 0) (hM : M_u ≠ 0) (hc : c ≠ 0) (hG : G ≠ 0)
    (hrho : rho = 4 * a0 ^ 2 / (G * c ^ 2)) :
    rhot L_u M_u rho = 4 * a0t L_u T_u a0 ^ 2 / (Gt L_u M_u T_u G * ct L_u T_u c ^ 2) := by
  unfold rhot a0t Gt ct
  rw [hrho]
  field_simp [hL, hT, hM, hc, hG]

#print axioms pi_invariant
#print axioms a0_relation_preserved
#print axioms vflat4_covariant
#print axioms rM2_covariant
#print axioms sigma_sq_preserved
#print axioms hybrid_detector
#print axioms footing_ratio_invariant
#print axioms rho_norm_covariant