import json,argparse
from pathlib import Path
from mixed_carrier import Mixed,transfer_species
from polish import polish
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[]}
 old=json.loads(Path('material_interface_2026_10_24/run_continue/results.json').read_text())['runs'][0]
 for ell,beta,k in [(10,2,0),(3,2,0),(3,2,.003),(3,4,.003),(5,4,.003)]:
  m=Mixed(n=96,domain=12,beta=beta,K=10,charge=k);m.ell2=(ell/m.rm)**2;v,info=transfer_species(m,old);assert min(m.cap(v))>0
  r=polish(m,v,dest.with_name(f'checkpoint_{ell}_{beta}_{k}.json'),maxiter=1600);r.update(capacity_model='mixed_carrier',transfer=info);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['ell_kpc','beta','charge','law_windows_dex','density_KKT_max','qouter','interpolated_crossings_kpc','optimizer']},flush=True)
