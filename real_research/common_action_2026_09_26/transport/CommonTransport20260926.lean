import Mathlib

/-! Exact algebra for a stated classical Cartesian field potential and transport
balance. No PDE, field-to-particle, global-clock, halo-clearing or full gravity
claim is encoded in these certificates. g denotes g² in the report. -/
namespace CommonTransport20260926

theorem quartic_square_completion (R s lR lS g : ℝ) (hlS : lS ≠ 0) :
    lR * R ^ 4 / 4 + lS * s ^ 4 / 4 - g * R ^ 2 * s ^ 2 / 2 =
    lS * (s ^ 2 - g * R ^ 2 / lS) ^ 2 / 4 +
      (lR - g ^ 2 / lS) * R ^ 4 / 4 := by
  field_simp
  ring

theorem quartic_margin (lR lS g : ℝ) (hlS : 0 < lS)
    (h : g ^ 2 < lR * lS) : 0 < lR - g ^ 2 / lS := by
  have hd : g ^ 2 / lS < lR := (div_lt_iff₀ hlS).2 h
  linarith

theorem completed_potential_nonnegative (R s m2 mu2 lS margin g : ℝ)
    (hm : 0 ≤ m2) (hu : 0 ≤ mu2) (hl : 0 ≤ lS) (hd : 0 ≤ margin) :
    0 ≤ m2 * R ^ 2 / 2 + mu2 * s ^ 2 / 2 +
      lS * (s ^ 2 - g * R ^ 2 / lS) ^ 2 / 4 + margin * R ^ 4 / 4 := by
  positivity

theorem cartesian_current_conservation (x y vx vy F : ℝ) :
    vx * vy + x * (-F * y) - vy * vx - y * (-F * x) = 0 := by ring

theorem sector_exchange_cancels (g R2 s radialFlux sdot : ℝ) :
    g * s ^ 2 * radialFlux + g * R2 * s * sdot +
      (-g * s ^ 2 * radialFlux - g * R2 * s * sdot) = 0 := by ring

theorem above_threshold_negative_mass (k2 mu2 g R2 : ℝ)
    (h : k2 + mu2 < g * R2) : k2 + mu2 - g * R2 < 0 := by linarith

theorem zero_seed_force (mu2 lS g R2 : ℝ) :
    (0 : ℝ) * (mu2 + lS * 0 ^ 2 - g * R2) = 0 := by ring

theorem release_square (lS d : ℝ) (hlS : lS ≠ 0) :
    -( -d * (d / lS) / 2 + lS * (d / lS) ^ 2 / 4) = d ^ 2 / (4 * lS) := by
  field_simp
  ring

theorem broken_mass_determinant (R s lR lS g : ℝ) :
    (2 * lR * R ^ 2) * (2 * lS * s ^ 2) - (-2 * g * R * s) ^ 2 =
      4 * R ^ 2 * s ^ 2 * (lR * lS - g ^ 2) := by ring

theorem broken_mass_determinant_positive (R s margin : ℝ)
    (hR : R ≠ 0) (hs : s ≠ 0) (hm : 0 < margin) :
    0 < 4 * R ^ 2 * s ^ 2 * margin := by positivity

theorem generic_energy_exchange (A B Ad Bd v W Wq : ℝ) (hA : A ≠ 0) :
    Ad * v ^ 2 / 2 + A * v * ((-Ad * v - B * Wq) / A) + Bd * W + B * Wq * v =
      -Ad * v ^ 2 / 2 + Bd * W := by
  field_simp
  ring

theorem exponential_gate_positive (Z : ℝ) :
    0 < Real.exp Z ∧ 0 < Real.exp (-Z) := by
  exact ⟨Real.exp_pos Z, Real.exp_pos (-Z)⟩

theorem kick_energy_cost (v n kick : ℝ) :
    ((v + kick * n) ^ 2 - v ^ 2) / 2 = kick * v * n + kick ^ 2 * n ^ 2 / 2 := by ring

end CommonTransport20260926

#print axioms CommonTransport20260926.quartic_square_completion
#print axioms CommonTransport20260926.quartic_margin
#print axioms CommonTransport20260926.completed_potential_nonnegative
#print axioms CommonTransport20260926.cartesian_current_conservation
#print axioms CommonTransport20260926.sector_exchange_cancels
#print axioms CommonTransport20260926.above_threshold_negative_mass
#print axioms CommonTransport20260926.zero_seed_force
#print axioms CommonTransport20260926.release_square
#print axioms CommonTransport20260926.broken_mass_determinant
#print axioms CommonTransport20260926.broken_mass_determinant_positive
#print axioms CommonTransport20260926.generic_energy_exchange
#print axioms CommonTransport20260926.exponential_gate_positive
#print axioms CommonTransport20260926.kick_energy_cost
