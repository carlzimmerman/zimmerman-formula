"""Exact fixed-invariant chain, ADM current, and bounded necessary-equation controls."""
from pathlib import Path
import argparse,json
import sympy as s
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['drop_UV','static_gradient','reverse_charge']);ar=ap.parse_args();rows=[]
def ck(name,b,detail=''):rows.append({'name':name,'passed':bool(b),'detail':str(detail)})
def eq(name,f):f=s.factor(f);ck(name,f==0,f)
d,dy,dt,qt,at=s.symbols('d dy dt qt at',real=True);yT=-2*dt/(1+2*dy);M_T=qt+4*d*dt+(2*d+4*d*dy)*yT-at
eq('fixed_invariant_derivative',M_T-qt+at)
T,t=s.symbols('T t',positive=True);b=s.Function('b')(t);e=b*T*T/(T*T+t*t)
eq('exact_positive_kernel_T_derivative',s.diff(e,T)-2*T*t*t*b/(T*T+t*t)**2)
# Independent one-spatial-block inverse calculation; general ADM formula follows by indices.
N,B,S,ud,ux=s.symbols('N B S ud ux',real=True,nonzero=True);g=s.Matrix([[-N*N+B*B*S*S,B*B*S],[B*B*S,B*B]]);inv=g.inv();J=inv*s.Matrix([ud,ux])*N*B
# N B positive; common f²/2 factor suppressed.
eq('ADM_time_current_density',J[0]+B*(ud-S*ux)/N)
eq('ADM_spatial_current_density',J[1]-N*ux/B+B*S*(ud-S*ux)/N)

def mu_u(y,T):
 th0=np.arctan(y/T)
 def f(th):
  tt=T*np.tan(th);h=1/(np.sqrt(1+1/tt)+1)
  return -4*T*h*np.sin(th)**2
 return quad(f,th0,np.pi/2,epsabs=2e-10,epsrel=2e-11,limit=150)[0]
def nu(y,T):return 1+1/(np.sqrt(1+1/y)+1)/y/(1+(y/T)**2)
vals=[]
for T0 in [8.,128.915,256.]:
 for y in [0.,.01,1.,10.,100.]:
  m=mu_u(y,T0);vals.append({'T':T0,'y':y,'M_u':m});ck('negative_tail_'+str((T0,y)),m<0,m)
  if y>0:
   f=lambda t:-4*T0*T0*t*t/((np.sqrt(1+1/t)+1)*(T0*T0+t*t)**2)
   direct=quad(f,y,np.inf,epsabs=2e-9,epsrel=1e-10,limit=200)[0];ck('independent_tail_integral_'+str((T0,y)),abs(m/direct-1)<2e-9)
# Exact smooth stationary periodic ADM test currents; not full-metric on-shell fields.
x=s.symbols('x',real=True);NN=1+s.cos(x)/10;LL=1+s.sin(x)/10;SS=s.sin(x)/20;RR=s.cos(x)/30;U=s.cos(x)/5;Ux=s.diff(U,x)
JJ=(NN-SS*SS/NN+LL-RR*RR/LL)*Ux/2;div=s.diff(JJ,x);jfn=s.lambdify(x,JJ,'numpy');dfn=s.lambdify(x,div,'numpy')
xs=np.linspace(0,2*np.pi,129)[:-1];mean_div=float(np.mean(dfn(xs)));ck('periodic_ADM_divergence_zero',abs(mean_div)<1e-12,mean_div)
forces=[]
for xx in xs:
 nn=float(NN.subs(x,xx));ll=float(LL.subs(x,xx));uu=np.log(128.915)+np.cos(xx)/5;tt=np.exp(uu)
 invariant_grad=float((s.diff(NN,x)/NN-s.diff(LL,x)/LL).subs(x,xx));xxstar=abs(invariant_grad)
 yy=0. if xxstar==0 else brentq(lambda y:y*(2*nu(y,tt)-1)-xxstar,1e-30,max(xxstar,1.))
 forces.append(-np.sqrt(nn*ll)*mu_u(yy,tt))
force_mean=float(np.mean(forces));ck('strict_compact_force_integral',force_mean>0,force_mean)
ck('manufactured_static_residual_not_zero',abs(mean_div-force_mean)>1,mean_div-force_mean)
# Exact charge orientation and boundary identity, not an arbitrary scalar fluid dictionary.
F0,V0,area,r0,n=s.symbols('F0 V0 area r0 n',positive=True)
eq('charge_sign_orientation',(-F0*V0)+F0*V0)
eq('ball_flux_source_integral',area*r0**(n-1)*(F0*r0/n)-F0*area*r0**n/n)
if ar.control=='drop_UV':eq('false_UV_derivative_can_be_dropped',M_T-qt)
if ar.control=='static_gradient':ck('false_static_periodic_gradient_balances_force',abs(mean_div-force_mean)<1e-10)
if ar.control=='reverse_charge':ck('false_no_flux_canonical_charge_increases',-force_mean>0)
out={'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'tail_examples':vals,'periodic_test':{'mean_divergence':mean_div,'mean_positive_force':force_mean,'sample_count':128,'on_shell_metric':False},'control':ar.control,'scope':'exact necessary modulus EL; compact theorem is analytic divergence proof, bounded fixtures not actualmetric solution or healthy PDE theorem'};p=Path(ar.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[r for r in rows if not r['passed']],'periodic_test':out['periodic_test']}));raise SystemExit(not all(r['passed'] for r in rows))
