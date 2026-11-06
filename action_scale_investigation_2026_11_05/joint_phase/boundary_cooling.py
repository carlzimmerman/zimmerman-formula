"""Soft-scattering boundary cooling and thin-wall phase conversion."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(e):return s.simplify(e)==0
beta,mu=s.symbols('beta mu',real=True)
boost=(1/(1-beta**2))*s.integrate((1-beta*mu)**2,(mu,-1,1))/2-1
check('flux weighted Doppler energy gain',zero(boost-4*beta**2/(3*(1-beta**2))))
n,T,TC,U,m,c,kB,K,sig=s.symbols('n T TC U m c kB K sig',positive=True)
a=4*n*sig*c*U*kB/(m*c*c);b=K*n*n*kB
H=a*(TC+(T if args.mutate else -T))
net=H+b*T
Tstar=a*TC/(a-b)
check('wall cooling equilibrium',zero(net.subs(T,Tstar)))
check('restoring thermal slope',zero(s.diff(net,T)-(b-a)))
check('same coupling bath threshold',zero((a/b).subs(sig,4*K/c)-16*U/(m*n*c*c)))
q=s.symbols('q',positive=True)
check('finite equilibrium temperature',zero(Tstar-TC/(1-b/a)))
R,v,G,L=s.symbols('R v G L',positive=True)
rhoR=v*v/(4*s.pi*G*R*R)
Lmin=v*v*c**3/(16*G)
check('one pass cooling luminosity lower bound',zero(4*s.pi*R*R*c*rhoR*c*c/16-Lmin))
Mvac,Mhalo=s.symbols('Mvac Mhalo',positive=True)
check('vacuum depletion upper bound',zero((Mvac*c*c/Lmin).subs(v*v,G*Mhalo/R)-16*(Mvac/Mhalo)*R/c))
phi,lam,vf,D,Sigma=s.symbols('phi lam vf D Sigma',positive=True)
tension=s.sqrt(lam/2)*s.integrate(vf*vf-phi*phi,(phi,-vf,vf))
check('quartic wall tension',zero(tension-2*s.sqrt(2*lam)*vf**3/3))
B=2*s.pi**2*Sigma*R**3-s.pi**2*D*R**4/2
Rb=3*Sigma/D
check('bounce stationary radius',zero(s.diff(B,R).subs(R,Rb)))
Bstar=27*s.pi**2*Sigma**4/(2*D**3)
check('bounce exponent',zero(B.subs(R,Rb)-Bstar))
check('quartic conversion exponent',zero(Bstar.subs(Sigma,tension)-32*s.pi**2*lam**2*vf**12/(3*D**3)))
t,tp,rate,w=s.symbols('t tp rate w',positive=True)
I=s.integrate(rate*4*s.pi*w**3*(t-tp)**3/3,(tp,0,t))
check('bubble growth overlap exponent',zero(I-s.pi*rate*w**3*t**4/3))
f=1-s.exp(-I);power=D*s.diff(f,t)
check('conversion power',zero(power-4*s.pi*rate*w**3*t**3*D*s.exp(-I)/3))
check('finite total latent energy',zero(s.integrate(power,(t,0,s.oo))-D))
peak=(9/(4*s.pi*rate*w**3))**s.Rational(1,4)
check('conversion power maximum time',zero(s.diff(s.log(power),t).subs(t,peak)))
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
