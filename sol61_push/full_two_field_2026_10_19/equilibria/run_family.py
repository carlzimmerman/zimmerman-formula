"""Fixed five-case bounded reproduction, no adaptive parameter search."""
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np
from verify_profiles import verify
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--outdir',required=True);a=p.parse_args()
contract=json.loads(Path(a.contract).read_text());out=Path(a.outdir);here=Path(__file__).parent
cases=contract['cases'];records=[];checks=[]
def check(name,ok,value):
 checks.append(dict(name=name,passed=bool(ok),value=value))
 if not ok:raise AssertionError((name,value))
for case in cases:
 name=case['name'];seed=case['seed']
 if seed.startswith('@'):seed=str(out/(seed[1:]+'.npz'))
 output=out/name
 argv=[sys.executable,str(here/'solve_tf_seeded_ekg.py'),'--G',str(case['G']),'--Z',str(case['Z']),'--tol',str(case['tol']),'--z0',str(case['z0']),'--points',str(case['points']),'--seed',seed,'--output',str(output)]
 if case.get('central_h') is not None:argv+=['--central-h',str(case['central_h'])]
 result=subprocess.run(argv,capture_output=True,text=True,timeout=20)
 (out/(name+'_solver.txt')).write_text(result.stdout+'\nSTDERR:\n'+result.stderr)
 if result.returncode:raise RuntimeError((name,result.returncode,result.stdout,result.stderr))
 rec=json.loads(Path(str(output)+'.json').read_text());audit=verify(str(output)+'.npz');rec['audit']=audit;records.append(rec)
 check(name+'_no_horizon',audit['min_N']>0,audit['min_N'])
 check(name+'_field_f_nodeless',audit['f_negative_relative']>-1e-10,audit['f_negative_relative'])
 check(name+'_field_h_nodeless',audit['h_negative_relative']>-1e-10,audit['h_negative_relative'])
 check(name+'_sub_free_mass',audit['mass_over_mQ_gauss']<1,audit['mass_over_mQ_gauss'])
 check(name+'_mass_integral',audit['ADM_integral_relative_error']<2e-7,audit['ADM_integral_relative_error'])
 check(name+'_charge_integral',audit['charge_integral_relative_error']<2e-7,audit['charge_integral_relative_error'])
 check(name+'_physical_ODE_residuals',max(audit['ODE_residuals'].values())<2e-7,audit['ODE_residuals'])
 check(name+'_negligible_outer_mass',abs(audit['tail_mass_fraction'])<1e-9,audit['tail_mass_fraction'])
for ia,ib,label in [(0,1,'tolerance'),(1,2,'outer_domain'),(2,3,'center_start')]:
 changes={k:abs(records[ia][k]/records[ib][k]-1) for k in ['ADM_mass','omega','R99','Q','central_f']}
 check(label+'_refinement',max(changes.values())<1e-5,changes)
final=records[3];check('gradient_branch_local_cap_exceeded',final['audit']['omega_local_center']>final['audit']['omega_cap'],[final['audit']['omega_local_center'],final['audit']['omega_cap']])
summary=dict(status='completed',assertion_tested=contract['mathematics']['assertion_tested'],cases=cases,records=records,checks=checks,non_claims=contract['mathematics']['non_claims'])
(out/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Completed',len(records),'full-field cases;',len(checks),'checks.')
