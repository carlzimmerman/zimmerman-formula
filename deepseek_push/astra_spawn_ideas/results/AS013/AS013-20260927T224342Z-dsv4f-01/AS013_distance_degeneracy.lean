import Mathlib

open scoped Real

/-!
# AS013 — a distance scaling degeneracy of the deep law (Lean certificate)

Certified content (all variables real; the physical variables are positive in the
applications, but the first three identities and the composition identity hold as
pure field statements with the stated nonzero declarations):

T1 `deep_product_invariance`   :  v^4 = G*M*a  is EXACTLY invariant under the
    distance rescaling (M, a) -> (lam^2 * M, a / lam^2)  [M ∝ D^2 at fixed flux].
T2 `combined_invariance`       :  the same product with the inclination factor,
    v_los^4 = (sin i)^4 * G*M*a, is invariant under
    (sin i, M, a) -> (s*sin i, lam^2*M, a/(lam^2 * s^4)).
T3 `mond_radius_scaling_law`   :  if r_M^2 = G*M/a  then the rescaled radius obeys
    (lam^2 * r_M)^2 = G*(lam^2*M)/(a/lam^2)  —  "r_M -> lam^2 * r_M".
T4 `orbit_composition`         :  the rescaling maps compose as a one-parameter
    group,  R(lam2) ∘ R(lam1) = R(lam1*lam2).
T5 `q_break_identity`          :  for the Q branch, the exact finite-y break is
    v'^4/v^4 - 1 = y*(lam^2 - 1)/(y + 1)  (the deep-limit leading neglected term
    y*(lam^2-1) up to -(lam^2-1)*y^2).
T6 `orbit_characterization`    :  PINNING. If two positive deep-law models share one
    flat velocity,  G*M*a = G*M'*a', then they differ exactly by an orbit element:
    with lam := sqrt(M'/M) > 0,  M' = lam^2*M  and  a' = a/lam^2.  Hence from the
    deep plateau alone the product M*a is determined; the  individual  M and a are
    not (one-parameter family), and a' = a/lam^2 is exactly the task's
    "a0 ∝ D^(-2) at fixed velocity".
-/

namespace AS013

theorem deep_product_invariance (G M a lam : ℝ) (hlam : lam ≠ 0) :
    G * M * a = G * (lam ^ 2 * M) * (a / lam ^ 2) := by
  field_simp [hlam]

theorem combined_invariance (G M a s lam sinI : ℝ)
    (hlam : lam ≠ 0) (hs : s ≠ 0) :
    G * M * a * (sinI ^ 4) =
      G * (lam ^ 2 * M) * (a / (lam ^ 2 * s ^ 4)) * ((s * sinI) ^ 4) := by
  field_simp [hlam, hs]

theorem mond_radius_scaling_law (G M a lam r : ℝ)
    (hdef : r ^ 2 = G * M / a) (hl : lam ≠ 0) :
    (lam ^ 2 * r) ^ 2 = G * (lam ^ 2 * M) / (a / lam ^ 2) := by
  calc
    (lam ^ 2 * r) ^ 2 = lam ^ 4 * r ^ 2 := by ring
    _ = lam ^ 4 * (G * M / a) := by rw [hdef]
    _ = G * (lam ^ 2 * M) / (a / lam ^ 2) := by
      by_cases ha : a = 0
      · subst a
        simp
      · field_simp [hl, ha]

theorem orbit_composition (M a lam1 lam2 : ℝ)
    (h1 : lam1 ≠ 0) (h2 : lam2 ≠ 0) :
    (lam2 ^ 2 * (lam1 ^ 2 * M)) = (lam1 * lam2) ^ 2 * M ∧
      (a / lam1 ^ 2) / lam2 ^ 2 = a / (lam1 * lam2) ^ 2 := by
  constructor
  · ring
  · by_cases ha : a = 0
    · subst a
      simp
    · field_simp [h1, h2, ha]

theorem q_break_identity (lam y : ℝ) (hy : y + 1 ≠ 0) :
    (lam ^ 2 * y + 1) / (y + 1) - 1 = y * (lam ^ 2 - 1) / (y + 1) := by
  field_simp [hy]; ring

theorem orbit_characterization (G M a M' a' lam : ℝ)
    (hG : G ≠ 0) (hM : 0 < M) (hM' : 0 < M')
    (hlam : lam = Real.sqrt (M' / M))
    (hp : G * M * a = G * M' * a') :
    M' = lam ^ 2 * M ∧ a' = a / lam ^ 2 := by
  subst lam
  have hMn : M ≠ 0 := ne_of_gt hM
  have hMpn : M' ≠ 0 := ne_of_gt hM'
  have hdiv : 0 ≤ M' / M := by
    exact le_of_lt (div_pos hM' hM)
  have hsq : Real.sqrt (M' / M) ^ 2 = M' / M := Real.sq_sqrt hdiv
  have hratio : a' = a * M / M' := by
    calc
      a' = (G * M * a) / (G * M') := by
        rw [hp]
        field_simp [hG, hMpn]
      _ = a * M / M' := by
        field_simp [hG, hMpn, hMn]
  constructor
  · calc
      M' = (M' / M) * M := by field_simp [hMn]
      _ = Real.sqrt (M' / M) ^ 2 * M := by rw [hsq]
  · calc
      a' = a * M / M' := hratio
      _ = a / (M' / M) := by field_simp [hMn, hMpn]
      _ = a / Real.sqrt (M' / M) ^ 2 := by rw [hsq]

#print axioms deep_product_invariance
#print axioms combined_invariance
#print axioms mond_radius_scaling_law
#print axioms orbit_composition
#print axioms q_break_identity
#print axioms orbit_characterization

end AS013