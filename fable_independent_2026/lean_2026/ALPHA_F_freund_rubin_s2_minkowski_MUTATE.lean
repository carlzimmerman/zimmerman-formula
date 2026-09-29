import Mathlib

/-!
# M6-I -- lane F, family B (Freund-Rubin M4 x S^2 with integer flux N): the radion potential's Minkowski point, DERIVED from V

Source: `real_research/alpha_principle_2026/F_kk_stabilization/f2_flux_freund_rubin.py`, part B2 (lines 62-84, sympy):
  U(R) = 4 pi R^2 (Lambda/kappa^2 - 1/(kappa^2 R^2) + N^2/(8 g^2 R^4)),  V_E(R) = (R0/R)^4 U(R),
  Minkowski point (V = 0, V' = 0):  R*^2 = N^2 kappa^2/(4 g^2), Lambda_6 = 1/(2 R*^2)   [checks B2a, B2b],
  V_E''(R*) = 64 pi g^2/(N^2 kappa^4) > 0                                             [check B2c],
  and the window in y = R^2 (units R_M = 1): W = Lambda/y - 1/y^2 + 1/(2 y^3), extremum at Lambda = 2/y - 3/(2 y^2),
  Lambda_c = 1/2 at y = 1, merger value 2/3 at y = 3/2                                 [check B2d].
Corpus check (2026-09-29): `ALPHA_F_Q3_flux_couplings.lean` (item A) takes "the Minkowski point R^2 = N^2 kappa^2/(4 g^2)" as a
printed PREMISE and certifies the coupling algebra downstream of it; it does NOT derive the Minkowski point from V.  Nothing in
the corpus derives V'(R*) = 0 = V(R*) => (R*, Lambda_6), or V''(R*), or the Lambda(y) window (`git grep -n -i -e "64 pi" -e "3/2"
-e Minkowski -- '*.lean'` on ALPHA_F_Q3 only).  New.

CERTIFIED (real analysis, exact; R0, kappa, g, N > 0):
  * `Vfr_eq`, `Vfr_hasDerivAt`, `Vfr1_hasDerivAt` : V_E = A/R^2 - B/R^4 + C/R^6 (A = 4 pi R0^4 Lambda/kappa^2, B = 4 pi R0^4/kappa^2,
                          C = 4 pi R0^4 N^2/(8 g^2)) and its first two derivatives in closed form;
  * `minkowski_point`   : V_E(R0) = 0 and V_E'(R0) = 0  <->  R0^2 = N^2 kappa^2/(4 g^2) and Lambda = 1/(2 R0^2);
  * `V2_minkowski`      : there V_E''(R0) = 64 pi g^2/(N^2 kappa^4), which is > 0 (radion stable, this direction only);
  * `W_hasDerivAt`, `Lambda_of_y`, `Lambda_c`, `Lambda_max` : W'(y) = -Lambda/y^2 + 2/y^3 - 3/(2 y^4) (HasDerivAt), and W'(y) = 0  <->  Lambda = 2/y - 3/(2 y^2) (y > 0); Lambda(1) = 1/2, Lambda(3/2) = 2/3
                          and Lambda(y) <= 2/3 for every y > 0 with equality only at y = 3/2 (the merger value).
NOT CERTIFIED: the reduction from the 6D Einstein-Maxwell-Lambda action to U(R) (the lane compares it with the D-dimensional
Einstein equations in B1); stability in directions other than the radion (the lane says "NOT tested"); that a minimum exists for
Lambda < 2/3 (only the extremum curve is certified here); the 3e-119 tuning; the coupling relations (see ALPHA_F_Q3, which takes
this file's conclusions as its premises).  alpha stays a free modulus (chat); kappa here is the 6D gravitational coupling,
unrelated to the framework's kappa = 1/2 (FITTED).
-/

noncomputable section
namespace M6I

open Real

/-- derivative of K / R^n -/
lemma hd_div_pow (K : ℝ) (n : ℕ) {R : ℝ} (hR : R ≠ 0) :
    HasDerivAt (fun R : ℝ => K / R ^ n) (-(K * ((n : ℝ) * R ^ (n - 1))) / (R ^ n) ^ 2) R := by
  have h := (hasDerivAt_const R K).fun_div (hasDerivAt_pow n R) (pow_ne_zero n hR)
  refine h.congr_deriv ?_
  ring

/-- the Einstein-frame radion potential of the n = 2 Freund-Rubin compactification -/
def Vfr (Lam kap g N R0 R : ℝ) : ℝ :=
  (R0 / R) ^ 4 * (4 * π * R ^ 2 * (Lam / kap ^ 2 - 1 / (kap ^ 2 * R ^ 2) + N ^ 2 / (8 * g ^ 2 * R ^ 4)))

/-- closed form of the first derivative -/
def Vfr1 (Lam kap g N R0 R : ℝ) : ℝ :=
  -2 * (4 * π * R0 ^ 4 * Lam / kap ^ 2) / R ^ 3 + 4 * (4 * π * R0 ^ 4 / kap ^ 2) / R ^ 5
    - 6 * (4 * π * R0 ^ 4 * N ^ 2 / (8 * g ^ 2)) / R ^ 7

theorem Vfr_eq (Lam kap g N R0 : ℝ) (hk : kap ≠ 0) (hg : g ≠ 0) {R : ℝ} (hR : R ≠ 0) :
    Vfr Lam kap g N R0 R = (4 * π * R0 ^ 4 * Lam / kap ^ 2) / R ^ 2 - (4 * π * R0 ^ 4 / kap ^ 2) / R ^ 4
      + (4 * π * R0 ^ 4 * N ^ 2 / (4 * g ^ 2)) / R ^ 6 := by
  unfold Vfr
  field_simp

theorem Vfr_hasDerivAt (Lam kap g N R0 : ℝ) (hk : kap ≠ 0) (hg : g ≠ 0) {R : ℝ} (hR : R ≠ 0) :
    HasDerivAt (Vfr Lam kap g N R0) (Vfr1 Lam kap g N R0 R) R := by
  have hA := hd_div_pow (4 * π * R0 ^ 4 * Lam / kap ^ 2) 2 hR
  have hB := hd_div_pow (4 * π * R0 ^ 4 / kap ^ 2) 4 hR
  have hC := hd_div_pow (4 * π * R0 ^ 4 * N ^ 2 / (8 * g ^ 2)) 6 hR
  have h1 := (hA.sub hB).add hC
  have h2 : HasDerivAt (Vfr Lam kap g N R0)
      (-((4 * π * R0 ^ 4 * Lam / kap ^ 2) * ((2 : ℕ) * R ^ (2 - 1))) / (R ^ 2) ^ 2
        - (-((4 * π * R0 ^ 4 / kap ^ 2) * ((4 : ℕ) * R ^ (4 - 1))) / (R ^ 4) ^ 2)
        + (-((4 * π * R0 ^ 4 * N ^ 2 / (8 * g ^ 2)) * ((6 : ℕ) * R ^ (6 - 1))) / (R ^ 6) ^ 2)) R := by
    refine h1.congr_of_eventuallyEq ?_
    have : ∀ᶠ y in nhds R, y ≠ 0 := isOpen_ne.mem_nhds hR
    filter_upwards [this] with y hy
    rw [Vfr_eq Lam kap g N R0 hk hg hy]
    simp
  refine h2.congr_deriv ?_
  unfold Vfr1
  simp only [Nat.cast_ofNat]
  field_simp
  ring

/-- second derivative, closed form -/
def Vfr2 (Lam kap g N R0 R : ℝ) : ℝ :=
  6 * (4 * π * R0 ^ 4 * Lam / kap ^ 2) / R ^ 4 - 20 * (4 * π * R0 ^ 4 / kap ^ 2) / R ^ 6
    + 42 * (4 * π * R0 ^ 4 * N ^ 2 / (8 * g ^ 2)) / R ^ 8

theorem Vfr1_hasDerivAt (Lam kap g N R0 : ℝ) {R : ℝ} (hR : R ≠ 0) :
    HasDerivAt (Vfr1 Lam kap g N R0) (Vfr2 Lam kap g N R0 R) R := by
  have hA := hd_div_pow (-2 * (4 * π * R0 ^ 4 * Lam / kap ^ 2)) 3 hR
  have hB := hd_div_pow (4 * (4 * π * R0 ^ 4 / kap ^ 2)) 5 hR
  have hC := hd_div_pow (-6 * (4 * π * R0 ^ 4 * N ^ 2 / (8 * g ^ 2))) 7 hR
  have h1 := (hA.add hB).add hC
  have h2 : HasDerivAt (Vfr1 Lam kap g N R0)
      (-((-2 * (4 * π * R0 ^ 4 * Lam / kap ^ 2)) * ((3 : ℕ) * R ^ (3 - 1))) / (R ^ 3) ^ 2
        + (-((4 * (4 * π * R0 ^ 4 / kap ^ 2)) * ((5 : ℕ) * R ^ (5 - 1))) / (R ^ 5) ^ 2)
        + (-((-6 * (4 * π * R0 ^ 4 * N ^ 2 / (8 * g ^ 2))) * ((7 : ℕ) * R ^ (7 - 1))) / (R ^ 7) ^ 2)) R := by
    refine h1.congr_of_eventuallyEq ?_
    filter_upwards with y
    unfold Vfr1
    simp only [Pi.add_apply]
    ring
  refine h2.congr_deriv ?_
  unfold Vfr2
  simp only [Nat.cast_ofNat]
  field_simp
  ring

/-- Minkowski point: V(R0) = 0 = V'(R0) iff R0^2 = N^2 kappa^2/(4 g^2) and Lambda = 1/(2 R0^2) -/
theorem minkowski_point (Lam N : ℝ) {kap g R0 : ℝ} (hk : 0 < kap) (hg : 0 < g) (hR0 : 0 < R0) :
    (Vfr Lam kap g N R0 R0 = 0 ∧ Vfr1 Lam kap g N R0 R0 = 0) ↔
      (R0 ^ 2 = N ^ 2 * kap ^ 2 / (4 * g ^ 2) ∧ Lam = 1 / (2 * R0 ^ 2)) := by
  have h0 : R0 ≠ 0 := hR0.ne'
  have hk0 : kap ≠ 0 := hk.ne'
  have hg0 : g ≠ 0 := hg.ne'
  have hp : 0 < π := Real.pi_pos
  rw [Vfr_eq Lam kap g N R0 hk0 hg0 h0]
  unfold Vfr1
  constructor
  · rintro ⟨e1, e2⟩
    field_simp at e1 e2
    have hp4 : (4 * π) ≠ 0 := by positivity
    have E1 : R0 ^ 2 * (R0 ^ 2 * Lam - 1) * 8 * g ^ 2 + kap ^ 2 * N ^ 2 = 0 := by
      rw [mul_zero] at e1
      rcases mul_eq_zero.1 e1 with h | h
      · exact absurd h hp4
      · exact h
    have E2 : R0 ^ 2 * 8 * g ^ 2 * (-(R0 ^ 2 * Lam * 2) + 4) - kap ^ 2 * N ^ 2 * 6 = 0 := by
      rw [mul_zero] at e2
      rcases mul_eq_zero.1 e2 with h | h
      · exact absurd h hp4
      · exact h
    have F : (R0 ^ 2 * 8 * g ^ 2) * (4 * (R0 ^ 2 * Lam) - 2) = 0 := by
      linear_combination E2 + 6 * E1
    have hne : R0 ^ 2 * 8 * g ^ 2 ≠ 0 := by positivity
    have hL : R0 ^ 2 * Lam = 1 / 2 := by
      rcases mul_eq_zero.1 F with h | h
      · exact absurd h hne
      · linarith
    refine ⟨?_, ?_⟩
    · field_simp
      nlinarith [E1, hL]
    · field_simp
      linarith [hL]
  · rintro ⟨hw, hL⟩
    subst hL
    have hN : N ^ 2 = 4 * g ^ 2 * R0 ^ 2 / kap ^ 2 := by
      field_simp at hw ⊢
      nlinarith [hw]
    rw [hN]
    constructor <;> (field_simp; ring)

theorem V2_minkowski (N : ℝ) {kap g R0 : ℝ} (hk : 0 < kap) (hg : 0 < g) (hR0 : 0 < R0)
    (hw : R0 ^ 2 = N ^ 2 * kap ^ 2 / (4 * g ^ 2)) :
    Vfr2 (1 / (2 * R0 ^ 2)) kap g N R0 R0 = 64 * π * g ^ 2 / (N ^ 2 * kap ^ 4) ∧
      0 < 64 * π * g ^ 2 / (N ^ 2 * kap ^ 4) := by
  have h0 : R0 ≠ 0 := hR0.ne'
  have hk0 : kap ≠ 0 := hk.ne'
  have hg0 : g ≠ 0 := hg.ne'
  have hN0 : N ≠ 0 := by
    intro hN
    rw [hN] at hw
    simp at hw
    exact h0 hw
  have hN : N ^ 2 = 4 * g ^ 2 * R0 ^ 2 / kap ^ 2 := by
    field_simp at hw ⊢
    nlinarith [hw]
  refine ⟨?_, by have := Real.pi_pos; positivity⟩
  unfold Vfr2
  rw [hN]
  field_simp
  ring

/-- the extremum curve Lambda(y) of W(y) = Lambda/y - 1/y^2 + 1/(2 y^3) -/
def Lam_of_y (y : ℝ) : ℝ := 2 / y - 3 / (2 * y ^ 2)

/-- W(y) = Lambda/y - 1/y^2 + 1/(2 y^3) and its derivative (so the extremum condition below is dW/dy = 0) -/
theorem W_hasDerivAt (Lam : ℝ) {y : ℝ} (hy : 0 < y) :
    HasDerivAt (fun y : ℝ => Lam / y - 1 / y ^ 2 + (1 / 2) / y ^ 3)
      (-Lam / y ^ 2 + 2 / y ^ 3 - 3 / (2 * y ^ 4)) y := by
  have h0 : y ≠ 0 := hy.ne'
  have hA := hd_div_pow Lam 1 h0
  have hB := hd_div_pow 1 2 h0
  have hC := hd_div_pow (1 / 2) 3 h0
  have h1 := (hA.sub hB).add hC
  have h2 : HasDerivAt (fun y : ℝ => Lam / y - 1 / y ^ 2 + (1 / 2) / y ^ 3)
      (-(Lam * ((1 : ℕ) * y ^ (1 - 1))) / (y ^ 1) ^ 2 - (-(1 * ((2 : ℕ) * y ^ (2 - 1))) / (y ^ 2) ^ 2)
        + (-((1 / 2) * ((3 : ℕ) * y ^ (3 - 1))) / (y ^ 3) ^ 2)) y := by
    refine h1.congr_of_eventuallyEq ?_
    filter_upwards with z
    simp only [Pi.add_apply, Pi.sub_apply, pow_one]
  refine h2.congr_deriv ?_
  simp only [Nat.cast_ofNat, Nat.cast_one, pow_one]
  field_simp
  ring

theorem Lambda_of_y (Lam y : ℝ) (hy : 0 < y) :
    (-Lam / y ^ 2 + 2 / y ^ 3 - 3 / (2 * y ^ 4) = 0) ↔ Lam = Lam_of_y y := by
  have h0 : y ≠ 0 := hy.ne'
  unfold Lam_of_y
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h
    rw [h]
    field_simp
    ring

theorem Lambda_c : Lam_of_y 1 = 1 / 2 := by unfold Lam_of_y; norm_num

theorem Lambda_merger : Lam_of_y (3 / 2) = 2 / 3 := by unfold Lam_of_y; norm_num

theorem Lambda_max (y : ℝ) (hy : 0 < y) : Lam_of_y y ≤ 2 / 3 ∧ (Lam_of_y y = 2 / 3 ↔ y = 3 / 2) := by
  have h0 : y ≠ 0 := hy.ne'
  have e : 2 / 3 - Lam_of_y y = (2 * y - 3) ^ 2 / (6 * y ^ 2) := by
    unfold Lam_of_y
    field_simp
    ring
  have hnn : 0 ≤ (2 * y - 3) ^ 2 / (6 * y ^ 2) := by positivity
  refine ⟨by linarith, ?_⟩
  constructor
  · intro h
    have : (2 * y - 3) ^ 2 / (6 * y ^ 2) = 0 := by linarith
    rcases div_eq_zero_iff.1 this with h1 | h1
    · have : 2 * y - 3 = 0 := pow_eq_zero_iff (by norm_num) |>.1 h1
      linarith
    · exfalso
      have : 0 < 6 * y ^ 2 := by positivity
      linarith
  · intro h
    rw [h]; exact Lambda_merger

end M6I

end

#print axioms M6I.Vfr_hasDerivAt
#print axioms M6I.Vfr1_hasDerivAt
#print axioms M6I.minkowski_point
#print axioms M6I.V2_minkowski
#print axioms M6I.W_hasDerivAt
#print axioms M6I.Lambda_of_y
#print axioms M6I.Lambda_max
