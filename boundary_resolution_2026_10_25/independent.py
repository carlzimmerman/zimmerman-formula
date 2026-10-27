import argparse,json
from pathlib import Path
from compact import Compact
from surface_checked import solve,transfer_species
from joint_recovery import moved
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);base=json.loads(Path('boundary_resolution_2026_10_25/run_verify/recover_0.5_-1.0.json').read_text());out={'runs':[]}
for h in [.5,.25]:
 m=Compact(domain=12,beta=2,K=30,charge=0,L=1,eta=0,sigma=.003,eps=.3,h=h);m.ell2=(3/m.rm)**2;v,info=transfer_species(m,base);r=solve(m,v,dest.with_name(f'base_{h}.json'),maxiter=2000);r.update(stage='base',transfer=info);base=r;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print('BASE',{k:r[k] for k in ['fine_spacing_kpc','n','law_endpoint_error_dex','density_KKT_max','density_rebound_full','mass_outside50','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
 for d in [-1.,1.]:
  v=moved(m,base,d);assert v is not None and min(m.cap(v))>0
  rr=solve(m,v,dest.with_name(f'recover_{h}_{d}.json'),maxiter=2000);rr.update(stage='recovery',displacement_kpc=d,energy_difference=rr['energy']-base['energy'],front_change_kpc=rr['interpolated_crossings_kpc'][-1]-base['interpolated_crossings_kpc'][-1]);out['runs'].append(rr);dest.write_text(json.dumps(out,indent=2)+'\n');print('RECOVER',h,d,{k:rr[k] for k in ['front_change_kpc','energy_difference','law_endpoint_error_dex','density_KKT_max','density_rebound_full','optimizer']},flush=True)
