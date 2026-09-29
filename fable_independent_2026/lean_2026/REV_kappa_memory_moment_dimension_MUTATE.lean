import Mathlib

/-!
# MineM5-B: kappa <=> memory first moment, and the two competing D-dependences of kappa (conditional on stated premises)

Source lanes:
* real_research/reviews/mi_N_count_and_kappa_iff_2026.py, Part C (lines ~192-215, checks C1-C3 and NC3): "kappa = 1/2 <==> M1 = (4/3) t_Lambda", proved with sympy; NC3: M1 = t_Lambda gives kappa = 2/3.
* real_research/reviews/mi_kappa_from_dimension_2026.py, Parts A-B (lines ~101-160): kappa = (2/3)/[(rho+p)/rho] = (2/3)(D-1)/D under the PREMISE M1/t_Lambda = D/(D-1); the script itself says "NOT A PROOF".
* real_research/reviews/mi_kappa_D_dependence_rigidity_2026.py, Parts A, D, E (lines ~150-300): kappa_D = (1/2) sqrt(6/((D-1)(D-2))) from a D-dimensional Friedmann relation, a D-independent memory time and a D-independent xi; and "D4: they DISAGREE for every D != 4".

CERTIFIED (premises => conclusions; real algebra only):
* `kappa_M1_relation`: a0 = kappa c s (s = sqrt(G rho) > 0, t = 1/s) and M1 = 2c/(3 a0) give M1 = (2/3) t/kappa.
* `kappa_half_iff_M1`: kappa = 1/2 <-> M1 = (4/3) t  (both directions; no kernel shape enters).  `M1_eq_t_gives_two_thirds`: M1 = t gives kappa = 2/3.
* `kappa_of_enthalpy_premise` / `kappa_half_iff_D4`: IF M1/t = D/(D-1) (D > 1; a PREMISE, not derived) THEN kappa = (2/3)(D-1)/D, and this is 1/2 iff D = 4.
* `kappa_D_derived`: IF H^2 = 16 pi s^2/((D-1)(D-2)) (the D-dimensional flat Friedmann relation, taken as a PREMISE here), a0 = (2/3) c H/xi (i.e. a0 = (2/3)c/M1 with M1 = xi/H), and xi = (4/3) sqrt(8 pi/3)
  (the D = 4 value, D-INDEPENDENT by the lane's worldline argument, which is NOT certified) THEN kappa_D = (1/2) sqrt(6/((D-1)(D-2))), equal to 1/2 at D = 4.
* `two_forms_agree_iff_D4`: for real D > 2 the two forms (2/3)(D-1)/D and (1/2) sqrt(6/((D-1)(D-2))) coincide iff D = 4 (the cubic 8D^3 - 8D^2 + 13D - 4 has no root above 2).
* `xi_sq`: ((4/3) sqrt(8 pi/3))^2 = 2 pi (4/3)^3.

NOT certified: either premise (M1/t = D/(D-1) has "no computed link", per the lane; the D-independence of xi and the memory factor 2/3 are argued, not proved); the D-dimensional Friedmann coefficient
itself (computed by sympy in the lane, here a hypothesis); the numerical statement M1/t_Lambda = 4/3 to 30 digits (circular: M1 is built from the kappa = 1/2 a0); anything empirical.
IMPORTANT: xi is the D = 4 value, which is equivalent to kappa(4) = 1/2, so `kappa_D_derived` gives the D-SCALING of kappa relative to its D = 4 value, not a derivation of kappa = 1/2.
kappa = 1/2 remains FITTED; nothing here says the theory is closed.
-/

open Real

namespace MineM5B

/-- a0 = kappa c s and the action's requirement M1 = 2c/(3 a0) give M1 = (2/3) t / kappa, with t = 1/s -/
theorem kappa_M1_relation {c s κ a0 M1 : ℝ} (hc : c ≠ 0) (hs : s ≠ 0) (hκ : κ ≠ 0)
    (ha : a0 = κ * c * s) (hM : M1 = 2 * c / (3 * a0)) : M1 = (2 / 3) * (1 / s) / κ := by
  subst ha hM
  field_simp

/-- kappa = 1/2 <-> M1 = (4/3) t (t = 1/s), given the two defining relations -/
theorem kappa_half_iff_M1 {c s κ a0 M1 : ℝ} (hc : c ≠ 0) (hs : s ≠ 0) (hκ : κ ≠ 0)
    (ha : a0 = κ * c * s) (hM : M1 = 2 * c / (3 * a0)) :
    κ = 1 / 2 ↔ M1 = (3 / 4) * (1 / s) := by
  have h := kappa_M1_relation hc hs hκ ha hM
  rw [h]
  constructor
  · intro hk; subst hk; field_simp; norm_num
  · intro hm
    field_simp at hm
    field_simp
    nlinarith [hm]

/-- a moment M1 = t gives kappa = 2/3 (so the iff is a real determination) -/
theorem M1_eq_t_gives_two_thirds {c s κ a0 M1 : ℝ} (hc : c ≠ 0) (hs : s ≠ 0) (hκ : κ ≠ 0)
    (ha : a0 = κ * c * s) (hM : M1 = 2 * c / (3 * a0)) (h1 : M1 = 1 / s) : κ = 2 / 3 := by
  have h := kappa_M1_relation hc hs hκ ha hM
  rw [h] at h1
  field_simp at h1
  nlinarith [h1]

/-- PREMISE M1/t = D/(D-1) (D > 1) gives kappa = (2/3)(D-1)/D -/
theorem kappa_of_enthalpy_premise {c s κ a0 M1 D : ℝ} (hc : c ≠ 0) (hs : s ≠ 0) (hκ : κ ≠ 0)
    (ha : a0 = κ * c * s) (hM : M1 = 2 * c / (3 * a0)) (hD : 1 < D)
    (hprem : M1 = (D / (D - 1)) * (1 / s)) : κ = (2 / 3) * (D - 1) / D := by
  have h := kappa_M1_relation hc hs hκ ha hM
  have hD1 : D - 1 ≠ 0 := by linarith
  have hD0 : D ≠ 0 := by linarith
  rw [h] at hprem
  field_simp at hprem
  field_simp
  nlinarith [hprem]

/-- the closed form (2/3)(D-1)/D equals 1/2 iff D = 4 (D > 0) -/
theorem kappa_half_iff_D4 {D : ℝ} (hD : 0 < D) : (2 / 3) * (D - 1) / D = 1 / 2 ↔ D = 4 := by
  constructor
  · intro h
    field_simp at h
    linarith
  · intro h
    subst h
    norm_num

/-- xi^2 = 2 pi (4/3)^3 for xi = (4/3) sqrt(8 pi/3) -/
theorem xi_sq : ((4 / 3) * Real.sqrt (8 * π / 3)) ^ 2 = 2 * π * (4 / 3) ^ 3 := by
  have hp := Real.pi_pos
  rw [mul_pow, Real.sq_sqrt (by positivity)]
  ring

/-- the D-scaling from the D-dimensional Friedmann relation (premise), a0 = (2/3) c H/xi, xi = (4/3) sqrt(8 pi/3) -/
theorem kappa_D_derived {c s H a0 κ D : ℝ} (hc : 0 < c) (hs : 0 < s) (hH : 0 < H) (hD : 2 < D)
    (hFried : H ^ 2 = 16 * π * s ^ 2 / ((D - 1) * (D - 2)))
    (ha : a0 = (2 / 3) * c * H / ((4 / 3) * Real.sqrt (8 * π / 3)))
    (hκ : a0 = κ * c * s) :
    κ = (1 / 2) * Real.sqrt (6 / ((D - 1) * (D - 2))) := by
  have hp := Real.pi_pos
  have hD1 : 0 < D - 1 := by linarith
  have hD2 : 0 < D - 2 := by linarith
  have hq : 0 < Real.sqrt (8 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hκdef : κ = (2 / 3) * H / ((4 / 3) * Real.sqrt (8 * π / 3) * s) := by
    have : κ * (c * s) = (2 / 3) * c * H / ((4 / 3) * Real.sqrt (8 * π / 3)) := by rw [← ha, hκ]; ring
    field_simp at this ⊢
    nlinarith [this]
  have hκpos : 0 < κ := by rw [hκdef]; positivity
  have hR : 0 ≤ (1 / 2) * Real.sqrt (6 / ((D - 1) * (D - 2))) := by positivity
  have e1 : κ ^ 2 = 3 / (2 * ((D - 1) * (D - 2))) := by
    have hsq : Real.sqrt (8 * π / 3) ^ 2 = 8 * π / 3 := Real.sq_sqrt (by positivity)
    have hk1 : κ * ((4 / 3) * Real.sqrt (8 * π / 3) * s) = (2 / 3) * H := by
      rw [hκdef]; field_simp
    have key : κ ^ 2 * (((4 / 3) * Real.sqrt (8 * π / 3) * s) ^ 2) = ((2 / 3) * H) ^ 2 := by
      rw [← hk1]; ring
    have hX : ((4 / 3) * Real.sqrt (8 * π / 3) * s) ^ 2 = (16 / 9) * (8 * π / 3) * s ^ 2 := by
      rw [mul_pow, mul_pow, hsq]; ring
    have hY : ((2 / 3) * H) ^ 2 = (4 / 9) * (16 * π * s ^ 2 / ((D - 1) * (D - 2))) := by
      rw [mul_pow, hFried]; ring
    have hne : (16 / 9) * (8 * π / 3) * s ^ 2 ≠ 0 := by positivity
    rw [hX, hY] at key
    apply mul_right_cancel₀ hne
    rw [key]
    field_simp
    ring
  have e2 : ((1 / 2) * Real.sqrt (6 / ((D - 1) * (D - 2)))) ^ 2 = 3 / (2 * ((D - 1) * (D - 2))) := by
    rw [mul_pow, Real.sq_sqrt (by positivity)]
    field_simp
    norm_num
  exact (sq_eq_sq₀ hκpos.le hR).mp (e1.trans e2.symm)

/-- at D = 4 the D-scaling form is exactly 1/2 -/
theorem kappa_D_at_four : (1 / 2 : ℝ) * Real.sqrt (6 / ((4 - 1) * (4 - 2))) = 1 / 2 := by
  norm_num

/-- the two forms coincide, for real D > 2, only at D = 4 (the second form squared: 3/(2(D-1)(D-2)) = 4(D-1)^2/(9 D^2)) -/
theorem two_forms_agree_iff_D4 {D : ℝ} (hD : 2 < D) :
    (2 / 3) * (D - 1) / D = (1 / 2) * Real.sqrt (6 / ((D - 1) * (D - 2))) ↔ D = 4 := by
  have hD1 : 0 < D - 1 := by linarith
  have hD2 : 0 < D - 2 := by linarith
  have hD0 : 0 < D := by linarith
  have hL : 0 ≤ (2 / 3) * (D - 1) / D := by positivity
  have hR : 0 ≤ (1 / 2) * Real.sqrt (6 / ((D - 1) * (D - 2))) := by positivity
  have e2 : ((1 / 2) * Real.sqrt (6 / ((D - 1) * (D - 2)))) ^ 2 = 3 / (2 * ((D - 1) * (D - 2))) := by
    rw [mul_pow, Real.sq_sqrt (by positivity)]
    field_simp
    norm_num
  constructor
  · intro h
    have hsq : ((2 / 3) * (D - 1) / D) ^ 2 = 3 / (2 * ((D - 1) * (D - 2))) := by
      rw [h]; exact e2
    have hpoly : (D - 4) * (8 * D ^ 3 - 8 * D ^ 2 + 13 * D - 4) = 0 := by
      field_simp at hsq
      nlinarith [hsq]
    rcases mul_eq_zero.mp hpoly with h4 | h3
    · linarith
    · exfalso
      nlinarith [mul_pos hD0 hD0, mul_pos (mul_pos hD0 hD0) hD1]
  · intro h
    subst h
    norm_num

end MineM5B

#print axioms MineM5B.kappa_M1_relation
#print axioms MineM5B.kappa_half_iff_M1
#print axioms MineM5B.M1_eq_t_gives_two_thirds
#print axioms MineM5B.kappa_of_enthalpy_premise
#print axioms MineM5B.kappa_half_iff_D4
#print axioms MineM5B.xi_sq
#print axioms MineM5B.kappa_D_derived
#print axioms MineM5B.kappa_D_at_four
#print axioms MineM5B.two_forms_agree_iff_D4
