#!/usr/bin/env python3
"""Known crop/bin answers and independent FITS access; no mask/fit claims."""
import hashlib,json,tempfile,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
import raw_cube as R
import io_beam as B
HERE=Path(__file__).resolve().parent;checks=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
with tempfile.TemporaryDirectory(prefix='az46_raw_') as d:
    p=Path(d)/'fixture.fits';a=np.random.default_rng(46).normal(size=(2,80,80)).astype('f4');a[0,10,10]=np.nan;a[0,11,11]=np.inf
    fits.PrimaryHDU(a).writeto(p);header,offset=B.metadata(p)
    for plane,binning,chunk in __import__('itertools').product([0,1],[2,4,8],[32,64]):
        got,bad=R.read_plane(p,header,offset,plane,3,5,64,binning,chunk)
        sub=a[plane,5:69,3:67].astype('f8');sub[~np.isfinite(sub)]=0
        expected=sub.reshape(64//binning,binning,64//binning,binning).mean(axis=(1,3)).astype('f4')
        check(f'fixture_p{plane}_b{binning}_rows{chunk}',np.array_equal(got,expected) and bad==(2 if plane==0 else 0))
    try:R.read_plane(p,header,offset,0,3,5,64,8,32,lambda:True);stopped=False
    except R.YieldRequested:stopped=True
    check('row_safe_point_stop',stopped)
old=R.ROOT/'finish_2026_11_04/FN4_galaxy_rows_data/FN4a_ic1613_cube_model/fn4a_s0.json'
crop=json.loads(old.read_text())['crop'];p=R.DATA/'IC1613_NA_ICL001.FITS';header,offset=B.metadata(p)
x,y=crop['x_lo'],crop['y_lo'];got,bad=R.read_plane(p,header,offset,0,x,y,1200,8,32)
with fits.open(p,memmap=True,lazy_load_hdus=True) as f:raw=np.asarray(f[0].section[0,0,y:y+1200,x:x+1200],dtype='f8')
raw[~np.isfinite(raw)]=0;expected=raw.reshape(150,8,150,8).mean(axis=(1,3)).astype('f4')
check('real_plane_independent_astropy',np.array_equal(got,expected),float(np.max(abs(got-expected))))
for weight in ['NA','R']:
    h,_=B.metadata(R.DATA/f'IC1613_{weight}_ICL001.FITS')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',R.FITSFixedWarning);w=R.WCS(h)
    velocity,linear=R.velocity_axis(h,w)
    delta=(np.arange(h['NAXIS3'])+1-h['CRPIX3'])*h['CDELT3'];v0=h['CRVAL3']
    analytic=(v0+delta/(1-delta/(299792458.+v0)))/1000
    difference=float(np.max(abs(velocity-analytic)))
    check(weight+'_spectral_optical_mapping',difference<=1e-9,dict(max_analytic_difference_kms=difference,max_old_linear_difference_kms=float(np.max(abs(velocity-linear)))))
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(R.__file__),Path(B.__file__),HERE/'FROZEN_CRITERIA.md',HERE/'AMENDMENTS.md']},scope='Raw cube preparation controls only; kappa=1/2 FITTED; not theory closed')
B.atomic(HERE/'raw_checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
