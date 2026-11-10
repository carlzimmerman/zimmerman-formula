#!/usr/bin/env python3
"""COL1 grader: labels from runs/*.json (FROZEN_CRITERIA.md section 6 with A2/A3), MUTATE bites, brackets.

    python3 col1_grade.py [--snapdir DIR]   -> col1_grade.json / col1_grade.out

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
RC = 3.0     # A3 core radius


def P(*a):
    s = ' '.join(str(x) for x in a); print(s); OUT.append(s)


def load(name):
    p = os.path.join(HERE, 'runs', name + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def name_of(mode, mu, f, M, J, visc=0, law='law', xout=8000.0):
    return f'{mode}_mu{mu:g}_{f}_M{M:g}_J{J}' + (f'_visc{visc:g}' if visc else '') + ('' if law == 'law' else f'_{law}') + \
        ('' if xout == 8000.0 else f'_X{xout:g}')


def lastread(run):
    rs = [x for x in run['reads'] if 'radii' in x]
    return rs[-1] if rs else None


def e3(n1, n2, snapdir, Xmin=80.0):
    """Non-convergence between resolutions at common read times (Lagrangian labels X >= Xmin)."""
    p1, p2 = os.path.join(snapdir, n1 + '.npz'), os.path.join(snapdir, n2 + '.npz')
    if not (os.path.exists(p1) and os.path.exists(p2)):
        return None
    a, b = np.load(p1), np.load(p2)
    n = min(len(a['t']), len(b['t']))
    worst = []
    for i in range(n):
        if abs(a['t'][i] - b['t'][i]) > 1e-6 * max(1.0, abs(a['t'][i])):
            continue
        Xa, Xb = a['X'], b['X']
        sel = Xa >= Xmin
        sel[-1] = False
        rb = np.interp(Xa[sel], Xb, b['r'][i])
        d = float(np.max(np.abs(rb - a['r'][i][sel]) / a['r'][i][sel]))
        worst.append((float(a['t'][i]), d))
        if d > 0.1:
            return {'t': float(a['t'][i]), 'max_rel_dr': d, 'series': worst}
    return {'t': None, 'series_max': max((w[1] for w in worst), default=None)}


def label_pair(r1, r2, snapdir):
    e1, e2 = r1['event'] or {}, r2['event'] or {}
    k1, k2 = e1.get('kind'), e2.get('kind')
    info = {'J1200': e1, 'J2400': e2}
    if 'STALL' in (k1, k2):
        return 'NO VERDICT', 'a resolution stalled (numerical)', info
    brk = lambda k: k in ('E1', 'E2')
    if brk(k1) and brk(k2):
        t1, t2 = e1['t_since_start_gyr'], e2['t_since_start_gyr']
        tconv = abs(t1 - t2) <= 0.1 * max(t1, t2)
        ra, rb = e1.get('r_kpc'), e2.get('r_kpc')
        rconv = (ra is not None and rb is not None and max(ra, rb) <= 2 * min(ra, rb))
        core = (ra is not None and ra < RC) or (rb is not None and rb < RC)
        info.update({'t_gyr_after_start': [t1, t2], 'r_kpc': [ra, rb], 'time_converged': tconv,
                     'radius_converged': rconv, 'core': core})
        if core:
            if tconv:
                return 'BREAKS DOWN', f'core caustic (r < {RC} kpc) at {t1:.4f} / {t2:.4f} Gyr after the start; radius grid-limited', info
            return 'NO VERDICT', 'core E1 whose time differs between resolutions by more than 10 %', info
        tag = '' if (tconv and rconv) else ' (time grid-limited)'
        return 'BREAKS DOWN' + tag, f'E1/E2 at {t1:.4f} / {t2:.4f} Gyr, r {ra} / {rb} kpc', info
    ee = e3(r1['name'], r2['name'], snapdir)
    info['E3'] = ee
    if ee and ee.get('t') is not None:
        return 'BREAKS DOWN', f'E3 non-convergence at t {ee["t"]:.4f} (max rel dr {ee["max_rel_dr"]:.3f})', info
    if brk(k1) != brk(k2):
        return 'NO VERDICT', 'one resolution breaks down, the other does not', info
    return 'UNGRADED (no event)', 'static / oscillation reads needed', info


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--snapdir', default=os.environ.get('COL1_SNAPDIR', '/tmp'))
    a = ap.parse_args()
    ka = json.load(open(os.path.join(HERE, 'col1_ka.json')))
    kas = {k: v['pass'] for k, v in ka.items()}
    syspass = json.load(open(os.path.join(HERE, 'col1_system.json')))['all_pass']
    P('COL1 grade. kappa = 1/2 FITTED; not theory closed. Footings never pooled.')
    P(f'Known answers: KA1 (symbolic) {"PASS" if syspass else "FAIL"}; ' + '; '.join(f'{k} {"PASS" if v else "FAIL"}' for k, v in sorted(kas.items())))
    res = {'known_answers': kas, 'KA1': syspass, 'rows': {}, 'headline': {}, 'brackets': {}, 'mutate': {}}
    MUS = {'canonical': [3.71, 1.78, 0.1], 'alt': [3.71, 1.74, 0.1]}
    MS = [9.4, 10.45, 10.7, 10.9]
    for f in ('canonical', 'alt'):
        for mu in MUS[f]:
            labs = []
            for M in MS:
                r1, r2 = load(name_of('hubble', mu, f, M, 1200)), load(name_of('hubble', mu, f, M, 2400))
                if not (r1 and r2):
                    P(f'  missing {f} mu {mu} M {M}'); continue
                lab, why, info = label_pair(r1, r2, a.snapdir)
                if not all(kas.get(k, False) for k in ('KA2a', 'KA2b', 'KA4', 'KA5', 'KA6', 'KA7')) or not syspass:
                    lab, why = 'NO VERDICT', 'a known answer failed: ' + why
                lr = lastread(r1) or {}
                ratios = {k: v.get('M_N_over_M_ph') for k, v in lr.get('radii', {}).items()}
                res['rows'][f'{f}|{mu}|{M}'] = {'label': lab, 'why': why, 'info': info, 'last_read_J1200': lr, 'M_N_over_M_ph': ratios}
                labs.append(lab)
                P(f'{f:9s} mu {mu:5g} log M_b {M:5g}: {lab} -- {why}; last read (J1200) t {lr.get("t_since_start_gyr", float("nan")):.3f} Gyr,'
                  f' M_N/M_ph at 10/30/100/300 = ' + ' / '.join('-' if ratios.get(k) is None else f'{ratios[k]:.3g}' for k in ('10', '30', '100', '300')))
            head = labs[0] if labs and all(l == labs[0] for l in labs) else (
                (res['rows'].get(f'{f}|{mu}|10.45', {}).get('label', '?') + ' (masses differ)') if labs else 'MISSING')
            res['headline'][f'{f}|{mu}'] = head
            P(f'  HEADLINE {f} mu {mu}: {head}')
    # brackets
    for tag, mode, mus, kw in [('at rest', 'rest', None, {}), ('damped', 'hubble', None, {'visc': 2}), ('mu 198', 'hubble', 'B', {})]:
        for f in ('canonical', 'alt'):
            mlist = MUS[f] if mus is None else [198.25 if f == 'canonical' else 198.24]
            for mu in mlist:
                r1 = load(name_of(mode, mu, f, 10.45, 1200, **kw)); r2 = load(name_of(mode, mu, f, 10.45, 2400, **kw))
                if not (r1 and r2):
                    continue
                lab, why, info = label_pair(r1, r2, a.snapdir)
                lr1, lr2 = lastread(r1) or {}, lastread(r2) or {}
                ratios = {k: v.get('M_N_over_M_ph') for k, v in lr1.get('radii', {}).items()}
                res['brackets'][f'{tag}|{f}|{mu}'] = {'reading': lab, 'why': why, 'info': info, 'last_read_J1200': lr1,
                                                     'last_read_J2400': lr2}
                P(f'BRACKET {tag:8s} {f:9s} mu {mu:6g}: reads {lab} -- {why}; end t {r1["t_end_gyr"] - r1["t_start_gyr"]:.3f} Gyr;'
                  f' M_N/M_ph 10/30/100/300 = ' + ' / '.join('-' if ratios.get(k) is None else f'{ratios[k]:.3g}' for k in ('10', '30', '100', '300')))
    # mutate
    base = load(name_of('hubble', 3.71, 'canonical', 10.45, 1200))
    for law in ('off', 'neg', 'flip', 'lin'):
        r = load(name_of('hubble', 3.71, 'canonical', 10.45, 1200, law=law))
        if not (r and base):
            continue
        tb = (base['event'] or {}).get('t_since_start_gyr', base['t_end_gyr'] - base['t_start_gyr'])
        tm = (r['event'] or {}).get('t_since_start_gyr', r['t_end_gyr'] - r['t_start_gyr'])
        lb, lm = lastread(base), lastread(r)
        mb = lb['radii'].get('100', {}).get('M_N'); mm = lm['radii'].get('100', {}).get('M_N')
        dt_rel = abs(tm - tb) / max(tb, 1e-12)
        dm_rel = abs(mm - mb) / max(abs(mb), 1e-300) if (mb is not None and mm is not None) else None
        bites = dt_rel >= 0.1 or (dm_rel is not None and dm_rel >= 0.1)
        same = (r['event'] == base['event']) and (json.dumps(lm, sort_keys=True) == json.dumps(lb, sort_keys=True))
        res['mutate'][law] = {'event': r['event'], 'event_time_rel_change': dt_rel, 'M_N100_rel_change': dm_rel,
                              'bites': bites, 'identical_to_primary': same}
        P(f'MUTATE {law}: event {(r["event"] or {}).get("kind")} at {tm:.4f} Gyr (primary {tb:.4f}); dt/t {dt_rel:.3g};'
          f' M_N(<100) change {dm_rel if dm_rel is None else f"{dm_rel:.3g}"}; bites {bites}; bit-identical to primary {same}')
    json.dump(res, open(os.path.join(HERE, 'col1_grade.json'), 'w'), indent=1, default=str)
    open(os.path.join(HERE, 'col1_grade.out'), 'w').write('\n'.join(OUT) + '\n\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n')


if __name__ == '__main__':
    main()
