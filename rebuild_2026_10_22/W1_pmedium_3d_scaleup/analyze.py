#!/usr/bin/env python3
"""Ladder analysis under FROZEN_CRITERIA.md sections 4-6 (convergence and binding-certificate reading rules).
Reads runs/ladder/*/result.json (direct and, when present, queued runs). Footings are never pooled.
  /usr/bin/python3 analyze.py            -> LADDER_RESULTS.json
  /usr/bin/python3 analyze.py --mutate   -> LADDER_RESULTS_MUTATE.json (two planted defects; the checks must catch both)"""
import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / 'runs' / 'ladder'
SE = HERE / 'repro' / 'spatial_expansion_2026_10_23'
SE_MAP = {('canonical', 'weak', 8): 'base', ('canonical', 'weak', 12): 'space', ('canonical', 'strong', 8): 'strong',
          ('canonical', 'strong', 12): 'strong_space', ('canonical', 'strong', 16): 'strong_fine'}
RADII = (0.3214846542759978, 1.44, 2.88)
# FROZEN_CRITERIA 4 enumerates 'R = 2.88 kpc: n >= 32; R = 1.44 kpc: n >= 64; .3215 kpc: never' and also states 'R >= 4 cells';
# 2.88 and 1.44 are roundings of 4 x 0.7206 and 4 x 0.3603 kpc, so the literal arithmetic gives 3.996 cells at 32^3 / 64^3.
# AMENDMENT A3: both readings are reported; 'enum' = the enumerated list, 'strict' = R_cells >= 4.
ENUM_MIN_N = {0.3214846542759978: 10 ** 9, 1.44: 64, 2.88: 32}
READING = 'enum'


def is_resolved(R, n, R_cells):
    return (n >= ENUM_MIN_N[R]) if READING == 'enum' else (R_cells >= 4)
CERT_RADII = (1.44, 2.88)


def load():
    runs = {}
    for f in sorted(RUNS.glob('*/result.json')):
        r = json.loads(f.read_text()); p = r['parameters']
        if p.get('mutate'): continue
        seed = {0.001: 'weak', 0.03: 'strong'}[p['amp']]
        runs[(p['footing'], seed, p['n'])] = r
    return runs


def completed(r):
    c = {x['name']: x['passed'] for x in r['checks']}
    return bool(c['reaches_target'] and c['static_residual'] and c['work_balance'] and len(r.get('cert_rows', [])) == 11)


def ap(r, k, R):
    row = next(c for c in r['cert_rows'] if c['k'] == k)
    return next(a for a in row['apertures'] if abs(a['R_kpc'] - R) < 1e-9)


def conv_peak(series):
    ns = sorted(series)
    if len(ns) < 2: return dict(verdict='UNDECIDED (one grid)')
    n1, n2 = ns[-2], ns[-1]; d = abs(series[n2] / series[n1] - 1)
    return dict(n1=n1, n2=n2, change=d, verdict='CONVERGED' if d <= .05 else 'NOT CONVERGED')


def conv_mass(series, resolved):
    ns = sorted(series)
    if len(ns) < 2: return dict(verdict='UNDECIDED (one grid)')
    n1, n2 = ns[-2], ns[-1]; d = abs(series[n2] / series[n1] - 1) if series[n1] else None  # empty aperture at n1
    if not resolved[n1]: v = 'UNRESOLVED'
    else: v = 'CONVERGED' if d <= .05 else 'NOT CONVERGED'
    return dict(n1=n1, n2=n2, change=d, resolved_at_n1=resolved[n1], verdict=v)


def order(series):
    ns = sorted(series)
    out = []
    for a, b, c in zip(ns, ns[1:], ns[2:]):
        if b == 2 * a and c == 2 * b:
            d1, d2 = series[b] - series[a], series[c] - series[b]
            out.append(dict(grids=[a, b, c], p=(math.log2(abs(d1 / d2)) if (d2 and d1) else None)))
    return out


def certificate(rs, R):
    per = {}
    for n, r in sorted(rs.items()):
        E = [ap(r, k, R)['E_iso'] for k in range(11)]
        res = is_resolved(R, n, ap(r, 10, R)['R_cells'])
        neg = all(e < 0 for e in E); stab = max(abs(e - E[10]) for e in E) <= .25 * abs(E[10])
        a10 = ap(r, 10, R); a0 = ap(r, 0, R)
        rows = [next(c for c in r['cert_rows'] if c['k'] == k) for k in range(11)]
        lnA = [c['lnA'] for c in rows]; WA = [ap(r, k, R)['W_A'] for k in range(11)]; EH = [ap(r, k, R)['E_H'] for k in range(11)]
        intW = sum(.5 * (WA[i] + WA[i + 1]) * (lnA[i + 1] - lnA[i]) for i in range(10))
        per[n] = dict(E_iso=E, negative=neg, stable=stab, max_rel_dev_from_end=max(abs(e - E[10]) for e in E) / abs(E[10]),
                      resolved=res, R_cells_z10=a10['R_cells'], bound=neg and stab and res,
                      virial_2K_over_U_start_end=[a0['virial_2K_over_U'], a10['virial_2K_over_U']],
                      E_field_over_absU_end=a10['E_field'] / abs(a10['U']) if a10['U'] else None,
                      matter_KU_end=a10['matter_KU'], cold_only_KU_end=a10['cold_only_KU'],
                      E_H_start_end=[EH[0], EH[10]], int_W_A_dlnA=intW, N_c_start_end=[a0['N_c'], a10['N_c']])
    resolved = [n for n in sorted(per) if per[n]['resolved']]
    if not resolved: v = 'UNDECIDED (aperture unresolved at every completed grid)'
    else:
        f = per[resolved[-1]]
        if not (f['negative'] and f['stable']): v = 'NOT CERTIFIED'
        elif len(resolved) >= 2 and per[resolved[-2]]['bound'] and abs(f['E_iso'][10] / per[resolved[-2]]['E_iso'][10] - 1) <= .25: v = 'BOUND-CERTIFIED'
        else: v = 'UNDECIDED'
    return dict(per_grid=per, finest_resolved=resolved[-1] if resolved else None, verdict=v)


def analyse(runs, planted=None):
    out = dict(criteria='FROZEN_CRITERIA.md sections 4-6', footings={}, checks={})
    checks = {}
    # tie-in: canonical 8/12/16 ladder peaks equal SE's recorded peaks bit for bit
    tie = {}
    for key, nm in SE_MAP.items():
        if key in runs:
            se = json.loads((SE / nm / 'result.json').read_text())['rows'][-1]['contrast_c_max']
            tie[f'{key}'] = runs[key]['rows'][-1]['contrast_c_max'] == se
    checks['ladder_ties_to_SE_recorded_peaks'] = bool(tie) and all(tie.values())
    sign_ok = True; mass_ok = True
    for (fo, seed, n), r in runs.items():
        box = r['parameters']['cold_box_mass_Msun']
        for c in r['cert_rows']:
            for a in c['apertures']:
                sign_ok &= a['K'] >= 0 and a['U'] <= 0 and a['E_field'] >= -1e-300
                mass_ok &= a['M_c_Msun'] <= box * (1 + 1e-12)
    checks['K_nonneg_U_nonpos_Efield_nonneg'] = bool(sign_ok); checks['aperture_mass_le_box'] = bool(mass_ok)
    both = [(s, n) for (fo, s, n) in runs if fo == 'canonical' and ('alt', s, n) in runs]
    checks['footings_distinct_not_pooled'] = bool(both) and all(runs[('canonical', s, n)]['rows'][-1]['contrast_c_max'] != runs[('alt', s, n)]['rows'][-1]['contrast_c_max'] for s, n in both)
    out['checks'] = checks; out['all_checks_pass'] = all(checks.values())
    for fo in ('canonical', 'alt'):
        F = out['footings'][fo] = {}
        for seed in ('weak', 'strong'):
            rs = {n: r for (f2, s2, n), r in runs.items() if f2 == fo and s2 == seed and completed(r)}
            notdone = sorted(n for (f2, s2, n), r in runs.items() if f2 == fo and s2 == seed and not completed(r))
            if not rs: continue
            prov = 128 not in rs
            peak = {n: r['rows'][-1]['contrast_c_max'] for n, r in rs.items()}
            S = F[seed] = dict(grids=sorted(rs), incomplete=notdone, provisional=prov,
                               steps={n: r['steps'] for n, r in rs.items()},
                               max_work_error={n: r['max_work_error'] for n, r in rs.items()},
                               peak_delta_c_z10=peak, peak_baryon_z10={n: r['rows'][-1]['contrast_b_max'] for n, r in rs.items()},
                               rms_c_z10={n: r['rows'][-1]['rms_c'] for n, r in rs.items()},
                               fof_max_members_z10={n: r['rows'][-1]['max_members'] for n, r in rs.items()},
                               convergence_peak=conv_peak(peak), order_peak=order(peak), apertures={}, certificate={})
            for R in RADII:
                Mc = {n: ap(r, 10, R)['M_c_Msun'] for n, r in rs.items()}
                res = {n: is_resolved(R, n, ap(r, 10, R)['R_cells']) for n, r in rs.items()}
                S['apertures'][f'{R:g}'] = dict(M_c_Msun=Mc, M_b_Msun={n: ap(r, 10, R)['M_b_Msun'] for n, r in rs.items()},
                                                delta_ap_c={n: ap(r, 10, R)['delta_ap_c'] for n, r in rs.items()},
                                                R_cells={n: ap(r, 10, R)['R_cells'] for n, r in rs.items()}, resolved=res,
                                                convergence=conv_mass(Mc, res), order=order(Mc))
            for R in CERT_RADII:
                S['certificate'][f'{R:g}'] = certificate(rs, R)
            prim = '1.44' if any(v['resolved'] for v in S['certificate']['1.44']['per_grid'].values()) else '2.88'
            S['certificate_primary_aperture_kpc'] = prim
            S['certificate_primary_verdict'] = S['certificate'][prim]['verdict'] + (' (PROVISIONAL)' if prov else '')
            S['convergence_peak']['verdict'] += ' (PROVISIONAL)' if prov else ''
            for k in S['apertures']: S['apertures'][k]['convergence']['verdict'] += ' (PROVISIONAL)' if prov else ''
    return out


def main():
    ap_ = argparse.ArgumentParser(); ap_.add_argument('--mutate', action='store_true'); a = ap_.parse_args()
    runs = load()
    if a.mutate:
        k = ('canonical', 'strong', 16)
        runs[k]['rows'][-1]['contrast_c_max'] = json.loads((SE / 'strong_space' / 'result.json').read_text())['rows'][-1]['contrast_c_max']
        k2 = next(iter(runs)); runs[k2]['cert_rows'][0]['apertures'][1]['U'] *= -1
        out = analyse(runs); out['mutate_caught'] = (not out['checks']['ladder_ties_to_SE_recorded_peaks']) and (not out['checks']['K_nonneg_U_nonpos_Efield_nonneg'])
        (HERE / 'LADDER_RESULTS_MUTATE.json').write_text(json.dumps(out, indent=1) + '\n'); print('mutate caught:', out['mutate_caught']); return
    global READING
    both = {}
    for READING in ('enum', 'strict'):
        both[READING] = analyse(json.loads(json.dumps({k: v for k, v in runs.items()}, default=str)) if False else runs)
    out = dict(both['enum']); out['reading'] = 'enum (FROZEN_CRITERIA 4 enumerated n-lists; AMENDMENT A3)'
    out['strict_reading'] = {fo: {seed: dict(apertures={R: A['convergence'] for R, A in S['apertures'].items()},
                                               certificate={R: C['verdict'] for R, C in S['certificate'].items()},
                                               primary=[S['certificate_primary_aperture_kpc'], S['certificate_primary_verdict']])
                                  for seed, S in F.items()} for fo, F in both['strict']['footings'].items()}
    (HERE / 'LADDER_RESULTS.json').write_text(json.dumps(out, indent=1) + '\n')
    print('checks', out['checks'])
    for fo, F in out['footings'].items():
        for seed, S in F.items():
            print(f"== {fo} {seed}: grids {S['grids']} incomplete {S['incomplete']}")
            print('  peak', {n: round(v, 4) for n, v in S['peak_delta_c_z10'].items()}, S['convergence_peak']['verdict'], S['order_peak'])
            for R, A in S['apertures'].items():
                st = out['strict_reading'][fo][seed]['apertures'][R]['verdict']
                print(f'  M_c(<{R})', {n: f'{v:.4e}' for n, v in A['M_c_Msun'].items()}, 'enum:', A['convergence']['verdict'], '| strict:', st)
            for R, C in S['certificate'].items():
                print(f'  cert {R}: enum {C["verdict"]} | strict {out["strict_reading"][fo][seed]["certificate"][R]}')
            print('  primary', S['certificate_primary_aperture_kpc'], S['certificate_primary_verdict'], '| strict', out['strict_reading'][fo][seed]['primary'])


if __name__ == '__main__':
    main()
