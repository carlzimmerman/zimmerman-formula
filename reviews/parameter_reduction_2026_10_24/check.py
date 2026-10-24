"""Invariant coordinates and conditional force/health reductions, not UV selection."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
K,D,a,b,gamma,q,V,z,G,M,u,v,w,e,r,m,A,n,ss=s.symbols('K D a b gamma q V z G M u v w e r m A n s',positive=True)
checks=[]
def ck(name,x):
 residual=s.factor(s.simplify(x));checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
d=D/K;alpha=a/s.sqrt(K);beta=b/K;lam=gamma/K**s.Rational(3,2);g=q/s.sqrt(K)
change={K:K/z**2,D:D/z**2,a:a/z,b:b/z**2,gamma:gamma/z**3,q:q if args.mutate else q/z}
for label,f in [('d',d),('alpha',alpha),('beta',beta),('lambda',lam),('g',g)]:
 ck('canonical_invariant_'+label,f.subs(change,simultaneous=True)-f)
a0=g**3/(4*s.pi*G*lam)
ck('force_invariant',a0.subs(change,simultaneous=True)-a0)
ck('canonical_force_ratio',a0-q**3/(4*s.pi*G*gamma))
L=s.Matrix([[-1,1,0,0,0,0,0],[-s.Rational(1,2),0,1,0,0,0,0],[-1,0,0,1,0,0,0],[-s.Rational(3,2),0,0,0,1,0,0],[-s.Rational(1,2),0,0,0,0,1,0],[0,0,0,0,0,0,1]])
ck('six_independent_invariants',L.rank()-6)
ck('normalization_null_direction',(L*s.Matrix([-2,-2,-1,-2,-3,-1,0])).norm())
# Independent canonical symbols for the dimensionless and radial checks.
ll,gg,dd,al,be=s.symbols('lambda_c g_c d_c alpha_c beta_c',positive=True)
a0c=gg**3/(4*s.pi*G*ll)
mp={G:1/(8*s.pi*M**2),gg:u/M,ll:v/M**2,V:e*M**4}
ck('dimensionless_acceleration',a0c.subs(mp)/M-2*u**3/v)
kappa=(a0c/s.sqrt(G*V)).subs(mp)
ck('dimensionless_vacuum_ratio',kappa-2*s.sqrt(8*s.pi)*u**3/(v*s.sqrt(e)))
ck('kappa_log_gradient_u',u*s.diff(kappa,u)/kappa-3)
ck('kappa_log_gradient_v',v*s.diff(kappa,v)/kappa+1)
ck('kappa_log_gradient_e',e*s.diff(kappa,e)/kappa+s.Rational(1,2))
chi=A*s.log(r)
lap=lambda f:s.diff(f,r,2)+(n-1)*s.diff(f,r)/r
ck('general_dimension_bilaplacian',lap(lap(chi))-2*A*(n-2)*(4-n)/r**4)
extra=-dd*r**(n-1)*s.diff(lap(chi),r)
ck('three_dimensional_extra_flux',extra.subs(n,3)-2*dd*A/r)
cubic=ll*r**2*s.diff(chi,r)**2
ck('three_dimensional_cubic_flux',cubic-ll*A*A)
Ac=s.sqrt(gg*m/(4*s.pi*ll))
ck('source_normalization',ll*Ac**2-gg*m/(4*s.pi))
rD=2*dd/(ll*Ac)
ck('higher_derivative_residual_ratio',(extra.subs({n:3,A:Ac})/cubic.subs(A,Ac))-rD/r)
ck('residual_scale_mass_power',m*s.diff(rD,m)/rD+s.Rational(1,2))
E=al*ss+be*ss**2/2+ll*ss**3/3
ck('radial_spatial_hessian',s.diff(E,ss,2)-(be+2*ll*ss))
ck('transverse_spatial_hessian',s.diff(E,ss)/ss-(al/ss+be+ll*ss))
result=dict(mutated=args.mutate,passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,invariant_rank=L.rank(),scope='finite derivative truncation; exact normalization quotient and conditional MOND constraints; no microscopic selection or full gravitational stability')
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
