#!/usr/bin/env python3
"""Fixed algebraic LG switch thresholds, with cached law-branch scores separated."""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REB=ROOT/'rebuild_2026_10_22';CSM=HERE.parent
FILES=[HERE/'LG_BOUND_CRITERIA.md',HERE/'lg_lower_bound.py',CSM/'heldout/run_006_final/results.json',
       CSM/'heldout/run_006_final/sigma_table.json',REB/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',
       REB/'BS1_basin_switch/bs1_basin_switch.py',REB/'BS1_basin_switch/bs1_basin_switch_results.json',
       REB/'BS1_basin_switch/bs1_basin_switch_results_MUTATE.json',HERE/'support_001/results.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 hashes={str(p.relative_to(ROOT)):sha(p) for p in FILES};held=read(FILES[2]);table=read(FILES[3]);s9=read(FILES[4])['cf_by_mass'];shape=[s9[k] for k in ('1e+12','1e+13','1e+14')];bs=read(FILES[6]);mut=read(FILES[7]);upper=read(FILES[8]);x=bs['LG']['basin']['lgM'];q=float(np.interp(x,[12.,13.,14.],shape))/shape[2];amp=4/(3*(3*math.log(2)-math.pi/2));rows=held['levels']['3.75']['selector_log']
 out=dict(input_sha256=hashes,checks={},LG_logM=x,thresholds={},conditional_necessary_interval={},cached_law_failures={})
 def check(k,ok,d):out['checks'][k]=dict(pass_=bool(ok),detail=d);print(k,'PASS' if ok else 'FAIL',json.dumps(d,sort_keys=True),flush=True)
 check('K0_LG_mass',abs(x-held['LG']['basin']['lgM'])<=1e-12,dict(logM=x,M=10**x))
 identity=[];branches=[];floorunique=[]
 for f in ('canonical','alt'):
  out['thresholds'][f]={}
  for kind,tags in (('MW',('A_c2b_refit','B_cfg886_bg')),('dwarfs',('A_c2b_refit',))):
   out['thresholds'][f][kind]={}
   for tag in tags:
    floors=sorted(set(z['floor'] for z in rows[kind] if z['footing']==f and z['background']==tag));floorunique.append(len(floors)==1);floor=floors[0];s=10**float(np.interp(x,table['lg'],table['lsc'][tag]));lc=(floor/(amp*s))**.8/q;ratio=lambda l:amp*(l*q)**1.25*s/floor
    identity.append(abs(ratio(lc)-1));branches.extend([ratio(lc*(1-1e-6))<1,ratio(lc*(1+1e-6))>1]);out['thresholds'][f][kind][tag]=dict(Lcrit=lc,floor=floor,Sigma_coll=s)
  mw=mut['primary']['mw'][f];dw=mut['primary']['grade'][f]['dwarfs']['MW ultra-faint'];out['cached_law_failures'][f]=dict(MW_branches=mw['branches'],MW_class=mw['cls'],MW_VK_cells=mw['n_L1_L2a_L2b'],UFD_Z=dw['Z'],provenance='Original BS1 flag-inversion output; law-branch scores independent of L')
  lower=max(out['thresholds'][f][kind]['A_c2b_refit']['Lcrit'] for kind in ('MW','dwarfs'));cap=upper['bound'][f]['necessary_L_upper_bound'];out['conditional_necessary_interval'][f]=dict(L_strict_lower=lower,L_inclusive_upper=cap,nonempty=lower<cap)
 check('K1_unique_actual_floors',all(floorunique),dict(n_subsystem_footing_backgrounds=len(floorunique)))
 check('K2_algebraic_thresholds',max(identity)<1e-12,dict(max_relative_residual=max(identity)))
 check('K3_threshold_sides',all(branches),dict(n_side_checks=len(branches)))
 check('K4_cached_law_failures',all(z['MW_branches']=={'law':175,'route E':0} and z['MW_VK_cells']==0 and abs(z['UFD_Z'])>=2 for z in out['cached_law_failures'].values()),out['cached_law_failures'])
 check('K5_inputs_stable',hashes=={str(p.relative_to(ROOT)):sha(p) for p in FILES},'All declared artifacts unchanged')
 out['scope']='Conditional necessary interval only; cached law scores inherited. It neither selects L nor proves there is a passing L inside.'
 (args.output/'results.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');n=sum(v['pass_'] for v in out['checks'].values());print(f'CSM1_LG_BOUND COMPLETE: {n}/{len(out["checks"])} checks PASS.');return 0 if n==len(out['checks']) else 1
if __name__=='__main__':raise SystemExit(main())
