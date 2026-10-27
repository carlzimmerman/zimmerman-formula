#!/usr/bin/env python3
"""Independent scalar/TT algebra checks from the raw action; no project imports."""
import hashlib
import json
import sys
from pathlib import Path
import sympy as s

K,beta,eta,gamma,k=s.symbols('K beta eta gamma k',positive=True)
z,zd,b,phi,sigma,sd=s.symbols('z zd b phi sigma sd',real=True)
checks=[]
def eq(name,value):
    if s.simplify(value)!=0:raise AssertionError((name,s.simplify(value)))
    checks.append(name)
Lg=(-(6+9*beta)*zd**2+(4+6*beta)*zd*b-beta*b*b+2*k*k*z*z+4*k*k*phi*z)/(4*K)
LP=k*k*phi*sigma-K*k*k*sigma*sigma/2+eta*k*k*sd*sd/2-gamma*k**4*sigma*sigma/2
L=Lg+LP
eq('lapse constraint',s.diff(L,phi)-k*k*(z/K+sigma))
bsol=(2+3*beta)*zd/beta
eq('shift constraint',s.diff(L,b).subs(b,bsol))
C=K*(2+3*beta)/beta
red=s.factor(L.subs(b,bsol).subs({z:-K*sigma,zd:-K*sd}))
eq('reduced scalar action',red-((C+eta*k*k)*sd*sd-gamma*k**4*sigma*sigma)/2)
eq('positive kinetic coefficient expression',s.diff(red,sd,2)-(C+eta*k*k))
omega=s.sqrt(gamma)*k*k/s.sqrt(C+eta*k*k)
t=s.symbols('t',positive=True)
vg=s.diff(omega,k)
eq('group velocity formula',vg**2-gamma/eta*(eta*k*k/C)*(eta*k*k/C+2)**2/(eta*k*k/C+1)**3)
Q=t*(t+2)**2/(1+t)**3
eq('group velocity derivative',s.diff(Q,t)-(4-t*t)/(1+t)**4)
eq('group velocity maximum',Q.subs(t,2)-s.Rational(32,27))

# Fourier wave k along z. Spatial TT metric h and covector P are arbitrary.
A,B,Px,Py,Pz=s.symbols('A B Px Py Pz',real=True)
h=s.Matrix([[A,B,0],[B,-A,0],[0,0,0]])
P=s.Matrix([Px,Py,Pz])
der=lambda i,e:k*e if i==2 else s.Integer(0) # real derivative amplitude
Gamma=[[[sum(s.KroneckerDelta(l,m)*(der(i,h[j,m])+der(j,h[i,m])-der(m,h[i,j]))/2 for m in range(3)) for j in range(3)] for i in range(3)] for l in range(3)]
DP=s.Matrix(3,3,lambda i,j:-sum(Gamma[l][i][j]*P[l] for l in range(3)))
eq('TT div P vanishes',s.trace(DP))
for i in range(3):
    for j in range(i):eq('TT exterior curl '+str((i,j)),DP[i,j]-DP[j,i])
eq('naive gradient differs',sum(v*v for v in DP)-k*k*(Px*Px+Py*Py+Pz*Pz)*(A*A+B*B)/2)
eq('TT expansion vanishes',s.trace(h))

# Flat-space Fourier Hodge identity for arbitrary P and wavevector.
kx,ky,kz=s.symbols('kx ky kz',real=True)
kv=s.Matrix([kx,ky,kz])
F=kv*P.T-P*kv.T
eq('flat Hodge identity',kv.dot(P)**2+sum(f*f for f in F)/2-kv.dot(kv)*P.dot(P))

# Static EH spatial variation and resulting Newtonian potential term.
static= k*k*z*z/(2*K)+k*k*phi*z/K
eq('static spatial equation',s.diff(static,z).subs(z,-phi))
eq('static Newtonian action',static.subs(z,-phi)+k*k*phi*phi/(2*K))

out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
result={'checks':checks,'count':len(checks),'sympy_version':s.__version__,
 'reduced_scalar_action':str(red),'dispersion_squared':str(s.factor(omega**2)),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'limits':['k>0','beta eta gamma K>0','Minkowski scalar background','frozen constant P for TT principal block',
           'symbolic checks do not establish full nonlinear or PPN viability']}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
