/-
DCN1 (fable52_push/DCN1_disc_centre_null): structural statements behind Part A (criteria d603f1703c, section 6).
  rate_identity   : with mu = u/(1+u), 4 pi G rho = mu L + mu'(u) Q (Q = grad u . grad Phi = u Phi_nn) and
                    4 pi G D.P = L/(1+u) - Q/(1+u)^2, route L's rate -4 pi G D.P u (2+u) equals (2+u)(Q/(1+u) - 4 pi G rho).
  slab_null / sphere_null : at a null (u -> 0) the rate is 2 (Q0 - s); the slab (Q0 = s/2) gives -s, the sphere
                    (Q0 = s/6) gives -(5/3) s; both negative for s > 0 (decay, not growth).
  raw_switch_zero : the raw stiffness -(gamma/2) max(Sigma,0)^2 vanishes for Sigma <= 0 (the blend equals it there).
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace DCN1

theorem rate_identity (u L Q : ℝ) (hu : 0 < u) :
    -(L / (1 + u) - Q / (1 + u) ^ 2) * (u * (2 + u))
      = (2 + u) * (Q / (1 + u) - (u / (1 + u) * L + Q / (1 + u) ^ 2)) := by
  have h1 : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

theorem slab_null (s : ℝ) : 2 * (s / 2 - s) = -s := by ring

theorem sphere_null (s : ℝ) : 2 * (s / 6 - s) = -(5 / 3) * s := by ring

theorem slab_null_neg (s : ℝ) (hs : 0 < s) : 2 * (s / 2 - s) < 0 := by linarith

theorem sphere_null_neg (s : ℝ) (hs : 0 < s) : 2 * (s / 6 - s) < 0 := by linarith

theorem raw_switch_zero (γ sig : ℝ) (h : sig ≤ 0) : -(γ / 2) * (max sig 0) ^ 2 = 0 := by
  rw [max_eq_right h]; ring

end DCN1

#print axioms DCN1.rate_identity
#print axioms DCN1.slab_null
#print axioms DCN1.sphere_null
#print axioms DCN1.slab_null_neg
#print axioms DCN1.sphere_null_neg
#print axioms DCN1.raw_switch_zero
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
