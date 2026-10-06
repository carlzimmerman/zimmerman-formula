"""Independent regular-center expansion of full stationary ADM plus fluid stress."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);ap.add_argument('--mutation',choices=['none','omit_acceleration_quadratic'],default='none');a=ap.parse_args();base=Path(__file__).resolve().parent;o=a.output_dir.resolve();o.relative_to(base);o.mkdir(parents=True,exist_ok=True)
r,K,H,eta,N0=s.symbols('r K H eta N0',positive=True);n2,b2,x,R,P=s.symbols('n2 b2 x R P',real=True);N=s.Function('N')(r);B=s.Function('B')(r);V=s.Function('V')(r);g=s.diff(N,r)/(N*B)
Q=K*g*g if a.mutation=='none' else s.Integer(0);c=3*K*eta*H*H;bc=2*K*eta*H;S=2*c*s.log(N)-3*K*H*H+Q
L=K*(N*(B+1/B)+2*r*s.diff(N,r)/B-r*V*V*(s.diff(B,r)/N+B*s.diff(N,r)/N**2))+N*B*r*r*S-bc*B*r*r*V*s.diff(N,r)/N
EL=[s.diff(L,q)-s.diff(s.diff(L,s.diff(q,r)),r) for q in [N,B,V]]
F=N*N-B*B*V*V;rho=K*R;p=K*P
sources=[-B*r*r*(N*N*(rho+p)/F-p),N*r*r*(p+B*B*V*V*(rho+p)/F),N*B**3*r*r*V*(rho+p)/F]
subs={N:N0*(1+n2*r*r),B:1+b2*r*r,V:N0*x*r};tot=[s.simplify((e+src).subs(subs).doit()) for e,src in zip(EL,sources)]
coeff=[s.simplify(s.limit(tot[0]/(K*r*r),r,0)),s.simplify(s.limit(tot[1]/(K*N0*r*r),r,0)),s.simplify(s.limit(tot[2]/(K*r**3),r,0))]
u0=-3*H*H+6*eta*H*H*s.log(N0)
expected=[6*b2-12*n2+3*x*x+6*eta*H*x+u0+6*eta*H*H-R,2*b2-4*n2+3*x*x+u0+P,-4*x*(b2+n2)-4*eta*H*n2+x*(R+P)]
checks={}
def ck(n,v):checks[n]=bool(v);print(('PASS ' if v else 'FAIL ')+n)
for name,c0,e0 in zip(['lapse_center','radial_center','momentum_center'],coeff,expected):ck(name,s.simplify(c0-e0)==0)
quad=x*x-eta*H*x-(1+eta)*H*H+2*eta*H*H*s.log(N0)+(R+3*P)/6
ck('central_quadratic_elimination',s.simplify((coeff[0]-3*coeff[1])/(-6)-quad)==0)
disc=eta*eta*H*H-4*(-(1+eta)*H*H+2*eta*H*H*s.log(N0)+(R+3*P)/6)
ck('discriminant_normalization',s.simplify(disc-((eta+2)**2*H*H-8*eta*H*H*s.log(N0)-s.Rational(2,3)*(R+3*P)))==0)
# Momentum adds a necessary condition beyond reality of x.
red=s.expand(expected[2].subs(b2,2*n2-P/2-3*x*x/2-u0/2));expr=red.subs(R,-3*P-6*x*x+6*eta*H*x-2*u0+6*eta*H*H)
ck('remaining_momentum_condition',s.simplify(expr-(-4*(3*x+eta*H)*n2+6*eta*H*x*(x+H)))==0)
(o/'results.json').write_text(json.dumps({'checks':checks,'coefficients':[str(v) for v in coeff],'quadratic':str(quad),'discriminant':str(s.factor(disc)),'limitations':['C2regularmetricandclock, finitecentralstaticKillingperfectfluid','Uleadingpositiveaccelerationquadratic','Noallmodifiedgravity or dynamicalstar no-go','Realquadraticroot not sufficient']},indent=2)+'\n');raise SystemExit(0 if all(checks.values()) else 1)
