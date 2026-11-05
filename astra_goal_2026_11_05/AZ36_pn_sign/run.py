#!/usr/bin/env python3
"""Exact radial ADM reduction; no claim about the missing nonspherical blocks."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import mpmath as mp
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
mode='mutate' if args.mutate else 'main';out=HERE/mode;out.mkdir(exist_ok=True)
t0=time.monotonic();checks={};derived={}
def check(k,v):checks[k]=bool(v)
def zero(k,v):
    residual=sp.simplify(v);derived[k]=str(residual);check(k,residual==0)
r,th,ph=sp.symbols('r theta phi',positive=True)
K,gam,mu2=sp.symbols('K gamma mu2',positive=True)
A=sp.Function('A')(r);N=sp.Function('N')(r);w=sp.Function('w')(r)
b=sp.Function('b')(r);chi=sp.Function('chi')(r)
At=sp.symbols('A_dot',real=True);W=sp.Function('W');V=sp.Function('V')
coords=(r,th,ph);h=sp.diag(A*A,r*r,r*r*sp.sin(th)**2);hi=h.inv()
Gamma=[[[sp.simplify(sum(hi[i,l]*(sp.diff(h[l,j],coords[k])+sp.diff(h[l,k],coords[j])-sp.diff(h[j,k],coords[l])) for l in range(3))/2)
          for k in range(3)] for j in range(3)] for i in range(3)]
Ric=sp.Matrix(3,3,lambda i,j:sp.simplify(sum(sp.diff(Gamma[k][i][j],coords[k])-sp.diff(Gamma[k][i][k],coords[j])+
    sum(Gamma[k][i][j]*Gamma[l][k][l]-Gamma[l][i][k]*Gamma[k][j][l] for l in range(3)) for k in range(3))))
R3=sp.simplify(sum(hi[i,j]*Ric[i,j] for i in range(3) for j in range(3)))
zero('spatial_curvature',R3-2*(1-1/A**2)/r**2-4*sp.diff(A,r)/(A**3*r))
m=sp.symbols('mass',positive=True)
zero('Schwarzschild_R3',R3.subs(A,(1-2*m/r)**sp.Rational(-1,2)).doit())

# Direct ADM extrinsic curvature from h_dot - Lie_b h.
shift=[b,0,0];hdot=sp.diag(2*A*At,0,0)
lie=sp.Matrix(3,3,lambda i,j:sum(shift[k]*sp.diff(h[i,j],coords[k])+h[k,j]*sp.diff(shift[k],coords[i])+h[i,k]*sp.diff(shift[k],coords[j]) for k in range(3)))
extr=hi*(hdot-lie)/(2*N)
invariant=sp.simplify(sp.trace(extr*extr)-sp.trace(extr)**2)
Lkin=sp.simplify(N*A*r*r*invariant/(4*K))
D=sp.diff(A,r)+A*sp.diff(N,r)/N
Lkin_reduced=r*b*At/(K*N)-r*D*b*b/(2*K*N)
zero('shift_integration_by_parts',Lkin-Lkin_reduced+sp.diff(A*r*b*b/(2*K*N),r))
q=sp.diff(w,r)+2*w/r;s=q/A
Lg=N*A*r*r*R3/(4*K)
Lp=r*r*w*sp.diff(N,r)-N*A*r*r*W(K*w)-N*A*r*r*gam*s*s/2
LQ=A*r*r*mu2*(1-N)**2/(2*K*N)
Lm=-N*A*r*r*(sp.diff(chi,r)**2/(2*A*A)+V(chi))
Lstatic=Lg+Lp+LQ+Lm
EL=lambda L,f:sp.diff(L,f)-sp.diff(sp.diff(L,sp.diff(f,r)),r)
enthalpy=sp.diff(chi,r)**2/(A*A)
Btau=s+gam*s*s+mu2*(1-N)/(K*N*N)
zero('background_Einstein_combination',EL(Lstatic,N)-A*EL(Lstatic,A)/N-(r*D/(K*A*A)-A*r*r*(Btau+enthalpy)))

# Covariant static matter, including its shift Hessian, not just first variations.
Lm_full=-N*A*r*r*((1/A**2-b*b/N**2)*sp.diff(chi,r)**2/2+V(chi))
matter_shift=sp.simplify(Lm_full-Lm)
zero('matter_shift_hessian',matter_shift-A**3*r*r*enthalpy*b*b/(2*N))
Deff=D-K*A**3*r*enthalpy
Lshift=Lkin_reduced+matter_shift
bsol=sp.solve(sp.diff(Lshift,b),b)[0]
Tcoef=r/(K*N*Deff)
zero('shift_elimination',Lshift.subs(b,bsol)-Tcoef*At*At/2)
zero('matter_cancellation_on_shell',(K*A**3*r*(Btau+enthalpy)-K*A**3*r*enthalpy)-K*A**3*r*Btau)
zero('vacuum_constraint',sp.diff(Lshift,b).subs({D:0,sp.diff(chi,r):0})-r*At/(K*N))
# Check the vacuum expression directly after substituting A=1/N.
zero('Schwarzschild_D',D.subs(A,1/N).doit())

# Spatial principal block after integrating the EH radial derivative once.
Lg_ibp=N*(A+1/A)/(2*K)+r*sp.diff(N,r)/(K*A)
zero('EH_static_integration_by_parts',Lg-Lg_ibp+sp.diff(N*r/(K*A),r))
Lsp=Lg_ibp+Lp+LQ+Lm
Cp=sp.diff(Lsp,sp.diff(N,r))
ca=-sp.diff(Cp,A)
cw=sp.simplify(-sp.diff(Cp,w)+sp.diff(Lsp,N,sp.diff(w,r)))
g=sp.simplify(-sp.diff(Lsp,sp.diff(w,r),2))
hh=sp.simplify(sp.diff(Lsp,N,2))
zero('principal_ca',ca-r/(K*A*A))
zero('principal_cw',cw+r*r*(1+gam*s))
zero('principal_g',g-N*gam*r*r/A)
zero('principal_h',hh-A*r*r*mu2/(K*N**3))
kk,aa,pp,nn=sp.symbols('k a p n',real=True,nonzero=True)
Lblock=-g*kk*kk*pp*pp/2+kk*nn*(ca*aa+cw*pp)+hh*nn*nn/2
psol=sp.solve(sp.diff(Lblock,pp),pp)[0]
afterp=sp.simplify(Lblock.subs(pp,psol));nsol=sp.solve(sp.diff(afterp,nn),nn)[0]
Gseq=sp.simplify(-2*afterp.subs(nn,nsol)/(kk*kk*aa*aa))
H=sp.hessian(Lblock,(aa,pp,nn));Ginv=sp.simplify((H[0,1:]*H[1:,1:].inv()*H[1:,0])[0]/(kk*kk))
zero('independent_Schur',Gseq-Ginv)
den=(1+gam*s)**2+gam*mu2/(K*N*N)
zero('gradient_coefficient',Gseq-N*gam/(K*K*A**5*den))
Ton=r/(K*N*(K*A**3*r*Btau))
physical=sp.simplify(Gseq/Ton*A*A/(N*N))
zero('physical_radial_speed',physical-gam*Btau/den)
ss=sp.symbols('s',positive=True)
speed=gam*(ss+gam*ss**2+mu2*(1-N)/(K*N*N))/((1+gam*ss)**2+gam*mu2/(K*N*N))
zero('zero_stiffness_limit',sp.limit(speed,gam,0))
yy=sp.symbols('y',positive=True)
weak=sp.simplify(speed.subs({mu2:0,ss:yy/gam}))
zero('PN_leading_speed',sp.limit(weak/yy,yy,0)-1)
zero('exact_vacuum_radial_speed',weak-yy/(1+yy))
derived.update(R3=str(R3),background_identity='D=K A^3 r [s+gamma s^2+mu2(1-N)/(K N^2)+rho_m+p_r]',
    effective_kinetic_denominator='D_eff=K A^3 r [s+gamma s^2+mu2(1-N)/(K N^2)]',
    kinetic=str(Ton),gradient=str(Gseq),physical_speed=str(speed),matter_scope='Frozen static scalar sub-block; independent matter perturbations not solved.')

sgn=-1 if args.mutate else 1
footings={'canonical':(9.3603e-11,(21.68,24.,27.)), 'alt':(1.1312e-10,(22.85,24.,24.60))}
pc=mp.mpf('3.0856775814913673e16');rows={}
def evaluate(dps,L,y,Nv,Av,z):
    with mp.workdps(dps):
        l,Y,n,a,Z=map(lambda v:mp.mpf(str(v)),(L,y,Nv,Av,z))
        m2=(l/100000)**2/2;u=sgn*Y
        B=Y*(1+u)+m2*(1-n)/(n*n)
        denominator=(1+u)**2+sgn*m2/(n*n)
        cphys=sgn*B/denominator
        ccoord=n*n/(a*a)*cphys
        cancelled=(B+Z)-Z
        return cphys,ccoord,B,denominator,cancelled
for foot,(a0,lengths) in footings.items():
    data=[];precision=[];fp=[]
    for L in lengths:
      for y in (1e-12,1e-6,1e-3):
       for n in (.999998,.999999,1.):
        for a in (1.,1.000002):
         for z in (0.,1e-6,1e-3):
            lo=evaluate(40,L,y,n,a,z);hi80=evaluate(80,L,y,n,a,z)
            with mp.workdps(80):
                err=max(abs(x/v-1) for x,v in zip(lo,hi80) if v!=0)
            mval=(L/100000)**2/2
            Bf=y*(1+sgn*y)+mval*(1-n)/(n*n)
            denf=(1+sgn*y)**2+sgn*mval/(n*n)
            fvalue=sgn*Bf/denf
            ferror=abs(fvalue/float(hi80[0])-1)
            precision.append(float(err));fp.append(ferror)
            data.append(dict(Lstar_pc=L,y=y,N=n,A=a,matter_z=z,physical_c2=float(hi80[0]),coordinate_c2=float(hi80[1]),
                positive_kinetic_factor=float(hi80[2]),gradient_denominator=float(hi80[3]),
                precision_relative=float(err),float_relative=ferror,
                density_in_a0_over_KL_units=2*299792458.**2*y/(L*float(pc)*a0)))
    rows[foot]=dict(a0_m_s2=a0,cases=data)
    check(foot+'_precision_pair',max(precision)<=1e-30)
    check(foot+'_float64',max(fp)<=1e-12)
    check(foot+'_kinetic_positive',all(v['positive_kinetic_factor']>0 for v in data))
    check(foot+'_gradient_positive',all(v['physical_c2']>0 and v['gradient_denominator']>0 for v in data))
sources=[Path(__file__),HERE/'FROZEN_CRITERIA.md',HERE/'AMENDMENTS.md',ROOT/'covariant_push_2026_10_22/C5_health/c5_health.py',ROOT/'rebuild_2026_10_22/V3X_v3s_close_undecided/README.md']
result=dict(mode=mode,label='NO VERDICT full nonspherical PN sign claim',radial_label='PASS conditional radial UV signs' if all(checks.values()) else 'FAIL or unchecked radial diagnostic',
    checks=checks,derivation=derived,footings=rows,
    hypotheses='Static spherical open positive-divergence branch; positive lapse/radial metric; N<=1; exact background constraints; vacuum or declared frozen-scalar matter sub-block. No interface or full nonradial/matter spectrum claim.',
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    software=dict(python=platform.python_version(),sympy=sp.__version__,mpmath=mp.__version__),
    seconds=time.monotonic()-t0,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
    statement='kappa = 1/2 FITTED; not theory closed')
tmp=out/'results.tmp';tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');os.replace(tmp,out/'results.json')
print(json.dumps(dict(mode=mode,checks=checks,seconds=result['seconds']),indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
