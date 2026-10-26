import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import brentq
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
source='reviews/cold_local_production_2026_10_25/run/result.json';req=json.load(open(source))['rows']
def U(q,d):
 z=np.sin(q/2)**2/(np.cos(q/2)*(1+np.cos(q/2)))
 return (d-8)*z+36*z*z+40*z**3+10*z**4
def force(q,d):
 x=1/np.cos(q/2);return (40*x**3-48*x+d)*.5*x*np.tan(q/2)
def hess(q,d):
 x=1/np.cos(q/2);xp=.5*x*np.tan(q/2);xpp=.25*x*(2*x*x-1)
 return (120*x*x-48)*xp*xp+(40*x**3-48*x+d)*xpp
def run(row,ks,tol):
 d=row['gas_d'];E=row['required_source_over_D'];m=math.sqrt((d-8)/4)
 A=brentq(lambda q:U(q,d)-E,0,math.pi-1e-5,xtol=1e-14)
 T=4*quad(lambda th:A*math.cos(th)/math.sqrt(2*(E-U(A*math.sin(th),d))),0,math.pi/2,epsabs=1e-10,epsrel=1e-10)[0]*m
 n=len(ks);y=np.zeros(2+4*n);y[0]=A;y[2:2+n]=1;y[2+3*n:]=1
 def fun(t,y):
  z=y[2:].reshape(4,n);w=ks*ks+hess(y[0],d)/(m*m)
  return np.r_[y[1],-force(y[0],d)/(m*m),z[1],-w*z[0],z[3],-w*z[2]]
 sol=solve_ivp(fun,(0,T),y,method='DOP853',rtol=tol,atol=tol*.1,max_step=T/128)
 assert sol.success
 z=sol.y[2:,-1].reshape(4,n);det=z[0]*z[3]-z[1]*z[2];tr=z[0]+z[3]
 err=float(np.max(abs(det-1)));energy=.5*m*m*sol.y[1]**2+U(sol.y[0],d);ed=float(np.max(abs(energy/E-1)));ret=max(abs(sol.y[0,-1]-A),abs(sol.y[1,-1]))
 assert err<1e-5 and ed<1e-7 and ret<1e-5,(err,ed,ret)
 # k=0 neutral mode can have a Jordan block; omit its roundoff growth from search.
 growth=np.arccosh(np.maximum(abs(tr)/2,1))/T;growth[0]=0
 return dict(name=row['name'],footing=row['footing'],model=row['model'],shell=row['shell'],d=d,E=E,amplitude=A,period_m_units=T,k_over_m=ks.tolist(),trace=tr.tolist(),growth_over_m=growth.tolist(),max_growth_over_m=float(max(growth)),peak_k_over_m=float(ks[np.argmax(growth)]),wronskian_error=err,energy_error=ed,return_error=float(ret))
ks=np.r_[0,np.linspace(.025,8,64)];rows=[run(r,ks,2e-10) for r in req]
order=np.argsort([r['required_source_over_D']/r['gas_d'] for r in req]);selected=sorted(set([int(order[0]),int(order[len(order)//2]),int(order[-1]),int(np.argmax([r['max_growth_over_m'] for r in rows]))]))
refined=[dict(index=i,result=run(req[i],np.r_[0,np.linspace(.025,8,257)],2e-12)) for i in selected]
summary=dict(cases=len(rows),sampled_growth_above_1e_5=sum(r['max_growth_over_m']>1e-5 for r in rows),max_growth_over_m=max(r['max_growth_over_m'] for r in rows),max_wronskian_error=max(r['wronskian_error'] for r in rows),selected_indices=selected)
(out/'result.json').write_text(json.dumps(dict(summary=summary,rows=rows,refined=refined),indent=2)+'\n');print(json.dumps(summary,indent=2))
