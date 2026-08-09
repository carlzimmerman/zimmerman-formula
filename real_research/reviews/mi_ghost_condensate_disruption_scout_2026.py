#!/usr/bin/env python3
"""
Ghost-condensate disruption / clustering scout: all load-bearing numbers.
Sources are cited inline. Natural units hbar=c=1 unless noted.
"""
import numpy as np

# ---- constants ----
eV      = 1.0
MPl_red = 2.435e27 * eV          # reduced Planck mass, ACLM define MPl^2 = 1/(8 pi G) (their eq 7.3)
hbarc_m = 1.9733e-7              # m per eV^-1
hbar_s  = 6.5821e-16             # s per eV^-1
Mpc_m   = 3.0857e22
kpc_m   = 3.0857e19
G       = 6.674e-11
c       = 2.99792458e8
Msun    = 1.989e30
yr      = 3.156e7
t0_s    = 13.8e9 * yr            # age of universe
H0      = 67.4e3 / Mpc_m         # s^-1
rho_crit= 3*H0**2/(8*np.pi*G)    # kg/m^3
rho_L   = 0.685*rho_crit
rho_dm0 = 0.265*rho_crit

def eVinv_to_m(x): return x*hbarc_m
def eVinv_to_s(x): return x*hbar_s

print("="*74)
print("BLOCK 1 -- ACLM 2004 (hep-th/0312099) linear Jeans rate and scales")
print("  Gamma = alpha M^3/(4 MPl^2) [eq 7.10];  r_c ~ MPl/M^2, t_c ~ MPl^2/(alpha M^3) [eq 7.15]")
print("="*74)
M_nat = (rho_L*c**2/ (1/(hbarc_m**3) * 1.602176634e-19))**0.25  # rho_L in eV^4 -> M in eV
# do it cleanly instead: rho_L [kg/m3] -> eV^4
J_per_eV = 1.602176634e-19
rho_L_eV4 = (rho_L*c**2/J_per_eV) * hbarc_m**3    # (eV/m^3)*(m^3 eV^3) = eV^4
M_nat = rho_L_eV4**0.25
print(f"  rho_Lambda            = {rho_L:.4e} kg/m^3 = {rho_L_eV4:.4e} eV^4")
print(f"  M_natural = rho_L^1/4 = {M_nat:.4e} eV = {M_nat*1e3:.3f} meV   (context says 2.24 meV)")

for label, M in [("M = 2.24 meV (natural)", M_nat), ("M = 10 MeV (ACLM upper)", 1e7)]:
    Gamma  = M**3/(4*MPl_red**2)          # alpha = 1
    t_c    = 1.0/Gamma
    m_mass = M**2/(np.sqrt(2)*MPl_red)    # eq 7.7
    r_c    = eVinv_to_m(1.0/m_mass)
    lamJ   = 2*np.pi*r_c
    print(f"\n  {label}")
    print(f"    Gamma^-1 = t_c   = {eVinv_to_s(t_c):.3e} s = {eVinv_to_s(t_c)/t0_s:.3e} x age of universe")
    print(f"    r_c = 1/m        = {r_c/Mpc_m:.4e} Mpc")
    print(f"    lambda_J = 2pi/m = {lamJ/Mpc_m:.4e} Mpc  = {lamJ/(c/H0):.3g} x Hubble radius")

# invert: what M gives t_c = age of universe?  (origin of ACLM's "10 MeV")
M_tc = (4*MPl_red**2 / (t0_s/hbar_s))**(1/3)
print(f"\n  M such that t_c = age of universe: {M_tc/1e6:.2f} MeV   -> ACLM's M <~ 10 MeV is exactly this")

print()
print("="*74)
print("BLOCK 2 -- ACLMW 2007 (hep-ph/0507120, JHEP 0701:036) nonlinear fluid")
print("  eq 3.15: rho = M^4 Sigma, p = (1/2) M^4 Sigma^2 = rho^2/(2 M^4)")
print("  footnote 2: L_J = 2 pi c_s / sqrt(4 pi G rho) with c_s^2 = rho/M^4  ==> DENSITY-INDEPENDENT")
print("="*74)
def LJ_nonlinear(M_eV):
    # L_J = 2 pi sqrt(2) MPl / M^2   (derivation checked below)
    return eVinv_to_m(2*np.pi*np.sqrt(2)*MPl_red/M_eV**2)
# explicit check at two very different densities
for rho_test_name, rho_test in [("cosmic mean DM", rho_dm0), ("1e6 x cosmic mean", 1e6*rho_dm0)]:
    M = M_nat
    M4_kg = (M**4 / hbarc_m**3) * J_per_eV / c**2    # eV^4 -> kg/m^3
    cs2 = rho_test/M4_kg
    lam = 2*np.pi*np.sqrt(cs2)*c/np.sqrt(4*np.pi*G*rho_test)
    print(f"  rho = {rho_test_name:20s}: c_s^2={cs2:.3e}, lambda_J = {lam/Mpc_m:.4e} Mpc")
print(f"  closed form 2pi sqrt(2) MPl/M^2 at M_nat = {LJ_nonlinear(M_nat)/Mpc_m:.4e} Mpc  (identical, as required)")

print()
print("="*74)
print("BLOCK 3 -- map ACLMW's M onto AeST/Khronon mu  [Blanchet-Skordis 2024 arXiv:2404.06584]")
print("  their eq 4.14: rho_K = mu^2 (Q^2-1)/(8 pi G);  P_K = K(Q)/(8 pi G) = mu^2 (Q-1)^2/(8 pi G)")
print("  => eps=Q-1: rho_K = mu^2 eps/(4 pi G), P_K = 2 pi G rho_K^2/mu^2")
print("  matching P = rho^2/(2 M^4)  =>  M^4 = mu^2/(4 pi G) = 2 mu^2 MPl^2  =>  M^2 = sqrt(2) mu MPl")
print("  => L_J = 2 pi sqrt(2) MPl/M^2 = 2 pi / mu   EXACTLY")
print("="*74)
print("  direct check: c_ad^2 = dP/drho = (Q-1)/Q ~= eps = 4 pi G rho_K/mu^2")
print("               L_J = 2 pi c_ad/sqrt(4 pi G rho_K) = 2 pi/mu    (rho cancels identically)")
for muinv_Mpc in [0.1, 1.0, 3.0]:
    mu_m = 1.0/(muinv_Mpc*Mpc_m)
    M_eq = np.sqrt(np.sqrt(2) * (mu_m*hbarc_m) * MPl_red)   # mu in eV = mu_m * hbarc_m
    print(f"  mu^-1 = {muinv_Mpc:5.2f} Mpc  ->  L_J = 2pi/mu = {2*np.pi*muinv_Mpc:7.3f} Mpc, "
          f"equivalent ACLMW M = {M_eq:.4g} eV")

print()
print("="*74)
print("BLOCK 4 -- the quasi-static Q-sector contribution xi = (mu R)^2")
print("  AeST static weak field [Durakovic-Skordis 2023 arXiv:2312.00889 eq 2.20/2.25]:")
print("     lap(Phi_tilde) + mu^2 Phi = 4 pi G rho_b     <-- BARYONS ONLY on the RHS")
print("  Mistele-McGaugh-Hossenfelder 2023 eq 2: rho_c = (m^2/f_G)(mu_chem/Q0 - Phi)/(4 pi G_N)")
print("  hydrostatic/linear-response equivalent: Delta rho_Q = mu^2 |Phi|/(4 pi G)")
print("="*74)
def xi_of(Mbar_Msun, R_m, muinv_Mpc, fdm_needed):
    mu_m = 1.0/(muinv_Mpc*Mpc_m)
    Phi = G*Mbar_Msun*Msun*(1+fdm_needed)/R_m      # total potential depth (SI, m^2/s^2)
    drho = mu_m**2 * Phi/(4*np.pi*G)               # kg/m^3
    Mtot = Mbar_Msun*Msun*(1+fdm_needed)
    rho_dm_need = (Mtot - Mbar_Msun*Msun)/(4/3*np.pi*R_m**3)
    return drho, rho_dm_need, drho/rho_dm_need, (mu_m*R_m)**2

systems = [
    ("Milky Way @ 10 kpc",  6.0e10, 10*kpc_m,  5.0),
    ("MW outskirts @156kpc",6.0e10, 156*kpc_m, 12.0),
    ("cluster @ R500=1.4Mpc",1.55e14, 1.4*Mpc_m, 5.4387),
]
for muinv in [1.0, 3.0]:
    print(f"\n  --- mu^-1 = {muinv} Mpc  (L_J = {2*np.pi*muinv:.2f} Mpc) ---")
    for nm, Mb, R, fdm in systems:
        drho, need, xi, muR2 = xi_of(Mb, R, muinv, fdm)
        print(f"    {nm:24s} xi = drho_Q/rho_dm,needed = {xi:.3e}   [(mu R)^2 = {muR2:.3e}]")

print("\n  Framework's requirement (context item 5): xi ~ 0 in galaxies, xi = 0.11-0.26 at cluster R500")
# solve for mu^-1 that gives xi=0.2 at R500
from scipy.optimize import brentq
f = lambda x: xi_of(1.55e14, 1.4*Mpc_m, x, 5.4387)[2] - 0.20
muinv_needed = brentq(f, 0.05, 50)
print(f"  mu^-1 giving xi = 0.20 at R500=1.4 Mpc : {muinv_needed:.3f} Mpc  "
      f"(mu^2 = {1/muinv_needed**2:.3f} Mpc^-2)")
print(f"    -> at that mu, MW @10 kpc: xi = {xi_of(6.0e10,10*kpc_m,muinv_needed,5.0)[2]:.3e}")

print()
print("="*74)
print("BLOCK 5 -- Mistele-McGaugh-Hossenfelder 2023 (A&A 676:A100) Table 1, in mu^-1")
print("="*74)
for b, desc in [(1.0,"galaxies, weak lensing, a_b >= 1e-13 m/s^2 (UPPER on mu^2)"),
                (0.001,"galaxies, weak lensing, a_b >= 1e-15 m/s^2 (UPPER on mu^2)"),
                (1.0,"galaxy clusters a_b~1e-10.5 (LOWER on mu^2)"),
                (2.5,"galaxy clusters, numerical (LOWER on mu^2)"),
                (7.9,"galaxy clusters, their eq 9 (LOWER on mu^2)")]:
    print(f"  mu^2 = {b:8.4g} Mpc^-2  ->  mu^-1 = {1/np.sqrt(b):7.3f} Mpc,  L_J = 2pi/mu = {2*np.pi/np.sqrt(b):7.3f} Mpc   [{desc}]")
print("  => the SAME parameter is pushed UP by clusters and DOWN by galaxy weak lensing:")
print(f"     cluster floor mu^2 >= 2.5 vs galaxy ceiling mu^2 <= 0.001  -> {2.5/0.001:.0f}x conflict in mu^2 "
      f"({np.sqrt(2.5/0.001):.1f}x in mu)")

print()
print("="*74)
print("BLOCK 6 -- ACLMW eq 5.7/5.8: aether DRAG radius r_drag ~ R_S/v^2")
print("="*74)
print("  For any VIRIALISED system v^2 = GM/(R c^2) and R_S = 2GM/c^2  =>  r_drag = 2R  EXACTLY.")
for nm, Mtot_Msun, R in [("Sun (ACLMW quote 10 R_sun)", 1.0, 6.957e8),
                         ("Milky Way", 1.0e12, 15*kpc_m),
                         ("cluster 1e15 Msun", 1.0e15, 1.4*Mpc_m)]:
    Rs = 2*G*Mtot_Msun*Msun/c**2
    v2 = G*Mtot_Msun*Msun/(R*c**2)
    print(f"    {nm:28s} R_S={Rs:.3e} m, v={np.sqrt(v2)*c/1e3:8.1f} km/s, r_drag={Rs/v2/R:.2f} R = {Rs/v2/kpc_m:.4g} kpc")
print("  CONCLUSION: the condensate is entrained out to ~2x the size of EVERY virialised system.")
print("  There is no 'the condensate is too stiff to notice the galaxy' escape.")

print()
print("="*74)
print("BLOCK 7 -- response/caustic timescales")
print("  ACLM eq 5.9: tau ~ M r^2 (k^4 static-limit validity time)")
print("  ACLMW eq 3.8: T_NL ~ L/sqrt(Phi) = the KEPLER time (caustics form on the dynamical time)")
print("="*74)
for nm, R, Phi in [("Milky Way 10 kpc", 10*kpc_m, (200e3)**2),
                   ("cluster R500 1.4 Mpc", 1.4*Mpc_m, (1300e3)**2)]:
    r_eVinv = R/hbarc_m
    tau = eVinv_to_s(M_nat * r_eVinv**2)
    TNL = R/np.sqrt(Phi)
    print(f"  {nm:22s} tau(k^4, M=M_nat) = {tau/t0_s:.3e} x age;  T_NL(Kepler) = {TNL/yr/1e6:.1f} Myr")
print("  => T_NL << tau << t_c: the NONLINEAR dynamics wins by ~20-30 orders. ACLMW sec 3.2:")
print("     'the nonlinear effects completely dominate the dynamics in all regimes of interest'")
print("  ACLMW eq 3.11: nonlinear regime for r > (1/M_src)(MPl/M)^2; 'earth surface gravity is")
print("     in the nonlinear regime for M >~ 1e-8 eV'  -- M_nat=2.24e-3 eV is 5 orders above that.")

print()
print("="*74)
print("BLOCK 8 -- Peloso & Sorbo 2004 (PLB 593:25) condensate signal speed")
print("="*74)
v_s = 1e-12
print(f"  quoted v_s ~ {v_s:.0e} m/s.  Galactic rotation 200 km/s is {200e3/v_s:.1e}x faster.")
print(f"  distance travelled by a condensate signal in one age of universe: {v_s*t0_s:.3e} m = {v_s*t0_s/1e3:.0f} km")
print("  => the k^4 condensate mode CANNOT track a moving source; they recover standard Newton.")

print()
print("="*74)
print("BLOCK 9 -- bounds on the ghost-condensate scale M, collected")
print("="*74)
rows = [
 ("ACLM 2004 hep-th/0312099 eq 1.12", "M <~ 10 MeV",  "linear Jeans time t_c > age of universe"),
 ("Peloso-Sorbo 2004 PLB 593:25",     "M <~ 10 MeV-ish","vacuum stability over lifetime of universe"),
 ("Frolov 2004 PRD 70:061501(R)",     "M <~ 1 keV",   "stellar-mass BH must not double in 14 Gyr"),
 ("Frolov 2004 PRD 70:061501(R)",     "M <~ 10 eV",   "1e9 Msun SMBH must not double in 14 Gyr"),
 ("  ^ disputed by Mukohyama 2005 PRD 71:104019", "-", "Frolov neglected gravitational backreaction"),
 ("ACLMW 2007 JHEP 0701:036 eq 5.14", "M <~ 100 GeV", "CMB 'twinkling' from lensing random walk"),
 ("ACLMW 2007 eq 5.10",               "M <~ 1e3 GeV", "Jeans lumps lighter than 1 Msun"),
 ("ACLMW 2007 eq 5.16",               "M <~ 1e3 GeV", "SN Ia time-delay vs WMAP"),
]
for a,b,d in rows: print(f"  {a:46s} {b:14s} {d}")
print(f"\n  Natural scale M = rho_L^(1/4) = {M_nat*1e3:.2f} meV clears every one of these by >= 3.6 orders")
print(f"  (tightest is Frolov's 10 eV: margin {10/M_nat:.0f}x).")
print("  AeST-equivalent: mu^-1 = 1 Mpc  <->  M = "
      f"{np.sqrt(np.sqrt(2)*(1/Mpc_m*hbarc_m)*MPl_red):.4g} eV, also far below every bound.")
