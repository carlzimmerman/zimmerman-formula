/-
FINAL6 (KAPPA): the Buckingham closure that carries the lane's positive half. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

Claim (K1).  Take the dimensionful data the formation event offers: Newton's G, the clock speed c, a cosmic
density rho_*, and the host's baryonic mass M.  Every monomial G^a c^b rho^g M^m that carries the
dimension of an acceleration forms a ONE-parameter family

        (a, b, g, m) = (3t - 1, 4 - 6t, t, 2t - 1),     t rational,

i.e.   a_0 = c sqrt(G rho_*) * ( G^3 rho_* M^2 / c^6 )^p   with p = t - 1/2.
Requiring universality -- no memory of which galaxy it is, i.e. m = 0 -- forces p = 0, so

        a_0 = kappa c sqrt(G rho_*)        with kappa = Phi(dimensionless formation data) a pure number.

That is the whole output of the formation reading: it fixes the FORM and (because a frozen normalisation
must not drift) picks rho_* = rho_Lambda.  It does not evaluate Phi, and Phi is kappa.
-/

import Mathlib

/-- Exponents of a monomial in (G, c, rho, M).  [G] = L^3 M^-1 T^-2, [c] = L T^-1, [rho] = M L^-3, [M] = M. -/
structure Exp where
  G   : Rat
  c   : Rat
  rho : Rat
  M   : Rat

namespace FINAL6

def dimL (e : Exp) : Rat := 3 * e.G + 1 * e.c - 3 * e.rho + 0 * e.M
def dimM (e : Exp) : Rat := (-1) * e.G + 0 * e.c + 1 * e.rho + 1 * e.M
def dimT (e : Exp) : Rat := (-2) * e.G + (-1) * e.c + 0 * e.rho + 0 * e.M

def IsAcceleration (e : Exp) : Prop := dimL e = 1 ∧ dimM e = 0 ∧ dimT e = -2

/-- The family: an exponent vector gives an acceleration iff it lies on the affine line above. -/
theorem accel_family (e : Exp) :
    IsAcceleration e ↔
      ∃ t : Rat, e.G = 3 * t - 1 ∧ e.c = 4 - 6 * t ∧ e.rho = t ∧ e.M = 2 * t - 1 := by
  constructor
  · rintro ⟨hL, hM, hT⟩
    dsimp [dimL, dimM, dimT] at hL hM hT
    refine ⟨e.rho, ?_, ?_, rfl, ?_⟩
    · linarith
    · linarith
    · linarith
  · rintro ⟨t, hG, hc, hr, hM⟩
    unfold IsAcceleration dimL dimM dimT
    rw [hG, hc, hr, hM]
    exact ⟨by ring, by ring, by ring⟩

/-- Universality (mass-independence) selects exactly one member of the family. -/
theorem mass_free_unique (e : Exp) (h : IsAcceleration e) (hm : e.M = 0) :
    e.G = (1/2 : Rat) ∧ e.c = 1 ∧ e.rho = (1/2 : Rat) := by
  rcases (accel_family e).mp h with ⟨t, hG, hc, hr, hM⟩
  have ht : t = (1/2 : Rat) := by linarith
  subst t
  exact ⟨by linarith, by linarith, by linarith⟩

/-- The residual mass-dependence sits in one dimensionless invariant,
    w = (G M sqrt(G rho_*)/c^3)^2 = G^3 rho_* M^2 / c^6.  Setting its exponent to zero is exactly the
    universality statement a_0 = Phi * c sqrt(G rho_*) with Phi = kappa a pure number. -/
theorem invariant_exponent_zero (c G rho M : ℝ) :
    (G ^ 3 * rho * M ^ 2 / c ^ 6) ^ (0 : Nat) = 1 := by
  norm_num

end FINAL6
