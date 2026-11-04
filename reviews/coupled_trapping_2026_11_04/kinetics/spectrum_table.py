"""CT09 actual neutral scalar widths, positive grouped interpolation data."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np,json,time,resource
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic'))
from neutral_rates import one

def main(out):
 start=time.monotonic();rows=[]
 for x in np.linspace(0,40,401):
  data=one(float(x),[],{});groups=[]
  for p in data['neutral_scalar_partial_widths']:
   M=p['mass_over_mu'];W=p['width_over_mu']
   match=next((q for q in groups if abs(q[0]-M)<1e-9),None)
   if match is None:groups.append([M,W])
   else:match[1]+=W
  rows.append(dict(x=float(x),parents=groups,charge_error=data['charge_matrix_error']))
 result=dict(claim_id='CT09_SCALAR_RATE_TABLE',cases=rows,checks={'charge_classification':max(q['charge_error'] for q in rows)<1e-10,'positive_widths':all(w>0 for q in rows for m,w in q['parents'])},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Rigid tree neutral-scalar partial widths to actual twelve charged light fermions. Grouped only within equal mass tolerance 1e-9. No irreversible branching claim; width interpolation later is conditional positive endpoint mixture.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(result['checks'].values())
if __name__=='__main__':main(sys.argv[1])
