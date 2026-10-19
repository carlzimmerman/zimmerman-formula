"""Collect PLAN C3 (NR-GPP stability along the fixed-f_c path) into a table + criteria."""
import glob, json, math, os, re
import numpy as np
from common import dump

recs = {}
for fn in sorted(glob.glob('results/partC3/*.json')):
    if 'summary' in fn:
        continue
    r = json.load(open(fn))
    recs[os.path.basename(fn)[:-5]] = r
merged = {}
for tag, r in sorted(recs.items()):          # '_a' (l=0,1,2 + VK) sorts before '_b' (l=3,4)
    key = (r['gamma'], r['N'])
    if key not in merged:
        merged[key] = dict(r, sectors=list(r['sectors']), tags=[tag])
    else:
        merged[key]['sectors'] += r['sectors']
        merged[key]['tags'].append(tag)
        merged[key]['peak_rss_MB'] = max(merged[key]['peak_rss_MB'], r['peak_rss_MB'])
by_G = {}
for (G, N), r in merged.items():
    r['sectors'] = sorted(r['sectors'], key=lambda s: s['l'])
    by_G.setdefault(G, []).append((N, ','.join(r['tags']), r))
s2_by_l = {}
rows = []
res_ok = True
for G in sorted(by_G, reverse=True):
    runs = sorted(by_G[G])
    fine = runs[-1][2]
    coarse = runs[0][2] if len(runs) > 1 else None
    row = dict(Gamma=G, N=[x[0] for x in runs], H1=fine['background']['H1'], vk=fine.get('vakhitov_kolokolov', {}).get('dN_dmu'),
               newton_rel=fine['newton']['rel'], f_at_box=fine['background']['H1']['f_at_box_over_fc'],
               rbox=fine['rbox'], dr=[x[2]['dr'] for x in runs], peak_rss_MB=max(x[2]['peak_rss_MB'] for x in runs),
               N_charge=fine['background']['N_charge'], mu=fine['background']['mu'], R99=fine['background']['R99'], sectors={})
    for s in fine['sectors']:
        l = s['l']
        idx = [1, 2] if l == 1 else [0, 1]
        for n in idx:
            key = f'{l}_{n}'
            s2_by_l.setdefault(key, {})[f'{G:.3e}'] = s['s2_natural'][n]
        rel = None
        if coarse is not None:
            cs = [c for c in coarse['sectors'] if c['l'] == l][0]
            rel = [abs(s['s2_natural'][n] / cs['s2_natural'][n] - 1) for n in idx]
            res_ok &= all(x <= 1e-2 for x in rel)
        row['sectors'][l] = dict(s2=[s['s2_natural'][n] for n in idx], resolution_rel=rel,
                                 translation=(s['s2_natural'][0] if l == 1 else None),
                                 n_neg_Splus=s['Splus_negative_count'],
                                 Splus_constrained_min=(s.get('Splus_constrained_lowest') or [None])[0])
    rows.append(row)
allpos = all(all(x > 0 for x in rw['sectors'][l]['s2']) for rw in rows for l in rw['sectors'])
h1 = all(rw['H1']['f_positive'] and rw['H1']['x_positive'] and rw['H1']['f_decreasing'] and rw['H1']['x_decreasing'] for rw in rows)
out = dict(rows=rows, s2_by_l=s2_by_l, all_monitored_s2_positive=allpos, two_resolution_agreement_1em2=res_ok, H1_all=h1,
           n_neg_Splus_l0=[rw['sectors'][0]['n_neg_Splus'] for rw in rows], dN_dmu=[rw['vk'] for rw in rows])
dump('results/partC3/summary_C3.json', out)
print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))
