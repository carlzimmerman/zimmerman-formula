#!/usr/bin/env python3
"""
ROUTE B galaxy veto on REAL SPARC: if 1/mu is pushed small enough for the AeST
mu^2*Phi enhancement to reach the cluster CORE (1/mu <~ 0.3 Mpc), does that same
screening length distort SPARC galaxy rotation curves beyond the floor?

For each SPARC galaxy: M_bar = Ups*L36 + 1.33*MHI (1.33 for He). The MOND RC at
the flat part is V_f = (G M_bar a0)^(1/4). The AeST mu^2*Phi term adds a
modified-Helmholtz correction that, at the galaxy's outer radius R_out ~ a few
disk scale lengths, perturbs the potential by ~ (R_out/(1/mu))^2 at leading
order (the term mu^2*Phi vs the Laplacian). We compute the AeST RC via the same
validated Hamiltonian integration and report the fractional |dV/V| at R_out.

Veto metric: median |dV/V| and fraction of galaxies with |dV/V|>10% (the SPARC
RC floor). Both ways: if small-1/mu leaves galaxies intact, the core route lives;
if it breaks them, the field route is confirmed dead.
"""
import numpy as np, pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1000*kpc; a0=9.36e-11; kms=1e3
Lsun=3.828e26  # not needed; L36 already in 1e9 Lsun

def Mfun(x):
    x=np.abs(x); s=np.sqrt(1+4*x); return (-1+s)/(1+s)
def x_of_zt(zt):
    if zt<=0: return 0.0
    f=lambda x: x*Mfun(x)-zt
    hi=max(2*zt,2*np.sqrt(zt),1e-8)
    while f(hi)<0: hi*=2
    return brentq(f,0,hi,xtol=1e-14,rtol=1e-12)

def aest_point_V(Mbar, inv_mu, R_out):
    """AeST RC at R_out for a point/compact baryon mass Mbar, Hamiltonian form."""
    mu2=(1/inv_mu)**2
    r0=0.2*kpc; gN0=G*Mbar/r0**2; g0=gN0*(0.5+np.sqrt(0.25+a0/gN0))
    P0=r0**2*Mfun(g0/a0)*g0; Phi0=-g0*r0
    def rhs(r,y):
        Ph,Pp=y; x=x_of_zt(abs(Pp)/(a0*r*r))
        Phip=np.sign(Pp)*a0*x if Pp!=0 else a0*x
        return [Phip, -mu2*r**2*Ph]   # vacuum outside compact source
    sol=solve_ivp(rhs,[r0,R_out],[Phi0,P0],method='Radau',rtol=1e-8,atol=1e-24,
                  max_step=0.5*kpc, dense_output=True)
    if not sol.success: return np.nan
    Ph,Pp=sol.sol(R_out); x=x_of_zt(abs(Pp)/(a0*R_out**2)); Phip=np.sign(Pp)*a0*x
    return np.sqrt(R_out*abs(Phip))   # V = sqrt(r*|Phi'|)

def mond_V(Mbar, R_out):
    gN=G*Mbar/R_out**2; g=gN*(0.5+np.sqrt(0.25+a0/gN)); return np.sqrt(R_out*g)

if __name__=="__main__":
    df=pd.read_csv('real_research/data/sparc_master_clean.csv')
    Ups=0.70  # framework M/L (eta-worst footing per MEMORY rule)
    df['Mbar']=(Ups*df['L36']+1.33*df['MHI'])*1e9*Msun
    df=df[df['Mbar']>0].copy()
    # outer radius proxy: use the flat-V radius. SPARC outer R ~ where V=Vflat.
    # Approximate R_out from V_flat and M_bar via deep-MOND R where g=a0:
    #   no direct R in this file -> use R_out = sqrt(G Mbar/a0) (MOND radius, the
    #   scale where curves flatten; outer points sit at ~1-3 rM). Conservative.
    df['rM']=np.sqrt(G*df['Mbar']/a0)
    print("SPARC galaxy veto: AeST mu^2*Phi RC distortion at R_out=2 rM")
    print("Ups=%.2f, N=%d galaxies, a0=%.3e"%(Ups,len(df),a0))
    print("%-12s %14s %14s %14s"%("1/mu[Mpc]","median|dV/V|","frac>10%","frac>20%"))
    R_out_fac=2.0
    for inv_mu in [0.1*Mpc,0.3*Mpc,1.0*Mpc,3.0*Mpc,10*Mpc,30*Mpc,97*Mpc]:
        dv=[]
        for _,g in df.iterrows():
            Rout=R_out_fac*g['rM']
            Va=aest_point_V(g['Mbar'], inv_mu, Rout)
            Vm=mond_V(g['Mbar'], Rout)
            if np.isfinite(Va) and Vm>0:
                dv.append(abs(Va-Vm)/Vm)
        dv=np.array(dv)
        if len(dv)==0:
            print("%-12.2f  all-fail"%(inv_mu/Mpc)); continue
        print("%-12.2f %14.3f %14.1f%% %13.1f%%"%(
            inv_mu/Mpc, np.median(dv), 100*np.mean(dv>0.10), 100*np.mean(dv>0.20)))
    print("\nReach: AeST core enhancement needs 1/mu <~ 0.3 Mpc (oscillation onset).")
    print("Verdict: if median|dV/V| or frac>10% blows up at 1/mu<=0.3 Mpc -> galaxy veto BREAKS.")
