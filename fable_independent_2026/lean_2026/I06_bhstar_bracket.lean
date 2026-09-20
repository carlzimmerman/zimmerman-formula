import Mathlib

/-!
# I06 — Wave N: the certified two-sided bracket on the global GR ceiling

SCOPE (per lean-math-certification): Lean certifies the ALGEBRA of the two-scale
discrimination. The chain (each link provenanced):

  T4 envelope (I01 gap_lower/gap_upper):   beta/6 <= gap <= beta/3
  Quartic band (I05):                      beta <= U and (sqrt(sqrt 2))^-1 * U <= beta,
                                           with U = sqrt(M_E/M)
  Absorbed criterion (Chandrasekhar 1965): instability iff gap < kappa_GR * alpha
  Compactness (M1):                        alpha = a5 * S, S = sqrt(M/M0)

STABILITY at M requires kappa*alpha <= gap. Two certified consequences, stated in the
S,U atoms (the S-atom firewall: no Real.sqrt inside any proof; the quartic band enters
ONLY as hypotheses):

  stable_band   : stability  =>  9*k^2*a5^2*S^2 <= U^2
      (i.e. 9 k^2 a5^2 M^2 <= M_E M0, i.e. M <= sqrt(M_E M0)/(3 k a5) = 1.23e8 Msun at
       the n=3 coefficient — ABOVE this edge the configuration is UNSTABLE, guaranteed)
  unstable_band : instability =>  (sqrt 2)^-1 * U^2 <= 36*k^2*a5^2*S^2
      (i.e. M >= (sqrt(sqrt 2))^-1 * sqrt(M_E M0)/(6 k a5) = 5.18e7 Msun — BELOW this
       mass the global mode CANNOT go unstable)

THE GLOBAL CEILING IS BRACKETED [5.18e7, 1.23e8] Msun (n=3); the literature PULSATIONAL
ceiling (Saio+24, accreting MESA structures) is [1e5, 1e6] — 1.7-3.1 dex below. The LRD
engines (10^3.4-4.3) sit below both. All numbers Python-verified in
`bhstar_n1_ceiling_bracket.py` (5/5). Zero `sorry`; axioms ⊆ {propext,
Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **N (the stability band).** If the configuration is stable (kappa*alpha <= gap),
then 9 k^2 a5^2 S^2 <= U^2, i.e. M <= sqrt(M_E M0)/(3 k a5). -/
theorem stable_band {κ a5 β gap α S U : ℝ}
    (hk : 0 < κ) (ha5 : 0 < a5) (hS : 0 < S) (hU : 0 < U)
    (hbeta_ub : β ≤ U)                 -- I05.quartic_beta_upper
    (hgx : gap ≤ β / 3)                -- T4 gap_upper
    (hstab : κ * α ≤ gap)              -- the absorbed criterion (stability)
    (halpha : α = a5 * S) :
    9 * κ ^ 2 * a5 ^ 2 * S ^ 2 ≤ U ^ 2 := by
  rw [halpha, ← mul_assoc] at hstab
  have h1 : κ * a5 * S ≤ U / 3 :=
    le_trans hstab (le_trans hgx (div_le_div_of_nonneg_right hbeta_ub
      (by norm_num : (0:ℝ) ≤ 3)))
  have h2 : κ * a5 * S * 3 ≤ U := by
    have h3 := mul_le_mul_of_nonneg_right h1 (by norm_num : (0:ℝ) ≤ 3)
    rw [div_mul_cancel₀ U (by norm_num : (3:ℝ) ≠ 0)] at h3
    exact h3
  have h6 : 9 * κ ^ 2 * a5 ^ 2 * S ^ 2 = (κ * a5 * S * 3) ^ 2 := by ring
  rw [h6]
  exact pow_le_pow_left₀ (by positivity) h2 2

/-- **N (the instability band).** If the configuration is unstable (gap <= kappa*alpha),
then (sqrt 2)^-1 U^2 <= 36 k^2 a5^2 S^2, i.e. M >= (sqrt(sqrt 2))^-1 sqrt(M_E M0)/(6 k a5).
Below that edge the global mode cannot go unstable. -/
theorem unstable_band {κ a5 β gap α S U : ℝ}
    (hk : 0 < κ) (ha5 : 0 < a5) (hS : 0 < S) (hU : 0 < U)
    (hbeta_lb : (Real.sqrt (Real.sqrt 2))⁻¹ * U ≤ β)   -- I05.quartic_beta4_lower
    (hgx : β / 6 ≤ gap)                                 -- T4 gap_lower
    (hinst : gap ≤ κ * α)                               -- the criterion (unstable side)
    (halpha : α = a5 * S) :
    (Real.sqrt 2)⁻¹ * U ^ 2 ≤ 36 * κ ^ 2 * a5 ^ 2 * S ^ 2 := by
  rw [halpha, ← mul_assoc] at hinst
  have h1 : (Real.sqrt (Real.sqrt 2))⁻¹ * U / 6 ≤ κ * a5 * S := by
    have h2 : (Real.sqrt (Real.sqrt 2))⁻¹ * U / 6 ≤ β / 6 :=
      div_le_div_of_nonneg_right hbeta_lb (by norm_num : (0:ℝ) ≤ 6)
    calc (Real.sqrt (Real.sqrt 2))⁻¹ * U / 6 ≤ β / 6 := h2
      _ ≤ gap := hgx
      _ ≤ κ * a5 * S := hinst
  have h2 : (Real.sqrt (Real.sqrt 2))⁻¹ * U ≤ κ * a5 * S * 6 := by
    have h3 := mul_le_mul_of_nonneg_right h1 (by norm_num : (0:ℝ) ≤ 6)
    rw [div_mul_cancel₀ _ (by norm_num : (6:ℝ) ≠ 0)] at h3
    exact h3
  have h4 : ((Real.sqrt (Real.sqrt 2))⁻¹ * U) ^ 2 ≤ (κ * a5 * S * 6) ^ 2 :=
    pow_le_pow_left₀ (by positivity) h2 2
  have h5 : ((Real.sqrt (Real.sqrt 2))⁻¹ * U) ^ 2 = (Real.sqrt 2)⁻¹ * U ^ 2 := by
    rw [mul_pow, inv_pow, Real.sq_sqrt (by positivity : (0:ℝ) ≤ Real.sqrt 2)]
  have h7 : (κ * a5 * S * 6) ^ 2 = 36 * κ ^ 2 * a5 ^ 2 * S ^ 2 := by ring
  rw [← h5, ← h7]
  exact h4

end

#print axioms stable_band
#print axioms unstable_band