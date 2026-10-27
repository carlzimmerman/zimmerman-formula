"""Reproduce output checks and follow identical particle cohorts across hosts."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import analyse
from run_dwarf import per_particle_EJ

HERE=Path(__file__).resolve().parent
EXPECTED=['base_iso','base_host','nocoll_iso','nocoll_host','dt_iso','dt_host',
          'n_iso','n_host','h_iso','h_host','eps_iso','replay_iso','replay_host']


def main(output):
    out=Path(output); out.mkdir(parents=True,exist_ok=True)
    checks=[]
    def check(name,value):
        checks.append(dict(name=name,passed=bool(value)))
    results={}
    for name in EXPECTED:
        folder=HERE/('run_'+name)
        manifest=json.loads((folder/'manifest.json').read_text())
        result=json.loads((folder/'results.json').read_text()); results[name]=result
        check(name+' recorded completed',manifest['run']['status']=='completed')
        first=np.load(folder/'initial.npz'); last=np.load(folder/'final.npz')
        check(name+' no particle/mass deletion',np.array_equal(first['m'],last['m']) and np.array_equal(first['cold'],last['cold']) and first['x'].shape==last['x'].shape)
        check(name+' finite final phase space',np.all(np.isfinite(last['x'])) and np.all(np.isfinite(last['v'])))
        s=result['summary']
        check(name+' E error below1percent initial binding',s['max_energy_total_error_scaled']<.01)
        check(name+' vector angular momentum ledger',max(s['max_J_int_closure_scaled'],s['max_J_orb_closure_scaled'],s['max_J_total_closure_scaled'])<1e-7)
        check(name+' energy group partition',abs(s['energy_group_sum_residual'])<1e-8*s['energy_scale'])
        check(name+' collision E/J defects negligible',abs(s['collision_energy_error_scaled'])<1e-8 and s['collision_J_error_scaled']<1e-8)
    replay_checks={}
    for label in ('iso','host'):
        replay_checks[label]={}
        for stage in ('initial','final'):
            a=np.load(HERE/('run_base_'+label)/(stage+'.npz'))
            b=np.load(HERE/('run_replay_'+label)/(stage+'.npz'))
            replay_checks[label][stage]={key:bool(np.array_equal(a[key],b[key])) for key in ('x','v','m','cold')}
            check(label+' replay '+stage+' bitwise identity',all(replay_checks[label][stage].values()))
    for prefix in ('base','nocoll','dt','n','h'):
        a=np.load(HERE/('run_'+prefix+'_iso')/'initial.npz')
        b=np.load(HERE/('run_'+prefix+'_host')/'initial.npz')
        delta_x=b['x']-a['x']; delta_v=b['v']-a['v']
        check(prefix+' same masses/labels',np.array_equal(a['m'],b['m']) and np.array_equal(a['cold'],b['cold']))
        check(prefix+' identical relative initial positions',np.max(np.abs(delta_x-np.array([80000.,0.,0.])))<2e-10)
        check(prefix+' identical relative initial velocities',np.max(np.abs(delta_v-delta_v[0]))<1e-11)
        check(prefix+' identical pretranslation hash',results[prefix+'_iso']['initial_conditions']['relative_state_sha256']==results[prefix+'_host']['initial_conditions']['relative_state_sha256'])
    analyse.main(out)
    analysis=json.loads((out/'analysis.json').read_text())
    states={}
    for label in ('iso','host'):
        first=np.load(HERE/('run_replay_'+label)/'initial.npz')
        last=np.load(HERE/('run_replay_'+label)/'final.npz')
        ep0,jp0,_=per_particle_EJ(first['x'],first['v'],first['m'],40.)
        ep1,jp1,_=per_particle_EJ(last['x'],last['v'],last['m'],40.)
        states[label]=(first,last,ep0,jp0,ep1,jp1)
    cohorts={}
    for selection in ('iso','host'):
        last=states[selection][1]
        centre=np.array(analysis['cases']['replay_'+selection]['remnant_diagnostic']['centre'])
        cohorts[selection+'_final_300pc']=last['cold'] & (np.linalg.norm(last['x']-centre,axis=1)<=300.)
    transfers={}
    for cohort,mask in cohorts.items():
        transfers[cohort]={}
        for environment in ('iso','host'):
            first,last,e0,j0,e1,j1=states[environment]
            cc=np.array(analysis['cases']['replay_'+environment]['remnant_diagnostic']['centre'])
            mass=last['m'][mask]
            wh=float(last['host_work_particle'][mask].sum())
            th=last['host_torque_particle'][mask].sum(axis=0)
            deltae=float(e1[mask].sum()-e0[mask].sum()); deltaj=j1[mask].sum(axis=0)-j0[mask].sum(axis=0)
            transfers[cohort][environment]=dict(count=int(mask.sum()),mass_Msun=float(mass.sum()),
                final_mass_inside_remnant300_Msun=float(mass[np.linalg.norm(last['x'][mask]-cc,axis=1)<=300.].sum()),
                final_median_radius_about_remnant_pc=float(np.median(np.linalg.norm(last['x'][mask]-cc,axis=1))),
                delta_E=deltae,host_work=wh,internal_energy_exchange=deltae-wh,
                delta_J=deltaj.tolist(),host_torque=th.tolist(),internal_J_exchange=(deltaj-th).tolist())
    (out/'same_material_transfer.json').write_text(json.dumps(transfers,indent=2)+'\n')
    with (out/'same_material_transfer.csv').open('w') as stream:
        writer=csv.writer(stream)
        writer.writerow(['cohort','environment','mass_Msun','retained_inside300_Msun','delta_E','host_work','internal_exchange',
                         'delta_Jx','delta_Jy','delta_Jz','host_Tx','host_Ty','host_Tz','internal_Jx','internal_Jy','internal_Jz'])
        for name,items in transfers.items():
            for env,s in items.items():
                writer.writerow([name,env,s['mass_Msun'],s['final_mass_inside_remnant300_Msun'],s['delta_E'],s['host_work'],s['internal_energy_exchange']]+s['delta_J']+s['host_torque']+s['internal_J_exchange'])
    audit=dict(checks=checks,all_checks_pass=all(row['passed'] for row in checks),
               replay_bitwise_identity=replay_checks,expected_cases=EXPECTED,
               interpretation='These checks verify finite records and bookkeeping, not full-theory validity or continuum convergence.')
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    if not audit['all_checks_pass']:
        raise RuntimeError('One or more finite implementation/provenance checks failed: '+str([row for row in checks if not row['passed']]))


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    main(parser.parse_args().output)
