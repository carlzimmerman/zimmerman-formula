"""Conditional global-vacuum subtraction for the joint condensed model."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
A,B,t,h,K,G,d=s.symbols('A B t h K G d',positive=True)
U0,Vcur,Vavg,kin,theta,endpoint=s.symbols('U0 Vcur Vavg kinetic_average other_trace endpoint',real=True)
mu2,mu3=s.symbols('mean_sigma2 mean_sigma3',real=True)
f,x=s.symbols('early_volume_fraction x',real=True)
checks={}
def check(name,ok):
 checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
residual=Vcur-Vavg+(d-2)*kin/(2*d)+theta/d
used=Vcur-(0 if args.mutate else Vavg)+(d-2)*kin/(2*d)+theta/d
shift=s.symbols('vacuum_shift',real=True)
check('absolute vacuum offset cancels',s.simplify(used.subs({Vcur:Vcur+shift,Vavg:Vavg+shift},simultaneous=True)-used)==0)
trace=-d*Vavg+(d-2)*kin/2+theta
check('trace subtraction gives residual density',s.simplify(Vcur+trace/d-residual)==0)
gap=t**3/(6*A*A);vf=U0-gap
twophase={Vcur:vf,Vavg:f*U0+(1-f)*vf,kin:0,theta:0}
check('two-state late residual sign',s.simplify(used.subs(twophase)+f*gap)==0)
time=s.symbols('time',real=True);scale=s.Function('a')(time);phi=s.Function('sigma')(time)
vp=s.symbols('Vprime',real=True);weight=scale**(d-1)
lhs=s.diff(weight*phi*s.diff(phi,time),time)
eom=-(d-1)*s.diff(scale,time)/scale*s.diff(phi,time)-vp
check('weighted virial boundary identity',s.simplify(lhs.subs(s.diff(phi,time,2),eom)-weight*(s.diff(phi,time)**2-phi*vp))==0)
avgV=U0-t*mu2/2+A*mu3/3
kin_virial=-t*mu2+A*mu3+endpoint
r=s.simplify(residual.subs({Vcur:vf,Vavg:avgV,kin:kin_virial}))
general=-gap+t*mu2/d+A*((d-2)*3-2*d)*mu3/(6*d)+(d-2)*endpoint/(2*d)+theta/d
check('dimension-dependent scalar history reduction',s.simplify(r-general)==0)
X2,X3=s.symbols('mean_x2 mean_x3',real=True);m=t/A
four=s.simplify(r.subs({d:4,mu2:m*m*X2,mu3:m**3*X3}))
history=-1+s.Rational(3,2)*X2-X3/2
check('four-dimensional residual',s.simplify(four-(gap*history+(endpoint+theta)/4))==0)
q=-1+s.Rational(3,2)*x*x-x**3/2
check('bounded-relaxation sign certificate',s.simplify(q+(1-x)*(2+2*x-x*x)/2)==0)
check('sign-certificate bracket positive on unit interval',s.simplify((2+2*x-x*x)-2-x*(2-x))==0)
a0=1/(K*B*h**3);pc=t/(A*h);lam=pc/a0
F=s.symbols('history_factor',positive=True)
ratio=a0*a0/(G*gap*F)
check('joint normalization retains history factor',s.simplify(ratio-6*K/G*(B/A)/(lam**3*F))==0)
check('history dependence is nonzero',s.simplify(s.diff(ratio,F)+ratio/F)==0 and s.diff(ratio,F)!=0)
check('cubic local response not changed by constant subtraction',s.diff(B*h**3*x**3/3-s.Symbol('global_constant'),x,3)==2*B*h**3)
out={'passed':all(checks.values()),'mode':'omit_historic_potential' if args.mutate else 'main','checks':checks,
 'residual_general_d':str(s.factor(r)),'residual_four_d':str(s.factor(four)),
 'history_factor':'-1+3< x^2 >/2-< x^3 >/2+(endpoint+other_trace)/(4*phase_gap)',
 'conditional_ratio':'kappa^2=24*pi*(B/A)/(lambda_phase^3*history_factor)',
 'scope':'Conditional homogeneous protected-sector matching, not a solved global cosmology or a constructed covariant MOND embedding.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['passed'] else 1)
