"""First-order mediator + baryon density/temperature transfer in imposed EdS."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from thermal import Thermal
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args()
eta=.005;fb=1/6.364;fc=1-fb;ell=.0004404221297174536;t0=.012074272908402984;H0=67.4*1000/3.085677581491367e22*365.25*86400*1e9;end=np.log(1101);vunit=ell*3.085677581491367e22/(t0*1e9*365.25*86400);kT=1.380649e-23/(1.22*1.67262192369e-27*vunit*vunit);th=Thermal();grid=np.linspace(0,end,8193);ts=solve_ivp(th.rhs,(0,end),[2.725*1101],method='Radau',t_eval=grid,rtol=1e-10,atol=1e-10);temp=CubicSpline(grid,np.log(ts.y[0]));amp=1e-8
rows=[]
def run(k,pressure,mediator,ratio,tol):
 def bg(N):
  zp=1101*np.exp(-N);H=H0*np.sqrt(.315)*zp**1.5*t0;q=k*ell*zp;J=1.5*H*H;T=float(np.exp(temp(N)));R=8.55e-13*2e-4*zp**4/(H/t0/1e9)
  return H,q,J,T,R,2.725*zp
 H,q,J,T,R,Tc=bg(0);p0=q*fc*J*amp/(1+q*q) if mediator else 0;vp0=p0*(-3+2*q*q/(1+q*q));y0=[ratio*amp,ratio*amp,amp,amp,p0,vp0,0.]
 def rhs(N,y):
  db,vb,dc,vc,p,vp,dt=y;H,q,J,T,R,Tc=bg(N);grav=J*(fb*db+fc*dc);E=fc*J*dc-q*p;press=q*q*kT*T*(db+dt) if pressure else 0
  return [vb,-.5*vb+(grav-press)/(H*H),vc,-.5*vc+(grav-q*q*E if mediator else grav)/(H*H),vp if mediator else 0,-1.5*vp+(-p+q*E)/(eta*H*H) if mediator else 0,2*vb/3-R*Tc/T*dt]
 sol=solve_ivp(rhs,(0,end),y0,method='Radau',rtol=tol,atol=tol*amp*1e-4,dense_output=True)
 assert sol.success
 vals=[]
 for zz in [100,30,10,0]:
  N=np.log(1101/(1+zz));y=sol.sol(N);vals.append(dict(z=zz,delta_b_over_initial=float(y[0]/amp),delta_c_over_initial=float(y[2]/amp),total_over_dust_equal_seed=float((fb*y[0]+fc*y[2])/(amp*np.exp(N))),temperature_perturbation_over_initial=float(y[6]/amp)))
 return dict(k_Mpc=k,pressure=pressure,mediator=mediator,baryon_ratio=ratio,tolerance=tol,nfev=sol.nfev,values=vals)
for k in [.1,1.,1/.04037934389859046]:
 for pressure,mediator,ratio in [(False,True,1),(True,True,1),(True,True,0),(True,False,1)]:rows.append(run(k,pressure,mediator,ratio,1e-8))
repeat=run(1.,True,True,1,2e-9);base=next(r for r in rows if r['k_Mpc']==1 and r['pressure'] and r['mediator'] and r['baryon_ratio']==1);error=abs(repeat['values'][-1]['total_over_dust_equal_seed']/base['values'][-1]['total_over_dust_equal_seed']-1)
Path(a.output).write_text(json.dumps(dict(checks=[dict(name='linear_tolerance_repeat',passed=error<1e-5,value=error)],rows=rows,repeat=repeat),indent=2)+'\n')
