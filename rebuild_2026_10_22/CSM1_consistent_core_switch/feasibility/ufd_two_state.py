#!/usr/bin/env python3
"""Two fixed class residual states; no observational harness or L scan."""
import argparse,ast,hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REB=ROOT/'rebuild_2026_10_22';CSM=HERE.parent
FILES=[HERE/'UFD_TWO_STATE_CRITERIA.md',HERE/'ufd_two_state.py',CSM/'heldout/run_heldout_v4.py',
       CSM/'heldout/run_006_final/executed_x51_source.py',CSM/'heldout/run_006_final/results.json',
       REB/'BS1_basin_switch/bs1_basin_switch.py',REB/'BS1_basin_switch/bs1_basin_switch_results_MUTATE.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 hashes={str(p.relative_to(ROOT)):sha(p) for p in FILES};j=read(FILES[4]);mut=read(FILES[6]);out=dict(input_sha256=hashes,checks={},states={},rng=dict(generator='numpy PCG64',seed=20261026,n_resamples=10000))
 def check(k,ok,d):out['checks'][k]=dict(pass_=bool(ok),detail=d);print(k,'PASS' if ok else 'FAIL',json.dumps(d,sort_keys=True),flush=True)
 cls='MW ultra-faint';parent=10**j['LG']['basin']['lgM'];memberok=[];uniform=[];same=[];diff=[]
 for f,a0 in (('canonical',9.3603e-11),('alt',1.1312e-10)):
  ref=[r for r in j['levels']['3.75']['dwarfs']['rows'][f] if r['cls']==cls];names={r['name'] for r in ref};memberok += [r['host']=='MW' for r in ref]
  for lev,cell in j['levels'].items():
   now=[r for r in cell['dwarfs']['rows'][f] if r['cls']==cls]
   same.append([{k:r[k] for k in ('name','host','gN','gh','gobs','s')} for r in now]==[{k:r[k] for k in ('name','host','gN','gh','gobs','s')} for r in ref])
   logs=[z for z in cell['selector_log']['dwarfs'] if z['footing']==f and z['name'] in names];uniform.append(len(logs)==len(ref) and all(z['selected_mass_Msun']==parent and z['background']=='A_c2b_refit' and z['in_LG'] for z in logs) and len(set(z['floor'] for z in logs))==1 and len(set(z['actual'] for z in logs))==1)
  gN=np.array([r['gN'] for r in ref]);gh=np.array([r['gh'] for r in ref]);obs=np.array([r['gobs'] for r in ref]);err=np.array([r['s'] for r in ref]);states={}
  for lab,gp in (('halo',gN+gh),('law',gN*(.5+np.sqrt(.25+a0/gN)))):
   residual=np.log10(obs/gp);rng=np.random.default_rng(20261026);ix=rng.integers(0,len(ref),(10000,len(ref)));med=float(np.median(residual));sd=float(np.std(np.median(residual[ix]+err[ix]*rng.standard_normal((10000,len(ref))),axis=1)));z=med/sd
   reference=j['levels']['3.75']['dwarfs']['footings'][f]['classes'][cls]['Z'] if lab=='halo' else mut['primary']['grade'][f]['dwarfs'][cls]['Z'];diff.append(abs(z-reference));states[lab]=dict(n=len(ref),median=med,sd=sd,Z=z,pass_=abs(z)<2,reference_Z=reference,residuals=residual.tolist())
  out['states'][f]=dict(members=[r['name'] for r in ref],states=states,both_states_fail=all(not v['pass_'] for v in states.values()),all_positive_L_excluded_by_this_class=all(not v['pass_'] for v in states.values()))
 check('K0_MW_membership',all(memberok),dict(class_members_per_footing={f:len(e['members']) for f,e in out['states'].items()}))
 check('K1_uniform_LG_selectors',all(uniform),dict(n_footing_level_checks=len(uniform),LG_Msun=parent))
 check('K2_profile_L_independence_witness',all(same),dict(n_footing_level_checks=len(same),source_argument='Executed X51 prefix has fixed atomic8 halo/floor inputs; L only reaches branch callback.'))
 check('K3_reproduce_both_states',max(diff)<1e-10,dict(max_abs_Z_error=max(diff)))
 src=FILES[3].read_text();tree=ast.parse(src);rowfn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='rows');calls=[n for n in ast.walk(rowfn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='CSM_DFLAG'];clsnode=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CLS' for t in n.targets));classorder=ast.literal_eval(clsnode.value)
 check('K4_source_state_reduction',len(calls)==1 and classorder[0]==cls and 'gp = gN + G * Mh / r12 ** 2 if above else' in src,dict(callback_calls=len(calls),first_bootstrap_class=classorder[0]))
 check('K5_inputs_stable',hashes=={str(p.relative_to(ROOT)):sha(p) for p in FILES},'All declared artifacts unchanged')
 out['scope']='Exhaustive over L only because fixed-profile MW UFD class shares one LG flag; does not constrain a revised cooling profile, class data, basin model or extra parameter.'
 (args.output/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');n=sum(v['pass_'] for v in out['checks'].values());print(f'CSM1_UFD_TWO_STATE COMPLETE: {n}/{len(out["checks"])} checks PASS.');return 0 if n==len(out['checks']) else 1
if __name__=='__main__':raise SystemExit(main())
