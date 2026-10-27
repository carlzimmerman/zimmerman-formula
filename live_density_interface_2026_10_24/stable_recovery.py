import argparse,json
from pathlib import Path
import numpy as np
from stable_compatible import Stable
from conservative_radius import transfer_species
from pressure_refine import extended
from joint_recovery import moved

def cross(r):
    rad=np.array(r['r']);q=np.array(r['q']);ids=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0]
    r['interpolated_crossings_kpc']=[float(rad[i]+(.5-q[i])*(rad[i+1]-rad[i])/(q[i+1]-q[i])) for i in ids];return r

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path(__file__).with_name('run_stable').joinpath('results.json').read_text())['joint'][0];out=dict(refinement=[],recovery=[])
    m=Stable(n=128,domain=4,beta=20,k=0,tau=0,K=3);v,info=transfer_species(m,old);base=cross(extended(m.solve_checkpointed(v,dest.with_name('refine_checkpoint.json'),maxiter=1500)));base['transfer']=info;out['refinement'].append(base);dest.write_text(json.dumps(out,indent=2)+'\n')
    for d in [-1.,1.]:
        v=moved(m,base,d);assert v is not None and min(m.cap(v))>0
        r=cross(extended(m.solve_checkpointed(v,dest.with_name('recovery_'+str(d)+'_checkpoint.json'),maxiter=1500)));r.update(displacement_kpc=d,energy_difference=r['energy']-base['energy'],front_change_kpc=r['interpolated_crossings_kpc'][-1]-base['interpolated_crossings_kpc'][-1]);out['recovery'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:[{k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']} for r in rows] for key,rows in out.items()},indent=2))
