#!/usr/bin/env python3
"""QX13 post-result diagnostic (reported, not graded): which hosts fail to converge at c_min, and their case/err.
kappa = 1/2 FITTED; not theory closed."""
import sys, json, math, os, runpy
sys.argv = ['x']
L = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qx13.py'), run_name='diag')
sp, L3, A0K = L['solve_poly'], L['L3'], L['A0K']
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qx13.json')))
FCAP, R, r_ta = L3['FCAP'], L3['R'], L3['r_ta']
out = []
for f in A0K:
    c = d['foot'][f]['c_min']['c']; c2 = c * c; a0k = A0K[f]
    bad = []
    for nm, Mb, Ro in L3['G5SYS']:
        s = sp(L3['expdisc'](Mb, Ro), FCAP * R * Mb, c2, r_ta(Mb), a0k)
        if not s['conv']: bad.append(('G5', nm, s['case'], s['err']))
    seen = set()
    for p in L3['LE']:
        Mb = p['Mb'] / L3['MS']; key = round(math.log10(Mb), 6)
        if key in seen: continue
        seen.add(key); s = sp(L3['expdisc'](Mb, 3.2 * L3['rd_of'](Mb)), FCAP * R * Mb, c2, r_ta(Mb), a0k)
        if not s['conv']: bad.append(('KiDS', key, s['case'], s['err']))
    for e in L3['EL']:
        Mt = e['Mbar'](1e9); s = sp(e['Mbar'], FCAP * R * Mt, c2, r_ta(Mt), a0k)
        if not s['conv']: bad.append(('ell', round(math.log10(Mt), 2), s['case'], s['err']))
    xc = []
    for nm, pts in L3['clusters'].items():
        Ml, rl = pts[0]['Mb_last']; host = L3['profile_core']([q['r_kpc'] for q in pts], [q['M_b'] for q in pts], Ml, rl)
        s = sp(host, FCAP * R * Ml, c2, r_ta(Ml), a0k); xc.append((nm, s['case'], s['conv'], round(s['Ksh'] / max(s['K0'], 1e-300), 3), s['capped']))
        if not s['conv']: bad.append(('XCOP', nm, s['case'], s['err']))
    gbad = 0
    for fst in (0.0, 1.0):
        for gp in L3['GR']:
            Mbt = gp['g5'] * (1 + fst)
            host = L3['profile_core']([q['r_kpc'] for q in gp['pts']], [q['M_gas'] * (1 + fst) for q in gp['pts']], Mbt, gp['R5'])
            s = sp(host, FCAP * R * Mbt, c2, r_ta(Mbt), a0k)
            if not s['conv']: bad.append(('group', gp['name'], s['case'], s['err'])); gbad += 1
    out.append(f"[{f}] c_min {c:.2f}: non-converged hosts {len(bad)}: {bad}")
    out.append(f"[{f}] X-COP hosts (name, case, conv, K_sh/K_0, capped): {xc}")
print("\n".join(out)); open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diag_conv.out'), 'w').write("\n".join(out) + "\n")
