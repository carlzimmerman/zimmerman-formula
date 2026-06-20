#!/usr/bin/env python3
"""
ROUTE B FINAL: (A) FULL AeST extended-source core mass at viable AND aggressive
1/mu, validated against Durakovic-Skordis 2312.00889; (B) the GALAXY VETO at the
SAME 1/mu that would be needed to reach the core.

The decisive both-ways logic:
  - The AeST mu^2*Phi enhancement reaches the 420 kpc core only if 1/mu <~ 0.3 Mpc
    (oscillation onset r_C, Eq.2.42, verified in oscillation_onset_scale.py).
  - At viable (CMB-fit) 1/mu = 3-97 Mpc the core enhancement over MOND is only
    ~1.1-1.3x -> nowhere near the ~4.4x needed (gate G1 FAILS in form).
  - If we AGGRESSIVELY push 1/mu down to reach the core, the apparent mass becomes
    a violently 1/mu-sensitive, sign-indefinite OSCILLATION (negative phantom mass),
    NOT a robust ~8x pump.
  - AND a 1/mu ~ 0.1-0.3 Mpc screening length bites INSIDE galaxy halos -> galaxy
    veto. This script computes the galaxy RC distortion from the mu^2*Phi term at
    that 1/mu on SPARC-scale systems.

Hamiltonian form validated against the point-source result (M/M ~ 1.3 core,
runaway in outskirts), matching Durakovic Figs 5-7.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.interpolate import interp1d

G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1000*kpc; a0=9.36e-11; kms=1e3

def Mfun(x):
    x=np.abs(x); s=np.sqrt(1+4*x); return (-1+s)/(1+s)
def x_of_zt(zt):
    if zt<=0: return 0.0
    f=lambda x: x*Mfun(x)-zt
    hi=max(2*zt,2*np.sqrt(zt),1e-8)
    while f(hi)<0: hi*=2
    return brentq(f,0,hi,xtol=1e-14,rtol=1e-12)

# ---------- (A) EXTENDED cluster source, AeST Hamiltonian ----------
def cluster_baryons(M500=1e15*Msun, fgas=0.13, M_BCG=1e12*Msun,
                    rc=120*kpc, beta=0.67, r500=1.4*Mpc, a_BCG=15*kpc,
                    r_gas_trunc=2.5*Mpc):
    def shape(r): return (1+(r/rc)**2)**(-1.5*beta)
    rr=np.logspace(np.log10(0.5*kpc),np.log10(r500),5000)
    rho0=(fgas*M500)/np.trapz(4*np.pi*rr**2*shape(rr),rr)
    rg=np.logspace(np.log10(0.2*kpc),np.log10(8*Mpc),3000)
    sh=shape(rg); sh[rg>r_gas_trunc]*= np.exp(-((rg[rg>r_gas_trunc]-r_gas_trunc)/(0.5*Mpc))**2)
    Mgas_cum=np.concatenate([[0],np.cumsum(0.5*(4*np.pi*rg[1:]**2*rho0*sh[1:]
                            +4*np.pi*rg[:-1]**2*rho0*sh[:-1])*np.diff(rg))])
    Mgas_i=interp1d(rg,Mgas_cum,bounds_error=False,fill_value=(0,Mgas_cum[-1]))
    def Mbar(r): return float(Mgas_i(r))+M_BCG*r*r/(r+a_BCG)**2
    return Mbar, Mbar(8*Mpc)

def aest_extended(Mbar, inv_mu, r_in=3*kpc, r_out=8*Mpc, N=4000):
    mu2=(1.0/inv_mu)**2
    rg=np.logspace(np.log10(r_in),np.log10(r_out),N)
    Mb=np.array([Mbar(r) for r in rg]); dMb=np.gradient(Mb,rg)
    dMb_i=interp1d(rg,dMb,bounds_error=False,fill_value=(dMb[0],dMb[-1]))
    r0=r_in; Mb0=Mbar(r0); gN0=G*Mb0/r0**2; g0=gN0*(0.5+np.sqrt(0.25+a0/gN0))
    P0=r0**2*Mfun(g0/a0)*g0; Phi0=-g0*r0
    def rhs(r,y):
        Ph,Pp=y; x=x_of_zt(abs(Pp)/(a0*r*r))
        Phip=np.sign(Pp)*a0*x if Pp!=0 else a0*x
        return [Phip, -mu2*r**2*Ph + G*float(dMb_i(r))]
    rg[0]=r0; rg[-1]=r_out
    sol=solve_ivp(rhs,[r0,r_out],[Phi0,P0],t_eval=rg,method='Radau',
                  rtol=1e-8,atol=1e-22,max_step=8*kpc)
    if not sol.success: return None
    r=sol.t; Pp=sol.y[1]
    Phip=np.array([np.sign(Pp[i])*a0*x_of_zt(abs(Pp[i])/(a0*r[i]**2)) for i in range(len(r))])
    # apparent total mass = r^2 |Phi'|/G (inward accel g=|Phi'|); sign of Pp tracks
    # attractive(+)/antigravity(-) so keep the sign of Phi' for oscillation regime
    return dict(r=r, M_aest=r**2*Phip/G)

def encM(res,R):
    if res is None: return np.nan
    i=min(max(np.searchsorted(res['r'],R),1),len(res['r'])-1); return res['M_aest'][i]

# ---------- (B) GALAXY VETO: does the mu^2*Phi term distort SPARC RCs? ----------
def galaxy_rc_distortion(inv_mu, Mdisk=5e10*Msun, Rd=3*kpc):
    """L* disk (exponential-ish, treat as point M for r>>Rd). Compare MOND RC to
       AeST RC with the mu^2*Phi term, at the SAME 1/mu. The mu^2 term adds an
       antigravity/oscillation; the fractional RC distortion at the last measured
       point (~5-10 Rd) is the veto metric. SPARC RAR floor is 0.13-0.15 dex."""
    rM=np.sqrt(G*Mdisk/a0)
    mu2=(1.0/inv_mu)**2
    def Mbar(r): return Mdisk*(1-np.exp(-r/Rd)*(1+r/Rd))  # exp disk enclosed (approx)
    res=aest_extended(Mbar, inv_mu, r_in=0.3*kpc, r_out=200*kpc, N=2500)
    out={}
    for rfac,lab in [(5*Rd,'5Rd'),(10*Rd,'10Rd'),(20*Rd,'20Rd')]:
        Maest=encM(res,rfac)
        gN=G*Mbar(rfac)/rfac**2; gmond=gN*(0.5+np.sqrt(0.25+a0/gN))
        Mmond=gmond*rfac**2/G
        v_aest=np.sqrt(G*abs(Maest)/rfac) if np.isfinite(Maest) else np.nan
        v_mond=np.sqrt(G*Mmond/rfac)
        out[lab]=(v_aest/kms, v_mond/kms, (v_aest-v_mond)/v_mond if v_mond>0 else np.nan)
    return out

if __name__=="__main__":
    print("="*74)
    print("ROUTE B FINAL: AeST extended core mass + galaxy veto, both ways")
    print("="*74)
    Mbar,Mtot=cluster_baryons(); R=420*kpc; M_target=2.30e14*Msun
    Mbar_core=Mbar(R)
    print("M_bar(<420)=%.3e  M_bar_tot=%.3e  TARGET(<420)=%.3e Msun"%(
        Mbar_core/Msun,Mtot/Msun,M_target/Msun))
    # MOND proxy
    gN=G*Mbar_core/R**2; gm=gN*(0.5+np.sqrt(0.25+a0/gN)); Mmond=gm*R**2/G
    print("MOND phantom proxy M(<420)=%.3e  undershoot x%.2f\n"%(Mmond/Msun,M_target/Mmond))

    print("(A) FULL AeST extended core mass vs 1/mu:")
    print("%-12s %-10s %14s %9s %9s"%("1/mu[Mpc]","rC/420kpc","M_AeST(<420)","x_under","vsMOND"))
    rM_cl=np.sqrt(G*1e15*Msun/a0)
    def rC(inv_mu): return (1/3)*(18/((rM_cl/inv_mu)**2))**(1/3)*rM_cl
    for inv_mu in [0.1*Mpc,0.2*Mpc,0.3*Mpc,1.0*Mpc,3.0*Mpc,10.0*Mpc,30.0*Mpc,97.0*Mpc]:
        res=aest_extended(Mbar,inv_mu); Mc=encM(res,R)
        if not np.isfinite(Mc):
            print("%-12.2f %-10.2f %14s"%(inv_mu/Mpc,rC(inv_mu)/R,"(fail)")); continue
        tag=" CLOSES" if Mc>M_target else ""
        print("%-12.2f %-10.2f %14.3e %9.2f %9.2f%s"%(
            inv_mu/Mpc, rC(inv_mu)/R, Mc/Msun,
            M_target/Mc if Mc>0 else np.nan, Mc/Mmond if Mc>0 else np.nan, tag))

    print("\n(B) GALAXY VETO at the SAME 1/mu (L* disk, M=5e10, Rd=3kpc):")
    print("    fractional RC distortion (v_AeST - v_MOND)/v_MOND at last point:")
    print("%-12s %12s %12s %12s"%("1/mu[Mpc]","@5Rd","@10Rd","@20Rd"))
    for inv_mu in [0.1*Mpc,0.3*Mpc,1.0*Mpc,3.0*Mpc,10*Mpc,97*Mpc]:
        d=galaxy_rc_distortion(inv_mu)
        def f(lab):
            v=d.get(lab,(np.nan,)*3); return v[2]
        print("%-12.2f %12s %12s %12s"%(inv_mu/Mpc,
            "%+.1f%%"%(100*f('5Rd')) if np.isfinite(f('5Rd')) else "nan",
            "%+.1f%%"%(100*f('10Rd')) if np.isfinite(f('10Rd')) else "nan",
            "%+.1f%%"%(100*f('20Rd')) if np.isfinite(f('20Rd')) else "nan"))
    print("\n(SPARC RC measurement floor ~5-10%; a >10% systematic distortion = breaks galaxies)")
