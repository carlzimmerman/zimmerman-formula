import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent

def main(output):
    runs=[];statuses={}
    for suite,count in [('base',8),('space',8),('velocity',8),('cell',4),('time',4),('seed',4),('shape',8),('high',4)]:
        d=p/('run_'+suite);manifest=json.loads((d/'manifest.json').read_text());statuses[suite]=manifest['run']['status'];assert statuses[suite]=='completed'
        rows=json.loads((d/'results.json').read_text())['runs'];assert len(rows)==count
        for r in rows:r['suite']=suite
        runs+=rows
    assert all(r['status']=='completed' for r in runs)
    active=json.loads((p/'run_active/results.json').read_text())['runs'];assert all(r['status']=='completed' for r in active)
    stress_ok=[];statuses['stress']='interrupted; excluded; no final manifest'
    out={'default_runs':len(runs),'active_controls':len(active),'stress_excluded':True,'suite_statuses':statuses,
         'max_final_T':max(r['final']['q'] for r in runs),
         'bound_free_range':[min(r['final']['bound_free_fraction'] for r in runs),max(r['final']['bound_free_fraction'] for r in runs)],
         'max_energy_error':max(r['max_energy_error'] for r in runs+active),
         'max_momentum_error':max(r['max_momentum_error'] for r in runs+active),
         'max_angular_error':max(r['max_angular_momentum_error'] for r in runs+active),
         'min_RAR_rms':min(r['final']['rar_rms_dex'] for r in runs),
         'min_RAR_max':min(r['final']['rar_max_dex'] for r in runs),
         'max_opacity_proxy':max(r['stats']['max_cell_width_over_mfp'] for r in runs),
         'max_actual_hazard_step':max(r['stats']['max_encounter_hazard_step'] for r in runs),
         'max_event_energy_error':max(r['stats']['event_energy_error'] for r in runs),
         'attempts':sum(r['stats']['attempts'] for r in runs),'captures':sum(r['stats']['captures'] for r in runs),
         'releases':sum(r['stats']['releases'] for r in runs),
         'max_expected_proposals_per_medium_sample':max(r['stats']['expected_medium_proposals']/r['n'] for r in runs),
         'profiles':[],'high_resolution':[],'stress':[]}
    assert out['max_energy_error']<1e-3
    for i in range(4):
        rows=[r for r in runs if r['profile_index']==i]
        out['profiles'].append({'profile_index':i,'mass':rows[0]['mass_msun'],'b_kpc':rows[0]['b_kpc'],'q_range':[min(r['final']['q'] for r in rows),max(r['final']['q'] for r in rows)],'bound_free_min':min(r['final']['bound_free_fraction'] for r in rows),'max_expected_proposals_per_sample':max(r['stats']['expected_medium_proposals']/r['n'] for r in rows)})
    for r in runs:
        if r['suite']=='high':out['high_resolution'].append({k:r[k] for k in ('profile_index','f','n','nspace','nvel','final','stats')})
    for r in stress_ok:
        out['stress'].append(dict(profile_index=r['profile_index'],f=r['f'],q=r['final']['q'],bound_free=r['final']['bound_free_fraction'],opacity=r['stats']['max_cell_width_over_mfp'],energy_error=r['max_energy_error'],attempts=r['stats']['attempts'],captures=r['stats']['captures'],releases=r['stats']['releases'],rar_rms=r['final']['rar_rms_dex']))
    checks=json.loads((p/'run_checks/results.json').read_text());flow=json.loads((p/'run_flow/results.json').read_text());fine=json.loads((p/'run_refined_rate/results.json').read_text())
    out['finest_rate_benchmark']=fine['benchmarks'][-1];out['cold_flow']=flow['cold_flow']
    out['operator_checks']={k:v for k,v in checks.items() if k not in ('manufactured','forced_capture_stats')}
    out['active_field_controls']=[{k:r[k] for k in ('spacing','max_energy_error','max_momentum_error','max_angular_momentum_error','final')} for r in active]
    out['stress_initial_screen']=json.loads((p/'run_stress_screen/results.json').read_text())
    Path(output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    plt.rcParams.update({'font.size':10});fig,ax=plt.subplots(1,3,figsize=(14,4.5),constrained_layout=True)
    vals=[r for r in checks['manufactured'] if r['kind']=='gaussian' and r['nvel']==2 and r['max_width']==2]
    ns=[r['nspace'] for r in vals];ys=[r['flux_ratio_mean'] for r in vals];err=[r['flux_ratio_se'] for r in vals]
    ax[0].errorbar(ns,ys,yerr=err,marker='o',label='Adaptive cells, width cap 2')
    rr=[r for r in fine['benchmarks'] if r['observable']=='flux'];ax[0].errorbar([r['nspace'] for r in rr],[r['ratio_mean'] for r in rr],yerr=[r['ratio_se'] for r in rr],marker='s',label='Width cap 0.25')
    ax[0].axhline(1,color='black',ls='--');ax[0].set_xscale('log');ax[0].set_xlabel('Spatial nodes per species');ax[0].set_ylabel('Computed / exact collision integral');ax[0].set_title('Manufactured Gaussian rate benchmark');ax[0].legend(fontsize=8)
    for f,marker,color in [(0,'o','#376996'),(.95,'^','#d47f35')]:
        for i in range(4):
            rows=[r for r in runs if r['profile_index']==i and r['f']==f]
            offsets=np.linspace(-.12,.12,len(rows))+(0 if f==0 else .22)
            ax[1].scatter(i+offsets,[100*r['final']['q'] for r in rows],marker=marker,color=color,alpha=.6,label=('Unordered' if f==0 else 'Rotating') if i==0 else None)
            ax[2].scatter(i+offsets,[r['final']['rar_rms_dex'] for r in rows],marker=marker,color=color,alpha=.6)
    labels=['3e5 / 0.3','1e8 / 1','6e10 / 3','1e14 / 300']
    for a in ax[1:]:a.set_xticks(np.arange(4)+.1,labels,rotation=25);a.set_xlabel('Baryon mass (Msun) / scale (kpc)')
    ax[1].set_ylabel('Final tethered reservoir (%)');ax[1].set_title('Default-coefficient live tests');ax[1].legend()
    ax[2].set_ylabel('3D acceleration residual RMS (dex)');ax[2].axhline(.05,color='black',ls='--',label='Illustrative target');ax[2].set_title('Acceleration relation not recovered');ax[2].legend(fontsize=8)
    fig.suptitle('Adaptive kinetic prototype: benchmark convergence does not establish live-system continuum convergence',fontsize=12)
    fig.savefig(Path(output).parent/'results.png',dpi=170)
    print(json.dumps({k:v for k,v in out.items() if k not in ('high_resolution','operator_checks','active_field_controls')},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();main(a.output)
