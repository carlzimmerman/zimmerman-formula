"""Cancellation-safe, guarded continuation of the previously derived exact ODE.
No regular-source or normalized cosmological boundary claim.
"""
import argparse,json,math,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--assert-exact-cosmic',action='store_true');args=ap.parse_args()
D=np.longdouble
eta=D('.5');A=D(1);H=D(1);m=D('1e-12');r0=D('1e-5');rmax=D('.03')
def rhsraw(x,y):
 r=np.exp(D(x));lnN,lnB,w,k=map(D,y);N=np.exp(lnN);B=np.exp(lnB);V=-w*r*N;P=N*k/r
 g=P/(N*B);ga=abs(g);ss=np.hypot(ga,A/2);wg=ga*ga/(ss+A/2);wgg=ga/ss;ug=2*(g-np.copysign(wg,g));ugg=2*(1-wgg)
 leg=(ga*ss-A*A/4*np.arcsinh(2*ga/A))/2 if ga/A>=D('1e-3') else 2*ga**3/(3*A)-4*ga**5/(5*A**3)+12*ga**7/(7*A**5)
 pressure=2*(leg-ga*ga/2)
 BP=B*k/r*(eta/w-1)
 curv=N*(-np.expm1(-2*lnB)-2*k*np.exp(-2*lnB))
 VP=N/(2*r*V)*(-curv-V*V/N*(1-2*k)-N*r*r*(6*eta*lnN-3+pressure)+2*eta*r*V*k)
 T=2*B*r*V*VP+2*r*BP*V*V+B*V*V
 ENrest=2*np.sinh(lnB)+2*r*BP/B**2+T/N**2+B*r*r*(6*eta*lnN-3+pressure+6*eta)+2*eta*B*r*r*(VP+BP/B*V+2*V/r)/N
 PP=N*B/(r*r*ugg)*(ENrest-2*r*ug+r*r*ugg*g*(P/N+BP/B))
 dy=[k,r*BP/B,w*(r*VP/V-1-k),k+r*r*PP/N-k*k]
 return np.array(dy,dtype=float)
rows=[]
for tol in [1e-7,3e-8]:
 counter=[0];start=time.monotonic()
 def rhs(x,y):
  counter[0]+=1
  if counter[0]>30000 or time.monotonic()-start>20:raise RuntimeError('Declared 30000 evaluations or20s percase cap')
  return rhsraw(x,y)
 y0=np.array([0.,math.log1p(float(np.sqrt(m*A))),.5,float(np.sqrt(m*A))])
 try:
  sol=solve_ivp(rhs,(float(np.log(r0)),float(np.log(rmax))),y0,method='Radau',rtol=tol,atol=np.array([tol*1e-6,tol*1e-6,tol*1e-2,tol*1e-6]),max_step=.08,dense_output=True)
  samples=[{'r':float(np.exp(x)),'y':sol.sol(x).tolist(),'derivative':rhsraw(x,sol.sol(x)).tolist()} for x in np.linspace(sol.t[0],sol.t[-1],81)]
  rows.append({'tol':tol,'success':bool(sol.success),'target_reached':bool(abs(sol.t[-1]-float(np.log(rmax)))<1e-9),'message':sol.message,'nfev':counter[0],'accepted_r_end':float(np.exp(sol.t[-1])),'end_y':sol.y[:,-1].tolist(),'samples':samples,'elapsed':time.monotonic()-start})
 except (RuntimeError,OverflowError,ValueError,ZeroDivisionError) as e:rows.append({'tol':tol,'success':False,'message':str(e),'nfev':counter[0],'elapsed':time.monotonic()-start})
result={'base':'b36e8fcb9','A_over_H':1,'eta':.5,'m':1e-12,'r0':float(r0),'rmax':float(rmax),'arithmetic':{'typename':'numpy.longdouble','eps':float(np.finfo(D).eps),'nmant':int(np.finfo(D).nmant),'state':'binary64 SciPy'},'runs':rows,'non_claims':['No regular interior','No imposed cosmological normalization','No physical G calibration','No exact existence/stability/selector proof']}
assert all(z['success'] and z['target_reached'] for z in rows), 'Finite interval not reached'
assert max(abs(a-b) for a,b in zip(rows[0]['end_y'],rows[1]['end_y']))<1e-8, 'Tolerance comparison failed'
if args.assert_exact_cosmic:
 assert abs(rows[-1]['end_y'][0])<1e-12, 'Finite exterior is not exactly normalized to cosmological lapse'
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps([{k:v for k,v in z.items() if k!='samples'} for z in rows]))
