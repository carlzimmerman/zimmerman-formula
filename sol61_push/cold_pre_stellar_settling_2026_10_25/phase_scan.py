import argparse,json,resource
from pathlib import Path
import numpy as np
from kernel_pade9 import Solver
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists();s=Solver(8,eta=.3,alpha=3,strength=0);rows=[]
for x in [0,1,2,4,8,16,32,64,1000,1e6]:
 z=-1j*x;r=np.prod((1+s.factors*z)/(1-s.factors*z));rows.append(dict(argument=x,unitarity_error=float(abs(abs(r)-1)),complex_phase_error=float(abs(r-np.exp(z)))))
assert max(r['unitarity_error'] for r in rows)<1e-10 and next(r['complex_phase_error'] for r in rows if r['argument']==4)<1e-8
(out/'result.json').write_text(json.dumps(dict(scope='finite scalar phase coverage, not a bound on occupied galaxy spectra',degree=s.degree,rows=rows,factors_real=s.factors.real.tolist(),factors_imag=s.factors.imag.tolist(),peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2));print(json.dumps(rows))
