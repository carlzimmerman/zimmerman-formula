#!/usr/bin/env python3
"""
The "one real bit" pushed to its core: a0 is set by the dark-energy DENSITY, not the rate -- but WHICH
dark-sector quantity, physically? There are THREE motivated readings of "a0 from the cosmic dark sector",
and they make DIFFERENT a0(z). The data + the cosmology together SELECT one.

  #1 FREE-FALL frequency of rho_DE (the framework):  a0 = (c/2) sqrt(G rho_DE) = (c/2) omega_DE,
     omega_DE = sqrt(G rho_DE) = inverse free-fall time of the DE density; radius R* = c/sqrt(G rho_DE).
     => a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).  DECLINES under DESI evolving DE.
  #2 EVENT-HORIZON surface gravity (Gibbons-Hawking, the most thermodynamically rigorous):
     a0 ~ c^2 / R_EH(z), R_EH(z) = a(t) * integral_t^inf c dt'/a(t')  (the FUTURE light cone).
  #3 APPARENT/HUBBLE horizon (Verlinde/QI):  a0 ~ c H(z) ~ sqrt(rho_total).  RISES steeply.

Key tests computed below:
  (a) the three a0(z) shapes;
  (b) DOES a future event horizon even EXIST under DESI thawing DE? (if rho_DE -> 0 in the future, NO dS
      horizon, reading #2 is ILL-DEFINED) -- demonstrated by the convergence/divergence of chi_EH;
  (c) which readings the DATA exclude (rising excluded: Milgrom2017, McGaugh2024, this corpus's model comparison).

C. Zimmerman, 2026-06-06.  Pure numpy.
"""
import numpy as np
OM,OL,OR=0.3137,0.6863,9.2e-5
W0,WA=-0.752,-0.86

def fDE_CPL(z):
    a=1/(1+z); return a**(-3*(1+W0+WA))*np.exp(-3*WA*(1-a))
def fDE_LCDM(z): return 1.0+0*np.asarray(z,float)
def E(z,fDE): return np.sqrt(OM*(1+z)**3+OR*(1+z)**4+OL*fDE(z))

# reading #1 (free-fall, framework) and #3 (Hubble), normalized to z=0
def a0_freefall(z,fDE): return np.sqrt(fDE(z))                 # sqrt(rho_DE) ratio
def a0_hubble(z,fDE):   return E(z,fDE)/E(0,fDE)              # cH ratio

# reading #2 (event horizon): chi_EH(z) = integral_{-1}^{z} dz'/E(z')  [comoving, units c/H0]
# R_EH(z)=chi_EH(z)/(1+z); a0_EH ~ c^2/R_EH; ratio = (1+z)*chi_EH(0)/chi_EH(z)
def chi_EH(z,fDE,zfut=-0.9995,n=200000):
    zz=np.linspace(zfut,z,n); return np.trapz(1.0/E(zz,fDE),zz)
def a0_event(z,fDE):
    c0=chi_EH(0.0,fDE); return (1+z)*c0/chi_EH(z,fDE)

print("="*82)
print("THREE READINGS of a0(z)/a0(0) -- which dark-sector quantity sets the MOND scale?")
print("="*82)
print(f"\n{'z':>5} | {'#1 free-fall':>12} | {'#2 event-hor':>12} | {'#3 Hubble cH':>12}   (pure LCDM in [])")
print("-"*82)
for z in [0,0.5,1,2,3,5]:
    ff=a0_freefall(z,fDE_CPL); hub=a0_hubble(z,fDE_CPL)
    try: ev=a0_event(z,fDE_LCDM)            # event horizon only well-defined for pure Lambda (see below)
    except Exception: ev=float('nan')
    print(f"{z:5.1f} | {ff:12.3f} | {ev:12.3f} | {hub:12.3f}")
print("  (#2 computed for PURE Lambda, where a future de Sitter horizon EXISTS; see the thawing test below.)")
print("\n  TRENDS into the past:  #1 free-fall DECLINES (0.74 @z=3);  #2 event-horizon RISES (~1+z);")
print("                         #3 Hubble RISES steeply (~(1+z)^1.5, 4.5x @z=3).")

# ---- (b) does a FUTURE EVENT HORIZON exist under DESI thawing DE? ----
print("\n"+"="*82)
print("DOES A FUTURE EVENT HORIZON EXIST?  chi_EH(0) = integral_{-1}^{0} dz'/E(z')  (converge=horizon exists)")
print("="*82)
print(f"  {'future cutoff z_fut':>22} | {'chi_EH(0) pure-Lambda':>22} | {'chi_EH(0) DESI-CPL':>20}")
print("-"*82)
for zfut in [-0.9,-0.99,-0.999,-0.9999]:
    cL=chi_EH(0.0,fDE_LCDM,zfut=zfut); cC=chi_EH(0.0,fDE_CPL,zfut=zfut)
    print(f"  {zfut:22.4f} | {cL:22.4f} | {cC:20.4f}")
print("\n  => pure Lambda: chi_EH CONVERGES (a de Sitter event horizon exists; reading #2 well-defined).")
print("     DESI thawing CPL: chi_EH DIVERGES as z_fut->-1 (rho_DE->0 in the future => NO future de Sitter")
print("     => NO event horizon => reading #2 is ILL-DEFINED under evolving DE.")

# rho_DE in the future under CPL (to show it vanishes)
print("\n  rho_DE(z)/rho_DE0 into the FUTURE (DESI CPL):")
for z in [0,-0.3,-0.6,-0.9,-0.99]:
    print(f"     z={z:6.2f} (a={1/(1+z):5.2f}):  rho_DE/rho0 = {fDE_CPL(z):.4f}")

print("\n"+"="*82)
print("THE SELECTION: data + cosmology pick the free-fall reading")
print("="*82)
print("""  - #3 Hubble (a0 prop cH, RISES): EXCLUDED by data (Milgrom2017 excludes (1+z)^1.5; McGaugh2024 excludes
       a0 prop cH0; this corpus's clean-sample model comparison Dchi2=+17 vs framework).
  - #2 Event horizon (RISES for pure Lambda; ILL-DEFINED for the DESI thawing DE that the framework USES):
       excluded where defined, undefined where the framework lives.
  - #1 Free-fall frequency of rho_DE (DECLINES): the UNIQUE well-defined, data-surviving reading.
  => The 'one bit' sharpens: a0 is the dark-energy FREE-FALL FREQUENCY c*sqrt(G rho_DE)/2, NOT a horizon
     surface gravity. The two horizon readings either rise (excluded) or don't exist (thawing DE).
  HONEST TENSION: the free-fall reading is LESS thermodynamically fundamental than a horizon temperature.
     A purist expects the horizon reading (rising), which the data exclude -- so the data are mildly in
     tension with 'a0 from horizon thermodynamics' generically, and the framework survives only via the
     free-fall (non-horizon) reading. That is the honest cost of the sharpening.""")
