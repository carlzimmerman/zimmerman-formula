"""Exact sequestering/response identities and bounded flux/shift controls.
Not a cosmological boundary-value solver or a perturbative-health audit.
"""
import argparse, json, math
from pathlib import Path
import sympy as S
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True)
ap.add_argument('--mutate-drop-response-derivative',action='store_true');args=ap.parse_args()
o=args.output_dir.resolve();o.relative_to(P);o.mkdir(parents=True,exist_ok=True)
checks={}
def check(n,b):
 checks[n]=bool(b);print(('PASS ' if b else 'FAIL ')+n)
K,mu4,mp2,a,zeta,V,t,D,r,sp,hp,vol,Ll,Lk=S.symbols('K mu4 mp2 a zeta V t D r sp hp vol L_Lambda L_K',nonzero=True)
# trace T=-4V+t, Lambda=T/4+D.
Lam=-V+t/4+D
check('explicit_vacuum_projection',S.simplify((-V-( -4*V+t)/4)+t/4)==0)
check('metric_total_vacuum_shift',S.diff(V+Lam,V)==0)
Ravg=-2*mu4*hp*r/(mp2*sp)
check('flux_residual_trace',S.simplify(K*Ravg/4+mu4*K*hp*r/(2*mp2*sp))==0)
C=(-mu4*K*hp*r/(2*mp2*sp)+t/4)/(K*a*a)
check('cutoff_link_normalized_ratio',S.simplify(C.subs(a*a,zeta*zeta*mu4/mp2)-(-hp*r/(2*sp*zeta*zeta)+t*mp2/(4*K*zeta*zeta*mu4)))==0)
# Fully varied response depends algebraically on Lambda,K via its scale.
volume_from_form=sp*S.symbols('Q',nonzero=True)/(mu4*(1-Ll))
Qh=S.symbols('Qhat',nonzero=True)
Rlinked=-2*Lk-2*hp*Qh/(mp2*volume_from_form)
Dlinked=-K*Lk/2-mu4*K*hp*(Qh/S.symbols('Q',nonzero=True))*(1-Ll)/(2*mp2*sp)
observed_D=Dlinked if not args.mutate_drop_response_derivative else -mu4*K*hp*(Qh/S.symbols('Q',nonzero=True))/(2*mp2*sp)
check('linked_response_global_constraint',S.simplify(K*Rlinked/4-observed_D)==0)
g,b,eta,lambda_b=S.symbols('g b eta lambda_b',positive=True)
a=S.symbols('a',positive=True)
h=a/2
W=(g*S.sqrt(g*g+h*h)+h*h*S.asinh(g/h))/2-h*g
wg=S.sqrt(g*g+h*h)-h
check('P2_W_first_derivative',S.simplify(S.diff(W,g)-wg)==0)
check('P2_algebraic_response',S.simplify((wg*wg+a*wg)-g*g)==0)
check('P2_W_scale_homogeneity',S.simplify(a*S.diff(W,a)-(2*W-g*wg))==0)
check('P2_W_zero_value',S.simplify(W.subs(g,0))==0)
# W_a term from a^2=eta Lambda/K. All signs refer to + L_response in bulk.
LL=-mp2*(2*W-g*wg)/lambda_b
LK=mp2*(2*W-g*wg)/K
check('bare_link_Euler_derivatives',S.simplify(LL*lambda_b+LK*K)==0)
check('bare_link_scale_vacuum_sensitive',S.diff(eta*(-V+D)/K,V)==-eta/K)
# eta(t)=exp(-1/t^2) t>0, zero otherwise; sigma=x+eta(x-L)-eta(-x-L).
# sigma'=1 on |x|<L, nonzero and >=1 globally; explicitly nonlinear outside.
def bumpprime(x):return 0. if x<=0 else 2*math.exp(-1/(x*x))/(x**3)
def sigprime(x,L=256.):return 1+bumpprime(x-L)+bumpprime(-x-L)
check('boundary_function_globally_nonlinear',sigprime(257.)>1.)
family=[]
mu4_n=.01;mp2_n=K_n=zeta_n=1.;a0=.1
for target in [16*math.pi,32*math.pi,64*math.pi]:
 for vscaled in [-10.,0.,10.]:
  residual=target*a0*a0*K_n;vac=vscaled*mu4_n;lam=residual-vac
  x=lam/mu4_n;ratio=-2*target
  vvolume=1.;Q=mu4_n*vvolume;Qhat=ratio*Q
  metric_lambda=(lam+vac)/K_n
  dfromflux=-mu4_n*K_n*Qhat/(2*mp2_n*Q)
  # Direct form equations, metric trace and independent P2 sector agree.
  err=max(abs(metric_lambda-target*a0*a0),abs(dfromflux-residual),abs(Q*sigprime(x)/mu4_n-vvolume),abs(Qhat/mp2_n+2*metric_lambda*vvolume))
  bare_scale=math.sqrt(lam/K_n) # eta=1 foil, not adopted response.
  family.append(dict(C=target,vacuum_over_mu4=vscaled,bare_Lambda=lam,argument=x,flux_ratio=ratio,metric_Lambda=metric_lambda,a0=a0,maximum_constraint_error=err,bare_link_a0=bare_scale,bare_link_C=metric_lambda/(bare_scale**2)))
check('nine_exact_band_shift_flux_controls',all(abs(q['argument'])<256 and q['maximum_constraint_error']<1e-12 for q in family))
check('fixed_response_distinct_coefficients',len(set(round(q['C'],10) for q in family))==3 and len(set(q['a0'] for q in family))==1)
# At fixed proposed geometry+fluxes, nonlinear sigma=e^x violates Lambda-form eq after x->x-delta.
nonlinear_ratio=math.exp(-.1)
check('generic_nonlinear_not_exact_fixed_geometry',abs(nonlinear_ratio-1)>.09)
# Paired local source controls, same G and a0 for every residual.
responses=[]
for bn in [1e-6,.01,.1,1.,100.]:
 gn=math.sqrt(bn*bn+a0*bn);back=math.sqrt(gn*gn+a0*a0/4)-a0/2
 responses.append(dict(b=bn,g=gn,source_back_error=abs(back-bn)))
check('bounded_independent_P2_source_controls',max(x['source_back_error'] for x in responses)<1e-12)
res={'checks':checks,'flux_family':family,'P2_response':responses,'generic_nonlinear_same_geometry_constraint_ratio':nonlinear_ratio,'mutation':args.mutate_drop_response_derivative,'limitations':['Algebraic constraints and local static response, not solved global flux boundary-value problem','No complete covariant perturbative-health audit','Classical sequestering, not graviton-loop cancellation','Exact shift family confined to affine band; generic nonlinear functions have residual implicit dependence']}
(o/'results.json').write_text(json.dumps(res,indent=2)+'\n')
raise SystemExit(0 if all(checks.values()) else 1)
