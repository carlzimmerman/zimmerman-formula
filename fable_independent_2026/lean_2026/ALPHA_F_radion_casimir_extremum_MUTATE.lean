import Mathlib

/-!
# M6-A -- the radion potential of lane F (5D on S^1, Casimir + 5D vacuum energy): derivative algebra

Source: `real_research/alpha_principle_2026/F_kk_stabilization/f1_radion_circle.py`, checks A2b, A2c, A2d and
the matching step of A3 (script lines 45-92):  V_E(R) = (R0/R)^2 (2 pi R rho5 - c/R^4)  (Einstein-frame radion
potential; c = Casimir coefficient; rho5 = 5D vacuum energy density).  The script obtains the extremum
condition, V_E(R*) = 5c/R*^4, V_E''(R*) = -30 c/R*^6 and R* = (40 pi |c|/x)^(1/4) with sympy.

Corpus check (2026-09-29):  `git grep -n -i -e radion -e Casimir -- '*.lean'` finds only the Freund-Rubin
coupling file ALPHA_F_Q3_flux_couplings.lean (which takes the S^2 Minkowski point as a printed premise and does
not touch this S^1 potential) and unrelated SU(N) Casimirs.  New.

CERTIFIED (real analysis, exact; R0 > 0):
  * `V_hasDerivAt`     : V'(R) = -2 pi rho5 R0^2/R^2 + 6 c R0^2/R^7   (R != 0), and `V1_hasDerivAt` : V'' formula;
  * `extremum_iff`     : V'(R0) = 0  <->  2 pi rho5 R0^5 = 6 c;
  * `V_at_extremum`    : at an extremum V(R0) = 5 c / R0^4;
  * `V2_at_extremum`   : at an extremum V''(R0) = -30 c / R0^6 (as HasDerivAt of the derivative function);
  * `sign_theorem`     : at an extremum, V(R0) > 0 <-> c > 0, and then V''(R0) < 0 (a MAXIMUM, the radion tachyon);
                         c < 0 gives V(R0) < 0 and V''(R0) > 0 (a minimum, AdS-type).  So no de Sitter minimum
                         arises from {rho5, Casimir} alone (the lane's "sign theorem", as mathematics);
  * `match_radius`     : for x > 0 and c != 0, |V(R0)| = x/(8 pi) <-> R0^4 = 40 pi |c| / x.
NOT CERTIFIED: the Weyl rescaling that produces V_E from the 5D action; the value of the Casimir coefficient c
(-3 zeta(5)/(64 pi^6) per dof) or the dof count; the identification rho_Lambda l_P^4 = x/(8 pi) with the observed
vacuum energy; any numerical R*/l_P; the absence of other modes/other compactifications.  No empirical premise;
alpha is not derived; kappa = 1/2 is unrelated.
-/

noncomputable section
namespace M6A

open Real

/-- the Einstein-frame radion potential of f1_radion_circle.py -/
def V (R0 rho5 c : ℝ) (R : ℝ) : ℝ := (R0 / R) ^ 2 * (2 * π * R * rho5 - c / R ^ 4)

/-- its first derivative, closed form -/
def V1 (R0 rho5 c : ℝ) (R : ℝ) : ℝ := -2 * π * rho5 * R0 ^ 2 / R ^ 2 + 6 * c * R0 ^ 2 / R ^ 7

lemma V_eq (R0 rho5 c : ℝ) {R : ℝ} (hR : R ≠ 0) :
    V R0 rho5 c R = 2 * π * rho5 * R0 ^ 2 / R - c * R0 ^ 2 / R ^ 6 := by
  unfold V
  field_simp

lemma V1_eq (R0 rho5 c : ℝ) {R : ℝ} :
    V1 R0 rho5 c R = -(2 * π * rho5 * R0 ^ 2) / R ^ 2 + 6 * c * R0 ^ 2 / R ^ 7 := by
  unfold V1
  ring

/-- derivative of K / R^n -/
lemma hd_div_pow (K : ℝ) (n : ℕ) {R : ℝ} (hR : R ≠ 0) :
    HasDerivAt (fun R : ℝ => K / R ^ n) (-(K * ((n : ℝ) * R ^ (n - 1))) / (R ^ n) ^ 2) R := by
  have h := (hasDerivAt_const R K).fun_div (hasDerivAt_pow n R) (pow_ne_zero n hR)
  refine h.congr_deriv ?_
  ring

theorem V_hasDerivAt (R0 rho5 c : ℝ) {R : ℝ} (hR : R ≠ 0) :
    HasDerivAt (V R0 rho5 c) (V1 R0 rho5 c R) R := by
  have hA := hd_div_pow (2 * π * rho5 * R0 ^ 2) 1 hR
  have hB := hd_div_pow (c * R0 ^ 2) 6 hR
  have h1 := hA.sub hB
  have h2 : HasDerivAt (V R0 rho5 c)
      (-(2 * π * rho5 * R0 ^ 2 * ((1 : ℕ) * R ^ (1 - 1))) / (R ^ 1) ^ 2 -
        (-(c * R0 ^ 2 * ((6 : ℕ) * R ^ (6 - 1))) / (R ^ 6) ^ 2)) R := by
    refine h1.congr_of_eventuallyEq ?_
    have : ∀ᶠ y in nhds R, y ≠ 0 := isOpen_ne.mem_nhds hR
    filter_upwards [this] with y hy
    rw [V_eq R0 rho5 c hy]
    simp
  refine h2.congr_deriv ?_
  unfold V1
  field_simp
  ring

theorem V1_hasDerivAt (R0 rho5 c : ℝ) {R : ℝ} (hR : R ≠ 0) :
    HasDerivAt (V1 R0 rho5 c)
      (4 * π * rho5 * R0 ^ 2 / R ^ 3 - 41 * c * R0 ^ 2 / R ^ 8) R := by
  have hA := hd_div_pow (-(2 * π * rho5 * R0 ^ 2)) 2 hR
  have hC := hd_div_pow (6 * c * R0 ^ 2) 7 hR
  have h1 := hA.add hC
  have h2 : HasDerivAt (V1 R0 rho5 c)
      (-(-(2 * π * rho5 * R0 ^ 2) * ((2 : ℕ) * R ^ (2 - 1))) / (R ^ 2) ^ 2 +
        (-(6 * c * R0 ^ 2 * ((7 : ℕ) * R ^ (7 - 1))) / (R ^ 7) ^ 2)) R := by
    refine h1.congr_of_eventuallyEq ?_
    filter_upwards with y
    unfold V1
    simp
  refine h2.congr_deriv ?_
  field_simp
  ring

/-- the extremum condition at R = R0 -/
theorem extremum_iff (rho5 c : ℝ) {R0 : ℝ} (hR0 : 0 < R0) :
    V1 R0 rho5 c R0 = 0 ↔ 2 * π * rho5 * R0 ^ 5 = 6 * c := by
  have h : R0 ≠ 0 := hR0.ne'
  unfold V1
  constructor
  · intro hz
    have : (-2 * π * rho5 * R0 ^ 2 / R0 ^ 2 + 6 * c * R0 ^ 2 / R0 ^ 7) * R0 ^ 5 = 0 := by rw [hz]; ring
    field_simp at this
    nlinarith [this]
  · intro hz
    field_simp
    nlinarith [hz]

theorem V_at_extremum (rho5 c : ℝ) {R0 : ℝ} (hR0 : 0 < R0) (h : V1 R0 rho5 c R0 = 0) :
    V R0 rho5 c R0 = 5 * c / R0 ^ 4 := by
  have hx := (extremum_iff rho5 c hR0).1 h
  have h0 : R0 ≠ 0 := hR0.ne'
  unfold V
  field_simp
  nlinarith [hx]

theorem V2_at_extremum (rho5 c : ℝ) {R0 : ℝ} (hR0 : 0 < R0) (h : V1 R0 rho5 c R0 = 0) :
    HasDerivAt (V1 R0 rho5 c) (-30 * c / R0 ^ 6) R0 := by
  have hx := (extremum_iff rho5 c hR0).1 h
  have h0 : R0 ≠ 0 := hR0.ne'
  have := V1_hasDerivAt R0 rho5 c h0
  refine this.congr_deriv ?_
  field_simp
  nlinarith [hx]

theorem sign_theorem (rho5 c : ℝ) {R0 : ℝ} (hR0 : 0 < R0) (h : V1 R0 rho5 c R0 = 0) :
    (0 < V R0 rho5 c R0 ↔ 0 < c) ∧
    (0 < c → ∃ d, HasDerivAt (V1 R0 rho5 c) d R0 ∧ d < 0) ∧
    (c < 0 → V R0 rho5 c R0 < 0 ∧ ∃ d, HasDerivAt (V1 R0 rho5 c) d R0 ∧ 0 < d) := by
  have hp : 0 < R0 ^ 4 := by positivity
  have hp6 : 0 < R0 ^ 6 := by positivity
  rw [V_at_extremum rho5 c hR0 h]
  refine ⟨?_, ?_, ?_⟩
  · constructor
    · intro hpos
      by_contra hc
      push Not at hc
      have : 5 * c / R0 ^ 4 ≤ 0 := div_nonpos_of_nonpos_of_nonneg (by linarith) hp.le
      linarith
    · intro hc
      positivity
  · intro hc
    exact ⟨-30 * c / R0 ^ 6, V2_at_extremum rho5 c hR0 h, by
      have : 0 < 30 * c / R0 ^ 6 := by positivity
      have e : -30 * c / R0 ^ 6 = -(30 * c / R0 ^ 6) := by ring
      linarith⟩
  · intro hc
    refine ⟨?_, -30 * c / R0 ^ 6, V2_at_extremum rho5 c hR0 h, ?_⟩
    · exact div_neg_of_neg_of_pos (by linarith) hp
    · have : 0 < -30 * c := by linarith
      positivity

/-- matching |V(R0)| to a vacuum energy x/(8 pi) gives R0^4 = 40 pi |c| / x -/
theorem match_radius (c x : ℝ) {R0 : ℝ} (hR0 : 0 < R0) (hx : 0 < x) :
    |5 * c / R0 ^ 4| = x / (8 * π) ↔ R0 ^ 4 = 40 * π * |c| / x := by
  have hp : 0 < R0 ^ 4 := by positivity
  have hpi := Real.pi_pos
  rw [abs_div, abs_of_pos hp, abs_mul]
  norm_num
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h
    field_simp at h ⊢
    nlinarith [h]

end M6A

end

#print axioms M6A.V_hasDerivAt
#print axioms M6A.V1_hasDerivAt
#print axioms M6A.extremum_iff
#print axioms M6A.V_at_extremum
#print axioms M6A.V2_at_extremum
#print axioms M6A.sign_theorem
#print axioms M6A.match_radius
