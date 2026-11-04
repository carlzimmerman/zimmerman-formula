"""A17: fuzzy dark matter soliton + NFW outer halo, per ../FROZEN_A17.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.integrate import cumulative_trapezoid
C, HBAR, EV = 2.998e8, 1.0546e-34, 1.602e-19
RHODE = cos.Ode0 * RHOC; AN = C * np.sqrt(G * RHODE)
XS = np.concatenate([[0], np.logspace(-4, 4, 4000)]); FS = cumulative_trapezoid(4 * np.pi * XS**2 / (1 + .091 * XS**2)**8, XS, initial=0)
def msol(r, rho0, rc): return rho0 * rc**3 * np.interp(r / rc, XS, FS)  # kpc, Msun
for g in GS: g.sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100; g.rk = g.r / kpc
def halo(g, k, rule='match'):
    lm, la, beta, s, dn, dc = (list(k) + [0, 1 / 3, 0, 0, 0][len(k) - 1:])[:6] if len(k) < 6 else k
    m22 = 10**lm; M = m200_of(g.Ms, dn); c = float(cflat(M, dc, 0)); fb = min(g.Mb / M, .5)
    R = (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3) / kpc; rs = R / c; rhos = (1 - fb) * M / (4 * np.pi * rs**3 * mu(c))
    rc = 10**la * 1.6 / m22 * (M / 1e9)**(-beta) * g.sb**(-s); rho0 = .019e9 / m22**2 / rc**4
    mn = lambda r: (1 - fb) * M * mu(r / rs) / mu(c)
    if rule == 'match':
        rg = np.logspace(-3, np.log10(R), 300); x = rg / rs; d = rho0 / (1 + .091 * (rg / rc)**2)**8 - rhos / (x * (1 + x)**2)
        idx = np.where(d > 0)[0]; rt = rg[idx[-1]] if len(idx) else 0.
    else: rt = 3 * rc
    if rt <= 0: m = mn(g.rk)
    else: m = np.where(g.rk < rt, msol(g.rk, rho0, rc), msol(rt, rho0, rc) + mn(g.rk) - mn(rt))
    return g.gb + G * m * Msun / g.r**2, dict(M=M, rc=rc, rho0=rho0, rt=rt, m22=m22)
def tot(S, k, rule='match'): return [halo(g, k, rule)[0] for g in S]
def res(S, k, rule='match'): return np.concatenate([np.log10(gt) - np.log10(g.gl) for g, gt in zip(S, tot(S, k, rule))])
def rms(S, k, rule='match'): return np.sqrt((res(S, k, rule)**2).mean())
def full(k, n): return list(k) + [0, 1 / 3, 0, 0, 0][n - 1:]
# M1 scan + fit
for rule in ['match', '3rc']:
    sc = [(lm, rms(GS, [lm], rule)) for lm in np.linspace(-1.5, 2, 36)]
    print(f'\nM1 scan ({rule}) log m22: ' + ' '.join(f'{a:.1f}:{b:.4f}' for a, b in sc[::3]), flush=True)
    j = int(np.argmin([b for _, b in sc])); lo_, hi_ = sc[max(j - 1, 0)][0], sc[min(j + 1, 35)][0]
    r = minimize_scalar(lambda x: rms(GS, [x], rule), bounds=(lo_, hi_), method='bounded', options=dict(xatol=1e-3))
    print(f'M1 ({rule}) best log m22 {r.x:.3f} (m22 {10**r.x:.3g}), rms to law {r.fun:.4f}')
    if rule == 'match': lm1 = r.x
    grade(f'A17 M1 m22 only, transition {rule}', tot(GS, [r.x], rule), '(1 knob)')
def m1fit(S): return minimize_scalar(lambda x: rms(S, [x]), bounds=(-1.5, 2), method='bounded', options=dict(xatol=1e-3)).x
BLO = [-1.5, -.5, 0, -1, -.3, -.3]; BHI = [2, .5, .7, 1, .3, .3]
def tune(S, n, x0):
    lo, hi = np.array(BLO[:n]), np.array(BHI[:n]); fn = lambda k: res(S, full(k, n))
    best = None
    for st in [x0, [x0[0], 0, 1 / 3, 0, 0, 0][:n]]:
        r = least_squares(fn, np.clip(st, lo + 1e-4, hi - 1e-4), bounds=(lo, hi), max_nfev=60, diff_step=.01)
        if best is None or r.cost < best.cost: best = r
    at = [i for i, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
    return list(best.x), at
NAMES = ['log m22', 'log A', 'beta', 's', 'dn', 'dc']; KN = {1: [lm1]}; x = [lm1]
for n, tag in [(3, 'M2 m22 + core-halo norm, slope'), (4, 'M3 M2 + compactness response s'), (6, 'M4 M3 + SHMR norm, c offset')]:
    x, at = tune(GS, n, x + [0, 1 / 3, 0, 0, 0][len(x) - 1:n - 1]); KN[n] = x
    print(f'\n{tag} knobs', dict(zip(NAMES, np.round(x, 3).tolist())), 'at bound', [NAMES[i] for i in at], flush=True)
    grade(f'A17 {tag}', tot(GS, full(x, n)), f'({n} knobs)')
print('\nholdout: tune on GS[::2], grade GS[1::2]')
HO = {}
for n in [1, 3, 4, 6]:
    if n == 1: k = [m1fit(GS[::2])]
    else: k, _ = tune(GS[::2], n, KN[n])
    tr, ev = rms(GS[::2], full(k, n)), rms(GS[1::2], full(k, n)); HO[n] = ev
    print(f' {n} knobs: tuned {tr:.4f}, unseen {ev:.4f} dex [{"PASS" if ev <= .025 else "FAIL"} <= 0.025] knobs {np.round(k, 3).tolist()}', flush=True)
print('\nacceleration scale g_c = G M_s(r_c)/r_c^2 per galaxy, at fitted knobs')
def zeta(z): om = cos.Om(z); x = om - 1; return (18 * np.pi**2 + 82 * x - 39 * x**2) / om
for n in [1, 3, 4, 6]:
    k = full(KN[n], n); gc = []; frt = 0
    for g in GS:
        _, h = halo(g, k); gc.append(G * msol(h['rc'], h['rho0'], h['rc']) * Msun / (h['rc'] * kpc)**2); frt += h['rt'] > 0
    gc = np.array(gc); ke = np.median(gc) / AN; sp = np.std(np.log10(gc))
    print(f' {n} knobs: median g_c {np.median(gc) / A0:.3g} a0, kappa_eff {ke:.3g} (log off {np.log10(ke / .5):+.2f} dex) [{"PASS" if abs(np.log10(ke / .5)) <= .05 else "FAIL"}]; rms log g_c {sp:.3f} dex [{"PASS" if sp <= .1 else "FAIL"} <= 0.1]; soliton present in {frt}/171')
    if n == 1:
        Ms = np.array([m200_of(g.Ms) for g in GS]); print(f'   slope dlog g_c/dlog M200 {np.polyfit(np.log10(Ms), np.log10(gc), 1)[0]:.3f}')
for z, (a, b) in zip([1, 1.5, 2.33], [(.76, 1.03), (.71, 1.12), (.33, 1.21)]):
    rr = (1 + z)**-.5 * (zeta(z) / zeta(0))**(-1 / 6); q = rr**-3
    print(f' z {z}: g_c(z)/g_c(0) at fixed M200 and m {q:.3f} [{"PASS" if a <= q <= b else "FAIL"} band {a}-{b}]')
m = 10**KN[1][0] * 1e-22 * EV / C**2; aq = np.sqrt(HBAR / m) * (G * RHODE)**.75
print(f' dimensional a_q = (hbar/m)^(1/2) (G rho_DE)^(3/4) at M1 m22 {10**KN[1][0]:.3g}: {aq:.3e} m/s^2 = {aq / A0:.3g} a0, kappa_eff {aq / AN:.3g}; rho_DE enters by hand')
print(' hbar/m and G alone form no acceleration; c sqrt(G rho_DE) contains no m, so m22 cannot set kappa.')
print('Rival language; every knob disclosed. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
