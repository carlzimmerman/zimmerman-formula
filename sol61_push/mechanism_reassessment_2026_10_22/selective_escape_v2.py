import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import roots_legendre,betainc
p=Path(__file__).parent
refs=json.load(open(p/'cold_limit_run/results.json'))['rows'];target=json.load(open(p/'angular_inventory_run/results.json'))['rows'][-1]['values'][-1]['mean_L2'];rows=[]
for ref in refs[:-1]:
 A=ref['A'];pc=ref['Psi_c'];r0=1e-6
 def rhs(r,y):
  m,psi=y;q=m/r**2;rho=A*max(psi,0)**2.5/(1+r*r);chi=2.5*rho/psi if psi>0 else 0
  return [r*r*rho,(q*q/(1-q)-r/(1+r*r)**1.5+.02*r*rho/(1+r*r))/(1+.01*chi)]
 def edge(r,y):return y[1]
 edge.terminal=True;edge.direction=-1
 sol=solve_ivp(rhs,[r0,100],[A*pc**2.5*r0**3/3,pc],rtol=2e-13,atol=2e-16,events=edge,dense_output=True,max_step=.05);R=sol.t[-1]
 for order in [256,512,1024]:
  gx,gw=roots_legendre(order);r=r0+(gx+1)*(R-r0)/2;w=gw*(R-r0)/2;psi=sol.sol(r)[1];rho=A*np.maximum(psi,0)**2.5/(1+r*r);dm=w*r*r*rho;dm/=dm.sum();b=2*r*r*psi/(1+r*r)
  def retained(cut):
   z=np.minimum(cut/b,1);fraction=float(dm@betainc(1,2.5,z));moment=float(dm@(b*(2/7)*betainc(2,2.5,z)));return fraction,moment
  cut=brentq(lambda c:retained(c)[1]/retained(c)[0]-target,1e-8,float(max(b)),xtol=1e-13)
  fraction,moment=retained(cut);full=float(dm@(2*b/7));rows.append(dict(A=A,order=order,L2_cut=cut,retained_fraction=fraction,removed_fraction=1-fraction,retained_mean=moment/fraction,full_mean=full,exported_L2_fraction=1-moment/full))
# Independent velocity marginal integral on t in [0,z].
x,w=roots_legendre(128);errors=[]
for z in [.01,.2,.7,1.]:
 t=z*(x+1)/2;weight=z*w/2*2.5*(1-t)**1.5
 errors.append(max(abs(weight.sum()-betainc(1,2.5,z)),abs(weight@t-(2/7)*betainc(2,2.5,z))))
changes={str(a):abs([r['retained_fraction'] for r in rows if r['A']==a][-1]/[r['retained_fraction'] for r in rows if r['A']==a][-2]-1) for a in [10,100,1000]}
checks=dict(velocity_marginal=bool(max(errors)<1e-9),mean_match=all(abs(r['retained_mean']/target-1)<1e-8 for r in rows),refinement=all(x<1e-5 for x in changes.values()),fractions=all(0<r['retained_fraction']<1 for r in rows))
out=dict(checks=checks,all_pass=all(checks.values()),target_mean_L2=target,rows=rows,relative_512_to_1024_changes=changes,velocity_marginal_error=float(max(errors)),scope='optimal retained-mass upper bound for matching one moment by removal only; not a physical escape process or full target distribution')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
