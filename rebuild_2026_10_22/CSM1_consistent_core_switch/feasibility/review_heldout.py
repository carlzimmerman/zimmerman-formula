#!/usr/bin/env python3
"""Independent arithmetic review of completed finite artifacts; no model runs."""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REB=ROOT/'rebuild_2026_10_22';CSM=HERE.parent
FILES=[HERE/'HELDOUT_REVIEW_CRITERIA.md',HERE/'review_heldout.py',CSM/'heldout/run_heldout_v4.py',
       CSM/'heldout/run_006_final/results.json',CSM/'heldout/run_006_final/sigma_table.json',
       CSM/'heldout/run_006_final/executed_ho2_source.py',CSM/'heldout/run_006_final/executed_x51_source.py',
       CSM/'heldout/run_006_final/manifest.json',CSM/'calibration/lens_support.json',HERE/'support_001/results.json',
       REB/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',REB/'BS1_basin_switch/bs1_basin_switch_results.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 hashes={str(p.relative_to(ROOT)):sha(p) for p in FILES};result=read(FILES[3]);table=read(FILES[4]);s9=read(FILES[10])['cf_by_mass'];shape=[s9[k] for k in ('1e+12','1e+13','1e+14')];bs=read(FILES[11]);parent=10**bs['LG']['basin']['lgM']
 out=dict(input_sha256=hashes,checks={},levels={})
 def check(k,ok,d):out['checks'][k]=dict(pass_=bool(ok),detail=d);print(k,'PASS' if ok else 'FAIL',json.dumps(d,sort_keys=True),flush=True)
 errors=[];violations=0;parents=[];knots=[]
 for key,entry in result['levels'].items():
  lev=entry['L'];rows=entry['selector_log']['MW']+entry['selector_log']['dwarfs'];worst=0.;bad=0
  for z in rows:
   x=math.log10(z['selected_mass_Msun']);c=lev*float(np.interp(x,[12.,13.,14.],shape))/shape[2];sc=10**float(np.interp(x,table['lg'],table['lsc'][z['background']]));col=4*c**1.25/(3*(3*math.log(2)-math.pi/2))*sc
   worst=max(worst,abs(col/z['column']-1));bad+=int(bool(col>z['floor'])!=z['actual'])
  knots.append(max(abs(a/(lev*b/shape[2])-1) for a,b in zip(entry['cf_table'],shape)))
  errors.append(worst);violations+=bad;parents += [z['selected_mass_Msun']==parent for z in entry['selector_log']['MW']]
  out['levels'][key]=dict(n_selectors=len(rows),column_max_relative_error=worst,branch_violations=bad,MW_floor_by_footing={f:sorted(set(z['floor'] for z in entry['selector_log']['MW'] if z['footing']==f)) for f in ('canonical','alt')},dwarf_floor_by_footing={f:sorted(set(z['floor'] for z in entry['selector_log']['dwarfs'] if z['footing']==f)) for f in ('canonical','alt')})
 check('K0_author_checks',all(result['checks'].values()),result['checks'])
 check('K1_independent_columns',max(errors)<1e-12,dict(max_relative_error=max(errors)))
 check('K2_independent_flags',violations==0,dict(violations=violations,total_selectors=sum(z['n_selectors'] for z in out['levels'].values())))
 check('K3_primary_LG_mass',all(parents),dict(LG_Msun=parent,MW_log_count=len(parents)))
 check('K4_concentration_knots',max(knots)<1e-12,dict(max_relative_error=max(knots)))
 theirs=read(FILES[8]);ours=read(FILES[9]);agreement=[]
 for b in range(4):
  a=ours['support'][str(b)];z=theirs[str(b+1)]
  agreement += [a['positive_weight_lenses']==z['n_positive'],a['native_logMs_min']==z['min_logMstar'],a['native_logMs_max']==z['max_logMstar'],a['support_indices']==z['support_indices']]
 check('K5_independent_lens_support',all(agreement),dict(n_compared_fields=len(agreement)))
 check('K6_inputs_stable',hashes=={str(p.relative_to(ROOT)):sha(p) for p in FILES},'Declared artifacts unchanged')
 out['review_scope']='Independent selector arithmetic and source semantics; raw-data geometry and observational likelihoods not independently rerun.'
 (args.output/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');n=sum(v['pass_'] for v in out['checks'].values());print(f'CSM1_HELDOUT_REVIEW COMPLETE: {n}/{len(out["checks"])} checks PASS.');return 0 if n==len(out['checks']) else 1
if __name__=='__main__':raise SystemExit(main())
