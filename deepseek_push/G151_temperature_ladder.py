"""
G151 -- THE TEMPERATURE LADDER
===============================
The framework's three temperatures, stated, on the committed record:
  (a) equilibrium phase:      T = m sigma^2/k_B            -> 9.17 K at 5 keV (G116/G084)
  (b) free dust kinetic:      T = m v_th^2/k_B             -> 2.04e-5 K at z=3, falls as (1+z)^2 (G116/G093)
  (c) baryonic gas:           T = mu m_p sigma^2/k_B       -> cluster 3.6-4.1 keV-class (G008/G075/G109)

Every number reproduced here from its registered lane; nothing new is claimed.
"""
import json

# ---- constants (CODATA-ish, repo-registered footings) ----
kB      = 1.380649e-23          # J/K
eV      = 1.602176634e-19       # J
K_per_eV = eV / kB              # 11604.5 K per eV
mp_c2_eV = 938.27208816e6       # proton rest energy, eV
mu      = 0.6                   # G075/G109 registered mean molecular weight
c_kms   = 299792.458            # km/s

sigma_gal_kms = 119.20924633196348   # G116/G091: (1/2) sqrt(G M_b a0), M_b = 6.5e10 Msun, a0 = 9.3623e-11
sigma_gal_reg = 119.2                # registered 119.2 km/s (G084)
m_sec_eV = 5000.0                    # reference mass 5 keV (G116's T_phase anchor)

def T_from_v2(mass_eV, v_kms):
    """T = m v^2 / k_B  (per-particle kinetic/thermal temperature)"""
    return mass_eV * (v_kms / c_kms)**2 * K_per_eV

def T_gas(v_kms):
    """T = mu m_p v^2 / k_B  (baryonic gas at velocity dispersion v, 1D)"""
    return mu * mp_c2_eV * (v_kms / c_kms)**2 * K_per_eV

def T_gas_eV(v_kms):
    """gas temperature in eV: mu m_p v^2 (per-particle energy)"""
    return mu * mp_c2_eV * (v_kms / c_kms)**2

# ---- (a) equilibrium phase ----
T_a = T_from_v2(m_sec_eV, sigma_gal_kms)          # K at m = 5 keV
T_per_eV_mK = (sigma_gal_kms / c_kms)**2 * K_per_eV * 1e3   # T/m registered linear law, mK/eV

# ---- (b) free dust kinetic ----
v_th_z3_3p3keV = 0.219        # km/s, G093 A1 (3.3 keV)
v_th_z3_5keV   = v_th_z3_3p3keV * (3.3 / 5.0)**0.5    # 0.178 km/s
T_b_z3 = T_from_v2(m_sec_eV, v_th_z3_5keV)            # K at z = 3
T_b_z0 = T_b_z3 / 16.0                                # v ~ (1+z) -> T ~ (1+z)^2
T_b_z3_reg = 2.043562265291894e-05                    # G116 registered
T_b_z0_reg = 1.2795603146644502e-06                   # G116 registered

# ---- (c) baryonic gas ----
c_same_sigma_K     = T_gas(sigma_gal_kms)             # at the SAME sigma as (a)
c_same_sigma_eV    = T_gas_eV(sigma_gal_kms)
ratio_c_over_a     = (mu * mp_c2_eV) / m_sec_eV       # = mu m_p / m, exact at equal sigma

# cluster rungs: triad sigma_pred at cluster M_b
G      = 6.67430e-11
a0     = 9.3619e-11            # canonical footing (G075)
Msun   = 1.98892e30
Mb_A85 = 1.1088914500216186e14 # M_b(R500) of A85, Msun (G095 committed row)
sig_pred_A85 = (G * Mb_A85 * Msun * a0)**0.25 / 2.0**0.5 / 1000.0    # km/s
T_c_A85_keV   = T_gas_eV(sig_pred_A85) / 1000.0
sig_809       = 809.0          # G008/STATE.md registered "T = 809 km/s from zero parameters"
T_c_809_keV   = T_gas_eV(sig_809) / 1000.0
T_obs_med_keV = 6.17           # X-COP kTvir median, 12 clusters (G075/G109)
sig_obs_1d    = c_kms * (T_obs_med_keV * 1000.0 / (mu * mp_c2_eV))**0.5   # km/s
sig_3p6keV    = c_kms * (3600.0 / (mu * mp_c2_eV))**0.5                   # sigma at 3.6 keV

# ---- the ratios ----
r_a_b = T_a / T_b_z3
r_c_a = c_same_sigma_K / T_a
r_c_b = c_same_sigma_K / T_b_z3
r_cA85_a = (T_c_A85_keV * 1000.0 * K_per_eV) / T_a
r_cA85_b = (T_c_A85_keV * 1000.0 * K_per_eV) / T_b_z3

out = {
 "rung_a_phase": {
   "formula": "T = m sigma^2/k_B",
   "m_keV": 5.0, "sigma_kms": sigma_gal_kms,
   "T_K": T_a,
   "T_per_eV_mK": T_per_eV_mK,
   "registered": "9.17 K at 5 keV; band 9.17-10.07 K (G084 thermo block); T/m mass-free = 1.83-2.01 mK/eV (G116 A2)"
 },
 "rung_b_dust_kinetic": {
   "formula": "T = m v_th^2/k_B",
   "v_th_z3_5keV_kms": v_th_z3_5keV,
   "T_z3_K": T_b_z3, "T_z3_registered_K": T_b_z3_reg,
   "T_z0_K": T_b_z0,  "T_z0_registered_K": T_b_z0_reg,
   "scaling": "T ~ (1+z)^2 (v_th ~ a^-1); T(z=3)/T(z=0) = 16"
 },
 "rung_c_baryonic_gas": {
   "formula": "T = mu m_p sigma^2/k_B, mu = 0.6",
   "same_sigma_as_a_K": c_same_sigma_K,
   "same_sigma_as_a_eV": c_same_sigma_eV,
   "cluster_triad_A85_keV": T_c_A85_keV, "sigma_A85_kms": sig_pred_A85,
   "registered_809kms_keV": T_c_809_keV,
   "sigma_at_3p6keV_kms": sig_3p6keV,
   "observed_median_kTvir_keV": T_obs_med_keV, "sigma_obs_1d_kms": sig_obs_1d,
   "G075_note": "median T_pred/T_obs = 0.28 (1D /2-convention floor, 3.6x hotter); G109 equipartition sigma_gal/sigma_gas = 0.998 (rms 0.062 dex); G095 closed form 2 f (r_M/r): median 3.51 vs 3.57 (1.8%), hse scatter 0.053 dex"
 },
 "ratios": {
   "a_over_b_z3": r_a_b,            # registered decoupling ratio 4.5e5
   "c_over_a_equal_sigma": r_c_a,   # = mu m_p / m exactly
   "c_over_b_z3_equal_sigma": r_c_b,
   "c_A85_over_a": r_cA85_a,
   "c_A85_over_b_z3": r_cA85_b,
   "parent_gloss_check": "committed numbers: a/b = 4.49e5 (not 1e4); c/a = 1.13e5 at equal sigma (matches ~1e5); c/b = 5.1e10 equal-sigma / 2.1e12 cluster-rung (not 1e9)"
 },
 "constants": {
   "mu": mu, "mp_c2_MeV": mp_c2_eV/1e6, "K_per_eV": K_per_eV,
   "a0_canonical": a0, "G": G
 }
}

print("=== G151 THE TEMPERATURE LADDER ===")
print(f"(a) T_phase = m sigma^2/k_B @ 5 keV, sigma = {sigma_gal_kms:.2f} km/s: {T_a:.4f} K   [T/m = {T_per_eV_mK:.4f} mK/eV]")
print(f"(b) T_kin,dust(z=3) = m v_th^2/k_B, v_th = {v_th_z3_5keV:.4f} km/s: {T_b_z3:.4e} K   [z=0: {T_b_z0:.4e} K; (1+z)^2]")
print(f"(c) T_gas = mu m_p sigma^2/k_B:")
print(f"    same sigma ({sigma_gal_kms:.1f} km/s): {c_same_sigma_eV:.2f} eV = {c_same_sigma_K:.4e} K")
print(f"    cluster triad sigma (A85 M_b(R500) = {Mb_A85:.3e} Msun): sigma_pred = {sig_pred_A85:.1f} km/s -> {T_c_A85_keV:.2f} keV")
print(f"    G008/STATE.md registered 809 km/s -> {T_c_809_keV:.2f} keV  (3.6 keV <-> sigma = {sig_3p6keV:.0f} km/s)")
print(f"    observed X-COP median kTvir = {T_obs_med_keV} keV <-> sigma_1d = {sig_obs_1d:.0f} km/s")
print(f"RATIOS: a/b(z=3) = {r_a_b:.3e}  |  c/a (equal sigma) = {r_c_a:.3e} = mu m_p/m = {mu*mp_c2_eV/m_sec_eV:.3e}  |  c/b(z=3, equal sigma) = {r_c_b:.3e}")
print(f"        c(A85)/a = {r_cA85_a:.3e}  |  c(A85)/b(z=3) = {r_cA85_b:.3e}")
print(f"VERIFY: T(z=3)/T(z=0) = {T_b_z3/T_b_z0:.0f} (expect 16); T_a reproduces 9.1729 K: {T_a:.4f}")

with open("G151_ladder_numbers.json", "w") as f:
    json.dump(out, f, indent=1)
print("[written] G151_ladder_numbers.json")
