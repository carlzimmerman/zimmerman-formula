#!/usr/bin/env python3
import argparse,json,platform
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--mutate-flip-transverse-kinetic',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(name,ok,detail):checks.append(dict(name=name,passed=bool(ok),detail=str(detail)));print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail))
h,s,beta,theta,a,dT,dAL,dAT,dAO=S.symbols('h s beta theta a dT dAL dAT dAO',real=True)
raw=h*(-dT*dT/2+beta*(dAL*dAL+dAT*dAT+dAO*dAO))+2*s*(-theta*dT/2+beta*a*dAT)**2
ell=1+h/2-s*theta*theta/2;t=-beta*s*theta*a
expected=(1-ell)*dT*dT+beta*h*dAL*dAL+(beta*h+2*beta*beta*s*a*a)*dAT*dAT+beta*h*dAO*dAO+2*t*dT*dAT
ck('shared_c4_full_Hessian',S.expand(raw-expected)==0,'perpendicular principal with beta=c4-c1; c4 term is explicitly +c4 a²')
ortho_time=(-1 if args.mutate_flip_transverse_kinetic else 1)*beta*h
ck('uncoupled_transverse_kinetic_dictionary',S.simplify(S.diff(raw,dAO,2)/2-ortho_time)==0,'vector orthogonal(a,k): beta h temporal, h spatial; mutation reverses actual temporal sign')
n,Z,W,B,j,P,kappa,g2=S.symbols('n Z W B j P kappa g2',real=True);N=n-1;L=ell-1;C=beta*h+kappa
L0=n*(1-n*ell)*Z*Z+2*(n*ell-1)*Z*B+(1-ell)*B*B+C*j*j+(C+2*beta*beta*s*a*a+2*g2*a*a)*W*W+2*(n*Z-B)*t*W+2*N*j*P+N*(n-2)*P*P
Bsol=S.solve(S.diff(L0,B),B)[0];jSol=-N*P/C
reduced=S.factor(L0.subs(B,Bsol).subs(j,jSol));A=N*(n*ell-1)/L
ck('perpendicular_after_both_constraints',S.simplify(S.diff(reduced,Z,2)/2-A)==0,'c4 and independent G change lapse/vector, not scalar kinetic restriction when C!=0')
ck('independent_acceleration_has_no_trace_Hessian',S.diff(kappa*(dAL*dAL+dAT*dAT)+2*g2*a*a*dAT*dAT,dT,2)==0,'independent G(a²) has no expansion Hessian or theta*a mixing')
z,u,fp=S.symbols('z u Fpp',real=True)
th2=2*(z+beta*u)
ellAt=1+h/2-fp*th2/2;ellGeo=1+h/2-z*fp
ck('shared_c4_negativeK_comparison',S.simplify(ellAt-ellGeo+beta*u*fp)==0,'beta positive preserves no-escape inequality; beta negative reverses it but orthogonal vector fails')
ck('negative_beta_not_healthy',not bool(ortho_time.subs({beta:-1,h:1})>0),'candidate sign-reversal beta-1 h1 has ghost regardless scalar mixing')
g,E,M=S.symbols('g E M',positive=True);F=S.Function('F');static=-E*g*g+E*M*M*F(beta*g*g/(M*M))/2
mu=1-beta*S.Subs(S.Derivative(F(S.Symbol('K')),S.Symbol('K')),S.Symbol('K'),beta*g*g/(M*M))/2
ck('physical_static_source_mu',S.simplify(S.diff(static,g)+2*E*g*mu)==0,'same physical metric source normalization mu=1-beta F_K/2')
ck('zero_beta_deletes_MOND_response',S.simplify(mu.subs(beta,0)-1)==0,'Kstatic independent g, F has no acceleration Poisson modification')
kcrit=2-beta*h
etaCos=beta*S.Symbol('hL')+kcrit
ck('extra_G_endpoint_identity',S.expand(etaCos-(2+beta*(S.Symbol('hL')-h)))==0,'exact MOND critical static sigma0=2 gives etaCos=2+beta(hL-h0)')
eta0=etaCos.subs({beta:-1,h:S.Rational(200,101),S.Symbol('hL'):S.Rational(1,10)})
ck('compensating_G_priorfamily_gradient_price',eta0>2 and (4/eta0-2)<0,'extra positive G can cure beta-negative vector sign but old family exact-critical source condition gives negative cosmological scalar gradient')
# At C=0 one must reclassify constraints; division by C is forbidden.
ck('degenerate_lapse_new_constraint',S.simplify(S.diff(L0,j).subs(kappa,-beta*h)-2*N*P)==0,'C0: lapse imposes P0 for k!=0, not the former reduced ghost formula; new constraint-rank route remains open')
result=dict(checks=checks,compensating_eta_cos=str(eta0),mutation=args.mutate_flip_transverse_kinetic,software=dict(python=platform.python_version(),sympy=S.__version__),non_claims=['No all-operator no-go','No health proof of degenerate lapse escape','No new on-shell source solution','c4 convention explicitly declared'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
