import Mathlib

/-!
# ZD02 — The Mass-Accounting Laws (the RAR in mass form)

Framework premise (docstring scope, NOT certified here): the a0-line
g_obs^2 - g_bar^2 = a0 * g_bar (PD08/PD13 in deepseek_push/STATE.md). For a
spherically symmetric system the fields are enclosed-mass fields,
g = G M(<r)/r^2, so the a0-line becomes the exact mass-accounting law

    M_tot(<r) / M_b(<r) = sqrt(1 + a0 / g_b(r)) = sqrt(1 + 1/x),

Certified consequences, all new to the corpus:

  1. THE MASS RATIO LAW: M_tot/M_b = sqrt(1 + 1/x), x = g_b/a0, exact; the
     phantom ratio M_phi/M_b = sqrt(1 + 1/x) - 1.
  2. THE DOUBLING THEOREM: the phantom mass equals the baryon mass EXACTLY
     at g_b = a0/3 (r_eq = sqrt(3 G M_b / a0)) — the 1:1 radius; the total is
     exactly 2 M_b there. Quadrupling at g_b = a0/15.
  3. ANTITONE: the mass ratio falls monotonically as the baryon field rises.
  4. THE FRACTION AT DOUBLING: f_phi = 1 - x/sqrt(x^2+x) = 1/2 exactly at
     x = 1/3.
  5. DEEP BAND: sqrt(a0 g_b) - g_b <= g_phi <= sqrt(a0 g_b) — the deep-MOND
     square-root law bracketed exactly (the phantom column ~a0/(2 pi G)
     content is the writeup's, the bracket here is the certified part).
  6. STRONG-FIELD BAND: for g_b >= a0/8 the phantom sits in the band
     [a0/2 - a0^2 r^2/(8 G M), a0/2) — the approach law in radius form.
  7. THE HANDOFF VALUE (exact): at r* with r*^2 = 2 G M_b / a0 (g_b = a0/2)
     the enclosed phantom mass is exactly (sqrt 3 - 1) * M_b, a pure number
     independent of a0, G and M — the phantom's share of the baryon mass at
     the halo handoff. Includes the certified lower bound M/2.

Lean certifies the mathematics; the a0-line premise is the framework's law
(STATE.md).
-/

noncomputable section
open scoped Real

/-- The phantom (dark) acceleration normalized by a0 — same function as in
ZD01, restated here so ZD02 is self-contained. -/
noncomputable def phi (a0 x : ℝ) : ℝ := Real.sqrt (x^2 + a0 * x) - x

/-- Strict ceiling (ZD01 restated): the phantom of a finite field is strictly
below a0/2. -/
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

/-- Approach law (ZD01 restated): for g >= a0/8 the phantom is bounded below
by the two-term expansion. -/
theorem phantom_approach_lower (a0 g : ℝ) (ha0 : 0 < a0) (hg : a0 / 8 ≤ g) :
    a0 / 2 - a0^2 / (8 * g) ≤ phi a0 g := by
  have hgpos : 0 < g := by nlinarith [ha0, hg]
  by_cases hb0 : a0 / 2 - a0^2 / (8 * g) ≤ 0
  · have hnnX : 0 ≤ g^2 + a0 * g := by nlinarith [sq_nonneg g, hgpos.le, ha0.le]
    have hroot : g ≤ Real.sqrt (g^2 + a0 * g) := by
      exact (Real.le_sqrt hgpos.le hnnX).2 (by nlinarith [sq_nonneg g, hgpos.le, ha0.le])
    unfold phi
    nlinarith [hb0, hroot]
  · have hbpos : 0 < a0 / 2 - a0^2 / (8 * g) := lt_of_not_ge hb0
    have hu : 0 ≤ g + a0 / 2 - a0^2 / (8 * g) := by nlinarith [hbpos, hgpos.le]
    have hnn : 0 ≤ g^2 + a0 * g := by
      nlinarith [sq_nonneg g, hgpos.le, ha0.le]
    have hsq : (g + a0 / 2 - a0^2 / (8 * g))^2 ≤ g^2 + a0 * g := by
      field_simp [hgpos.ne', ha0.ne']
      ring_nf
      have h8 : 0 ≤ 8 * g - a0 := by nlinarith [hg]
      have hpow : 0 ≤ a0^3 := by positivity
      nlinarith [mul_nonneg hpow h8]
    have hsq2 : (g + a0 / 2 - a0^2 / (8 * g))^2 ≤ (Real.sqrt (g^2 + a0 * g))^2 := by
      rwa [← Real.sq_sqrt hnn] at hsq
    have habs : |g + a0 / 2 - a0^2 / (8 * g)| ≤ |Real.sqrt (g^2 + a0 * g)| :=
      sq_le_sq.mp hsq2
    have hroot : g + a0 / 2 - a0^2 / (8 * g) ≤ Real.sqrt (g^2 + a0 * g) := by
      simpa [abs_of_nonneg hu, abs_of_nonneg (Real.sqrt_nonneg _)] using habs
    unfold phi
    linarith

/-- THE MASS RATIO LAW: g_obs/g_b = sqrt(1 + 1/x) exactly (x = g_b/a0 > 0). -/
theorem rat_form (x : ℝ) (hx : 0 < x) :
    Real.sqrt (x^2 + x) / x = Real.sqrt (1 + 1 / x) := by
  have hnn : 0 ≤ x^2 + x := by nlinarith [sq_nonneg x, hx.le]
  have hnn2 : 0 ≤ 1 + 1 / x := by positivity
  have hEq : Real.sqrt (x^2 + x) = x * Real.sqrt (1 + 1 / x) := by
    have hsq : (Real.sqrt (x^2 + x))^2 = (x * Real.sqrt (1 + 1 / x))^2 := by
      rw [Real.sq_sqrt hnn, mul_pow, Real.sq_sqrt hnn2]
      field_simp [hx.ne']
    rcases eq_or_eq_neg_of_sq_eq_sq
        (Real.sqrt (x^2 + x)) (x * Real.sqrt (1 + 1 / x)) hsq with hpos | hneg
    · exact hpos
    · exfalso
      have hs : 0 < x * Real.sqrt (1 + 1 / x) :=
        mul_pos hx (Real.sqrt_pos.mpr (by positivity : 0 < 1 + 1 / x))
      have hcontra : 0 ≤ -(x * Real.sqrt (1 + 1 / x)) := by
        rw [← hneg]
        exact Real.sqrt_nonneg _
      nlinarith
  have hEq' : Real.sqrt (x^2 + x) = Real.sqrt (1 + 1 / x) * x := by
    simpa [mul_comm] using hEq
  exact (div_eq_iff (ne_of_gt hx)).mpr hEq'

/-- THE DOUBLING THEOREM: the phantom equals the baryons (M_tot = 2 M_b)
exactly at g_b = a0/3. -/
theorem doubling_iff (x : ℝ) (hx : 0 < x) :
    Real.sqrt (1 + 1 / x) = 2 ↔ x = 1 / 3 := by
  constructor
  · intro h
    have hnn : 0 ≤ 1 + 1 / x := by positivity
    have hsq : 1 + 1 / x = 4 := by
      have h2 : (Real.sqrt (1 + 1 / x))^2 = 4 := by rw [h]; norm_num
      rwa [Real.sq_sqrt hnn] at h2
    field_simp [hx.ne'] at hsq
    nlinarith
  · intro hx3
    rw [hx3]
    norm_num [Real.sqrt_sq_eq_abs]

/-- Quadrupling: M_tot = 4 M_b exactly at g_b = a0/15. -/
theorem quadrupling_iff (x : ℝ) (hx : 0 < x) :
    Real.sqrt (1 + 1 / x) = 4 ↔ x = 1 / 15 := by
  constructor
  · intro h
    have hnn : 0 ≤ 1 + 1 / x := by positivity
    have hsq : 1 + 1 / x = 16 := by
      have h2 : (Real.sqrt (1 + 1 / x))^2 = 16 := by rw [h]; norm_num
      rwa [Real.sq_sqrt hnn] at h2
    field_simp [hx.ne'] at hsq
    nlinarith
  · intro hx15
    rw [hx15]
    norm_num [Real.sqrt_sq_eq_abs]

/-- The mass ratio falls monotonically as the baryon field rises. -/
theorem ratio_antitone (x y : ℝ) (hx : 0 < x) (hxy : x ≤ y) :
    Real.sqrt (1 + 1 / y) ≤ Real.sqrt (1 + 1 / x) := by
  have h1 : 1 / y ≤ 1 / x := one_div_le_one_div_of_le hx hxy
  have h2 : 1 + 1 / y ≤ 1 + 1 / x := by linarith
  exact Real.sqrt_le_sqrt h2

/-- THE FRACTION AT DOUBLING: f_phi = 1 - g_b/g_obs = 1/2 exactly at
x = 1/3 (the phantom carries half the mass at the 1:1 radius). -/
theorem fraction_doubling_exact (x : ℝ) (hx : 0 < x) (hx3 : x = 1 / 3) :
    1 - x / Real.sqrt (x^2 + x) = 1 / 2 := by
  rw [hx3]
  have hs : Real.sqrt ((1 / 3 : ℝ)^2 + (1 / 3 : ℝ)) = 2 / 3 := by
    have hsq_ : (Real.sqrt ((1 / 3 : ℝ)^2 + (1 / 3 : ℝ)))^2 = (2 / 3 : ℝ)^2 := by
      rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ (1 / 3 : ℝ)^2 + (1 / 3 : ℝ))]
      norm_num
    rcases eq_or_eq_neg_of_sq_eq_sq
        (Real.sqrt ((1 / 3 : ℝ)^2 + (1 / 3 : ℝ))) (2 / 3 : ℝ) hsq_ with hp | hn
    · exact hp
    · exfalso
      nlinarith [Real.sqrt_nonneg ((1 / 3 : ℝ)^2 + (1 / 3 : ℝ))]
  rw [hs]
  norm_num

/-- DEEP BAND: the deep-MOND square-root law bracketed exactly:
sqrt(a0 g_b) - g_b <= g_phi <= sqrt(a0 g_b). -/
theorem deep_band (a0 g : ℝ) (ha0 : 0 < a0) (hg : 0 ≤ g) :
    Real.sqrt (a0 * g) - g ≤ phi a0 g ∧ phi a0 g ≤ Real.sqrt (a0 * g) := by
  constructor
  · unfold phi
    have h1 : a0 * g ≤ g^2 + a0 * g := by nlinarith [sq_nonneg g]
    have h2 : Real.sqrt (a0 * g) ≤ Real.sqrt (g^2 + a0 * g) := Real.sqrt_le_sqrt h1
    linarith
  · unfold phi
    have hnn : 0 ≤ g^2 + a0 * g := by nlinarith [sq_nonneg g, hg, ha0.le]
    have hnn2 : 0 ≤ a0 * g := mul_nonneg ha0.le hg
    have hz : 0 ≤ 2 * g * Real.sqrt (g * a0) := by positivity
    have h1 : (Real.sqrt (g^2 + a0 * g))^2 ≤ (Real.sqrt (a0 * g) + g)^2 := by
      rw [Real.sq_sqrt hnn]
      rw [pow_two]
      ring_nf
      rw [Real.sq_sqrt (by simpa [mul_comm] using hnn2)]
      nlinarith [hz]
    have habs : |Real.sqrt (g^2 + a0 * g)| ≤ |Real.sqrt (a0 * g) + g| := sq_le_sq.mp h1
    have hnon : 0 ≤ Real.sqrt (a0 * g) + g := add_nonneg (Real.sqrt_nonneg _) hg
    have hroot : Real.sqrt (g^2 + a0 * g) ≤ Real.sqrt (a0 * g) + g := by
      simpa [abs_of_nonneg (Real.sqrt_nonneg _), abs_of_nonneg hnon] using habs
    linarith

/-- STRONG-FIELD BAND in radius form: for g_b = G M / r^2 >= a0/8 the
phantom sits in [a0/2 - a0^2 r^2/(8 G M), a0/2). -/
theorem strong_field_band (a0 G M r : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hM : 0 < M)
    (hr : 0 < r) (hrb : r^2 ≤ 8 * G * M / a0) :
    a0 / 2 - a0^2 * r^2 / (8 * G * M) ≤ phi a0 (G * M / r^2) ∧
      phi a0 (G * M / r^2) < a0 / 2 := by
  have hgb : a0 / 8 ≤ G * M / r^2 := by
    have h3 : r^2 * a0 ≤ 8 * G * M := (le_div_iff₀ ha0).mp hrb
    have h2 : r^2 * (a0 / 8) ≤ G * M := by nlinarith [h3]
    exact (le_div_iff₀ (sq_pos_of_pos hr)).2 (by nlinarith [h2])
  constructor
  · have hl := phantom_approach_lower a0 (G * M / r^2) ha0 hgb
    convert hl using 1
    field_simp [hG.ne', hM.ne', hr.ne']
  · have hp : 0 < G * M / r^2 := by positivity
    exact phantom_ceiling_strict a0 (G * M / r^2) ha0 hp

/-- THE HANDOFF VALUE: the phantom of the a0/2 field is exactly
a0 (sqrt 3 - 1) / 2. -/
theorem handoff_root_value (a0 : ℝ) (ha0 : 0 < a0) :
    phi a0 (a0 / 2) = a0 * (Real.sqrt 3 - 1) / 2 := by
  have harg : (a0 / 2)^2 + a0 * (a0 / 2) = (3 : ℝ) * a0^2 / 4 := by ring
  have hrt : Real.sqrt ((a0 / 2)^2 + a0 * (a0 / 2)) = Real.sqrt 3 * a0 / 2 := by
    rw [harg]
    have hx : (3 : ℝ) * a0^2 / 4 = ((Real.sqrt 3 * a0) / 2)^2 := by
      field_simp
      ring_nf
      rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]
      ring
    rw [hx]
    exact Real.sqrt_sq (by positivity)
  unfold phi
  rw [hrt]
  ring

/-- THE HANDOFF MASS (exact): at r^2 = 2 G M / a0 (g_b = a0/2) the enclosed
phantom mass is exactly (sqrt 3 - 1) * M_b — a pure number, independent of
a0, G and M. -/
theorem mphi_handoff_exact (a0 G M r : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hM : 0 < M)
    (_hr : 0 < r) (hr2 : r^2 = 2 * G * M / a0) :
    r^2 * phi a0 (G * M / r^2) / G = (Real.sqrt 3 - 1) * M := by
  have hgb : G * M / r^2 = a0 / 2 := by
    rw [hr2]
    field_simp [hG.ne', hM.ne', ha0.ne']
  rw [hgb]
  rw [handoff_root_value a0 ha0]
  rw [hr2]
  field_simp [hG.ne', ha0.ne']

/-- The handoff phantom mass exceeds half the baryon mass. -/
theorem mphi_handoff_lower (M : ℝ) (hM : 0 < M) :
    M / 2 ≤ (Real.sqrt 3 - 1) * M := by
  have hlt : (3 : ℝ) / 2 < Real.sqrt 3 := by
    exact (Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 3 / 2)).2 (by norm_num)
  nlinarith [hlt, hM]

end

#print axioms rat_form
#print axioms doubling_iff
#print axioms quadrupling_iff
#print axioms ratio_antitone
#print axioms fraction_doubling_exact
#print axioms deep_band
#print axioms strong_field_band
#print axioms handoff_root_value
#print axioms mphi_handoff_exact
#print axioms mphi_handoff_lower