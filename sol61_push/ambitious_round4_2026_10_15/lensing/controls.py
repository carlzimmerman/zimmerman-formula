import argparse,json,time
import numpy as np
from scipy.integrate import quad
from model import *

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);args=p.parse_args()
t=time.monotonic();r,y,c=data();rr=r[0]
env=Environment();hd=hankel(rr);los=env.los(rr)
ref=Environment(power_points=131072,padding=64);hf=hankel(rr,nk=131073);lr=ref.los(rr,order=1024,rmax=450.)
# Direct independent one-halo quadrature integrates density and cylinder caps.
onechecks=[]
for ex in (5.,30.,54.):
    for x in (.02,.5,2.,ex*.999,ex,ex*1.1):
        rho=lambda s:1/(2*np.pi*s*np.sqrt(1+4*s*s))
        sig=2*quad(lambda tt:rho(np.hypot(x,tt)),0,np.sqrt(max(0,ex*ex-x*x)),epsabs=1e-11,epsrel=1e-10)[0] if x<ex else 0.
        m=min(x,ex);mass=(np.sqrt(1+4*m*m)-1)/2
        if x<ex:mass+=quad(lambda s:2*s/np.sqrt(1+4*s*s)*(1-np.sqrt(1-x*x/s**2)),x,ex,epsabs=1e-10,epsrel=1e-10)[0]
        direct=(1+mass)/(np.pi*x*x)-sig;fast=float(profile(np.array([x]),ex)[0])
        onechecks.append(dict(edge=ex,x=x,direct=direct,fast=fast,relative=abs(fast/direct-1)))
# Independent analytic infinite projection against direct full-density cylinder integral.
infchecks=[]
for x in (.02,.5,2.,20.,100.):
    sig=quad(lambda u:1/np.sqrt(1+4*x*x*np.cosh(u)**2),0,30,epsabs=1e-11)[0]/np.pi
    mc=(np.sqrt(1+4*x*x)-1)/2+quad(lambda u:2*x*x*np.exp(2*u)/np.sqrt(1+4*x*x*np.exp(2*u))*(1-np.sqrt(1-np.exp(-2*u))),0,22,epsabs=1e-9)[0]
    direct=(1+mc)/(np.pi*x*x)-sig;fast=float(profile(np.array([x]))[0]);infchecks.append(dict(x=x,relative=abs(fast/direct-1)))
identities=[]
for convention in ('native_h','legacy_physical'):
    for lm in np.linspace(9.5,12,21):
        ex,n,mt,e,rm=edge(lm,convention)
        mass=(np.sqrt(1+4*e*e)-1)/2
        identities.append(abs(mass/(SUP*n)-1))
eg,table=env.table(rr,nedge=1201,order=512)
# Inferred zero-exclusion table cross-check and exclusion-sensitive convention.
mutation=[]
for lm in (10.3,10.8,11.2):
    ex,*_=edge(lm)
    at=env.los(rr,ex);mutation.append(dict(logMb=lm,edge=ex,relative_by_radius=((at-los)/np.maximum(abs(los),.01*max(abs(los)))).tolist()))
checks=dict(hankel_vs_los=floor_relative(los,hd),refined_hankel_vs_los=floor_relative(lr,hf),hankel_refinement=floor_relative(hd,hf),los_refinement=floor_relative(los,lr),onehalo_finite_max_relative=max(v['relative'] for v in onechecks),onehalo_infinite_max_relative=max(v['relative'] for v in infchecks),edge_mass_identity_max=max(identities),normalization_mutation_relative=1.,table_zero_vs_hankel=floor_relative(table[:,0],hd))
passed=(max(checks[k] for k in ('hankel_vs_los','refined_hankel_vs_los','hankel_refinement','los_refinement','table_zero_vs_hankel'))<=.01 and checks['onehalo_finite_max_relative']<=.001 and checks['onehalo_infinite_max_relative']<=.001 and checks['edge_mass_identity_max']<=1e-9)
np.savez(args.cache,edge_grid=eg,table=table,radii=rr,zero_hankel=hd,zero_los=los)
result=dict(status='PASS' if passed else 'FAIL',checks=checks,radii_physical_Mpc=rr.tolist(),hankel=hd.tolist(),los=los.tolist(),refined_hankel=hf.tolist(),refined_los=lr.tolist(),finite_onehalo_checks=onechecks,infinite_onehalo_checks=infchecks,exclusion_mutation=mutation,covariance=covariance_diagnostics(c),elapsed_seconds=time.monotonic()-t,fft=dict(dk=env.dk,dr=env.dr,refined_dk=ref.dk,refined_dr=ref.dr),old_sigma8_K2='REMAINS FAILED; no estimator renormalization')
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status=result['status'],checks=checks,seconds=result['elapsed_seconds'])))
