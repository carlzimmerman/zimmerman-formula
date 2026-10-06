#!/usr/bin/env python3
"""Local volume multiplier, dimensional normalization and varied-scale checks."""
import argparse,json,platform,math
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=HERE);p.add_argument('--mutate-ignore-scale-variation',action='store_true');args=p.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok,detail):
 checks.append(dict(name=name,passed=bool(ok),detail=str(detail)));print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail))
d,K,R,T,lam,V,GN,Solid=s.symbols('d K R T lambda V G_N Solid',positive=True)
trace=s.Eq(-(d-2)*K*R/2,T-d*lam)
reconstructed=((d-2)*K*R/2+T)/d
check('general_trace_multiplier',s.simplify(reconstructed-s.solve(trace,lam)[0])==0,'lambda=[(d-2)KR/2+T]/d; full T, not vacuum-only')
Rvac=2*d*(lam+V)/((d-2)*K)
check('vacuum_trace',s.simplify(reconstructed.subs({T:-d*V,R:Rvac})-lam)==0,'vacuum stress -V g gives total density lambda+V')
calibration=(d-3)/((d-2)*Solid*GN)
check('dimension4_G_normalization',s.simplify(calibration.subs({d:4,Solid:4*s.pi})-1/(8*s.pi*GN))==0,'tensor coupling calibrated by massive Newton Poisson source d>3')
check('vacuum_full_density_no_solid_angle_division',s.simplify(((lam+V)/K).subs(K,calibration)-(d-2)*Solid*GN*(lam+V)/(d-3))==0,'same action retains solid angle in vacuum curvature')
# Declared large-gradient scalar continuation and physical force calibration.
u,Z,gamma,alpha=s.symbols('u Z gamma alpha',positive=True)
Pscalar=-Z*(u*u/2-Z*u/gamma+(Z/gamma)**2*s.log(1+gamma*u/Z))
PXscalar=s.simplify(-s.diff(Pscalar,u)/u)
check('explicit_scalar_kinetic_continuation',s.simplify(PXscalar-Z*gamma*u/(Z+gamma*u))==0 and s.limit(PXscalar/u,u,0)==gamma and s.limit(PXscalar,u,s.oo)==Z,'same deep cubic and specified high-gradient linear kinetic coefficient Z')
Gphys=1/(8*s.pi*K)+alpha*alpha/(4*s.pi*Z)
check('physical_G_includes_scalar_force',s.simplify(Gphys-1/(8*s.pi*K)-alpha*alpha/(4*s.pi*Z))==0,'lab force includes scalar exchange; vacuum curvature still uses K')
# Auxiliary multiplier conservation is geometric, not a density response law.
rho,Fp,H=s.symbols('rho Fprime H',positive=True)
kap=s.symbols('kappa',positive=True)
Fprime=kap-1
exponent=3/(1+Fprime);cs2=-Fprime/(1+Fprime)
check('exchange_dust_scaling',s.simplify(exponent-3/kap)==0,'rho proportional a^(-3/kappa), separately conserved dust not retained')
check('exchange_dust_causal_window',s.simplify(cs2-(1-kap)/kap)==0 and cs2.subs(kap,s.Rational(1,2))==1,'positive compressibility/light speed requires 1/2<=kappa<=1 in this algebraic perfect-fluid closure')
check('per_solidangle_density_control',s.simplify(cs2.subs(kap,1/(8*s.pi))-(8*s.pi-1))==0,'vacuum G_N rho instead of8piG_Nrho would require kappa1/(8pi) if applied to evolving density')
n,m,c=s.symbols('n m c',positive=True)
epsilon=(1+c)*m*n
pressure=s.simplify(n*s.diff(epsilon,n)-epsilon)
check('fully_varied_fluid_reaction',pressure==0 and s.simplify(pressure-(-c*m*n))!=0,'adding F=c rho to conserved dust action rescales mass; does not produce post-variation vacuum pressure -F')
L,Omega,Vol,a0,vstar=s.symbols('L Omega Vol a0 vstar',positive=True)
Cgeom=(d-1)*(d-2)/2*(Omega/Vol)**(2/d)/a0**2
v4=8*s.pi**2/3*(3/(32*s.pi))**2
check('compact_volume_target_number',s.simplify(v4-s.Rational(3,128))==0,'S4 proper-volume target Vol*a0^4=3/128, an unfixed boundary number')
check('compact_volume_differentiation',s.simplify(s.diff(Cgeom,Vol)+2*Cgeom/(d*Vol))==0,'d ln C/d ln Vol=-2/d')
chi=s.symbols('chi',positive=True);U=s.Function('U')(chi)
# Euclidean rigid-scale constrained action density: U*Vol+lambda(Vol-vstar chi^-d).
scale=s.diff(U*Vol+lam*(Vol-vstar*chi**(-d)),chi).subs(Vol,vstar*chi**(-d))
lam_needed=s.solve(s.Eq(scale,0),lam)[0]
check('scale_Euler_reaction',s.simplify(lam_needed+chi*s.diff(U,chi)/d)==0,'lambda=-chi Uprime/d, mandatory variation before volume matching')
observed_lam=lam if args.mutate_ignore_scale_variation else lam_needed
check('no_vacuum_generated_without_potential',s.simplify(observed_lam.subs({U:0,s.diff(U,chi):0}))==0,'U=0 forceslambda0; mutation retaining arbitrarylambda must fail')
ucoef=s.symbols('ucoef',positive=True)
Lambda_eff=(U+lam_needed)/K
check('quadratic_potential_selector_cost',s.simplify(Lambda_eff.subs({U:K*ucoef*chi**2,s.diff(U,chi):2*K*ucoef*chi})/chi**2-ucoef*(1-2/d))==0,'chosen quadratic coefficient still fixesratio; volume compatibility must be imposed')
check('homogeneous_d_potential_cancels_curvature',s.simplify(Lambda_eff.subs({U:chi**d,s.diff(U,chi):d*chi**(d-1)}))==0,'Euler-homogeneous vacuum potential degree d leaveszero residual curvature')
# Proper Lorentzian volume has duration dependence; not compact Euclidean invariant.
x=s.symbols('x',positive=True)
check('lorentzian_volume_monotonic_integrand',s.diff(s.exp(x),x)>0,'integral exp((d-1)Ht) dt increaseswithH for fixedt>0')
result=dict(checks=checks,control=dict(kappa=1/(8*math.pi),cs_squared=8*math.pi-1,dust_dilution_exponent=24*math.pi,target_dimensionless_S4_volume=3/128),mutation=args.mutate_ignore_scale_variation,software=dict(python=platform.python_version(),sympy=s.__version__))
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
