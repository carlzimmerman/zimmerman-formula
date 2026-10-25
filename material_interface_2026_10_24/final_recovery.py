import json,argparse
from pathlib import Path
import numpy as np
from mixed_carrier import Mixed,transfer_species
from polish import polish
from joint_recovery import moved
from joint import outer

def model(r,n=None,domain=None):
 m=Mixed(n=n or r['n'],domain=domain or 12,beta=r['beta'],K=r['K'],charge=r['charge'],rhos=r['rhos']);m.ell2=(r['ell_kpc']/m.rm)**2;return m
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--index',type=int,required=True);ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);base=json.loads(Path(a.input).read_text())['runs'][a.index];out={'source_index':a.index,'runs':[]}
 for n in [144,192]:
  m=model(base,n);v,info=transfer_species(m,base);assert min(m.cap(v))>0
  r=polish(m,v,dest.with_name(f'base_{n}.json'),maxiter=1400);r.update(stage='base',capacity_model='mixed_carrier',transfer=info);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');base=r
  print('BASE',n,{k:r[k] for k in ['law_windows_dex','density_KKT_max','interpolated_crossings_kpc','optimizer']},flush=True)
  for d in [-1.,1.]:
   v=moved(m,base,d);assert v is not None and min(m.cap(v))>0
   initial_E=m.direct(v)[0];rr=polish(m,v,dest.with_name(f'recovery_{n}_{d}.json'),maxiter=1400);rr.update(stage='recovery',displacement_kpc=d,initial_energy_difference=initial_E-base['energy'],energy_difference=rr['energy']-base['energy'],front_change_kpc=rr['interpolated_crossings_kpc'][-1]-base['interpolated_crossings_kpc'][-1],capacity_model='mixed_carrier');out['runs'].append(rr);dest.write_text(json.dumps(out,indent=2)+'\n');print('RECOVERY',n,d,{k:rr[k] for k in ['front_change_kpc','energy_difference','density_KKT_max','optimizer']},flush=True)
