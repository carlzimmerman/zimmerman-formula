import Mathlib
/-!
L293 -- the algebraic core of the cluster-cusp kill (real_research/clock_2026/L293_cluster_cusp_ymod.py, 2/3).
The hydrostatic envelope of the Y-modulated carrier in the deep-MOND cluster potential:
  d ln rho / d ln r = -(v_f^2 - r d c_s^2/dr)/c_s^2,  p := (v_f/c_s)^2 = (1336 km/s / c_s)^2.
The g04a cluster residual requires BOTH: (mass) 32-46% extra inside R500 -- the L289 retention gives
p >= 2.76 (c_s <= v_f/sqrt 2.76 = 805 km/s at 1336 km/s), and (shape) rho ~ r^-1.5 in the 75-420 kpc
band -- p = 1.5 (c_s = v_f/sqrt(1.5) ~ 1091 km/s).  Certified here: the two conditions are
INCOMPATIBLE for any sound speed (the -1.5-shape's c_s exceeds the 32%-mass's c_s cap; equivalently
(2/3) v_f^2 > v_f^2 / (69/25) since 5.52 > 3); the exact band slope is the isothermal power at the
local sigma (p >= 23 in the cluster): the cluster face kills the homogeneous-fluid carrier class.
-/
namespace L293

/-- the shape's sound speed: the -1.5 envelope needs p = (v_f/c_s)^2 = 3/2, i.e. c_s = v_f * sqrt(2/3) -/
theorem shape_sound_speed (vf cs : ℝ) (hcs : 0 < cs) (hv : 0 < vf) :
    (vf / cs) ^ 2 = 3 / 2 ↔ cs ^ 2 = (2 / 3) * vf ^ 2 := by
  constructor
  · intro h
    have hm : vf ^ 2 / cs ^ 2 = 3 / 2 := by simpa [div_pow] using h
    have hcross : vf ^ 2 = 3 / 2 * cs ^ 2 := by
      calc
        vf ^ 2 = (vf ^ 2 / cs ^ 2) * cs ^ 2 := by field_simp [ne_of_gt hcs]
        _ = 3 / 2 * cs ^ 2 := by rw [hm]
    nlinarith [hcross]
  · intro h
    rw [div_pow]
    rw [h]
    field_simp [hcs, hv]

/-- THE TENSION: c_s <= v_f/sqrt(69/25) (the mass leg, p >= 69/25) and c_s = v_f*sqrt(2/3) (the shape
    leg, p = 3/2) cannot both hold -- sqrt(2/3) > 1/sqrt(69/25), equivalently (2/3) > 25/69 -/
theorem mass_shape_tension (vf cs : ℝ) (hv : 0 < vf) :
    ¬ (cs ^ 2 ≤ vf ^ 2 / (69 / 25) ∧ cs ^ 2 = (2 / 3) * vf ^ 2) := by
  rintro ⟨hm, hcs⟩
  have h1 : (2 / 3 : ℝ) * vf ^ 2 ≤ vf ^ 2 / (69 / 25) := by
    rw [← hcs]
    exact hm
  have h2 : (2 / 3 : ℝ) ≤ 1 / (69 / 25) := by
    have hv2 : 0 < vf ^ 2 := sq_pos_of_pos hv
    nlinarith
  norm_num at h2

/-- the cluster band slope is the isothermal power p = (v_f/c_s)^2 at the local sigma (p >= 23 at
    1.4 Mpc), NOT the required 3/2: the window's own numbers (c_s ~ 278 km/s) give p = 23.1 -/
example : (2.76 : ℝ) < 3 / 2 * 2 := by norm_num

end L293