import Mathlib

/-!
# RH13-L -- THE DOUBLED COMPLETION: TWO REFLECTION AXES, NO NEW ZERO CONTROL (Lean-certified, zero sorry)
========================================================================================================

CONTEXT (from RH05L's certified ladder): the ladder rung l > 1 has Mellin transform
    B_l(s) := B(s, l-s) = Γ(s)·Γ(l−s)/Γ(l)   (Mellin transform of (1+u)^(−l), 0 < Re s < l),
reflection axis l/2.  This file attaches the ladder's beta to the completed zeta
    Ξ(s) = s(s−1)π^(−s/2)Γ(s/2)ζ(s),  Ξ(s) = Ξ(1−s)   [classical functional equation, NOT re-proved here]
and certifies the ALGEBRAIC CORE of the DOUBLED completion
    P_l(s) := Ξ(s)·B_l(s).

THE TWO AXES (both certified below as clean identities, generic in the completion h):

  AXIS A (s → 1−s):   P_l(s) = P_l(1−s) · R_l(s),   R_l(s) := B_l(s)/B_l(1−s)
                       = Γ(s)Γ(l−s)/(Γ(1−s)Γ(l−1+s))   [the Γ(l) factors cancel — gamma_cancellation_ratio]
      Certified in the sharpest honest form (doubled_symmetry_axis12): for ANY h with h(1−s)=h(s),
      the identity holds with h in place of Ξ — the Ξ/functional-equation factor CANCELS identically.
      Hence the identity carries zero information about h's zeros.

  AXIS B (s → l−s):   P_l(s)·h(l−s) = P_l(l−s)·h(s)   [doubled_symmetry_axis_ls — the B factor cancels;
      holds for ANY h, no functional equation needed at all; uses the certified beta symmetry
      B_l(s) = B_l(l−s), the Mellin kernel's own reflection].

  INVOLUTION:  R_l(s)·R_l(1−s) = 1  [doubled_ratio_involution — the doubled symmetry is an involution].
  The two maps coincide exactly at the ladder edge l = 1 (axes_coincide_at_edge).

THE EULER-PRODUCT SIDE (part 1 of the delegation), with exact-vs-numeric honesty:
  * EXACT and certified here: at σ = 1 the FINITE log-product identity over the primes
    {2,3,5,7,11,13}  —  ln(∏(1−1/p)) = Σ ln(1−1/p)  —  plus the exact rational value
    ∏(1−1/p) = 192/1001  (log_product_six_primes, thirteen_prime_product_exact).
    This is the exact-finite content behind the "ln of the partition function" reading of
    the Euler product; the full infinite statement is classical (Re s > 1) and NOT re-certified.
  * NUMERIC only (RH13_doubled_completion.py, 30 digits): at σ = 1/2 the partial sums
    Σ_{p≤x} ln(1−p^{−1/2}) DIVERGE to −∞ (Euler product converges only for Re s > 1), and
    ζ(1/2) = −1.46035… < 0 so ln ζ(1/2) is not real; at σ = 1 the partial sums diverge to −∞
    (Mertens) matching the pole of ζ at 1 — the literal "= ln(1/ζ(1))" is a divergence
    statement, not an equality of real numbers; at σ = 3/2 (the l = 3 LADDER AXIS inside the
    convergence region) the Euler product converges and matches ln ζ(3/2) (residual ~5.7e-5,
    agreeing with the predicted tail ~6.4e-5).

THE HONEST DISPATCH (part 3): does the doubled symmetry constrain the zeros of P_l?  NO.
  * P_l's zeros are exactly Ξ's zeros (B_l is zero-free away from its poles at s ∈ ℤ≤0 ∪ l+ℤ≥0,
    which B_l ADDS as poles, not zeros) — classical facts, cited, not re-proved.
  * The only zero consequence of AXIS A — the pairing ρ ↔ 1−ρ — is the CLASSICAL functional-
    equation pairing already present in Ξ (R_l(ρ) ≠ 0 away from the beta poles).  Nothing new.
  * The reflection class alone cannot place zeros on the axis: RH05L certified this for
    (s−2)(s+1); this file extends the principle INTO the doubled class itself:
    h0(s) = s(1−s) − 1/8 is 1−s-symmetric (h0_axis12_symmetry) with roots
    a0 = (1+√(1/2))/2 ≈ 0.8536 and b0 = (1−√(1/2))/2 ≈ 0.1464, both OFF the critical line
    (h0_root_a0, h0_root_b0, doubled_class_off_axis_roots), and the completed product
    P_{h0,l}(a0) = P_{h0,l}(b0) = 0 for every l (doubled_class_zeros) while satisfying the
    doubled symmetry (doubled_symmetry_holds_for_h0).  TWO reflection axes ⇒ NO zero control.
  * K1 (pre-registered): doubled-symmetry identities fail numerically → algebra error.
    NOT triggered: python run shows residuals ≤ 4e-31 at 30 digits (10 s-values × 3 rungs).
  * K2 (pre-registered): the honest conclusion is that NO new zero control follows.  CONFIRMED.

WHAT IS CERTIFIED HERE (all theorems below, exit 0, zero sorry):
  (1) beta_axis_symmetry          : B_l(s) = B_l(l−s)                     [kernel's own reflection]
  (2) gamma_cancellation_ratio    : B_l(s)/B_l(1−s) = Γ(s)Γ(l−s)/(Γ(1−s)Γ(l−1+s))  [Γ(l) cancels]
  (3) doubled_symmetry_axis12     : P(s)·B_l(1−s) = P(1−s)·B_l(s) for ANY h, h(1−s)=h(s)
  (4) doubled_symmetry_axis_ls    : P(s)·h(l−s) = P(l−s)·h(s) for ANY h
  (5) doubled_ratio_involution    : R_l(s)·R_l(1−s) = 1
  (6) axes_coincide_at_edge       : l = 1 ⇒ the two axes coincide
  (7) h0 machinery                : h0 symmetric; roots a0, b0 OFF the axis; P_{h0,l} zero there;
                                    the doubled class contains off-axis zeros
  (8) log_product_six_primes      : ln ∏_{p∈{2,3,5,7,11,13}}(1−1/p) = Σ ln(1−1/p)   (σ = 1, EXACT)
  (9) thirteen_prime_product_exact: ∏(1−1/p) = 192/1001                            (σ = 1, EXACT)

NOT certified here (classical mathematics, cited): Ξ(s)=Ξ(1−s) via the theta transformation;
Euler product for Re s > 1; zero-freeness Re s > 1 and off Re s = 1; Mertens; RH (open).
NO RH claim, in whole or in part.
-/

noncomputable section

open scoped Real

-- ============================================================
-- THE OBJECTS
-- ============================================================

-- the ladder beta: B_l(s) := Γ(s)·Γ(l−s)/Γ(l)  (Mellin transform of (1+u)^(−l))
noncomputable def lB (l s : ℝ) : ℝ :=
  Real.Gamma s * Real.Gamma (l - s) / Real.Gamma l

-- the completed product with generic completion factor h (h = Ξ = completed zeta in the application)
noncomputable def lP (h : ℝ → ℝ) (l s : ℝ) : ℝ :=
  h s * lB l s

-- the two off-axis root representatives of h0(s) = s(1−s) − 1/8
noncomputable def a0 : ℝ := (1 + Real.sqrt (1 / 2)) / 2
noncomputable def b0 : ℝ := (1 - Real.sqrt (1 / 2)) / 2

-- ============================================================
-- (1) THE BETA'S OWN REFLECTION: B_l(s) = B_l(l−s)
-- ============================================================
theorem beta_axis_symmetry (l s : ℝ) : lB l s = lB l (l - s) := by
  unfold lB
  have h : l - (l - s) = s := by ring
  rw [h]
  ring

-- ============================================================
-- (2) THE GAMMA-CANCELLATION RATIO (the certified algebraic core):
--     B_l(s)/B_l(1−s) = Γ(s)Γ(l−s) / (Γ(1−s)Γ(l−1+s))   [the Γ(l) denominators cancel]
--     Meromorphic identity: holds wherever the displayed Γ-products are nonzero.
-- ============================================================
theorem gamma_cancellation_ratio (l s : ℝ) (hl : Real.Gamma l ≠ 0) :
    lB l s / lB l (1 - s)
      = Real.Gamma s * Real.Gamma (l - s) / (Real.Gamma (1 - s) * Real.Gamma (l - 1 + s)) := by
  unfold lB
  have hw : l - (1 - s) = l - 1 + s := by ring
  rw [hw]
  field_simp [hl]

-- ============================================================
-- (3) AXIS A (doubled symmetry, s → 1−s):  for ANY completion h with h(1−s) = h(s),
--     P_l(s)·B_l(1−s) = P_l(1−s)·B_l(s)  — the h-factor cancels: the identity is a tautology
--     of the construction and carries zero information about h's zeros.
-- ============================================================
theorem doubled_symmetry_axis12 (h : ℝ → ℝ) (l s : ℝ) (hfe : h (1 - s) = h s) :
    lP h l s * lB l (1 - s) = lP h l (1 - s) * lB l s := by
  unfold lP
  rw [hfe]
  ring

-- ============================================================
-- (4) AXIS B (doubled symmetry, s → l−s):  for ANY h (no functional equation needed at all),
--     P_l(s)·h(l−s) = P_l(l−s)·h(s)  — the B factor cancels identically (beta symmetry).
-- ============================================================
theorem doubled_symmetry_axis_ls (h : ℝ → ℝ) (l s : ℝ) :
    lP h l s * h (l - s) = lP h l (l - s) * h s := by
  unfold lP
  rw [beta_axis_symmetry l s]
  ring

-- ============================================================
-- (5) THE INVOLUTION:  R_l(s)·R_l(1−s) = 1  (the doubled symmetry applied twice is the identity)
-- ============================================================
theorem doubled_ratio_involution (l s : ℝ) (ha : lB l s ≠ 0) (hb : lB l (1 - s) ≠ 0) :
    (lB l s / lB l (1 - s)) * (lB l (1 - s) / lB l s) = 1 := by
  field_simp [ha, hb]

-- ============================================================
-- (6) AT THE LADDER EDGE the two axes coincide:  l = 1 ⇒ 1−s = l−s
-- ============================================================
theorem axes_coincide_at_edge (l s : ℝ) (hl : l = 1) : 1 - s = l - s := by
  rw [hl]

-- ============================================================
-- (7) THE HONEST COUNTEREXAMPLE, INSIDE THE DOUBLED CLASS:
--     h0(s) = s(1−s) − 1/8 is 1−s-symmetric with roots a0, b0 OFF the critical line;
--     the completed product P_{h0,l} vanishes there for every l yet satisfies AXIS A.
-- ============================================================
noncomputable def h0 (s : ℝ) : ℝ := s * (1 - s) - (1 : ℝ) / 8

theorem h0_axis12_symmetry (s : ℝ) : h0 (1 - s) = h0 s := by
  unfold h0
  ring

-- the square of the sqrt constant: (√(1/2))² = 1/2
private theorem sqrt_half_sq : (Real.sqrt (1 / 2)) ^ 2 = 1 / 2 :=
  Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1 / 2)

theorem h0_root_a0 : h0 a0 = 0 := by
  unfold h0 a0
  have hsq : (Real.sqrt (1 / 2)) ^ 2 = 1 / 2 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1 / 2)
  calc
    ((1 + Real.sqrt (1 / 2)) / 2) * (1 - (1 + Real.sqrt (1 / 2)) / 2) - 1 / 8
        = ((1 + Real.sqrt (1 / 2)) * (1 - Real.sqrt (1 / 2))) / 4 - 1 / 8 := by
          have hc : 1 - (1 + Real.sqrt (1 / 2)) / 2 = (1 - Real.sqrt (1 / 2)) / 2 := by
            field_simp
            ring
          rw [hc]
          field_simp
          ring
    _ = (1 - (Real.sqrt (1 / 2)) ^ 2) / 4 - 1 / 8 := by ring
    _ = (1 - 1 / 2) / 4 - 1 / 8 := by rw [hsq]
    _ = 0 := by norm_num

theorem h0_root_b0 : h0 b0 = 0 := by
  unfold h0 b0
  have hsq : (Real.sqrt (1 / 2)) ^ 2 = 1 / 2 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1 / 2)
  calc
    ((1 - Real.sqrt (1 / 2)) / 2) * (1 - (1 - Real.sqrt (1 / 2)) / 2) - 1 / 8
        = ((1 - Real.sqrt (1 / 2)) * (1 + Real.sqrt (1 / 2))) / 4 - 1 / 8 := by
          have hc : 1 - (1 - Real.sqrt (1 / 2)) / 2 = (1 + Real.sqrt (1 / 2)) / 2 := by
            field_simp
            ring
          rw [hc]
          field_simp
          ring
    _ = (1 - (Real.sqrt (1 / 2)) ^ 2) / 4 - 1 / 8 := by ring
    _ = (1 - 1 / 2) / 4 - 1 / 8 := by rw [hsq]
    _ = 0 := by norm_num

-- the representative a0 lies strictly on the positive side of the critical line: a0 ≠ 1/2
theorem a0_ne_half : a0 ≠ (1 : ℝ) / 2 := by
  unfold a0
  by_contra h
  have hc : Real.sqrt (1 / 2) = 0 := by linarith
  have hcp : 0 < Real.sqrt (1 / 2) := (Real.sqrt_pos).2 (by norm_num : (0 : ℝ) < 1 / 2)
  linarith

theorem b0_ne_half : b0 ≠ (1 : ℝ) / 2 := by
  unfold b0
  by_contra h
  have hc : Real.sqrt (1 / 2) = 0 := by linarith
  have hcp : 0 < Real.sqrt (1 / 2) := (Real.sqrt_pos).2 (by norm_num : (0 : ℝ) < 1 / 2)
  linarith

-- P_{h0,l} vanishes at the off-axis roots (0 · B_l = 0), for EVERY ladder rung l
theorem doubled_class_zero_a0 (l : ℝ) : lP h0 l a0 = 0 := by
  rw [lP, h0_root_a0]
  simp

theorem doubled_class_zero_b0 (l : ℝ) : lP h0 l b0 = 0 := by
  rw [lP, h0_root_b0]
  simp

-- the counterexample member satisfies the doubled symmetry (AXIS A) ...
theorem doubled_symmetry_holds_for_h0 (l s : ℝ) :
    lP h0 l s * lB l (1 - s) = lP h0 l (1 - s) * lB l s :=
  doubled_symmetry_axis12 h0 l s (h0_axis12_symmetry s)

-- ... yet it has zeros OFF the critical line: the doubled class does not constrain zero location.
theorem doubled_class_off_axis_zeros (l : ℝ) :
    lP h0 l a0 = 0 ∧ lP h0 l b0 = 0 ∧ a0 ≠ (1 : ℝ) / 2 ∧ b0 ≠ (1 : ℝ) / 2 := by
  constructor
  · exact doubled_class_zero_a0 l
  · constructor
    · exact doubled_class_zero_b0 l
    · constructor
      · exact a0_ne_half
      · exact b0_ne_half

-- ============================================================
-- (8) EULER PRODUCT SIDE, sigma = 1, EXACT AND FINITE:
--     ln ∏_{p ∈ {2,3,5,7,11,13}} (1 − 1/p)  =  Σ_p ln(1 − 1/p)
-- ============================================================
theorem log_product_six_primes :
    Real.log ((1 - 1 / 2) * (1 - 1 / 3) * (1 - 1 / 5) * (1 - 1 / 7) * (1 - 1 / 11) * (1 - 1 / 13))
      = Real.log (1 - 1 / 2) + Real.log (1 - 1 / 3) + Real.log (1 - 1 / 5) + Real.log (1 - 1 / 7)
        + Real.log (1 - 1 / 11) + Real.log (1 - 1 / 13) := by
  have hp2 : (0 : ℝ) < 1 - 1 / 2 := by norm_num
  have hp3 : (0 : ℝ) < 1 - 1 / 3 := by norm_num
  have hp5 : (0 : ℝ) < 1 - 1 / 5 := by norm_num
  have hp7 : (0 : ℝ) < 1 - 1 / 7 := by norm_num
  have hp11 : (0 : ℝ) < 1 - 1 / 11 := by norm_num
  have hp13 : (0 : ℝ) < 1 - 1 / 13 := by norm_num
  have h12 : (0 : ℝ) < (1 - 1 / 2) * (1 - 1 / 3) := mul_pos hp2 hp3
  have h123 : (0 : ℝ) < (1 - 1 / 2) * (1 - 1 / 3) * (1 - 1 / 5) := mul_pos h12 hp5
  have h1234 : (0 : ℝ) < (1 - 1 / 2) * (1 - 1 / 3) * (1 - 1 / 5) * (1 - 1 / 7) := mul_pos h123 hp7
  have h12345 : (0 : ℝ) < (1 - 1 / 2) * (1 - 1 / 3) * (1 - 1 / 5) * (1 - 1 / 7) * (1 - 1 / 11) :=
    mul_pos h1234 hp11
  rw [Real.log_mul (ne_of_gt h12345) (ne_of_gt hp13)]
  rw [Real.log_mul (ne_of_gt h1234) (ne_of_gt hp11)]
  rw [Real.log_mul (ne_of_gt h123) (ne_of_gt hp7)]
  rw [Real.log_mul (ne_of_gt h12) (ne_of_gt hp5)]
  rw [Real.log_mul (ne_of_gt hp2) (ne_of_gt hp3)]

-- ============================================================
-- (9) the exact rational value of the finite Euler product at sigma = 1
-- ============================================================
theorem thirteen_prime_product_exact :
    (1 - 1 / 2) * (1 - 1 / 3) * (1 - 1 / 5) * (1 - 1 / 7) * (1 - 1 / 11) * (1 - 1 / 13)
      = (192 : ℝ) / 1001 := by
  norm_num

end