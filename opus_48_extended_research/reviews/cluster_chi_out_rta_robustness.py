#!/usr/bin/env python3
"""
ROUTE A robustness: does eta(R500) at the cosmologically-fixed chi_out depend on the
matching-radius choice r_ta/R500 and the chi_out estimator? If chi_out is small
(cosmological) the answer must be ~ the deficit-to-mild regime regardless. We sweep
r_ta/R500 in {2,3,4,5.64} and recompute chi_out=Phi_cosmo(r_ta) and eta(R500) for the
5e14 fiducial. This isolates whether the cosmological BC is robustly NON-2.15.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

c=2.99792458e8; G_N=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
a0=9.36e-11; H0=67.4e3/Mpc; Om,OL=0.315,0.685
Lambda_OL=3.0*OL*H0**2/c**2
z=0.3; Ez2=Om*(1+z)**3+OL; Hz=H0*np.sqrt(Ez2)
rho_crit_z=3.0*Hz**2/(8*np.pi*G_N); rho_crit0=3*H0**2/(8*np.pi*G_N)
rho_m_z=Om*(1+z)**3*rho_crit0
mu=1.0/Mpc; v_c2_ref=(1000e3)**2

def Mfunc(x): s=np.sqrt(1+4*x); return (s-1)/(s+1)
def u_from_flux(F,r):
    if r==0.0: return 0.0
    f=abs(F)/(a0*r*r); return np.sign(F)*a0*(np.sqrt(f)+f)
def rhs(r,y,mu2,rho):
    Phi,F=y; return [u_from_flux(F,r), r*r*(4*np.pi*G_N*rho(r)-mu2*Phi)]

class Cluster:
    def __init__(s,M500,R500,f_gas500,f_star500=0.012,rc_over_R500=0.18,beta=2/3,a_star_kpc=30.0):
        s.M500=M500; s.R500=R500; s.beta=beta; s.rc=rc_over_R500*R500
        s.a_star=a_star_kpc*kpc; s.M_star=f_star500*M500
        rr=np.linspace(0,R500,40000)
        Ig=np.trapz(4*np.pi*rr**2*(1+(rr/s.rc)**2)**(-1.5*beta),rr); s.rho_g0=f_gas500*M500/Ig
    def rho_b(s,r): return s.rho_g0*(1+(r/s.rc)**2)**(-1.5*s.beta)
    def M_gas(s,r):
        rr=np.linspace(0,r,4000); return np.trapz(4*np.pi*rr**2*s.rho_g0*(1+(rr/s.rc)**2)**(-1.5*s.beta),rr)
    def M_bar(s,r): return s.M_gas(r)+s.M_star*r**2/(r+s.a_star)**2
    def g_bar(s,r): return G_N*s.M_bar(r)/r**2
def g_MOND(cl,r):
    gN=G_N*cl.M_bar(r)/r**2; f=gN/a0; return a0*(f+np.sqrt(f))

def _Mbar(rho,r):
    rr=np.linspace(0,r,2000); return np.trapz(4*np.pi*rr**2*np.array([rho(x) for x in rr]),rr)
def shoot(cl,chi_out,r_ta,r0=2*kpc):
    r_end=1.15*r_ta; F0=G_N*_Mbar(cl.rho_b,r0); mu2=mu*mu
    def Phi_rta(L):
        sol=solve_ivp(rhs,[r0,r_end],[-10.0**L,F0],args=(mu2,cl.rho_b),rtol=1e-9,atol=1e-11,
                      method='DOP853',dense_output=True,max_step=(r_end-r0)/1500.0)
        return sol.sol(r_ta)[0] if sol.success else None
    g=lambda L:(Phi_rta(L)-chi_out)
    Ls=np.linspace(9.0,13.5,24); gs=np.array([(lambda v:np.nan if v is None else v-chi_out)(Phi_rta(L)) for L in Ls])
    root=None
    for i in range(len(Ls)-1):
        if np.isfinite(gs[i]) and np.isfinite(gs[i+1]) and gs[i]*gs[i+1]<0:
            root=brentq(g,Ls[i],Ls[i+1],xtol=1e-4); break
    if root is None:
        root=minimize_scalar(lambda L:abs(g(L)),bounds=(9.0,13.5),method='bounded',options={'xatol':1e-4}).x
    sol=solve_ivp(rhs,[r0,r_end],[-10.0**root,F0],args=(mu2,cl.rho_b),rtol=1e-9,atol=1e-11,
                  method='DOP853',dense_output=True,max_step=(r_end-r0)/3000.0)
    return abs(u_from_flux(sol.sol(r_ta)[0] and sol.sol(cl.R500)[1],cl.R500))  # placeholder
def eta_R500(cl,chi_out,r_ta):
    r_end=1.15*r_ta; F0=G_N*_Mbar(cl.rho_b,2*kpc); mu2=mu*mu
    def Phi_rta(L):
        sol=solve_ivp(rhs,[2*kpc,r_end],[-10.0**L,F0],args=(mu2,cl.rho_b),rtol=1e-9,atol=1e-11,
                      method='DOP853',dense_output=True,max_step=(r_end-2*kpc)/1500.0)
        return sol if sol.success else None
    def val(L):
        s=Phi_rta(L); return None if s is None else s.sol(r_ta)[0]
    g=lambda L:(val(L)-chi_out)
    Ls=np.linspace(9.0,13.5,24); gs=np.array([(lambda v:np.nan if v is None else v-chi_out)(val(L)) for L in Ls])
    root=None
    for i in range(len(Ls)-1):
        if np.isfinite(gs[i]) and np.isfinite(gs[i+1]) and gs[i]*gs[i+1]<0:
            root=brentq(g,Ls[i],Ls[i+1],xtol=1e-4); break
    if root is None:
        root=minimize_scalar(lambda L:abs(g(L)) if val(L) is not None else 1e300,
                             bounds=(9.0,13.5),method='bounded',options={'xatol':1e-4}).x
    sol=Phi_rta(root)
    gA=abs(u_from_flux(sol.sol(cl.R500)[1],cl.R500))
    return gA/g_MOND(cl,cl.R500)

# fiducial 5e14
M=5e14; M500=M*Msun
R500=(M500/((4/3)*np.pi*500*rho_crit_z))**(1/3)
cl=Cluster(M500,R500,f_gas500=0.09+0.06*(np.log10(M)-14.0))
print("="*80)
print("ROUTE A robustness: eta(R500) vs matching radius r_ta/R500 and chi_out estimator")
print("  fiducial M500=5e14, R500=%.3f Mpc, 1/mu=1 Mpc"%(R500/Mpc))
print("="*80)
print(f"  {'r_ta/R500':>10} {'r_ta[Mpc]':>10} {'(mu r_ta)':>10} {'chiout(DE)':>12} {'eta(DE)':>9} {'chiout(mn)':>12} {'eta(mn)':>9}")
for ratio in [2.0,3.0,4.0,5.638]:
    r_ta=ratio*R500
    chi_DE=-(1/6)*Lambda_OL*c**2*r_ta**2
    chi_mn=-0.5*(4*np.pi/3)*G_N*rho_m_z*r_ta**2
    e_DE=eta_R500(cl,chi_DE,r_ta)
    e_mn=eta_R500(cl,chi_mn,r_ta)
    print(f"  {ratio:>10.2f} {r_ta/Mpc:>10.3f} {mu*r_ta:>10.3f} {chi_DE:>12.3e} {e_DE:>9.3f} {chi_mn:>12.3e} {e_mn:>9.3f}")
print("\n  -> if eta stays O(1) (0.5-1.6), never 2.15, across ALL r_ta choices and BOTH")
print("     estimators, the cosmological-BC verdict (no 2.15 boost) is ROBUST to the")
print("     matching-radius convention. The chi_out NEEDED for 2.15 is ~ -2e11 to -3e11")
print("     (=0.2-0.3 v_c^2), 3-10x LARGER than any cosmological estimator (~ -3 to -6e10).")
