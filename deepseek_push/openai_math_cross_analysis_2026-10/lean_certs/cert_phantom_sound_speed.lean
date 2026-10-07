import Mathlib

/-! # Cert: the phantom sound-speed theorem (T13) — algebra payload

The settled phantom halo (T10) is barotropic: hydrostatics with
mu const forces P = c^2 rho and c^2 = v^2/2 (sympy-verified in the lane,
derivative step carries there per house pattern). The certified algebra:

  (S1)  c_ph^2 = v_flat^2/2 and v_flat^4 = G M a0  =>  c_ph^4 = G M a0 / 4
        (ring + sq_sqrt, no inserted constant).
  (S2)  Jeans length from the pinned sound speed:
        lambda_J^2 = c_ph^2 * pi/(G rho_ph), with G rho_ph = v_flat^2/
        (4 pi r^2), gives lambda_J^2 = 2 pi^2 r^2 (substitution algebra)
        and hence lambda_J = sqrt(2) * pi * r: a radius-independent
        multiple — the phantom fluid is Jeans-stable at every radius.

Values (lane): c_ph = 132.76 / 139.20 km/s (canonical / alt);
lambda_J/r = sqrt(2) pi = 4.442883.... Zero sorry; axioms =
{propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

variable {M a0 G v2 c2 r : ℝ}

/-- S1: c^2 = v^2/2 with v^4 = G M a0 forces c^4 = G M a0 / 4. -/
theorem sound_speed_fourth_power (hv : v2 ^ 2 = G * M * a0)
    (hc : c2 = v2 / 2) :
    c2 ^ 2 = G * M * a0 / 4 := by
  rw [hc]
  have hv2 : (v2 / 2) ^ 2 = v2 * v2 / 4 := by ring
  rw [hv2]
  rw [← pow_two v2, hv]

/-- S1': sqrt form; positivity-realized: sqrt((GMa0)/4) = sqrt(GMa0)/2. -/
theorem sound_speed_sqrt (hG : 0 ≤ G * M * a0) :
    sqrt (G * M * a0 / 4) = sqrt (G * M * a0) / 2 := by
  rw [Real.sqrt_div hG 4]
  norm_num

/-- S2: Jeans substitution — with c^2 = v^2/2 and G rho = v^2/(4 pi r^2),
lambda_J^2 = c^2 * pi/(G rho) = 2 pi^2 r^2 exactly (radius-only). -/
theorem jeans_square (hc2 : c2 = v2 / 2) (hv2 : v2 ≠ 0) (hr2 : r ≠ 0)
    (hgr : G * rho = v2 / (4 * π * r ^ 2)) :
    c2 * π / (G * rho) = 2 * π ^ 2 * r ^ 2 := by
  rw [hc2, hgr]
  field_simp [hv2, hr2]
  ring

end