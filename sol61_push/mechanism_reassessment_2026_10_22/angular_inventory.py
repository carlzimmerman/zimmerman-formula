import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre
p=Path(__file__).parent;rows=[]
for ref in json.load(open(p/'cold_limit_run/results.json'))['rows']:
 A=ref['A'];pc=ref['Psi_c'];r0=1e-6
 def rhs(r,y):
  m,psi=y;q=m/r**2;rho=A*max(psi,0)**2.5/(1+r*r);chi=2.5*rho/psi if psi>0 else 0
  return [r*r*rho,(q*q/(1-q)-r/(1+r*r)**1.5+.02*r*rho/(1+r*r))/(1+.01*chi)]
 def edge(r,y):return y[1]
 edge.terminal=True;edge.direction=-1
 sol=solve_ivp(rhs,[r0,100],[A*pc**2.5*r0**3/3,pc],rtol=2e-13,atol=2e-16,events=edge,dense_output=True,max_step=.05);R=sol.t[-1];values=[]
 for order in [256,512]:
  gx,gw=roots_legendre(order);r=r0+(gx+1)*(R-r0)/2;w=gw*(R-r0)/2;psi=sol.sol(r)[1];rho=A*np.maximum(psi,0)**2.5/(1+r*r);dm=w*r*r*rho;mass=dm.sum()
  l2=4*r*r*psi/(7*(1+r*r));l4=32*r**4*psi**2/(63*(1+r*r)**2)
  values.append(dict(order=order,mass=float(mass),mean_L2=float(dm@l2/mass),mean_L4=float(dm@l4/mass)))
 rows.append(dict(A=A,edge=R,values=values))
# Independent velocity-space quadrature at Psi=1,r=1 (anisotropy factor2).
x,w=roots_legendre(64);s=(x+1)/2;ws=w/2;mu=x;wm=w
speed2=2*s[:,None]**2;L2=speed2*(1-mu[None,:]**2)/2
weight=ws[:,None]*wm[None,:]*s[:,None]**2*(1-s[:,None]**2);norm=weight.sum();num2=(weight*L2).sum()/norm;num4=(weight*L2**2).sum()/norm
checks=dict(mass=all(abs(r['values'][-1]['mass']-1)<1e-5 for r in rows),radial_refinement=all(max(abs(r['values'][0][key]/r['values'][1][key]-1) for key in ['mean_L2','mean_L4'])<1e-6 for r in rows),velocity_moments=bool(abs(num2-2/7)<1e-12 and abs(num4-8/63)<1e-12))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,velocity_check=dict(L2=float(num2),L4=float(num4)),warm_cold_L2_ratio=rows[0]['values'][-1]['mean_L2']/rows[-1]['values'][-1]['mean_L2'],scope='equilibrium angular momentum moments; exact conservation applies only closed spherical central-force evolution')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
