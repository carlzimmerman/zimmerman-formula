"""Formal leading weak-field scalar reduction: nonlinear potential and frozen modes."""
import sympy as s
import json,math,sys
from pathlib import Path
K,a0,p=s.symbols('K a0 p',positive=True)
q=s.symbols('q',positive=True)
W=a0*a0/K*(-K*p/a0-s.log(1-K*p/a0))
F=W-K*p*p/2
if '--mutate' in sys.argv:F=s.S.Zero
Fr=s.factor(s.diff(F,p)); Frr=s.factor(s.diff(F,p,2)); Ft=s.factor(Fr/p)
qsub={p:a0*q/K}
checks={'radial_Hessian':s.simplify(Frr.subs(qsub)-K*((1-q)**-2-1))==0,
 'tangential_Hessian':s.simplify(Ft.subs(qsub)-K*((1-q)**-1-1))==0}
x=s.symbols('x',positive=True)
# Field strength x=g/a0 and equilibrium polarization q=x/(1+x).
checks['equilibrium_source_law']=s.simplify(Fr.subs(p,a0*x/(K*(1+x)))-a0*x*x/(1+x))==0
checks['energy_remainder_derivative']=s.simplify(Fr.subs(qsub)-a0*q*q/(1-q))==0
# Orthogonal direct Cartesian Hessian, evaluated on axis P=(p,0,0).
u,v,z=s.symbols('u v z',real=True)
norm=s.sqrt(u*u+v*v+z*z)
Fc=F.subs(p,norm)
H=s.hessian(Fc,(u,v,z)).subs({u:p,v:0,z:0})
checks['cartesian_Hessian']=all(s.simplify(H[i,j]-(Frr if i==j==0 else Ft if i==j else 0))==0 for i in range(3) for j in range(3))
ct=s.symbols('cos_theta',real=True)
Hdir=s.factor((Ft+(Frr-Ft)*ct**2).subs(p,a0*x/(K*(1+x))))
checks['angular_stiffness']=s.simplify(Hdir-K*(x+(x+x*x)*ct**2))==0
wr=s.factor(Frr.subs(p,a0*x/(K*(1+x)))+K); wt=s.factor(Ft.subs(p,a0*x/(K*(1+x)))+K)
WLL=wt+(wr-wt)*ct**2
WTT=wr-(wr-wt)*ct**2
WLTsq=(wr-wt)**2*ct**2*(1-ct**2)
Heff=s.factor(WLL-K-WLTsq/WTT)
checks['transverse_eliminated_stiffness']=s.simplify(Heff-K*x*(1+x+ct**2)/(1+x-x*ct**2))==0
checks['parallel_decoupling']=s.simplify(Heff.subs(ct,1)-K*x*(2+x))==0
checks['perpendicular_decoupling']=s.simplify(Heff.subs(ct,0)-K*x)==0
checks['vacuum_Hessian_limit']=s.limit(Frr,p,0)==0 and s.limit(Ft,p,0)==0
# Illustration, not a galaxy solution; SI values only in dimensionless ratios / response.
beta=.02798; L=24*3.085677581491367e16; R=10e3*3.085677581491367e16
eta_over_K=L*L/2; B_over_K=(2+3*beta)/beta; k=1/R;c=299792458.
Gyr=365.25*86400*1e9
rows=[]
for cosine in [0.,1.]:
 factor=1+2*cosine*cosine
 if '--mutate' in sys.argv:factor=0.
 omega=c*math.sqrt((factor*k*k+eta_over_K*k**4)/(B_over_K+eta_over_K*k*k))
 omega_v=c*math.sqrt(eta_over_K*k**4/(B_over_K+eta_over_K*k*k))
 rows.append({'cos_theta':cosine,'H_over_K':factor,'response_Gyr':1/omega/Gyr,'vacuum_response_Gyr':1/omega_v/Gyr,'response_speed_c':omega/(c*k),'k2_over_k4':factor/(eta_over_K*k*k)})
result={'checks':checks,'all_pass':all(checks.values()),'Fprime':str(Fr),'radial_Hessian':str(Frr),'tangential_Hessian':str(Ft),'angular_Hessian_scalar_restricted':str(Hdir),'low_k_full_vector_stiffness':str(Heff),'illustration':rows,'assumptions':{'x':1,'beta':beta,'L_pc':24,'inverse_wavenumber_kpc':10,'eta_over_gamma':1,'footings':'same at fixed x and L; not independent predictions'},'mutated':'--mutate' in sys.argv}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
for name,ok in checks.items():print(name,'PASS' if ok else 'FAIL')
print('COMPLETE',sum(checks.values()),'/',len(checks))
print(json.dumps(rows))
sys.exit(0 if all(checks.values()) else 1)
