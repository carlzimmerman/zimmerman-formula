from pathlib import Path
import json,hashlib,subprocess,math
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');S=next((R/'campaign_fresh_gravity').glob('CFG859*'));names=['cfg859.py','FROZEN_CRITERIA.md','README.md','cfg859_results.json','cfg859_results_MUTATE.json'];hs={str((S/n).relative_to(R)):hashlib.sha256((S/n).read_bytes()).hexdigest() for n in names};matches={p:hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','915b108f8:'+p])).hexdigest()==h for p,h in hs.items()};assert all(matches.values());a=json.loads((S/names[3]).read_text());m=json.loads((S/names[4]).read_text());oldp=R/'sol61_push/cold_final_mile_2026_10_13/extra_speed_arrival_2026_10_19/receipt.json';old=json.loads(oldp.read_text());checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)});assert v,n
for k,x in a.items():
 if not isinstance(x,dict):continue
 ck(k+' negative beyond two SE',x['E']<=-2*x['se']);ck(k+' class',x['cls']=='OVER-PREDICTS UFDs (needs a core)');ck(k+' count',x['N']==len(x['names']));ck(k+' mutation moves toward law',abs(m[k]['E']-x['E_law_only'])<abs(x['E']-x['E_law_only']))
c=a['canonical|primary (binary-corrected)']['rc_pc'];rows=[]
for r in old['rows']:
 rad=r['radius_pc'];f=rad**2/(rad**2+c*c);v=old['Vx_canonical']*math.sqrt(f);sig=math.sqrt(r['retained_baseline_sigma']**2+v*v/3);ck(r['name']+' core suppresses',0<f<1);rows.append({'name':r['name'],'fraction_of_flat_extra_mass':f,'sigma_pred_kms':sig,'sigma_catalogue_kms':r['catalogue_observed_sigma']})
ck('Draco more suppressed than Fornax',rows[0]['fraction_of_flat_extra_mass']<rows[2]['fraction_of_flat_extra_mass'])
res={'record':'CFG859-arrival-2026-10-19','source_commit':'915b108f8','criteria_commit':'a40dd5cd9','format':'custom stdlib saved-arithmetic audit, not v2','hashes':hs,'committed_matches':matches,'prior_receipt_sha256':hashlib.sha256(oldp.read_bytes()).hexdigest(),'checks':checks,'n_checks':len(checks),'core_pc':c,'rows':rows,'scope':'Saved E/SE/count/control arithmetic and separate capped-retained aperture bridge. No raw binary likelihood, UFD data authentication, post-hoc core optimization, or SPARC rerun. Source uses full exponential law; bridge uses prior capped rational baseline.'};Path('/private/tmp/ce859_receipt.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':rows}))
