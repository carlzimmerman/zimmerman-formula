#!/usr/bin/env python3
import argparse,json,hashlib,platform
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');ap.add_argument('--out',required=True);args=ap.parse_args()
checks=[]
def z(x):return S.simplify(x)==0
def ck(n,x):checks.append({'name':n,'passed':bool(x)})
M,b,T,k,c,mu,ell=S.symbols('M b T k c mu ell',positive=True)
Z,lam,alpha,zd,zeta,X=S.symbols('Z lam alpha zd zeta X',real=True)
sign=-1 if args.mutate else 1
F=sign*M*M*b*T*T*(S.sqrt(1-Z*Z/T**2)-1)
# Use dimensionless u=Z/T with |u|<1 for square-root substitutions.
u=S.symbols('u',real=True);r=S.symbols('r',positive=True)
aux=sign*M*M*(-lam*Z+T*S.sqrt(lam*lam+b*b*T*T)-b*T*T)
# Solve by substituting Z=T*lam/sqrt(lam^2+b^2 T^2); converse uses |Z|<T.
Zoflam=T*lam/S.sqrt(lam*lam+b*b*T*T)
ck('auxiliary_constraint',z(S.diff(aux,lam).subs(Z,Zoflam)))
ck('auxiliary_inside_cap',z(T*T-Zoflam**2-b*b*T**4/(lam*lam+b*b*T*T)))
# Rational parametrization Z=T*r/sqrt(1+r^2), lambda=b*T*r avoids abs branches.
sub={Z:T*r/S.sqrt(1+r*r),lam:b*T*r}
ck('auxiliary_elimination_positive_branch',z(aux.subs(sub,simultaneous=True)-F.subs(Z,sub[Z])))
ck('even_cap_function',z(F.subs(Z,-Z)-F))
ck('cap_zero_value',F.subs(Z,0)==0)
ck('cap_zero_first_variation',S.diff(F,Z).subs(Z,0)==0)
ck('healthy_small_expansion_sign',z(S.diff(F,Z,2).subs(Z,0)+M*M*b))
beff=-S.diff(F,Z,2)/M**2
ck('effective_expansion_stiffness',z(beff-sign*b/(1-Z*Z/T**2)**S.Rational(3,2)))
ck('bounded_cap_lagrangian',z(S.limit(F,Z,T,dir='-')+M*M*b*T*T))
# This is a frozen gravity/clock ADM block, not the whole rolling-field theory.
bused=sign*b
L=M*M*(3*zd**2-2*zd*X-bused*X*X/2+k*k*zeta*zeta+2*k*k*alpha*zeta+(c*k*k+mu*mu)*alpha*alpha)
sol=S.solve([S.diff(L,X),S.diff(L,alpha)],[X,alpha],dict=True)[0]
red=S.factor(L.subs(sol));kin=S.diff(red,zd,2)/(2*M*M);grad=-S.diff(red,zeta,2)/(2*M*M)
expected_kin=3+2/bused
omega= S.factor(grad/kin)
want=bused*k*k*((1-c)*k*k-mu*mu)/((2+3*bused)*(c*k*k+mu*mu))
ck('ADM_constraint_elimination',z(kin-expected_kin) and z(omega-want))
ck('native_null_has_zero_restoring_force',z(omega.subs({c:1,mu:0})))
ck('unswitched_stiffness_dispersion',z(omega.subs({c:1/(1+ell*ell*k*k),mu:0})-b*ell*ell*k**4/(2+3*b)))
ck('positive_kinetic_witness',kin.subs(b,S.Rational(1,10))>0)
ck('positive_frequency_witness',omega.subs({b:S.Rational(1,10),k:1,c:S.Rational(1,2),mu:0})>0)
ck('finite_norm_mass_IR_tachyon',omega.subs({b:S.Rational(1,10),k:1,c:1,mu:1})<0)
eta,g,a=S.symbols('eta g a',positive=True)
gb=(1+eta)*g-a*g/(a+g)
ck('bare_acceleration_changes_deep_MOND',z(S.limit(gb/g,g,0)-eta))
ck('native_deep_MOND_recovered',z(S.limit((gb.subs(eta,0))/g**2,g,0)-1/a))
# Canonical 1+1 wave: tau=t+f(x-t)+g(x+t).
f1,g1,p=S.symbols('f1 g1 p',real=True)
qt=1-f1+g1;qx=f1+g1
ck('canonical_null_factorization',z(qt**2-qx**2-(1-2*f1)*(1+2*g1)))
finit=(1-p-S.sqrt(1+p*p))/2;ginit=(-p+S.sqrt(1+p*p)-1)/2
ck('same_unit_clock_initial_data',z(qx.subs({f1:finit,g1:ginit})+p) and z(qt.subs({f1:finit,g1:ginit})-S.sqrt(1+p*p)))
ck('initial_null_factor_product',z((1-2*finit)*(1+2*ginit)-1))
# Smooth spherical data, tau_t(0,r)=1 and |tau_r(0,r)|<=2/5.
x,t=S.symbols('x t',real=True)
f=S.exp(-(x*x-100)**2/400)/10
center=1+2*S.diff(f,x).subs(x,t)+t*S.diff(f,x,2).subs(x,t)
ck('spherical_initial_future_direction',center.subs(t,0)==1)
ck('spherical_timelike_clock_breakdown_witness',center.subs(t,10)==-1)
ck('spherical_smooth_origin',S.diff(f,x).subs(x,0)==0)
# Exact massless Fourier mode on fixed de Sitter, conformal eta<0.
e,kc=S.symbols('eta kc',real=True)
mode=S.cos(kc*e)+kc*e*S.sin(kc*e)
ck('deSitter_free_clock_mode',z(S.diff(mode,e,2)-2*S.diff(mode,e)/e+kc*kc*mode))
ck('deSitter_mode_freezes_spatially',mode.subs(e,0)==1)
# Cap characteristic lower bound and old fold timing, Theta_star=0 planar case.
theta0,s=S.symbols('theta0 s',positive=True)
J=S.exp(-T*s)
ck('bounded_expansion_volume_lower_solution',z(S.diff(J,s)+T*J))
oldtheta=-theta0/(1-theta0*s);hit=1/theta0-1/T
ck('old_geodesic_hits_cap_before_fold',z(oldtheta.subs(s,hit)+T))
# New cap's proper-time derivative does not impose an artificial viscosity.
ck('cap_is_a_real_variational_potential',F.has(S.sqrt(1-Z*Z/T**2)) and not F.has(S.I))
here=Path(__file__).resolve().parent
R=dict(mutate=args.mutate,checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),formulas={'cap':str(F),'effective_stiffness':str(beff),'auxiliary_expansion':str(Zoflam),'kinetic':str(kin),'frequency_squared':str(omega)},source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [here/'clock_math.py',here/'CONTRACT.md',here/'CAP_EXTENSION.md']},versions={'python':platform.python_version(),'sympy':S.__version__},scope='Exact restricted identities; no full nonlinear existence or coupled-action health proof.')
path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps({'passed':R['passed'],'total':R['total'],'failed':[x['name'] for x in checks if not x['passed']]},indent=2));raise SystemExit(int(R['passed']!=R['total']))
