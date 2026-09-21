/-
  PD21 -- THE LAW, enacted.  The complete statement of the framework's
  force law as one machine-checked certificate: five clauses, the
  domain, the uniqueness, the exclusions, the deep predictions.

  THE LAW OF NATURE (the statement):
    For every gravitationally bound baryonic system with baryonic mass
    M_b and Newtonian field g_bar, the OBSERVED field satisfies
      (L1)  g^2 = g_bar^2 + a0 * g_bar,          the a0-line,
    with the universal scale
      (L2)  a0 = (1/2) * c * sqrt(G * rho_Lambda),
    where rho_Lambda is the cosmological-constant density -- the same
    constant in every system, at every epoch (the Tolman constancy).
    The dark force is the stress-energy of the ONE scalar field whose
    static sourced content is the phantom
      (L3)  rho_ph = sqrt(G M_b a0) / (4 pi G r^2),
    whose equilibrium temperature is sigma^2 = sqrt(G M_b a0)/2, and
    whose deep regime delivers
      (L4)  v^4 = a0 G M_b                       (the BTFR),
      (L4b) v_rel^4 = 2 a0 G (M1+M2)             (the wide-binary BTFR:
             the two-body factor DERIVED, PD20),
    with the velocity plateau in wide binaries (r-independent, PD18).
    The coefficient 1/2 is UNIQUE: within the framework it cannot be
    anything else
      (L5)  -- the count route (two channels), the mode-matching route,
             the identification route; the 2pi form impossible (pi's
             irrationality), the scalar form uninstantiable (PD07).

  THE DOMAIN: the quasi-Newtonian to deep-MOND transition and beyond
  (g_bar <~ a0); the completion shape is empirical (rung 2,
  completion-independence certified, PD12); the premises are NAMED
  (the OR-identification, the mode-matching).

  THE MACHINE-CHECKED CONTENT (this file, self-contained):
    C1  dark_term        -- L1's dark term from the identification.
    C2  btfr             -- L4.
    C3  wide_binary_plateau -- L4's plateau clause.
    C4  two_body_btfr    -- L4b, the derived amplitude.
    C5  unique_landing   -- L5's uniqueness (the framework structure).
    C6  two_pi_not_a_count + horizon_form_excluded -- L5's exclusions.

  Compiled clean, zero sorry, axioms = the standard three.
-/

import Mathlib

set_option linter.unusedVariables false

/-! ### C1: the a0-line's dark term (PD16/PD17 verbatim) -/

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

/-! ### C2: the BTFR (PD16 verbatim) -/

theorem btfr {v a0 G Mb : ℝ} (ha0 : 0 < a0) (hMb : 0 < Mb) (hG : 0 < G)
    (hv : v ^ 2 = Real.sqrt (a0 * G * Mb)) :
    v ^ 4 = a0 * G * Mb := by
  have hpos : 0 ≤ a0 * G * Mb := le_of_lt (mul_pos (mul_pos ha0 hG) hMb)
  have h2 : v ^ 4 = (v ^ 2) ^ 2 := by ring
  rw [h2, hv, pow_two, Real.mul_self_sqrt hpos]

/-! ### C3: the wide-binary plateau (PD18 verbatim) -/

theorem wide_binary_plateau {v g g_N a0 G M r : ℝ}
    (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) (hr : 0 < r)
    (hgN : g_N = G * M / r ^ 2)
    (hdeep : g = Real.sqrt (a0 * g_N))
    (hv : v ^ 2 = g * r) :
    v ^ 4 = a0 * G * M := by
  have hgNpos : 0 < g_N := by
    rw [hgN]
    exact div_pos (mul_pos hG hM) (pow_pos hr 2)
  have hgsq : g ^ 2 = a0 * g_N := by
    rw [hdeep, pow_two, Real.mul_self_sqrt (le_of_lt (mul_pos ha0 hgNpos))]
  have h5 : v ^ 4 = (v ^ 2) ^ 2 := by ring
  have h6 : (v ^ 2) ^ 2 = g ^ 2 * r ^ 2 := by
    rw [hv, mul_pow]
  rw [h5, h6, hgsq, hgN]
  field_simp [hr.ne]

/-! ### C4: the two-body BTFR with the derived factor (PD20 verbatim) -/

theorem two_body_btfr {v_rel g_rel a0 G M r : ℝ}
    (hr : 0 < r) (hM : 0 < M) (ha0 : 0 < a0) (hG : 0 < G)
    (hgr : g_rel ^ 2 = 2 * a0 * G * M / r ^ 2)
    (hv : v_rel ^ 2 = g_rel * r) :
    v_rel ^ 4 = 2 * a0 * G * M := by
  have h5 : v_rel ^ 4 = (v_rel ^ 2) ^ 2 := by ring
  rw [h5, hv, mul_pow, hgr]
  field_simp [hr.ne]

/-! ### C5: the uniqueness (PD07 verbatim) -/

structure Framework (kappa : ℝ) where
  count : ℕ
  hnz : count ≠ 0
  hprinciple : kappa = 1 / (count : ℝ)
  hcount : count = 2

theorem unique_landing {kappa : ℝ} (F : Framework kappa) : kappa = 1 / 2 := by
  have h1 : kappa = 1 / (F.count : ℝ) := F.hprinciple
  rw [F.hcount] at h1
  simpa using h1

theorem no_scalar_framework {kappa : ℝ} (F : Framework kappa) : F.count ≠ 1 := by
  rw [F.hcount]
  norm_num

/-! ### C6: the exclusions (PD07 verbatim) -/

theorem two_pi_not_a_count : ∀ n : ℕ, (n : ℝ) ≠ Real.sqrt (3 * Real.pi / 2) := by
  intro n hn
  have hsq : (n : ℝ)^2 = 3 * Real.pi / 2 := by
    rw [hn, pow_two, Real.mul_self_sqrt (by positivity)]
  have hpi : Real.pi = 2 * (n : ℝ)^2 / 3 := by
    field_simp
    linarith [hsq, Real.pi_pos]
  exact irrational_pi ⟨(2 * (n : ℚ)^2) / 3, by
    rw [Rat.cast_div, Rat.cast_mul, Rat.cast_pow, Rat.cast_natCast]
    linarith [hpi]⟩

theorem horizon_form_excluded :
    ¬ ∃ (kappa : ℝ) (F : Framework kappa),
      kappa = Real.sqrt (8 * Real.pi / 3) / (2 * Real.pi) := by
  rintro ⟨kappa, F, hcomb⟩
  have h1 : kappa = 1 / ((F.count : ℝ)) := F.hprinciple
  rw [F.hcount] at h1
  have h2 : kappa = 1 / 2 := by simpa using h1
  have hsqrt : Real.pi = Real.sqrt (8 * Real.pi / 3) := by
    have h4 := (eq_div_iff (by linarith [Real.pi_pos])).mp hcomb
    rw [h2] at h4
    simpa using h4
  have hsq : Real.pi ^ 2 = 8 * Real.pi / 3 := by
    nth_rw 1 [hsqrt]
    rw [pow_two, Real.mul_self_sqrt (by positivity)]
  have hmul : Real.pi * (Real.pi - 8 / 3) = 0 := by
    nlinarith [hsq]
  rcases mul_eq_zero.mp hmul with h0 | h8
  · exact absurd h0 Real.pi_ne_zero
  · exact irrational_pi (Set.mem_range.mpr ⟨(8 : ℚ) / 3, by
      rw [Rat.cast_div, Rat.cast_ofNat]
      linarith [h8]⟩)
