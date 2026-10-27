import json,argparse
from pathlib import Path
from carrier_checked import Carrier,transfer_species
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output);out={'runs':[]}
 old=json.loads(Path('material_interface_2026_10_24/run_thickness/results.json').read_text())['runs'][6]
 for K in [10,30]:
  m=Carrier(n=128,domain=16,beta=2,K=K,charge=.003);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);assert min(m.cap(v))>0
  r=m.solve_checkpointed(v,dest.with_name(f'checkpoint_{K}.json'),maxiter=1800);r.update(ell_kpc=10,transfer=info);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({a:r[a] for a in ['K','gap_mass','law_windows_dex','qouter','outer_mass','edge_mass_fraction','density_KKT_max','interpolated_crossings_kpc','optimizer']},flush=True)
