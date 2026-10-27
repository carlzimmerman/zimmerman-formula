import json,argparse
from pathlib import Path
from mixed_carrier import Mixed,transfer_species
from polish import polish
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[]};old=json.loads(Path('material_interface_2026_10_24/run_recovery/results.json').read_text())['runs'][3]
 for beta,K in [(0,15),(.5,15),(1,15),(.5,30)]:
  m=Mixed(n=144,domain=12,beta=beta,K=K,charge=0);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);r=polish(m,v,dest.with_name(f'checkpoint_{beta}_{K}.json'),maxiter=1400);r.update(capacity_model='mixed_carrier',transfer=info);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['beta','K','qinner','law_windows_dex','density_KKT_max','qouter','interpolated_crossings_kpc','optimizer']},flush=True)
