"""EP1 grader: lines from CRITERIA.md (d8fc918584). Kappa = 1/2 FITTED; not theory closed. Run from the repo root.
EP1_MUTATE=m2 / plantR: grade that kind in place of main; must give UNSTABLE."""
import json, math, os
from pathlib import Path
D = Path('closure_2026_11_06/EP1_decelerating_slow_roots')
MUT = os.environ.get('EP1_MUTATE', '')
MAIN = MUT or 'main'
N_OBS = math.log(1101.0)


def load(sub):
    P = {}
    for f in (D / sub).glob('*.json'):
        p = json.loads(f.read_text()); j = p['job']
        P[(j['epsilon_phi'], j['epsilon_m'], j['Lstar'], j['k'], j['kind'], j['rtol'])] = p
    return P


P = load('parts')


def at(p, N):
    for s in p['snaps']:
        if abs(s['N'] - N) < 1e-9 and not s.get('failed'):
            return s
    return None


def R(c, kind, rtol, N=N_OBS, PP=P):
    a, g = PP.get(c + (kind, rtol)), PP.get(c + ('gr', rtol))
    if a is None or g is None: return None
    sa, sg = at(a, N), at(g, N)
    if sa is None or sg is None: return None
    return max(sa['max_I'] / sg['max_I'], sa['max_II'] / sg['max_II'])


def detmin(c, kind, rtol, PP=P):
    p = PP[c + (kind, rtol)]
    v = [s['detK_over_a6_min'] for s in p['snaps'] if s['N'] <= N_OBS + 1e-9]
    failed = any(s.get('failed') for s in p['snaps'])
    return (min(v) if v else None), failed


def rel(x, y): return abs(x - y) / abs(y)


# KA1: AC13's 2 eps_phi = 2 fixtures through EP1's runner
K1 = load('ka1'); ka1_rel = 0.0; ka1_n = 0
for (es, ms, ls, ks, kind, rtol), p in K1.items():
    ref = json.loads(Path(f'action_search_2026_11_05/AC13_slow_root_closure/parts/c{es}_{ms}_{ls}_{ks}_{kind}_{rtol:g}_{N_OBS:g}.json').read_text())
    sa, sr = at(p, N_OBS), at(ref, N_OBS)
    ka1_rel = max([ka1_rel] + [rel(sa[x], sr[x]) for x in ('max_I', 'max_II', 'detK_over_a6_min')]); ka1_n += 1
ka1 = ka1_n == 8 and ka1_rel <= 1e-10
# KA2a: AC23's committed grade.py on its committed parts, output redirected
g23 = Path('action_search_2026_11_05/AC23_fresh_slow_roots/grade.py').read_text()
a_, b_ = "(D / name).write_text", "(Path('closure_2026_11_06/EP1_decelerating_slow_roots/ka2_AC23_regrade.json')).write_text"
assert g23.count(a_) == 1
g23 = g23.replace(a_, b_).replace('raise SystemExit', '_rc =')
saved = os.environ.pop('AC23_MUTATE', None); ns = {'__name__': 'ac23grade'}
exec(compile(g23, 'AC23/grade.py[EP1 KA2]', 'exec'), ns)
ref23 = json.loads(Path('action_search_2026_11_05/AC23_fresh_slow_roots/GRADE.json').read_text()); new23 = ns['out']
ka2a = (new23['label'] == 'PASS (HARMLESS, scoped)' == ref23['label'] and new23['n_powered'] == 16 == ref23['n_powered']
        and rel(new23['max_R_main_Nobs'], ref23['max_R_main_Nobs']) <= 1e-12 and rel(new23['min_main_detK_Nobs'], ref23['min_main_detK_Nobs']) <= 1e-12)
# KA2b: AC23 witness (0.25, 0.6, 0.0003, 3) main rtol 1e-9, rerun to N_obs
kb = json.loads(next((D / 'ka2').glob('*.json')).read_text())
rb = json.loads(Path('action_search_2026_11_05/AC23_fresh_slow_roots/parts/c0.25_0.6_0.0003_3_main_1e-09_20.json').read_text())
ka2b_rel = max(rel(at(kb, N_OBS)[x], at(rb, N_OBS)[x]) for x in ('max_I', 'max_II', 'detK_over_a6_min'))
ka2 = ka2a and ka2b_rel <= 1e-10
W = json.loads((D / 'witnesses.json').read_text())
ka3 = W['KA3']['pass_'] and W['prec_agree']
cases = [(w['epsilon_phi'], w['epsilon_m'], w['Lstar'], w['k']) for w in W['witnesses']]
if W['add_AC13_fixtures']:
    cases += [('2', '.9', '.001', '10'), ('2', '.9', '.001', '100')]
rows = {}; powered = []; unstable = []; conv_p = om_p = True; over10 = False
for c in cases:
    key = ','.join(c); row = {}
    r9, r11 = R(c, MAIN, 1e-9), R(c, MAIN, 1e-11); row['R_main_Nobs'] = [r9, r11]
    conv = r9 is not None and r11 is not None and abs(r9 - r11) / r11 <= 1e-3; row['converged'] = conv
    if r9 is not None and r11 is not None: row['conv_rel'] = abs(r9 - r11) / r11
    dr = [s['omega_drift'] for kind in (MAIN, 'gr') for t in (1e-9, 1e-11) for s in P[c + (kind, t)]['snaps']
          if s['N'] <= N_OBS + 1e-9 and not s.get('failed') and s['omega_drift'] is not None]
    row['omega_drift'] = max(dr) if dr else None; om_ok = bool(dr) and max(dr) <= 1e-6
    dm = [detmin(c, MAIN, t) for t in (1e-9, 1e-11)]
    row['main_detK_min'] = [d[0] for d in dm]; row['main_failed'] = [d[1] for d in dm]
    det_ok = all(d[0] is not None and d[0] > 0 and not d[1] for d in dm)
    pr = [R(c, 'plantR', t) for t in (1e-9, 1e-11)]; row['R_PWR_Nobs'] = pr
    pwr = all(x is not None and x >= 1e3 for x in pr)
    m2d = [detmin(c, 'm2', t) for t in (1e-9, 1e-11)]
    row['m2_detK_min'] = [d[0] for d in m2d]; row['m2_failed'] = [d[1] for d in m2d]
    pwd = all((d[0] is not None and d[0] <= 0) or d[1] for d in m2d)
    row['PW_R_bites'] = pwr; row['PW_D_bites'] = pwd; row['powered'] = pwr and pwd
    row['R_m2_Nobs'] = R(c, 'm2', 1e-11); row['R_AC13_plant_Nobs_reported'] = R(c, 'plant', 1e-11)
    if (conv and r11 is not None and r11 >= 1e3) or not det_ok:
        unstable.append(key)
    if row['powered']:
        powered.append(key); conv_p &= conv; om_p &= om_ok
        if r11 is None or r11 > 10 or not det_ok: over10 = True
    rows[key] = row
if unstable: label = 'UNSTABLE (' + '; '.join(unstable) + ')'
elif len(powered) < 3: label = 'NO VERDICT (no power)'
elif not (ka1 and ka2 and ka3 and conv_p and om_p): label = 'NO VERDICT'
elif not over10: label = 'HARMLESS (scoped)'
else: label = 'NO VERDICT, bracket 10 < R < 1e3'
# PW-R on AC13's fixtures (reported)
F = load('ac13fix'); A13 = load_ref = {}
fix = {}
for c in [('2', '.9', '.001', '10'), ('2', '.9', '.001', '100')]:
    vals = []
    for t in (1e-9, 1e-11):
        p = F.get(c + ('plantR', t)); g = json.loads(Path(f'action_search_2026_11_05/AC13_slow_root_closure/parts/c{c[0]}_{c[1]}_{c[2]}_{c[3]}_gr_{t:g}_{N_OBS:g}.json').read_text())
        sa, sg = at(p, N_OBS), at(g, N_OBS)
        vals.append(max(sa['max_I'] / sg['max_I'], sa['max_II'] / sg['max_II']) if sa and sg else None)
    fix[','.join(c)] = vals
mx = [r['R_main_Nobs'][1] for r in rows.values() if r['R_main_Nobs'][1] is not None]
out = dict(label=label, mutate=MUT or None, KA1=ka1, KA1_rel=ka1_rel, KA1_n=ka1_n, KA2=ka2, KA2a=ka2a, KA2b_rel=ka2b_rel,
           KA2a_values=dict(label=new23['label'], n_powered=new23['n_powered'], max_R=new23['max_R_main_Nobs'], min_det=new23['min_main_detK_Nobs']),
           KA3=ka3, n_witnesses=len(rows), n_powered=len(powered), powered=powered, converged_powered=conv_p, omega_powered=om_p,
           max_R_main_Nobs=max(mx) if mx else None, min_R_main_Nobs=min(mx) if mx else None,
           min_main_detK=min(min(x for x in r['main_detK_min'] if x is not None) for r in rows.values()),
           PW_R_range=[min(min(r['R_PWR_Nobs']) for r in rows.values()), max(max(r['R_PWR_Nobs']) for r in rows.values())],
           m2_detK_max_of_min=max(max(x for x in r['m2_detK_min'] if x is not None) for r in rows.values()),
           PW_R_on_AC13_fixtures_reported=fix, rows=rows, note='kappa = 1/2 FITTED; not theory closed')
name = f'GRADE_MUTATE_{MUT}.json' if MUT else 'GRADE.json'
(D / name).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))
raise SystemExit(0 if ((not MUT) or label.startswith('UNSTABLE')) else 1)
