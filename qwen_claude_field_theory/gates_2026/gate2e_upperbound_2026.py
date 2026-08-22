#!/usr/bin/env python3
r"""gate2e -- the honest upper bound on the environmental exponent beta.

Profiles beta_M with Sigma, bulge and V_flat FREE, marginalised over a0, then inflates the
band by the permutation-measured calibration factor (the profile sigma was 2.23x too small).
This is the number that goes into the go/no-go inequality."""
import os,sys,json
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import gate2d_multivariate_2026 as M
import numpy as np
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
CAL=0.0780/0.0350          # permutation sd / profile sigma, measured in gate2c
X, Xs, best = M.X, M.Xs, M.best
sdM=X.std(0)[0]
grid=np.linspace(-0.30,0.30,41)         # in STANDARDISED units of ln M_bar
_,cF=best(Xs)
pr=[]
for v in grid:
    _,c=best(Xs,fixed=(0,float(v))); pr.append(c)
pr=np.array(pr); pr-=pr.min()
def band(th):
    o=grid[pr<=th]; return float(o.min()),float(o.max())
b1,b2=band(1.0),band(4.0)
info("A1  conditional profile on beta_M (standardised)",
     f"best {grid[np.argmin(pr)]:+.4f}   raw 1sig [{b1[0]:+.3f},{b1[1]:+.3f}]   "
     f"raw 2sig [{b2[0]:+.3f},{b2[1]:+.3f}]")
c=grid[np.argmin(pr)]
b2c=(c+(b2[0]-c)*CAL, c+(b2[1]-c)*CAL)
info("A2  calibration factor from permutations",f"{CAL:.2f}x  (profile sigma is too small)")
info("A3  CALIBRATED 2sigma on beta_M (standardised)",f"[{b2c[0]:+.3f}, {b2c[1]:+.3f}]")
# convert: beta_env = -2 * beta_M_raw ; beta_M_raw = beta_M_std / sd(ln M)
lo,hi=sorted([-2*b2c[0]/sdM, -2*b2c[1]/sdM])
info("A4  *** CALIBRATED 2sigma on beta_env = -2 beta_M ***",f"[{lo:+.4f}, {hi:+.4f}]")
info("A5  sd(ln M_bar) across the sample",f"{sdM:.3f}")
json.dump(dict(beta_env_2sig=[lo,hi],cal=CAL,sd_lnM=float(sdM),
               beta_M_std_best=float(c)),open("gate2e_result.json","w"),indent=1)
