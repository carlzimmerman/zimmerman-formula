"""Read-only finite-record checks; physical convergence is a separate decision."""
import argparse
import json
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent


def audit_case(folder):
    folder=Path(folder);manifest=json.loads((folder/'manifest.json').read_text())
    r=json.loads((folder/'results.json').read_text());a=np.load(folder/'initial.npz');b=np.load(folder/'final.npz')
    checks=[]
    def check(name,value):checks.append(dict(name=name,passed=bool(value)))
    check('manifest_completed',manifest['run']['status']=='completed')
    check('all_original_masses_and_labels_retained',np.array_equal(a['m'],b['m']) and np.array_equal(a['cold'],b['cold']))
    check('unchanged_particle_count',a['x'].shape==b['x'].shape==(r['args']['ncold']*9//8,3))
    check('finite_saved_phase_space',all(np.all(np.isfinite(z[k])) for z in (a,b) for k in ('x','v','m')))
    check('positive_masses',np.all(b['m']>0.))
    check('recorded_cold_count',int(np.sum(b['cold']))==r['args']['ncold'])
    check('recorded_stellar_count',int(np.sum(~b['cold']))==r['args']['ncold']//8)
    check('physical_energy_gate_0p1_percent',r['maxima']['E']<.001)
    # Evolution stores both residuals already normalized by the initial dwarf
    # internal-energy scale, independent of the (possibly much larger) host
    # orbital energy. Particle-sum partitions alone do not test these closures.
    check('internal_energy_host_work_gate_0p1_percent',r['maxima']['internal_work']<=.001)
    check('host_potential_work_gate_0p1_percent',r['maxima']['host_work']<=.001)
    check('vector_angular_momentum_ledgers',max(r['maxima'][k] for k in ('Jint','Jorb','Jtotal'))<1e-7)
    check('momentum_ledger',r['maxima']['P']<1e-7)
    check('negligible_collision_energy_defect',abs(r['collision_energy_defect'])/r['energy_scale']<1e-10)
    check('negligible_collision_vectorJ_defect',np.linalg.norm(r['collision_J_defect'])/r['J_scale']<1e-10)
    check('perparticle_host_work_partition',abs(r['host_work_particle_sum_residual'])/r['energy_scale']<1e-10)
    check('perparticle_host_torque_partition',np.linalg.norm(r['host_torque_particle_sum_residual'])/r['J_scale']<1e-10)
    rows=r['snapshots'];ts=np.array([s['time_Myr'] for s in rows])
    check('full_declared_time_coverage',ts[0]==0 and abs(ts[-1]-r['args']['duration'])<1e-8 and np.all(np.diff(ts)>0.))
    check('declared_record_interval',np.max(np.diff(ts))<=r['args']['record_interval']+1e-8)
    de=sum(g['delta_E'] for g in r['fixed_membership_groups'].values())
    check('fixed_material_energy_partition',abs(de-(rows[-1]['conservation']['Eint']-rows[0]['conservation']['Eint']))/r['energy_scale']<1e-10)
    dj=sum((np.array(g['delta_J']) for g in r['fixed_membership_groups'].values()),np.zeros(3))
    expected=np.array(rows[-1]['conservation']['Jint'])-rows[0]['conservation']['Jint']
    check('fixed_material_vectorJ_partition',np.linalg.norm(dj-expected)/r['J_scale']<1e-10)
    if r['args']['collisionless']:
        check('collisionless_control_has_zero_events',r['collisions']==0 and r['collision_energy_defect']==0. and np.array_equal(r['collision_J_defect'],np.zeros(3)))
    else:
        check('actual_revised_below_resonance_domain',r['max_resonance_z']<.1)
    if r['args']['backend']=='metal':
        pc=r.get('evolved_state_precision_checks',[])
        check('gpu_has_evolved_state_cpu_comparisons',len(pc)>=2)
        check('all_gpu_cpu_comparisons_pass',all(max(z['force_relative_L2'],z['phi_relative_L2'],z['potential_energy_relative'])<1e-11 for z in pc))
    t=np.load(folder/'trajectory.npz')
    check('trajectory_has_initial_and_final_epochs',t['time_Myr'][0]==0. and t['time_Myr'][-1]==r['args']['duration'])
    check('trajectory_final_matches_endpoint',np.array_equal(t['x'][-1],b['x']) and np.array_equal(t['v'][-1],b['v']))
    check('trajectory_initial_matches_initial',np.array_equal(t['x'][0],a['x']) and np.array_equal(t['v'][0],a['v']))
    final=rows[-1];radius=np.linalg.norm(b['x']-np.array(final['centre']),axis=1)
    for R,key in [(100.,'M100'),(300.,'M300')]:
        check('independent_endpoint_'+key,abs(float(b['m'][b['cold']&(radius<=R)].sum())-final[key])<1e-6)
    return dict(case=folder.name[4:],checks=checks,all_checks_pass=all(c['passed'] for c in checks),
        failed=[c['name'] for c in checks if not c['passed']],maxima=r['maxima'],args=r['args'],
        receipt_energy_normalization='initial dwarf internal-energy scale; residuals supplied by evolution, allocation sums checked separately',
        interpretation='Finite bookkeeping and admission checks only. Profile/host convergence and core classification require independent controls and resolved radial coverage.')


def main(args):
    out=Path(args.output)
    if out.exists():raise FileExistsError('fresh audit output required')
    out.mkdir(parents=True)
    skipped=[]
    if args.case:
        selected=args.case
    else:
        selected=[]
        for folder in sorted(HERE.glob('run_*')):
            if not folder.is_dir() or not (folder/'manifest.json').exists():continue
            if 'pilot' in folder.name and not args.include_pilots:continue
            manifest=json.loads((folder/'manifest.json').read_text())
            status=manifest.get('run',{}).get('status')
            if status=='completed':selected.append(folder.name[4:])
            else:skipped.append(dict(case=folder.name[4:],manifest_status=status,reason='manifest_not_completed'))
    cases={n:audit_case(HERE/('run_'+n)) for n in selected}
    all_pass=bool(cases) and all(z['all_checks_pass'] for z in cases.values())
    result=dict(cases=cases,all_checks_pass=all_pass,
        status=('inconclusive_no_completed_cases' if not cases else 'completed_checks_pass' if all_pass else 'completed_checks_failed'),
        expected_cases=selected,completed_case_count=len(cases),skipped_cases=skipped,not_a_convergence_certificate=True)
    (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(cases=len(cases),all_checks_pass=result['all_checks_pass'],failures={n:z['failed'] for n,z in cases.items() if z['failed']})))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--case',action='append');p.add_argument('--include-pilots',action='store_true')
    main(p.parse_args())
