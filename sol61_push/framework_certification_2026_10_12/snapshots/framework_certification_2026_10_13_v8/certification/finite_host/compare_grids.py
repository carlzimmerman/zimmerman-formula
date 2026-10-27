from pathlib import Path
import json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
coarse=json.loads((HERE/'run_N32/results.json').read_text()); fine=json.loads((HERE/'run_N64/results.json').read_text())
a=np.load(HERE/'run_N32/fields.npz');b=np.load(HERE/'run_N64/fields.npz');N=32;dx=2.;x=(np.arange(N)-N/2)*dx;X=np.meshgrid(x,x,x,indexing='ij');r=np.sqrt(sum(v*v for v in X));sel=(r>=4)&(r<=8);center=(N//2,)*3
centered=lambda q:q-q[(slice(None),)+center].reshape(3,1,1,1)
checks=[]
for name in ['satellite','incremental']:
 qa=a['satellite'] if name=='satellite' else a['combined']-a['host'];qb=b['satellite'] if name=='satellite' else b['combined']-b['host'];qb=qb[:,::2,::2,::2]
 qa=centered(qa);qb=centered(qb);error=float(np.linalg.norm((qa-qb)[:,sel])/np.linalg.norm(qb[:,sel]));checks.append({'name':name+' matched-grid fidelity','value':error,'tolerance':.03,'passed':error<=.03})
value=abs(coarse['primary_vector_nonadditivity']-fine['primary_vector_nonadditivity']);checks.append({'name':'primary metric absolute grid difference','value':value,'tolerance':.03,'passed':value<=.03})
passed=all(c['passed'] for c in checks) and coarse['numerical_checks_pass'] and fine['numerical_checks_pass'];fail=coarse['primary_vector_nonadditivity']>.05 and fine['primary_vector_nonadditivity']>.05
verdict=('DECLARED FINITE-HOST EFE-BLINDNESS GATE FAILS' if fail else 'DECLARED FINITE-HOST GATE SURVIVES ONLY') if passed else 'INCONCLUSIVE: NUMERICAL FIDELITY/RESIDUAL GATE FAILED'
inputs=['run_N32/results.json','run_N32/fields.npz','run_N64/results.json','run_N64/fields.npz']
out={'verdict':verdict,'numerical_fidelity_pass':passed,'primary_N32':coarse['primary_vector_nonadditivity'],'primary_N64':fine['primary_vector_nonadditivity'],'primary_threshold':.05,'checks':checks,'input_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in inputs},'scope':'Finite periodic nonlinear candidate and specified host only; not entire framework rejection or Lean/continuum proof.'}
(HERE/'comparison_run/results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
