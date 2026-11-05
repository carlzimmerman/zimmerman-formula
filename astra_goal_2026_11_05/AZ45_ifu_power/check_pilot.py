#!/usr/bin/env python3
"""Report all four pilot pairs, including an unresolved mutation."""
import json
import engine as E
rows=[]
for mode in ['reference','double','main','mutate']:
    values=[]
    for rung in [1,2]:
        key=f't00_r{rung}_canonical_n0_flat_s30_free_{mode}_0.01.json'
        obj=json.loads((E.HERE/'pilot'/mode/key).read_text())
        if obj['identity']['sources']!=E.hashes():raise RuntimeError('Stale pilot sources')
        values.append(obj['scientific'])
    a,b=values;change=abs(a['delta']-b['delta'])
    rows.append(dict(mode=mode,coarse_delta=a['delta'],fine_delta=b['delta'],delta_change=change,
                     passed=change<=.01 and a['resolved'] and b['resolved']))
E.atomic(E.HERE/'pilot_pairs.json',dict(scope='One canonical template only; no population verdict',rows=rows))
print(json.dumps(rows,indent=2));raise SystemExit(int(not all(r['passed'] for r in rows)))
