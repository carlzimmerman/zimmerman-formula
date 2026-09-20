import Mathlib

/-!
# I09 — Wave R: the wind-kinematic radius identities

SCOPE (per lean-math-certification): Lean certifies the algebra of the two kinematic
routes (numbers Python-verified in `bhstar_r1_wind_kinematics.py`, 6/6):

  (1) THE LAUNCH-RADIUS IDENTITY: with the launch surface defined by
      r_launch = 2GM/v_inf^2 (the escape-speed inversion of the measured P-Cygni
      terminal velocity), the ratio to the transition radius is
      r*/r_launch = r* v_inf^2/(2GM) — pure algebra. At (M = 1e4, v_inf = 495 km/s):
      r_launch = 72 au vs r* = 100 au; with the CAK line-driven factor
      v_inf = (2.6-3) v_esc the band [72, 650] au brackets r*. The in-situ CAK
      factor is MEASURED: v_inf/v_esc(R_phot) = 495/137 = 3.6.

  (2) THE TIMING IDENTITY: the photospheric dynamical time R/v_esc(R) with
      v_esc^2 = 2GM/R gives (R/v_esc)^2 = R^3/(2GM) — the 30-yr lensed variability
      is the PHOTOSPHERE's time (32.5 yr at 941 au), NOT the Balmer layer's
      (t_dyn(r*) = 1.6 yr) — the honest re-frame after the first draft's failure.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **R (the launch-radius identity).** r*/r_launch = r* v_inf^2/(2GM) — the
coincidence test in its kinematic form. -/
theorem launch_ratio {G M v rstar rlaunch : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hv : 0 < v)
    (hrl : rlaunch = 2 * G * M / v ^ 2) :
    rstar / rlaunch = rstar * v ^ 2 / (2 * G * M) := by
  rw [hrl]
  field_simp

/-- **R (the timing identity).** (R/v_esc)^2 = R^3/(2GM) — the dynamical time in
its two equivalent forms. -/
theorem timescale_forms {G M R vesc tR : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hR : 0 < R) (hvesc : 0 < vesc) (htR : 0 < tR)
    (hvesc2 : vesc ^ 2 = 2 * G * M / R)
    (htRdef : tR = R / vesc) :
    tR ^ 2 = R ^ 3 / (2 * G * M) := by
  rw [htRdef, div_pow, hvesc2]
  field_simp

end

#print axioms launch_ratio
#print axioms timescale_forms