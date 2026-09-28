import Mathlib
open MeasureTheory Real

/-! ### LR4b: cov discharge ASSEMBLY (Z7-wave successor lane)
    Stage bank (conductor, zero-sorry: bridges, pair Fubini, tri_fubini,
    disk_fubini, slice_subst, lr5_l2_cs) + outer_v (per-slice disk->chord map)
    + LR3b conditional chains with covStatement DISCHARGED by the
    conductor-proven disk Fubini.  -/

theorem step1_gen (r : ℝ) (hr : r ≠ 0) (F : ℝ → ℝ) :
    ∫ mu in (-1:ℝ)..1, F (r * mu) = (1/r) * ∫ v in (-r:ℝ)..r, F v := by
  rw [intervalIntegral.integral_comp_mul_left F hr, smul_eq_mul, inv_eq_one_div, mul_neg_one, mul_one]


noncomputable def chordVol (r mu : ℝ) : ℝ := r * mu + Real.sqrt (1 - r ^ 2 * (1 - mu ^ 2))

noncomputable def covStatement (H : ℝ → ℝ → ℝ) : Prop :=
  3 * ∫ r in (0:ℝ)..1, r ^ 2 * (1 / 2 * ∫ mu in (-1:ℝ)..1, H (r * Real.sqrt (1 - mu ^ 2)) (r * mu))
    = (3/2) * ∫ u in (0:ℝ)..1, ∫ v in -(Real.sqrt (1 - u ^ 2))..(Real.sqrt (1 - u ^ 2)), u * H u v

theorem setIcc_to_ivl (f : ℝ → ℝ) (a b : ℝ) (hab : a ≤ b) :
    ∫ x in Set.Icc a b, f x ∂volume = ∫ x in a..b, f x := by
  rw [← setIntegral_congr_set Ioc_ae_eq_Icc, ← intervalIntegral.integral_of_le hab]

theorem setIoc_to_ivl (f : ℝ → ℝ) (a b : ℝ) (hab : a ≤ b) :
    ∫ x in Set.Ioc a b, f x ∂volume = ∫ x in a..b, f x := by
  rw [← intervalIntegral.integral_of_le hab]

theorem pair_int (G : ℝ × ℝ → ℝ) (hG : Integrable G (volume.prod volume)) :
    ∫ x, ∫ y, G (x, y) ∂volume ∂volume = ∫ p, G p ∂(volume.prod volume) :=
  (integral_prod G hG).symm

theorem pair_swap (G : ℝ × ℝ → ℝ) (hG : Integrable G (volume.prod volume)) :
    ∫ x, ∫ y, G (x, y) ∂volume ∂volume = ∫ y, ∫ x, G (x, y) ∂volume ∂volume :=
  integral_integral_swap hG

theorem disk_fubini (Φ : ℝ → ℝ → ℝ) (hΦ : Continuous (fun p : ℝ × ℝ => Φ p.1 p.2)) :
    ∫ u in (0:ℝ)..1, ∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2), Φ u v
      = ∫ v in -(1:ℝ)..1, ∫ u in (0:ℝ)..Real.sqrt (1 - v ^ 2), Φ u v := by
  classical
  set D : Set (ℝ × ℝ) := {p | 0 ≤ p.1 ∧ p.1 ≤ 1 ∧ p.1 * p.1 + p.2 * p.2 ≤ 1} with hDdef
  have hDmem : ∀ a b : ℝ, 0 ≤ a → a ^ 2 + b ^ 2 ≤ 1 → (a, b) ∈ D := by
    intro a b ha h
    simp only [hDdef, Set.mem_setOf_eq]
    exact ⟨ha, by nlinarith [h, ha, sq_nonneg (a - 1)], by rw [← pow_two, ← pow_two]; exact h⟩
  have hD : MeasurableSet D := by
    have h1 : MeasurableSet {p : ℝ × ℝ | 0 ≤ p.1} := measurableSet_le measurable_const measurable_fst
    have h2 : MeasurableSet {p : ℝ × ℝ | p.1 ≤ 1} := measurableSet_le measurable_fst measurable_const
    have h3 : MeasurableSet {p : ℝ × ℝ | p.1 * p.1 + p.2 * p.2 ≤ 1} :=
      measurableSet_le
        (Measurable.add (measurable_fst.mul measurable_fst) (measurable_snd.mul measurable_snd))
        measurable_const
    exact h1.inter (h2.inter h3)
  have hDsub : D ⊆ Set.Icc (0:ℝ) 1 ×ˢ Set.Icc (-(1:ℝ)) 1 := by
    intro p hp
    obtain ⟨h1, h2, h3⟩ := hp
    exact ⟨⟨h1, h2⟩, ⟨by nlinarith [sq_nonneg p.2, h3], by nlinarith [sq_nonneg p.2, h3]⟩⟩
  have hcomp : ContinuousOn (fun p : ℝ × ℝ => Φ p.1 p.2)
      (Set.Icc (0:ℝ) 1 ×ˢ Set.Icc (-(1:ℝ)) 1) := hΦ.continuousOn
  obtain ⟨B₀, hB₀⟩ := IsCompact.exists_bound_of_continuousOn
    (isCompact_Icc.prod (isCompact_Icc (a := -(1:ℝ)) (b := 1))) hcomp
  have hB₀nn : 0 ≤ B₀ := by
    have hb := hB₀ (0, 0) ⟨⟨by norm_num, by norm_num⟩, ⟨by norm_num, by norm_num⟩⟩
    rw [Real.norm_eq_abs] at hb
    exact le_trans (abs_nonneg _) hb
  have hfinK : (volume.prod volume) (Set.Icc (0:ℝ) 1 ×ˢ Set.Icc (-(1:ℝ)) 1) < ⊤ := by
    rw [Measure.prod_prod]; simp
  have hfinD : (volume.prod volume) D ≠ ⊤ :=
    ne_top_of_le_ne_top (ne_of_lt hfinK) (measure_mono hDsub)
  have hint : Integrable (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (volume.prod volume) := by
    have hdom : Integrable (D.indicator (fun _ : ℝ × ℝ => (B₀:ℝ))) (volume.prod volume) := by
      refine (integrable_indicator_iff hD).mpr ?_
      exact integrableOn_const hfinD (by simp)
    refine Integrable.mono hdom (AEStronglyMeasurable.indicator
      (Continuous.aestronglyMeasurable hΦ) hD) ?_
    filter_upwards with p
    by_cases hp : p ∈ D
    · simp only [Set.indicator_of_mem hp]
      have hbb := hB₀ p (hDsub hp)
      simp only [Real.norm_eq_abs] at hbb ⊢
      have habs : |B₀| = B₀ := abs_eq_self.mpr hB₀nn
      rw [habs]
      exact hbb
    · simp [hp]
  have hint' : Integrable (fun p : ℝ × ℝ => (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) p)
      (volume.prod volume) := hint
  have hsliceA : (fun u : ℝ => (Set.Icc (0:ℝ) 1).indicator
      (fun u : ℝ => ∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2), Φ u v) u)
      =ᵐ[volume] (fun u : ℝ => ∫ v, (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v)) := by
    filter_upwards with u
    by_cases hu : u ∈ Set.Icc (0:ℝ) 1
    · have hkey : ∀ v : ℝ, v ^ 2 ≤ 1 - u ^ 2 ↔ |v| ≤ Real.sqrt (1 - u ^ 2) := by
        intro v
        have hh0 : 0 ≤ 1 - u ^ 2 := by nlinarith [hu.1, hu.2]
        constructor
        · intro h
          have h2 : v ^ 2 ≤ (Real.sqrt (1 - u ^ 2)) ^ 2 := by
            rw [Real.sq_sqrt hh0]; exact h
          have hab := (sq_le_sq (a := v) (b := Real.sqrt (1 - u ^ 2))).mp h2
          have habs2 : |Real.sqrt (1 - u ^ 2)| = Real.sqrt (1 - u ^ 2) :=
            abs_eq_self.mpr (Real.sqrt_nonneg _)
          rw [habs2] at hab
          exact hab
        · intro h
          have h2 : v ^ 2 ≤ (Real.sqrt (1 - u ^ 2)) ^ 2 :=
            (sq_le_sq (a := v) (b := Real.sqrt (1 - u ^ 2))).mpr (by
              rw [abs_eq_self.mpr (Real.sqrt_nonneg _)]; exact h)
          rwa [Real.sq_sqrt hh0] at h2
      have hset2 : {v : ℝ | u ^ 2 + v ^ 2 ≤ 1}
          = Set.Icc (-(Real.sqrt (1 - u ^ 2))) (Real.sqrt (1 - u ^ 2)) := by
        ext v
        simp only [Set.mem_setOf_eq, Set.mem_Icc]
        constructor
        · intro h
          exact abs_le.mp ((hkey v).mp (by linarith [h]))
        · intro h
          exact by linarith [(hkey v).mpr (abs_le.mpr h)]
      have hcongr : ∀ v : ℝ, (Set.Icc (-(Real.sqrt (1 - u ^ 2))) (Real.sqrt (1 - u ^ 2))).indicator
          (fun v => Φ u v) v = (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v) := by
        intro v
        by_cases hv : u ^ 2 + v ^ 2 ≤ 1
        · rw [Set.indicator_of_mem (by rw [← hset2]; exact hv),
            Set.indicator_of_mem (hDmem u v hu.1 hv)]
        · rw [Set.indicator_of_notMem (by rw [← hset2]; simpa using hv),
            Set.indicator_of_notMem (by
              intro hc
              simp only [hDdef, Set.mem_setOf_eq] at hc
              exact hv (by linarith [hc.2.2]))]
      simp only [Set.indicator_of_mem hu]
      rw [← setIcc_to_ivl (f := fun v => Φ u v) (a := -(Real.sqrt (1 - u ^ 2)))
        (b := Real.sqrt (1 - u ^ 2))
        (by exact neg_le_self_iff.mpr (by linarith [Real.sqrt_nonneg (1 - u ^ 2)]))]
      rw [← integral_indicator (hs := measurableSet_Icc)
        (s := Set.Icc (-(Real.sqrt (1 - u ^ 2))) (Real.sqrt (1 - u ^ 2)))]
      rw [integral_congr_ae (Filter.Eventually.of_forall hcongr)]
    · have hcongr : (fun v : ℝ => (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v))
          =ᵐ[volume] (fun _ : ℝ => (0:ℝ)) :=
        Filter.Eventually.of_forall (fun v => by
          have hnot : (u, v) ∉ D := fun hmem => hu ⟨hmem.1, hmem.2.1⟩
          show (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v) = (0:ℝ)
          rw [Set.indicator_of_notMem hnot])
      rw [Set.indicator_of_notMem hu, integral_congr_ae hcongr, integral_zero]
  have hsliceB : (fun v : ℝ => (Set.Icc (-(1:ℝ)) 1).indicator
      (fun v : ℝ => ∫ u in (0:ℝ)..Real.sqrt (1 - v ^ 2), Φ u v) v)
      =ᵐ[volume] (fun v : ℝ => ∫ u, (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v)) := by
    filter_upwards with v
    by_cases hv : v ∈ Set.Icc (-(1:ℝ)) 1
    · have hkey : ∀ u : ℝ, 0 ≤ u → (u ^ 2 ≤ 1 - v ^ 2 ↔ u ≤ Real.sqrt (1 - v ^ 2)) := by
        intro u hu0
        have hh0 : 0 ≤ 1 - v ^ 2 := by nlinarith [hv.1, hv.2]
        constructor
        · intro h
          have h2 : u ^ 2 ≤ (Real.sqrt (1 - v ^ 2)) ^ 2 := by
            rw [Real.sq_sqrt hh0]; exact h
          have hab := (sq_le_sq (a := u) (b := Real.sqrt (1 - v ^ 2))).mp h2
          have habs2 : |Real.sqrt (1 - v ^ 2)| = Real.sqrt (1 - v ^ 2) :=
            abs_eq_self.mpr (Real.sqrt_nonneg _)
          rw [habs2, abs_eq_self.mpr hu0] at hab
          exact hab
        · intro h
          have h2 : u ^ 2 ≤ (Real.sqrt (1 - v ^ 2)) ^ 2 :=
            (sq_le_sq (a := u) (b := Real.sqrt (1 - v ^ 2))).mpr (by
              rw [abs_eq_self.mpr (Real.sqrt_nonneg _), abs_eq_self.mpr hu0]; exact h)
          rwa [Real.sq_sqrt hh0] at h2
      have hset2 : {u : ℝ | 0 ≤ u ∧ u ^ 2 + v ^ 2 ≤ 1}
          = Set.Icc (0:ℝ) (Real.sqrt (1 - v ^ 2)) := by
        ext u
        simp only [Set.mem_setOf_eq, Set.mem_Icc]
        constructor
        · intro h
          exact ⟨h.1, (hkey u h.1).mp (by linarith [h.2])⟩
        · intro h
          exact ⟨h.1, by linarith [(hkey u h.1).mpr h.2]⟩
      have hcongr : ∀ u : ℝ, (Set.Icc (0:ℝ) (Real.sqrt (1 - v ^ 2))).indicator
          (fun u => Φ u v) u = (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v) := by
        intro u
        by_cases hu : 0 ≤ u ∧ u ^ 2 + v ^ 2 ≤ 1
        · rw [Set.indicator_of_mem (by rw [← hset2]; exact hu),
            Set.indicator_of_mem (hDmem u v hu.1 hu.2)]
        · rw [Set.indicator_of_notMem (by rw [← hset2]; tauto),
            Set.indicator_of_notMem (by
              intro hc
              simp only [hDdef, Set.mem_setOf_eq] at hc
              rw [← pow_two, ← pow_two] at hc
              exact hu ⟨hc.1, hc.2.2⟩)]
      simp only [Set.indicator_of_mem hv]
      rw [← setIoc_to_ivl (f := fun u => Φ u v) (a := (0:ℝ)) (b := Real.sqrt (1 - v ^ 2))
        (Real.sqrt_nonneg _)]
      rw [setIntegral_congr_set Ioc_ae_eq_Icc]
      rw [← integral_indicator (hs := measurableSet_Icc)
        (s := Set.Icc (0:ℝ) (Real.sqrt (1 - v ^ 2)))]
      rw [integral_congr_ae (Filter.Eventually.of_forall hcongr)]
    · have hcongr : (fun u : ℝ => (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v))
          =ᵐ[volume] (fun _ : ℝ => (0:ℝ)) :=
        Filter.Eventually.of_forall (fun u => by
          have hnot : (u, v) ∉ D := fun hmem => hv ⟨by nlinarith [hmem.2.2, sq_nonneg (v + 1)],
            by nlinarith [hmem.2.2, sq_nonneg (v - 1)]⟩
          show (D.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (u, v) = (0:ℝ)
          rw [Set.indicator_of_notMem hnot])
      rw [Set.indicator_of_notMem hv, integral_congr_ae hcongr, integral_zero]
  rw [intervalIntegral.integral_of_le (by norm_num : (0:ℝ) ≤ 1)]
  rw [setIntegral_congr_set Ioc_ae_eq_Icc]
  rw [← integral_indicator (hs := measurableSet_Icc) (s := Set.Icc (0:ℝ) 1)]
  rw [integral_congr_ae hsliceA]
  rw [pair_int _ hint']
  rw [intervalIntegral.integral_of_le (by norm_num : (-(1:ℝ)) ≤ 1)]
  rw [setIntegral_congr_set Ioc_ae_eq_Icc]
  rw [← integral_indicator (hs := measurableSet_Icc) (s := Set.Icc (-(1:ℝ)) 1)]
  rw [integral_congr_ae hsliceB]
  rw [← pair_swap _ hint']
  rw [pair_int _ hint']

theorem tri_fubini (Φ : ℝ → ℝ → ℝ) (hΦ : Continuous (fun p : ℝ × ℝ => Φ p.1 p.2)) :
    ∫ r in (0:ℝ)..1, ∫ v in (0:ℝ)..r, Φ r v
      = ∫ v in (0:ℝ)..1, ∫ r in v..1, Φ r v := by
  classical
  set T : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ p.1} with hTdef
  have hT : MeasurableSet T := by
    have h1 : MeasurableSet {p : ℝ × ℝ | 0 < p.1} := measurableSet_lt measurable_const measurable_fst
    have h2 : MeasurableSet {p : ℝ × ℝ | p.1 ≤ 1} := measurableSet_le measurable_fst measurable_const
    have h3 : MeasurableSet {p : ℝ × ℝ | 0 < p.2} := measurableSet_lt measurable_const measurable_snd
    have h4 : MeasurableSet {p : ℝ × ℝ | p.2 ≤ p.1} := measurableSet_le measurable_snd measurable_fst
    exact h1.inter (h2.inter (h3.inter h4))
  have hTsub : T ⊆ Set.Icc (0:ℝ) 1 ×ˢ Set.Icc (0:ℝ) 1 := by
    intro p hp
    obtain ⟨h1, h2, h3, h4⟩ := hp
    exact ⟨⟨le_of_lt h1, h2⟩, ⟨le_of_lt h3, h4.trans h2⟩⟩
  have hcomp : ContinuousOn (fun p : ℝ × ℝ => Φ p.1 p.2) (Set.Icc (0:ℝ) 1 ×ˢ Set.Icc (0:ℝ) 1) :=
    hΦ.continuousOn
  obtain ⟨B₀, hB₀⟩ := IsCompact.exists_bound_of_continuousOn (isCompact_Icc.prod isCompact_Icc) hcomp
  have hB₀nn : 0 ≤ B₀ := by
    have hb := hB₀ (0, 0) ⟨⟨by norm_num, by norm_num⟩, ⟨by norm_num, by norm_num⟩⟩
    rw [Real.norm_eq_abs] at hb
    exact le_trans (abs_nonneg _) hb
  have hfinK : (volume.prod volume) (Set.Icc (0:ℝ) 1 ×ˢ Set.Icc (0:ℝ) 1) < ⊤ := by
    rw [Measure.prod_prod]; simp
  have hfinT : (volume.prod volume) T ≠ ⊤ :=
    ne_top_of_le_ne_top (ne_of_lt hfinK) (measure_mono hTsub)
  have hint : Integrable (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (volume.prod volume) := by
    have hdom : Integrable (T.indicator (fun _ : ℝ × ℝ => (B₀:ℝ))) (volume.prod volume) := by
      refine (integrable_indicator_iff hT).mpr ?_
      exact integrableOn_const hfinT (by simp)
    refine Integrable.mono hdom (AEStronglyMeasurable.indicator
      (Continuous.aestronglyMeasurable hΦ) hT) ?_
    filter_upwards with p
    by_cases hp : p ∈ T
    · simp only [Set.indicator_of_mem hp]
      have hbb := hB₀ p (hTsub hp)
      simp only [Real.norm_eq_abs] at hbb ⊢
      have habs : |B₀| = B₀ := abs_eq_self.mpr hB₀nn
      rw [habs]
      exact hbb
    · simp [hp]
  have hint' : Integrable (fun p : ℝ × ℝ => (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) p)
      (volume.prod volume) := hint
  have hsliceA : (fun r : ℝ => (Set.Ioc (0:ℝ) 1).indicator
      (fun r : ℝ => ∫ v in (0:ℝ)..r, Φ r v) r)
      =ᵐ[volume] (fun r : ℝ => ∫ v, (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v)) := by
    filter_upwards with r
    by_cases hr : r ∈ Set.Ioc (0:ℝ) 1
    · have hcongr : ∀ v : ℝ, (Set.Ioc (0:ℝ) r).indicator (fun v => Φ r v) v
          = (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v) := by
        intro v
        by_cases hv : v ∈ Set.Ioc (0:ℝ) r
        · have hTm : (r, v) ∈ T := ⟨hr.1, hr.2, hv.1, hv.2⟩
          simp only [Set.indicator_of_mem hv, Set.indicator_of_mem hTm]
        · have hnot : (r, v) ∉ T := fun hmem => hv ⟨hmem.2.2.1, hmem.2.2.2⟩
          simp only [Set.indicator_of_notMem hv, Set.indicator_of_notMem hnot]
      simp only [Set.indicator_of_mem hr]
      rw [intervalIntegral.integral_of_le hr.1.le]
      rw [← integral_indicator (hs := measurableSet_Ioc) (s := Set.Ioc (0:ℝ) r)]
      rw [integral_congr_ae (Filter.Eventually.of_forall hcongr)]
    · have hcongr : (fun v : ℝ => (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v))
          =ᵐ[volume] (fun _ : ℝ => (0:ℝ)) :=
        Filter.Eventually.of_forall (fun v => by
          have hnot : (r, v) ∉ T := fun hmem => hr ⟨hmem.1, hmem.2.1⟩
          show (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v) = (0:ℝ)
          rw [Set.indicator_of_notMem hnot])
      rw [Set.indicator_of_notMem hr, integral_congr_ae hcongr, integral_zero]
  have hsliceB : (fun v : ℝ => (Set.Ioc (0:ℝ) 1).indicator
      (fun v : ℝ => ∫ r in v..1, Φ r v) v)
      =ᵐ[volume] (fun v : ℝ => ∫ r, (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v)) := by
    filter_upwards with v
    by_cases hv : v ∈ Set.Ioc (0:ℝ) 1
    · have hcongr : ∀ r : ℝ, (Set.Icc v 1).indicator (fun r => Φ r v) r
          = (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v) := by
        intro r
        by_cases hr : r ∈ Set.Icc v 1
        · have hTm : (r, v) ∈ T := ⟨lt_of_lt_of_le hv.1 hr.1, hr.2, hv.1, hr.1⟩
          simp only [Set.indicator_of_mem hr, Set.indicator_of_mem hTm]
        · have hnot : (r, v) ∉ T := fun hmem => hr ⟨hmem.2.2.2, hmem.2.1⟩
          simp only [Set.indicator_of_notMem hr, Set.indicator_of_notMem hnot]
      simp only [Set.indicator_of_mem hv]
      rw [intervalIntegral.integral_of_le hv.2]
      rw [setIntegral_congr_set Ioc_ae_eq_Icc]
      rw [← integral_indicator (hs := measurableSet_Icc) (s := Set.Icc v 1)]
      rw [integral_congr_ae (Filter.Eventually.of_forall hcongr)]
    · have hcongr : (fun r : ℝ => (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v))
          =ᵐ[volume] (fun _ : ℝ => (0:ℝ)) :=
        Filter.Eventually.of_forall (fun r => by
          have hnot : (r, v) ∉ T := fun hmem => hv ⟨hmem.2.2.1, le_trans hmem.2.2.2 hmem.2.1⟩
          show (T.indicator (fun p : ℝ × ℝ => Φ p.1 p.2)) (r, v) = (0:ℝ)
          rw [Set.indicator_of_notMem hnot])
      rw [Set.indicator_of_notMem hv, integral_congr_ae hcongr, integral_zero]
  rw [intervalIntegral.integral_of_le (by norm_num : (0:ℝ) ≤ 1)]
  rw [← integral_indicator (hs := measurableSet_Ioc) (s := Set.Ioc (0:ℝ) 1)]
  rw [integral_congr_ae hsliceA]
  rw [pair_int _ hint']
  rw [intervalIntegral.integral_of_le (by norm_num : (0:ℝ) ≤ 1)]
  rw [← integral_indicator (hs := measurableSet_Ioc) (s := Set.Ioc (0:ℝ) 1)]
  rw [integral_congr_ae hsliceB]
  rw [← pair_swap _ hint']
  rw [pair_int _ hint']

#print axioms tri_fubini

theorem slice_subst (H : ℝ → ℝ → ℝ) (hHc : Continuous (fun p : ℝ × ℝ => H p.1 p.2))
    (w : ℝ) (hw : 0 ≤ w) (hw1 : w ≤ 1) (c : ℝ) :
    ∫ r in w..1, r * H (Real.sqrt (r ^ 2 - w ^ 2)) c
      = ∫ u in (0:ℝ)..Real.sqrt (1 - w ^ 2), u * H u c := by
  by_cases hw0 : w = 0
  · subst hw0
    have key : ∫ r in (0:ℝ)..1, r * H (Real.sqrt (r ^ 2 - (0:ℝ) ^ 2)) c
        = ∫ r in (0:ℝ)..1, r * H r c := by
      refine intervalIntegral.integral_congr (fun r hr => ?_)
      show r * H (Real.sqrt (r ^ 2 - (0:ℝ) ^ 2)) c = r * H r c
      have hr01 : (0:ℝ) ≤ r := by
        rw [Set.uIcc_of_le (by norm_num : (0:ℝ) ≤ 1)] at hr
        exact hr.1
      rw [show ((r:ℝ) ^ 2 - (0:ℝ) ^ 2) = r ^ 2 from by ring, Real.sqrt_sq_eq_abs,
        abs_eq_self.mpr hr01]
    rw [show (((1:ℝ) - (0:ℝ) ^ 2)) = 1 from by ring, Real.sqrt_one]
    exact key
  · have hwpos : 0 < w := lt_of_le_of_ne hw (Ne.symm hw0)
    set b : ℝ := Real.sqrt (1 - w ^ 2) with hbdef
    have hb0 : 0 ≤ 1 - w ^ 2 := by nlinarith [sq_nonneg w, hw1]
    have hbsq : b ^ 2 = 1 - w ^ 2 := Real.sq_sqrt hb0
    have hbpos : 0 ≤ b := Real.sqrt_nonneg _
    have hw2pos : (0:ℝ) < w ^ 2 := sq_pos_of_ne_zero hwpos.ne.symm
    have hf' : ∀ u ∈ Set.uIcc (0:ℝ) b, HasDerivAt (fun x => Real.sqrt (x ^ 2 + w ^ 2))
        (u / Real.sqrt (u ^ 2 + w ^ 2)) u := by
      intro u _
      have hpos : (0:ℝ) < u ^ 2 + w ^ 2 := by linarith [sq_nonneg u, hw2pos]
      have hg2 : HasDerivAt (fun x : ℝ => x ^ 2 + w ^ 2) (2 * u) u :=
        ((hasDerivAt_pow 2 u).add_const (w ^ 2)).congr_deriv (by norm_num)
      have hsqrt : HasDerivAt (fun x => Real.sqrt x) (1 / (2 * Real.sqrt (u ^ 2 + w ^ 2)))
          (u ^ 2 + w ^ 2) := Real.hasDerivAt_sqrt (ne_of_gt hpos)
      have key : HasDerivAt ((fun x => Real.sqrt x) ∘ (fun x : ℝ => x ^ 2 + w ^ 2))
          ((1 / (2 * Real.sqrt (u ^ 2 + w ^ 2))) * (2 * u)) u := HasDerivAt.comp u hsqrt hg2
      exact key.congr_deriv (by ring)
    have hden : ∀ x : ℝ, Real.sqrt (x ^ 2 + w ^ 2) ≠ 0 := by
      intro x
      have hp : (0:ℝ) < x ^ 2 + w ^ 2 := by linarith [sq_nonneg x, hw2pos]
      exact ne_of_gt (Real.sqrt_pos.mpr hp)
    have hfc : ContinuousOn (fun u => u / Real.sqrt (u ^ 2 + w ^ 2)) (Set.uIcc (0:ℝ) b) :=
      (Continuous.div (by fun_prop) (by fun_prop) hden).continuousOn
    have hpoly : Continuous (fun r => r ^ 2 - w ^ 2) := by continuity
    have hslice : Continuous (fun r => H (Real.sqrt (r ^ 2 - w ^ 2)) c) :=
      hHc.comp (Continuous.prodMk (Continuous.sqrt hpoly) (by fun_prop))
    have hgc : Continuous (fun r => r * H (Real.sqrt (r ^ 2 - w ^ 2)) c) :=
      Continuous.mul (by fun_prop) hslice
    have hf0 : Real.sqrt ((0:ℝ) ^ 2 + w ^ 2) = w := by
      rw [show ((0:ℝ) ^ 2 + w ^ 2) = w ^ 2 from by ring, Real.sqrt_sq_eq_abs,
        abs_eq_self.mpr hw]
    have hfb : Real.sqrt (b ^ 2 + w ^ 2) = 1 := by
      rw [hbsq, show ((1 - w ^ 2) + w ^ 2) = (1:ℝ) from by ring, Real.sqrt_one]
    have hcongr : ∀ u ∈ Set.uIcc (0:ℝ) b,
        (fun x => (fun v => v / Real.sqrt (v ^ 2 + w ^ 2)) x •
          ((fun r => r * H (Real.sqrt (r ^ 2 - w ^ 2)) c) ∘
            (fun x => Real.sqrt (x ^ 2 + w ^ 2))) x) u
        = (fun u => u * H u c) u := by
      intro u hu
      have hu01 : u ∈ Set.Icc (0:ℝ) b := (Set.uIcc_of_le hbpos) ▸ hu
      show (u / Real.sqrt (u ^ 2 + w ^ 2)) *
          (Real.sqrt (u ^ 2 + w ^ 2) *
            H (Real.sqrt ((Real.sqrt (u ^ 2 + w ^ 2)) ^ 2 - w ^ 2)) c)
          = u * H u c
      have hsq : (Real.sqrt (u ^ 2 + w ^ 2)) ^ 2 - w ^ 2 = u ^ 2 := by
        rw [Real.sq_sqrt (by linarith [sq_nonneg u, hw2pos] : (0:ℝ) ≤ u ^ 2 + w ^ 2)]
        ring
      rw [hsq, Real.sqrt_sq_eq_abs, abs_eq_self.mpr hu01.1]
      field_simp
    have hsub := intervalIntegral.integral_deriv_smul_comp
      (f := fun x => Real.sqrt (x ^ 2 + w ^ 2))
      (f' := fun u => u / Real.sqrt (u ^ 2 + w ^ 2))
      (g := fun r => r * H (Real.sqrt (r ^ 2 - w ^ 2)) c) hf' hfc hgc
    rw [intervalIntegral.integral_congr hcongr] at hsub
    rw [hf0, hfb] at hsub
    exact hsub.symm

theorem lr5_l2_cs {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}
    (f g : Ω → ℝ) (hf : MemLp f 2 μ) (hg : MemLp g 2 μ) :
    (∫ x, f x * g x ∂μ) ^ 2 ≤ (∫ x, f x ^ 2 ∂μ) * (∫ x, g x ^ 2 ∂μ) := by
  classical
  have hf2 : Integrable (fun x => f x ^ 2) μ := hf.integrable_sq
  have hg2 : Integrable (fun x => g x ^ 2) μ := hg.integrable_sq
  have hfg : Integrable (fun x => f x * g x) μ := hf.integrable_mul hg
  have hDge : 0 ≤ ∫ x, f x ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg (f x))
  have hAge : 0 ≤ ∫ x, g x ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg (g x))
  have hexp : ∀ t : ℝ, ∫ x, (f x - t * g x) ^ 2 ∂μ
      = (∫ x, f x ^ 2 ∂μ) - 2 * t * (∫ x, f x * g x ∂μ) + t * t * (∫ x, g x ^ 2 ∂μ) := by
    intro t
    have i2 : Integrable (fun x => 2 * t * (f x * g x)) μ := hfg.const_mul (2 * t)
    have i3 : Integrable (fun x => t * t * (g x ^ 2)) μ := hg2.const_mul (t * t)
    have s1 : Integrable (fun x => f x ^ 2 - 2 * t * (f x * g x)) μ := hf2.sub i2
    have hcongr : (fun x => (f x - t * g x) ^ 2) =ᵐ[μ]
        (fun x => f x ^ 2 - 2 * t * (f x * g x) + t * t * (g x ^ 2)) :=
      Filter.Eventually.of_forall (fun x => by ring)
    rw [integral_congr_ae hcongr, integral_add s1 i3, integral_sub hf2 i2,
        integral_const_mul, integral_const_mul]
  set A : ℝ := ∫ x, g x ^ 2 ∂μ with hAdef
  set C : ℝ := ∫ x, f x * g x ∂μ with hCdef
  set D : ℝ := ∫ x, f x ^ 2 ∂μ with hDdef
  by_cases hA : A = 0
  · have hint0 : ∫ x, g x ^ 2 ∂μ = 0 := by rw [← hAdef]; exact hA
    have hg0 : (fun x => g x ^ 2) =ᵐ[μ] (fun _ : Ω => (0:ℝ)) :=
      (integral_eq_zero_iff_of_nonneg (fun x => sq_nonneg (g x)) hg2).mp hint0
    have hfg0 : (fun x => f x * g x) =ᵐ[μ] (fun _ : Ω => (0:ℝ)) := by
      filter_upwards [hg0] with x hx
      have hgx : g x = 0 := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp hx
      simp [hgx]
    have hC0 : C = 0 := by
      rw [hCdef, integral_congr_ae hfg0, integral_zero]
    rw [hC0, hA]
    simp
  · have hApos : 0 < A := lt_of_le_of_ne hAge (Ne.symm hA)
    have hq : 0 ≤ ∫ x, (f x - (C / A) * g x) ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg _)
    rw [hexp (C / A)] at hq
    have h2 : 0 ≤ A * (D - 2 * (C / A) * C + (C / A) * (C / A) * A) := by
      nlinarith [hq, hApos]
    have h3 : A * (D - 2 * (C / A) * C + (C / A) * (C / A) * A) = A * D - C * C := by
      have hne : A ≠ 0 := Ne.symm (hApos.ne)
      field_simp
      ring
    linarith [h2, h3]

#print axioms tri_fubini
#print axioms disk_fubini
#print axioms slice_subst
#print axioms lr5_l2_cs

theorem outer_v (G : ℝ → ℝ → ℝ) (hGc : Continuous (fun p : ℝ × ℝ => G p.1 p.2))
    (v : ℝ) (hv : |v| ≤ 1) :
    ∫ r in Set.Icc (|v|) 1, (fun r => r * G (Real.sqrt (r ^ 2 - v ^ 2)) v) r ∂volume
      = ∫ u in (0:ℝ)..Real.sqrt (1 - v ^ 2), u * G u v := by
  have hw0 : 0 ≤ |v| := abs_nonneg v
  have hsq : |v| ^ 2 = v ^ 2 := by
    have h := sq_abs v
    rw [pow_two, pow_two] at h
    linarith [h]
  rw [← setIntegral_congr_set Ioc_ae_eq_Icc, ← intervalIntegral.integral_of_le hv]
  have hgoal : ∫ r in |v|..1, r * G (Real.sqrt (r ^ 2 - |v| ^ 2)) v
      = ∫ u in (0:ℝ)..Real.sqrt (1 - |v| ^ 2), u * G u v :=
    slice_subst (H := G) (hHc := hGc) (w := |v|) (hw := hw0) (hw1 := hv) (c := v)
  rw [hsq] at hgoal
  exact hgoal

theorem val_I1 : ∫ u in (0:ℝ)..1, ((1:ℝ) * u ^ 1 + (1:ℝ) * u ^ 3 + (-2:ℝ) * u ^ 5) = ((5:ℚ)/12 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun u => (1:ℝ)*u^1 + (1:ℝ)*u^3) (g := fun u => (-2:ℝ)*u^5)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (1:ℝ)*u^1) (g := fun u => (1:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, integral_pow, integral_pow, integral_pow]
  norm_num

theorem outer_I1val : ∫ x in (0:ℝ)..1,
    ((2/3:ℝ) * x ^ 1 + (2/3:ℝ) * x ^ 3 + (-4/3:ℝ) * x ^ 5) = ((5:ℚ)/18 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun x => (2/3:ℝ)*x^1 + (2/3:ℝ)*x^3)
      (g := fun x => (-4/3:ℝ)*x^5)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun x => (2/3:ℝ)*x^1) (g := fun x => (2/3:ℝ)*x^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, integral_pow, integral_pow, integral_pow]
  norm_num

theorem chord_cond (cov : ∀ H : ℝ → ℝ → ℝ,
    Continuous (fun p : ℝ × ℝ => H p.1 p.2) → covStatement H) :
    3 * (∫ r in (0:ℝ)..1, r ^ 2 * (1 / 2 * (∫ mu in (-1:ℝ)..1, chordVol r mu))) = 3/4 := by
  have inst : covStatement (fun u v => v + Real.sqrt (1 - u ^ 2)) := cov _ (by fun_prop)
  simp only [covStatement] at inst
  have hmucongr : ∀ r : ℝ, Set.EqOn (fun mu : ℝ => chordVol r mu)
      (fun mu : ℝ => (r * mu) + Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2))
      (Set.uIcc (-(1:ℝ)) 1) := by
    intro r mu hmu
    simp only [chordVol]
    have hb : mu ∈ Set.Icc (-(1:ℝ)) 1 := by
      rw [← Set.uIcc_of_le (by norm_num : (-(1:ℝ)) ≤ 1)]
      exact hmu
    have h1 : (-(1:ℝ)) ≤ mu := hb.1
    have h2 : mu ≤ 1 := hb.2
    rw [mul_pow, sq_sqrt (by nlinarith [sq_nonneg mu, h1, h2])]
  rw [intervalIntegral.integral_congr (show Set.EqOn
      (fun r : ℝ => r ^ 2 * (1 / 2 * ∫ mu in (-1:ℝ)..1, chordVol r mu))
      (fun r : ℝ => r ^ 2 * (1 / 2 * ∫ mu in (-1:ℝ)..1,
        (r * mu) + Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2)))
      (Set.uIcc (0:ℝ) 1) from by
      intro r hr
      exact congrArg (fun X : ℝ => r ^ 2 * (1 / 2 * X))
        (intervalIntegral.integral_congr (hmucongr r)))]
  rw [inst]
  rw [intervalIntegral.integral_congr (show Set.EqOn
      (fun u => ∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (v + Real.sqrt (1 - u ^ 2)))
      (fun u => 2 * u * (1 - u ^ 2)) (Set.uIcc (0:ℝ) 1) from by
      intro u hu
      have hu2 : u ∈ Set.Icc (0:ℝ) 1 := by
        rw [← Set.uIcc_of_le (by norm_num : (0:ℝ) ≤ 1)]
        exact hu
      have hs : 0 ≤ 1 - u ^ 2 := by
        have h1 : (0:ℝ) ≤ u := hu2.1
        have h2 : u ≤ 1 := hu2.2
        nlinarith [sq_nonneg u]
      show (∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (v + Real.sqrt (1 - u ^ 2))) = 2 * u * (1 - u ^ 2)
      have h2 : 2 * u * Real.sqrt (1 - u ^ 2) ^ 2 = 2 * u * (1 - u ^ 2) := by
        rw [Real.sq_sqrt hs]
      simp only [show ∀ v : ℝ, u * (v + Real.sqrt (1 - u ^ 2))
        = (u * Real.sqrt (1 - u ^ 2)) + u * v ^ 1 from by intro v; ring]
      rw [intervalIntegral.integral_add (f := fun v => u * Real.sqrt (1 - u ^ 2))
        (g := fun v => u * v ^ 1)
        (Continuous.intervalIntegrable (by fun_prop) _ _)
        (Continuous.intervalIntegrable (by fun_prop) _ _)]
      simp only [intervalIntegral.integral_const_mul, intervalIntegral.integral_const,
        integral_pow, smul_eq_mul]
      ring_nf
      linear_combination h2)]
  simp only [show ∀ u : ℝ, (2 * u * (1 - u ^ 2)) = (2:ℝ) * u ^ 1 + (-2:ℝ) * u ^ 3 from by intro u; ring]
  rw [intervalIntegral.integral_add (f := fun u => (2:ℝ)*u^1) (g := fun u => (-2:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      integral_pow, integral_pow]
  norm_num

theorem I1_cond (cov : ∀ H : ℝ → ℝ → ℝ,
    Continuous (fun p : ℝ × ℝ => H p.1 p.2) → covStatement H) :
    3 * (∫ r in (0:ℝ)..1, r ^ 2 * (1 / 2 * (∫ mu in (-1:ℝ)..1,
        (r * Real.sqrt (1 - mu ^ 2)) ^ 2 * (Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2) - r * mu)
        + ((Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2)) ^ 3 - (r * mu) ^ 3) / 3))) = 5/12 := by
  have inst : covStatement (fun u v => u ^ 2 * (Real.sqrt (1 - u ^ 2) - v)
      + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3) :=
    cov _ (by show Continuous (fun p : ℝ × ℝ => p.1 ^ 2 * (Real.sqrt (1 - p.1 ^ 2) - p.2)
      + ((Real.sqrt (1 - p.1 ^ 2)) ^ 3 - p.2 ^ 3) / 3); fun_prop)
  simp only [covStatement] at inst
  rw [inst]
  rw [intervalIntegral.integral_congr (show Set.EqOn
      (fun u => ∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (u ^ 2 * (Real.sqrt (1 - u ^ 2) - v) + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3))
      (fun u => 2 * u ^ 3 * (1 - u ^ 2) + (2/3) * u * (1 - u ^ 2) ^ 2) (Set.uIcc (0:ℝ) 1) from by
      intro u hu
      have hu2 : u ∈ Set.Icc (0:ℝ) 1 := by
        rw [← Set.uIcc_of_le (by norm_num : (0:ℝ) ≤ 1)]
        exact hu
      have hs : 0 ≤ 1 - u ^ 2 := by
        have h1 : (0:ℝ) ≤ u := hu2.1
        have h2 : u ≤ 1 := hu2.2
        nlinarith [sq_nonneg u]
      show (∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (u ^ 2 * (Real.sqrt (1 - u ^ 2) - v) + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3))
        = 2 * u ^ 3 * (1 - u ^ 2) + (2/3) * u * (1 - u ^ 2) ^ 2
      have hs2 : Real.sqrt (1 - u ^ 2) ^ 2 = 1 - u ^ 2 := Real.sq_sqrt hs
      have h4 : Real.sqrt (1 - u ^ 2) ^ 4 = (1 - u ^ 2) ^ 2 := by
        rw [show (Real.sqrt (1 - u ^ 2)) ^ 4
          = (Real.sqrt (1 - u ^ 2)) ^ 2 * (Real.sqrt (1 - u ^ 2)) ^ 2 from by ring, hs2]
        ring
      have h2 : 2 * u ^ 3 * Real.sqrt (1 - u ^ 2) ^ 2 + (2/3) * u * Real.sqrt (1 - u ^ 2) ^ 4
          = 2 * u ^ 3 * (1 - u ^ 2) + (2/3) * u * (1 - u ^ 2) ^ 2 := by
        rw [hs2, h4]
      simp only [show ∀ v : ℝ, u * (u ^ 2 * (Real.sqrt (1 - u ^ 2) - v)
          + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3)
        = (u ^ 3 * Real.sqrt (1 - u ^ 2) + u * (Real.sqrt (1 - u ^ 2)) ^ 3 / 3)
          + (-(u ^ 3)) * v ^ 1 + (-(u / 3)) * v ^ 3 from by intro v; ring]
      rw [intervalIntegral.integral_add
        (f := fun v => (u ^ 3 * Real.sqrt (1 - u ^ 2) + u * (Real.sqrt (1 - u ^ 2)) ^ 3 / 3)
          + (-(u ^ 3)) * v ^ 1)
        (g := fun v => (-(u / 3)) * v ^ 3)
        (Continuous.intervalIntegrable (by fun_prop) _ _)
        (Continuous.intervalIntegrable (by fun_prop) _ _)]
      rw [intervalIntegral.integral_add
        (f := fun v => (u ^ 3 * Real.sqrt (1 - u ^ 2) + u * (Real.sqrt (1 - u ^ 2)) ^ 3 / 3))
        (g := fun v => (-(u ^ 3)) * v ^ 1)
        (Continuous.intervalIntegrable (by fun_prop) _ _)
        (Continuous.intervalIntegrable (by fun_prop) _ _)]
      simp only [intervalIntegral.integral_const, intervalIntegral.integral_const_mul,
        integral_pow, smul_eq_mul]
      ring_nf
      linear_combination h2)]
  simp only [show ∀ x : ℝ, (2 * x ^ 3 * (1 - x ^ 2) + (2/3) * x * (1 - x ^ 2) ^ 2)
      = (2/3:ℝ) * x ^ 1 + (2/3:ℝ) * x ^ 3 + (-4/3:ℝ) * x ^ 5 from by intro x; ring]
  rw [outer_I1val]
  ring

#print axioms outer_v
#print axioms chord_cond
#print axioms I1_cond
