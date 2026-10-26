"""Same inner R matrix, independent propagation radii; no nuclear loss."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from run_point import replace
from kmat import read_k
p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--bin',required=True);p.add_argument('--output',required=True);a=p.parse_args()
w=Path(a.work).resolve();rows=[];inp=(w/'scattering.rsolve.inp').read_text()
for radius in [20.,40.,80.,160.]:
    text=replace(inp,'raf',str(radius))
    if 'nrange' in text:text=replace(text,'nrange',str(max(0,int(radius-20))))
    else:text=text.replace('&bprop', '&bprop\n nrange = '+str(max(0,int(radius-20)))+',')
    with (w/f'outer_{radius}.out').open('w') as f:
        subprocess.run([str(Path(a.bin).resolve()/'rsolve')],input=text,text=True,cwd=w,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=60)
    rows.append(dict(radius=radius,data=read_k(w/'fort.19')))
Path(a.output).write_text(json.dumps(dict(rows=rows),indent=2)+'\n')
print([(r['radius'],r['data'][0]['eigenphase_sum']) for r in rows])
