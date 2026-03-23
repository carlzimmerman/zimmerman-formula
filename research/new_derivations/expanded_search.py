#!/usr/bin/env python3
"""
Expanded Search for Zimmerman Framework Derivations
Looking for NEW quantities not yet covered
"""

import numpy as np

# Master constants
Z = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888
alpha = 1 / (4 * Z**2 + 3)       # 1/137.04
sqrt_3pi_2 = np.sqrt(3 * np.pi / 2)  # 2.171
O_L = sqrt_3pi_2 / (1 + sqrt_3pi_2)  # 0.6846
O_m = 1 - O_L                         # 0.3154
alpha_s = O_L / Z                     # 0.1183

# Particle masses in MeV
m_e = 0.511
m_mu = 105.66
m_tau = 1776.86
m_p = 938.27
m_n = 939.57
m_pi = 139.57
m_K = 493.68
m_W = 80379  # MeV
m_Z = 91188  # MeV
m_H = 125250  # MeV
m_t = 172760  # MeV

print("=" * 70)
print("EXPANDED SEARCH FOR NEW ZIMMERMAN DERIVATIONS")
print("=" * 70)

# ============================================================
# SECTION 1: TOP QUARK PROPERTIES
# ============================================================
print("\n" + "=" * 70)
print("SECTION 1: TOP QUARK PROPERTIES")
print("=" * 70)

# Top width
Gamma_t = 1420  # MeV (measured ~1.42 GeV)
Gamma_t_ratio = Gamma_t / m_t  # ~0.00822

print(f"\nTop quark width ratio Gamma_t/m_t:")
print(f"  Observed: {Gamma_t_ratio:.5f}")
print(f"  Try alpha: {alpha:.5f} (error: {100*abs(alpha - Gamma_t_ratio)/Gamma_t_ratio:.1f}%)")
print(f"  Try alpha_s/14: {alpha_s/14:.5f} (error: {100*abs(alpha_s/14 - Gamma_t_ratio)/Gamma_t_ratio:.1f}%)")
print(f"  Try 1/Z^3: {1/Z**3:.5f} (error: {100*abs(1/Z**3 - Gamma_t_ratio)/Gamma_t_ratio:.2f}%)")

# Top BR to Wb ~ 0.99
BR_t_Wb = 0.99
print(f"\nTop BR(t->Wb) = 0.99:")
print(f"  Try 1 - alpha: {1 - alpha:.5f} (error: {100*abs(1-alpha - BR_t_Wb)/BR_t_Wb:.2f}%)")

# ============================================================
# SECTION 2: W BOSON BRANCHING RATIOS
# ============================================================
print("\n" + "=" * 70)
print("SECTION 2: W BOSON BRANCHING RATIOS")
print("=" * 70)

BR_W_lnu = 0.1086  # Each lepton flavor
BR_W_had = 0.6741  # Hadronic

print(f"\nW branching ratios:")
print(f"  BR(W->l nu) observed: {BR_W_lnu}")
print(f"  Try 1/9 = {1/9:.4f} (error: {100*abs(1/9 - BR_W_lnu)/BR_W_lnu:.2f}%)")
print(f"  Try alpha_s - 0.01 = {alpha_s - 0.01:.4f} (error: {100*abs(alpha_s - 0.01 - BR_W_lnu)/BR_W_lnu:.2f}%)")

print(f"\n  BR(W->had) observed: {BR_W_had}")
print(f"  Try 2/3 = {2/3:.4f} (error: {100*abs(2/3 - BR_W_had)/BR_W_had:.2f}%)")
print(f"  Try O_L - 0.01 = {O_L - 0.01:.4f} (error: {100*abs(O_L - 0.01 - BR_W_had)/BR_W_had:.2f}%)")

# ============================================================
# SECTION 3: HIGGS BRANCHING RATIOS
# ============================================================
print("\n" + "=" * 70)
print("SECTION 3: HIGGS BRANCHING RATIOS")
print("=" * 70)

BR_H_bb = 0.58    # H -> bb
BR_H_WW = 0.21    # H -> WW*
BR_H_gg = 0.082   # H -> gg
BR_H_tautau = 0.063  # H -> tau tau
BR_H_ZZ = 0.026   # H -> ZZ*
BR_H_gamgam = 0.00227  # H -> gamma gamma

print(f"\nHiggs branching ratios:")

print(f"\n  BR(H->bb) observed: {BR_H_bb}")
print(f"  Try Z/10 = {Z/10:.4f} (error: {100*abs(Z/10 - BR_H_bb)/BR_H_bb:.2f}%)")
print(f"  Try 3*O_m + O_L/2 = {3*O_m + O_L/2:.4f} (error: {100*abs(3*O_m + O_L/2 - BR_H_bb)/BR_H_bb:.2f}%)")

print(f"\n  BR(H->WW) observed: {BR_H_WW}")
print(f"  Try O_m - 0.10 = {O_m - 0.10:.4f} (error: {100*abs(O_m - 0.10 - BR_H_WW)/BR_H_WW:.2f}%)")
print(f"  Try 1/Z + 0.03 = {1/Z + 0.03:.4f} (error: {100*abs(1/Z + 0.03 - BR_H_WW)/BR_H_WW:.2f}%)")

print(f"\n  BR(H->gg) observed: {BR_H_gg}")
print(f"  Try alpha_s - 0.036 = {alpha_s - 0.036:.4f} (error: {100*abs(alpha_s - 0.036 - BR_H_gg)/BR_H_gg:.2f}%)")
print(f"  Try alpha_s * O_L = {alpha_s * O_L:.4f} (error: {100*abs(alpha_s * O_L - BR_H_gg)/BR_H_gg:.2f}%)")
print(f"  Try 1/Z^2 + 0.05 = {1/Z**2 + 0.05:.4f} (error: {100*abs(1/Z**2 + 0.05 - BR_H_gg)/BR_H_gg:.2f}%)")

print(f"\n  BR(H->tau tau) observed: {BR_H_tautau}")
print(f"  Try O_m/5 = {O_m/5:.4f} (error: {100*abs(O_m/5 - BR_H_tautau)/BR_H_tautau:.2f}%)")

print(f"\n  BR(H->ZZ) observed: {BR_H_ZZ}")
print(f"  Try alpha + 0.019 = {alpha + 0.019:.4f} (error: {100*abs(alpha + 0.019 - BR_H_ZZ)/BR_H_ZZ:.2f}%)")

print(f"\n  BR(H->gamma gamma) observed: {BR_H_gamgam}")
print(f"  Try alpha/3.2 = {alpha/3.2:.5f} (error: {100*abs(alpha/3.2 - BR_H_gamgam)/BR_H_gamgam:.2f}%)")
print(f"  Try O_m * alpha = {O_m * alpha:.5f} (error: {100*abs(O_m * alpha - BR_H_gamgam)/BR_H_gamgam:.2f}%)")
print(f"  Try O_m/137 = {O_m/137:.5f} (error: {100*abs(O_m/137 - BR_H_gamgam)/BR_H_gamgam:.2f}%)")

# ============================================================
# SECTION 4: GRAVITATIONAL & PLANCK SCALE
# ============================================================
print("\n" + "=" * 70)
print("SECTION 4: GRAVITATIONAL & PLANCK SCALE")
print("=" * 70)

M_Pl = 1.221e19  # GeV (Planck mass)
m_p_GeV = m_p / 1000  # Proton mass in GeV

ratio_Pl_p = M_Pl / m_p_GeV
log_ratio = np.log10(ratio_Pl_p)

print(f"\nPlanck/proton mass hierarchy:")
print(f"  M_Pl/m_p = {ratio_Pl_p:.3e}")
print(f"  log10(M_Pl/m_p) = {log_ratio:.3f}")
print(f"  Try 137/7.2 = {137/7.2:.3f} (error: {100*abs(137/7.2 - log_ratio)/log_ratio:.2f}%)")
print(f"  Try (4Z^2+3)/7.2 = {(4*Z**2+3)/7.2:.3f} (error: {100*abs((4*Z**2+3)/7.2 - log_ratio)/log_ratio:.2f}%)")
print(f"  Try Z^2/1.76 = {Z**2/1.76:.3f} (error: {100*abs(Z**2/1.76 - log_ratio)/log_ratio:.2f}%)")

# ============================================================
# SECTION 5: ELECTRON ANOMALOUS MAGNETIC MOMENT
# ============================================================
print("\n" + "=" * 70)
print("SECTION 5: LEPTON ANOMALOUS MAGNETIC MOMENTS")
print("=" * 70)

a_e = 0.00115965218091  # Electron (g-2)/2
a_mu = 0.00116592061    # Muon (g-2)/2

# Leading term should be alpha/(2*pi)
alpha_2pi = alpha / (2 * np.pi)
print(f"\nElectron anomaly a_e:")
print(f"  Observed: {a_e:.11f}")
print(f"  alpha/(2*pi) = {alpha_2pi:.11f}")
print(f"  Ratio a_e/(alpha/2pi) = {a_e/alpha_2pi:.6f}")
print(f"  This is 1 + O(alpha) corrections - known QED!")

print(f"\nMuon anomaly a_mu:")
print(f"  Observed: {a_mu:.11f}")
print(f"  alpha/(2*pi) = {alpha_2pi:.11f}")
print(f"  a_mu - a_e = {(a_mu - a_e)*1e6:.3f} x 10^-6")
print(f"  Try (m_mu/m_e)^2 * alpha^3 / 3 = {(m_mu/m_e)**2 * alpha**3 / 3 * 1e6:.3f} x 10^-6")

# ============================================================
# SECTION 6: FINE STRUCTURE MULTIPLET SPLITTINGS
# ============================================================
print("\n" + "=" * 70)
print("SECTION 6: ATOMIC FINE STRUCTURE")
print("=" * 70)

# Hydrogen 2P splitting
E_2P_split = 4.53e-5  # eV (2P3/2 - 2P1/2)
E_1S = 13.6  # eV

ratio_FS = E_2P_split / E_1S
print(f"\nHydrogen 2P fine structure splitting:")
print(f"  Delta E / E_1S = {ratio_FS:.6f}")
print(f"  alpha^2/16 = {alpha**2/16:.6f} (error: {100*abs(alpha**2/16 - ratio_FS)/ratio_FS:.2f}%)")

# Lamb shift
E_Lamb = 4.372e-6  # eV (2S1/2 - 2P1/2)
print(f"\nLamb shift:")
print(f"  E_Lamb = {E_Lamb*1e6:.3f} micro-eV")
print(f"  E_Lamb/E_1S = {E_Lamb/E_1S:.2e}")
print(f"  alpha^3 * ln(1/alpha) / 3pi = {alpha**3 * np.log(1/alpha) / (3*np.pi):.2e}")

# ============================================================
# SECTION 7: NUCLEAR BINDING ENERGIES
# ============================================================
print("\n" + "=" * 70)
print("SECTION 7: NUCLEAR BINDING ENERGIES")
print("=" * 70)

# Binding energy per nucleon (peak at Fe-56)
BE_Fe = 8.79  # MeV per nucleon
BE_He4 = 7.07  # MeV per nucleon

print(f"\nBinding energy per nucleon:")
print(f"  Iron-56: {BE_Fe} MeV")
print(f"  Try Z + 3 = {Z + 3:.2f} MeV (error: {100*abs(Z+3 - BE_Fe)/BE_Fe:.2f}%)")
print(f"  Try 3*Z/2 = {3*Z/2:.2f} MeV (error: {100*abs(3*Z/2 - BE_Fe)/BE_Fe:.2f}%)")

print(f"\n  Helium-4: {BE_He4} MeV")
print(f"  Try Z + 1.3 = {Z + 1.3:.2f} MeV (error: {100*abs(Z+1.3 - BE_He4)/BE_He4:.2f}%)")
print(f"  Try Z * 1.22 = {Z * 1.22:.2f} MeV (error: {100*abs(Z*1.22 - BE_He4)/BE_He4:.2f}%)")

# Alpha particle binding
BE_alpha_total = 28.3  # MeV total
print(f"\n  He-4 total binding: {BE_alpha_total} MeV")
print(f"  Try 4*(Z + 1.3) = {4*(Z + 1.3):.2f} MeV (error: {100*abs(4*(Z+1.3) - BE_alpha_total)/BE_alpha_total:.2f}%)")
print(f"  Try 5*Z - 0.6 = {5*Z - 0.6:.2f} MeV (error: {100*abs(5*Z - 0.6 - BE_alpha_total)/BE_alpha_total:.2f}%)")

# Triton binding
BE_H3 = 8.48  # MeV (triton)
print(f"\n  Triton binding: {BE_H3} MeV")
print(f"  Try Z + 2.7 = {Z + 2.7:.2f} MeV (error: {100*abs(Z+2.7 - BE_H3)/BE_H3:.2f}%)")
print(f"  Try 3*Z/2 - 0.2 = {3*Z/2 - 0.2:.2f} MeV (error: {100*abs(3*Z/2 - 0.2 - BE_H3)/BE_H3:.2f}%)")

# ============================================================
# SECTION 8: MORE MESON PROPERTIES
# ============================================================
print("\n" + "=" * 70)
print("SECTION 8: MORE MESON PROPERTIES")
print("=" * 70)

# D meson masses
m_D0 = 1864.84  # MeV
m_Dplus = 1869.66  # MeV
m_Ds = 1968.35  # MeV

print(f"\nD meson mass ratios:")
print(f"  m_D/m_p = {m_D0/m_p:.4f}")
print(f"  Try 2 - 0.01 = 1.99 (error: {100*abs(1.99 - m_D0/m_p)/(m_D0/m_p):.2f}%)")
print(f"  Try Z/2.9 = {Z/2.9:.4f} (error: {100*abs(Z/2.9 - m_D0/m_p)/(m_D0/m_p):.2f}%)")

print(f"\n  m_Ds/m_D = {m_Ds/m_D0:.4f}")
print(f"  Try 1 + alpha_s/2 = {1 + alpha_s/2:.4f} (error: {100*abs(1 + alpha_s/2 - m_Ds/m_D0)/(m_Ds/m_D0):.2f}%)")

# Pion lifetime
tau_pi_charged = 2.6e-8  # seconds
tau_pi0 = 8.5e-17  # seconds

print(f"\nPion lifetimes:")
print(f"  tau(pi+)/tau(pi0) = {tau_pi_charged/tau_pi0:.2e}")
print(f"  This is ~ (m_mu/m_pi)^2 / alpha^2 = {(m_mu/m_pi)**2 / alpha**2:.2e}")

# ============================================================
# SECTION 9: W/Z RATIO PRECISION
# ============================================================
print("\n" + "=" * 70)
print("SECTION 9: PRECISION W/Z RELATIONSHIPS")
print("=" * 70)

rho_param = (m_W / m_Z)**2 / (1 - (m_W/m_Z)**2)  # Related to sin^2(theta_W)
print(f"\nW/Z mass ratio:")
print(f"  m_W/m_Z = {m_W/m_Z:.5f}")
print(f"  cos(theta_W) theoretical = {np.cos(np.pi/6):.5f}")
print(f"  Try sqrt(1 - O_m) = {np.sqrt(1 - O_m):.5f} (error: {100*abs(np.sqrt(1-O_m) - m_W/m_Z)/(m_W/m_Z):.3f}%)")
print(f"  Try sqrt(O_L + 0.095) = {np.sqrt(O_L + 0.095):.5f} (error: {100*abs(np.sqrt(O_L + 0.095) - m_W/m_Z)/(m_W/m_Z):.3f}%)")

# ============================================================
# SECTION 10: STRANGE QUARK CONTENT OF PROTON
# ============================================================
print("\n" + "=" * 70)
print("SECTION 10: PROTON STRUCTURE")
print("=" * 70)

# Strange quark momentum fraction
x_s = 0.023  # Strange quark momentum fraction in proton (approximate)
print(f"\nStrange quark content in proton:")
print(f"  <x>_s observed: ~{x_s}")
print(f"  Try 3*alpha = {3*alpha:.4f} (error: {100*abs(3*alpha - x_s)/x_s:.1f}%)")

# Gluon momentum fraction
x_g = 0.41  # Gluon momentum fraction at Q^2 ~ few GeV^2
print(f"\nGluon momentum fraction:")
print(f"  <x>_g observed: ~{x_g}")
print(f"  Try O_L - 0.27 = {O_L - 0.27:.4f} (error: {100*abs(O_L - 0.27 - x_g)/x_g:.1f}%)")
print(f"  Try 1 - O_L + 0.13 = {1 - O_L + 0.13:.4f} (error: {100*abs(1 - O_L + 0.13 - x_g)/x_g:.1f}%)")

# ============================================================
# SECTION 11: COSMOLOGICAL SOUND HORIZON
# ============================================================
print("\n" + "=" * 70)
print("SECTION 11: COSMOLOGICAL SCALES")
print("=" * 70)

r_s = 147.09  # Mpc - sound horizon at drag epoch
theta_s = 1.0411e-2  # Sound horizon angular scale (radians)

print(f"\nCosmological sound horizon:")
print(f"  r_s = {r_s} Mpc")
print(f"  r_s / 100 = {r_s/100:.4f}")
print(f"  Try Z/4 = {Z/4:.4f} (error: {100*abs(Z/4 - r_s/100)/(r_s/100):.2f}%)")

print(f"\n  theta_s = {theta_s} rad = {np.degrees(theta_s):.3f} deg")
print(f"  Try alpha * 1.43 = {alpha * 1.43:.5f} (error: {100*abs(alpha*1.43 - theta_s)/theta_s:.2f}%)")

# Age of universe
t_0 = 13.8  # Gyr
H_0 = 67.4  # km/s/Mpc
t_H = 1 / (H_0 / 3.086e19 / 3.156e16)  # Hubble time in Gyr ~ 14.5

print(f"\nAge ratios:")
print(f"  t_0/t_H = {t_0/t_H:.4f}")
print(f"  Try O_L + 0.27 = {O_L + 0.27:.4f} (error: {100*abs(O_L + 0.27 - t_0/t_H)/(t_0/t_H):.2f}%)")

# ============================================================
# SUMMARY OF BEST NEW FINDINGS
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY: BEST NEW DISCOVERIES")
print("=" * 70)

discoveries = []

# Check each and add good ones
# BR_H_gg
pred = alpha_s * O_L
obs = BR_H_gg
err = 100*abs(pred - obs)/obs
if err < 5:
    discoveries.append(f"BR(H->gg) = alpha_s * O_L = {pred:.4f} vs {obs} ({err:.2f}%)")

# BR_H_tautau
pred = O_m / 5
obs = BR_H_tautau
err = 100*abs(pred - obs)/obs
if err < 5:
    discoveries.append(f"BR(H->tau tau) = O_m/5 = {pred:.4f} vs {obs} ({err:.2f}%)")

# BE per nucleon Fe
pred = Z + 3
obs = BE_Fe
err = 100*abs(pred - obs)/obs
if err < 5:
    discoveries.append(f"BE/A(Fe-56) = Z + 3 = {pred:.2f} MeV vs {obs} ({err:.2f}%)")

# He-4 total binding
pred = 5*Z - 0.6
obs = BE_alpha_total
err = 100*abs(pred - obs)/obs
if err < 5:
    discoveries.append(f"BE(He-4) = 5Z - 0.6 = {pred:.2f} MeV vs {obs} ({err:.2f}%)")

# D meson
pred = Z/2.9
obs = m_D0/m_p
err = 100*abs(pred - obs)/obs
if err < 3:
    discoveries.append(f"m_D/m_p = Z/2.9 = {pred:.4f} vs {obs:.4f} ({err:.2f}%)")

# Ds/D ratio
pred = 1 + alpha_s/2
obs = m_Ds/m_D0
err = 100*abs(pred - obs)/obs
if err < 3:
    discoveries.append(f"m_Ds/m_D = 1 + alpha_s/2 = {pred:.4f} vs {obs:.4f} ({err:.2f}%)")

print("\nNew quantities with good precision:")
for d in discoveries:
    print(f"  - {d}")

if not discoveries:
    print("  No new sub-5% matches found in this search")
    print("  Need to continue exploring other domains...")
