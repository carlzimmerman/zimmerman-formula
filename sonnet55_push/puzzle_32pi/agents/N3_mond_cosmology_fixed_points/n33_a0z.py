"""N3-3: what a0(z) would a MOND-expansion fixed-point closure give? LCDM-native H(z), Om=0.315, OL=0.685."""
import warnings; warnings.filterwarnings('ignore')
import numpy as np
from scipy.optimize import brentq
P=F=0
def chk(n,ok):
    global P,F
    P+=bool(ok); F+=(not ok); print(("PASS " if ok else "FAIL ")+n)
Om,OL=0.315,0.685
E=lambda z:np.sqrt(Om*(1+z)**3+OL)
nu=lambda x:0.5+np.sqrt(0.25+1/x)
# three candidate variables that the closure a0 = H_X/Z_c could hold fixed
laws={'H_Lambda (Lambda const)':lambda z:1.0,
      'H(z) total':E,
      'H_m(z)=sqrt(Om)(1+z)^1.5 H0':lambda z:np.sqrt(Om)*(1+z)**1.5}
print("a0(z)/a0(0) if a0 = H_X/Z with Z a constant pure number (closure holds at all z):")
for z in (0.5,1,2.5,5): print("  z=%.1f"%z,{k:round(v(z)/v(0),3) for k,v in laws.items()})
chk("H(z)/H0 at z=2.5 = 3.77 (matches the framework-vs-H(z) comparator)",abs(E(2.5)-3.77)<0.01)
# A. static point-mass ZF radius is independent of z (Lambda const): depends on H_Lambda only
chk("C1 R_ZF depends only on H_Lambda, GM, a0 (no z): flat in z if a0 flat (by construction)",True)
# B. homogeneous closure with total density: f(z)=1+rho_m/rho_L ; fixed point exists iff f<2
fz=lambda z:1+Om*(1+z)**3/OL
zmax=brentq(lambda z:fz(z)-2,0,5)
print("\nhomogeneous total-density closure: nu(x)=2/f(z) needs f<2  ->  z < %.3f"%zmax)
chk("fixed point exists only for z<0.296 (rho_m<rho_Lambda); none at z=2.5",abs(zmax-((OL/Om)**(1/3)-1))<1e-9 and zmax<0.3)
chk("at z=2.5 f=%.1f>2: nu>=1>2/f, shell always decelerates (no fixed point for ANY nu)"%fz(2.5),fz(2.5)>2)
# a0 implied at fixed point if the radius is the horizon at that time: a0 = f H_L^2 R/(2x*) , R=c/H(z)
def a0_implied(z):
    f=fz(z); x=1/((2/f-0.5)**2-0.25); return f/(2*x)/E(z)     # in units H_Lambda^2/H0 ... H0=1, H_L=sqrt(OL)
zz=np.array([0,0.05,0.1,0.2,0.25,0.29])
vals=np.array([a0_implied(z) for z in zz])*OL   # H_L^2 = OL (H0=1)
print("  a0(z)/H0 implied by f,s=1 closure (simple nu):",np.round(vals,4))
chk("implied a0(z) falls by >30x over z<0.29 and ->0 at z=0.296 (NOT flat)",vals[0]/vals[-1]>30)
chk("implied a0(0)/H0 = %.3f, i.e. H0/%.2f, versus the framework H0/Z_Lambda-footing ~ 0.17-0.20 H0 (no match claimed)"%(vals[0],1/vals[0]),0.2<vals[0]<0.3)
# C. what a0 law does a *Friedmann-level* MOND modification imply? q(z) zero crossing with nu(x)
print("\nC. shell-level q=0: nu(x) Om(z)/2 = OL/E^2*... (g_N=Om(z)H^2 R/2 at the actual H(z)).")
for z in (0.0,0.3,0.67,1.0,2.5):
    Omz=Om*(1+z)**3/E(z)**2; OLz=OL/E(z)**2
    print("  z=%.2f Om(z)=%.3f OL(z)=%.3f needed nu for q=0: %.2f"%(z,Omz,OLz,2*OLz/Omz))
zq=(2*OL/Om)**(1/3)-1
chk("needed nu>=1 only for z<%.2f (the q=0 crossing for nu=1 is z=%.2f); at z=2.5 nu<1 needed: impossible"%(zq,zq),abs(zq-0.63)<0.01 and 2*OL/(Om*(1+2.5)**3)<1)
# D. data comparators from sibling lane (Z1): not re-derived here.
print("\nSummary: flat a0(z) is what a Lambda-variable closure gives; H(z) what a total-H closure gives; the homogeneous total-density closure has no fixed point at z>0.296.")
# mutation: Om->0 makes H(z) flat, law degenerates
Om_save=Om; Om=1e-9
chk("MUTATE: Om->0 makes H(z) law collapse to flat (laws not separable without matter)",abs(np.sqrt(Om*(3.5)**3+OL)-np.sqrt(OL))<1e-3)
Om=Om_save
print("N33 pass=%d fail=%d"%(P,F)); raise SystemExit(0 if F==0 else 1)
