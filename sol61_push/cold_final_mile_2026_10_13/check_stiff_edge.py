import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,nnls
checks=[]
def check(name,c,detail):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 if not c:raise AssertionError(name)
def m0(r):return 2*r*r/(np.sqrt(1+4*r*r)+1)
core=float(m0(2.));supply=2.
def solve(n,beta):
 r=np.geomspace(2.,20.,n);dr=np.diff(r);rm=(r[:-1]+r[1:])/2
 wt=np.r_[dr[0]/2,(dr[:-1]+dr[1:])/2,dr[-1]/2];r2=r*r
 def full(x):return np.r_[core,x,supply]
 def energygrad(x):
  m=full(x);u=m/r2;du=np.diff(u);d=-u*u/2-u-np.log1p(-u)
  en=np.sum(wt*(r2*d-m/r2))+beta/2*np.sum(rm*rm*du*du/dr)+beta*np.sum(wt*u*u)
  gr=wt*(u*u/(1-u)-1/r2)
  flux=beta*rm*rm*du/dr
  gu=2*beta*wt*u;gu[:-1]-=flux;gu[1:]+=flux
  gr+=gu/r2
  return float(en),gr[1:-1]
 x0=np.minimum(supply,m0(r))[1:-1]
 # Cx-d >=0 describes the full monotonic chain including fixed endpoints.
 C=np.zeros((n-1,n-2));d=np.zeros(n-1);C[0,0]=1.;d[0]=core
 for i in range(1,n-2):C[i,i]=1.;C[i,i-1]=-1.
 C[-1,-1]=-1.;d[-1]=-supply
 con=dict(type='ineq',fun=lambda x:C@x-d,jac=lambda x:C)
 sol=minimize(lambda x:energygrad(x)[0],x0,jac=lambda x:energygrad(x)[1],
              constraints=[con],method='SLSQP',options=dict(ftol=1e-13,maxiter=1000))
 m=full(sol.x);en,gr=energygrad(sol.x);slack=C@sol.x-d
 check('solver n%d beta%g'%(n,beta),sol.success,str(sol.message))
 check('monotonic positivity n%d beta%g'%(n,beta),np.min(slack)>-1e-8,float(np.min(slack)))
 active=slack<1e-7
 if np.any(active):_,res=nnls(C[active].T,gr,maxiter=10000)
 else:res=np.linalg.norm(gr)
 rel=res/max(1.,np.linalg.norm(gr))
 check('KKT n%d beta%g'%(n,beta),rel<1e-6,float(rel))
 for i in [0,(n-2)//2,n-3]:
  h=1e-5;x=sol.x.copy();x[i]+=h;y=sol.x.copy();y[i]-=h
  fd=(energygrad(x)[0]-energygrad(y)[0])/(2*h)
  check('energy gradient n%d beta%g i%d'%(n,beta,i),abs(fd-gr[i])<1e-6,float(abs(fd-gr[i])))
 if beta==0:check('zero stiffness cap n%d'%n,np.max(abs(m-np.minimum(supply,m0(r))))<1e-5,float(np.max(abs(m-np.minimum(supply,m0(r))))))
 ix=np.flatnonzero(m>supply-1e-6)
 return dict(n=n,beta=beta,r=r.tolist(),m=m.tolist(),energy=en,kkt_residual=float(rel),
             first_supply_plateau_radius=float(r[ix[0]]),iterations=int(sol.nit))
rows=[]
for b in [0.,.01,.1,1.]:
 coarse=solve(81,b);fine=solve(161,b)
 cmp=np.max(abs(np.interp(fine['r'],coarse['r'],coarse['m'])-np.array(fine['m'])))
 check('mesh mass comparison beta%g'%b,cmp<=.005,float(cmp));rows +=[coarse,fine]
out=dict(checks=checks,profiles=rows,scope='Convex finite radial optimization; conditional carrier energy and prescribed inner support. Not continuum convergence, formation or relativistic completion.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),summary=[{k:x[k] for k in ['n','beta','first_supply_plateau_radius','kkt_residual','iterations']} for x in rows]),indent=2))
