namespace RouteECriticalCondensation
def sigma_coll_12 : Rat := 684 / 100
def sigma_coll_13 : Rat := 1195 / 100
def sigma_a0_can  : Rat := 10685 / 100
def sigma_a0_alt  : Rat := 12913 / 100
def eta_cf4       : Rat := 1082 / 100
def eta_stip      : Rat := 1430 / 100
theorem cert1_condensation_threshold_bracketed :
    (eta_cf4 * sigma_coll_12 < sigma_a0_can) ∧
    (sigma_a0_can < eta_cf4 * sigma_coll_13) ∧
    (eta_stip * sigma_coll_12 < sigma_a0_can) ∧
    (sigma_a0_can < eta_stip * sigma_coll_13) ∧
    (eta_stip * sigma_coll_12 < sigma_a0_alt) ∧
    (sigma_a0_alt < eta_stip * sigma_coll_13) := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel⟩
def A_raw     : Rat := 24 / 100
def sig_raw   : Rat := 19 / 100
def v_scale   : Rat := 264 / 194
def A_ctrl    : Rat := 58 / 100
theorem cert2_gh9_ksz_upper_bounds :
    (A_raw + (196 / 100) * sig_raw = 6124 / 10000) ∧
    (A_raw + (196 / 100) * sig_raw < 1) ∧
    (v_scale * (A_raw + (196 / 100) * sig_raw) < 84 / 100) ∧
    (v_scale * (A_raw + (196 / 100) * sig_raw) < 1) ∧
    (A_raw / A_ctrl = 12 / 29) := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel⟩
def dV_cf4  : Rat := -347 / 10
def dV_e21  : Rat := -186 / 10
def dV_law  : Rat := -125 / 10
theorem cert3_ls1_velocity_decomposition :
    (dV_cf4 - dV_law = -222 / 10) ∧
    (dV_e21 - dV_law = -61 / 10) ∧
    ((-dV_law) / (-dV_cf4) < 37 / 100) := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩
def eta_CE1_13 : Rat := 1767 / 100
def eta_CE1_14 : Rat := 1691 / 100
def eta_pass   : Rat := 1430 / 100
def R_CL5_min  : Rat := 91 / 100
theorem cert4_cluster_reduction_bounds :
    (80 / 100 < eta_pass / eta_CE1_13) ∧
    (eta_pass / eta_CE1_13 < 85 / 100) ∧
    (80 / 100 < eta_pass / eta_CE1_14) ∧
    (eta_pass / eta_CE1_14 < 85 / 100) ∧
    (eta_pass / eta_CE1_14 < R_CL5_min) := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel⟩
end RouteECriticalCondensation
