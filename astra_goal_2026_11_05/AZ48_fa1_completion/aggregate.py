#!/usr/bin/env python3
"""Authenticate every required physical field and sign twin before convergence grading."""
import argparse,json
from pathlib import Path
import numpy as np
import audit_inputs as A
import convergence as C
import evidence as E
import sampling3d as S

def key_name(source,n,width,foot):return f'{source}_{foot}_n{n}_L{int(width)}'
def sign_twin(main,mutate):
    if main['mutate'] or not mutate['mutate'] or main['field_sha256']!=mutate['field_sha256'] or main['field_identity']!=mutate['field_identity']:return False
    if main['source_hashes']!=mutate['source_hashes'] or main['inherited_threshold']!=mutate['inherited_threshold']:return False
    if 'points' in main:
        return all(mutate['points'][k]['s']==-main['points'][k]['s'] and mutate['points'][k]['norm']==main['points'][k]['norm'] for k in S.POINTS) and all(mutate['discs'][k][i]['mean_s']==-main['discs'][k][i]['mean_s'] for k in S.POINTS for i in [0,1])
    if 's' not in main.get('plummer',{}) or 's' not in mutate.get('plummer',{}):return False
    return np.array_equal(np.asarray(mutate['plummer']['s']),-np.asarray(main['plummer']['s']))

def collect(tree):
    prereq=E.prerequisites();footings={};provenance=[]
    for foot in ['canonical','alt']:
        records={'main':[],'mutate':[]};missing=[];errors=[];twins=[]
        for source,n,width in C.REQUIRED:
            name=key_name(source,n,width,foot);field=tree/'fields'/name;pair={}
            for mode in ['main','mutate']:
                sample=tree/'samples'/mode/name
                required=[field/'result.json',field/'field.npy',field/'checkpoint.npz',sample/'samples.json',sample/'sampling_checkpoint.json']
                absent=[A.relative(p) for p in required if not p.is_file()]
                if absent:missing.append(dict(key=name,mode=mode,files=absent));continue
                try:
                    value,proof=E.authenticate_sample(field,sample)
                    config=value['field_identity']['arguments']
                    if (config['source'],config['n'],config['half_width'],config['foot'])!=(source,n,width,foot):raise E.EvidenceError('Unexpected source/grid/footing in planned role')
                    if value['mutate']!=(mode=='mutate'):raise E.EvidenceError('Wrong mutation mode')
                    pair[mode]=value;records[mode].append(value);provenance.append(proof)
                except (E.EvidenceError,OSError,ValueError,KeyError,TypeError) as exc:errors.append(dict(key=name,mode=mode,error=str(exc)))
            if len(pair)==2:
                try:okay=bool(sign_twin(pair['main'],pair['mutate']))
                except (ValueError,KeyError,TypeError,IndexError):okay=False
                twins.append(dict(key=name,passed=okay))
        all_twins=len(twins)==len(C.REQUIRED) and all(t['passed'] for t in twins)
        eligible=prereq['verified'] and all_twins and not errors and not missing
        footings[foot]=dict(authenticated_main=len(records['main']),authenticated_mutate=len(records['mutate']),required_per_mode=len(C.REQUIRED),missing=missing,errors=errors,sign_twins=twins,main=C.evaluate(records['main'],foot,eligible),mutate=C.evaluate(records['mutate'],foot,eligible))
    return dict(status='INCOMPLETE' if any(f['missing'] for f in footings.values()) else 'EVIDENCE COLLECTED; inspect numerical gates',prerequisites=prereq,footings=footings,provenance=provenance,source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(E.__file__).resolve(),Path(C.__file__).resolve(),Path(S.__file__).resolve(),A.HERE/'FROZEN_BULLET.md',A.HERE/'SAMPLING_CONTRACT.md']},scope='Both footings separate; no physical verdict from missing or stale evidence. MUTATE is the deliberately reversed selector, not an alternative fit. kappa=1/2 FITTED; not theory closed')

def main():
    p=argparse.ArgumentParser();p.add_argument('--tree',default='production');p.add_argument('--tag',default='aggregation');args=p.parse_args()
    tree=(A.HERE/args.tree).resolve();out=(A.HERE/args.tag).resolve()
    if A.HERE.resolve() not in tree.parents or A.HERE.resolve() not in out.parents:raise ValueError('Paths must be within lane')
    obj=collect(tree);A.atomic(out/'result.json',obj)
    print(json.dumps(dict(status=obj['status'],prerequisites=obj['prerequisites']['verified'],footings={f:dict(main=v['authenticated_main'],mutate=v['authenticated_mutate'],required=v['required_per_mode'],numerical_status=v['main']['numerical_status']) for f,v in obj['footings'].items()}),indent=2))
if __name__=='__main__':main()
