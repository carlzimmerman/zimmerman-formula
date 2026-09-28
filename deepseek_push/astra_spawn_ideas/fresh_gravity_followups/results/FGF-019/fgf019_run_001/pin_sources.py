from pathlib import Path
import json,hashlib
R=Path.cwd();D=R/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
m=json.loads((R/'campaign_fresh_gravity_astra/stage_04/cluster_observables/run_002/manifest.json').read_text());expected={x['path']:x.get('sha256_after',x['sha256']) for x in m['input_artifacts']+m['outputs']}
paths=['deepseek_push/Z06_data/ilc_actplanck_ymap.fits','deepseek_push/Z06_data/wide_mask_GAL070_apod_1.50_deg_wExtended.fits','deepseek_push/Z06_data/ilc_beam.txt','deepseek_push/Z06_data/PROVENANCE.md','real_research/data/erass1cl_primary_v3.2.fits','real_research/data/xcop/xcop_r500_ettori2019.json','campaign_fresh_gravity_astra/stage_04/cluster_observables/run_002/catalogue_matches.csv']
for n in ['A644','ZW1215']:
 for kind in ['mstar','hydro_mass','fgas_profile']:paths.append(f'real_research/data/xcop/{n}/{n}_{kind}.fits')
expected['campaign_fresh_gravity_astra/stage_04/cluster_observables/NEXT_TASKS.md']='2955ad11fa5cd6b061c2c5e265ed3d33bcbfea15aff972e49c575cd0ead11d54';expected['deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-012/fgf012_audit_001/result.json']='fcf82978e181d266bf0c504f80d5c7507a3b288014b73e5a0ad76e73aaf3f28a';paths+=list(expected)[-2:]
rows=[dict(path=p,expected=expected[p],actual=sha(R/p)) for p in paths]
for x in rows:x['pass_']=x['expected']==x['actual']
(D/'source_hash_check.json').write_text(json.dumps(rows,indent=2)+'\n');assert all(x['pass_'] for x in rows);print(len(rows),'source hashes match')
