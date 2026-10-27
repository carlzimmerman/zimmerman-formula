import json,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from field import Field3D

p=Path(__file__).resolve().parent

def main(output):
    runs=[]
    for name,count in [('scan',16),('refinement',8),('interval',4),('encounter',2)]:
        manifest=json.loads((p/('run_'+name+'_exact')/'manifest.json').read_text())
        assert manifest['run']['status']=='completed'
        rows=json.loads((p/('run_'+name+'_exact')/'results.json').read_text())['runs']
        assert len(rows)==count
        for r in rows:r['suite']=name
        runs+=rows
    assert all(r['status']=='completed' for r in runs)
    a=json.loads((p/'run_active_exact/results.json').read_text());checks=json.loads((p/'run_checks_exact/results.json').read_text())
    summary=dict(formation_runs=len(runs),active_transport_controls=len(a['seeded_transport']),
        max_T=max(r['final']['q'] for r in runs),min_bound_free=min(r['final']['bound_free_fraction'] for r in runs),
        max_energy_error=max(r['max_energy_error'] for r in runs+a['seeded_transport']),
        max_momentum_error=max(r['max_momentum_error'] for r in runs+a['seeded_transport']),
        max_angular_error=max(r['max_angular_momentum_error'] for r in runs+a['seeded_transport']),
        captures=sum(r['stats']['captures'] for r in runs),attempts=sum(r['stats']['attempts'] for r in runs),
        cooling_events=sum(r['stats']['cooling_events'] for r in runs),
        min_rar_max_dex=min(r['final']['rar_max_dex'] for r in runs),
        min_rar_rms_dex=min(r['final']['rar_rms_dex'] for r in runs),
        max_actual_hazard_step=max(r['stats']['max_encounter_hazard_step'] for r in runs),
        checks=checks,profiles=[])
    summary['inner_counts']=[]
    for r in runs:
        x=np.array(r['final_positions']);n=r['n'];center=x[:n].mean(0);radius=np.linalg.norm(x-center,axis=1)
        mask=radius[n:]<np.median(radius[:n]);state=np.array(r['final_states'])[n:]
        summary['inner_counts'].append(dict(suite=r['suite'],profile_index=r['profile_index'],f=r['f'],flat=r['flat'],n=n,inner_packets=int(sum(mask)),inner_T_packets=int(sum(state&mask)),inner_q=r['final']['inner_q']))
    trunc=1000/101**1.5
    for i in range(4):
        subset=[r for r in runs if r['profile_index']==i];b=subset[0]['b_kpc'];h=.1/b
        summary['profiles'].append(dict(profile_index=i,mass_msun=subset[0]['mass_msun'],b_kpc=b,
            max_observed_neighbor_mean=max(t['local_neighbor_mean'] for r in subset for t in r['history']),
            final_empty_fraction_range=[min(r['final']['local_empty_fraction'] for r in subset),max(r['final']['local_empty_fraction'] for r in subset)],
            initial_expected_neighbors_upper_bound_n128_flat025=128*h**3/(27*.25*trunc),
            initial_n_lower_bound_for_32_expected_neighbors_flat025=32*27*.25*trunc/h**3,
            final_rar_max_dex_range=[min(r['final']['rar_max_dex'] for r in subset),max(r['final']['rar_max_dex'] for r in subset)]))
    # Exact isolated Gaussian maximum estimates packet saturation requirements.
    field=Field3D(1,1,1,1)
    opt=minimize_scalar(lambda r:-r*field.kernel(np.array([[r,0,0]]))[0][0],bounds=(.01,8),method='bounded')
    summary['isolated_gaussian_peak_coefficient']=-opt.fun
    summary['interval_comparisons']=[]
    for r in [v for v in runs if v['suite'] in ('interval','encounter')]:
        base=next(v for v in runs if v['suite']=='scan' and v['profile_index']==r['profile_index'] and v['f']==r['f'] and v['flat']==r['flat'])
        summary['interval_comparisons'].append(dict(profile_index=r['profile_index'],f=r['f'],flat=r['flat'],q_difference=r['final']['q']-base['final']['q'],rar_max_difference=abs(r['final']['rar_max_dex']-base['final']['rar_max_dex'])))
    Path(output).write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    plt.rcParams.update({'font.size':10})
    fig,axes=plt.subplots(1,3,figsize=(14,4.3),constrained_layout=True)
    labels=['3e5 / 0.3','1e8 / 1','6e10 / 3','1e14 / 300']
    for suite,offset,color in [('scan',-.15,'#376996'),('refinement',.15,'#df7e35')]:
        ys=[max(t['local_neighbor_mean'] for r in runs if r['suite']==suite and r['profile_index']==i and r['flat']==.25 for t in r['history']) for i in range(4)]
        axes[0].bar(np.arange(4)+offset,ys,.28,color=color,label='N='+('64' if suite=='scan' else '128'))
    axes[0].set_xticks(range(4),labels,rotation=25);axes[0].set_ylabel('Maximum mean local baryon count');axes[0].set_title('Short-range capture is sparsely sampled');axes[0].legend()
    needed=[x['initial_n_lower_bound_for_32_expected_neighbors_flat025'] for x in summary['profiles']]
    axes[1].bar(range(4),needed,color='#637b59');axes[1].axhline(128,color='black',ls='--',label='Largest tested N')
    axes[1].set_yscale('log');axes[1].set_xticks(range(4),labels,rotation=25);axes[1].set_ylabel('Necessary N for 32 expected neighbors');axes[1].set_title('Initial central-density upper bound');axes[1].legend()
    for f,marker in [(0,'o'),(.95,'^')]:
        for i in range(4):
            ys=[r['final']['rar_rms_dex'] for r in runs if r['suite']=='scan' and r['profile_index']==i and r['f']==f]
            axes[2].scatter([i+(-.08 if f==0 else .08)]*len(ys),ys,marker=marker,color=('#376996' if f==0 else '#df7e35'),label=('Unordered' if f==0 else 'Rotating') if i==0 else None)
    axes[2].axhline(.05,color='black',ls='--',label='Illustrative target');axes[2].set_xticks(range(4),labels,rotation=25);axes[2].set_ylabel('3D radial-force residual RMS (dex)');axes[2].set_title('No RAR recovery in these initial-value tests');axes[2].legend(fontsize=8)
    for ax in axes:ax.set_xlabel('Baryon mass (Msun) / scale (kpc)')
    fig.suptitle('3D field + fixed 0.1 kpc capture: numerical prototype, not continuum or observational validation',fontsize=12)
    fig.savefig(Path(output).parent/'results.png',dpi=170)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('checks',)},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();main(args.output)
