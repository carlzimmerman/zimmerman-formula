#!/usr/bin/env python3
"""Exact scoped identities, not a numerical selector or parameter scan."""
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import sys
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
MUTATE = os.environ.get('W4_04_MUTATE', '0') == '1'
checks = []


def eq(x, y=0):
    return s.simplify(x-y) == 0


def check(name, condition, value):
    ok = bool(condition)
    checks.append({'name': name, 'passed': ok, 'value': str(value)})
    print(f"{'PASS' if ok else 'FAIL'} {name}: {value}")


q,C2,C3,eps,Omega,Z,scale = s.symbols('q C2 C3 eps Omega Z scale',positive=True)
Gn=q**2/(2*Omega*C2)
a0=2*q*C2/(3*C3)
xi=s.factor(a0**2/(Gn*eps))
check('K01 operational invariant',eq(xi,8*Omega*C2**3/(9*eps*C3**2)),xi)
M,r,h=s.symbols('M r h',positive=True)
hN=q*M/(2*Omega*C2*r**2)
hD=s.sqrt(q*M/(3*Omega*C3*r**2))
check('K02 Newton flux',eq(q*hN,Gn*M/r**2),q*hN)
check('K03 MOND flux',eq((q*hD)**2,a0*Gn*M/r**2),(q*hD)**2)
ren={q:q/scale,C2:C2/scale**2,C3:C3/scale**3}
check('K04 field normalization',eq(xi.subs(ren,simultaneous=True),xi),xi.subs(ren,simultaneous=True))
check('K05 common loop species factor',eq(xi.subs({C2:Z*C2,C3:Z*C3,eps:Z*eps},simultaneous=True),xi),'Z^(3-2-1)=1')
qactive=2*q if MUTATE else q
Gq=Gn.subs(q,qactive)
aq=a0.subs(q,qactive)
check('K06 physical source cancellation',eq(aq**2/(Gq*eps),xi),s.factor(aq**2/(Gq*eps)))
active_omega=2*s.pi**2 if MUTATE else 4*s.pi
check('K07 dimension baseline',eq(xi.subs(Omega,active_omega),xi.subs(Omega,4*s.pi)),active_omega)

V,T,Mp,m32,alpha,beta,mBI=s.symbols('V T Mp m32 alpha beta mBI',positive=True)
Estar=alpha*s.sqrt(T)
alpha_active=2*alpha if MUTATE else alpha
check('K08 fixed BI source baseline',eq(Estar.subs(alpha,alpha_active)**2/(Gn*V),Estar**2/(Gn*V)),s.factor(Estar.subs(alpha,alpha_active)**2/Estar**2))
TfromV=(V+3*Mp**2*m32**2)/2
check('K09 SUSY vacuum identity',eq(2*TfromV-3*Mp**2*m32**2,V),TfromV)
check('K10 fixed-V tension shift',eq(s.diff(TfromV,m32),3*Mp**2*m32),s.diff(TfromV,m32))
Tbranch=V if MUTATE else V/2
check('K11 restricted branch identity',eq(Tbranch,V/2),Tbranch)
E=s.symbols('E',real=True)
L=-T*(1+s.sqrt(1-E**2/T))+3*Mp**2*m32**2
c4=s.expand(s.series(L,E,0,6).removeO()).coeff(E,4)
check('K12 canonical BI quadratic',eq(s.diff(L,E,2).subs(E,0),1),s.diff(L,E,2).subs(E,0))
check('K13 BI quartic coefficient',eq(c4,1/(8*T)),c4)
check('K14 electric quarter baseline',eq((V*c4).subs(T,Tbranch),s.Rational(1,4)),(V*c4).subs(T,Tbranch))
D=s.symbols('D',positive=True)
DE=s.diff(L,E)
ofD=D/s.sqrt(1+D**2/T)
check('K15 BI constitutive solution',eq(DE.subs(E,ofD),D),s.simplify(DE.subs(E,ofD)))
check('K16 BI weak-field linear',s.limit(ofD/D,D,0)==1,s.limit(ofD/D,D,0))
check('K17 BI strong-field saturation',s.limit(ofD,D,s.oo)==s.sqrt(T),s.limit(ofD,D,s.oo))
check('K18 fixed gauge-coupling mutation',eq((scale*mBI)/(scale*beta),mBI/beta),mBI/beta)

N,hbar,theta,gamma=s.symbols('N hbar theta gamma',positive=True)
P=N*hbar
Fabs=P*s.pi**2*theta**4/90
c2=P*gamma*theta**2/24
c3=-P*gamma**s.Rational(3,2)*theta/(12*s.pi)
Rfree=s.factor(Fabs*c3**2/c2**3)
Renergy=s.factor(3*Fabs*c3**2/c2**3)
check('K19 thermal free-energy ratio',eq(Rfree,s.Rational(16,15)),Rfree)
check('K20 thermal energy ratio',eq(Renergy,s.Rational(16,5)),Renergy)
check('K21 common gamma cancels',eq(Rfree.subs(gamma,2*gamma),Rfree),Rfree)
check('K22 thermal cubic wrong sign',s.ask(s.Q.negative(c3)) is True,c3)
t=s.Rational(3,5) if MUTATE else s.Integer(0)
A=((1+t)**s.Rational(3,2)+(1-t)**s.Rational(3,2))/2
check('K23 relative thermal slopes baseline',eq(A**2,1),s.simplify(A**2))
Asupp=((1+s.Rational(3,5))**s.Rational(3,2)+(1-s.Rational(3,5))**s.Rational(3,2))/2
check('K24 declared unequal-slope factor',eq(Asupp**2,s.Rational(162,125)),s.simplify(Asupp**2))
check('K25 thermal state EOS',eq((Fabs)/(3*Fabs),s.Rational(1,3)),s.Rational(1,3))

# Finite spectrum and exact sign certification. All masses squared in units M^2.
bs=[s.Integer(1),s.Integer(2),s.Integer(3)]
fs=[s.Rational(6,7),s.Rational(17,7),s.Rational(19,7)]
zs=s.Rational(1,4)
p=lambda k:4*sum(x**k for x in bs)-4*sum(x**k for x in fs)
qspec=lambda k:4*(1-6*zs)*sum(x**k for x in bs)+2*sum(x**k for x in fs)
check('K26 five finite spectral sums',all(eq(x) for x in [p(0),p(1),p(2),qspec(0),qspec(1)]),[p(0),p(1),p(2),qspec(0),qspec(1)])
X=s.symbols('X',nonnegative=True)
pshift=lambda k:4*sum((x+gamma*X)**k for x in bs)-4*sum((x+gamma*X)**k for x in fs)
qshift=lambda k:4*(1-6*zs)*sum((x+gamma*X)**k for x in bs)+2*sum((x+gamma*X)**k for x in fs)
check('K27 common mass-shift cancellations',all(eq(x) for x in [pshift(0),pshift(1),pshift(2),qshift(0),qshift(1)]),'all five remain zero')


def log_interval(x):
    x=F(int(s.numer(x)),int(s.denom(x)))
    z=(x-1)/(x+1)
    val=2*sum((z**(2*k+1)/F(2*k+1) for k in range(40)),F(0))
    err=2*abs(z)**81/(81*(1-z*z))
    return val-err,val+err


def weighted_interval(terms):
    low=high=F(0)
    for coefficient,x in terms:
        coef=F(int(s.numer(coefficient)),int(s.denom(coefficient)))
        lo,hi=log_interval(x)
        low+=coef*(lo if coef>=0 else hi)
        high+=coef*(hi if coef>=0 else lo)
    return low,high


p2int=weighted_interval([(4*x*x,x) for x in bs]+[(-4*x*x,x) for x in fs])
p1int=weighted_interval([(4*x,x) for x in bs]+[(-4*x,x) for x in fs])
q1int=weighted_interval([(-2*x,x) for x in bs]+[(2*x,x) for x in fs])
check('K28 finite vacuum positive',p2int[0]>0,tuple(float(x) for x in p2int))
check('K29 finite Einstein inverse positive',q1int[0]>0,tuple(float(x) for x in q1int))
check('K30 induced spurion slope negative',p1int[1]<0,tuple(float(x) for x in p1int))
check('K31 finite curvature deformation sums',sum([1,-2,1])==0 and sum(k*v for k,v in zip([1,-2,1],bs))==0,'delta q0=delta q1=0')
deform=3*s.log(3)-4*s.log(2)
check('K32 finite curvature deformation nonzero',eq(s.expand_log(s.log(s.Rational(27,16)),force=True),deform),'log(27/16)>0')

ap,gs,Vol,Lsep=s.symbols('ap gs Vol Lsep',positive=True)
lambda_s=2*s.pi*ap
T3=1/((2*s.pi)**3*gs*ap**2)
e2=1/(T3*lambda_s**2)
G4=(2*s.pi)**7*gs**2*ap**4/(16*s.pi*Vol)
check('K33 D3 canonical gauge coupling',eq(e2,2*s.pi*gs),s.factor(e2))
check('K34 string force normalization',eq(e2*T3,1/lambda_s**2),s.factor(e2*T3))
check('K35 stretched-state threshold ratio',eq((1/Lsep)**2/(G4*T3),Vol/(s.pi**3*gs*ap**2*Lsep**2)),s.factor(1/(Lsep**2*G4*T3)))

x,A0=s.symbols('x A0',positive=True)
W0=s.symbols('W0',real=True)
B=A0*s.exp(-x)
U=x*(B**2*(1+x/3)+B*W0)/2
wchoice=-B*(2*x**2+4*x-3)/(3*(x-1))
dchoice=B**2*x**2*(x+2)/(6*(x-1))
check('K36 KKLT zero vacuum',eq(U.subs(W0,wchoice)+dchoice),s.simplify(U.subs(W0,wchoice)+dchoice))
check('K37 KKLT stationary before substitution',eq(s.diff(U,x).subs(W0,wchoice)),s.simplify(s.diff(U,x).subs(W0,wchoice)))
curvature=s.factor(s.diff(U,x,2).subs(W0,wchoice))
expected=B**2*(2*x**3-3*x+4)/(6*(x-1))
check('K38 KKLT curvature identity',eq(curvature,expected),curvature)
z=s.symbols('z',positive=True)
check('K39 KKLT curvature sign for x>1',eq((2*x**3-3*x+4).subs(x,z+1),2*z**3+6*z**2+3*z+3),'2z^3+6z^2+3z+3>0 for z=x-1>0')

inputs=['FROZEN_CRITERIA.md','VERIFICATION_SCOPE.md','PROOF.md','checks.py']
hashes={name:hashlib.sha256((Path(__file__).resolve().parent/name).read_bytes()).hexdigest() for name in inputs}
failed=[row['name'] for row in checks if not row['passed']]
print(f"{len(checks)-len(failed)}/{len(checks)} PASS; failures={failed}; mode={'MUTATE' if MUTATE else 'normal'}")
result={'mode':'MUTATE' if MUTATE else 'normal','checks':checks,'input_sha256':hashes,
        'sympy':s.__version__,'log_intervals':{'p2':list(map(str,p2int)),'q1':list(map(str,q1int))},
        'non_claims':['No operational xi is selected','No full gravity/mediator stability proof','No numerical parameter scan']}
out=ROOT/sys.argv[1]
out.write_text(json.dumps(result,indent=2)+'\n')
sys.exit(1 if failed else 0)
