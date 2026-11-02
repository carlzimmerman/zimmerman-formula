"""Amendment A1 of ../FROZEN_RECIPE.md. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
import lib, importlib.util as iu, sys
sp = iu.spec_from_file_location('rt', os.path.join(HERE, '..', '..', 'REDTEAM_LCDM_PRIEST', 'scripts', 'lib.py')); rt = iu.module_from_spec(sp); sp.loader.exec_module(rt)
def r3params(g, s, Sig, a=A0):
    sig = (s * G * g.mbtot * a / 4)**.25; return 4 * np.pi * G * Sig**2 / (9 * sig**2), sig
def thermal(g, rho0, sig, n=160):
    x = np.linspace(np.log(g.r[0] * .05), np.log(g.r[-1]), n); dx = x[1] - x[0]; lr0 = np.log(g.r)
    gbg = np.interp(x, lr0, g.gb); ins = x < lr0[0]; gbg[ins] = g.gb[0] * np.exp(x[ins] - lr0[0])
    rr = np.exp(x); s2 = sig**2; lr = 0.; M = 4 * np.pi / 3 * rho0 * rr[0]**3; out = np.empty(n); fp = 4 * np.pi * rho0
    for i in range(n):
        out[i] = M; r = rr[i]; lr -= dx * r * (gbg[i] + G * M / r**2) / s2; M += fp * np.exp(lr) * r**3 * dx
    return g.gb + G * np.interp(lr0, x, out) / g.r**2
# R3 recheck
def thermal_rho(g, rho0, sig, n=160):
    x = np.linspace(np.log(g.r[0] * .05), np.log(g.r[-1]), n); dx = x[1] - x[0]; lr0 = np.log(g.r)
    gbg = np.interp(x, lr0, g.gb); ins = x < lr0[0]; gbg[ins] = g.gb[0] * np.exp(x[ins] - lr0[0])
    rr = np.exp(x); s2 = sig**2; lr = 0.; M = 4 * np.pi / 3 * rho0 * rr[0]**3; out = np.empty(n)
    for i in range(n):
        out[i] = M; r = rr[i]; lr -= dx * r * (gbg[i] + G * M / r**2) / s2; M += 4 * np.pi * rho0 * np.exp(lr) * r**3 * dx
    return g.gb + G * np.interp(lr0, x, out) / g.r**2
def r3(g, k): return thermal_rho(g, *r3params(g, 10**k[0], 10**k[1]))
ALLR = lambda fn, k: np.log10(np.concatenate([fn(g, k) for g in GS])) - np.log10(ALLL)
lo, hi = [-1, np.log10(A0 / G) - 2], [1, np.log10(A0 / G) + 2]
r = least_squares(lambda k: ALLR(r3, k), [0, np.log10(.27 * A0 / G)], bounds=(lo, hi), max_nfev=40, diff_step=.01)
grade('R3 recheck, restart at R4 medians', [r3(g, r.x) for g in GS], f'(s={10**r.x[0]:.3f}, G Sigma*/a0={10**r.x[1] * G / A0:.3f})')
# R6
def r6(gd): return lambda g: g.gb / (1 - np.exp(-np.sqrt(g.gb / gd)))
rr6 = minimize_scalar(lambda x: ((np.log10(np.concatenate([r6(10**x)(g) for g in GS])) - np.log10(ALLL))**2).sum(), bounds=(-11, -9), method='bounded').x
grade('R6 one published function', [r6(10**rr6)(g) for g in GS], f'(g_dagger={10**rr6:.3e}, ratio to a0 {10**rr6 / A0:.3f})')
# R7, R8: halo with contraction and core
def halo(g, M, c, f, n, eta=1., fbmax=.5):
    fb = min(g.Mb / M, fbmax); mi0 = nfw_m(g.r, M, c)[0]; ri = g.r.copy()
    for _ in range(15):
        mi = nfw_m(ri, M, c)[0]; ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * mi0 + f * nfw_m(ri, M, c)[0], 1e-3 * mi0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m / g.r**2
SB = {g.n: (g.Mb / (g.Rd / kpc)**2 / 1e6) / 100 for g in GS}
def r7(g, k, cmul=1.):
    dc, sc, dn, f, eta, n0, n1, gc, gm = k; sb = SB[g.n]; M = m200_of(g.Ms, dn) * sb**gm; c = cflat(M, dc, sc) * sb**gc * cmul
    return halo(g, M, c, f, np.clip(n0 * (g.Ms / M / .01)**n1, 0, 1), eta)
LO7 = [-.33, -.15, -.54, -1, .1, 0, -2, -1, -1.5]; HI7 = [.33, .15, .54, 1, 10, 3, 2, 1, 1.5]
k7 = fit(r7, np.array([0, 0, 0, .3, 1, .5, 0, 0, 0.]), LO7, HI7, 'R7')
g7 = [r7(g, k7) for g in GS]; grade('R7 global, surface-density coupling', g7, '(9 knobs)')
def r8(bw, bm, tag):
    out, P = [], []
    for g in GS:
        M0 = m200_of(g.Ms); c0 = float(cflat(M0, 0, 0)); lo = [np.log10(M0) - bm, np.log10(c0) - bw, -1, 0]; hi = [np.log10(M0) + bm, np.log10(c0) + bw, 1, 1]
        fn = lambda v: np.log10(halo(g, 10**v[0], 10**v[1], v[2], v[3])) - np.log10(g.gl); best = None
        for st in ((.0, .0, .3, .3), (.2 * bm, -.5 * bw, -.3, .7), (-.2 * bm, .5 * bw, .7, .1)):
            x = np.clip([np.log10(M0) + st[0], np.log10(c0) + st[1], st[2], st[3]], np.array(lo) + 1e-4, np.array(hi) - 1e-4)
            r_ = least_squares(fn, x, bounds=(lo, hi), max_nfev=40, diff_step=.01)
            if best is None or r_.cost < best.cost: best = r_
        out.append(halo(g, 10**best.x[0], 10**best.x[1], best.x[2], best.x[3])); P.append([best.x[0] - np.log10(M0), best.x[1] - np.log10(c0), best.x[2], best.x[3]])
    P = np.array(P); grade(tag, out, f'({4 * len(GS)} parameters)')
    print(' median, p16, p84 of dlogM200, dlog c, f, n:', np.round(np.percentile(P, [50, 16, 84], axis=0), 2).tolist()); return out
r8(1.5, 2., 'R8 per galaxy, wide'); r8(.11, .3, 'R8p per galaxy, referee priors')
# J: cosmology and redshift on R7
def setcos(C, z=0):
    cc.setCurrent(C); h = C.h; lib.CG = np.array([float(CM.concentration(10**m * h, '200c', z, model='diemer19')) for m in LM]); lib.RHOC = C.rho_c(z) * h**2 * Msun / kpc**3
    return C.Ode0 * C.rho_c(0) * h**2 * Msun / kpc**3
def afit(k, cmul): return fit_a(ALLB, np.concatenate([r7(g, k, cmul) for g in GS]))
u, d, dl = rt.cosmo_case('rde'); wb = .0493 * .674**2
CU, CD = rt.setc(**u)[0], rt.setc(**d)[0]; C0 = rt.setc()[0]
KS = [rt.setc(H0=67.4, OL=.70, wb=wb)[0], rt.setc(H0=73., OL=.685, wb=wb)[0], rt.setc(H0=73., OL=.65, wb=wb)[0]]
BAND = {1.: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
def sl_of(p):
    v = []
    for C in (CU, CD):
        R = setcos(C); v.append(afit(k7, (R / R0)**p))
    return np.log(v[0] / v[1]) / dl
R0 = setcos(C0); a00 = afit(k7, 1.); print(f'\nJ: R7 a at base {a00:.3e}')
s0 = sl_of(0.); print(f' E4 no hand term: rho_DE slope {s0:+.3f} [{"PASS" if abs(s0 - .5) <= .05 else "FAIL"}]')
try: p = brentq(lambda q: sl_of(q) - .5, -1, 3, xtol=.01); print(f' hand exponent p = {p:.2f}: slope {sl_of(p):+.3f}')
except ValueError: p = None; print(' no p in [-1,3] gives 0.5:', sl_of(-1), sl_of(3))
UNIT = lambda R: 2.998e8 * np.sqrt(G * R)
for C in KS:
    R = setcos(C)
    print(f' kappa at (OL {C.Ode0:.3f}, H0 {C.H0:.1f}): no hand {afit(k7, 1.) / UNIT(R):.3f}; with p {afit(k7, (R / R0)**(p or 0)) / UNIT(R):.3f}')
setcos(C0); zs = {}; 
for z in BAND:
    setcos(C0, z); zs[z] = afit(k7, 1.) / a00
print(' a(z)/a(0), no hand:', {z: round(float(v), 3) for z, v in zs.items()}, 'E5', all(BAND[z][0] <= v <= BAND[z][1] for z, v in zs.items()))
def zerr(q):
    t = 0
    for z in BAND: setcos(C0, z); t += np.log(afit(k7, (1 + z)**q) / a00 / {1.: .91, 1.5: .94, 2.33: .91}[z])**2
    return t
q = minimize_scalar(zerr, bounds=(-3, 2), method='bounded', options=dict(xatol=.01, maxiter=14)).x; z2 = {}
for z in BAND: setcos(C0, z); z2[z] = afit(k7, (1 + z)**q) / a00
print(f' hand exponent q = {q:.2f}; a(z)/a(0):', {z: round(float(v), 3) for z, v in z2.items()}, 'E5', all(BAND[z][0] <= v <= BAND[z][1] for z, v in z2.items()))
# C3 control
def edd(rr, rho, g):
    x = np.log(rr); dx = x[1] - x[0]; psi = np.cumsum((g * rr)[::-1])[::-1] * dx; P = psi[::-1]; R = rho[::-1]; E = np.linspace(P[3], P[-1], 240); dR = np.diff(R) / np.maximum(np.diff(P), 1e-30); I = np.empty(240)
    for j, e in enumerate(E): I[j] = (dR * 2 * (np.sqrt(np.maximum(e - P[:-1], 0)) - np.sqrt(np.maximum(e - P[1:], 0)))).sum()
    f = np.gradient(I, E); return f.min() / f.max()
rr = np.logspace(-3, 4, 500)
print(f'\nC3 control, min f/max f: Hernquist self-consistent {edd(rr, 1 / (rr * (1 + rr)**3), (rr / (1 + rr))**2 / rr**2):+.4f}; cored tracer in point mass {edd(rr, 1 / (1 + rr**2)**2.5, 1 / rr**2):+.4f}')
print('\nRival language; every knob disclosed. kappa = 1/2 FITTED; not theory closed.')
