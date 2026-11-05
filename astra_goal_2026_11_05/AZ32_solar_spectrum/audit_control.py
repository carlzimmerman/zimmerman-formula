#!/usr/bin/env python3
"""Independent high-precision negative Rayleigh witnesses for AZ32's control."""
import hashlib
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
os.environ.pop('V3X_MUTATE',None)
import mpmath as mp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=ROOT/'complete_theory_2026_11_04/CT14_Cpp_health/ct14_h3_w4b.py'
env={'__file__':str(source),'__name__':'az32_control_audit'}
exec(compile(source.read_text().split('ND = (12, 16, 24, 32, 48)')[0],
             str(source.relative_to(ROOT))+'[definitions]','exec'),env)
ns=env['ns']; rows=[]
with mp.workdps(60):
    for foot in ('canonical','alt'):
        B=ns['background'](foot); g=B['g']; lam=B['Lam']
        dom=g.r<=lam*(1+1e-12)
        bounds={'lo':float(1+B['vm'][dom].min()),'hi':float((1+B['vm'][dom].max())**2)}
        for nd in (24,32,48):
            rff,rcc=ns['grid_r'](1e-4,lam,nd)
            rf=[mp.mpf(float(x)) for x in rff]; rc=[mp.mpf(float(x)) for x in rcc]
            n=len(rc); vol=[(rf[i+1]**3-rf[i]**3)/3 for i in range(n)]
            d,e=ns['tridiag'](rf,rc,[mp.mpf(1)]*(n+1),[mp.mpf(1)]*n,4,'neumann')
            d=[d[i]/vol[i] for i in range(n)]
            e=[e[i]/mp.sqrt(vol[i]*vol[i+1]) for i in range(n-1)]
            linv=ns['tri_inv'](d,e)
            gamma=mp.mpf(lam)**2/2
            for br,M in bounds.items():
                diagonal=[(mp.mpf(M)-1)*linv[i,i] for i in range(n)]
                i=min(range(n),key=lambda j:diagonal[j])
                main=diagonal[i]+gamma; mutant=diagonal[i]-gamma
                rows.append(dict(footing=foot,nd=nd,l=4,bracket=br,index=i,
                    main_Rayleigh=str(main),mutant_Rayleigh=str(mutant),
                    mutant_over_gamma=str(mutant/gamma),negative_witness=bool(mutant<0)))
result=dict(rows=rows,all_negative=all(r['negative_witness'] for r in rows),digits=60,
    argument='A positive definite implies C=R.T V R has V inertia; a negative diagonal entry of V is a negative Rayleigh witness.',
    scope='discrete control at each frozen fine rung; divergent high-frequency minimum is not a converged finite growth rate',
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    statement='kappa = 1/2 FITTED; not theory closed')
path=HERE/'mutate/control_audit.json'; tmp=path.with_suffix('.tmp')
tmp.write_text(json.dumps(result,indent=2)+'\n'); os.replace(tmp,path)
print(json.dumps(result,indent=2))
sys.exit(0 if result['all_negative'] else 1)
