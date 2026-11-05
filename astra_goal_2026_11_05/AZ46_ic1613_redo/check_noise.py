#!/usr/bin/env python3
"""Independent linear/covariance checks for paired physical mock noise."""
import json,platform,resource,time
from pathlib import Path
import numpy as np
from scipy import ndimage
import scipy
import mock_noise as N
import io_beam as B
import raw_cube as R
start=time.time();checks=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
seed=[20261105,46,0,0,0];beam=[13.19112,10.98504,-4.95];shape=(9,24,24)
white=np.random.default_rng(np.random.SeedSequence(seed)).standard_normal(shape)
kernel=B.beam_kernel(24,24,1.5,beam,5)
# Independent circular-convolution reference using shifts and positive weights.
full=np.zeros(shape)
for y in range(24):
 for x in range(24):full+=kernel[y,x]*np.roll(white,(y,x),axis=(1,2))
full=ndimage.convolve1d(full,[.25,.5,.25],axis=0,mode='nearest')
for bins in (1,2,4,8):
 actual=N.noise_field(shape,1.5,beam,bins,(0,8),seed)
 reference=full.reshape(9,24//bins,bins,24//bins,bins).mean(axis=(2,4))
 error=float(np.max(abs(actual-reference)))
 check('streamed_full_reference_bin'+str(bins),error<=1e-12,error)
fine=N.noise_field(shape,1.5,beam,2,(0,8),seed)
coarse=N.noise_field(shape,1.5,beam,4,(0,8),seed)
check('same_physical_noise_block_pair',np.max(abs(fine.reshape(9,6,2,6,2).mean(axis=(2,4))-coarse))<=1e-12)
trim=N.noise_field(shape,1.5,beam,4,(2,6),seed)
check('trim_after_native_spectral_filter',np.array_equal(trim,coarse[2:7]))
check('exact_repeat',np.array_equal(trim,N.noise_field(shape,1.5,beam,4,(2,6),seed)))
check('seed_separation',not np.array_equal(trim,N.noise_field(shape,1.5,beam,4,(2,6),seed[:-1]+[1])))
scaled,meta=N.scale_rms(trim,.00123)
check('measured_rms_recovered',abs(scaled.std()/.00123-1)<=1e-12)
check('realized_mean_not_subtracted',np.allclose(scaled,trim*meta['scale_factor'],rtol=0,atol=0))
try:N.noise_field(shape,1.5,beam,4,(2,6),seed,stop=lambda:True)
except N.YieldRequested:stopped=True
else:stopped=False
check('stop_at_channel_boundary',stopped)
# Statistical correlation fixture fixed in NOISE_CONTRACT before running.
a=N.noise_field((64,64,64),1.5,beam,1,(0,63),seed)
def corr(x,y):
 x=x.ravel()-np.mean(x);y=y.ravel()-np.mean(y)
 return float(np.sum(x*y)/np.sqrt(np.sum(x*x)*np.sum(y*y)))
k=B.beam_kernel(64,64,1.5,beam,5);expected_x=float(np.sum(k*np.roll(k,1,axis=1))/np.sum(k*k))
rho_x=corr(a[:, :, :-1],a[:, :, 1:]);rho_v=corr(a[1:-2],a[2:-1])
check('spatial_covariance',abs(rho_x-expected_x)<=.05,dict(measured=rho_x,expected=expected_x))
check('spectral_covariance',abs(rho_v-2/3)<=.05,dict(measured=rho_v,expected=2/3))
mut=np.random.default_rng(np.random.SeedSequence(seed)).standard_normal(a.shape)
mut_x=corr(mut[:,:,:-1],mut[:,:,1:]);mut_v=corr(mut[1:-2],mut[2:-1])
check('uncorrelated_mutation_spatial_bites',abs(mut_x-expected_x)>.05,dict(measured=mut_x,expected=expected_x))
check('uncorrelated_mutation_spectral_bites',abs(mut_v-2/3)>.05,dict(measured=mut_v,expected=2/3))
for wi,weight in enumerate(['NA','R']):
 for fi,foot in enumerate(['canonical','alt']):
  for mi in (0,1):
   prepared=dict(weight=weight,binning=4,native_shape=[9,6,6],native_channel_range=[2,6],pixel=[6.,6.],beam=beam,noise=.00123)
   field,meta=N.prepared_noise(prepared,foot,mi)
   expected_seed=[20261105,46,wi,fi,mi]
   expected,_=N.scale_rms(N.noise_field(shape,1.5,beam,4,(2,6),expected_seed),.00123)
   check('prepared_seed_'+weight+'_'+foot+'_'+str(mi),meta['seed']==expected_seed and np.array_equal(field,expected))
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
 source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in [Path(__file__),Path(N.__file__),R.HERE/'io_beam.py',R.HERE/'NOISE_CONTRACT.md',R.HERE/'FROZEN_CRITERIA.md']},
 versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
 scope='Noise implementation only; full signal mocks and frozen fit-based KA1/KA2 remain separate')
B.atomic(R.HERE/'noise_checks.json',obj);B.atomic(R.HERE/'noise_runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
B.atomic(R.HERE/'mutate/noise_fixture.json',dict(source_hashes=obj['source_hashes'],seed=seed,
    mutation='Uncorrelated standard-normal field replaces spatial beam and spectral Hanning convolution',
    spatial=dict(measured=mut_x,expected=expected_x,tolerance=.05,accepted=abs(mut_x-expected_x)<=.05),
    spectral=dict(measured=mut_v,expected=2/3,tolerance=.05,accepted=abs(mut_v-2/3)<=.05),
    scope='Noise implementation mutation only; physical channel-shuffle fit mutation remains separate'))
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
