#!/usr/bin/env python3
"""Numerical small-gate pair checks; an incomplete grid has no final label."""
import argparse,json,os
from pathlib import Path
import engines as E
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
HERE=Path(__file__).resolve().parent;mode='mutate' if args.mutate else 'main';out=HERE/mode
results=[]
for index,point in enumerate(E.points()):
    paths=[out/'small'/('p%03d_r%d.json'%(index,r)) for r in [1,2]]
    if not all(p.exists() for p in paths):continue
    raw=[json.loads(p.read_text()) for p in paths];a,b=[v['result'] for v in raw]
    checks=[]
    def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
    for foot in ['canonical','alt']:
        for gate,key in [('T1','Q2'),('T4','Z')]:
            av,bv=a[gate][foot][key],b[gate][foot][key]
            err=abs(av-bv)/max(abs(bv),1e-300)
            check(foot+'_'+gate+'_pair',err<=.02 and a[gate][foot]['ok']==b[gate][foot]['ok'],err)
        old=raw[0]['dwarf_evaluations'];new=raw[1]['dwarf_evaluations']
        relevant=[k for k,v in old.items() if v['footing']==foot]
        missing=[k for k in relevant if k not in new]
        err=max([abs(old[k]['sigma']/new[k]['sigma']-1) for k in relevant if k in new]+[0.])
        check(foot+'_T2_pair',not missing and err<=.01 and set(a['T2'][foot]['passed'])==set(b['T2'][foot]['passed']),dict(max_relative=err,missing=len(missing)))
        err=max(abs(a['T3'][foot][k]-b['T3'][foot][k]) for k in ['d_rms','med'])
        check(foot+'_T3_pair',err<=.001 and a['T3'][foot]['label']==b['T3'][foot]['label'],err)
        check(foot+'_fine_evaluability',all(b[gate][foot]['evaluable'] for gate in ['T1','T2','T3','T4']))
    results.append(dict(index=index,p=point[0],L_MW=point[1],checks=checks,
                        failed=[c['name'] for c in checks if not c['passed']]))
obj=dict(status='INCOMPLETE: no final robustness verdict',pairs=len(results),required_points=len(E.points()),results=results)
mw=[]
for index,point in enumerate(E.points()):
    for foot in ['canonical','alt']:
        paths=[out/'mw'/('%s_p%03d_r%d.json'%(foot,index,r)) for r in [1,2]]
        if not all(p.exists() for p in paths):continue
        a,b=[json.loads(p.read_text()) for p in paths]
        if not a['complete'] or not b['complete']:continue
        checks=[]
        check('cell_grid_identical',a['grid_cells']==b['grid_cells'])
        pair=[]
        for key,ar in a['cells'].items():
            br=b['cells'][key];dk=abs(ar['K0']-br['K0']);dv=abs(ar['vc']-br['vc'])
            flip=ar['all_four']!=br['all_four']
            pair.append(dict(cell=int(key),dK0=dk,dvc=dv,flip=flip,evaluable=dk<=1 and dv<=.3 and not flip,
                             coarse_pass=ar['all_four'],fine_pass=br['all_four']))
        check('V1_both_rungs',all(v['evaluable'] for r in [a,b] for v in r['V1'].values()))
        stable=[r['cell'] for r in pair if r['evaluable'] and r['fine_pass']]
        mw.append(dict(index=index,footing=foot,coarse_passes=len(a['passing']),fine_passes=len(b['passing']),
                       stable_passes=stable,checks=checks,rows=pair))
obj['mw_pairs']=mw
path=out/'small_pair_checks.json';tmp=path.with_suffix('.json.tmp')
with tmp.open('w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
os.replace(tmp,path)
print(json.dumps(dict(pairs=len(results),failed_points=[r['index'] for r in results if r['failed']],
                     mw_pairs=[dict(index=r['index'],footing=r['footing'],stable=len(r['stable_passes'])) for r in mw]),indent=2))
