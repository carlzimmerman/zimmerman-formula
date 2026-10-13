"""Follow-up after the N32 run: double the box at fixed spacing and physical filter length."""
from pathlib import Path
import json
import numpy as np
HERE=Path(__file__).resolve().parent
source=(HERE/'calculate.py').read_text()
results={}; fields={}
for n in (32,64):
    code=source.replace('N=32;box=64.',f'N={n};box={2*n}.').replace("for L in (4,8,16,'local'):","for L in (16,'local'):")
    code='\n'.join("assert out['all_checks_pass']" if line.startswith("(HERE/'run/results.json')") else line for line in code.splitlines())
    code=code.replace("profiles[str(L)]=rad[sel]", "profiles[str(L)]=rad[sel]\n fields_grid[str(L)]=rad.copy()")
    env={'__file__':str(HERE/'calculate.py'),'fields_grid':{}}
    exec(compile(code,str(HERE/'calculate.py'),'exec'),env)
    results[str(n)]=env['out']; fields[n]=env['fields_grid']
    if n==32: mask=env['sel']
checks=[]
for L in ('16','local'):
    a=fields[32][L][mask];b=fields[64][L][16:48,16:48,16:48][mask]
    error=float(np.linalg.norm(a-b)/np.linalg.norm(b))
    checks.append(dict(name='fixed-spacing box doubling '+L,value=error,tolerance=.05,passed=error<=.05))
out={'runs':results,'refinement_checks':checks,'all_checks_pass':all(c['passed'] for c in checks)}
(HERE/'boundary_checked/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2)); assert out['all_checks_pass']
