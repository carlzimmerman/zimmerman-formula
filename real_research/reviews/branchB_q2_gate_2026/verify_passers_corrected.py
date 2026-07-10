#!/usr/bin/env python3
"""Corrected Q2 (Milgrom 2009 eq 23, no /sqrt(D)) for the EXACT laneA passer sets,
parsed from laneA_output.txt. Prints corrected chi_max, ratio to laneA's value,
and the corrected best members. Also the near-boundary sensitivity: the y_t=0.5,n=2
canonical members killed only by d(6) in (-0.09,-0.05) -- the band the framework's own
nu violates at y=6 (V1: d(6)=-0.102)."""
import numpy as np, re
from scipy.optimize import brentq
from scipy import integrate
import warnings; warnings.filterwarnings("ignore")

G=6.674e-11; Msun=1.989e30; GM=G*Msun
Z=np.sqrt(32*np.pi/3.0); A=np.sqrt(Z/6.0)
A0_CANON=9.36e-11; A0_ALT=1.13e-10
Q2_CEIL=5.2e-27; GEXT=2.2e-10

def F_mem(y,p,yt,n): return A*y**-0.5*(1+(y/yt)**n)**(-(p-0.5)/n)
def solve_eN(F,et): return brentq(lambda e: e*(1+F(e))-et,1e-9,10*et,xtol=1e-15)
def Q2_corr(F,a0,gext,vmax=200.0):
    eN=solve_eN(F,gext/a0)
    def ig(xi,v):
        D=eN*eN+v**4+2*eN*v*v*xi
        return 0.0 if D<=1e-30 else F(np.sqrt(D))*(eN*(3*xi-5*xi**3)+v*v*(1-3*xi*xi))
    val,_=integrate.dblquad(ig,0,vmax,lambda v:-1,lambda v:1,epsabs=1e-12,epsrel=1e-9)
    return -(3.0*a0**1.5)/(2.0*np.sqrt(GM))*1.5*val

txt=open("laneA_output.txt").read()
def parse(block):
    rows=[]
    for ln in block.splitlines():
        m=re.match(r"\s+(\d\.\d\d)\s+(\d\.\d)\s+(\d)\s+([\d.]+)\s+([\d.e+-]+)\s+([\d.]+)\s+([\d.]+)",ln)
        if m:
            rows.append((float(m.group(1)),float(m.group(2)),int(m.group(3)),
                         float(m.group(5)),float(m.group(7))))  # p,yt,n,|Q2|lane,chimax lane
    return rows
blocks=txt.split("members passing SPARC+Saturn+deep")
canon=parse(blocks[1]); alt=parse(blocks[2])
print(f"parsed passers: canonical {len(canon)}, alt {len(alt)}")

for label,rows,a0 in [("CANONICAL",canon,A0_CANON),("ALT",alt,A0_ALT)]:
    print(f"\n [{label}] corrected Q2 for exact passers:")
    print(f"  {'p':>5}{'y_t':>5}{'n':>3}{'|Q2| lane':>11}{'|Q2| corr':>11}{'ratio':>7}"
          f"{'chi_max lane':>13}{'chi_max corr':>13}")
    out=[]
    for p,yt,n,Q2l,cml in rows:
        F=lambda y,p=p,yt=yt,n=n: F_mem(y,p,yt,n)
        Q2c=Q2_corr(F,a0,GEXT)
        cmc=min(1.0,Q2_CEIL/abs(Q2c))
        out.append((p,yt,n,Q2l,abs(Q2c),cml,cmc))
        print(f"  {p:>5.2f}{yt:>5.1f}{n:>3d}{Q2l:>11.2e}{abs(Q2c):>11.2e}{abs(Q2c)/Q2l:>7.2f}"
              f"{cml:>13.2f}{cmc:>13.3f}")
    best=max(out,key=lambda r:r[6])
    print(f"  => corrected best: p={best[0]}, y_t={best[1]}, n={best[2]}, chi_max={best[6]:.3f}"
          f" (lane said {best[5]:.2f} for this member)")
    print(f"  => corrected chi_max range over passers: {min(r[6] for r in out):.3f} - "
          f"{max(r[6] for r in out):.3f} (lane: {min(r[5] for r in out):.2f} - {max(r[5] for r in out):.2f})")

# strict-band best (lane: p=3.0, y_t=1.5, n=2 canonical) corrected:
Q2s=Q2_corr(lambda y:F_mem(y,3.0,1.5,2),A0_CANON,GEXT)
print(f"\n strict-band best (3.0,1.5,2) canonical: corrected chi_max={Q2_CEIL/abs(Q2s):.3f} (lane 0.21)")

# near-boundary sensitivity: members killed ONLY by d(6) in (-0.09,-0.05) at yt=0.5 canonical
print("\n SPARC-band sensitivity (canonical, members failing ONLY the loose d(6) band, "
      "|d6| <= 0.10 = the framework-nu's own y=6 residual):")
for p,yt,n,d6 in [(2.0,0.5,2,-0.070),(2.25,0.5,2,-0.068),(2.5,0.5,2,-0.079),(3.0,0.5,2,-0.090),
                  (2.0,0.5,4,-0.052),(2.25,0.5,4,-0.057),(2.5,0.5,4,-0.056),(3.0,0.5,4,-0.065)]:
    Q2c=Q2_corr(lambda y:F_mem(y,p,yt,n),A0_CANON,GEXT)
    cm=min(1.0,Q2_CEIL/abs(Q2c))
    tag=" PASSES chi=1" if abs(Q2c)<=Q2_CEIL else ""
    print(f"  p={p}, yt={yt}, n={n} (d6={d6:+.3f}): |Q2|corr={abs(Q2c):.2e}, chi_max={cm:.3f}{tag}")
print("\nEXIT 0")
