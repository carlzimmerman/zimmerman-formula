"""Exact constrained log-KGB/P2 quadratic repair and bounded mode controls.
Sourced control is conserved comoving dust at first order, not nonlinear galaxy.
"""
import argparse,json,math
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);ap.add_argument('--mutation',choices=['none','drop_clock_mixing','drop_acceleration_kinetic','rescale_fixed_scale'],default='none');args=ap.parse_args()
b=Path(__file__).resolve().parent;o=args.output_dir.resolve();o.relative_to(b);o.mkdir(parents=True,exist_ok=True)
checks={}
def ck(n,v):checks[n]=bool(v);print(('PASS ' if v else 'FAIL ')+n)
K,H,c,X,Xref,scale,Delta,rho,p=s.symbols('K H c X Xref scale Delta rho p',positive=True);z=s.symbols('z',real=True);q,nu,t,zet=s.symbols('q nu t zeta',real=True)
# scale=exp(-Delta/(2c)) >0; covariant normalized u and acceleration are unchanged.
ck('normalized_clock_rescaling',s.simplify(scale/s.sqrt(scale**2)-1)==0)
ck('log_vacuum_map',s.simplify(-c*s.log(s.exp(-Delta/c)*X/Xref)+c*s.log(X/Xref)-Delta)==0)
ck('braid_map',s.simplify((scale**2*X)**(-s.Rational(1,2))*scale-X**(-s.Rational(1,2)))==0)
A,g=s.symbols('A g',positive=True)
W=(g*s.sqrt(g*g+A*A/4)+A*A*s.asinh(2*g/A)/4)/2-A*g/2
ck('response_quadratic',s.simplify(s.limit(W/g**2,g,0))==0)
resp=-2*K*(W-g*g/2)
ck('response_acceleration_coefficient',s.simplify(s.limit(resp/g**2,g,0)-K)==0)
An=scale*A if args.mutation=='rescale_fixed_scale' else A
ck('fixed_response_scale_invariant',s.simplify(resp.subs(A,An)-resp)==0)
Theta=K*H*(1+z);Sigma=-3*K*H*H*(1+2*z)
D=K if args.mutation!='drop_acceleration_kinetic' else s.Integer(0)
L=-3*K*q*q+K*p*p*zet*zet+Sigma*nu*nu-2*Theta*nu*t+2*K*q*t+6*Theta*nu*q+2*K*p*p*nu*zet+D*p*p*nu*nu
nus=K*q/Theta
ck('momentum_constraint_unchanged',s.simplify(s.diff(L,t).subs(nu,nus))==0)
Ls=s.simplify(L.subs(nu,nus));kin=s.diff(Ls,q,2)/2
G=3*K*z*z/(1+z)**2;F=-K*z/(1+z);extra=K*p*p/(H*H*(1+z)**2)
ck('full_reduced_kinetic',s.simplify(kin-G-extra)==0)
# cross term 2K^2/Theta p^2 zeta zetadot, integrated with a^3p^2 proportional a.
Fcalc=K*K*H/Theta-K
ck('reduced_static_stiffness_unchanged',s.simplify(Fcalc-F)==0)
ck('effective_dispersion',s.simplify(F*p*p/(G+extra)-(-z*(1+z)*p*p/(3*z*z+p*p/(H*H))))==0)
# Exact deSitter time-dependence: p=k/a, so p_dot=-Hp; coefficients are not frozen UV waves.
Atot=G+extra
Adot=s.diff(Atot,p)*(-H*p)
damping=s.simplify(3*H+Adot/Atot)
ck('deSitter_mode_friction',s.simplify(damping-H*(3*G+extra)/(G+extra))==0)
r=s.symbols('r',real=True)
uvpoly=r*r+H*r-z*(1+z)*H*H
ck('UV_relaxation_roots',s.simplify(uvpoly-(r-H*z)*(r+H*(1+z)))==0)
ck('UV_frequency_coefficient_bound',s.simplify(s.Rational(1,4)+z*(1+z)-(z+s.Rational(1,2))**2)==0)
# Lapse constraint from L-rho*nu. Static unitary zeta=0,nu=0 and comoving dust rho~a^-3.
ts=-rho/(2*Theta)
ck('sourced_lapse_constraint',s.simplify((s.diff(L,nu)-rho).subs({nu:0,q:0,zet:0,t:ts}))==0)
beta=rho/(2*Theta*p*p) # t=-p² beta
# beta~a^-1: Psi=nu+betadot=-H beta, Phi=-zeta-H beta.
psi=-H*beta
if args.mutation=='drop_clock_mixing':psi=-rho/(2*K*p*p)
ck('conserved_dust_force_dictionary',s.simplify(psi+rho/(2*K*(1+z)*p*p))==0)
ck('geodesic_clock_with_nonzero_metric_force',s.simplify(psi+H*beta)==0)
rows=[]
for zz in [-.1,-.25,-.5,-.9]:
 for pp in [.1,1.,10.,100.]:
  gs=3*zz*zz/(1+zz)**2;fs=-zz/(1+zz);plus=pp*pp/(1+zz)**2;w=fs*pp*pp/(gs+plus)
  rows.append(dict(z=zz,p_over_H=pp,Gs_over_K=gs,Fs_over_K=fs,Gextra_over_K=plus,omega2_over_H2=w,high_p_limit=-zz*(1+zz),GN_over_bare=1/(1+zz)))
ck('bounded_healthy_vacuum_modes',all(r['Gs_over_K']>0 and r['Fs_over_K']>0 and r['omega2_over_H2']>0 for r in rows))
res={'checks':checks,'mode_controls':rows,'mutation':args.mutation,'limitations':['Four dimensional log KGB constant-q rolling deSitter','Quadratic constraints only, not nonlinear galaxy matching','Dust source conserved at first order and comoving, homogeneous free scalar waves set to zero','FixedA or positive beta theta, no selected beta','No finite-gradient or EFT health claim']};(o/'results.json').write_text(json.dumps(res,indent=2)+'\n');raise SystemExit(0 if all(checks.values()) else 1)
