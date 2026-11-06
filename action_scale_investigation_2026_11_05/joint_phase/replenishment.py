"""Physical fluxes, transonic accretion, and vacuum-front illumination."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def zero(e):return s.simplify(e)==0
rhoE,p,v,c,R=s.symbols('rhoE p v c R',positive=True)
flux=(rhoE if args.mutate else rhoE+p)*v/(1-v*v/(c*c))
check('vacuum carries no advective power',zero(flux.subs(p,-rhoE)))
G,M,cs,rhoi=s.symbols('G M cs rhoi',positive=True)
rs=G*M/(2*cs**2);rhos=rhoi*s.exp(s.Rational(3,2))
check('sonic critical numerator',zero(2*cs**2/rs-G*M/rs**2))
check('sonic Bernoulli density',zero(cs**2/2+cs**2*s.log(rhos/rhoi)-G*M/rs))
mdot=4*s.pi*rs**2*rhos*cs
check('isothermal accretion normalization',zero(mdot-s.pi*s.exp(s.Rational(3,2))*G**2*M**2*rhoi/cs**3))
check('accretion mass power',zero(M*s.diff(mdot,M)/mdot-2))
y=s.symbols('y',positive=True);mu=s.symbols('mu',real=True)
f=(1-s.sqrt(1-y*y))/2
check('intercepted isotropic fraction',zero(s.integrate(s.Rational(1,2),(mu,s.sqrt(1-y*y),1))-f))
Rh,D,w,eff=s.symbols('Rh D w eff',positive=True)
Lf=4*s.pi*(Rh/y)**2*w*D*eff*f
Lr=2*s.pi*Rh**2*w*D*eff/(1+s.sqrt(1-y*y))
check('exact intercepted luminosity',zero(Lf-Lr))
check('far front interception',zero(s.limit(Lf,y,0)-s.pi*Rh**2*w*D*eff))
check('near front upper interception',zero(s.limit(Lf,y,1,dir='-')-2*s.pi*Rh**2*w*D*eff))
zeta,P,vh=s.symbols('zeta P vh',positive=True)
ratio=2*G*zeta*Lr/c/(8*s.pi*G*P*Rh**2)
check('pressure and power consistency ratio',zero(ratio-zeta*eff*(w/c)*(D/P)/(2*(1+s.sqrt(1-y*y)))))
Lupper=2*s.pi*Rh**2*w*D*eff
Lcool=vh**2*c**3/(16*G)
check('cooling bath supply bound',zero((Lupper/Lcool).subs(Rh**2,vh**4/(8*s.pi*G*D))-4*eff*(w/c)*vh**2/c**2))
H,epsilon,rhoDE=s.symbols('H epsilon rhoDE',positive=True)
Rt=(G*M/H**2)**s.Rational(1,3)
Lturn=4*s.pi*Rt**2*(epsilon*H*Rt)*D
check('turnaround formal linear mass power',zero(Lturn-4*s.pi*epsilon*G*M*D/H))
check('turnaround vacuum-level substitution',zero((Lturn/M).subs(D,3*H**2*c**2/(8*s.pi*G))-s.Rational(3,2)*epsilon*c**2*H))
check('sweeping coefficient remains free',zero((2*zeta*(s.Rational(3,2)*epsilon*c**2*H)/c)/(c*s.sqrt(G*rhoDE))-3*zeta*epsilon*H/s.sqrt(G*rhoDE)))
Path(args.out).write_text(json.dumps({'checks':checks,'passed':all(checks.values()),'mutated':args.mutate},indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
