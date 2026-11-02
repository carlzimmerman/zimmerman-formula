"""Knob tuning per ../FROZEN_TUNING.md. Hypothetical rival, not a framework result. kappa = 1/2 FITTED; not theory closed."""
from lib import *
from scipy.optimize import least_squares
MS = 10**np.linspace(10, 12.7, 8)
NAMES = ['c_norm', 'c_slope', 'shmr_norm', 'logM1', 'beta', 'gamma', 'contract', 'size_norm', 'size_slope', 'gas_norm', 'gas_slope']
BASE_K = np.zeros(11); BASE_K[6] = 1.  # base: Blumenthal, all shifts zero
T1 = np.array([.11, .05, .18, .3, .4, .2, 0, .2, .2, .3, .2])
def bounds(mult, lo_c, hi_c):
    w = T1 * mult; lo, hi = -w.copy(), w.copy(); lo[6], hi[6] = lo_c, hi_c; return lo, hi
class Cos:
    def __init__(s, cos, z=0):
        s.cos, s.z = cos, z; s.c = np.array([float(CM.concentration(M * cos.h, '200c', z, model='diemer19')) for M in MS])
        s.rde = cos.Ode0 * cos.rho_c(0) * cos.h**2 * Msun / kpc**3
def gal(C, i, k, cmul=1.):
    M = MS[i]; dc, sc, dn, dm1, db, dg, f, sn, ss, gn, gs = k
    cv = C.c[i] * 10**dc * (M / 1e12)**sc * cmul
    h = H(C.cos, M, C.z, conc=cv)
    Ms = smhm(M, N=.0351 * 10**dn, lM1=11.59 + dm1, b=1.376 + db, g=.608 + dg)
    Mg = Ms * 10**gn * (Ms / 10**9.5)**(-.55 + gs); Mb = (Ms + Mg) * Msun; fb = min((Ms + Mg) / M, .5)
    Rd = .0089 * 10**sn * (M / 1e12)**ss * h.R
    rd = np.logspace(np.log10(h.R * 1e-4), np.log10(h.R * 1.2), 300)
    m0 = (1 - fb) * h.m(rd)
    _, m1 = contract(h, Mb, Rd, 'blumenthal', fb)
    m = np.maximum((1 - f) * m0 + f * m1, 1e-3 * m0)
    r = np.logspace(np.log10(.5 * Rd), np.log10(5 * Rd), 12)
    gb = np.maximum(disc_v2(r, Mb, Rd), 1e-30) / r
    return r, gb, gb + G * np.interp(r, rd, m) / r**2, Rd, Mb, h
def res(k, C, cmul=1.):
    out = []
    for i in range(len(MS)):
        _, gb, gt, *_ = gal(C, i, k, cmul); out += list(np.log10(gt) - np.log10(law_g(gb)))
    return np.array(out)
def stack_a(k, C, cmul=1.):
    GB, GT = [], []
    for i in range(len(MS)):
        _, gb, gt, *_ = gal(C, i, k, cmul); GB += list(gb); GT += list(gt)
    return fit_a(np.array(GB), np.array(GT))
def permass(k, C, cmul=1.):
    return np.array([fit_a(*gal(C, i, k, cmul)[1:3]) for i in range(len(MS))])
base = Cos(setc()[0])
def mk(**kw): return Cos(setc(**kw)[0])
u, d, dl = cosmo_case('rde'); CU, CD = mk(**u), mk(**d)
wb = .0493 * .674**2
CK = {(.70, 67.4): mk(H0=67.4, OL=.70, wb=wb), (.685, 73.): mk(H0=73., OL=.685, wb=wb), (.65, 73.): mk(H0=73., OL=.65, wb=wb)}
CZ = {1.: Cos(base.cos, 1.), 1.5: Cos(base.cos, 1.5), 2.33: Cos(base.cos, 2.33)}
BAND = {1.: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
UNIT = lambda C: c * np.sqrt(G * C.rde)
def report(tag, k, p=0.):
    mul = lambda C: (C.rde / base.rde)**p
    a0_ = stack_a(k, base); pm = permass(k, base); rms = res(k, base).std(); rmsz = np.sqrt((res(k, base)**2).mean())
    sl = np.log(stack_a(k, CU, mul(CU)) / stack_a(k, CD, mul(CD))) / dl
    ks = {kk: stack_a(k, C, mul(C)) / UNIT(C) for kk, C in CK.items()}
    zs = {z: stack_a(k, C) / a0_ for z, C in CZ.items()}
    P = dict(T1=abs(a0_ / A0 - 1) <= .01, T2=np.log10(pm.max() / pm.min()) <= .05, T3=rmsz <= .02, T4=abs(sl - .5) <= .05,
             T5=all(abs(v / .5 - 1) <= .05 for v in ks.values()), T6=all(BAND[z][0] <= v <= BAND[z][1] for z, v in zs.items()))
    print(f'\n== {tag}'); print(f'a {a0_:.4e} ratio {a0_/A0:.4f}; per-mass spread {np.log10(pm.max()/pm.min()):.3f} dex; rms to law {rmsz:.4f} dex')
    print('per-mass a', ' '.join(f'{x:.2e}' for x in pm)); print(f'rho_DE slope {sl:+.3f}')
    print('kappa', {k_: round(float(v), 3) for k_, v in ks.items()}); print('a(z)/a(0)', {k_: round(float(v), 3) for k_, v in zs.items()})
    print('verdict', ' '.join(f"{n}:{'PASS' if v else 'FAIL'}" for n, v in P.items()))
    return a0_
def tune(tag, lo, hi):
    best = None
    for s in range(3):
        x0 = np.clip(np.random.default_rng(s).uniform(lo, hi) if s else np.clip(BASE_K, lo, hi), lo + 1e-6, hi - 1e-6)
        r = least_squares(res, x0, args=(base,), bounds=(lo, hi), max_nfev=30, diff_step=.02, xtol=1e-4, ftol=1e-4)
        if best is None or r.cost < best.cost: best = r
    print(f'\n{tag} knobs:', ' '.join(f'{n}={v:+.3f}{"*" if min(abs(v-a),abs(v-b))<1e-3*max(b-a,1e-9) else ""}' for n, v, a, b in zip(NAMES, best.x, lo, hi)), '(* at bound)')
    return best.x
report('BASE: no tuning, Blumenthal', BASE_K)
k1 = tune('TIER 1', *bounds(1, 0, 1)); report('TIER 1 plausible ranges', k1)
k2 = tune('TIER 2', *bounds(3, -1, 1)); report('TIER 2 ranges tripled', k2)
# Tier 3: explicit rho_DE dependence
def sl_p(p):
    mul = lambda C: (C.rde / base.rde)**p
    return np.log(stack_a(k2, CU, mul(CU)) / stack_a(k2, CD, mul(CD))) / dl - .5
try:
    p = brentq(sl_p, -2, 6, xtol=.01); print(f'\nTIER 3: c must scale as rho_DE^{p:.2f} at fixed omega_m, A_s'); report('TIER 3 with rho_DE exponent', k2, p)
except ValueError:
    p = None; print('\nTIER 3: no exponent in [-2,6] reaches slope 0.5', sl_p(-2) + .5, sl_p(6) + .5)
print('\nTIER 3b: c shift (dex) solved per cosmology and redshift, on Tier 2 knobs')
for kk, C in CK.items():
    t = .5 * UNIT(C)
    try: print(' cosmology', kk, f'{brentq(lambda s: np.log(stack_a(k2, C, 10**s) / t), -2, 2, xtol=.002):+.3f} dex')
    except ValueError: print(' cosmology', kk, 'no solution within +-2 dex')
a_b = stack_a(k2, base)
for z, C in CZ.items():
    t = a_b * {1.: .91, 1.5: .94, 2.33: .91}[z]
    try: print(' redshift', z, f'{brentq(lambda s: np.log(stack_a(k2, C, 10**s) / t), -2, 2, xtol=.002):+.3f} dex to band centre')
    except ValueError: print(' redshift', z, 'no solution within +-2 dex')
# Tier 4: free-form halo
print('\nTIER 4: free-form halo M_DM = r^2 (g_law - g_bar)/G, baseline baryons, no contraction')
for i in [0, 3, 5, 7]:
    k0 = BASE_K.copy(); k0[6] = 0.
    r, gb, gt, Rd, Mb, h = gal(base, i, k0)
    rr = np.logspace(np.log10(.05 * Rd), np.log10(h.R), 200)
    gbb = np.maximum(disc_v2(rr, Mb, Rd), 1e-30) / rr
    gdm = law_g(gbb) - gbb; md = rr**2 * gdm / G; rho = np.gradient(md, rr) / (4 * np.pi * rr**2)
    nf = (1 - min(Mb / Msun / MS[i], .5)) * h.m(rr); ix = (rr >= .5 * Rd) & (rr <= 5 * Rd)
    gam = -np.gradient(np.log(np.maximum(rho, 1e-60)), np.log(rr))
    print(f' logM {np.log10(MS[i]):.1f}: min rho>0 {bool((rho > 0).all())}; M_free/M_NFW at 0.5-5 Rd {(md/nf)[ix].min():.2f} to {(md/nf)[ix].max():.2f}; at R200 {md[-1]/nf[-1]:.2f}; rho slope at 2 Rd {np.interp(2*Rd, rr, gam):.2f}, at R200 {gam[-2]:.2f}')
print('\nHypothetical rival; every knob disclosed. kappa = 1/2 FITTED; not theory closed.')
