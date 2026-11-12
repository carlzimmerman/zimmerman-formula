/-
  FINAL-16 (KAPPA_REAL) -- the two EXACT statements the lane's no-go rests on.

  F1 (formation reading): the settled charge-to-baryon ratio is fixed at the
  assembly event and conserved afterwards,

      X = X_L(g ; a0) := ( sqrt(1 + 4 a0 / g) - 1 ) / 2 .

  (KA-3)  X_L is the positive root of      g X (1 + X) = a0 .
  (J1)    X_L is invariant under the simultaneous rescaling
              (a0, g) -> (lam*a0, lam*g),   lam > 0 .
          Hence G_lam is an exact symmetry of F1 (and of F3, which mentions no
          dimensionful formation datum at all), while kappa in
              a0 = kappa * c * sqrt(G rho_*)
          is the ONLY G_lam-charged quantity: kappa -> lam * kappa.  No
          G_lam-invariant built from the formation data can fix kappa, so kappa
          is a flat direction of the formation physics.

  TEST lane, quarantined.  Adopts nothing.
-/

import Mathlib

noncomputable section

/-- the formation law -/
def XL (a0 g : ℝ) : ℝ := (Real.sqrt (1 + 4 * a0 / g) - 1) / 2

/-- (KA-3)  g X (1 + X) = a0 : the formation relation is a quadratic,
    and X_L is its positive root. -/
theorem XL_quadratic (a0 g : ℝ) (ha0 : 0 < a0) (hg : 0 < g) :
    g * (XL a0 g) * (1 + XL a0 g) = a0 := by
  unfold XL
  set u : ℝ := Real.sqrt (1 + 4 * a0 / g)
  have hnonneg : 0 ≤ 1 + 4 * a0 / g := by positivity
  have hu2 : u ^ 2 = 1 + 4 * a0 / g := by
    rw [show u = Real.sqrt (1 + 4 * a0 / g) from rfl]
    exact Real.sq_sqrt hnonneg
  have hring : g * ((u - 1) / 2) * (1 + (u - 1) / 2) = g * (u ^ 2 - 1) / 4 := by
    ring
  rw [hring, hu2]
  field_simp [ne_of_gt hg]
  ring

/-- (J1 i)  scale covariance: the formation law cannot see the overall
    acceleration scale, because it only ever depends on the ratio a0/g. -/
theorem XL_covariant (a0 g lam : ℝ) (hg : g ≠ 0) (hl : lam ≠ 0) :
    XL (lam * a0) (lam * g) = XL a0 g := by
  unfold XL
  have h : 4 * (lam * a0) / (lam * g) = 4 * a0 / g := by
    field_simp [hl, hg]
    ring
  rw [h]

/-- (J1 ii)  the quadratic form carries weight 1 under the scaling, so the
    relation is preserved: (lam g) X' (1 + X') = lam * (g X (1+X)).
    Consequence: kappa -> lam * kappa.  kappa is the orbit coordinate. -/
theorem XL_quadratic_weight (a0 g lam : ℝ) (hg : g ≠ 0) (hl : lam ≠ 0) :
    (lam * g) * (XL (lam * a0) (lam * g)) * (1 + XL (lam * a0) (lam * g))
      = lam * (g * (XL a0 g) * (1 + XL a0 g)) := by
  rw [XL_covariant a0 g lam hg hl]
  ring

/-- (J1 iii)  the ratio a0/g is G_lam-invariant -- the whole formation law is a
    function of this invariant alone, which is why no kappa can be extracted. -/
theorem ratio_invariant (a0 g lam : ℝ) (hg : g ≠ 0) (hl : lam ≠ 0) :
    (lam * a0) / (lam * g) = a0 / g := by
  field_simp [hl, hg]
  ring

end
