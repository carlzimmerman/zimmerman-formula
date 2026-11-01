import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,resource
import numpy as np
from gaugino_threshold import build_model,ext_basis,threshold,Z0

def run(path):
    rows=[];checks={}
    for e in [.01,.03]:
        d=build_model(Z0/math.sqrt(31*e),e,e,math.sqrt(29/200)*e,vertices=False)
        ext,C=ext_basis(d);gold=np.r_[d['F'].conj(),np.zeros(24)]
        gold=gold/np.linalg.norm(gold);full=np.column_stack([ext,gold]);out=threshold(d,full)['matrix']
        ph=int(np.where(abs(C)<1e-7)[0][0]);scale=abs(out[ph,ph]);mixed=float(np.max(abs(out[:-1,-1]))/scale)
        rows.append({'e':e,'mixed_relative':mixed,'Goldstino_diagonal_real':float(out[-1,-1].real),
                     'Goldstino_diagonal_imag':float(out[-1,-1].imag),'photino_mass':float(abs(out[ph,ph])),
                     'tree_null_residual':float(np.max(abs(d['MF']@gold)))})
        checks['neutral_mixing_'+str(e)]=mixed<1e-7
    checks={k:bool(v) for k,v in checks.items()};r={'claim_id':'TP04-NEUTRAL-NULLSPACE','checks':checks,'cases':rows,'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    Path(path).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));assert all(checks.values()),checks
if __name__=='__main__':run(sys.argv[1])
