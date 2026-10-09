# Look-elsewhere for Brannen's delta = 2/9. delta lives in the fundamental domain [0, pi/3] (Z3 shift + reflection).
# Data precision on delta without assuming Koide: sigma ~ 1.9e-6 (Brannen eq 15, tau-limited). Hit window: |delta - target| <= 2 sigma.
import numpy as np
from fractions import Fraction as F
lo,hi=0.0,np.pi/3; w=2*1.9e-6
def frac_targets(qmax):
    return sorted({float(F(p,q)) for q in range(1,qmax+1) for p in range(0,int(hi*q)+1) if lo<=p/q<=hi})
def pi_targets(qmax):
    return sorted({float(F(p,q))*np.pi for q in range(1,qmax+1) for p in range(0,q+1) if lo<=p/q*np.pi<=hi})
for qmax in (9,12,20):
    T=frac_targets(qmax)+pi_targets(qmax)
    # prob a uniform delta lands within w of some target (union of windows)
    cover=sum(min(t+w,hi)-max(t-w,lo) for t in T)/(hi-lo)
    print(f"targets p/q and (p/q)pi, q<={qmax}: {len(T)} targets, chance hit = {cover:.2e}  (1 in {1/cover:,.0f})")
print("observed |delta - 2/9| (Koide-free, Brannen eq15) ~ 2e-7 inside sigma 1.9e-6")
