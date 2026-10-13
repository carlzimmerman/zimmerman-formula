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
    inner=half*((np.maximum(1-e1/esc,0)**3.5*np.maximum(1-e2/esc,0)**3.5)@w)
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


from scipy.special import beta as betaf
from scipy.integrate import quad
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];g=params['cubic_g_eV'];hbev=1.054571817e-34/1.602176634e-19;hc=hbev*c;year=365.25*86400
n0=1e-21*c*c/1.602176634e-19*hc**3/m;w0=(m*u)**3/(2*math.pi**2)
A0=n0/(w0*math.sqrt(2)*esc0**1.5*betaf(1.5,4.5));fconstant=A0/esc0**3.5
GammaGyr=g*g*u/(16*math.pi*m)/hbev*year*1e9

def mean_power(B,q):
 B,q=np.broadcast_arrays(np.asarray(B),np.asarray(q));out=np.empty_like(q,dtype=float)
 zero=q==0;out[zero]=B[zero]**3.5
 inside=(q<B)&~zero;z=q[inside]/B[inside]
 out[inside]=(B[inside]+q[inside])**4.5*(-np.expm1(4.5*(np.log1p(-z)-np.log1p(z))))/(9*q[inside])
 other=(~zero)&(~inside);out[other]=(B[other]+q[other])**4.5/(9*q[other])
 return out
for ratio in [0.,1e-8,.1,.99,1.,1.01,10.]:
 exact=quad(lambda z:max(1-ratio*z,0)**3.5,-1,1,epsabs=1e-11)[0]/2
 val=float(mean_power(1.,ratio));check('angular occupation integral',abs(val/exact-1)<1e-9)

def run(R,Q,U,O):
 r,v,w,E,L2,rp,ra,rooterr=births(R,Q,U);z,gw=leggauss(O)
 theta=math.pi*(z+1)/4;span=ra-rp
 rad=rp[:,None]+span[:,None]*np.sin(theta)**2
 vr2=2*(E[:,None]+1/np.sqrt(1+rad*rad))-L2[:,None]/(rad*rad)
 if np.min(vr2)<=0:raise ValueError('orbit resolution failed')
 dt=(math.pi/4*gw)*2*span[:,None]*np.sin(theta)*np.cos(theta)/np.sqrt(vr2)
 B=-esc0*E-.5;q2=2*esc0*(E[:,None]+1/np.sqrt(1+rad*rad))
 check('bound-parent deficit positive',float(B.min())>0 and float(q2.min())>0)
 localrate=GammaGyr*(1+2*fconstant*mean_power(B[:,None],np.sqrt(q2)))
 period=2*dt.sum(axis=1)*unitMyr/1000
 optical=2*(dt*localrate).sum(axis=1)*unitMyr/1000
 averaged=optical/period
 # Solve d(delta F)/dt=-L(t) delta F analytically via cumulative integral.
 return dict(radial_order=R,energy_order=Q,orientation_order=U,orbit_order=O,orbits=len(w),birth_weighted_mean_relaxation_rate_per_Gyr=float(w@averaged),birth_weighted_mean_radial_period_Gyr=float(w@period),mean_optical_depth_per_radial_period=float(w@optical),mean_memory_after_one_radial_period=float(w@np.exp(-optical)),mean_memory_after_three_radial_periods=float(w@np.exp(-3*optical)),birth_fraction_with_optical_depth_above_one=float(w[optical>1].sum()),minimum_rate_per_Gyr=float(averaged.min()),maximum_rate_per_Gyr=float(averaged.max()))
runs=[run(16,16,8,32),run(24,24,12,32),run(24,24,12,64)]
check('orbit quadrature refinement',abs(runs[1]['mean_memory_after_one_radial_period']-runs[2]['mean_memory_after_one_radial_period'])<1e-6)
check('birth quadrature refinement',abs(runs[0]['mean_memory_after_one_radial_period']-runs[2]['mean_memory_after_one_radial_period'])<1e-5)
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,runs=runs,central_occupation_amplitude=A0,non_claims=['Fixed daughter bath and fixed potential','Memory of a source occupation perturbation, not tagged-particle survival','Not a self-consistent mixed-species stationary solution','No heat export or halo profile prediction'])
(p/'orbital_reaction_memory_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks:',len(checks));assert out['all_pass']
