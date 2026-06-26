#!/usr/bin/env python3
"""
PART F-H: the decisive questions.
 F. Does the non-equ drive SET the scale a0 = (active-kernel amplitude), and is that
    amplitude the DECLINING sqrt(rho_DE) branch or the total-horizon cH(z)?
 G. Does the drive magnitude FIX kappa (=1/2) or the a0/cH_Lambda ratio?
 H. Numerical a0(z) on the non-equ reading vs the framework declining branch vs rising rival.
Both ways. Honest about every inserted vs derived step.
"""
import numpy as np
C=2.99792458e8; MPC=3.0857e22; H0=67.4e3/MPC; G=6.674e-11
Z=2*np.sqrt(8*np.pi/3); Om,OL=0.315,0.685
def make_bg(w0,wa):
    def rhoDE(z): a=1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
    def Hsq(z): return Om*(1+z)**3 + OL*rhoDE(z)
    def H(z):   return np.sqrt(Hsq(z))
    def HDE(z): return np.sqrt(OL*rhoDE(z))
    def w(z):   return w0+wa*z/(1+z)
    def q(z):   weff=w(z)*OL*rhoDE(z)/Hsq(z); return 0.5*(1+3*weff)
    return rhoDE,Hsq,H,HDE,w,q
CPL=make_bg(-0.752,-0.86); LAM=make_bg(-1.0,0.0)

print("="*88)
print("PART F. What scale does the active amplitude set?  (active = -eps*T from Part D)")
print("="*88)
print("""  From Part D, the active (negative-residue, deep-MOND DC) amplitude is
        A_active(z) = eps_KMS(z) * T_dS(z),   T_dS = H_bath/2pi,
  i.e. the PRODUCT of the drive size and the bath temperature. The candidate a0 is
        a0_neq(z) ~ c * A_active(z) / (geometric factor).
  Question: is A_active the DECLINING sqrt(rho_DE) branch?  Test BOTH bath choices:
    (i)  bath = total horizon:    T=H(z)/2pi,    eps=|1+q(z)|    -> A = |1+q| H(z)
    (ii) bath = dark-energy only: T=H_DE(z)/2pi, eps=(3/2)|1+w| -> A = (3/2)|1+w| H_DE(z)""")
print(f"  {'z':>5}{'H(z)':>8}{'H_DE':>8}{'A_tot=|1+q|H':>14}{'A_DE=(3/2)|1+w|H_DE':>20}{'sqrt(rhoDE)=H_DE':>16}")
rhoDE,Hsq,H,HDE,w,q=CPL
for z in [0,0.5,1,2,3,5]:
    Atot=abs(1+q(z))*H(z); ADE=1.5*abs(1+w(z))*HDE(z)
    print(f"  {z:>5.1f}{H(z):>8.3f}{HDE(z):>8.3f}{Atot:>14.3f}{ADE:>20.3f}{HDE(z):>16.3f}")
print("""  READING: NEITHER product reproduces the clean declining sqrt(rho_DE)=H_DE branch.
   - A_tot rises (tracks H, ~ the RISING rival, not the declining branch);
   - A_DE = (3/2)|1+w| H_DE is the declining H_DE MODULATED by the drive |1+w| -- it is
     NOT proportional to H_DE alone, and |1+w| is small near z~0.3 (w crosses -1) so A_DE
     DIPS there, unlike any monotone branch. => the drive-amplitude does NOT equal the
     posited declining a0(z); it is a DIFFERENT function. The declining branch is recovered
     ONLY if one DROPS the eps factor (i.e. sets a0 ~ T_DE, not eps*T_DE) -- but dropping
     eps is exactly re-positing the equilibrium (passive) scale, which has NO active sign.""")
print()

print("="*88)
print("PART G. Does the drive magnitude FIX kappa (=1/2) or the a0/cH_Lambda ratio?")
print("="*88)
# The framework: a0 = kappa * c * H_DE / sqrt(8pi/3)  with kappa=1/2 the lone free O(1).
# Non-equ claim to test: kappa is fixed by the drive size at the relevant epoch.
# Evaluate eps_KMS and (3/2)|1+w| TODAY and ask if either equals 1/2 or pins Z's 1/2.
for name,BG in [("CPL",CPL),("LAM",LAM)]:
    rhoDE,Hsq,H,HDE,w,q=BG
    print(f"  --- {name} today (z=0) ---")
    print(f"    eps_KMS(tot)=|1+q(0)|        = {abs(1+q(0)):.4f}")
    print(f"    eps_KMS_DE =(3/2)|1+w(0)|    = {1.5*abs(1+w(0)):.4f}")
    print(f"    Omega_Lambda(0)             = {OL*rhoDE(0)/Hsq(0):.4f}  (= -2q in pure dS-limit)")
print("""  None of these locks to 1/2 robustly: |1+q(0)| ~ 0.47 (LAM) is NEAR 1/2 but that is a
  COINCIDENCE of today's Omega_Lambda=0.685 (since in flat LCDM q0 = (1/2)Om - OL = -0.527,
  so 1+q0 = 0.473 = (3/2)Om ... = (3/2)*0.315). It equals (3/2)*Om_m, NOT a forced 1/2:
  it would be exactly 1/2 only if Om_m = 1/3. So the 'kappa=1/2' would be DERIVED only by
  ASSUMING Om_m=1/3 -- an unforced cosmic coincidence, not a theorem. The drive does NOT
  fix kappa.""")
qLAM=LAM[5]; print(f"   check: (3/2)*Om_m = {1.5*Om:.4f}  vs |1+q0|_LAM = {abs(1+qLAM(0)):.4f}  (equal).")
print()

print("="*88)
print("PART H. a0(z) numbers: non-equ active amplitude vs framework-declining vs rising")
print("="*88)
rhoDE,Hsq,H,HDE,w,q=CPL
a0_0=C*H0/Z
print(f"  normalizing all to a0(0). Framework declining = H_DE(z)/H_DE(0).")
print(f"  {'z':>5}{'FRAMEWORK decl':>16}{'RISING rival':>14}{'NEQ A_tot(norm)':>16}{'NEQ A_DE(norm)':>16}")
Atot0=abs(1+q(0))*H(0); ADE0=1.5*abs(1+w(0))*HDE(0)
for z in [0,0.5,1,2,3]:
    decl=HDE(z)/HDE(0); rise=H(z)/H(0)
    At=abs(1+q(z))*H(z)/Atot0; Ad=1.5*abs(1+w(z))*HDE(z)/ADE0
    print(f"  {z:>5.1f}{decl:>16.3f}{rise:>14.3f}{At:>16.3f}{Ad:>16.3f}")
print("""  The non-equ amplitudes are a THIRD and FOURTH curve, distinct from both the framework's
  declining branch AND the rising rival. So the non-equ drive does NOT reproduce the posited
  a0(z); it predicts its OWN (different) a0(z). That is falsifiable -- but it is NOT a
  derivation of the framework's branch.""")
