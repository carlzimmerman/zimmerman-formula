"""One-dimensional periodic GP evolution with exact local pair loss."""
import json,sys,math
from pathlib import Path
import numpy as np
checks=[]
def test(name,x):
 checks.append({'name':name,'passed':bool(x)}); assert x,name

def run(N,dt,eta,r,seed=.001,end=20):
 L=8*math.pi/math.sqrt(2); x=np.arange(N)*L/N;k=2*math.pi*np.fft.fftfreq(N,d=L/N)
 mod=seed*(np.cos(4*2*math.pi*x/L)+.05*np.cos(2*math.pi*x/L))
 p=np.sqrt(1+mod).astype(complex);q=np.sqrt(1-mod).astype(complex)
 phase=np.exp(-.25j*k*k*dt)
 def diag():
  a=abs(p)**2;b=abs(q)**2
  energy=np.mean(.5*abs(np.fft.ifft(1j*k*np.fft.fft(p)))**2+.5*abs(np.fft.ifft(1j*k*np.fft.fft(q)))**2+.5*(a*a+b*b)+eta*a*b)
  tail=sum(np.sum(abs(np.fft.fft(v)/N)[abs(k)>max(abs(k))*2/3]**2) for v in [p,q])
  return float(np.mean(a)),float(np.mean(b)),float(np.mean(a*b)),float(energy),float(tail)
 start=diag();old=start;integral=0.;emin=1.;hist=[];maxcharge=0.;maxtail=0.;maxenergy=0.
 for i in range(round(end/dt)):
  p=np.fft.ifft(np.fft.fft(p)*phase);q=np.fft.ifft(np.fft.fft(q)*phase)
  a=abs(p)**2;b=abs(q)**2
  if r==0:
   p*=np.exp(-1j*(a+eta*b)*dt);q*=np.exp(-1j*(b+eta*a)*dt)
  else:
   hi=np.maximum(a,b);lo=np.minimum(a,b);d=hi-lo
   # (1-exp(-r*d*dt))/d with continuous d=0 limit.
   z=r*d*dt;f=np.empty_like(d);nz=d>1e-12
   f[nz]=-np.expm1(-z[nz])/d[nz];f[~nz]=r*dt
   denominator=1+lo*f;newlo=lo*np.exp(-z)/denominator;newhi=newlo+d
   Ilo=np.log1p(lo*f)/r;Ihi=Ilo+d*dt
   newa=np.where(a>=b,newhi,newlo);newb=np.where(a>=b,newlo,newhi)
   Ia=np.where(a>=b,Ihi,Ilo);Ib=np.where(a>=b,Ilo,Ihi)
   p*=np.sqrt(newa/np.maximum(a,1e-300))*np.exp(-1j*(Ia+eta*Ib))
   q*=np.sqrt(newb/np.maximum(b,1e-300))*np.exp(-1j*(Ib+eta*Ia))
  p=np.fft.ifft(np.fft.fft(p)*phase);q=np.fft.ifft(np.fft.fft(q)*phase)
  now=diag();integral+=dt*(old[2]+now[2])/2
  maxcharge=max(maxcharge,abs(now[0]-now[1]));maxtail=max(maxtail,now[4]);maxenergy=max(maxenergy,abs(now[3]-start[3]))
  overlap=now[2]/(now[0]*now[1]);emin=min(emin,overlap)
  if (i+1)%round(.2/dt)==0:hist.append({'t':(i+1)*dt,'survival':(now[0]+now[1])/2,'overlap_normalized':overlap})
  old=now
 residual=abs(now[0]-start[0]+r*integral)
 test('charge '+str((N,dt,eta,r,seed)),maxcharge<1e-9)
 test('integrated loss '+str((N,dt,eta,r,seed)),residual<2e-5)
 test('spectral tail '+str((N,dt,eta,r,seed)),maxtail<1e-7)
 if r==0:test('energy conservation',maxenergy<1e-4)
 if seed==0:test('uniform exact loss',abs(now[0]-1/(1+r*end))<1e-9)
 return {'N':N,'dt':dt,'eta':eta,'loss_ratio_r':r,'seed':seed,'final_survival':(now[0]+now[1])/2,'uniform_survival':1/(1+r*end),'minimum_normalized_overlap':emin,'final_normalized_overlap':overlap,'loss_integral_residual':residual,'max_charge_error':maxcharge,'max_spectral_tail':maxtail,'max_energy_change':maxenergy,'history':hist}
rows=[run(256,.002,2.0002,r) for r in [0,.01,.1,1]]
rows.extend([run(256,.002,.5,.1),run(256,.002,2.0002,.1,seed=0),run(256,.001,2.0002,.1),run(512,.001,2.0002,.1)])
rows.extend([run(256,.001,2.0002,.01),run(512,.001,2.0002,.01)])
for first,second,name in [(rows[2],rows[6],'time'),(rows[6],rows[7],'grid'),(rows[1],rows[8],'low-loss time'),(rows[8],rows[9],'low-loss grid')]:
 err=max(abs(a['survival']-b['survival']) for a,b in zip(first['history'],second['history']))
 test(name+' refinement survival',err<2e-4)
 err2=max(abs(a['overlap_normalized']-b['overlap_normalized']) for a,b in zip(first['history'],second['history']))
 test(name+' refinement overlap',err2<2e-3)
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'rows':rows,'scope':'Finite 1D periodic seeded two-condensate mean-field model. No production, trap design, thermalization or 3D longevity claim.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
for row in rows:print(json.dumps({k:v for k,v in row.items() if k!='history'}),flush=True)
