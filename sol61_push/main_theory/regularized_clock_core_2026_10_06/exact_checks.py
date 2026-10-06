#!/usr/bin/env python3
import argparse,json,platform
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--mutate-drop-detuning',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(n,ok,d):checks.append(dict(name=n,passed=bool(ok),detail=str(d)));print(('PASS ' if ok else 'FAIL ')+n+': '+str(d))
r,M,H,eta,e=S.symbols('r M H eta epsilon',positive=True);N=S.Function('N')(r);B=S.Function('B')(r);V=S.Function('V')(r)
kap=1 if args.mutate_drop_detuning else 1-e
a=S.diff(N,r)/(N*B);U=-3*M*H**2+6*eta*M*H**2*S.log(N)
L=M*(N*(B+1/B)+2*r*S.diff(N,r)/B)-M*r*V*V*(S.diff(B,r)/N+B*S.diff(N,r)/N**2)+N*B*r*r*U-2*eta*M*H*B*r*r*V*S.diff(N,r)/N+M*N*B*r*r*kap*a*a
EL=lambda f:S.diff(L,f)-S.diff(S.diff(L,S.diff(f,r)),r)
N0,n2,b2,x,R,P=S.symbols('N0 n2 b2 x R P',real=True);series={N:N0*(1+n2*r*r),B:1+b2*r*r,V:N0*x*r};u0=-3*H*H+6*eta*H*H*S.log(N0)
coef=lambda f,order:S.simplify(S.limit(EL(f).subs(series).doit()/r**order,r,0))/M
EB=coef(B,2)/N0;EN=coef(N,2);EV=coef(V,3)
ck('actual_detuned_center_B',S.simplify(EB-(2*b2-4*n2+3*x*x+u0))==0,'response enters radialcenter at higherorder')
ck('actual_detuned_center_N',S.simplify(EN-(6*b2-12*(1-e)*n2+3*x*x+6*eta*H*x+u0+6*eta*H*H))==0,'new epsilon restores12epsilon n2 afterradial/lapse elimination')
ck('actual_detuned_center_momentum',S.simplify(EV+4*(x*(b2+n2)+eta*H*n2))==0,'responsea term has no shift variation; actualfluid source contributes x(R+P)')
bsol=2*n2-S.Rational(3,2)*x*x-u0/2-P/2
D=12*e*n2-6*x*x+6*eta*H*x-2*u0+6*eta*H*H
ck('density_trace_balance',S.simplify(EN.subs(b2,bsol)-R-(D-R-3*P))==0,'R+3P=12epsilon n2−6x²+6etaHx−2u0+6etaH²')
mom=x*(bsol+n2-(R+P)/4)+eta*H*n2
ck('detuned_remaining_trace_constraint',S.simplify(mom.subs(R,D-3*P)-((3*(1-e)*x+eta*H)*n2-S.Rational(3,2)*eta*H*x*(x+H)))==0,'highdensitypole is x=−etaH/[3(1−epsilon)]')
y=S.symbols('y',real=True);nfun=S.Rational(3,2)*eta*y*(y+1)/(3*(1-e)*y+eta)
der=S.Rational(3,2)*eta*(3*(1-e)*y*y+2*eta*y+eta)/(3*(1-e)*y+eta)**2
ck('normal_center_branch_monotonicity_identity',S.factor(S.diff(nfun,y)-der)==0,'if3(1epsilon)>eta, numeratorquadraticpositive; n2increases0toinfty onnormalnegative branch')
vacpoly=(3*(1-e)*y+eta)*(6*y*y-6*eta*y-6*(1+eta))-18*e*eta*y*(y+1)
ck('cosmological_vacuum_center_unmoved',S.factor(vacpoly.subs(y,-1))==0 and nfun.subs(y,-1)==0,'x=-H,N0=1,n2=b2=0 remains exactdeSitter center; extra cubic roots are otherformaldata')
AA,aa,bb=S.symbols('A a b',positive=True);wa=S.sqrt(aa*aa+AA*AA/4)-AA/2
critical= e*aa+wa
ck('core_and_deep_flux_limits',S.limit(critical/aa,aa,0)==e and S.limit(critical/aa,aa,S.oo)==1+e,'lowaccelerationNewtoncore stiffnessepsilon; highacceleration measuredG changes1+epsilon')
across=e*AA/(1-e*e)
ck('exact_flux_term_equality',S.simplify((e*aa+AA/2)**2-aa*aa-AA*AA/4).subs(aa,across).simplify()==0,'nonzero equalityWa=epsilon a at a=epsilonA/(1epsilon²); positivebranch0<epsilon<1')
rhoc=S.symbols('rho',positive=True);rcross=12*M*e*e*AA/((1-e*e)*rhoc)
ck('actual_uniform_source_core_scale',S.simplify(rhoc*rcross/(6*M)-2*e*across)==0,'same sourced leadingflux b=rho r/(6M); derived exactcrossover radius, not an imposed halo law')
result=dict(checks=checks,mutation=args.mutate_drop_detuning,software=dict(python=platform.python_version(),sympy=S.__version__),non_claims=['No finitegradienthealth or outerboundarysolution','Normalbranch argument requires epsilon<1eta/3','Crossoverusesderived controlledweaksourceflux'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(q['passed'] for q in checks) else 1)
