"""Independent Gaussian convolution check on a nonspherical analytic source.

For solid harmonic H2=r²P2(cos theta), convolving H2 exp(-r²/(2q²))
with a variance-sigma² Gaussian gives beta^(7/2) H2 exp(-r²/(2(q²+sigma²))),
beta=q²/(q²+sigma²). Test sampled interior r<30 at two existing resolutions.
No new astrophysical calculation is performed.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
sys.dont_write_bytecode=True
import numpy as np
import scipy

SOURCE=Path('/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/KT33_reciprocal_filter/mw/mw_reciprocal.py')
before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('review_mw',SOURCE)
mw=importlib.util.module_from_spec(spec); spec.loader.exec_module(mw)
start=time.monotonic()
out=dict(assertion_tested=__doc__,source_file=str(SOURCE),source_sha256_before=before,rows=[])
for refine in (1,2):
    g,_=mw.make_grid(mw.C.A0['canonical'],refine=refine)
    S=mw.Gaussian(g,5,lmax=24,cut=120)
    r,c=g.r2d,np.cos(g.t2d)
    q=6.;s=5.;beta=q*q/(q*q+s*s)
    h=r*r*(3*c*c-1)/2
    f=h*np.exp(-r*r/(2*q*q))
    exact=beta**3.5*h*np.exp(-r*r/(2*(q*q+s*s)))
    actual=S.forward(f)
    region=r<30
    error=float(np.max(np.abs(actual[region]-exact[region]))/np.max(np.abs(exact[region])))
    out['rows'].append(dict(refine=refine,nr=g.Nr,nt=g.Nt,lmax=24,cut=120,sigma=5,q=6,max_absolute_over_exact_peak=error))
out.update(source_sha256_after=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__),wall_seconds=time.monotonic()-start)
Path('/private/tmp/kt33_review/gaussian_l2.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
