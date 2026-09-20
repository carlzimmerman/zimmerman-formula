import Mathlib
/-!
L291 -- the algebraic core of the carrier on FRW (real_research/clock_2026/L291_frw_ymod_carrier.py).
The cosmological state of the Y-modulated carrier (L290): G1 = -3 Om_m a^-3 (16 pi G rho = 2 Cc^2 p1,
Cc = 1), G2 = -(A-1)/2 3 Om_m a^-3 with A = 1e10, so c_s^2 = p1/(p1 + 2 Cc^2 g2) = 1/A = 1e-10 for
EVERY epoch (the Y-switch is linearly off at the homogeneous background: dY = 0, L290 V3 -- the sound
speed of the cosmic-mean carrier is a fixed ratio of the dust energy, not a new function of time).
Certified here: (1) the stress identity: rho = -2 Cc^2 G1 with G1 = -3 Om_m a^-3 gives the positive
dust density 6 Om_m a^-3, and the shift-symmetric charge a^3 P_X chi' = const is the a-independence
of the ratio g2/p1 = (A-1)/2 (both scale as a^-3: the dust stays dust); (2) the harmonic inversion:
c_s^2 = p1/(p1 + 2 g2) = 1/A iff g2 = (A-1) p1 / 2 -- the fixed ratio that makes the CLASS face run
a single cs2 = 1e-10 at every epoch (L292); (3) A = 1e10: the carrier's cosmological sound speed.
-/
namespace L291

/-- the stress identity: G1 = -p1 gives rho = +2 Cc^2 p1; with p1 = 3 Om_m a^-3 and Cc = 1:
    16 pi G-normalized rho = 6 Om_m a^-3 (the positive dust) -/
theorem dust_stress (Om a : ℝ) (ha : a ≠ 0) : -2 * (1 : ℝ) ^ 2 * (-3 * Om / a ^ 3) = 6 * Om / a ^ 3 := by
  field_simp [ha]
  ring

/-- the shift-symmetric charge: for G1 = -3 Om_m/a^3 the ratio g2/p1 is a-INDEPENDENT
    (both scale as a^-3): g2/p1 = (A-1)/2 at every epoch -/
theorem ratio_a_independent (A Om a : ℝ) (hp : (3 : ℝ) * Om / a ^ 3 ≠ 0) :
    (-(A - 1) * 3 * Om / a ^ 3 / 2) / (3 * Om / a ^ 3) = -(A - 1) / 2 := by
  have hO : Om ≠ 0 := by
    intro hz; apply hp; rw [hz]; simp
  have ha : a ≠ 0 := by
    intro hz; apply hp; rw [hz]; simp
  have h1 : Om * a * Om⁻¹ * a⁻¹ = 1 := by
    field_simp [hO, ha]
  field_simp [hO, ha, h1]

/-- the harmonic inversion: c_s^2 = p1/(p1 + 2 g2) = 1/A iff the stiffness ratio is g2 = (A-1) p1 / 2 -/
theorem inertia_inversion (A g2 p1 : ℝ) (hp : p1 ≠ 0) (hden : p1 + 2 * g2 ≠ 0) (hA0 : A ≠ 0) :
    p1 / (p1 + 2 * g2) = 1 / A ↔ g2 = (A - 1) * p1 / 2 := by
  constructor
  · intro h
    have hm' : p1 = (p1 + 2 * g2) / A := by
      calc
        p1 = (p1 / (p1 + 2 * g2)) * (p1 + 2 * g2) := by field_simp [hden]
        _ = (1 / A) * (p1 + 2 * g2) := by rw [h]
        _ = (p1 + 2 * g2) / A := by field_simp [hA0]
    have hm2 : p1 * A = p1 + 2 * g2 := by
      calc
        p1 * A = (p1 + 2 * g2) / A * A := by rw [← hm']
        _ = p1 + 2 * g2 := by field_simp [hA0]
    nlinarith [hm2]
  · intro hg
    rw [hg]
    field_simp [hp, hden, hA0]
    ring

/-- A = 1e10: the carrier's cosmological sound speed is 1e-10 (c^2 units) -/
example : (1 : ℝ) / 10 ^ 10 = 1e-10 := by norm_num

end L291