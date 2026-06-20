#!/usr/bin/env python3
"""
amount_and_pathologies_calc.py
Ghost-condensate dark sector for the Zimmerman/AeST framework:
(a) AMOUNT pinning, (b) PATHOLOGY timescales.

Primary source: Arkani-Hamed, Cheng, Luty, Mukohyama (ACLM) hep-th/0312099.
  Eq (1.10): r_c ~ M_Pl/M^2,   t_c ~ M_Pl^2/M^3   (oscillation length/time)
  Eq (1.11): M ~ 1e-3 eV if GC drives today's acceleration (rho_DE ~ (1e-3 eV)^4)
  Eq (7.10): Gamma = alpha*M^3/(4*M_Pl^2)  (Jeans growth rate, instability magnitude)
  Eq (8.19): de Sitter REMOVES the instability iff  H > Gamma
  Eq (3.1):  T_mu_nu -> -g_mu_nu M^4 P(c^2)  => w = -1 (cosmological-constant-like) on attractor
  Eq (3.2):  off attractor P'(phidot^2) ~ 1/a^3 => sources gravity like NON-REL MATTER (w=0 dust)
  Strong coupling cutoff: Lambda_c ~ M  (EFT breaks at the symmetry-breaking scale)

AeST realization (Verwayen-Skordis-Boehm 2304.05134, Skordis-Zlosnik 2007.00082):
  - AeST weak-field Poisson eq (11): grad^2 Phi + (1+beta0) mu^2 Phi = 4 pi G rho_b
    "also results from the non-rel weak-field limit of the Ghost condensate model (ACLM 2004)"
  - oscillation radius r_C set by mu; mu^-1 >~ 1 Mpc to keep MOND at galaxy scales
  - r_C(mu=1 Mpc^-1)=156 kpc, r_C(mu=10 Mpc^-1)=33.6 kpc (Verwayen Fig.4)
  - Minkowski linear stability: lambda_s>0 and mu^2>0 (Skordis-Zlosnik 2021)

All units SI unless flagged eV.
"""
import math

# ---------- constants ----------
c    = 2.99792458e8          # m/s
hbar = 1.054571817e-34       # J s
G    = 6.674e-11             # SI
eV   = 1.602176634e-19       # J
Mpc  = 3.0857e22             # m
kpc  = 3.0857e19             # m
yr   = 3.1557e7              # s
Gyr  = 1e9*yr

# cosmology / framework
H0   = 67.4 *1e3/Mpc         # s^-1
OmL  = 0.685
OmM  = 0.315
Om_dm= 0.265                 # cold dark sector (~CDM)
Om_b = 0.0493
Lam  = 1.0909e-52            # m^-2  (banked)
a0   = 9.3624e-11            # m/s^2 (framework)
rho_crit = 3*H0**2/(8*math.pi*G)
rho_DE   = OmL*rho_crit
H_Lam = math.sqrt(Lam/3.0)*c        # de Sitter Hubble of the Lambda-only future ~ cH_Lam/c... see below
cH_Lam = c*math.sqrt(Lam/3.0)       # has units m/s; a0=cH_Lam/Z

# Planck mass (reduced, the M_Pl in ACLM with M_Pl^2 = 1/8piG)
M_Pl_red_J = math.sqrt(hbar*c**5/(8*math.pi*G))   # reduced Planck energy in Joules
M_Pl_red_eV = M_Pl_red_J/eV
M_Pl_GeV = M_Pl_red_eV/1e9

print("="*78)
print("FRAMEWORK / COSMOLOGY ANCHORS")
print("="*78)
print(f"H0                = {H0:.4e} s^-1   (1/H0 = {1/H0/Gyr:.2f} Gyr)")
print(f"rho_crit          = {rho_crit:.4e} kg/m^3")
print(f"rho_DE            = {rho_DE:.4e} kg/m^3")
print(f"a0 (framework)    = {a0:.4e} m/s^2")
print(f"cH_Lam            = {cH_Lam:.4e} m/s ;  Z=cH_Lam/a0 = {cH_Lam/a0:.4f}  (sqrt(32pi/3)={math.sqrt(32*math.pi/3):.4f})")
print(f"reduced M_Pl      = {M_Pl_red_eV:.4e} eV = {M_Pl_GeV:.4e} GeV")

# ---------- (a) AMOUNT: is M / Omega_dm pinned? ----------
print()
print("="*78)
print("(a) AMOUNT PINNING")
print("="*78)

# A1. The DARK-ENERGY face: ACLM Eq 3.1 + 1.11. If the GC drives today's acceleration,
#     rho_DE = M^4 |P(c^2)|.  With O(1) P, M ~ rho_DE^(1/4).
rho_DE_eV4 = rho_DE * c**2 / eV / (eV/( (hbar*c)**3 ))   # convert kg/m^3 -> eV^4
# cleaner: energy density in eV^4 :  rho c^2 [J/m^3] ; 1 eV^4 = (eV)^4/(hbar c)^3 J/m^3
u_DE = rho_DE*c**2                      # J/m^3
eV4_in_Jm3 = eV**4/(hbar*c)**3         # J/m^3 per eV^4
rho_DE_eV4 = u_DE/eV4_in_Jm3
M_from_DE_eV = rho_DE_eV4**0.25
print(f"A1 DARK-ENERGY face (ACLM 3.1, w=-1 attractor):")
print(f"   rho_DE = {u_DE:.3e} J/m^3 = {rho_DE_eV4:.3e} eV^4")
print(f"   M ~ rho_DE^(1/4) = {M_from_DE_eV:.4e} eV   (ACLM say ~1e-3 eV, Eq 1.11) -- MATCHES")
print(f"   => This face IS ~pinned by Lambda: M~(rho_DE)^1/4. But it gives w=-1 (dark ENERGY),")
print(f"      NOT the w=0 cold dust. It reproduces the framework's a0<->Lambda tie, not Omega_dm.")

# A2. The DARK-MATTER (dust) face: ACLM Eq 3.2 off-attractor P' ~ 1/a^3, rho_dust = Q0*I0/a^3.
#     Amplitude I0 is an INTEGRATION CONSTANT (first integral a^3 K'(Q)=I0). Independent of Lambda.
print()
print(f"A2 DARK-MATTER (dust) face (ACLM 3.2 off-attractor; AeST shift-sym first integral):")
print(f"   rho_dust = Q0*I0/a^3 ;  a^3 K'(Q)=I0 solves EOM for ANY I0.")
print(f"   d rho_dust/d Lambda = 0  (Lambda enters K only as additive -2Lambda; shift leaves K' fixed)")
print(f"   => Omega_dm={Om_dm} sets I0; I0 is a FREE boundary datum, NOT fixed by sqrt(Lambda).")
print(f"   why-now ratio Omega_dm/Omega_L = {Om_dm/OmL:.3f} is epoch-dependent -> cannot be a const")
print(f"      of the a-independent dS vacuum. No tracker/attractor present to pin it.")

# A3. The amplitude of P(X) curvature M^4: does it set BOTH faces? No -- M^4 sets the overall
#     scale (rho_DE) but the OFFSET P'(c^2)=0 attractor value (the dust amplitude) is the IC.
print()
print(f"A3 P(X) curvature M^4 sets the SCALE (rho_DE), the dust amplitude rides the OFFSET from")
print(f"   the attractor (I0). One number (M) is ~fixed by Lambda; the second (I0~Omega_dm) is free.")

# ---------- (b) PATHOLOGIES: timescales ----------
print()
print("="*78)
print("(b) PATHOLOGY TIMESCALES")
print("="*78)

def in_eV(M_eV): return M_eV*eV          # energy in Joules
def length_from_energy(E_J): return hbar*c/E_J   # Compton length of energy E

# Use ACLM Eq 1.10 with M as an ENERGY scale; M_Pl is the (reduced) Planck energy.
# r_c ~ M_Pl/M^2 (in natural units, length) ; t_c ~ M_Pl^2/M^3.
# Convert: in natural units length = 1/energy. r_c[length] = (M_Pl/M^2)*(hbar c) with M_Pl,M as energies^...
# Cleanest: work in natural units (hbar=c=1), energies in eV, lengths in 1/eV, then convert.
hbarc_eV_m = 197.3269804e-9 *1e-9   # hbar*c in eV*m :  197.33 MeV*fm = 197.33e6 eV * 1e-15 m
hbarc_eV_m = 197.3269804e6 * 1e-15  # = 1.9733e-7 eV*m
# time: hbar in eV*s
hbar_eV_s = 6.582119569e-16

def patho(M_eV, label):
    MPl = M_Pl_red_eV
    # natural-unit length 1/eV -> meters: L[m] = (1/eV)*hbarc_eV_m
    rc_invEV = MPl/M_eV**2                 # 1/eV
    rc_m = rc_invEV*hbarc_eV_m
    tc_invEV = MPl**2/M_eV**3              # 1/eV (a time in natural units = 1/energy)
    tc_s = tc_invEV*hbar_eV_s
    # Jeans growth rate Gamma = alpha M^3/(4 M_Pl^2), alpha~O(1) -> energy; 1/Gamma is a time
    alpha=1.0
    Gamma_eV = alpha*M_eV**3/(4*MPl**2)    # eV
    Gamma_s  = Gamma_eV/hbar_eV_s          # s^-1
    tJeans_s = 1.0/Gamma_s
    print(f"\n[{label}]  M = {M_eV:.3e} eV")
    print(f"   r_c ~ M_Pl/M^2 = {rc_m:.3e} m = {rc_m/Mpc:.3e} Mpc = {rc_m/kpc:.3e} kpc")
    print(f"   t_c ~ M_Pl^2/M^3 = {tc_s:.3e} s = {tc_s/Gyr:.3e} Gyr  (1/H0={1/H0/Gyr:.1f} Gyr)")
    print(f"   Gamma = M^3/(4 M_Pl^2) = {Gamma_s:.3e} s^-1 ; t_Jeans=1/Gamma = {tJeans_s/Gyr:.3e} Gyr")
    print(f"   H0/Gamma (dS stabilization needs >1): {H0/Gamma_s:.3e}  --> {'STABLE (H>Gamma)' if H0>Gamma_s else 'UNSTABLE'}")
    return rc_m, tc_s, tJeans_s, Gamma_s, H0/Gamma_s

# Scenario 1: GC-as-dark-ENERGY, M ~ 1e-3 eV (ACLM canonical; framework a0<->Lambda face)
patho(1e-3, "DE-scale (ACLM 1.11)")
# Scenario 2: ACLM upper window M ~ 10 MeV
patho(10e6, "10 MeV (ACLM upper)")
# Scenario 3: the AeST mass scale mu directly. mu is NOT M; mu is the screening mass with
# mu^-1 ~ 1 Mpc. Map: in AeST Poisson eq (11) mu^2 Phi term IS the ghost-condensate graviton
# mass^2. ACLM's m = M^2/(sqrt2 M_Pl) is the graviton mass. So mu ~ m = M^2/(sqrt2 M_Pl).
print()
print("="*78)
print("AeST mu <-> ACLM graviton mass m = M^2/(sqrt2 M_Pl); mu^-1 ~ 1 Mpc")
print("="*78)
mu_inv_m = 1.0*Mpc
m_eV = hbarc_eV_m/mu_inv_m              # graviton mass in eV from mu^-1 = 1 Mpc
print(f"mu^-1 = 1 Mpc  => m = hbar c / (1 Mpc) = {m_eV:.3e} eV  (graviton mass scale)")
# invert m = M^2/(sqrt2 M_Pl) -> M = sqrt(sqrt2 M_Pl m)
M_eV = math.sqrt(math.sqrt(2)*M_Pl_red_eV*m_eV)
print(f"=> M = sqrt(sqrt2 * M_Pl * m) = {M_eV:.3e} eV  (the GC symmetry-breaking scale for AeST)")
patho(M_eV, "AeST mu=1/Mpc")

# de Sitter stabilization condition, general:
print()
print("="*78)
print("dS STABILIZATION (ACLM Eq 8.19-8.24): H > Gamma => potential decays e^{-Ht}, NO growth")
print("="*78)
print("The framework LIVES in a de Sitter universe (Lambda>0, H0>0). For ALL M in the AeST/DE")
print("window, Gamma << H0, so H>>Gamma is satisfied by many orders -> the Jeans IR instability")
print("is REMOVED by Hubble friction. This is ACLM's own resolution and it is GENERIC for any")
print("M small enough to be cosmologically relevant. The pathology is NOT fatal in de Sitter.")
print()
print("Antigravity/oscillation onset time t_c >> 1/H0 for M~1e-3 eV (ACLM Eq 1.11): the")
print("oscillatory/antigravity modulation never has time to develop within a Hubble time.")
print("For AeST (mu^-1~1 Mpc), oscillation is a SPATIAL feature at r>r_C~156 kpc, pushed")
print("beyond galaxy disks by choosing mu small (mu is FREE, squeezed by data).")
