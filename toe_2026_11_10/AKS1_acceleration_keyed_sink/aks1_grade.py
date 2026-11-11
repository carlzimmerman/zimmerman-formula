#!/usr/bin/env python3
"""AKS1 grading (FROZEN_CRITERIA.md s. 4, 5, 7): reads runs/*.json, aks1_sym.json, aks1_ka.json.

    python3 aks1_grade.py -> aks1_grade.out / aks1_grade.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import aks1_lib as L

RD = os.path.join(HERE, 'runs')
OUT, RES = [], {'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
MASSES = (9.0, 10.5, 11.5)
CFG = json.load(open(os.path.join(HERE, '../../campaign_fresh_gravity/CFG461_settling_temperature_mechanism/cfg461_results.json')))
CF = {f: CFG['postfreeze_contraction_Rvir_over_redge'][f'zc1_{f}'] for f in ('canonical', 'alt')}
XCAP = 59.5
SCAN_FROM = float(os.environ.get('AKS1_SCAN_FROM', '3.0'))   # A1 (frozen pre-A1: 1.0)


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def load(name):
    p = os.path.join(RD, name + '.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return None if 'not_run' in d else d


def law_slope(f, lM, rc):
    Mb = 10 ** lM; rM = math.sqrt(L.G * Mb / L.a0_of(f)); s = rc / rM
    rho = 1.0 / (s * np.sqrt(1 + 4 * s * s))
    return float(np.polyfit(np.log10(rc), np.log10(rho), 1)[0])


def edge_and_window(row, f, lM):
    """Settled bins, r_edge, the R window and its readings (s. 4)."""
    S = row['summary']; p = S['profile']
    rc = np.array(p['r']); cnt = np.array(p['count']); rho = np.array(p['rho'], float)
    vm = np.array(p['vmean'], float); sg = np.array(p['sigma_r'], float); vc = np.array(p['vc'], float)
    pop = cnt >= 5
    with np.errstate(invalid='ignore'):
        settled = pop & (np.abs(vm) <= 0.25 * np.maximum(sg, 0.1 * vc))
    nb = len(rc)
    lo = L.PEDGES[:-1] >= SCAN_FROM * (1 - 1e-9)             # A1: scan from the first populated bin >= 3 kpc
    cand = np.where(pop & lo)[0]
    start = int(cand[0]) if len(cand) else nb
    i, last = start, None
    while i < nb:
        if settled[i]:
            last = i; i += 1; continue
        if i + 1 >= nb or not settled[i + 1]:
            break
        i += 1
    r_edge = float(L.PEDGES[last + 1]) if last is not None else 0.0
    out = {'r_edge': r_edge, 'n_settled_bins': int(settled.sum()), 'first_bin': start, 'amp': None, 'slope': None,
           'slope_law': None, 'logsig4': None, 'nwin': 0}
    if r_edge > 0:
        w = (rc >= 0.1 * r_edge) & (rc <= r_edge) & pop & (rho > 0)
        out['nwin'] = int(w.sum())
        if w.sum() >= 4:
            Mb = 10 ** lM; a0 = L.a0_of(f)
            ls4 = np.log10((2 * math.pi * L.G * rho[w] * rc[w] ** 2) ** 2)
            out['logsig4'] = float(ls4.mean())
            out['amp'] = float(ls4.mean() - math.log10(L.G * Mb * a0 / 4))
            out['slope'] = float(np.polyfit(np.log10(rc[w]), np.log10(rho[w]), 1)[0])
            out['slope_law'] = law_slope(f, lM, rc[w])
    return out


def gN(Mb, r):
    return L.G * Mb * r / (r * r + L.EPS ** 2) ** 1.5


def main():
    sym = json.load(open(os.path.join(HERE, 'aks1_sym.json')))
    ka = json.load(open(os.path.join(HERE, 'aks1_ka.json')))
    KA = {'KA1': sym['KA1']['pass'], 'KA2': sym['KA2_oscillator_residual'] == '0', 'KA3': ka.get('KA3', {}).get('pass'),
          'KA4': ka.get('KA4', {}).get('pass'), 'KA5a': ka.get('KA5', {}).get('pass_a'), 'KA5b': ka.get('KA5', {}).get('pass_b'),
          'KA8': ka.get('KA8', {}).get('pass'),
          'KA9': ka.get('KA9', {}).get('pass')}
    P('Known answers:', ', '.join(f'{k} {"PASS" if v else ("FAIL" if v is False else "missing")}' for k, v in KA.items()),
      '| KA7:', {f: v.get('KA7_pass') for f, v in ka.get('KA7', {}).items()})
    RES['KA'] = KA
    H = sym['H_pass']
    P(f'H (sym): H1 {sym["H1"]["pass"]}, H2 {sym["H2"]["pass"]}, H3 {sym["H3"]["pass"]}, H4 {sym["H4"]["pass"]} -> {"PASS" if H else "FAIL"}')
    labels = {}
    for f in ('canonical', 'alt'):
        P(f'\n===== footing {f} =====')
        rows = {}
        for key in ('P', 'Pc', 'MU1', 'MU2', 'B1'):
            for lM in MASSES:
                rows[(key, lM)] = load(f'{key}_{f}_{lM:g}')
        if f == 'canonical':
            for lM in MASSES:
                for k2 in ('B2_C10', 'B2_C100', 'B2_C1000', 'B3', 'B4'):
                    rows[(k2, lM)] = load(f'{k2}_canonical_{lM:g}')
        missing = [k for k, v in rows.items() if v is None]
        if missing:
            P('missing rows:', missing)
        EW = {k: (edge_and_window(v, f, k[1]) if v is not None else None) for k, v in rows.items()}
        # table
        P('key   logM  r_edge  r_e*   gN(r_edge)/g_e*  nwin  slope (law)    R2 amp   N_Gamma@r_e*  NGmax    Ediss_Mc/E_req  maxA/a0   R_fold  R_ta')
        tab = {}
        for (key, lM), row in sorted(rows.items(), key=lambda kv: (kv[0][0], kv[0][1])):
            if row is None:
                continue
            S = row['summary']; e = EW[(key, lM)]
            Mb = 10 ** lM
            ge, re = S['g_e_star'], S['r_e_star']
            cf = CF[f][MASSES.index(lM)]
            Ereq = L.G * S['M_c'] ** 2 / (4 * re) * (1 - 1 / cf)
            ratio_g = gN(Mb, e['r_edge']) / ge if e['r_edge'] > 0 else 0.0
            tab[(key, lM)] = {'r_edge': e['r_edge'], 'r_e_star': re, 'gN_over_ge': ratio_g, 'nwin': e['nwin'], 'slope': e['slope'],
                              'slope_law': e['slope_law'], 'amp': e['amp'], 'logsig4': e['logsig4'],
                              'NG_near_edge': S['NG_median_near_edge'], 'NG_max': S['NG_max'], 'Ediss_Mc': S['Ediss_Mc'],
                              'E_req': Ereq, 'S1_ratio': S['Ediss_Mc'] / Ereq, 'Ediss_total': S['Ediss_total'],
                              'Pdiss_total': S['Pdiss_total'], 'Pdiss_Mc': S['Pdiss_Mc'], 'maxA_over_a0': S['maxA_over_a0_max'],
                              'R_fold': S['R_fold_end'], 'R_ta': S['R_ta_end'], 'charge_dev': S['charge_t0_over_start_minus_1'],
                              't_first_centre': row.get('t_first_centre_gyr'), 't_first_cross': row.get('t_first_cross_gyr')}
            t = tab[(key, lM)]
            fmt = lambda x, s='{:.3g}': ('--' if x is None else s.format(x))
            P(f'{key:8s} {lM:4g} {t["r_edge"]:7.1f} {re:6.1f}  {t["gN_over_ge"]:8.3g}       {t["nwin"]:3d}  '
              f'{fmt(t["slope"], "{:+.2f}")} ({fmt(t["slope_law"], "{:+.2f}")})  {fmt(t["amp"], "{:+.3f}")}  '
              f'{fmt(t["NG_near_edge"])}  {t["NG_max"]:.3g}  {t["S1_ratio"]:.3g}  {t["maxA_over_a0"]:.3g}  {t["R_fold"]:.0f}  {t["R_ta"]:.0f}')
        RES[f] = {'table': {f'{k[0]}_{k[1]:g}': v for k, v in tab.items()}}
        # ---- gates on P (and Pc) ----
        g = {}
        Pt = [tab.get(('P', lM)) for lM in MASSES]; Pct = [tab.get(('Pc', lM)) for lM in MASSES]
        if any(x is None for x in Pt + Pct):
            P('P or Pc rows missing: NO VERDICT for this footing'); labels[f] = 'NO VERDICT (rows missing)'; continue
        R1 = [x['slope'] is not None and (abs(x['slope'] + 2) <= 0.1 or abs(x['slope'] - x['slope_law']) <= 0.1) for x in Pt]
        R2 = [x['amp'] is not None and abs(x['amp']) <= 0.1 for x in Pt]
        ls4 = [x['logsig4'] for x in Pt]
        R3s = float(np.polyfit(MASSES, ls4, 1)[0]) if all(v is not None for v in ls4) else None
        R3 = R3s is not None and abs(R3s - 1) <= 0.1
        R4s = [((c['logsig4'] - p_['logsig4']) / math.log10(2)) if (c['logsig4'] is not None and p_['logsig4'] is not None) else None
               for p_, c in zip(Pt, Pct)]
        R4 = all(v is not None and abs(v - 1) <= 0.1 for v in R4s)
        Rp = all(R1) and all(R2) and R3 and R4
        E = [x['r_edge'] > 0 and 0.5 <= x['gN_over_ge'] <= 2 for x in Pt]
        Ep = all(E)
        S1 = [0.5 <= x['S1_ratio'] <= 2 for x in Pt]
        Sp = all(S1)          # S2 (budget stated) holds: it is printed below
        C1 = True             # P: f(x) = x, no number (by construction)
        C2 = all(abs(x['charge_dev']) <= 1e-12 for x in Pt)
        Cp = C1 and C2
        rcap = [math.sqrt(L.G * 10 ** lM / L.a0_of(f)) * math.sqrt(XCAP * (XCAP + 1)) for lM in MASSES]
        T1 = [(x['NG_near_edge'] is not None and x['NG_near_edge'] >= 1) and x['r_edge'] <= rc_ for x, rc_ in zip(Pt, rcap)]
        hom = ka.get('KA7', {}).get(f, {})
        T2 = bool(hom.get('T2_pass'))
        Tp = all(T1) and T2
        T3 = [x['r_edge'] >= rc_ for x, rc_ in zip(Pt, rcap)]
        g = {'H': H, 'R': Rp, 'E': Ep, 'S': Sp, 'C': Cp, 'T': Tp, 'R1': R1, 'R2': R2, 'R3_slope': R3s, 'R3': R3,
             'R4_by_mass': R4s, 'R4': R4, 'E_by_mass': E, 'S1_by_mass': S1, 'C2': C2, 'T1_by_mass': T1, 'T2': T2,
             'T3_reported': T3, 'R_cap': rcap}
        P(f'\nGates ({f}, P):')
        P(f'  H {"PASS" if H else "FAIL"}')
        P(f'  R {"PASS" if Rp else "FAIL"}: R1 slope {[x["slope"] for x in Pt]} (law {[x["slope_law"] for x in Pt]}) -> {R1}; '
          f'R2 amp {[x["amp"] for x in Pt]} -> {R2}; R3 d log s4/d log M_b {R3s} -> {R3}; R4 d log s4/d log c {R4s} -> {R4}')
        P(f'  E {"PASS" if Ep else "FAIL"}: r_edge {[round(x["r_edge"], 1) for x in Pt]} kpc vs r_e* {[round(x["r_e_star"], 1) for x in Pt]}; '
          f'g_N(r_edge)/g_e* {[round(x["gN_over_ge"], 4) for x in Pt]} (line 0.5-2)')
        P(f'  S {"PASS" if Sp else "FAIL"}: E_diss(M_c shells)/E_req {[x["S1_ratio"] for x in Pt]} (line 0.5-2); open budget: '
          f'E_diss total {[x["Ediss_total"] for x in Pt]} Msun (km/s)^2, radial momentum removed {[x["Pdiss_total"] for x in Pt]} Msun km/s; '
          f'E_req {[x["E_req"] for x in Pt]}. Heat reading: no energy leaves the clock, S1 = 0 -> FAIL')
        P(f'  C {"PASS" if Cp else "FAIL"}: C1 f(x) = x, no number (PASS by construction); C2 charge deviation {[x["charge_dev"] for x in Pt]}')
        P(f'  T {"PASS" if Tp else "FAIL"}: T1 median N_Gamma at r_e* {[x["NG_near_edge"] for x in Pt]} (line >= 1), r_edge <= R_cap '
          f'{[round(r_, 0) for r_ in rcap]}; T2 FRW (P vs MU1, homogeneous) {hom.get("max_rel_P_vs_MU1")} -> {T2}; '
          f'T3 reported (settled region reaching R_cap): {T3}')
        # ---- label ----
        if not H:
            lab = 'ILL-POSED'
        elif not (Rp and Ep):
            lab = 'RELAXES, NOT SETTLED'
        elif not (Sp and Cp and Tp):
            lab = 'SETTLES, NOT DERIVED'
        else:
            lab = 'JOINT DERIVED'
        # KA map: does a failing part rest only on failed KAs?
        ka_fail = [k for k, v in KA.items() if v is False]
        if ka_fail:
            P('  failed known answers:', ka_fail)
        # frozen KA map (s. 6) with A1's part-by-part KA5: a failing part counts only if all its KAs pass
        T2ok = bool(ka.get('KA7', {}).get(f, {}).get('KA7_pass'))
        parts = {'R1': (all(R1), ('KA1', 'KA3', 'KA5a', 'KA8')), 'R2': (all(R2), ('KA1', 'KA3', 'KA5a', 'KA8')),
                 'R3': (R3, ('KA1', 'KA3', 'KA5a', 'KA8')), 'R4': (R4, ('KA1', 'KA3', 'KA5a')),
                 'E': (Ep, ('KA3', 'KA5a', 'KA8', 'KA9')), 'S1': (Sp, ('KA5b', 'KA9')), 'T1': (all(T1), ('KA5a',)),
                 'T2': (T2, ('KA7',)), 'H': (H, ('KA2',))}
        def ka_ok(k):
            return T2ok if k == 'KA7' else KA.get(k) is True
        failing_sound = [p_ for p_, (ok_, kas) in parts.items() if not ok_ and all(ka_ok(k) for k in kas)]
        failing_unsound = [p_ for p_, (ok_, kas) in parts.items() if not ok_ and not all(ka_ok(k) for k in kas)]
        g['failing_parts_with_KAs_passing'] = failing_sound; g['failing_parts_resting_on_failed_KAs'] = failing_unsound
        P(f'  failing parts with all KAs passing: {failing_sound}; failing parts resting on a failed KA (NO VERDICT parts): {failing_unsound}')
        indep_fail = bool(failing_sound)
        if lab != 'JOINT DERIVED' and not indep_fail and ka_fail:
            lab = 'NO VERDICT'
        labels[f] = lab
        g['label'] = lab
        RES[f]['gates'] = g
        P(f'  LABEL ({f}): {lab}')
        # ---- P vs MU1, brackets ----
        P('\nP against MU1 (sink off), row by row:')
        for lM in MASSES:
            a, b = tab.get(('P', lM)), tab.get(('MU1', lM))
            if a and b:
                dre = (math.log10(a['r_edge'] / b['r_edge']) if a['r_edge'] > 0 and b['r_edge'] > 0 else None)
                dam = (a['amp'] - b['amp']) if (a['amp'] is not None and b['amp'] is not None) else None
                P(f'  log M_b {lM:g}: dlog r_edge {dre}, d amp {dam}, P N_Gamma max {a["NG_max"]:.3g}, P E_diss/E_req {a["S1_ratio"]:.3g}')
        # ---- MUTATE ----
        mu2 = [tab.get(('MU2', lM)) for lM in MASSES]
        if all(x is not None for x in mu2):
            re_ = [x['r_edge'] for x in mu2]
            if all(v > 0 for v in re_):
                sl = float(np.polyfit(MASSES, np.log10(re_), 1)[0]); bite2 = not (0.4 <= sl <= 0.6)
            else:
                sl = None; bite2 = True
            P(f'MU2 (c-free Gamma(rho), lambda 0.028): r_edge {[round(v, 1) for v in re_]}, d ln r_edge/d ln M_b {sl} -> '
              f'{"bites" if bite2 else "DOES NOT BITE"}')
            RES[f]['MU2'] = {'r_edge': re_, 'slope': sl, 'bites': bite2}
        b1 = [tab.get(('B1', lM)) for lM in MASSES]
        if all(x is not None for x in b1):
            P(f'B1 (as if standing, f = x on |g_pec|): N_Gamma at r_e* {[x["NG_near_edge"] for x in b1]}, E_diss/E_req '
              f'{[x["S1_ratio"] for x in b1]}, r_edge {[round(x["r_edge"], 1) for x in b1]}, amp {[x["amp"] for x in b1]}')
            RES[f]['B1'] = {'NG_near_edge': [x['NG_near_edge'] for x in b1], 'S1_ratio': [x['S1_ratio'] for x in b1]}
        if f == 'canonical':
            pairs = [(lM, tab.get(('MU1', lM)), tab.get(('B2_C1000', lM))) for lM in MASSES]
            pairs = [p_ for p_ in pairs if p_[1] is not None and p_[2] is not None]
            if pairs:
                bite1 = False
                for lM, x, y in pairs:
                    if (x['r_edge'] > 0) != (y['r_edge'] > 0):
                        bite1 = True
                    elif x['r_edge'] > 0 and abs(math.log10(x['r_edge'] / y['r_edge'])) > 0.15:
                        bite1 = True
                    if (x['amp'] is None) != (y['amp'] is None) or (x['amp'] is not None and y['amp'] is not None and abs(x['amp'] - y['amp']) > 0.1):
                        bite1 = True
                P(f'MU1 (sink off) against B2 C = 1000 at log M_b {[p_[0] for p_ in pairs]}: {"bites" if bite1 else "DOES NOT BITE"} '
                  f'(r_edge {[round(p_[1]["r_edge"], 1) for p_ in pairs]} vs {[round(p_[2]["r_edge"], 1) for p_ in pairs]}; '
                  f'amp {[p_[1]["amp"] for p_ in pairs]} vs {[p_[2]["amp"] for p_ in pairs]})')
                RES[f]['MU1_bites'] = bite1
            for k2 in ('B2_C10', 'B2_C100', 'B2_C1000', 'B3', 'B4'):
                xs = [(lM, tab.get((k2, lM))) for lM in MASSES]
                xs = [(lM, x) for lM, x in xs if x is not None]
                if xs:
                    ok = [x['r_edge'] > 0 and 0.5 <= x['gN_over_ge'] <= 2 for _, x in xs]
                    P(f'{k2:9s} at log M_b {[lM for lM, _ in xs]}: r_edge {[round(x["r_edge"], 1) for _, x in xs]}, '
                      f'gN/g_e* {[round(x["gN_over_ge"], 3) for _, x in xs]} (E {ok}), slope {[x["slope"] for _, x in xs]}, '
                      f'amp {[x["amp"] for _, x in xs]}, N_Gamma@r_e* {[x["NG_near_edge"] for _, x in xs]}, '
                      f'E_diss/E_req {[round(x["S1_ratio"], 3) for _, x in xs]}')
                    RES[f][k2] = {'logMb': [lM for lM, _ in xs], 'r_edge': [x['r_edge'] for _, x in xs],
                                  'NG_near_edge': [x['NG_near_edge'] for _, x in xs], 'S1_ratio': [x['S1_ratio'] for _, x in xs],
                                  'amp': [x['amp'] for _, x in xs]}
    RES['labels'] = labels
    P('\nLABELS:', labels)
    P('\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.')
    open(os.path.join(HERE, 'aks1_grade.out'), 'w').write('\n'.join(OUT) + '\n')
    json.dump(RES, open(os.path.join(HERE, 'aks1_grade.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
