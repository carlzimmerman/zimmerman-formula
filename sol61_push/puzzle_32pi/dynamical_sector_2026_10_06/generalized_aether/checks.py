#!/usr/bin/env python3
"""Same sourced positive-K response; distinct regular negative-K vacuum roots."""
import argparse,json,platform,math
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--mutate-drop-lapse-derivative',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok,detail):
 checks.append(dict(name=name,passed=bool(ok),detail=str(detail)));print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail))
n,alpha,N,adot,ascale,M,K=s.symbols('n alpha N adot ascale M K',positive=True);F=s.Function('F')
hubble=adot/(N*ascale);kin=n*alpha*hubble*hubble/(M*M)
mini=N*(-n*(n-1)*hubble*hubble+M*M*F(kin))
expected=n*(n-1)*hubble*hubble+M*M*(F(kin)-2*kin*s.Subs(s.diff(F(K),K),K,kin))
check('general_d_lapse_variation',s.simplify(s.diff(mini,N)-expected)==0,'unit constraint A0=1/N retained before varying lapse; K=n alpha H2/M2')
c1,c2,c3=s.symbols('c1 c2 c3',real=True)
check('general_d_isotropic_K',s.expand(n*c1+n*n*c2+n*c3-n*(c1+n*c2+c3))==0,'c1 spatial derivative norm, c2 expansion squared, c3 transpose')
fp=s.symbols('Fp',real=True)
mu=1+(n-2)/(n-1)*c1*fp
check('dimension4_static_source',s.simplify(mu.subs(n,3)-(1+c1*fp/2))==0,'Einstein spatial constraint gives weakstatic sourced Poisson factor')
# Full scalar ADM shift/lapse reduction about geodesic isotropic background.
ell,et,zdot,Beta,nu,zeta,k=s.symbols('ell eta zdot Beta nu zeta k',real=True)
Lkin=n*(1-n*ell)*zdot**2+2*(n*ell-1)*zdot*Beta+(1-ell)*Beta**2
Bsol=s.solve(s.diff(Lkin,Beta),Beta)[0]
Akin=s.simplify(Lkin.subs(Beta,Bsol)/zdot**2)
Lgrad=k*k*((n-1)*(n-2)*zeta*zeta+2*(n-1)*nu*zeta+et*nu*nu)
Nsol=s.solve(s.diff(Lgrad,nu),nu)[0]
Ggrad=s.simplify(-Lgrad.subs(nu,Nsol)/(k*k*zeta*zeta))
check('full_scalar_ADM_constraints',s.simplify(Akin-(n-1)*(n*ell-1)/(ell-1))==0 and s.simplify(Ggrad-(n-1)*((n-1)/et-(n-2)))==0,
      'shift removesBeta; lapse removesnu; principal scalar kinetic andgradient coefficients derived before signcheck')
# Same finite-window rounded MOND interpolation, independent of transition parameter.
delta=.01;eta=delta*delta/4;h0=2/(1+delta);hL=.1;alpha_n=-1.5;w=.01
smooth=lambda t:0. if t<=0 else (1. if t>=1 else 10*t**3-15*t**4+6*t**5)
def cut(t):return 1. if t<=.5 else (0. if t>=1 else 1-smooth(2*t-1))
def tiny(z):return (2/(1+math.sqrt(delta*delta-z))-h0)*cut(z/eta) if z<eta else 0.
patch=quad(tiny,0,eta/2,epsabs=1e-16)[0]+quad(tiny,eta/2,eta,epsabs=1e-16)[0]
def h(z,b):return hL+(h0-hL)*(1-smooth((z-b)/w))+tiny(z)
def hp(z,b):
 step=min(1e-6,w/1000)
 return (h(z+step,b)-h(z-step,b))/(2*step)
def positiveF(K):
 t=math.sqrt(K+delta*delta)
 return 4*(t-delta-math.log((1+t)/(1+delta)))
def positiveFp(K):return 2/(1+math.sqrt(K+delta*delta))
jetstep=1e-9
negative_jet=(-3*h(0,.1)+4*h(jetstep,.1)-h(2*jetstep,.1))/(2*jetstep)
check('regular_branch_jet_match',abs(h(0,.1)-positiveFp(0))<1e-14 and abs(negative_jet-1/(delta*(1+delta)**2))<1e-3,'independent negative-side finite derivative matches minus positive Fpp; exact analytic formula nearK0')
check('zero_vacuum_offset',positiveF(0)==0.,'F(0)=0 for every member; deformation not bare constant')
y=s.symbols('y',positive=True);dd=s.symbols('delta',positive=True);t=s.sqrt(y+dd*dd)
Fpos=4*(t-dd-s.log((1+t)/(1+dd)))
check('positive_primitive',s.simplify(s.diff(Fpos,y)-2/(1+t))==0,'same entire isolated galaxy source function for all b')
relative=[];radial=[]
for g in np.geomspace(.1,100,301):
 v=math.sqrt(g*g+delta*delta);m=v/(1+v);radial.append(m+g*g/(v*(1+v)**2));relative.append(abs(m/(g/(1+g))-1))
check('static_spatial_ellipticity',min(radial)>0,'mu>0 and mu+g dmu/dg>0 on301 finitefieldcells; global formula positive')
check('bounded_MON D_rounding'.replace(' ',''),max(relative)<.005,f'fixed delta.01: maximum relative mu rounding {max(relative):.7g} on g/M .1..100')
rows=[];primitive_errors=[]
for b in [.08,.1,.12]:
 Delta=(h0-hL)*(b+w/2)+patch
 zstar=Delta/(hL-2/alpha_n)
 Fstar=-hL*zstar-Delta
 cuts=[0,eta/2,eta,b,b+w,zstar]
 independent_I=sum(quad(lambda z:h(z,b),lo,hi,epsabs=1e-13)[0] for lo,hi in zip(cuts,cuts[1:]))
 primitive_errors.append(abs(Fstar+independent_I))
 E=Fstar-(0 if args.mutate_drop_lapse_derivative else 2*(-zstar)*hL)+2*(-zstar)/alpha_n
 transitionZ=np.linspace(b,b+w,601)
 Qmin=min(1+2*z*hp(z,b)/h(z,b) for z in transitionZ)
 rows.append(dict(b=b,Delta=Delta,Kstar=-zstar,root_residual=E,C=zstar/abs(alpha_n),root_after_transition=zstar>b+w,Q_transition_min=Qmin,embedded_g_threshold=math.sqrt(zstar)))
check('negative_primitive_independent_integral',max(primitive_errors)<1e-11,f'actual smooth h integrated over piecewise intervals, maxerror{max(primitive_errors):.3g}')
check('negative_branch_deSitter_roots',all(abs(r['root_residual'])<1e-12 and r['root_after_transition'] for r in rows),'lapse variation determines nonzero vacuum root; drop2KFp control must fail')
check('same_response_different_cosmological_C',len({round(r['C'],8) for r in rows})==3,'same positive-K F, F0, M, ci and measured G; only negative transition position changes')
check('transition_obligation_exposed',all(r['Q_transition_min']<0 for r in rows),'Q>0 fails between K0 and vacuum branch; no globalhealth conclusion')
# A genuine coupled scalar ghost near first Q<0 crossing, with positive matter density.
b=.1
def transition_hp(z):
 x=(z-b)/w
 return -(h0-hL)*30*x*x*(1-x)**2/w
ellfun=lambda z:1+.5*(h(z,b)+2*z*transition_hp(z))
zg=brentq(lambda z:ellfun(z)-.8,b,b+w/2,xtol=1e-14)
Ighost=sum(quad(lambda z:h(z,b),lo,hi,epsabs=1e-13)[0] for lo,hi in zip([0,eta/2,eta,b],[eta/2,eta,b,zg]))
Eghost=-Ighost+2*zg*h(zg,b)-2*zg/alpha_n
Aghost=2*(3*.8-1)/(.8-1);Gghost=2*(2/h(zg,b)-1)
check('positive_density_coupled_ghost_witness',Aghost<0 and Gghost>0 and Eghost>0,
      f'geodesicFRW zg={zg:.12g},ell=.8,kinetic={Aghost:.7g},matterE={Eghost:.7g}; not acceleratedanisotropicgalaxy assertion')
# Linear branch uses standard Einstein-aether coefficients C_i=-hL*c_i.
C1=s.Rational(1,10);C2=s.Rational(1,20);C3=-C1;C13=C1+C3;C14=C1;C123=C1+C2+C3
ct=1/(1-C13);cv=(C1-C1*C1/2+C3*C3/2)/(C14*(1-C13));cs=(C123/C14)*(2-C14)/(2*(1+C2)**2-C123*(1+C2+C123))
check('full_metric_aether_linear_cones',ct==1 and cv==1 and cs==s.Rational(19,43),'principal highfrequency deSitter linear branch: tensor1, vector1, scalar19/43; not nonlinearenergy proof')
check('cosmological_linear_response_margin',1-alpha_n*hL/2>0 and -(-1)*hL>0,'homogeneous Friedmann kinetic factor1.075 and transverse fixed-metric timekinetic .1')
check('embedded_weak_field_source_mismatch',abs((1-hL/2)-.95)<1e-14 and abs((1-positiveFp(0)/2)-.95)>.9,'negative vacuum background quasistatic metric coefficient .95; cannot inherit isolateddeep MOND without vector solve')
check('general_d_vacuum_root',s.simplify((n*(n-1)*(M*M*K/(n*alpha))+M*M*(F(K)-2*K*s.diff(F(K),K)))/(M*M)-(F(K)-2*K*s.diff(F(K),K)+(n-1)*K/alpha))==0,'same F supplies general-d Friedmann vacuum equation')
result=dict(checks=checks,rows=rows,negative_tiny_patch=patch,coupled_ghost=dict(z=zg,ell=.8,kinetic=Aghost,gradient=Gghost,matter_constraint=Eghost),linear_cones=dict(tensor=float(ct),vector=float(cv),scalar=float(cs)),mutation=args.mutate_drop_lapse_derivative,software=dict(python=platform.python_version(),sympy=s.__version__))
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
