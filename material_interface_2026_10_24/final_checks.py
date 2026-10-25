import json,argparse
from pathlib import Path
import numpy as np
from mixed_carrier import Mixed,transfer_species
from polish import polish
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[]};old=json.loads(Path('material_interface_2026_10_24/run_final_recovery/base_192.json').read_text())
 for start,n,domain,scale in [('domain',256,64/3,None),('seed',144,12,4),('seed',144,12,8)]:
  m=Mixed(n=n,domain=domain,beta=.5,K=15,charge=0);m.ell2=(10/m.rm)**2
  if start=='domain':v,info=transfer_species(m,old)
  else:
   v=m.start(scale=scale);v[n:]=.01*np.exp(-m.r.numpy()/(4*m.b));info={'density_scale_b':scale,'phase_amplitude':.01};assert min(m.cap(v))>0
   pre=m.solve_checkpointed(v,dest.with_name(f'prepolish_seed_{scale}.json'),maxiter=1800);v=np.r_[pre['mass'],pre['v'][n:]]
  r=polish(m,v,dest.with_name(f'checkpoint_{start}_{scale}.json'),maxiter=1600);r.update(stage=start,initialization=info,capacity_model='mixed_carrier');out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['stage','n','energy','qinner','law_windows_dex','density_KKT_max','qouter','edge_mass_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
