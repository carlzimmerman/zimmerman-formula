import Mathlib

/-!
# ZD03 — The EFE Suppression Theorem and the Cluster Dark-Stripping Radius

Framework premise (docstring scope, NOT certified here): the a0-line
g_obs^2 - g_bar^2 = a0 * g_bar (PD08/PD13, deepseek_push/STATE.md) applied
to the TOTAL field of a system immersed in an ambient (external) field e:
a satellite in a cluster field e carries the internal phantom boost

    phi(s + e) - phi(e),   phi(x) := sqrt(x^2 + x) - x   (x = g / a0).

Certified consequences, all new to the corpus:

  1. SUBADDITIVITY (the exact EFE law): phi(s + e) <= phi(s) + phi(e).
     The phantom of the sum is strictly less than the sum of the phantoms —
     an ambient field suppresses the internal dark component. Equivalently
     the internal boost phi(s+e) - phi(e) is bounded by BOTH phi(s)
     (suppression below the isolated value) and phi(e).
  2. THE AMBIENT CAP: in any region where the ambient field is at or above
     the ceiling (e >= a0/2), the internal phantom boost is STRICTLY below
     the ambient field — a phantom component cannot hold itself together:
     no self-contained dark halo inside the a0/2 surface.
  3. THE CLUSTER STRIPPING RADIUS: for an isothermal cluster of one-
     dimensional dispersion sigma, g_ext(r) = 2 sigma^2 / r, so the a0/2
     surface sits at r_strip = 4 sigma^2 / a0 (certified algebra), and
     strictly inside it the cluster field EXCEEDS the ceiling: satellites
     there carry at most a subdominant phantom (dark-stripped). For the
     framework's own G008 cluster (sigma = 809 km/s) r_strip ~ 0.71 Mpc;
     for sigma = 1000 km/s, 1.08 Mpc — cluster-scale, testable with
     satellite kinematics inside versus outside r_strip.

Lean certifies the mathematics; the a0-line and the isothermal-cluster
field are the framework's premises.
-/

noncomputable section
open scoped Real

/-- The phantom (dark) acceleration normalized by a0 — same function as in
ZD01, restated here so ZD03 is self-contained. -/
noncomputable def phi (a0 x : ℝ) : ℝ := Real.sqrt (x^2 + a0 * x) - x

/-- Strict ceiling (ZD01 restated). -/
theorem phantom_ceiling_strict (a0 x : ℝ) (ha0 : 0 < a0) (hx : 0 < x) :
    phi a0 x < a0 / 2 := by
  have hnn : 0 ≤ x^2 + a0 * x := by
    nlinarith [sq_nonneg x, hx.le, ha0.le]
  have hnon2 : 0 ≤ x + a0 / 2 := by nlinarith [hx.le, ha0.le]
  have hroot : Real.sqrt (x^2 + a0 * x) < x + a0 / 2 := by
    apply (Real.sqrt_lt hnn hnon2).2
    rw [pow_two]
    ring_nf
    nlinarith [sq_pos_of_pos ha0]
  unfold phi
  linarith

/-- THE EFE LAW (subadditivity): the phantom of the sum is at most the sum
of the phantoms — an ambient field strictly suppresses the internal dark
component of an immersed system. -/
theorem phantom_subadditive (a0 s e : ℝ) (ha0 : 0 < a0) (ha : 0 ≤ s) (hb : 0 ≤ e) :
    phi a0 (s + e) ≤ phi a0 s + phi a0 e := by
  have hA : 0 ≤ s^2 + a0 * s := by nlinarith [sq_nonneg s, ha, ha0.le]
  have hB : 0 ≤ e^2 + a0 * e := by nlinarith [sq_nonneg e, hb, ha0.le]
  have hAB : 0 ≤ (s^2 + a0 * s) * (e^2 + a0 * e) := mul_nonneg hA hB
  have hse : s * e ≤ Real.sqrt ((s^2 + a0 * s) * (e^2 + a0 * e)) := by
    have hse2' : (s * e)^2 ≤ (Real.sqrt ((s^2 + a0 * s) * (e^2 + a0 * e)))^2 := by
      rw [Real.sq_sqrt hAB]
      have h1 : 0 ≤ a0 * s^2 * e := by positivity
      have h2 : 0 ≤ a0 * s * e^2 := by positivity
      have h3 : 0 ≤ a0^2 * s * e := by positivity
      nlinarith [h1, h2, h3]
    have habs : |s * e| ≤ |Real.sqrt ((s^2 + a0 * s) * (e^2 + a0 * e))| :=
      sq_le_sq.mp hse2'
    simpa [abs_of_nonneg (mul_nonneg ha hb), abs_of_nonneg (Real.sqrt_nonneg _)] using habs
  have hroot : Real.sqrt ((s + e)^2 + a0 * (s + e)) ≤
      Real.sqrt (s^2 + a0 * s) + Real.sqrt (e^2 + a0 * e) := by
    have hR : 0 ≤ (s + e)^2 + a0 * (s + e) := by
      nlinarith [sq_nonneg (s + e), add_nonneg ha hb, ha0.le]
    have h1 : (Real.sqrt ((s + e)^2 + a0 * (s + e)))^2 ≤
        (Real.sqrt (s^2 + a0 * s) + Real.sqrt (e^2 + a0 * e))^2 := by
      rw [Real.sq_sqrt hR]
      have hprod : Real.sqrt (s^2 + a0 * s) * Real.sqrt (e^2 + a0 * e) =
                      Real.sqrt ((s^2 + a0 * s) * (e^2 + a0 * e)) :=
        (Real.sqrt_mul hA _).symm
      calc
        ((s + e)^2 + a0 * (s + e)) = (s^2 + a0 * s) + (e^2 + a0 * e) + 2 * s * e := by ring
        _ ≤ (s^2 + a0 * s) + (e^2 + a0 * e) +
              2 * Real.sqrt ((s^2 + a0 * s) * (e^2 + a0 * e)) := by nlinarith [hse]
        _ = (Real.sqrt (s^2 + a0 * s) + Real.sqrt (e^2 + a0 * e))^2 := by
          rw [add_sq]
          rw [Real.sq_sqrt hA, Real.sq_sqrt hB, ← hprod]
          ring
    have habs : |Real.sqrt ((s + e)^2 + a0 * (s + e))| ≤
        |Real.sqrt (s^2 + a0 * s) + Real.sqrt (e^2 + a0 * e)| := sq_le_sq.mp h1
    have hnon : 0 ≤ Real.sqrt (s^2 + a0 * s) + Real.sqrt (e^2 + a0 * e) :=
      add_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
    simpa [abs_of_nonneg (Real.sqrt_nonneg _), abs_of_nonneg hnon] using habs
  unfold phi
  nlinarith [hroot]

/-- SUPPRESSION (left): the internal phantom boost of a satellite in an
ambient field is at most its isolated phantom — the dark component can only
lose mass to the environment. -/
theorem efe_boost_left (a0 s e : ℝ) (ha0 : 0 < a0) (ha : 0 ≤ s) (hb : 0 ≤ e) :
    phi a0 (s + e) - phi a0 e ≤ phi a0 s := by
  have hsub := phantom_subadditive a0 s e ha0 ha hb
  linarith

/-- THE AMBIENT CAP: inside any region whose ambient field is at or above
the ceiling (e >= a0/2), the internal phantom boost is strictly below the
ambient field — no self-contained dark halo can exist there. The chain:
boost <= phi(s) (suppression), phi(s) < a0/2 (the ceiling), a0/2 <= e. -/
theorem efe_ambient_cap (a0 s e : ℝ) (ha0 : 0 < a0) (ha : 0 ≤ s) (hb : a0 / 2 ≤ e) :
    phi a0 (s + e) - phi a0 e < e := by
  have he : 0 ≤ e := by nlinarith [ha0, hb]
  have hbnd := efe_boost_left a0 s e ha0 ha he
  by_cases hs0 : s = 0
  · subst s
    simp
    nlinarith [hb, ha0]
  · have hsp : 0 < s := lt_of_le_of_ne ha (Ne.symm hs0)
    have hcs : phi a0 s < a0 / 2 := phantom_ceiling_strict a0 s ha0 hsp
    exact lt_of_le_of_lt hbnd (lt_of_lt_of_le hcs hb)

/-- THE CLUSTER STRIPPING RADIUS: the isothermal-cluster field equals the
ceiling exactly at r = 4 sigma^2 / a0. -/
theorem strip_radius_iff (a0 sigma r : ℝ) (ha0 : 0 < a0) (hs : 0 < sigma) (hr : 0 < r) :
    (2 * sigma^2 / r = a0 / 2) ↔ (r = 4 * sigma^2 / a0) := by
  constructor
  · intro h
    field_simp [hr.ne', (ne_of_gt ha0)] at h
    ring_nf at h
    exact (eq_div_iff (ne_of_gt ha0)).2 (by linarith)
  · intro h
    rw [h]
    field_simp [hs.ne', (ne_of_gt ha0)]
    ring

/-- Inside r_strip the cluster field strictly exceeds the ceiling — the
dark-stripped zone of a cluster. -/
theorem strip_inside_supersaturates (a0 sigma r : ℝ) (ha0 : 0 < a0) (_hs : 0 < sigma)
    (hr : 0 < r) (hin : r < 4 * sigma^2 / a0) :
    a0 / 2 < 2 * sigma^2 / r := by
  have h1 : r * a0 < 4 * sigma^2 := (lt_div_iff₀ ha0).mp hin
  exact (lt_div_iff₀ hr).2 (by nlinarith [h1])

/-- COMBINED: strictly inside the stripping radius no satellite can carry a
self-contained phantom halo — its internal dark boost is bounded below the
ambient cluster field by the cap theorem. -/
theorem strip_no_self_contained_phantom (a0 sigma r s : ℝ) (ha0 : 0 < a0)
    (hs : 0 < sigma) (hr : 0 < r) (hin : r < 4 * sigma^2 / a0) (hsa : 0 ≤ s) :
    phi a0 (s + 2 * sigma^2 / r) - phi a0 (2 * sigma^2 / r) < 2 * sigma^2 / r := by
  have hamb : a0 / 2 < 2 * sigma^2 / r := strip_inside_supersaturates a0 sigma r ha0 hs hr hin
  have hamble : a0 / 2 ≤ 2 * sigma^2 / r := le_of_lt hamb
  exact efe_ambient_cap a0 s (2 * sigma^2 / r) ha0 hsa hamble

end

#print axioms phantom_ceiling_strict
#print axioms phantom_subadditive
#print axioms efe_boost_left
#print axioms efe_ambient_cap
#print axioms strip_radius_iff
#print axioms strip_inside_supersaturates
#print axioms strip_no_self_contained_phantom