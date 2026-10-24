"""RG vacuum-shift and physical-ratio identities; no invented beta functions."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
checks=[]
def ck(name,e):
 z=s.factor(s.simplify(e));checks.append(dict(name=name,passed=z==0,residual=str(z)))
k,d,D,V,phi=s.symbols('k d Delta volume phi',positive=True)
F=s.Function('F')(phi)
ck('matter_Hessian_shift',s.diff(F+D*V,phi,2)-s.diff(F,phi,2))
dv=D/k**d
claimed=(d if args.mutate else -d)*dv
ck('vacuum_critical_scaling',k*s.diff(dv,k)-claimed)
ck('dimensionful_vacuum_shift',k*s.diff(k**d*dv,k))
k0=s.symbols('k0',positive=True)
ck('vacuum_difference_transport',dv-dv.subs(k,k0)*(k0/k)**d)
c0,c3,cb=s.symbols('c0 c3 cb',positive=True)
b0,b3,bb=s.symbols('beta0 beta3 betab',real=True)
R=2*s.sqrt(8*s.pi)*cb**3/(c3*s.sqrt(c0))
betaR=sum(s.diff(R,c)*b for c,b in [(c0,b0),(c3,b3),(cb,bb)])
expected=(2 if args.mutate else 3)*bb/cb-b3/c3-b0/(2*c0)
ck('ratio_log_beta',betaR/R-expected)
t,v0,v3,vb=s.symbols('t v0 v3 vb',real=True)
curve=R.subs({c0:c0*s.exp(t*v0),c3:c3*s.exp(t*v3),cb:cb*s.exp(t*vb)})
ck('free_direction_projection',s.diff(curve,t).subs(t,0)/R-(-v0/2-v3+3*vb))
# Two independent directions preserving the ratio: a useful counterexample
# to the claim that every amplitude must be individually fixed.
ck('ratio_preserving_direction_one',s.simplify(curve.subs({v0:6,v3:0,vb:1}))-R)
ck('ratio_preserving_direction_two',s.simplify(curve.subs({v0:0,v3:3,vb:1}))-R)
A,xi,H,scl=s.symbols('A xi H rescale',positive=True)
closure=3*H*H-A*xi*xi*H*H
ck('endpoint_vacuum_closure',closure-(3-A*xi*xi)*H*H)
ck('nonzeroH_fixes_xi_only',closure.subs(xi,s.sqrt(3/A)))
ck('closure_scale_degeneracy',closure.subs(H,scl*H)-scl*scl*closure)
result=dict(mutated=args.mutate,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,scope='exact matter-only shift and matching-ratio identities; conditional endpoint Einstein closure; no actual coupled quantum gravity/MOND RG computation')
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
