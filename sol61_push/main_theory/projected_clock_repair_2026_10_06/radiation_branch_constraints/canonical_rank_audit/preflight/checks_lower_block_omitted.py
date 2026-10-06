#!/usr/bin/env python3
"""Exact canonical auxiliary reduction plus a bounded rank-crossing fixture."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['none','chart','legendre'],default='none');args=ap.parse_args();rows=[]
def eq(n,x):
 z=s.factor(s.cancel(x));rows.append(dict(name=n,passed=z==0,residual=str(z)))
def ck(n,x,detail):rows.append(dict(name=n,passed=bool(x),detail=detail))
A,B,D,G,g,j=s.symbols('A B D Gamma g j',positive=True);ell,e=s.symbols('ell e',real=True)
w,ch,wd,cd,ng,nh,u,pw,pc=s.symbols('w chi wdot chidot ng nh u pw pchi',real=True)
L=A*(wd-e*w-ng)**2+B*ng**2+D*nh**2+2*g*(u+ch)*ng+2*j*u*nh+G*(cd+e*w-ell*u+ng-nh)**2-g*e*w**2
vel={wd:pw/(2*A)+ng+e*w,cd:pc/(2*G)+ell*u-ng+nh-e*w}
eq('momentum_w',s.diff(L,wd).subs(vel)-pw);eq('momentum_chi',s.diff(L,cd).subs(vel)-pc)
Hraw=s.expand((pw*wd+pc*cd-L).subs(vel));aa=pw-pc-2*g*ch
base=pw**2/(4*A)+pc**2/(4*G)+e*w*(pw-pc)+g*e*w**2
expected=base+aa*ng+pc*nh+ell*pc*u-B*ng**2-D*nh**2-2*g*u*ng-2*j*u*nh
eq('raw_Legendre',Hraw-expected)
C=s.Matrix([[B,0,g],[0,D,j],[g,j,0]]);eq('canonical_aux_hessian',sum(s.hessian(Hraw,[ng,nh,u])/2+C));eq('canonical_aux_det',C.det()+B*j*j+D*g*g)
S=g*g/B+j*j/D;z=g*aa/B+j*pc/D-ell*pc
us=z/(2*S);sol={u:us,ng:(aa-2*g*us)/(2*B),nh:(pc-2*j*us)/(2*D)}
for x in [ng,nh,u]:eq('canonical_secondary_'+str(x),s.diff(Hraw,x).subs(sol))
H=base+aa**2/(4*B)+pc**2/(4*D)-z**2/(4*S)
if args.control=='legendre':H=base+aa**2/(4*B)+pc**2/(4*D)+z**2/(4*S)
eq('actual_reduced_H',H-Hraw.subs(sol))
# Envelope theorem, no velocity auxiliary inverse.
for x in [w,ch,pw,pc]:eq('Hamilton_envelope_'+str(x),s.diff(H,x)-s.diff(Hraw,x).subs(sol))
Cl=s.Matrix([[A+B+G,-G,g-G*ell],[-G,D+G,j+G*ell],[g-G*ell,j+G*ell,G*ell**2]])
Hpp=s.hessian(H,[pw,pc]);eq('velocity_chart_det_relation',Hpp.det()+Cl.det()/(4*A*G*(B*j*j+D*g*g)))
# Dirac bracket matrix for primary auxiliary momenta and secondary rows.
HH=s.hessian(Hraw,[ng,nh,u]);O=s.zeros(3);Dirac=O.row_join(-HH).col_join(HH.row_join(O))
eq('Dirac_second_class_det',Dirac.det()-64*(B*j*j+D*g*g)**2)
# Canonical coordinate potential is positive for actual radiation e>0.
Vq=s.factor(H.subs({pw:0,pc:0}));eq('coordinate_potential',Vq-(g*e*w*w+g*g*j*j*ch*ch/(B*j*j+D*g*g)))
# A single exact admitted instantaneous fixture; not a time-evolution health survey.
p=s.symbols('p',positive=True)
fix={A:18,B:36,D:9,g:2*p,j:p/32,G:5*p/16,ell:s.Rational(45,8),e:3}
poly=21125*p*p-348912*p-78732000
Dfix=s.factor(Cl.det().subs(fix));eq('fixture_velocity_chart_det',Dfix+p*poly/16384)
root=(348912+s.sqrt(348912**2+4*21125*78732000))/(2*21125)
Hp=s.factor(H.subs(fix));Hp0=s.hessian(Hp,[pw,pc]);eq('fixture_zero_momentum_det',s.factor(Hp0.det()).subs(p,root))
if args.control=='chart':eq('false_physical_constraint_rank_zero',C.det().subs(fix).subs(p,root))
# Finite phase matrices through the crossing; all four coordinates are retained.
J=s.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
F=s.lambdify(p,J*s.hessian(Hp,[w,ch,pw,pc]),'numpy');pr=float(root);sample=[]
for d in [-1e-5,0,1e-5]:
 mat=np.asarray(F(pr*(1+d)),dtype=float);ev=np.linalg.eigvals(mat)
 ck('finite_phase_matrix_'+str(d),np.isfinite(mat).all() and np.isfinite(ev).all(),dict(p=pr*(1+d),norm=float(np.linalg.norm(mat)),eigenvalues=[[float(x.real),float(x.imag)] for x in ev]))
 sample.append(mat)
ck('bounded_crossing_continuity',np.linalg.norm(sample[2]-sample[0])/np.linalg.norm(sample[1])<1e-3,float(np.linalg.norm(sample[2]-sample[0])/np.linalg.norm(sample[1])))
r=dict(passed=sum(x['passed'] for x in rows),total=len(rows),checks=rows,control=args.control,fixture_root=pr,scope='exact quadratic canonical constraints k>0; bounded instantaneous on-shell coefficient fixture, not physical time-evolution stability')
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['passed','total','fixture_root']}));raise SystemExit(r['passed']!=r['total'])
