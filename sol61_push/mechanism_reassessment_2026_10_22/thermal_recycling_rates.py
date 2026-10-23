"""Finite-temperature contact 4<->2 and vacuum X-pair rates.
The contact collision kernel is a subset of the original action, not a
RIS-subtracted calculation of every cubic-containing off-shell diagram.
"""
import json,sys
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy.special import kve
from scipy.integrate import quad, cumulative_trapezoid
from scipy.stats import qmc
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
m=.001;M=2*m*np.sqrt(1+.02**2);g=2.168e-6;lam=.00881292

def pair(T):
 x=M/T; k2=kve(2,x)
 def fun(t):
  w=2+t/x;beta=np.sqrt(1-4/w**2);betaf=np.sqrt(1-4*(m/M)**2/w**2)
  sv=2*betaf*g**4/(np.pi*M**6*w*w*(1+(m/M)**2*(w*w-4)))
  sigma=sv/(2*beta)
  return .25*sigma*(w*w-4)*w*w*kve(1,x*w)*np.exp(-t)/(k2*k2)
 return quad(fun,0,80,epsabs=1e-22,epsrel=2e-7,limit=120)[0]

def amps(p,charges):
 total=np.zeros(len(p))
 for others in combinations(range(1,6),2):
  ids=(0,)+others
  if abs(sum(charges[i] for i in ids))!=1:continue
  q=p[:,ids,:].sum(axis=1);den=q[:,0]**2-(q[:,1:]**2).sum(axis=1)-1
  total+=1/den
 return 16*lam**2*total

def contact(theta,power,seed):
 u=qmc.Sobol(14,scramble=True,seed=seed).random_base2(power);N=len(u)
 qgrid=np.linspace(0,max(30*np.sqrt(theta),45*theta),20000)
 f=qgrid*qgrid*np.exp(-(np.sqrt(1+qgrid*qgrid)-1)/theta)
 cdf=cumulative_trapezoid(f,qgrid,initial=0);cdf/=cdf[-1]
 mom=np.zeros((N,6,4))
 for i in range(4):
  r=np.interp(u[:,3*i],cdf,qgrid);z=2*u[:,3*i+1]-1;ph=2*np.pi*u[:,3*i+2]
  mom[:,i,0]=np.sqrt(1+r*r);mom[:,i,1]=r*np.sqrt(1-z*z)*np.cos(ph);mom[:,i,2]=r*np.sqrt(1-z*z)*np.sin(ph);mom[:,i,3]=r*z
 total=mom[:,:4].sum(axis=1);s=total[:,0]**2-(total[:,1:]**2).sum(axis=1);ecm=np.sqrt(s)/2;pf=np.sqrt(s/4-1)
 z=2*u[:,12]-1;ph=2*np.pi*u[:,13];vec=np.column_stack((pf*np.sqrt(1-z*z)*np.cos(ph),pf*np.sqrt(1-z*z)*np.sin(ph),pf*z))
 beta=total[:,1:]/total[:,0,None];b2=(beta*beta).sum(axis=1);gamma=total[:,0]/np.sqrt(s);dot=(beta*vec).sum(axis=1)
 for j,sgn in [(4,1),(5,-1)]:
  mom[:,j,0]=-gamma*(ecm+sgn*dot)
  mom[:,j,1:]=-(sgn*vec+beta*((gamma-1)*sgn*dot/b2+gamma*ecm)[:,None])
 a31=amps(mom,[1,1,1,-1,-1,-1]);a22=amps(mom,[1,1,-1,-1,-1,1])
 phase=np.sqrt(1-4/s)/(8*np.pi)/(16*np.prod(mom[:,:4,0],axis=1))
 samples=phase*(2*a31*a31/12+a22*a22/4)/8/m**8
 return float(samples.mean()),float(samples.std()/np.sqrt(N)),float(np.max(abs(mom.sum(axis=1))))

thetas=np.geomspace(.02,2,25);rows=[]
for i,t in enumerate(thetas):
 c1,err,cons=contact(t,14,202610231);c2,err2,cons2=contact(t,16,202610232)
 rows.append({'T_over_m':float(t),'C_contact':c2,'C_coarse':c1,'MC_iid_error_diagnostic':err2,'coarse_fine_relative':abs(c2/c1-1),'momentum_error_m':max(cons,cons2),'pair_sigma_v':pair(t*m)})
 print(i,t,c2,flush=True)
# Independent threshold values at zero velocity.
p=np.zeros((1,6,4));p[0,:4,0]=1;p[0,4:,0]=-2;p[0,4,1]=np.sqrt(3);p[0,5,1]=-np.sqrt(3)
a31=amps(p,[1,1,1,-1,-1,-1])[0];a22=amps(p,[1,1,-1,-1,-1,1])[0]
threshold=45*np.sqrt(3)*lam**4/(1024*np.pi*m**8)
sv0=g**4*np.sqrt(1-m*m/M**2)/(2*np.pi*M**6)
checks={'contact31_threshold':abs(a31/(-18*lam**2)-1)<1e-12,'contact22_threshold':abs(a22/(-12*lam**2)-1)<1e-12,'four_momentum':max(r['momentum_error_m'] for r in rows)<1e-10,'pair_cold_limit':abs(pair(m*1e-5)/sv0-1)<1e-4,'contact_MC_agreement_15percent':max(r['coarse_fine_relative'] for r in rows)<.15}
out={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':bool(all(checks.values())),'rates':rows,'contact_threshold':threshold,'pair_threshold':sv0,'scope':'Maxwell-Boltzmann incoming particles, no Bose enhancement. Finite-energy quartic contact trees only for 4-to-2. Explicit X reactions handle the resonant recycling subnetwork; off-shell cubic corrections and full RIS subtraction not calculated.'}
(O/'results.json').write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
