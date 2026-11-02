"""LCDM-flavoured recipes against the law on real SPARC baryons, per ../FROZEN_RECIPE.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import numpy as np, os, glob, json, warnings
from scipy.optimize import least_squares, minimize_scalar, brentq
from scipy.ndimage import gaussian_filter1d
from colossus.cosmology import cosmology as cc
from colossus.halo import concentration as CM
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '..', '..', '..', 'real_research', 'data')
G, kpc, Msun, A0 = 6.674e-11, 3.0857e19, 1.989e30, 9.3625e-11
YD, YB = .5, .7
cos = cc.setCosmology('fc', dict(flat=True, H0=67.4, Om0=.315, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False))
RHOC = cos.rho_c(0) * cos.h**2 * Msun / kpc**3
LM = np.linspace(8.5, 15.5, 71)
CG = np.array([float(CM.concentration(10**m * cos.h, '200c', 0, model='diemer19')) for m in LM])
LMS = np.linspace(8.5, 15.5, 701)
def smhm(M, dn=0.): x = M / 10**11.59; return 2 * .0351 * 10**dn * M / (x**-1.376 + x**.608)
def m200_of(Ms, dn=0.): return 10**np.interp(np.log10(Ms), np.log10(smhm(10**LMS, dn)), LMS)
def mu(x): return np.log(1 + x) - x / (1 + x)
def law(gb, a=A0): return .5 * (gb + np.sqrt(gb**2 + 4 * gb * a))
def table():
    out = {}
    for l in open(os.path.join(D, 'SPARC_Lelli2016c.mrt')):
        p = l.split()
        if len(p) >= 17 and p[1].isdigit() and len(l) > 90:
            try: out[p[0]] = dict(L=float(p[7]), Rd=float(p[11]), MHI=float(p[13]), Q=int(p[17]))
            except (ValueError, IndexError): pass
    return out
class Gal: pass
def load():
    T, gs = table(), []
    for f in sorted(glob.glob(os.path.join(D, 'sparc_data', '*_rotmod.dat'))):
        n = os.path.basename(f).replace('_rotmod.dat', '')
        if n not in T: continue
        a = np.loadtxt(f); a = a[a[:, 0] > 0]
        vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5])
        ok = vb2 > 0
        if ok.sum() < 5: continue
        g = Gal(); g.n = n; g.r = a[ok, 0] * kpc; g.vb2 = vb2[ok] * 1e6; g.gb = g.vb2 / g.r; g.gobs = (a[ok, 1] * 1e3)**2 / g.r
        g.Ms = YD * T[n]['L'] * 1e9; g.Mb = g.Ms + 1.33 * T[n]['MHI'] * 1e9; g.Rd = T[n]['Rd'] * kpc; g.mb = g.vb2 * g.r / G
        g.mbtot = g.Mb * Msun; g.gl = law(g.gb); gs.append(g)
    return gs
GS = load(); ALLB = np.concatenate([g.gb for g in GS]); ALLL = np.concatenate([g.gl for g in GS]); ALLO = np.concatenate([g.gobs for g in GS])
print(f'sample: {len(GS)} galaxies, {len(ALLB)} points; Y_disk {YD}, Y_bul {YB}')
def fit_a(gb, gt):
    return 10**minimize_scalar(lambda x: ((np.log10(law(gb, 10**x)) - np.log10(gt))**2).sum(), bounds=(-12, -8), method='bounded').x
def grade(tag, cur, extra=''):
    gt = np.concatenate(cur); d = np.log10(gt) - np.log10(ALLL); ob = np.log10(gt) - np.log10(ALLO)
    idx = np.cumsum([0] + [len(c) for c in cur]); per = np.array([np.sqrt((d[idx[i]:idx[i + 1]]**2).mean()) for i in range(len(cur))])
    e1 = np.sqrt((d**2).mean()); e2 = np.percentile(per, 95); b = np.floor(np.log10(ALLB) * 2) / 2; bins = []
    for x in np.unique(b):
        if (b == x).sum() >= 50: bins.append((x, d[b == x].mean()))
    e3 = max(abs(v) for _, v in bins)
    print(f'\n== {tag} {extra}\n rms to law {e1:.4f} dex [{"PASS" if e1 <= .02 else "FAIL"} E1]; p95 per-galaxy {e2:.4f} [{"PASS" if e2 <= .04 else "FAIL"} E2]; worst bin {e3:.4f} [{"PASS" if e3 <= .02 else "FAIL"} E3]')
    print(' bins', ' '.join(f'{x:.1f}:{v:+.3f}' for x, v in bins))
    print(f' a fit {fit_a(ALLB, gt):.3e}; rms to observed {np.sqrt((ob**2).mean()):.4f} dex, mean {ob.mean():+.4f}')
    return e1
def nfw_m(r, M200, c):
    R = (3 * M200 * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3); rs = R / c
    return M200 * Msun * mu(r / rs) / mu(c), R
def cflat(M, dc, sc): return np.interp(np.log10(M), LM, CG) * 10**dc * (M / 1e12)**sc
def r1(g, k):
    dc, sc, dn, f = k[:4]; M = m200_of(g.Ms, dn); c = cflat(M, dc, sc); fb = min(g.Mb / M, .5)
    m0 = (1 - fb) * nfw_m(g.r, M, c)[0]
    if f != 0:
        ri = g.r.copy()
        for _ in range(25):
            mi = nfw_m(ri, M, c)[0]; ri = .5 * ri + .5 * g.r * (np.maximum(g.mb, 0) + (1 - fb) * mi) / mi
        m0 = np.maximum((1 - f) * m0 + f * (1 - fb) * nfw_m(ri, M, c)[0], 1e-3 * m0)
    return g.gb + G * m0 / g.r**2
def r2(g, k):
    dc, sc, dn, f, eta, n0, n1 = k; M = m200_of(g.Ms, dn); c = cflat(M, dc, sc); fb = min(g.Mb / M, .5)
    n = np.clip(n0 * (g.Ms / M / .01)**n1, 0, 1); ft = np.tanh(g.r / (eta * 1.75 * g.Rd))
    return g.gb + G * (1 - fb) * nfw_m(g.r, M, c)[0] * ft**n / g.r**2
def fit(fn, x0, lo, hi, tag):
    resid = lambda k: np.log10(np.concatenate([fn(g, k) for g in GS])) - np.log10(ALLL)
    best = None
    for s in range(3):
        st = x0 if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        r = least_squares(resid, np.clip(st, np.array(lo) + 1e-6, np.array(hi) - 1e-6), bounds=(lo, hi), max_nfev=25, diff_step=.02)
        if best is None or r.cost < best.cost: best = r
    print(f'\n{tag} knobs', np.round(best.x, 3).tolist(), 'at bound', [i for i, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)])
    return best.x
def thermal(g, rho0, sig, n=160):
    x = np.linspace(np.log(g.r[0] * .05), np.log(g.r[-1]), n); dx = x[1] - x[0]; lr0 = np.log(g.r)
    gbg = np.interp(x, lr0, g.gb); ins = x < lr0[0]; gbg[ins] = g.gb[0] * np.exp(x[ins] - lr0[0])
    rr = np.exp(x); s2 = sig**2; lr = 0.; M = 4 * np.pi / 3 * rho0 * rr[0]**3; out = np.empty(n); fp = 4 * np.pi * rho0
    for i in range(n):
        out[i] = M; r = rr[i]; rho = rho0 * np.exp(lr)
        lr -= dx * r * (gbg[i] + G * M / r**2) / s2; M += fp * np.exp(lr) * r**3 * dx
    return g.gb + G * np.interp(lr0, x, out) / g.r**2
def r3params(g, s, Sig, a=A0):
    sig = (s * G * g.mbtot * a / 4)**.25; return 4 * np.pi * G * Sig**2 / (9 * sig**2), sig
