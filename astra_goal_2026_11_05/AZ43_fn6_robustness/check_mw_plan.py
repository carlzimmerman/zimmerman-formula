#!/usr/bin/env python3
"""Known-answer decisive-gate fixtures and a nonconvergence-as-failure mutation."""
import argparse,copy,hashlib,json,os
from pathlib import Path
import plan_mw as P
parser=argparse.ArgumentParser();parser.add_argument('--mutate',action='store_true');args=parser.parse_args()
checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
a={g:{f:dict(ok=True,evaluable=True) for f in ['canonical','alt']} for g in P.GATES}
pairs={f+'_'+g+'_pair':True for f in ['canonical','alt'] for g in P.GATES}
def decide(a,b,p,foot='canonical'):return P.classify(a,b,p,foot,mutate=args.mutate)
check('all_small_pass_requires_MW',decide(a,a,pairs)['status']=='MW REQUIRED')
for gate in P.GATES:
 b=copy.deepcopy(a);b[gate]['canonical']['ok']=False
 check(gate+'_pass_flip_unresolved',decide(a,b,pairs)['status']=='SMALL GATE UNRESOLVED')
 check(gate+'_stable_failure_decisive',decide(b,b,pairs)['status']=='EXCLUDED BY SMALL GATE')
 q=dict(pairs);q['canonical_'+gate+'_pair']=False
 check(gate+'_nonconverged_failure_not_decisive',decide(b,b,q)['status']=='SMALL GATE UNRESOLVED')
 check(gate+'_footings_not_pooled',decide(b,b,q,'alt')['status']=='MW REQUIRED')
 b[gate]['canonical']['evaluable']=False
 check(gate+'_unevaluable_failure_not_decisive',decide(b,b,pairs)['status']=='SMALL GATE UNRESOLVED')
b=copy.deepcopy(a);b['T1']['canonical']['ok']=False;b['T2']['canonical']['ok']=False
q=dict(pairs);q['canonical_T2_pair']=False
r=decide(b,b,q);check('independent_failure_can_exclude_unresolved',r['status']=='EXCLUDED BY SMALL GATE' and 'T1' in r['decisive_failures'])
check('missing_pair_not_a_verdict',decide(a,None,pairs)['status']=='MISSING SMALL PAIR')
obj=dict(mutate=args.mutate,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(P.__file__)]},scope='Planner fixtures only, no physical verdict. kappa=1/2 FITTED; not theory closed')
path=P.HERE/('mutate/mw_plan_checks.json' if args.mutate else 'main/mw_plan_checks.json');tmp=path.with_suffix('.tmp')
with tmp.open('w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
os.replace(tmp,path);print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c['name'] for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
