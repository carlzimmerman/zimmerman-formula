from pathlib import Path
import hashlib,json
R=Path.cwd();D=R/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-018/fgf018_run_001';m=json.loads((R/'campaign_fresh_gravity_astra/stage_03/cluster_precision/run_003/manifest.json').read_text())
paths=['campaign_fresh_gravity_astra/stage_03/cluster_precision/constraint.py','real_research/data/xcop/xcop_r500_ettori2019.json']
for n in ['A1795','A2029','A2142','A2319','A644','A85','ZW1215']:
 for kind in ['mstar','hydro_mass','fgas_profile']:paths.append(f'real_research/data/xcop/{n}/{n}_{kind}.fits')
paths += ['campaign_fresh_gravity_astra/stage_03/cluster_precision/run_003/shell_constraints.csv','campaign_fresh_gravity_astra/stage_03/cluster_precision/run_003/continuity_intervals.csv']
expected={x['path']:x.get('sha256_after',x['sha256']) for x in m['input_artifacts']+m['outputs']}
expected['campaign_fresh_gravity_astra/stage_04/cluster_observables/NEXT_TASKS.md']='2955ad11fa5cd6b061c2c5e265ed3d33bcbfea15aff972e49c575cd0ead11d54'
expected['deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-012/fgf012_audit_001/result.json']='fcf82978e181d266bf0c504f80d5c7507a3b288014b73e5a0ad76e73aaf3f28a'
paths+=list(expected)[-2:]
rows=[]
for p in paths:
 h=hashlib.sha256((R/p).read_bytes()).hexdigest();rows.append(dict(path=p,actual=h,expected=expected[p],pass_=h==expected[p]))
(D/'source_hash_check.json').write_text(json.dumps(rows,indent=2)+'\n')
assert all(x['pass_'] for x in rows);print(len(rows),'source hashes match')
