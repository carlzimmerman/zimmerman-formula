"""CT09 physical charged scalar pair resonances, including F-closed parents."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import kv
from scipy.optimize import brentq
from scalar_network import one,build_model,E,G
I2=1.8030853547393915
MUS={'canonical':544638.2663769713,'protected':18170662.111498855}

def phase(M,m,t,n=128,MB=False):
 z,w=leggauss(n);u=40*(z+1);wu=40*w;c,wc=leggauss(n);en=np.sqrt(u*u+(M/t)**2)
 if MB:avg=np.exp(-en)
 else:
  beta=math.sqrt(max(0,1-4*m*m/(M*M)))
  e1=en[:,None]/2+u[:,None]*beta*c[None,:]/2;e2=en[:,None]-e1
  p1=np.sqrt(np.maximum(0,e1*e1-(m/t)**2));p2=np.sqrt(np.maximum(0,e2*e2-(m/t)**2))
  f1=2*np.exp(-p1)/(1+np.exp(-p1));f2=2*np.exp(-p2)/(1+np.exp(-p2))
  avg=(f1*f2)@wc/2
 return float((wu*u*u/en)@avg)

def scalar_mass(x):
 d=build_model(x,E,E,G,vertices=False)
 # Lowest positive scalar is neutral at large x; charged formula has been
 # independently identified by network at all sampled points.
 aa=math.sqrt(2/(31*E))
 return E/2*math.sqrt(x*x+aa*aa)

def main(out):
 start=time.monotonic();rows=[];threshold=brentq(lambda x:2*scalar_mass(x)-math.sqrt(.006),20,30)
 xs=sorted(set([20,23,24,24.8,25,25.1,25.2,25.3,25.4,25.5,26,27,30,threshold-.01,threshold-.001,threshold-.0001,threshold,threshold+.0001]))
 controls=[abs(phase(M,.1,1,128,True)/(M*kv(1,M))-1) for M in (1,10,100)]
 maxrepeat=0
 for x in xs:
  r=one(x);m=r['m_light_S'];assert abs(m-scalar_mass(x))<1e-10
  parents=[]
  for p in r['neutral_parents']:
   W=p['to_light_scalar_pair'];M=p['mass']
   if W<1e-25:continue
   q=dict(index=p['index'],mass=M,detuning=M-2*m,width_to_light_scalar_pair=W,total_width_included=p['width'],terminal_charged=p['terminal_charged_multiplicity'],loss_fraction=1-p['terminal_charged_multiplicity']/2,terminal_neutral_rest_energy=sum(d['mass']*d['expected_number'] for d in p['terminal_daughters'] if not d['charged']),rates=[])
   for t in (.001,.00064,.0005):
    gammas={n:W*M*t*t/(2*math.pi**2)*phase(M,m,t,n) for n in (96,192)}
    gamma=gammas[192];repeat=abs(gammas[96]/gamma-1) if gamma>1e-100 else 0;maxrepeat=max(maxrepeat,repeat)
    nscalar=24*I2*t**3/(2*math.pi**2)
    loss=2*gamma/nscalar
    q['rates'].append(dict(t=t,number_mu3=nscalar,gamma_inv_mu4=gamma,absorbing_loss_over_mu=loss,net_included_loss_over_mu=loss*q['loss_fraction'],comparisons={k:dict(absorbing_loss_over_H=loss*mu/(math.sqrt(math.pi**2*106.75/90)*(t*mu/.02)**2/2.435e18),net_included_loss_over_H=loss*q['loss_fraction']*mu/(math.sqrt(math.pi**2*106.75/90)*(t*mu/.02)**2/2.435e18)) for k,mu in MUS.items()},quadrature_relative_repeat=repeat))
   parents.append(q)
  rows.append(dict(x=x,mS=m,constant_singlet_detuning=math.sqrt(.006)-2*m,parents=parents))
  print(json.dumps(dict(x=x,mS=m,constant_detuning=math.sqrt(.006)-2*m,parents=len(parents))),flush=True)
 checks=dict(MB_limit=bool(max(controls)<1e-10),quadrature_repeat=maxrepeat<.01,charged_scalar_exact_mass=True)
 result=dict(claim_id='CT09_CHARGED_SCALAR_RESONANCE',checks=checks,cases=rows,threshold_x_constant_singlet=threshold,MB_relative_errors=controls,max_quadrature_relative_repeat=maxrepeat,scope='Charged scalar isotropic frozen FD diagnostic fC=2/(exp(p/Tc)+1) per each of12 real charged scalar states, preserving original24spin initialcarrier number. Not derived daughter distribution. 96/192quadrature; parentempty. Cascade losses SSS/FFS only; vector/loop exits omitted. No cosmologicaltrajectory supplied.',runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','threshold_x_constant_singlet','max_quadrature_relative_repeat','runtime_seconds')}));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
