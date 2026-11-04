"""A18: published hydro-calibrated halo responses (DC14, coreNFW, Lazar+2020 FIRE-2), per ../FROZEN_A18.md.
Stand-ins for hydro runs, not hydro runs. Rival language, adopts nothing, not a framework result.
kappa = 1/2 FITTED; not theory closed."""
import sys, os, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
C = 2.998e8; GYR = 3.156e16; TSF = 13.8 * GYR; RHODE = cos.Ode0 * RHOC; AN = C * np.sqrt(G * RHODE)
def halo(g, dn, dc):
    M = m200_of(g.Ms, dn); R = (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3); fb = min(g.Mb / M, .5)
    return M, R, fb, float(cflat(M, dc, 0.)), np.log10(g.Ms / M)
def cum_mass(rho, r0, r1, n=500, gin=0.):
    """cumulative mass (unnormalised) on a log grid for density function rho(r); inner piece as r^-gin."""
    rr = np.exp(np.linspace(np.log(r0), np.log(r1), n)); f = rho(rr) * rr**3; dl = np.log(rr[1] / rr[0])
    m = np.concatenate([[0.], np.cumsum(.5 * (f[1:] + f[:-1]) * dl)]) + f[0] / (3 - gin); return rr, m
def dc14_par(X, s=1.):
    if X < -4.1: a, b, gm, lr = 1., 3., 1., 0.
    else:
        Xc = min(X, -1.3); y = 10**(Xc + 2.33); z = 10**(Xc + 2.56)
        a = 2.94 - np.log10(y**-1.08 + y**2.29); b = 4.23 + 1.34 * Xc + .26 * Xc**2; gm = -.06 + np.log10(z**-.68 + z)
        lr = np.log10(1 + 3e-5 * np.exp(3.4 * (Xc + 4.5)))
    a, b, gm = max(1 + s * (a - 1), .3), max(3 + s * (b - 3), 2.05), max(1 + s * (gm - 1), 0.)
    return a, b, gm, s * lr
def g_dc14(g, k):
    dn, dc, s = k; M, R, fb, cdm, X = halo(g, dn, dc); a, b, gm, lr = dc14_par(X, s)
    c = cdm * 10**lr; rm2 = R / c; rs = rm2 / ((2 - gm) / (b - 2))**(1 / a)
    rho = lambda r: (r / rs)**-gm * (1 + (r / rs)**a)**(-(b - gm) / a)
    rr, m = cum_mass(rho, 1e-5 * rs, max(R, g.r[-1]) * 1.01, gin=gm); mR = np.interp(np.log(R), np.log(rr), m)
    md = (1 - fb) * M * Msun * np.interp(np.log(g.r), np.log(rr), m) / mR
    return g.gb + G * md / g.r**2
def g_cnfw(g, k):
    dn, dc, lq = k; M, R, fb, c, X = halo(g, dn, dc); rs = R / c
    mn = (1 - fb) * nfw_m(g.r, M, c)[0]; mrs = (1 - fb) * nfw_m(rs, M, c)[0]
    tdyn = 2 * np.pi * np.sqrt(rs**3 / (G * mrs)); n = np.tanh(.04 * 10**lq * TSF / tdyn); rc = 1.75 * 1.678 * g.Rd
    return g.gb + G * mn * np.tanh(g.r / rc)**n / g.r**2
def lazar_par(x):
    x = np.clip(x, 10**-3.54, 10**-.97)
    rc = 10**1.21 * (.71 + x / 7.2e-3)**-2.31 * (x / .011)**1.55 * kpc
    rsr = (1 + x / .044)**-31.79 + 1.51 * (x / .28)**.40
    crat = (1 + x / 4.28e-3)**-1.80 + .374 * (x / 4.28e-3)**.66
    return rc, rsr, crat
def g_lazar(g, k):
    dn, dc, lr = k; M, R, fb, cdm, X = halo(g, dn, dc); rc, rsr, crat = lazar_par(10**X); rc *= 10**lr
    rts = rsr * R / (cdm * crat); A = .16
    rho = lambda r: np.exp(-(2 / A) * (((r + rc) / rts)**A - 1))
    rr, m = cum_mass(rho, 1e-5 * R, max(R, g.r[-1]) * 1.01); mR = np.interp(np.log(R), np.log(rr), m)
    md = (1 - fb) * M * Msun * np.interp(np.log(g.r), np.log(rr), m) / mR
    return g.gb + G * md / g.r**2
def rms(fn, k, S): return np.sqrt((np.concatenate([np.log10(fn(g, k)) - np.log10(g.gl) for g in S])**2).mean())
def tune(fn, S, x0, lo, hi):
    res = lambda k: np.concatenate([np.log10(fn(g, k)) - np.log10(g.gl) for g in S]); lo, hi = np.array(lo), np.array(hi)
    r = least_squares(res, np.clip(x0, lo + 1e-4, hi - 1e-4), bounds=(lo, hi), max_nfev=30, diff_step=.02)
    at = [i for i, (v, a, b) in enumerate(zip(r.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]; return r.x, at
def report(tag, fn, k, nk, hold=None, at=()):
    cur = [fn(g, k) for g in GS]; e1 = grade(tag, cur, f'({nk} knobs; knobs {np.round(k, 3).tolist()})')
    a = fit_a(ALLB, np.concatenate(cur)); ke = a / AN
    print(f' kappa_eff (read-off, info only, not a native scale) {ke:.3f}; log10 vs 0.5 {np.log10(ke / .5):+.3f} dex [{"within" if abs(np.log10(ke / .5)) <= .05 else "outside"} 0.05]; z-band E5 N/A')
    ev = rms(fn, k, GS[1::2]) if hold is None else hold
    print(f' holdout unseen GS[1::2] rms to law {ev:.4f} [{"PASS" if ev <= .025 else "FAIL"} <= 0.025]; knobs at bound {list(at)}')
    gt = np.concatenate(cur); d = np.log10(gt) - np.log10(ALLL)
    idx = np.cumsum([0] + [len(c) for c in cur]); per = np.array([np.sqrt((d[idx[i]:idx[i + 1]]**2).mean()) for i in range(len(cur))])
    b = np.floor(np.log10(ALLB) * 2) / 2; e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    ok = e1 <= .02 and np.percentile(per, 95) <= .04 and e3 <= .02 and ev <= .025
    print(f' VERDICT {"EXACT" if ok else "NOT EXACT"}', flush=True)
# published-formula sanity prints (controls)
for X in (-4.11, -3.5, -2.5, -2.0, -1.5, -1.3): print(f'DC14 X={X}: alpha,beta,gamma,log c ratio', np.round(dc14_par(X), 3).tolist())
for x in (1e-3, 5e-3, 2e-2): r_, s_, c_ = lazar_par(x); print(f'Lazar x={x}: r_c {r_ / kpc:.2f} kpc, rs~/r-2 {s_:.3f}, cF2/cDM {c_:.3f}')
gnfw = GS[0]; print('control NFW limit: DC14 at s=0 vs lib NFW, max |dlog g| on', gnfw.n,
      f'{np.abs(np.log10(g_dc14(gnfw, [0, 0, 0.])) - np.log10(gnfw.gb + G * (1 - min(gnfw.Mb / m200_of(gnfw.Ms), .5)) * nfw_m(gnfw.r, m200_of(gnfw.Ms), float(cflat(m200_of(gnfw.Ms), 0, 0)))[0] / gnfw.r**2)).max():.2e}')
X = np.array([np.log10(g.Ms / m200_of(g.Ms)) for g in GS]); print(f'log M*/M200 over SPARC: p5 {np.percentile(X, 5):.2f}, p50 {np.median(X):.2f}, p95 {np.percentile(X, 95):.2f}; outside DC14 range {(X > -1.3).sum() + (X < -4.1).sum()}, outside Lazar range {(X > -.97).sum() + (X < -3.54).sum()}')
MODELS = [('DC14', g_dc14, [0, 0, 1.], [-.5, -.3, 0.], [.5, .3, 2.]),
          ('coreNFW', g_cnfw, [0, 0, 0.], [-.5, -.3, -1.], [.5, .3, 1.5]),
          ('Lazar20', g_lazar, [0, 0, 0.], [-.5, -.3, -1.], [.5, .3, 1.])]
t0 = time.time()
for name, fn, k0, lo, hi in MODELS:
    report(f'A18 {name} as published, zero free knobs', fn, k0, 0)
    ka, at = tune(fn, GS, k0, lo, hi); ko, _ = tune(fn, GS[::2], k0, lo, hi); ev = rms(fn, ko, GS[1::2])
    print(f'\n{name} holdout knobs (tuned on GS[::2]) {np.round(ko, 3).tolist()}; tuned-set rms {rms(fn, ko, GS[::2]):.4f}')
    report(f'A18 {name} + 3 global knobs (dn, dc, strength), all-data tuning', fn, ka, 3, hold=ev, at=at)
    print(f' [{time.time() - t0:.0f} s]', flush=True)
print('\nStand-ins for hydro runs, not hydro runs. Rival language; every knob disclosed. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
