"""Independent controls and resolution comparison for the accepted NR crossing."""
import json
from pathlib import Path
import sys
import numpy as np
from compression_entry import Model

def energy(model,state,P):
    n,v=np.split(state,2);Pi=model.D@P
    pp=np.maximum(Pi,0);S=np.exp(-pp**3);p=abs(P)
    W=-p-np.log1p(-p)
    return float(np.mean(.5*n*v*v+(n-Pi)**2/(4*model.C*S)+model.gamma*pp**2/2+W+.5*n*model.phi(n)))

def main(output):
    base=Path(__file__).parent; rows=[];sets={}
    for name in ['compression256','compression512','compression512half']:
        record=json.loads((base/name/'results.json').read_text())
        a=np.load(base/name/'results.npz');m=Model(record['N'])
        m.constraint(a['initial_state'][:m.N]);e0=energy(m,a['initial_state'],m.P)
        e1=energy(m,a['final_state'],a['final_P'])
        sets[name]=a
        assert record['event']=='negative_highk_charge_coefficient'
        assert record['initial']['max_D_all']<=0 and record['last']['max_D_all']>0
        assert record['last']['min_n']>0 and record['last']['min_ePP']>0
        rows.append({'name':name,'initial_energy':e0,'final_energy':e1,
                     'relative_energy_change':abs(e1-e0)/abs(e0),'event_bracket':record['event_bracket']})
    n256,v256=np.split(sets['compression256']['final_state'],2)
    n512,v512=np.split(sets['compression512']['final_state'],2)
    n512h,v512h=np.split(sets['compression512half']['final_state'],2)
    convergence={'spatial_n_max':float(max(abs(n256-n512[::2]))),
                 'spatial_v_max':float(max(abs(v256-v512[::2]))),
                 'time_n_max':float(max(abs(n512-n512h))),
                 'time_v_max':float(max(abs(v512-v512h)))}
    controls=[]
    for label,factor in [('zero_initial_velocity',0),('reversed_velocity',-1)]:
        m=Model(256);y=m.near_transition();y[m.N:]*=factor
        start=m.inspect(y);dt=1e-5
        for i in range(174):
            a=m.rhs(y);b=m.rhs(y+dt*a/2);c=m.rhs(y+dt*b/2);d=m.rhs(y+dt*c)
            y+=dt*(a+2*b+2*c+d)/6
        end=m.inspect(y)
        assert not end['negative_highk_charge_coefficient_reached']
        assert end['min_n']>0
        controls.append({'label':label,'initial':start,'final':end})
    result={'scope':'Finite NR discretization controls; no continuum or GR evolution theorem',
            'crossing_runs':rows,'convergence':convergence,'controls':controls}
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'convergence':convergence,'controls_passed':len(controls)},indent=2))

if __name__=='__main__':main(sys.argv[1])
