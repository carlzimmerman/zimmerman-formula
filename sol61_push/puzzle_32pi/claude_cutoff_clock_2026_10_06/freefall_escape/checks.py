import argparse,json,math,pathlib
from scipy.optimize import brentq
from scipy.integrate import quad
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','geodesic','physical_clock'],default='none');args=p.parse_args();checks=[]
def ck(n,ok,d=None):checks.append({'name':n,'passed':bool(ok),'detail':d})
T=128.9153707043;eta=.5;M=1.
def kern(y):
 if y==0:return 0.,float('inf')
 rr=math.sqrt(1+1/y);bb=1/(rr+1);bp=1/(2*y*y*rr*(rr+1)**2);D=1+(y/T)**2;dp=2*y/T**2;return bb/D,bp/D-bb*dp/D**2
yc=brentq(lambda y:kern(y)[1],1.,100.);hmax=kern(yc)[0]
def roots(d):
 low=brentq(lambda z:kern(math.exp(z))[0]-d,-100.,math.log(yc),xtol=1e-13);high=brentq(lambda z:kern(math.exp(z))[0]-d,math.log(yc),100.,xtol=1e-13);return math.exp(low),math.exp(high)
def clock(rr,R=1.,mass=1.):
 v0=-math.sqrt(2*mass/rr);d=eta*abs(v0)/R;y,_=roots(d);h,hp=kern(y);alpha=-R*(y+h);return alpha,y,h,hp,v0
rows=[]
for rr in [50.,100.,200.]:
 alpha,y,h,hp,v0=clock(rr);ck('low_root_positive_Hessian_'+str(rr),hp>0 and 2*hp/(1+hp)>0);ck('low_phantom_equation_'+str(rr),math.isclose(h,eta*abs(v0),rel_tol=2e-13))
 hi=roots(eta*abs(v0))[1];ck('separate_high_root_negative_Hessian_'+str(rr),hi>yc and kern(hi)[1]<0)
 I=quad(lambda xx:clock(xx)[0],100.,rr,epsabs=1e-11,epsrel=1e-11)[0]
 J=quad(lambda zz:2*zz*kern(zz*zz)[0] if zz else 0.,0.,math.sqrt(y),epsabs=1e-14,epsrel=1e-12)[0]
 residuals=[]
 for H in [1e-6,5e-7,2.5e-7]:
  A=H;N=1+H*I;B=1/N;P=H*alpha;BP=-P/N**2;F=1-2/rr-H*H*rr*rr;Fp=2/rr**2-2*H*H*rr;D=N*N-F;V=-N*math.sqrt(D);VP=-P*math.sqrt(D)-N*(2*N*P-Fp)/(2*math.sqrt(D));c=3*eta*H*H;bcoef=2*eta*H;pot=-3*H*H+2*c*math.log(N)
  a=P;Q=A*A*(h*h+2*J);Qp=-2*A*h;Q2=2*hp/(1+hp);Qprime_r=2*eta*H*(-v0/(2*rr));press=Q-a*Qp
  EB=N*(1-1/B**2)-2*rr*P/B**2+(V*V+2*rr*V*VP)/N-2*rr*V*V*P/N**2-bcoef*rr*rr*V*P/N+N*rr*rr*(pot+press)
  EN=B-1/B+2*rr*BP/B**2+((B+2*rr*BP)*V*V+2*rr*B*V*VP)/N**2+bcoef*(B*rr*rr*VP+BP*rr*rr*V+2*B*rr*V)/N+B*rr*rr*(pot+2*c+press)-(2*rr*Qp+rr*rr*Qprime_r)
  mom=V*(BP/B+P/N)+eta*H*rr*P
  current=bcoef*(P/B**2-3*H*V-V/N*(VP+(BP/B+2/rr)*V))+V/(B*rr*rr)*(2*rr*Qp+rr*rr*Qprime_r)
  # Compare with truly geodesic Schwarzschildfreefall at sameH: zero response thencurrentO(H).
  geo_current=bcoef*(-3*H*v0-v0*(-v0/(2*rr)+2*v0/rr))
  ck('exact_trial_metric_'+str((rr,H)),math.isclose(N*N-B*B*V*V,F,abs_tol=5e-15));ck('weak_nearlygeodesic_'+str((rr,H)),abs(a)<.15*A and abs(a)/(1/rr**2)<.004)
  residuals.append({'H':H,'EB':EB,'EN':EN,'momentum':mom,'qjr':current,'geodesic_qjr':geo_current,'N':N,'B':B,'V':V,'clock_signed':a,'Uaa':Q2,'H_r_over_V0':H*rr/abs(v0)})
 for key in ['EB','EN','momentum','qjr']:
  scaled=[v[key]/v['H']**2 for v in residuals];ck('orderH2_residual_'+str((rr,key)),max(scaled)-min(scaled)<.08*max(abs(v) for v in scaled)+1e-5,scaled)
 ck('freefall_correction_cancels_orderH_current_'+str(rr),abs(residuals[-1]['qjr'])<.03*abs(residuals[-1]['geodesic_qjr']))
 rows.append({'r':rr,'alpha':alpha,'y_clocksource':y,'residuals':residuals})
# Conditional Solar roots, same declaredp56 constants, no observationsverified.
GM=1.32712440018e20;AU=1.495978707e11;cl=299792458.;ASI=9.3603e-11;v0=-math.sqrt(2*GM/(cl*cl*AU));solar=[]
for R in [.3,1.,3.]:
 d=eta*abs(v0)/R;yl,yh=roots(d);h,hp=kern(yl);gclock_A=yl+h;solar.append({'A_over_H':R,'V0':v0,'y_low':yl,'gclock_over_A':gclock_A,'clock_acceleration_SI':ASI*gclock_A,'physical_Newton_over_A':GM/(AU*AU*ASI),'Uaa_low':2*hp/(1+hp),'high_clock_root_over_A':yh+kern(yh)[0]});ck('Solar_low_root_belowcritical_'+str(R),gclock_A<.001 and yl<yc)
if args.control=='geodesic':ck('CONTROL_exactgeodesic_currentvanishes',abs(rows[1]['residuals'][0]['geodesic_qjr'])<1e-20)
if args.control=='physical_clock':
 R=1.;sphys=solar[1]['physical_Newton_over_A'];h,hp=kern(sphys);ck('CONTROL_physicalforce_is_clock',math.isclose(h,eta*abs(v0)/R,rel_tol=1e-6))
res={'passed':all(v['passed'] for v in checks),'checks':checks,'rows':rows,'solar_conditional':solar,'control':args.control,'non_claims':['Formal throughorderHonly, exactresidualsnotzero','No conservedinterior/Cselection','No MONDoutermatching','No finitegradient health','No observationalexclusion/32pi']};out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'checks':len(checks),'failed':[v['name'] for v in checks if not v['passed']]}));raise SystemExit(0 if res['passed'] else 1)
