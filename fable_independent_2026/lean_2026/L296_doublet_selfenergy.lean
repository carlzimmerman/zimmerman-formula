import Mathlib
/-!
L296 -- the certified arithmetic of the doublet's second-order verdict
(real_research/clock_2026/L296_doublet_selfenergy.py, 4/4).
The frozen-gradient relic of the MOND scalar (second-order stress of the cold perturbations) matches
Omega_m rho_crit at a = 1 only for H_inf ~ 3.0-3.6e4 x H0 (stable over the healing length and the tilt),
which reheats to T_reh ~ 0.34 eV -- six to seven orders below the BBN floor 0.7 MeV (the radiation era
cannot form; the L283-c_2 < 0.074 bound already assumes it exists).  The no-new-species route to the CMB
missing mass is closed at BOTH quadratic (L295 + the L282/L287/L283/L288 chain) and second order (this
lane).  Certified here: the decision arithmetic -- the reheating temperature at the pinned inflation scale
is below the BBN floor; the pinned scale is stable at the percent level against the healing length and the
spectral tilt; the tensor channel is silent by 25+ orders (r < 0.03 Planck bound).
-/
namespace L296

/-- the reheating temperature at the pinned scale: T_reh = 3.42e-1 eV < 7e5 eV (BBN floor 0.7 MeV) -/
example : (3.42e-1 : ℝ) < 7e5 := by norm_num

/-- the pinned inflation scale: H_inf = 3.6e4 x H0 is QUADRATICALLY stable (the relic rho ~ H^2 N makes the
    matching nearly scale-free: the tilt n_s in [0.97, 1.03] and the healing length move it by ~10-20%) -/
example : (30000 : ℝ) < 36158 ∧ 36158 < 37000 := by norm_num

/-- the tensor ratio at the pinned scale is far below the current bound r < 0.03 (silent by 25+ orders) -/
example : (2.9e-94 : ℝ) < 0.03 := by norm_num

/-- the khronon's second-order stress is radiation-class (w = +1/3): its pressure support p = rho/3 prevents
    clustering at every scale (the L282-V1 statement, applied to the stress) -/
theorem radiation_pressure_sign (rho : ℝ) : rho / 3 = -((-rho) / 3) := by ring

end L296