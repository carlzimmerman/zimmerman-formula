"""Nonzero-field and guaranteed local-event unit controls; not formation evidence."""
import argparse,json
from pathlib import Path
import numpy as np
from simulate import Simulation

def main():
    out={'seeded_transport':[]}
    for spacing in (1.,.5):
        s=Simulation(6e10,3,n=32,f=.95,spacing=spacing,extent=12)
        medium=np.arange(s.n,2*s.n);ids=medium[np.argsort(np.linalg.norm(s.x[medium],axis=1))[:2]]
        s.state[ids]=True
        E,_,_=s.energy_force(s.x,s.state);s.initialE=E+s.kinetic(s.v);s.norm=max(abs(E),abs(s.initialE))
        row=s.run(duration=.1,dt=.01)
        assert row['status']=='completed',row['reason']
        assert row['max_energy_error']<1e-3
        row['purpose']='Initial T deliberately seeded: integration control, not formation'
        out['seeded_transport'].append(row)
    # Isolated local reaction through the actual production collide() routine.
    s=Simulation(1e8,1,n=16,extent=12)
    s.x[:]=np.arange(32)[:,None]*np.array([3.,0,0]);s.v[:]=0
    s.x[16]=[.05,0,0];s.v[16]=[-20.,0,0]
    E,_,_=s.energy_force(s.x,s.state);s.initialE=E+s.kinetic(s.v);s.norm=max(abs(E),abs(s.initialE))
    # Huge interval is solely to guarantee the Bernoulli test for this one-pair
    # algebraic unit fixture. It is never used in a live integration.
    s.collide(1e10)
    Ef,_,_=s.energy_force(s.x,s.state)
    out['production_collision']={'state_changed':bool(s.state[16]),'energy_error':abs(Ef+s.kinetic(s.v)+s.Q-s.initialE)/s.norm,'stats':s.stats}
    assert s.state[16]
    assert out['production_collision']['energy_error']<1e-12
    assert s.stats['max_encounter_distance_kpc']<.1
    # State toggle and impulse can occur while actual field energy is recomputed.
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
    out=main();Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'seeded_transport':[{k:r[k] for k in ('spacing','status','max_energy_error','max_momentum_error','max_angular_momentum_error','final')} for r in out['seeded_transport']], 'production_collision':out['production_collision']},indent=2))
