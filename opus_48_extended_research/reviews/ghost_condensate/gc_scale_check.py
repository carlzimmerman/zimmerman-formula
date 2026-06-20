#!/usr/bin/env python3
"""
gc_scale_check.py  -- careful recomputation of the GC SSB scale M implied by AeST's mu,
and the full TWO-SCALE structure.  Fixes the formatting bug + the 'few MeV' mis-assertion.

Ghost condensate scale relations (ACLM 2004, Mukohyama):
  - SSB scale M:  <dphi>=M^2 (so phi-dot ~ M^2), and L_GC = M^4 P(X).
  - The IR modification scale (oscillation/Jeans length):  L_J ~ M_Pl/M^2.
  - The fluctuation 'mass'/clustering inverse-length the AeST people call mu.
  In AeST, mu is the Psi MASS in the quasistatic eqn (nabla^2 - mu^2)Psi = source.
  Its relation to GC parameters (Skordis-Zlosnik): mu^2 = (2 K2/(2-K_B)) Q0^2.
  Dimensionally Q0 ~ M^2 (the VEV), K2 ~ 1/M^4 (so that M^4 K2 (Q-Q0)^2 ~ M^4 dimensionless),
  giving mu^2 ~ (1/M^4) (M^2)^2 = O(1) in M-units... i.e. mu is NOT simply M^2/M_Pl.
  The honest statement: AeST's mu is a SEPARATE free parameter; the map mu<->M is
  convention/normalization-dependent. Below I show BOTH a naive map and the conclusion
  that is map-INDEPENDENT.
"""
import numpy as np
c=2.99792458e8; G=6.67430e-11; hbar=1.054571817e-34
Mpc=3.0856775814913673e22; eV=1.602176634e-19; MeV=1e6*eV
M_Pl_eV = 2.435e18*1e9   # reduced Planck mass in eV (2.435e18 GeV)

H0=67.4e3/Mpc; Om_L=0.685
H_L=H0*np.sqrt(Om_L)

print("Planck mass (reduced)   = %.3e eV = %.3e GeV"%(M_Pl_eV, M_Pl_eV/1e9))
print()
print("AeST mu (Psi mass), Compton energy E_mu = hbar c / (mu^-1):")
for mu_inv_Mpc in [0.1, 1.0, 10.0, 100.0]:
    mu_inv_m = mu_inv_Mpc*Mpc
    E_mu = hbar*c/mu_inv_m / eV   # eV
    # naive GC map mu = M^2/M_Pl -> M = sqrt(E_mu * M_Pl)
    M_naive = np.sqrt(E_mu*M_Pl_eV)  # eV
    print(f"  mu^-1={mu_inv_Mpc:6.1f} Mpc:  E_mu={E_mu:.3e} eV ; sqrt(E_mu*M_Pl)={M_naive:.3e} eV = {M_naive/1e6:.3e} MeV")

print()
print("So the naive GC map mu=M^2/M_Pl gives M ~ 0.1-1 eV (NOT MeV) -- my earlier 'few MeV'")
print("comment was a formatting+order-of-mag error. Corrected.")
print()
# The PROPER GC IR scale: equate AeST mu^-1 to the GC Jeans length L_J ~ M_Pl/M^2.
# L_J = M_Pl/M^2 (natural units, length = 1/energy): in eV-length, L_J[m] = hbar c/(M^2/M_Pl)[eV]^-1
# Set L_J = mu^-1: M^2/M_Pl = hbar c / mu_inv_m  -> M = sqrt(M_Pl * hbar c / mu_inv_m)
print("Proper GC Jeans-length map L_J = M_Pl/M^2 set to AeST mu^-1:")
for mu_inv_Mpc in [0.1, 1.0, 10.0]:
    mu_inv_m=mu_inv_Mpc*Mpc
    E_mu=hbar*c/mu_inv_m/eV
    M = np.sqrt(M_Pl_eV*E_mu)    # same as naive (since L_J->mu and mu=M^2/M_Pl identical)
    print(f"  mu^-1={mu_inv_Mpc:5.1f} Mpc -> M = {M:.3e} eV")

print()
print("=> The GC SSB scale implied by AeST's Mpc clustering is M ~ 0.1-1 eV.")
print("   The GC energy-density scale (rho^(1/4)) is ~ 2 meV (dark-energy-class).")
print("   The canonical GC laboratory bound is M <~ 10 MeV (twinkling) -> framework's")
print("   implied M ~ 0.1-1 eV is WELL BELOW that bound (safe by ~7 orders) -- so the")
print("   GC pathology bound does NOT kill the framework's needed scale. GOOD (both-ways).")
print()
# Now the DECISIVE point: does any dS scale SET M ~ 0.1-1 eV ?
# dS energy scales available: hbar H_L ~ 1e-33 eV; rho_DE^1/4 ~ 2 meV; T_GH ~ 1e-34 eV.
E_HL = hbar*H_L/eV
print("dS energy scales: hbar*H_L = %.2e eV ; rho_DE^(1/4) = 2.24e-3 eV"%E_HL)
print("Needed GC scale M ~ 0.1-1 eV.")
print("  M / (rho_DE^1/4) ~ %.1f-%.0f  (M is ~50-500x the dark-energy scale)"%(0.1/2.24e-3, 1.0/2.24e-3))
print("  M / (hbar H_L)   ~ 1e32-1e33  (M is ~32 orders above the Hubble energy)")
print("  -> NO single dS scale equals M. The dS sector supplies ~meV (energy) and ~1e-33 eV")
print("     (Hubble); the clustering M~0.1-1 eV sits in BETWEEN, set by mu (a free Mpc scale).")
print("     The framework's OWN dimensionless ratio (mu^-1)/(c/H_L) ~ 2e-4 is the free input.")
