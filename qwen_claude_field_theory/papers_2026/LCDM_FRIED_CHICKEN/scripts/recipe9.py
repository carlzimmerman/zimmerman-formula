"""Amendment A7 of ../FROZEN_RECIPE.md: particle reading of the formula-exact halo: mixing theorem, energy, scattering. Spherical, isotropic. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
def DF(x, rr, rho, gt):
    dx = x[1] - x[0]; psi = np.cumsum((gt * rr)[::-1])[::-1] * dx; P, R = psi[::-1], rho[::-1]; E = np.logspace(np.log10(P[3]), np.log10(P[-1]), 200); dR = np.diff(R) / np.maximum(np.diff(P), 1e-30); I = np.empty(len(E)); gE = np.empty(len(E))
    for j, e in enumerate(E):
        a, b = np.sqrt(np.maximum(e - P[:-1], 0)), np.sqrt(np.maximum(e - P[1:], 0)); I[j] = (dR * 2 * (a - b)).sum(); gE[j] = 16 * np.pi**2 * (rr**3 * np.sqrt(2 * np.maximum(psi - e, 0))).sum() * dx
    f = np.maximum(np.gradient(I, E) / (np.sqrt(8) * np.pi**2), 0); return E, f, gE, psi
def Dx(f0, E, f, gE): return np.array([np.trapezoid(np.maximum(f - a, 0) * gE, E) for a in f0])
def nfw_prof(rr, x, R200, Md, Mt, c):
    rs = R200 / c; mu_ = lambda y: np.log(1 + y) - y / (1 + y); m = mu(rr / rs) / mu(c); rho = Md * Msun / mu(c) / (4 * np.pi * rr * (rr + rs)**2); return rho * np.exp(-(rr / (2 * R200))**2), G * Mt * Msun * m / rr**2
def setup(g):
    x = np.linspace(np.log(g.r[0]) - 3, np.log(g.r[-1]) + 5, 500); lr = np.log(g.r); rr = np.exp(x); lg = np.interp(x, lr, np.log(g.gb)); h = x < lr[0]; lg[h] = np.log(g.gb[0]) + (x[h] - lr[0]); t = x > lr[-1]; lg[t] = np.log(G * max(g.mbtot, g.mb[-1]) / rr[t]**2); lg = gaussian_filter1d(lg, .1 * np.log(10) / (x[1] - x[0]))
    gb = np.exp(lg); gl = law(gb); md = rr**2 * (gl - gb) / G; mt = rr**2 * gl / G; rho = np.maximum(np.gradient(md, x) / (4 * np.pi * rr**3), 1e-40); i = np.argmax(mt / (4 / 3 * np.pi * rr**3) < 200 * RHOC)
    return x, rr, gb, gl, md, rho, rr[i], mt[i] / Msun, md[i] / Msun, i
def ratio(fin, ini, f0): return np.max(Dx(f0, *fin[:3]) / np.maximum(Dx(f0, *ini[:3]), 1e-300))
def grid(fin, rr, r1, r2):
    psi = fin[3]; E, f = fin[0], fin[1]; e1, e2 = np.interp(np.log(r1), np.log(rr), psi), np.interp(np.log(r2), np.log(rr), psi); w = (E >= min(e1, e2)) & (E <= max(e1, e2)) & (f > 0)
    return np.logspace(np.log10(f[w].min()), np.log10(f[w].max()), 30)[:-1] if w.sum() > 3 else None
print('Controls on 12 galaxies, NFW final against NFW initial')
ct = {'same': [], 'c x4': [], 'c /4': []}
for g in GS[::14]:
    x, rr, gb, gl, md, rho, R, Mt, Md, i = setup(g); c = float(cflat(Mt, 0, 0)); ini = DF(x, rr, *nfw_prof(rr, x, R, Md, Mt, c))
    for k, m in (('same', 1), ('c x4', 4), ('c /4', .25)):
        fin = DF(x, rr, *nfw_prof(rr, x, R, Md, Mt, c * m)); f0 = grid(ini, rr, g.r[0], g.r[-1]); ct[k].append(ratio(fin, ini, f0))
for k, v in ct.items(): print(f' {k}: median worst ratio {np.median(v):.3f}, max {np.max(v):.3f}, allowed {(np.array(v) <= 1.05).sum()} of {len(v)}')
ROWS = {'c Diemer19': 0, 'c -0.22 dex': -.22, 'c +0.22 dex': .22}; W = {k: [] for k in ROWS}; MB = []; E2, S1, S2 = [], [], []; SK = 0
for g in GS:
    x, rr, gb, gl, md, rho, R, Mt, Md, i = setup(g); rt = rho * np.exp(-(rr / (2 * R))**2); fin = DF(x, rr, rt, gl); f0 = grid(fin, rr, g.r[0], g.r[-1])
    if f0 is None: SK += 1; continue
    MB.append(g.Mb); c = float(cflat(Mt, 0, 0))
    for k, d in ROWS.items(): W[k].append(ratio(fin, DF(x, rr, *nfw_prof(rr, x, R, Md, Mt, c * 10**d)), f0))
    w = rr <= R; dU = lambda m: -(G * m[w][:-1] * np.diff(m[w]) / rr[w][1:]).sum(); rs = R / c; mi = Md * Msun * mu(rr / rs) / mu(c); Ef, Ei = dU(md), dU(mi); E2.append((Ef - Ei) * 1e7 / (g.Ms * 1e49))
    rb = np.maximum(np.gradient(rr**2 * gb / G, x) / (4 * np.pi * rr**3), 1e-40); v = np.sqrt(gl * rr); T = 13 * 3.156e16; j = np.argmin(abs(gb - A0)); k = np.argmin(abs(rr - g.r[-1])); S1.append(10 / (rb[j] * v[j] * T)); S2.append(10 / (rb[k] * v[k] * T))
print(f'\nM1 mixing theorem, {len(MB)} galaxies graded, {SK} with no positive f range')
lM = np.log10(MB)
for k, v in W.items():
    v = np.array(v); print(f' {k}: allowed {(v <= 1.05).sum()} of {len(v)}; worst ratio p50 {np.median(v):.2f}, p84 {np.percentile(v, 84):.2f}, max {v.max():.2f}; by log M_b <9, 9-10, 10-11, >=11 allowed ' + ' '.join(f'{(v[(lM >= a) & (lM < b)] <= 1.05).sum()}/{((lM >= a) & (lM < b)).sum()}' for a, b in ((0, 9), (9, 10), (10, 11), (11, 14))))
E2 = np.array(E2); print(f'\nM2 energy, R12 minus NFW, in units of all SN energy: needs heating in {(E2 > 0).sum()} of {len(E2)}, median among those {np.median(E2[E2 > 0]):.3f}, p84 {np.percentile(E2[E2 > 0], 84):.3f}, above 1 in {(E2 > 1).sum()}; more bound in {(E2 < 0).sum()}, median {np.median(E2[E2 < 0]) if (E2 < 0).any() else 0:.3f}')
print(f'\nM3 sigma/m for one exchange in 13 Gyr, cm^2/g, p16, p50, p84: at g_b = a0 {np.round(np.percentile(S1, [16, 50, 84]), 3).tolist()}; at last point {np.round(np.percentile(S2, [16, 50, 84]), 3).tolist()}')
print('Necessary conditions only; isotropy assumed. Not a detection. kappa = 1/2 FITTED; not theory closed.')
