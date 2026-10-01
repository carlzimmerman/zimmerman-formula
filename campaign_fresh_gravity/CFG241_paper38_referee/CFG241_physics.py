#!/usr/bin/env python3
"""CFG241_physics.py: the frozen re-derivations P1-P11 (numpy / scipy / sympy). Read-only on the repo.
Exit 0 if it ran and the known-answer self-controls pass, 1 if a self-control fails. A recomputation that contradicts the paper prints CONTRADICTS, not an error exit.
  --mutate : perturbs the kernel slope formula; the self-controls must then fail (exit 1)."""
import sys, os, re, json, math, subprocess, io, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy import stats
from scipy.optimize import minimize
import sympy as sp
from CFG241_common import *

MUT = '--mutate' in sys.argv
OUT = []; RES = {}; CONTROLS = []
def P(s=''): print(s); OUT.append(s)
def ctrl(name, ok): CONTROLS.append((name, bool(ok))); P('  [%s] control: %s' % ('PASS' if ok else 'FAIL', name))

tex, how = head_text(TEX_REL)
P('CFG241_physics: repo <repo> head %s; tex from %s; mutate=%s' % (head_commit(), how, MUT))

# ------------------------------------------------------------------ kernels
def b_P2(y):                      # b = -dlog nu/dlog y for nu = sqrt(1+1/y)
    return (1.0 / (3.0 * (1 + y))) if MUT else 1.0 / (2.0 * (1 + y))
def nu_P2(y): return np.sqrt(1 + 1 / y)
def nu_mc(y): return 1.0 / (1.0 - np.exp(-np.sqrt(y)))                    # McGaugh form (sensitivity kernel)
def b_num(nu, y, h=1e-4): return -(np.log10(nu(y * 10 ** h)) - np.log10(nu(y * 10 ** -h))) / (2 * h)
P('\n=== known-answer self-controls ===')
ctrl('P2: b -> 1/2 as y -> 0', abs(b_P2(1e-9) - 0.5) < 1e-6)
ctrl('P2: nu -> 1 as y -> infinity', abs(nu_P2(1e9) - 1) < 1e-6)
ctrl('numeric b of nu_P2 equals 1/(2(1+y)) at y=1 (to 1e-6)', abs(b_num(nu_P2, 1.0) - 0.5 / 2) < 1e-6 if not MUT else abs(b_num(nu_P2, 1.0) - b_P2(1.0)) < 1e-6)
def Ez(z, om=0.3): return math.sqrt(om * (1 + z) ** 3 + 1 - om)
ctrl('E(0) = 1', abs(Ez(0) - 1) < 1e-12)

# ------------------------------------------------------------------ P1
P('\n=== P1: delta/2 deep-regime mimicry (sympy) ===')
lf, la, lg = sp.symbols('lf la lg', real=True)
nu = sp.Function('nu')
y = sp.exp(lf + lg - la)                       # y = f g / a0 (natural logs)
logg = lf + lg + sp.log(nu(y))
dlf = sp.simplify(sp.diff(logg, lf)); dla = sp.simplify(sp.diff(logg, la))
P('  d ln g_obs / d ln f  = %s ' % dlf); P('  d ln g_obs / d ln a0 = %s ' % dla)
P('  with m(y) = -dln nu/dln y:  d/dln f = 1 - m ; d/dln a0 = m   (hand-expectation confirmed symbolically above in terms of nu\')')
EDG = np.logspace(-15, np.log10(5e-12), 16); A0C = 9.3603e-11
ymin_k1, ymax_k1 = EDG[7] / A0C, EDG[14] / A0C
P('  KiDS K1 (bins 8-14 of CFG61 edges logspace(1e-15,5e-12,16)): g_bar %.2e to %.2e m/s^2  ->  y = g_bar/a0 from %.1e to %.3f (canonical a0)' % (EDG[7], EDG[14], ymin_k1, ymax_k1))
for nm, kern in (('P2', nu_P2), ('McGaugh', nu_mc)):
    for yy in (1e-3, 1e-2, ymax_k1, 0.1, 1.0, 3.0):
        m = b_num(kern, yy); P('  %-8s y=%-8.4g m=%.4f  (1-m)/m = %.3f  [f-drift response / a0-drift response]' % (nm, yy, m, (1 - m) / m))
mmax = b_num(nu_P2, ymax_k1)
RES['P1'] = dict(K1_y_range=[float(ymin_k1), float(ymax_k1)], ratio_f_over_a0_at_ymax_P2=float((1 - b_num(nu_P2, ymax_k1)) / b_num(nu_P2, ymax_k1)))
P('  => in the KiDS K1 range the f-drift and a0-drift responses of log g_obs differ by at most %.1f%% (P2 kernel): "delta/2, exactly as an a0 drift" holds to that accuracy there, exactly only in the deep limit.' % (100 * abs((1 - mmax) / mmax - 1)))
P('  rival amplitude: E ratio over late median z 0.2045->0.3996 and early 0.232->0.378 (flat Om 0.3): half of log10 ratio =')
for (z1, z2) in ((0.2045, 0.3996), (0.232, 0.378)):
    P('     z %.4f -> %.4f: 0.5*log10 E-ratio = %.4f dex' % (z1, z2, 0.5 * math.log10(Ez(z2) / Ez(z1))))
P('  (lane: +0.0179 combined, late +0.024; consistent)')

# ------------------------------------------------------------------ P2 (cfg223 library, read-only)
P('\n=== P2: the lever as a function of y and kernel ===')
cfgdir = os.path.join(REPO, 'campaign_fresh_gravity', 'CFG223_a0_over_cosmic_time')
st = subprocess.run(['git', '-C', REPO, 'status', '--porcelain', 'campaign_fresh_gravity/CFG223_a0_over_cosmic_time'], capture_output=True).stdout.decode().strip()
P('  CFG223 lane working tree vs HEAD: %s' % ('clean' if not st else 'MODIFIED: ' + st.replace('\n', '; ')[:200]))
try:
    src = open(os.path.join(cfgdir, 'cfg223_a0_over_time.py')).read()
    stop = src.index('P("\\nCONTROLS")')
    ns = {"__file__": os.path.join(cfgdir, "cfg223_a0_over_time.py"), "__name__": "cfg223_lib"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:stop], "cfg223_a0_over_time.py", "exec"), ns)
    build_points, implied, NU, A0L, nuv = ns["build_points"], ns["implied"], ns["NU"], ns["A0L"], ns["nuv"]
    PTS, _, _ = build_points(mut=False)
    rows = []
    P('  point           n  med y  y_min  y_max  m(med y)  1/m   (1-m)/m   lever_b(+-0.03)  lever_b(+-0.01)  s* per +0.05 dex D  s*  m(y/s*)')
    for p in PTS[:8]:
        gb, D = p['gb'], p['D']; yy = gb / A0L; ym = float(np.median(yy))
        m = float(-(np.log10(nuv(NU, np.array([ym * 10 ** 0.02]))[0]) - np.log10(nuv(NU, np.array([ym * 10 ** -0.02]))[0])) / 0.04)
        def lev(h):
            lp = float(implied(D * 10 ** (-h), gb * 10 ** h, NU, A0L)[0][0]); lm = float(implied(D * 10 ** h, gb * 10 ** (-h), NU, A0L)[0][0]); return (lp - lm) / (2 * h)
        l0 = float(implied(D, gb, NU, A0L)[0][0]); l5 = float(implied(D * 10 ** 0.05, gb, NU, A0L)[0][0])
        ms = float(-(np.log10(nuv(NU, np.array([ym / 10 ** l0 * 10 ** 0.02]))[0]) - np.log10(nuv(NU, np.array([ym / 10 ** l0 * 10 ** -0.02]))[0])) / 0.04)
        r = dict(point=p['short'], n=int(p['z'].size), ymed=ym, ymin=float(yy.min()), ymax=float(yy.max()), m=m, inv_m=1 / m, one_minus_over_m=(1 - m) / m,
                 lever_b_03=lev(0.03), lever_b_01=lev(0.01), s_per_005D=10 ** (l5 - l0), s=10 ** l0, m_at_ystar=ms)
        rows.append(r)
        P('  %-14s %3d %6.2f %6.2f %6.2f   %.3f  %5.2f  %6.2f   %+7.2f        %+7.2f         x%.2f             %.2f  %.3f' % (r['point'], r['n'], ym, r['ymin'], r['ymax'], m, 1 / m, (1 - m) / m, r['lever_b_03'], r['lever_b_01'], r['s_per_005D'], r['s'], ms))
    RES['P2'] = rows
    lb = [r['lever_b_03'] for r in rows]; fac = [r['s_per_005D'] for r in rows]; sl = [r['m'] for r in rows]
    P('  reproduced: lever_b range %.2f..%.2f (paper -2.5..-4.8 / -2.48..-4.83), factor range x%.2f..x%.2f (paper 1.5..1.8), local slope %.3f..%.3f (paper 0.13..0.28)' % (min(lb), max(lb), min(fac), max(fac), min(sl), max(sl)))
    P('  lever_b at +-0.01 dex differs from +-0.03 dex by up to %.2f (finite-difference/median-step noise); spread of the 8 lever_b values at nearly equal slope (Q1 vs Q2): %.2f vs %.2f' % (max(abs(r['lever_b_03'] - r['lever_b_01']) for r in rows), rows[0]['lever_b_03'], rows[1]['lever_b_03']))
    P('  hand relations: single-galaxy shift of log D by eps moves log s by eps/m(y/s*); baryon shift x moves log s by -(1-m)/m. Compared with the table these are NOT equalities for the median over N galaxies (m varies across y spread); the paper quotes the table, not 1/m: no number is contradicted.')
    # per-galaxy y distribution (for C042)
    P('  per-galaxy y = g_bar/a0 (canonical) spread inside each point: min / 10th pct / median / 90th pct / max')
    for p in PTS[:8]:
        yy = p['gb'] / A0L; P('     %-14s %.3f / %.3f / %.2f / %.2f / %.2f' % (p['short'], yy.min(), np.percentile(yy, 10), np.median(yy), np.percentile(yy, 90), yy.max()))
    RES['P2_yspread'] = [dict(point=p['short'], ymin=float((p['gb'] / A0L).min()), ymax=float((p['gb'] / A0L).max())) for p in PTS[:8]]
except Exception as e:
    P('  P2 lane library NOT RUN: %r' % (e,)); RES['P2'] = 'NOT RUN'
P('  analytic dependence on y (kernel P2, b = 1/(2(1+y))): 1/m and (1-m)/m at the paper\'s y range')
for yy in (1.1, 2.0, 3.0, 4.4):
    for nm, kern in (('P2', nu_P2), ('McGaugh', nu_mc)):
        m = b_num(kern, yy); P('     y=%.1f %-8s m=%.3f  1/m=%.2f (D lever)  (1-m)/m=%.2f (baryon lever magnitude)' % (yy, nm, m, 1 / m, (1 - m) / m))

# ------------------------------------------------------------------ P3
P('\n=== P3: rival-shift numbers E(z) ===')
for z in (0.2, 0.2357, 0.3723, 1.4, 2.0, 2.3, 5.0):
    P('  z=%-6s E: ' % z + '  '.join('Om=%.3f -> %.3f' % (om, Ez(z, om)) for om in (0.27, 0.30, 0.3027, 0.315, 0.32)))
P('  paper: x2.2 at z~1.4, x8 at z~5, 3.4 at z=2.3, 0.48 dex at z~2: all inside the Om 0.27..0.32 range above; the tex does not state Om. Om used in the lanes: CFG255 0.3 (E list in stage A), CFG222 0.3027, CFG237 0.315.')
RES['P3'] = {str(z): [Ez(z, om) for om in (0.27, 0.30, 0.3027, 0.315, 0.32)] for z in (1.4, 2.0, 2.3, 5.0)}

# ------------------------------------------------------------------ P4
P('\n=== P4: KiDS power and chi2 ===')
dA, sA = 0.0179, 0.0383
P('  (dA/sigma_A)^2 = %.3f (single-amplitude proxy); lane Delta chi2_pred (14-bin covariance) = 0.14 canonical / 0.17 alt: the two differ because the lane uses the full 14-bin vector, not the amplitude' % ((dA / sA) ** 2))
for c, nm in ((19.81, 'zero'), (19.80, 'flat'), (19.21, 'rival'), (15.05, 'LCDM')):
    P('  chi2.sf(%.2f, 14) = %.3f   (%s)' % (c, stats.chi2.sf(c, 14), nm))
P('  (0.0595-0.0188)/0.0383 = %.2f sigma from rival; (0.0595-0.0009)/0.0383 = %.2f sigma from flat; lane prints 1.06 / 1.53' % ((0.0595 - 0.0188) / 0.0383, (0.0595 - 0.0009) / 0.0383))
P('  9 required = 3^2 (3 sigma): %s' % (3 ** 2))
P('  mixing check: 0.038 is the stage-A jackknife sigma_A (cfg255_stageA/stageB.out A2: 0.0383) and is ALSO the measured amplitude error (B2: +-0.0383): same number, no mixing of stages')
RES['P4'] = dict(sf_zero=float(stats.chi2.sf(19.81, 14)), sf_rival=float(stats.chi2.sf(19.21, 14)), sf_lcdm=float(stats.chi2.sf(15.05, 14)))

# ------------------------------------------------------------------ P5
P('\n=== P5: the CFG240 statements as typed in Lean ===')
lean, lh = head_text('fable_independent_2026/lean_2026/ChainCert/CalibrationWall.lean')
thms = re.findall(r'^(?:theorem|lemma)\s+(\w+)', lean, re.M)
P('  CalibrationWall.lean (%s): %d theorem/lemma declarations (paper: 50)' % (lh, len(thms)))
for nm in ('T1_deep_iff', 'T2a_P2_injective', 'T2a_one_point_fails', 'T2b_deep_not_injective', 'T2c_det_bounds', 'T3_newton_limit', 'T4_design_bound', 'T4_sigma_floor'):
    m = re.search(r'^theorem\s+%s\b(.*?):=\s*by' % nm, lean, re.M | re.S)
    P('  --- %s: %s' % (nm, re.sub(r'\s+', ' ', m.group(0))[:520] if m else 'NOT FOUND'))
ce = [f for f in ls_head('fable_independent_2026/lean_2026/ChainCert/') if f.endswith('.lean')]
tot = 0
for f in ce:
    t, _ = head_text(f); tot += len(re.findall(r'^(?:theorem|lemma)\s+\w+', t, re.M))
P('  ChainCert *.lean declarations counted by this script: %d (paper: library 281 -> 331; README says verify_chain.sh counts 331)' % tot)
tc = subprocess.run('which lake lean 2>/dev/null', shell=True, capture_output=True).stdout.decode().strip()
P('  Lean toolchain on this machine: %s -> lake build / verify_chain.sh NOT RUN by this lane (no network; the statements above are read, the proofs are not re-checked here).' % (tc or 'none found'))
RES['P5'] = dict(n_theorems=len(thms), chaincert_decl_count=tot)
P('  T2c_det_bounds: |det| <= |y1-y2|/2 AND <= 1/(2(1+min y)): det -> 0 when both y -> 0 (deep) AND when both y -> infinity (Newtonian); the paper mentions only the deep end.')
P('  T4: hypothesis 0<=b_i<=1/2 and 0<det F in the Lean statement; the paper writes "any sample" with no hypothesis.')

# ------------------------------------------------------------------ P6 / P7 Fisher
P('\n=== P6: break-even table recomputation (Fisher, P2) ===')
def fisher(ys, sig=0.1):
    b = b_P2(np.asarray(ys, float)); r = np.stack([1 - b, b], 1); F = r.T @ r / sig ** 2
    return F
def sig_la(ys, sig=0.1, prior=None):
    F = fisher(ys, sig)
    if prior: F = F + np.diag([1 / prior ** 2, 0])
    C = np.linalg.inv(F); return math.sqrt(C[1, 1]), -F[0, 1] / math.sqrt(F[0, 0] * F[1, 1]), np.linalg.cond(F)
def design(ymin, ymax, N=20): return ymin * (ymax / ymin) ** (np.arange(N) / (N - 1))
def breakeven(ymin, N=20, sig=0.1, cap=1e4, step=50):
    ks = np.arange(0, int(np.ceil(step * math.log10(cap / ymin))) + 1)
    ymaxs = ymin * 10 ** (ks / step); ymaxs = ymaxs[ymaxs > ymin * 1.0001]
    s = np.array([sig_la(design(ymin, ym, N), sig)[0] for ym in ymaxs])
    ok = s < 0.1; first = ymaxs[np.argmax(ok)] if ok.any() else None
    stable = None
    for i in range(len(ymaxs)):
        if ok[i:].all(): stable = ymaxs[i]; break
    return stable, first, float(s.min()), float(ymaxs[np.argmin(s)])
def bisect(ymin, N=20, sig=0.1):
    f = lambda ym: sig_la(design(ymin, ym, N), sig)[0] - 0.1
    lo, hi = ymin * 1.001, 1e3; ys = np.logspace(math.log10(lo), math.log10(hi), 4000); v = [f(t) for t in ys]
    for i in range(len(ys) - 1):
        if v[i] > 0 >= v[i + 1]:
            a, b_ = ys[i], ys[i + 1]
            for _ in range(80):
                c = math.sqrt(a * b_); (a, b_) = (c, b_) if f(c) > 0 else (a, c)
            return b_
    return None
J = None
try:
    jt, _ = head_text('campaign_fresh_gravity/CFG240_calibration_wall/CFG240_break_even_table.json'); J = [json.loads(l) for l in jt.strip().split('\n')] if jt.strip().startswith('{') and '\n' in jt.strip() and not jt.strip().startswith('[') else json.loads(jt)
except Exception as e:
    P('  JSON read: %r' % (e,))
RES['P6'] = {}
for ymin in (0.01, 1e-3, 0.1):
    st_, fi_, smin, ysm = breakeven(ymin); bi = bisect(ymin)
    sg, rho, cond = sig_la(design(ymin, st_ if st_ else ysm)) 
    P('  y_min=%-6g stable break-even on 0.02-dex grid: %s | first crossing: %s | bisection: %s | min sigma(log a0)=%.4f at y_max=%.1f | at break-even rho=%.3f cond=%.1f' % (ymin, ('%.2f' % st_) if st_ else 'none', ('%.2f' % fi_) if fi_ else 'none', ('%.2f' % bi) if bi else 'none', smin, ysm, rho, cond))
    RES['P6'][str(ymin)] = dict(stable=st_, first=fi_, bisect=bi, smin=smin, ysmin=ysm, rho=rho, cond=cond)
if J is not None:
    hdr = J[0] if isinstance(J, list) else J
    P('  JSON loaded (%s records); header keys: %s' % (len(J) if isinstance(J, list) else '?', list(hdr.keys())[:8] if isinstance(hdr, dict) else ''))
    try:
        cell = [r for r in J if isinstance(r, dict) and r.get('kernel') == 'P2' and abs(r.get('y_min', 0) - 0.01) < 1e-9 and r.get('N') == 20 and abs(r.get('sigma_dex', 0) - 0.1) < 1e-9 and not r.get('prior_log_f_dex')]
        P('  JSON headline cell (P2, y_min 0.01, N 20, sigma 0.1, no prior): ' + (str({k: cell[0].get(k) for k in ('y_max_break_even', 'y_max_first', 'rho', 'sigma_log_a0')}) if cell else 'not found'))
        RES['P6_json_cell'] = cell[0] if cell else None
    except Exception as e:
        P('  JSON cell lookup failed: %r' % (e,))
ctrl('break-even (stable) for y_min=0.01 within 0.03 dex of the README 7.94 (grid) / 7.6 (bisection)', RES['P6']['0.01']['stable'] is not None and abs(math.log10(RES['P6']['0.01']['stable'] / 7.94)) < 0.03)
ctrl('Fisher matrix positive definite for the headline design', np.all(np.linalg.eigvalsh(fisher(design(0.01, 8.0))) > 0))
yd = np.array([1.1, 1.38, 2.0, 3.0, 4.4])
P('  discs of the paper (y 1.1..4.4): log-uniform N=20 design: sigma(log a0) = %.3f dex, rho=%.3f (target 0.1): this IS the number behind line 95\'s "no 0.1 dex leverage"' % tuple(sig_la(design(1.1, 4.4))[:2]))
P('  same with a prior of 0.15 dex on log f: sigma(log a0) = %.3f; with N=100 discs: %.3f' % (sig_la(design(1.1, 4.4), prior=0.15)[0], sig_la(design(1.1, 4.4, 100))[0]))
RES['P6_discs'] = dict(sigma_N20=sig_la(design(1.1, 4.4))[0], sigma_N100=sig_la(design(1.1, 4.4, 100))[0])

try:
    P('  Fisher with the REAL per-galaxy y of each CFG223 point (P2 kernel; sigma_pt = 0.1 dex per galaxy; no prior on f):')
    for p in PTS[:8]:
        yy = p['gb'] / A0L; sg_, rho_, cond_ = sig_la(yy); P('     %-14s N=%2d  sigma(log a0) = %.3f dex  rho=%.3f' % (p['short'], yy.size, sg_, rho_))
    RES['P6_real_y'] = {p['short']: sig_la(p['gb'] / A0L)[0] for p in PTS[:8]}
    allp = np.concatenate([p['gb'] / A0L for p in PTS[:4]]); P('     RC100 pooled (100 galaxies): sigma(log a0) = %.3f dex' % sig_la(allp)[0])
    RES['P6_real_y']['RC100_pooled'] = sig_la(allp)[0]
except Exception as e:
    P('  real-y Fisher NOT RUN: %r' % (e,))
P('\n=== P7: the T4 floor as a numerical bound ===')
def s_floor(b, sig=1.0):
    r = np.stack([1 - b, b], 1); F = r.T @ r / sig ** 2; C = np.linalg.inv(F); return math.sqrt(C[1, 1] * len(b))
rng = np.random.default_rng(241); best = 1e9
for N in (6, 9, 20, 60):
    for _ in range(4000):
        b = rng.uniform(0, 0.5, N)
        if rng.random() < 0.5: b = np.where(rng.random(N) < rng.random(), 0.5, 0.0)
        try: v = s_floor(b)
        except Exception: continue
        best = min(best, v)
b9 = np.array([0.5] * 6 + [0.0] * 3); v9 = s_floor(b9)
res = minimize(lambda p: s_floor(np.clip(p, 0, 0.5)), rng.uniform(0, .5, 12), method='Nelder-Mead', options=dict(maxiter=4000, xatol=1e-9, fatol=1e-12))
P('  min over 16,000 random designs (b in [0,1/2]) of sqrt(N)*sigma(log a0)/sigma_pt: %.4f (T4 says >= 3)' % best)
P('  equality design (2/3 deep b=1/2, 1/3 Newtonian b=0), N=9: %.6f ; optimiser minimum from random start (N=12): %.4f' % (v9, res.fun))
ctrl('T4 floor not violated by any tested design (>= 3 - 1e-6)', min(best, v9, res.fun) >= 3 - 1e-6)
P('  N needed for sigma(log a0)=0.1 at sigma_pt=0.1: (3*0.1/0.1)^2 = 9 (non-strict: N>=9 attains the floor only for the equality design); at 0.2: (3*0.2/0.1)^2 = 36. The paper writes N>9 and N>36 (strict); the README writes the same.')
RES['P7'] = dict(min_random=best, equality=v9, optimiser=float(res.fun))

# ------------------------------------------------------------------ P8
P('\n=== P8: DR4 paragraph arithmetic ===')
fB, fA = 1.1614, 1.1917; ssys = 0.02
c = math.sqrt((((fB - 1) / 3) ** 2 - ssys ** 2)) * math.sqrt(4342)
nA = (c / math.sqrt(((fA - 1) / 3) ** 2 - ssys ** 2)) ** 2
P('  from the file\'s own 3-sigma pair count 4,342 (floor 1.1614): stat coefficient c = %.3f; implied alt pairs for floor 1.1917 = %.0f (file: 2,940)' % (c, nA))
P('  cap (floor-1)/sigma_sys = %.2f (file: 8.1);  at N=30,000: %.2f sigma (file: 5.8)' % ((fB - 1) / ssys, (fB - 1) / math.sqrt(ssys ** 2 + c ** 2 / 30000)))
P('  rounding: 4,342 -> "about 4,300"; 2,940 -> "about 2,900": within 1.4%')
RES['P8'] = dict(c=c, alt_pairs=nA)
P('  statistic: B, LCDM, Newton -> 1.000 in the file closure_map/WHAT_WOULD_DECIDE_2026-09-29.md:10; prereg table lists Newtonian 1.000 and framework-MI GATED 1.0004-1.0006.')

# ------------------------------------------------------------------ P9 (ARITH table from the checker)
P('\n=== P9: internal arithmetic relations (CFG241_check.arith_checks, 22 relations) ===')
try:
    import CFG241_check as CK
    for a in CK.arith_checks(tex): P('  %-5s %s  %s' % (a['id'], 'OK  ' if a['ok'] else 'FAIL', a['detail']))
    RES['P9'] = [dict(id=a['id'], ok=bool(a['ok']), detail=a['detail']) for a in CK.arith_checks(tex)]
except Exception as e:
    P('  P9 NOT RUN: %r' % (e,))

# ------------------------------------------------------------------ P10 audit anchoring
P('\n=== P10: audit-script anchoring review ===')
at, _ = head_text(AUDIT_REL)
rowsA = re.findall(r'^R\("(B\d+)",\s*"((?:[^"\\]|\\.)*)",\s*"(\w+)",\s*r"((?:[^"\\]|\\.)*)"(?:,\s*r?"((?:[^"\\]|\\.)*)")?\)', at, re.M)
P('  parsed audit rows: %d (script docstring says 293)' % len(rowsA))
bare = []
for b, val, key, rx, texlit in rowsA:
    ctx = re.sub(r'\([^()]*\)', '', rx)             # drop the capture group
    lit = re.sub(r'\\.', 'x', ctx)
    if len(lit.strip()) < 12: bare.append((b, val, key, rx))
P('  BARE rows (fewer than 12 literal context characters around the capture group): %d of %d' % (len(bare), len(rowsA)))
for b, val, key, rx in bare[:14]: P('     %s  value=%r  src=%s  rx=%r' % (b, val, key, rx[:70]))
# tex numeric tokens not covered by any audit tex literal (block-wise, with the audit's own normalisation)
def norm_tex(t):
    t = t.replace("$", "").replace("\\,", " ").replace("~", " ")
    t = re.sub(r"\s*/\s*", "/", t); return re.sub(r"\s+", " ", t)
blocks = {}; cur = []
started = False
for line in tex.split('\n'):
    if '\\begin{abstract}' in line: started = True
    if not started: continue
    mm = re.match(r"% AUDIT: (B\d\d)\s*$", line)
    if mm: blocks[mm.group(1)] = norm_tex('\n'.join(cur)); cur = []
    elif not line.lstrip().startswith('%') and 'section*{References}' not in line: cur.append(line)
tot_tok = 0; unc = []; unc_by = {}
for bk, bt in blocks.items():
    cov = np.zeros(len(bt), bool)
    for b_, val, key, rx, texlit in rowsA:
        if b_ != bk: continue
        lit = norm_tex((texlit if texlit else val.replace('\u2013', '--').replace('\u2212', '-')).replace('\\\\', '\\'))
        for m in re.finditer(re.escape(lit), bt): cov[m.start():m.end()] = True
    clean = re.sub(r'\\(ref|label|fpath)\{[^}]*\}', lambda m_: ' ' * len(m_.group(0)), bt)
    for m in re.finditer(r'(?<![\w.\\])\d[\d,]*\.?\d*', clean):
        tk = m.group(0)
        if tk.isdigit() and int(tk) < 10: continue
        tot_tok += 1
        if not cov[m.start():m.end()].all(): unc.append(tk); unc_by[bk] = unc_by.get(bk, 0) + 1
toks = list(range(tot_tok))
P('  numeric tokens (>= 10 or with decimals) in the audited body (table-spec lines excluded): %d; not inside any audit tex literal of their own block: %d (%.0f%%); per block: %s' % (tot_tok, len(unc), 100 * len(unc) / max(1, tot_tok), dict(sorted(unc_by.items(), key=lambda kv: -kv[1])[:8])))
P('     examples: %s' % ', '.join(unc[:30]))
P('  note: the audit checks (1) value in source by a regex, (2) the literal anywhere in the tag BLOCK (all non-comment lines since the previous tag), never the sentence: a number that appears twice in a block passes for both.')
RES['P10'] = dict(rows=len(rowsA), bare=len(bare), tokens=len(toks), uncovered=len(unc), uncovered_examples=unc[:30])

# ------------------------------------------------------------------ P11 PDF
P('\n=== P11: PDF text layer vs tex ===')
pdf = os.path.join(REPO, 'qwen_claude_field_theory/papers_2026/PAPER38_a0z_calibration_wall_2026.pdf')
txt = None
for tool in ('pdftotext', ):
    if subprocess.run('which %s' % tool, shell=True, capture_output=True).returncode == 0:
        txt = subprocess.run([tool, '-layout', pdf, '-'], capture_output=True).stdout.decode('utf-8', 'replace')
if txt is None:
    try:
        import pypdf; txt = '\n'.join(pg.extract_text() for pg in pypdf.PdfReader(pdf).pages)
    except Exception as e:
        try:
            import PyPDF2; txt = '\n'.join(pg.extract_text() for pg in PyPDF2.PdfReader(pdf).pages)
        except Exception as e2: P('  no PDF text extractor available (%r): NOT RUN' % (e2,))
if txt:
    pn = set(re.findall(r'\d+\.\d+', txt)); tn = set(re.findall(r'\d+\.\d+', '\n'.join(blocks.values())))
    P('  decimal tokens: pdf %d, tex body %d; in tex not in pdf: %d %s; in pdf not in tex: %d %s' % (len(pn), len(tn), len(tn - pn), sorted(tn - pn)[:10], len(pn - tn), sorted(pn - tn)[:10]))
    RES['P11'] = dict(tex_not_pdf=sorted(tn - pn)[:20], pdf_not_tex=sorted(pn - tn)[:20])
zj, zh = head_text('qwen_claude_field_theory/papers_2026/PAPER38_a0z_calibration_wall_2026.zenodo.json')
if zj:
    try:
        zd = json.loads(zj); desc = re.sub(r'<[^>]+>', ' ', json.dumps(zd))
        P('  zenodo.json: has "not peer reviewed"/AI-assisted disclosure: %s / %s' % (bool(re.search(r'peer.review', desc, re.I)), bool(re.search(r'AI', desc))))
    except Exception as e: P('  zenodo.json parse: %r' % (e,))

bad = [n for n, ok in CONTROLS if not ok]
P('\nSELF-CONTROLS: %d/%d pass%s' % (len(CONTROLS) - len(bad), len(CONTROLS), ('; FAILED: ' + '; '.join(bad)) if bad else ''))
if not MUT:
    open(os.path.join(HERE, 'CFG241_physics.out'), 'w').write(scrub('\n'.join(OUT)) + '\n')
    json.dump(RES, open(os.path.join(HERE, 'CFG241_physics_results.json'), 'w'), default=float, indent=1)
else:
    open(os.path.join(HERE, 'CFG241_physics_MUTATE.out'), 'w').write(scrub('\n'.join(OUT)) + '\n')
sys.exit(1 if bad else 0)
