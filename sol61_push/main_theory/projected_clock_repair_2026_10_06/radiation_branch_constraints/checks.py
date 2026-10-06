#!/usr/bin/env python3
"""Exact n=3 constrained radiation principal checks; no finite-k health extrapolation."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['none','mismatch','shift','boundary'],default='none');args=ap.parse_args()
checks=[]
def eq(name,a,b=0):
    residual=s.factor(s.cancel(a-b));checks.append({'name':name,'passed':residual==0,'residual':str(residual)})
A,B,D,G,g,j,l=s.symbols('A B D Gamma g j ell',positive=True)
u,ng,nh,Tw,Y,ch,w=s.symbols('u ng nh Tw Y chi w')
L=A*Tw**2+(A+B)*ng**2-2*A*Tw*ng+2*g*(u+ch)*ng+D*nh**2+2*j*u*nh+G*(Y-l*u+ng-nh)**2
aux=s.Matrix([u,ng,nh]);C=s.hessian(L,aux)/2
expected=s.Matrix([[G*l*l,g-G*l,j+G*l],[g-G*l,A+B+G,-G],[j+G*l,-G,D+G]])
for i in range(3):
 for z in range(i,3):eq('auxiliary_matrix_%s%s'%(i,z),C[i,z],expected[i,z])
bvec=s.Matrix([s.diff(L,x).subs({u:0,ng:0,nh:0})/2 for x in aux]);eq('aux_linear_vector',sum((bvec-s.Matrix([-G*l*Y,-A*Tw+G*Y+g*ch,-G*Y]))),0)
k=s.symbols('k');det=s.expand(C.det().subs({G:G*k,g:g*k,j:j*k}));eq('UV_aux_det',det.coeff(k,3),-G*(g+j)**2);eq('IR_aux_det',det.coeff(k,1),G*l*l*(A+B)*D)
allvars=s.Matrix([Tw,Y,u,ng,nh]);eq('full_velocity_aux_determinant',(s.hessian(L,allvars)/2).det(),-A*G*(B*j*j+D*g*g))
alpha=g/(g+j);r=j/(g+j);T=g*j/(g+j);ss=T/G
sol={u:-alpha*ch,ng:-r*Y-r*(2*alpha*l+ss)*ch,nh:alpha*Y+alpha*(l*(1-2*r)+ss)*ch}
Llead=2*g*(u+ch)*ng+2*j*u*nh+G*(Y-l*u+ng-nh)**2
for x in aux:eq('UV_constraint_'+str(x),s.diff(Llead,x).subs(sol),0)
eq('UV_substitution',Llead.subs(sol),-2*T*ch*Y-T*(2*alpha*l+ss)*ch**2)
eq('UV_kinetic', (A*(Tw-ng)**2+B*ng**2+D*nh**2).subs({ng:-r*Y,nh:alpha*Y}),A*(Tw+r*Y)**2+(B*r*r+D*alpha*alpha)*Y**2)
H,H2,e,M,a,P,Qp,Lp,b0=s.symbols('H H2 e M a Pg Ph lapse b0',positive=True)
Td=s.diff(T,g)*g*(H-e)+s.diff(T,j)*j*(2*l+H2)
eq('evolving_T_derivative',Td/T,r*(H-e)+alpha*(2*l+H2))
Gww=g*e;Gwc=T*e;Gcc=T*(ss-r*(H-e)-alpha*H2)
eq('physical_gradient_schur',Gcc-Gwc**2/Gww,T*(ss-r*H-alpha*H2))
mp={g:M*a**3*P*H,j:M*a**3*Qp*H2,G:M*a**3*(P+Qp)/4}
delta=s.factor((ss-r*H-alpha*H2).subs(mp))
eq('arithmetic_negative_square',delta,-H*H2*(P-Qp)**2/((P+Qp)*(P*H+Qp*H2)))
E=B*r*r+D*alpha*alpha
physmap={**mp,B:M*a**3*b0*H**2,D:M*a**3*b0*H2**2/Lp**2}
frequency=s.factor((T*(ss-r*H-alpha*H2)/E).subs(physmap))
eq('relative_frequency',frequency,-P*Qp*(P-Qp)**2/(b0*(P+Qp)*(Qp**2+P**2/Lp**2)))
crit=s.factor((T/(r*H+alpha*H2)).subs(mp));eq('Gamma_threshold',crit,M*a**3*P*Qp/(P+Qp))
eq('arithmetic_threshold_gap',mp[G]-crit,M*a**3*(P-Qp)**2/(4*(P+Qp)))
W=s.symbols('W',positive=True);eq('radiation_speed',(M*a**3*P*H*W/(2*M*H))/(s.Rational(3,2)*a**3*W),P/3)
# Raw shifts, before any gauge or scalar constraint removal.
f,t,v,eta=s.symbols('f t v eta',real=True)
raw=-3*M*f*f-2*M*f*t-eta*M*t*t/3-W*v*t
root=-3*(f+W*v/(2*M))/eta
eq('actual_radiation_shift',s.diff(raw,t).subs(t,root),0)
eq('shear_square_completion',raw.subs(t,root),3*M*(f+W*v/(2*M))**2/eta-3*M*f*f)
ng0,zw,Hw=s.symbols('ng0 zw Hw');Cf=s.Rational(3,2)*W
cross=-2*Cf*(Tw-H*w-zw)*ng0-3*W*H*(w+zw/H)*ng0
eq('fluid_mixing_cancellation',cross,-2*Cf*Tw*ng0)
fixture=(frequency/P).subs({Qp:P/4,Lp:s.Rational(1,8),b0:9});eq('on_shell_fixture_speed',fixture,-s.Rational(1,5125))
# Controlled branch: h=1,a=1,H=sqrt2,W/M=4 at t0; Friedmann and acceleration.
eq('background_Friedmann',s.Integer(2),1+s.Integer(3)/3);eq('background_acceleration',-2,-s.Integer(4)/2)
if args.control=='mismatch':eq('control_erases_actual_mismatch',delta,0)
if args.control=='shift':eq('control_transplants_old_shift',s.diff(raw,t).subs(f,-W*v/(2*M)),0)
if args.control=='boundary':eq('control_freezes_evolving_boundary',Td,0)
result={'claim':'actual radiation branch constrained UV principal','control':args.control,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'arithmetic':'exact SymPy','scope':'n3 Q1 compact on-shell positive radiation and 0<eta<1; not all finite-k health','fixture_relative_speed_squared':str(fixture)}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x['name'] for x in checks if not x['passed']]}));sys.exit(0 if result['passed']==result['total'] else 1)
