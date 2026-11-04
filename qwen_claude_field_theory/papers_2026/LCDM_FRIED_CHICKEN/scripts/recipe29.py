"""A27: exhaustive dimensional search for a = kappa c sqrt(G rho_DE) from LCDM quantities, per ../FROZEN_A27.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import numpy as np, itertools, warnings
from fractions import Fraction as Fr
from colossus.cosmology import cosmology as cc
from colossus.lss import peaks
from colossus.halo import concentration as CM
warnings.filterwarnings('ignore')
G, kpc, Msun, c_ = 6.674e-11, 3.0857e19, 1.989e30, 2.998e8
SB, TCMB = 5.670374e-8, 2.7255
H0b, OMb, OBb, S8b, NS = 67.4, .315, .0493, .811, .965
ZS = (1.0, 1.5, 2.33); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
NAMES = ['H0', 'Lambda', 'rho_L', 'rho_m0', 'rho_b0', 'rho_c0', 'rho_g0', 't_age', 'L_H', 'M_*', 'V_*', 'g_*', 'f_b', 'sigma8', 'n_s']
DIMS = np.array([(0, -1, 0), (-2, 0, 0), (-3, 0, 1), (-3, 0, 1), (-3, 0, 1), (-3, 0, 1), (-3, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, 1), (1, -1, 0), (1, -2, 0),
                 (0, 0, 0), (0, 0, 0), (0, 0, 0)], float)  # (L, T, M)
EXPS = [-2, -1.5, -1, -.5, .5, 1, 1.5, 2]
PREF = {'1': 1., '2': 2., '1/2': .5, 'pi': np.pi, '2pi': 2 * np.pi, '1/2pi': 1 / (2 * np.pi), '4pi': 4 * np.pi, '1/4pi': 1 / (4 * np.pi),
        '6': 6., '1/6': 1 / 6, 'sqrt3': 3**.5, '1/sqrt3': 3**-.5}
n_cos = [0]
def mk(h, om, ob, s8):
    n_cos[0] += 1; return cc.setCosmology(f'a27_{n_cos[0]}', dict(flat=True, H0=100 * h, Om0=om, Ob0=ob, sigma8=s8, ns=NS, relspecies=False))
def ingredients(C, z=0.):
    """ln of each ingredient in SI (kg, m, s); C must be the current colossus cosmology."""
    rc = C.rho_c(z) * C.h**2 * Msun / kpc**3; H = C.Hz(z) * 1e3 / (kpc * 1e3)
    rL = C.Ode0 * C.rho_c(0) * C.h**2 * Msun / kpc**3
    Ms = peaks.nonLinearMass(z) / C.h * Msun; R = (3 * Ms / (800 * np.pi * rc))**(1 / 3)
    v = dict(H0=H, Lambda=8 * np.pi * G * rL / c_**2, rho_L=rL, rho_m0=C.Om0 * C.rho_c(0) * C.h**2 * Msun / kpc**3 * (1 + z)**3,
             rho_b0=C.Ob0 * C.rho_c(0) * C.h**2 * Msun / kpc**3 * (1 + z)**3, rho_c0=rc, rho_g0=4 * SB * TCMB**4 / c_**3 * (1 + z)**4,
             t_age=C.age(z) * 3.15576e16, L_H=c_ / H, **{'M_*': Ms, 'V_*': np.sqrt(G * Ms / R), 'g_*': G * Ms / R**2},
             f_b=C.Ob0 / C.Om0, sigma8=C.sigma8 * C.growthFactor(z), n_s=NS)
    return np.log(np.array([v[k] for k in NAMES])), rL, Ms
# ---- base, redshifts
h0 = H0b / 100; C0 = mk(h0, OMb, OBb, S8b); L0, RDE0, MS0 = ingredients(C0)
LZ = {z: ingredients(C0, z)[0] for z in ZS}
aT = .5 * c_ * np.sqrt(G * RDE0); A0 = 9.3625e-11
print(f'base: rho_DE {RDE0:.4e} kg/m^3, c sqrt(G rho_DE) {aT / .5:.4e}, target a_T {aT:.4e} (lib A0 {A0:.4e}); M_* {MS0 / Msun:.3e} Msun (log {np.log10(MS0 / Msun):.2f})')
print(' ingredient values today:', '; '.join(f'{k} {np.exp(x):.3e}' for k, x in zip(NAMES, L0)))
print(' M_*(z)/M_*(0):', ', '.join(f'z {z}: {np.exp(LZ[z][9] - L0[9]):.2e}' for z in ZS), '; sigma8 D(z):', ', '.join(f'{np.exp(LZ[z][13]):.3f}' for z in ZS))
# ---- G2 cosmologies: rho_DE x f at fixed omega_m, omega_b
wm, wb, wl = OMb * h0**2, OBb * h0**2, (1 - OMb) * h0**2
Rp = 8. / h0  # Mpc physical
mk(h0, OMb, OBb, S8b); s_ref = cc.getCurrent().sigma(Rp * h0, z=30.)
LF = {}
for f in (.8, 1.25):
    h1 = np.sqrt(wm + f * wl); om1, ob1 = wm / h1**2, wb / h1**2
    CA = mk(h1, om1, ob1, S8b); LA, rA, _ = ingredients(CA)
    s1 = CA.sigma(Rp * h1, z=30.); s8B = S8b * s_ref / s1
    CB = mk(h1, om1, ob1, s8B); LB, rB, _ = ingredients(CB); chk = CB.sigma(Rp * h1, z=30.) / s_ref
    LF[f] = (LA, LB, np.log(rA / RDE0))
    print(f'G2 cosmology f {f}: h {h1:.4f}, Om0 {om1:.4f}, rho_DE ratio {rA / RDE0:.4f}; footing B sigma8 {s8B:.4f} (z30 match {chk:.5f}); M_* A {np.exp(LA[9]) / Msun:.3e}, B {np.exp(LB[9]) / Msun:.3e}')
# ---- enumerate
rows_set, rows_exp = [], []
for k in (1, 2, 3):
    for S in itertools.combinations(range(15), k):
        for E in itertools.product(EXPS, repeat=k):
            rows_set.append(S + (-1,) * (3 - k)); rows_exp.append(E + (0.,) * (3 - k))
RS, RE = np.array(rows_set), np.array(rows_exp)
EM = np.zeros((len(RS), 15))
for j in range(3):
    m = RS[:, j] >= 0; EM[np.where(m)[0], RS[m, j]] = RE[m, j]
D = EM @ DIMS; valid = np.abs(D.sum(1) + 1) < 1e-9
print(f'\nenumeration: {len(RS)} ingredient-exponent products, {valid.sum()} dimensionally valid ({len(RS) - valid.sum()} rejected)')
EM, RS, RE, D = EM[valid], RS[valid], RE[valid], D[valid]
q = D[:, 2]; p = 1 - 3 * q - D[:, 0]
assert np.allclose(-p - 2 * q + D[:, 1], -2)
base = p * np.log(c_) + q * np.log(G) + EM @ L0          # ln a without prefactor
sl = {f: [(EM @ (LF[f][i] - L0)) / LF[f][2] for i in (0, 1)] for f in LF}  # footing A, B slopes
g2A = np.all([np.abs(sl[f][0] - .5) <= .05 for f in LF], 0); g2B = np.all([np.abs(sl[f][1] - .5) <= .05 for f in LF], 0)
zr = {z: np.exp(EM @ (LZ[z] - L0)) for z in ZS}; g3 = np.all([(zr[z] >= ZB[z][0]) & (zr[z] <= ZB[z][1]) for z in ZS], 0)
print(f'products (no prefactor): G2 footing A pass {g2A.sum()}, footing B pass {g2B.sum()}, G3 pass {g3.sum()}, G2B+G3 {(g2B & g3).sum()}')
def label(i, pk):
    t = [f'{NAMES[RS[i, j]]}^{Fr(RE[i, j]).limit_denominator(2)}' for j in range(3) if RS[i, j] >= 0]
    return f'{pk} c^{Fr(p[i]).limit_denominator(4)} G^{Fr(q[i]).limit_denominator(4)} ' + ' '.join(t)
def G5(i):
    r = 10 * kpc; best, why = 0., []
    ing = {NAMES[RS[i, j]] for j in range(3) if RS[i, j] >= 0}
    X = dict(zip(NAMES, np.exp(L0))); q0 = .5 * C0.Om0 - C0.Ode0
    for n in ing:
        if n in ('Lambda', 'rho_L'): v = X['Lambda'] * c_**2 * r / 3
        elif n in ('H0', 't_age', 'L_H'): v = abs(q0) * X['H0']**2 * r
        elif n in ('rho_m0', 'rho_b0', 'rho_c0', 'rho_g0'): v = 4 * np.pi * G / 3 * X[n] * r
        elif n in ('M_*', 'V_*', 'g_*'):
            lm = np.log10(MS0 / Msun)
            if 11 <= lm <= 12.5:
                rc = C0.rho_c(0) * C0.h**2 * Msun / kpc**3; R = (3 * MS0 / (800 * np.pi * rc))**(1 / 3); cv = float(CM.concentration(MS0 / Msun * C0.h, '200c', 0, model='diemer19'))
                mu = lambda x: np.log(1 + x) - x / (1 + x); v = G * MS0 * mu(r / (R / cv)) / mu(cv) / r**2
            else: v = 0.
        else: continue
        why.append(f'{n} {v / aT:.1e} a_T'); best = max(best, v)
    return best >= .1 * aT, ', '.join(why)
def run(prefs, tag, show):
    vals = np.log10(np.exp(base))[:, None] + np.log10(np.array(list(prefs.values())))[None, :] - np.log10(aT)  # dex from target
    N = vals.size; g1 = np.abs(vals) <= .05; full = g1 & (g2B & g3)[:, None]; fullA = g1 & (g2A & g3)[:, None]
    uv = np.unique(np.round(vals, 4)); uf = np.unique(np.round(vals[(g2B & g3)], 4))
    fam = np.unique(np.round(np.c_[sl[.8][0], sl[1.25][0], sl[.8][1], sl[1.25][1], np.log(zr[1.0]), np.log(zr[1.5]), np.log(zr[2.33])], 4), axis=0)
    print(f'\n==== {tag}: {len(prefs)} prefactors; N_expr {N}, N_val {len(uv)} distinct values, {len(fam)} functional families; log10(a/a_T) spans {vals.min():+.1f} to {vals.max():+.1f}, '
          f'{(np.abs(vals) <= 1.5).sum()} expr within 1.5 dex')
    K1e, K1v = g1.sum(), (np.abs(uv) <= .05).sum(); K3e, K3v = full.sum(), (np.abs(uf) <= .05).sum()
    print(f' G1 hits: {K1e} expressions, {K1v} distinct values; G1+G2(B)+G3 full: {K3e} expressions, {K3v} distinct values; G1+G2(A)+G3: {fullA.sum()} expressions')
    ds = np.round(np.arange(-1.5, 1.5001, .01), 2); ds = ds[np.abs(ds) >= .1]
    c1 = np.array([(np.abs(uv - d) <= .05).sum() for d in ds]); c3 = np.array([(np.abs(uf - d) <= .05).sum() for d in ds])
    from scipy.stats import poisson
    # FIX after first run (disclosed): 1e-4 dex rounding caps distinct values in a 0.1 dex window at 1001, so the frozen
    # distinct counts saturate; add the same slide on 1e-7 dex distinct values and on raw expression counts.
    uv7 = np.unique(np.round(vals, 7)); uf7 = np.unique(np.round(vals[(g2B & g3)], 7)); ve = np.sort(vals.ravel()); vf = np.sort(vals[(g2B & g3)].ravel())
    cnt_in = lambda a, d: np.searchsorted(a, d + .05, 'right') - np.searchsorted(a, d - .05, 'left')
    c1_7 = np.array([cnt_in(uv7, d) for d in ds]); c3_7 = np.array([cnt_in(uf7, d) for d in ds])
    c1_e = np.array([cnt_in(ve, d) for d in ds]); c3_e = np.array([cnt_in(vf, d) for d in ds])
    K1_7, K3_7 = cnt_in(uv7, 0.), cnt_in(uf7, 0.)
    print(f' distinct values at 1e-7 dex: N_val {len(uv7)}; G1 {K1_7}, full {K3_7}')
    for nm, cnt, K in (('G1', c1, K1v), ('G1+G2B+G3', c3, K3v), ('G1 [1e-7 distinct]', c1_7, K1_7), ('G1+G2B+G3 [1e-7 distinct]', c3_7, K3_7),
                       ('G1 [expressions]', c1_e, K1e), ('G1+G2B+G3 [expressions]', c3_e, K3e)):
        mu = cnt.mean(); print(f' slid target ({len(ds)} offsets): {nm} chance hits mean {mu:.1f}, 16-84% {np.percentile(cnt, 16):.0f}-{np.percentile(cnt, 84):.0f}, max {cnt.max()}; observed {K}; '
                              f'Poisson P(N>={K}) {poisson.sf(K - 1, mu) if mu > 0 else (0. if K else 1.):.3g}; fraction of offsets with >= observed {np.mean(cnt >= K):.3f} '
                              f'-> {"WITHIN CHANCE (numerology)" if (K <= np.percentile(cnt, 84) or (mu > 0 and poisson.sf(K - 1, mu) > .01)) else "BEYOND CHANCE"}')
    if show:
        gi = np.argwhere(g1); print(f' G1 hits by gate status (expressions): G2B pass {(g2B[gi[:, 0]]).sum()}, G3 pass {(g3[gi[:, 0]]).sum()}, both {full.sum()}')
        fi = np.argwhere(full); pk = list(prefs.keys()); nonL = 0
        print(f'\n full survivors (G1 + G2 footing B + G3), {len(fi)}; G4 passes by construction (mass-free):')
        for i, j in sorted(fi.tolist(), key=lambda x: abs(vals[x[0], x[1]])):
            ok5, why = G5(i); ings = {NAMES[RS[i, k]] for k in range(3) if RS[i, k] >= 0}; isL = bool(ings & {'Lambda', 'rho_L'}); nonL += not isL
            print(f'  {label(i, pk[j]):58s} kappa_eff {.5 * 10**vals[i, j]:.4f} ({vals[i, j]:+.4f} dex); slopes B {sl[.8][1][i]:+.4f} {sl[1.25][1][i]:+.4f}, A {sl[.8][0][i]:+.3f} {sl[1.25][0][i]:+.3f}; '
                  f'a(z)/a0 {zr[1.0][i]:.3f} {zr[1.5][i]:.3f} {zr[2.33][i]:.3f}; G5 {"PASS" if ok5 else "FAIL"} [{why}]{"" if isL else "  <-- NON-LAMBDA SURVIVOR"}')
        print(f' non-Lambda full survivors: {nonL}')
        # near misses: G1 hits failing only one of G2B / G3, by ingredient class
        nm = np.argwhere(g1 & ~(g2B & g3)[:, None]); cls = {}
        for i, j in nm.tolist():
            ings = {NAMES[RS[i, k]] for k in range(3) if RS[i, k] >= 0 and NAMES[RS[i, k]] not in ('f_b', 'sigma8', 'n_s')}
            key = '+'.join(sorted(ings)) or 'dimensionless only'; why = ('G2B ' if not g2B[i] else '') + ('G3' if not g3[i] else '')
            cls.setdefault(key, [0, set()]); cls[key][0] += 1; cls[key][1].add(why.strip())
        print(' G1 hits failing G2B and/or G3, by dimensional ingredient set (count; failing gates):')
        for k_, (n_, w_) in sorted(cls.items(), key=lambda x: -x[1][0])[:25]: print(f'  {k_:32s} {n_:5d}  {sorted(w_)}')
        print(f'  ... {len(cls)} ingredient sets in all')
        # G2A-only survivors (footing A full but not B)
        dA = np.argwhere(fullA & ~full)
        print(f' full on footing A but not B: {len(dA)}', '; '.join(label(i, pk[j]) for i, j in dA.tolist()[:8]))
run(PREF, 'PRIMARY, single prefactor', True)
P2 = {}
for (a, x), (b, y) in itertools.combinations_with_replacement(PREF.items(), 2):
    v = round(x * y, 12)
    if v not in P2.values(): P2[f'{a}*{b}'] = v
run(P2, 'SENSITIVITY, two-element prefactor products', False)
mil = np.where((RS[:, 0] == 1) & (RS[:, 1] < 0) & (RE[:, 0] == .5))[0][0]
print(f'\ncheck: Milgrom c^2 sqrt(Lambda/3)/2pi = kappa_eff {np.exp(base[mil]) / np.sqrt(3) / (2 * np.pi) / (2 * aT):.4f} (A13: 0.461); tie (1/2) c sqrt(G rho_L) kappa_eff '
      f'{.5 * np.exp(base[np.where((RS[:, 0] == 2) & (RS[:, 1] < 0) & (RE[:, 0] == .5))[0][0]]) / (2 * aT):.4f}')
# ---- verification of the non-Lambda full-survivor families (diagnostic, added after the first run; gates unchanged)
print('\nverify non-Lambda families by direct colossus calls (diagnostic):')
mk(h0, OMb, OBb, S8b); Cv = cc.getCurrent(); Hb = Cv.Hz(0)
for z in (.5, 1., 1.5, 2., 2.33, 3., 4.):
    Hr, Dz, tr = Cv.Hz(z) / Hb, Cv.growthFactor(z), Cv.age(z) / Cv.age(0)
    print(f'  z {z}: F1 = H D^1.5 / H0 = {Hr * Dz**1.5:.4f}; F2 = H^1.5 t^0.5 D / (same at 0) = {Hr**1.5 * tr**.5 * Dz:.4f}; plain H/H0 {Hr:.4f}')
for f in (.64, .8, .9, 1.1, 1.25, 1.5625):
    h1 = np.sqrt(wm + f * wl); om1, ob1 = wm / h1**2, wb / h1**2; CA = mk(h1, om1, ob1, S8b); s1 = CA.sigma(Rp * h1, z=30.); s8B = S8b * s_ref / s1
    CB = mk(h1, om1, ob1, s8B); lf = np.log(f)
    F1 = np.log(h1 / h0) + 1.5 * np.log(s8B / S8b); F2 = 1.5 * np.log(h1 / h0) + .5 * np.log(CB.age(0) / Cv.age(0)) + np.log(s8B / S8b)
    print(f'  rho_DE x {f}: sigma8_B {s8B:.4f}; slope B: H0 alone {np.log(h1 / h0) / lf:.4f}, F1 {F1 / lf:.4f}, F2 {F2 / lf:.4f}; footing A F1 {np.log(h1 / h0) / lf:.4f}')
    mk(h0, OMb, OBb, S8b); Cv = cc.getCurrent()
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
