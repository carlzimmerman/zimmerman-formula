#!/usr/bin/env python3
"""
CFG155 R5 (post hoc, written after both frozen runs of cfg155_eddington_referee.py): CFG130's printed numbers for the
point-mass Eddington headline, tabulated against this lane's code.

Reads (does not modify, does not run) ../CFG130_door5_fEL/D5_A_eddington_pointmass.out, its _results.json and the MUTATE
pair, and this lane's own _results.json files.  Evaluates this lane's Route B at CFG130's exact grid energies
(r_E = geomspace(1e-5, 1e5, 481)), both untruncated and with CFG130's actual cut, Phi_max = Phi(1e7 r_M) with no tail and
no boundary term (found only on opening its script; the frozen R3 rows used x_out = 1e5 and 1e6).
Spec tolerance (R5): f at matching E within 1e-3 relative.  Output: cfg155_compare_cfg130.out and _results.json.
"""
import hashlib
import importlib.util
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
C130 = os.path.join(HERE, '..', 'CFG130_door5_fEL')
spec_ = importlib.util.spec_from_file_location('ref', os.path.join(HERE, 'cfg155_eddington_referee.py'))
ref = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(ref)
LOG = []


def log(s=''):
    print(s, flush=True)
    LOG.append(s)


def main():
    sha = hashlib.sha256(open(os.path.join(HERE, '..', 'CFG155_FROZEN_CRITERIA.md'), 'rb').read()).hexdigest()
    log('spec campaign_fresh_gravity/CFG155_FROZEN_CRITERIA.md sha256 = ' + sha)
    log('R5 (post hoc): CFG130 D5_A printed numbers against CFG155 (read-only; CFG130 was not re-run)')
    tgt, mut, her, sis = ref.build_profiles()
    out130 = open(os.path.join(C130, 'D5_A_eddington_pointmass.out')).read()
    js130 = json.load(open(os.path.join(C130, 'D5_A_eddington_pointmass_results.json')))
    jm130 = json.load(open(os.path.join(C130, 'D5_A_eddington_pointmass_MUTATE_results.json')))
    js155 = json.load(open(os.path.join(HERE, 'cfg155_eddington_referee_results.json')))
    jm155 = json.load(open(os.path.join(HERE, 'cfg155_eddington_referee_MUTATE_results.json')))
    res = {'spec_sha256': sha, 'rows': []}
    rE130 = np.geomspace(1e-5, 1e5, 481)

    # ---- A3 rows: f at CFG130's printed energies
    a3 = out130.split('A3  f(E)')[1].split('A4 the analytic')[0]
    pat = re.compile(r'r_E =\s*([0-9.e+-]+)\s+E =\s*([0-9.e+-]+)\s+f =\s*([0-9.e+-]+)\s+f/Int\|\.\| =\s*([0-9.+-]+)')
    log()
    log('== f(E) at CFG130\'s printed energies (CFG130 cuts its t-integral at Phi(1e7 r_M), no tail, no boundary term) ==')
    log('  r_E          E(CFG130)      f(CFG130)     f(CFG155, full)   rel diff    f(CFG155, cut 1e7)  rel diff    tol 1e-3')
    worst_full = worst_cut = 0.0
    for m in pat.finditer(a3):
        rp, Ep, fp, ratio_p = (float(v) for v in m.groups())
        i = int(np.argmin(np.abs(rE130 - rp)))
        x = float(rE130[i])
        E = float(tgt.phi(np.array([x]))[0])
        f_full = ref.route_B(tgt, x)
        f_cut = ref.route_B(tgt, x, xtop=1e7)
        d_full, d_cut = fp / f_full - 1, fp / f_cut - 1
        worst_full, worst_cut = max(worst_full, abs(d_full)), max(worst_cut, abs(d_cut))
        log(f'  {x:.4e}  {Ep:+.5e}  {fp:.5e}   {f_full:.6e}      {d_full:+.1e}     {f_cut:.6e}        {d_cut:+.1e}'
            f'   E match {abs(E - Ep) <= 5e-6 * max(1, abs(Ep))}')
        res['rows'].append(dict(r_E=x, E_cfg130=Ep, f_cfg130=fp, f_cfg155_full=f_full, f_cfg155_cut1e7=f_cut,
                                rel_full=d_full, rel_cut=d_cut, f_over_Iabs_cfg130=ratio_p))
    log(f'  worst |rel diff|: against the full f {worst_full:.1e}; against the matched cut {worst_cut:.1e} '
        f'(CFG130 prints 6 significant digits, so ~5e-6 is its print resolution).  Within 1e-3: {worst_full <= 1e-3}')
    res['worst_rel_full'], res['worst_rel_cut'] = worst_full, worst_cut

    # ---- min f
    fmin130 = js130['numbers']['fE_min']
    x5 = 1e5
    fB5 = ref.route_B(tgt, x5)
    fB5c = ref.route_B(tgt, x5, xtop=1e7)
    log()
    log(f'== min f: CFG130 {fmin130:.10e} (at r_E = 1e5, its window end);  CFG155 full {fB5:.10e} '
        f'(rel {fmin130 / fB5 - 1:+.2e});  CFG155 with the cut at 1e7 {fB5c:.10e} (rel {fmin130 / fB5c - 1:+.2e}) ==')
    log(f'   CFG155 min over its own grid [1e-6, 1e6]: {js155["checks"]["H1b_f_positive_on_grid"]["min_f"]:.6e} at x_E = 1e6')
    res['min_f'] = dict(cfg130=fmin130, cfg155_full=fB5, cfg155_cut=fB5c)

    # ---- A4 Kepler, A5 round trip, A6 dlnf/dE
    m4 = re.search(r'f / f_Kepler = ([0-9.]+) at E = ([0-9.e+-]+)', out130)
    fK4 = ref.route_B(tgt, 1e-4) / float(ref.f_kepler(tgt.phi(np.array([1e-4]))[0]))
    log()
    log(f'== Kepler limit at r_E = 1e-4: CFG130 f/f_K = {m4.group(1)} (criterion 5%; README "to 4 digits"); '
        f'CFG155 {fK4:.12f} (|.-1| = {abs(fK4 - 1):.1e}); CFG155 at 1e-6 and 1e-5: '
        f'{js155["checks"]["Q3_kepler_limit"]["at_1e_6"]:.1e}, {js155["checks"]["Q3_kepler_limit"]["at_1e_5"]:.1e} ==')
    res['kepler'] = dict(cfg130=float(m4.group(1)), cfg155=fK4)
    log()
    log('== round trip rho(f)/rho_c - 1 ==')
    pat5 = re.compile(r'r =\s*([0-9.e+-]+): rho\(round trip\) = [0-9.e+-]+, target = [0-9.e+-]+, ratio - 1 =\s*([0-9.e+-]+)')
    rt = []
    for m in pat5.finditer(out130):
        r0, d130 = float(m.group(1)), float(m.group(2))
        rho_f, _ = ref.moments_from_f(tgt, r0)
        d155 = rho_f / float(tgt.rho(np.array([r0]))[0]) - 1
        rt.append(dict(r=r0, cfg130=d130, cfg155=d155))
        log(f'   r = {r0:7.0e}: CFG130 {d130:+.2e}   CFG155 {d155:+.2e}')
    res['roundtrip'] = rt
    log()
    log('== d ln f/dE (CFG130: np.gradient on its 48-per-decade grid, r_E in (1e-3, 1e3); CFG155: 5-point, Route A) ==')
    pat6 = re.compile(r'r_E =\s*([0-9.e+-]+)\s+E =\s*([0-9.e+-]+)\s+d ln f/dE =\s*([0-9.e+-]+)')
    a6 = out130.split('A6  LYNDEN-BELL')[1]
    dl = []
    for m in pat6.finditer(a6):
        r0, d130 = float(m.group(1)), float(m.group(3))
        i = int(np.argmin(np.abs(rE130 - r0)))
        x = float(rE130[i])
        fa = float(ref.route_A(tgt, np.array([x]))[0])
        fp = float(ref.fd5(tgt, np.array([x]), lambda xm: ref.route_A(tgt, xm))[0])
        dl.append(dict(r_E=x, cfg130=d130, cfg155=fp / fa))
        log(f'   r_E = {x:.3e}: CFG130 {d130:+.4e}   CFG155 {fp / fa:+.4e}   diff {d130 - fp / fa:+.1e}')
    rng130 = js130['numbers']['dlnf_dE_range']
    R2 = js155['rows']['R2']
    log(f'   range: CFG130 [{rng130[0]:+.4f}, {rng130[1]:+.4f}];  CFG155 max {R2["max_dlnf_dE"]:+.4f} at x_E = '
        f'{R2["x_at_max"]:.3f}, {R2["at_1e5"]:+.4f} at x_E = 1e5')
    # the same np.gradient as CFG130 (second order, its 48-per-decade grid, r_E in (1e-3, 1e3)) applied to CFG155's f
    sel = (rE130 > 1e-3) & (rE130 < 1e3)
    fsel = np.array([ref.route_B(tgt, float(x)) for x in rE130[sel]])
    gsel = np.gradient(np.log(fsel), tgt.phi(rE130[sel]))
    i1 = int(np.argmin(np.abs(rE130[sel] - 1.0)))
    log(f'   CFG130\'s np.gradient on its grid applied to CFG155\'s f: {gsel[i1]:+.6e} at r_E = 1, range '
        f'[{gsel.min():+.6f}, {gsel.max():+.6f}]  (reproduces CFG130\'s printed values: the r_E = 1 gap is the '
        f'coarse-grid gradient, not f)')
    res['dlnf'] = dict(points=dl, cfg130_range=rng130, cfg155_max=R2['max_dlnf_dE'], cfg155_at_1e5=R2['at_1e5'],
                       cfg130_gradient_on_cfg155_f=dict(at_r1=float(gsel[i1]), range=[float(gsel.min()),
                                                                                      float(gsel.max())]))

    # ---- CFG130's integrand as its code builds it (sympy, NOT simplified before lambdify) against the exact closed form
    import sympy as sp
    r_ = sp.symbols('r', positive=True)
    s_ = sp.sqrt(1 + r_ ** 2)
    rs_, gs_ = 1 / (4 * sp.pi * r_ * s_), s_ / r_ ** 2
    rpp130 = sp.lambdify(r_, sp.diff(sp.diff(rs_, r_) / gs_, r_) / gs_, 'numpy')
    exact = lambda x: x ** 5 / (np.pi * (1 + x * x) ** 3.5)
    log()
    log('== CFG130\'s rho\'\' as its code builds it (unsimplified sympy, then lambdify) against x^5/(pi (1+x^2)^(7/2)) ==')
    hyg = []
    for x in 10.0 ** np.arange(-8, 8):
        v, e = float(rpp130(np.array([x]))[0]), float(exact(x))
        hyg.append(dict(r=x, cfg130_form=v, exact=e, rel=v / e - 1))
        log(f'   r = {x:7.0e}: CFG130 form {v:+.4e}   exact {e:.4e}   rel err {v / e - 1:+.1e}')
    xs_n = np.geomspace(1e-5, 1e-2, 3001)
    N = float(np.max(np.abs(rpp130(xs_n) - exact(xs_n))))
    E5 = float(tgt.phi(np.array([1e-5]))[0])
    T = math.sqrt(float(tgt.phi(np.array([1e-2]))[0]) - E5)
    f5 = ref.route_B(tgt, 1e-5)
    bound = ref.C2 * N * T / f5
    log(f'   max |error| on r in [1e-5, 1e-2]: {N:.1e};  its effect on f at r_E = 1e-5 (CFG130\'s inner end) is below '
        f'C2 N T / f = {bound:.1e} (T = sqrt(Phi(1e-2) - E) = {T:.0f})')
    res['cfg130_rho2_form'] = dict(rows=hyg, max_abs_err_1e_5_to_1e_2=N, effect_bound_on_f_at_1e_5=bound)

    # ---- the MUTATE controls (different mutations; both must bite)
    log()
    log('== MUTATE controls (different mutations) ==')
    log(f'   CFG130: shell bump x (1 + 3 exp(-(ln r - 1)^2/0.18)); f < 0 at r_E in {jm130["numbers"]["negative_r_range"]}, '
        f'min f {jm130["numbers"]["fE_min"]:.4e}, {jm130["numbers"]["n_negative"]} of 481 energies; '
        f'load-bearing failures {jm130["load_bearing_failures"]}')
    hb = jm155['checks']['H1b_f_positive_on_grid']
    log(f'   CFG155: cored tracer (x_core = 0.1); f < 0 with certainty at {hb["n_neg_certain"]} of 1201 energies, '
        f'x_E from 1e-6 to 0.138; min f {hb["min_f"]:.4e} at x_E = {hb["x_at_min_f"]:.3e}; exit code {jm155["exit_code"]}')
    res['mutate'] = dict(cfg130=jm130['numbers'], cfg155=dict(n_neg=hb['n_neg_certain'], min_f=hb['min_f'],
                                                              exit=jm155['exit_code']))
    ok = worst_full <= 1e-3
    log()
    log(f'R5 verdict: every f CFG130 prints for this headline agrees with CFG155 within 1e-3: {ok} '
        f'(worst {worst_full:.1e}; {worst_cut:.1e} once CFG130\'s cut is matched)')
    res['within_tolerance'] = ok
    open(os.path.join(HERE, 'cfg155_compare_cfg130.out'), 'w').write('\n'.join(LOG) + '\n')
    json.dump(res, open(os.path.join(HERE, 'cfg155_compare_cfg130_results.json'), 'w'), indent=1,
              default=lambda o: float(o) if isinstance(o, (np.floating,)) else str(o))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
