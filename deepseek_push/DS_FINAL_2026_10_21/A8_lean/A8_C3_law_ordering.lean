/-
A8 / C3 — the two galactic laws and their exact ordering.

Physics claim being certified (BRIEF section 1).  `g` = observed (total)
acceleration, `gN` = baryonic acceleration, `a0 > 0` the vacuum-tied scale.

  canonical law (frozen S2 rest state, PAPER57 / AG4 branch a):
      g_N = g^2/(g + a0)      <=>     g = g_c := (gN/2)(1 + sqrt(1 + 4 a0/gN))
  n = 2 "a0-line" half-capacity variant:
      g^2 - gN^2 = a0 gN      <=>     g = g_q := sqrt(gN^2 + a0 gN)

Certified here, for all gN > 0 and a0 > 0:

* `gCanon_root`:      g_c^2 = gN (g_c + a0)          (it IS the canonical law)
* `gCanon_root_unique`: any g > 0 with g^2 = gN (g + a0) equals g_c, so g_c is
                       THE positive root, not merely a root.
* `gQuad_root`:       g_q^2 = gN^2 + a0 gN           (it IS the n = 2 law)
* `gCanon_gt_gN`, `gQuad_gt_gN`: both laws exceed Newton.
* `gQuad_lt_gCanon`:  g_q < g_c strictly, for ALL gN, a0 > 0.  No extra
                       hypothesis is needed: the ordering is unconditional on
                       the positive quadrant, and `gCanon_sq_sub_gQuad_sq`
                       shows the gap is exactly gN (g_c - gN) > 0.
* `gCanon_sub_gQuad_eq`: the exact gap, g_c - g_q = a0 gN^2/(g_c (g_c + g_q)),
                       with the two bounds g_c - g_q <= gN and <= a0.
* deep limit: both normalised laws tend to 1 (i.e. both are asymptotic to
                       sqrt(a0 gN)) as gN/a0 -> 0, which is the precise sense
                       in which the two laws are "equal only in the limit".

What is NOT certified: that either law is the physically correct one; that the
deep limit sqrt(a0 gN) is realised by any data; any statement about galaxies,
rotation curves or fits; the "capacity a0 vs a0/2" reading (that is an
integral statement about the interpolation, not proved here).
-/
import Mathlib

namespace A8

open Filter Topology

/-- Canonical law, solved for `g`: `g_c = (gN/2)(1 + sqrt(1 + 4 a0/gN))`. -/
noncomputable def gCanon (gN a0 : ℝ) : ℝ :=
  gN / 2 * (1 + Real.sqrt (1 + 4 * a0 / gN))

/-- `n = 2` law, solved for `g`: `g_q = sqrt(gN^2 + a0 gN)`. -/
noncomputable def gQuad (gN a0 : ℝ) : ℝ := Real.sqrt (gN ^ 2 + a0 * gN)

/-! ## Algebraic form of the canonical root -/

/-- The canonical closed form rewritten without a division under the root:
`g_c = gN/2 + sqrt(gN^2/4 + a0 gN)`.  This is the form in which positivity is
manifest, and it is what the ordering proofs use. -/
theorem gCanon_form {gN a0 : ℝ} (hgN : 0 < gN) :
    gCanon gN a0 = gN / 2 + Real.sqrt (gN ^ 2 / 4 + a0 * gN) := by
  unfold gCanon
  have harg : gN ^ 2 / 4 + a0 * gN = (gN / 2) ^ 2 * (1 + 4 * a0 / gN) := by
    field_simp
    ring
  rw [harg, Real.sqrt_mul (by positivity : (0 : ℝ) ≤ (gN / 2) ^ 2),
    Real.sqrt_sq (by positivity : (0 : ℝ) ≤ gN / 2)]
  ring

/-! ## Both laws exceed Newton -/

/-- The canonical law exceeds `gN`. -/
theorem gCanon_gt_gN {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gN < gCanon gN a0 := by
  rw [gCanon_form hgN]
  have h1 : gN / 2 < Real.sqrt (gN ^ 2 / 4 + a0 * gN) := by
    rw [Real.lt_sqrt (by positivity)]
    nlinarith
  linarith

/-- The `n = 2` law exceeds `gN`. -/
theorem gQuad_gt_gN {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gN < gQuad gN a0 := by
  have h : Real.sqrt (gN ^ 2) < Real.sqrt (gN ^ 2 + a0 * gN) :=
    Real.sqrt_lt_sqrt (by positivity) (by nlinarith)
  rwa [Real.sqrt_sq (le_of_lt hgN)] at h

/-! ## C3 (i): each closed form satisfies its own law -/

/-- **C3, canonical root.**  `g_c^2 = gN (g_c + a0)`, i.e. `gN = g_c^2/(g_c + a0)`. -/
theorem gCanon_root {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 ^ 2 = gN * (gCanon gN a0 + a0) := by
  rw [gCanon_form hgN]
  have hs : Real.sqrt (gN ^ 2 / 4 + a0 * gN) ^ 2 = gN ^ 2 / 4 + a0 * gN :=
    Real.sq_sqrt (by positivity)
  nlinarith [hs]

/-- **C3, n = 2 root.**  `g_q^2 = gN^2 + a0 gN`. -/
theorem gQuad_root {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gQuad gN a0 ^ 2 = gN ^ 2 + a0 * gN := by
  unfold gQuad
  exact Real.sq_sqrt (by positivity)

/-- **C3, uniqueness.**  Any positive `g` obeying the canonical law's defining
equation equals the closed form.  So `gCanon` is *the* positive root. -/
theorem gCanon_root_unique {g gN a0 : ℝ} (hg : 0 < g) (hgN : 0 < gN) (ha0 : 0 < a0)
    (h : g ^ 2 = gN * (g + a0)) : g = gCanon gN a0 := by
  have hc : gCanon gN a0 ^ 2 = gN * (gCanon gN a0 + a0) := gCanon_root hgN ha0
  have hcgt : gN < gCanon gN a0 := gCanon_gt_gN hgN ha0
  have hfac : (g - gCanon gN a0) * (g + gCanon gN a0 - gN) = 0 := by
    nlinarith [h, hc]
  have hpos : 0 < g + gCanon gN a0 - gN := by linarith
  rcases mul_eq_zero.mp hfac with h1 | h1
  · linarith
  · linarith

/-! ## C3 (ii): strict ordering of the two laws -/

/-- **C3, exact difference of squares.**  `g_c^2 - g_q^2 = gN (g_c - gN)`.  Both
root equations are used; this is the whole content of the ordering. -/
theorem gCanon_sq_sub_gQuad_sq {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 ^ 2 - gQuad gN a0 ^ 2 = gN * (gCanon gN a0 - gN) := by
  rw [gCanon_root hgN ha0, gQuad_root hgN ha0]
  ring

/-- **C3, the ordering.**  `g_q < g_c` for every `gN > 0`, `a0 > 0`.  No extra
hypothesis: the inequality is strict on the whole positive quadrant (see
`A8_C3_MUTATE.lean` for the reversed claim, which does not compile). -/
theorem gQuad_lt_gCanon {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gQuad gN a0 < gCanon gN a0 := by
  have hcgt : gN < gCanon gN a0 := gCanon_gt_gN hgN ha0
  have hsq : gQuad gN a0 ^ 2 < gCanon gN a0 ^ 2 := by
    have h := gCanon_sq_sub_gQuad_sq hgN ha0
    nlinarith [h, hcgt, hgN]
  have h1 : 0 ≤ gQuad gN a0 := by unfold gQuad; positivity
  have h2 : 0 ≤ gCanon gN a0 := le_of_lt (lt_trans hgN hcgt)
  have habs := sq_lt_sq.mp hsq
  rwa [abs_of_nonneg h1, abs_of_nonneg h2] at habs

/-! ## C3 (iii): the exact gap, its two bounds, and the limits -/

/-- **C3, exact gap.**  `g_c - g_q = a0 gN^2/(g_c (g_c + g_q))`.  This makes the
"equality only in the limit" statement algebraic: the gap is positive for
`a0 > 0` and vanishes only as `a0 gN^2 / g_c^3 -> 0`. -/
theorem gCanon_sub_gQuad_eq {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 - gQuad gN a0 =
      a0 * gN ^ 2 / (gCanon gN a0 * (gCanon gN a0 + gQuad gN a0)) := by
  have hc : gCanon gN a0 ^ 2 = gN * (gCanon gN a0 + a0) := gCanon_root hgN ha0
  have hq : gQuad gN a0 ^ 2 = gN ^ 2 + a0 * gN := gQuad_root hgN ha0
  have hcgt : gN < gCanon gN a0 := gCanon_gt_gN hgN ha0
  have hcpos : 0 < gCanon gN a0 := lt_trans hgN hcgt
  have hqpos : 0 < gQuad gN a0 := lt_trans hgN (gQuad_gt_gN hgN ha0)
  have hden : gCanon gN a0 * (gCanon gN a0 + gQuad gN a0) ≠ 0 := by positivity
  field_simp
  nlinarith [hc, hq]

/-- **C3, gap bound 1.**  `g_c - g_q ≤ gN`: the two laws never differ by more
than Newton's own acceleration. -/
theorem gCanon_sub_gQuad_le_gN {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 - gQuad gN a0 ≤ gN := by
  rw [gCanon_sub_gQuad_eq hgN ha0]
  have hc : gCanon gN a0 ^ 2 = gN * (gCanon gN a0 + a0) := gCanon_root hgN ha0
  have hcgt : gN < gCanon gN a0 := gCanon_gt_gN hgN ha0
  have hcpos : 0 < gCanon gN a0 := lt_trans hgN hcgt
  have hqpos : 0 < gQuad gN a0 := lt_trans hgN (gQuad_gt_gN hgN ha0)
  have hden : 0 < gCanon gN a0 * (gCanon gN a0 + gQuad gN a0) := by positivity
  rw [div_le_iff₀ hden]
  have h1 : gN * a0 ≤ gCanon gN a0 ^ 2 := by nlinarith [hc]
  have h2 : gCanon gN a0 ^ 2 ≤ gCanon gN a0 * (gCanon gN a0 + gQuad gN a0) := by
    nlinarith [hcpos, hqpos]
  have h3 : gN * (gN * a0) ≤ gN * gCanon gN a0 ^ 2 := by nlinarith [h1, hgN]
  have h4 : gN * gCanon gN a0 ^ 2
      ≤ gN * (gCanon gN a0 * (gCanon gN a0 + gQuad gN a0)) := by nlinarith [h2, hgN]
  linarith

/-- **C3, gap bound 2.**  `g_c - g_q ≤ a0`. -/
theorem gCanon_sub_gQuad_le_a0 {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 - gQuad gN a0 ≤ a0 := by
  rw [gCanon_sub_gQuad_eq hgN ha0]
  have hcgt : gN < gCanon gN a0 := gCanon_gt_gN hgN ha0
  have hcpos : 0 < gCanon gN a0 := lt_trans hgN hcgt
  have hqpos : 0 < gQuad gN a0 := lt_trans hgN (gQuad_gt_gN hgN ha0)
  have hden : 0 < gCanon gN a0 * (gCanon gN a0 + gQuad gN a0) := by positivity
  rw [div_le_iff₀ hden]
  have h1 : gN ^ 2 ≤ gCanon gN a0 ^ 2 := by nlinarith [hcgt, hgN]
  have h2 : gCanon gN a0 ^ 2 ≤ gCanon gN a0 * (gCanon gN a0 + gQuad gN a0) := by
    nlinarith [hcpos, hqpos]
  have h3 : a0 * gN ^ 2 ≤ a0 * gCanon gN a0 ^ 2 := by nlinarith [h1, ha0]
  have h4 : a0 * gCanon gN a0 ^ 2
      ≤ a0 * (gCanon gN a0 * (gCanon gN a0 + gQuad gN a0)) := by nlinarith [h2, ha0]
  linarith

/-! ## C3 (iv): equality only in the limit -/

/-- **C3, the deep limit, `n = 2` side.**  With `a0 = 1` and `delta = gN/a0`,
`g_q/sqrt(delta) -> 1`, i.e. `g_q ~ sqrt(a0 gN)`. -/
theorem gQuad_normalised_tendsto :
    Tendsto (fun δ : ℝ => gQuad δ 1 / Real.sqrt δ) (nhdsWithin 0 (Set.Ioi 0)) (nhds 1) := by
  have heq : (fun δ : ℝ => gQuad δ 1 / Real.sqrt δ)
      =ᶠ[nhdsWithin 0 (Set.Ioi 0)] (fun δ => Real.sqrt (1 + δ)) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have htpos : 0 < Real.sqrt t := Real.sqrt_pos_of_pos ht
    unfold gQuad
    rw [show t ^ 2 + 1 * t = t * (1 + t) by ring, Real.sqrt_mul (le_of_lt ht)]
    field_simp
  have hcont : ContinuousAt (fun δ : ℝ => Real.sqrt (1 + δ)) 0 :=
    ContinuousAt.sqrt (continuousAt_const.add continuousAt_id)
  have hlim : Tendsto (fun δ : ℝ => Real.sqrt (1 + δ))
      (nhdsWithin 0 (Set.Ioi 0)) (nhds 1) := by
    have h := hcont.tendsto.mono_left (nhdsWithin_le_nhds (a := 0) (s := Set.Ioi 0))
    simpa using h
  exact hlim.congr' heq.symm

/-- **C3, the deep limit, canonical side.**  `g_c/sqrt(delta) -> 1` as well:
both laws share the deep limit `sqrt(a0 gN)`, so they are equal only in the
limit, in the precise sense that their normalised difference tends to zero. -/
theorem gCanon_normalised_tendsto :
    Tendsto (fun δ : ℝ => gCanon δ 1 / Real.sqrt δ) (nhdsWithin 0 (Set.Ioi 0)) (nhds 1) := by
  have heq : (fun δ : ℝ => gCanon δ 1 / Real.sqrt δ)
      =ᶠ[nhdsWithin 0 (Set.Ioi 0)] (fun δ => Real.sqrt δ / 2 + Real.sqrt (1 + δ / 4)) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have htpos : 0 < Real.sqrt t := Real.sqrt_pos_of_pos ht
    have hst : Real.sqrt t * Real.sqrt t = t := Real.mul_self_sqrt (le_of_lt ht)
    rw [gCanon_form ht]
    rw [show t ^ 2 / 4 + 1 * t = t * (1 + t / 4) by ring, Real.sqrt_mul (le_of_lt ht)]
    field_simp
    nlinarith [hst]
  have hcont : ContinuousAt (fun δ : ℝ => Real.sqrt δ / 2 + Real.sqrt (1 + δ / 4)) 0 := by
    apply ContinuousAt.add
    · exact (ContinuousAt.sqrt continuousAt_id).div_const 2
    · exact ContinuousAt.sqrt (continuousAt_const.add (continuousAt_id.div_const 4))
  have hlim : Tendsto (fun δ : ℝ => Real.sqrt δ / 2 + Real.sqrt (1 + δ / 4))
      (nhdsWithin 0 (Set.Ioi 0)) (nhds 1) := by
    have h := hcont.tendsto.mono_left (nhdsWithin_le_nhds (a := 0) (s := Set.Ioi 0))
    simpa using h
  exact hlim.congr' heq.symm

/-- **C3, Newton limit.**  As `a0 -> 0+` at fixed `gN > 0`, the two laws
coincide: `g_c - g_q -> 0`.  (Both tend to `gN`.) -/
theorem gap_tendsto_a0_zero {gN : ℝ} (hgN : 0 < gN) :
    Tendsto (fun a0 : ℝ => gCanon gN a0 - gQuad gN a0) (nhdsWithin 0 (Set.Ioi 0)) (nhds 0) := by
  have hcont : ContinuousAt (fun a0 : ℝ => gCanon gN a0 - gQuad gN a0) 0 := by
    unfold gCanon gQuad
    fun_prop
  have h0 : gCanon gN 0 - gQuad gN 0 = 0 := by
    unfold gCanon gQuad
    simp [Real.sqrt_sq_eq_abs, abs_of_pos hgN]
    ring
  simpa [h0] using hcont.tendsto.mono_left nhdsWithin_le_nhds

end A8

#print axioms A8.gCanon_form
#print axioms A8.gCanon_gt_gN
#print axioms A8.gQuad_gt_gN
#print axioms A8.gCanon_root
#print axioms A8.gQuad_root
#print axioms A8.gCanon_root_unique
#print axioms A8.gCanon_sq_sub_gQuad_sq
#print axioms A8.gQuad_lt_gCanon
#print axioms A8.gCanon_sub_gQuad_eq
#print axioms A8.gCanon_sub_gQuad_le_gN
#print axioms A8.gCanon_sub_gQuad_le_a0
#print axioms A8.gQuad_normalised_tendsto
#print axioms A8.gCanon_normalised_tendsto
#print axioms A8.gap_tendsto_a0_zero
