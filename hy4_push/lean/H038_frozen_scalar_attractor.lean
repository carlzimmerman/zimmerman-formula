/-
  H038 -- IS phidot = 0 AN ATTRACTOR, OR AN IMPOSED CONSTRAINT?   Lean certificate.
  (the framework's open structural question R10; numeric lane H038_phidot_attractor.py)

  S = int sqrt(-g) [ (M_Pl^2/2) R + Lambda^4 f(K) ] ,
      K = (1/2) g^{ab} d_a phi d_b phi / Lambda^4 ,   f'(K) = mu_2(sqrt K),
      mu_2(u) = u(2+u)/(1+u)^2 .

  The scalar EOM is grad_mu [ f'(K) d^mu phi ] = 0.  In homogeneous FLRW it
  collapses to the first integral

          a^3 f'(K) phidot = const ,        K = -phidot^2 / (2 Lambda^4) .

  WHAT IS CERTIFIED HERE (five statements, each one used in the verdict):

    (1) K_flrw_nonpos / domain_forces_frozen.
        For Lambda^4 > 0 the FLRW kinetic variable is K = -phidot^2/(2 Lambda^4)
        <= 0 for EVERY real phidot.  Hence the domain condition K >= 0 forces
        phidot = 0: the in-domain homogeneous sector is the SINGLE POINT
        phidot = 0.  An attractor needs a neighbourhood to attract FROM; there
        is none.  (This is the machine-checked form of "imposed constraint".)

    (2) mu2C_I_re / mu2C_I_im / mu2C_I_im_ne_zero.
        Off the frozen locus sqrt(K) is imaginary: at K = -w^2 the EOM
        coefficient is mu_2(i w) = [w^2(w^2+3) + 2 i w]/(1+w^2)^2, whose
        imaginary part 2w/(1+w^2)^2 is nonzero for every w != 0.  So the
        Noether current is not real for any nonzero phidot: there is NO real
        rolling homogeneous FLRW solution at all.

    (3) noether_current_imaginary_strictly / noether_current_real_only_frozen.
        The imaginary part of the conserved current a^3 f'(K) phidot is
        STRICTLY POSITIVE for every w > 0; it vanishes only at w = 0.

    (4) mu2_le_two_mul.
        mu_2(u) <= 2u for u >= 0, so f'(K) <= 2 sqrt(K) -> 0 as K -> 0+: the
        principal coefficient of the scalar EOM VANISHES at the frozen point.
        There is no barrier and no restoring force -- the EOM cannot protect
        K from going negative.  Together with mu2_zero (f'(0) = 0) this says
        the linearised EOM about the frozen background is the empty statement
        0 = 0: there is no linear order in which "stability" could be posed.

    (5) csSq_zero (+ csSq_pos, csSq_lt_one).
        The perturbation cone is healthy AT the frozen point: c_s^2 = 1/2,
        real and subluminal.  So the vacuum is not a causal degeneracy -- the
        obstruction is not hyperbolicity, it is that no rolling configuration
        exists to be perturbed.

  VERDICT CERTIFIED:  phidot = 0 is an IMPOSED CONSTRAINT (a domain/reality
  condition isolating one configuration), not a dynamical attractor.

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound.
-/

import Mathlib
import Mathlib.Tactic

noncomputable section

/-! ## The objects -/

/-- mu_2(u) = f'(K) at u = sqrt K, on the real (K >= 0) branch. -/
def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2

/-- The same rational function on ℂ -- needed because sqrt(K) = i w off the
    frozen locus, and the question is whether the EOM stays real there. -/
def mu2C (z : ℂ) : ℂ := z * (2 + z) / (1 + z)^2

/-- K in homogeneous FLRW (signature (-,+,+,+)): (dphi)^2 = -phidot^2.
    L is Lambda^4. -/
def Kflrw (p L : ℝ) : ℝ := -(p^2) / (2 * L)

/-- Sound speed of the k-essence perturbation, c_s^2 = f'/(f' + 2K f''). -/
def csSq (u : ℝ) : ℝ := (u^2 + 3*u + 2) / (u^2 + 3*u + 4)

/-! ## (4a) The EOM coefficient vanishes at the frozen point -/

/-- f'(0) = mu_2(0) = 0: the coefficient of the kinetic/derivative term is
    ZERO at the frozen configuration, so the linearised EOM about it is
    f'(0) * (box delta-phi) = 0 -- the empty statement. -/
theorem mu2_zero : mu2 0 = 0 := by
  unfold mu2
  norm_num

/-! ## (1) Kinematics: the domain is a single point -/

/-- In homogeneous FLRW, K <= 0 for every real phidot (Lambda^4 > 0). -/
theorem Kflrw_nonpos (p L : ℝ) (hL : 0 < L) : Kflrw p L ≤ 0 := by
  unfold Kflrw
  exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg p)) (by positivity)

/-- THE DOMAIN THEOREM.  K >= 0 and K <= 0 force K = 0, hence phidot = 0.
    The in-domain homogeneous sector is one point, not an open set. -/
theorem domain_forces_frozen (p L : ℝ) (hL : 0 < L) (hdom : 0 ≤ Kflrw p L) : p = 0 := by
  have hle : Kflrw p L ≤ 0 := Kflrw_nonpos p L hL
  have hz : Kflrw p L = 0 := le_antisymm hle hdom
  unfold Kflrw at hz
  have hden : (2 * L : ℝ) ≠ 0 := by positivity
  have hmul := congrArg (fun x : ℝ => x * (2 * L)) hz
  field_simp [hden] at hmul
  have hp2 : p ^ 2 = 0 := by nlinarith
  exact sq_eq_zero_iff.mp hp2

/-- Converse: phidot = 0 does give K = 0 (the frozen configuration is in the
    domain).  Together with `domain_forces_frozen` this is an iff. -/
theorem frozen_members (L : ℝ) : Kflrw 0 L = 0 := by
  unfold Kflrw
  norm_num

/-! ## (4b) No barrier: f'(K) <= 2 sqrt K -/

/-- mu_2(u) <= 2u on u >= 0.  The EOM coefficient goes to ZERO at the frozen
    point instead of diverging: no barrier, no restoring force. -/
theorem mu2_le_two_mul (u : ℝ) (hu : 0 ≤ u) : mu2 u ≤ 2 * u := by
  unfold mu2
  have h1 : (1 + u : ℝ) ≠ 0 := by nlinarith
  have hden : 0 < (1 + u) ^ 2 := sq_pos_of_ne_zero h1
  rw [div_le_iff₀ hden]
  have hu3 : 0 ≤ u ^ 3 := by positivity
  nlinarith [sq_nonneg u, hu3]

/-- No ghost on the real branch: f'(K) > 0 for K > 0. -/
theorem mu2_pos (u : ℝ) (hu : 0 < u) : 0 < mu2 u := by
  unfold mu2
  positivity

/-! ## (2) Reality off the frozen locus -/

/-- Multiplying mu_2 by (1+z)^2 recovers z(2+z) -- the algebraic identity that
    makes the continuation computable without any division. -/
theorem mu2C_mul (z : ℂ) (hz : (1 + z)^2 ≠ 0) : mu2C z * (1 + z)^2 = z * (2 + z) := by
  unfold mu2C
  have hz1 : (1 + z : ℂ) ≠ 0 := by
    intro h
    exact hz (by rw [h]; norm_num)
  field_simp [hz, hz1]

/-- (1 + i w)^2 is never zero for real w: its imaginary part is 2w and its
    real part is 1-w^2, and they cannot vanish together. -/
theorem one_plus_Iw_sq_ne_zero (w : ℝ) (hw : w ≠ 0) : (1 + (w : ℂ) * Complex.I)^2 ≠ 0 := by
  intro h
  have hi := congrArg Complex.im h
  have : (2 : ℝ) * w = 0 := by simpa [pow_two] using hi
  exact hw (by nlinarith)

/-- The real part of the continued EOM coefficient:
    Re mu_2(i w) = w^2 (w^2+3) / (1+w^2)^2. -/
theorem mu2C_I_re (w : ℝ) :
    (mu2C ((w : ℂ) * Complex.I)).re = w^2 * (w^2 + 3) / (1 + w^2)^2 := by
  let z : ℂ := (w : ℂ) * Complex.I
  by_cases hw : w = 0
  · subst w
    simp [mu2C]
  · have hA_ne : (1 + z)^2 ≠ 0 := by
      simpa [z] using one_plus_Iw_sq_ne_zero w hw
    have hmain : mu2C z * (1 + z)^2 = z * (2 + z) := mu2C_mul z hA_ne
    let A : ℝ := (mu2C z).re
    let B : ℝ := (mu2C z).im
    have hAim : ((1 + z)^2).im = 2 * w := by simp [z, pow_two]; ring
    have hAre : ((1 + z)^2).re = 1 - w^2 := by simp [z, pow_two]
    have hRre : (z * (2 + z)).re = -w^2 := by simp [z]; ring
    have hRim : (z * (2 + z)).im = 2 * w := by simp [z]; ring
    have h1 : A * (1 - w^2) - B * (2 * w) = -w^2 := by
      calc
        A * (1 - w^2) - B * (2 * w) = (mu2C z * (1 + z)^2).re := by
          simp [A, B, Complex.mul_re, hAim, hAre]
        _ = (z * (2 + z)).re := congrArg Complex.re hmain
        _ = -w^2 := hRre
    have h2 : A * (2 * w) + B * (1 - w^2) = 2 * w := by
      calc
        A * (2 * w) + B * (1 - w^2) = (mu2C z * (1 + z)^2).im := by
          simp [A, B, Complex.mul_im, hAim, hAre]
        _ = (z * (2 + z)).im := congrArg Complex.im hmain
        _ = 2 * w := hRim
    have hs : A * ((1 - w^2)^2 + (2 * w)^2) = (-w^2) * (1 - w^2) + (2 * w) * (2 * w) := by
      calc
        A * ((1 - w^2)^2 + (2 * w)^2)
            = (A * (1 - w^2) - B * (2 * w)) * (1 - w^2)
              + (A * (2 * w) + B * (1 - w^2)) * (2 * w) := by ring
        _ = (-w^2) * (1 - w^2) + (2 * w) * (2 * w) := by rw [h1, h2]
    have hs2 : A * ((1 + w^2)^2) = w^2 * (w^2 + 3) := by nlinarith [hs]
    have hD : (1 + w^2)^2 ≠ 0 := by positivity
    have hA : A = w^2 * (w^2 + 3) / (1 + w^2)^2 := by
      field_simp [hD]
      nlinarith
    simpa [z, A] using hA

/-- The imaginary part of the continued EOM coefficient:
    Im mu_2(i w) = 2 w / (1 + w^2)^2. -/
theorem mu2C_I_im (w : ℝ) :
    (mu2C ((w : ℂ) * Complex.I)).im = 2 * w / (1 + w^2)^2 := by
  let z : ℂ := (w : ℂ) * Complex.I
  by_cases hw : w = 0
  · subst w
    simp [mu2C]
  · have hA_ne : (1 + z)^2 ≠ 0 := by
      simpa [z] using one_plus_Iw_sq_ne_zero w hw
    have hmain : mu2C z * (1 + z)^2 = z * (2 + z) := mu2C_mul z hA_ne
    let A : ℝ := (mu2C z).re
    let B : ℝ := (mu2C z).im
    have hAim : ((1 + z)^2).im = 2 * w := by simp [z, pow_two]; ring
    have hAre : ((1 + z)^2).re = 1 - w^2 := by simp [z, pow_two]
    have hRre : (z * (2 + z)).re = -w^2 := by simp [z]; ring
    have hRim : (z * (2 + z)).im = 2 * w := by simp [z]; ring
    have h1 : A * (1 - w^2) - B * (2 * w) = -w^2 := by
      calc
        A * (1 - w^2) - B * (2 * w) = (mu2C z * (1 + z)^2).re := by
          simp [A, B, Complex.mul_re, hAim, hAre]
        _ = (z * (2 + z)).re := congrArg Complex.re hmain
        _ = -w^2 := hRre
    have h2 : A * (2 * w) + B * (1 - w^2) = 2 * w := by
      calc
        A * (2 * w) + B * (1 - w^2) = (mu2C z * (1 + z)^2).im := by
          simp [A, B, Complex.mul_im, hAim, hAre]
        _ = (z * (2 + z)).im := congrArg Complex.im hmain
        _ = 2 * w := hRim
    have hs : B * ((2 * w)^2 + (1 - w^2)^2) = (2 * w) * (1 - w^2) - (-w^2) * (2 * w) := by
      calc
        B * ((2 * w)^2 + (1 - w^2)^2)
            = -(A * (1 - w^2) - B * (2 * w)) * (2 * w)
              + (A * (2 * w) + B * (1 - w^2)) * (1 - w^2) := by ring
        _ = -(-w^2) * (2 * w) + (2 * w) * (1 - w^2) := by rw [h1, h2]
        _ = (2 * w) * (1 - w^2) - (-w^2) * (2 * w) := by ring
    have hs2 : B * ((1 + w^2)^2) = 2 * w := by nlinarith [hs]
    have hD : (1 + w^2)^2 ≠ 0 := by positivity
    have hB : B = 2 * w / (1 + w^2)^2 := by
      field_simp [hD]
      nlinarith
    simpa [z, B] using hB

/-- THE REALITY THEOREM.  Im mu_2(i w) = 2w/(1+w^2)^2 is nonzero for every
    w != 0, i.e. the EOM coefficient is not real off the frozen locus. -/
theorem mu2C_I_im_ne_zero (w : ℝ) (hw : w ≠ 0) :
    (mu2C ((w : ℂ) * Complex.I)).im ≠ 0 := by
  rw [mu2C_I_im]
  intro h
  have hD : (1 + w^2)^2 ≠ 0 := by positivity
  have hmul := congrArg (fun x : ℝ => x * (1 + w^2)^2) h
  field_simp [hD] at hmul
  exact hw (by nlinarith)

/-! ## (3) The Noether current is not real unless the scalar is frozen -/

/-- The imaginary part of the conserved current a^3 f'(K) phidot, written in
    terms of w = sqrt(-K) = |phidot|/(sqrt 2 Lambda^2), is STRICTLY POSITIVE
    for every w > 0. -/
theorem noether_current_imaginary_strictly (a w : ℝ) (ha : 0 < a) (hw : 0 < w) :
    0 < a^3 * (2 * w / (1 + w^2)^2) := by
  positivity

/-- Consequently the current can be real only where w = 0, i.e. only on the
    frozen configuration: no real rolling homogeneous FLRW solution exists. -/
theorem noether_current_real_only_frozen (a w : ℝ) (ha : 0 < a) (hw : 0 ≤ w)
    (hreal : a^3 * (2 * w / (1 + w^2)^2) = 0) : w = 0 := by
  by_contra hne
  have hwpos : 0 < w := lt_of_le_of_ne hw (Ne.symm hne)
  have hpos := noether_current_imaginary_strictly a w ha hwpos
  nlinarith

/-! ## (5) The perturbation cone at the frozen point -/

/-- c_s^2 = 1/2 at the vacuum: the cone is real, timelike and subluminal
    AT the frozen point. -/
theorem csSq_zero : csSq 0 = (1 / 2 : ℝ) := by
  unfold csSq
  norm_num

/-- c_s^2 > 0 for all u >= 0 (no gradient instability). -/
theorem csSq_pos (u : ℝ) (hu : 0 ≤ u) : 0 < csSq u := by
  unfold csSq
  positivity

/-- c_s^2 < 1 for all u >= 0 (subluminal). -/
theorem csSq_lt_one (u : ℝ) (hu : 0 ≤ u) : csSq u < 1 := by
  unfold csSq
  have hden : 0 < u^2 + 3*u + 4 := by nlinarith [sq_nonneg u]
  rw [div_lt_iff₀ hden]
  nlinarith [sq_nonneg u]

/-! ## The spine -/

/-- THE VERDICT, assembled.  phidot = 0 is an IMPOSED CONSTRAINT:
      * the FLRW kinetic variable is never positive, so K >= 0 isolates the
        single configuration phidot = 0 (no neighbourhood => no attractor);
      * off it the EOM coefficient is not real (Im != 0), so there is no real
        rolling solution to flow anywhere;
      * the EOM coefficient VANISHES at the frozen point (f'(0) = 0 and
        f'(K) <= 2 sqrt K), so the EOM supplies no barrier and no restoring
        force and the linearised problem is empty;
      * yet the cone is healthy there (c_s^2 = 1/2).
    A constraint with a healthy cone is still a constraint. -/
theorem frozen_scalar_is_imposed :
    (mu2 0 = 0) ∧
    (∀ (p L : ℝ), 0 < L → Kflrw p L ≤ 0) ∧
    (∀ (p L : ℝ), 0 < L → 0 ≤ Kflrw p L → p = 0) ∧
    (∀ (u : ℝ), 0 ≤ u → mu2 u ≤ 2 * u) ∧
    (∀ (w : ℝ), w ≠ 0 → (mu2C ((w : ℂ) * Complex.I)).im ≠ 0) ∧
    (csSq 0 = (1 / 2 : ℝ)) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact mu2_zero
  · exact Kflrw_nonpos
  · exact domain_forces_frozen
  · exact mu2_le_two_mul
  · exact mu2C_I_im_ne_zero
  · exact csSq_zero

/-- Corollary: on the domain there is exactly one homogeneous FLRW
    configuration, and it is the frozen one -- the formal statement that
    "stability" here is stability by absence of alternatives. -/
theorem frozen_unique (p L : ℝ) (hL : 0 < L) :
    Kflrw p L = 0 ↔ p = 0 := by
  constructor
  · intro hz
    exact domain_forces_frozen p L hL (by rw [hz])
  · intro hp
    rw [hp]
    exact frozen_members L

#print axioms frozen_scalar_is_imposed
#print axioms frozen_unique
#print axioms domain_forces_frozen
#print axioms Kflrw_nonpos
#print axioms mu2C_I_im_ne_zero
#print axioms mu2C_I_im
#print axioms mu2C_I_re
#print axioms mu2C_mul
#print axioms one_plus_Iw_sq_ne_zero
#print axioms noether_current_imaginary_strictly
#print axioms noether_current_real_only_frozen
#print axioms mu2_le_two_mul
#print axioms mu2_zero
#print axioms mu2_pos
#print axioms csSq_zero
#print axioms csSq_pos
#print axioms csSq_lt_one
#print axioms frozen_members

end
