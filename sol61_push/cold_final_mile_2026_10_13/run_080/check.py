from pathlib import Path
import json,math,hashlib,subprocess,sys,time
root=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');out=Path(__file__).parent;t=time.time();b=root/'sol61_push/cold_final_mile_2026_10_13'
paths=['campaign_fresh_gravity/CFG822_hex_dsph/cfg822_results.json','campaign_fresh_gravity/CFG822_hex_dsph/cfg822.out','campaign_fresh_gravity/CFG822_hex_dsph/cfg822.py','campaign_fresh_gravity/CFG822_hex_dsph/FROZEN_CRITERIA.md','sol61_push/cold_final_mile_2026_10_13/run_077/results.json','campaign_fresh_gravity/CFG821_stiffness_from_dsph/cfg821_results.json']
hashes={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths};src=json.loads((root/paths[0]).read_text());old=json.loads((root/paths[4]).read_text());c821=json.loads((root/paths[5]).read_text())
import csv
errs={}
for r in csv.DictReader((root/'real_research/data/dsph/lvd_dwarf_mw.csv').open()):
 try:errs[r['name']]=float(r['vlos_sigma_em'])/float(r['vlos_sigma'])
 except:pass
checks=[]
def ck(n,x):
 checks.append({'name':n,'pass':bool(x)})
 if not x:raise AssertionError(n)
res={}
for foot in ['canonical','alt']:
 chi=0;rows=[]
 for x in old['dwarfs']:
  y=src['rows'][foot+'|'+x['name']];obs=x['sigma_obs_kms'];pred=y['sig'];D=x['Mdyn_in_r12_over_Mb'];free=y['free_in_r12_over_Mb'];tot=D*(pred/obs)**2;base=tot-free;target=D-base
  ck(foot+x['name']+' inferred nonnegative base',base>=0)
  con=math.log(obs/pred)**2/(errs.get(x['name'],.1)**2+(math.log(10)*.15/2)**2);chi+=con
  ck(foot+x['name']+' enclosed-free below total-stock',0<=free<=53.64*y['free_frac'])
  rows.append({'name':x['name'],'sigma_obs':obs,'sigma_pred':pred,'chi2':con,'inferred_core_plus_settled_over_Mb':base,'actual_free_inside_over_Mb':free,'required_free_inside_signed_over_Mb':target,'target_over_actual_free':target/free,'extra_inner_mass_needed_over_Mb':D-tot})
 ck(foot+' chi2 independently replayed',abs(chi-src[foot]['chi2'])<1e-10)
 res[foot]={'chi2':chi,'old_unscreened_chi2':c821['isolated law|'+foot]['chi2_unscreened'],'improvement_vs_821':c821['isolated law|'+foot]['chi2_unscreened']-chi,'rows':rows}
ck('source unchanged',hashes=={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths})
result={'claim_id':'CE-FM-080','status':'completed','all_pass':all(c['pass'] for c in checks),'n_checks':len(checks),'checks':checks,'results':res,'scope':'Independent score and enclosed-mass reconstruction from saved CFG822 rows; no MethodA dynamics rerun; mutation/raw trajectory/conservation not newly certified.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
receipt={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'command':['python3',str(Path(__file__))],'software':sys.version,'input_sha256':hashes,'inputs_unchanged':True,'seconds':time.time()-t,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'result_sha256':hashlib.sha256((out/'results.json').read_bytes()).hexdigest(),'format':'custom execution receipt; not a mathbox-v2 runner manifest'}
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'n_checks':len(checks),'results':res},indent=2))
