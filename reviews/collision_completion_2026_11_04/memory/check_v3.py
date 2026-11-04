"""Fresh occupation-independent kernel and charged-width perturbation controls."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import time,resource,json,math
from pathlib import Path
import numpy as np
from response_api_v3 import *

def main(out):
    start=time.monotonic();early=json.loads((PRIOR/'kinetics/run_leading_two_001/result.json').read_text())['case']
    late=json.loads((PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    packet=json.loads((PRIOR/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    channels=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_basis002/result.json').read_text())['Gamma_by_daughter_pair_CT09_mu']
    omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62);rows=[]
    for index in (0,40,79):
        h=late['history'][index];frac=(h['N']-late['initial_N'])/(late['final_N']-late['initial_N'])
        f=np.exp((1-frac)*np.log(early['final_f_S_number_normalization'])+frac*np.log(late['final_f_S_number_normalization']))
        args=dict(xmid=h['x_minimum'],amplitude=(h['x_outer']-h['x_inner'])/2,omega=omega,Tc=h['Tc_over_mu'],edges=late['q_edges'])
        k=band_kernel(**args,radial=2,angular=8,channels=channels);c=contract_band(k,args['Tc'],args['edges'],f)
        ref=orbit_response(**args,f_number=f,radial=2,angular=8)
        edges=np.asarray(args['edges']);W=(edges[1:]**3-edges[:-1]**3)/3;prob=W*f/float(W@f)
        contraction=float(prob@k['K']@prob);channel_total=sum(k['channel_K'].values())
        d=mode_data(**args,f_number=f,radial=1,angular=8)
        num=0.;den=0.;res=0.
        for lo in range(0,len(d['delta']),64):
            sl=slice(lo,lo+64)
            a=local_charged_width_modes(d['delta'][sl],d['A'][sl],d['boost'][sl],args['xmid'],args['amplitude'],omega,nodes=256,iterations=10)
            num+=float(np.sum(d['w'][sl]*d['pref'][sl]*a['rate']))
            den+=float(np.sum(d['w'][sl]*d['pref'][sl]*a['rate_without_charged']))
            res=max(res,a['last_iteration_relative'])
        select=np.linspace(0,len(d['delta'])-1,13,dtype=int)
        aa=local_charged_width_modes(d['delta'][select],d['A'][select],d['boost'][select],args['xmid'],args['amplitude'],omega,nodes=256,iterations=10)
        bb=local_charged_width_modes(d['delta'][select],d['A'][select],d['boost'][select],args['xmid'],args['amplitude'],omega,nodes=512,iterations=14)
        bound=charged_width_bound(args['xmid'],args['amplitude'])
        rows.append(dict(Tc=args['Tc'],history_index=index,
             occupation_independent_contraction_relative=abs(contraction/ref['dynamic_pair_sigma_v']-1),
             symmetry=float(np.max(abs(k['K']-k['K'].T))),minimum=float(k['K'].min()),
             channel_sum_relative=float(np.max(abs(channel_total-k['K']))/np.max(k['K'])),
             carrier_identity_relative=abs(c['charged_number_loss_mu4']/(2*c['event_rate_mu4'])-1),
             charged_width_bound=bound,local_absorptive_charged_width_multiplier=num/den,
             charged_width_iteration_residual=res,
             FFT_node_iteration_repeat=float(np.max(abs(aa['rate']/bb['rate']-1))),
             original_pair_sigma_v=den,with_local_charged_width_pair_sigma_v=num,
             maximum_energy_exchange_bound_per_event=c['absolute_energy_exchange_bound_mu5']/c['event_rate_mu4']))
    checks=dict(contraction=all(x['occupation_independent_contraction_relative']<1e-10 for x in rows),
                symmetric_positive=all(x['symmetry']<1e-8 and x['minimum']>=0 for x in rows),
                channel_sum=all(x['channel_sum_relative']<1e-11 for x in rows),
                number_identity=all(x['carrier_identity_relative']<1e-14 for x in rows),
                perturbation_bound=all(x['charged_width_bound']['minimum_rate_ratio']<x['local_absorptive_charged_width_multiplier']<x['charged_width_bound']['maximum_rate_ratio'] for x in rows),
                contraction_iterations=all(x['charged_width_iteration_residual']<1e-6 for x in rows),
                FFT_repeat=all(x['FFT_node_iteration_repeat']<.001 for x in rows))
    result=dict(claim_id='CC10_OCCUPATION_INDEPENDENT_MEMORY_KERNEL',checks=checks,rows=rows,
                scope='Actual four-state occupation-independent physical pair kernel; tests full local absorptive on-shell charged-width perturbation on occupied continuum. The norm bound does not cover unspecified nonlocal/dispersive matching.',
                runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps(serialize(result)));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
