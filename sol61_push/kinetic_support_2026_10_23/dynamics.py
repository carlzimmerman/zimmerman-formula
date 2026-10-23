import numpy as np,json,argparse
from scipy.stats import qmc
from particle_base import Model
from equilibrium import solve
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--n',type=int,default=32);p.add_argument('--power',type=int,default=10);p.add_argument('--dilate',type=float,default=1);p.add_argument('--end',type=float,default=40);p.add_argument('--dt',type=float,default=.006);a=p.parse_args()
m=Model(n=a.n,box=16,np_side=4,mass_ratio=1,spin=0);m.sg[:]=0
s,res=solve(R=36,n=1000,tol=1e-7);r=np.array(res['r']);rho=np.array(res['rho']);cum=np.r_[0,np.cumsum((rho*r*r)[:-1]+(rho*r*r)[1:])*(r[1]-r[0])/2];cum/=cum[-1]
u=qmc.Sobol(6,scramble=True,seed=61423).random_base2(a.power-1)
def direction(v,w):
 z=2*v-1;ang=2*np.pi*w;return np.column_stack([np.sqrt(1-z*z)*np.cos(ang),np.sqrt(1-z*z)*np.sin(ang),z])
rad=np.interp(u[:,0],cum,r);x=rad[:,None]*direction(u[:,1],u[:,2]);fields=s.sol(rad);speed=np.sqrt(2*np.maximum(s.p[0]-fields[0]-fields[2],0))*u[:,3]**(1/3);v=speed[:,None]*direction(u[:,4],u[:,5]);x=np.r_[x,-x];v=np.r_[v,-v]
# Canonical deformation preserves phase-space occupancy; dilate excites collapse.
axes=a.dilate*np.array([np.exp(.05),np.exp(-.05),1.]);x*=axes;v/=axes;m.m=m.mass/len(x)
P,chi,init=m.static(x);Pv=np.zeros_like(P);cv=np.zeros_like(chi);pot,acc,ap,ac,h,d=m.evaluate(x,P,chi);E0=pot+m.kinetic(v,Pv,cv);rows=[];reason='endpoint';last=(x.copy(),v.copy());maxerr=0
for step in range(round(a.end/a.dt)+1):
 t=step*a.dt
 if step%max(1,round(.2/a.dt))==0 or step==round(a.end/a.dt):
  rad=np.linalg.norm(x-x.mean(axis=0),axis=1);shape=np.linalg.eigvalsh(x.T@x/len(x));err=(pot+m.kinetic(v,Pv,cv)-E0)/abs(E0);maxerr=max(maxerr,abs(err));rows.append(dict(t=t,r10=float(np.quantile(rad,.1)),r50=float(np.median(rad)),r90=float(np.quantile(rad,.9)),shape_ratio=float(np.sqrt(shape[-1]/shape[0])),energy_error=float(err),**d))
 if step==round(a.end/a.dt):break
 try:
  vn=v+a.dt*acc/2;xn=x+a.dt*vn;pn=Pv+a.dt*ap/2;cn=cv+a.dt*ac/2;Pn=P+a.dt*pn;chin=chi+a.dt*cn
  if max(abs(xn).ravel())>m.box/2-2*m.dx:raise ValueError('matter_boundary')
  en,an,apn,acn,hn,dn=m.evaluate(xn,Pn,chin);vn+=a.dt*an/2;pn+=a.dt*apn/2;cn+=a.dt*acn/2
  x,v,P,Pv,chi,cv,pot,acc,ap,ac,h,d=xn,vn,Pn,pn,chin,cn,en,an,apn,acn,hn,dn
 except ValueError as exc:reason=str(exc);break
result=dict(parameters=vars(a),initial_equilibrium={k:v for k,v in res.items() if k not in ['r','rho','fields']},field_init=init,reason=reason,rows=rows,max_energy_error=maxerr,final_x=x.tolist(),final_v=v.tolist(),E0=float(E0),particles=len(x),field_cell=m.dx)
json.dump(result,open(a.output,'w'),indent=2);print(reason,rows[-1],flush=True)
