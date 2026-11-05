#!/usr/bin/env python3
"""Six relativity claims must use the new audit and retain scope qualifiers."""
import argparse
import copy
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'explainers'))
import make_status_board as b
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');ap.add_argument('--output',required=True)
args=ap.parse_args()
tiles=copy.deepcopy(b.LAW_TILES);by={t['name']:t for t in tiles}
if args.mutate:
    by['Matter conservation (G9)']['note']='Conservation holds off shell.'
expected={'Binary pulsars + GW170817':('UNDEC','full radiation'),
          'Leaf problem well-posed':('UNDEC','existence'),
          'Causality: criterion A / B':('UNDEC','retarded response'),
          'Strong coupling':('COND','estimate'),
          'Matter conservation (G9)':('PASS','matter-shell'),
          'Black holes (EHT, LIGO ringdown)':('COND','static')}
checks={'clean_guard':not b.check_law(tiles)}
for name,(status,qualifier) in expected.items():
    t=by[name]
    checks[name+'_source']='AZ34' in t['lanes'] and not t['carried']
    checks[name+'_scope']=qualifier in t['note']
    checks[name+'_status']=t['st']==status
    broken=copy.deepcopy(tiles);b._by(broken,name)['lanes']=[x for x in t['lanes'] if x!='AZ34']
    checks[name+'_source_removal_caught']=bool(b.check_law(broken))
checks['off_shell_claim_removed']='holds off shell' not in by['Matter conservation (G9)']['note']
checks['no_radiative_channel_removed']='no radiative channel' not in by['Binary pulsars + GW170817']['note']
result=dict(checks=checks,errors=b.check_law(tiles),mutate=args.mutate)
(HERE/args.output).write_text(json.dumps(result,indent=2)+'\n')
print(sum(checks.values()),'/',len(checks),result['errors'])
raise SystemExit(0 if all(checks.values()) else 1)
