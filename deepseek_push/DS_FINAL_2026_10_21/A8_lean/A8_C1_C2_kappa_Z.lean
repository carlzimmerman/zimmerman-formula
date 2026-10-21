/-
A8 / C1 + C2 — the kappa-Z identity and the exact closed forms.

Physics claim being certified (BRIEF section 1):

  Vacuum-tied scale:   a0 = kappa * c * sqrt(G * rho_Lambda)          (definition, kappa = 1/2 canonical)
  Friedmann (flat, Lambda-only, rho = rho_Lambda):
                       H^2 = 8*pi*G*rho/3
  =>  (a0/(c*H))^2 = kappa^2 * 3/(8*pi)
  =>  with kappa = 1/2:  (a0/(c*H))^2 = 3/(32*pi)
  =>  with a0/(c*H) > 0: a0/(c*H) = 1/(2*sqrt(8*pi/3)) = 1/Z,  Z = 2*sqrt(8*pi/3).

What is proved here is exactly this algebra, over Real, with Real.sqrt, no
numerics.  It certifies that "a0/(cH) = 1/Z" is a consequence of the two
stated equations and nothing else.  It does NOT certify that either equation
is true of the world, and it does not certify any value of G, H or a0.

C2 additionally proves the two closed forms are the SAME real number
(1/(2 sqrt(8 pi/3)) = sqrt(3/(32 pi))) and that
2*sqrt(32*pi/3) = 2*(2*sqrt(8*pi/3)) = 2Z, so no numerical coincidence is
being asserted anywhere: these are identities in pi.

A strict bracket on 1/(2Z) is included: 1/12 < 1/(2*sqrt(8*pi/3)) < 1/11,
i.e. the "one twelfth of the horizon" reading is a ~3.7% misstatement of
1/(2Z) and is NOT an identity.  (And a0/(cH) = 1/Z = 2/(2Z) = 0.172746 is
itself about 2.07 times 1/12, not 1/12.)
-/
import Mathlib

namespace A8

/-! ## C1 — the kappa-Z identity -/

/-- Square of the vacuum-tied scale: `a0 = kappa c sqrt(G rho)` gives
`a0^2 = kappa^2 c^2 (G rho)`.  Pure algebra plus `Real.sq_sqrt`. -/
theorem a0_sq (κ c G ρ a0 : ℝ) (hG : 0 < G) (hρ : 0 < ρ)
    (ha0 : a0 = κ * c * Real.sqrt (G * ρ)) :
    a0 ^ 2 = κ ^ 2 * c ^ 2 * (G * ρ) := by
  have hsq : Real.sqrt (G * ρ) ^ 2 = G * ρ := Real.sq_sqrt (le_of_lt (by positivity))
  rw [ha0]
  calc (κ * c * Real.sqrt (G * ρ)) ^ 2
      = κ ^ 2 * c ^ 2 * Real.sqrt (G * ρ) ^ 2 := by ring
    _ = κ ^ 2 * c ^ 2 * (G * ρ) := by rw [hsq]

/-- **C1, general kappa.**  If `a0 = kappa c sqrt(G rho)` and the flat
Friedmann equation `H^2 = 8 pi G rho / 3` holds, then
`(a0/(cH))^2 = kappa^2 * 3/(8 pi)`.

Hypotheses: `kappa > 0`, `c > 0`, `G > 0`, `rho > 0`, `H > 0`.  These are the
positivity hypotheses that make both sides nonzero; the identity itself is
algebraic.  Nothing about the value of any constant is used beyond `pi != 0`. -/
theorem kappa_Z_identity (κ c G ρ H a0 : ℝ)
    (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) (hH : 0 < H)
    (ha0 : a0 = κ * c * Real.sqrt (G * ρ))
    (hFried : H ^ 2 = 8 * Real.pi * G * ρ / 3) :
    (a0 / (c * H)) ^ 2 = κ ^ 2 * 3 / (8 * Real.pi) := by
  have ha0sq : a0 ^ 2 = κ ^ 2 * c ^ 2 * (G * ρ) := a0_sq κ c G ρ a0 hG hρ ha0
  have hpi : (Real.pi : ℝ) ≠ 0 := Real.pi_ne_zero
  have hGρ : G * ρ ≠ 0 := ne_of_gt (by positivity)
  have hcH : c * H ≠ 0 := ne_of_gt (by positivity)
  have hc2 : c ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hc)
  rw [div_pow, ha0sq, mul_pow, hFried]
  field_simp

/-- **C1, kappa = 1/2 (canonical).**  `(a0/(cH))^2 = 3/(32 pi)`. -/
theorem kappa_half_sq (c G ρ H a0 : ℝ)
    (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) (hH : 0 < H)
    (ha0 : a0 = (1 / 2) * c * Real.sqrt (G * ρ))
    (hFried : H ^ 2 = 8 * Real.pi * G * ρ / 3) :
    (a0 / (c * H)) ^ 2 = 3 / (32 * Real.pi) := by
  have h := kappa_Z_identity (1 / 2) c G ρ H a0 (by norm_num) hc hG hρ hH ha0 hFried
  have hcast : ((1 / 2 : ℝ) ^ 2) * 3 / (8 * Real.pi) = 3 / (32 * Real.pi) := by
    field_simp
    ring
  rwa [hcast] at h

/-- The target closed form squares to `3/(32 pi)`. -/
theorem inv_two_sqrt_sq : (1 / (2 * Real.sqrt (8 * Real.pi / 3))) ^ 2 = 3 / (32 * Real.pi) := by
  have h8 : (0 : ℝ) < 8 * Real.pi / 3 := by positivity
  have hpi : (Real.pi : ℝ) ≠ 0 := Real.pi_ne_zero
  rw [div_pow, one_pow, mul_pow, Real.sq_sqrt (le_of_lt h8)]
  field_simp
  ring

/-- **C1, closed form.**  With the sign of `a0/(cH)` fixed positive (physical
branch: `a0 > 0`, `c > 0`, `H > 0`), the square identity upgrades to
`a0/(cH) = 1/(2 sqrt(8 pi/3)) = 1/Z`.  Sign matters: the square identity alone
only gives `a0/(cH) = +-1/(2 sqrt(8 pi/3))`. -/
theorem a0_over_cH_eq_inv_two_sqrt (c G ρ H a0 : ℝ)
    (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) (hH : 0 < H)
    (ha0 : a0 = (1 / 2) * c * Real.sqrt (G * ρ))
    (hFried : H ^ 2 = 8 * Real.pi * G * ρ / 3)
    (hpos : 0 < a0 / (c * H)) :
    a0 / (c * H) = 1 / (2 * Real.sqrt (8 * Real.pi / 3)) := by
  have hsq : (a0 / (c * H)) ^ 2 = 3 / (32 * Real.pi) :=
    kappa_half_sq c G ρ H a0 hc hG hρ hH ha0 hFried
  have hx : a0 / (c * H) = Real.sqrt (3 / (32 * Real.pi)) := by
    rw [← Real.sqrt_sq (x := a0 / (c * H)) (le_of_lt hpos), hsq]
  have hy : 1 / (2 * Real.sqrt (8 * Real.pi / 3)) = Real.sqrt (3 / (32 * Real.pi)) := by
    rw [← Real.sqrt_sq (x := 1 / (2 * Real.sqrt (8 * Real.pi / 3))) (by positivity),
      inv_two_sqrt_sq]
  rw [hx, ← hy]

/-! ## C2 — the two closed forms are the same number, exactly -/

/-- **C2 (a).**  `2*sqrt(32 pi/3) = 2*(2*sqrt(8 pi/3)) = 2Z`, i.e. the
"11.5776" number is literally twice `Z = 2 sqrt(8 pi/3)`; the factor 4 under
the root is the only content and it is exact. -/
theorem two_sqrt_32pi_3 : 2 * Real.sqrt (32 * Real.pi / 3) = 2 * (2 * Real.sqrt (8 * Real.pi / 3)) := by
  have h4 : Real.sqrt (4 : ℝ) = 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have harg : (32 : ℝ) * Real.pi / 3 = 4 * (8 * Real.pi / 3) := by ring
  rw [harg, Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 4), h4]

/-- **C2 (b).**  `1/(2 sqrt(8 pi/3)) = sqrt(3/(32 pi))`: the reciprocal form and
the sqrt-of-ratio form are the same real number.  Stated as an identity of the
closed forms, so no decimal coincidence is involved. -/
theorem inv_two_sqrt_eq_sqrt_ratio :
    1 / (2 * Real.sqrt (8 * Real.pi / 3)) = Real.sqrt (3 / (32 * Real.pi)) := by
  rw [← Real.sqrt_sq (x := 1 / (2 * Real.sqrt (8 * Real.pi / 3))) (by positivity),
    inv_two_sqrt_sq]

/-- `Z = 2 sqrt(8 pi/3)`, the constant of BRIEF section 1 (Z = 5.78881...). -/
noncomputable def Z : ℝ := 2 * Real.sqrt (8 * Real.pi / 3)

/-- **C2 (b'), the 1/12 bracket.**  `1/12 < 1/(2Z) < 1/11`, i.e.
`0.083333... < 0.086373... < 0.090909...`.

So "one twelfth of the horizon" is NOT an identity for `1/(2Z)`: it is a
~3.7% understatement.  (`a0/(cH) = 1/Z = 2/(2Z) = 0.172747...`, i.e. about
`2.07/12`, by `a0_over_cH_eq_inv_two_sqrt`.)  No decimal is used in the proof:
only `3 < pi < 3.14159265358979323847`. -/
theorem inv_twoZ_bracket : 1 / 12 < 1 / (2 * Z) ∧ 1 / (2 * Z) < 1 / 11 := by
  have hpi3 : (3 : ℝ) < Real.pi := Real.pi_gt_three
  have hpid : Real.pi < 3.14159265358979323847 := Real.pi_lt_d20
  have hlt3 : Real.sqrt (8 * Real.pi / 3) < 3 := by
    rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 3)]
    nlinarith
  have hgt : (11 / 4 : ℝ) < Real.sqrt (8 * Real.pi / 3) := by
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 11 / 4)]
    nlinarith
  have hZ : Z = 2 * Real.sqrt (8 * Real.pi / 3) := rfl
  have hpos : (0 : ℝ) < 2 * Z := by rw [hZ]; positivity
  have hlt12 : 2 * Z < 12 := by rw [hZ]; linarith
  have hgt11 : (11 : ℝ) < 2 * Z := by rw [hZ]; linarith
  constructor
  · rw [one_div_lt_one_div (by norm_num : (0 : ℝ) < 12) hpos]
    exact hlt12
  · rw [one_div_lt_one_div hpos (by norm_num : (0 : ℝ) < 11)]
    exact hgt11

/-- Corollary in the form used by the report: `1/(2Z)` is not `1/12`. -/
theorem inv_twoZ_ne_twelfth : 1 / (2 * Z) ≠ 1 / 12 := ne_of_gt inv_twoZ_bracket.1

end A8

#print axioms A8.a0_sq
#print axioms A8.kappa_Z_identity
#print axioms A8.kappa_half_sq
#print axioms A8.inv_two_sqrt_sq
#print axioms A8.a0_over_cH_eq_inv_two_sqrt
#print axioms A8.two_sqrt_32pi_3
#print axioms A8.inv_two_sqrt_eq_sqrt_ratio
#print axioms A8.inv_twoZ_bracket
#print axioms A8.inv_twoZ_ne_twelfth
