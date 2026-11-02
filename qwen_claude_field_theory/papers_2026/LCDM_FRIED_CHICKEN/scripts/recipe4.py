"""Amendment A3 of ../FROZEN_RECIPE.md: 12 feedback knobs, analytic stand-in, not hydro. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
from scipy.special import gammainc
A = .16
def ein(r, M, c):
    R = (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3); return M * Msun * gammainc(3 / A, 2 / A * (r * c / R)**A) / gammainc(3 / A, 2 / A * c**A)
def m200k(Ms, dn, dm, db, dg):
    x = 10**LMS / 10**(11.59 + dm); s = 2 * .0351 * 10**dn * 10**LMS / (x**-(1.376 + db) + x**(.608 + dg)); i = np.argmax(s); return 10**np.interp(np.log10(Ms), np.log10(s[:i + 1]), LMS[:i + 1])
def gal(g, k):
    dn, dm, db, dg, le, a1, a2, a4, le0, a3, f0, f1 = k[:12]; dc, sc = (k[12], k[13]) if len(k) > 12 else (0, 0)
    M = m200k(g.Ms, dn, dm, db, dg); c = float(cflat(M, dc, sc)); fb = min(g.Mb / M, .5); fg = max((g.Mb - g.Ms) / g.Mb, .01); sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100
    e = 10**le * (g.Ms / M / .01)**a1 * sb**a2 * (fg / .5)**a4; n = np.tanh(min(e, 50)); eta = 10**le0 * (g.Ms / 1e9)**a3; f = np.clip(f0 + f1 * (np.log10(g.Mb) - 9.5), -1, 1)
    m0 = np.maximum(ein(g.r, M, c), 1e-30); ri = g.r.copy()
    for _ in range(12):
        mi = np.maximum(ein(ri, M, c), 1e-30); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m / g.r**2
LO = [-.54, -.9, -1.2, -.6, -2, -3, -3, -3, -1, -1, -1, -1]; HI = [.54, .9, 1.2, .6, 1.48, 3, 3, 3, 1, 1, 1, 1]; NM = 'SHMRnorm logM1 beta gamma log_eps a1 a2 a4 log_eta0 a3 f0 f1 cnorm cslope'.split()
def run(S, lo, hi, x0=None):
    fn = lambda k: np.concatenate([np.log10(gal(g, k)) - np.log10(g.gl) for g in S]); best = None
    lo, hi = np.array(lo), np.array(hi)
    for s in range(4):
        x = (x0 if x0 is not None else .5 * (lo + hi)) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        r = least_squares(fn, np.clip(x, lo + 1e-4, hi - 1e-4), bounds=(lo, hi), max_nfev=25, diff_step=.02)
        if best is None or r.cost < best.cost: best = r
    return best.x, fn
ODD, EVEN = GS[::2], GS[1::2]
def report(tag, lo, hi):
    ko, fo = run(ODD, lo, hi); ev = np.concatenate([np.log10(gal(g, ko)) - np.log10(g.gl) for g in EVEN])
    print(f'\n== {tag} tuned on odd\n rms on tuned {np.sqrt((fo(ko)**2).mean()):.4f} dex; on unseen {np.sqrt((ev**2).mean()):.4f} dex')
    ka, _ = run(GS, lo, hi, ko); grade(f'{tag} tuned on all', [gal(g, ka) for g in GS], f'({len(lo)} knobs)')
    print(' knobs', ' '.join(f'{n}={v:+.3f}{"*" if min(v - a, b - v) < 1e-3 * (b - a) else ""}' for n, v, a, b in zip(NM, ka, lo, hi)), '(* at bound)')
    dM = [np.log10(m200k(g.Ms, *ka[:4]) / m200_of(g.Ms)) for g in GS]; print(f' dlogM200 against base SHMR: p16, p50, p84 {np.round(np.percentile(dM, [16, 50, 84]), 2).tolist()}')
report('R11 12 feedback knobs', LO, HI); report('R11b 14 knobs, c norm and slope', LO + [-.33, -.15], HI + [.33, .15])
print('\nRival language; every knob disclosed. kappa = 1/2 FITTED; not theory closed.')
