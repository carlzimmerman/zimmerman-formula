#!/usr/bin/env python3
"""Known line profile, independent softened-point field, and old-field anchors."""
import hashlib,json,math,platform,resource,time
from pathlib import Path
import numpy as np
import scipy
import model as M
import io_beam as B
import raw_cube as R
start=time.time();checks=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
pix=12.;axis=(np.arange(41)-20)*pix;east,north=np.meshgrid(-axis,axis,indexing='xy');vel=np.arange(-262.,-201.,2.)
I=np.exp(-(east**2+north**2)/(2*70**2));inst=4/2.355;profile=np.exp(-.5*((vel+232)/np.sqrt(9**2+inst**2))**2)
D=profile[:,None,None]*I[None]
P=dict(cube=D,v=vel,mask=np.ones(D.shape,bool),grid=np.ones(D.shape,bool),mom0=D.sum(0),XE=east,YN=north,noise=.01,pixel=[pix,pix],beam=[13.19112,10.98504,-4.95],gas_sky=np.zeros_like(I),star_R=np.array([0.,2000.]),star_prof=np.zeros(2),star_norm=1.)
c=M.Cube(P);result=c.model(np.full(I.shape,-232.),np.full(I.shape,9.));error=float(np.max(abs(result-D)))
check('constant_velocity_Gaussian_recovered',error<=1e-12,error)
check('masked_local_intensity_conserved',np.max(abs((result*c.mask).sum(0)-c.Sobs))<=1e-11)
check('known_truth_residual_zero',np.max(abs(c.residual(np.full(I.shape,-232.),np.full(I.shape,9.))))<=1e-10)
check('wrong_velocity_control_bites',np.mean(c.residual(np.full(I.shape,-222.),np.full(I.shape,9.))**2)>1.)
# Diagnose, do not waive, the extended-source corner failure above. The fixed
# border removes its intrinsic intensity; local normalization then divides by
# extremely small beam leakage. A source contained inside the border provides
# a separate well-conditioned known answer with the same absolute tolerance.
location=np.unravel_index(np.argmax(abs(result-D)),D.shape)
edge_diagnostic=dict(max_error_index=[int(i) for i in location],data_at_max=float(D[location]),
    error_at_max=float(result[location]-D[location]),
    interior_max_error=float(np.max(abs(result[:,3:-3,3:-3]-D[:,3:-3,3:-3]))),
    direct_fallback_max_pixels=c.fallback_max)
compact=I*(np.hypot(east,north)<=120.)
compact_P=dict(P,cube=profile[:,None,None]*compact[None],mom0=profile.sum()*compact)
compact_cube=M.Cube(compact_P)
compact_result=compact_cube.model(np.full(I.shape,-232.),np.full(I.shape,9.))
compact_error=float(np.max(abs(compact_result-compact_P['cube'])))
check('compact_source_Gaussian_recovered',compact_error<=1e-12,compact_error)
check('compact_source_truth_residual_zero',np.max(abs(compact_cube.residual(np.full(I.shape,-232.),np.full(I.shape,9.))))<=1e-10)
# One central surface-density pixel is a softened point source of known mass.
P['gas_sky'][20,20]=1.;b=M.Baryons(P,0.);r,v2,gas=b.vc2(0.,0.,90.,0.,M.A0['canonical'],modified=False,thickness=200.)
radius=np.hypot(b.FX,b.FY);rpc=M.C.arcsec_to_pc(radius);mass=M.C.arcsec_to_pc(pix)**2
point=M.C.GPC*mass*rpc/(rpc**2+200.**2)**1.5
edges=np.r_[0,.5*(r[1:]+r[:-1]),r[-1]+.5*(r[-1]-r[-2])];idx=np.digitize(radius.ravel(),edges)-1;good=(idx>=0)&(idx<len(r))
expected=np.bincount(idx[good],weights=point.ravel()[good],minlength=len(r))/np.maximum(np.bincount(idx[good],minlength=len(r)),1)*M.C.arcsec_to_pc(r)
err=float(np.max(abs(v2-expected))/np.max(abs(expected)))
check('FFT_softened_point_independent',err<=1e-10,err)
check('fixed_physical_field_range',r[-1]<960 and r[-1]>960-pix,float(r[-1]))
# Reproduce the original field on the identical explicit physical radial grid.
oldpix=M.C.PIX;M.C.PIX=pix
try:
 old=M.C.Baryons(P,0.)
 for foot,a0 in M.A0.items():
  for modified in [False,True]:
   rr,vv,gg=b.vc2(0.,0.,90.,35.,a0,modified=modified,radii=r)
   ro,vo,go=old.vc2(0.,0.,90.,35.,a0,nu=modified,eps_pc=200.,Rgrid=r)
   diff=float(np.max(abs(vv-vo))/max(float(np.max(abs(vo))),1e-300))
   check(f'original_field_{foot}_{modified}',diff<=1e-10 and np.array_equal(rr,ro) and np.allclose(gg,go,rtol=1e-10,atol=0),diff)
finally:M.C.PIX=oldpix
for weight in ['NA','R']:
 prepared=M.load_prepared(f'prepare_verified/baseline/{weight}_bin8');cube=M.Cube(prepared)
 check(weight+'_own_beam_loaded',cube.beam==prepared['beam'])
 check(weight+'_finite_forward_model',np.all(np.isfinite(cube.model(np.full(cube.XE.shape,-232.2),np.full(cube.XE.shape,9.)))))
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in [Path(__file__),Path(M.__file__),M.OLD,R.HERE/'io_beam.py',R.HERE/'FROZEN_CRITERIA.md',R.HERE/'AMENDMENTS.md']},versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),scope='Forward/field implementation checks only; full fits and mocks pending; kappa=1/2 FITTED; not theory closed')
obj['source_hashes'][str((R.HERE/'MODEL_NUMERICS.md').relative_to(R.ROOT))]=R.sha(R.HERE/'MODEL_NUMERICS.md')
obj['edge_normalization_diagnostic']=edge_diagnostic
B.atomic(R.HERE/'model_checks.json',obj);B.atomic(R.HERE/'model_runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
