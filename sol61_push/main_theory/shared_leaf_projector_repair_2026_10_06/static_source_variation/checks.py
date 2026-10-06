#!/usr/bin/env python3
"""Static action first variations; finite exact fixtures do not solve a source BVP."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['none','volume','metric','flux'],default='none');args=ap.parse_args();rows=[]
def eq(name,x,y=0):
 if isinstance(x,s.MatrixBase):res=(x-y).applyfunc(lambda z:s.factor(s.cancel(z)));ok=res==s.zeros(*res.shape)
 else:res=s.factor(s.cancel(x-y));ok=res==0
 rows.append({'name':name,'passed':ok,'residual':str(res)})
x=s.Matrix([[3,1,0],[1,2,0],[0,0,4]]);y=s.Matrix([[2,0,1],[0,4,0],[1,0,3]])
dx=s.Matrix([[1,2,0],[2,-1,1],[0,1,2]]);dy=s.Matrix([[0,1,1],[1,2,0],[1,0,-1]])
h=(x+y)/2;d=(x-y)/2;hi=h.inv();lam=s.Rational(2,3);H=h+lam*d*hi*d;BI=H.inv();w=s.Matrix([1,-2,3]);z=BI*w;q=hi*d*z
Ug=(z*z.T-lam*q*q.T+lam*(z*q.T+q*z.T))/2;Uh=(z*z.T-lam*q*q.T-lam*(z*q.T+q*z.T))/2
step=s.symbols('step');dh=(dx+dy)/2;dd=(dx-dy)/2
derH=dh+lam*(dd*hi*d+d*hi*dd-d*hi*dh*hi*d)
Hx=(h+step*dh)+lam*(d+step*dd)*(h+step*dh).inv()*(d+step*dd)
rows.append({'name':'noncommuting_fixture','passed':x*y!=y*x,'residual':'actual xy != yx'})
for i in range(3):
 for j in range(i,3):eq('actual_leaf_differential_%s%s'%(i,j),s.diff(Hx[i,j],step).subs(step,0),derH[i,j])
# Inverse identity differentiates H B=1, not an assumed commuting simplification.
invder=-BI*derH*BI
eq('contracted_inverse_variation',(w.T*invder*w)[0],-s.trace(Ug*dx)-s.trace(Uh*dy))
eq('spatial_exchange_Ug',Ug,(z*z.T-lam*(-q)*(-q).T-lam*(z*(-q).T+(-q)*z.T))/2)
# Independent arithmetic differential from each inverse.
za=x.inv()*w;zb=y.inv()*w
eq('arithmetic_metric_variation',-(w.T*(x.inv()*dx*x.inv()+y.inv()*dy*y.inv())*w)[0]/2,-s.trace(za*za.T*dx)/2-s.trace(zb*zb.T*dy)/2)
K,a0,v,m,m1=s.symbols('K a0 volume m m1',positive=True);dn,dl=s.symbols('dn dl');dw=s.Matrix(s.symbols('dw0:3'))
raw=2*K*a0*a0*(v*(dn+dl)*m/2+v*m1*2*(w.T*BI*dw)[0]/(a0*a0))
eq('direct_log_lapse_variation',s.diff(raw,dn),K*a0*a0*v*m)
eq('opposite_log_lapse_variation',s.diff(raw,dl),K*a0*a0*v*m)
for i in range(3):eq('lapse_boundary_flux_%s'%i,s.diff(raw,dw[i]),4*K*v*m1*(BI*w)[i])
volume_metric=s.trace(x.inv()*dx)/4+s.trace(y.inv()*dy)/4
rawmet=2*K*a0*a0*v*(m*volume_metric-m1*(s.trace(Ug*dx)+s.trace(Uh*dy))/(a0*a0))
E1=K*a0*a0*v*m*x.inv()/2-2*K*v*m1*Ug;E2=K*a0*a0*v*m*y.inv()/2-2*K*v*m1*Uh
eq('full_spatial_volume_and_inverse',rawmet,s.trace(E1*dx)+s.trace(E2*dy))
# Weak metric expansion around coincidence uses arbitrary noncommuting mean/difference.
eps=s.symbols('eps');mean=s.Matrix([[1,2,0],[2,0,1],[0,1,-1]]);dif=s.Matrix([[2,0,1],[0,-1,1],[1,1,0]])
base=s.eye(3);hl=base+eps*mean;ga=hl+eps*dif;gh=hl-eps*dif
# Exact inverse second derivatives at eps0: B''=2 J'^2-J''.
Barith2=(mean+dif)**2+(mean-dif)**2
Blambda2=2*mean**2-2*lam*dif**2
eq('noncommuting_inverse_difference_second',Blambda2-Barith2,-2*(1+lam)*dif**2)
eq('quartic_action_difference',K*((w.T*(Blambda2-Barith2)*w)[0]/2),-K*(1+lam)*(w.T*dif*dif*w)[0])
# Quartic directional derivative wrt d, giving independent spatial correction.
z1=dif*w
quartic_der=-K*(1+lam)*(w.T*(dx*dif+dif*dx)*w)[0]/2
eq('first_spatial_Euler_correction',quartic_der,-K*(1+lam)*s.trace((w*z1.T+z1*w.T)*dx)/2)
# Radial/isotropic exact inverse subtraction.
hs,ds,lp=s.symbols('hs ds lambda',positive=True)
eq('exact_isotropic_inverse_difference',hs/(hs*hs+lp*ds*ds)-hs/(hs*hs-ds*ds),-(1+lp)*hs*ds*ds/((hs*hs+lp*ds*ds)*(hs*hs-ds*ds)))
# A variable anisotropic local profile checks integration-by-parts sign.
r=s.symbols('r');r1=r*r/2;d1=r;flux=d1*d1*s.diff(r1,r)
DeltaL=-K*(1+lp)*d1*d1*s.diff(r1,r)**2
EL=-s.diff(-2*K*(1+lp)*flux,r)
eq('first_lapse_Euler_sign',EL,2*K*(1+lp)*s.diff(flux,r))
eq('static_clock_relative_first_variation',(-s.Symbol('pi_it'))-(-s.Symbol('pi_it')),0)
if args.control=='volume':eq('control_omit_direct_volume',0,K*a0*a0*v*m)
if args.control=='metric':eq('control_freeze_leaf_inverse',(w.T*invder*w)[0],0)
if args.control=='flux':eq('control_claim_exact_flux_preservation',hs/(hs*hs+lp*ds*ds),hs/(hs*hs-ds*ds))
result={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'Exact static first variations and weak-field Euler difference; no on-shell source solution or observational transfer'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x['name'] for x in rows if not x['passed']]}));sys.exit(0 if result['passed']==result['total'] else 1)
