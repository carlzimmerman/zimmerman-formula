import argparse,json,math,pathlib
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','omit_Uprime','freefall_orientation','pressure_sign'],default='none');args=p.parse_args();cks=[]
def ck(n,b,d=None):cks.append({'name':n,'passed':bool(b),'detail':d})
def zero(n,e):ck(n,s.simplify(e)==0,str(s.simplify(e)))
N,B,H,r,w,M,eta,rho,pressure=s.symbols('N B H r w M eta rho p',positive=True);V=-H*r*N*w;chi=1/B**2-H**2*r**2*w**2;F=N**2*B**2*chi;S=rho+pressure;Xi=r*S/(2*M*chi);Pr=pressure+S*H**2*r**2*w**2/chi;pot=M*H**2*(-3+6*eta*s.log(N));VP=-(N**2*(1-B**-2)+V**2+N**2*r**2*(pot+Pr)/M)/(2*r*V)
kappa=B*eta*H*(3*H+(VP+(Xi+2/r)*V)/N);D=(1-B**-2)/(H**2*r**2);wanted=B*eta*H**2*(D+6*eta*s.log(N)-3*(w-1)**2+pressure/(M*H**2))/(2*w)
zero('sourced_crossing_slope',kappa-wanted)
ms=r/2*(1-chi-H*H*r*r);g=-V*(VP+Xi*V)/(N*N*s.sqrt(chi));gwanted=(ms/r**2-H**2*r*(1-3*eta*s.log(N))+r*pressure/(2*M))/s.sqrt(chi)
zero('sourced_physical_force',g-gwanted)
# Source contributions cancel in exact current/Euler identity.
E=N*N*S/F-pressure;P=pressure+B*B*V*V*S/F;Sv=N*B**3*r*r*V*S/F
zero('staticfluid_current_source_cancels',V*B*r*r*E+V*B*r*r*P-(V*V/N+N/B**2)*Sv)
# Numeric exact cutoff and short local vacuum system, no source force imposed.
HH=1.;ee=.5;AA=1.;TT=128.9153707043

def hh(y):
 if y==0:return 0.,float('inf')
 R=math.sqrt(1+1/y);b=1/(R+1);bp=1/(2*y*y*R*(R+1)**2);den=1+(y/TT)**2;return b/den,bp/den-b*(2*y/TT**2)/(den*den)
def response(a):
 g=abs(a)
 if g==0:return 0.,0.,2.,0.
 target=g/AA;y=brentq(lambda z:z+hh(z)[0]-target,0.,target,xtol=1e-30,rtol=1e-14);h,hp=hh(y);J=quad(lambda z:2*z*hh(z*z)[0] if z else 0.,0.,math.sqrt(y),epsabs=1e-28,epsrel=1e-11)[0];Q=AA*AA*(h*h+2*J);Qp=math.copysign(2*AA*h,a);Qpp=2*hp/(1+hp);return Q,Qp,Qpp,Q-a*Qp

def rhs(rr,y):
 nn,bb,v,a=y;np_=a*nn*bb;bp=bb*(-np_/nn-ee*HH*rr*np_/v);Q,Qp,Qpp,press=response(a);U=-3*HH*HH+6*ee*HH*HH*math.log(nn)
 vp=-nn/(2*rr*v)*(nn*(1-bb**-2)-2*rr*np_/bb**2+v*v/nn-2*rr*v*v*np_/nn**2-2*ee*HH*rr*rr*v*np_/nn+nn*rr*rr*(U+press))
 jK=2*ee*HH*(np_/bb**2-3*HH*v-v/nn*(vp+(bp/bb+2/rr)*v));ap=(-bb*jK/v-2*Qp/rr)/Qpp
 return np.array([np_,bp,vp,ap])
r0=.001;N0=.99999;w0=.5;mm=1e-8;mu=mm/r0**3;d=2*mu+1-w0*w0;B0=1/math.sqrt(1-r0*r0*d);V0=-r0*N0*w0;y0=np.array([N0,B0,V0,0.]);f0=rhs(r0,y0);kap=f0[3];theta=-(f0[2]+2*V0/r0)/N0;F0=N0*N0-B0*B0*V0*V0
ck('point_metric_admissible',F0>0 and N0>0 and B0>0);ck('desired_positive_crossing',kap>0,kap);ck('isolatedzero_not_expansion3H',abs(theta-3)>1,theta);ck('point_slope_formula',math.isclose(kap,B0*ee*(d+6*ee*math.log(N0)-3*(w0-1)**2)/(2*w0),rel_tol=2e-12))
N2=N0*B0*kap;B2=-B0*B0*kap*(1-ee/w0);Upot=-3+6*ee*math.log(N0);V2=N0*N2/(V0*B0**2)+V0*N2/N0+ee*r0*N2-2*f0[2]/r0-f0[2]**2/V0-N0*N0*Upot/V0
fd=(rhs(r0+1e-9,y0+f0*1e-9)-rhs(r0-1e-9,y0-f0*1e-9))/(2e-9)
for idx,expected,name in [(0,N2,'N2'),(1,B2,'B2'),(2,V2,'V2')]:ck('Taylor_'+name,math.isclose(fd[idx],expected,rel_tol=2e-5,abs_tol=2e-5),[fd[idx],expected])
# Exactfreefall zero-point is a validmetric but haswrongcrossingorientation.
wff=math.sqrt(2*mu+1);kff=ee*(-3*(wff-1)**2)/(2*wff);ck('freefall_wrong_orientation',kff<0,kff)
records=[];ends=[]
for direction in [-1.,1.]:
 end=r0+direction*1e-6;sol=solve_ivp(rhs,(r0,end),y0,method='DOP853',rtol=2e-10,atol=2e-13,max_step=1e-7,dense_output=True);ref=solve_ivp(rhs,(r0,end),y0,method='DOP853',rtol=2e-12,atol=2e-15,max_step=5e-8,dense_output=True)
 ck('local_IVP_success_'+str(direction),sol.success and ref.success);diff=np.max(np.abs(sol.y[:,-1]-ref.y[:,-1]));ck('tolerance_refinement_'+str(direction),diff<2e-10,float(diff));ends.append(sol.y[:,-1].tolist());pts=[]
 for rr in np.linspace(r0,end,9):
  nn,bb,v,a=sol.sol(rr);Np,Bp,Vp,ap=rhs(rr,[nn,bb,v,a]);F=nn*nn-bb*bb*v*v;Q,Qp,Qpp,press=response(a);jK=2*ee*(Np/bb**2-3*v-v/nn*(Vp+(Bp/bb+2/rr)*v));current=jK+v/(bb*rr*rr)*(2*rr*Qp+rr*rr*Qpp*ap)
  Up=-3+6*ee*math.log(nn);EN=bb-1/bb+2*rr*Bp/bb**2+((bb+2*rr*Bp)*v*v+2*rr*bb*v*Vp)/nn**2+2*ee*(Bp*rr*rr*v+bb*2*rr*v+bb*rr*rr*Vp)/nn+bb*rr*rr*(Up+6*ee+press)-(2*rr*Qp+rr*rr*Qpp*ap)
  pts.append({'lapse_residual':float(EN),'r':float(rr),'N':float(nn),'B':float(bb),'V':float(v),'a':float(a),'a_prime':float(ap),'F':float(F),'Uaa':float(Qpp),'qjr':float(current)})
 ck('two_sided_signed_cross_'+str(direction),direction*sol.y[3,-1]>0);ck('regular_clock_metric_patch_'+str(direction),all(v['F']>0 and v['Uaa']>1.99 and v['V']<0 for v in pts));ck('zero_current_constraint_'+str(direction),max(abs(v['qjr']) for v in pts)<1e-13)
 ck('full_lapse_equation_'+str(direction),max(abs(v['lapse_residual']) for v in pts)<1e-13)
 delta=direction*1e-6;nt=N0+.5*N2*delta**2;bt=B0+.5*B2*delta**2;vt=V0+f0[2]*delta+.5*V2*delta**2;ck('local_metric_Taylor_control_'+str(direction),abs(sol.y[0,-1]-nt)<5e-13 and abs(sol.y[1,-1]-bt)<5e-13 and abs(sol.y[2,-1]-vt)<5e-8);records.append({'direction':direction,'nfev':sol.nfev,'refinement_nfev':ref.nfev,'samples':pts,'end_difference':float(diff)})
if args.control=='omit_Uprime':ck('CONTROL_false_geodesic_interval_condition',math.isclose(theta,3.,rel_tol=1e-12))
if args.control=='freefall_orientation':ck('CONTROL_false_freefall_positive_cross',kff>0)
if args.control=='pressure_sign':zero('CONTROL_wrong_pressure_sign',g-((ms/r**2-H**2*r*(1-3*eta*s.log(N))-r*pressure/(2*M))/s.sqrt(chi)))
result={'passed':all(v['passed'] for v in cks),'checks':cks,'point':{'r':r0,'N':N0,'B':B0,'V':V0,'mass_MS':mm,'mu':mu,'theta':theta,'kappa':float(kap),'N2':float(N2),'B2':float(B2),'V2':float(V2)},'local_integrations':records,'control':args.control,'non_claims':['No globalMOND/freefall/cosmicmatching','Localmassnotbaryoniccalibration','No centerfluidconstruction','No fullfinitegradientcharacteristics','No A/Hselector']};out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(cks),'failed':[v['name'] for v in cks if not v['passed']]}));raise SystemExit(0 if result['passed'] else 1)
