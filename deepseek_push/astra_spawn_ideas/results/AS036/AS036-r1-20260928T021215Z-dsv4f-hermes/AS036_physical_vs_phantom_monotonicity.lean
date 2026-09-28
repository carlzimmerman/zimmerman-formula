import Mathlib
import Mathlib.Tactic

/-
  AS036 -- Physical monotonicity versus phantom monotonicity (Lean 4 certificate).

  Framework (dimensionless, a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED):
    B = g_N > 0,  y = B/a0 > 0,  g = total radial acceleration,  x = g/a0 = y + h(y).
    Physical monotonicity : dg/dB = 1 + h'(y) > 0   (invertibility of the force law).
    Phantom monotonicity  : h'(y) > 0               (monotone extra acceleration).

  Formalized content:
    A  Q branch: dg/dB = (2y+1)/(2 sqrt(y^2+y)) and dg/dB > 1 for every y > 0
       (hence dg/dB > 0 and h'_Q = dg/dB - 1 > 0: Q is BOTH physically and
       phantom monotone).
    B  Class-level implication: h' > 0  ==>  1 + h' > 1 > 0.  A kernel in the
       declared class x = y + h(y) cannot be phantom-monotone and
       physical-nonmonotone (impossibility direction).
    C  MONO branch: the floor phi(y) = delta*h_p/(y+y_p) with delta, h_p, y+y_p > 0
       is strictly positive; h'_mono = max(h'_RAR, phi) >= phi > 0 (phantom
       monotone by construction) and dg/dB = 1 + h'_mono > 1 (physical).
    D  RAR branch (closed-form h'_RAR(s) = (2(e^s-1) - s e^s)/(2(e^s-1)^2),
       s = sqrt y): 1 + h'_RAR > 0 for every s > 0  [exact proof:
       2(e^s - 1) > s since e^s >= 1 + s].  Hence RAR is PHYSICALLY monotone on
       all of y > 0 even though its phantom is NOT monotone (h' < 0 for y > y_p,
       transcendental root s_p = 1.5936242600400..., bracketed numerically).
       The sign of h' is equivalent to 2(e^s-1) - s e^s; the exact
       threshold-equivalence is certified.
    E  MU2 branch: dy/dx = 1 - (1+x/2)^(-2) + x(1+x/2)^(-3) > 0 for all x > 0
       (physical monotone), while the phantom h = x(1+x/2)^(-2) has
       h'(x) = (1-x/2)(1+x/2)^(-3), sign x < 2: phantom monotone iff x < 2
       (y < 3/2).  Physical monotone + phantom non-monotone example: x > 2.
    F  EXP branch (historical): dy/dx = 1 - e^(-x)(1-x) > 0 for all x > 0
       (physical monotone); phantom h = x e^(-x), h' = (1-x)e^(-x): sign x < 1.
    G  Q phantom bounded: 0 <= h_Q(y) = sqrt(y^2+y) - y < 1/2 for y >= 0.

  Note: monotonicity statements are dimensionless; both a0 footings
  (9.3619e-11 and 1.1279e-10 m/s^2) apply unchanged.
-/

noncomputable section
open Real

/- A1: derivative identity of the Q branch: dg/dB = 1 + h'_Q. -/
theorem q_dgdB_formula (y : ℝ) :
    1 + ((2 * y + 1) / (2 * Real.sqrt (y ^ 2 + y)) - 1)
      = (2 * y + 1) / (2 * Real.sqrt (y ^ 2 + y)) := by
  ring

/- A2: Q branch: dg/dB > 1 for every y > 0. -/
theorem q_dgdB_gt_one (y : ℝ) (hy : 0 < y) :
    1 < (2 * y + 1) / (2 * Real.sqrt (y ^ 2 + y)) := by
  have harg : 0 < y ^ 2 + y := by nlinarith [sq_pos_of_pos hy]
  have hsp : 0 < Real.sqrt (y ^ 2 + y) := Real.sqrt_pos.2 harg
  have hden : 0 < 2 * Real.sqrt (y ^ 2 + y) := by positivity
  rw [lt_div_iff₀ hden]
  have hsq : (Real.sqrt (y ^ 2 + y)) ^ 2 = y ^ 2 + y := Real.sq_sqrt (le_of_lt harg)
  have hlt : (2 * Real.sqrt (y ^ 2 + y)) ^ 2 < (2 * y + 1) ^ 2 := by
    nlinarith [hsq]
  have habs : |2 * Real.sqrt (y ^ 2 + y)| < |2 * y + 1| := (sq_lt_sq).1 hlt
  have hb : 0 < 2 * y + 1 := by nlinarith
  have hlt2 : 2 * Real.sqrt (y ^ 2 + y) < 2 * y + 1 := by
    rwa [abs_of_nonneg (by positivity : 0 ≤ 2 * Real.sqrt (y ^ 2 + y)), abs_of_pos hb] at habs
  simpa using hlt2

/- A3: Q branch: dg/dB > 0 (trivially from > 1). -/
theorem q_dgdB_pos (y : ℝ) (hy : 0 < y) :
    0 < (2 * y + 1) / (2 * Real.sqrt (y ^ 2 + y)) := by
  linarith [q_dgdB_gt_one y hy]

/- A4: Q branch: phantom derivative positive: h'_Q(y) = dg/dB - 1 > 0. -/
theorem q_hprime_pos (y : ℝ) (hy : 0 < y) :
    0 < (2 * y + 1) / (2 * Real.sqrt (y ^ 2 + y)) - 1 := by
  linarith [q_dgdB_gt_one y hy]

/- B1: phantom monotonicity implies physical monotonicity (strict version). -/
theorem phantom_implies_physical (h : ℝ) (hh : 0 < h) : 1 < 1 + h := by
  linarith

/- B2: weak phantom monotonicity still implies physical monotonicity. -/
theorem phantom_implies_physical_weak (h : ℝ) (hh : 0 ≤ h) : 0 < 1 + h := by
  linarith

/- C1: MONO floor positivity: phi(y) = delta*h_p/(y+y_p) > 0. -/
theorem mono_floor_pos {hp δ : ℝ} (hhp : 0 < hp) (hδ : 0 < δ)
    {yp y : ℝ} (hsum : 0 < y + yp) : 0 < δ * hp / (y + yp) := by
  exact div_pos (mul_pos hδ hhp) hsum

/- C2: MONO phantom monotone by construction: max(h'_RAR, phi) >= phi > 0. -/
theorem mono_hprime_pos {hR φ : ℝ} (hφ : 0 < φ) : 0 < max hR φ := by
  exact lt_of_lt_of_le hφ (le_max_right hR φ)

/- C3: MONO physical monotone with margin: 1 + h'_mono > 1. -/
theorem mono_physical_margin {hR φ : ℝ} (hφ : 0 < φ) : 1 < 1 + max hR φ := by
  have hm : 0 < max hR φ := mono_hprime_pos hφ
  linarith

/- D0: auxiliary exponential fact: e^s >= 1 + s. -/
theorem exp_ge_add_one (s : ℝ) : 1 + s ≤ Real.exp s := by
  have h1 : s + 1 ≤ Real.exp s := Real.add_one_le_exp s
  linarith

/- D1: 2(e^s - 1) > s for s > 0 (exact RAR physical-monotonicity inequality). -/
theorem two_exp_sub_one_gt_s (s : ℝ) (hs : 0 < s) : s < 2 * (Real.exp s - 1) := by
  have h1 : 1 + s ≤ Real.exp s := exp_ge_add_one s
  nlinarith

/- D2: RAR phantom derivative closed form (dimensionless, s = sqrt y):
   h'_RAR(s) = (2(e^s-1) - s e^s) / (2 (e^s-1)^2). -/
def hRARp (s : ℝ) : ℝ := (2 * (Real.exp s - 1) - s * Real.exp s) / (2 * (Real.exp s - 1) ^ 2)

/- D3: RAR physical monotonicity: 1 + h'_RAR(s) > 0 for every s > 0. -/
theorem rar_one_plus_hprime_pos (s : ℝ) (hs : 0 < s) : 0 < 1 + hRARp s := by
  unfold hRARp
  have hE : 1 < Real.exp s := by
    have h1 : 1 + s ≤ Real.exp s := exp_ge_add_one s
    nlinarith
  have hE1 : 0 < Real.exp s - 1 := by linarith
  have hden : 0 < 2 * (Real.exp s - 1) ^ 2 := by positivity
  have hmain : 0 < 2 * (Real.exp s - 1) - s := by linarith [two_exp_sub_one_gt_s s hs]
  have hsum : 1 + (2 * (Real.exp s - 1) - s * Real.exp s) / (2 * (Real.exp s - 1) ^ 2)
      = (Real.exp s * (2 * (Real.exp s - 1) - s)) / (2 * (Real.exp s - 1) ^ 2) := by
    field_simp [ne_of_gt hE1]
    ring
  rw [hsum]
  have hnum : 0 < Real.exp s * (2 * (Real.exp s - 1) - s) := mul_pos (Real.exp_pos s) hmain
  exact div_pos hnum hden

/- D4: RAR phantom sign equivalence:
   0 < h'_RAR(s)  <->  0 < 2(e^s-1) - s e^s   (s > 0; i.e. 2(e^s-1) > s e^s).
   The root s_p of 2(e^s-1) = s e^s is transcendental (s_p = 1.5936242600...,
   y_p = s_p^2 = 2.5396382821..., bracketed numerically, not formalized). -/
theorem rar_hprime_pos_iff (s : ℝ) (hs : 0 < s) :
    0 < hRARp s ↔ 0 < 2 * (Real.exp s - 1) - s * Real.exp s := by
  unfold hRARp
  have hE : 1 < Real.exp s := by
    have h1 : 1 + s ≤ Real.exp s := exp_ge_add_one s
    nlinarith
  have hE1 : 0 < Real.exp s - 1 := by linarith
  have hden : 0 < 2 * (Real.exp s - 1) ^ 2 := by positivity
  constructor
  · intro h
    have hd : 0 < (2 * (Real.exp s - 1) - s * Real.exp s) / (2 * (Real.exp s - 1) ^ 2) := h
    have hq : 0 < ((2 * (Real.exp s - 1) - s * Real.exp s) / (2 * (Real.exp s - 1) ^ 2))
        * (2 * (Real.exp s - 1) ^ 2) := mul_pos hd hden
    have hsim : ((2 * (Real.exp s - 1) - s * Real.exp s) / (2 * (Real.exp s - 1) ^ 2))
        * (2 * (Real.exp s - 1) ^ 2) = 2 * (Real.exp s - 1) - s * Real.exp s := by
      field_simp [ne_of_gt hden]
    rwa [hsim] at hq
  · intro hgt
    exact div_pos hgt hden

/- E1: MU2 physical monotonicity: dy/dx = 1 - (1+x/2)^(-2) + x(1+x/2)^(-3) > 0. -/
theorem mu2_dydx_pos (x : ℝ) (hx : 0 < x) :
    0 < 1 - (1 + x / 2) ^ (-2 : ℤ) + x * (1 + x / 2) ^ (-3 : ℤ) := by
  have hu : 0 < 1 + x / 2 := by positivity
  have hden : 0 < (1 + x / 2) ^ 3 := by positivity
  have hprod : (1 - (1 + x / 2) ^ (-2 : ℤ) + x * (1 + x / 2) ^ (-3 : ℤ))
      * (1 + x / 2) ^ 3 = (1 + x / 2) ^ 3 - (1 + x / 2) + x := by
    field_simp [ne_of_gt hu]
  have hfac : (1 + x / 2) ^ 3 - (1 + x / 2) + x = (1 + x / 2) * (x / 2) * (2 + x / 2) + x := by
    ring
  have hposf : 0 < (1 + x / 2) ^ 3 - (1 + x / 2) + x := by
    rw [hfac]
    positivity
  have hmul : 0 < (1 - (1 + x / 2) ^ (-2 : ℤ) + x * (1 + x / 2) ^ (-3 : ℤ))
      * (1 + x / 2) ^ 3 := by
    rw [hprod]
    exact hposf
  have hq : 0 < ((1 - (1 + x / 2) ^ (-2 : ℤ) + x * (1 + x / 2) ^ (-3 : ℤ)) * (1 + x / 2) ^ 3)
      / (1 + x / 2) ^ 3 := div_pos hmul hden
  have hsim2 : ((1 - (1 + x / 2) ^ (-2 : ℤ) + x * (1 + x / 2) ^ (-3 : ℤ)) * (1 + x / 2) ^ 3)
      / (1 + x / 2) ^ 3 = 1 - (1 + x / 2) ^ (-2 : ℤ) + x * (1 + x / 2) ^ (-3 : ℤ) := by
    field_simp [ne_of_gt hden]
  rwa [hsim2] at hq

/- E2: MU2 phantom sign (declared branch x = g/a0 > 0):
   0 < h'(x) = (1-x/2)(1+x/2)^(-3)  <->  x < 2. -/
theorem mu2_hprime_pos_iff (x : ℝ) (hx : 0 < x) :
    0 < (1 - x / 2) * (1 + x / 2) ^ (-3 : ℤ) ↔ x < 2 := by
  have hu : 0 < 1 + x / 2 := by positivity
  have hb : 0 < (1 + x / 2) ^ 3 := by positivity
  have heq : (1 - x / 2) * (1 + x / 2) ^ (-3 : ℤ) = (1 - x / 2) / (1 + x / 2) ^ 3 := by
    field_simp [ne_of_gt hu]
  rw [heq]
  constructor
  · intro h
    have hm : 0 < (1 - x / 2) / (1 + x / 2) ^ 3 * (1 + x / 2) ^ 3 := mul_pos h hb
    have h2x : 2 + x ≠ 0 := by nlinarith [hx]
    have hsim : (1 - x / 2) / (1 + x / 2) ^ 3 * (1 + x / 2) ^ 3 = 1 - x / 2 := by
      field_simp [ne_of_gt hb, h2x]
    have hgt : 0 < 1 - x / 2 := by
      simpa [hsim] using hm
    linarith
  · intro hx2
    exact div_pos (by linarith) hb

/- E3: MU2 phantom root (declared branch x > 0): h'(x) = 0  <->  x = 2; y(2) = 3/2. -/
theorem mu2_hprime_zero_iff (x : ℝ) (hx : 0 < x) :
    (1 - x / 2) * (1 + x / 2) ^ (-3 : ℤ) = 0 ↔ x = 2 := by
  have hc : (1 + x / 2) ^ (-3 : ℤ) ≠ 0 := by
    have hu2 : 0 < 1 + x / 2 := by positivity
    rw [zpow_neg (1 + x / 2) (3 : ℤ)]
    exact inv_ne_zero (pow_ne_zero 3 (ne_of_gt hu2))
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h1 | h2
    · linarith
    · exfalso
      exact hc h2
  · intro hx2
    rw [hx2]
    norm_num

/- F1: EXP physical monotonicity: dy/dx = 1 - e^(-x)(1-x) > 0 for x > 0. -/
theorem exp_dydx_pos (x : ℝ) (hx : 0 < x) : 0 < 1 - Real.exp (-x) * (1 - x) := by
  by_cases hx1 : 1 ≤ x
  · have hle : Real.exp (-x) * (1 - x) ≤ 0 := by
      have h1 : 0 ≤ Real.exp (-x) := le_of_lt (Real.exp_pos (-x))
      have h2 : 1 - x ≤ 0 := by linarith
      nlinarith
    linarith
  · have hlt : x < 1 := lt_of_not_ge hx1
    have hlm : Real.exp (-x) ≤ 1 := by
      have hne : -x ≤ 0 := by linarith
      have he : Real.exp (-x) ≤ Real.exp 0 := (Real.exp_le_exp).2 hne
      rwa [Real.exp_zero] at he
    have hge0 : 0 ≤ 1 - x := by linarith
    have hprod : Real.exp (-x) * (1 - x) ≤ 1 - x := by
      simpa using (mul_le_mul_of_nonneg_right hlm hge0)
    linarith

/- F2: EXP phantom sign: 0 < h'(x) = (1-x)e^(-x)  <->  x < 1. -/
theorem exp_hprime_pos_iff (x : ℝ) : 0 < (1 - x) * Real.exp (-x) ↔ x < 1 := by
  have he : 0 < Real.exp (-x) := Real.exp_pos (-x)
  constructor
  · intro h
    have hq : 0 < (1 - x) * Real.exp (-x) / Real.exp (-x) := div_pos h he
    have hsim : (1 - x) * Real.exp (-x) / Real.exp (-x) = 1 - x := by
      field_simp [ne_of_gt he]
    have hgt : 0 < 1 - x := by
      simpa [hsim] using hq
    linarith
  · intro hx1
    exact mul_pos (by linarith) he

/- G1: Q phantom nonneg: h_Q(y) = sqrt(y^2+y) - y >= 0 for y >= 0. -/
theorem q_h_Q_nonneg (y : ℝ) (hy : 0 ≤ y) : 0 ≤ Real.sqrt (y ^ 2 + y) - y := by
  have harg : 0 ≤ y ^ 2 + y := by nlinarith [sq_nonneg y, hy]
  have hsq : (Real.sqrt (y ^ 2 + y)) ^ 2 = y ^ 2 + y := Real.sq_sqrt harg
  have hcmp : y ^ 2 ≤ (Real.sqrt (y ^ 2 + y)) ^ 2 := by
    nlinarith [hsq, hy]
  have habs : |y| ≤ |Real.sqrt (y ^ 2 + y)| := (sq_le_sq).1 hcmp
  have hle : y ≤ Real.sqrt (y ^ 2 + y) := by
    rwa [abs_of_nonneg hy, abs_of_nonneg (Real.sqrt_nonneg (y ^ 2 + y))] at habs
  linarith

/- G2: Q phantom bounded: h_Q(y) < 1/2 for y >= 0. -/
theorem q_h_Q_lt_half (y : ℝ) (hy : 0 ≤ y) : Real.sqrt (y ^ 2 + y) - y < 1 / 2 := by
  have harg : 0 ≤ y ^ 2 + y := by nlinarith [sq_nonneg y, hy]
  have hsq : (Real.sqrt (y ^ 2 + y)) ^ 2 = y ^ 2 + y := Real.sq_sqrt harg
  have hcmp : (Real.sqrt (y ^ 2 + y)) ^ 2 < (y + 1 / 2) ^ 2 := by
    nlinarith [hsq]
  have habs : |Real.sqrt (y ^ 2 + y)| < |y + 1 / 2| := (sq_lt_sq).1 hcmp
  have hlt : Real.sqrt (y ^ 2 + y) < y + 1 / 2 := by
    have hb : 0 < y + 1 / 2 := by positivity
    rwa [abs_of_nonneg (Real.sqrt_nonneg (y ^ 2 + y)), abs_of_pos hb] at habs
  linarith

end
