#!/usr/bin/env python3
"""Preparation known answers, independent weighting, live interruption and replay."""
import argparse,json,signal,subprocess,sys,tempfile,time
from pathlib import Path
import numpy as np
from astropy.io import fits
import prepare as P
import raw_cube as R
import io_beam as B
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='prepare_verified');a=ap.parse_args();base=R.HERE/a.tag
if base.exists():raise RuntimeError('Use a fresh tag')
base.mkdir();checks=[]
def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
with tempfile.TemporaryDirectory(prefix='az46_map_') as d:
    path=Path(d)/'map.fits';image=np.arange(6400,dtype='f4').reshape(80,80);image[10,10]=np.nan
    h=fits.Header({k:v for k,v in zip(['CRPIX1','CRPIX2','CRVAL1','CRVAL2','CDELT1','CDELT2'],[40.,40.,16.,2.,-.001,.001])});fits.PrimaryHDU(image,header=h).writeto(path)
    hd,_=B.metadata(path);crop=dict(xlo=3,ylo=5,size=64);got,_=P.crop_map(path,crop,8,hd)
    expected=np.array([[np.nanmean(image[5+iy*8:5+(iy+1)*8,3+ix*8:3+(ix+1)*8].astype('f8')) for ix in range(8)] for iy in range(8)])
    check('map_mean_independent_blocks',np.array_equal(got,expected))
    wrong=hd.copy();wrong['CRVAL1']+=.01
    try:P.crop_map(path,crop,8,wrong);rejected=False
    except ValueError:rejected=True
    check('map_grid_mismatch_rejected',rejected)
r,c=P.geometry(np.array([10.,0.]),np.array([0.,10.]),90.,60.)
check('disc_geometry_known_axes',np.allclose(r,[10.,20.],atol=1e-12,rtol=0) and np.allclose(c,[1.,0.],atol=1e-12,rtol=0))
def command(tag,weight='NA',extra=()):return [sys.executable,'-W','error',str(R.HERE/'prepare.py'),'--raw',f'raw_verified/baseline/{weight}_bin8_rows32','--tag',tag,*extra]
def run(tag,weight='NA',extra=()):
    with (base/(tag.split('/')[-1]+'_'+weight+'.log')).open('a') as log:return subprocess.run(command(tag,weight,extra),stdout=log,stderr=subprocess.STDOUT,timeout=120).returncode
def directory(tag,weight='NA'):return R.HERE/tag/f'{weight}_bin8'
for weight in ['NA','R']:check(weight+'_pilot_complete',run(a.tag+'/baseline',weight)==0)
na=directory(a.tag+'/baseline');rob=directory(a.tag+'/baseline','R')
check('common_gas_map_byte_identical',(na/'maps_gas_sky.npy').read_bytes()==(rob/'maps_gas_sky.npy').read_bytes())
m0=json.loads((na/'mask.json').read_text())['scientific'];m1=json.loads((rob/'mask.json').read_text())['scientific']
check('weighting_specific_noise',m0['noise_Jy_per_beam']!=m1['noise_Jy_per_beam'],[m0['noise_Jy_per_beam'],m1['noise_Jy_per_beam']])
check('weighting_specific_beam',m0['beam_arcsec_deg']!=m1['beam_arcsec_deg'])
check('weighting_specific_mask',(na/'mask_mask.npy').read_bytes()!=(rob/'mask_mask.npy').read_bytes())
tag=a.tag+'/interrupted';out=directory(tag);sent=False
with (base/'interrupt.log').open('w') as log:
    child=subprocess.Popen(command(tag),stdout=log,stderr=subprocess.STDOUT);deadline=time.monotonic()+60
    while child.poll() is None and time.monotonic()<deadline:
        if (out/'mask.json').exists() and not (out/'prep_manifest.json').exists() and child.poll() is None:
            child.send_signal(signal.SIGTERM);sent=True;break
        time.sleep(.005)
    code=child.wait(timeout=60)
check('live_preparation_SIGTERM_exit75',sent and code==75,code)
check('resume_completes',run(tag,extra=['--resume'])==0)
check('resume_manifest_byte_identical',(na/'prep_manifest.json').read_bytes()==(out/'prep_manifest.json').read_bytes())
for name in ['mask','maps','stars','rings']:check('resume_'+name+'_byte_identical',(na/(name+'.json')).read_bytes()==(out/(name+'.json')).read_bytes())
check('complete_resume_idempotent',run(tag,extra=['--resume'])==0)
check('fresh_repeat_complete',run(a.tag+'/repeat')==0)
repeat=directory(a.tag+'/repeat')
check('fresh_repeat_manifest_byte_identical',(na/'prep_manifest.json').read_bytes()==(repeat/'prep_manifest.json').read_bytes())
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={p.name:R.sha(p) for p in [Path(__file__),Path(P.__file__),R.HERE/'masking.py',R.HERE/'stars.py',R.HERE/'FROZEN_CRITERIA.md',R.HERE/'AMENDMENTS.md']},scope='8x8 preparation only; no production cube fit or physical acceptance; kappa=1/2 FITTED; not theory closed')
B.atomic(R.HERE/'prepare_checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
