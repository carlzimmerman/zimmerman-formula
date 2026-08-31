#!/usr/bin/env python3
"""
phase6_scan.py -- transition + parameter scan for FC-KH.

For each (beta,lambda) on alpha=2beta, sweep y0=a/a0 in [0.01,100] and record:
  A(kinetic), min/worst c_par^2 (deep physical band k>>a0, = c_par,UV^2),
  c_perp^2 (always), Jeans mass m^2, hyperbolicity.
Emit PARAMETER_SCAN.csv and PARAMETER_SCAN.json.

Decisive quantities (analytic, physical/sub-horizon k>>a0):
  A            = (1-beta)(2+beta+3lam)/(beta+lam)
  c_par,UV^2   = (4 - W2)(beta+lam) / [ W2 (1-beta)(2+beta+3lam) ]      W2=f''(y0)
  c_perp,UV^2  = (4 y0 - W1)(beta+lam) / [ W1 (1-beta)(2+beta+3lam) ]   W1=F'(y0)>0
  sign(c_par,UV^2) = sign(4-W2)/sign(W2) = sign(W2) = sign(f'')  (independent of beta,lambda)
"""
import numpy as np, json, csv

def Wprim(y): return 0.5*y*y+(1+y)*np.exp(-y)-1
def F(y,al):  return 2*y*y-2*(2-al)*Wprim(y)
def F1(y,al): return 2*y*(al+(2-al)*np.exp(-y))
def F2(y,al): return 2*al+2*(2-al)*(1-y)*np.exp(-y)

def A_kin(b,l):      return (1-b)*(2+b+3*l)/(b+l)
def cpar2_UV(y,b,l):
    al=2*b; W2=F2(y,al)
    return (4-W2)*(b+l)/(W2*(1-b)*(2+b+3*l))
def cperp2_UV(y,b,l):
    al=2*b; W1=F1(y,al)
    return (4*y-W1)*(b+l)/(W1*(1-b)*(2+b+3*l))
def mass2(y,b,l):
    al=2*b; W0,W1,W2=F(y,al),F1(y,al),F2(y,al)
    # m_eff^2 = V0/A ; V0 = -a0^2 y0 (W0 W1 + W0 W2 y0 - W1^2 y0)/(4 W0), a0=1
    V0=-1.0*y*(W0*W1+W0*W2*y-W1**2*y)/(4*W0)
    return V0/A_kin(b,l)

betas=[1e-18,1e-16,1e-15,1e-14,1e-13,1e-12]
lams =[1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1]
ys=np.concatenate([np.logspace(-2,np.log10(0.999),60),
                   np.linspace(1.0,3.0,200),
                   np.logspace(np.log10(3.01),2,120)])

rows=[]
print(f"{'beta':>10}{'lambda':>9}{'A(kin)':>13}{'min c_par^2':>14}{'@y0':>7}"
      f"{'min c_perp^2':>14}{'window f<0':>18}{'verdict':>10}")
for b in betas:
    for l in lams:
        A=A_kin(b,l)
        cpars=np.array([cpar2_UV(y,b,l) for y in ys])
        cperps=np.array([cperp2_UV(y,b,l) for y in ys])
        imin=np.argmin(cpars); ycrit=ys[imin]
        # instability window in y (f''<0): where cpar<0
        neg=ys[cpars<0]
        wlo,whi=(neg.min(),neg.max()) if neg.size else (None,None)
        verdict='UNSTABLE' if cpars.min()<0 else 'stable'
        rows.append(dict(beta=b,lam=l,A=A,min_cpar2=float(cpars.min()),y_at_min=float(ycrit),
                         min_cperp2=float(cperps.min()),
                         window_lo=(float(wlo) if wlo else None),
                         window_hi=(float(whi) if whi else None),verdict=verdict))
        print(f"{b:>10.0e}{l:>9.0e}{A:>13.4e}{cpars.min():>14.4e}{ycrit:>7.2f}"
              f"{cperps.min():>14.4e}{f'[{wlo:.3f},{whi:.2f}]' if wlo else 'none':>18}{verdict:>10}")

# write artifacts
with open('PARAMETER_SCAN.json','w') as f: json.dump(rows,f,indent=1)
with open('PARAMETER_SCAN.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# unavoidability summary
allneg=all(r['min_cpar2']<0 for r in rows)
print("\n"+"="*70)
print("UNAVOIDABILITY: min c_par^2 < 0 on EVERY grid point ?  ->", allneg)
print("worst overall min c_par^2 =", min(r['min_cpar2'] for r in rows))
# analytic sign proof
print("\nANALYTIC: sign(c_par,UV^2) = sign(4-W2)*sign(W2) with 4-W2>0 (W2<=4) always")
print("          => sign(c_par,UV^2) = sign(W2) = sign(f''),  INDEPENDENT of (beta,lambda).")
print("          f''(y)=2a+2(2-a)(1-y)e^-y < 0  for  1 < y < y* ,  y* solves (y-1)e^-y=a/(2-a).")
for b in betas:
    al=2*b
    # find y* upper edge of f''<0 window
    from scipy.optimize import brentq
    g=lambda y: F2(y,al)
    try:
        yhi=brentq(g,1.5,200); print(f"   beta={b:.0e}: f''<0 window = (1, {yhi:.2f})")
    except Exception:
        print(f"   beta={b:.0e}: upper edge not bracketed")

# growth timescale at worst point (order of magnitude), physical units
print("\nGrowth rate gamma=|omega|=sqrt|c_par^2| * k. Worst |c_par^2|~",
      f"{abs(min(r['min_cpar2'] for r in rows)):.2e}",
      "(near y0~2). For k~1/kpc: tau~kpc/(sqrt|c|*c) ~",
      "%.1e yr"%( (3.086e19/ (np.sqrt(0.005)*3e8) )/3.15e7 ))
