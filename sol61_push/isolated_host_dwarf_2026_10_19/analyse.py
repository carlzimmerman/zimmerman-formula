"""Read recorded runs, compare controls, and create a standalone scientific plot."""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/cold_dwarf_matplotlib')
import csv
import json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run_dwarf import centre, gravity, vector_J
from remnant import diagnose_remnant

HERE=Path(__file__).resolve().parent


def tail_mean(r,key):
    end=r['args']['duration']
    vals=[z[key] for z in r['snapshots'] if z['time_Myr']>=end-1000 and z[key] is not None]
    if not vals:
        return None,None
    return float(np.mean(vals)),float(np.std(vals))


def inspect_case(r):
    summary=dict(r['summary'])
    for key in ['M100','M300','M1000','cold_rhalf_pc','central_sigma_star_1d_kms']:
        value,scatter=tail_mean(r,key)
        summary['last_Gyr_mean_'+key]=value
        summary['last_Gyr_temporal_std_'+key]=scatter
    snapshots=[z for z in r['snapshots'] if z['time_Myr']>=r['args']['duration']-1000]
    density=np.mean([z['cold_shell_density_Msun_pc3'] for z in snapshots],axis=0)
    summary['last_Gyr_mean_shell_density']=density.tolist()
    summary['last_Gyr_mean_enclosed']=np.mean([z['cold_enclosed_Msun'] for z in snapshots],axis=0).tolist()
    summary['initial_M100']=r['snapshots'][0]['M100']
    summary['initial_M300']=r['snapshots'][0]['M300']
    folder=HERE/r['args']['output'].split('/')[-1]
    first=np.load(folder/'initial.npz'); final=np.load(folder/'final.npz')
    x=final['x']; v=final['v']; m=final['m']; cold=final['cold']
    remnant=diagnose_remnant(x,v,m,cold,r['args']['eps'])
    summary['remnant_diagnostic']=remnant
    cc=np.array(remnant['centre']); rr=np.linalg.norm(x-cc,axis=1)
    ids=cold & (rr<=300.)
    summary['remnant_M100']=remnant['M100']; summary['remnant_M300']=remnant['M300']
    summary['remnant_M1000']=float(m[cold & (rr<=1000)].sum())
    order=np.argsort(rr[cold]); cr=np.cumsum(m[cold][order])
    summary['remnant_cold_rhalf_pc']=float(np.interp(.5*m[cold].sum(),cr,rr[cold][order]))
    summary['remnant_cumulative_mass']=[float(m[cold & (rr<=rad)].sum()) for rad in r['radii_pc']]
    summary['remnant_shell_density']=(np.diff(np.r_[0.,summary['remnant_cumulative_mass']])/(4*np.pi/3*np.diff(np.r_[0.,np.array(r['radii_pc'])**3]))).tolist()
    summary['legacy_centre_offset_pc']=float(np.linalg.norm(cc-np.array(r['snapshots'][-1]['centre'])))
    tree=cKDTree(x[cold]); pm=float(m[cold][0])
    count300=tree.query_ball_point(x[cold],300.,return_length=True)
    count600=tree.query_ball_point(x[cold],600.,return_length=True)
    summary['max_particle_centred_cold_M300']=float(max(count300)*pm)
    # Any300pc sphere containing particles is contained in the600pc ball of
    # any one of those particles: this is a conservative any-centre upper bound.
    summary['any_centre_cold_M300_geometric_upper_bound']=float(max(count600)*pm)
    cohort={}
    for label,data in [('initial',first),('final',final)]:
        xx=data['x'][ids]; vv=data['v'][ids]; mm=m[ids]
        if not len(mm):
            cohort[label]=None
            continue
        X=np.average(xx,axis=0,weights=mm); V=np.average(vv,axis=0,weights=mm)
        _,U=gravity(xx,mm,r['args']['eps'])
        K=float(.5*np.sum(mm[:,None]*(vv-V)**2))
        cohort[label]=dict(count=int(ids.sum()),mass_Msun=float(mm.sum()),
            own_COM=X.tolist(),own_velocity=V.tolist(),intrinsic_J=vector_J(xx-X,vv-V,mm).tolist(),
            cold_only_self_energy=K+U,cold_only_self_kinetic=K,cold_only_self_potential=U,
            rms_size_pc=float(np.sqrt(np.average(np.sum((xx-X)**2,axis=1),weights=mm))))
    summary['final_300pc_cohort_own_frame']=cohort
    summary['conservation_gate_pass']=summary['max_energy_total_error_scaled']<.01 and summary['max_J_int_closure_scaled']<1e-7
    summary['initial_phase_space_sha256']=r['initial_conditions']['relative_state_sha256']
    summary['run_status']=json.loads((folder/'manifest.json').read_text())['run']['status']
    return summary


def main(output=HERE):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    raw={}
    for path in sorted(HERE.glob('run_*/results.json')):
        name=path.parent.name[4:]
        manifest=path.parent/'manifest.json'
        if not name.startswith('pilot') and manifest.exists() and json.loads(manifest.read_text())['run']['status']=='completed':
            raw[name]=json.loads(path.read_text())
    summaries={name:inspect_case(r) for name,r in raw.items()}
    comparisons={}
    for label in ['iso','host']:
        base=summaries.get('base_'+label)
        if base is None:
            continue
        for variant in ['nocoll','dt','n','h','eps']:
            alt=summaries.get(variant+'_'+label)
            if alt is None:
                continue
            comparisons[variant+'_'+label]={}
            reference=summaries.get('dt_'+label,base) if variant=='eps' else base
            for key in ['M100','M300','M1000','cold_rhalf_pc']:
                a=reference['remnant_'+key]; b=alt['remnant_'+key]
                comparisons[variant+'_'+label][key]=dict(base=a,variant=b,relative_difference=abs(a-b)/max(abs(a),1.))
            comparisons[variant+'_'+label]['reference_case']='dt_'+label if variant=='eps' else 'base_'+label
    result=dict(cases=summaries,comparisons=comparisons,
       comparison_definition='Final10Gyr apertures about independently located potential-minimum remnants; v1 host late-Gyr stellar-centred means are unreliable and are retained only as original diagnostics.',
       interpretation='Fixed initial state and finite particle/softening/kernel scales; a300pc concentration is not automatically a100pc density core.',
       conventions=dict(energy='Msun pc2/Myr2; one unit=1.901e36J',J='Msun pc2/Myr; vector components retained',
                        endpoint_energy='Half cross-potential assigned to each group; host work subtracted for internal exchange',
                        cohort='Final300pc cohort selected retrospectively; own-frame spin separated from its motion about total dwarf COM'))
    (output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    with (output/'comparison.csv').open('w') as stream:
        writer=csv.writer(stream)
        writer.writerow(['case','remnant_M100','remnant_M300','remnant_M1000','cold_rhalf_about_remnant_pc','cold_count300','star_count300','collisions','max_relative_energy_error','original_centre_offset_pc'])
        for name,s in summaries.items():
            writer.writerow([name]+[s['remnant_'+k] for k in ['M100','M300','M1000','cold_rhalf_pc']]+
                            [s['remnant_diagnostic']['cold_count300'],s['remnant_diagnostic']['star_count300'],s['collisions'],s['max_energy_total_error_scaled'],s['legacy_centre_offset_pc']])
    if not all(name in raw for name in ['base_iso','base_host']):
        print('Available cases:',','.join(raw)); return
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(12,9),constrained_layout=True)
    colors={'iso':'#176b9a','host':'#d36d26'}
    budget_values=[[],[]]
    for label,title in [('iso','Isolated'),('host','Around host')]:
        chosen='replay_'+label if 'replay_'+label in raw else 'base_'+label
        r=raw[chosen]; s=summaries[chosen]; color=colors[label]
        ts=np.array([z['time_Myr'] for z in r['snapshots']])/1000
        if label=='iso' or chosen.startswith('replay'):
            axes[0,0].plot(ts,np.array([z['M300'] for z in r['snapshots']])/1e6,color=color,label=title)
        else:
            axes[0,0].scatter([ts[-1]],[s['remnant_M300']/1e6],color=color,label=title+' endpoint (re-centred)')
        if label=='iso' and 'nocoll_'+label in raw:
            control=raw['nocoll_'+label]
            axes[0,0].plot(np.array([z['time_Myr'] for z in control['snapshots']])/1000,
                           np.array([z['M300'] for z in control['snapshots']])/1e6,color=color,ls=':',alpha=.8)
        rr=np.array(r['radii_pc'])
        axes[0,1].plot(rr,np.array(s['remnant_cumulative_mass'])/1e6,color=color,label=title)
        initialJ=np.array(r['snapshots'][0]['Jint']); direction=initialJ/np.linalg.norm(initialJ)
        groups=s['fixed_membership_groups']; names=['final_core_material','other_cold_material','stars']
        offset=-.18 if label=='iso' else .18; pos=np.arange(3)+offset
        internalE=np.array([groups[k]['inferred_internal_energy_transfer'] for k in names])/1e8
        hostE=np.array([groups[k]['host_internal_work'] for k in names])/1e8
        internalJ=np.array([np.array(groups[k]['inferred_internal_J_transfer'])@direction for k in names])/1e10
        hostJ=np.array([np.array(groups[k]['host_internal_torque'])@direction for k in names])/1e10
        axes[1,0].bar(pos,internalE,width=.34,color=color,label=title+' internal exchange')
        axes[1,0].scatter(pos,internalE+hostE,color=color,marker='x',s=50)
        axes[1,1].bar(pos,internalJ,width=.34,color=color,label=title+' internal exchange')
        axes[1,1].scatter(pos,internalJ+hostJ,color=color,marker='x',s=50)
        budget_values[0].extend(internalE.tolist()+(internalE+hostE).tolist())
        budget_values[1].extend(internalJ.tolist()+(internalJ+hostJ).tolist())
    initial=raw['base_iso']['snapshots'][0]
    axes[0,1].plot(raw['base_iso']['radii_pc'],np.array(initial['cold_enclosed_Msun'])/1e6,c='.45',ls='--',label='Initial diffuse cloud')
    axes[0,0].set(xlabel='Time (Gyr)',ylabel=r'Cold mass inside 300 pc (million $M_\odot$)',title='Central concentration; dotted = isolated collisionless control')
    axes[0,1].set(xscale='log',xlabel='Radius (pc)',ylabel=r'Enclosed cold mass (million $M_\odot$)',title='Final profile about the potential-minimum remnant')
    axes[1,0].set(ylabel=r'Energy change / $10^8$ ($M_\odot$ pc$^2$/Myr$^2$)',title='Recipients: bars internal; crosses include host work')
    axes[1,1].set(ylabel=r'Projected $\Delta J$ / $10^{10}$ ($M_\odot$ pc$^2$/Myr)',title='J about original-dwarf COM; crosses include host torque')
    for ax,values in zip(axes[1],budget_values):
        ax.set_xticks(np.arange(3),['Final-core cohort','Other cold / tails','Stars']); ax.axhline(0,color='.5',lw=.7)
        ax.set_yscale('symlog',linthresh=1.)
        ax.set_ylim(1.5*min(min(values),-.1),1.8*max(max(values),.1))
    for ax in axes[0]:
        ax.legend(frameon=False)
    axes[1,0].legend(frameon=False,fontsize=8)
    fig.suptitle('Prepared carrier dwarf: no imposed cold core\nNewtonian kinetic reduction; fixed host; finite numerical experiment',fontsize=15)
    fig.savefig(output/'isolated_host_comparison.png',dpi=170)
    plt.close(fig)
    print(json.dumps({name:{k:s[k] for k in ['last_Gyr_mean_M100','last_Gyr_mean_M300','last_Gyr_mean_cold_rhalf_pc','collisions','conservation_gate_pass']} for name,s in summaries.items()},indent=2))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(HERE))
    main(parser.parse_args().output)
