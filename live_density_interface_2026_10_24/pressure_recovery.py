import argparse,json
from pathlib import Path
from checkpoint_solver import Checkpoint
from conservative_radius import transfer_species
from pressure_refine import extended
from joint_recovery import moved

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();outpath=Path(a.output);old=json.loads(Path(__file__).with_name('run_pressure').joinpath('results.json').read_text())['runs'][0];out=dict(refinement=[],recovery=[])
    m=Checkpoint(n=128,domain=4,beta=20,k=0,tau=0,K=3);v,check=transfer_species(m,old);base=extended(m.solve_checkpointed(v,outpath.with_name('refine_checkpoint.json')));base['transfer']=check;out['refinement'].append(base);outpath.write_text(json.dumps(out,indent=2)+'\n')
    for d in [-1.,1.]:
        v=moved(m,base,d);assert v is not None and min(m.cap(v))>0
        r=extended(m.solve_checkpointed(v,outpath.with_name('recovery_'+str(d)+'_checkpoint.json')));r.update(displacement_kpc=d,energy_difference=r['energy']-base['energy']);out['recovery'].append(r);outpath.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:[{key:val for key,val in r.items() if key not in ['v','r','mass','q','g_total','g_law']} for r in rows] for k,rows in out.items()},indent=2))
