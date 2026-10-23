import numpy as np,json,sys
import sympy as sp
from scipy.integrate import solve_ivp,quad

def model(A,pc,ra,tol=1e-9,gamma=0):
 r0=1e-6
 def fun(r,y):
  m,p=y;q=m/r**2
  rho=A*max(p,0)**2.5/(1+r*r/ra**2)
  susceptibility=2.5*rho/p if p>0 else 0.
  partial_r=-2*r*rho/(ra*ra+r*r)
  return [r*r*rho,(q*q/(1-q)-r/(1+r*r)**1.5-gamma*partial_r)/(1+gamma*susceptibility)]
 def edge(r,y):return y[1]
 edge.terminal=True;edge.direction=-1
 def cap(r,y):return .99-y[0]/r**2
 cap.terminal=True;cap.direction=-1
 sol=solve_ivp(fun,[r0,100],[A*pc**2.5*r0**3/3,pc],rtol=tol,atol=tol*1e-3,events=[edge,cap],dense_output=True,max_step=.1)
 end=sol.t[-1];mass=sol.y[0,-1];q=mass/end**2
 status='edge' if len(sol.t_events[0]) else ('cap' if len(sol.t_events[1]) else 'outer_limit')
 out=dict(gamma=gamma,A=A,Psi_c=pc,ra=ra,status=status,solver_success=bool(sol.success),edge=end,mass=mass,q_edge=q)
 if status=='edge':
  def muprime(r):
   q=mass/r**2
   return r/(1+r*r)**1.5-q*q/(1-q)
  depth=quad(muprime,end,np.inf,epsabs=1e-11)[0]
  grid=np.geomspace(r0,end,500);vals=sol.sol(grid)
  exterior=np.geomspace(end,max(1e4,100*end),500)
  profiles=[]
  for frac in [.1,.5,.9]:
   rr=frac*end;mm,pp=sol.sol(rr);qq=mm/rr**2;gn=rr/(1+rr*rr)**1.5;qlaw=(np.sqrt(gn*gn+4*gn)-gn)/2
   profiles.append(dict(radius=rr,q_over_cold_law=qq/qlaw,total_g_over_cold_law=(gn+qq)/(gn+qlaw)))
  out['profile']=profiles
  common=[]
  for rr in [.1,.3,.5,1.]:
   if rr<end:
    mm,pp=sol.sol(rr);qq=mm/rr**2;gn=rr/(1+rr*rr)**1.5;qlaw=(np.sqrt(gn*gn+4*gn)-gn)/2
    den=A*max(pp,0)**2.5/(1+rr*rr/ra**2)
    dp=fun(rr,[mm,pp])[1];rhoder=(2.5*den/pp*dp if pp>0 else 0)-2*rr*den/(ra*ra+rr*rr)
    common.append(dict(r=rr,q=qq,qn=qlaw,total_g_over_algebraic=(gn+qq)/(gn+qlaw),Psi=pp,rho=den,cold_balance_residual=(qq*qq/(1-qq)-gamma*rhoder-gn)/gn))
  out['common_profile']=common
  out.update(depth_to_infinity=depth,edge_inward_force=muprime(end),min_exterior_force=float(min(muprime(r) for r in exterior)),max_q=float(max(vals[0]/grid**2)),min_Psi=float(min(vals[1])))
 return out
