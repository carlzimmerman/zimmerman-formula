#!/usr/bin/env python3
"""Milgrom linear/time-nonlocal no-EFE MOND (arXiv:2503.07106) -- wide-binary gamma.

Paper facts used (verbatim eq refs):
  Eq(8/9):  linear DML EoM d^4r/dt^4 = grad(psi), psi = -(A0/2) int rho/|r-r'|^2
  Eq(19-20): COM decouples EXACTLY from internal dynamics -> ZERO EFE (linearity)
  Eq(29):   two-body circular V12^4 = M*A0            (linear, beta=1; mass-ratio FREE)
  Eq(56):   beta-family  V12^4 = M*A0*[mu1^(1/(2b-1))+mu2^(1/(2b-1))]^(2b-1)
  Eq(31):   beta=3/2 (pure MI): V12^4 = (mu1^.5+mu2^.5)^2 M*A0
  Eq(30):   AQUAL/QUMOND-class isolated DML: V12^4 = (4/9)[(1-mu1^1.5-mu2^1.5)/(mu1 mu2)]^2 M*A0
Pure-DML models: NO Newtonian limit (Sec IV). Bridge for 2-30 kAU: quadrature
V^4 = V_N^4 + C*M*A0  ->  gamma=(1+C/y)^(1/4), y=g_N/a0. For C=1 this is EXACTLY
the framework's own nu(y)=sqrt(1+1/y) isolated curve -- fair shared interpolation.
Strict-DML (no bridge): gamma=(C/y)^(1/4)  [shown for honesty; <1 at y>C].
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kAU=1.496e14
M=1.5*Msun  # typical WB total mass
forks={'a0=9.36e-11 (canonical)':9.36e-11,'a0=1.13e-10 (fork)':1.13e-10,'a0=1.2e-10 (Milgrom std)':1.2e-10}
seps=np.array([2,5,10,15,20,30])  # kAU

def C_beta(b,mu1,mu2):
    e=1/(2*b-1); return (mu1**e+mu2**e)**(2*b-1)
def C_aqual(mu1,mu2):
    return (4/9)*((1-mu1**1.5-mu2**1.5)/(mu1*mu2))**2

mu=(0.5,0.5)
C_lin=C_beta(1,*mu)            # =1 exactly, ANY mass ratio (Eq29)
C_mi =C_beta(1.5,*mu)          # =2 equal masses (Eq31)
C_aq =C_aqual(*mu)             # isolated AQUAL-class DML coeff
print(f"DML two-body coeffs C (V^4=C*M*A0), equal masses: linear={C_lin:.3f}  MI(b=3/2)={C_mi:.3f}  AQUAL-iso={C_aq:.3f}")
print(f"  mass-ratio q=0.5 check: linear={C_beta(1,2/3,1/3):.3f}  MI={C_beta(1.5,2/3,1/3):.3f}  AQUAL-iso={C_aqual(2/3,1/3):.3f}")
print(f"  beta->2 limit, eq masses: C={C_beta(1.999,.5,.5):.3f}")

for name,a0 in forks.items():
    print(f"\n=== {name}, M_tot=1.5 Msun ===")
    print(f"{'s(kAU)':>7} {'g_N':>9} {'y':>6} | {'lin(bridge)':>11} {'lin(strict)':>11} {'MI b=3/2':>9} {'iso-nu(fw)':>10}")
    for s in seps:
        gN=G*M/(s*kAU)**2; y=gN/a0
        g_lb=(1+C_lin/y)**.25   # linear, quadrature bridge
        g_ls=(C_lin/y)**.25     # linear, strict DML
        g_mi=(1+C_mi/y)**.25    # beta=3/2 MI family, bridged
        g_fw=(1+1/y)**.25       # framework nu isolated (== lin bridge; shown as anchor)
        print(f"{s:>7} {gN:>9.2e} {y:>6.3f} | {g_lb:>11.3f} {g_ls:>11.3f} {g_mi:>9.3f} {g_fw:>10.3f}")

# external field irrelevance check (linear model): Eq(19-20) exact -> suppression factor = 1 identically
print("\nEFE in linear model: COM eq(20) exact for ANY external field -> gamma unsuppressed (suppression=1.000)")
print("Galactic g_ext=1.9e-10 = {:.2f} a0(canonical): dominates y at s>10kAU in EFE theories -> their plateau ~1.14 (MG) / 1.05-1.10 (framework MI-EFE)".format(1.9e-10/9.36e-11))
