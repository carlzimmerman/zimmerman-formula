"""AC23 grader: lines from FROZEN_CRITERIA.md (6b3a77495e). Kappa = 1/2 FITTED; not theory closed.
Run from the repo root. AC23_MUTATE=1: grade with main replaced by m2 (flipped stiffness); must FAIL."""
import json, math, os
from pathlib import Path
D = Path('action_search_2026_11_05/AC23_fresh_slow_roots')
MUT = os.environ.get('AC23_MUTATE') == '1'
N_OBS = math.log(1101.0)
W = json.loads((D / 'witnesses.json').read_text())
P = {}
for p in (D / 'parts').glob('*.json'):
    p = json.loads(p.read_text()); j = p['job']
    P[(j['epsilon_phi'], j['epsilon_m'], j['Lstar'], j['k'], j['kind'], j['rtol'])] = p
MAIN = 'm2' if MUT else 'main'


def at(p, N):
    for s in p['snaps']:
        if abs(s['N'] - N) < 1e-9 and not s.get('failed'):
            return s
    return None


def R(c, kind, rtol, N):
    a, g = P.get(c + (kind, rtol)), P.get(c + ('gr', rtol))
    if a is None or g is None: return None
    sa, sg = at(a, N), at(g, N)
    if sa is None or sg is None: return None
    return max(sa['max_I'] / sg['max_I'], sa['max_II'] / sg['max_II'])


def detmin(c, kind, rtol, Nmax):
    p = P[c + (kind, rtol)]
    v = [s['detK_over_a6_min'] for s in p['snaps'] if s['N'] <= Nmax + 1e-9]
    failed = any(s.get('failed') and s['N'] <= Nmax + 1e-9 for s in p['snaps'])
    return (min(v) if v else None), failed, p['ok']


# KA1
ka = json.loads(next((D / 'ka1').glob('*.json')).read_text())
ref = json.loads(Path('action_search_2026_11_05/AC13_slow_root_closure/parts/c.05_.3_.001_10_main_1e-09_20.json').read_text())
sa, sr = at(ka, N_OBS), at(ref, N_OBS)
ka1_rel = max(abs(sa[x] - sr[x]) / abs(sr[x]) for x in ('max_I', 'max_II', 'detK_over_a6_min'))
ka1 = ka1_rel <= 1e-10
ka2 = W['KA2']['pass_'] and W['prec_agree']
rows = {}; powered = []; fail_any = False; conv_powered = True; omega_powered = True; over10 = False
for w in W['witnesses']:
    c = (w['epsilon_phi'], w['epsilon_m'], w['Lstar'], w['k']); key = ','.join(c); row = {'omega2_min': w['min_neg_omega2']}
    r9, r11 = R(c, MAIN, 1e-9, N_OBS), R(c, MAIN, 1e-11, N_OBS)
    row['R_main_Nobs'] = [r9, r11]
    conv = r9 is not None and r11 is not None and abs(r9 - r11) / r11 <= 1e-3
    row['converged'] = conv
    dr = [s['omega_drift'] for kind in (MAIN, 'gr') for t in (1e-9, 1e-11) for s in P[c + (kind, t)]['snaps']
          if s['N'] <= N_OBS + 1e-9 and not s.get('failed') and s['omega_drift'] is not None]
    row['omega_drift'] = max(dr) if dr else None; om_ok = bool(dr) and max(dr) <= 1e-6
    dm = [detmin(c, MAIN, t, N_OBS) for t in (1e-9, 1e-11)]
    row['main_detK_min_Nobs'] = [d[0] for d in dm]; row['main_failed_by_Nobs'] = [d[1] for d in dm]
    main_det_ok = all(d[0] is not None and d[0] > 0 and not d[1] for d in dm)
    pr = [R(c, 'plant', t, N_OBS) for t in (1e-9, 1e-11)]; row['R_plant_Nobs'] = pr
    pw = all(x is not None and x >= 1e3 for x in pr); row['powered'] = pw
    m2d = [detmin(c, 'm2', t, 20.0) for t in (1e-9, 1e-11)]
    row['m2_detK_min_N20'] = [d[0] for d in m2d]; row['m2_failed_by_N20'] = [d[1] for d in m2d]
    row['detK_disc_bites'] = all((d[0] is not None and d[0] <= 0) or d[1] for d in m2d)
    for N in (10.0, 15.0, 20.0):
        row[f'R_main_N{N:g}'] = R(c, MAIN, 1e-11, N)
    if conv and ((r11 is not None and r11 >= 1e3) or not main_det_ok): fail_any = True
    if not conv and not main_det_ok and any(d[0] is not None and d[0] <= 0 for d in dm): fail_any = True
    if pw:
        powered.append(key); conv_powered &= conv; omega_powered &= om_ok
        if r11 is None or r11 > 10 or not main_det_ok: over10 = True
    rows[key] = row
if fail_any: label = 'FAIL'
elif len(powered) < 3: label = 'NO VERDICT (no power)'
elif not (ka1 and ka2 and conv_powered and omega_powered): label = 'NO VERDICT'
elif not over10: label = 'PASS (HARMLESS, scoped)'
else: label = 'UNDECIDED'
out = dict(label=label, mutate=MUT, KA1_rel=ka1_rel, KA1=ka1, KA2=ka2, n_witnesses=len(rows), n_powered=len(powered),
           powered=powered, converged_powered=conv_powered, omega_powered=omega_powered,
           max_R_main_Nobs=max((r['R_main_Nobs'][1] or float('inf')) for r in rows.values()),
           min_main_detK_Nobs=min(min(x for x in r['main_detK_min_Nobs'] if x is not None) for r in rows.values()),
           detK_disc_bites_on=sum(r['detK_disc_bites'] for r in rows.values()), rows=rows,
           note='kappa = 1/2 FITTED; not theory closed')
name = 'GRADE_MUTATE.json' if MUT else 'GRADE.json'
(D / name).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))
raise SystemExit(0 if (label.startswith('PASS') != MUT or (MUT and label == 'FAIL')) else 1)
