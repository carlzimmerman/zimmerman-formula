"""Shared-condensate scalar-tensor and conditional local-force matching."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
sig,p,s0,A,B,t,h,xi,Z,R,F0,K,G,x,rb,theta,eps,c=s.symbols('sigma p sigma0 A B t h xi Z R F0 K G x ratio_BA theta epsilon c',positive=True)
U0,zeta=s.symbols('U0 zeta',real=True)
F=xi*(sig*sig+zeta*p*p)
U=U0-t*(sig*sig+p*p)/2+A*h**3*(sig*sig+p*p)**s.Rational(3,2)/3+B*h**3*p**3/3
uv=U.subs(p,0);fv=F.subs(p,0)
checks={}
def check(name,ok):
 checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def at_vac(expr):
 return s.simplify(expr.subs(sig,s0).subs(A,x*t/(h**3*s0)).subs(U0,t*s0*s0*(3-x)/12).subs(F0,xi*s0*s0))
stationarity=s.diff(uv,sig)-2*s.diff(fv,sig)*uv/fv
check('constant vacuum scalar and metric equations',at_vac(stationarity)==0)
vac=at_vac(uv)
check('stationary vacuum energy',s.simplify(vac-t*s0*s0*(x-1)/4)==0)
VE=F0**2*uv/fv**2
KE=F0*(Z/fv+s.Rational(3,2)*(s.diff(fv,sig)/fv)**2)
check('Einstein-frame stationary point',at_vac(s.diff(VE,sig))==0)
check('Einstein-frame amplitude kinetic coefficient',s.simplify(at_vac(KE)-(Z+6*xi))==0)
mass=at_vac(s.diff(VE,sig,2)/KE)
check('amplitude mass including scalar metric mixing',s.simplify(mass-t*(2-x)/(Z+6*xi))==0)
H2=s.simplify(vac/(3*xi*s0*s0))
check('Compton to Hubble hierarchy',s.simplify(mass/H2-12*xi*(2-x)/((Z+6*xi)*(x-1)))==0)
ae=s.sqrt(F0/fv)
alpha2=F0*s.diff(s.log(ae),sig)**2/KE
check('matter scalar exchange coupling',s.simplify(at_vac(alpha2)-xi/(Z+6*xi))==0)
# At fixed curvature the stationary amplitude depends on p^2, not on p^3.
rho=(t+xi*R)/(A*h**3)
radial_equation=s.diff(U-F*R/2,sig)
check('fixed-curvature amplitude equation',s.simplify(radial_equation-sig*(-t+A*h**3*s.sqrt(sig*sig+p*p)-xi*R))==0)
reduced=U0-(t+xi*R)**3/(6*A*A*h**6)+xi*R*(1-zeta)*p*p/2+B*h**3*p**3/3
explicit=U0-t*rho*rho/2+A*h**3*rho**3/3+B*h**3*p**3/3-xi*R*(rho*rho+(zeta-1)*p*p)/2
check('fixed-curvature amplitude elimination',s.simplify(reduced-explicit)==0)
used=xi*R if args.mutate else s.diff(reduced,p,2).subs(p,0)
check('full curvature quadratic coefficient',s.simplify(used-xi*R*(1-zeta))==0)
check('radial curvature coupling cancels quadratic at tree level',s.simplify(used.subs(zeta,1))==0)
check('cubic response survives amplitude elimination',s.simplify(s.diff(reduced,p,3)/2-B*h**3)==0)
a0=1/(K*B*h**3)
kap2=(a0*a0/(G*(t*s0*s0*(x-1)/4))).subs({K:1/(2*F0),G:1/(8*s.pi*F0),B:rb*A}).subs(A,x*t/(h**3*s0))
expected=128*s.pi*F0**3/(rb**2*x*x*t**3*(x-1))
check('gravity-calibrated joint normalization',s.simplify(kap2-expected)==0)
dimensionless=128*s.pi/(rb**2*x*x*theta**3*(x-1))
check('equal spectral amplitudes still leave parameters',s.simplify(dimensionless.subs(rb,1)-128*s.pi/(x*x*theta**3*(x-1)))==0)
epsilon_relation=theta*(x-1)/(4*xi)
check('vacuum ratio calibration',s.simplify((vac/(xi*s0*s0)**2).subs(t,theta*xi*s0*s0)-epsilon_relation)==0)
xeps=1+4*xi*eps/theta
kap_eps=s.simplify(dimensionless.subs(x,xeps))
check('small vacuum coefficient scaling',s.simplify(s.limit(eps*kap_eps,eps,0)-32*s.pi/(rb**2*xi*theta**2))==0)
check('finite coefficient needs an unfixed scaling amplitude',s.simplify(s.limit(kap_eps.subs(theta,c/s.sqrt(eps)),eps,0)-32*s.pi/(rb**2*xi*c*c))==0)
mass_planck=theta*(2-xeps)/(Z+6*xi)
check('canonical amplitude mass scaling',s.simplify(s.limit(s.sqrt(eps)*mass_planck.subs(theta,c/s.sqrt(eps)),eps,0)-c/(Z+6*xi))==0)
out={'passed':all(checks.values()),'mode':'omit_curvature_p_term' if args.mutate else 'main','checks':checks,
 'results':{'positive_stable_amplitude_domain':'1<x<2','vacuum_energy':str(vac),'mass_squared':str(mass),
 'quadratic_response':'xi R (1-zeta)','cubic_response':'B h^3','kappa_squared':str(dimensionless)},
 'scope':'Scalar-tensor vacuum and fixed-curvature/local held-amplitude response, not full clock/polarization health or a protected microscopic completion.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['passed'] else 1)
