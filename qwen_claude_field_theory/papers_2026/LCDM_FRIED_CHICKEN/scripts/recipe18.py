"""A16: greedy search over LCDM knob blocks on R11b, per ../FROZEN_RECIPE.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
src = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(src[src.index('def m200k'):src.index('def gal(')])
K11B = [-.512, .363, -.142, -.6, -.988, -.44, .051, -.139, .8, .6, 1., -.416, -.33, .15]
LO = [-.54, -.9, -1.2, -.6, -2, -3, -3, -3, -1, -1, -1, -1, -.33, -.15]; HI = [.54, .9, 1.2, .6, 1.48, 3, 3, 3, 1, 1, 1, 1, .33, .15]
BL = {'N1': (-.1, .1), 'N2': (-.5, .5), 'N4': (-1, 1), 'N5': (-1, 1)}
def ein2(r, M, c, A):
    R = (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3); return M * Msun * gammainc(3 / A, 2 / A * (r * c / R)**A) / gammainc(3 / A, 2 / A * c**A)
def gal3(g, k, on):
    dn, dm, db, dg, le, a1, a2, a4, le0, a3, f0, f1, dc, sc = k[:14]; x = dict(zip(on, k[14:])); x = {b: x.get(b, 0.) for b in BL}
    M = m200k(g.Ms, dn, dm, db, dg); sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100; A = max(.16 + x['N1'] * np.log10(M / 1e12), .05)
    c = float(cflat(M, dc, sc)) * sb**x['N2']; fb = min(g.Mb / M, .5); fg = max((g.Mb - g.Ms) / g.Mb, .01)
    e = 10**le * (g.Ms / M / .01)**a1 * sb**a2 * (fg / .5)**a4; n = np.tanh(min(e, 50)); eta = 10**le0 * (g.Ms / 1e9)**a3 * sb**x['N5']
    f = np.clip(f0 + f1 * (np.log10(g.Mb) - 9.5) + x['N4'] * np.log10(sb), -1, 1)
    m0 = np.maximum(ein2(g.r, M, c, A), 1e-30); ri = g.r.copy()
    for _ in range(12):
        mi = np.maximum(ein2(ri, M, c, A), 1e-30); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m / g.r**2
def tune(S, on, x0, lo, hi):
    fn = lambda k: np.concatenate([np.log10(gal3(g, k, on)) - np.log10(g.gl) for g in S]); lo, hi = np.array(lo), np.array(hi)
    r = least_squares(fn, np.clip(x0, lo + 1e-4, hi - 1e-4), bounds=(lo, hi), max_nfev=20, diff_step=.02); return r.x, np.sqrt((fn(r.x)**2).mean())
def bounds(on, lo=LO, hi=HI): return lo + [BL[b][0] for b in on], hi + [BL[b][1] for b in on]
on, x, best = [], list(K11B), None
_, e0 = tune(GS, [], K11B, LO, HI); print(f'start R11b re-tuned: rms to law {e0:.4f} dex (14 knobs)', flush=True); best = e0
while len(on) < len(BL):
    trial = {}
    for b in BL:
        if b in on: continue
        lo, hi = bounds(on + [b]); k, e = tune(GS, on + [b], x + [0.], lo, hi); trial[b] = (e, list(k)); print(f'  + {b} to {on}: {e:.4f} dex', flush=True)
    b = min(trial, key=lambda t: trial[t][0])
    if trial[b][0] > best - .0005: print(f'stop: best addition {b} gains under 0.0005 dex'); break
    on.append(b); best, x = trial[b]; print(f'keep {b}: {best:.4f} dex, {len(x)} knobs', flush=True)
lo, hi = bounds(on); grade(f'A16 best set R11b + {on}', [gal3(g, x, on) for g in GS], f'({len(x)} knobs)')
at = [i for i, (v, a, b) in enumerate(zip(x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]; print(f' at bound {len(at)} of {len(x)}: {at}')
W_LO, W_HI = list(LO), list(HI); W_LO[3], W_HI[3], W_LO[12], W_HI[12], W_LO[13], W_HI[13] = -.9, .9, -.5, .5, -.3, .3
wlo, whi = bounds(on, W_LO, W_HI); kw, ew = tune(GS, on, x, wlo, whi)
e1w = grade(f'A16 best set with W widened bounds', [gal3(g, kw, on) for g in GS], f'({len(kw)} knobs, plausibility cost)')
kb, eb = (kw, ew) if ew < best else (x, best); lb, hb = (wlo, whi) if ew < best else (lo, hi)
ko, eo = tune(GS[::2], on, kb, lb, hb); ev = np.sqrt((np.concatenate([np.log10(gal3(g, ko, on)) - np.log10(g.gl) for g in GS[1::2]])**2).mean())
print(f'holdout: tuned on odd {eo:.4f}, unseen even {ev:.4f} dex [{"PASS" if ev <= .025 else "FAIL"} <= 0.025]')
dM = [np.log10(m200k(g.Ms, *kb[:4]) / m200_of(g.Ms)) for g in GS]; print(f'dlogM200 p16, p50, p84 {np.round(np.percentile(dM, [16, 50, 84]), 2).tolist()}')
print('Rival language; every knob disclosed. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
