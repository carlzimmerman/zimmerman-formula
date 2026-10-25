import json,argparse
from pathlib import Path
from carrier_checked import Carrier,transfer_species
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output);out={'runs':[]}
 old=json.loads(Path('material_interface_2026_10_24/run_checked/results.json').read_text())['runs'][3]
 for ell,beta,k in [(3,0,.003),(3,0,.03),(3,2,.003),(3,2,.03),(10,0,.003),(10,0,.03),(10,2,.003),(10,2,.03)]:
  m=Carrier(n=64,domain=4,beta=beta,K=3,charge=k);m.ell2=(ell/m.rm)**2;v,info=transfer_species(m,old);assert min(m.cap(v))>0
  r=m.solve_checkpointed(v,dest.with_name(f'checkpoint_{ell}_{beta}_{k}.json'),maxiter=1500);r.update(ell_kpc=ell,transfer=info);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({a:r[a] for a in ['ell_kpc','beta','charge','gap_mass','law_windows_dex','qouter','density_KKT_max','interpolated_crossings_kpc','optimizer']},flush=True)
