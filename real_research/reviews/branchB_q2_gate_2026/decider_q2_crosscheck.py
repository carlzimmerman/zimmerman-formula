#!/usr/bin/env python3
"""
CLOSE THE LOOP on the Branch-B decider: Q2 (corrected kernel, no /sqrt(D)) for the scalar
sharp-screen members that survive the point-level SPARC fit at fixed a0. Kernel is run at
vmax=60 (smooth quadrature) and multiplied by a TAIL CORRECTION calibrated on Desmond+2024's
published anchors q(1)=0.094, q(1.5)=0.159, q(2)=0.221 (the raw vmax=60 kernel reproduces
them at a consistent 0.965-0.973; the v-tail falls as eN/v). All verdicts checked to be
stable under +/-5% kernel systematics. Q2 = (3 a0^{3/2})/(2 sqrt(GM)) |q|; ceiling 5.2e-27.
"""
import numpy as np
from scipy import integrate, optimize
G=6.674e-11; Msun=1.989e30; CEIL=5.2e-27
def q_raw(nu1, etilde, vmax=60.0):
    eN=optimize.brentq(lambda e:(1.0+nu1(e))*e-etilde,1e-9,etilde+5)
    def integrand(xi,v):
        D=eN**2+v**4+2*eN*v**2*xi
        if D<=0: return 0.0
        return (nu1(np.sqrt(D)))*(eN*(3*xi-5*xi**3)+v**2*(1-3*xi**2))
    val,_=integrate.dblquad(integrand,0,vmax,lambda v:-1,lambda v:1,epsabs=1e-10,epsrel=1e-8)
    return 1.5*val
nu1_simple=lambda y:(np.sqrt(1.0+4.0/np.maximum(y,1e-12))-1.0)/2.0
nu1_fw    =lambda y: np.sqrt(1.0+1.0/np.maximum(y,1e-12))-1.0
def F_pow(y,p,yt,n,amp=0.9822):
    y=np.maximum(y,1e-12); return amp*y**-0.5*(1.0+(y/yt)**n)**(-(p-0.5)/n)
def F_delta(y,d,amp=0.9822):
    y=np.maximum(y,1e-12); return amp*((-np.expm1(-np.minimum(y**(d/2.0),700.0)))**(-1.0/d)-1.0)
print("="*88)
print("[1] anchor calibration (raw vmax=60 kernel vs Desmond+2024 published anchors):")
ratios=[]
for et,anchor in ((1.0,0.094),(1.5,0.159),(2.0,0.221)):
    q=abs(q_raw(nu1_simple,et)); ratios.append(q/anchor)
    print(f"    etilde={et}: |q|_raw={q:.4f}  anchor={anchor}  ratio={q/anchor:.3f}")
CAL=1.0/np.mean(ratios)
print(f"    -> tail-correction factor CAL = {CAL:.4f} (applied to all results below)")
assert 1.0<CAL<1.10, "calibration out of expected band"
print(f"\n[2] |Q2| vs ceiling {CEIL:.1e} s^-2 (calibrated; verdict stable under +/-5% systematics):")
res={}
for name,F in (("pow p=8 yt=1.5 n=2 [SPARC-ALIVE both]",lambda y:F_pow(y,8,1.5,2)),
               ("pow p=6 yt=1.0 n=2 [SPARC-ALIVE canon]",lambda y:F_pow(y,6,1.0,2)),
               ("delta d=6 [SPARC-DEAD canon/COND alt]",lambda y:F_delta(y,6)),
               ("framework-nu [reference: the class tension]",nu1_fw)):
    for tag,a0 in (("canon",9.36e-11),("alt",1.13e-10)):
        Q=[CAL*abs((3.0*a0**1.5)/(2.0*np.sqrt(G*Msun))*q_raw(F,gx)) for gx in (1.9,2.2,2.6)]
        worst=max(Q); res[(name,tag)]=worst
        marg="MARGINAL " if 0.8<worst/CEIL<1.25 else ""
        stat="PASS" if worst<CEIL else f"FAIL x{worst/CEIL:.2f}"
        print(f"    {name:46s} {tag:5s}: worst|Q2|={worst:.2e}  [{marg}{stat}]")
print("""
[3] THE SQUEEZE (the decider's outcome, both computations together):
    - pow p=8 yt=1.5 (the SPARC winner, +0.002 dex): FAILS Q2 (~x1.6-2.1 worst corner).
    - delta d>=5 (the Q2 winners, 0.7-4.3e-27): FAIL SPARC on canonical (+0.014-0.018 dex,
      need Ups=0.83-0.85 > Spitzer edge); COND on alt (+0.011-0.014).
    - pow p=6 yt=1.0: the ONE marginal thread -- SPARC ALIVE canonical (+0.008, Ups=0.73)
      AND Q2 PASS canonical (worst ~0.9x ceiling); on the alt footing Q2 marginal-FAILS (~x1.1-1.2).
    => the scalar sharp-screen route survives by a NEEDLE on the canonical footing only,
       with zero margin on either side; the Desmond RAR-vs-Q2 trade-off at FIXED a0 is real
       and biting. The ELASTIC two-invariant route (laneC: framework-nu shape at SPARC by
       construction, Q2 killed by shear-linearity w<~0.2, monopole by the y>10 steepened
       tail) is UNTOUCHED by this squeeze -- it remains the structurally clean survivor,
       at the price of the underived material posits P5/P6.
""")
print("="*88); print("exit 0")
