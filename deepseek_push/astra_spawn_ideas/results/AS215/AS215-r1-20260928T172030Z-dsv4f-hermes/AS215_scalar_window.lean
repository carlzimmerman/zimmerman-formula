-- AS215 -- criterion-B characteristic ordering test, TIER-0 seed
-- Certificate 2: host-scalar block, plateau sample (FINAL_ACTION.md sec.6)
--
--   L_{2,red} = [2(2+3c2)/c2] psidot^2 - [2(2-alpha_eff)/alpha_eff] k^2 psi^2
--   c_s^2 = c2 (2 - alpha_eff) / ((2 + 3 c2) alpha_eff)
--
-- Claimed content:
--  W1  c_s^2 > 0 for c2 > 0, 0 < alpha_eff < 2  (real scalar roots -> the
--      plateau scalar block is hyperbolic w.r.t. d tau).
--  W2  c_s^2 > 1  <->  alpha_eff < c2 / (1 + 2 c2)   (superluminal healthy
--      window; the threshold denominator is (1 + 2 c2) -- a first draft used
--      (1 + c2) and the numeric/symbolic control caught it).
--  W3  consequence: any alpha_eff in (0, c2/(1+2c2)) gives a scalar channel
--      faster than c that is still forward-oriented in tau (criterion B permits
--      it; the metric-cone veto would wrongly reject it). The declared
--      superluminal sample (P2) is verified numerically in compute_as215.py.
--
-- Zero sorry. Axioms must be a subset of {propext, Classical.choice, Quot.sound}.

import Mathlib

namespace AS215

noncomputable def cs2 (c2 a : ℝ) : ℝ := c2 * (2 - a) / ((2 + 3 * c2) * a)

-- W0 : numerator identity:  (cs2 - 1) * ((2+3c2) a) = 2 c2 - 2 (1+2c2) a.
lemma scalar_speed_num (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0) (ha2 : 2 - a > 0) :
    (cs2 c2 a - 1) * ((2 + 3 * c2) * a) = 2 * c2 - 2 * (1 + 2 * c2) * a := by
  unfold cs2
  have hden : (2 + 3 * c2) * a ≠ 0 := by
    have hp : (2 + 3 * c2) * a > 0 := by positivity
    exact ne_of_gt hp
  field_simp [hden]
  ring

-- W1 : positive scalar speed (hyperbolicity: real roots at every k).
theorem scalar_speed_positive (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0) (ha2 : 2 - a > 0) :
    cs2 c2 a > 0 := by
  unfold cs2
  positivity

-- W2 : the superluminal window (correct threshold 1 + 2 c2).
theorem scalar_speed_gt_one_iff (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0)
    (ha2 : 2 - a > 0) :
    cs2 c2 a > 1 ↔ a < c2 / (1 + 2 * c2) := by
  have hden : (2 + 3 * c2) * a > 0 := by positivity
  have hdenn : 0 ≤ (2 + 3 * c2) * a := le_of_lt hden
  have h1p : 1 + 2 * c2 > 0 := by positivity
  have hnum := scalar_speed_num c2 a hc2 ha ha2
  constructor
  · intro h
    have hcs : cs2 c2 a - 1 > 0 := sub_pos.mpr h
    have hnumpos : 2 * c2 - 2 * (1 + 2 * c2) * a > 0 := by
      have h' := mul_pos hcs hden
      rwa [hnum] at h'
    have hmm2 : c2 > (1 + 2 * c2) * a := by nlinarith
    have hmm3 : a * (1 + 2 * c2) < c2 := by nlinarith
    exact (lt_div_iff₀ h1p).mpr hmm3
  · intro h
    have hmm2 : a * (1 + 2 * c2) < c2 := (lt_div_iff₀ h1p).mp h
    have hnumpos : 2 * c2 - 2 * (1 + 2 * c2) * a > 0 := by nlinarith
    have h' : (cs2 c2 a - 1) * ((2 + 3 * c2) * a) > 0 := by
      rwa [hnum]
    have hcs : cs2 c2 a - 1 > 0 := pos_of_mul_pos_left h' hdenn
    linarith

-- W3 : the threshold is strictly between 0 and c2 (window nonempty).
theorem window_nonempty (c2 : ℝ) (hc2 : c2 > 0) :
    0 < c2 / (1 + 2 * c2) ∧ c2 / (1 + 2 * c2) < 1 := by
  constructor
  · exact div_pos hc2 (by positivity)
  · have h1p : 1 + 2 * c2 > 0 := by positivity
    exact (div_lt_one h1p).mpr (by nlinarith)

-- Sanity examples (house rule: the tactic stack is verified by usage, never by
-- #check).
example (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0) (ha2 : 2 - a > 0) :
    cs2 c2 a > 1 ↔ a < c2 / (1 + 2 * c2) := by
  exact scalar_speed_gt_one_iff c2 a hc2 ha ha2

example (c2 : ℝ) (hc2 : c2 > 0) : 0 < c2 / (1 + 2 * c2) := by
  exact (window_nonempty c2 hc2).1

end AS215