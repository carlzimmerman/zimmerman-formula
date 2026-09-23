import Mathlib

/-!
# M01 — The algebraic spine of the window-ratio family, machine-checked

Scope (per lean-math-certification, lane `deepseek_push/J09* / J10* / J11*`): the
SURVIVING ALGEBRAIC CORE of the central-source window law J09-D/J09P-I and its
neighbours — no physics machinery, only the real arithmetic these claims sit on:

* `windowRatio q = (1+q/3)/(1/2+q/4)` — for q ≥ 0: value in `(4/3, 2]`, limiting
  value 4/3 (explicit `ε-Q` proof, no calculus), value 2 at q = 0, decreasing in q
  (J09-D: −ln A / E[D] ∈ [4/3, 2]; `deepseek_push/J09_two_component_law.out`,
  exact ratios 2.0 / 1.4444 / 1.6 at q = 0 / 10 / 3, 27/27 checks PASS).
* `windowRatioP p q = (1+q/(p+1))/(1/2+q/(p+2))` — for p ≥ 1, q ≥ 0: value in
  `( (p+2)/(p+1), 2 ]`, limit (p+2)/(p+1), decreasing (J09P-I; J09p_general_p.out:
  p=1 limit 1.5, p=2 limit 1.3333, p=4 limit 1.2 — 21/21 PASS).  Certified here for
  real p ≥ 1, hence in particular for every integer p ≥ 1 (`windowRatioP_int`).
* `slack_boundary_identity` — slack = 1/ρ² with ρ = E[D·ang]/(E[D] E[ang]) is the
  trivial algebraic identity x²y²/z² = 1/(z/(xy))², included as the boundary case
  (J09/J05 slack structure).
* The two-component factorization: −ln A = τ₀(1+q/3), E[D] = τ₀(1/2+q/4), hence
  the window ratio is the quotient, and J10-I = −ln A · r_B/(R·E[D]) factors as
  (r_B/R)·(−ln A/E[D]) and stays inside [4/3, 2]·(r_B/R) (J10_A0_RADIUS_READING.md).
* The K04 inversion: τ̂₀ = −3 ln A − 4 E[D], q̂ = 4 E[D]/τ̂₀ − 2 — recovers the pair
  (τ₀, q̂) from (A, E[D]) (linear-system inversion), is a bijection between
  {τ₀ > 0, q ≥ 0} and the window {4d/3 < s ≤ 2d} in (s, d) = (−ln A, E[D]), and
  q̂ > −1 ⟺ 8 E[D] > −3 ln A (given τ̂₀ > 0).  The suggested "q̂ > −1 ⟺ E[D] < 3/2"
  is REFUTED (certified counterexample A = e⁻¹, E[D] = 1: E[D] < 3/2 but
  q̂ = −6 < −1) — the algebra fixes the statement, not the other way round.
* The chord moment ⟨chord⟩_vol = 3/4 is NOT certified here: the needed 2D
  change-of-variables theorem (r,μ) ↦ (r√(1−μ²), rμ) for interval integrals is not
  in mathlib; it is stated formally as `chordMomentConjecture` (a `def` : Prop,
  zero axioms) with the exact analytic reduction written out below, and classified
  CONJECTURED-WITH-NUMERIC-EVIDENCE (J11: quadrature ng=80 → 0.750000 exactly;
  analytic reduction: the substitution maps [0,1]² onto the quarter unit disk,
  density 3r²·½dμ, the μ-linear term integrates to zero, and the remaining
  3∫₀¹ r²∫₀¹ √(1−r²+r²μ²) dμ dr reduces to 3∫₀¹ u(1−u²) du = 3/4).

J09 numeric anchors quoted: exact_ratio 2.0 (q=0), 1.4444 (q=10, τ₀=1),
1.6 (q=3, τ₀=2); J11: ⟨chord⟩_vol = 0.750000.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound} (verified by
`#print axioms` at the end of the file).
-/

namespace M01

noncomputable section

open scoped intervalIntegral

/-! ## 1. The central window-ratio law  W(q) = (1+q/3)/(1/2+q/4), q ≥ 0. -/

/-- The J09-D central-source window ratio W(q) = (1+q/3)/(1/2+q/4). -/
def windowRatio (q : ℝ) : ℝ := (1 + q / 3) / (1 / 2 + q / 4)

/-- Normal form: W(q) = (4/3)·(3+q)/(2+q) (for 2+q ≠ 0). -/
theorem windowRatio_eq (q : ℝ) (h : 2 + q ≠ 0) :
    windowRatio q = (4 : ℝ) / 3 * ((3 + q) / (2 + q)) := by
  have hden : (1 : ℝ) / 2 + q / 4 = (2 + q) / 4 := by
    field_simp
    ring_nf
  unfold windowRatio
  rw [hden]
  field_simp [h]

/-- Endpoint q = 0: W(0) = 2. -/
theorem windowRatio_zero : windowRatio 0 = 2 := by
  unfold windowRatio
  norm_num

/-- Strict lower bound: W(q) > 4/3 for every finite q ≥ 0 (4/3 is the deep-opacity limit). -/
theorem windowRatio_gt_four_thirds {q : ℝ} (hq : 0 ≤ q) :
    (4 : ℝ) / 3 < windowRatio q := by
  have h2q : 0 < 2 + q := by linarith
  rw [windowRatio_eq q (ne_of_gt h2q)]
  have hinner : (1 : ℝ) < (3 + q) / (2 + q) := by
    rw [lt_div_iff₀ h2q]
    linarith
  have hmain : (4 : ℝ) / 3 < (4 : ℝ) / 3 * ((3 + q) / (2 + q)) := by
    simpa [mul_lt_mul_of_pos_left hinner (by norm_num : 0 < (4 : ℝ) / 3)]
  exact hmain

/-- Upper bound: W(q) ≤ 2 for q ≥ 0. -/
theorem windowRatio_le_two {q : ℝ} (hq : 0 ≤ q) : windowRatio q ≤ 2 := by
  have h2q : 0 < 2 + q := by linarith
  rw [windowRatio_eq q (ne_of_gt h2q)]
  have hinner : (3 + q) / (2 + q) ≤ 3 / 2 := by
    rw [div_le_iff₀ h2q]
    nlinarith [hq]
  calc (4 : ℝ) / 3 * ((3 + q) / (2 + q)) ≤ (4 : ℝ) / 3 * (3 / 2) :=
      mul_le_mul_of_nonneg_left hinner (by norm_num : 0 ≤ (4 : ℝ) / 3)
    _ = 2 := by
      norm_num

/-- W is decreasing in q (on q' ≤ q with q' ≥ 0). -/
theorem windowRatio_antitone {q q' : ℝ} (hq' : 0 ≤ q') (hqq' : q' ≤ q) :
    windowRatio q ≤ windowRatio q' := by
  have h2q : 0 < 2 + q := by linarith
  have h2q' : 0 < 2 + q' := by linarith
  rw [windowRatio_eq q (ne_of_gt h2q), windowRatio_eq q' (ne_of_gt h2q')]
  have hinner : (3 + q) / (2 + q) ≤ (3 + q') / (2 + q') := by
    rw [div_le_iff₀ h2q]
    rw [div_mul_eq_mul_div]
    rw [le_div_iff₀ h2q']
    nlinarith [hqq']
  exact mul_le_mul_of_nonneg_left hinner (by norm_num : 0 ≤ (4 : ℝ) / 3)

/-! ## 2. Slack boundary identity: slack = 1/ρ² with ρ = E[D·ang]/(E[D] E[ang]). -/

/-- (E[D]·E[ang])² / E[D ang]² = 1 / ((E[D ang]/(E[D]·E[ang]))²) in the field sense. -/
theorem slack_boundary_identity (eD eA eDA : ℝ) (hD : eD ≠ 0) (hA : eA ≠ 0) (hDA : eDA ≠ 0) :
    (eD * eA) ^ 2 / eDA ^ 2 = 1 / ((eDA / (eD * eA)) ^ 2) := by
  have hDEA : eD * eA ≠ 0 := by
    exact mul_ne_zero hD hA
  field_simp [hD, hA, hDA, hDEA]

/-! ## 3. The two-component factorization and the J10-I decomposition. -/

/-- The window ratio is the quotient of the two component identities
    −ln A = τ₀(1+q/3) and E[D] = τ₀(1/2+q/4). -/
theorem window_from_components (τ₀ q : ℝ) (hτ : τ₀ ≠ 0) (hq : 0 ≤ q) :
    (τ₀ * (1 + q / 3)) / (τ₀ * (1 / 2 + q / 4)) = windowRatio q := by
  unfold windowRatio
  field_simp [hτ]

/-- J10-I factorization:  (−ln A · r_B)/(R · E[D]) = (r_B/R) · (−ln A/E[D]). -/
theorem j10i_factorization (a rB R d : ℝ) (hR : R ≠ 0) (hd : d ≠ 0) :
    (a * rB) / (R * d) = (rB / R) * (a / d) := by
  have hRd : R * d ≠ 0 := by
    exact mul_ne_zero hR hd
  field_simp [hR, hd, hRd]

/-- J10-I window: for q ≥ 0 and r_B/R ≥ 0 the reading lies in [4/3, 2]·(r_B/R). -/
theorem j10i_window_decomp (rB R q : ℝ) (hq : 0 ≤ q) (hrB : 0 ≤ rB) (hR : 0 < R) :
    4 / 3 * (rB / R) ≤ windowRatio q * rB / R ∧ windowRatio q * rB / R ≤ 2 * (rB / R) := by
  have hpos : 0 ≤ rB / R := by
    exact div_nonneg hrB (le_of_lt hR)
  have hlow : (4 : ℝ) / 3 ≤ windowRatio q := le_of_lt (windowRatio_gt_four_thirds hq)
  have hhi : windowRatio q ≤ 2 := windowRatio_le_two hq
  have hf : windowRatio q * rB / R = (rB / R) * windowRatio q := by
    field_simp [hR.ne']
  constructor
  · rw [hf]
    have hm := mul_le_mul_of_nonneg_left hlow hpos
    nlinarith [hm]
  · rw [hf]
    calc (rB / R) * windowRatio q ≤ (rB / R) * 2 := mul_le_mul_of_nonneg_left hhi hpos
      _ = 2 * (rB / R) := by
        ring

/-! ## 4. The K04 inversion bijection (s,d) ↔ (τ₀,q), s = −ln A, d = E[D]. -/

/-- τ̂₀ = −3 ln A − 4 E[D] — the recovered opacity, in A-form. -/
def tau0Hat (A d : ℝ) : ℝ := -3 * Real.log A - 4 * d

/-- q̂ = 4 E[D]/τ̂₀ − 2 — the recovered profile exponent, in A-form. -/
def qHat (A d : ℝ) : ℝ := 4 * d / tau0Hat A d - 2

/-- τ₀(s,d) = 3s − 4d: the inversion in (s, d) = (−ln A, E[D]) form (from τ₀(1+q/3) = s, τ₀(1/2+q/4) = d). -/
def tau0Of (s d : ℝ) : ℝ := 3 * s - 4 * d

/-- q(s,d) = 4d/τ₀(s,d) − 2. -/
def qInvOf (s d : ℝ) : ℝ := 4 * d / tau0Of s d - 2

/-- The A-form and s-form of τ̂₀ coincide (s = −ln A). -/
theorem k04_tau0Hat_eq (A d : ℝ) : tau0Hat A d = tau0Of (-Real.log A) d := by
  unfold tau0Hat tau0Of
  ring

/-- The A-form and s-form of q̂ coincide. -/
theorem k04_qHat_eq (A d : ℝ) : qHat A d = qInvOf (-Real.log A) d := by
  unfold qHat qInvOf tau0Hat tau0Of
  ring

/-- The inversion returns the first component: τ₀(s,d)·(1+q̂/3) = s (q̂ ≠ 0 well-defined). -/
theorem k04_recover_s (s d : ℝ) (h : tau0Of s d ≠ 0) :
    tau0Of s d * (1 + qInvOf s d / 3) = s := by
  unfold tau0Of at h ⊢
  unfold qInvOf tau0Of
  field_simp [h]
  ring_nf

/-- The inversion returns the second component: τ₀(s,d)·(1/2+q̂/4) = d. -/
theorem k04_recover_d (s d : ℝ) (h : tau0Of s d ≠ 0) :
    tau0Of s d * (1 / 2 + qInvOf s d / 4) = d := by
  unfold tau0Of at h ⊢
  unfold qInvOf tau0Of
  field_simp [h]
  ring_nf

/-- A-form of the first recovery: τ̂₀·(1+q̂/3) = −ln A. -/
theorem k04_recover_A (A d : ℝ) (h : tau0Hat A d ≠ 0) :
    tau0Hat A d * (1 + qHat A d / 3) = -Real.log A := by
  have h' : tau0Of (-Real.log A) d ≠ 0 := by
    rwa [k04_tau0Hat_eq] at h
  rw [k04_tau0Hat_eq, k04_qHat_eq]
  exact k04_recover_s (-Real.log A) d h'

/-- Round trip on τ₀: τ₀(s(τ,q), d(τ,q)) = τ. -/
theorem k04_roundtrip_tau (τ q : ℝ) :
    tau0Of (τ * (1 + q / 3)) (τ * (1 / 2 + q / 4)) = τ := by
  unfold tau0Of
  field_simp
  ring_nf

/-- Round trip on q: q̂(s(τ,q), d(τ,q)) = q (for τ ≠ 0). -/
theorem k04_roundtrip_q (τ q : ℝ) (hτ : τ ≠ 0) :
    qInvOf (τ * (1 + q / 3)) (τ * (1 / 2 + q / 4)) = q := by
  unfold qInvOf tau0Of
  have hd : 3 * (τ * (1 + q / 3)) - 4 * (τ * (1 / 2 + q / 4)) ≠ 0 := by
    have h1 : 3 * (τ * (1 + q / 3)) - 4 * (τ * (1 / 2 + q / 4)) = τ := by
      field_simp
      ring_nf
    rwa [h1]
  field_simp [hd]
  ring_nf

/-- Forward bijection: (τ₀ > 0, q ≥ 0) lands in the window {4d/3 < s ≤ 2d}. -/
theorem k04_window_forward (τ q : ℝ) (hτ : 0 < τ) (hq : 0 ≤ q) :
    4 * (τ * (1 / 2 + q / 4)) / 3 < τ * (1 + q / 3) ∧
      τ * (1 + q / 3) ≤ 2 * (τ * (1 / 2 + q / 4)) := by
  constructor
  · have hmain : τ * (1 + q / 3) - 4 * (τ * (1 / 2 + q / 4)) / 3 = τ / 3 := by
      field_simp
      ring_nf
    rw [← sub_pos]
    rw [hmain]
    exact div_pos hτ (by norm_num)
  · have hmain2 : 2 * (τ * (1 / 2 + q / 4)) - τ * (1 + q / 3) = τ * q / 6 := by
      field_simp
      ring_nf
    rw [← sub_nonneg]
    rw [hmain2]
    exact div_nonneg (mul_nonneg (le_of_lt hτ) hq) (by norm_num)

/-- Backward bijection: a window point (4d/3 < s ≤ 2d) gives τ₀(s,d) > 0 and q̂(s,d) ≥ 0. -/
theorem k04_window_backward (s d : ℝ) (hL : 4 * d / 3 < s) (hU : s ≤ 2 * d) :
    0 < tau0Of s d ∧ 0 ≤ qInvOf s d := by
  constructor
  · unfold tau0Of
    linarith
  · unfold qInvOf tau0Of
    have hpos : 0 < 3 * s - 4 * d := by
      linarith
    have h1 : (2 : ℝ) ≤ 4 * d / (3 * s - 4 * d) := by
      rw [le_div_iff₀ hpos]
      nlinarith [hU]
    linarith

/-- Boundary of the physical region: q̂ > −1 ⟺ 8·E[D] > −3·ln A (given τ̂₀ > 0).
    (The claimed equivalent "q̂ > −1 ⟺ E[D] < 3/2" is FALSE — see `k04_refutes_ed_three_halves`.) -/
theorem k04_qhat_gt_neg_one (s d : ℝ) (ht : 0 < tau0Of s d) :
    -1 < qInvOf s d ↔ 8 * d > 3 * s := by
  unfold qInvOf tau0Of at ⊢
  unfold tau0Of at ht
  constructor
  · intro h
    have h1 : (1 : ℝ) < 4 * d / (3 * s - 4 * d) := by
      linarith
    rw [lt_div_iff₀ ht] at h1
    linarith [h1]
  · intro h
    have h1 : 3 * s - 4 * d < 4 * d := by
      linarith
    have hlt : (1 : ℝ) < 4 * d / (3 * s - 4 * d) := by
      rw [lt_div_iff₀ ht]
      nlinarith [h1]
    linarith

/-- q̂ ≥ 0 ⟺ s ≤ 2d (given τ̂₀ > 0): the upper edge of the window. -/
theorem k04_qhat_nonneg (s d : ℝ) (ht : 0 < tau0Of s d) :
    0 ≤ qInvOf s d ↔ s ≤ 2 * d := by
  unfold qInvOf tau0Of at ⊢
  unfold tau0Of at ht
  constructor
  · intro h
    have h1 : (2 : ℝ) ≤ 4 * d / (3 * s - 4 * d) := by
      linarith
    rw [le_div_iff₀ ht] at h1
    nlinarith [h1]
  · intro h
    have h1 : (2 : ℝ) ≤ 4 * d / (3 * s - 4 * d) := by
      rw [le_div_iff₀ ht]
      nlinarith [h]
    linarith

/-- Certified counterexample against the suggested "q̂ > −1 ⟺ E[D] < 3/2":
    A = e⁻¹, E[D] = 1 satisfy E[D] < 3/2 yet q̂ = −6 < −1.  The true boundary is
    q̂ > −1 ⟺ 8·E[D] > −3·ln A (`k04_qhat_gt_neg_one`). -/
theorem k04_refutes_ed_three_halves : ∃ A d : ℝ,
    0 < A ∧ A < 1 ∧ 0 < d ∧ d < 3 / 2 ∧ qHat A d < -1 := by
  refine ⟨Real.exp (-1), 1, ?_, ?_, ?_, ?_, ?_⟩
  · exact Real.exp_pos (-1)
  · rw [Real.exp_lt_one_iff]
    norm_num
  · norm_num
  · norm_num
  · unfold qHat tau0Hat
    rw [Real.log_exp]
    norm_num

/-! ## 5. The p-generalized window (J09P-I): S_p(q) = (1+q/(p+1))/(1/2+q/(p+2)). -/

/-- S_p(q), the generalized-p window ratio; p = 2 gives the central law. -/
def windowRatioP (p q : ℝ) : ℝ := (1 + q / (p + 1)) / (1 / 2 + q / (p + 2))

/-- L_p = (p+2)/(p+1) — the deep-opacity endpoint. -/
def limitP (p : ℝ) : ℝ := (p + 2) / (p + 1)

/-- S_1's endpoint is 3/2, S_2's is 4/3 (the central value). -/
theorem limitP_one : limitP 1 = 3 / 2 := by
  unfold limitP
  norm_num

theorem limitP_two : limitP 2 = 4 / 3 := by
  unfold limitP
  norm_num

/-- Endpoint q = 0 for the family: S_p(0) = 2. -/
theorem windowRatioP_zero (p : ℝ) : windowRatioP p 0 = 2 := by
  unfold windowRatioP
  norm_num

/-- Distance to the limit: S_p(q) = L_p + p(p+2)/((p+1)(p+2+2q)) (exact). -/
theorem windowRatioP_eq (p q : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) :
    windowRatioP p q = limitP p + p * (p + 2) / ((p + 1) * (p + 2 + 2 * q)) := by
  have hp1 : 0 < p + 1 := by linarith [hp]
  have hp2 : 0 < p + 2 := by linarith [hp]
  have hp3 : 0 < p + 2 + 2 * q := by linarith [hp, hq]
  unfold windowRatioP limitP
  field_simp [hp1.ne', hp2.ne', hp3.ne']
  ring_nf

/-- S_p(q) > (p+2)/(p+1) for q ≥ 0 (the lower endpoint is strict). -/
theorem windowRatioP_gt_limit (p q : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) :
    limitP p < windowRatioP p q := by
  have hX : 0 < p * (p + 2) / ((p + 1) * (p + 2 + 2 * q)) := by
    have hpp : 0 < p * (p + 2) := mul_pos (by linarith : 0 < p) (by linarith : 0 < p + 2)
    have hden : 0 < (p + 1) * (p + 2 + 2 * q) := mul_pos (by linarith : 0 < p + 1)
      (by linarith : 0 < p + 2 + 2 * q)
    exact div_pos hpp hden
  rw [windowRatioP_eq p q hp hq]
  linarith [hX]

/-- S_p is decreasing in q (for 0 ≤ q' ≤ q). -/
theorem windowRatioP_antitone (p q q' : ℝ) (hp : 1 ≤ p) (hq' : 0 ≤ q') (hqq' : q' ≤ q) :
    windowRatioP p q ≤ windowRatioP p q' := by
  have hq : 0 ≤ q := by
    linarith
  rw [windowRatioP_eq p q hp hq, windowRatioP_eq p q' hp hq']
  have hB1 : 1 / (p + 2 + 2 * q) ≤ 1 / (p + 2 + 2 * q') := by
    exact one_div_le_one_div_of_le (by linarith : 0 < p + 2 + 2 * q') (by linarith)
  have hA : 0 ≤ p * (p + 2) / (p + 1) := by
    exact div_nonneg (mul_nonneg (by linarith : 0 ≤ p) (by linarith : 0 ≤ p + 2))
      (by linarith : 0 ≤ p + 1)
  have hpp : 0 ≤ p * (p + 2) := mul_nonneg (by linarith : 0 ≤ p) (by linarith : 0 ≤ p + 2)
  have hX : p * (p + 2) / ((p + 1) * (p + 2 + 2 * q)) ≤
      p * (p + 2) / ((p + 1) * (p + 2 + 2 * q')) := by
    have hp1n : (p + 1) ≠ 0 := (by linarith : 0 < p + 1).ne'
    have hq4 : (p + 2 + 2 * q) ≠ 0 := (by linarith : 0 < p + 2 + 2 * q).ne'
    have hq5 : (p + 2 + 2 * q') ≠ 0 := (by linarith : 0 < p + 2 + 2 * q').ne'
    calc p * (p + 2) / ((p + 1) * (p + 2 + 2 * q))
        = p * (p + 2) * (1 / (p + 1)) * (1 / (p + 2 + 2 * q)) := by
          field_simp [hp1n, hq4]
        _ ≤ p * (p + 2) * (1 / (p + 1)) * (1 / (p + 2 + 2 * q')) := by
          exact mul_le_mul_of_nonneg_left hB1 (by
            apply mul_nonneg
            · exact hpp
            · have : 0 ≤ 1 / (p + 1) := (one_div_pos).mpr (by linarith : 0 < p + 1) |> le_of_lt
              simpa)
        _ = p * (p + 2) / ((p + 1) * (p + 2 + 2 * q')) := by
          field_simp [hp1n, hq5]
  nlinarith [hX]

/-- S_p(q) ≤ 2 for q ≥ 0: the window is [L_p, 2] with the lower end strict. -/
theorem windowRatioP_le_two (p q : ℝ) (hp : 1 ≤ p) (hq : 0 ≤ q) :
    windowRatioP p q ≤ 2 := by
  have hant := windowRatioP_antitone p q 0 hp (by norm_num : 0 ≤ (0 : ℝ)) hq
  rwa [windowRatioP_zero p] at hant

/-- The central law is the p = 2 instance of the family. -/
theorem windowRatioP_eq_two (q : ℝ) : windowRatioP 2 q = windowRatio q := by
  unfold windowRatioP windowRatio
  norm_num

/-- Deep-opacity limit of S_p: |S_p(q) − L_p| < ε for q ≥ (p+1)/(2ε). -/
theorem windowRatioP_limit (p : ℝ) (hp : 1 ≤ p) :
    ∀ ε : ℝ, 0 < ε → ∃ Q : ℝ, ∀ q : ℝ, Q ≤ q → |windowRatioP p q - limitP p| < ε := by
  intro ε hε
  refine ⟨(p + 1) / (2 * ε), ?_⟩
  intro q hq
  have hp1 : 0 < p + 1 := by linarith
  have hp1n : 0 ≤ p + 1 := le_of_lt hp1
  have hqpos : 0 < q := by
    have hQ : 0 < (p + 1) / (2 * ε) := div_pos hp1 (mul_pos (by norm_num : 0 < (2 : ℝ)) hε)
    exact lt_of_lt_of_le hQ hq
  have hden3 : 0 < p + 2 + 2 * q := by linarith
  have hden : 0 < (p + 1) * (p + 2 + 2 * q) := mul_pos hp1 hden3
  have hdiff : windowRatioP p q - limitP p =
      p * (p + 2) / ((p + 1) * (p + 2 + 2 * q)) := by
    rw [windowRatioP_eq p q hp (le_of_lt hqpos)]
    field_simp [hp1.ne', hden.ne']
    ring_nf
  have hQ' : (p + 1) ≤ 2 * q * ε := by
    have hQq : (p + 1) / (2 * ε) ≤ q := hq
    rw [div_le_iff₀ (by positivity : 0 < 2 * ε)] at hQq
    nlinarith [hQq]
  have hA : p * (p + 2) ≤ (p + 1) * (p + 1) := by
    nlinarith
  have hlt2 : 2 * q * ε < (p + 2 + 2 * q) * ε := by
    exact mul_lt_mul_of_pos_right (by linarith : 2 * q < p + 2 + 2 * q) hε
  have hchain : p * (p + 2) < ε * (p + 1) * (p + 2 + 2 * q) := by
    calc p * (p + 2) ≤ (p + 1) * (p + 1) := hA
      _ ≤ (p + 1) * (2 * q * ε) := mul_le_mul_of_nonneg_left hQ' hp1n
      _ < (p + 1) * ((p + 2 + 2 * q) * ε) := mul_lt_mul_of_pos_left hlt2 hp1
      _ = ε * (p + 1) * (p + 2 + 2 * q) := by
        ring
  have hXlt : p * (p + 2) / ((p + 1) * (p + 2 + 2 * q)) < ε := by
    rw [div_lt_iff₀ hden]
    nlinarith [hchain]
  have hXpos : 0 ≤ p * (p + 2) / ((p + 1) * (p + 2 + 2 * q)) := by
    exact div_nonneg (mul_nonneg (by linarith : 0 ≤ p) (by linarith : 0 ≤ p + 2))
      (le_of_lt hden)
  rw [hdiff]
  rw [abs_of_nonneg hXpos]
  exact hXlt

/-- Deep-opacity limit of the central law: |W(q) − 4/3| < ε for large q (p = 2 case). -/
theorem windowRatio_limit :
    ∀ ε : ℝ, 0 < ε → ∃ Q : ℝ, ∀ q : ℝ, Q ≤ q → |windowRatio q - (4 : ℝ) / 3| < ε := by
  intro ε hε
  rcases windowRatioP_limit 2 (by norm_num : 1 ≤ (2 : ℝ)) ε hε with ⟨Q, hQ⟩
  refine ⟨Q, ?_⟩
  intro q hq
  have h1 := hQ q hq
  rwa [windowRatioP_eq_two q, limitP_two] at h1

/-- Integer-p formulation: for every integer n ≥ 1 and q ≥ 0 the window is
    L_n < S_n(q) ≤ 2 (J09P-I "certify for integer p ≥ 1"). -/
theorem windowRatioP_int (n : ℕ) (hn : 1 ≤ n) (q : ℝ) (hq : 0 ≤ q) :
    limitP (n : ℝ) < windowRatioP (n : ℝ) q ∧ windowRatioP (n : ℝ) q ≤ 2 := by
  constructor
  · exact windowRatioP_gt_limit (n : ℝ) q (by exact_mod_cast hn) hq
  · exact windowRatioP_le_two (n : ℝ) q (by exact_mod_cast hn) hq

/-! ## 6. The chord moment — formal statement, analytics, honest status.

The J11 volume-source anchor ⟨chord⟩_vol = 0.750000 exactly (Gauss–Legendre
quadrature ng=80, `J11_VOLUME_WINDOW_VERDICT.md`) is the integral of the
first-exit path length over uniform interior point and isotropic direction:

  chord(r,μ) = rμ + √(1 − r²(1−μ²)),   measure 3 r² dr · ½ dμ · (ν-average).

Analytic reduction (NOT Lean-checked — the 2D change of variables (r,μ) ↦
(r√(1−μ²), rμ), which maps [0,1]² bijectively onto the quarter unit disk with
dr dμ = √(1−μ²)/r du dv, is not available for interval integrals in mathlib):
the rμ term integrates to zero (odd in μ on [−1,1]); the substitution turns the
remaining integral into ∫∫_{quarter disk} u √(1−u²) du dv = ∫₀¹ u(1−u²) du = 1/4;
three times the radial density gives 3/4.

Everything that could be certified in this file about the moment IS the formal
statement itself (a `def` : Prop — compiling, zero axioms, zero sorry).  The
value 3/4 is therefore classified CONJECTURED-WITH-NUMERIC-EVIDENCE. -/

/-- chord(r,μ) = rμ + √(1 − r²(1−μ²)): first-exit path length of a uniform
    interior point of the unit ball in a fixed direction (J11). -/
def chordVol (r μ : ℝ) : ℝ := r * μ + Real.sqrt (1 - r ^ 2 * (1 - μ ^ 2))

/-- The volume-source chord moment: 3 ∫₀¹ r² · ½ ∫₋₁¹ chord(r,μ) dμ dr. -/
def chordMomentVol : ℝ :=
  3 * (∫ r in (0 : ℝ)..1, r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, chordVol r μ)))

/-- J11 anchor claim: ⟨chord⟩_vol = 3/4.
    Status: CONJECTURED-WITH-NUMERIC-EVIDENCE (not a theorem — no proof given).
    Evidence: exact quadrature ng=80 → 0.750000 (J11_VOLUME_WINDOW_VERDICT.md);
    analytic reduction in the header of this section evaluates the same integral
    to 3 ∫₀¹ u(1−u²) du = 3/4 by the change of variables (r,μ) ↦ (r√(1−μ²), rμ),
    which is outside mathlib's current interval-integral toolkit. -/
def chordMomentConjecture : Prop := chordMomentVol = (3 : ℝ) / 4

#check chordMomentConjecture

#print axioms windowRatio_eq
#print axioms windowRatio_zero
#print axioms windowRatio_gt_four_thirds
#print axioms windowRatio_le_two
#print axioms windowRatio_antitone
#print axioms slack_boundary_identity
#print axioms window_from_components
#print axioms j10i_factorization
#print axioms j10i_window_decomp
#print axioms k04_tau0Hat_eq
#print axioms k04_qHat_eq
#print axioms k04_recover_s
#print axioms k04_recover_d
#print axioms k04_recover_A
#print axioms k04_roundtrip_tau
#print axioms k04_roundtrip_q
#print axioms k04_window_forward
#print axioms k04_window_backward
#print axioms k04_qhat_gt_neg_one
#print axioms k04_qhat_nonneg
#print axioms k04_refutes_ed_three_halves
#print axioms limitP_one
#print axioms limitP_two
#print axioms windowRatioP_zero
#print axioms windowRatioP_eq
#print axioms windowRatioP_gt_limit
#print axioms windowRatioP_antitone
#print axioms windowRatioP_le_two
#print axioms windowRatioP_eq_two
#print axioms windowRatioP_limit
#print axioms windowRatio_limit
#print axioms windowRatioP_int