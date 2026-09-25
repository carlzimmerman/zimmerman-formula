import Mathlib

/-!
# L341 — the FRW gate for C-H/K: algebraic certificates

SCOPE. Lean certifies the algebra behind `real_research/g03_audit_2026/L341_chk_frw_gate.py`: the CMC stiffness of
C-H/K's foliation in the scalar block, the suppression bound of the quartic K-floor, and the identity that makes
the K-floor the record's dS-Unruh floor.  The growth integrations, SPARC and KiDS numbers are not certified here.

* `cmc_newtonian`: over ℂ (the frequency-domain block), with C = 0 and alpha_c = 0 the block's lapse, U and beta equations force the
  expansion perturbation K to vanish for ANY time-derivative symbol D (static or not): the foliation is CMC.
* `cmc_static`: for a static source (D = 0), any C and alpha_c, the beta equation forces K = 0.
* `quartic_floor_suppression`: with s_eff^4 = s^4 + kappa^4 the effective MOND susceptibility factor
  (s/s_eff)^2 is at most s^2/kappa^2 -- the linear response on FRW is suppressed when s << kappa.
* `floor_is_dS_unruh`: with a0 = c H_Lambda / Z, kappa = c H/a0 = Z H/H_Lambda.
-/

theorem cmc_newtonian {k eps D R psi phi U K : ℂ} (hk : k ≠ 0) (heps : eps ≠ 0)
    (hU : 4 * k ^ 2 * (U - phi) = 0)                                   -- U equation at C = 0
    (hphi : -4 * k ^ 2 * psi - 4 * k ^ 2 * (U - phi) - R = 0)          -- lapse equation at alpha_c = 0
    (hbeta : 4 * k ^ 2 * (D * psi) - 2 * eps * k ^ 2 * K + D * R = 0) :  -- beta equation, K = 3 D psi - k^2 beta
    K = 0 := by
  have hk2 : (k ^ 2 : ℂ) ≠ 0 := pow_ne_zero 2 hk
  have h : (2 * eps * k ^ 2) * K = 0 := by linear_combination -hbeta - D * hphi - D * hU
  rcases mul_eq_zero.mp h with h | h
  · exact absurd h (mul_ne_zero (mul_ne_zero two_ne_zero heps) hk2)
  · exact h

theorem cmc_static {k eps K : ℂ} (hk : k ≠ 0) (heps : eps ≠ 0)
    (hbeta : -2 * eps * k ^ 2 * K = 0) : K = 0 := by
  have hne : (-2 * eps * k ^ 2 : ℂ) ≠ 0 :=
    mul_ne_zero (mul_ne_zero (neg_ne_zero.mpr two_ne_zero) heps) (pow_ne_zero 2 hk)
  rcases mul_eq_zero.mp hbeta with h | h
  · exact absurd h hne
  · exact h

theorem quartic_floor_suppression {s se kap : ℝ} (hs : 0 ≤ s) (hk : 0 < kap) (hse : 0 < se)
    (hdef : se ^ 4 = s ^ 4 + kap ^ 4) : (s / se) ^ 2 ≤ s ^ 2 / kap ^ 2 := by
  have hge : kap ≤ se := by
    by_contra h
    push Not at h
    have : se ^ 4 < kap ^ 4 := by
      have := pow_lt_pow_left₀ h hse.le (by norm_num : (4 : ℕ) ≠ 0); simpa using this
    nlinarith [pow_nonneg hs 4]
  rw [div_pow]
  apply div_le_div_of_nonneg_left (by positivity) (by positivity)
  exact pow_le_pow_left₀ hk.le hge 2

theorem floor_is_dS_unruh {c H HL Z a0 : ℝ} (hc : 0 < c) (hHL : 0 < HL) (hZ : 0 < Z)
    (ha0 : a0 = c * HL / Z) : c * H / a0 = Z * H / HL := by
  rw [ha0]; field_simp

#print axioms cmc_newtonian
#print axioms cmc_static
#print axioms quartic_floor_suppression
#print axioms floor_is_dS_unruh
