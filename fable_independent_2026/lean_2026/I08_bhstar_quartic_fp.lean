import Mathlib

/-!
# I08 — Wave Q: the Eddington quartic constant from first principles

SCOPE (per lean-math-certification): Lean certifies the ALGEBRA of the derivation —
the step that turns (i) the equation of state and (ii) the polytropic mass into the
quartic constant. The inputs are hypotheses (provenanced):

  EoS   (the first law + the beta definition):
        (1 - beta)/beta^4 = (a mu^4 mp^4 / (3 k^4)) * K^3
  MASS  (the n=3 Lane-Emden, u = (-xi_1^2 theta'_1) an absorbed atom, numerically
        verified 2.01826 in `bhstar_q1_quartic_first_principles.py`):
        K^3 = M^2 G^3 pi / (16 u^2)

CONCLUSION (pure field algebra, no roots anywhere):

  (1 - beta)/beta^4 = M^2 * (a mu^4 mp^4 G^3 pi / (48 k^4 u^2)) = M^2 / M_E^2

i.e. the Eddington standard-model quartic with the mass constant

  M_E = sqrt(48 k^4 u^2 / (a mu^4 mp^4 pi G^3)) = 48-52 Msun (mu = 0.59-0.61),

derived from G, k_B, a (the radiation constant), m_p, pi and the Lane-Emden zero —
ZERO fitted anchors — confirming the M1 calibrated anchor (53.8 Msun) to 3.8% and
re-anchoring the Wave N global-ceiling bracket by <= 2%. Numbers Python-verified
(5/5). Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **Q (the quartic constant).** From the EoS and the polytropic mass, pure algebra:
(1-beta)/beta^4 = M^2 / M_E^2 with 1/M_E^2 = a mu^4 mp^4 G^3 pi/(48 k^4 u^2). -/
theorem quartic_constant {a mu mp k G M K u beta : ℝ}
    (ha : 0 < a) (hmu : 0 < mu) (hmp : 0 < mp) (hk : 0 < k) (hG : 0 < G) (hK : 0 < K)
    (hu : 0 < u) (hbeta : 0 < beta)
    (heos : (1 - beta) / beta ^ 4 = (a * mu ^ 4 * mp ^ 4 / (3 * k ^ 4)) * K ^ 3)
    (hmass : K ^ 3 = M ^ 2 * G ^ 3 * π / (16 * u ^ 2)) :
    (1 - beta) / beta ^ 4 = M ^ 2 * (a * mu ^ 4 * mp ^ 4 * G ^ 3 * π / (48 * k ^ 4 * u ^ 2)) := by
  rw [heos, hmass]
  field_simp
  ring

end

#print axioms quartic_constant