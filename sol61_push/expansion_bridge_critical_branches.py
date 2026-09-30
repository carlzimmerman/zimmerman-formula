"""Finite two-sided offset integrations; not a proven smooth crossing."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import root
from scipy.integrate import solve_ivp
ns={};src=Path('sol61_push/expansion_bridge_radial_ivp.py').read_text().split('\nparser=argparse.ArgumentParser();')[0]
exec(compile(src,'reviewed_radial','exec'),ns)
body=src[src.index('def parts('):src.index('\ndef rhs_r(')];body=body[:body.index(' pp=-constant/denom')]+' return np.array([C,denom,constant])\n';body=body.replace('def parts(','def algebra(');exec(compile(body,'algebra','exec'),ns)
fn=ns['algebra'];r=.001;beta=10.
def state(x):return np.array([0,x[0]*r**3,0,x[1]*r**3,x[2]*r**2])
z=root(lambda x:fn(r,state(x))/[r,r,r*r],[.5,-.5,.5],tol=1e-10);y=state(z.x)
sig,dW,dt,p=y[1:];E=np.exp(sig);W=-1+dW;th=3+dt;ct=1+2*beta*p**3/th**3
base=np.array([E*(p+1.5*beta*p*p/th),E*(p-1.5*beta*p*p/th),-(dt+3*dW)/r-2*E*W*p,-4*W*E*p/ct,0])
k=np.array([0,r*E,-r*E*W,(3*beta*p*p/th**2-2*r*W*E)/ct,1])
grad=[]
for i in range(1,5):
 yy=y.astype(complex);yy[i]+=1e-30j;grad.append(np.imag(fn(r,yy))/1e-30)
grad=np.array(grad).T;dr=np.imag(fn(r+1e-30j,y.astype(complex)))/1e-30
# base and k include logN; algebra is independent of logN.
D0=dr[1]+grad[1]@base[1:];D1=grad[1]@k[1:]
R0=dr[2]+grad[2]@base[1:];R1=grad[2]@k[1:]
pp=float(np.min(np.roots([D1,D0+R1,R0])));slope=base+k*pp

parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
branches=[]
for frac in [.001,.0005,.00025]:
 for side,end in [(-1,1e-6),(1,.1)]:
  start=r*(1+side*frac);ys=y+side*r*frac*slope
  dt,W,p=ys[3],-1+ys[2],ys[4];th=3+dt
  rest=5*dt+.5*dt*dt-2*dt*ys[2]-3*ys[2]**2-p*p-2*beta*p**3/th;aa=p+1.5*beta*p*p/th
  dd=start*start*(aa*aa+rest);ys[1]=-np.log1p(-start*aa+dd/(np.sqrt(1+dd)+1))
  sol=solve_ivp(lambda l,y:np.exp(l)*ns['rhs_r'](np.exp(l),y),(np.log(start),np.log(end)),ys,
   method='DOP853',rtol=1e-10,atol=[1e-17,1e-17,1e-16,1e-16,1e-13],max_step=.02,dense_output=True)
  assert sol.success and abs(np.exp(sol.t[-1])/end-1)<1e-12
  radii=np.geomspace(start,end,128);states=sol.sol(np.log(radii));rows=ns['diagnostics'](radii,states)
  assert all(v['P']>0 and v['Theta']>0 and v['static_F_over_N_squared']>0 for v in rows)
  assert all(v['D']*side>0 for v in rows)
  max_lapse=max(abs(v['lapse_normalized_residual']) for v in rows)
  max_shift=max(abs(v['shift_normalized_residual']) for v in rows)
  assert max_lapse<1e-10 and max_shift<1e-10
  endpoint=rows[-1]
  branches.append({'fractional_start_offset':frac,'side':side,'end_r':end,'endpoint_state':sol.y[:,-1].tolist(),
   'endpoint':endpoint,'max_lapse_normalized_residual':max_lapse,'max_shift_normalized_residual':max_shift,
   'min_theta':min(v['Theta'] for v in rows),'min_static_metric_factor':min(v['static_F_over_N_squared'] for v in rows)})
convergence=[]
for side in [-1,1]:
 vals=[v for v in branches if v['side']==side];first=vals[0]['endpoint']['P']-vals[1]['endpoint']['P'];second=vals[1]['endpoint']['P']-vals[2]['endpoint']['P']
 ratio=abs(first/second);assert 3<ratio<5
 convergence.append({'side':side,'endpoint_P_difference_reduction_factor':ratio})
out={'critical_radius':r,'beta':beta,'critical_state':y.tolist(),'critical_Pprime':pp,
 'branches':branches,'convergence':convergence,
 'scope':'Finite offset integrations on both sides of a candidate negative-slope critical point. The point itself is excluded; no exact smooth crossing, source interior, prescribed cosmological boundary, full covariant health or 32pi selection.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'critical_Pprime':pp,'convergence':convergence,'endpoints':[{'side':v['side'],'offset':v['fractional_start_offset'],'P':v['endpoint']['P'],'dTheta':v['endpoint_state'][3]} for v in branches]},indent=2))
