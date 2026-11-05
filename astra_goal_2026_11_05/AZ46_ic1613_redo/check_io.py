#!/usr/bin/env python3
"""Independent raw-reader anchors; parser checks are not observational gates."""
import hashlib,json,math
from pathlib import Path
import numpy as np
from astropy.io import fits
import io_beam as B
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
p=ROOT.parent/'_external_data/fn4a_ic1613_2026_11/IC1613_NA_X0_P_R.FITS'
hd,offset=B.metadata(p);beam=B.clean_beam(hd);checks=[];results=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
for chunk in [32,64]:
    positive=np.longdouble(0);signed=np.longdouble(0);count=0;sample=None
    for lo,a in B.rows(p,hd,offset,row_chunk=chunk):
        good=a[np.isfinite(a)].astype(np.longdouble);positive+=np.maximum(good,0).sum();signed+=good.sum();count+=len(good)
        if lo<=900 and 905<=lo+len(a):sample=a[900-lo:905-lo,900:905].copy()
    results.append(dict(row_chunk=chunk,positive_sum=float(positive),signed_sum=float(signed),finite_pixels=count))
    with fits.open(p,memmap=True,lazy_load_hdus=True) as f:expected=np.array(f[0].section[0,0,900:905,900:905],dtype='f8').squeeze()
    check(f'astropy_section_{chunk}',sample is not None and np.array_equal(sample,expected,equal_nan=True))
check('row_chunk_pair',all(math.isclose(results[0][k],results[1][k],rel_tol=1e-10,abs_tol=0) for k in ['positive_sum','signed_sum']) and results[0]['finite_pixels']==results[1]['finite_pixels'])
beam_pixels=1.1331*beam[0]*beam[1]/(abs(hd['CDELT1']*hd['CDELT2'])*3600**2)
flux=results[0]['positive_sum']/1000/beam_pixels
check('original_rounded_flux_parser_anchor',abs(flux/262.8614460793164-1)<=1e-8,flux)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),raw_sums=results,
         header_sha256=hashlib.sha256(hd.tostring().encode()).hexdigest(),source_hashes={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),Path(B.__file__),HERE/'FROZEN_CRITERIA.md']},
         scope='Raw parser checks only; not an observational flux pass; kappa=1/2 FITTED; not theory closed')
B.atomic(HERE/'io_checks.json',obj);print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
