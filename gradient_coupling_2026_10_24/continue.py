import argparse,json
from pathlib import Path
import numpy as np
from coupled_model import Coupled,solve,transfer_species
from joint_recovery import moved

def support(r):
 rad=np.array(r['r']);mass=np.array(r['mass']);edges=[0.]
 for rr in rad:edges.append(2*rr-edges[-1])
 rho=mass/(np.diff(np.array(edges)**3)/3);R=r['interpolated_crossings_kpc'][-1] if r['interpolated_crossings_kpc'] else 0;sel=(rad>15)&(rad<R);v=rho[sel];rebound=float(max(v/np.minimum.accumulate(v))) if len(v) else 1e99
 return dict(density_rebound_factor=rebound,eligible=bool(R>15 and rebound<10 and r['min_transition_cell_mass']>1e-6 and r['explicit_exterior_mass']>.1 and r['explicit_exterior_T_fraction']<.05))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);rows=json.loads(Path('gradient_coupling_2026_10_24/run_checked/results.json').read_text())['runs'];rank=[(not support(r)['eligible'],r['law_endpoint_error_dex'],i) for i,r in enumerate(rows)];index=min(rank)[2];old=rows[index];out={'selected_index':index,'screen_support':[support(r) for r in rows],'runs':[]}
 for n in [96,144]:
  m=Coupled(n=n,domain=12,beta=2,K=30,charge=0,L=old['density_stiffness_length_kpc'],eta=old['eta']);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);base=solve(m,v,dest.with_name(f'base_{n}.json'),maxiter=1800);base.update(stage='base',support=support(base));out['runs'].append(base);dest.write_text(json.dumps(out,indent=2)+'\n');print('BASE',n,{k:base[k] for k in ['eta','density_stiffness_length_kpc','law_endpoint_error_dex','density_KKT_max','support','interpolated_crossings_kpc']},flush=True)
  for d in [-1.,1.]:
   v=moved(m,base,d)
   if v is None or min(m.cap(v))<=0:out.setdefault('failures',[]).append(dict(n=n,displacement=d,reason='infeasible remapping'));continue
   r=solve(m,v,dest.with_name(f'recover_{n}_{d}.json'),maxiter=1800);r.update(stage='recovery',displacement_kpc=d,energy_difference=r['energy']-base['energy'],front_change_kpc=(r['interpolated_crossings_kpc'][-1]-base['interpolated_crossings_kpc'][-1]) if r['interpolated_crossings_kpc'] else None,support=support(r));out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print('RECOVER',n,d,{k:r[k] for k in ['front_change_kpc','energy_difference','law_endpoint_error_dex','density_KKT_max','support']},flush=True)
  old=base
