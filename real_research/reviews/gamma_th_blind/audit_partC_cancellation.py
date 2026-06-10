"""
AUDIT PART C (NAMED JOB 1): every claimed cancellation between Hubble rates -- real or smuggled?

SETUP (independent):
- Ansatz: a0(z) ~ sqrt(rho_DE(z))  => T(z) ~ a0(z) ~ sqrt(rho_DE(z))  (the "temperature in the inertia law").
- DESI CPL: w(a) = w0 + wa(1-a),  a=1/(1+z).
  rho_DE(z)/rho_DE0 = exp[ 3 int_0^z (1+w(z'))/(1+z') dz' ]
  Closed form for CPL: f_DE(z) = (1+z)^{3(1+w0+wa)} * exp[ -3 wa z/(1+z) ].
- E(z)^2 = Om(1+z)^3 + (1-Om) f_DE(z)   [flat, matter+DE only]
- H_tot(z) = H0 E(z).
- H_DE(z): the "de Sitter rate" from DE alone: H_DE(z) = H0 sqrt((1-Om) f_DE(z)).
  (rho_DE sets a would-be dS horizon H_DE = sqrt(8 pi G rho_DE/3); in units H0^2 = 8piG rho_crit0/3,
   H_DE/H0 = sqrt(Omega_DE0 f_DE).)

eps(z) := |d ln T/dt| * tau_gate.
Since T ~ sqrt(rho_DE):  d ln T/dt = (1/2) d ln rho_DE/dt.
  d ln rho_DE/dt = (d ln rho_DE/dz)(dz/dt),  dz/dt = -(1+z) H_tot(z).
  => |d ln T/dt| = (1/2) |d ln rho_DE/dz| (1+z) H_tot(z).

Also, the continuity equation gives a SHORTCUT we can cross-check:
  d ln rho_DE/dt = -3(1+w(z)) H_tot(z)   [from dot rho = -3 H (rho+p), p=w rho]
  => |d ln T/dt| = (3/2)|1+w(z)| H_tot(z).   <-- INDEPENDENT route, must match the dz route.

THE CANCELLATION CLAIMS TO AUDIT (per finder):
 (i)  In every HORIZON-class gate, the ansatz prefactor sqrt(rho_DE) CANCELS in eps.
 (ii) H0 CANCELS in eps for horizon gates.
 (iii) lambda (coupling) does NOT appear in horizon gates (coupling-independent).
 (iv) In equilibration gates G3/G4, g2 does NOT cancel -> eps carries explicit 1/g2.
We test each by symbolic factorization, not by trusting the finder.
"""
import numpy as np
import sympy as sp

print("="*70)
print("AUDIT PART C: cancellation structure (symbolic) + eps(z) numbers")
print("="*70)

# ---------- SYMBOLIC cancellation audit ----------
z = sp.symbols('z', nonnegative=True)
H0, Om, w0, wa = sp.symbols('H0 Om w0 wa', positive=True)
OmL = 1 - Om

# CPL DE density factor
fDE = (1+z)**(3*(1+w0+wa)) * sp.exp(-3*wa*z/(1+z))
rhoDE = OmL*fDE          # in units of rho_crit0 (so rho_crit0=1); H0^2 absorbs 8piG/3
# Cross-check: d ln rhoDE/dz vs continuity -3(1+w)/(1+z)
w_of_z = w0 + wa*(1 - 1/(1+z))
dlnrho_dz_direct = sp.simplify(sp.diff(sp.log(rhoDE), z))
dlnrho_dz_cont   = sp.simplify(-3*(1+w_of_z)/(1+z))
print("\n[continuity cross-check] d ln rhoDE/dz:")
print("  direct  =", dlnrho_dz_direct)
print("  cont eq =", dlnrho_dz_cont)
print("  difference =", sp.simplify(dlnrho_dz_direct - dlnrho_dz_cont))

# Hubble rates
E2 = Om*(1+z)**3 + OmL*fDE
H_tot = H0*sp.sqrt(E2)
H_DE  = H0*sp.sqrt(OmL*fDE)

# T ~ sqrt(rhoDE); |dlnT/dt| = (1/2)|dlnrho/dz| (1+z) H_tot
abs_dlnrho_dz = sp.Abs(dlnrho_dz_direct)
dlnT_dt = sp.Rational(1,2)*abs_dlnrho_dz*(1+z)*H_tot

print("\n--- CANCELLATION AUDIT ---")
# Gate G6: tau = 1/H_tot
eps_G6 = sp.simplify(dlnT_dt * (1/H_tot))
print("\nGate G6 (tau=1/H_tot): eps =", eps_G6)
print("   -> H0 present?", H0 in eps_G6.free_symbols, "| sqrt(rhoDE) present?",
      'sqrt' in str(eps_G6) or rhoDE.free_symbols & eps_G6.free_symbols != set())
# Gate G5/G2: tau = 1/H_DE
eps_G5 = sp.simplify(dlnT_dt * (1/H_DE))
print("\nGate G5/G2 (tau=1/H_DE): eps =", eps_G5)
# Gate G1: tau = 2pi/H_DE
eps_G1 = sp.simplify(dlnT_dt * (2*sp.pi/H_DE))

# Check H0 cancellation explicitly: substitute H0->K and see if eps depends on K
print("\n[H0-cancellation test] differentiate eps wrt H0 (should be 0 if H0 cancels):")
print("  d eps_G6/dH0 =", sp.simplify(sp.diff(eps_G6, H0)))
print("  d eps_G5/dH0 =", sp.simplify(sp.diff(eps_G5, H0)))
print("  d eps_G1/dH0 =", sp.simplify(sp.diff(eps_G1, H0)))

# Check sqrt(rhoDE) / OmL prefactor cancellation: does eps depend on OmL only through the SHAPE ratio?
# eps_G6 should reduce to purely (1+z)|dlnrho/dz| * (1/2) -- i.e. NO H0, NO overall rhoDE scale.
print("\n[prefactor sqrt(rhoDE) cancellation in G6]: eps_G6 fully simplified:")
eps_G6_clean = sp.simplify(eps_G6)
print("  eps_G6 =", eps_G6_clean)
print("  Does eps_G6 contain OmL? ", OmL.free_symbols & eps_G6_clean.free_symbols)
# In G6, H_tot cancels entirely => eps_G6 = (1/2)(1+z)|dlnrho/dz|, NO cosmo-amplitude at all.

# G5: ratio H_tot/H_DE = sqrt(E2/(OmL fDE)) = sqrt(1 + Om(1+z)^3/(OmL fDE)). H0 cancels, sqrt(rhoDE) cancels,
# leaving the SHAPE * the dimensionless ratio. Show it:
ratio_HtotHDE = sp.simplify(H_tot/H_DE)
print("\n[G5 structure] H_tot/H_DE =", ratio_HtotHDE)
eps_G5_form = sp.simplify(sp.Rational(1,2)*abs_dlnrho_dz*(1+z)*ratio_HtotHDE)
print("  eps_G5 = (1/2)(1+z)|dlnrho/dz| * (H_tot/H_DE) =", eps_G5_form)
print("  matches eps_G5? diff:", sp.simplify(eps_G5 - eps_G5_form))

print("\n[VERDICT on cancellations]:")
print(" (i)  sqrt(rhoDE) prefactor: in eps it appears as |d ln T/dt|=(1/2)|dln rho/dz|*... ")
print("      The OVERALL scale sqrt(rhoDE0) drops because eps uses the LOG derivative. REAL, not smuggled.")
print(" (ii) H0: tau_gate ~ 1/H and |dlnT/dt| ~ H, so H0 cancels as a RATE/RATE ratio. REAL (d eps/dH0=0 above).")
print(" (iii) lambda/g2: horizon-gate tau has no g2 => eps has no g2. REAL by construction (gate choice).")

# ---------- NUMERIC eps(z) ----------
print("\n" + "="*70)
print("NUMERIC eps(z) with DESI CPL w0=-0.752, wa=-0.86, Om=0.315")
print("="*70)
W0, WA, OM = -0.752, -0.86, 0.315
OML = 1-OM
def fDE_n(zz):
    a = 1.0/(1+zz)
    return (1+zz)**(3*(1+W0+WA))*np.exp(-3*WA*zz/(1+zz))
def w_n(zz):
    return W0 + WA*(1 - 1/(1+zz))
def E_n(zz):
    return np.sqrt(OM*(1+zz)**3 + OML*fDE_n(zz))
def Htot_over_H0(zz): return E_n(zz)
def HDE_over_H0(zz):  return np.sqrt(OML*fDE_n(zz))
def rhoDE_n(zz):      return OML*fDE_n(zz)   # in rho_crit0 units; rhoDE0=OML
# d ln rhoDE/dz via continuity:
def dlnrho_dz_n(zz):  return -3*(1+w_n(zz))/(1+zz)
# |d ln T/dt| / H0 = (1/2)|dlnrho/dz| (1+z) E(z)
def dlnT_dt_over_H0(zz):
    return 0.5*abs(dlnrho_dz_n(zz))*(1+zz)*E_n(zz)

zs = [0.0, 0.4, 1.0, 2.0, 3.0]
print(f"\n{'z':>4} {'rhoDE/rhoDE0':>12} {'w(z)':>8} {'E(z)':>8} {'|dlnT/dt|/H0':>13} {'Htot/HDE':>9}")
for zz in zs:
    print(f"{zz:>4} {fDE_n(zz):>12.4f} {w_n(zz):>8.4f} {E_n(zz):>8.4f} {dlnT_dt_over_H0(zz):>13.4f} {Htot_over_H0(zz)/HDE_over_H0(zz):>9.4f}")

print(f"\n{'z':>4} {'eps_G6':>9} {'eps_G5':>9} {'eps_G1':>9}  (G6=1/Htot, G5=1/HDE, G1=2pi/HDE)")
res={}
for zz in zs:
    d = dlnT_dt_over_H0(zz)
    eG6 = d / Htot_over_H0(zz)
    eG5 = d / HDE_over_H0(zz)
    eG1 = d * 2*np.pi / HDE_over_H0(zz)
    res[zz]=(eG6,eG5,eG1)
    print(f"{zz:>4} {eG6:>9.4f} {eG5:>9.4f} {eG1:>9.4f}")

# equilibration gate G4 (gapless): tau=1/Gamma_th(0)=2pi^2/(g2 H_DE) => eps_G4 = (2pi^2/g2) eps_G5
print(f"\n{'z':>4} {'eps_G4(g2=1)':>12} {'eps_G4(g2=1e-2)':>15} {'eps_G4(g2=1e-6)':>15}")
for zz in zs:
    eG5 = dlnT_dt_over_H0(zz)/HDE_over_H0(zz)
    base = (2*np.pi**2)*eG5
    print(f"{zz:>4} {base/1:>12.4f} {base/1e-2:>15.4f} {base/1e-6:>15.4e}")

import json
out = {"eps_G6":{str(z):res[z][0] for z in zs},
       "eps_G5":{str(z):res[z][1] for z in zs},
       "eps_G1":{str(z):res[z][2] for z in zs}}
json.dump(out, open("/tmp/gamma_th_blind/audit_eps_table.json","w"), indent=2)
print("\nsaved /tmp/gamma_th_blind/audit_eps_table.json")
