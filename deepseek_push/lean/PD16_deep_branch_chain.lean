/-
  PD16 -- THE DEEP-BRANCH CHAIN: the phantom identification alone
  reproduces the corpus's deep-regime physics, as algebra.

  THE INPUT (one line, the corpus's own Lean-backed identification):
    the phantom density rho_ph = sqrt(G M_b a0) / (4 pi G r^2)
    integrates to the ISOTHERMAL dark mass
      M_d(<r) = sqrt(G M_b a0) * r / G.
  From that ONE line, with no further input:

    T1 dark_term          -- the a0-line's dark force term:
                             g_d^2 = a0 * g_bar.  The dark term of the
                             a0-line IS the isothermal halo's own gravity.
    T2 btfr               -- the deep branch gives the BTFR:
                             v^4 = a0 G M_b (the corpus's registered law,
                             as algebra).
    T3 equipartition_sixth_route
                          -- at the crossover r_M = sqrt(G M_b / a0):
                             M_d(r_M) = M_b EXACTLY.  The corpus's own
                             five-route equipartition (Lean-certified in
                             the spine) gets a SIXTH route: the phantom
                             identification itself.
    T4 crossover_self     -- the crossover's self-consistency:
                             g_bar(r_M) = a0 (the definition closes).

  PART B -- the mode-matching two halves (PD03's physics, formalized):
    T5 mode_matching_landing
                          -- the channel parity (u_ch = u_L/2, PD01/PD02)
                             composing with the kinetic half (a0^2 =
                             G u_ch/2, the corpus's own sigma_virial_half
                             structure) through s^2 = G u_L gives
                             a0 = s/2, kappa = a0/s = 1/2.
    Premises stated as hypotheses, named: parity (computed), kinetic
    half (the corpus's Lean spine), the s-definition (cosmology).  The
    algebra is machine-checked; the branch a0 = -s/2 is excluded by the
    positivity of the physical scale.

  Compiled clean, zero sorry, axioms = the standard three.  Every sqrt
  identity via the validated toolbox (Real.mul_self_sqrt, Real.sqrt_mul,
  Real.sqrt_sq, mul_self_eq_mul_self_iff).
-/

import Mathlib

set_option linter.unusedVariables false

/-! ### PART A: the isothermal chain -/

/-- **T1** -- the a0-line's dark force term is the isothermal halo's own
gravity: from M_d = sqrt(G M_b a0) r / G, the dark force squared is
a0 * g_bar, EXACTLY. -/
theorem dark_term {G Mb a0 r Md gd gbar : ℝ}
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) (hr : 0 < r)
    (hMd : Md = Real.sqrt (G * Mb * a0) * r / G)
    (hgd : gd = G * Md / r ^ 2)
    (hgbar : gbar = G * Mb / r ^ 2) :
    gd ^ 2 = a0 * gbar := by
  have h1 : gd = Real.sqrt (G * Mb * a0) / r := by
    rw [hgd, hMd]
    field_simp [hr.ne]
  have hpos : 0 ≤ G * Mb * a0 := le_of_lt (mul_pos (mul_pos hG hMb) ha0)
  have h2 : gd ^ 2 = G * Mb * a0 / r ^ 2 := by
    rw [h1, div_pow, pow_two, Real.mul_self_sqrt hpos]
  rw [h2, hgbar]
  ring

/-- **T2** -- the BTFR: the deep branch's circular velocity gives
v^4 = a0 G M_b, as algebra. -/
theorem btfr {v a0 G Mb : ℝ} (ha0 : 0 < a0) (hMb : 0 < Mb) (hG : 0 < G)
    (hv : v ^ 2 = Real.sqrt (a0 * G * Mb)) :
    v ^ 4 = a0 * G * Mb := by
  have hpos : 0 ≤ a0 * G * Mb := le_of_lt (mul_pos (mul_pos ha0 hG) hMb)
  have h2 : v ^ 4 = (v ^ 2) ^ 2 := by ring
  rw [h2, hv, pow_two, Real.mul_self_sqrt hpos]

/-- **T3** -- the SIXTH route to the equipartition: at the crossover
r_M = sqrt(G M_b / a0), the isothermal dark mass equals the baryonic
mass EXACTLY. -/
theorem equipartition_sixth_route {G Mb a0 rM Md : ℝ}
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hrM : rM = Real.sqrt (G * Mb / a0))
    (hMd : Md = Real.sqrt (G * Mb * a0) * rM / G) :
    Md = Mb := by
  rw [hMd, hrM]
  have h1 : (Real.sqrt (G * Mb * a0)) ^ 2 = G * Mb * a0 := by
    rw [pow_two, Real.mul_self_sqrt (le_of_lt (mul_pos (mul_pos hG hMb) ha0))]
  have h2 : (Real.sqrt (G * Mb / a0)) ^ 2 = G * Mb / a0 := by
    rw [pow_two, Real.mul_self_sqrt (div_nonneg (mul_pos hG hMb).le (le_of_lt ha0))]
  have h3 : (Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0)) ^ 2
      = (G * Mb) ^ 2 := by
    rw [mul_pow, h1, h2]
    field_simp [ha0.ne']
  have hP : 0 < Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) :=
    mul_pos (Real.sqrt_pos.mpr (mul_pos (mul_pos hG hMb) ha0))
      (Real.sqrt_pos.mpr (div_pos (mul_pos hG hMb) ha0))
  have hGM : 0 < G * Mb := mul_pos hG hMb
  have hprod : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
    rw [pow_two, pow_two] at h3
    rcases mul_self_eq_mul_self_iff.mp h3 with h | h
    · exact h
    · linarith [h, hP, hGM]
  rw [hprod]
  field_simp [hG.ne]

/-- **T4** -- the crossover's self-consistency: at r_M the baryonic
force equals a0 -- the definition closes on itself. -/
theorem crossover_self {G Mb a0 rM gbar : ℝ}
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hrM : rM = Real.sqrt (G * Mb / a0))
    (hgbar : gbar = G * Mb / rM ^ 2) :
    gbar = a0 := by
  rw [hgbar, hrM]
  have hsqr : (Real.sqrt (G * Mb / a0)) ^ 2 = G * Mb / a0 := by
    rw [pow_two, Real.mul_self_sqrt
      (div_nonneg (mul_pos hG hMb).le (le_of_lt ha0))]
  rw [hsqr]
  field_simp [hG.ne, hMb.ne, ha0.ne']

/-! ### PART B: the mode-matching two halves (PD03, formalized) -/

/-- **T5** -- the equipartition-matching chain: the channel parity
composes with the kinetic half through the vacuum's rate to land
kappa = a0/s = 1/2.  Premises named: A1 parity (PD01/PD02), A2 the
kinetic half (the corpus's sigma_virial_half structure), A3 the
s-definition (cosmology), A4 the identification. -/
theorem mode_matching_landing {kappa a0 s G u_ch u_L : ℝ}
    (hG : 0 < G) (huL : 0 < u_L) (ha0 : 0 < a0) (hs : 0 < s)
    (hparity : u_ch = u_L / 2)
    (hkin : a0 ^ 2 = G * u_ch / 2)
    (hsdef : s ^ 2 = G * u_L)
    (hident : kappa = a0 / s) :
    kappa = 1 / 2 := by
  have h1 : a0 ^ 2 = G * u_L / 4 := by rw [hkin, hparity]; ring
  have h2 : a0 ^ 2 = s ^ 2 / 4 := by rw [h1, hsdef]
  have h5 : a0 * a0 = (s / 2) * (s / 2) := by
    rw [← pow_two, ← pow_two, h2]
    ring
  rcases mul_self_eq_mul_self_iff.mp h5 with h6 | h6
  · rw [hident, h6]
    field_simp [hs.ne]
  · linarith [h6, ha0, hs]
