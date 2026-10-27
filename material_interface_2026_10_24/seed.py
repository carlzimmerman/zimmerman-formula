import json,argparse
from pathlib import Path
import numpy as np
from mixed_carrier import Mixed
from polish import polish
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[]}
 for scale in [4,8]:
  m=Mixed(n=96,domain=12,beta=2,K=10,charge=0);m.ell2=(10/m.rm)**2;v=m.start(scale=scale);v[m.n:]=.01*np.exp(-m.r.numpy()/(4*m.b));assert min(m.cap(v))>0
  r=m.solve_checkpointed(v,dest.with_name(f'prepolish_{scale}.json'),maxiter=1600);v=np.r_[r['mass'],r['v'][m.n:]];r=polish(m,v,dest.with_name(f'checkpoint_{scale}.json'),maxiter=1000);r.update(initial_density_scale_b=scale,initial_phase_amplitude=.01,capacity_model='mixed_carrier');out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['initial_density_scale_b','energy','qinner','law_windows_dex','density_KKT_max','qouter','interpolated_crossings_kpc','optimizer']},flush=True)
