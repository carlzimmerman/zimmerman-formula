"""Dense late-window Floquet response table; prescribed history, not new evolution."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from response_api_v2 import *

def main(out):
    start=time.monotonic()
    early=json.loads((PRIOR/'kinetics/run_leading_two_001/result.json').read_text())['case']
    late=json.loads((PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    packet=json.loads((PRIOR/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    channels=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_basis002/result.json').read_text())['Gamma_by_daughter_pair_CT09_mu']
    omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62)
    f0=np.asarray(early['final_f_S_number_normalization']);f1=np.asarray(late['final_f_S_number_normalization'])
    edges=np.asarray(late['q_edges']);W=(edges[1:]**3-edges[:-1]**3)/3
    number_norm=float(W@f0)/early['history'][-1]['survival']
    rows=[]
    for i,h in enumerate(late['history']):
        frac=(h['N']-late['initial_N'])/(late['final_N']-late['initial_N'])
        f=np.exp((1-frac)*np.log(f0)+frac*np.log(f1))
        f*=h['survival']*number_norm/float(W@f)
        args=dict(xmid=h['x_minimum'],amplitude=(h['x_outer']-h['x_inner'])/2,
                  omega=omega,Tc=h['Tc_over_mu'],edges=edges,f_number=f)
        r=orbit_response(**args,radial=2,angular=12)
        row=dict(N=h['N'],Tc=h['Tc_over_mu'],xmid=args['xmid'],amplitude=args['amplitude'],omega=omega,
                 dynamic_pair_sigma_v=r['dynamic_pair_sigma_v'],stationary_pair_sigma_v=r['stationary_pair_sigma_v'],
                 multiplier=r['multiplier'],parent_density_mu3=r['parent_density_mu3'],
                 event_rate_mu4=r['event_rate_mu4'],one_sign_charged_density_mu3=r['one_sign_charged_density_mu3'],
                 rho_pair=r['rho_pair'],positive_injection_pair=r['positive_injection_pair'],
                 channel_exit_pair_sigma_v={k:float(np.trace(np.asarray(g)@r['rho_pair']).real) for k,g in channels.items()},
                 distribution='recorded endpoint' if i in (0,len(late['history'])-1) else 'endpoint log-shape interpolation normalized to recorded charged number')
        if i in (0,10,20,30,40,50,60,70,79):
            fine=orbit_response(**args,radial=4,angular=24)
            row['fine_dynamic_pair_sigma_v']=fine['dynamic_pair_sigma_v']
            row['fine_multiplier']=fine['multiplier']
            row['radial_angular_relative_difference']=abs(r['dynamic_pair_sigma_v']/fine['dynamic_pair_sigma_v']-1)
        rows.append(row)
    # Only a diagnostic on a prescribed old trajectory: ratio of integrated
    # inverse-yield optical depth, using actual saved old local loss/H.
    # A full history must evaluate kernels on the changed orbit/distribution.
    Ns=np.asarray([r['N'] for r in rows]);ratio=np.asarray([r['multiplier'] for r in rows])
    weight=np.asarray([h['numberloss_over_H']/h['Y_charged'] for h in late['history']])
    static_depth=float(np.trapz(weight,Ns));dynamic_depth=float(np.trapz(weight*ratio,Ns))
    y0=late['history'][0]['Y_charged'];counterfactual=1/(1/y0+dynamic_depth)
    checks=dict(positive=all(r['dynamic_pair_sigma_v']>=0 and r['parent_density_mu3']>=0 for r in rows),
                refinement=all(r.get('radial_angular_relative_difference',0)<.06 for r in rows),
                finite=all(math.isfinite(r['multiplier']) for r in rows))
    result=dict(claim_id='CC10_PRESCRIBED_LATE_MEMORY_TABLE',checks=checks,rows=rows,
                endpoint_distribution_scope='Only endpoint distributions are recorded. Interior shapes are log-interpolated and normalized to saved physical charged number; orbit and action are recorded.',
                prescribed_history_optical_depth_ratio=dynamic_depth/static_depth,
                counterfactual_fixed_history_charged_yield=counterfactual,
                counterfactual_scope='Applies multiplier along the old trajectory only; not a recomputed collision/force/action history and not a physical final abundance.',
                runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('checks','prescribed_history_optical_depth_ratio','counterfactual_fixed_history_charged_yield','runtime_seconds','peak_rss_bytes')}))
    print('range',min(r['multiplier'] for r in rows),max(r['multiplier'] for r in rows))
    assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
