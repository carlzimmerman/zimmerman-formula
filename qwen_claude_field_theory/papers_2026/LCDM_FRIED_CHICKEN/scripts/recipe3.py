"""Amendment A2 of ../FROZEN_RECIPE.md: LCDM parts only. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
import lib, importlib.util as iu
from scipy.special import gammainc
sp = iu.spec_from_file_location('rt', os.path.join(HERE, '..', '..', 'REDTEAM_LCDM_PRIEST', 'scripts', 'lib.py')); rt = iu.module_from_spec(sp); sp.loader.exec_module(rt)
def ein(r, M, c, a):
    R = (3 * M * Msun / (4 * np.pi * 200 * lib.RHOC))**(1 / 3); return M * Msun * gammainc(3 / a, 2 / a * (r * c / R)**a) / gammainc(3 / a, 2 / a * c**a)
def halo(g, M, c, a, f, n, eta):
    fb = min(g.Mb / M, .5); m0 = np.maximum(ein(g.r, M, c, a), 1e-30); ri = g.r.copy()
    for _ in range(12):
        mi = np.maximum(ein(ri, M, c, a), 1e-30); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m / g.r**2
LO = np.array([.10, -1, 0, np.log10(.3)]); HI = np.array([.30, 1, 1, np.log10(3)])
def perg(bc, bm, tag):
    out, P = [], []
    for g in GS:
        M0 = np.log10(m200_of(g.Ms)); c0 = np.log10(float(cflat(10**M0, 0, 0))); lo = np.r_[M0 - bm, c0 - bc, LO]; hi = np.r_[M0 + bm, c0 + bc, HI]
        fn = lambda v: np.log10(halo(g, 10**v[0], 10**v[1], v[2], v[3], v[4], 10**v[5])) - np.log10(g.gl); best = None
        for s in range(3):
            x = .5 * (lo + hi) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
            r = least_squares(fn, np.clip(x, lo + 1e-4, hi - 1e-4), bounds=(lo, hi), max_nfev=30, diff_step=.01)
            if best is None or r.cost < best.cost: best = r
        v = best.x; out.append(halo(g, 10**v[0], 10**v[1], v[2], v[3], v[4], 10**v[5])); P.append(np.r_[v[0] - M0, v[1] - c0, v[2:]])
    P = np.array(P); grade(tag, out, f'({6 * len(GS)} parameters)'); print(' p50, p16, p84 of dlogM, dlogc, alpha, f, n, logeta:', np.round(np.percentile(P, [50, 16, 84], axis=0), 2).tolist()); return P
P1 = perg(.11, .3, 'R9 per galaxy, 1 sigma priors'); P2 = perg(.22, .6, 'R9 per galaxy, 2 sigma priors')
for g in GS: g.x = np.array([np.log10(g.Mb) - 9.5, np.log10(g.Mb / (g.Rd / kpc)**2 / 1e6) - 2, 1.33 * (g.Mb - g.Ms) / 1.33 / g.Mb])
def feats(g): x = g.x; return np.array([1, x[0], x[1], x[2], x[0]**2, x[1]**2, x[0] * x[1]])
NF = 7
def glob(g, w, cmul=1., Mmul=1.):
    W = w.reshape(6, NF); y = W @ feats(g); M = m200_of(g.Ms) * 10**y[0] * Mmul
    return halo(g, M, float(cflat(M, 0, 0)) * 10**y[1] * cmul, np.clip(y[2], .08, .4), np.clip(y[3], -1, 1), np.clip(y[4], 0, 1), 10**np.clip(y[5], -1, 1))
def resid(w, S): return np.concatenate([np.log10(glob(g, w)) - np.log10(g.gl) for g in S])
F = np.array([feats(g) for g in GS]); w0 = np.linalg.lstsq(F, P2, rcond=None)[0].T.ravel()
ODD, EVEN = GS[::2], GS[1::2]
def tune(S, x0): return least_squares(resid, x0, args=(S,), max_nfev=14, diff_step=.02, x_scale=.1).x
wo = tune(ODD, w0); ro = resid(wo, ODD); re_ = resid(wo, EVEN)
print(f'\n== R10 tuned on odd galaxies, 42 coefficients\n rms on tuned {np.sqrt((ro**2).mean()):.4f} dex; on unseen {np.sqrt((re_**2).mean()):.4f} dex')
wa = tune(GS, wo); g10 = [glob(g, wa) for g in GS]; grade('R10 tuned on all', g10, '(42 coefficients)')
ys = np.array([wa.reshape(6, NF) @ feats(g) for g in GS]); print(' p50, p16, p84 of dlogM, dlogc, alpha, f, n, logeta:', np.round(np.percentile(ys, [50, 16, 84], axis=0), 2).tolist())
print(f' galaxies with |dlogM| <= 0.3 and |dlogc| <= 0.11: {((abs(ys[:, 0]) <= .3) & (abs(ys[:, 1]) <= .11)).sum()} of {len(GS)}; within 0.6, 0.22: {((abs(ys[:, 0]) <= .6) & (abs(ys[:, 1]) <= .22)).sum()}')
print(' coefficients', np.round(wa, 3).tolist())
def setcos(C, z=0):
    cc.setCurrent(C); h = C.h; lib.CG = np.array([float(CM.concentration(10**m * h, '200c', z, model='diemer19')) for m in LM]); lib.RHOC = C.rho_c(z) * h**2 * Msun / kpc**3
    return C.Ode0 * C.rho_c(0) * h**2 * Msun / kpc**3
def af(cm=1., Mm=1.): return fit_a(ALLB, np.concatenate([glob(g, wa, cm, Mm) for g in GS]))
u, d, dl = rt.cosmo_case('rde'); wb = .0493 * .674**2
CU, CD = rt.setc(**u)[0], rt.setc(**d)[0]; KS = [rt.setc(H0=67.4, OL=.70, wb=wb)[0], rt.setc(H0=73., OL=.685, wb=wb)[0], rt.setc(H0=73., OL=.65, wb=wb)[0]]; C0 = rt.setc()[0]
R0 = setcos(C0); a00 = af(); print(f'\nJ2 base a {a00:.3e}')
GRP = [(C, setcos(C)) for C in (CU, CD, *KS)]; UNIT = lambda R: 2.998e8 * np.sqrt(G * R)
def state(v):
    p, r, s = v; A = []
    for C, R in GRP:
        setcos(C); h = C.H0 / 67.4; A.append(af((R / R0)**p * h**r, h**s))
    return A
def jres(v):
    A = state(v); return np.r_[(np.log(A[0] / A[1]) / dl - .5) * 2, [np.log(A[i + 2] / UNIT(GRP[i + 2][1]) / .5) for i in range(3)]]
A = state((0, 0, 0)); print(f' no hand: slope {np.log(A[0] / A[1]) / dl:+.3f}; kappa', [round(float(A[i + 2] / UNIT(GRP[i + 2][1])), 3) for i in range(3)])
v = least_squares(jres, [.2, 0, 0], max_nfev=12, diff_step=.05, bounds=([-3, -12, -12], [3, 12, 12])).x; A = state(v); sl = np.log(A[0] / A[1]) / dl; ks = [float(A[i + 2] / UNIT(GRP[i + 2][1])) for i in range(3)]
print(f' hand p {v[0]:.2f}, r {v[1]:.2f}, s {v[2]:.2f}: slope {sl:+.3f} [{"PASS" if abs(sl - .5) <= .05 else "FAIL"} E4]; kappa', [round(k, 3) for k in ks], f'[{"PASS" if all(abs(k / .5 - 1) <= .05 for k in ks) else "FAIL"}]')
BAND = {1.: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; TG = {1.: .91, 1.5: .94, 2.33: .91}
def zs(q):
    o = {}
    for z in BAND: setcos(C0, z); o[z] = af((1 + z)**(q[0] + q[1] * z)) / a00
    return o
print(' a(z)/a(0) no hand', {z: round(float(x), 3) for z, x in zs((0, 0)).items()})
q = least_squares(lambda q: [np.log(zs(q)[z] / TG[z]) for z in BAND], [-1, 0], max_nfev=10, diff_step=.05).x; o = zs(q)
print(f' hand q1 {q[0]:.2f}, q2 {q[1]:.2f}:', {z: round(float(x), 3) for z, x in o.items()}, f'[{"PASS" if all(BAND[z][0] <= o[z] <= BAND[z][1] for z in BAND) else "FAIL"} E5]')
setcos(C0)
print('\nRival language; every knob disclosed. kappa = 1/2 FITTED; not theory closed.')
