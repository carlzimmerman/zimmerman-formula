#!/usr/bin/env python3
"""AKS1 known answers KA3-KA9 (FROZEN_CRITERIA.md s. 6).

    python3 aks1_ka.py [--only KA3,KA4,...] -> aks1_ka.out / aks1_ka.json
KA7 and KA8 read runs/*.json written by aks1_run.py (run that first). Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import aks1_lib as L

OUT, RES = [], {'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
SNAP = os.environ.get('AKS1_SNAP', '')


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def lsq_slope(x, y):
    return float(np.polyfit(x, y, 1)[0])


def ka3():
    """Bertschinger: sink off, pressure off, EdS, point seed; inner slope -9/4 over [0.01, 0.1] r_ta."""
    o = L.run('canonical', 11.0, key='off', N=3000, mu_Mpc=0, eds=True, Ms_seed=1e11, Xlo=0.53, Xhi=20.0, zi=300.0,
              verbose=True, snap_path=(os.path.join(SNAP, 'ka3.npz') if SNAP else None))
    r, v = o['_r'], o['_v']
    rta = float(r[v <= 0].max())
    prof = L.profile(o['_snaps'], o['_dm'], 1e11)
    rc = np.array(prof['r']); rho = np.array(prof['rho']); cnt = np.array(prof['count'])
    w = (rc >= 0.01 * rta) & (rc <= 0.1 * rta) & (cnt >= 5) & (rho > 0)
    s = lsq_slope(np.log10(rc[w]), np.log10(rho[w]))
    ok = abs(s + 2.25) <= 0.15
    P(f'KA3 Bertschinger (EdS, seed 1e11, N 3000, z_i 300): r_ta = {rta:.1f} kpc, {int(w.sum())} bins in [0.01, 0.1] r_ta, '
      f'slope {s:.3f} (line -2.25 +- 0.15) -> {"PASS" if ok else "FAIL"}; steps {o["steps"]}, {o["wall_s"]:.0f}s')
    # reported: slope over [0.03, 0.3] r_ta and the local slopes
    w2 = (rc >= 0.03 * rta) & (rc <= 0.3 * rta) & (cnt >= 5) & (rho > 0)
    s2 = lsq_slope(np.log10(rc[w2]), np.log10(rho[w2]))
    P(f'    reported: slope over [0.03, 0.3] r_ta = {s2:.3f}')
    RES['KA3'] = {'r_ta': rta, 'slope': s, 'slope_003_03': s2, 'nbins': int(w.sum()), 'pass': bool(ok),
                  'profile_r': rc[w].tolist(), 'profile_rho': rho[w].tolist()}


def ka4():
    """COL1's focusing check with this lane's leapfrog."""
    want = {9.4: 0.1533, 10.45: 0.0824, 10.7: 0.0712, 10.9: 0.0633}
    rows = []; allok = True
    for f in ('canonical', 'alt'):
        cos = L.cosmo_of(f)
        ti = cos.t_of_a(1 / 11.); H = cos.H_of_a(1 / 11.)
        for lM, tw in want.items():
            Mb = 10 ** lM; r0 = 0.01
            r, v, t = r0, H * r0, ti; dt = 1e-6

            def acc(t, r):
                a = cos.a_of_t(t); M = Mb * L.smoothstep((t - ti) / (1 / L.TU))
                return (-L.G * M * r / (r * r + 1.0) ** 1.5
                        + (-(4 * math.pi / 3) * L.G * (cos.nbar0 + cos.rhob0) * a ** -3 + cos.OL * cos.H0 ** 2) * r)
            A = acc(t, r); tz = None
            while t < ti + 1.0 / L.TU:
                vh = v + 0.5 * dt * A; rn = r + dt * vh
                if rn <= 1e-6 * r0:
                    tz = t + dt * (r - 1e-6 * r0) / (r - rn); break
                t += dt; r = rn; A = acc(t, r); v = vh + 0.5 * dt * A
            tg = (tz - ti) * L.TU if tz is not None else float('nan')
            ok = abs(tg / tw - 1) <= 1e-2
            allok &= ok
            rows.append({'footing': f, 'logMb': lM, 't_gyr': tg, 'COL1': tw, 'rel': tg / tw - 1, 'pass': bool(ok)})
            P(f'KA4 {f:9s} log M_b {lM:5g}: centre at {tg:.4f} Gyr vs COL1 {tw:.4f} (rel {tg / tw - 1:+.2e}) -> {"PASS" if ok else "FAIL"}')
    RES['KA4'] = {'rows': rows, 'pass': bool(allok)}


def ka5():
    """Energy: (a) sink off, (b) Gamma = 1000 |g|/c; static point mass, 5 M_b of shells at rest in 1-100 kpc."""
    st = {'Mb': 10 ** 10.5, 'Mc': 5 * 10 ** 10.5, 'r1': 1.0, 'r2': 100.0, 'T_gyr': 2.0}
    res = {}
    for tag, key, C in (('a', 'off', 1.0), ('b', 'gpec', 1000.0)):
        o = L.run('canonical', 10.5, key=key, C=C, N=2000, static=st)
        E0 = o['E0']; Eh = np.array(o['E_hist'])
        absdev = np.max(np.abs(Eh[:, 1] + (Eh[:, 2] if tag == 'b' else 0.0) - E0))
        dev = absdev / abs(E0)
        ok = dev <= 1e-3
        thr = absdev / max(abs(E0), Eh[-1, 2])           # reported (A1): relative to the energy through the sink
        res[tag] = {'E0': E0, 'max_rel_dev': float(dev), 'Ediss_end_over_E0': float(Eh[-1, 2] / abs(E0)), 'steps': o['steps'],
                    'dev_over_throughput': float(thr), 'pass': bool(ok)}
        P(f'KA5{tag} ({"sink off" if tag == "a" else "Gamma = 1000 |g|/c"}): E0 = {E0:.4e}, max |E{" + E_diss" if tag == "b" else ""} - E0|/|E0| = '
          f'{dev:.2e} (line 1e-3), E_diss/|E0| = {Eh[-1, 2] / abs(E0):.3f}, steps {o["steps"]} -> {"PASS" if ok else "FAIL"}'
          + (f'; reported (A1): deviation / max(|E0|, E_diss) = {thr:.2e}' if tag == 'b' else ''))
    res['pass'] = res['a']['pass'] and res['b']['pass']
    res['pass_a'] = res['a']['pass']; res['pass_b'] = res['b']['pass']   # A1 map: (a) dynamics, (b) S1 only
    RES['KA5'] = res


def law_phantom_window(f, lM, re):
    Mb = 10 ** lM; a0 = L.a0_of(f); rM = math.sqrt(L.G * Mb / a0)
    rc = L.PCEN; w = (rc >= 0.1 * re) & (rc <= re)
    s = rc[w] / rM
    rho = Mb / (2 * math.pi * rM ** 3 * s * np.sqrt(1 + 4 * s * s))
    slope = lsq_slope(np.log10(rc[w]), np.log10(rho))
    amp = float(np.mean(np.log10((2 * math.pi * L.G * rho * rc[w] ** 2) ** 2)) - math.log10(L.G * Mb * a0 / 4))
    return slope, amp, int(w.sum())


def ka6():
    rows = []
    for f in ('canonical', 'alt'):
        for lM in (9.0, 10.5, 11.5):
            ge, re = L.target_edge(f, 10 ** lM)
            s, a, n = law_phantom_window(f, lM, re)
            rows.append({'footing': f, 'logMb': lM, 'slope': s, 'amp_dex': a, 'nbins': n})
            P(f'KA6 {f:9s} log M_b {lM:4g}: the law\'s phantom over [0.1, 1] r_e* ({n} bins): slope {s:.3f}, R2 amplitude {a:+.3f} dex')
    RES['KA6'] = {'rows': rows}


def ka9():
    cfg = {'canonical': (7.1, 40.1, 126.9), 'alt': (6.5, 36.5, 115.5)}
    rows = []; allok = True
    for f in ('canonical', 'alt'):
        for lM, rcfg in zip((9.0, 10.5, 11.5), cfg[f]):
            ge, re = L.target_edge(f, 10 ** lM)
            ok = abs(re / rcfg - 1) <= 0.02; allok &= ok
            rows.append({'footing': f, 'logMb': lM, 'r_e_star': re, 'g_e_over_a0': ge / L.a0_of(f), 'CFG461': rcfg,
                         'rel': re / rcfg - 1, 'pass': bool(ok)})
            P(f'KA9 {f:9s} log M_b {lM:4g}: r_e* = {re:.2f} kpc (g_e* = {ge / L.a0_of(f):.5f} a0) vs CFG461 {rcfg} (rel {re / rcfg - 1:+.4f}) -> {"PASS" if ok else "FAIL"}')
    RES['KA9'] = {'rows': rows, 'pass': bool(allok)}


def ka7_ka8():
    rd = os.path.join(HERE, 'runs')
    out = {}
    for f in ('canonical', 'alt'):
        p = os.path.join(rd, f'HOM_{f}.json')
        if not os.path.exists(p):
            P(f'KA7 {f}: runs/HOM_{f}.json missing'); continue
        h = json.load(open(p))
        ok7 = h['max_rel_MU1_vs_FRW'] <= 1e-3; okT2 = h['max_rel_P_vs_MU1'] <= 1e-6
        out[f] = {'max_rel_MU1_vs_FRW': h['max_rel_MU1_vs_FRW'], 'max_rel_P_vs_MU1': h['max_rel_P_vs_MU1'],
                  'KA7_pass': bool(ok7), 'T2_pass': bool(okT2)}
        P(f'KA7 {f}: homogeneous MU1 vs FRW max |r/(a X) - 1| = {h["max_rel_MU1_vs_FRW"]:.2e} (line 1e-3) -> {"PASS" if ok7 else "FAIL"}; '
          f'T2: P vs MU1 max |Delta r/r| = {h["max_rel_P_vs_MU1"]:.2e} (line 1e-6) -> {"PASS" if okT2 else "FAIL"}')
    RES['KA7'] = out
    # KA8 needs the graded summary of P at N 1000 and 2000 (aks1_grade computes r_edge; import its function)
    try:
        import aks1_grade as GR
        a = json.load(open(os.path.join(rd, 'P_canonical_10.5.json')))
        b = json.load(open(os.path.join(rd, 'P_canonical_10.5_N1000.json')))
        ea, eb = GR.edge_and_window(a, 'canonical', 10.5), GR.edge_and_window(b, 'canonical', 10.5)
        dre = (abs(math.log10(ea['r_edge'] / eb['r_edge'])) if ea['r_edge'] > 0 and eb['r_edge'] > 0
               else (0.0 if ea['r_edge'] == eb['r_edge'] else float('inf')))
        damp = (abs(ea['amp'] - eb['amp']) if (ea['amp'] is not None and eb['amp'] is not None)
                else (0.0 if ea['amp'] is None and eb['amp'] is None else float('inf')))
        ok8 = dre <= 0.05 + 1e-9 and damp <= 0.03
        RES['KA8'] = {'r_edge_2000': ea['r_edge'], 'r_edge_1000': eb['r_edge'], 'dlog_r_edge': dre, 'amp_2000': ea['amp'],
                      'amp_1000': eb['amp'], 'damp': damp, 'pass': bool(ok8)}
        P(f'KA8 N 2000 vs 1000 (P, canonical, 10.5): r_edge {ea["r_edge"]:.1f} / {eb["r_edge"]:.1f} kpc (dlog {dre:.3f}, line 0.05); '
          f'R2 amp {ea["amp"]} / {eb["amp"]} (diff {damp:.3f}, line 0.03) -> {"PASS" if ok8 else "FAIL"}')
    except FileNotFoundError as e:
        P('KA8: missing', e)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--only', default='KA3,KA4,KA5,KA6,KA9,KA7')
    a = ap.parse_args(); todo = a.only.split(',')
    prev = {}
    pj = os.path.join(HERE, 'aks1_ka.json')
    if os.path.exists(pj) and a.only != 'KA3,KA4,KA5,KA6,KA9,KA7':
        prev = json.load(open(pj))
    if 'KA9' in todo: ka9()
    if 'KA6' in todo: ka6()
    if 'KA4' in todo: ka4()
    if 'KA5' in todo: ka5()
    if 'KA7' in todo: ka7_ka8()
    if 'KA3' in todo: ka3()
    prev.update(RES)
    P('\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.')
    tag = '' if a.only == 'KA3,KA4,KA5,KA6,KA9,KA7' else '_' + a.only.replace(',', '_')
    open(os.path.join(HERE, f'aks1_ka{tag}.out'), 'w').write('\n'.join(OUT) + '\n')
    json.dump(prev, open(pj, 'w'), indent=1, default=str)
