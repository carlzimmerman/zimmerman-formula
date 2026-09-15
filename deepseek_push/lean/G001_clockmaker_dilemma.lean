/-
  G001 — the Clockmaker's Dilemma, certified in Lean 4 (mathlib).

  L236 proved (see Mondlean.`cuscuton_needs_a_potential`): a cuscuton clock's own field
  equation fixes V'(τ) = -3HU for a CONSTANT coefficient U, so a vanishing potential
  forces a vanishing expansion rate. L236's LIMITS section named one loophole: with
  U depending on τ there is an extra term, "and whether that term can substitute for
  the potential is NOT computed here -- it is the one loophole in the no-go."

  G001 (the Python lane) closes it with the closure family the construction itself
  requires (L200): U ∝ a^(-3(1+w)), d ∝ a^(-3(1-w)), q ∝ a^(-3w), μ = 2dq²/U constant,
  s₀ = 1 + w/m_rel. Substituting that family into the clock equation exactly as L200
  writes it, the potential-free part collapses identically to 3HUw/m_rel, i.e.

      V_τ = 3 H U (s₀ - 1).

  This file certifies the algebra of that reduction, its calibration against L236's
  constant-U result, and the two-horn dilemma it forces:

    horn (i)  V ≠ 0  — the potential exists; L226's zero-mode no-go bites; κ underivable;
    horn (ii) V = 0  — forces w = 0 hence s₀ = 1, a clock at exactly proper time,
                       excluded by criticality (needs w > 0) and by the solar system
                       (needs s₀ ≥ 1.5e7, L216).

  Scope, as Mondlean's header insists: Lean certifies the MATHEMATICS. The physical
  readings (which gate excludes which branch) are the Python lane's; the theorems here
  are the arithmetic those readings rest on.
-/
import Mathlib

/-! ## G001 — the reduction -/

/-- **G001 V2.** On the closure family (μ = 2dq²/U constant, the coefficient and charge
running as powers of the scale factor), the potential-free part of the clock equation
collapses identically to 3HUw/m_rel. Stated as algebra: given the running values
`Up = -3(1+w)HU` (the coefficient's τ-derivative), `qp = -3wHq` (the charge's), and the
closure identity `2dq² = μU`, the combination `-2Udqqp/((1-μ)U) - Up - 3HU` equals
`3HUw/(1-μ)`. -/
theorem clock_free_part_reduces (U d q qp Up H w mu : ℝ)
    (hU : U ≠ 0) (hmr : 1 - mu ≠ 0)
    (hmu : mu * U = 2 * d * q ^ 2)
    (hqp : qp = -3 * w * H * q) (hUp : Up = -3 * (1 + w) * H * U) :
    -2 * U * d * q * qp / ((1 - mu) * U) - Up - 3 * H * U = 3 * H * U * w / (1 - mu) := by
  subst hqp; subst hUp
  have key : (2 * d * q ^ 2) * w = mu * U * w := by rw [← hmu]
  have hf : -2 * U * d * q * (-3 * w * H * q) / ((1 - mu) * U) = 6 * w * H * d * q ^ 2 / (1 - mu) := by
    field_simp; ring
  have h6 : 6 * w * H * d * q ^ 2 / (1 - mu) = 3 * H * (mu * U * w) / (1 - mu) := by
    rw [← key]; field_simp; ring
  rw [hf, h6]
  field_simp
  ring

/-- **G001 V2 (rate form).** With the clock rate `s₀ = 1 + w/m_rel` (L200's identity,
the clock's excess rate over proper time), the required potential slope is exactly
`3HU(s₀ - 1)`: the running of U does not substitute for the potential, it multiplies
the constant-U slope by the clock's excess rate itself. -/
theorem required_slope_is_excess_rate (U H w mu s0 : ℝ)
    (hs : s0 = 1 + w / (1 - mu)) :
    3 * H * U * w / (1 - mu) = 3 * H * U * (s0 - 1) := by
  rw [hs]; ring

/-- **G001 V4 (calibration).** The pure-cuscuton limit — d-sector off (μ = 0, m_rel = 1),
constant U (w = -1, the vacuum) — sends the reduced slope to exactly `-3HU`, which is
L236's V' = -3HU. The two lanes are one algebra. -/
theorem pure_cuscuton_limit (U H : ℝ) :
    3 * H * U * (-1) / (1 - 0) = -3 * H * U := by
  norm_num

/-! ## G001 — the dilemma -/

/-- **G001 V5 (the loophole closed).** With V = 0 and U, H, m_rel all non-vanishing, the
clock equation `3HUw/m_rel = 0` forces `w = 0`: the no-potential branch is a single
point of the family. -/
theorem no_potential_forces_w_zero (U H w mu : ℝ)
    (hU : U ≠ 0) (hH : H ≠ 0) (hmr : 1 - mu ≠ 0)
    (hV : 3 * H * U * w / (1 - mu) = 0) : w = 0 := by
  have h0 : (3 : ℝ) * (H * U) * w = 0 := by
    rcases div_eq_zero_iff.mp hV with h | h
    · linear_combination h
    · exact absurd h hmr
  have hHU : H * U ≠ 0 := mul_ne_zero hH hU
  have h3 : (3 : ℝ) * (H * U) ≠ 0 := mul_ne_zero (by norm_num) hHU
  rcases mul_eq_zero.mp h0 with h1 | h1
  · exact absurd h1 h3
  · exact h1

/-- **G001 V5 (rate form).** On the no-potential branch the clock runs at exactly proper
time: `s₀ = 1`. -/
theorem no_potential_forces_proper_time (w mu s0 : ℝ)
    (_hmr : 1 - mu ≠ 0) (hs : s0 = 1 + w / (1 - mu)) (hw : w = 0) : s0 = 1 := by
  rw [hw, zero_div] at hs; linarith

/-- **G001 V6 (the solar floor).** A clock at proper time is seven orders below the
solar-system alignment requirement `s₀ ≥ 1.5 × 10⁷` (L216). -/
theorem proper_time_fails_solar_floor (s0 : ℝ) (h : s0 = 1) :
    s0 < 15000000 := by
  rw [h]; norm_num

/-- **G001 V7 (the amplification).** At the solar-system clock rate the required
potential slope exceeds the constant-U estimate `3HU` by more than a factor 10⁶: the
extra term from the running coefficient makes the potential MORE required, not less. -/
theorem amplification_at_solar_clock : (1000000 : ℝ) < 15000000 - 1 := by
  norm_num

/-- **G001 V8 (the capstone).** The dilemma is exhaustive and both horns fail the
construction's own gates: if V = 0 then the clock runs at proper time, which the
solar-system floor excludes by seven orders. (The other horn, V ≠ 0, is L226's zero
mode — Mondlean.`cuscuton_needs_a_potential` plus the L226 lane.) -/
theorem the_clockmaker_dilemma (U H w mu s0 : ℝ)
    (hU : U ≠ 0) (hH : H ≠ 0) (hmr : 1 - mu ≠ 0)
    (hs : s0 = 1 + w / (1 - mu))
    (hV : 3 * H * U * w / (1 - mu) = 0) :
    s0 = 1 ∧ s0 < 15000000 := by
  have hw := no_potential_forces_w_zero U H w mu hU hH hmr hV
  have h1 := no_potential_forces_proper_time w mu s0 hmr hs hw
  exact ⟨h1, proper_time_fails_solar_floor s0 h1⟩

#print axioms the_clockmaker_dilemma
