"""Compare AC13 stress rows: legacy pol_on 0.64 (stored) vs corrected 0.81 (reruns/ac13_stress).
R uses AC13 grade.py's definition (max_I, max_II over the stored gr row at the same rtol, at N_obs).
Writes reruns/ac13_stress_compare.json. Run from the repo root."""
import json, math
from pathlib import Path
N_OBS = math.log(1101.0)
S = Path('action_search_2026_11_05/AC13_slow_root_closure/parts')
C = Path('closure_2026_11_06/FRW_RECONCILIATION_CHAIN/reruns/ac13_stress')
def at(p, N):
    for s in p['snaps']:
        if abs(s['N'] - N) < 1e-9 and not s.get('failed'): return s
def R(a, g):
    sa, sg = at(a, N_OBS), at(g, N_OBS)
    return max(sa['max_I'] / sg['max_I'], sa['max_II'] / sg['max_II'])
rows = []
for p in sorted(C.glob('*_stress_*.json')):
    new = json.loads(p.read_text()); old = json.loads((S / p.name).read_text())
    gr = json.loads((S / p.name.replace('_stress_', '_gr_').replace('_7.00397', '_7.00397')).read_text()) \
        if (S / p.name.replace('_stress_', '_gr_')).exists() else None
    if gr is None:   # gr rows run to N = 20 for eps_phi <= 0.5
        gr = json.loads((S / p.name.replace('_stress_', '_gr_').replace('_7.00397', '_20')).read_text())
    rows.append(dict(tag=p.stem, pol_old=old['job']['pol_on'], pol_new=new['job']['pol_on'], ok_new=new['ok'],
                     R_old=R(old, gr), R_new=R(new, gr),
                     detK_min_old=min(s['detK_over_a6_min'] for s in old['snaps']),
                     detK_min_new=min(s['detK_over_a6_min'] for s in new['snaps'])))
out = dict(n=len(rows), R_old_range=[min(r['R_old'] for r in rows), max(r['R_old'] for r in rows)],
           R_new_range=[min(r['R_new'] for r in rows), max(r['R_new'] for r in rows)],
           detK_min_new=min(r['detK_min_new'] for r in rows), all_ok=all(r['ok_new'] for r in rows), rows=rows,
           note='post-hoc corrected-coefficient stress rows; reported only (AC13 stress was never graded). kappa = 1/2 FITTED')
Path('closure_2026_11_06/FRW_RECONCILIATION_CHAIN/reruns/ac13_stress_compare.json').write_text(json.dumps(out, indent=1) + '\n')
print({k: v for k, v in out.items() if k != 'rows'})
for r in rows: print(r['tag'], f"R {r['R_old']:.4f} -> {r['R_new']:.4f}  detKmin {r['detK_min_old']:.4g} -> {r['detK_min_new']:.4g}")
