"""Collisionless orbital residence distribution of initial source births in a fixed Plummer halo."""
import json,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
p=Path(__file__).parent
prior=json.loads((p/'bound_halo_reactions_run/results.json').read_text())
bkpc=prior['halo']['scale_radius_kpc'];xmax=prior['halo']['activation_radius_over_scale']
u=.001;c=299792458.;sig=200000.;esc0=6*sig*sig/(u*c)**2
unitMyr=bkpc*3.0856775814913673e19/(math.sqrt(6)*sig)/(365.25*86400*1e6)
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
cache={}
def births(R,Q,U):
 key=(R,Q,U)
 if key in cache:return cache[key]
 zr,wr=leggauss(R);z,w=leggauss(Q);mu,wm=leggauss(U);rr=[];vv=[];mm=[];ww=[]
 for lo,hi in [(0.,1.),(1.,xmax)]:
  xs=lo+(hi-lo)*(zr+1)/2;wx=wr*(hi-lo)/2
  for x,weightx in zip(xs,wx):
   esc=esc0/math.sqrt(1+x*x);qmax=math.sqrt(2*esc-1);split=math.sqrt(2*esc)-1
   for qlo,qhi in [(0.,split),(split,qmax)]:
    qs=qlo+(qhi-qlo)*(z+1)/2;wq=w*(qhi-qlo)/2;ec=1+qs*qs;half=np.minimum(qs,esc-ec/2)
    e1=ec[:,None]/2+half[:,None]*z;e2=ec[:,None]-e1
    inner=half@np.zeros(Q) if False else half*((np.maximum(1-e1/esc,0)**3.5*np.maximum(1-e2/esc,0)**3.5)@w)
    weights=weightx*x*x/(1+x*x)**3.5*wq*2*qs*inner
    for q,weight in zip(qs,weights):
     rr.extend([x]*U);vv.extend([q/math.sqrt(esc0)]*U);mm.extend(mu);ww.extend(weight*wm/2)
 r=np.array(rr);v=np.array(vv);mu=np.array(mm);w=np.array(ww);w/=sum(w)
 E=v*v/2-1/np.sqrt(1+r*r);L2=(r*v)**2*(1-mu*mu)
 rp=np.empty_like(r);ra=np.empty_like(r);rooterr=0.
 for i in range(len(r)):
  def radial(x):return 2*(E[i]+1/math.sqrt(1+x*x))-L2[i]/(x*x)
  rp[i]=brentq(radial,1e-18,r[i],xtol=1e-15,rtol=1e-13)
  ra[i]=brentq(radial,r[i],xmax+1e-8,xtol=1e-15,rtol=1e-13)
  rooterr=max(rooterr,abs(radial(rp[i])),abs(radial(ra[i])))
 check('source binding and orbital support',float(max(E))<-.5/esc0 and float(max(ra))<=xmax+1e-8)
 check('turning point residual',rooterr<1e-7)
 result=(r,v,w,E,L2,rp,ra,rooterr);cache[key]=result;return result

def run(R,Q,U,O):
 r,v,w,E,L2,rp,ra,rooterr=births(R,Q,U);z,gw=leggauss(O)
 def integrals(indices,upper=None):
  low=rp[indices];high=ra[indices];span=high-low
  uppertheta=np.full(len(low),math.pi/2) if upper is None else np.arcsin(np.sqrt((upper-low)/span))
  theta=uppertheta[:,None]*(z+1)/2;rad=low[:,None]+span[:,None]*np.sin(theta)**2
  speed2=2*(E[indices,None]+1/np.sqrt(1+rad*rad))-L2[indices,None]/(rad*rad)
  if np.min(speed2)<=0:raise ValueError('nonpositive interior radial speed; turning-point resolution insufficient')
  measure=(uppertheta[:,None]/2*gw)*2*span[:,None]*np.sin(theta)*np.cos(theta)/np.sqrt(speed2)
  return rad,measure
 ids=np.arange(len(w));rad,measure=integrals(ids);halfperiod=measure.sum(axis=1)
 r2=(measure*rad*rad).sum(axis=1)/halfperiod
 velocity2=(measure*2*(E[:,None]+1/np.sqrt(1+rad*rad))).sum(axis=1)/halfperiod
 virial=(measure*rad*rad/(1+rad*rad)**1.5).sum(axis=1)/halfperiod
 err=abs(velocity2-virial);check('weighted orbit virial identity',float(w@err)<1e-7)
 cdf=[]
 for cut in [.25,.5,1.,2.,4.,xmax]:
  fractions=(ra<=cut).astype(float);cross=np.where((rp<cut)&(ra>cut))[0]
  if len(cross):_,dtime=integrals(cross,cut);fractions[cross]=dtime.sum(axis=1)/halfperiod[cross]
  check('CDF probabilities',float(min(fractions))>=0 and float(max(fractions))<=1+1e-7)
  cdf.append(dict(radius_over_b=cut,birth_fraction=float(w[r<=cut].sum()),orbital_residence_fraction=float(w@fractions)))
 return dict(radial_order=R,energy_order=Q,orientation_order=U,orbit_order=O,orbits=len(w),root_residual=rooterr,weighted_virial_residual=float(w@err),max_virial_residual=float(max(err)),birth_rms_radius_over_b=float(math.sqrt(w@(r*r))),orbit_rms_radius_over_b=float(math.sqrt(w@r2)),birth_1d_dispersion_kms=float(math.sqrt(w@(v*v)/3)*math.sqrt(6)*sig/1000),orbit_1d_dispersion_kms=float(math.sqrt(w@velocity2/3)*math.sqrt(6)*sig/1000),mean_radial_period_Myr=float(w@(2*halfperiod)*unitMyr),cdf=cdf)
runs=[run(16,16,8,32),run(24,24,12,32),run(24,24,12,64)]
check('orbit quadrature refinement',abs(runs[1]['cdf'][2]['orbital_residence_fraction']-runs[2]['cdf'][2]['orbital_residence_fraction'])<1e-6)
check('birth quadrature refinement',abs(runs[0]['cdf'][2]['orbital_residence_fraction']-runs[2]['cdf'][2]['orbital_residence_fraction'])<.003)
check('birth normalization matches prior independent rate integral',abs(runs[-1]['cdf'][2]['birth_fraction']-prior['runs'][-1]['birth_fraction_inside_scale_radius'])<1e-8)
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,runs=runs,scale_radius_kpc=bkpc,non_claims=['Fixed potential and dilute collisionless source tracers only','Residence average, not a time-resolved density or attractor','No decay, inverse reaction after birth, potential response or halo law'])
(p/'source_orbits_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks:',len(checks));assert out['all_pass']
