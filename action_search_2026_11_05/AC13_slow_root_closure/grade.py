"""AC13 grader: lines from FROZEN_CRITERIA.md (12b71c9c08). Kappa = 1/2 FITTED; not theory closed."""
import json, math, sys
from pathlib import Path
D = Path('action_search_2026_11_05/AC13_slow_root_closure')
N_OBS = math.log(1101.0)
parts = [json.loads(p.read_text()) for p in sorted((D / 'parts').glob('*.json'))]
ac5 = {(r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k']): r['R'] for r in
       json.loads(Path('action_search_2026_11_05/AC5_rolling_clock/evidence/main/result.json').read_text())['rows'] if r['witness']}
ac5_m2 = json.loads(Path('action_search_2026_11_05/AC5_rolling_clock/evidence/GRADE.json').read_text())['m2_R_by_witness']
P = {}
for p in parts:
    j = p['job']; P[(j['epsilon_phi'], j['epsilon_m'], j['Lstar'], j['k'], j['kind'], j['rtol'])] = p


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


cases = sorted(ac5)
out = dict(cases={}, note='kappa = 1/2 FITTED; not theory closed')
ka1 = conv = omega_ok = order5 = order_obs = True; main_obs = []; m2_bite = []; plant_bite = []
for c in cases:
    key = ','.join(c); row = {}
    r5 = R(c, 'main', 1e-11, 5.0); row['R_main_N5'] = r5; row['AC5_R'] = ac5[c]
    row['KA1_rel'] = abs(r5 - ac5[c]) / ac5[c] if r5 else None
    ka1 &= row['KA1_rel'] is not None and row['KA1_rel'] <= 1e-6
    r9, r11 = R(c, 'main', 1e-9, N_OBS), R(c, 'main', 1e-11, N_OBS)
    row['R_main_Nobs'] = r11; row['converged_Nobs'] = (r9 is not None and r11 is not None and abs(r9 - r11) / r11 <= 1e-3)
    conv &= row['converged_Nobs']; main_obs.append(r11 if r11 is not None else float('inf'))
    for N in (10.0, 15.0, 20.0):
        row[f'R_main_N{N:g}'] = R(c, 'main', 1e-11, N)
    dr = [s['omega_drift'] for kind in ('main', 'gr') for t in (1e-9, 1e-11) for s in P[c + (kind, t)]['snaps']
          if s['N'] <= N_OBS + 1e-9 and s['omega_drift'] is not None]
    row['omega_drift_main_gr_to_Nobs'] = max(dr); omega_ok &= max(dr) <= 1e-6
    drm = [s['omega_drift'] for t in (1e-9, 1e-11) for s in P[c + ('m2', t)]['snaps']
           if s['N'] <= N_OBS + 1e-9 and not s.get('failed') and s['omega_drift'] is not None]
    row['omega_drift_m2_to_Nobs'] = max(drm) if drm else None
    m2_5 = R(c, 'm2', 1e-11, 5.0); m2_obs = R(c, 'm2', 1e-11, N_OBS)
    row['R_m2_N5'] = m2_5; row['AC5_R_m2'] = ac5_m2.get(key); row['R_m2_Nobs'] = m2_obs
    order5 &= ac5[c] <= ac5_m2[key]
    m2p = P[c + ('m2', 1e-11)]; fail = [s for s in m2p['snaps'] if s.get('failed')]
    row['m2_ok'] = m2p['ok']; row['m2_failed_at_N'] = fail[0]['N'] if fail else None
    row['m2_detK_over_a6_min'] = min(s['detK_over_a6_min'] for s in m2p['snaps'])
    row['m2_N_first_abs_1e3'] = [P[c + ('m2', t)]['snaps'][-1]['N_first_abs_1e3'] for t in (1e-9, 1e-11)]
    row['main_detK_over_a6_min'] = min(s['detK_over_a6_min'] for t in (1e-9, 1e-11) for s in P[c + ('main', t)]['snaps'])
    # M2 order at N_obs: if M2 broke down before N_obs, its amplitude there is unbounded (>= any main R)
    order_obs &= (m2_obs is None and fail and fail[0]['N'] <= N_OBS) or (m2_obs is not None and r11 is not None and r11 <= m2_obs)
    # power (a): R >= 1e3 by N = 20; GR max is the denominator (gr runs to the same N or N_obs)
    gmax = max(max(s['max_I'], s['max_II']) for s in P[c + ('gr', 1e-11)]['snaps'])
    m2_hit = all(x is not None for x in row['m2_N_first_abs_1e3']) and all(x <= 20.0 for x in row['m2_N_first_abs_1e3'])
    row['m2_R_ge_1e3_by_N20'] = bool(m2_hit and gmax < 1.0 + 1e-6) or any(
        (R(c, 'm2', 1e-11, N) or 0) >= 1e3 for N in (5.0, N_OBS, 10.0, 15.0, 20.0))
    row['gr_max_abs'] = gmax
    m2_bite.append(row['m2_R_ge_1e3_by_N20'])
    pr = [R(c, 'plant', t, N_OBS) for t in (1e-9, 1e-11)]
    row['R_plant_Nobs'] = pr; plant_bite.append(all(x is not None and x >= 1e3 for x in pr))
    row['R_stress_Nobs'] = R(c, 'stress', 1e-11, N_OBS)
    out['cases'][key] = row
power = any(m2_bite) or all(plant_bite)
mx = max(main_obs)
if not power: label = 'NO VERDICT (no power)'
elif not (ka1 and conv and omega_ok): label = 'NO VERDICT'
elif mx >= 1e3: label = 'FAIL'
elif mx <= 10: label = 'HARMLESS (scoped)'
else: label = 'UNDECIDED'
out.update(label=label, KA1=ka1, converged_Nobs=conv, omega_line=omega_ok, O1_N5_AC5=order5, O1_Nobs=bool(order_obs),
           power_a_m2=m2_bite, power_b_plant=plant_bite, power=power, max_R_main_Nobs=mx,
           B1_frozen_bound=dict(Gamma_over_H=math.sqrt(0.898421), N_obs=math.exp(math.sqrt(0.898421) * N_OBS),
                                N20=math.exp(math.sqrt(0.898421) * 20)), lines=dict(fail=1e3, harmless=10, linearity=1e5))
(D / 'GRADE.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'cases'}, indent=1))
