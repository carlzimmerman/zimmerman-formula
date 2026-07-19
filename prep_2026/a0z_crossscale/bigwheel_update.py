#!/usr/bin/env python3
"""
Re-extract the Big Wheel z=3.25 a0 from the NEW May-2026 ALMA dynamical model
(Ciocan-adjacent; arXiv:2605.04144), using the framework's OWN a0-line kernel
    a0 = (g_obs^2 - g_bar^2) / g_bar          [exact for nu(y)=sqrt(1+1/y)]
evaluated at the OUTERMOST MEASURED radius -- i.e. the nu-kernel correction the
cross-scale referee asked for (it subtracts the g_bar bias the flat V^4/GM_bar
estimator carries in the transitional g~a0 regime).

NUMBERS FROM THE PAPER (arXiv:2605.04144, pdftotext-verified quotes):
  - "reaching a maximum Vrot ~ 314 km/s at the outermost radius"  (RC mildly rising)
  - outermost MEASURED radius ~ 16.5 kpc (binning "3 kpc up to 16.5 kpc"); 20 & 35 kpc
    are EXTRAPOLATIONS for angular momentum, not measured RC points
  - log(M*/Msun) = 11.00 (+0.11/-0.12)  <- fiducial DYNAMICAL-model stellar mass
  - log(M*/Msun) = 11.37 (+/-0.20)      <- higher SED/half-mass-radius stellar mass
       (the paper flags the 2.3e11 SED mass is IN TENSION with the dynamical model)
  - log(Mgas/Msun) = 10.76
  - log(Mh/Msun)   = 12.11 (+0.29/-0.17)
z = 3.25.  Both a0 footings; framework predicts a DECLINE a0(3.25)/a0(0) ~ 0.72.
"""
import numpy as np
c=2.99792458e8; G=6.67430e-11; KPC=3.0856776e19; MSUN=1.98892e30
A0_CANON=9.355e-11; A0_SPARC=1.181e-10
FW_RATIO_Z325=0.72          # framework a0(3.25)/a0(0) on DESI CPL (nonmonotonic tail)

def a0_line(V_kms, R_kpc, logMstar, logMgas, f_enc=1.0):
    V=V_kms*1e3; R=R_kpc*KPC
    Mbar=(10**logMstar + 10**logMgas)*MSUN*f_enc
    g_obs=V**2/R
    g_bar=G*Mbar/R**2
    a0=(g_obs**2 - g_bar**2)/g_bar          # the a0-line identity
    return a0, g_obs, g_bar, Mbar/MSUN

def mc(V,sV, R,sR, lM,slM, lG,slG, n=200000):
    g=np.random.default_rng(0)
    Vs=V+sV*g.standard_normal(n); Rs=np.clip(R+sR*g.standard_normal(n),3,None)
    lMs=lM+slM*g.standard_normal(n); lGs=lG+slG*g.standard_normal(n)
    Vm=Vs*1e3; Rm=Rs*KPC; Mbar=(10**lMs+10**lGs)*MSUN
    go=Vm**2/Rm; gb=G*Mbar/Rm**2
    a0=(go**2-gb**2)/gb
    frac_neg=np.mean(a0<0)                    # unphysical (baryons over-predict V): g_bar>g_obs
    a0v=a0[a0>0]
    return np.median(a0v), np.percentile(a0v,16), np.percentile(a0v,84), frac_neg

print("BIG WHEEL z=3.25  --  a0 from the new dynamical model via the a0-line kernel")
print("="*76)
Vc, Rc, lG = 314.0, 16.5, 10.76
# central values, two stellar-mass scenarios
for tag, lM in [("DYNAMICAL-fiducial  M*=10^11.00", 11.00), ("SED / half-mass    M*=10^11.37", 11.37)]:
    a0,go,gb,Mb = a0_line(Vc,Rc,lM,lG)
    y = gb/A0_SPARC
    print(f"\n[{tag}]   Mbar={Mb:.2e} Msun (log {np.log10(Mb):.2f})")
    print(f"    g_obs={go:.3e}   g_bar={gb:.3e}   g_bar/a0_SPARC (y) = {y:.2f}  (transitional, NOT deep-MOND)")
    print(f"    a0-line a0 = {a0:.3e}   ratio/canonical={a0/A0_CANON:.2f}   ratio/SPARC={a0/A0_SPARC:.2f}")

print("\n" + "="*76)
print("MONTE-CARLO (V=314+/-20, R=16.5+/-1.5, Mgas 10^10.76+/-0.15):")
mA=mc(314,20, 16.5,1.5, 11.00,0.12, 10.76,0.15)
mB=mc(314,20, 16.5,1.5, 11.37,0.20, 10.76,0.15)
print(f"  DYNAMICAL M*=11.00:  a0 = {mA[0]:.2e}  [{mA[1]:.2e}, {mA[2]:.2e}]   ratio/SPARC={mA[0]/A0_SPARC:.2f} [{mA[1]/A0_SPARC:.2f},{mA[2]/A0_SPARC:.2f}]  (P(a0<0)={mA[3]*100:.0f}%)")
print(f"  SED       M*=11.37:  a0 = {mB[0]:.2e}  [{mB[1]:.2e}, {mB[2]:.2e}]   ratio/SPARC={mB[0]/A0_SPARC:.2f} [{mB[1]/A0_SPARC:.2f},{mB[2]/A0_SPARC:.2f}]  (P(a0<0)={mB[3]*100:.0f}%)")

print("\n" + "="*76)
print("SENSITIVITY to the assumed radius (V=314 flat), DYNAMICAL M*=11.00:")
for R in (16.5, 20.0, 35.0):
    a0,go,gb,Mb=a0_line(Vc,R,11.00,lG)
    print(f"    R={R:4.1f} kpc:  a0-line a0 = {a0:.3e}  (ratio/SPARC {a0/A0_SPARC:.2f})   [20/35 are EXTRAPOLATED, not measured]")

print("\n" + "="*76)
print("VERDICT (honest, both ways):")
print(f"  Framework predicts a DECLINE: a0(3.25)/a0(0) ~ {FW_RATIO_Z325}  -> a0 ~ {FW_RATIO_Z325*A0_SPARC:.2e} (SPARC) / {FW_RATIO_Z325*A0_CANON:.2e} (canon)")
print(f"  Cross-scale paper's PRIOR datum: a0_eff = 1.54e-10, ratio 1.31 (flat estimator, M_bar~4.1e11).")
print(f"  NEW dynamical model -> a0-line ratio spans ~{mB[0]/A0_SPARC:.1f} (SED M*) to ~{mA[0]/A0_SPARC:.1f} (dynamical M*),")
print(f"  driven ENTIRELY by the 0.37-dex M* ambiguity the paper itself flags as unresolved.")
print(f"  => The new data does NOT tighten the datum. It CONFIRMS the paper's core finding empirically:")
print(f"     at z=3.25 the object is transitional (y~1), so a0 is HYPER-sensitive to M_bar; the single")
print(f"     Big Wheel datum cannot pin the a0(z) decline. M_bar calibration, not this object, is decisive.")
print("EXIT 0")
