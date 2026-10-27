import json,sys
from pathlib import Path
import numpy as np
N=64;RMIN=2.;CORE=(np.sqrt(17)-1)/2;TOTAL=5.;DM=(TOTAL-CORE)/N
low=CORE+DM*np.arange(N);high=low+DM
checks=[]
def check(name,c,detail=''):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 if not c:raise AssertionError(name)
def w(x):
 x=np.asarray(x)
 if np.any(x>=1):raise ValueError('full saturation wall')
 z=np.empty_like(x);sm=x<.05
 z[sm]=sum(x[sm]**i/i for i in range(3,25))
 z[~sm]=-x[~sm]**2/2-x[~sm]-np.log1p(-x[~sm]);return z
def force(r):
 order=np.argsort(r);rs=r[order]
 if np.any(rs<=RMIN):raise ValueError('prescribed core touched')
 ui=low/rs**2;uo=high/rs**2
 av=(w(uo)-w(ui))/(uo-ui);a=np.empty(N);a[order]=-1/rs**2+av
 return a
nodes,weights=np.polynomial.legendre.leggauss(96)
def energy(r,v):
 rs=np.sort(r);bounds=np.r_[0.,1/rs[::-1],1/RMIN];mass=np.r_[high[::-1],CORE]
 lo,hi=bounds[:-1],bounds[1:];q=(hi+lo)[:,None]/2+(hi-lo)[:,None]*nodes/2
 field=np.sum((hi-lo)/2*np.sum(weights*w(mass[:,None]*q*q)/q**4,axis=1))
 return float(DM*np.sum(v*v)/2-DM*np.sum(1/r)+field)
lo=np.sqrt(high)*(1+1e-12);hi=np.maximum(high+2,2*lo)
for _ in range(100):
 mid=(lo+hi)/2;ui=low/mid**2;uo=high/mid**2
 ff=-1/mid**2+(w(uo)-w(ui))/(uo-ui)
 lo=np.where(ff>0,mid,lo);hi=np.where(ff>=0,hi,mid)
eq=(lo+hi)/2
check('equilibrium full force',np.max(abs(force(eq))*eq**2)<1e-10,float(np.max(abs(force(eq))*eq**2)))
for i in [0,40,63]:
 hh=eq[i]*1e-5;p=eq.copy();p[i]+=hh;m=eq.copy();m[i]-=hh
 fd=-(energy(p,np.zeros(N))-energy(m,np.zeros(N)))/(2*hh*DM)
 check('full field derivative packet%d'%i,abs(fd-force(eq)[i])<1e-7,float(abs(fd-force(eq)[i])))
from scipy.integrate import solve_ivp

def run_adaptive(tol):
 v=np.zeros(N);v[40:48]=.8
 initial=np.r_[eq,v];e0=energy(eq,v);ground=energy(eq,np.zeros(N));injected=e0-ground
 def rhs(t,y):return np.r_[y[N:],force(y[:N])]
 times=np.linspace(0,200,201)
 sol=solve_ivp(rhs,[0,200],initial,method='DOP853',rtol=tol,atol=tol*1e-2,t_eval=times)
 check('adaptive solver tol%g'%tol,sol.success,str(sol.message))
 energies=[energy(y[:N],y[N:]) for y in sol.y.T]
 maxerr=float(np.max(abs(np.array(energies)-e0)))
 check('adaptive energy tol%g'%tol,maxerr<1e-4*injected,maxerr)
 r=sol.y[:N,-1];v=sol.y[N:,-1];cert=(v>0)&(v*v/2>1/r)
 return dict(tolerance=tol,r=r.tolist(),v=v.tolist(),initial_energy=e0,ground_energy=ground,
  injected_energy=injected,max_energy_error=maxerr,nfev=int(sol.nfev),
  conditionally_certified_escape_ids=np.flatnonzero(cert).tolist(),
  total_kinetic=DM*float(np.sum(v*v))/2,final_energy=energies[-1])
coarse=run_adaptive(1e-8);fine=run_adaptive(1e-10)
diff=float(np.max(abs(np.array(coarse['r'])-np.array(fine['r']))))
sorted_diff=float(np.max(abs(np.sort(coarse['r'])-np.sort(fine['r']))))
out=dict(checks=checks,core=CORE,total_supply=TOTAL,N=N,packet_mass=DM,coarse=coarse,fine=fine,
 label_radius_difference=diff,sorted_radius_difference=sorted_diff,
 scope='Adaptive nonlinear radial finite-shell comparison; escape certificate requires admissible future model continuation. No cold formation or profile selection established.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(label_radius_difference=diff,sorted_radius_difference=sorted_diff,summaries=[{k:t[k] for k in ['tolerance','max_energy_error','nfev','conditionally_certified_escape_ids','total_kinetic']} for t in [coarse,fine]]),indent=2))
check('adaptive label trajectory agreement',diff<.01,diff)
check('adaptive escaped IDs agreement',coarse['conditionally_certified_escape_ids']==fine['conditionally_certified_escape_ids'])
out['checks']=checks;Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
