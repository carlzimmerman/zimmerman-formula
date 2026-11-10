#!/usr/bin/env python3
"""FLD1 grader: R_fold(z; M_b) from runs/, against SPARC last radii, ONE1's KiDS windows, RC100 at 2.2 R_e, PD1's cap.
Also KA1b, KA1c, KA3, MUTATE and brackets (FROZEN_CRITERIA.md sections 3-7; AMENDMENT_A1.md).

    python3 fld1_compare.py -> fld1_compare.json / fld1_compare.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import csv, glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'COL1_clock_collapse'))
import col1_lib as L
G = L.G; GSI = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
OUT, RES = [], {}


def P(*a):
    s = ' '.join(str(x) for x in a); print(s); OUT.append(s)


def load(name):
    p = os.path.join(HERE, 'runs', name + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def name(f, M, zi=10, N=2400, mode='hubble', extra=''):
    return f'{mode}_{f}_M{M:g}_zi{zi:g}_N{N}{extra}'


def at_z(run, z, col=2):
    S = np.array(run['series']); zz = S[:, 1]
    o = np.argsort(zz)
    return float(np.interp(z, zz[o], S[o, col]))


def rfold_table(f):
    rows = {M: load(name(f, M)) for M in MASSES}
    return {M: r for M, r in rows.items() if r is not None}


def rfold(tab, z, lM):
    Ms = sorted(tab); R = np.array([at_z(tab[M], z) for M in Ms])
    lMc = min(max(lM, Ms[0]), Ms[-1])
    if np.any(R <= 0):
        return float(np.interp(lMc, Ms, R))
    return float(10 ** np.interp(lMc, Ms, np.log10(R)))


def sparc():
    d = os.path.join(REPO, 'real_research', 'data'); out = []
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(d, 'SPARC_Lelli2016c.mrt')):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            tab[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
        except ValueError:
            continue
    for fn in sorted(os.listdir(os.path.join(d, 'sparc_data'))):
        if not fn.endswith('_rotmod.dat'):
            continue
        try:
            a = np.genfromtxt(os.path.join(d, 'sparc_data', fn), comments='#')
        except Exception:
            continue
        if a.ndim != 2 or a.shape[1] < 6:
            continue
        nm = fn.replace('_rotmod.dat', '')
        if nm not in tab:
            continue
        m = tab[nm]
        out.append({'name': nm, 'R_last': float(a[:, 0].max()), 'L36': m['L36'] * 1e9, 'MHI': m['MHI'] * 1e9})
    return out


def kids_edges():
    return np.load(os.path.join(REPO, 'real_research', 'data', 'lensing_rar', 'cfg110_perlens.npz'))['gbar_edges']


def R_of_g(M, g):
    return math.sqrt(GSI * M * MSUN / g) / KPC


def rc100():
    rows = []
    with open(os.path.join(REPO, 'data_assembly', 'rc100_provenance', 'rc100_table3_six_fields_paper_values.csv')) as fh:
        for r in csv.DictReader(fh):
            rows.append({'idx': int(r['idx']), 'name': r['name'], 'z': float(r['z']), 'logM': float(r['logMbar_Msun']), 'Re': float(r['Re_kpc'])})
    return rows


def main():
    P('FLD1 compare. kappa = 1/2 FITTED; not theory closed. Footings never pooled.')
    ka = json.load(open(os.path.join(HERE, 'fld1_ka.json')))
    E = kids_edges()
    SP = sparc(); RC = rc100()
    RES['n_sparc'] = len(SP); RES['n_rc100'] = len(RC)
    P(f'inputs: SPARC galaxies {len(SP)} (QX8 loader); RC100 rows {len(RC)}; KiDS g_bar edges {len(E)}')
    # ---------- known answers from runs ----------
    base = load(name('canonical', 10.45)); pert = load(name('canonical', 10.45, extra='_perturb'))
    zs = [4, 2, 1, 0]
    d1b = max(abs(at_z(pert, z) - at_z(base, z)) / max(at_z(base, z), 1e-300) for z in zs)
    ka1b = d1b <= 1e-3
    P(f'KA1b round-off: max rel change of R_fold at z 4/2/1/0 under r x (1 + 1e-12): {d1b:.2e} (line 1e-3) -> {"PASS" if ka1b else "FAIL"}')
    ka1c_ok = True; rows1c = {}
    for f in ('canonical', 'alt'):
        for M in (9.4, 10.45, 10.7, 10.9):
            r = load(name(f, M, extra='_a4'))
            col1 = json.load(open(os.path.join(HERE, '..', 'COL1_clock_collapse', 'runs', f'outer_{f}_M{M:g}.json')))
            t3n = r['first_crossing_outside']['3']['t_since_start_gyr']; t3o = col1['first_crossing_outside']['3.0']['t_since_start_gyr']
            dev = abs(t3n - t3o) / t3o; ka1c_ok = ka1c_ok and dev <= 0.02
            new = [r['first_crossing_outside'][k] for k in ('10', '30', '100')]
            old = [col1['first_crossing_outside'][k] for k in ('10.0', '30.0', '100.0')]
            rows1c[f'{f}|{M}'] = {'t3_new': t3n, 't3_A4': t3o, 'dev': dev,
                                  'new_10_30_100': [x['t_since_start_gyr'] if x else None for x in new],
                                  'A4_10_30_100': [x['t_since_start_gyr'] if x else None for x in old]}
            P(f'KA1c {f} {M}: 3 kpc {t3n:.3f} vs A4 {t3o:.3f} ({dev:.1e}); 10/30/100 kpc corrected '
              + ' / '.join('none' if x is None else f'{x["t_since_start_gyr"]:.3f}' for x in new)
              + ' vs A4 ' + ' / '.join('none' if x is None else f'{x["t_since_start_gyr"]:.3f}' for x in old))
    P(f'KA1c: {"PASS" if ka1c_ok else "FAIL"}')
    n12, n24, n48 = load(name('canonical', 10.45, N=1200)), base, load(name('canonical', 10.45, N=4800))
    conv = []
    for z in zs:
        a, b, c = at_z(n12, z), at_z(n24, z), at_z(n48, z)
        conv.append((z, a, b, c, abs(b - c) / c if c > 0 else float('nan')))
    ka3 = all(x[4] <= 0.05 for x in conv if x[3] > 0)
    P('KA3 convergence (canonical 10.45) R_fold N 1200 / 2400 / 4800: ' + '; '.join(f'z {x[0]}: {x[1]:.1f} / {x[2]:.1f} / {x[3]:.1f} ({x[4]:.3f})' for x in conv)
      + f' -> {"PASS" if ka3 else "FAIL"} (line 5 %)')
    kas = {'KA1a': ka['KA1a']['pass'], 'KA1b': ka1b, 'KA1c': ka1c_ok, 'KA2': ka['KA2']['pass'], 'KA3': ka3}
    RES['known_answers'] = kas; RES['KA1c'] = rows1c; RES['KA3'] = conv; RES['KA1b'] = d1b
    allka = all(kas.values())
    # ---------- per footing ----------
    RES['footings'] = {}
    for f in ('canonical', 'alt'):
        a0 = L.a0_of(f); tab = rfold_table(f)
        R = RES['footings'][f] = {}
        P(f'\n=== {f} ===')
        # table
        T = {}
        for M in MASSES:
            if M not in tab:
                continue
            rM = math.sqrt(G * 10 ** M / a0)
            T[M] = {'R_fold': {z: at_z(tab[M], z) for z in (0, 1, 2, 4)}, 'R_ta': {z: at_z(tab[M], z, 3) for z in (0, 1, 2, 4)},
                    'R_cap': math.sqrt(59.5 * 60.5) * rM, 'r_M': rM,
                    'kids_inner_edge': R_of_g(10 ** M, E[7]), 'kids_middle_edge': R_of_g(10 ** M, E[4]), 'kids_outer_edge': R_of_g(10 ** M, E[0])}
            x = T[M]['R_fold'][0] / rM; T[M]['X_fold'] = (-1 + math.sqrt(1 + 4 * x * x)) / 2
            P(f'log M_b {M:5g}: R_fold z0/1/2/4 = ' + ' / '.join(f'{T[M]["R_fold"][z]:.1f}' for z in (0, 1, 2, 4))
              + ' kpc; R_ta z0/1/2/4 = ' + ' / '.join(f'{T[M]["R_ta"][z]:.1f}' for z in (0, 1, 2, 4))
              + f'; PD1 cap {T[M]["R_cap"]:.1f}; X_fold {T[M]["X_fold"]:.2f}; KiDS inner/middle/outer edge {T[M]["kids_inner_edge"]:.0f} / {T[M]["kids_middle_edge"]:.0f} / {T[M]["kids_outer_edge"]:.0f}')
        R['table'] = {str(k): v for k, v in T.items()}
        # (a1) SPARC
        fails = []
        for g in SP:
            for ups in (0.5, 0.3, 0.8):
                Mb = ups * g['L36'] + 1.33 * g['MHI']
                lM = math.log10(Mb); rf = rfold(tab, 0.0, lM)
                g[f'ratio_{ups}'] = g['R_last'] / rf if rf > 0 else float('inf')
                g[f'logM_{ups}'] = lM
        beyond = [g for g in SP if g['ratio_0.5'] > 1]
        a1 = len(beyond) == 0
        R['SPARC'] = {'n': len(SP), 'n_beyond': len(beyond), 'n_beyond_ups0.3': sum(g['ratio_0.3'] > 1 for g in SP),
                      'n_beyond_ups0.8': sum(g['ratio_0.8'] > 1 for g in SP),
                      'worst': sorted(({'name': g['name'], 'R_last': g['R_last'], 'logM': g['logM_0.5'], 'ratio': g['ratio_0.5']} for g in SP),
                                      key=lambda d: -d['ratio'])[:15],
                      'median_ratio': float(np.median([g['ratio_0.5'] for g in SP])), 'out_of_grid': sum(g['logM_0.5'] < 6.5 or g['logM_0.5'] > 12 for g in SP)}
        P(f'(a1) SPARC: {len(beyond)} of {len(SP)} galaxies have R_last beyond R_fold(0) (Upsilon 0.3: {R["SPARC"]["n_beyond_ups0.3"]}, 0.8: {R["SPARC"]["n_beyond_ups0.8"]});'
          f' median R_last/R_fold {R["SPARC"]["median_ratio"]:.2f}; worst ' + ', '.join(f'{w["name"]} {w["ratio"]:.2f}' for w in R['SPARC']['worst'][:6])
          + f' -> {"PASS" if a1 else "FAIL"}')
        # (a2) KiDS
        k_in = all(T[M]['R_fold'][0] >= T[M]['kids_inner_edge'] for M in (9.4, 10.45, 10.7, 10.9))
        k_mid = all(T[M]['R_fold'][0] >= T[M]['kids_middle_edge'] for M in (9.4, 10.45, 10.7, 10.9))
        R['KiDS'] = {M: {'R_fold0': T[M]['R_fold'][0], 'inner_edge': T[M]['kids_inner_edge'], 'middle_edge': T[M]['kids_middle_edge'],
                         'inner_factor': T[M]['kids_inner_edge'] / T[M]['R_fold'][0], 'middle_factor': T[M]['kids_middle_edge'] / T[M]['R_fold'][0],
                         'X_fold': T[M]['X_fold']} for M in (9.4, 10.45, 10.7, 10.9)}
        P('(a2) KiDS: ' + '; '.join(f'{M}: R_fold {T[M]["R_fold"][0]:.0f} vs inner {T[M]["kids_inner_edge"]:.0f} (x{T[M]["kids_inner_edge"] / T[M]["R_fold"][0]:.2f}),'
                                     f' middle {T[M]["kids_middle_edge"]:.0f} (x{T[M]["kids_middle_edge"] / T[M]["R_fold"][0]:.2f}), X_fold {T[M]["X_fold"]:.1f}' for M in (9.4, 10.45, 10.7, 10.9))
          + f' -> inner {"PASS" if k_in else "FAIL"}, middle {"PASS" if k_mid else "FAIL"}')
        # (b) RC100
        rcrows = []
        for g in RC:
            rf = rfold(tab, g['z'], g['logM'])
            rcrows.append({**g, 'R_fold': rf, 'ratio_2.2': 2.2 * g['Re'] / rf if rf > 0 else float('inf'), 'ratio_4': 4 * g['Re'] / rf if rf > 0 else float('inf')})
        bb = [g for g in rcrows if g['ratio_2.2'] > 1]
        b_ok = len(bb) == 0
        R['RC100'] = {'n_beyond_2.2Re': len(bb), 'n_beyond_4Re': sum(g['ratio_4'] > 1 for g in rcrows),
                      'worst': sorted(rcrows, key=lambda d: -d['ratio_2.2'])[:10], 'median_ratio_2.2': float(np.median([g['ratio_2.2'] for g in rcrows]))}
        P(f'(b) RC100: {len(bb)} of {len(rcrows)} beyond R_fold(z) at 2.2 R_e ({R["RC100"]["n_beyond_4Re"]} at 4 R_e); median 2.2 R_e/R_fold {R["RC100"]["median_ratio_2.2"]:.2f};'
          ' worst ' + ', '.join(f'{w["name"]} z{w["z"]:.2f} x{w["ratio_2.2"]:.2f}' for w in R['RC100']['worst'][:5]) + f' -> {"PASS" if b_ok else "FAIL"}')
        # (c) PD1 cap
        capM = [M for M in MASSES if 7 <= M <= 11.5 and M in T]
        c_ok = all(T[M]['R_fold'][0] >= T[M]['R_cap'] for M in capM)
        R['cap'] = {M: {'R_fold0': T[M]['R_fold'][0], 'R_cap': T[M]['R_cap'], 'factor': T[M]['R_cap'] / T[M]['R_fold'][0]} for M in capM}
        P('(c) PD1 cap: ' + '; '.join(f'{M}: {T[M]["R_fold"][0]:.0f} vs {T[M]["R_cap"]:.0f} (x{T[M]["R_cap"] / T[M]["R_fold"][0]:.2f})' for M in capM)
          + f' -> {"PASS" if c_ok else "FAIL"}')
        lab = 'NO VERDICT' if not allka else ('FOLD COVERS THE LAW\'S RANGE' if (a1 and k_in and k_mid and b_ok and c_ok) else 'DOES NOT')
        R['lines'] = {'a1_SPARC': a1, 'a2_KiDS_inner': k_in, 'a2_KiDS_middle': k_mid, 'b_RC100': b_ok, 'c_cap': c_ok}
        R['label'] = lab
        P(f'LABEL {f}: {lab}')
    # ---------- MUTATE and brackets ----------
    b0 = at_z(base, 0)
    mut = {'law off (up)': (load(name('canonical', 10.45, extra='_lawoff')), +1), 'z_i 5 (down)': (load(name('canonical', 10.45, zi=5)), -1),
           'mass x 10 (up)': (load(name('canonical', 11.45)), +1)}
    RES['mutate'] = {}
    for k, (r, sgn) in mut.items():
        v = at_z(r, 0); ch = (v - b0) / b0; bites = sgn * ch >= 0.05
        RES['mutate'][k] = {'R_fold0': v, 'base': b0, 'rel_change': ch, 'bites': bites}
        P(f'MUTATE {k}: R_fold(0) {v:.1f} vs {b0:.1f} kpc ({ch:+.3f}) -> {"bites" if bites else "DOES NOT BITE"}')
    RES['brackets'] = {}
    for f in ('canonical', 'alt'):
        for M in (8, 10.45):
            pr = load(name(f, M))
            cells = {'z_i 10 (primary)': pr, 'z_i 20': load(name(f, M, zi=20)), 'z_i 30': load(name(f, M, zi=30)),
                     'mu_K 0.1': load(name(f, M, extra='_mu0.1'))}
            line = []
            for k, r in cells.items():
                if r is None:
                    continue
                line.append(f'{k}: R_fold z0 {at_z(r, 0):.1f}, z2 {at_z(r, 2):.1f}')
                RES['brackets'][f'{f}|{M}|{k}'] = {'R_fold0': at_z(r, 0), 'R_fold2': at_z(r, 2)}
            rest = load(name(f, M, mode='rest'))
            if rest:
                S = np.array(rest['series']); t_end = S[-1, 0]
                tP = np.array(pr['series'])[:, 0]
                r_at = lambda tt: float(np.interp(tt, S[:, 0], S[:, 2]))
                t_z2 = float(np.interp(2.0, np.array(pr['series'])[::-1, 1], tP[::-1]))
                line.append(f'at rest: R_fold at the end ({t_end:.1f} Gyr) {S[-1, 2]:.1f}, at the time z 2 has in the primary {r_at(t_z2):.1f}')
                RES['brackets'][f'{f}|{M}|at rest'] = {'R_fold_end': float(S[-1, 2]), 'R_fold_at_tz2': r_at(t_z2)}
            P(f'BRACKETS {f} {M}: ' + '; '.join(line))
    P('\nValidity of the law-dominated limit, (mu_K R)^2 <= 0.1: R <= ' + ', '.join(f'{math.sqrt(0.1) / (mu / 1000):.0f} kpc at mu_K {mu}' for mu in (0.1, 1.78, 3.71, 198.25)))
    json.dump(RES, open(os.path.join(HERE, 'fld1_compare.json'), 'w'), indent=1, default=str)
    open(os.path.join(HERE, 'fld1_compare.out'), 'w').write('\n'.join(OUT) + '\n\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n')


if __name__ == '__main__':
    main()
