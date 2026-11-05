#!/usr/bin/env python3
"""Post-result AZ34 A1: resolve the transition without changing tolerances."""
import hashlib
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import numpy as np
HERE=Path(__file__).resolve().parent
amp=.5;rows=[]
for mode in ('main','mutate'):
    for n in (16,32,64,128):
        values={}
        for q in (16,32):
            xx,ww=np.polynomial.legendre.leggauss(q)
            y=np.arange(n)[:,None]+(xx[None,:]+1)/2
            w=np.broadcast_to(ww[None,:]/2,y.shape)
            u=amp*np.tanh(y)
            base=float(np.sum(w*(-u-np.log1p(-u)-u*u/2)))*2/n
            norm=float(np.sum(w/np.cosh(y)**4))*2*amp*amp*n
            values[str(q)]=dict(energy=base+(norm/2 if mode=='mutate' else 0),norm2=norm)
        exact=2*amp*amp*n*(np.tanh(n)-np.tanh(n)**3/3)
        error=abs(values['32']['norm2']/exact-1)
        change=abs(values['16']['energy']/values['32']['energy']-1)
        rows.append(dict(mode=mode,n=n,values=values,exact_norm2=exact,
                         norm_relative_error=error,energy_pair_change=change,
                         pass_check=bool(error<=1e-8 and change<=1e-6)))
result=dict(label='PASS' if all(r['pass_check'] for r in rows) else 'UNDECIDED',rows=rows,
    amendment='ea24dbeba4 POST-RESULT A1; original failures retained',
    inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            (Path(__file__),HERE/'FROZEN_CRITERIA.md',HERE/'AMENDMENTS.md')},
    statement='kappa = 1/2 FITTED; not theory closed')
p=HERE/'quadrature_diagnostic.json';tmp=p.with_suffix('.tmp')
tmp.write_text(json.dumps(result,indent=2)+'\n');os.replace(tmp,p)
print(json.dumps(result,indent=2));sys.exit(0 if result['label']=='PASS' else 1)
