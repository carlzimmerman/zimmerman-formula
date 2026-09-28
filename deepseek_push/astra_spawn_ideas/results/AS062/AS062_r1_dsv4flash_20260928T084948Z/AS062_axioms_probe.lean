import Mathlib

/-!
AS062 -- Spherical source normalization and Gauss flux: Lean certificate.

Certified content (MU2 branch, kappa = 1/2 adopted so that s = 2 a0):

  mu2(Y)   = 1 - 1/(1+Y)^2                       (unit-slope two-channel response)
  g        = s Y = 2 a0 Y                        (field normalized by the vacuum rate)
  B        = mu2(Y) * g                          (integrated radial equation  mu2*g = B
                                                  after the 4*pi of the sphere area
                                                  cancels the 4*pi of the source coupling:
                                                  4 pi R^2 mu2 g = 4 pi G M_b  <=>  R^2 mu2 g = G M_b)

  T1 flux_ratio:       g^2 = a0 B (1 + Y(3+2Y)/(2+Y))     -- EXACT for every Y > 0.
                       The 4*pi never reaches the deep coefficient: the deep identity
                       g^2 -> a0 B (v_flat^4 = G M_b a0) carries correction
                       Y(3+2Y)/(2+Y), leading term (3/2)Y.
  T2 correction_bound: (3/2)Y < Y(3+2Y)/(2+Y) < 2Y         -- the leading term is
                       exactly the (3/2)Y of the MU2 deep expansion.
  T3 newtonian_tail:   mu2(Y) * (1 + 1/(Y(Y+2))) = 1, i.e. g/B = 1 + 1/(Y^2+2Y):
                       Newtonian recovery with relative correction 1/Y^2.
  T4 wrong_kappa:      4*pi ≠ 1.  Under the negative control (source coupling
                       G M_b WITHOUT the 4*pi, sphere area kept) the deep law reads
                       g^2 = a0 B / (4 pi), i.e. kappa_eff = kappa/(4 pi) with
                       kappa = 1/2: kappa_eff = 1/(8 pi) ≠ 1/2.  T4 certifies the
                       contraction 4 pi ≠ 1 that makes the control detectable.

These are algebraic identities of the definitions; their physics content is
bounded by the semantic mapping stated in derivation.md (the flux integral,
the MU2 branch, adopted kappa = 1/2).  No filtering, no MONO transfer.
-/

noncomputable def mu2 (Y : ℝ) : ℝ := 1 - 1 / ((1 + Y) * (1 + Y))

theorem flux_ratio (a0 Y : ℝ) (ha0 : 0 < a0) (hY : 0 < Y) :
    (2 * a0 * Y) * (2 * a0 * Y) =
      a0 * (mu2 Y * (2 * a0 * Y)) * (1 + Y * (3 + 2 * Y) / (2 + Y)) := by
  unfold mu2
  have h1p : (1 : ℝ) + Y ≠ 0 := by positivity
  have h2p : (2 : ℝ) + Y ≠ 0 := by positivity
  field_simp [ha0.ne', hY.ne', h1p, h2p]
  ring

theorem correction_bound (Y : ℝ) (hY : 0 < Y) :
    (3 / 2 : ℝ) * Y < Y * (3 + 2 * Y) / (2 + Y) ∧
      Y * (3 + 2 * Y) / (2 + Y) < 2 * Y := by
  have hpos2 : 0 < (2 : ℝ) + Y := by positivity
  constructor
  · have heqL : (3 / 2 : ℝ) * Y = (3 / 2 : ℝ) * Y * (2 + Y) / (2 + Y) := by
      field_simp [hpos2.ne']
    rw [heqL]
    rw [div_lt_iff₀ hpos2]
    rw [div_mul_cancel₀ (Y * (3 + 2 * Y)) hpos2.ne']
    nlinarith [hY]
  · rw [div_lt_iff₀ hpos2]
    nlinarith [hY]

theorem newtonian_tail (Y : ℝ) (hY : 0 < Y) :
    mu2 Y * (1 + 1 / (Y * (Y + 2))) = 1 := by
  unfold mu2
  have h1p : (1 : ℝ) + Y ≠ 0 := by positivity
  have hz : Y * (Y + 2) ≠ 0 := by positivity
  field_simp [h1p, hz]
  ring

theorem wrong_kappa : (2 : ℝ) * (2 * Real.pi) ≠ 1 := by
  have hpi : (3 : ℝ) < Real.pi := Real.pi_gt_three
  have hbig : (1 : ℝ) < 2 * (2 * Real.pi) := by nlinarith [hpi]
  exact ne_of_gt hbig

/-! Axiom hygiene: the four theorems above are the only claims.  No sorry. -/
#print axioms flux_ratio
#print axioms correction_bound
#print axioms newtonian_tail
#print axioms wrong_kappa
