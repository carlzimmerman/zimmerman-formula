"""Explicit collision-operator choice around the frozen resolution driver.

The native Bernoulli-pair operator remains an independent time-discretization
control. The optional thinning operator samples the same fixed-position
central-pair Markov generator in continuous collision time. Neither applies
negative collision time in the Hamiltonian composition.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import run_resolution as core


def main(args):
    totals=dict(proposals=0,events=0)
    precision_checks=[]
    if args.backend=='metal':
        import metal_gravity
        original=metal_gravity.gravity
        calls=[0]
        def checked_gravity(x,m,eps):
            answer=original(x,m,eps);calls[0]+=1
            if calls[0] in (1,2,100,1000,6000,30000,60000,120000,240000):
                ref=core.cpu_gravity(x,m,eps,threads=args.threads)
                force_error=float(np.linalg.norm(answer[0]-ref[0])/max(np.linalg.norm(ref[0]),1e-300))
                phi_error=float(np.linalg.norm(answer[2]-ref[2])/max(np.linalg.norm(ref[2]),1e-300))
                energy_error=abs(answer[1]-ref[1])/max(abs(ref[1]),1e-300)
                row=dict(gravity_call=calls[0],N=len(m),force_relative_L2=force_error,phi_relative_L2=phi_error,potential_energy_relative=energy_error)
                precision_checks.append(row)
                if max(force_error,phi_error,energy_error)>1e-11:
                    raise RuntimeError('Evolved-state GPU/CPU precision gate failed: '+str(row))
            return answer
        metal_gravity.gravity=checked_gravity
    if args.collision_method=='ctmc' and not args.collisionless:
        from null_scatter import scatter as sample
        def wrapped(*pos,**kw):
            result=sample(*pos,**kw)
            totals['proposals']+=result.get('proposals',0)
            totals['events']+=result['n']
            return result
        core.scatter=wrapped
    core.simulate(args)
    p=Path(args.output)/'results.json';result=json.loads(p.read_text())
    if args.backend=='metal':result['backend']=metal_gravity.backend_metadata()
    result['evolved_state_precision_checks']=precision_checks
    result['collision_method']=args.collision_method
    result['null_sampler_totals']=totals
    result['collision_method_convention']='frozen-position central elastic CTMC' if args.collision_method=='ctmc' else 'sequential central-pair Bernoulli first-order time approximation'
    p.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--ncold',type=int,default=8192);p.add_argument('--seed',type=int,default=87319)
    p.add_argument('--collision-seed',type=int);p.add_argument('--eps',type=float,default=10.)
    p.add_argument('--h',type=float,default=25.);p.add_argument('--dt',type=float,default=.5)
    p.add_argument('--duration',type=float,default=10000.);p.add_argument('--record-interval',type=float,default=10.)
    p.add_argument('--host',action='store_true');p.add_argument('--collisionless',action='store_true')
    p.add_argument('--threads',type=int,default=4);p.add_argument('--backend',choices=('cpu','metal'),default='metal')
    p.add_argument('--collision-method',choices=('bernoulli','ctmc'),default='ctmc')
    main(p.parse_args())
