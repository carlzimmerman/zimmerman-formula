import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parent
# Independent single-mode implementation: state (q,p,a,a',b,b').
def deriv(q,d):
 x=1/math.cos(q/2);return .5*x*math.tan(q/2)*(40*x**3-48*x+d)
def U(q,d):
 x=1/math.cos(q/2);return 10*x**4-24*x*x+14+d*(x-1)
def second(q,d):
 h=1e-4
 return (-U(q+2*h,d)+16*U(q+h,d)-30*U(q,d)+16*U(q-h,d)-U(q-2*h,d))/(12*h*h)
# Constant-frequency monodromy benchmark; reversed restoring sign must fail.
w=1.7;T=2.3
s=solve_ivp(lambda t,y:[y[1],(1 if a.mutate else -1)*w*w*y[0],y[3],(1 if a.mutate else -1)*w*w*y[2]],(0,T),[1,0,0,1],method='DOP853',rtol=1e-12,atol=1e-13)
actual=s.y[:,-1].reshape(2,2).T;expected=np.array([[math.cos(w*T),math.sin(w*T)/w],[-w*math.sin(w*T),math.cos(w*T)]])
error=float(np.max(abs(actual-expected)));assert error<1e-9,'harmonic restoring-sign benchmark'
f=json.load(open(root/'floquet/result.json'));checks=[]
for item in f['refined']:
 r=item['result'];k=r['peak_k_over_m'] or 1;d=r['d'];m2=(d-8)/4;T=r['period_m_units']
 def rhs(t,y):
  # Independent numerical Hessian instead of the production analytic Hessian.
  omega=k*k+second(y[0],d)/m2
  return [y[1],-deriv(y[0],d)/m2,y[3],-omega*y[2],y[5],-omega*y[4]]
 s=solve_ivp(rhs,(0,T),[r['amplitude'],0,1,0,0,1],method='DOP853',rtol=2e-9,atol=2e-10,max_step=T/256)
 assert s.success
 tr=s.y[2,-1]+s.y[5,-1];growth=float(np.arccosh(max(abs(tr)/2,1))/T)
 target=r['max_growth_over_m'];assert abs(growth-target)<2e-5,(growth,target)
 checks.append(dict(index=item['index'],growth_independent=growth,growth_production=target,absolute_difference=abs(growth-target)))
result=dict(harmonic_matrix_error=error,independent_checks=checks)
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
