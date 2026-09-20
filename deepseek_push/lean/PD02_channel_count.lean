/-
  PD02 -- the channel-count core of kappa = 1/2, Lean-certified.

  STATUS: IN-FLIGHT (2026-09-19) -- does not compile yet (four error sites in
  the filter-arithmetic bookkeeping: Tendsto.congr' direction, div_mul_cancel₀
  application shape, self_mem_nhdsWithin name, omega on a cast goal).  The
  ALGEBRA it states is the sympy-verified content of PD01 Part A and PD02's
  lane (both committed, PASS).  Committed marked IN-FLIGHT per the corpus's
  C5 pattern; NOT a certificate until it compiles.

  The lanes are deepseek_push/PD01_polarization_count.py (17/17 PASS) and
  PD02_polarization_count.py (the dimension invariance).  This file certifies
  the exact algebra those lanes rest on -- nothing regime-dependent, nothing
  numerical.  Physical readings are the Python lanes'; Lean certifies
  mathematics.  All difference quotients are stated over the PUNCTURED
  neighbourhood `𝓝[≠] 0` -- the honest home of a slope.

  Certified here:
    quot_gen (T1)      : the master difference-quotient lemma.  For ANY curve
      a(Y) with a -> 1 and (a Y - 1)/Y -> c at Y = 0, ((a Y)^n - 1)/Y -> n*c.
      (Induction on n; elementary algebra plus Filter.Tendsto arithmetic.)
    slope_family (T2)  : the corpus's family mu_n(Y) = 1 - (1+Y)^(-n) has
      deep-MOND slope exactly n: mu_n(Y)/Y -> n at Y = 0, mu_n 0 = 0.
      (T1 with a = 1+Y, c = 1, divided by (1+Y)^n -> 1.)
    or_slope (T3)      : COMPLETION INDEPENDENCE.  For ANY engagement p with
      p 0 = 0 and p(Y)/Y -> 1, the OR response 1-(1-p Y)^n has deep-MOND
      slope exactly n.  The slope is the channel count for EVERY completion
      of the per-channel engagement -- deriving the count does not wait on
      deriving the shape.
    mond_matching (T4) : the deep-MOND matching: r^2 * (n g^2 / s) = GM gives
      g^2 = (s/n) * (GM/r^2) -- the a0-line's coefficient is s/n, so
      kappa = a0/s = 1/n.
    kappa_half (T5)    : the landing: mode count two gives exactly 1/2.

  The compounding law 1 - mu_n = (1 - mu_1)^n and the geometric channel count
  (two static Poisson sectors) stay with the Python lanes.
-/

import Mathlib

open Filter

/-- **T1** -- if `a Y -> 1` and `(a Y - 1)/Y -> c` at the origin (punctured),
then `((a Y)^n - 1)/Y -> n * c` (punctured). -/
theorem quot_gen {a : ℝ → ℝ} {c : ℝ}
    (ha : Tendsto a (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds 1))
    (hd : Tendsto (fun Y : ℝ => (a Y - 1) / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds c)) (n : ℕ) :
    Tendsto (fun Y : ℝ => ((a Y) ^ n - 1) / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds ((n : ℝ) * c)) := by
  induction n with
  | zero =>
      simp only [pow_zero, sub_self, zero_div]
      exact tendsto_const_nhds
  | succ m ih =>
      have hfe : (fun Y : ℝ => ((a Y) ^ (m + 1) - 1) / Y)
          = (fun Y : ℝ => (a Y) * (((a Y) ^ m - 1) / Y) + ((a Y) - 1) / Y) := by
        funext Y
        by_cases hY : Y = 0
        · subst hY
          norm_num [div_zero]
        · rw [div_eq_iff hY]
          have hda : ((a Y) * (((a Y) ^ m - 1) / Y)) * Y
              = (a Y) * ((a Y) ^ m - 1) := by
              rw [mul_assoc, div_mul_cancel₀ hY]
          have hdb : (((a Y) - 1) / Y) * Y = (a Y) - 1 := div_mul_cancel₀ hY _
          simp only [mul_add, hda, hdb]
          ring
      have h1 : Tendsto (fun Y : ℝ => (a Y) * (((a Y) ^ m - 1) / Y))
          (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds ((1 : ℝ) * ((m : ℝ) * c))) :=
        Tendsto.mul ha ih
      have hsum := h1.add hd
      have hlim : ((1 : ℝ) * ((m : ℝ) * c) + c) = ((m + 1 : ℕ) : ℝ) * c := by
        push_cast
        ring
      rw [hlim] at hsum
      rw [hfe]
      exact hsum

/-- The corpus's family, as a function (Lean's junk conventions included:
`muFam n 0 = 0`). -/
noncomputable def muFam (n : ℕ) (Y : ℝ) : ℝ := 1 - (1 + Y)^(-((n : ℤ)))

@[simp] theorem muFam_eq (n : ℕ) (Y : ℝ) :
    muFam n Y = 1 - (1 + Y)^(-((n : ℤ))) := rfl

/-- **T2** -- the family's deep-MOND slope is exactly its mode count `n`. -/
theorem slope_family (n : ℕ) :
    Tendsto (fun Y : ℝ => muFam n Y / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds (n : ℝ)) := by
  have hnum : Tendsto (fun Y : ℝ => ((1 + Y) ^ n - 1) / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds (n : ℝ)) := by
    have h := quot_gen (a := fun Y : ℝ => 1 + Y)
      (ha := by
        have hc : Continuous (fun Y : ℝ => 1 + Y) := by continuity
        exact tendsto_nhdsWithin_of_tendsto_nhds (hc.tendsto 0))
      (hd := by
        have hev : (fun Y : ℝ => ((1 + Y) - 1) / Y) =ᶠ[nhdsWithin (0 : ℝ) ({0}ᶜ)]
            (fun _ : ℝ => 1) := by
          filter_upwards [(Filter.self_mem_nhdsWithin : ({0}ᶜ : Set ℝ)
            ∈ nhdsWithin (0 : ℝ) ({0}ᶜ))] with Y hY
          field_simp
        exact hev.symm.tendsto tendsto_const_nhds) n
    simpa using h
  have hden : Tendsto (fun Y : ℝ => (1 + Y) ^ (n : ℕ))
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds 1) := by
    have hc : Continuous (fun Y : ℝ => (1 + Y) ^ (n : ℕ)) := by continuity
    exact tendsto_nhdsWithin_of_tendsto_nhds (hc.tendsto 0)
  have hdiv := hnum.div hden (by norm_num)
  have hres2 : Tendsto (fun Y : ℝ => muFam n Y / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds ((n : ℝ) / 1)) := by
    refine hdiv.congr' ?_
    filter_upwards [(Filter.self_mem_nhdsWithin : ({0}ᶜ : Set ℝ)
      ∈ nhdsWithin (0 : ℝ) ({0}ᶜ))] with Y hY
    have h1p : (1 : ℝ) + Y ≠ 0 := by omega
    have hz : (1 + Y)^(-((n : ℤ))) = ((1 + Y) ^ (n : ℕ))⁻¹ := by
      rw [zpow_neg, zpow_natCast]
    field_simp [muFam, hz, h1p, pow_ne_zero n h1p]
    ring
  simpa using hres2

/-- **T3** -- COMPLETION INDEPENDENCE: for any engagement `p` with `p 0 = 0`
and `p Y / Y -> 1` (punctured), the OR response `1 - (1 - p Y)^n` has
deep-MOND slope exactly `n`, for every completion of the per-channel
engagement. -/
theorem or_slope {p : ℝ → ℝ} (hp0 : p 0 = 0)
    (hp : Tendsto (fun Y : ℝ => p Y / Y) (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds 1))
    (n : ℕ) :
    Tendsto (fun Y : ℝ => (1 - (1 - p Y) ^ n) / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds (n : ℝ)) := by
  have hp0' : Tendsto (fun Y : ℝ => p Y) (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds 0) := by
    have h1 : Tendsto (fun Y : ℝ => Y * (p Y / Y))
        (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds ((0 : ℝ) * 1)) := tendsto_id.mul hp
    have hfe : (fun Y : ℝ => Y * (p Y / Y)) = (fun Y : ℝ => p Y) := by
      funext Y
      by_cases hY : Y = 0
      · simp [hY, hp0]
      · field_simp
    rw [hfe] at h1
    simpa using h1
  have ha : Tendsto (fun Y : ℝ => 1 - p Y) (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds 1) := by
    have h1 : Tendsto (fun Y : ℝ => p Y) (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds 0) := hp0'
    have h2 : Tendsto (fun _ : ℝ => 1) (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds 1) :=
      tendsto_const_nhds
    have := h1.sub h2
    have hfe : (fun Y : ℝ => 1 - p Y) = (fun Y : ℝ => -(p Y - 1)) := by
      funext Y; ring
    rw [hfe]
    exact this.neg
  have hd : Tendsto (fun Y : ℝ => ((1 - p Y) - 1) / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds (-1 : ℝ)) := by
    have hfe : (fun Y : ℝ => ((1 - p Y) - 1) / Y) = (fun Y : ℝ => -(p Y / Y)) := by
      funext Y
      by_cases hY : Y = 0
      · simp [hY, hp0, div_zero]
      · field_simp; ring
    rw [hfe]
    exact hp.neg
  have hq : Tendsto (fun Y : ℝ => ((1 - p Y) ^ n - 1) / Y)
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds ((n : ℝ) * (-1 : ℝ))) := quot_gen ha hd n
  have hneg : Tendsto (fun Y : ℝ => -(((1 - p Y) ^ n - 1) / Y))
      (nhdsWithin (0 : ℝ) ({0}ᶜ)) (nhds (-((n : ℝ) * (-1 : ℝ)))) := hq.neg
  have hfe : (fun Y : ℝ => (1 - (1 - p Y) ^ n) / Y)
      = (fun Y : ℝ => -(((1 - p Y) ^ n - 1) / Y)) := by
    funext Y; ring
  rw [hfe] at hneg
  simpa using hneg

/-- **T4** -- the deep-MOND matching: a response of slope `n` (mu ~ n g/s)
sourced by a point mass gives `g^2 = (s/n) * gN` with `gN = GM/r^2` -- the
a0-line's coefficient is `s/n`, so kappa = a0/s = 1/n. -/
theorem mond_matching {n s g2 gN GM r : ℝ} (hn : (n : ℝ) ≠ 0) (hs : s ≠ 0)
    (hr : r ≠ 0) (h : r ^ 2 * ((n : ℝ) * g2 / s) = GM) (hGN : gN = GM / r ^ 2) :
    g2 = (s / (n : ℝ)) * gN := by
  subst hGN
  field_simp at h ⊢
  linarith

/-- **T5** -- the landing: mode count two gives exactly one half. -/
theorem kappa_half {s a0 : ℝ} (hs : s ≠ 0) (h : a0 = s / 2) :
    a0 / s = 1 / 2 := by
  subst h
  field_simp
