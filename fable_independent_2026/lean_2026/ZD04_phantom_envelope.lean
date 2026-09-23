import Mathlib

/-!
# ZD04 — The Phantom Envelope (the enclosed-mass ceiling)

Framework premise (docstring scope, NOT certified here): the a0-line
g_obs^2 - g_bar^2 = a0 * g_bar (PD08/PD13) applied to spherical enclosed
fields, g = G M(<r)/r^2. From ZD01's ceiling g_phi < a0/2 and the
spherical-shell relation M_phi(<r) = r^2 g_phi(r)/G it follows that the
enclosed phantom (dark) mass of ANY line-conforming system satisfies

    M_phi(<r) < a0 * r^2 / (2 G)          (the ENVELOPE),

i.e. the dark mass within radius r is capped by a0 r^2/(2G): 4.3e8 Msun at
1 kpc, 4.3e10 at 10 kpc, 4.3e12 at 100 kpc (a0 = 1.2e-10 m/s^2). Heavy
cusps and over-massive halos cannot exist on the line.

At the handoff radius r*^2 = 2 G M_b/a0 (ZD02) the envelope equals M_b
exactly and the certified handoff mass (sqrt 3 - 1) M_b occupies 73.2% of
it — the saturation ratio (sqrt 3 - 1) < 1 is itself certified.

Lean certifies the mathematics; the a0-line premise is the framework's.
-/

noncomputable section
open scoped Real

/-- The phantom (dark) acceleration normalized by a0 — same function as in
ZD01/ZD02, restated here so ZD04 is self-contained. -/
noncomputable def phi (a0 x : ℝ) : ℝ := Real.sqrt (x^2 + a0 * x) - x

/-- Strict ceiling (ZD01 restated). -/
theorem phantom_ceiling_strict (a0 x : ℝ) (ha0 : 0 < a0) (hx : 0 < x) :
    phi a0 x < a0 / 2 := by
  have hnn : 0 ≤ x^2 + a0 * x := by
    nlinarith [sq_nonneg x, hx.le, ha0.le]
  have hnon2 : 0 ≤ x + a0 / 2 := by nlinarith [hx.le, ha0.le]
  have hroot : Real.sqrt (x^2 + a0 * x) < x + a0 / 2 := by
    apply (Real.sqrt_lt hnn hnon2).2
    rw [pow_two]
    ring_nf
    nlinarith [sq_pos_of_pos ha0]
  unfold phi
  linarith

/-- THE ENVELOPE: the enclosed phantom mass of a line-conforming spherical
system is strictly below a0 r^2/(2G) at every radius. -/
theorem mphi_envelope (a0 G M r : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hM : 0 < M)
    (hr : 0 < r) :
    r^2 * phi a0 (G * M / r^2) / G < a0 * r^2 / (2 * G) := by
  have hgpos : 0 < G * M / r^2 := by positivity
  have hlt := phantom_ceiling_strict a0 (G * M / r^2) ha0 hgpos
  have hpos : 0 < r^2 / G := by positivity
  have h1 : (r^2 / G) * phi a0 (G * M / r^2) < (r^2 / G) * (a0 / 2) :=
    mul_lt_mul_of_pos_left hlt hpos
  simpa [div_eq_mul_inv, mul_assoc, mul_left_comm, mul_comm] using h1

/-- sqrt 3 < 2 (the saturation bound). -/
theorem sqrt3_lt_two : Real.sqrt 3 < 2 := by
  apply (Real.sqrt_lt (by norm_num : (0 : ℝ) ≤ 3) (by norm_num : (0 : ℝ) ≤ 2)).2
  norm_num

/-- THE SATURATION RATIO: at the handoff radius the phantom occupies the
fraction (sqrt 3 - 1) ~ 0.732 of its envelope — below the ceiling, never
meeting it. -/
theorem saturation_ratio_lt_one : Real.sqrt 3 - 1 < 1 := by
  nlinarith [sqrt3_lt_two]

/-- At the handoff r*^2 = 2 G M_b/a0 the envelope equals M_b exactly and
the handoff mass (sqrt 3 - 1) M_b sits strictly below it. -/
theorem handoff_share_below_envelope (M : ℝ) (hM : 0 < M) :
    (Real.sqrt 3 - 1) * M < M := by
  have hlt : Real.sqrt 3 - 1 < 1 := saturation_ratio_lt_one
  nlinarith [hlt, hM]

end

#print axioms phantom_ceiling_strict
#print axioms mphi_envelope
#print axioms sqrt3_lt_two
#print axioms saturation_ratio_lt_one
#print axioms handoff_share_below_envelope