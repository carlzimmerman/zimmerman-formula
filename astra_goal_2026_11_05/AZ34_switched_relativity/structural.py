#!/usr/bin/env python3
"""Exact switched-action identities and explicit regularity/control witnesses."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import numpy as np
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
MODE='mutate' if args.mutate else 'main'
OUT=HERE/MODE;OUT.mkdir(exist_ok=True)
t0=time.monotonic(); checks={}
def check(name,value):
    checks[name]=bool(value);print(name,checks[name],flush=True)
def save(name,data):
    p=OUT/(name+'.json');q=p.with_suffix('.tmp')
    q.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n');os.replace(q,p)

psi,gamma=sp.symbols('psi gamma',real=True)
positive=gamma*psi**2/2 if not args.mutate else sp.Integer(0)
negative=sp.Integer(0) if not args.mutate else gamma*psi**2/2
branches={'positive':positive,'negative':negative}
switch={k:dict(F=str(v),first=str(sp.diff(v,psi)),second=str(sp.diff(v,psi,2))) for k,v in branches.items()}
check('switch_C1',positive.subs(psi,0)==negative.subs(psi,0) and sp.diff(positive-negative,psi).subs(psi,0)==0)
check('zero_stiffness_known',all(v.subs(gamma,0)==0 for v in branches.values()))
csrows=[]
for density in (-2.,-.5,.5,2.):
    for dust in (0.,.1,3.):
        stiffness=float(sp.diff(branches['positive' if density>0 else 'negative'],psi,2).subs(gamma,1))
        csrows.append(dict(psi=density,dust=dust,c2=(density+dust)*stiffness))
check('nonnegative_principal_sound_speed',all(r['c2']>=0 for r in csrows))
save('switch',dict(branches=switch,sound_speed=csrows,
    scope='local principal coefficient with nonnegative dust; not nonlinear PDE well-posedness'))

# Convex energy does not control the full divergence norm after switching.
u,K,a0=sp.symbols('u K a0',positive=True)
g=(-a0*u-a0**2*sp.log(1-u/a0)-u**2/2)/K
gp=sp.diff(g,u);gpp=sp.diff(g,u,2)
check('g_derivative_exact',sp.simplify(gp-u**2/(K*(a0-u)))==0)
check('g_second_derivative_exact',sp.simplify(gpp-u*(2*a0-u)/(K*(a0-u)**2))==0)
x,n,a=sp.symbols('x n a',positive=True)
p=-a*sp.tanh(n*x)
Phi=(-a*sp.log(sp.cosh(n*x))+a*sp.log(sp.cosh(n)))/n
check('leaf_square_term_zero',sp.simplify(sp.diff(Phi,x)-p)==0)
check('leaf_boundary_zero',Phi.subs(x,1)==0 and Phi.subs(x,-1)==0)
# Primitive of sech^4(nx) verifies the derivative-norm integral exactly.
primitive=a*a*n*(sp.tanh(n*x)-sp.tanh(n*x)**3/3)
check('derivative_norm_primitive',sp.simplify(sp.diff(primitive,x)-sp.diff(p,x)**2)==0)
norm=sp.simplify(primitive.subs(x,1)-primitive.subs(x,-1))
coefficient=sp.limit(norm/n,n,sp.oo)
check('unbounded_divergence_exact',sp.simplify(coefficient-4*a*a/3)==0)
amp=.5;gu=lambda z:-z-np.log1p(-z)-z*z/2
bound=2*float(gu(amp)); rows=[]
quadrature={q:np.polynomial.legendre.leggauss(q) for q in (512,1024)}
for N in (16,32,64,128):
    exact=float(norm.subs({n:N,a:amp}))
    values={}
    for q,(xx,ww) in quadrature.items():
        pp=-amp*np.tanh(N*xx);dp=-amp*N/np.cosh(N*xx)**2
        energy=float(np.dot(ww,gu(np.abs(pp))))
        penalty=float(np.dot(ww,np.minimum(dp,0)**2 if args.mutate else np.maximum(dp,0)**2))/2
        values[str(q)]=dict(energy=energy+penalty,base_energy=energy,penalty=penalty,
                            div_norm2=float(np.dot(ww,dp*dp)))
    er=abs(values['512']['energy']/values['1024']['energy']-1)
    dr=abs(values['1024']['div_norm2']/exact-1)
    rows.append(dict(n=N,exact_div_norm2=exact,quadrature=values,energy_relative_change=er,
                     norm_relative_error=dr))
check('leaf_quadrature_pair',all(r['energy_relative_change']<=1e-6 for r in rows))
check('leaf_quadrature_exact_norm',all(r['norm_relative_error']<=1e-8 for r in rows))
check('leaf_uniform_energy_bound',all(r['quadrature']['1024']['energy']<=bound*(1+1e-12) for r in rows))
save('leaf',dict(label='UNDECIDED full well-posedness',g_prime=str(sp.factor(gp)),g_second=str(sp.factor(gpp)),
    sequence=dict(p=str(p),Phi=str(Phi),norm2=str(norm),norm2_over_n_limit=str(coefficient),amplitude=amp),
    energy_bound_main=bound,rows=rows,
    conclusion='Main sequence disproves H(div) coercivity from this energy. It does not prove nonexistence of a minimizer. Strict convexity gives at-most-one minimizer if it exists; relaxed measure-divergence domains require separate treatment.'))

# Full symbolic matter Noether identity for an arbitrary diagonal 1+1 metric.
t,z=sp.symbols('t z',real=True);coords=(t,z)
A=sp.Function('A')(t,z);B=sp.Function('B')(t,z);chi=sp.Function('chi')(t,z)
m=sp.symbols('m',real=True)
metric=sp.diag(-sp.exp(2*A),sp.exp(2*B));inv=metric.inv();vol=sp.exp(A+B)
d=[sp.diff(chi,c) for c in coords]
kin=sum(inv[i,j]*d[i]*d[j] for i in range(2) for j in range(2))/2
T=sp.Matrix(2,2,lambda i,j:sum(inv[i,k]*d[k]*d[j] for k in range(2))-(kin+m*m*chi*chi/2)*(1 if i==j else 0))
Gamma=[[[sp.simplify(sum(inv[i,l]*(sp.diff(metric[l,k],coords[j])+sp.diff(metric[l,j],coords[k])-sp.diff(metric[j,k],coords[l])) for l in range(2))/2)
          for k in range(2)] for j in range(2)] for i in range(2)]
div=[]
for j in range(2):
    div.append(sp.simplify(sum(sp.diff(T[i,j],coords[i]) for i in range(2))+
        sum(Gamma[i][i][k]*T[k,j]-Gamma[k][i][j]*T[i,k] for i in range(2) for k in range(2))))
E=sp.simplify(sum(sp.diff(vol*inv[i,j]*d[j],coords[i]) for i in range(2) for j in range(2))/vol-m*m*chi)
residual=[sp.simplify(div[j]-E*d[j]) for j in range(2)]
check('matter_Noether_identity',all(r==0 for r in residual))
off=[sp.simplify(v.subs({A:0,B:0,chi:t*t,m:0}).doit()) for v in div]
on=[sp.simplify(v.subs({A:0,B:0,chi:t+z,m:0}).doit()) for v in div]
check('matter_on_shell_known',on==[0,0])
check('off_shell_counterexample',sp.simplify(off[0]+4*t)==0 and off[1]==0)
save('G9',dict(label='PASS matter-shell identity; off-shell-zero wording false',residuals=list(map(str,residual)),
    off_shell_counterexample=list(map(str,off)),on_shell_known=list(map(str,on)),
    identity='nabla_mu T^mu_nu = (Box chi - m^2 chi) partial_nu chi',
    switch='Either sign orientation is a scalar function of D.P and preserves diffeomorphism invariance.',
    scope='1+1 symbolic check plus general minimally-coupled-matter Noether argument; not full gravitational health'))

# C8 arithmetic, with explicit record-derived observational precisions.
PC=3.0856775814913673e16;GMSUN=1.32712440018e20;G=6.67430e-11
footings={'canonical':9.3603e-11,'alt':1.1312e-10}
lengths={'canonical':(21.68,24.,27.),'alt':(22.85,24.,24.60)}
psr={'J0737-3039A/B':(.1022515592973,2.587052,6.3e-5),
     'B1913+16':(.322997448911,2.828378,1.6e-3),
     'J1738+0333':(.3547907398724,1.641,3.2/27.7)}
refpath=ROOT/'covariant_push_2026_10_22/C8_instantaneous/c8_instantaneous_results.json'
ref=json.loads(refpath.read_text())['K7']['systems']
known=[];pulsars={};causal={}
for foot,A0 in footings.items():
    pulsars[foot]={};causal[foot]={}
    for name,(Pb,mass,precision) in psr.items():
        radius=(GMSUN*mass*(Pb*86400)**2/(4*math.pi**2))**(1/3)
        known.append(abs((radius/(24*PC))**2/ref[name]['L24']['eps']-1))
        pulsars[foot][name]={str(L):dict(epsilon=(radius/(L*PC))**2,
            ratio_to_precision=(radius/(L*PC))**2/precision,
            nonlinear=(radius/(L*PC))**2*GMSUN*mass/((L*PC)**2*A0)) for L in lengths[foot]}
    causal[foot]={str(L):G*1000/(L*PC)**2*(1/1000) for L in lengths[foot]}
check('C8_known_24pc',max(known)<=1e-10)
check('pulsar_conservative_estimate',all(r['ratio_to_precision']<1 for f in pulsars.values() for s in f.values() for r in s.values()))
save('pulsars',dict(label='NO VERDICT full radiation; conservative estimate survives',footings=pulsars,
    known_max_relative=max(known),precision_source='C8 record transcriptions; no new observational validation',
    scope='C8 no-radiative-channel assertion is not carried; P3 supplies a propagating background-gradient mode.'))
save('causality',dict(label='NO VERDICT gauge-invariant retarded response',force_estimates_m_s2=causal,
    GR_control='An elliptic lapse/Poisson constraint is compatible with retarded gauge-invariant observables after the full constrained equations and conserved sources are included. The constraint alone cannot decide criterion A.',
    criterion_B='A globally regular timelike khronon provides an ordering conditional on its global existence.',
    scope='C8 instantaneous-force formula is illustrative, not a new full-system response calculation.'))
result=dict(mode=MODE,checks=checks,seconds=time.monotonic()-t0,
    sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
             (Path(__file__),HERE/'FROZEN_CRITERIA.md',refpath)},
    statement='kappa = 1/2 FITTED; not theory closed')
save('structural_results',result)
print(json.dumps(result,indent=2));sys.exit(0 if all(checks.values()) else 1)
