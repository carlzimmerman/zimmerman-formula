#!/usr/bin/env python3
"""
ROUTE B decisive: is the small-1/mu core-mass enhancement a ROBUST closure or a
fine-tuned, sign-indefinite OSCILLATION artifact?

Using the VALIDATED point-source Hamiltonian machinery (reproduces Durakovic-
Skordis Figs 5-7: M/M~1.3 core, runaway in outskirts), scan 1/mu FINELY in the
0.05-0.6 Mpc band where r_C reaches the 420 kpc cluster core, and read off the
apparent core mass M(<420kpc)/M_bar_core. Both ways:
  - if M(<420)/M_bar settles at a STABLE ~4.4x across the band -> field closure WINS.
  - if it swings wildly / goes negative (antigravity) as 1/mu varies by small
    factors -> the "closure" is an oscillation node landing, NOT physics.

We also check: for the cluster, where does the FIRST oscillation MAXIMUM of the
apparent mass sit, and is the core ever robustly at a maximum?
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1000*kpc; a0=9.36e-11

def Mfun(x):
    x=np.abs(x); s=np.sqrt(1+4*x); return (-1+s)/(1+s)
def x_of_zt(zt):
    if zt<=0: return 0.0
    f=lambda x: x*Mfun(x)-zt
    hi=max(2*zt,2*np.sqrt(zt),1e-8)
    while f(hi)<0: hi*=2
    return brentq(f,0,hi,xtol=1e-14,rtol=1e-12)

def aest_pointsource_Mprofile(Mpt, inv_mu, r_in=2*kpc, r_out=3*Mpc, N=4000):
    """Validated point-source AeST. Returns r (Mpc), M_apparent/Mpt."""
    rM=np.sqrt(G*Mpt/a0); mu2=(1/inv_mu)**2
    r0=r_in; gN0=G*Mpt/r0**2; g0=gN0*(0.5+np.sqrt(0.25+a0/gN0))
    P0=r0**2*Mfun(g0/a0)*g0; Phi0=-g0*r0
    def rhs(r,y):
        Ph,Pp=y; x=x_of_zt(abs(Pp)/(a0*r*r))
        Phip=np.sign(Pp)*a0*x if Pp!=0 else a0*x
        return [Phip, -mu2*r**2*Ph]
    rg=np.logspace(np.log10(r0),np.log10(r_out),N); rg[0]=r0; rg[-1]=r_out
    sol=solve_ivp(rhs,[r0,r_out],[Phi0,P0],t_eval=rg,method='Radau',
                  rtol=1e-9,atol=1e-25,max_step=3*kpc)
    if not sol.success: return None,None
    r=sol.t; Pp=sol.y[1]
    Phip=np.array([np.sign(Pp[i])*a0*x_of_zt(abs(Pp[i])/(a0*r[i]**2)) for i in range(len(r))])
    return r, r**2*Phip/G/Mpt   # M_apparent/Mpt (signed)

if __name__=="__main__":
    print("="*72)
    print("ROUTE B: is small-1/mu core enhancement robust or an oscillation artifact?")
    print("="*72)
    # Represent the cluster core baryons as a compact point of M~core baryon mass
    # within 420 kpc PLUS the surrounding; use the full baryon mass as the source
    # scale. For the apparent-mass-at-core question, use Mpt = M_bar(<420kpc) for
    # the inner part but the enhancement depends on total -> use M500 scale.
    Mpt=1e15*Msun*0.13   # ~ gas mass scale (the MOND source)
    R_core=420*kpc
    # target ratio: M_total(<420) / M_bar(<420). M_bar_core~2.9e13, target 2.3e14
    target_ratio=2.30e14/2.937e13
    print("Cluster: need M_apparent(<420kpc)/M_bar_core ~ %.2f (the ~4.4x undershoot)\n"%target_ratio)
    print("Fine 1/mu scan in the core-reaching band (point-source, M_src=%.2e Msun):"%(Mpt/Msun))
    print("%-12s %16s %12s"%("1/mu[Mpc]","M_app(<420)/M_src","sign"))
    vals=[]
    for inv_mu in np.array([0.05,0.08,0.10,0.12,0.15,0.20,0.25,0.30,0.40,0.50,0.60])*Mpc:
        r,Mrat=aest_pointsource_Mprofile(Mpt,inv_mu)
        if r is None:
            print("%-12.3f %16s"%(inv_mu/Mpc,"(integ fail=osc)")); vals.append(np.nan); continue
        i=min(max(np.searchsorted(r,R_core),1),len(r)-1)
        m=Mrat[i]; vals.append(m)
        print("%-12.3f %16.3f %12s"%(inv_mu/Mpc, m, "ATTRACT" if m>0 else "ANTIGRAV"))
    vals=np.array(vals); fin=vals[np.isfinite(vals)]
    print("\nAcross the band: min=%.2f max=%.2f  swing factor=%.1fx, sign flips=%d"%(
        np.nanmin(vals), np.nanmax(vals), np.nanmax(vals)/max(np.nanmin(np.abs(fin[fin!=0])),1e-9),
        int(np.sum(np.diff(np.sign(fin))!=0))))
    print("\nIf the apparent core mass swings by large factors / flips sign as 1/mu")
    print("varies by <2x, the 'closure' is an oscillation-node coincidence, NOT a")
    print("robust field-sector mass source. A real closure would be stable.")
