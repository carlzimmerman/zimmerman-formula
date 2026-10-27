"""LD-10: refine low-tension mobile candidate and perturb matter with phase."""
import argparse,json
from pathlib import Path
import numpy as np
from reservoir import Reservoir
from conservative_radius import transfer_species
from joint import RESERVOIR

def moved(m,r,displacement):
    rad=np.array(r['r']);edges=[0.]
    for rr in rad:edges.append(2*rr-edges[-1])
    edges=np.array(edges);R=r['crossings_kpc'][-1];width=.25*R
    shape=edges/R*np.exp(-((edges-R)/width)**2);shifted=edges+displacement*shape
    if min(np.diff(shifted))<=0:return None
    mm=np.array(r['mass']);q=np.array(r['q']);parts=[]
    for frac in [q,1-q]:parts.append(np.maximum(np.diff(np.interp(edges**3,shifted**3,np.r_[0,np.cumsum(mm*frac)])),0))
    mass=parts[0]+parts[1];qq=np.divide(parts[0],mass,out=np.zeros_like(mass),where=mass>1e-14);mass=np.maximum(mass,1e-12);mass*=RESERVOIR/sum(mass)
    return np.r_[mass,2/np.pi*np.arcsin(np.sqrt(np.clip(qq,0,1)))]

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();old=json.loads(Path(__file__).with_name('run_conservative_radius').joinpath('results.json').read_text())['runs'][0];out=dict(refinement=[],recovery=[])
    m=Reservoir(n=256,domain=4,beta=1000,k=120,tau=.1,K=3);v,check=transfer_species(m,old);base=m.solve_scaled(v);base['transfer']=check;out['refinement'].append(base);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    for sign in [-1,1]:
        chosen=None
        for amplitude in [1.,.5,.2,.1,.05]:
            d=sign*amplitude;v=moved(m,base,d)
            if v is not None and min(m.cap(v))>1e-4:chosen=(v,d);break
        if chosen is None:out['recovery'].append(dict(sign=sign,status='no_admissible_test_perturbation'));continue
        v,d=chosen;r=m.solve_scaled(v);r.update(displacement_kpc=d,energy_difference=r['energy']-base['energy'],reference_front_kpc=base['crossings_kpc'][-1] if base['crossings_kpc'] else None);out['recovery'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:[{k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']} for r in rows] for key,rows in out.items()},indent=2))
