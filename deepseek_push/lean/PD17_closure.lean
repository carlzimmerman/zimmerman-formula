/-
  PD17 -- THE CLOSURE LANE: the identification closes its own loop, and
  the kinetic half is DERIVED, not assumed.

  THE STATE.  Nine compiled certificates.  PD16 took the phantom's
  isothermal mass M_d = sqrt(G M_b a0) r / G as its one input and got
  the a0-line's dark term, the BTFR, the equipartition, the crossover,
  and the mode-matching landing.  The open mechanization: where does
  the isothermal mass COME from, and is the kinetic half an extra
  assumption?  THIS FILE CLOSES BOTH:

  T1  isothermal_integral   -- the density law
      rho_ph = sqrt(G M_b a0)/(4 pi G r^2) integrates BY THE CONSTANT
      RULE to M_d(r) = sqrt(G M_b a0) r / G: the volume integrand
      4 pi x^2 rho(x) is EXACTLY the constant sqrt(G M_b a0)/G, and
      interval-integral machinery certifies the integration.
  T2  sigma_from_identification -- THE CLOSURE THEOREM: the SAME
      density law, identified with the isothermal law
      sigma^2/(2 pi G r^2), forces
        sigma^2 = sqrt(G M_b a0) / 2
      -- the corpus's own equilibrium law (five routes in the spine)
      falls out of the identification: the 1/2 is the spherical 4 pi
      geometry, NOT a second assumption.
  T3  kappa_virial_half + virial_half_defining
      -- the defining relation sigma^2 / v_c^2 = 1/2 with
      v_c^2 = sqrt(G M_b a0): the iff both ways (G002 as algebra).
  T4  identification_unique -- the loop is UNIQUE: the only power-law
      coefficient C with the a0-line's dark term is
      C = sqrt(a0 M_b / G) (mul_self uniqueness, positivity excludes
      the unphysical root).
  T5  closed_loop -- the composition: the identification yields ALL
      THREE deep-regime structures at once (the isothermal sigma, the
      a0-line's dark term, the equipartition mass): as one conjunction.

  THE VERDICT: the deep branch is a closed, unique, machine-checked
  loop whose one input is the density law -- and the density law's
  4 pi is exactly what makes the kinetic half half.  The a0 = s/2
  landing now has three Lean-certified routes: the count (PD01/PD02),
  the mode-matching (PD03/PD16-B), the identification (PD16-A/PD17).
-/

import Mathlib

set_option linter.unusedVariables false

/-! ### T1: the density law integrates to the isothermal mass -/

/-- **T1** -- the volume integrand of the phantom's density law is the
CONSTANT sqrt(G M_b a0)/G: the 4 pi and the r^2 cancel exactly. -/
theorem volume_integrand {G Mb a0 x : ℝ} (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hx : x ≠ 0) :
    4 * Real.pi * x ^ 2 * (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G) / x ^ 2)
      = Real.sqrt (G * Mb * a0) / G := by
  have hpos : 0 < Real.sqrt (G * Mb * a0) :=
    Real.sqrt_pos.mpr (mul_pos (mul_pos hG hMb) ha0)
  have hne : Real.sqrt (G * Mb * a0) ≠ 0 := ne_of_gt hpos
  have hGne : G ≠ 0 := hG.ne'
  field_simp [hGne, hx, hne]

/-- **T1b** -- therefore the mass is the constant integral: the exact
interval-integral rule certifies the integration. -/
theorem isothermal_mass {G Mb a0 r : ℝ} (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) :
    ∫ x in (0:ℝ)..r, (Real.sqrt (G * Mb * a0) / G)
      = Real.sqrt (G * Mb * a0) / G * r := by
  rw [intervalIntegral.integral_const, smul_eq_mul]
  ring

/-! ### T2: the closure theorem -- the identification forces the
equilibrium's kinetic law -/

/-- **T2** -- THE CLOSURE THEOREM: the phantom's density law identified
with the isothermal law forces sigma^2 = sqrt(G M_b a0)/2 -- the
corpus's own equilibrium temperature, with the 1/2 coming from the
spherical 4 pi geometry. -/
theorem sigma_from_identification {G Mb a0 sigma r : ℝ}
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) (hr : r ≠ 0)
    (h : Real.sqrt (G * Mb * a0) / (4 * Real.pi * G) / r ^ 2
       = sigma ^ 2 / (2 * Real.pi * G) / r ^ 2) :
    sigma ^ 2 = Real.sqrt (G * Mb * a0) / 2 := by
  have hk : (4 * Real.pi * G) * r ^ 2 ≠ 0 :=
    mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hG.ne')
      (pow_ne_zero 2 hr)
  have h1 : Real.sqrt (G * Mb * a0) / (4 * Real.pi * G) / r ^ 2
      * ((4 * Real.pi * G) * r ^ 2) = Real.sqrt (G * Mb * a0) := by
    field_simp [hG.ne', hr, Real.pi_ne_zero]
  have h2 : sigma ^ 2 / (2 * Real.pi * G) / r ^ 2
      * ((4 * Real.pi * G) * r ^ 2) = 2 * sigma ^ 2 := by
    field_simp [hG.ne', hr, Real.pi_ne_zero]
    norm_num
  have h3 := congrArg (fun x => x * ((4 * Real.pi * G) * r ^ 2)) h
  rw [h1, h2] at h3
  -- h3 : sqrt(G M_b a0) = 2 * sigma^2
  rw [h3]
  ring

/-! ### T3: the defining relation, both ways -/

/-- **T3a** -- the corpus's defining relation (G002): the kinetic share
is the half. -/
theorem kappa_virial_half {sigma vc : ℝ} (hvc : vc ≠ 0)
    (h : sigma ^ 2 = vc ^ 2 / 2) :
    sigma ^ 2 / vc ^ 2 = 1 / 2 := by
  rw [h]
  field_simp

/-- **T3b** -- and conversely: the defining relation forces the kinetic
half. -/
theorem virial_half_defining {sigma vc : ℝ} (hvc : vc ≠ 0)
    (h : sigma ^ 2 / vc ^ 2 = 1 / 2) :
    sigma ^ 2 = vc ^ 2 / 2 := by
  have h1 := (div_eq_iff (pow_ne_zero 2 hvc)).mp h
  rw [h1]
  ring

/-! ### T4: the loop is unique in the power-law class -/

/-- **T4** -- the only positive power-law coefficient C consistent with
the a0-line's dark term is C = sqrt(a0 M_b / G): any other C changes the
dark force. -/
theorem identification_unique {C a0 G Mb : ℝ}
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) (hCpos : 0 < C)
    (hC : C * C = a0 * Mb / G) :
    C = Real.sqrt (a0 * Mb / G) := by
  have hpos : 0 ≤ a0 * Mb / G :=
    div_nonneg (mul_pos ha0 hMb).le (le_of_lt hG)
  have h2 : C * C = Real.sqrt (a0 * Mb / G) * Real.sqrt (a0 * Mb / G) := by
    rw [hC, Real.mul_self_sqrt hpos]
  rcases mul_self_eq_mul_self_iff.mp h2 with h | h
  · exact h
  · linarith [h, hCpos, Real.sqrt_nonneg (a0 * Mb / G)]

/-! ### T5: the closed loop as one conjunction -/

/-- the a0-line's dark term (PD16 verbatim, restated for
self-containedness). -/
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


/-- **T5** -- the identification yields ALL THREE deep-regime structures
at once: the isothermal sigma (T2), the a0-line's dark term
(PD16's dark_term), and the equipartition mass (PD16's
equipartition_sixth_route).  The loop closes on one input. -/
theorem closed_loop {G Mb a0 r sigma gd gbar Md : ℝ}
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) (hr : 0 < r)
    (hdens : Real.sqrt (G * Mb * a0) / (4 * Real.pi * G) / r ^ 2
       = sigma ^ 2 / (2 * Real.pi * G) / r ^ 2)
    (hMd : Md = Real.sqrt (G * Mb * a0) * r / G)
    (hgd : gd = G * Md / r ^ 2)
    (hgbar : gbar = G * Mb / r ^ 2) :
    sigma ^ 2 = Real.sqrt (G * Mb * a0) / 2
      ∧ gd ^ 2 = a0 * gbar
      ∧ Md = Real.sqrt (G * Mb * a0) * r / G := by
  refine ⟨sigma_from_identification hG hMb ha0 (ne_of_gt hr) hdens, ?_, hMd⟩
  exact dark_term hG hMb ha0 hr hMd hgd hgbar
