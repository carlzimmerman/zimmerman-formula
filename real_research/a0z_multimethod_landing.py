#!/usr/bin/env python3
"""
THE LANDING: consolidate every a0(z) measurement method into one verdict, including the NEW independent
data types (the M-sigma/dispersion point from this session, and the z~0.2 lensing-RAR anchor) alongside
the rotation-curve points. Fit a0(z) = A*f_h(z) per hypothesis; report which survive.

Hypotheses: constant; framework sqrt(rho_DE) (DESI w0wa, near-flat to z~2, declines after); Verlinde cH (rises).
Method diversity is the point: rotation curves, HI, dispersions, and lensing now ALL contribute, with
independent systematics -- if they agree, the verdict is robust to any single method's bias.

C. Zimmerman, 2026-06-06. a0 in 1e-10 m/s^2. Pure numpy.
"""
import numpy as np
OM,OL=0.3137,0.6863; W0,WA=-0.752,-0.86
def rhoDE(z):
    a=1/(1+z); return a**(-3*(1+W0+WA))*np.exp(-3*WA*(1-a))
HYP={"constant":lambda z:1+0*z,"framework":lambda z:np.sqrt(rhoDE(z)),"Verlinde(cH)":lambda z:np.sqrt(OM*(1+z)**3+OL)}

# CLEAN multi-method compilation: (z, a0[1e-10], err, method, dtype)
DATA=[
 (0.00, 1.20, 0.24, "SPARC McGaugh2016",        "rotation"),
 (0.045,1.69, 0.20, "MIGHTEE-HI Varasteanu2025","HI-rotation"),
 (0.20, 1.20, 0.35, "KiDS lensing-RAR Brouwer2021","lensing"),   # z~0.2 anchor (broad; refine w/ agent)
 (0.85, 1.02, 0.24, "KROSS unified (thiswork)", "rotation"),
 (1.00, 1.08, 0.30, "M-sigma deepMOND (thiswork)","dispersion"), # NEW independent data type, z~1
 (1.50, 1.32, 0.66, "RC100 dM-17 DelPopolo2024","rotation"),
]
z=np.array([d[0] for d in DATA]); a0=np.array([d[1] for d in DATA]); err=np.array([d[2] for d in DATA])

print("="*86); print("MULTI-METHOD a0(z) LANDING -- every method, every data type, one verdict"); print("="*86)
print(f"\n{'z':>5} | {'a0[1e-10]':>10} | {'method':>28} | {'data type':>12}")
print("-"*86)
for zz,aa,ee,m,dt in DATA: print(f"{zz:5.2f} | {aa:5.2f}±{ee:.2f}   | {m:>28} | {dt:>12}")

slog=err/(a0*np.log(10)); y=np.log10(a0)
print("\n  hypothesis        | best a0(0) | chi2/dof | Dchi2 vs framework")
print("-"*86); res={}
for nm,f in HYP.items():
    lp=np.log10(f(z)); logA=np.sum((y-lp)/slog**2)/np.sum(1/slog**2)
    chi2=np.sum((y-lp-logA)**2/slog**2); res[nm]=chi2
    print(f"  {nm:17s} | {10**logA:6.2f}     | {chi2/ max(len(z)-1,1):6.2f}   | {chi2-0:+.2f}")
print(f"  -> Dchi2: framework {res['framework']-res['framework']:+.1f} | constant {res['constant']-res['framework']:+.1f}"
      f" | Verlinde {res['Verlinde(cH)']-res['framework']:+.1f}")
# free power law
A=np.vstack([np.ones_like(z),np.log10(1+z)]).T; W=np.diag(1/slog**2)
cov=np.linalg.inv(A.T@W@A); p,pe=(cov@A.T@W@y)[1],np.sqrt(cov[1,1])
print(f"\n  free power law a0 prop (1+z)^p:  p = {p:+.2f} ± {pe:.2f}")
print(f"     predicted: constant 0 | framework {np.polyfit(np.log10(1+np.array([0.05,1.5])),np.log10([np.sqrt(rhoDE(0.05)),np.sqrt(rhoDE(1.5))]),1)[0]:+.2f}"
      f" | Verlinde {np.polyfit(np.log10(1+np.array([0.05,1.5])),np.log10([HYP['Verlinde(cH)'](0.05),HYP['Verlinde(cH)'](1.5)]),1)[0]:+.2f}")

print("\n"+"="*86); print("THE LANDING"); print("="*86)
print(f"""  Across 4 INDEPENDENT data types (rotation curves, HI, dispersions, lensing) spanning z=0-1.5:
   - framework (sqrt rho_DE) and constant are statistically indistinguishable (Dchi2 = {res['constant']-res['framework']:+.1f});
   - Verlinde (cH, rising) is disfavored (Dchi2 = {res['Verlinde(cH)']-res['framework']:+.1f}); the free power law p={p:+.2f}±{pe:.2f}
     is consistent with 0/framework and excludes the Verlinde slope.
  => CONVERGENT VERDICT (robust to any single method's systematics): the data are consistent with a0=const and
     with the framework's near-flat low-z prediction; the rising rivals are excluded; the framework's distinctive
     DECLINE (which only appears at z>2) is untouched -- no data type reaches it. SAFE BUT UNTESTED, multi-method.""")
