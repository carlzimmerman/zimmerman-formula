"""A44: halo shape (homoeoid in-plane force), tidal truncation, substructure smooth fraction, environment-dependent c,
and the A25 compact Pareto point plus the best shape block, per ../FROZEN_A44.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, signal, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc, gamma as GAM
from scipy.stats import qmc
from colossus.lss import mass_function as MF
T00 = time.time()
def tl(): return f'[{time.time() - T00:.0f} s]'
s4 = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(s4[s4.index('def m200k'):s4.index('def gal(')])
s18 = open(os.path.join(HERE, 'recipe18.py'), encoding='utf-8').read(); exec(s18[s18.index('K11B ='):s18.index('def tune(')])
c_ = 2.998e8; MPC = kpc * 1e3; BASE = cos  # recipe31's slice needs BASE = cos for S30; redefined below as a context
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('OR_H2 ='):s31.index('# ---------- scales')])
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZS = [0.] + list(ZB)
RDE0 = cos.Ode0 * RHOC; AN = c_ * np.sqrt(G * RDE0)
CK = os.path.join(HERE, 'recipe45.json'); OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK + '.tmp', 'w'), indent=1, default=float); os.replace(CK + '.tmp', CK)
signal.signal(signal.SIGTERM, lambda *a: (print('SIGTERM: checkpoint is saved after every row', flush=True), sys.exit(0)))
NG = len(GS); ALLI = list(range(NG)); TUNE, UNSEEN = ALLI[::2], ALLI[1::2]
SB = np.array([g.Mb / (g.Rd / kpc)**2 / 1e6 / 100 for g in GS]); M2P = np.array([m200_of(g.Ms) for g in GS])
for g in GS: g.lgl = np.log10(g.gl)
print(f'A44 recipe45; c sqrt(G rho_DE0) {AN:.4e}, A0 {A0:.4e} ({A0 / AN:.4f} of it)', flush=True)
# ======================= profiles and the four blocks =======================
GX, GW = np.polynomial.legendre.leggauss(48); GU = (GX + 1) / 2; GWU = GW / 2
def dM_nfw(M, c, R):
    rs = R / c; k = M * Msun / mu(c); return lambda r: k * (r / rs**2) / (1 + r / rs)**2
def dM_ein(M, c, R, A):
    s = 3 / A; k = M * Msun / gammainc(s, 2 / A * c**A) / GAM(s)
    def f(r):
        y = (r * c / R)**A; x = 2 / A * y; return k * x**(s - 1) * np.exp(-x) * 2 * y / np.maximum(r, 1e-300)
    return f
def M_nfw(r, M, c, R): return M * Msun * mu(r * c / R) / mu(c)
def M_ein(r, M, c, R, A): return M * Msun * gammainc(3 / A, 2 / A * (r * c / R)**A) / gammainc(3 / A, 2 / A * c**A)
def shape_ratio(r, dMdr, q, norm='geo'):
    """v_c^2 flattened / v_c^2 spherical in the midplane (BT08 eq. 2.132), same nodes for both (m = R u^2)."""
    e2 = 1 - q * q; k = q**(1 / 3) if norm == 'geo' else 1.; m = r[:, None] * GU[None, :]**2; jac = 2 * r[:, None] * GU[None, :] * GWU[None, :]
    num = (k * dMdr(k * m) / np.sqrt(r[:, None]**2 - e2 * m**2) * jac).sum(1); den = (dMdr(m) / r[:, None] * jac).sum(1)
    return num / den
def trunc_ratio(r, dMdr, rt):
    m = r[:, None] * GU[None, :]**2; jac = 2 * r[:, None] * GU[None, :] * GWU[None, :]; d = dMdr(m) * jac
    return (d * rt**2 / (rt**2 + m**2)).sum(1) / d.sum(1)
GAO_A, GAO_B = .244, 2.75
def S_sub(x, c): x = np.minimum(x, 1.); return (1 + GAO_A * c) * x**GAO_B / (1 + GAO_A * c * x**2)
def qof(md, i): return float(np.clip(md['q0'] * SB[i]**md.get('sq', 0.), .3, 1.5))
def ratio(i, r, M, c, R, A, md):
    if not any(k in md for k in ('q0', 'lkt', 'fsub')): return 1.
    dMdr = dM_nfw(M, c, R) if A is None else dM_ein(M, c, R, A); rat = np.ones_like(r)
    if 'q0' in md: rat = rat * shape_ratio(r, dMdr, qof(md, i), md.get('norm', 'geo'))
    if 'lkt' in md: rat = rat * trunc_ratio(r, dMdr, 10**md['lkt'] * R)
    if 'fsub' in md:
        Mr = M_nfw(r, M, c, R) if A is None else M_ein(r, M, c, R, A); rat = rat * ((1 - md['fsub']) * Mr + md['fsub'] * M * Msun * S_sub(r / R, c)) / Mr
    return rat
# ======================= contexts =======================
def mkc(C, z):
    cc.setCurrent(C); h = C.h
    e = dict(rhoc=float(C.rho_c(z) * h**2 * Msun / kpc**3), CG=np.array([float(CM.concentration(10**m * h, '200c', z, model='diemer19')) for m in LM]),
             rde=float(C.rho_de(z) * h**2 * Msun / kpc**3), z=z)
    cc.setCurrent(cos); return e
BASE = dict(rhoc=RHOC, CG=CG, rde=RDE0, z=0.)
# ======================= the two recipes =======================
def plain(i, K, md, ctx):
    g = GS[i]; M = M2P[i]; c = float(np.interp(np.log10(M), LM, ctx['CG'])) * 10**md.get('dlc', 0.); R = (3 * M * Msun / (4 * np.pi * 200 * ctx['rhoc']))**(1 / 3)
    fb = min(g.Mb / M, .5); return g.gb + G * (1 - fb) * M_nfw(g.r, M, c, R) * ratio(i, g.r, M, c, R, None, md) / g.r**2
def r11(i, K, md, ctx):
    g = GS[i]; dn, dm, db, dg, le, a1, a2, a4, le0, a3, f0, f1, dc, sc = K[:14]; M = m200k(g.Ms, dn, dm, db, dg); sb = SB[i]
    c = float(np.interp(np.log10(M), LM, ctx['CG'])) * 10**dc * (M / 1e12)**sc * 10**md.get('dlc', 0.); A = .16
    R = (3 * M * Msun / (4 * np.pi * 200 * ctx['rhoc']))**(1 / 3); fb = min(g.Mb / M, .5); fg = max((g.Mb - g.Ms) / g.Mb, .01)
    e = 10**le * (g.Ms / M / .01)**a1 * sb**a2 * (fg / .5)**a4; n = np.tanh(min(e, 50)); eta = 10**le0 * (g.Ms / 1e9)**a3
    f = np.clip(f0 + f1 * (np.log10(g.Mb) - 9.5), -1, 1); ein = lambda r: np.maximum(M_ein(r, M, c, R, A), 1e-30)
    m0 = ein(g.r); ri = g.r.copy()
    for _ in range(12):
        mi = ein(ri); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m * ratio(i, g.r, M, c, R, A, md) / g.r**2
FN = dict(plain=plain, r11=r11)
def curves(kind, K, md, idx=ALLI, ctx=BASE): return [FN[kind](i, K, md, ctx) for i in idx]
def stats(cur, idx=ALLI):
    d_ = [np.log10(c) - GS[i].lgl for i, c in zip(idx, cur)]; d = np.concatenate(d_); ob = np.concatenate([np.log10(c) - np.log10(GS[i].gobs) for i, c in zip(idx, cur)])
    per = np.array([np.sqrt((x**2).mean()) for x in d_]); gb = np.concatenate([GS[i].gb for i in idx]); b = np.floor(np.log10(gb) * 2) / 2
    e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    return dict(e1=float(np.sqrt((d**2).mean())), e2=float(np.percentile(per, 95)), e3=float(e3), obs=float(np.sqrt((ob**2).mean())))
# ======================= controls =======================
print('\n==== CONTROLS', flush=True)
e0 = mkc(cos, 0.); print(f' C0 context c-grid vs lib CG max rel {np.abs(e0["CG"] / CG - 1).max():.1e}', flush=True)
mx = max(np.abs(np.log10(r11(i, K11B, {}, BASE)) - np.log10(gal3(GS[i], K11B, []))).max() for i in ALLI)
print(f' C0 r11 at K11B vs recipe18 gal3: max |dlog g| {mx:.2e} dex [{"PASS" if mx < 1e-6 else "FAIL"}]', flush=True)
rr = np.array([.3, 1., 3., 10., 30.]) * kpc; M_, c_h = 1e12, 10.; R_ = (3 * M_ * Msun / (800 * np.pi * RHOC))**(1 / 3)
c1 = max(np.abs(shape_ratio(rr, dM_nfw(M_, c_h, R_), 1.) - 1).max(), np.abs(shape_ratio(rr, dM_ein(M_, c_h, R_, .16), 1.) - 1).max())
print(f' C1 q = 1 gives F = 1: max |F - 1| {c1:.1e} [{"PASS" if c1 < 1e-6 else "FAIL"}]', flush=True)
q_ = .8; e_ = np.sqrt(1 - q_**2); one = lambda m: np.ones_like(m)
c2g = abs(shape_ratio(rr, one, q_, 'geo')[0] - q_**(1 / 3) * np.arcsin(e_) / e_); c2m = abs(shape_ratio(rr, one, q_, 'major')[0] - np.arcsin(e_) / e_)
print(f' C2 isothermal q 0.8: geo F {shape_ratio(rr, one, q_, "geo")[0]:.5f} vs analytic {q_**(1 / 3) * np.arcsin(e_) / e_:.5f} (|d| {c2g:.1e}); major F {shape_ratio(rr, one, q_, "major")[0]:.5f} vs {np.arcsin(e_) / e_:.5f} (|d| {c2m:.1e}) [{"PASS" if max(c2g, c2m) < 1e-4 else "FAIL"}]', flush=True)
TH = np.linspace(0, np.pi / 2, 4001)
def frac_in(x, q):  # fraction of a thin homoeoid (in-plane semi-axis m) inside a sphere of radius x m
    s = 1 / np.sqrt(np.sin(TH)**2 + np.cos(TH)**2 / q**2); w = s**3 * np.sin(TH); return np.trapz(w * (s[None, :] <= np.atleast_1d(x)[:, None]), TH, axis=1) / np.trapz(w, TH)
for q_ in (.8, .5):
    out = []
    for rq in (R_ / c_h / 10, R_ / c_h, R_):
        k = q_**(1 / 3); mm = np.linspace(rq, rq / q_, 801); dMm = k * dM_nfw(M_, c_h, R_)(k * mm)
        Ms_ = M_nfw(k * rq, M_, c_h, R_) + np.trapz(dMm * frac_in(rq / mm, q_), mm); out.append(Ms_ / M_nfw(rq, M_, c_h, R_) - 1)
    print(f' C3 spherically averaged mass of the geo-normalised flattened NFW (c 10), q {q_}: M_sph/M_NFW - 1 at r_s/10, r_s, R200 = {", ".join(f"{x:+.4f}" for x in out)}', flush=True)
mq = np.linspace(1e-3, 1, 2001) * rr[:, None]; c4a = np.abs(trunc_ratio(rr, dM_nfw(M_, c_h, R_), 1e6 * R_) - 1).max()
gq = (dM_ein(M_, c_h, R_, .16)(rr[:, None] * GU[None, :]**2) * 2 * rr[:, None] * GU[None, :] * GWU[None, :]).sum(1); c4b = np.abs(gq / M_ein(rr, M_, c_h, R_, .16) - 1).max()
gn = (dM_nfw(M_, c_h, R_)(rr[:, None] * GU[None, :]**2) * 2 * rr[:, None] * GU[None, :] * GWU[None, :]).sum(1); c4c = np.abs(gn / M_nfw(rr, M_, c_h, R_) - 1).max()
print(f' C4 truncation at k_t 1e6: max |ratio - 1| {c4a:.1e}; quadrature of dM/dr vs analytic M: Einasto {c4b:.1e}, NFW {c4c:.1e} [{"PASS" if max(c4a, c4b, c4c) < 1e-4 else "FAIL"}]', flush=True)
print(f' S_sub(1) = {S_sub(np.array(1.), 10.):.4f} (must be 1); S_sub at x 0.1, 0.3: {S_sub(np.array(.1), 10.):.4f}, {S_sub(np.array(.3), 10.):.4f}', flush=True)
t = time.time(); _ = curves('r11', K11B, {'q0': .85}); t1 = time.time() - t; t = time.time(); _ = curves('r11', K11B, {'q0': .85, 'lkt': 0., 'fsub': .1}); t2 = time.time() - t
print(f' timing: r11 + shape {t1:.3f} s, r11 + shape + truncation + substructure {t2:.3f} s {tl()}', flush=True)
# ======================= rows =======================
BLK = {'qg': [('q0', .3, 1.5, 1.)], 'qs': [('q0', .3, 1.5, 1.), ('sq', -.5, .5, 0.)], 'kt': [('lkt', -1.5, 1., 0.)], 'fs': [('fsub', 0., .5, .05)], 'env': [('dlc', -.1, .1, 0.)]}
LIT = {'q0': (.8, .95), 'lkt': (0., np.log10(2.)), 'fsub': (0., .2), 'dlc': (-.1, .1)}
def unpack(kind, refit, blk, x, md0):
    md = dict(md0); j = 0; K = list(K11B)
    if refit: K = list(x[:14]); j = 14
    for (n, a_, b_, s_) in BLK.get(blk, []): md[n] = float(x[j]); j += 1
    return K, md
def setup(kind, refit, blk):
    lo, hi, x0 = [], [], []
    if refit: lo += list(LO[:14]); hi += list(HI[:14]); x0 += list(K11B)
    for (n, a_, b_, s_) in BLK.get(blk, []): lo.append(a_); hi.append(b_); x0.append(s_)
    return np.array(lo, float), np.array(hi, float), np.array(x0, float)
def tune(kind, refit, blk, md0, idx, nfev, x0=None):
    lo, hi, xs = setup(kind, refit, blk); x0 = xs if x0 is None else np.array(x0, float)
    if len(lo) == 0: return np.array([]), 0
    fn = lambda x: np.concatenate([np.log10(c) - GS[i].lgl for i, c in zip(idx, curves(kind, *unpack(kind, refit, blk, x, md0), idx))])
    eps = 1e-6 * (hi - lo); r = least_squares(fn, np.clip(x0, lo + eps, hi - eps), bounds=(lo, hi), x_scale='jac', diff_step=.02, max_nfev=nfev); return r.x, int(r.nfev)
ROWS = {}
def row(tag, kind, refit=False, blk=None, md0={}, nk_frozen=0):
    if tag in OUT:
        ROWS[tag] = OUT[tag]; o = OUT[tag]
        print(f'\n== {tag} (checkpoint): E1 {o["e1"]:.4f} E2 {o["e2"]:.4f} E3 {o["e3"]:.4f} holdout {o["hold"]} knobs {o["nk"]}', flush=True); return o
    nf = 40 if refit else 60; lo, hi, _ = setup(kind, refit, blk)
    x, nfe = tune(kind, refit, blk, md0, ALLI, nf); K, md = unpack(kind, refit, blk, x, md0); cur = curves(kind, K, md)
    nk = len(lo); grade(f'A44 {tag}', cur, f'({nk} fitted + {nk_frozen} frozen knobs)'); s = stats(cur)
    names = (['dn', 'dm', 'db', 'dg', 'le', 'a1', 'a2', 'a4', 'le0', 'a3', 'f0', 'f1', 'dc', 'sc'] if refit else []) + [b[0] for b in BLK.get(blk, [])]
    atb = [n for n, v, a_, b_ in zip(names, x, lo, hi) if min(v - a_, b_ - v) < 1e-3 * (b_ - a_)]
    outl = [n for n, v in zip(names, x) if n in LIT and not (LIT[n][0] - 1e-9 <= v <= LIT[n][1] + 1e-9)]
    if nk:
        xh, _ = tune(kind, refit, blk, md0, TUNE, nf); hold = stats(curves(kind, *unpack(kind, refit, blk, xh, md0), UNSEEN), UNSEEN)['e1']
    else: hold = stats([cur[i] for i in UNSEEN], UNSEEN)['e1']
    ex = s['e1'] <= .02 and s['e2'] <= .04 and s['e3'] <= .02 and hold <= .025
    blkk = {n: round(float(md[n]), 4) for n in ('q0', 'sq', 'lkt', 'fsub', 'dlc', 'norm') if n in md and n != 'norm'}
    print(f' knobs fitted {nk} (+{nk_frozen} frozen), nfev {nfe}; block values {blkk}; at bound {atb}; outside literature range {outl}', flush=True)
    if refit: print(' K ' + ' '.join(f'{n}={v:+.3f}' for n, v in zip(names[:14], x[:14])), flush=True)
    print(f' holdout: tuned on GS[::2], unseen GS[1::2] E1 {hold:.4f} [{"PASS" if hold <= .025 else "FAIL"} <= 0.025]; VERDICT {"EXACT" if ex else "NOT EXACT"} {tl()}', flush=True)
    o = dict(kind=kind, refit=refit, blk=blk, md0={k: v for k, v in md0.items()}, x=[float(v) for v in x], K=[float(v) for v in K], md=md, nk=nk, nkf=nk_frozen, hold=float(hold), atb=atb, outl=outl, exact=bool(ex), **s)
    ck(tag, o); ROWS[tag] = o; return o
print('\n==== (a) HALO SHAPE, (b) TRUNCATION, (c) SUBSTRUCTURE, (d1) ENVIRONMENT c SHIFT', flush=True)
row('P0 plain baseline', 'plain')
row('Pa q 0.85 geo', 'plain', md0={'q0': .85}); row('Pa q 0.85 major (sensitivity)', 'plain', md0={'q0': .85, 'norm': 'major'})
row('Pa q global', 'plain', blk='qg'); row('Pa q global major (sensitivity)', 'plain', blk='qg', md0={'norm': 'major'}); row('Pa q(Sigma_b)', 'plain', blk='qs')
for k in (.5, 1., 2.): row(f'Pb k_t {k}', 'plain', md0={'lkt': np.log10(k)})
row('Pb k_t global', 'plain', blk='kt')
row('Pc f_sub 0.1', 'plain', md0={'fsub': .1}); row('Pc f_sub global', 'plain', blk='fs')
row('Pd env -0.05', 'plain', md0={'dlc': -.05}); row('Pd env global', 'plain', blk='env')
row('R0 R11b K11B', 'r11', nk_frozen=14)
row('Ra q 0.85 geo', 'r11', md0={'q0': .85}, nk_frozen=14); row('Ra q 0.85 major (sensitivity)', 'r11', md0={'q0': .85, 'norm': 'major'}, nk_frozen=14)
row('Ra q global', 'r11', blk='qg', nk_frozen=14); row('Ra q(Sigma_b)', 'r11', blk='qs', nk_frozen=14)
for k in (.5, 1., 2.): row(f'Rb k_t {k}', 'r11', md0={'lkt': np.log10(k)}, nk_frozen=14)
row('Rb k_t global', 'r11', blk='kt', nk_frozen=14)
row('Rc f_sub 0.1', 'r11', md0={'fsub': .1}, nk_frozen=14); row('Rc f_sub global', 'r11', blk='fs', nk_frozen=14)
row('Rd env -0.05', 'r11', md0={'dlc': -.05}, nk_frozen=14); row('Rd env global', 'r11', blk='env', nk_frozen=14)
row('RF0 R11b re-fit control', 'r11', refit=True)
for b, t_ in (('qg', 'RFa q global'), ('qs', 'RFa q(Sigma_b)'), ('kt', 'RFb k_t global'), ('fs', 'RFc f_sub global'), ('env', 'RFd env global')): row(t_, 'r11', refit=True, blk=b)
# truncation diagnostics
rl = np.array([GS[i].r[-1] / (3 * M2P[i] * Msun / (800 * np.pi * RHOC))**(1 / 3) for i in ALLI]); rlr = np.array([GS[i].r[-1] / (3 * m200k(GS[i].Ms, *K11B[:4]) * Msun / (800 * np.pi * RHOC))**(1 / 3) for i in ALLI])
print(f'\n truncation geometry: r_last/R200 median {np.median(rl):.3f} (plain SHMR), {np.median(rlr):.3f} (K11B SHMR); max {rl.max():.3f}, {rlr.max():.3f}', flush=True)
for k in (.5, 1., 2.):
    fr_ = np.mean(np.concatenate([GS[i].r / ((3 * M2P[i] * Msun / (800 * np.pi * RHOC))**(1 / 3) * k) > .5 for i in ALLI])); print(f'  k_t {k}: fraction of points with r > r_t/2 (plain) {fr_:.4f}', flush=True)
for tag in ('Pb k_t 0.5', 'Pb k_t 1.0', 'Pb k_t 2.0', 'Pb k_t global'):
    o = ROWS[tag]; dl = [np.log10(plain(i, None, o['md'], BASE)[-1] / plain(i, None, {}, BASE)[-1]) for i in ALLI]
    ext = []
    for fac in (2., 4.):
        d_ = []
        for i in ALLI:
            g = GS[i]; M = M2P[i]; c = float(np.interp(np.log10(M), LM, CG)); R = (3 * M * Msun / (800 * np.pi * RHOC))**(1 / 3); r = np.array([g.r[-1] * fac]); fb = min(g.Mb / M, .5)
            gb = G * g.mb[-1] / r**2; dm = (1 - fb) * M_nfw(r, M, c, R); dt = dm * trunc_ratio(r, dM_nfw(M, c, R), 10**o['md']['lkt'] * R)
            d_.append(float(np.log10((gb + G * dt / r**2) / (gb + G * dm / r**2))[0]))
        ext.append(np.median(d_))
    print(f'  {tag} (k_t {10**o["md"]["lkt"]:.3f}): median dlog g at the last point {np.median(dl):+.4f}, min {np.min(dl):+.4f}; past the data (no data graded) at 2 r_last {ext[0]:+.4f}, 4 r_last {ext[1]:+.4f}', flush=True)
# ======================= tie gates =======================
print(f'\n==== TIE GATES (knobs fixed, M200 per galaxy held at z 0, baryons fixed) {tl()}', flush=True)
CJ = [mkc(cc.Cosmology(name=f'a44J{j}', flat=True, H0=H0, Om0=1 - OL, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False, persistence='', print_warnings=False), 0.) for j, (OL, H0) in enumerate([(.70, 67.4), (.685, 73.), (.65, 73.)])]
CZ = {z: mkc(cos, z) for z in ZB}
BGC = {}
for b in BG:
    C, s8 = mkP(BG[b]); BGC[b] = (C, s8, {z: mkc(C, z) for z in ZS})
print(' backgrounds (footing P): ' + ', '.join(f'{b} sigma8 {BGC[b][1]:.4f} rho_DE(z)/rho_DE0 ' + '/'.join(f'{BGC[b][2][z]["rde"] / BGC[b][2][0.]["rde"]:.4f}' for z in ZB) for b in BGC) + f' {tl()}', flush=True)
def afit(cur): return fit_a(ALLB, np.concatenate(cur))
def ties(tag, cfn):
    """cfn(ctx) -> curves on all galaxies; ctx in the recipe's own format."""
    key = f'T_{tag}'
    if key in OUT: o = OUT[key]
    else:
        a0 = afit(cfn('base')); aJ = [afit(cfn(('J', j))) for j in range(3)]; sl = [float(np.log(aJ[k] / aJ[0]) / np.log(CJ[k]['rde'] / CJ[0]['rde'])) for k in (1, 2)]
        zr = [afit(cfn(('Z', z))) / a0 for z in ZB]; dev, pool = {}, []
        for b in BGC:
            ab = {z: afit(cfn(('B', b, z))) for z in ZS}; rr_ = {z: BGC[b][2][z]['rde'] / BGC[b][2][0.]['rde'] for z in ZS}
            dev[b] = [float(np.log10(ab[z] / ab[0.]) - .5 * np.log10(rr_[z])) for z in ZB]
            if b in ('B1', 'B1p', 'B1u', 'B2', 'B3', 'B4'): pool += [(np.log(rr_[z]), np.log(ab[z] / ab[0.])) for z in ZB]
        px, py = np.array(pool).T; pslope = float((px * py).sum() / (px * px).sum())
        o = dict(a0=float(a0), ke=float(a0 / AN), sl=sl, zr=[float(x) for x in zr], dev=dev, pslope=pslope); ck(key, o)
    g1 = abs(np.log10(o['ke'] / .5)) <= .05; g2 = all(abs(x - .5) <= .05 for x in o['sl']); g3 = all(ZB[z][0] <= x <= ZB[z][1] for z, x in zip(ZB, o['zr']))
    gtp = [b for b in o['dev'] if b != 'B0' and all(abs(x) <= .05 for x in o['dev'][b])]
    print(f' {tag}: a {o["a0"]:.4e}, kappa_eff {o["ke"]:.3f} [{"PASS" if g1 else "FAIL"} G1]; G2 slopes {o["sl"][0]:+.3f} {o["sl"][1]:+.3f} [{"PASS" if g2 else "FAIL"}]; '
          f'G3 a(z)/a(0) {" ".join(f"{x:.3f}" for x in o["zr"])} [{"PASS" if g3 else "FAIL"}]; G5 halo gravity, by definition', flush=True)
    print('   GT dev at z 1, 1.5, 2.33: ' + '; '.join(f'{b} ' + ' '.join(f'{x:+.3f}' for x in o['dev'][b]) for b in o['dev']) + f'; GT passes in {gtp} of the 7 evolving; pooled slope B1-B4 {o["pslope"]:+.3f} (0.5 to track) {tl()}', flush=True)
    return o
def ctx_of(spec):
    if spec == 'base': return BASE
    if spec[0] == 'J': return CJ[spec[1]]
    if spec[0] == 'Z': return CZ[spec[1]]
    return BGC[spec[1]][2][spec[2]]
def g4(kind, K, md):
    cur = curves(kind, K, md); lM = np.log10(M2P if kind == 'plain' else np.array([m200k(g.Ms, *K[:4]) for g in GS]))
    sel = [i for i in ALLI if 11 <= lM[i] <= 12.5]; la = np.log10([fit_a(GS[i].gb, cur[i]) for i in sel]); return len(sel), float(la.std())
TIE = ['P0 plain baseline', 'R0 R11b K11B', 'Pa q 0.85 geo', 'Ra q 0.85 geo']
for fam, pre in (('a', ('Pa q global', 'Pa q(Sigma_b)')), ('b', ('Pb k_t global',)), ('c', ('Pc f_sub global',)), ('d', ('Pd env global',))):
    TIE.append(min(pre, key=lambda t: ROWS[t]['e1']))
    TIE.append(min([t for t in ROWS if t.startswith(('R' + fam, 'RF' + fam)) and 'sensitivity' not in t], key=lambda t: ROWS[t]['e1']))
for t_ in TIE:
    o = ROWS[t_]; ties(t_, lambda s, o=o: curves(o['kind'], o['K'], o['md'], ALLI, ctx_of(s))); n4, s4_ = g4(o['kind'], o['K'], o['md'])
    print(f'   G4 {n4} hosts log M200 11-12.5: rms log a_i {s4_:.3f} dex [{"PASS" if s4_ <= .1 else "FAIL"}]', flush=True)
# ======================= (d2) environment term in A40's mock =======================
print(f'\n==== (d2) ENVIRONMENT TERM IN A40 MOCK {tl()}', flush=True)
s41 = open(os.path.join(HERE, 'recipe41.py'), encoding='utf-8').read(); exec(s41[s41.index('CGZ = '):s41.index('HP = np.concatenate')])
HP = np.concatenate([g.ev / g.vo <= .05 for g in GS]); SEEDS = (100, 101, 102)
A40J = json.load(open(os.path.join(HERE, 'recipe41.json')))
if 'sparc' not in OUT:
    sS, aS, rS = observer([g.gobs for g in GS]); ck('sparc', dict(s=sS, a=aS, hp=float(np.sqrt((rS[HP]**2).mean()))))
SP = OUT['sparc']; print(f' SPARC observer fit: scatter all {SP["s"]:.4f}, good points {SP["hp"]:.4f}, a0 {SP["a"]:.3e} (A40: {A40J["sparc"]["s"]:.4f}, {A40J["sparc"]["hp"]:.4f}, {A40J["sparc"]["a"]:.3e})', flush=True)
def mock2(rcm, p, be, db_, seed, errors=True, noiseless=False):
    rng = np.random.default_rng(seed); rng2 = np.random.default_rng(500 + seed); out = []
    for j, g in enumerate(GS):
        nu, x, e = rng.normal(0, 1, 3); y = rng2.normal(0, 1); ut = trend(g, p) + (0 if noiseless else .1 * nu)
        gbt = gbu(g, ut); Mst = g.Ms * 10**ut; Mbt = Mst + 1.33 * g.t['MHI'] * 1e9
        M = m200_of(Mst * 10**(0 if noiseless else .15 * x))
        dc = (be * db_) if noiseless else .11 * (rcm * x + np.sqrt(max(1 - rcm**2, 0)) * e) + be * (y + db_)
        c = cz(M, 0.) * 10**dc; gt = halo(g, gbt, M, c, min(Mbt / M, .5), False, 0.)
        if errors:
            vt = np.sqrt(gt * g.r); fD = max(1 + rng.normal(0, g.t['eD'] / g.t['D']), .3); io = np.clip(g.t['i'] + rng.normal(0, g.t['ei']), 15, 89)
            vo = np.maximum(vt * np.sin(np.radians(g.t['i'])) / np.sin(np.radians(io)) + rng.normal(0, 1, len(g.r)) * g.ev, 1e3); gt = vo**2 / (g.r * fD)
        out.append(gt)
    return out
def cell2(rcm, p, be, db_):
    key = f'D2_{rcm:+.2f}_{p:+.2f}_{be:.2f}_{db_:+.2f}'
    if key in OUT: return OUT[key]
    obs = [observer(mock2(rcm, p, be, db_, s)) for s in SEEDS]; intr = mock2(rcm, p, be, db_, SEEDS[0], errors=False); e = egates(intr)
    r = dict(s_hp=float(np.mean([np.sqrt((o[2][HP]**2).mean()) for o in obs])), s_hp_sd=float(np.std([np.sqrt((o[2][HP]**2).mean()) for o in obs])), s_all=float(np.mean([o[0] for o in obs])),
             a=float(np.mean([o[1] for o in obs])), E=e, ev=egates(intr, range(0, NG, 2))[0], od=egates(intr, range(1, NG, 2))[0])
    ck(key, r); return r
D2 = []
for rcm in (0., -.6):
    for be, db_ in ((0., 0.), (.05, 0.), (.05, -.5), (.1, 0.), (.1, -.5)):
        r = cell2(rcm, -.1, be, db_); D2.append((rcm, be, db_, r)); b1 = abs(r['s_hp'] - SP['hp']) <= .02; b2 = abs(np.log10(r['a'] / A0)) <= .05
        print(f' rho_cM {rcm:+.2f} b_env {be:.2f} dbar {db_:+.2f}: good-points scatter {r["s_hp"]:.4f}+-{r["s_hp_sd"]:.4f} [{"PASS" if b1 else "FAIL"} B1]; all {r["s_all"]:.4f}; a0 {r["a"]:.3e} ({np.log10(r["a"] / A0):+.3f} dex) [{"PASS" if b2 else "FAIL"} B2]; '
              f'intrinsic E1 {r["E"][0]:.4f} E2 {r["E"][1]:.4f} E3 {r["E"][2]:.4f} [{"PASS" if r["E"][0] <= .02 and r["E"][1] <= .04 and r["E"][2] <= .02 else "FAIL"}] {tl()}', flush=True)
        if be == 0.:
            a40 = A40J[f'{rcm:+.2f}_+0.00_-0.10_0']; dmx = max(abs(r['s_hp'] - a40['s_hp']), abs(r['a'] / a40['a'] - 1), max(abs(x - y) for x, y in zip(r['E'], a40['E'])))
            print(f'   control vs recipe41.json cell: max difference {dmx:.1e} [{"PASS" if dmx < 1e-6 else "FAIL"}]', flush=True)
hb = min(D2, key=lambda t: t[3]['ev']); print(f' holdout: cell chosen on GS[::2] by intrinsic rms: rho_cM {hb[0]:+.2f} b_env {hb[1]:.2f} dbar {hb[2]:+.2f}; unseen GS[1::2] {hb[3]["od"]:.4f} [{"PASS" if hb[3]["od"] <= .025 else "FAIL"}]', flush=True)
nl = mock2(0., -.1, .1, -.5, 100, errors=False, noiseless=True); a_nl = fit_a(ALLB, np.concatenate(nl)); e_nl = egates(nl)
print(f' noiseless mock with the field offset (b_env 0.1, dbar -0.5): E1 {e_nl[0]:.4f}, fitted a {a_nl:.3e}, kappa_eff {a_nl / AN:.3f} {tl()}', flush=True)
# ======================= A25 compact Pareto point + best shape block =======================
print(f'\n==== A25 COMPACT PARETO POINT + BEST SHAPE BLOCK {tl()}', flush=True)
fam_a = {t: ROWS[t]['e1'] for t in ('RFa q global', 'RFa q(Sigma_b)')}; gain = ROWS['RF0 R11b re-fit control']['e1'] - min(fam_a.values())
SHB = 'qs' if fam_a['RFa q(Sigma_b)'] < fam_a['RFa q global'] - .0005 else 'qg'
print(f' shape on the R11b re-fit: control {ROWS["RF0 R11b re-fit control"]["e1"]:.4f}, q global {fam_a["RFa q global"]:.4f}, q(Sigma_b) {fam_a["RFa q(Sigma_b)"]:.4f}; best gain {gain:+.4f}; block used {SHB}', flush=True)
s27 = open(os.path.join(HERE, 'recipe27.py'), encoding='utf-8').read(); NS = dict(globals())
exec(s27[s27.index('# A19 SIDM solver'):s27.index('# ---------------- checkpoint')], NS)
ST27 = json.load(open(os.path.join(HERE, 'recipe27_ckpt.json'))); allrec = ST27['S1'] + list(ST27['S3'].values()) + ST27['S2']; PAR = {}
for d in allrec:
    if d['k'] not in PAR or d['rms'] < PAR[d['k']]['rms']: PAR[d['k']] = d
def a25_shape(P, on, sh, idx, ctx):
    cur = NS['curves'](P, on, idx, ctx=ctx, mode='direct'); lM = NS['shmr'](P, idx); p = dict(zip(NS['NAMES'], P)); out = []
    for i, l, cu in zip(idx, lM, cur):
        g = GS[i]; M = 10**l; R = (3 * M * Msun / (4 * np.pi * 200 * ctx.rhoc))**(1 / 3)
        c = float(np.interp(l, LM, ctx.CG)) * 10**p['dc'] * (M / 1e12)**p['sc'] * g.sb**p['N2']; A = max(.16 + p['N1'] * (l - 12), .05)
        F = shape_ratio(g.r, dM_ein(M, c, R, A), float(np.clip(sh[0] * SB[i]**(sh[1] if len(sh) > 1 else 0.), .3, 1.5)))
        out.append(g.gb + (cu - g.gb) * F)
    return out
NSH = len(BLK[SHB]); SLO = np.array([b[1] for b in BLK[SHB]]); SHI = np.array([b[2] for b in BLK[SHB]]); SX0 = np.array([b[3] for b in BLK[SHB]])
J25 = None
for kp in (18, 28):
    d = PAR[kp]; on, P0 = d['on'], np.array(d['P']); fr = NS['free_of'](on); tagk = f'A25 {kp}'
    s0 = stats(NS['curves'](P0, on, mode='direct')); print(f'\n A25 Pareto {kp} knobs, units {[u for u in on if u in NS["BLOCKS"]]}: control E1 {s0["e1"]:.4f} (recipe27.out {"0.0230" if kp == 18 else "0.0222"}), E2 {s0["e2"]:.4f}, E3 {s0["e3"]:.4f} {tl()}', flush=True)
    t = time.time(); _ = a25_shape(P0, on, SX0, ALLI, NS['BASE']); te = time.time() - t; print(f'  timing: one evaluation with shape {te:.3f} s', flush=True)
    def mkfn(idx, free_all):
        def fn(x):
            P = P0.copy()
            if free_all: P[fr] = x[:len(fr)]; sh = x[len(fr):]
            else: sh = x
            return np.concatenate([np.log10(c) - GS[i].lgl for i, c in zip(idx, a25_shape(P, on, sh, idx, NS['BASE']))])
        return fn
    for step, free_all in (('step 1 (A25 knobs frozen, shape fitted)', False), ('step 2 (all re-fitted)', True)):
        key = f'{tagk} {step[:6]}'
        if key not in OUT:
            lo = np.concatenate([NS['LO'][fr], SLO]) if free_all else SLO; hi = np.concatenate([NS['HI'][fr], SHI]) if free_all else SHI
            x0 = np.concatenate([P0[fr], SX0]) if free_all else SX0; eps = 1e-6 * (hi - lo)
            r = least_squares(mkfn(ALLI, free_all), np.clip(x0, lo + eps, hi - eps), bounds=(lo, hi), x_scale='jac', diff_step=.02, max_nfev=60 if free_all else 40)
            P = P0.copy(); sh = r.x
            if free_all: P[fr] = r.x[:len(fr)]; sh = r.x[len(fr):]
            cur = a25_shape(P, on, sh, ALLI, NS['BASE']); s = stats(cur)
            atb = [NS['NAMES'][j] for j in fr if min(P[j] - NS['LO'][j], NS['HI'][j] - P[j]) < 1e-3 * (NS['HI'][j] - NS['LO'][j])] + [b[0] for b, v in zip(BLK[SHB], sh) if min(v - b[1], b[2] - v) < 1e-3 * (b[2] - b[1])]
            if free_all:
                lo_, hi_ = lo, hi; xc = (lo_ + hi_) / 2; xc[len(fr):] = SX0; Pc = NS['OFF'].copy()
                rh = least_squares(mkfn(TUNE, True), np.clip(xc, lo_ + eps, hi_ - eps), bounds=(lo_, hi_), x_scale='jac', diff_step=.02, max_nfev=80)
                Ph = P0.copy(); Ph[fr] = rh.x[:len(fr)]; hcl = stats(a25_shape(Ph, on, rh.x[len(fr):], UNSEEN, NS['BASE']), UNSEEN)['e1']
                rl_ = least_squares(mkfn(TUNE, True), r.x, bounds=(lo_, hi_), x_scale='jac', diff_step=.02, max_nfev=60)
                Pl = P0.copy(); Pl[fr] = rl_.x[:len(fr)]; hlk = stats(a25_shape(Pl, on, rl_.x[len(fr):], UNSEEN, NS['BASE']), UNSEEN)['e1']
            else:
                rh = least_squares(mkfn(TUNE, False), np.clip(SX0, SLO + eps[:NSH], SHI - eps[:NSH]), bounds=(SLO, SHI), x_scale='jac', diff_step=.02, max_nfev=40)
                hcl = stats(a25_shape(P0, on, rh.x, UNSEEN, NS['BASE']), UNSEEN)['e1']; hlk = None
            OUT_ = dict(P=[float(v) for v in P], sh=[float(v) for v in sh], nk=kp + NSH, atb=atb, hold=float(hcl), leaky=None if hlk is None else float(hlk), **s); ck(key, OUT_)
        o = OUT[key]; P, sh = np.array(o['P']), o['sh']
        grade(f'A44 {tagk} + shape {SHB} {step}', a25_shape(P, on, sh, ALLI, NS['BASE']), f'({o["nk"]} knobs)')
        ex = o['e1'] <= .02 and o['e2'] <= .04 and o['e3'] <= .02 and o['hold'] <= .025
        print(f'  shape knobs {np.round(sh, 4).tolist()}; at bound {o["atb"]}; holdout clean (centre start, GS[::2] tuned) unseen {o["hold"]:.4f} [{"PASS" if o["hold"] <= .025 else "FAIL"}]' + (f'; leaky {o["leaky"]:.4f} (not gated)' if o['leaky'] is not None else '') +
              f'; change in E1 vs A25 point {o["e1"] - s0["e1"]:+.4f}; VERDICT {"EXACT" if ex else "NOT EXACT"} {tl()}', flush=True)
        if free_all and kp == 18:
            CJ25 = [NS['mkctx'](cc.Cosmology(name=f'a44j{j}', flat=True, H0=H0, Om0=1 - OL, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False, persistence='', print_warnings=False)) for j, (OL, H0) in enumerate([(.70, 67.4), (.685, 73.), (.65, 73.)])]
            CZ25 = {z: NS['mkctx'](cos, z) for z in ZB}; BG25 = {b: {z: NS['mkctx'](BGC[b][0], z) for z in ZS} for b in BGC}
            for j, C in enumerate(CJ25): C.rde = CJ[j]['rde']
            def c25(s, P=P, sh=sh, on=on):
                if s == 'base': ctx = NS['BASE']
                elif s[0] == 'J': ctx = CJ25[s[1]]
                elif s[0] == 'Z': ctx = CZ25[s[1]]
                else: ctx = BG25[s[1]][s[2]]
                return a25_shape(P, on, sh, ALLI, ctx)
            ties(f'{tagk} + shape re-fit', c25)
            cur = c25('base'); lM = NS['shmr'](P, ALLI); sel = [i for i in ALLI if 11 <= lM[i] <= 12.5]; la = np.log10([fit_a(GS[i].gb, cur[i]) for i in sel])
            print(f'   G4 {len(sel)} hosts: rms log a_i {la.std():.3f} dex [{"PASS" if la.std() <= .1 else "FAIL"}]', flush=True)
    # A25 holdout rule completed (fix after the first run, see FROZEN_A44.md): one Latin-hypercube start (seed 99, 60 evaluations) beside the centre start; keep the lower tuned-set cost
    keyh = f'{tagk} holdout two-start'
    if keyh not in OUT:
        lo = np.concatenate([NS['LO'][fr], SLO]); hi = np.concatenate([NS['HI'][fr], SHI]); eps = 1e-6 * (hi - lo); xc = (lo + hi) / 2; xc[len(fr):] = SX0
        fnT = mkfn(TUNE, True); rc_ = least_squares(fnT, np.clip(xc, lo + eps, hi - eps), bounds=(lo, hi), x_scale='jac', diff_step=.02, max_nfev=80)
        xl = lo + qmc.LatinHypercube(d=len(lo), seed=99).random(1)[0] * (hi - lo); rl2 = least_squares(fnT, np.clip(xl, lo + eps, hi - eps), bounds=(lo, hi), x_scale='jac', diff_step=.02, max_nfev=60)
        res = []
        for rr_ in (rc_, rl2):
            Ph = P0.copy(); Ph[fr] = rr_.x[:len(fr)]; res.append((float(np.sqrt(2 * rr_.cost / len(rr_.fun))), stats(a25_shape(Ph, on, rr_.x[len(fr):], UNSEEN, NS['BASE']), UNSEEN)['e1']))
        ck(keyh, dict(centre=res[0], lhs=res[1]))
    o = OUT[keyh]; pick = o['centre'] if o['centre'][0] <= o['lhs'][0] else o['lhs']
    print(f'  {tagk} + shape re-fit, holdout with both starts: centre tuned {o["centre"][0]:.4f} unseen {o["centre"][1]:.4f}; LHS tuned {o["lhs"][0]:.4f} unseen {o["lhs"][1]:.4f}; kept (lower tuned cost) unseen {pick[1]:.4f} [{"PASS" if pick[1] <= .025 else "FAIL"} <= 0.025] {tl()}', flush=True)
print(f'\npeak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6:.0f} MB {tl()}')
print('Rival language; every knob disclosed. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
