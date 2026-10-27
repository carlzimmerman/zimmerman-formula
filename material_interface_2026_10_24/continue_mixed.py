import json,argparse
from pathlib import Path
import numpy as np
from mixed_carrier import Mixed,transfer_species
from polish import polish
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output);out={'runs':[]}
 old=json.loads(Path('material_interface_2026_10_24/run_mixed/checkpoint_10_0.003.json').read_text())
 for K in [10,15,30]:
  m=Mixed(n=96,domain=12,beta=2,K=K,charge=.003);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);assert min(m.cap(v))>0
  r=polish(m,v,dest.with_name(f'checkpoint_{K}.json'),maxiter=1800);r.update(capacity_model='mixed_carrier',transfer=info);out['runs'].append(r);old=r;dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['K','energy','law_windows_dex','density_KKT_max','qouter','interpolated_crossings_kpc','optimizer']},flush=True)
