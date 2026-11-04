"""A15: galaxy-mass halo scale, observable-only gates, one-recipe SIDM core, per ../FROZEN_RECIPE.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.optimize import least_squares as LSQ
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
def hal(M, z=0):
    rc = cos.rho_c(z) * cos.h**2 * Msun / kpc**3; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3)
    c = float(CM.concentration(M * cos.h, '200c', z, model='diemer19')); rs = R / c; rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); return 2 * np.pi * G * rhos * rs, c, rs, rhos, R
print(f'base cosmology OL {cos.Ode0:.3f}: c sqrt(G rho_DE) {AC:.4e}, a0 {A0:.4e}')
M2 = np.array([m200_of(g.Ms) for g in GS]); gi = np.array([hal(M)[0] for M in M2]); lg = np.log10(gi)
h1 = lg.std() <= .1; ke = np.median(gi) / AC; h2 = abs(np.log10(ke / .5)) <= .05
print(f'\nU1: log M200 p5-p95 {np.percentile(np.log10(M2), 5):.2f}-{np.percentile(np.log10(M2), 95):.2f}; g_i median {np.median(gi) / A0:.3f} a0, rms {lg.std():.3f} dex [{"PASS" if h1 else "FAIL"} H1]; kappa_eff {ke:.3f} [{"PASS" if h2 else "FAIL"} H2]')
e = grade('U1 H3 swap, a = g_i per galaxy', [law(g.gb, a) for g, a in zip(GS, gi)])
f = 10**minimize_scalar(lambda x: ((np.log10(np.concatenate([law(g.gb, a * 10**x) for g, a in zip(GS, gi)])) - np.log10(ALLL))**2).sum(), bounds=(-1, 1), method='bounded').x
e2 = grade('U1 H3 swap with one global factor', [law(g.gb, a * f) for g, a in zip(GS, gi)], f'(factor {f:.3f}, one knob)')
Mm = np.median(M2); zr = {z: hal(Mm, z)[0] / hal(Mm)[0] for z in ZB}; h4 = all(ZB[z][0] <= zr[z] <= ZB[z][1] for z in ZB)
print(f'U1 H4 at median log M200 {np.log10(Mm):.2f}: ' + ', '.join(f'{z}: {x:.3f}' for z, x in zr.items()) + f' [{"PASS" if h4 else "FAIL"} H4]')
print('U1 verdict:', 'SUPPLIES THE TIE' if (h1 and h2 and e <= .02 and h4) else 'NO TIE')
k2 = .5 * np.sqrt(8 * np.pi / 3) / np.pi
print(f'\nU2 observable gates: T2 Lambda coincidence kappa_eff {k2:.3f} [{"PASS" if abs(np.log10(k2 / .5)) <= .05 else "FAIL"} G1], a(z)/a(0) = 1 [PASS G3], mass-free [PASS G4]: indistinguishable from the tie on observables; G5 alone separates.')
print(f'U2 observable gates: U1 G1 {"PASS" if h2 else "FAIL"}, G3 {"PASS" if h4 else "FAIL"}, G4 {"PASS" if h1 else "FAIL"}')
T = 10 * 3.156e16; RG = np.logspace(-3, 0, 120)
def sidm(g, M, sm):
    _, c, rs, rhos, R = hal(M); fb = min(g.Mb / M, .5); w = 1 - fb
    rN = lambda r: w * rhos / ((r / rs) * (1 + r / rs)**2); mN = lambda r: w * M * Msun * mu(r / rs) / mu(c)
    lr, lm = np.log(g.r), np.log(np.maximum(g.mb, 1e-30))
    def mb(r): return np.where(r < g.r[0], g.mb[0] * (r / g.r[0])**2, np.where(r > g.r[-1], g.mb[-1], np.exp(np.interp(np.log(r), lr, lm))))
    def prof(p, r1):
        rho0, s2 = np.exp(p[0]), np.exp(2 * p[1]); r = r1 * RG; dr = np.diff(r, prepend=0); rho = np.empty_like(r); m = 0.; lrho = np.log(rho0); B = mb(r)
        for i in range(len(r)):
            rho[i] = np.exp(lrho); m += 4 * np.pi * r[i]**2 * rho[i] * dr[i]
            if i + 1 < len(r): lrho -= G * (B[i] + m) / r[i]**2 / s2 * (r[i + 1] - r[i])
        return r, rho, np.cumsum(4 * np.pi * r**2 * rho * dr)
    r1 = rs; p = np.array([np.log(rN(rs)), np.log(np.sqrt(G * M * Msun / R))])
    for _ in range(5):
        sol = LSQ(lambda q: [np.log(prof(q, r1)[1][-1] / rN(r1)), np.log(prof(q, r1)[2][-1] / mN(r1))], p, max_nfev=30); p = sol.x; s0 = np.exp(p[1])
        r1 = brentq(lambda r: np.log(rN(r) * sm * 4 / np.sqrt(np.pi) * s0 * T), 1e-4 * rs, 50 * rs) if rN(1e-4 * rs) * sm * 4 / np.sqrt(np.pi) * s0 * T > 1 > rN(50 * rs) * sm * 4 / np.sqrt(np.pi) * s0 * T else 1e-4 * rs
    r, rho, m = prof(p, r1); md = np.where(g.r < r1, np.exp(np.interp(np.log(g.r), np.log(r), np.log(m))), mN(g.r))
    return g.gb + G * md / g.r**2, r1, sol.cost
for sm in (.5, 1., 3.):
    out = [sidm(g, M, sm * .1) for g, M in zip(GS, M2)]
    grade(f'U3 SIDM sigma/m {sm} cm^2/g', [o[0] for o in out], f'(median r1 {np.median([o[1] for o in out]) / kpc:.2f} kpc; matching cost > 1e-3 in {sum(o[2] > 1e-3 for o in out)} of {len(out)})')
print('\nNot run: hydrodynamic simulations, fuzzy dark matter, interacting vacuum, systematic reading.')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
