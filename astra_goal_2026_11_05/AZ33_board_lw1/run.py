#!/usr/bin/env python3
"""Integration checks: catch omitted forms, stale verdicts and lost sources."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'explainers'))
import make_status_board as board
ap=argparse.ArgumentParser()
ap.add_argument('--mutate',action='store_true')
ap.add_argument('--output',default=None)
args=ap.parse_args()
tiles=copy.deepcopy(board.LAW_TILES)
by={t['name']:t for t in tiles}
if args.mutate:
    by['MW vertical force'].setdefault('forms',{}).pop('R',None)
checks={}
checks['clean_guard']=not board.check_law(tiles)
checks['X_FAIL_both']=by['X-COP']['st']=='FAIL' and by['X-COP']['alt'] in (None,'FAIL')
expected={'MW vertical force':{'A':{'canonical':'FAIL','alt':'FAIL'},'R':{'canonical':'PASS','alt':'PASS'}},
          'DiskMass':{'A':{'canonical':'STALE','alt':'STALE'},'R':{'canonical':'FAIL','alt':'FAIL'}}}
for name, forms in expected.items():
    checks[name+'_forms']=by[name].get('forms')==forms
    for form in ('A','R'):
        broken=copy.deepcopy(tiles)
        board._by(broken,name).setdefault('forms',{}).pop(form,None)
        checks[name+'_missing_'+form+'_caught']=bool(board.check_law(broken))
        broken=copy.deepcopy(tiles)
        board._by(broken,name).setdefault('forms',{}).setdefault(form,{})['alt']='OPEN'
        checks[name+'_wrong_'+form+'_alt_caught']=bool(board.check_law(broken))
for name in ('X-COP','Local Group dwarfs (five classes)','Cluster keys (15, old template)'):
    broken=copy.deepcopy(tiles); board._by(broken,name)['st']='PASS'
    checks[name+'_false_pass_caught']=bool(board.check_law(broken))
broken=copy.deepcopy(tiles); board._by(broken,'X-COP')['st']='STALE'
checks['X_back_to_grey_caught']=bool(board.check_law(broken))
for name in ('MW vertical force','DiskMass','X-COP'):
    broken=copy.deepcopy(tiles); board._by(broken,name)['lw1']=None
    checks[name+'_override_dropped_caught']=bool(board.check_law(broken))
    checks[name+'_source_present']='LW1' in by[name]['lanes']
lw1=json.loads((ROOT/'rebuild_2026_10_22/LW1_law_scorecard/lw1_results.json').read_text())
counts={}
for key,row in lw1['keys'].items():
    z=[r['Z'] for r in row['cells'].values()]
    count=sum(all(abs(r[k])<=2 for r in z) for k in z[0])
    counts[key]=count
    checks['raw_key_count_'+key]=count==row['n']==10
checks['all_FG1_lines']=set(board.FG1_LINES)<={t['fg1'] for t in tiles}
checks['MUST_STAY_RED']=all(by[n]['st']=='FAIL' for n in board.MUST_STAY_RED)
result=dict(label='PASS' if all(checks.values()) else 'FAIL',checks=checks,raw_counts=counts,
            errors=board.check_law(tiles),mutate=args.mutate,
            inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                (Path(__file__),HERE/'FROZEN_CRITERIA.md',ROOT/'explainers/make_status_board.py',
                 ROOT/'rebuild_2026_10_22/LW1_law_scorecard/lw1_results.json')},
            scope='board integration only; no physical verdict regraded',
            statement='kappa = 1/2 FITTED; not theory closed')
path=HERE/(args.output or ('mutate_results.json' if args.mutate else 'main_results.json'))
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(0 if result['label']=='PASS' else 1)
