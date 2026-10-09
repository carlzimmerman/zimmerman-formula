#!/usr/bin/env python3
"""CFG567: census of z ~ 1.5-3 discs that could support CFG385's self-calibrated a0(z) test.

Applies the frozen rules (FROZEN_CRITERIA.md) to cfg567_census.csv. Q1 is COMPUTED wherever the row carries
radii and velocities; otherwise the per-row judgement (with its source) is used. Census only: no a0 is scored
unless >= 5 primary-band discs pass Q1-Q6 (they do not; see the output).

kappa = 1/2 is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s^2.

Usage: python cfg567_census.py            (frozen run)
       python cfg567_census.py --mutate   (MUTATE: Q3 relaxed; exits 1 if the qualifying count changes)
"""
import csv, json, sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
A0_LO, A0_HI = 9.3603e-11, 1.1312e-10
KPC = 3.0857e19
IN_T, OUT_T = 3.5, 0.55            # frozen: g_obs >= 3.5 a0 inner, <= 0.55 a0 outer, at BOTH footings
MUTATE = '--mutate' in sys.argv


def g_obs(v_kms, r_kpc):
    return (v_kms * 1e3) ** 2 / (r_kpc * KPC)


def q1(row, out_t=OUT_T):
    """Frozen Q1. Inner must hold at the HIGH footing, outer at the LOW footing (both footings)."""
    f = lambda k: float(row[k]) if row[k] not in ('', None) else None
    ri, vi, ro, vo = f('R_in_kpc'), f('V_in_kms'), f('R_out_kpc'), f('V_out_kms')
    if ro is None or vo is None:
        return row['Q1_given'] or 'UNKNOWN', None, None
    gout = g_obs(vo, ro)
    outer_ok = gout <= out_t * A0_LO
    if not outer_ok:
        res = 'FAIL'
    elif ri is None or vi is None:
        res = 'UNKNOWN'
    else:
        res = 'PASS' if g_obs(vi, ri) >= IN_T * A0_HI else 'FAIL'
    gin = g_obs(vi, ri) / A0_HI if (ri and vi) else None
    return res, gout / A0_LO, gin


def evaluate(rows, relax_q3=False, out_t=OUT_T):
    out = []
    for r in rows:
        s1, gout, gin = q1(r, out_t)
        st = {'Q1': s1, 'Q2': r['Q2'], 'Q3': r['Q3_relaxed'] if relax_q3 else r['Q3'],
              'Q4': r['Q4'], 'Q5': r['Q5'], 'Q6': r['Q6']}
        npass15 = sum(st[k] == 'PASS' for k in ('Q1', 'Q2', 'Q3', 'Q4', 'Q5'))
        out.append(dict(cid=r['cid'], name=r['name'], z=r['z'], band=r['band'], in_record=r['in_record'],
                        gout_over_a0lo=None if gout is None else round(gout, 3),
                        gin_over_a0hi=None if gin is None else round(gin, 3),
                        **st, n_pass_Q1to5=npass15,
                        qualifies=all(v == 'PASS' for v in st.values()),
                        qualified_not_obtainable=all(st[k] == 'PASS' for k in ('Q1', 'Q2', 'Q3', 'Q4', 'Q5')) and st['Q6'] != 'PASS',
                        no_fail=all(v != 'FAIL' for v in st.values()),
                        lacks=r['lacks']))
    return out


def counts(ev):
    prim = [e for e in ev if e['band'] == 'primary']
    rep = [e for e in ev if e['band'].startswith('report')]
    return dict(n_rows=len(ev), n_primary_rows=len(prim),
                qualify_primary=sum(e['qualifies'] for e in prim),
                qualify_report_band=sum(e['qualifies'] for e in rep),
                qualified_not_obtainable_primary=sum(e['qualified_not_obtainable'] for e in prim),
                no_fail_primary=sum(e['no_fail'] for e in prim),
                q1_pass_any=sum(e['Q1'] == 'PASS' for e in ev),
                q1_unknown_any=sum(e['Q1'] == 'UNKNOWN' for e in ev),
                near_miss_ge3_of_Q1to5=[e['cid'] for e in ev if e['n_pass_Q1to5'] >= 3 and not e['qualifies']])


def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, 'cfg567_census.csv'))))
    res = {'mode': 'MUTATE (Q3 relaxed)' if MUTATE else 'FROZEN'}

    # ---- C1: a KURVS-type synthetic row (deep outer points, no inner Newtonian anchor) must FAIL Q1
    vi = np.sqrt(2.2 * A0_HI * 6.0 * KPC) / 1e3     # inner at 2.2 a0 (CFG386's best KURVS inner) at R = 6 kpc
    vo = np.sqrt(0.02 * A0_LO * 15.0 * KPC) / 1e3
    syn = dict(R_in_kpc=6.0, V_in_kms=vi, R_out_kpc=15.0, V_out_kms=vo, Q1_given='')
    c1 = q1(syn)[0]
    res['C1'] = dict(synthetic_KURVS_row_Q1=c1, PASS=(c1 == 'FAIL'))

    # ---- C2: thresholds vs the kernels at y = 3 and y = 0.3 (10 % tolerance, frozen)
    ker = {'P2': lambda y: y * np.sqrt(1 + 1 / y), 'expRAR': lambda y: y / (1 - np.exp(-np.sqrt(y)))}
    try:
        import CFG2_common as C
        ker['nu_mono'] = lambda y: y * C.nu_mono(y)
    except Exception as ex:                          # reported, not hidden
        res['C2_nu_mono_import'] = repr(ex)
    c2 = {k: dict(g_y3=round(float(f(3.0)), 3), g_y03=round(float(f(0.3)), 3),
                  inner_dev=round(abs(f(3.0) / IN_T - 1), 3), outer_dev=round(abs(f(0.3) / OUT_T - 1), 3)) for k, f in ker.items()}
    ok = all(v['inner_dev'] <= 0.10 and v['outer_dev'] <= 0.10 for v in c2.values())
    res['C2'] = dict(per_kernel=c2, PASS=ok,
                     note='0.55 a0 corresponds to y ~ 0.2, stricter than y = 0.3; sensitivity run below uses nu_mono(0.3)')

    ev = evaluate(rows, relax_q3=MUTATE)
    res['counts'] = counts(ev)
    # sensitivity (labelled post-freeze): outer threshold at the y = 0.3 kernel value (most lenient kernel)
    t_len = max(v['g_y03'] for v in c2.values())
    res['sensitivity_outer_threshold_y03'] = dict(outer_threshold_a0=t_len,
                                                  counts=counts(evaluate(rows, relax_q3=MUTATE, out_t=t_len)))
    # the deep-regime corridor: R_out needed for g_obs <= threshold, per flat V
    res['corridor_R_out_kpc_needed'] = {str(v): dict(frozen_0p55_lo=round((v * 1e3) ** 2 / (OUT_T * A0_LO) / KPC, 1),
                                                     y03_lenient=round((v * 1e3) ** 2 / (t_len * A0_LO) / KPC, 1))
                                        for v in (100, 125, 150, 175, 200, 250, 300)}
    res['corridor_V_in_needed_kms'] = {str(r): round(np.sqrt(IN_T * A0_HI * r * KPC) / 1e3, 1) for r in (0.5, 1.0, 1.5, 2.0)}
    res['rows'] = ev

    n = res['counts']['qualify_primary']
    verdict = ('ENOUGH TO SCORE' if n >= 5 else ('CENSUS ONLY: FEW' if n >= 1 else 'CENSUS ONLY: NONE'))
    res['verdict'] = verdict

    print(f"CFG567 census [{res['mode']}]  rows {res['counts']['n_rows']} (primary-band rows {res['counts']['n_primary_rows']})")
    print(f"C1 (KURVS-type synthetic row fails Q1): {'PASS' if res['C1']['PASS'] else 'FAIL'}")
    print(f"C2 (thresholds within 10% of kernels at y=3/0.3): {'PASS' if ok else 'FAIL'}  {json.dumps(c2)}")
    print(f"qualifying (Q1-Q6, z 1.5-3.0): {n}   report band (z 3-4.5): {res['counts']['qualify_report_band']}")
    print(f"qualified-not-obtainable: {res['counts']['qualified_not_obtainable_primary']}   primary rows with no FAIL: {res['counts']['no_fail_primary']}")
    print(f"Q1 PASS anywhere: {res['counts']['q1_pass_any']}   Q1 UNKNOWN: {res['counts']['q1_unknown_any']}")
    print(f"near-misses (>=3 of Q1-Q5): {res['counts']['near_miss_ge3_of_Q1to5']}")
    print(f"sensitivity (outer threshold {t_len} a0): qualifying {res['sensitivity_outer_threshold_y03']['counts']['qualify_primary']}")
    print("corridor R_out needed (kpc) per flat V:", json.dumps(res['corridor_R_out_kpc_needed']))
    print("corridor V_in needed at R_in (km/s):", json.dumps(res['corridor_V_in_needed_kms']))
    print("closest Q1 rows (smallest g_out/a0_lo):")
    for e in sorted([e for e in ev if e['gout_over_a0lo'] is not None], key=lambda e: e['gout_over_a0lo'])[:8]:
        print(f"  {e['cid']:7s} {e['name'][:34]:34s} z {e['z']:>9} g_out/a0lo {e['gout_over_a0lo']:6.2f}  Q1 {e['Q1']:7s} Q3 {e['Q3']}  lacks: {e['lacks'][:60]}")
    print(f"VERDICT: {verdict}")

    tag = '_MUTATE' if MUTATE else ''
    json.dump(res, open(os.path.join(HERE, f'cfg567_census{tag}_results.json'), 'w'), indent=1, default=str)

    if MUTATE:
        frozen = counts(evaluate(rows, relax_q3=False))
        changed = (frozen['qualify_primary'] != n)
        changed_open = (frozen['no_fail_primary'] != res['counts']['no_fail_primary'])
        print(f"MUTATE: qualifying frozen {frozen['qualify_primary']} -> relaxed {n}; "
              f"no-FAIL rows frozen {frozen['no_fail_primary']} -> relaxed {res['counts']['no_fail_primary']} (post-freeze diagnostic)")
        if changed:
            print('MUTATE DETECTED (qualifying count changed)'); sys.exit(1)
        print('MUTATE NOT DETECTED by the frozen count: Q3 is not the binding rule (Q1 binds).'
              + (' The no-FAIL count does change (post-freeze diagnostic).' if changed_open else ''))
        sys.exit(0)


if __name__ == '__main__':
    main()
