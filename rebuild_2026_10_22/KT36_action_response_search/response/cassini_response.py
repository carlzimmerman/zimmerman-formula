"""Corrected Cassini quadrupole with explicit response injection; no monkeypatching."""
import importlib.util
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
_path=ROOT/'rebuild_2026_10_22/KT33_reciprocal_filter/cassini/cassini_v2.py'
_spec=importlib.util.spec_from_file_location('kt33_cassini_readonly',_path)
baseline=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(baseline)


def quadrupole(response,eta,epsilon,nr=3000,nm=80,rmin=1e-7,rmax=1e5):
    """Equal source/outer Gaussian; KT33 independent flux and density forms."""
    if epsilon<0 or eta<0: raise ValueError('Nonnegative epsilon and eta required')
    log_r=np.linspace(math.log(rmin),math.log(rmax),nr); r=np.exp(log_r)
    mu,w=baseline.angular_rule(nm); mu=mu[None,:]; p=3*mu*mu-1
    f1=np.zeros(nr); f2=np.zeros(nr); fd=np.zeros(nr); surface=np.zeros(nr)
    for start in range(0,nr,256):
        sl=slice(start,min(start+256,nr)); rr=r[sl,None]
        g=baseline.gaussian_field(rr,epsilon)
        divg=np.zeros_like(rr) if epsilon==0 else baseline.SQRT2PI*np.exp(-.5*(rr/epsilon)**2)/epsilon**3
        gp=divg-2*g/rr
        h=np.sqrt((g+eta*mu)**2+eta*eta*(1-mu*mu)); h0=np.hypot(g,eta)
        a=response.excess(h); a0=response.excess(h0); aa=a-a0
        dn=response.nud(h); dn0=response.nud(h0)
        d=a*divg+(dn/h)*(gp*(g+eta*mu)**2+eta*eta*g*(1-mu*mu)/rr)
        d0=a0*divg+(dn0/h0)*(gp*g*g+eta*eta*g/rr); dd=d-d0
        t=baseline.kernel_weight(rr[:,0],epsilon); tp=baseline.kernel_weight_prime(rr[:,0],epsilon)
        b=(aa*(eta*(3*mu-5*mu**3)+g*(1-3*mu*mu)))@w
        c=(aa*(g+eta*mu)*p)@w; dp=(dd*p)@w
        f1[sl]=1.5*t*b/r[sl]; f2[sl]=.5*tp*c; fd[sl]=-.5*t*dp; surface[sl]=.5*t*c/r[sl]
    q1=float(np.trapz(f1,log_r)); q2=float(np.trapz(f2,log_r)); qd=float(np.trapz(fd,log_r))
    boundary=float(surface[-1]-surface[0]); q=q1+q2-boundary
    return dict(q_hessian_signed=q,q_density_signed=qd,flux_density_difference=q-qd,
                weighted_old_term=q1,gaussian_derivative_term=q2,boundary_term=boundary,
                epsilon=epsilon,nr=nr,nm=nm,rmin=rmin,rmax=rmax)


def physical(response,foot,epsilon,**settings):
    a0=baseline.A0[foot]; out=quadrupole(response,baseline.GEXT/a0,epsilon,**settings)
    pref=1.5*a0/math.sqrt(baseline.GM/a0); q2=out['q_hessian_signed']*pref
    out.update(footing=foot,Q2_signed_s_minus_2=q2,x_ceiling=abs(q2)/baseline.CEILING,
               cassini_pass=abs(q2)<=baseline.CEILING)
    return out
