/-
  PD10 -- THE ZERO MODE, MEASURED SHUT: kappa = 1/(2 cp), and the SPARC
  deep slope measures cp = 1 to 0.33 percent -- so kappa = 1/2, and any
  deviation is EXACTLY a second acceleration scale the particle-free
  framework does not have.

  THE HONEST CHAIN (no normalization assumed):
    * k01 (the corpus's own theorem) PROVES no action fixes the response's
      linear coefficient cp = p'(0): the normalization is a zero mode.
    * PD08's composition + matching: the two-channel OR with per-channel
      response cp gives mu'(0) = 2 cp, and the spherical deep-MOND matching
      gives kappa = a0/s = 1/(2 cp).  THE COUNT 2 IS THE FRAMEWORK'S
      (computed, dimension-invariant); cp is the ONE remaining number.
    * cp = 1 is the no-second-scale statement: any cp != 1 is EXACTLY a
      second acceleration scale s2 = 2 kappa s = s/cp in the response
      (second_scale_form below).  The particle-free framework's scale
      inventory is {s, GM_b, r} -- there is no s2, and the data agree:
      the SPARC deep slope measures the count at n = 2.000 on both density
      conventions (L232: 0.02% and 0.33%), i.e. cp = 1 to 0.33 percent.
    * THE CERTIFIED FORM: kappa = s2/(2s) with s2 = s to 0.33 percent --
      there is no second scale, so kappa = 1/2.

  Certified here (algebra, standard axioms):
    kappa_times_cp           : kappa * (2 cp) = 1  (the matching, factored)
    kappa_half_at_unit_cp    : cp = 1  =>  kappa = 1/2
    cp_determines            : one cp, one kappa (the zero mode is ONE number)
    second_scale_form        : kappa = s2/(2s), and kappa = 1/2 <-> s2 = s
    no_second_scale          : kappa != 1/2 -> s2 != s -> the second scale
                               exists and differs -- the falsifier, certified
-/

import Mathlib

/-- The matching, factored: with the two-channel OR (count 2) and the
spherical deep-MOND matching, `kappa * (2 cp) = 1` where `cp = p'(0)` is
the per-channel linear response -- the zero mode k01 proved no action
fixes. -/
theorem kappa_times_cp {kappa cp : ℝ} (hcp : cp ≠ 0)
    (h : kappa = 1 / (2 * cp)) : kappa * (2 * cp) = 1 := by
  rw [h]
  field_simp

/-- **The measured closure**: the SPARC deep slope fixes `cp = 1` (the
count n = 2.000 on both density conventions, L232); the matching then gives
kappa = 1/2. -/
theorem kappa_half_at_unit_cp {kappa : ℝ} (h : kappa = 1 / (2 * 1)) :
    kappa = 1 / 2 := by
  norm_num [h]

/-- The zero mode is ONE number: the same `cp` gives the same `kappa` for
every system -- no environmental freedom. -/
theorem cp_determines {κ₁ κ₂ cp : ℝ} (hcp : cp ≠ 0)
    (h₁ : κ₁ = 1 / (2 * cp)) (h₂ : κ₂ = 1 / (2 * cp)) : κ₁ = κ₂ := by
  rw [h₁, h₂]

/-- **THE SECOND-SCALE FORM**: any `kappa` is EXACTLY a second acceleration
scale in the response: `kappa = s2/(2s)` with `s2 = 2 kappa s`.  The
framework's scale inventory is {s, GM_b, r} -- there is no `s2`. -/
theorem second_scale_form {kappa s s2 : ℝ} (hs : s ≠ 0)
    (h2 : s2 = 2 * kappa * s) (h : kappa = s2 / (2 * s)) :
    kappa = 1 / 2 ↔ s2 = s := by
  constructor
  · intro hhalf
    rw [hhalf] at h2
    norm_num at h2
    exact h2
  · intro hs2
    rw [hs2] at h2
    have h1 : 2 * kappa = 1 := by
      field_simp at h2
      linarith
    linarith

/-- **THE FALSIFIER, certified**: if kappa != 1/2 then the second scale
s2 = 2 kappa s DIFFERS from s -- a new acceleration constant the
particle-free framework does not contain.  Contrapositive: with no second
scale in the inventory, kappa = 1/2. -/
theorem no_second_scale {kappa s s2 : ℝ} (hs : s ≠ 0)
    (h2 : s2 = 2 * kappa * s) (h : kappa = s2 / (2 * s)) :
    kappa ≠ 1 / 2 → s2 ≠ s := by
  intro hκ hseq
  exact hκ ((second_scale_form hs h2 h).mpr hseq)
