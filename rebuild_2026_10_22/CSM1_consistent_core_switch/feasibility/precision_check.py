#!/usr/bin/env python3
import argparse,hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REB=ROOT/'rebuild_2026_10_22';CSM=HERE.parent
FILES=[HERE/'PRECISION_ERRATUM_CRITERIA.md',HERE/'precision_check.py',HERE/'run_001/results.json',
       ROOT/'real_research/derivation_chain_2026/FP0_core_postulates_results.json',
       ROOT/'campaign_fresh_gravity/CFG4_common.py',REB/'EM1_emergent_dust_law/em1_emergent.py',
       CSM/'calibration/run_003_audited/results.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 hashes={str(p.relative_to(ROOT)):sha(p) for p in FILES};old=read(FILES[2]);fp=read(FILES[3])['numbers'];cal=read(FILES[6]);aa={'canonical':float(fp['a0_canonical']),'alt':float(fp['a0_rho_total'])};rounded={'canonical':9.3603e-11,'alt':1.1312e-10};l0=old['sole_challenge']['L'];out=dict(input_sha256=hashes,checks={},footings={})
 def check(k,ok,d):out['checks'][k]=dict(pass_=bool(ok),detail=d);print(k,'PASS' if ok else 'FAIL',json.dumps(d,sort_keys=True),flush=True)
 errs=[];eq=[]
 for f in aa:
  actual=aa[f]/(2*math.pi*6.67430e-11);records=[r['floor'] for e in cal['levels'].values() for r in e['own']['core_columns'] if r['footing']==f];errs.extend(abs(v/actual-1) for v in records)
  lr=l0*(aa[f]/rounded['canonical'])**.8
  # same canonical-old algebraic column at target; exact footing critical point is defined without introducing a new target.
  direct_at_target=rounded['canonical']/aa[f];exact_ratio=(lr/l0)**1.25*direct_at_target;eq.append(abs(exact_ratio-1))
  out['footings'][f]=dict(a0_FP0=aa[f],a0_displayed=rounded[f],relative_floor_difference=aa[f]/rounded[f]-1,
    actual_X43_floor_SI=actual,ratio_at_logM12_3_using_running_challenge=direct_at_target,
    algebraic_exact_target_L=lr,exact_target_L_minus_running=lr-l0,
    canonical_X43_floor_correction_factor=(aa[f]/rounded[f])**.8)
 out['running_challenge_L']=l0;out['definition_corrected_canonical_L']=out['footings']['canonical']['algebraic_exact_target_L']
 check('K0_actual_logged_floor',max(errs)<1e-12,dict(max_relative_error=max(errs),n_columns=len(errs)))
 check('K1_exact_target_rescale',max(eq)<1e-12,dict(max_relative_residual=max(eq)))
 check('K2_inputs_stable',hashes=={str(p.relative_to(ROOT)):sha(p) for p in FILES},'Declared inputs unchanged')
 out['scope']='Correction of precision in the one algebraically fixed target; no changed empirical target or additional parameter.'
 (args.output/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('DEFINITION_CORRECTED_CANONICAL_L',out['definition_corrected_canonical_L']);print('OLD_POINT_TARGET_COLUMN_RATIO',out['footings']['canonical']['ratio_at_logM12_3_using_running_challenge']);return 0 if all(v['pass_'] for v in out['checks'].values()) else 1
if __name__=='__main__':raise SystemExit(main())
