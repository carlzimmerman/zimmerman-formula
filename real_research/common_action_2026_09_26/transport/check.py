#!/usr/bin/env python3
"""Bounded exact field transport identities and homogeneous conservative controls."""
import argparse,json,math
from pathlib import Path
import sympy as S
import numpy as np
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
checks={}
def exact(name,expr):
 v=S.simplify(S.expand(expr));assert v==0,(name,v);checks[name]='exact zero'
def yes(name,p):
 assert bool(p),name;checks[name]=True
R,s,m2,mu2,lr,ls,g2,k2,y,Om=S.symbols('R s m2 mu2 lr ls g2 k2 y Om',real=True)
V=m2*R**2/2+lr*R**4/4+mu2*s**2/2+ls*s**4/4-g2*R**2*s**2/2
exact('bounded potential square completion',V-(m2*R**2/2+mu2*s**2/2+ls*(s**2-g2*R**2/ls)**2/4+(lr-g2**2/ls)*R**4/4))
exact('radial force',S.diff(V,R)-R*(m2+lr*R**2-g2*s**2))
exact('transition force',S.diff(V,s)-s*(mu2+ls*s**2-g2*R**2))
exact('invariant s zero',S.diff(V,s).subs(s,0))
exact('s threshold mass',S.diff(V,s,2).subs(s,0)-(mu2-g2*R**2))
u=S.symbols('u',real=True)
s2star=(g2*R**2-mu2)/ls
Vstar=S.expand(V).subs(s**4,u**2).subs(s**2,u).subs(u,s2star)
release=(g2*R**2-mu2)**2/(4*ls)
exact('fixed R release',V.subs(s,0)-Vstar-release)
exact('broken angular speed',S.diff(V,R)/R-(m2+lr*R**2-g2*s**2))
a=2*lr*R**2;d=2*ls*s**2;b=-2*g2*R*s
exact('broken radial Hessian',S.diff(V,R,2)-(m2+lr*R**2-g2*s**2)-a)
exact('broken real Hessian',(S.diff(V,s,2)-d).subs(mu2,g2*R**2-ls*s**2))
exact('broken mixed Hessian',S.diff(V,R,s)-b)
exact('broken determinant',a*d-b*b-4*R**2*s**2*(lr*ls-g2*g2))
chi,sig,pc,pz,ps,z,omega=S.symbols('chi sig pc pz ps z omega',real=True)
energy=((pz-2*omega*chi)**2+pc**2+ps**2+k2*(chi**2+z**2+sig**2)+a*chi**2+2*b*chi*sig+d*sig**2)/2
square=(pz-2*omega*chi)**2/2+(pc**2+ps**2+k2*(chi**2+z**2+sig**2))/2+d*(sig+b*chi/d)**2/2+(a-b*b/d)*chi**2/2
exact('positive broken Hamiltonian squares',energy-square)
exact('broken radial Schur',a-b*b/d-2*R**2*(lr-g2*g2/ls))
# Cartesian current, local mechanical energy and sector exchange.
f1,f2,p1,p2,sd=S.symbols('f1 f2 p1 p2 sd',real=True)
r2=f1*f1+f2*f2;F=m2+lr*r2-g2*s*s;Fs=mu2+ls*s*s-g2*r2
acc1,acc2,accs=-F*f1,-F*f2,-Fs*s
exact('cartesian charge derivative',f1*acc2-f2*acc1)
Vc=V.subs(R**2,r2).subs(R**4,r2**2)
exact('homogeneous total energy',p1*acc1+p2*acc2+sd*accs+S.diff(Vc,f1)*p1+S.diff(Vc,f2)*p2+S.diff(Vc,s)*sd)
Edot_phi=p1*acc1+p2*acc2+(m2+lr*r2)*(f1*p1+f2*p2)
Edot_s=sd*accs+(mu2+ls*s*s)*s*sd
Edot_int=-g2*s*s*(f1*p1+f2*p2)-g2*r2*s*sd
exact('bare complex energy exchange',Edot_phi-g2*s*s*(f1*p1+f2*p2))
exact('bare real energy exchange',Edot_s-g2*r2*s*sd)
exact('interaction energy closes balance',Edot_phi+Edot_s+Edot_int)
# Generic preferred foliation energy accounting; spatial flux is handled analytically.
A,B,At,Bt,vel,vv,W,Wq=S.symbols('A B At Bt vel vv W Wq',real=True)
Eprime=At*vel**2/2+A*vel*(-At*vel-B*Wq)/A+Bt*W+B*Wq*vel
exact('generic A B energy exchange',Eprime-(-At*vel**2/2+Bt*W))
Z=S.symbols('Z',real=True)
L=S.exp(Z)*vel**2/2-S.exp(-Z)*W
rho=S.exp(Z)*vel**2/2+S.exp(-Z)*W
exact('exponential gate derivative equals energy',S.diff(L,Z)-rho)
exact('exponential speed',S.exp(-Z)/S.exp(Z)-S.exp(-2*Z))
# Exact envelope equation before dropping psi_tt, using independent jets.
M,n,psi,pt,ptt,lap=S.symbols('M n psi pt ptt lap',nonzero=True)
KG=ptt-2*S.I*M*pt-lap+(lr*n/M-g2*s*s)*psi
sch=S.I*pt-(-lap/(2*M)+(lr*n/(2*M*M)-g2*s*s/(2*M))*psi+ptt/(2*M))
exact('exact NR envelope remainder',KG+2*M*sch)
x=S.symbols('x',real=True);nf=S.Function('n',positive=True)(x)
Q=(S.diff(nf,x)**2/nf-S.diff(nf,x,2))/(4*M)
exact('one dimensional quantum stress',S.diff(Q,x)+nf/(2*M)*S.diff(S.diff(S.sqrt(nf),x,2)/S.sqrt(nf),x))
# Exact two-mode free solution: a regular Cartesian field need not define timelike phase.
AA,BB,kk,ww=S.symbols('AA BB kk ww',positive=True)
spacelike=(kk*(AA+BB))**2-(ww*(AA-BB))**2
sample=spacelike.subs({AA:1,BB:S.Rational(3,4),kk:1,ww:S.sqrt(2)})
yes('nodefree spacelike phase counterexample',sample>0)
yes('positive density lower bound counterexample',(1-S.Rational(3,4))**2>0)
# Conditional fixed-R kick budget; no trajectory or efficiency is inferred.
params={m2:1,mu2:S.Rational(1,250),lr:S.Rational(1,10000),ls:1,g2:S.Rational(1,125),R:1}
rel=S.simplify(release.subs(params));q=S.sqrt(1+S.Rational(1,10000))
yes('cold budget Hessian margin',(lr*ls-g2*g2).subs(params)>0)
yes('conditional 0.002 speed budget',2*rel/q>S.Rational(2,1000)**2)
# Independent finite normal-mode check for one broken-branch witness.
roots={}
for kp in [0,0.01,1,100]:
 # R=1,s=.5,m²=1,lr=ls=2,g²=1,mu²=.5 => Om²=2.75,a4,d1,b-1.
 poly=((y-kp)*(y-kp-4)-11*y)*(y-kp-1)-(y-kp)
 vals=np.sort(np.real_if_close(np.roots([float(c)for c in S.Poly(poly,y).all_coeffs()])))
 yes('three real nonnegative roots k2='+str(kp),np.max(abs(np.imag(vals)))<1e-9 and np.min(np.real(vals))>=-1e-10)
 if kp>0:yes('strict roots k2='+str(kp),np.min(vals)>0)
 roots[str(kp)]=[float(v)for v in vals]
# Homogeneous finite-volume mode: energy/charge conserved, no spatial evacuation possible.
def potential(f1,f2,s):
 r=f1*f1+f2*f2
 return .5*r+.5*r*r+.25*s*s+.5*s**4-.5*r*s*s

def rhs(t,Y):
 f1,f2,s,p1,p2,ps=Y;r=f1*f1+f2*f2
 return [p1,p2,ps,-(1+2*r-s*s)*f1,-(1+2*r-s*s)*f2,-(.5+2*s*s-r)*s]

def invariants(Y):
 f1,f2,s,p1,p2,ps=Y
 return .5*(p1*p1+p2*p2+ps*ps)+potential(f1,f2,s),f1*p2-f2*p1
initial=np.array([1,0,.001,0,math.sqrt(3),0.])
times=np.linspace(0,60,3001)
sol=solve_ivp(rhs,[0,60],initial,method='DOP853',rtol=2e-12,atol=2e-13,t_eval=times)
yes('homogeneous solver completed',sol.success)
E,J=invariants(sol.y);driftE=float(max(abs(E-E[0]))/E[0]);driftJ=float(max(abs(J-J[0]))/J[0])
yes('energy relative tolerance',driftE<1e-9);yes('charge relative tolerance',driftJ<1e-9)
yes('seeded transition grows',max(abs(sol.y[2]))>.1)
# Reversing all canonical velocities exactly reverses this autonomous field ODE.
rev=sol.y[:,-1].copy();rev[3:]*=-1
back=solve_ivp(rhs,[0,60],rev,method='DOP853',rtol=2e-12,atol=2e-13,t_eval=[60])
target=initial.copy();target[3:]*=-1
rev_error=float(max(abs(back.y[:,-1]-target)))
yes('Hamiltonian time reversal control',back.success and rev_error<1e-7)
# No seed is an exact invariant solution even above threshold.
unseeded=initial.copy();unseeded[2]=0
zero=solve_ivp(rhs,[0,10],unseeded,method='DOP853',rtol=2e-12,atol=2e-13,t_eval=[10])
yes('unseeded transition remains zero',zero.y[2,-1]==0 and zero.y[5,-1]==0)
# A random isotropic prescribed kick changes energy on average, with no reservoir in L377.
vx,vy,vz,nx,ny,nz,vk=S.symbols('vx vy vz nx ny nz vk',real=True)
kick=((vx+vk*nx)**2+(vy+vk*ny)**2+(vz+vk*nz)**2-vx*vx-vy*vy-vz*vz)/2
exact('kick energy identity',kick-vk*(vx*nx+vy*ny+vz*nz)-vk*vk*(nx*nx+ny*ny+nz*nz)/2)
out={'result':'bounded transport identities and conservative field controls accepted','checks':checks,'check_count':len(checks),
 'broken_branch_frequency_squared':roots,'homogeneous':{'interval':[0,60],'samples':len(times),'energy_relative_error':driftE,'charge_relative_error':driftJ,'max_abs_s':float(max(abs(sol.y[2]))),'time_reversal_max_error':rev_error},
 'conditional_cold_budget':{'m2':1,'R2':1,'lambda_R':'1/10000','lambda_s':1,'g2':'1/125','mu2':'1/250','fixed_R_release':str(rel),'charge':str(q),'v_if_all_release_to_carrier_kinetic':math.sqrt(float(2*rel/q))},
 'non_claims':['No field-derived Poisson decay law or kick distribution','No demonstrated halo clearing','No timelike phase for arbitrary field data','No global coupled-gravity existence theorem','No observational fit','No global gravitational constraints proved']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
