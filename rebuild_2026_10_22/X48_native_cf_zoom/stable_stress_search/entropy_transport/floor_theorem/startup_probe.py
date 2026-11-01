"""Finite startup-compression discriminator; never an all-resolution proof.

The existing physical RHS and cold invariant-subspace integration are unchanged.
Only diagnostic minima on the first ceil(N/4) material cells are added.
"""
import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import refinement
import material


class StartupObserver(refinement.FloorAuditedCollapse):
    def diagnostics(self,t,y):
        result=super().diagnostics(t,y)
        f=self.fields(y)
        count=(self.n+3)//4
        compression=np.maximum(-f['theta'][:count],0)
        result.update(startup_source_cells=count,
            quarter_min_C=float(compression.min()),
            quarter_max_C=float(compression.max()),
            quarter_min_rho=float(f['rho'][:count].min()),
            quarter_min_Qold=float(f['dk_original'][:count].min()),
            quarter_max_K=float(f['K'][:count].max()))
        return result


def run(n,duration,wall_seconds):
    params=material.MaterialParameters(rho_q=1,G=1,a0=np.sqrt(8*np.pi),tau=.5)
    model=StartupObserver(n,params)
    dust_activation=.5907973398405011
    result=refinement.simulate(model,t_end=dust_activation+duration,samples=81,
        rtol=2e-9,atol=1e-11,max_step=.01,wall_seconds=wall_seconds)
    activation=result['cold_phase']['final_time']
    rows=[r for r in result['time_history']
          if r['t']>=activation and 'quarter_min_C' in r]
    trace=[{key:r[key] for key in ('t','quarter_min_C','quarter_max_C',
        'quarter_min_rho','quarter_min_Qold','quarter_max_K','prefix_5pct_min_K')}
        for r in rows]
    for row in trace:row['s']=row['t']-activation
    reference=result['initial']['total']
    return dict(N=n,status=result['status'],t_reached=result['t_reached'],
        activation_time=activation,duration=result['t_reached']-activation,
        elapsed_seconds=result['elapsed_seconds'],rhs_calls=result['rhs_calls'],
        energy_error_reference=result.get('energy_error_reference'),
        accepted_state_energy_error_bound=result['max_relative_energy_error'],
        maximum_sampled_energy_error=max(abs(r['total']/reference-1)
            for r in result['time_history'] if 'total' in r),
        minimum_sampled_quarter_C=min(r['quarter_min_C'] for r in rows),
        sampled_compression_hypothesis_pass=all(r['quarter_min_C']>=4 for r in rows),
        final_core5_min_K=result['final']['prefix_5pct_min_K'],
        invalid_dense_samples=result['invalid_dense_sample_count'],
        accepted_negative_K_rejections=result['accepted_negative_memory_rejections'],
        trace=trace)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shells',type=int,nargs='+',default=[32,64,128,256,512,1024])
    parser.add_argument('--duration',type=float,default=.005)
    parser.add_argument('--wall-seconds',type=float,default=6)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    cases=[run(n,args.duration,args.wall_seconds) for n in args.shells]
    report=dict(assertion_tested='Recorded quarter-prefix compression is >=4 '
        'on the finite sampled startup intervals; physical operator unchanged',
        cases=cases,non_claims=['No bound between diagnostic times',
        'No proof uniform over all N','No continuum existence/convergence theorem'])
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps([{k:c[k] for k in ('N','status','minimum_sampled_quarter_C',
        'final_core5_min_K','elapsed_seconds')} for c in cases]))
    return 0 if all(c['status']=='completed' and c['sampled_compression_hypothesis_pass']
                    for c in cases) else 2


if __name__=='__main__':
    raise SystemExit(main())
