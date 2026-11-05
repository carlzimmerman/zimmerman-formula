#!/usr/bin/env python3
"""Classify required MW work under frozen decisive-gate rules, never a final verdict."""
import argparse,hashlib,json,os
from pathlib import Path
import engines as E
HERE=Path(__file__).resolve().parent
GATES=['T1','T2','T3','T4']
def classify(coarse,fine,pairs,foot,mutate=False):
    if coarse is None or fine is None:return dict(status='MISSING SMALL PAIR',decisive_failures=[],unresolved=GATES)
    decisive=[];unresolved=[];passed=[]
    for gate in GATES:
        a,b=coarse[gate][foot],fine[gate][foot]
        numerical=bool(pairs.get(foot+'_'+gate+'_pair',False)) and a['evaluable'] and b['evaluable']
        if numerical and a['ok'] and b['ok']:passed.append(gate)
        elif (numerical or mutate) and not a['ok'] and not b['ok']:decisive.append(gate)
        else:unresolved.append(gate)
    status='EXCLUDED BY SMALL GATE' if decisive else ('MW REQUIRED' if len(passed)==4 else 'SMALL GATE UNRESOLVED')
    return dict(status=status,decisive_failures=decisive,unresolved=unresolved)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['main','mutate'],required=True);args=parser.parse_args()
    folder=HERE/args.mode;auditpath=folder/'small_pair_checks.json';audit=json.loads(auditpath.read_text())
    indexed={r['index']:r for r in audit['results']}
    if len(indexed)!=len(audit['results']):raise ValueError('Duplicate pair index')
    expected=E.hashes()
    for name in ['small_worker.py','engines.py','FROZEN_CRITERIA.md']:expected[name]=sha(HERE/name)
    inputs={str(auditpath.relative_to(E.ROOT)):sha(auditpath)};rows=[]
    for index,(p,width) in enumerate(E.points()):
        paths=[folder/'small'/('p%03d_r%d.json'%(index,r)) for r in [1,2]]
        raw=[]
        for path in paths:
            if path.exists():
                obj=json.loads(path.read_text())
                if obj['source_hashes']!=expected:raise ValueError('Stale small engine')
                if obj['result']['p']!=p or obj['result']['L_MW']!=width:raise ValueError('Wrong parameter point')
                if not all(c['passed'] for c in obj['checks']):raise ValueError('Known-answer failure')
                inputs[str(path.relative_to(E.ROOT))]=sha(path);raw.append(obj['result'])
            else:raw.append(None)
        if all(v is not None for v in raw) and index not in indexed:raise ValueError('Refresh pair audit before planning')
        if any(v is None for v in raw) and index in indexed:raise ValueError('Pair audit refers to absent raw output')
        pair=indexed.get(index,{})
        if pair and (pair['p']!=p or pair['L_MW']!=width):raise ValueError('Wrong pair identity')
        checks={c['name']:c['passed'] for c in pair.get('checks',[])}
        for foot in ['canonical','alt']:
            decision=classify(*raw,checks,foot)
            rows.append(dict(index=index,p=p,L_MW=width,footing=foot,**decision))
    counts={foot:{status:sum(r['footing']==foot and r['status']==status for r in rows) for status in ['MW REQUIRED','EXCLUDED BY SMALL GATE','SMALL GATE UNRESOLVED','MISSING SMALL PAIR']} for foot in ['canonical','alt']}
    obj=dict(mode=args.mode,status='WORK PLAN ONLY: no final robustness verdict',counts=counts,rows=rows,input_hashes=inputs,source_hashes={str(p.relative_to(E.ROOT)):sha(p) for p in [Path(__file__).resolve(),HERE/'engines.py',HERE/'FROZEN_CRITERIA.md',HERE/'check_pairs.py']},scope='Independent decisive small-gate failures may exclude a point despite another unresolved gate. MW REQUIRED is not a physical pass. kappa=1/2 FITTED; not theory closed')
    path=folder/'mw_work_plan.json';tmp=path.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path);print(json.dumps(counts,indent=2))
if __name__=='__main__':main()
