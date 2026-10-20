module

public import Mathlib.Algebra.Order.Field.Basic
meta import Mathlib.Tactic.FieldSimp
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.Ring.Basic

@[expose] public section

/-!
Ordered-field algebra for the principal polynomial in
MICROSCOPIC_CONTINUATION.md, section B. The coefficients and their physical
interpretation are explicit inputs. This file makes no quantum, PDE, gauge
invariance, background-existence, or amplitude-selection claim.

The universal root theorem bounds every root that exists in the field.
An arbitrary ordered field need not contain square roots; the optional
quadratic-formula theorem therefore supplies an explicit discriminant root
as a hypothesis, rather than asserting root existence in every field.
-/

namespace Why4.GaugeCones

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def principal (alpha beta delta z : K) : K :=
  z ^ 2 - (alpha + beta + delta) * z + alpha * beta

def discriminant (alpha beta delta : K) : K :=
  (alpha + beta + delta) ^ 2 - 4 * alpha * beta

theorem discriminant_identity (alpha beta delta : K) :
    discriminant alpha beta delta =
      (alpha - beta) ^ 2 + delta * (2 * alpha + 2 * beta + delta) := by
  dsimp [discriminant]
  ring1

theorem discriminant_nonneg {alpha beta delta : K}
    (ha : 0 ≤ alpha) (hb : 0 ≤ beta) (hd : 0 ≤ delta) :
    0 ≤ discriminant alpha beta delta := by
  rw [discriminant_identity]
  exact add_nonneg (sq_nonneg _) (mul_nonneg hd (by linarith))

theorem principal_root_bounds {alpha beta delta z : K}
    (ha : 0 < alpha) (hb : 0 < beta) (ha1 : alpha ≤ 1) (hb1 : beta ≤ 1)
    (hd : 0 ≤ delta) (hbudget : delta ≤ (1 - alpha) * (1 - beta))
    (hroot : principal alpha beta delta z = 0) : 0 < z ∧ z ≤ 1 := by
  have hp : 0 < alpha * beta := mul_pos ha hb
  have hs : 0 < alpha + beta + delta := by linarith
  have hp1 : alpha * beta ≤ 1 := by
    calc
      alpha * beta ≤ 1 * 1 := mul_le_mul ha1 hb1 (le_of_lt hb) (by exact zero_le_one)
      _ = 1 := one_mul 1
  have hgap : 0 ≤ 1 + alpha * beta - (alpha + beta + delta) := by
    nlinarith only [hbudget]
  have hz : 0 < z := by
    by_contra h
    have hzn : z ≤ 0 := le_of_not_gt h
    have hm : (alpha + beta + delta) * z ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos (le_of_lt hs) hzn
    dsimp [principal] at hroot
    nlinarith only [hroot, sq_nonneg z, hp, hm]
  refine ⟨hz, ?_⟩
  by_contra h
  have hz1 : 1 < z := lt_of_not_ge h
  have hfirst : 0 < (z - 1) * (z - alpha * beta) :=
    mul_pos (by linarith) (by linarith)
  have hsecond : 0 ≤ z * (1 + alpha * beta - (alpha + beta + delta)) :=
    mul_nonneg (le_of_lt hz) hgap
  have hfactor : principal alpha beta delta z =
      (z - 1) * (z - alpha * beta) +
        z * (1 + alpha * beta - (alpha + beta + delta)) := by
    dsimp [principal]
    ring1
  have hpositive : 0 < principal alpha beta delta z := by
    rw [hfactor]
    exact add_pos_of_pos_of_nonneg hfirst hsecond
  rw [hroot] at hpositive
  exact (lt_irrefl 0) hpositive

theorem quadratic_formula_roots {alpha beta delta r : K}
    (hrsq : r ^ 2 = discriminant alpha beta delta) :
    principal alpha beta delta ((alpha + beta + delta - r) / 2) = 0 ∧
      principal alpha beta delta ((alpha + beta + delta + r) / 2) = 0 := by
  have hm : 4 * principal alpha beta delta ((alpha + beta + delta - r) / 2) =
      r ^ 2 - discriminant alpha beta delta := by
    dsimp [principal, discriminant]
    ring1
  have hp : 4 * principal alpha beta delta ((alpha + beta + delta + r) / 2) =
      r ^ 2 - discriminant alpha beta delta := by
    dsimp [principal, discriminant]
    ring1
  rw [hrsq, sub_self] at hm hp
  constructor <;> linarith only [hm, hp]

theorem quadratic_formula_root_bounds {alpha beta delta r : K}
    (ha : 0 < alpha) (hb : 0 < beta) (ha1 : alpha ≤ 1) (hb1 : beta ≤ 1)
    (hd : 0 ≤ delta) (hbudget : delta ≤ (1 - alpha) * (1 - beta))
    (hrsq : r ^ 2 = discriminant alpha beta delta) :
    (0 < (alpha + beta + delta - r) / 2 ∧ (alpha + beta + delta - r) / 2 ≤ 1) ∧
      (0 < (alpha + beta + delta + r) / 2 ∧ (alpha + beta + delta + r) / 2 ≤ 1) := by
  have hroots := quadratic_formula_roots hrsq
  exact ⟨principal_root_bounds ha hb ha1 hb1 hd hbudget hroots.1,
    principal_root_bounds ha hb ha1 hb1 hd hbudget hroots.2⟩

def stiffness (F b y : K) : K := F * y / (y + b)

def curvature (F b gamma y Hsq : K) : K :=
  gamma * y + F * b * Hsq / (y + b) ^ 3

def massSquared (k gamma y : K) : K := k * gamma * y

def slope (F b y : K) : K := F * b / (y + b) ^ 2

def coneAlpha (F b gamma y Hsq k : K) : K :=
  massSquared k gamma y / curvature F b gamma y Hsq

def coneBeta (F b y : K) : K := stiffness F b y / F

def coneDelta (F b gamma y Hsq T : K) : K :=
  slope F b y ^ 2 * Hsq * T / (curvature F b gamma y Hsq * F)

theorem refined_budget_identity (F b gamma y Hsq k T : K)
    (hF : F ≠ 0) (hs : y + b ≠ 0) :
    (1 - y / (y + b)) *
        ((gamma * y + F * b * Hsq / (y + b) ^ 3) - k * gamma * y) -
        (F * b / (y + b) ^ 2) ^ 2 * Hsq * T / F =
      b * gamma * y * (1 - k) / (y + b) +
        F * b ^ 2 * Hsq * (1 - T) / (y + b) ^ 4 := by
  field_simp [hF, hs] <;> ring1

theorem refined_budget_nonnegative {F b gamma y Hsq k T : K}
    (hF : 0 < F) (hb : 0 < b) (hg : 0 < gamma) (hy : 0 < y)
    (hH : 0 ≤ Hsq) (hk1 : k ≤ 1) (hT1 : T ≤ 1) :
    0 ≤ (1 - y / (y + b)) *
        ((gamma * y + F * b * Hsq / (y + b) ^ 3) - k * gamma * y) -
        (F * b / (y + b) ^ 2) ^ 2 * Hsq * T / F := by
  have hs : 0 < y + b := add_pos hy hb
  rw [refined_budget_identity F b gamma y Hsq k T (ne_of_gt hF) (ne_of_gt hs)]
  apply add_nonneg
  · exact div_nonneg
      (mul_nonneg (le_of_lt (mul_pos (mul_pos hb hg) hy)) (sub_nonneg.mpr hk1))
      (le_of_lt hs)
  · exact div_nonneg
      (mul_nonneg (mul_nonneg (mul_nonneg (le_of_lt hF) (sq_nonneg b)) hH)
        (sub_nonneg.mpr hT1)) (pow_nonneg (le_of_lt hs) 4)

theorem curvature_pos {F b gamma y Hsq : K}
    (hF : 0 < F) (hb : 0 < b) (hg : 0 < gamma) (hy : 0 < y) (hH : 0 ≤ Hsq) :
    0 < curvature F b gamma y Hsq := by
  have hs : 0 < y + b := add_pos hy hb
  have hrest : 0 ≤ F * b * Hsq / (y + b) ^ 3 :=
    div_nonneg (mul_nonneg (le_of_lt (mul_pos hF hb)) hH)
      (le_of_lt (pow_pos hs 3))
  exact add_pos_of_pos_of_nonneg (mul_pos hg hy) hrest

theorem stiffness_pos {F b y : K} (hF : 0 < F) (hb : 0 < b) (hy : 0 < y) :
    0 < stiffness F b y :=
  div_pos (mul_pos hF hy) (add_pos hy hb)

theorem coneBeta_eq {F b y : K} (hF : F ≠ 0) (hs : y + b ≠ 0) :
    coneBeta F b y = y / (y + b) := by
  dsimp [coneBeta, stiffness]
  field_simp [hF, hs]

theorem scaled_budget_identity {a m f Z c : K} (ha : a ≠ 0) (hZ : Z ≠ 0) :
    a * ((1 - m / a) * (1 - f / Z) - c / (a * Z)) =
      (1 - f / Z) * (a - m) - c / Z := by
  field_simp [ha, hZ] <;> ring1

theorem substituted_cone_conditions {F b gamma y Hsq k T : K}
    (hF : 0 < F) (hb : 0 < b) (hg : 0 < gamma) (hy : 0 < y)
    (hH : 0 ≤ Hsq) (hk : 0 < k) (hk1 : k ≤ 1) (hT : 0 ≤ T) (hT1 : T ≤ 1) :
    0 < coneAlpha F b gamma y Hsq k ∧ coneAlpha F b gamma y Hsq k ≤ 1 ∧
      0 < coneBeta F b y ∧ coneBeta F b y < 1 ∧
      0 ≤ coneDelta F b gamma y Hsq T ∧
      coneDelta F b gamma y Hsq T ≤
        (1 - coneAlpha F b gamma y Hsq k) * (1 - coneBeta F b y) := by
  have hs : 0 < y + b := add_pos hy hb
  have ha := curvature_pos hF hb hg hy hH
  have hm : 0 < massSquared k gamma y := mul_pos (mul_pos hk hg) hy
  have hrest : 0 ≤ F * b * Hsq / (y + b) ^ 3 :=
    div_nonneg (mul_nonneg (le_of_lt (mul_pos hF hb)) hH)
      (le_of_lt (pow_pos hs 3))
  have hm_le : massSquared k gamma y ≤ curvature F b gamma y Hsq := by
    have hsmall : k * (gamma * y) ≤ 1 * (gamma * y) :=
      mul_le_mul_of_nonneg_right hk1 (le_of_lt (mul_pos hg hy))
    dsimp [massSquared, curvature]
    calc
      k * gamma * y = k * (gamma * y) := by ring1
      _ ≤ 1 * (gamma * y) := hsmall
      _ ≤ gamma * y + F * b * Hsq / (y + b) ^ 3 := by linarith only [hrest]
  have halpha : 0 < coneAlpha F b gamma y Hsq k := div_pos hm ha
  have halpha1 : coneAlpha F b gamma y Hsq k ≤ 1 := (div_le_one ha).2 hm_le
  have hbeta : 0 < coneBeta F b y := div_pos (stiffness_pos hF hb hy) hF
  have hbeta1 : coneBeta F b y < 1 := by
    rw [coneBeta_eq (ne_of_gt hF) (ne_of_gt hs)]
    apply (div_lt_one hs).2
    linarith only [hb]
  have hdelta : 0 ≤ coneDelta F b gamma y Hsq T :=
    div_nonneg (mul_nonneg (mul_nonneg (sq_nonneg _) hH) hT)
      (le_of_lt (mul_pos ha hF))
  have hbudget := refined_budget_nonnegative hF hb hg hy hH hk1 hT1
  have hscaled : curvature F b gamma y Hsq *
      ((1 - coneAlpha F b gamma y Hsq k) * (1 - coneBeta F b y) -
        coneDelta F b gamma y Hsq T) =
      (1 - y / (y + b)) *
        ((gamma * y + F * b * Hsq / (y + b) ^ 3) - k * gamma * y) -
        (F * b / (y + b) ^ 2) ^ 2 * Hsq * T / F := by
    dsimp [coneAlpha, coneBeta, coneDelta]
    rw [scaled_budget_identity (ne_of_gt ha) (ne_of_gt hF)]
    have hbetaeq : stiffness F b y / F = y / (y + b) :=
      coneBeta_eq (ne_of_gt hF) (ne_of_gt hs)
    rw [hbetaeq]
    rfl
  have hprod : 0 ≤ curvature F b gamma y Hsq *
      ((1 - coneAlpha F b gamma y Hsq k) * (1 - coneBeta F b y) -
        coneDelta F b gamma y Hsq T) := by
    rw [hscaled]
    exact hbudget
  have hgap := (mul_nonneg_iff_of_pos_left ha).1 hprod
  exact ⟨halpha, halpha1, hbeta, hbeta1, hdelta, sub_nonneg.mp hgap⟩

theorem substituted_principal_root_bounds {F b gamma y Hsq k T z : K}
    (hF : 0 < F) (hb : 0 < b) (hg : 0 < gamma) (hy : 0 < y)
    (hH : 0 ≤ Hsq) (hk : 0 < k) (hk1 : k ≤ 1) (hT : 0 ≤ T) (hT1 : T ≤ 1)
    (hroot : principal (coneAlpha F b gamma y Hsq k) (coneBeta F b y)
      (coneDelta F b gamma y Hsq T) z = 0) : 0 < z ∧ z ≤ 1 := by
  obtain ⟨ha, ha1, hbeta, hbeta1, hdelta, hbudget⟩ :=
    substituted_cone_conditions hF hb hg hy hH hk hk1 hT hT1
  exact principal_root_bounds ha hbeta ha1 (le_of_lt hbeta1) hdelta hbudget hroot

#check @discriminant_nonneg
#check @principal_root_bounds
#check @quadratic_formula_roots
#check @quadratic_formula_root_bounds
#check @refined_budget_identity
#check @refined_budget_nonnegative
#check @substituted_cone_conditions
#check @substituted_principal_root_bounds
#print axioms discriminant_nonneg
#print axioms principal_root_bounds
#print axioms quadratic_formula_roots
#print axioms quadratic_formula_root_bounds
#print axioms refined_budget_identity
#print axioms refined_budget_nonnegative
#print axioms substituted_cone_conditions
#print axioms substituted_principal_root_bounds

end Why4.GaugeCones
