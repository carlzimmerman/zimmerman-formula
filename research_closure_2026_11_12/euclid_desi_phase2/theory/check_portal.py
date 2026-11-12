#!/usr/bin/env python3
"""Bounded exact/matrix checks of a changed density-portal kernel, not a data fit."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()

x,u,eta=sp.symbols('x u eta', positive=True)
f=((1+2*x)**sp.Rational(3,2)-3*sp.sqrt(1+2*x)+2)/6
p=sp.simplify(sp.diff(f,x)); d=sp.simplify(sp.diff(p,x))
h=sp.simplify(2*f-x*p); DD=sp.simplify(p*p/d-x*p)
assert sp.simplify(p-x/sp.sqrt(1+2*x))==0
assert sp.simplify(d-(1+x)/(1+2*x)**sp.Rational(3,2))==0
assert sp.simplify(DD-x**3/((1+x)*sp.sqrt(1+2*x)))==0
hu=(u-1)**3*(u+3)/(12*u)
Du=(u*u-1)**3/(4*u*(u*u+1))
R=sp.factor(2*hu/Du)
assert sp.simplify(R-sp.Rational(2,3)*(1-2*(u-1)/(u+1)**3))==0
assert sp.simplify(sp.diff(R,u)-8*(u-2)/(3*(u+1)**4))==0
assert R.subs(u,2)==sp.Rational(50,81)
# Independent fixed-P Legendre differentiation, with a=sqrt(rho/R0).
g,rho,R0=sp.symbols('g rho R0',positive=True)
aa=sp.sqrt(rho/R0)
FF=aa**2*f.subs(x,g/aa)
Fg=sp.diff(FF,g); Fgg=sp.diff(Fg,g)
Fr=sp.diff(FF,rho); Frr=sp.diff(Fr,rho); Fgr=sp.diff(Fg,rho)
locked=sp.simplify(1+Fr+eta*rho*(Frr-Fgr**2/Fgg))
expect=1+(h-eta*DD/2)/(2*R0)
assert sp.simplify((locked-expect.subs(x,g/aa)))==0

mp.mp.dps=80
xi=mp.mpf(1)/4; eps=xi/(8*mp.pi); E=4*mp.pi/xi
def slow(xx,ee):
    xx=mp.mpf(xx);ee=mp.mpf(ee);uu=mp.sqrt(1+2*xx)
    pp=xx/uu;dd=(1+xx)/uu**3
    hh=(uu-1)**3*(uu+3)/(12*uu)
    delta=xx**3/((1+xx)*uu)
    KL=1+eps*(hh-ee*delta/2)
    GG=1+eps*hh
    bb=mp.sqrt(ee)/(2*mp.sqrt(E))*(xx-pp/dd)
    return dd,hh,KL,GG,bb

xs=['0.001','0.1','1','1.5','10','100','1e6','1e12','1e22']
etas=[mp.mpf(0),mp.mpf('0.1'),mp.mpf(1)/3,mp.mpf('0.6'),mp.mpf(50)/81]
angles=[mp.mpf(0),mp.pi/4,mp.pi/2]
gammas=[mp.mpf(0),mp.mpf('1000')]
ks=[mp.mpf('100'),mp.mpf('1e6')]
ncase=0; worst_match=mp.mpf(0); min_K=mp.inf; max_anti=mp.mpf(0)
for xx,ee,th,gamma,k,with_lapse in itertools.product(xs,etas,angles,gammas,ks,[False,True]):
    dd,hh,KL,GG,bb=slow(xx,ee)
    xx=mp.mpf(xx);uu=mp.sqrt(1+2*xx)
    H=mp.diag([uu,uu,1/dd]);nh=mp.matrix([mp.sin(th),0,mp.cos(th)])
    D=H+gamma*k*k*(nh*nh.T);Di=D**-1
    Q=(nh.T*Di*nh)[0]
    assert 0<Q<1 and KL>=1-mp.mpf('1e-70') and GG>=1
    C=mp.zeros(4)
    C[0,0]=-k*k
    for i in range(3):
        C[0,i+1]=C[i+1,0]=k*nh[i]
        for j in range(3):C[i+1,j+1]=-D[i,j]
    mp.cholesky(-C)
    B=mp.zeros(4,2)
    B[3,0]=-bb
    for i in range(3):B[i+1,1]=-nh[i]
    # Canonical lapse/phi_dot term in a Hermitian Fourier convention.
    if with_lapse:B[0,0]=mp.j*mp.sqrt(ee*E)*GG
    KR=mp.diag([KL,0])-B.H*(C**-1)*B
    # Complex diagonal roundoff can trigger mpmath's absolute Hermitian test.
    # Validate the raw relative defect before enforcing the exact adjoint identity.
    anti=mp.norm(KR-KR.H)/max(1,mp.norm(KR))
    assert anti<mp.mpf('1e-60')
    max_anti=max(max_anti,anti)
    KR=(KR+KR.H)/2
    mp.cholesky(KR)
    det=mp.re(mp.det(KR))
    assert det>0
    min_K=min(min_K,KL)
    if not with_lapse:
        bv=mp.matrix([0,0,bb]);B0=(nh.T*Di*bv)[0];C0=(bv.T*Di*bv)[0]
        known=mp.matrix([[KL+C0+B0*B0/(1-Q),B0/(1-Q)],[B0/(1-Q),Q/(1-Q)]])
        err=mp.norm(KR-known)/max(1,mp.norm(KR))
        assert err<mp.mpf('1e-60')
        worst_match=max(worst_match,err)
    ncase+=1
assert ncase==1080

# Sign-reversing/known-failure controls; none is a claimed viable branch.
ss=mp.mpf('108.9');ee=mp.mpf('0.05')
hs=ss+ss/(1+ss)-2*mp.log1p(ss)
simple_lock=1+eps*(hs-ee*ss**3/(2*(1+ss)))
simple_free=1+eps*(hs-ee*ss**3/(2*(1+ss)**2))
assert simple_lock<0<simple_free
exp_d=(1-mp.mpf(2))*mp.exp(-2)
assert exp_d/(1-exp_d)<0
bad_slow=slow('1e6',mp.mpf(2)/3)[2]
assert bad_slow<0

# Explicit local toy PDE, not a solved covariant galaxy background.
GSI=6.67430e-11;c=299792458.;MS=1.98847e30;pc=3.0857e16;AU=1.495978707e11
A0=9.3603e-11;epsf=float(eps);OmDE=.685
fixtures=[('Sun_1AU',MS,6.957e8,AU),('Earth_surface',5.9722e24,6.371e6,6.371e6),
          ('MW_8kpc',6e10*MS,100*pc,8e3*pc),('cluster_1Mpc',1e14*MS,1e3*pc,1e6*pc)]
def invert_mu(y):
    lo=np.zeros_like(y);hi=y+np.sqrt(2*y)+1
    for unused in range(70):
        mid=(lo+hi)/2;uu=np.sqrt(1+2*mid)
        value=2*mid*mid/(uu*(uu+1))
        move=value<y
        lo=np.where(move,mid,lo);hi=np.where(move,hi,mid)
    return (lo+hi)/2
def radial(name,mass,core,ro,ee,N,outer):
    rM=math.sqrt(GSI*mass/A0)
    r=np.unique(np.concatenate([np.geomspace(core*1e-6,outer*rM,N),[core,ro]]))
    gb=np.where(r<core,GSI*mass*r/core**3,GSI*mass/r**2)
    xx=invert_mu(gb/A0);uu=np.sqrt(1+2*xx)
    hh=(2*xx/(uu+1))**3*(uu+3)/(12*uu)
    xhp=xx**3/(1+2*xx)**1.5
    Z=1+epsf*hh
    ageo=A0/c**2
    Hgeo=ageo/math.sqrt(3*epsf*OmDE)
    q_over_M=ageo*math.sqrt(ee/epsf)
    source=2*(1-ee/2)*ageo**2*hh+1.5*Hgeo*ageo*math.sqrt(epsf)*ee**1.5*xhp
    rrsource=r*r*source
    interior=np.concatenate([[0],np.cumsum((rrsource[1:]+rrsource[:-1])/2*np.diff(r))])
    deriv=interior/(r*r*Z)
    shells=(deriv[1:]+deriv[:-1])/2*np.diff(r)
    magchi=np.concatenate([np.cumsum(shells[::-1])[::-1],[0]])
    val=float(np.interp(ro,r,magchi))
    return {'name':name,'eta':ee,'N':N,'outer_rM':outer,
            'frozen_PDE_abs_delta_lna_at_observation':(1-ee/2)*val/2,
            'max_gradient_to_background_q':float(np.max(deriv/q_over_M)),
            'baryonic_metric_redshift_estimate_only':ee*GSI*mass/(2*ro*c*c)}
radials=[]
for fix,ee in itertools.product(fixtures,[.1,1/3]):
    rows=[radial(*fix,ee,N,outer) for N,outer in [(8001,1e4),(16001,1e4),(16001,1e5)]]
    base=rows[-1]['frozen_PDE_abs_delta_lna_at_observation']
    radials.append({'fixture':fix[0],'eta':ee,'runs':rows,'resolution_relative_change':abs(rows[0]['frozen_PDE_abs_delta_lna_at_observation']/rows[1]['frozen_PDE_abs_delta_lna_at_observation']-1),
                    'outer_relative_change':abs(rows[1]['frozen_PDE_abs_delta_lna_at_observation']/base-1)})

inputs=json.loads((ROOT/'inputs.json').read_text())
unchanged={}
for row in inputs['files']:
    unchanged[row['path']]=hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
assert all(unchanged.values())
output={'symbolic_identities_verified':True,'minimum_ratio_2h_to_D':'50/81 at u=2',
        'matrix_cases':ncase,'precision_decimal_digits':mp.mp.dps,'minimum_K_lock_in_cases':str(min_K),
        'max_relative_direct_matrix_vs_formula':str(worst_match),
        'max_relative_antihermitian_before_roundoff_projection':str(max_anti),
        'controls':{'simple_CT14_K_lock_at108p9_eta0p05':str(simple_lock),'same_scalar_only_K_free':str(simple_free),
                    'exponential_clock_kinetic_x2':str(exp_d/(1-exp_d)),
                    'slow_kernel_K_lock_x1e6_eta2over3':str(bad_slow)},
        'radial_frozen_PDE_fixtures':radials,
        'unscreened_solar_delta_g_asymptote_m_per_s2':math.sqrt(A0*GSI*MS/AU**2/2),
        'original_inputs_unchanged':unchanged,
        'non_claims':['No data fit or kappa derivation.','Matrix proof is the aligned timelike frozen PN principal reduction, not full covariant constraint closure.',
                      'Positive scalar kinetic matrix does not prove metric-cone causality; a parallel fast mode is superluminal.',
                      'Radial response holds g fixed, includes a uniform toy baryon core, and solves a specified first-order quasi-static PDE; it is not a coupled screened galaxy/Solar solution.',
                      'No inherited SPARC, lensing, Solar-System, matter-growth or caustic pass.']}
args.output.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'matrix_cases':ncase,'controls':output['controls'],'radial_max_dln':max(q['runs'][-1]['frozen_PDE_abs_delta_lna_at_observation'] for q in radials),
                  'max_resolution_change':max(q['resolution_relative_change'] for q in radials),
                  'max_outer_change':max(q['outer_relative_change'] for q in radials)},indent=2))
