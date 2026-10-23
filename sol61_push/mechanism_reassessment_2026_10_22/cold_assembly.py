import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import eigh_tridiagonal
p=Path(__file__).parent;x=np.linspace(1e-6,1,600);guess=np.array([2.5*x**3-1.5*x**5,7.5*(1-x*x)/8]);Rguess=2.;previous=1.;rows=[]
for beta in [1.,.7,.5,.3,.2,.1,.05,.02,.01]:
 scale=np.sqrt(previous/beta);Rguess*=scale;guess[1]/=scale**3
 def fun(t,y,a):
  R=a[0];r=R*t;q=y[0]/r**2
  return np.array([R*r*r*y[1],R/.01*(q*q/(1-q)-beta*r/(1+r*r)**1.5)])
 def bc(a,b,z):return np.array([a[0]-a[1]*(z[0]*1e-6)**3/3,b[0]-1,b[1]])
 sol=solve_bvp(fun,bc,x,guess,p=[Rguess],tol=2e-8,max_nodes=30000);R=float(sol.p[0]);r=R*x;m,d=sol.sol(x);q=m/r**2;spectra=[]
 if sol.status==0 and min(d)>-1e-7 and max(q)<1:
  for n in [512,1024]:
   h=R/(n+1);rr=h*np.arange(1,n+1);mm,dd=sol.sol(rr/R);qq=mm/rr**2;weight=1/(rr*rr*dd);faces=.01/(h*(np.arange(n+1)+.5))**2
   diag=(faces[:-1]+faces[1:])/h**2+qq*(2-qq)/(1-qq)**2/rr**2;off=-faces[1:-1]/h**2
   vals=eigh_tridiagonal(diag/weight,off/np.sqrt(weight[:-1]*weight[1:]),select='i',select_range=(0,2),eigvals_only=True,tol=1e-12)
   spectra.append(dict(n=n,omega2=vals.tolist(),omega=np.sqrt(np.maximum(vals,0)).tolist()))
 rows.append(dict(beta=beta,status=int(sol.status),edge=R,central_density=float(d[0]),min_density=float(min(d)),max_q=float(max(q)),max_bvp_residual=float(max(sol.rms_residuals)),spectra=spectra))
 if sol.status!=0:break
 guess=sol.sol(x);Rguess=R;previous=beta
checks=dict(complete=len(rows)==9,backgrounds=all(r['status']==0 and r['min_density']>-1e-7 and r['max_q']<1 for r in rows),positive=all(r['spectra'] and min(r['spectra'][-1]['omega2'])>0 for r in rows),spectral_refinement=all(len(r['spectra'])==2 and max(abs(np.array(r['spectra'][0]['omega'])/r['spectra'][1]['omega']-1))<.02 for r in rows))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='unit cold mass, gamma .01, Plummer scale1 and external baryon amplitude beta .01 to1; static continuation and radial frequencies, not live assembly')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
