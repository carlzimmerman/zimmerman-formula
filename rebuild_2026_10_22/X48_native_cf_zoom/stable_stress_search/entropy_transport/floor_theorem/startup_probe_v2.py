"""Resolve the startup observation window with 81 warm diagnostic times.

The historical first probe used the original driver's proportional allocation
and retained just two warm times. This driver uses its unchanged exact cold
phase followed by its unchanged full-law integrator with an explicit grid.
"""
import argparse
import json
from pathlib import Path
import time

import startup_probe as original


def run(n,duration,wall_seconds):
    p=original.material.MaterialParameters(rho_q=1,G=1,
        a0=original.np.sqrt(8*original.np.pi),tau=.5)
    model=original.StartupObserver(n,p)
    started=time.monotonic()
    cold,triggered=original.refinement._cold_phase(model,model.initial_state(),
        t_end=.5907973398405011+duration,samples=2,rtol=2e-9,atol=1e-11,
        wall_seconds=wall_seconds,max_rhs_calls=300000,max_step=.01,
        initial_time=0,max_domain_retries=80,minimum_retry_step=1e-12,started=started)
    if not triggered:
        return dict(N=n,status=cold['status'],phase='cold',trace=[])
    activation=cold['t_reached']
    remaining_wall=wall_seconds-(time.monotonic()-started)
    remaining_calls=300000-cold['rhs_calls']
    if remaining_wall<=0 or remaining_calls<=0:
        return dict(N=n,status='resource_limit',phase='handoff',trace=[])
    warm=original.refinement.convective.simulate(model,
        initial_state=cold['final_state'],initial_time=activation,
        t_end=activation+duration,samples=81,rtol=2e-9,atol=1e-11,
        max_step=.01,wall_seconds=remaining_wall,max_rhs_calls=remaining_calls,
        max_domain_retries=80-len(cold['domain_rejections']),minimum_retry_step=1e-12)
    trace=[]
    for row in warm['time_history']:
        if 'quarter_min_C' not in row:continue
        trace.append({key:row[key] for key in ('t','quarter_min_C','quarter_max_C',
            'quarter_min_rho','quarter_min_Qold','quarter_max_K','prefix_5pct_min_K')})
        trace[-1]['s']=row['t']-activation
    reference=cold['initial']['total']
    accepted_bound=cold['max_relative_energy_error']+warm['max_relative_energy_error']*abs(
        warm['initial']['total']/reference)
    history=cold['time_history']+warm['time_history']
    return dict(N=n,status=warm['status'],phase='warm',activation_time=activation,
        t_reached=warm['t_reached'],duration=warm['t_reached']-activation,
        elapsed_seconds=time.monotonic()-started,
        rhs_calls=cold['rhs_calls']+warm['rhs_calls'],warm_sample_count=len(trace),
        cold_handoff_K_exactly_zero=cold['cold_phase']['handoff_K_exactly_zero'],
        handoff_energy_difference=warm['initial']['total']-cold['final']['total'],
        accepted_state_energy_error_bound=accepted_bound,
        maximum_sampled_energy_error=max(abs(row['total']/reference-1)
            for row in history if 'total' in row),
        minimum_sampled_quarter_C=min(row['quarter_min_C'] for row in trace),
        sampled_compression_hypothesis_pass=all(row['quarter_min_C']>=4 for row in trace),
        final_core5_min_K=warm['final']['prefix_5pct_min_K'],
        invalid_dense_samples=cold['invalid_dense_sample_count']+warm['invalid_dense_sample_count'],
        accepted_negative_K_rejections=warm['accepted_negative_memory_rejections'],trace=trace)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shells',type=int,nargs='+',default=[32,64,128,256,512,1024])
    parser.add_argument('--duration',type=float,default=.005)
    parser.add_argument('--wall-seconds',type=float,default=6)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    cases=[run(n,args.duration,args.wall_seconds) for n in args.shells]
    report=dict(assertion_tested='C>=4 on first ceil(N/4) cells at 81 recorded '
        'warm times for each finite declared N; unchanged physical RHS',cases=cases,
        non_claims=['No between-sample bound','No universal-N theorem',
            'No continuum existence/convergence theorem'])
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps([{k:case.get(k) for k in ('N','status','warm_sample_count',
        'minimum_sampled_quarter_C','final_core5_min_K','elapsed_seconds')} for case in cases]))
    return 0 if all(case['status']=='completed' and case['warm_sample_count']==81
        and case['sampled_compression_hypothesis_pass'] for case in cases) else 2


if __name__=='__main__':
    raise SystemExit(main())
