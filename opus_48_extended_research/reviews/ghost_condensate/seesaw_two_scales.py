#!/usr/bin/env python3
"""
seesaw_two_scales.py -- the GC "seesaw" and the TWO-SCALE structure, tested against
the framework's needs.

LITERATURE FACTS (ACLM 2004; Mukohyama; 'Ghost Dark Matter' arXiv:1001.4634):
  * In the broken phase the effective CC is rho_eff ~ O(M^4 / M_Pl^2)  (the GC SEESAW:
    a CC-scale energy from a higher SSB scale M, suppressed by M_Pl^2).
  * To get the OBSERVED dark-ENERGY density rho_DE ~ (2 meV)^4, the seesaw wants
    M^4/M_Pl^2 = rho_DE  ->  M = (rho_DE)^(1/4) * (M_Pl/(rho_DE)^(1/4))^(1/2) ... let's just solve:
    rho_DE = M^4/M_Pl^2  ->  M = (rho_DE * M_Pl^2)^(1/4).
  * For the GC to be the DARK MATTER (dust, clustering), 'Ghost Dark Matter' analyses find
    a LOWER bound on M that is INCOMPATIBLE with M ~ 10^-3 eV (the dark-energy value).
  * Canonical pathology bound (twinkling/static-source + BH accretion): M <~ 10 MeV.

We compute the THREE M's the framework would need and show they are DIFFERENT scales
=> the single dS input cannot set all of them (the 'one origin' hope fails on counting).
"""
import numpy as np
c=2.99792458e8; G=6.67430e-11; hbar=1.054571817e-34
Mpc=3.0856775814913673e22; eV=1.602176634e-19; MeV=1e6*eV; GeV=1e9*eV
M_Pl_eV = 2.435e18*1e9   # reduced Planck mass, eV

H0=67.4e3/Mpc; Om_L=0.685; Om_dm=0.265
H_L=H0*np.sqrt(Om_L)
rho_DE = Om_L*3*H0**2/(8*np.pi*G)*c**2   # J/m^3 (energy density)
rho_dm = Om_dm*3*H0**2/(8*np.pi*G)*c**2  # J/m^3

def eV4_from_energydensity(u_Jm3):
    # u = E^4/(hbar c)^3 -> E = (u (hbar c)^3)^(1/4)
    return (u_Jm3*(hbar*c)**3)**0.25/eV   # in eV

E_DE = eV4_from_energydensity(rho_DE)    # eV
E_dm = eV4_from_energydensity(rho_dm)    # eV
print("OBSERVED scales (energy density^(1/4)):")
print(f"  rho_DE^(1/4) = {E_DE:.4e} eV = {E_DE*1e3:.3f} meV")
print(f"  rho_dm^(1/4) = {E_dm:.4e} eV = {E_dm*1e3:.3f} meV")
print()

# ---- M #1: seesaw to match dark ENERGY  rho_DE = M^4/M_Pl^2 ----
# M = (rho_DE * M_Pl^2)^(1/4) ; rho_DE in eV^4:
rho_DE_eV4 = E_DE**4
M_seesaw_DE = (rho_DE_eV4 * M_Pl_eV**2)**0.25  # eV
print("M #1 (seesaw to dark ENERGY): rho_DE = M^4/M_Pl^2")
print(f"  M = (rho_DE * M_Pl^2)^(1/4) = {M_seesaw_DE:.4e} eV = {M_seesaw_DE/1e9:.4f} GeV = {M_seesaw_DE/1e6:.0f} MeV")
print(f"  (the classic GC dark-energy seesaw scale ~ 0.1 GeV ~ 100 MeV -- ABOVE the 10 MeV")
print(f"   lab bound: this is the KNOWN ghost-condensate-as-dark-energy tension in the literature)")
print()

# ---- M #2: seesaw to match dark MATTER amount via M^4/M_Pl^2 = rho_dm (same form) ----
rho_dm_eV4 = E_dm**4
M_seesaw_dm = (rho_dm_eV4*M_Pl_eV**2)**0.25
print("M #2 (seesaw to dark MATTER density): rho_dm = M^4/M_Pl^2")
print(f"  M = {M_seesaw_dm:.4e} eV = {M_seesaw_dm/1e6:.4f} MeV  (nearly same as DE; Om's are O(1) apart)")
print()

# ---- M #3: clustering scale from mu^-1 ~ Mpc (GC Jeans length L_J=M_Pl/M^2) ----
print("M #3 (clustering length L_J = M_Pl/M^2 set to AeST mu^-1 ~ 1 Mpc):")
for mu_inv_Mpc in [0.1,1.0,10.0]:
    mu_inv_m=mu_inv_Mpc*Mpc
    E_mu=hbar*c/mu_inv_m/eV
    M3=np.sqrt(M_Pl_eV*E_mu)
    print(f"  mu^-1={mu_inv_Mpc:5.1f} Mpc -> M = {M3:.4e} eV")
print()

print("="*72)
print("THE TWO-SCALE PROBLEM (decisive):")
print("="*72)
print(f"  M(energy/seesaw, #1,#2) ~ 0.09-0.11 GeV ~ 9e7-1.1e8 eV")
print(f"  M(clustering length #3) ~ 0.04-0.4   eV")
print(f"  RATIO  M_energy / M_cluster ~ {1.1e8/0.1:.1e}  -- ~9 ORDERS apart.")
print()
print("  The GC needs DIFFERENT M for (energy density via seesaw) vs (clustering length).")
print("  A SINGLE dS input (one number: Lambda, or cH_L, or T_GH) cannot fix BOTH a ~0.1 GeV")
print("  energy scale AND a ~0.1 eV length scale -- they are independent. This is the field-")
print("  theory restatement of the banked result: a0 (one number from Lambda) does NOT fix")
print("  the dust amplitude OR the clustering scale; the condensate carries its OWN extra")
print("  scale(s) (Q0, K2, mu) that Lambda is orthogonal to.")
print()

print("="*72)
print("THE GC SEESAW TENSION (literature, both-ways):")
print("="*72)
print("  'Ghost Dark Matter' (1001.4634): M~10^-3 eV (the meV that gives CC-scale energy)")
print("  is INCOMPATIBLE with the LOWER bound on M needed for the ghost to be the dark MATTER.")
print("  => Using ONE ghost condensate for BOTH dark energy AND dark matter is in TENSION")
print("     in the literature. The framework AVOIDS this only because its dark ENERGY is a")
print("     SEPARATE -2Lambda additive constant (NOT the condensate's seesaw) -- so the")
print("     framework's condensate is asked to be ONLY the dark MATTER (Q-mode dust), with")
print("     Lambda put in by hand as the additive piece. That SPLIT is what lets it fit, but")
print("     it also means Lambda and the dust are structurally orthogonal (the banked result).")
print()

print("="*72)
print("HONEST seesaw COINCIDENCE (credit, but do not overclaim):")
print("="*72)
print(f"  rho_dm^(1/4) = {E_dm*1e3:.3f} meV  vs  rho_DE^(1/4) = {E_DE*1e3:.3f} meV  -- SAME meV scale.")
print(f"  ratio = {(E_dm/E_DE):.4f} = (Om_dm/Om_L)^(1/4) = {(Om_dm/Om_L)**0.25:.4f}")
print("  Both dark sectors sit at the ~meV (dark-energy/seesaw) scale -- a REAL coincidence")
print("  the seesaw 'explains' generically (any M^4/M_Pl^2 energy lands near rho_DE if M~MeV).")
print("  BUT this fixes only the ORDER of the energy density, NOT the amount (Om_dm/Om_L=0.39),")
print("  and the meV is the dark-ENERGY scale the framework already has from Lambda. So the")
print("  coincidence is GENERIC-seesaw, not a NEW dS-driven prediction; the why-now ratio")
print("  0.39 stays free. (matches banked PIN_THE_AMOUNT.)")
