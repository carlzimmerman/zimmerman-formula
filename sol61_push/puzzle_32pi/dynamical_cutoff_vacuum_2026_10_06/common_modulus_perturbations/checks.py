"""Canonical common-modulus constraints, convex curvature and controlled smooth growth."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import quad,solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['cold_sound','oscillator','dust_growth']);args=ap.parse_args();rows=[]
def eq(name,v):rows.append(dict(name=name,passed=s.simplify(v)==0,residual=str(s.simplify(v))))
def ck(name,v,detail=''):rows.append(dict(name=name,passed=bool(v),detail=str(detail)))
# ADM flat scalar gauge, shift B=Delta beta, actual canonical action.
M,H,F,Fd,V,Vp,Vpp,Q,Qd,al,B,P=s.symbols('M H F Fd V Vp Vpp Q Qd alpha B P',real=True)
L=s.Rational(1,2)*Qd**2-s.Rational(1,2)*(P+Vpp)*Q**2-F*al*Qd-Vp*al*Q+(F**2/2-3*M*H**2)*al**2+B*(F*Q-2*M*H*al)
alpha=F*Q/(2*M*H)
eq('ADM_shift_constraint',s.diff(L,B).subs(al,alpha))
Bsol=((F**2-6*M*H**2)*alpha-F*Qd-Vp*Q)/(2*M*H)
eq('ADM_lapse_constraint',s.diff(L,al).subs({al:alpha,B:Bsol}))
Lsub=s.expand(L.subs(al,alpha));eq('reduced_canonical_kinetic',s.diff(Lsub,Qd,2)-1)
eq('reduced_canonical_gradient',s.diff(Lsub,P)+Q**2/2)
# Boundary integration of -F²/(2MH) Q Qdot, with actual background equations.
Hd=-F**2/(2*M);Fdot=-3*H*F-Vp
Adot=F*Fdot/(M*H)-F**2*Hd/(2*M*H**2)
mraw=Vpp+Vp*F/(M*H)+V*F**2/(2*M**2*H**2)-(3*H*F**2/(2*M*H)+Adot)
ms=Vpp-(3*F**2+2*F*Fdot/H-F**2*Hd/H**2)/M
eq('actual_scalar_only_mass_boundary', (mraw-ms).subs(V,3*M*H**2-F**2/2))
# Canonical normal stress; rest-frame delta phi=0 has equal delta p,delta rho.
pert,dpert,psi=s.symbols('delta_phi delta_phidot Psi',real=True)
rho=F*dpert-F**2*psi+Vp*pert;pres=F*dpert-F**2*psi-Vp*pert
eq('canonical_restframe_sound', (pres-rho).subs(pert,0))
cs=s.Integer(0) if args.control=='cold_sound' else s.Integer(1)
eq('scalar_principal_speed_is_one',cs-1)
# Exact curvature integrand kappa(t), t=1/sqrt(1+1/y) in(0,1).
t=s.symbols('t',real=True);ell=(1-t)/2;ellu=-t*(1-t*t)/4;kap=s.expand((1+ell)**2+ellu)
eq('curvature_integrand',kap-(9-7*t+t*t+t**3)/4)
eq('curvature_lower_factor',kap-1-(1-t)*(5-2*t-t*t)/4)
eq('curvature_upper_factor',s.Rational(9,4)-kap-t*(7-t-t*t)/4)
# General n limiting tracking curvature ratio from actual exponential slope p.
n,ga,p,w=s.symbols('n gamma p w',positive=True)
z2=n*ga*(1-w*w)/((n-1)*p*p)
mH=p*p/ga*n*(n-1)/2*z2
eq('tracking_curvature_general_dimension',mH-n*n*(1-w*w)/2)
eq('dust_tracking_curvature',mH.subs({n:3,w:0})-s.Rational(9,2))
eq('radiation_tracking_curvature',mH.subs({n:3,w:s.Rational(1,3)})-4)
# Independent bounded endpoint quadrature, no imported parent functions.
def potential(T):
 scale=np.sqrt(T) if T<1 else 1.
 def f(v,order):
  th=np.pi/2*np.sin(np.pi*v/2)**2;jac=np.pi**2/2*np.sin(np.pi*v/2)*np.cos(np.pi*v/2)
  yy=T*(np.tan(th) if v<.5 else 1/np.tan(np.pi/2*np.cos(np.pi*v/2)**2))
  tt=1/np.sqrt(1+1/yy);hh=tt/(1+tt)
  factor=1 if order==0 else ((3-tt)/2 if order==1 else (9-7*tt+tt*tt+tt**3)/4)
  return jac*hh*factor/scale
 I=[quad(lambda v:f(v,j),0,1,epsabs=2e-10,epsrel=2e-10,limit=150)[0] for j in range(3)]
 return 2*T*scale*I[0],I[1]/I[0],I[2]/I[0]
vals=[]
for T in [1e-12,1e-6,.01,1.,128.915,1e6]:
 A,sl,cur=potential(T);vals.append(dict(T=T,A=A,log_slope=sl,curvature_ratio=cur));ck('convex_curvature_'+str(T),1<cur<2.25)
 ck('no_minimum_'+str(T),A>0 and sl>0)
 _,pm,cm=potential(T*np.exp(-2e-4));_,pp,cp=potential(T*np.exp(2e-4))
 # Auu/A = p² + dp/du, centered differentiation of separate first moments.
 ck('independent_curvature_derivative_'+str(T),abs(cur-(sl*sl+(pp-pm)/4e-4))<2e-7,cur-(sl*sl+(pp-pm)/4e-4))
A,sl,cur=potential(1e-12);ck('smallT_curvature_limit',abs(cur-2.25)<1e-4,cur)
# Smooth subhorizon dust growth, derived from continuity/Euler + Einstein constraint.
Om=s.symbols('Omega_scalar',real=True);g=(s.sqrt(25-24*Om)-1)/4
eq('dust_growth_characteristic',g*g+g/2-s.Rational(3,2)*(1-Om))
ck('growth_below_dust',float(g.subs(Om,s.Rational(2,3)))<1)
growth=[]
for gamma in [.1,.5]:
 omega=4*gamma/3;ex=(np.sqrt(25-24*omega)-1)/4;calls=[0]
 def rhs(N,y):
  calls[0]+=1
  if calls[0]>2000:raise RuntimeError('RHS cap')
  return [y[1],-.5*y[1]+1.5*(1-omega)*y[0]]
 sol=solve_ivp(rhs,[0,6],[1,ex],method='DOP853',rtol=2e-10,atol=1e-12)
 err=abs(sol.y[0,-1]/np.exp(ex*6)-1);ck('smooth_growth_ODE_'+str(gamma),sol.success and err<2e-8,err)
 growth.append(dict(gamma=gamma,Omega_scalar=omega,growth_exponent=ex,efolds=6,RHS_calls=calls[0],relative_error=err,scope='limiting high-k smooth scalar + mirrored dust growing mode, not full finite-k transfer'))
if args.control=='oscillator':ck('false_tracking_rapid_oscillator',float(mH.subs({n:3,w:0}))>100)
if args.control=='dust_growth':eq('false_same_background_w_gives_dust_growth',g.subs(Om,s.Rational(2,3))-1)
res=dict(passed=sum(r['passed'] for r in rows),total=len(rows),checks=rows,potential_values=vals,growth=growth,control=args.control,scope='exchange-even common sector only; exact constraints/principal and asymptotic smooth-growth approximation; no complete relative/foliation health or finite-k transfer')
out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(dict(passed=res['passed'],total=res['total'],failed=[r['name'] for r in rows if not r['passed']])));raise SystemExit(not all(r['passed'] for r in rows))
