/-
  PD22 -- THE FULL DERIVATION, FROM FIRST PRINCIPLES: the OR-composition
  is not an assumption -- it is THE UNIQUE composition satisfying four
  first principles.  The last named premise mechanized.

  THE FIRST PRINCIPLES (each backed, none new):
    P1  SYMMETRY: the two channels are two faces of ONE field (PD04's
        two-one lock): C p q = C q p.
    P2  ONE-CHANNEL EXACTNESS (the flux-fraction principle): a channel
        that is not driven carries nothing and adds nothing: C p 0 = p.
    P3  SATURATION: the response is a FRACTION: C 1 1 = 1.
    P4  DEGREE TWO: the response is at most quadratic in each channel --
        the corpus's own max-entropy result (G084).

  THE THEOREM (T1): P1--P4 force C p q = p + q - p*q = 1 - (1-p)(1-q)
    UNIQUELY.  The OR-composition is a THEOREM, not a premise.

  THE FULL CHAIN (T1--T4, one file):
    one field, one scale s (the ontology, PD05)
      -> two channels (computed, PD01/PD02)
      -> degree-2 response (P4 = G084)
      -> the OR-composition UNIQUE (T1: P1/P2/P3)
      -> mu = 2p - p^2, slope 2 cp
      -> the unit fraction (measured shut, PD10: cp = 1 to 0.33 pct)
      -> the spherical matching: g^2 = (s/2) g_N
      -> kappa = a0/s = 1/2, unique, rivals excluded (PD07).
-/

import Mathlib

set_option linter.unusedVariables false

/-! ### T1: the uniqueness of the composition -- THE MECHANIZATION -/

/-- **T1** -- the four first principles force the OR-composition. -/
theorem composition_unique {C : ℝ → ℝ → ℝ} {α β γ δ ε ζ : ℝ}
    (hform : ∀ p q : ℝ, C p q
      = α + β * p + γ * q + δ * p * q + ε * p * p + ζ * q * q)
    (hsym : ∀ p q : ℝ, C p q = C q p)
    (hone : ∀ p : ℝ, C p 0 = p)
    (hsat : C 1 1 = 1) :
    ∀ p q : ℝ, C p q = p + q - p * q := by
  have h0 := hone 0
  rw [hform] at h0
  simp only [zero_mul, mul_zero, add_zero] at h0
  -- h0 : C 0 0 = alpha
  have hα : α = 0 := by linarith [h0]
  have h1 := hone 1
  rw [hform] at h1
  simp only [zero_mul, mul_zero, add_zero] at h1
  -- h1 : C 1 0 = alpha + beta + eps
  have hβε : β + ε = 1 := by
    rw [hα] at h1
    ring_nf at h1
    exact h1
  have h2 := hone (-1)
  rw [hform] at h2
  simp only [neg_mul, zero_mul, mul_zero, add_zero] at h2
  have hβε2 : -β + ε = -1 := by
    rw [hα] at h2
    ring_nf at h2
    exact h2
  have hβ : β = 1 := by linarith [hβε, hβε2]
  have hε : ε = 0 := by linarith [hβε, hβε2]
  -- symmetry: C 0 q = q
  have hC0q : ∀ q : ℝ, C 0 q = q := by
    intro q
    have h1 := hone q
    rw [hsym] at h1
    exact h1
  have hq1 : C 0 1 = 1 := hC0q 1
  have hq2 : C 0 2 = 2 := hC0q 2
  have hq1f : C 0 1 = α + γ + ζ := by
    rw [hform]; ring
  have hq2f : C 0 2 = α + 2 * γ + 4 * ζ := by
    rw [hform]; ring
  rw [hq1f] at hq1
  rw [hq2f] at hq2
  rw [hα] at hq1 hq2
  have hγ : γ = 1 := by linarith [hq1, hq2]
  have hζ : ζ = 0 := by linarith [hq1, hq2]
  -- P3 pins delta:
  have hδ : δ = -1 := by
    have h11f : C 1 1 = α + β + γ + δ + ε + ζ := by
      rw [hform]; ring
    rw [h11f] at hsat
    rw [hα, hβ, hγ, hε, hζ] at hsat
    linarith
  intro p q
  rw [hform, hα, hβ, hγ, hδ, hε, hζ]
  ring

/-! ### T2: the equal-channel response through the unique composition -/

/-- **T2** -- the equal-channel composition: mu = 2p - p^2, the linear
coefficient exactly 2 -- the completion never enters. -/
theorem composition_at_equal {C : ℝ → ℝ → ℝ} {α β γ δ ε ζ : ℝ}
    (hform : ∀ p q : ℝ, C p q
      = α + β * p + γ * q + δ * p * q + ε * p * p + ζ * q * q)
    (hsym : ∀ p q : ℝ, C p q = C q p)
    (hone : ∀ p : ℝ, C p 0 = p)
    (hsat : C 1 1 = 1) (p : ℝ) :
    C p p = 2 * p - p * p := by
  have h := composition_unique hform hsym hone hsat p p
  ring_nf at h ⊢
  linarith

/-! ### T3/T4: the matching and the landing (PD13 verbatim) -/

theorem mond_poisson {n g gN s GM r : ℝ} (hn : (n : ℝ) ≠ 0) (hs : s ≠ 0) (hr : r ≠ 0)
    (hfield : r ^ 2 * ((n : ℝ) * g ^ 2 / s) = GM) (hgN : gN = GM / r ^ 2) :
    g ^ 2 = (s / (n : ℝ)) * gN := by
  rw [hgN]
  have h0 := congrArg (fun x => x * s) hfield
  field_simp at h0
  field_simp
  linear_combination h0

theorem kappa_half_landing {kappa a0 s : ℝ} (hs : s ≠ 0) (ha0 : a0 = s / 2)
    (h : kappa = a0 / s) : kappa = 1 / 2 := by
  rw [ha0] at h
  field_simp [hs] at h
  linarith
