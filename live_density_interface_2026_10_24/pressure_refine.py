import argparse,json
from pathlib import Path
import numpy as np
from reservoir import Reservoir
from conservative_radius import transfer_species
from joint_recovery import moved

def extended(r):
    rad=np.array(r['r']);ratio=np.array(r['g_total'])/r['g_law'];r['law_windows_dex']={str(hi):float(max(abs(np.log10(ratio[(rad>=1.5)&(rad<=hi)])))) for hi in [15,30,50]};return r

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();old=json.loads(Path(__file__).with_name('run_pressure').joinpath('results.json').read_text())['runs'][0];out=dict(refinement=[],recovery=[])
    for K,domain in [(3,4),(10,8)]:
        m=Reservoir(n=192,domain=domain,beta=20,k=0,tau=0,K=K);v,check=transfer_species(m,old);r=extended(m.solve_scaled(v));r['transfer']=check;out['refinement'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    # Joint displacement of the original K3 candidate after refinement.
    base=out['refinement'][0];m=Reservoir(n=192,domain=4,beta=20,k=0,tau=0,K=3)
    for d in [-1.,1.]:
        v=moved(m,base,d)
        if v is None or min(m.cap(v))<=0:out['recovery'].append(dict(displacement_kpc=d,status='inadmissible perturbation'));continue
        r=extended(m.solve_scaled(v));r.update(displacement_kpc=d,energy_difference=r['energy']-base['energy']);out['recovery'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:[{k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']} for r in rows] for key,rows in out.items()},indent=2))
