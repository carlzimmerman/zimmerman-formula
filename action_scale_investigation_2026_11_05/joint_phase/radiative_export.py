"""Excitation-line cooling with retained heavy particles: conditional checks."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
checks={}
def eq(name,a,b):checks[name]=bool(s.simplify(a-b)==0)
m,d,g,h,T,n,k=s.symbols('m d g h T n k',positive=True)
M=m+d;eps=(M*M-m*m)/(2*M);recoil=(M*M+m*m)/(2*M)-m
width=g*g*(1-m*m/M**2)/(16*s.pi*M)
eq('decay energy conservation',eps+recoil,d)
eq('decay daughter recoil',recoil,d*d/(2*M))
eq('small splitting decay width',s.limit(width/d,d,0),g*g/(8*s.pi*m*m))
Eres=(M*M-m*m)/(2*m)
eq('absorption emission detuning',Eres-eps,(M*M-m*m)*d/(2*m*M))
# Nonrel excitation cross section prefactor h^2/(16 pi s).
eq('excitation threshold prefactor',h*h/(16*s.pi*4*m*m),h*h/(64*s.pi*m*m))
t,x=s.symbols('t x',positive=True)
E=d*(1+s.cosh(t))/2
# Positive t makes sqrt(E*(E-d))=d*sinh(t)/2.
eq('thermal integral transformed measure',d*s.sinh(t)/2*s.diff(E,t),d*d*s.sinh(t)**2/4)
K0,K1=s.symbols('K0 K1')
K2=K0+2*K1/x
I=d*d*s.exp(-x)*(K2-K0)/8
eq('Bessel thermal integral recurrence',I,d*d*s.exp(-x)*K1/(4*x))
sigstar=h*h/(64*s.pi*m*m)
rate=2*sigstar*d/(s.sqrt(s.pi*m*T))*s.exp(-d/(2*T))*s.besselk(1,d/(2*T))
# Verify the logarithmic slope using K1'=-K0-K1/x.
f=s.exp(-x)*s.besselk(1,x)*s.sqrt(x)
der=s.diff(f,x).subs(s.besselk(2,x),s.besselk(0,x)+2*s.besselk(1,x)/x)
eq('thermal rate logarithmic slope',-x*der/f,s.Rational(1,2)+x*(1+s.besselk(0,x)/s.besselk(1,x)))
Ccool=n*n*k*eps if args.mutate else n*n*k*eps/2
eq('one photon per identical incoming pair',Ccool,n*n*k*eps/2)
# Narrow inverse decay line integral in a stationary target.
linearea=s.pi*g*g/(4*m*m*Eres)
pCM=(M*M-m*m)/(2*M)
BWarea=4*s.pi/pCM**2*s.pi*M*width/(2*m)
eq('inverse line integrated cross section',BWarea,linearea)
amp=2*g*g/(m*m+M*M)
Kann=amp**2/(64*s.pi*m*m)
eq('extra annihilation rate',Kann,g**4/(16*s.pi*m*m*(m*m+M*M)**2))
J,K,ein,theta=s.symbols('J K ein theta',positive=True);cv=s.Rational(3,2)
Lam=s.Function('Lam')(theta);F=J-K*n*n;G=(J*(ein-cv*theta)-n*n*Lam)/(cv*n)
eq('local cooling energy conservation',cv*(n*G+theta*F),J*ein-cv*theta*K*n*n-n*n*Lam)
mat=s.Matrix([F,G]).jacobian([n,theta]);L,Lp=s.symbols('L Lp',positive=True)
mat=mat.subs({s.diff(Lam,theta):Lp,Lam:L}).subs({J:K*n*n,ein:cv*theta+L/K})
eq('local density restoring diagonal',mat[0,0],-2*K*n)
eq('local temperature restoring diagonal',mat[1,1],-n*(K+Lp/cv))
eq('local Jacobian upper off diagonal',mat[0,1],0)
r,r0,R,A=s.symbols('r r0 R A',positive=True)
j=K*A*A/(r0*R);U=-K*A*(1/r0+1/R)
required=j*r*r*(ein-s.Rational(9,2)*theta)-2*A*theta*U*r-K*A*A*theta
residual=required-A*A*L
eq('spatial cooling mismatch linear coefficient',s.expand(residual).coeff(r,1),2*K*A*A*theta*(1/r0+1/R))
# Prompt decay vs conservative optically thin Doppler peak bound, uniform column.
Ncol,Rad=s.symbols('Ncol Rad',positive=True);sigD=Eres*s.sqrt(T/m)
gupper=4*m*m*Eres*s.sqrt(2*s.pi)*sigD/(s.pi*Ncol)
glower=16*s.pi*M**3/(M*M-m*m)*s.sqrt(T/m)/Rad
ratio=s.simplify((gupper/glower).subs(Ncol,n*Rad))
eq('prompt escape window small splitting',s.limit(ratio/d**3,d,0),s.sqrt(2*s.pi)/(2*s.pi**2*n))
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'mutation':args.mutate,'scope':'Explicit scalar extension; thin escaping line and prompt decay; local fixed-volume stability; trial flat-flow mismatch.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
