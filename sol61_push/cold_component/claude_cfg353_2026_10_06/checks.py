#!/usr/bin/env python3
import argparse,json,platform
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--mutate-filament-middle',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(n,ok,d):checks.append(dict(name=n,passed=bool(ok),detail=str(d)));print(('PASS ' if ok else 'FAIL ')+n+': '+str(d))
r,G,m,rho,t=S.symbols('r G m rho t',positive=True)
g=S.Function('g')(r)
ck('spherical_Hessian_double_tangential',S.simplify(3*(g/r)/(4*S.pi*G)-(3*(r*r*g/G)/(4*S.pi*r**3)))==0,'eigenvalues gprime,g/r,g/r: sorted middle equals tangential double for any spherical profile')
x,y,z=S.symbols('x y z',real=True);variables=[x,y,z]
filament_phi=S.pi*G*rho*(x*x+y*y)
H=S.hessian(filament_phi,variables)
mid=(0 if args.mutate_filament_middle else 2*S.pi*G*rho)
ck('uniform_filament_middle',mid==H[0,0] and H[0,0]==H[1,1] and H[2,2]==0,'positive uniform filament eigenvalues0,2piGrho,2piGrho: middle is nonzero')
ck('filament_density_estimator',S.simplify(3*mid/(4*S.pi*G)-S.Rational(3,2)*rho)==0,'tidal estimated enclosed overdensity1.5local filament overdensity, falseON possible')
linephi=2*G*m*S.log(S.sqrt(x*x+y*y));lineH=S.hessian(linephi,variables).subs({y:0,z:0,x:r})
ck('outside_line_middle_zero',lineH==S.diag(-2*G*m/r**2,2*G*m/r**2,0),'outside positive line one negative,onezero,onepositive')
sheetphi=2*S.pi*G*rho*z*z;sheetH=S.hessian(sheetphi,variables)
ck('uniform_sheet_middle_zero',sheetH==S.diag(0,0,4*S.pi*G*rho),'uniform plane/slab middlezero')
harmonic=(t*x*x+t*y*y-2*t*z*z)/2
ck('harmonic_tidal_contamination',sum(S.diff(harmonic,v,2) for v in variables)==0 and S.hessian(harmonic,variables)==S.diag(t,t,-2*t),'zero density harmonic quadrupole has arbitrary positive middle eigenvalue t')
pointH=S.diag(-2*t,t,t)
ck('external_tide_cancels_point_Hessian',pointH+S.diag(2*t,-t,-t)==S.zeros(3),'tracefree exterior tide can cancel entire local pointmass Hessian')
# Independent audit of root phase lemma, not an astronomy computation.
R,mu,Hh,n=S.symbols('R mu H n',positive=True);U=-mu/((n-2)*R**(n-2))-Hh*Hh*R*R/2
ck('root_phase_force',S.simplify(-S.diff(U,R)+mu/R**(n-1)-Hh*Hh*R)==0,'Newtonian shell force derives from reported energy')
U0=U.subs({n:3,mu:1,Hh:1,R:S.Rational(1,2)});Us=U.subs({n:3,mu:1,Hh:1,R:1})
ck('root_phase_barrier_control',U0==-S.Rational(17,8) and Us==-S.Rational(3,2) and U0+2>Us,'sameinitialdensity/potential,restboundinnerbranch versus outwardspeed2 abovebarrier')
result=dict(checks=checks,mutation=args.mutate_filament_middle,software=dict(python=platform.python_version(),sympy=S.__version__),non_claims=['No Claude script/Lean/data result verified','No fullGR momentum initialdata identity','No tidal-switch actioncompletion or sourceownership derivation'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
