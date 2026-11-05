"""Finite radial variational diagnostic, fixed background interpolants."""
import argparse,json,time,warnings
from pathlib import Path
import numpy as np
import sympy as s
from scipy.interpolate import CubicSpline
from scipy.linalg import eigh,solve,eigvalsh
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
r,B,N,p,Bp,pp,m2,K,b,q2,V,gam=s.symbols('r B N p Bp pp M2 K b q2 V gamma',positive=True)
X=q2/(2*N*N);aa=s.sqrt(b*(X+V));W=aa*aa/K*(-p/aa-s.log(1-p/aa));d=pp+2*p/r
L=m2*N*(B-1/B+2*r*Bp/B**2)+N*B*r*r*(X-V-W)-N*(r*r*pp+2*r*p)/K-gam*N*r*r*d*d/(2*K*K*B)
variables=[B,N,p,Bp,pp];params=(r,B,N,p,Bp,pp,m2,K,b,q2,V,gam)
hf=s.lambdify(params,s.hessian(L,variables),'numpy',cse=True)
gf=s.lambdify(params,s.Matrix([s.diff(L,x) for x in variables]),'numpy',cse=True)
base=Path(__file__).resolve().parent;data=json.loads((base/'evidence/shell/result.json').read_text());results=[]
controls=[]
for cells in [40,80,160]:
 n=cells-1;hh=1/cells
 stiff=(np.diag(np.full(n,2))+np.diag(np.full(n-1,-1),1)+np.diag(np.full(n-1,-1),-1))/hh
 mass=(np.diag(np.full(n,4))+np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1))*hh/6
 first=float(eigh(stiff,mass,subset_by_index=[0,0],eigvals_only=True)[0])
 mutant=float(eigh(-stiff,mass,subset_by_index=[0,0],eigvals_only=True)[0])
 controls.append({'cells':cells,'first':first,'relative_error':abs(first/np.pi**2-1),'reversed_min':mutant})

for case in data['cases']:
 start=time.monotonic();bb=case['b'];length=case['Lstar'];gamma=.5*length*length/2;aref=np.sqrt(bb*1.1e-8)
 interpolant=CubicSpline(np.array(case['profile']['r']),np.array(case['profile']['scaled_fields']),axis=1)
 rows=[]
 for cells in [40,80,160]:
  grid=np.geomspace(1,20,cells+1);mid=(grid[:-1]+grid[1:])/2;width=np.diff(grid);nb=cells-1;nt=2*nb+cells
  H=np.zeros((nt,nt));Mass=np.zeros((nb,nb));grad=np.zeros(nt)
  field=interpolant(mid);NN=np.exp(1e-4*field[0]);BB=np.exp(1e-4*field[1]);PP=aref*field[2];DD=aref*field[3]
  for j,(rr,hh,nn,bmet,pol,div) in enumerate(zip(mid,width,NN,BB,PP,DD)):
   xx=1e-9/(nn*nn);rho=xx+1e-8;a0=np.sqrt(bb*rho);u=pol/a0;ss=u/(1-u)
   wp=a0*a0/.5*(-u-np.log1p(-u));hhfun=ss+ss/(1+ss)-2*np.log1p(ss);nwn=bb*xx/.5*hhfun
   nprime=((bmet*bmet-1)+bmet*bmet*rr*rr*(xx-1e-8-wp)+gamma*rr*rr*div*div/.5)/(2*rr)
   bp=bmet*bmet/(2*rr)*(bmet*rr*rr*(rho+wp+nwn)+rr*rr*div/.5+gamma*rr*rr*div*div/(.5*bmet)-(bmet-1/bmet))
   ppjet=div-2*pol/rr
   vals=(rr,bmet,nn,pol,bp,ppjet,1.,.5,bb,2e-9,1e-8,gamma)
   local=np.asarray(hf(*vals),float);lg=np.asarray(gf(*vals),float).reshape(5)
   # Local columns correspond to existing B endpoints, lapse cell, p endpoints.
   ids=[];cols=[];bids=[]
   for node,weight,deriv in [(j,.5,-1/hh),(j+1,.5,1/hh)]:
    if 0<node<cells:
     ids.append(node-1);cols.append([weight,0,0,deriv,0]);bids.append((node-1,node-j))
   ids.append(nb+j);cols.append([0,1,0,0,0])
   for node,weight,deriv in [(j,.5,-1/hh),(j+1,.5,1/hh)]:
    if 0<node<cells:
     ids.append(nb+cells+node-1);cols.append([0,0,weight,0,deriv])
   transform=np.array(cols,float).T;H[np.ix_(ids,ids)]+=hh*transform.T@local@transform;grad[ids]+=hh*transform.T@lg
   bg=bmet*rr/2*(bmet*bmet*(2*xx+nwn)+bmet*div/.5+gamma*div*div/.25)
   mt=2*rr/(nn*bg);localmass=hh*mt/6*np.array([[2.,1.],[1.,2.]])
   for ii,li in bids:
    for jj,lj in bids:Mass[ii,jj]+=localmass[li,lj]
  symmetry=float(np.max(abs(H-H.T))/max(1,np.max(abs(H))))
  H=(H+H.T)/2;Hcc=H[nb:,nb:];Hcb=H[nb:,:nb]
  scale=1/np.sqrt(np.maximum(np.max(abs(Hcc),axis=1),1e-300))
  equil=Hcc*scale[:,None]*scale[None,:];rhs=Hcb*scale[:,None]
  with warnings.catch_warnings(record=True) as ws:
   warnings.simplefilter('always');xs=solve(equil,rhs,assume_a='sym');sol=xs*scale[:,None]
  backward=float(np.linalg.norm(Hcc@sol-Hcb,np.inf)/(np.linalg.norm(Hcc,np.inf)*np.linalg.norm(sol,np.inf)+np.linalg.norm(Hcb,np.inf)))
  evc=eigvalsh(equil);condition=float(max(abs(evc))/min(abs(evc)))
  reduced=H[:nb,:nb]-H[:nb,nb:]@sol;reduced=(reduced+reduced.T)/2
  values,vectors=eigh(-reduced,Mass,subset_by_index=[0,4])
  residual=0.
  for lam,vec in zip(values,vectors.T):
   residual=max(residual,float(np.linalg.norm(-reduced@vec-lam*Mass@vec)/(np.linalg.norm(reduced,2)*np.linalg.norm(vec)+abs(lam)*np.linalg.norm(Mass,2)*np.linalg.norm(vec))))
  row={'cells':cells,'omega2_low5':values.tolist(),'constraint_backward_error':backward,'eigen_backward_error':residual,
       'constraint_condition_scaled':condition,'symmetry_error':symmetry,'background_gradient_inf':float(max(abs(grad))),
       'warnings':[str(w.message) for w in ws]}
  rows.append(row);print(json.dumps({'b':bb,'Lstar':length,**row}),flush=True)
 low80=np.array(rows[1]['omega2_low5'][:3]);low160=np.array(rows[2]['omega2_low5'][:3]);ladder=float(max(abs(low80/low160-1)))
 passed=bool(ladder<=.02 and all(min(z['omega2_low5'])>0 and z['constraint_backward_error']<=1e-8 and z['eigen_backward_error']<=1e-8 and z['constraint_condition_scaled']<1e14 for z in rows))
 results.append({'b':bb,'Lstar':length,'passed':passed,'last_ladder_relative':ladder,'rows':rows,'elapsed_seconds':time.monotonic()-start})
controlpass=controls[-1]['relative_error']<=1e-3 and all(z['reversed_min']<0 for z in controls)
out={'passed':controlpass and all(z['passed'] for z in results),'controls':controls,'cases':results,'scope':'Finite radial box low-mode diagnostic on fixed background interpolants, not continuum/full theory stability.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n');raise SystemExit(0 if out['passed'] else 1)
