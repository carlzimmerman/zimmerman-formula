"""Heavy-field barrier origin and finite-reservoir supply identities."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(e):return s.simplify(e)==0
phi,S,M,h,g,lam,a,V0=s.symbols('phi S M h g lam a V0',positive=True)
V=V0+a*phi**2/2+lam*phi**4/4+(M**2+h*phi**2)*S**2/2+g*S*phi**2/2
Sstar=-g*phi**2/(2*(M*M+h*phi**2))
W=V0+a*phi**2/2+lam*phi**4/4-g*g*phi**4/(8*(M*M+h*phi**2))
check('heavy field stationary solution',zero(s.diff(V,S).subs(S,Sstar)))
check('exact effective potential',zero(V.subs(S,Sstar)-W))
check('kinetic correction derivative',zero(s.diff(Sstar,phi)+g*M*M*phi/(M*M+h*phi**2)**2))
b=g*g/(2*M*M)-lam;d=3*g*g*h/(4*M**4)
check('effective sextic expansion',zero(s.series(W,phi,0,8).removeO()-(V0+a*phi**2/2-b*phi**4/4+d*phi**6/6)))
delta,x=s.symbols('delta x',positive=True)
gco=s.sqrt(2*lam)*M+delta
xc=M*delta/(h*s.sqrt(2*lam));ac=delta**2/(4*h)
Wx=V0+a*x/2+lam*x*x/4-g*g*x*x/(8*(M*M+h*x))
Wco=s.simplify(Wx.subs({g:gco,a:ac})-V0)
factor=lam*h*x*(x-xc)**2/(4*(M*M+h*x))
check('exact coexistence factorization',zero(Wco-factor))
check('equal vacuum levels',zero(Wco.subs(x,xc)))
check('coexistence minimum stationary',zero(s.diff(Wco,x).subs(x,xc)))
polynomial=2*h*x*x+3*M*M*x-M*M*xc
check('barrier stationary polynomial',zero(s.diff(factor,x)-lam*h*(x-xc)*polynomial/(4*(M*M+h*x)**2)))
check('offset does not select barrier',zero(s.diff(W-V0,V0)))
bb,dd=s.symbols('bb dd',positive=True)
x0=3*bb/(4*dd);a0=3*bb*bb/(16*dd)
W6=a0*x/2-bb*x*x/4+dd*x**3/6
check('sextic coexistence',zero(W6-dd*x*(x-x0)**2/6))
check('sextic barrier height',zero(W6.subs(x,bb/(4*dd))-bb**3/(96*dd**2)))
T,Tc,kappa=s.symbols('T Tc kappa',positive=True)
free=kappa*x0*(Tc*Tc-T*T)/2
latent=free-T*s.diff(free,T)
check('thermal free energy versus latent energy',zero(latent-kappa*x0*(Tc*Tc+T*T)/2))
Bthermal=1/(T*(Tc*Tc-T*T)**2)
check('thermal bounce slope',zero(s.diff(s.log(Bthermal),T)-(-1/T+4*T/(Tc*Tc-T*T))))
F,U,rate,eta,D,tau,supply=s.symbols('F U rate eta D tau supply',positive=True)
Fdot=rate if args.mutate else -rate
Udot=eta*D*rate-U/tau
check('radiative reservoir budget',zero(Udot+eta*D*Fdot+U/tau))
check('full energy including other products',zero((eta*D*rate-U/tau)-D*rate+U/tau+(1-eta)*D*rate))
check('no positive closed steady bath',s.solve([-rate,eta*D*rate-U/tau],[rate,U])=={rate:0,U:0})
check('external supply sets steady power',zero((eta*D*rate-U/tau).subs({rate:supply,U:eta*D*tau*supply})))
check('replenished budget',zero((eta*D*rate-U/tau)+eta*D*(supply-rate)-(eta*D*supply-U/tau)))
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
