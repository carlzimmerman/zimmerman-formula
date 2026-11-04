"""A25: deepest single-recipe knob search, every LCDM block on record stacked, per ../FROZEN_A25.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os, time, json, signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
from scipy.stats import qmc
from colossus.lss import mass_function as MF
T00 = time.time()
def tl(): return f'[{time.time() - T00:.0f} s]'
# A19 SIDM solver (core, svm, mbfun) and A18 DC14 pieces, reused verbatim
_s = open(os.path.join(HERE, 'recipe21.py'), encoding='utf-8').read(); exec(_s[_s.index('c_ = 2.998e8'):_s.index('MBF = ')])
_s = open(os.path.join(HERE, 'recipe20.py'), encoding='utf-8').read(); exec(_s[_s.index('def cum_mass'):_s.index('def g_dc14')])
GYR = 3.156e16; MBF = [mbfun(g) for g in GS]; NG = len(GS); ALLI = list(range(NG)); ODD, EVEN = ALLI[::2], ALLI[1::2]
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); ok = vb2 > 0
    g.bul = float((np.abs(a[ok, 5]) > 0).any()); g.sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100; g.fg = max((g.Mb - g.Ms) / g.Mb, .01)
    g.gr = float(g.fg >= .5); g.lr = np.log(g.r); g.lmb = np.log(np.maximum(g.mb, 1e-30)); g.lgl = np.log10(g.gl)
LMSALL = np.array([np.log10(g.Ms) for g in GS]); LM0 = np.array([np.log10(m200_of(g.Ms)) for g in GS])
print(f'bulge galaxies {int(sum(g.bul for g in GS))}, gas-rich (f_gas >= 0.5) {int(sum(g.gr for g in GS))} of {NG}', flush=True)
cc.setCurrent(cos)
AH = np.gradient(np.log10(MF.massFunction(10**LMS * cos.h, 0., mdef='200c', model='tinker08', q_out='dndlnM')), LMS)
print(f'Tinker08 slope d log(dn/dlnM)/d log M at log M 10, 11, 12, 13: {np.round(np.interp([10, 11, 12, 13], LMS, AH), 3).tolist()}', flush=True)
class Ctx: pass
def mkctx(C, z=0., tsf=None):
    cc.setCurrent(C); x = Ctx(); x.z = z; x.rhoc = C.rho_c(z) * C.h**2 * Msun / kpc**3
    x.CG = np.array([float(CM.concentration(10**m * C.h, '200c', z, model='diemer19')) for m in LM])
    x.tsf = (C.age(z) if tsf is None else tsf) * GYR; x.tsidm = min(10., C.age(z)) * GYR; x.rde = C.Ode0 * C.rho_c(0) * C.h**2 * Msun / kpc**3
    cc.setCurrent(cos); return x
BASE = mkctx(cos, 0., 13.8)
assert np.allclose(BASE.CG, CG) and abs(BASE.rhoc / RHOC - 1) < 1e-12
AN = c_ * np.sqrt(G * BASE.rde)
# ---------------- knobs: name, unit, off value, frozen lo, hi
SPEC = [('dn', 'dn', 0, -.54, .54), ('dm', 'dm', 0, -.9, .9), ('db', 'db', 0, -1.2, 1.2), ('dg', 'dg', 0, -.6, .6),
        ('le', 'le', -6, -2, 1.48), ('a1', 'a1', 0, -3, 3), ('a2', 'a2', 0, -3, 3), ('a4', 'a4', 0, -3, 3),
        ('le0', 'le0', 0, -1, 1), ('a3', 'a3', 0, -1, 1), ('f0', 'f0', 0, -1, 1), ('f1', 'f1', 0, -1, 1), ('dc', 'dc', 0, -.33, .33), ('sc', 'sc', 0, -.15, .15),
        ('N1', 'N1', 0, -.1, .1), ('N2', 'N2', 0, -.5, .5), ('N4', 'N4', 0, -1, 1), ('N5', 'N5', 0, -1, 1),
        ('kq', 'HC', 0, 0, 2), ('s14', 'HD', 0, 0, 1.5), ('lsm', 'SI', -1., -1, 1), ('wg', 'AC', .8, .6, 1.), ('Ag', 'AC', .85, .85, 1.6),
        ('Df0g', 'PG', 0, -1, 1), ('Dle0g', 'PG', 0, -1, 1), ('Df0b', 'PB', 0, -1, 1), ('Dle0b', 'PB', 0, -1, 1), ('sl', 'SL', 0, -.3, .3), ('ss', 'SS', 0, 0, .3)]
NK = len(SPEC); NAMES = [s[0] for s in SPEC]; UNIT = [s[1] for s in SPEC]; OFF = np.array([s[2] for s in SPEC], float)
LO = np.array([s[3] for s in SPEC], float); HI = np.array([s[4] for s in SPEC], float)
WLO, WHI = (LO + HI) / 2 - 1.5 * (HI - LO) / 2, (LO + HI) / 2 + 1.5 * (HI - LO) / 2
for n, (a_, b_) in {'dg': (-.9, .9), 'dc': (-.5, .5), 'sc': (-.3, .3), 'lsm': (-2, 2)}.items(): j = NAMES.index(n); WLO[j], WHI[j] = a_, b_
for n in ('kq', 's14', 'ss'): WLO[NAMES.index(n)] = 0.
WHI[NAMES.index('wg')] = min(WHI[NAMES.index('wg')], 1.2); WLO[NAMES.index('Ag')] = max(WLO[NAMES.index('Ag')], .5)
BASEU = NAMES[:14]; BLOCKS = ['N1', 'N2', 'N4', 'N5', 'HC', 'HD', 'SI', 'AC', 'PG', 'PB', 'SL', 'SS']; ALLU = BASEU + BLOCKS
IX = {n: j for j, n in enumerate(NAMES)}
K11B = [-.512, .363, -.142, -.6, -.988, -.44, .051, -.139, .8, .6, 1., -.416, -.33, .15]
def free_of(on): return [j for j in range(NK) if UNIT[j] in on]
def nknob(on): return len(free_of(on))
# ---------------- SIDM response table (fits only; grades use the direct solver)
TDM = np.arange(-1., 1.61, .2); TDC = np.arange(-1., 1.01, .25); TSM = np.arange(-2., 2.01, .5)
TAB = os.path.join(HERE, 'recipe27_sidm_table.npz')
def nfw2(r, M, c, rhoc):
    R = (3 * M * Msun / (4 * np.pi * 200 * rhoc))**(1 / 3); return M * Msun * mu(r * c / R) / mu(c)
def sidm_direct(i, M, c, fb, lsm, ctx):
    g = GS[i]
    try:
        md, s, r1s, mis, rs = core(MBF[i], M, c, fb, svm(10**lsm), T=ctx.tsidm, rhoc=ctx.rhoc, rd=g.r)
        rat = md / ((1 - fb) * nfw2(g.r, M, c, ctx.rhoc)); bad = mis > .03 * np.log(10)
    except Exception: rat, bad = np.ones_like(g.r), True
    if not np.all(np.isfinite(rat)) or np.any(rat <= 0): rat, bad = np.ones_like(g.r), True
    return rat, bad
if os.path.exists(TAB):
    z_ = np.load(TAB); STAB = [z_[f't{i}'] for i in range(NG)]; print(f'SIDM table loaded from cache {tl()}', flush=True)
else:
    STAB, nbad = [], 0
    for i, g in enumerate(GS):
        t = np.zeros((len(TDM), len(TDC), len(TSM), len(g.r)), np.float32)
        for a_, dm_ in enumerate(TDM):
            M = 10**(LM0[i] + dm_); c0 = float(np.interp(np.log10(M), LM, CG)); fb = min(g.Mb / M, .5)
            for b_, dlc in enumerate(TDC):
                for k_, ls in enumerate(TSM):
                    rat, bad = sidm_direct(i, M, c0 * 10**dlc, fb, ls, BASE); t[a_, b_, k_] = np.log(rat); nbad += bad
        STAB.append(t)
        if i % 20 == 0: print(f' SIDM table galaxy {i + 1} of {NG} {tl()}', flush=True)
    np.savez_compressed(TAB, **{f't{i}': t for i, t in enumerate(STAB)})
    print(f'SIDM table built: {NG} x {len(TDM) * len(TDC) * len(TSM)} nodes, unmatched or failed cores {nbad} {tl()}', flush=True)
CLIP = [0, 0]
def sidm_table(i, lM, dlc, lsm):
    u = np.clip((lM - LM0[i] - TDM[0]) / .2, 0, len(TDM) - 1 - 1e-9); v = np.clip((dlc - TDC[0]) / .25, 0, len(TDC) - 1 - 1e-9); w = np.clip((lsm - TSM[0]) / .5, 0, len(TSM) - 1 - 1e-9)
    CLIP[0] += 1; CLIP[1] += (lM - LM0[i] < TDM[0] or lM - LM0[i] > TDM[-1] or dlc < TDC[0] or dlc > TDC[-1])
    a_, b_, k_ = int(u), int(v), int(w); fa, fb_, fk = u - a_, v - b_, w - k_; t = STAB[i]; out = 0.
    for da, wa in ((0, 1 - fa), (1, fa)):
        for db_, wb in ((0, 1 - fb_), (1, fb_)):
            for dk, wk in ((0, 1 - fk), (1, fk)):
                if wa * wb * wk > 0: out = out + wa * wb * wk * t[a_ + da, b_ + db_, k_ + dk]
    return np.exp(out)
# ---------------- the recipe
def shmr(P, idx):
    dn, dm, db, dg = P[:4]; x = 10**LMS / 10**(11.59 + dm); s = 2 * .0351 * 10**dn * 10**LMS / (x**-(1.376 + db) + x**(.608 + dg)); i = np.argmax(s)
    ls, lm = np.log10(s[:i + 1]), LMS[:i + 1]; lMs = LMSALL[idx]; lM = np.interp(lMs, ls, lm)
    lM = lM + P[IX['sl']] * np.minimum(lMs - 9, 0)
    if P[IX['ss']] > 0:
        sl_ = np.interp(lM, lm, np.gradient(ls, lm)); dl = np.interp(lM, LMS, AH) * np.log(10) * P[IX['ss']]**2 / np.maximum(sl_, 1e-3)**2
        lM = lM + np.clip(dl, -.6, 0)
    return lM
def gal(i, P, on, ctx, lM, mode, info=None):
    g = GS[i]; p = dict(zip(NAMES, P)); M = 10**lM; R = (3 * M * Msun / (4 * np.pi * 200 * ctx.rhoc))**(1 / 3)
    c = float(np.interp(lM, LM, ctx.CG)) * 10**p['dc'] * (M / 1e12)**p['sc'] * g.sb**p['N2']; A = max(.16 + p['N1'] * (lM - 12), .05); fb = min(g.Mb / M, .5)
    gA = gammainc(3 / A, 2 / A * c**A)
    def Me(r): return np.maximum(M * Msun * gammainc(3 / A, 2 / A * (r * c / R)**A) / gA, 1e-30)
    e = 10**p['le'] * (g.Ms / M / .01)**p['a1'] * g.sb**p['a2'] * (g.fg / .5)**p['a4']
    if p['kq'] > 0:
        rs = R / c; tdyn = 2 * np.pi * np.sqrt(rs**3 / (G * (1 - fb) * M * Msun * mu(1.) / mu(c))); e += p['kq'] * .04 * ctx.tsf / tdyn
    n = np.tanh(min(e, 50)); eta = 10**(p['le0'] + p['Dle0g'] * g.gr + p['Dle0b'] * g.bul) * (g.Ms / 1e9)**p['a3'] * g.sb**p['N5']
    f = np.clip(p['f0'] + p['Df0g'] * g.gr + p['Df0b'] * g.bul + p['f1'] * (np.log10(g.Mb) - 9.5) + p['N4'] * np.log10(g.sb), -1, 1)
    r = g.r; m0 = Me(r); ri = r.copy()
    if 'AC' in on:
        Ag, w = p['Ag'], p['wg']; rbf = Ag * R * (r / R)**w
        mbf = np.where(rbf < r[0], g.mb[0] * (rbf / r[0])**2, np.where(rbf > r[-1], g.mb[-1], np.exp(np.interp(np.log(rbf), g.lr, g.lmb))))
        for _ in range(12):
            mib = Me(Ag * R * (ri / R)**w); ri = .5 * ri + .5 * r * (mbf + (1 - fb) * mib) / mib
        mi = Me(ri)
    else:
        for _ in range(12):
            mi = Me(ri); ri = .5 * ri + .5 * r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(r / (eta * 1.75 * g.Rd))**n
    if 'HD' in on and p['s14'] > 0:
        a_, b_, gm, lr = dc14_par(np.log10(g.Ms / M), p['s14']); cd = c * 10**lr; rs = R / cd / ((2 - gm) / (b_ - 2))**(1 / a_)
        rho = lambda x: (x / rs)**-gm * (1 + (x / rs)**a_)**(-(b_ - gm) / a_)
        rr, mm = cum_mass(rho, 1e-5 * rs, max(R, r[-1]) * 1.01, n=300, gin=gm); mR = np.interp(np.log(R), np.log(rr), mm)
        m = m * (np.interp(np.log(r), np.log(rr), mm) / mR) / (mu(r * c / R) / mu(c))
    if 'SI' in on:
        if mode == 'table': rat = sidm_table(i, lM, np.log10(c / float(np.interp(lM, LM, CG))), p['lsm'])
        else:
            rat, bad = sidm_direct(i, M, c, fb, p['lsm'], ctx)
            if info is not None: info['bad'] = info.get('bad', 0) + bad
        m = m * rat
    return g.gb + G * m / r**2
def curves(P, on, idx=ALLI, ctx=BASE, mode='table', info=None):
    lM = shmr(P, idx); return [gal(i, P, on, ctx, l, mode, info) for i, l in zip(idx, lM)]
def resid(P, on, idx, mode='table', wts=None):
    r = np.concatenate([np.log10(c) - GS[i].lgl for i, c in zip(idx, curves(P, on, idx, mode=mode))])
    return r if wts is None else r * wts
def rmsl(P, on, idx, mode='table'): return float(np.sqrt((resid(P, on, idx, mode)**2).mean()))
def stats(cur, idx=ALLI):
    d = np.concatenate([np.log10(c) - GS[i].lgl for i, c in zip(idx, cur)]); ob = np.concatenate([np.log10(c) - np.log10(GS[i].gobs) for i, c in zip(idx, cur)])
    per = np.array([np.sqrt(((np.log10(c) - GS[i].lgl)**2).mean()) for i, c in zip(idx, cur)]); gb = np.concatenate([GS[i].gb for i in idx]); b = np.floor(np.log10(gb) * 2) / 2
    e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    return dict(e1=float(np.sqrt((d**2).mean())), e2=float(np.percentile(per, 95)), e3=float(e3), obs=float(np.sqrt((ob**2).mean())), worst=[GS[idx[j]].n for j in np.argsort(per)[::-1][:5]])
def fit(on, P0, idx, nfev, lo=LO, hi=HI, wts=None, mode='table'):
    fr = free_of(on); P = np.array(P0, float).copy(); Pn = OFF.copy(); Pn[fr] = P[fr]; P = Pn
    if not fr: return P, rmsl(P, on, idx), 0
    lo_, hi_ = lo[fr], hi[fr]; eps = 1e-6 * (hi_ - lo_)
    def fn(x): Q = P.copy(); Q[fr] = x; return resid(Q, on, idx, mode, wts)
    r = least_squares(fn, np.clip(P[fr], lo_ + eps, hi_ - eps), bounds=(lo_, hi_), x_scale='jac', diff_step=.02, max_nfev=nfev)
    P[fr] = r.x; return P, rmsl(P, on, idx), int(r.nfev)
def lhs(on, nst, seed, lo=LO, hi=HI):
    fr = free_of(on); X = qmc.LatinHypercube(d=len(fr), seed=seed).random(nst); out = []
    for x in X:
        P = OFF.copy(); P[fr] = lo[fr] + x * (hi[fr] - lo[fr]); out.append(P)
    return out
def atbound(P, on, lo=LO, hi=HI): return [NAMES[j] for j in free_of(on) if min(P[j] - lo[j], hi[j] - P[j]) < 1e-3 * (hi[j] - lo[j])]
def warm():
    P = OFF.copy(); P[:14] = K11B; P[IX['lsm']] = -1.; P[IX['wg']], P[IX['Ag']] = .8, .85; P[IX['s14']] = .05; P[IX['kq']] = .05; P[IX['ss']] = .05; return P
# ---------------- checkpoint
CK = os.path.join(HERE, 'recipe27_ckpt.json')
ST = json.load(open(CK)) if os.path.exists(CK) else {}
def save(): json.dump(ST, open(CK + '.tmp', 'w')); os.replace(CK + '.tmp', CK)
signal.signal(signal.SIGTERM, lambda *a: (save(), print('SIGTERM: checkpoint saved', flush=True), sys.exit(0)))
def rec(on, P, e): return dict(on=list(on), P=[float(v) for v in P], rms=float(e), k=nknob(on))
t = time.time(); _ = resid(warm(), ALLU, ALLI); print(f'timing: one full-stack evaluation (table mode) {time.time() - t:.3f} s', flush=True)
t = time.time(); _ = curves(warm(), ALLU, mode='direct'); print(f'timing: one full-stack evaluation (direct SIDM) {time.time() - t:.3f} s', flush=True)
# control: recipe with only base knobs at K11B reproduces gal3 (recipe18) R11b
_s = open(os.path.join(HERE, 'recipe18.py'), encoding='utf-8').read(); exec(_s[_s.index('BL = '):_s.index('def tune(')])
_s = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(_s[_s.index('def m200k'):_s.index('def gal(')])
Pk = OFF.copy(); Pk[:14] = K11B
dd = np.concatenate([np.log10(a_) - np.log10(gal3(g, K11B, [])) for a_, g in zip(curves(Pk, BASEU), GS)])
print(f'control: R11b at K11B, this code vs recipe18 gal3: max |dlog g| {np.abs(dd).max():.2e} dex [{"PASS" if np.abs(dd).max() < 1e-6 else "FAIL"}]; rms to law {rmsl(Pk, BASEU, ALLI):.4f}', flush=True)
if os.environ.get('A25_TEST'): sys.exit(0)
# ---------------- S1 full stack
if 'S1' not in ST: ST['S1'] = []
starts = [warm()] + lhs(ALLU, 8, 27)
for s in range(len(ST['S1']), len(starts)):
    P, e, nf = fit(ALLU, starts[s], ALLI, 150); ST['S1'].append(rec(ALLU, P, e)); save()
    print(f'S1 start {s} ({"warm" if s == 0 else "LHS"}): rms to law {e:.4f} dex, nfev {nf} {tl()}', flush=True)
S1 = min(ST['S1'], key=lambda d: d['rms']); r_ = sorted(d['rms'] for d in ST['S1'])
print(f'S1 best {S1["rms"]:.4f} dex ({S1["k"]} knobs); all starts sorted {np.round(r_, 4).tolist()}', flush=True)
# ---------------- S3 forward one round from R11b
if 'S3' not in ST: ST['S3'] = {}
if 'R11b' not in ST['S3']:
    P0 = OFF.copy(); P0[:14] = K11B; P, e, _ = fit(BASEU, P0, ALLI, 60); ST['S3']['R11b'] = rec(BASEU, P, e); save()
print(f'S3 R11b re-fitted (14 knobs): {ST["S3"]["R11b"]["rms"]:.4f} dex {tl()}', flush=True)
for b in BLOCKS:
    if b in ST['S3']: continue
    on = BASEU + [b]; P0 = warm(); P0[:14] = ST['S3']['R11b']['P'][:14]; P, e, _ = fit(on, P0, ALLI, 60); ST['S3'][b] = rec(on, P, e); save()
    print(f'S3 R11b + {b} ({nknob(on)} knobs): {e:.4f} dex {tl()}', flush=True)
# ---------------- S2 backward elimination
if 'S2' not in ST: ST['S2'] = [rec(ALLU, S1['P'], S1['rms'])]; save()
while ST['S2'][-1]['on']:
    cur = ST['S2'][-1]; on = cur['on']; P = np.array(cur['P']); q = []
    for u in on:
        on2 = [v for v in on if v != u]; P2, e2, _ = fit(on2, P, ALLI, 4); q.append((e2, u, P2))
    q.sort(key=lambda t: t[0]); best = None
    for e2, u, P2 in q[:2]:
        on2 = [v for v in on if v != u]; P3, e3, _ = fit(on2, P2, ALLI, 60)
        if best is None or e3 < best[0]: best = (e3, u, P3)
    on2 = [v for v in on if v != best[1]]; ST['S2'].append(rec(on2, best[2], best[0]) | dict(removed=best[1])); save()
    print(f'S2 remove {best[1]}: {nknob(on2)} knobs, rms to law {best[0]:.4f} dex (quick screen best {q[0][1]} {q[0][0]:.4f}) {tl()}', flush=True)
# ---------------- Pareto set
allrec = ST['S1'] + list(ST['S3'].values()) + ST['S2']; PAR = {}
for d in allrec:
    if d['k'] not in PAR or d['rms'] < PAR[d['k']]['rms']: PAR[d['k']] = d
print('\nPareto (frozen bounds, table-mode rms used for selection): ' + ', '.join(f'{k}:{PAR[k]["rms"]:.4f}' for k in sorted(PAR)), flush=True)
# ---------------- S4 widened, S5 equal-galaxy weight
if 'S4' not in ST:
    best = None
    for s, P0 in enumerate([np.array(S1['P'])] + lhs(ALLU, 3, 28, WLO, WHI)):
        P, e, _ = fit(ALLU, P0, ALLI, 150, WLO, WHI); print(f'S4 widened start {s}: {e:.4f} dex {tl()}', flush=True)
        if best is None or e < best[0]: best = (e, P)
    ST['S4'] = rec(ALLU, best[1], best[0]); save()
if 'S5' not in ST:
    W = np.concatenate([np.full(len(GS[i].r), 1 / np.sqrt(len(GS[i].r))) for i in ALLI]); W = W / np.sqrt((W**2).mean())
    P, e, _ = fit(ALLU, S1['P'], ALLI, 150, wts=W); ST['S5'] = rec(ALLU, P, e); save(); print(f'S5 equal-galaxy weight fitted {tl()}', flush=True)
# ---------------- grading
CJ = [mkctx(cc.setCosmology(f'a25_{OL}_{H0}', dict(flat=True, H0=H0, Om0=1 - OL, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False))) for OL, H0 in [(.70, 67.4), (.685, 73.), (.65, 73.)]]
cc.setCurrent(cos); CZ = {z: mkctx(cos, z) for z in ZB}
def plaus(P, on):
    out = []
    for j in free_of(on):
        x = max(LO[j] - P[j], P[j] - HI[j], 0) / (HI[j] - LO[j])
        if x > 1e-9: out.append((NAMES[j], round(float(x), 3)))
    return out
def gradept(tag, d, lo=LO, hi=HI, wide=False):
    key = f'G_{tag}'
    if key in ST: return ST[key]
    on, P = d['on'], np.array(d['P']); info = {}; cur = curves(P, on, mode='direct', info=info); s = stats(cur)
    print(f'\n######## {tag}: {nknob(on)} knobs, units {on}', flush=True)
    grade(f'A25 {tag}', cur, f'({nknob(on)} knobs)')
    ctrl = None
    if 'SI' in on:
        CLIP[:] = [0, 0]; ctab = curves(P, on, mode='table'); ctrl = float(np.sqrt((np.concatenate([np.log10(a_) - np.log10(b_) for a_, b_ in zip(ctab, cur)])**2).mean()))
        print(f' SIDM control: table vs direct rms {ctrl:.4f} dex [{"PASS" if ctrl <= .003 else "FAIL"} <= 0.003]; table clipped {CLIP[1]} of {CLIP[0]} galaxies; direct unmatched cores {info.get("bad", 0)}', flush=True)
    ab = atbound(P, on, lo, hi); lM = shmr(P, ALLI); dM = np.median(lM - LM0)
    print(f' knobs at bound {len(ab)}: {ab}; median dlogM200 vs base SHMR {dM:+.2f}; worst galaxies {s["worst"]}', flush=True)
    print(' knobs ' + ' '.join(f'{NAMES[j]}={P[j]:+.3f}' for j in free_of(on)), flush=True)
    pl = plaus(P, on) if wide else []
    if wide: print(f' plausibility cost: sum {sum(x for _, x in pl):.3f}, max {max([x for _, x in pl], default=0):.3f} range widths outside the frozen range; {pl}', flush=True)
    # holdout, clean and leaky
    fr = free_of(on)
    if fr:
        Pc = OFF.copy(); Pc[fr] = (lo[fr] + hi[fr]) / 2; c1 = fit(on, Pc, ODD, 80, lo, hi); c2 = fit(on, lhs(on, 1, 99, lo, hi)[0], ODD, 60, lo, hi); Ph = min((c1, c2), key=lambda t: t[1])
        hcl = stats(curves(Ph[0], on, EVEN, mode='direct'), EVEN)['e1']; Pl = fit(on, P, ODD, 60, lo, hi); hlk = stats(curves(Pl[0], on, EVEN, mode='direct'), EVEN)['e1']
        print(f' holdout clean: tuned on GS[::2] {Ph[1]:.4f} (centre start {c1[1]:.4f}, LHS start {c2[1]:.4f}), unseen GS[1::2] {hcl:.4f} [{"PASS" if hcl <= .025 else "FAIL"} <= 0.025]; leaky (from all-data knobs, not gated): tuned {Pl[1]:.4f}, unseen {hlk:.4f}', flush=True)
    else: hcl = hlk = stats([cur[i] for i in EVEN], EVEN)['e1']; print(f' holdout: nothing tuned, GS[1::2] {hcl:.4f} [{"PASS" if hcl <= .025 else "FAIL"}]', flush=True)
    ex = s['e1'] <= .02 and s['e2'] <= .04 and s['e3'] <= .02 and hcl <= .025
    # tie gates
    a0 = fit_a(ALLB, np.concatenate(cur)); ke = a0 / AN; g1 = abs(np.log10(ke / .5)) <= .05
    aJ = [fit_a(ALLB, np.concatenate(curves(P, on, ctx=C, mode='direct'))) for C in CJ]; sl = [np.log(aJ[k] / aJ[0]) / np.log(CJ[k].rde / CJ[0].rde) for k in (1, 2)]; g2 = all(abs(x - .5) <= .05 for x in sl)
    zr = {z: fit_a(ALLB, np.concatenate(curves(P, on, ctx=CZ[z], mode='direct'))) / a0 for z in ZB}; g3 = all(ZB[z][0] <= zr[z] <= ZB[z][1] for z in ZB)
    sel = [i for i in ALLI if 11 <= lM[i] <= 12.5]; la = np.log10([fit_a(GS[i].gb, cur[i]) for i in sel]); g4 = la.std() <= .1
    print(f' G1 a {a0:.4e} kappa_eff {ke:.3f} [{"PASS" if g1 else "FAIL"}] (inherited from the target); G2 a at J cosmologies {[f"{x:.3e}" for x in aJ]}, slopes {sl[0]:+.3f} {sl[1]:+.3f} [{"PASS" if g2 else "FAIL"}]; '
          f'G3 a(z)/a(0) {", ".join(f"{z}: {x:.3f}" for z, x in zr.items())} [{"PASS" if g3 else "FAIL"}]; G4 {len(sel)} hosts log M200 11-12.5, rms log a_i {la.std():.3f} dex, median {np.median(la) - np.log10(A0):+.3f} vs a0 [{"PASS" if g4 else "FAIL"}]', flush=True)
    tie = g1 and g2 and g3 and g4
    print(f' VERDICT {tag}: {"EXACT" if ex else "NOT EXACT"}; tie {"TIES (check coincidence)" if tie else "NO TIE"} {tl()}', flush=True)
    out = dict(k=nknob(on), on=on, **{x: s[x] for x in ('e1', 'e2', 'e3', 'obs')}, hold=hcl, leaky=hlk, exact=ex, ke=ke, sl=sl, zr=[zr[z] for z in ZB], g4=float(la.std()),
               g=[bool(g1), bool(g2), bool(g3), bool(g4)], atb=len(ab), dM=float(dM), ctrl=ctrl, pl=pl)
    ST[key] = out; save(); return out
GR = {}
GR['S1'] = gradept('S1 full stack frozen', S1)
GR['S5'] = gradept('S5 full stack equal-galaxy weight', ST['S5'])
GR['S4'] = gradept('S4 full stack widened', ST['S4'], WLO, WHI, wide=True)
for k in sorted(PAR, reverse=True): GR[k] = gradept(f'Pareto {k} knobs', PAR[k])
print('\n==== A25 PARETO TABLE (graded with direct SIDM) ====')
print(' knobs | E1 rms law | E2 p95 | E3 worst | holdout clean | leaky | rms obs | at bound | dlogM200 | kappa_eff | G2 slopes | G3 z1, 1.5, 2.33 | G4 | EXACT | units')
for k in sorted(PAR, reverse=True):
    o = GR[k]; print(f' {k:2d} | {o["e1"]:.4f} | {o["e2"]:.4f} | {o["e3"]:.4f} | {o["hold"]:.4f} | {o["leaky"]:.4f} | {o["obs"]:.4f} | {o["atb"]} | {o["dM"]:+.2f} | {o["ke"]:.3f} | {o["sl"][0]:+.3f} {o["sl"][1]:+.3f} | '
                   f'{" ".join(f"{x:.3f}" for x in o["zr"])} | {o["g4"]:.3f} | {"Y" if o["exact"] else "N"} | {" ".join(u for u in o["on"] if u in BLOCKS)}')
for t_ in ('S1', 'S4', 'S5'): o = GR[t_]; print(f' {t_}: E1 {o["e1"]:.4f} E2 {o["e2"]:.4f} E3 {o["e3"]:.4f} holdout {o["hold"]:.4f} EXACT {"Y" if o["exact"] else "N"}; G {o["g"]}')
ex = [k for k in sorted(PAR) if GR[k]['exact']]
print(f'\nA25 VERDICT: {"minimal EXACT knob count " + str(ex[0]) if ex else "NO global recipe in the stack is EXACT at any knob count"}; tie gates G1-G4 all pass at {[k for k in PAR if all(GR[k]["g"])]} {tl()}')
print('Rival language; every knob disclosed. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
