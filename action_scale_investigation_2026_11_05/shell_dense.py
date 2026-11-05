"""Four finite-shell static diagnostics; arbitrary units, no physical fit."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp, cumulative_trapezoid
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
V=1e-8;q2=2e-9;m=1e-4;K=.5;M2=1.
cases=[]
for b in [.1,.3]:
 for length in [1.,3.]:
  start=time.monotonic();gam=K*length**2/2;aref=np.sqrt(b*(q2/2+V))
  def physical(r,y):
   N=np.exp(m*y[0]);B=np.exp(m*y[1]);X=q2/(2*N*N);rho=X+V
   a=np.sqrt(b*rho);u=np.tanh(y[2]);p=a*u;d=aref*y[3]
   return N,B,X,rho,a,u,p,d
  def ode(r,y):
   N,B,X,rho,a,u,p,d=physical(r,y)
   au=np.abs(u)
   with np.errstate(divide='raise',invalid='raise',over='raise'):
    W=a*a/K*(-au-np.log1p(-au))
    ss=au/(1-au)
    hh=ss+ss/(1+ss)-2*np.log1p(ss)
    NWn=b*X/K*hh
    n=(M2*(B*B-1)+B*B*r*r*(X-V-W)+gam*r*r*d*d/(2*K*K))/(2*M2*r)
    Bprime=B*B/(2*M2*r)*(B*r*r*(rho+W+NWn)+r*r*d/K+gam*r*r*d*d/(2*K*K*B)-M2*(B-1/B))
    dp=d-2*p/r
    zp=(dp+p*X/rho*n)/(a*(1-u*u))
    dprime=K*B*B/gam*p/(1-au)-K*B/gam*n-(n-Bprime/B)*d
    return np.array([n/m,Bprime/(B*m),zp,dprime/aref])
  def bc(yi,yo):
   return np.array([yi[1]+np.log1p(-2*m)/(2*m),yo[0],yi[3],yo[3]])
  solutions=[];runs=[];error=None
  try:
   for nodes,tol in [(400,1e-9),(800,1e-10)]:
    r=np.geomspace(1,20,nodes);gn=m/r**2
    g=(gn+np.sqrt(gn*gn+4*aref*gn))/2
    logN=cumulative_trapezoid(g,r,initial=0);logN-=logN[-1]
    pp=aref*g/(aref+g);zz=np.arctanh(pp/aref)
    dd=np.gradient(pp,r,edge_order=2)+2*pp/r
    seed=np.array([logN/m,r*g/m,zz,dd/aref])
    sol=solve_bvp(ode,bc,r,seed,tol=tol,max_nodes=10000,bc_tol=1e-10)
    solutions.append(sol)
    runs.append({'initial_nodes':nodes,'tolerance':tol,'status':int(sol.status),
      'message':sol.message,'nodes':len(sol.x),'max_rms_residual':float(max(sol.rms_residuals)),
      'boundary_residual':float(max(abs(bc(sol.y[:,0],sol.y[:,-1]))))})
   grid=np.geomspace(1,20,2001)
   def scaled(sol,grid):
    yy=sol.sol(grid);N,B,X,rho,a,u,p,d=physical(grid,yy)
    return np.array([yy[0],yy[1],p/aref,d/aref])
   coarse,fine=(scaled(sol,grid) for sol in solutions)
   delta=float(np.max(np.abs(coarse-fine)/np.maximum(1,np.abs(fine))))
   samp=np.unique(np.concatenate([grid,solutions[0].x,solutions[1].x]))
   all_domain=True;bounds=[]
   for sol in solutions:
    N,B,X,rho,a,u,p,d=physical(samp,sol.sol(samp))
    good=bool(np.all(np.isfinite(N)) and np.all(np.isfinite(B)) and np.all(N>0) and np.all(B>0) and np.all(u>0) and np.all(u<1))
    all_domain &= good
    bounds.append({'min_p_over_a':float(min(u)),'max_p_over_a':float(max(u)),
                   'min_N':float(min(N)),'max_N':float(max(N)),
                   'min_B':float(min(B)),'max_B':float(max(B))})
   passed=bool(all_domain and delta<=1e-5 and all(z['status']==0 and z['max_rms_residual']<=z['tolerance'] and z['boundary_residual']<=1e-8 for z in runs))
   result={'b':b,'Lstar':length,'passed':passed,'runs':runs,'mesh_difference':delta,
           'sampled_bounds':bounds,'profile':{'r':grid.tolist(),'scaled_fields':fine.tolist()}}
  except Exception as ex:
   result={'b':b,'Lstar':length,'passed':False,'runs':runs,'error':type(ex).__name__+': '+str(ex)}
  result['elapsed_seconds']=time.monotonic()-start;cases.append(result)
  print(json.dumps({key:val for key,val in result.items() if key!='profile'}),flush=True)
out={'passed':len(cases)==4 and all(x['passed'] for x in cases),'cases':cases,
     'scope':'Finite-shell sampled numerical convergence only; no physical fit, stability proof or coefficient prediction.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['passed'] else 1)
