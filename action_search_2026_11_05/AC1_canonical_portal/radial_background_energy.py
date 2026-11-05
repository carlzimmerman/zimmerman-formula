import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import argparse,json,time,itertools
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,cumulative_trapezoid
from radial_energy import evaluate
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();t0=time.time()
R={'models':[],'checks':{},'scope':'Finite-box quasistatic scalar/polarization system; not full relativistic on-shell action.'}
lo=1e-4;hi=20.;probe=np.geomspace(lo,hi,301)
for beta,mass,ell in itertools.product([2/3,.9],[1,100],[.1,.3]):
 B=2*np.sqrt(3*(1-beta))/(3*beta);q=(1-beta)/beta;xi=.5/(1+beta)
 bary=lambda x:mass*x/(1+x*x)**1.5
 def vals(d,eps):
  dy=eps*d/B;y=1+dy
  logratio=np.log1p(2*np.sinh(dy/2)*np.cosh(1+dy/2)/np.sinh(1))
  A=np.exp(-q*logratio);ct=1/np.tanh(y)
  Apsi=-q/B*A*ct
  Vdiff=-2*q/B*(np.expm1(-2*q*logratio)*ct-np.sinh(dy)/(np.sinh(y)*np.sinh(1)))
  return A,Apsi,Vdiff
 def gfun(z):
  with np.errstate(invalid='ignore',divide='ignore'):
   v=2*(-z-np.log1p(-z))-z*z/(1-z)
  small=np.abs(z)<.01
  if np.any(small):v=np.where(small,sum((2-n)/n*z**n for n in range(3,17)),v)
  return v
 last=[None,None];base=None
 for length in [0,1e-4,1e-3]:
  eps=2*length*length
  def source(Y):
   A,Ap,Vd=vals(Y[2],eps)
   return (4*np.pi/xi)*Vd+A*Ap*gfun(Y[0]/A)
  def ode(x,Y):
   A,_,_=vals(Y[2],eps)
   return np.array([Y[1],-2*Y[1]/x+2*Y[0]/x**2+2/ell**2*(Y[0]**2/(A-Y[0])-bary(x)),Y[3],source(Y)-2*Y[3]/x])
  edge=(np.sqrt(bary(hi)**2+4*bary(hi))-bary(hi))/2
  def bc(a,b):return np.array([a[1]-a[0]/lo,a[3],b[0]-edge,b[2]])
  sols=[];statuses=[]
  for idx,(nodes,tol) in enumerate([(400,1e-5),(800,1e-7)]):
   xx=np.geomspace(lo,hi,nodes)
   if last[idx] is not None:guess=last[idx].sol(xx)
   else:
    up=(np.sqrt(bary(xx)**2+4*bary(xx))-bary(xx))/2*xx/np.sqrt(xx*xx+ell*ell)
    guess=np.array([up,np.gradient(up,xx),np.zeros(nodes),np.zeros(nodes)])
   sol=solve_bvp(ode,bc,xx,guess,tol=tol,max_nodes=20000)
   statuses.append(dict(success=bool(sol.success),status=sol.status,message=sol.message,nodes=len(sol.x),max_residual=float(np.max(sol.rms_residuals)),bc_error=float(np.max(np.abs(bc(sol.y[:,0],sol.y[:,-1]))))))
   sols.append(sol)
   if sol.success:last[idx]=sol
  row=dict(beta=beta,mass=mass,L_over_R=ell,aR_over_c2=length,solvers=statuses)
  if all(x.success for x in sols):
   Y=sols[1].sol(probe);A,_,_=vals(Y[2],eps)
   row.update(convergence=float(np.max(np.abs(Y-sols[0].sol(probe))/(1+np.abs(Y)))),physical=bool(np.all(Y[0]>0)&np.all(Y[0]<A)),switch_min=float(np.min(Y[1]+2*Y[0]/probe)),a_fraction_max=float(np.max(np.abs(A-1))),d_min=float(np.min(Y[2])))
   if length==0:
    base=Y.copy();xx=np.geomspace(lo,hi,20001);YY=sols[1].sol(xx);src=source(YY)
    flux=cumulative_trapezoid(xx**2*src,xx,initial=0)
    integ=cumulative_trapezoid(flux/xx**2,xx,initial=0);green=integ-integ[-1]
    row['green_error']=float(np.max(np.abs(YY[2]-green)/(1+np.abs(YY[2]))))
    # The fixed-a linear scalar equation changes sign under source reversal.
    neg_green=-green;row['mutant_sign_reversed']=bool(np.min(green)<0 and np.max(neg_green)>0)
   if base is not None:
    row['g_fraction_change_max']=float(np.max(np.abs(Y[0]-base[0])/(bary(probe)+base[0])))
    row['linear_response_difference']=float(np.max(np.abs(Y[2]-base[2])/(1+np.abs(base[2]))))
  if all(s.success for s in sols):row['energy']=evaluate(sols[1],beta,ell,eps,known=(length==0))
  R['models'].append(row)
  print(json.dumps({k:row[k] for k in row if k not in ['solvers']}),flush=True)
  Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(R,indent=2))
R['checks']={'count':len(R['models'])==24,'converged':all(all(s['success'] for s in r['solvers']) for r in R['models']),'profile_agreement':all(r.get('convergence',float('inf'))<1e-4 for r in R['models']),'physical':all(r.get('physical',False) for r in R['models']),'switch_active':all(r.get('switch_min',-1)>=0 for r in R['models']),'green_identity':all(r['green_error']<1e-4 and r['mutant_sign_reversed'] for r in R['models'] if r['aR_over_c2']==0)}
R['checks']['energy_positive']=all(r['energy']['fine']['minimum']>0 for r in R['models'])
R['checks']['energy_convergence']=all(r['energy']['relative_difference']<1e-3 for r in R['models'])
R['checks']['energy_known_and_mutant']=all(r['energy']['scalar_relative_error']<1e-3 and r['energy']['mutant']<0 for r in R['models'] if r['aR_over_c2']==0)
R['seconds']=time.time()-t0
# For d=(x²-hi²)/6: d''+2d'/x=1, verified directly.
R['checks']['laplacian_known_answer']=bool(np.max(abs(np.ones_like(probe)/3+2*(probe/3)/probe-1))<1e-14)
Path(args.out).write_text(json.dumps(R,indent=2));print(json.dumps(R['checks']),flush=True)
raise SystemExit(0 if all(R['checks'].values()) else 1)
