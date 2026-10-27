"""Actual free-domain energy on independent infall/front coordinates.

The manifold is explicitly restricted. It is a discriminator for the missing
path, not a simulated trajectory or a galaxy-law fit.
"""
import argparse,json,sys,heapq
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from free_formation import FreeVacuum
from joint import T,RESERVOIR

def landscape(step_R=.5,steps_lambda=40):
 m=FreeVacuum();initial=json.loads(Path('physical_completion_2026_10_25/run_free_formation/all_F.json').read_text());final=json.loads(Path('physical_completion_2026_10_25/run_free_finish/formed.json').read_text());m0=np.array(initial['mass']);m1=np.array(final['mass']);rr=m.r.numpy()*m.rm;xf=np.array(final['v'][m.n:]);Rf=final['scaled_boundary_kpc']
 lam=np.linspace(0,1,steps_lambda+1);R=np.sort(np.unique(np.r_[np.arange(-20,80+.1*step_R,step_R),Rf]));E=np.empty((len(lam),len(R)));cap=np.empty_like(E);tm=np.empty_like(E)
 for i,L in enumerate(lam):
  mass=(1-L)*m0+L*m1
  for j,r in enumerate(R):
   x=np.interp(rr+Rf-r,rr,xf,left=1.,right=0.);q=np.sin(np.pi*x/2)**2;E[i,j]=float(m.energy(T(np.log(mass)),T(x)));cap[i,j]=min(.9997-m.A.numpy()@(mass*q));tm[i,j]=mass@q
 start=(0,0);goal=(len(lam)-1,int(np.argmin(abs(R-Rf))));barrier=np.full(E.shape,np.inf);barrier[start]=E[start];parent={};queue=[(float(E[start]),*start)]
 while queue:
  value,i,j=heapq.heappop(queue)
  if value>barrier[i,j]:continue
  if (i,j)==goal:break
  for di,dj in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
   a=i+di;b=j+dj
   if not (0<=a<len(lam) and 0<=b<len(R)) or cap[a,b]<=0:continue
   vv=max(value,float(E[a,b]))
   if vv<barrier[a,b]:barrier[a,b]=vv;parent[(a,b)]=(i,j);heapq.heappush(queue,(vv,a,b))
 path=[];cur=goal
 while cur!=start:
  path.append([float(lam[cur[0]]),float(R[cur[1]]),float(E[cur]),float(tm[cur])]);cur=parent[cur]
 path.append([float(lam[0]),float(R[0]),float(E[start]),float(tm[start])]);path.reverse()
 # Energy-only reachability: no extra imposed trajectory time or final-density
 # penalty. Every point still has the fixed endpoint-interpolation shape.
 return {'lambda_grid':lam.tolist(),'R_grid_kpc':R.tolist(),'energy':E.tolist(),'cap_slack':cap.tolist(),'T_mass':tm.tolist(),'minimum_discrete_energy_barrier_above_initial':float(barrier[goal]-E[start]),'minimax_grid_path':path,'initial_energy':float(E[start]),'initial_allF_error':float(E[start]-initial['energy']),'goal_energy':float(E[goal]),'goal_endpoint_error':float(E[goal]-final['energy']),'grid_step_R_kpc':step_R,'grid_steps_lambda':steps_lambda,'minimum_cap_on_selected_path':float(min(cap[int(round(p[0]*steps_lambda)),np.argmin(abs(R-p[1]))] for p in path))}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[],'non_claims':['A restricted two-coordinate potential landscape, not a physical time trajectory','Density shape interpolates two previously solved physical endpoints, not arbitrary live density','Material and vacuum phase locked in this diagnostic; independent field corrections untested','Grid reachability is not a certified continuous sublevel path or formation proof']}
 for h,n in [(1.,20),(.5,40),(.25,80)]:
  r=landscape(h,n);assert abs(r['goal_endpoint_error'])<1e-9;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['lambda_grid','R_grid_kpc','energy','cap_slack','T_mass','minimax_grid_path']},flush=True)
