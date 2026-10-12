"""Frozen produced radial spectrum: continuum angular forced-source response."""
import json,math
from pathlib import Path
import numpy as np
from scipy.special import sici
from scipy.integrate import quad
p=Path(__file__).parent
prod=json.loads((p/'detuned_bogoliubov_run/results.json').read_text())
par=prod['parameters'];u=par['u'];eps=par['epsilon'];R=par['M_eV']/par['m_eV']
gamma=0.5772156649015328606
checks=[]
def check(n,error,tol):checks.append(dict(name=n,error=float(error),passed=bool(abs(error)<tol)))
def primitive(d,t):
 y=d*t;small=abs(y)<.01;safe=np.where(small,1.,abs(y));si,ci=sici(safe)
 i0=t*(2*np.sign(y)*si+2*np.expm1(1j*y).real/np.where(small,1.,y))
 i1=2*(gamma+np.log(safe)-ci)
 i0=np.where(small,t*(y-y**3/36+y**5/1800),i0)
 i1=np.where(small,y*y/2-y**4/48+y**6/2160,i1)
 return i0,i1
def bounds(q,r):
 la=lambda k:u*u*(k*k-1)/(eps*(np.sqrt(1+u*u*k*k)+math.sqrt(1+u*u)))
 ell=la(q)+la(r)
 lb=lambda k:u*u*k*k/(eps*(np.sqrt(R*R+u*u*k*k)+R))
 lo=lb(q-r)-ell;hi=lb(q+r)-ell
 a=(R+eps*ell)*eps/(2*u*u*q*r);b=eps*eps/(2*u*u*q*r)
 return lo,hi,a,b,ell
def kernel(q,r,t):
 lo,hi,a,b,_=bounds(q,r)
 j0,j1=primitive(hi,t);i0,i1=primitive(lo,t)
 return a*(j0-i0)+b*(j1-i1)
# Independent angular integration, including off-shell daughter radii.
for q,r,t in [(1.,1.,.1),(.999,1.001,.1),(1.001,1.001,.1),(.999,.999,.1)]:
 lo,hi,a,b,_=bounds(q,r)
 direct=quad(lambda d:(a+b*d)*t*t*np.sinc(d*t/(2*math.pi))**2,lo,hi,epsabs=1e-11,limit=300)[0]
 check('angular integral '+str((q,r,t)),kernel(q,r,t)-direct,1e-10)
 check('angular normalization '+str((q,r)),a*(hi-lo)+b*(hi*hi-lo*lo)/2-1,1e-12)
rows=[]
times=[1.,10.,30.,100.,200.]
for row in prod['rows'][:3]:
 q=np.asarray(row['initial_mode_p_over_m'])/u;f=np.asarray(row['final_pair_fractions'])
 result=np.zeros(len(times));rate=0.;resweight=0.;minval=1e100
 for start in range(0,len(q),64):
  qi=q[start:start+64,None];qj=q[None,:];ff=f[start:start+64,None]*f[None,:]
  lo,hi,a,b,ell=bounds(qi,qj)
  resonant=(lo<0)&(hi>0)
  rate+=float(np.sum(4*math.pi*ff*a*resonant))
  resweight+=float(np.sum(ff*resonant))
  for j,t in enumerate(times):
   val=kernel(qi,qj,t);minval=min(minval,float(np.min(val)))
   result[j]+=float(2*np.sum(ff*val))
 check('kernel positivity K'+str(row['K']),min(0,minval),1e-10)
 rows.append(dict(K=row['K'],vmax=row['vmax'],daughter_fraction=float(f.sum()),times=times,source_response=result.tolist(),long_time_Born_slope=rate,radial_pair_weight_with_interior_resonance=resweight/float(f.sum())**2,minimum_kernel=minval))
for j,t in enumerate(times):
 check('radial resolution x='+str(t),rows[0]['source_response'][j]-rows[1]['source_response'][j],1e-4)
 check('radial bandwidth x='+str(t),rows[1]['source_response'][j]-rows[2]['source_response'][j],1e-4)
out=dict(parameters=par,rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Frozen free-evolving Gaussian ensemble using occupation spectrum at production x=200; elapsed response time is separate','No daughter depletion, source remnant, quartic mean-field shift or expansion','Not actual unequal-time produced correlations or nonlinear survival','Classical envelope coupling convention; relativistic vertex corrections omitted'])
(p/'detuned_radial_response_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
