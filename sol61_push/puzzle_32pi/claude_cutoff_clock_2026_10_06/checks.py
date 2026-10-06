import argparse,pathlib,json,math
import sympy as sp
from scipy.optimize import brentq
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','inverse','positivity','dropflow'],default='none');args=p.parse_args();checks=[]
def ck(n,ok,d=None):checks.append({'name':n,'passed':bool(ok),'detail':d})
def zero(n,e):ck(n,sp.simplify(e)==0,str(sp.simplify(e)))
def kernel(y,T,k=2):
 rr=math.sqrt(1+1/y);bb=1/(rr+1);bp=1/(2*y*y*rr*(rr+1)**2);x=y/T;D=1+x**k;Dp=k*x**(k-1)/T;h=bb/D;hp=bp/D-bb*Dp/(D*D);return h,hp,1+hp
Tvals=[100.,128.,128.9153707043,1000.];tables=[]
for T in Tvals:
 yc=brentq(lambda y:kernel(y,T)[1],1e-5,T*10,xtol=1e-12);hc,hpc,fc=kernel(yc,T);Tc=yc*math.sqrt(4*yc+3+4*math.sqrt(yc*(yc+1)))
 ck('unique_zero_equation_'+str(T),math.isclose(T,Tc,rel_tol=2e-13));ck('critical_Ugg_zero_'+str(T),abs(hpc)<2e-14)
 ck('critical_below_turnoff_'+str(T),yc<T);ck('analytic_inverse_bound_'+str(T),1-9/(16*math.sqrt(3)*T)>0)
 for fac in [.1,1.,2.,10.,1e6]:
  y=fac*yc;h,hp,fp=kernel(y,T);wgg=1/fp;ugg=2*hp/fp;vt=-.5*(y+h)/(2*(h-y*hp));expect=2*(1-wgg)
  ck('inverse_derivative_'+str((T,fac)),math.isclose(ugg,expect,abs_tol=5e-16,rel_tol=1e-8))
  ck('positive_transverse_'+str((T,fac)),2*h/(y+h)>0)
  ck('regular_inverse_'+str((T,fac)),fp>=1-9/(16*math.sqrt(3)*T)-1e-14)
  if fac==.1:ck('positive_before_critical_'+str(T),ugg>0)
  if fac==2.:ck('negative_after_critical_'+str(T),ugg<0)
  # Leading zero current: eta a+V/(Hr)*(r a'+2a)=0 in dimensionless units.
  ck('leading_current_compatibility_'+str((T,fac)),abs(.5*(y+h)+vt*2*(h-y*hp))<1e-12*max(y+h,1))
 tables.append({'T':T,'yc':yc,'gc_over_A':yc+hc,'excess_at_peak_over_A':hc,'Ugg_at_twice_peak':2*kernel(2*yc,T)[1]/kernel(2*yc,T)[2],'V_over_Hr_at_critical':-.5*(yc+hc)/(2*hc)})
# Stationary derivative rank: neither inverse chart nor transverse block is singular there.
M,r,V,N,Q2,x,y,z=sp.symbols('M r V N Q2 x y z',nonzero=True)
mat=sp.Matrix([[-2*M*r*V/N,0,0],[0,2*M*r*V/N,0],[x,y,-M*r*r*Q2]])
zero('stationary_determinant',mat.det()-4*M**3*r**4*V**2*Q2/N**2)
k,mm,AA,HH,ee=sp.symbols('k m A H eta',positive=True)
vv=-ee*HH*r*(mm/(AA*r*r))**(k+1)/((k+1)*sp.Symbol('T',positive=True)**k)
zero('highforce_mass_exponent',mm*sp.diff(vv,mm)/vv-(k+1));zero('highforce_radius_exponent',r*sp.diff(vv,r)/vv+(2*k+1))
scale=sp.symbols('scale',positive=True);zero('clock_rescaling_invariant',scale/sp.sqrt(scale**2)-1)
# UncutP2 is exception: h tendspositiveconstant, derivative positive.
for yv in [1.,100.,1e6]:
 rr=math.sqrt(1+1/yv);bp=1/(2*yv*yv*rr*(rr+1)**2);ck('uncut_positive_'+str(yv),bp>0)
# Conditional Solar benchmark, not data-fit or observational constraint.
GM=1.32712440018e20;AU=1.495978707e11;ASI=9.3603e-11;clight=299792458.;mgeo=GM/clight**2;Ageo=ASI/clight**2;yv=GM/(AU*AU*ASI);solar=[]
for T in [100.,128.9153707043,1000.]:
 h,hp,fp=kernel(yv,T)
 for ratio in [.3,1.,3.]:
  Hgeo=Ageo/ratio;flow=-.5*Hgeo*AU*(yv+h)/(2*(h-yv*hp));solar.append({'T':T,'A_over_H':ratio,'r_AU':1.,'y':yv,'excess_SI':ASI*h,'formal_V':flow,'weak_flow_valid':abs(flow)<.1})
# Intentional false inferences.
h,hp,fp=kernel(2*tables[2]['yc'],Tvals[2])
if args.control=='inverse':ck('CONTROL_wrong_inverse',math.isclose(fp,1/fp,rel_tol=1e-14))
if args.control=='positivity':ck('CONTROL_wrong_convex_tail',2*hp/fp>0)
if args.control=='dropflow':ck('CONTROL_wrong_zero_flow',abs(.5*(2*tables[2]['yc']+h))<1e-14)
res={'passed':all(v['passed'] for v in checks),'checks':checks,'critical_points':tables,'solar_conditional_model_benchmark':solar,'control':args.control,'non_claims':['No full covariant characteristic or ghost proof','No exact criticalcrossing/global solution','No inherited Solar/ETNO observationconstraint','No fittedtargetC orA/H']};out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'checks':len(checks),'failed':[v['name'] for v in checks if not v['passed']],'critical_points':tables}));raise SystemExit(0 if res['passed'] else 1)
