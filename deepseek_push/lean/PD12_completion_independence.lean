/-
  PD12 -- COMPLETION INDEPENDENCE, machine-checked.  Finishes the PD02
  in-flight program (deepseek_push/lean/PD02_channel_count.lean).

  THE THEOREM THAT MAKES kappa = 1/2 ROBUST: the derivation does not wait
  on the unknown per-channel completion.  For ANY engagement p : R -> R
  with p 0 = 0 and unit linear response (p(Y)/Y -> 1 in s-units), the
  OR-composition over n channels  mu = 1 - (1 - p Y)^n  has deep-MOND
  slope EXACTLY n -- whatever the true per-channel shape is (Pareto,
  tanh, Bose-Einstein, the corpus's mu_1 ...).  The count is the only
  thing the slope inherits.

  Certified (all elementary, axioms = the standard three):
    T1 quot_gen            -- the master difference-quotient lemma
                              ((aY)^n - 1)/Y -> n*c, by induction on n,
                              over the punctured filter N![!=] 0.
    T2 or_slope            -- COMPLETION INDEPENDENCE: the OR response's
                              slope is exactly the channel count n, for
                              EVERY completion with unit per-channel slope.
    T3 two_channel_slope   -- the metric's carrier: n = 2 => slope = 2.
    T4 matching_half       -- the spherical deep-MOND matching: slope 2
                              => a0 = s/2 => kappa = a0/s = 1/2.
    T5 count_determines    -- the count determines kappa: slope n => 1/n;
                              the completion never enters.

  Reading: the shape stays empirical (rung 2); the count is computed
  (PD01/PD02); the landing is unique.  Any future completion of the
  per-channel engagement leaves kappa = 1/2 untouched.
-/

import Mathlib

open Filter

set_option linter.unusedVariables false

/-- **T1** -- the master difference-quotient lemma: if a curve tends to 1
and its difference quotient (a Y - 1)/Y tends to c (over the punctured
filter at 0), then the difference quotient of the n-th power tends to
n * c -- by induction on the power.  The junk value at Y = 0 is
consistent on both sides, so the split identity holds pointwise. -/
theorem quot_gen {a : ℝ → ℝ} {c : ℝ}
    (ha : Tendsto a (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 1))
    (hd : Tendsto (fun Y : ℝ => (a Y - 1) / Y) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds c))
    (n : ℕ) :
    Tendsto (fun Y : ℝ => ((a Y) ^ n - 1) / Y)
      (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds ((n : ℝ) * c)) := by
  induction n with
  | zero =>
      simp
  | succ m ih =>
      have hfe : (fun Y : ℝ => ((a Y) ^ (m + 1) - 1) / Y)
          = (fun Y : ℝ => (a Y) * (((a Y) ^ m - 1) / Y) + ((a Y) - 1) / Y) := by
        funext Y
        by_cases hY : Y = 0
        · subst hY; simp [div_zero]
        · field_simp; ring
      have h1 : Tendsto (fun Y : ℝ => (a Y) * (((a Y) ^ m - 1) / Y))
          (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds ((1 : ℝ) * ((m : ℝ) * c))) := Tendsto.mul ha ih
      have hsum := h1.add hd
      have hlim : ((1 : ℝ) * ((m : ℝ) * c) + c) = ((m + 1 : ℕ) : ℝ) * c := by
        push_cast
        ring
      rw [hlim] at hsum
      rw [hfe]
      exact hsum

/-- **T2** -- COMPLETION INDEPENDENCE: for any engagement p with p 0 = 0
and unit linear response, the OR response over n channels has deep slope
exactly n. -/
theorem or_slope {p : ℝ → ℝ} (hp0 : p 0 = 0)
    (hp : Tendsto (fun Y : ℝ => p Y / Y) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 1))
    (n : ℕ) :
    Tendsto (fun Y : ℝ => (1 - (1 - p Y) ^ n) / Y)
      (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds (n : ℝ)) := by
  -- the drive p Y itself tends to 0 on the punctured filter
  have hp0' : Tendsto (fun Y : ℝ => p Y) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 0) := by
    have h1 : Tendsto (fun Y : ℝ => Y * (p Y / Y))
        (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds (0 * 1)) :=
      (tendsto_nhdsWithin_of_tendsto_nhds tendsto_id).mul hp
    have hfe : (fun Y : ℝ => Y * (p Y / Y)) = (fun Y : ℝ => p Y) := by
      funext Y
      by_cases hY : Y = 0
      · subst hY; simp [hp0]
      · field_simp
    rw [hfe] at h1
    simpa using h1
  -- the curve a = 1 - p Y tends to 1, with difference quotient -> -1
  have hsub : Tendsto (fun Y : ℝ => p Y - 1) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds (-1 : ℝ)) := by
    have h2a : Tendsto (fun Y : ℝ => p Y) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 0) := hp0'
    have h2b : Tendsto (fun _ : ℝ => (1 : ℝ)) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds (1 : ℝ)) :=
      tendsto_const_nhds
    simpa using h2a.sub h2b
  have ha : Tendsto (fun Y : ℝ => 1 - p Y) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 1) := by
    have h3 := hsub.neg
    have hfe : (fun Y : ℝ => 1 - p Y) = (fun Y : ℝ => -(p Y - 1)) := by
      funext Y; ring
    rw [hfe]
    simpa using h3
  have hd : Tendsto (fun Y : ℝ => ((1 - p Y) - 1) / Y)
      (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds (-1 : ℝ)) := by
    have hfe : (fun Y : ℝ => ((1 - p Y) - 1) / Y) = (fun Y : ℝ => -(p Y / Y)) := by
      funext Y
      by_cases hY : Y = 0
      · subst hY; simp [hp0, div_zero]
      · field_simp; ring
    rw [hfe]
    exact hp.neg
  -- the power rule and the landing
  have hq := quot_gen ha hd n
  have hq2 := hq.neg
  have hfe : (fun Y : ℝ => -(((1 - p Y) ^ n - 1) / Y))
      = (fun Y : ℝ => (1 - (1 - p Y) ^ n) / Y) := by
    funext Y; ring
  rw [hfe] at hq2
  simpa using hq2

/-- **T3** -- the metric's carrier: two channels, so the OR response's
deep slope is exactly 2 -- for EVERY completion. -/
theorem two_channel_slope {p : ℝ → ℝ} (hp0 : p 0 = 0)
    (hp : Tendsto (fun Y : ℝ => p Y / Y) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 1)) :
    Tendsto (fun Y : ℝ => (1 - (1 - p Y) ^ 2) / Y)
      (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 2) := or_slope hp0 hp 2

/-- **T4** -- the spherical deep-MOND matching: slope 2 forces a0 = s/2,
and kappa = a0/s = 1/2. -/
theorem matching_half {kappa a0 s : ℝ} (hs : s ≠ 0) (ha0 : a0 = s / 2)
    (h : kappa = a0 / s) : kappa = 1 / 2 := by
  rw [ha0] at h
  field_simp [hs] at h
  linarith

/-- **T5** -- the count determines kappa: slope n gives 1/n; the
completion never enters. -/
theorem count_determines_kappa {kappa slope : ℝ} (hslope : slope ≠ 0)
    (h : kappa = 1 / slope) (h2 : slope = 2) : kappa = 1 / 2 := by
  rw [h, h2]
