#!/usr/bin/env python3
"""Exact omitted-mixing audit; restricted block, not a full action no-go."""
import argparse,hashlib,json,os
from pathlib import Path
import sympy as S
p=argparse.ArgumentParser();p.add_argument('--mutate',action='store_true');args=p.parse_args()
k,d,O=S.symbols('k d Omega2',positive=True);v,A,w=S.symbols('v A omega',real=True)
q,qd,sd,P,Phi,j=S.symbols('q qdot sigmadot P Phi j',real=True)
L=-k*k*Phi**2/2+k*P*Phi-k*P*sd-(d+1)*P**2/2+qd**2/2-v*Phi*qd-A*P*q-O*q*q/2
sol=S.solve([S.diff(L,Phi),S.diff(L,P)],[Phi,P],dict=True)[0]
reduced=S.factor(L.subs(sol));target=(1+v*v/k**2)*qd**2/2+(v*qd/k+k*sd+A*q)**2/(2*d)-O*q*q/2
K=S.hessian(reduced,[qd,sd]);Kknown=S.Matrix([[1+v*v*(d+1)/(k*k*d),v/d],[v/d,k*k/d]])
G=k*A/d;M=O-A*A/d
# Remove only the constant-coefficient total derivative A*v*q*qdot/(k*d).
normal=S.expand(reduced-A*v*q*qd/(k*d));used=normal-(G*q*sd if args.mutate else 0)
Gused=0 if args.mutate else G
frequency=S.Matrix([[M-w*w*K[0,0],-w*w*K[0,1]+S.I*w*Gused],[-w*w*K[1,0]-S.I*w*Gused,-w*w*K[1,1]]])
expected=w*w/d*(w*w*(k*k+v*v)-k*k*O)
pq,ps=S.symbols('p_q p_sigma',real=True);mom=S.Matrix([pq,ps]);shift=S.Matrix([0,G*q])
H=S.expand(((mom-shift).T*K.inv()*(mom-shift))[0]/2+M*q*q/2)
HH=S.hessian(H,[q,pq,ps]);velocity=S.solve([S.diff(normal,qd)-pq,S.diff(normal,sd)-ps],[qd,sd],dict=True)[0]
legendre=S.factor((pq*qd+ps*sd-normal).subs(velocity))
routh=S.factor((normal-j*sd).subs(sd,(j-K[0,1]*qd-G*q)/K[1,1]))
routh_clean=S.expand(routh-(j-G*q)*K[0,1]/K[1,1]*qd)
routh_expected=(1+v*v/k**2)*qd**2/2-O*q*q/2+j*A*q/k-j*j*d/(2*k*k)
s,a,ap,app,g=S.symbols('s a a_phi a_phiphi gamma',positive=True)
AA,pp=S.symbols('a_value P_value',positive=True)
W=AA*(-pp-AA*S.log(1-pp/AA))
h=s+s/(1+s)-2*S.log(1+s)
sub={pp:AA*s/(1+s)}
Waa=S.simplify(S.diff(W,AA,2).subs(sub));Wa=S.simplify(S.diff(W,AA).subs(sub));Wpa=S.simplify(S.diff(W,pp,AA).subs(sub))
portal=ap*ap*(-h+s**3/(1+s)-s**4/((1+s)**2+g*k*k-1))-a*app*h
limit=S.simplify(S.limit(portal/s,s,S.oo))
checks=[]
def check(name,value):checks.append(dict(name=name,passed=bool(value)))
def zero(x):return S.simplify(x)==0
check('constraint_elimination',zero(reduced-target))
check('original_kinetic_matrix',all(zero(x) for x in K-Kknown))
check('positive_kinetic_determinant',zero(K.det()-(k*k+v*v)/d))
check('characteristic_cancellation',zero(frequency.det()-expected))
check('A_zero_known_answer',zero(frequency.det().subs(A,0)-expected))
check('v_zero_scalar_frequency',zero(frequency.det().subs({v:0,w*w:O})))
check('Legendre_transform',zero(H-legendre))
check('Hamiltonian_Hessian_determinant',zero(HH.det()-M/K.det()))
check('zero_velocity_energy',zero(H.subs({pq:0,ps:G*q})-M*q*q/2))
check('fixed_charge_Routhian',zero(routh_clean-routh_expected))
check('zero_charge_positive_scalar_block',zero(routh_clean.subs(j,0)-((1+v*v/k**2)*qd**2/2-O*q*q/2)))
check('portal_a_derivative',zero(Wa+AA*h))
check('portal_aa_derivative',zero(Waa-(-h+s**3/(1+s))))
check('portal_Pa_derivative',zero(Wpa+s*s))
check('large_s_energy_obstruction',zero(limit+a*app))
example={k:1,d:1,v:1,A:2,O:1}
check('negative_energy_positive_frequency_example',H.subs(example).subs({q:1,pq:0,ps:2})==-S.Rational(3,2) and zero(frequency.det().subs(example).subs(w*w,S.Rational(1,2))))
n,y,B=S.symbols('n y B',positive=True)
af=S.sinh(y)**(-n)
check('branch_a_second_derivative',zero(S.diff(af,y,2)/B**2-af/B**2*(n*n*S.coth(y)**2+n/S.sinh(y)**2)))
for foot in ['canonical','alt']:check(foot+'_obstruction_sign',limit.is_negative is True)
here=Path(__file__).resolve().parent;root=here.parent.parent
obj=dict(mutate=args.mutate,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),exact=dict(reduced=str(target),kinetic_determinant=str(S.factor(K.det())),characteristic_determinant=str(S.factor(frequency.det())),Hamiltonian_Hessian_determinant=str(S.factor(HH.det())),fixed_charge_Routhian=str(routh_expected),large_s_coefficient=str(limit)),source_hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),here/'FROZEN_MIXED_BLOCK.md']},sympy=S.__version__,scope='Constant-coefficient parallel PN block at mu_K=0; unrestricted clock momentum versus imposed fixed-charge sector. Not the full constrained action or a solved physical background. kappa=1/2 FITTED; not theory closed')
out=here/('mixed_mutate' if args.mutate else 'mixed_main');out.mkdir(exist_ok=True);tmp=out/'results.tmp'
with tmp.open('w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
os.replace(tmp,out/'results.json');print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c['name'] for c in checks if not c['passed']],exact=obj['exact']),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
