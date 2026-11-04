import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from spectrum_v2 import microscopic
import solve as m
HERE=Path(__file__).resolve().parent

def main(path):
 start=time.monotonic();e=float(m.E);x=float(m.X0*m.T);g=math.sqrt(29/200)*e;data=m.build_model(x,e,e,g,vertices=False);z=data['z'];Y=data['Y'];R=data['R'];y=1/math.sqrt(93)
 ev,O=eigh(data['H']);B=O[:,ev>1e-10*max(ev)];UF=data['U'][:,data['mF']>1e-9*max(data['mF'])];rows=[]
 for q in (2e-4,1e-4,5e-5):
  pl=microscopic(z,Y,R,g,1/q,y);mi=microscopic(z,Y,R,g,-1/q,y)
  dH=B.T@(pl['H']-mi['H'])@B/(2*q);dM=UF.T@(pl['MF']-mi['MF'])@UF/(2*q)
  rows.append(dict(q=q,max_field_over_formal_Mp=float(np.linalg.norm(z)*q),scalar_heavy_odd_derivative_norm=float(np.linalg.norm(dH,2)),fermion_heavy_odd_derivative_norm=float(np.linalg.norm(dM,2)),gauge_mixing_odd_derivative_norm=float(np.linalg.norm((pl['MF'][49:,:49]-mi['MF'][49:,:49])/(2*q)))))
 ratios={k:[rows[i][k]/rows[i+1][k] for i in range(2)] for k in ('scalar_heavy_odd_derivative_norm','fermion_heavy_odd_derivative_norm')}
 checks=dict(heavy_subspaces_counts=B.shape[1]==84 and UF.shape[1]==60,odd_heavy_derivative_scales_q_squared=all(abs(r/4-1)<.02 for rr in ratios.values() for r in rr),gauge_mixing_no_q_term=max(r['gauge_mixing_odd_derivative_norm'] for r in rows)==0)
 out=dict(claim_id='CANONICAL_DIRECT_GRAVITY_LOOP_ORDER_CONTROL',checks=checks,cases=rows,halving_ratios=ratios,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite check supporting exact all-field Euler cancellation and rigid-valley Goldstino orthogonality: no direct heavy-spectrum O(1/p) term. Does not include quantum anomaly counterterms or full offshell1PI super-Higgs current.')
 Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
