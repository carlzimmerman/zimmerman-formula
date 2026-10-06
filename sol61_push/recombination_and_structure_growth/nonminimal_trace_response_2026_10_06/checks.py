"""Conformal trace conservation and controlled first-order dust forcing at stable cutoff."""
from pathlib import Path
import argparse,json
import numpy as np
import sympy as s
from scipy.integrate import quad,solve_ivp
from scipy.optimize import brentq
from scipy.special import expit
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['radiation_density','dust_frozen','adiabatic']);args=ap.parse_args();rows=[]
def eq(n,x):rows.append(dict(name=n,passed=s.simplify(x)==0,residual=str(s.simplify(x))))
def ck(n,b,d=''):rows.append(dict(name=n,passed=bool(b),detail=str(d)))
n,w,al,rho,v,H,Uprime=s.symbols('n w alpha rho velocity H Uprime',real=True)
trace=1-n*w;Fmatter=al*trace*rho*v;Fscalar=-al*trace*rho*v
eq('total_energy_exchange_cancel',Fmatter+Fscalar)
eq('radiation_trace_vanishes',trace.subs(w,1/n))
eq('dust_trace_nonzero',trace.subs(w,0)-1)
eq('frame_density_exponent',n+1-n*(1+w)-trace)
# Action variation: scalar □ψ-Uψ+αT=0, T=−(1−nw)ρ.
acc=-n*H*v-Uprime-al*trace*rho
rhophidot=v*(acc+Uprime);eq('scalar_conservation_from_EL',rhophidot+n*H*v*v-Fscalar)
# Canonical potential and coupling independently evaluated from retained kernel.
def moments(u):
 def f(v,j):
  t=np.sqrt(expit(u+v));h=t/(1+t);k=np.exp(-abs(v))/(1+np.exp(-2*abs(v)));ell=(1-t)/2
  return h*k*[1,ell,np.tanh(v),ell*np.tanh(v)][j]
 ints=[quad(lambda v:f(v,j),-np.inf,np.inf,epsabs=2e-11,epsrel=2e-11,limit=180)[0] for j in range(4)]
 J=ints[0];p=1+ints[1]/J;dp=ints[3]/J-ints[1]*ints[2]/J**2
 return 2*np.exp(u)*J,p,dp
F0=1.;curv=10.;gamma=.1;nn=3;dd=4;beta=1.
def coupling(u):
 F=F0+curv*u*u;q=2*curv*u/F;qp=2*curv*(F0-curv*u*u)/(F*F)
 A,p,pp=moments(u);z=gamma/F+nn/(nn-1)*q*q;alpha=-q/((nn-1)*np.sqrt(z));Lpp=pp-beta*qp;mu2=nn*(nn-1)/2*Lpp/z
 return dict(F=F,A=A,q=q,qprime=qp,p=p,pprime=pp,Z_over_M=z,alpha_sqrt_M=alpha,logU_second=Lpp,mass2_Hvac2=mu2)
u0=brentq(lambda u:moments(u)[1]-2*curv*u/(F0+curv*u*u),1.,2.,xtol=1e-12);c=coupling(u0);alpha=c['alpha_sqrt_M'];mu=c['mass2_Hvac2']
ck('stable_actual_vacuum',abs(c['p']-c['q'])<1e-10 and c['logU_second']>0,c)
ck('negative_actual_matter_coupling',alpha<0,alpha)
ck('light_actual_vacuum_scalar',0<mu<1,mu)
# Exact first-order deSitter retarded solution; N=Hvac(t−t0).
N=s.symbols('N',real=True);m2,source=s.symbols('m2 source',positive=True)
lam_p=(-3+s.sqrt(9-4*m2))/2;lam_m=(-3-s.sqrt(9-4*m2))/2
X=source/m2*(s.exp(-3*N)-lam_p/(lam_p-lam_m)*s.exp(lam_p*N)+lam_m/(lam_p-lam_m)*s.exp(lam_m*N))
eq('retarded_initial_value',X.subs(N,0));eq('retarded_initial_velocity',s.diff(X,N).subs(N,0))
eq('retarded_actual_forcing',s.diff(X,N,2)+3*s.diff(X,N)+m2*X-source*s.exp(-3*N))
lp=float(lam_p.subs(m2,mu));lm=float(lam_m.subs(m2,mu));amp=-3*alpha
ck('retarded_overdamped_rates',lm<lp<0,[lp,lm])
# Tiny mirrored dust is added to exact scalar-vacuum+radiation background.
# Solve X=(δψ/sqrtM)/epsilon, with positive dust amplitude epsilon U0.
sols=[]
for R0 in [0.,10.]:
 calls=[0]
 def rhs(N,y):
  calls[0]+=1
  if calls[0]>4000:raise RuntimeError('RHS cap')
  R=R0*np.exp(-4*N);hh=-2*R/(1+R);force=-3*alpha*np.exp(-3*N)/(1+R)
  return [y[1],-(3+hh)*y[1]-mu/(1+R)*y[0]+force]
 coarse=solve_ivp(rhs,[0,8],[0,0],method='DOP853',rtol=2e-9,atol=2e-12,dense_output=True)
 fine=solve_ivp(rhs,[0,8],[0,0],method='DOP853',rtol=2e-10,atol=2e-13,dense_output=True)
 grid=np.linspace(0,8,201);ya=coarse.sol(grid);yb=fine.sol(grid);err=float(np.max(np.abs(ya-yb)/(1+np.max(np.abs(yb),axis=1)[:,None])))
 ck('trace_integrator_'+str(R0),coarse.success and fine.success and err<2e-8,err)
 ck('positive_dust_departure_'+str(R0),np.min(yb[0])>=0 and np.max(yb[0])>0,float(np.max(yb[0])))
 epsilon=1e-5;peak=float(np.max(np.abs(yb[0])));delta_u=epsilon*peak/np.sqrt(c['Z_over_M'])
 ck('small_declared_cutoff_displacement_'+str(R0),delta_u<1e-4,delta_u)
 instant=amp/mu*np.exp(-3*grid);ratio=float(yb[0,-1]/instant[-1])
 ck('retarded_not_generic_instantaneous_minimum_'+str(R0),ratio>1000,ratio)
 if R0==0:
  exact=s.lambdify((N,m2,source),X,'numpy')(grid,mu,amp)
  ck('independent_retarded_exact_'+str(R0),np.max(np.abs(exact-yb[0]))<2e-9,float(np.max(np.abs(exact-yb[0]))))
 sols.append(dict(initial_radiation_over_U=R0,efolds=8,RHS_calls=calls[0],epsilon=epsilon,end_X=float(yb[0,-1]),peak_X=peak,peak_delta_u=delta_u,late_instantaneous_minimum_ratio=ratio,tolerance_error=err,scope='first-order in epsilon, not large dust cosmology or nonlinearfulltheory'))
# Actual force residuals of purported frozen solutions are the controls.
if args.control=='radiation_density':eq('false_radiation_totaldensity_force',(-al*rho)-( -al*trace*rho).subs(w,1/n))
if args.control=='dust_frozen':ck('false_constant_cutoff_with_dust',abs(alpha)<1e-12,alpha)
if args.control=='adiabatic':ck('false_retarded_equals_instantaneous_minimum',sols[0]['late_instantaneous_minimum_ratio']<1.01,sols[0]['late_instantaneous_minimum_ratio'])
res=dict(passed=sum(x['passed'] for x in rows),total=len(rows),checks=rows,vacuum=dict(u0=u0,T0=float(np.exp(u0)),F0=F0,curvature_coefficient=curv,gamma=gamma,**c),retarded_rates=[lp,lm],trace_solutions=sols,control=args.control,scope='consistent common mirroredfluid Einsteinframe, exact radiationtrace and controlled firstorder dust forcing; no real recombination, ordinary-only source or operationala0dictionary')
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(dict(passed=res['passed'],total=res['total'],failed=[x['name'] for x in rows if not x['passed']])));raise SystemExit(not all(x['passed'] for x in rows))
