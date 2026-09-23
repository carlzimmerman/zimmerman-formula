import Mathlib

/-! Independent reconstruction of PD02's valid algebra, with the normalization
parameter retained. This file does not assert a physical channel identification.
The original source files are unchanged. -/

open Filter
open scoped Topology

namespace PDNormalization

theorem quot_gen {a : ℝ → ℝ} {c : ℝ}
    (ha : Tendsto a (𝓝[≠] 0) (𝓝 1))
    (hd : Tendsto (fun Y : ℝ => (a Y - 1) / Y) (𝓝[≠] 0) (𝓝 c))
    (n : ℕ) :
    Tendsto (fun Y : ℝ => ((a Y) ^ n - 1) / Y)
      (𝓝[≠] 0) (𝓝 ((n : ℝ) * c)) := by
  induction n with
  | zero =>
      simpa using (tendsto_const_nhds :
        Tendsto (fun _ : ℝ => (0 : ℝ)) (𝓝[≠] 0) (𝓝 0))
  | succ m ih =>
      have hf : (fun Y : ℝ => ((a Y) ^ (m + 1) - 1) / Y) =
          (fun Y : ℝ => a Y * (((a Y) ^ m - 1) / Y) + (a Y - 1) / Y) := by
        funext Y
        simp only [pow_succ, div_eq_mul_inv]
        ring
      rw [hf]
      convert (ha.mul ih).add hd using 1 <;> push_cast <;> ring

/-- Unit slope is a separate assumption: arbitrary slope c gives n*c. -/
theorem or_slope_general {p : ℝ → ℝ} {c : ℝ}
    (hp : Tendsto (fun Y : ℝ => p Y / Y) (𝓝[≠] 0) (𝓝 c))
    (n : ℕ) :
    Tendsto (fun Y : ℝ => (1 - (1 - p Y) ^ n) / Y)
      (𝓝[≠] 0) (𝓝 ((n : ℝ) * c)) := by
  have hY : Tendsto (fun Y : ℝ => Y) (𝓝[≠] 0) (𝓝 0) :=
    tendsto_nhdsWithin_of_tendsto_nhds tendsto_id
  have hpzero : Tendsto p (𝓝[≠] 0) (𝓝 0) := by
    have hm := hY.mul hp
    have he : (fun Y : ℝ => Y * (p Y / Y)) =ᶠ[𝓝[≠] 0] p := by
      filter_upwards [self_mem_nhdsWithin] with Y hY
      have hne : Y ≠ 0 := by simpa using hY
      field_simp
    simpa using hm.congr' he
  have ha : Tendsto (fun Y : ℝ => 1 - p Y) (𝓝[≠] 0) (𝓝 1) := by
    simpa using (tendsto_const_nhds.sub hpzero)
  have hd : Tendsto (fun Y : ℝ => ((1 - p Y) - 1) / Y)
      (𝓝[≠] 0) (𝓝 (-c)) := by
    convert hp.neg using 1
    funext Y
    ring
  have hq := (quot_gen ha hd n).neg
  convert hq using 1 <;> (try funext Y) <;> ring

theorem or_slope {p : ℝ → ℝ}
    (hp : Tendsto (fun Y : ℝ => p Y / Y) (𝓝[≠] 0) (𝓝 1))
    (n : ℕ) :
    Tendsto (fun Y : ℝ => (1 - (1 - p Y) ^ n) / Y)
      (𝓝[≠] 0) (𝓝 (n : ℝ)) := by
  simpa using or_slope_general hp n

theorem rational_engagement_slope (c : ℝ) :
    Tendsto (fun Y : ℝ => (c * Y / (1 + c * Y)) / Y)
      (𝓝[≠] 0) (𝓝 c) := by
  have hden : Tendsto (fun Y : ℝ => 1 + c * Y) (𝓝[≠] 0) (𝓝 1) := by
    have hc : Continuous (fun Y : ℝ => 1 + c * Y) := by continuity
    simpa using tendsto_nhdsWithin_of_tendsto_nhds (hc.tendsto 0)
  have hlim := (tendsto_const_nhds :
    Tendsto (fun _ : ℝ => c) (𝓝[≠] 0) (𝓝 c)).div hden
    (by norm_num : (1 : ℝ) ≠ 0)
  have he : (fun Y : ℝ => c / (1 + c * Y)) =ᶠ[𝓝[≠] 0]
      (fun Y : ℝ => (c * Y / (1 + c * Y)) / Y) := by
    filter_upwards [self_mem_nhdsWithin] with Y hY
    have hne : Y ≠ 0 := by simpa using hY
    field_simp
  simpa using hlim.congr' he

noncomputable def muRate (c : ℝ) (n : ℕ) (Y : ℝ) : ℝ :=
  1 - (1 - c * Y / (1 + c * Y)) ^ n

theorem rate_family_slope (c : ℝ) (n : ℕ) :
    Tendsto (fun Y : ℝ => muRate c n Y / Y)
      (𝓝[≠] 0) (𝓝 ((n : ℝ) * c)) :=
  or_slope_general (rational_engagement_slope c) n

/-- Same two-channel OR law, different slope: the common rate is load-bearing. -/
theorem two_channels_need_not_have_slope_two :
    ¬ Tendsto (fun Y : ℝ => muRate 2 2 Y / Y) (𝓝[≠] 0) (𝓝 2) := by
  intro h
  have hfour : Tendsto (fun Y : ℝ => muRate 2 2 Y / Y) (𝓝[≠] 0) (𝓝 4) := by
    convert rate_family_slope (2 : ℝ) 2 using 1 <;> norm_num
  have hbad : (4 : ℝ) = 2 := tendsto_nhds_unique hfour h
  norm_num at hbad

noncomputable def muFam (n : ℕ) (Y : ℝ) : ℝ :=
  1 - (1 + Y) ^ (-((n : ℤ)))

theorem slope_family (n : ℕ) :
    Tendsto (fun Y : ℝ => muFam n Y / Y) (𝓝[≠] 0) (𝓝 (n : ℝ)) := by
  have hden : Tendsto (fun Y : ℝ => 1 + Y) (𝓝[≠] 0) (𝓝 1) := by
    simpa using (tendsto_const_nhds.add
      (tendsto_nhdsWithin_of_tendsto_nhds
        (tendsto_id : Tendsto (fun Y : ℝ => Y) (𝓝 0) (𝓝 0))))
  have hp : Tendsto (fun Y : ℝ => (Y / (1 + Y)) / Y)
      (𝓝[≠] 0) (𝓝 1) := by
    have hlim := (tendsto_const_nhds :
      Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[≠] 0) (𝓝 1)).div hden
      (by norm_num : (1 : ℝ) ≠ 0)
    have he : (fun Y : ℝ => (1 : ℝ) / (1 + Y)) =ᶠ[𝓝[≠] 0]
        (fun Y : ℝ => (Y / (1 + Y)) / Y) := by
      filter_upwards [self_mem_nhdsWithin] with Y hY
      have hne : Y ≠ 0 := by simpa using hY
      field_simp
    simpa using hlim.congr' he
  have hOr := or_slope hp n
  have hnonzero : ∀ᶠ Y : ℝ in 𝓝[≠] 0, 1 + Y ≠ 0 :=
    hden.eventually_ne (by norm_num : (1 : ℝ) ≠ 0)
  apply hOr.congr'
  filter_upwards [hnonzero] with Y hY
  have he : 1 - Y / (1 + Y) = (1 + Y)⁻¹ := by
    field_simp
    ring
  simp only [muFam, he, zpow_neg, zpow_natCast, inv_pow]

theorem mond_matching {n s g2 gN GM r : ℝ}
    (hn : n ≠ 0) (hs : s ≠ 0) (hr : r ≠ 0)
    (h : r ^ 2 * (n * g2 / s) = GM) (hGN : gN = GM / r ^ 2) :
    g2 = (s / n) * gN := by
  rw [hGN]
  field_simp at h ⊢
  nlinarith [h]

theorem kappa_half {s a0 : ℝ} (hs : s ≠ 0) (h : a0 = s / 2) :
    a0 / s = 1 / 2 := by
  rw [h]
  field_simp

/-- Generalized matching explicitly exposes the per-channel normalization. -/
theorem kappa_normalization {s a0 c : ℝ} (hs : s ≠ 0) (hc : c ≠ 0)
    (h : a0 = s / (2 * c)) : a0 / s = 1 / (2 * c) := by
  rw [h]
  field_simp

/-- PD03's quarter-energy matching is equivalent to kappa squared = 1/4. -/
theorem quarter_matching_iff {a0 s G u : ℝ}
    (hG : G ≠ 0) (hs : s ≠ 0) (hsu : s ^ 2 = G * u) :
    a0 ^ 2 / G = u / 4 ↔ (a0 / s) ^ 2 = 1 / 4 := by
  constructor <;> intro h <;> field_simp at h ⊢ <;> nlinarith [hsu]

#print axioms or_slope_general
#print axioms two_channels_need_not_have_slope_two
#print axioms slope_family
#print axioms mond_matching
#print axioms quarter_matching_iff

end PDNormalization
