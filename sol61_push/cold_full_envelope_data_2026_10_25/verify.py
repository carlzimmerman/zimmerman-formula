"""Independent controls, mutation, raw-result invariants and current-hash verification."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,hashlib,json,pathlib,resource,subprocess,sys,time,unittest
import numpy as np
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();dest=pathlib.Path(args.out);dest.mkdir(exist_ok=True,parents=True);assert not (dest/'result.json').exists();start=time.time();records=[]
 def check(label,value):
  assert bool(value),label;records.append(label)
 suite=unittest.TestSuite()
 for name in ['test_physics','test_likelihood_v2','test_response']:suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))
 result=unittest.TextTestRunner(verbosity=2).run(suite);check('seven independent physics, likelihood, virial and response tests',result.wasSuccessful() and result.testsRun==7)
 import fit,fit_v2
 d=dict(v=np.array([2.]),ev=np.array([0.]),lo=np.array([-5.]),hi=np.array([5.]),logprior=np.zeros((1,2)));var=np.array([[16.,400.]])
 wrong=fit.nll(d,var,0.,np.log(9.));right=fit_v2.nll(d,var,0.,np.log(9.));check('old mixture normalization mutation detected',abs(wrong-right)>.001)
 canonical=json.loads((P/'fit_002/result.json').read_text());co=json.loads((P/'core_001/result.json').read_text());frac=json.loads((P/'core_fraction_001/result.json').read_text());response=json.loads((P/'response_002/result.json').read_text());hst=json.loads((P/'hst_002/result.json').read_text())
 for n,N in [('Draco',458),('Sextans',298),('Fornax',807),('Leo I',299)]:
  ds=canonical['datasets'][n];check(n+' selected unique source count',len(ds['ids'])==len(set(ds['ids']))==N==len(ds['R_pc'])==len(ds['vel_kms'])==len(ds['error_kms']))
 check('all baseline Plummer fits converged',all(x['free_Plummer']['optimizer_success'] for x in canonical['rows']))
 check('all shared-scale fits converged',all(x['optimizer_success'] for x in canonical['shared_scale_tests']))
 check('projection refinements below0.13percent',max(canonical['checks'].values())<.0013)
 for row in canonical['rows']:
  for p in row['trial_profiles']:check('failed evolved F/Leo endpoints excluded '+p['tag'],not (row['name'] in ['Fornax','Leo I'] and 'late' in p['tag']))
 for row in co['rows']:
  for e in row['core_plus_envelope']:
   check('core plus envelope counted once '+row['name'],abs((e['cold_mass_Msun']+row['core_Msun'])/e['total_Msun']-1)<1e-12 and e['minimum_added_variance_kms2']>=0)
 for row in frac['rows']:
  check('21 coefficient points '+row['name'],len(row['grid'])==21)
  for g in row['grid']:check('redistribution leaves same total '+row['name'],abs((g['cold_mass_Msun']+g['central_cut_Msun'])/row['total_Msun']-1)<1e-12)
 for c in frac['endpoint_checks']:check('c0/c1 exact previous fit '+c['name'],max(c['c0_nll_match'],c['c1_nll_match'])<1e-6)
 check('response exact50cases',len(response['rows'])==50)
 old=json.loads((P/'response_001/result.json').read_text())
 for row,prior in zip(response['rows'],old['rows']):
  witness=row['worst_star_witness'];check('worst-star work witness '+row['name'],len(witness['normalized_residual'])==601 and max(abs(x) for x in witness['normalized_residual'])==row['work_ledger_max_relative'])
  check('response repeat numeric identity '+row['name'],all(row[k]==prior[k] for k in ['late_r50_ratio','late_variance_ratio','work_ledger_max_relative']))
  check('stellar source-work ledger '+row['name'],row['work_ledger_max_relative']<1e-5)
  if row['epsilon']==0:check('static stars stationary '+row['name'],max(abs(row['late_r50_ratio']-1),abs(row['late_variance_ratio']-1))<1e-7)
 check('five tight response repeats',len(response['refinement'])==5 and max(max(x['r50_relative'],x['variance_relative']) for x in response['refinement'])<1e-4)
 check('HST author release MD5 matched',hst['download']['md5_matches_published'])
 check('20 HST screens',len(hst['rows'])==20)
 check('independent LOS PM-projector agreement',hst['LOS_projection_control_max']<1e-12)
 for row in hst['rows']:
  rr=np.array(row['standardized_residual']);check('five PM bins, no extra LOS bins',rr.shape==(5,2) and abs(float((rr*rr).sum())-row['sum_squared_residual'])<1e-10)
 manifests=[];validator='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py'
 tags=['fit_001','fit_002','response_001','response_002','core_001','core_fraction_001','hst_001','hst_002'];peaks=[]
 for tag in tags:
  manifest=P/tag/'manifest.json';q=subprocess.run(['/opt/homebrew/bin/python3',validator,str(manifest),'--root',str(ROOT)],capture_output=True,text=True);check('manifest current hashes '+tag,q.returncode==0);m=json.loads(manifest.read_text());check('run completed '+tag,m['run']['status']=='completed');raw=json.loads((P/tag/'result.json').read_text());check('producer before/after unchanged '+tag,raw['inputs_before']==raw['inputs_after']);peaks.append(raw['peak_RSS_bytes']);manifests.append(dict(path=str(manifest.relative_to(ROOT)),sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),validation_stdout=q.stdout))
 check('all reported producers below750MB',max(peaks)<750_000_000)
 out=dict(status='finite controls and provenance passed; not four-dwarf closure',checks=records,count=len(records),unit_tests=result.testsRun,old_mixture_mutation_absolute_nll_difference=abs(wrong-right),manifests=manifests,maximum_reported_producer_RSS_bytes=max(peaks),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (dest/'result.json').write_text(json.dumps(out,indent=2)+'\n');print('VERIFIED',len(records),'checks,',max(peaks),'maximum reported producer bytes',flush=True)
if __name__=='__main__':main()
