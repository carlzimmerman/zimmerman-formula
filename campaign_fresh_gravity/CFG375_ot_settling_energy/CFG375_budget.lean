import Mathlib

/-!
# CFG375 -- arithmetic certificate for the vacuum-budget inequality

The largest cell of cfg375_results.json (alt footing, M_b = 1e13 Msun, f_ret = 0.18, kinetic bound with tau = 1 Gyr) has
E = 1.3707e58 J and budget rho_Lambda c^2 V_catch = 1.3709e62 J.  With the rational enclosures E <= 1.38e58 and B >= 1.37e62,
the budget ratio epsilon = E / B is at most 1/10 (the ALLOWED threshold), and in fact at most 1/1000.
CERTIFIED: arithmetic only, at these enclosures.  NOT CERTIFIED: the physics (the transport construction, the potential,
the supply amount, or that the settling energy goes into the vacuum).  Zero sorry.
-/

theorem cfg375_eps_le_tenth (E B : ℝ) (hE : E ≤ 138 * 10 ^ 56) (hB : 137 * 10 ^ 60 ≤ B) :
    E / B ≤ 1 / 10 := by
  have hBpos : 0 < B := lt_of_lt_of_le (by norm_num) hB
  rw [div_le_iff₀ hBpos]
  nlinarith

theorem cfg375_eps_le_thousandth (E B : ℝ) (hE : E ≤ 138 * 10 ^ 56) (hB : 137 * 10 ^ 60 ≤ B) :
    E / B ≤ 1 / 1000 := by
  have hBpos : 0 < B := lt_of_lt_of_le (by norm_num) hB
  rw [div_le_iff₀ hBpos]
  nlinarith

#print axioms cfg375_eps_le_tenth
#print axioms cfg375_eps_le_thousandth
