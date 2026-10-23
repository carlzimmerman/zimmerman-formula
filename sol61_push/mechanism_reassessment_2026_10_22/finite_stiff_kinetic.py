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
  out.update(depth_to_infinity=depth,edge_inward_force=muprime(end),min_exterior_force=float(min(muprime(r) for r in exterior)),max_q=float(max(vals[0]/grid**2)),min_Psi=float(min(vals[1])))
 return out
rows=[model(10,.5,ra,gamma=g) for g in [.0001,.01,.1] for ra in [.5,1,3]]
finite=[r for r in rows if r['status']=='edge']
refinements=[]
for r in finite:
 rr=model(r['A'],r['Psi_c'],r['ra'],2e-11,gamma=r['gamma'])
 refinements.append(dict(A=r['A'],Psi_c=r['Psi_c'],ra=r['ra'],status=rr['status'],edge_change=abs(rr['edge']/r['edge']-1),mass_change=abs(rr['mass']/r['mass']-1)))
checks=dict(integrators=all(r['solver_success'] for r in rows),finite_examples=bool(finite),bound_examples=all(r['depth_to_infinity']>0 and r['edge_inward_force']>0 and r['min_exterior_force']>0 for r in finite),cap_respected=all(r['max_q']<1 for r in finite),refinement=all(r['status']=='edge' and max(r['edge_change'],r['mass_change'])<1e-5 for r in refinements))
x,rr,ra0,A0=sp.symbols('Psi r ra A',positive=True)
y=sp.Function('Psi')(rr)
density=A0*y**sp.Rational(5,2)/(1+rr**2/ra0**2)
pressure=sp.Rational(2,7)*density*y
beta=rr**2/(rr**2+ra0**2)
checks['jeans_identity']=sp.simplify(sp.diff(pressure,rr)+2*beta*pressure/rr-density*sp.diff(y,rr))==0
checks={k:bool(v) for k,v in checks.items()}
out=dict(rows=rows,refinements=refinements,checks=checks,all_pass=all(checks.values()),scope='positive distribution family finite gamma; fixed Plummer baryons; no stability/formation')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
