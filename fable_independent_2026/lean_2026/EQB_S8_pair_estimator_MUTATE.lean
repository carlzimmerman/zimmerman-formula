import Mathlib

/-!
# EQB_S8 -- the distance-free, inclination-free pair estimator of a0 (Lean 4 certificate)

Source (committed): `prep_2026/equation_book/eqbook_S8_estimators.py`, checks E-S8.1 (lines 67-83, pair estimator, nuisance
cancellation, degeneracy guard), E-S8.2/8.3 (lines 85-94, distance and inclination estimators), E-S8.4 (lines 96-107, the
three-radius polygon); write-up `MINE_M1.md` item 2 and rows 6-7, 10.

PREMISES (declared, NOT certified as physics): (i) the framework law at each radius, g_j^2 = (U s_j)^2 + a0 (U s_j), where
U = Upsilon is the stellar mass-to-light factor and s_j the photometric shape (g_bar,j = U s_j, gas-dominated case U = 1 with s_j
the gas field); (ii) the observable model  v_j^2 = (sin i)^2 * D * theta_j * g_j  (v_los = v_true sin i, r_j = D theta_j,
g_j = v_true^2 / r_j).  D (distance) and sin i (inclination) are ARBITRARY positive reals: the conclusions hold for every
value, which IS the "distance- and inclination-free" statement.

CERTIFIED (premises => conclusions, exact algebra):
  * `pair_R_eq`        : R12 := (v1/v2)^4 (theta2/theta1)^2 = g_1^2 / g_2^2  (D and sin i cancel)
  * `pair_estimator`   : (s1^2 - R12 s2^2)/(R12 s2 - s1) = a0/U  whenever s1 != s2
  * `pair_denominator` : R12 s2 - s1 = U s1 (s1 - s2)/(U s2 + a0), so the denominator vanishes iff s1 = s2 (a degenerate pair)
  * `pair_gas`         : the gas-dominated case U = 1 returns a0 itself
  * `polygon`          : the pair estimates from radii (1,2) and (2,3) coincide, and the cross-multiplied pure-observable identity
                         (s1^2 - R12 s2^2)(R23 s3 - s2) = (s2^2 - R23 s3^2)(R12 s2 - s1) holds (tests the LAW with no a0, U, D, i)
  * `distance_estimator`, `inclination_estimator` : D = v^2/((sin i)^2 theta sqrt(g(g + a0))) with g = U s, and the analogous sin i^2
NOT certified: real-data systematics (asymmetric drift, warps, non-circular motion, disk geometry: the script says the estimator is
exact and the observable model is the approximation); that the estimator is well conditioned in practice (the script's SPARC fire found
2 usable gas-dominated pairs); the value of a0.  The "no closed form for McGaugh's nu" remark is a sympy observation, not a Lean statement.
kappa = 1/2 (FITTED) does not enter.
-/

open Real

noncomputable section

/-- R12 in pure observables. -/
def Rpair (v1 v2 θ1 θ2 : ℝ) : ℝ := (v1 / v2) ^ 4 * (θ2 / θ1) ^ 2

theorem pair_R_eq {v1 v2 θ1 θ2 D si g1 g2 : ℝ}
    (hθ1 : θ1 ≠ 0) (hθ2 : θ2 ≠ 0) (hD : D ≠ 0) (hsi : si ≠ 0) (hg2 : g2 ≠ 0)
    (m1 : v1 ^ 2 = si ^ 2 * D * θ1 * g1) (m2 : v2 ^ 2 = si ^ 2 * D * θ2 * g2) :
    Rpair v1 v2 θ1 θ2 = g1 ^ 2 / g2 ^ 2 := by
  unfold Rpair
  have e1 : v1 ^ 4 = (si ^ 2 * D * θ1 * g1) ^ 2 := by rw [← m1]; ring
  have e2 : v2 ^ 4 = (si ^ 2 * D * θ2 * g2) ^ 2 := by rw [← m2]; ring
  rw [div_pow, e1, e2]
  field_simp

/-- the law at a radius, for shape s and mass-to-light factor U. -/
def gLaw (a0 U s : ℝ) : ℝ := (U * s) ^ 2 + a0 * (U * s)

theorem pair_denominator {a0 U s1 s2 : ℝ} (ha : 0 < a0) (hU : 0 < U) (h1 : 0 < s1) (h2 : 0 < s2) :
    (gLaw a0 U s1 / gLaw a0 U s2) * s2 - s1 = U * s1 * (s1 - s2) / (U * s2 + a0) := by
  unfold gLaw
  have : U * s2 + a0 ≠ 0 := by positivity
  have : (U * s2) ^ 2 + a0 * (U * s2) ≠ 0 := by positivity
  field_simp
  ring

theorem pair_estimator {a0 U s1 s2 R : ℝ} (ha : 0 < a0) (hU : 0 < U) (h1 : 0 < s1) (h2 : 0 < s2)
    (hne : s1 ≠ s2) (hR : R = gLaw a0 U s1 / gLaw a0 U s2) :
    (s1 ^ 2 - R * s2 ^ 2) / (R * s2 - s1) = 2 * a0 / U := by
  have hden : R * s2 - s1 = U * s1 * (s1 - s2) / (U * s2 + a0) := by
    rw [hR]; exact pair_denominator ha hU h1 h2
  have hpos : U * s2 + a0 ≠ 0 := by positivity
  have hd0 : R * s2 - s1 ≠ 0 := by
    rw [hden]
    have : s1 - s2 ≠ 0 := sub_ne_zero.mpr hne
    positivity
  rw [div_eq_div_iff hd0 hU.ne']
  rw [hR]
  unfold gLaw
  have : (U * s2) ^ 2 + a0 * (U * s2) ≠ 0 := by positivity
  field_simp
  ring

/-- the full chain: from the observables and the two premises, the estimator returns a0/U for every D, sin i. -/
theorem pair_estimator_observables {a0 U s1 s2 v1 v2 θ1 θ2 D si : ℝ}
    (ha : 0 < a0) (hU : 0 < U) (h1 : 0 < s1) (h2 : 0 < s2) (hne : s1 ≠ s2)
    (hθ1 : θ1 ≠ 0) (hθ2 : θ2 ≠ 0) (hD : D ≠ 0) (hsi : si ≠ 0)
    (m1 : v1 ^ 2 = si ^ 2 * D * θ1 * Real.sqrt (gLaw a0 U s1))
    (m2 : v2 ^ 2 = si ^ 2 * D * θ2 * Real.sqrt (gLaw a0 U s2)) :
    ((s1 ^ 2 - Rpair v1 v2 θ1 θ2 * s2 ^ 2) / (Rpair v1 v2 θ1 θ2 * s2 - s1)) = a0 / U := by
  have hg1 : 0 < gLaw a0 U s1 := by unfold gLaw; positivity
  have hg2 : 0 < gLaw a0 U s2 := by unfold gLaw; positivity
  have hs2 : Real.sqrt (gLaw a0 U s2) ≠ 0 := (Real.sqrt_pos.mpr hg2).ne'
  have hR := pair_R_eq hθ1 hθ2 hD hsi hs2 m1 m2
  rw [Real.sq_sqrt hg1.le, Real.sq_sqrt hg2.le] at hR
  exact pair_estimator ha hU h1 h2 hne hR

theorem pair_gas {a0 s1 s2 R : ℝ} (ha : 0 < a0) (h1 : 0 < s1) (h2 : 0 < s2) (hne : s1 ≠ s2)
    (hR : R = gLaw a0 1 s1 / gLaw a0 1 s2) :
    (s1 ^ 2 - R * s2 ^ 2) / (R * s2 - s1) = a0 := by
  have := pair_estimator ha one_pos h1 h2 hne hR
  simpa using this

/-- the three-radius polygon: two independent pair estimates agree, in fact and in cross-multiplied form. -/
theorem polygon {a0 U s1 s2 s3 R12 R23 : ℝ} (ha : 0 < a0) (hU : 0 < U)
    (h1 : 0 < s1) (h2 : 0 < s2) (h3 : 0 < s3) (n12 : s1 ≠ s2) (n23 : s2 ≠ s3)
    (hR12 : R12 = gLaw a0 U s1 / gLaw a0 U s2) (hR23 : R23 = gLaw a0 U s2 / gLaw a0 U s3) :
    (s1 ^ 2 - R12 * s2 ^ 2) / (R12 * s2 - s1) = (s2 ^ 2 - R23 * s3 ^ 2) / (R23 * s3 - s2) ∧
    (s1 ^ 2 - R12 * s2 ^ 2) * (R23 * s3 - s2) = (s2 ^ 2 - R23 * s3 ^ 2) * (R12 * s2 - s1) := by
  have e12 := pair_estimator ha hU h1 h2 n12 hR12
  have e23 := pair_estimator ha hU h2 h3 n23 hR23
  refine ⟨by rw [e12, e23], ?_⟩
  have d12 : R12 * s2 - s1 = U * s1 * (s1 - s2) / (U * s2 + a0) := by
    rw [hR12]; exact pair_denominator ha hU h1 h2
  have d23 : R23 * s3 - s2 = U * s2 * (s2 - s3) / (U * s3 + a0) := by
    rw [hR23]; exact pair_denominator ha hU h2 h3
  have hd12 : R12 * s2 - s1 ≠ 0 := by
    rw [d12]; have : s1 - s2 ≠ 0 := sub_ne_zero.mpr n12
    have : U * s2 + a0 ≠ 0 := by positivity
    positivity
  have hd23 : R23 * s3 - s2 ≠ 0 := by
    rw [d23]; have : s2 - s3 ≠ 0 := sub_ne_zero.mpr n23
    have : U * s3 + a0 ≠ 0 := by positivity
    positivity
  have n1 : s1 ^ 2 - R12 * s2 ^ 2 = (a0 / U) * (R12 * s2 - s1) := by
    rw [div_eq_div_iff hd12 hU.ne'] at e12
    field_simp
    linarith
  have n2 : s2 ^ 2 - R23 * s3 ^ 2 = (a0 / U) * (R23 * s3 - s2) := by
    rw [div_eq_div_iff hd23 hU.ne'] at e23
    field_simp
    linarith
  rw [n1, n2]; ring

theorem distance_estimator {a0 U s θ D si v : ℝ} (hθ : θ ≠ 0) (hsi : si ≠ 0) (hg : 0 < gLaw a0 U s)
    (m : v ^ 2 = si ^ 2 * D * θ * Real.sqrt (gLaw a0 U s)) :
    D = v ^ 2 / (si ^ 2 * θ * Real.sqrt (gLaw a0 U s)) := by
  have hs : Real.sqrt (gLaw a0 U s) ≠ 0 := (Real.sqrt_pos.mpr hg).ne'
  rw [m]; field_simp

theorem inclination_estimator {a0 U s θ D si v : ℝ} (hθ : θ ≠ 0) (hD : D ≠ 0) (hg : 0 < gLaw a0 U s)
    (m : v ^ 2 = si ^ 2 * D * θ * Real.sqrt (gLaw a0 U s)) :
    si ^ 2 = v ^ 2 / (D * θ * Real.sqrt (gLaw a0 U s)) := by
  have hs : Real.sqrt (gLaw a0 U s) ≠ 0 := (Real.sqrt_pos.mpr hg).ne'
  rw [m]; field_simp

end

#print axioms pair_R_eq
#print axioms pair_denominator
#print axioms pair_estimator
#print axioms pair_estimator_observables
#print axioms pair_gas
#print axioms polygon
#print axioms distance_estimator
#print axioms inclination_estimator
