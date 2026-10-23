"""Full vacuum tree X+Phi+antiPhi -> Phi+Phi (and conjugate).
Thermal averages are collision-kernel tests, NOT an assumed source bath.
"""
from pathlib import Path
from functools import lru_cache
from itertools import combinations
import json, sys, math
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.stats import qmc
P=Path(__file__).resolve().parent
m=.001; M=2*m*np.sqrt(1+.02**2); g=2.168e-6; lam=.00881292
charges=(2,1,-1,-1,-1)
def square(p): return p[...,0]**2-np.sum(p[...,1:]**2,axis=-1)
@lru_cache(None)
def partitions(items,count):
 if count==1:return ((items,),)
 if len(items)<count:return ()
 out=[]
 for k in range(len(items)):
  for chosen in combinations(items[1:],k):
   rest=tuple(i for i in items[1:] if i not in chosen)
   for p in partitions(rest,count-1):out.append(((items[0],)+chosen,)+p)
 return tuple(out)
def recursive(p,root):
 @lru_cache(None)
 def cur(ids,amputated=False):
  if len(ids)==1:return 1.
  q=sum(charges[i] for i in ids)
  if abs(q) not in (1,2):return 0.
  value=0.
  for count in (2,3):
   for groups in partitions(ids,count):
    v=sorted([sum(charges[i] for i in group) for group in groups]+[-q])
    factor=2*g if v in ([-2,1,1],[-1,-1,2]) else (4*lam if v==[-1,-1,1,1] else 0)
    if factor:value=value+factor*math.prod(cur(group) for group in groups)
  if amputated:return value
  return value/(square(p[:,ids,:].sum(axis=1))-(m if abs(q)==1 else M)**2)
 return cur(tuple(i for i in range(5) if i!=root),True)
def explicit(p):
 mixed=np.zeros(len(p)); cubic=np.zeros(len(p)); gaps=[]
 for j in (2,3,4):
  d=square(p[:,0]+p[:,j])-m*m
  others=[k for k in (2,3,4) if k!=j]
  dx=square(p[:,others,:].sum(axis=1))-M*M
  mixed+=8*g*lam/d; cubic+=8*g**3/(d*dx)
  gaps.extend([np.min(abs(d))/m**2,np.min(abs(dx))/m**2])
 return mixed+cubic,mixed,cubic,min(gaps)
def momenta(theta,power,seed):
 u=qmc.Sobol(11,scramble=True,seed=seed).random_base2(power);n=len(u);p=np.zeros((n,5,4));T=theta*m
 for i,mass in enumerate((M,m,m)):
  grid=np.linspace(0,max(30*np.sqrt(mass*T),45*T),30000)
  f=grid**2*np.exp(-(np.sqrt(mass**2+grid**2)-mass)/T)
  cdf=cumulative_trapezoid(f,grid,initial=0);cdf/=cdf[-1]
  r=np.interp(u[:,3*i],cdf,grid);z=2*u[:,3*i+1]-1;phi=2*np.pi*u[:,3*i+2]
  p[:,i,0]=np.sqrt(mass**2+r*r)
  p[:,i,1:]=np.column_stack((r*np.sqrt(1-z*z)*np.cos(phi),r*np.sqrt(1-z*z)*np.sin(phi),r*z))
 total=p[:,:3].sum(axis=1);s=square(total);E=np.sqrt(s)/2;r=np.sqrt(s/4-m*m)
 z=2*u[:,9]-1;phi=2*np.pi*u[:,10]
 vec=np.column_stack((r*np.sqrt(1-z*z)*np.cos(phi),r*np.sqrt(1-z*z)*np.sin(phi),r*z))
 b=total[:,1:]/total[:,0,None];b2=(b*b).sum(axis=1);gamma=total[:,0]/np.sqrt(s);dot=(b*vec).sum(axis=1)
 for j,sgn in ((3,1),(4,-1)):
  p[:,j,0]=-gamma*(E+sgn*dot)
  p[:,j,1:]=-(sgn*vec+b*((gamma-1)*sgn*dot/b2+gamma*E)[:,None])
 return p,s

def run():
 O=P/sys.argv[1];O.mkdir(exist_ok=True)
 p=np.zeros((1,5,4));p[0,:3,0]=[M,m,m];p[0,3:,0]=-(M+2*m)/2
 p[0,3,1]=np.sqrt(((M+2*m)/2)**2-m*m);p[0,4,1]=-p[0,3,1]
 a,am,ac,gap=explicit(p);beta=np.sqrt(1-4*m*m/(M+2*m)**2)
 D0=float(beta*a[0]**2/(256*np.pi*M*m*m))
 roots=[float(recursive(p,r)[0]) for r in range(5)]
 rows=[];root_error=0.;balance_error=0.
 for theta in np.geomspace(.01,2,17):
  vals=[]
  for power,seed in ((14,202610233),(16,202610234)):
   p,s=momenta(theta,power,seed);a,am,ac,gap=explicit(p)
   sample=np.sqrt(1-4*m*m/s)*a*a/(256*np.pi*np.prod(p[:,:3,0],axis=1))
   # BE/MB equilibrium forward reaction density ratio, not a rate per BE density.
   energies=abs(p[:,:,0]);bose=1/(-np.expm1(-energies/(theta*m)))
   vals.append((float(sample.mean()),float((sample*bose.prod(axis=1)).mean()/sample.mean())))
  for r in range(5):
   ar=recursive(p[:100],r);root_error=max(root_error,float(np.max(abs(ar-a[:100]))/max(abs(a[:100]))))
  # log forward/inverse Bose weights at mu=0 reduces to energy balance.
  balance_error=max(balance_error,float(np.max(abs(p.sum(axis=1)[:,0]/(theta*m)))))
  rows.append(dict(T_over_m=float(theta),D_MB_GeV_minus5=vals[1][0],coarse_fine_relative=abs(vals[1][0]/vals[0][0]-1),BE_to_MB_equilibrium_forward_density=vals[1][1],minimum_sample_propagator_gap_over_m2=gap,momentum_error_over_m=float(np.max(abs(p.sum(axis=1)))/m)))
  print(theta,vals[1],flush=True)
 # Exact neutral quantum states with identical one-body data and distinct pair rates.
 counterexample=[dict(N=10,K=k,mean_n_plus=10,mean_n_minus=10,net_charge=0,pair_moment=10*k,rate_relative_to_number_state=k/10) for k in (10,100,1000)]
 checks=dict(root_invariance=root_error<1e-10,threshold_root_invariance=max(abs(x/roots[0]-1) for x in roots)<1e-12,MC_agreement=max(r['coarse_fine_relative'] for r in rows)<.05,four_momentum=max(r['momentum_error_over_m'] for r in rows)<1e-10,detailed_balance_equilibrium=balance_error<1e-10,cold_limit=abs(rows[0]['D_MB_GeV_minus5']/D0-1)<.1)
 out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),threshold=dict(amplitude=float(a[0]) if False else roots[0],D_GeV_minus5=D0,roots=roots),rates=rows,root_relative_error=root_error,neutral_state_counterexample=counterexample,scope='Vacuum quasiparticles; all six tree diagrams for this channel. MB thermal averages and equilibrium Bose forward-density correction. No source thermalization time or cosmological yield derived. Other crossed 3-to-2 channels need real-intermediate-state subtraction.')
 (O/'results.json').write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
if __name__=='__main__':run()
