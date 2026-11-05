#!/usr/bin/env python3
"""Bounded model/optimizer implementation tests, not frozen production mocks."""
import json,platform,resource,time
from pathlib import Path
import numpy as np
from scipy import ndimage
import scipy
import fitting as F
import model as M
import io_beam as B
import raw_cube as R
start=time.time();checks=[]
def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
a=np.sin(np.arange(160)*.17)+np.arange(160)*.01
check('physical_smoothing_original_6arcsec',np.allclose(F.smooth_physical(a,6),ndimage.uniform_filter1d(a,5),rtol=0,atol=1e-14))
weights=np.r_[.5,np.ones(9),.5]/10
check('physical_smoothing_3arcsec_half_endcells',np.allclose(F.smooth_physical(a,3),ndimage.convolve1d(a,weights,mode='reflect'),rtol=0,atol=1e-14))
check('physical_smoothing_constant_DC',all(np.max(abs(F.smooth_physical(np.ones(40),p)-1))<1e-14 for p in (3.,6.,12.)))
# Independent cell-overlap integral with explicit half-sample reflection.
def direct(q,pixel):
 out=[];half=15/pixel
 for i in range(len(q)):
  total=0.
  for j in range(int(np.floor(i-half-.5)),int(np.ceil(i+half+.5))+1):
   w=max(0.,min(j+.5,i+half)-max(j-.5,i-half))
   k=j%(2*len(q));k=k if k<len(q) else 2*len(q)-k-1
   total+=w*q[k]
  out.append(total/(2*half))
 return np.array(out)
check('physical_smoothing_independent_integral',all(np.max(abs(F.smooth_physical(a,p)-direct(a,p)))<1e-13 for p in (3.,6.,12.)))
pixel=12.;axis=(np.arange(21)-10)*pixel;xe,yn=np.meshgrid(-axis,axis);v=np.arange(-262.,-201.,2.)
I=np.exp(-(xe**2+yn**2)/(2*40**2))*(np.hypot(xe,yn)<70.)
profile=np.exp(-.5*((v+232.2)/9.)**2);D=profile[:,None,None]*I[None]
P=dict(cube=D,v=v,mask=np.ones(D.shape,bool),grid=np.ones(D.shape,bool),mom0=D.sum(0),XE=xe,YN=yn,noise=.01,
       pixel=[pixel,pixel],beam=[13.19112,10.98504,-4.95],nring=6,ring_width=13.19112,R_out=79.14672,
       initial_ring_R=np.arange(6)*13.19112+6.59556,initial_ring_V=np.linspace(3.,18.,6))
c=M.Cube(P);free=F.Free(c,P);truth=free.start(35.);vl,sg,_=free.fields(truth);mock=c.model(vl,sg)
Q=dict(P,cube=mock);cc=M.Cube(Q);ff=F.Free(cc,Q)
check('free_truth_forward_residual',np.max(abs(ff.residual(truth)))<=1e-10)
r=ff.fit(truth,budget=2);result=F.summarize(r,cc,ff,2)
check('exact_truth_optimizer_stationary',r.status>0 and np.max(abs(r.x-truth))<1e-10 and result['chi2_red']<1e-20)
check('pilot_not_accepted_production',not result['optimizer_accepted'] and result['scope'].startswith('UNGRADED'))
wrong=truth.copy();wrong[4]+=10
check('wrong_systemic_velocity_control',np.mean(ff.residual(wrong)**2)>1.)
try:F.Free(cc,Q,stop=lambda:True).residual(truth)
except F.YieldRequested:stopped=True
else:stopped=False
check('signal_stop_at_residual_boundary',stopped)
class ConstantBaryons:
 pixel=6.
 def vc2(self,*args,**kwargs):
  rr=(np.arange(160)+.5)*self.pixel
  return rr,np.full(160,100.),np.ones(160)
for nc in (False,True):
 law=F.Law(cc,Q,ConstantBaryons(),M.A0['canonical'],nc=nc)
 p=law.start();rotation,rr,vc=law.rotation(0,0,73.7,35,np.full(6,9.))
 check('constant_density_pressure_zero_'+str(nc),np.max(abs(rotation(rr)-10))<1e-12 and np.all(vc==10))
 vl,sg,rad=law.fields(p,35)
 pa=np.deg2rad(73.7);major=xe*np.sin(pa)+yn*np.cos(pa);minor=(-xe*np.cos(pa)+yn*np.sin(pa))/np.cos(np.deg2rad(35));radius=np.hypot(major,minor)
 co=np.divide(major,radius,out=np.zeros_like(radius),where=radius>0)
 expected=-232.2+np.sin(np.deg2rad(35))*10*co
 check('constant_rotation_projected_'+str(nc),np.max(abs(vl-expected))<1e-12 and np.all(sg==9))
 if nc:
  p[10:16]=2;p[16:22]=3;p[22:28]=4
  vv,_,_=law.fields(p,35);sn=np.divide(minor,radius,out=np.zeros_like(radius),where=radius>0)
  expected=expected+np.sin(np.deg2rad(35))*(2*sn+3*(2*co*co-1)+4*2*sn*co)
  check('six_node_harmonics_independent',np.max(abs(vv-expected))<1e-12)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),pilot_fit=result,
 source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in [Path(__file__),Path(F.__file__),Path(M.__file__),M.OLD,R.HERE/'MODEL_NUMERICS.md',R.HERE/'FROZEN_CRITERIA.md']},
 versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
 scope='Synthetic implementation checks only, not KA1/KA2, real fits, convergence or production eligibility')
B.atomic(R.HERE/'fitting_checks.json',obj);B.atomic(R.HERE/'fitting_runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2))
raise SystemExit(int(obj['passed']!=obj['total']))
