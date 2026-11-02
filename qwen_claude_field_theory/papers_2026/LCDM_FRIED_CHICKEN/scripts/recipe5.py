"""Amendment A4 of ../FROZEN_RECIPE.md: convergence, real halo scatter, past the last point. Analytic stand-in. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
import copy
src = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read().split("\nreport('R11 12")[0]
exec(src.split('\n', 2)[2])
K11 = np.array([-.319, .705, -.884, -.600, -.639, -.760, .091, -.097, 1., .466, 1., -.335]); K14 = np.array([-.512, .363, -.142, -.600, -.988, -.440, .051, -.139, .800, .600, 1., -.416, -.330, .150])
def refit(S, lo, hi, x0):
    fn = lambda k: np.concatenate([np.log10(gal(g, k)) - np.log10(g.gl) for g in S]); lo, hi = np.array(lo), np.array(hi)
    r = least_squares(fn, np.clip(x0, lo + 1e-4, hi - 1e-4), bounds=(lo, hi), max_nfev=200, diff_step=.005); return r.x, r.nfev, r.status
def t1(tag, lo, hi, x0, old):
    ka, nf, st = refit(GS, lo, hi, x0); e1 = grade(f'T1 {tag} tuned on all, max_nfev 200', [gal(g, ka) for g in GS], f'({len(lo)} knobs)')
    print(f' nfev {nf}, status {st}; deposited {old:.4f}, moved {e1 - old:+.4f} dex [{"converged" if abs(e1 - old) < .001 else "MOVED"}]')
    print(' knobs', ' '.join(f'{n}={v:+.3f}{"*" if min(v - a, b - v) < 1e-3 * (b - a) else ""}' for n, v, a, b in zip(NM, ka, lo, hi)), '(* at bound)')
    ko, _, _ = refit(ODD, lo, hi, ka); ev = np.concatenate([np.log10(gal(g, ko)) - np.log10(g.gl) for g in EVEN]); od = np.concatenate([np.log10(gal(g, ko)) - np.log10(g.gl) for g in ODD])
    print(f' tuned on odd, started from the all-galaxy knobs (none recorded for odd, disclosed): {np.sqrt((od**2).mean()):.4f} on tuned, {np.sqrt((ev**2).mean()):.4f} on unseen', flush=True)
    return ka
def gals(g, k, dlc=0., dlm=0.):
    dn, dm, db, dg, le, a1, a2, a4, le0, a3, f0, f1 = k[:12]; dc, sc = (k[12], k[13]) if len(k) > 12 else (0, 0)
    M0 = m200k(g.Ms, dn, dm, db, dg); M = M0 * 10**dlm; c = float(cflat(M0, dc, sc)) * 10**dlc; fb = min(g.Mb / M, .5); fg = max((g.Mb - g.Ms) / g.Mb, .01); sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100
    e = 10**le * (g.Ms / M / .01)**a1 * sb**a2 * (fg / .5)**a4; n = np.tanh(min(e, 50)); eta = 10**le0 * (g.Ms / 1e9)**a3; f = np.clip(f0 + f1 * (np.log10(g.Mb) - 9.5), -1, 1)
    m0 = np.maximum(ein(g.r, M, c), 1e-30); ri = g.r.copy()
    for _ in range(12):
        mi = np.maximum(ein(ri, M, c), 1e-30); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m / g.r**2
assert all(np.allclose(gals(g, K11), gal(g, K11)) for g in GS[:5])
def t2(tag, k):
    for lab, sc, sm in (('c 0.11 dex', .11, 0.), ('c 0.11 + M200 0.15 dex', .11, .15)):
        L, O = [], []
        for s in range(40):
            rng = np.random.default_rng(1000 + s); gt = np.concatenate([gals(g, k, rng.normal(0, sc), rng.normal(0, sm) if sm else 0.) for g in GS])
            L.append(np.sqrt(((np.log10(gt) - np.log10(ALLL))**2).mean())); O.append(np.sqrt(((np.log10(gt) - np.log10(ALLO))**2).mean()))
        p = np.percentile(O, [50, 16, 84]); q = np.percentile(L, [50, 16, 84])
        print(f'T2 {tag}, {lab}: rms to law {q[0]:.4f} ({q[1]:.4f}-{q[2]:.4f}); rms to observed {p[0]:.4f} ({p[1]:.4f}-{p[2]:.4f}) [{"PASS" if p[0] <= .205 else "FAIL"} S, <= 0.205]', flush=True)
def t3(tag, k):
    X, Y, RR = [], [], []
    for g in GS:
        rk = np.array([30., 50., 100., 200., 300.]) * kpc; rk = rk[rk > g.r[-1]]
        if not len(rk): continue
        h = copy.copy(g); h.r = rk; h.mb = np.full(len(rk), g.mbtot); h.gb = G * h.mb / rk**2; h.gl = law(h.gb); X.append(h.gb); Y.append(np.log10(gals(h, k)) - np.log10(h.gl))
    X, Y = np.concatenate(X), np.concatenate(Y); b = np.floor(np.log10(X) * 2) / 2; first = None; print(f'T3 {tag}: {len(X)} outer points; median log(recipe/law) by log g_b')
    for x in sorted(np.unique(b), reverse=True):
        if (b == x).sum() < 20: continue
        m = np.median(Y[b == x]); print(f'  {x:+.1f}: {m:+.3f} (n {(b == x).sum()})')
        if first is None and abs(m) > .1: first = x
    print(f'  first bin with |median| > 0.1 dex: {first}', flush=True)
ka = t1('R11', LO, HI, K11, .0415); kb = t1('R11b', LO + [-.33, -.15], HI + [.33, .15], K14, .0275)
print(); t2('R11', ka); t2('R11b', kb); print(); t3('R11', ka); t3('R11b', kb)
print('\nAnalytic stand-in; no data graded in T3. Rival language; every knob disclosed. kappa = 1/2 FITTED; not theory closed.')
