"""A34: analytic LCDM papers that claim the MOND scale (Kaplinghat & Turner 2002, van den Bosch & Dalcanton 2000,
Mo Mao White 1998 engine, Di Cintio & Lelli 2016, Desmond 2017, Salucci/Donato), per ../FROZEN_A34.md.
Analytic stand-ins, not the papers' codes. Rival language, adopts nothing, not a framework result.
kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
T0 = time.time(); CK = os.path.join(HERE, 'recipe35.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
c_ = 2.998e8; MPC = kpc * 1e3; ZS = [0., 1., 1.5, 2.33]; ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
h0 = .674; BASE = cos; RDE0 = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE0)
# reuse A29 background code (recipe31.py) and A18 DC14 code (recipe20.py) unchanged
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('# ---------- backgrounds'):s31.index('# ---------- scales')])
s20 = open(os.path.join(HERE, 'recipe20.py'), encoding='utf-8').read(); exec(s20[s20.index('def cum_mass'):s20.index('def g_dc14')])
P = lambda b: 'PASS' if b else 'FAIL'
FB = .0493 / .315; FKT = .0493 / (.315 - .0493); BETA = 5.; MD = .05
def slope(x, y): return float(np.polyfit(np.log(x), np.log(y), 1)[0])
def gt_dev(a, r): return {z: float(np.log10(a[z] / a[0.]) - .5 * np.log10(r[z] / r[0.])) for z in ZB}
M2 = np.array([m200_of(g.Ms) for g in GS]); LMH = np.arange(11, 12.51, .25); SEL = (np.log10(M2) >= 11) & (np.log10(M2) <= 12.5)
# ---------- halo pieces in an environment e (rhoc, cg, z, H, rde) ----------
def cof(e, M): return 10**np.interp(np.log10(M), LM, np.log10(e['cg']))
def R200(e, M): return (3 * M * Msun / (800 * np.pi * e['rhoc']))**(1 / 3)
def mnfw(r, M, c, e): R = R200(e, M); rs = R / c; return M * Msun * mu(r / rs) / mu(c)
def contract(g, M, c, e, fdm):
    ri = g.r.copy()
    for _ in range(25):
        mi = mnfw(ri, M, c, e); ri = .5 * ri + .5 * g.r * (g.mb + fdm * mi) / mi
    return fdm * mnfw(ri, M, c, e)
def mmw(g, e, md=MD): M = g.Mb / md; return g.gb + G * contract(g, M, cof(e, M), e, 1 - md) / g.r**2
def vdbd(g, e, dn=0.): M = m200_of(g.Ms) * 10**dn; fb = min(g.Mb / M, .5); return g.gb + G * contract(g, M, cof(e, M), e, 1 - fb) / g.r**2
def des(g, e, nu, dlm=0., dlc=0.):
    M = m200_of(g.Ms) * 10**dlm; c = cof(e, M) * 10**dlc; fb = min(g.Mb / M, .5)
    m = contract(g, M, c, e, 1 - fb) if nu else (1 - fb) * mnfw(g.r, M, c, e); return g.gb + G * m / g.r**2
def cDM14(M, z=0.): return 10**(.520 + (.905 - .520) * np.exp(-.617 * z**1.21) + (-.101 + .026 * z) * np.log10(M * h0 / 1e12))
def dl16(g, e, cmode='d19', dn=0., dc=0.):
    M = m200_of(g.Ms) * 10**dn; c = (cDM14(M) if cmode == 'dm14' else cof(e, M)) * 10**dc; X = np.log10(g.Ms / M); R = R200(e, M)
    if M > 1e12: return g.gb + G * .842 * mnfw(g.r, M, c, e) / g.r**2
    a, b, gm, lr = dc14_par(X); c = c * 10**lr; rm2 = R / c; rs = rm2 / ((2 - gm) / (b - 2))**(1 / a)
    rho = lambda r: (r / rs)**-gm * (1 + (r / rs)**a)**(-(b - gm) / a)
    rr, m = cum_mass(rho, 1e-5 * rs, max(R, g.r[-1]) * 1.01, gin=gm); mR = np.interp(np.log(R), np.log(rr), m)
    return g.gb + G * .842 * M * Msun * np.interp(np.log(g.r), np.log(rr), m) / mR / g.r**2
SIG0 = 10**2.15 * Msun / (kpc / 1e3)**2  # rho0 r0 in kg m^-2
GR0 = 2 * np.pi * (np.log(2) + .5 * np.log(2) - np.pi / 4) * G * SIG0
def burk(g, k):
    r0 = k * g.Rd; x = g.r / r0; m = 2 * np.pi * SIG0 * r0**2 * (np.log(1 + x) + .5 * np.log(1 + x**2) - np.arctan(x)); return g.gb + G * m / g.r**2
# ---------- analytic scales ----------
def zgrid(C):
    zz = np.linspace(0, 30, 601); return zz, np.array([C.growthFactor(z) for z in zz])
def kt(M, C, e, zg, mode='G', f=FKT, beta=BETA):
    """KT eq (4) in physical form; returns a0_eq = 2 a_DM. M array or scalar."""
    h = C.h; rhom0 = C.rho_m(0) * h**2 * Msun / kpc**3; M = np.atleast_1d(M).astype(float)
    L = (3 * M * Msun / (4 * np.pi * rhom0))**(1 / 3); s0 = np.asarray(C.sigma(L / MPC * h, 0.), float)
    if mode == 'E': zc = np.maximum(s0 - 1, 0.)
    else: zz, D = zg; zc = np.where(s0 > 1, np.interp(1 / s0, D[::-1], zz[::-1]), 0.)
    zc = np.maximum(zc, e['z']); a = 4 * np.pi * G * beta**2 * rhom0 * L * (1 + zc)**2 / f
    return 2 * a, zc
def ktnfw(M, e, mb=None):
    M = float(M); c = cof(e, M); mb = FB * M * Msun if mb is None else mb; fdm = 1 - mb / (M * Msun); R = R200(e, M)
    r = brentq(lambda r: fdm * mnfw(r, M, c, e) - mb, 1e-6 * R, 50 * R); return 2 * G * mb / r**2
def btfr(M, e, mb): R = R200(e, M); V2 = G * M * Msun / R; return V2**2 / (G * mb)
def gnfw_rs(M, e): c = cof(e, M); rs = R200(e, M) / c; return G * (1 - FB) * mnfw(rs, M, c, e) / rs**2
def zx(C):
    zz = np.linspace(0, 10, 2001); d = np.array([C.rho_de(z) - C.rho_m(z) for z in zz]); i = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    if len(i) == 0: return np.nan, np.nan
    z = zz[i[0]] - d[i[0]] * (zz[i[0] + 1] - zz[i[0]]) / (d[i[0] + 1] - d[i[0]]); return z, C.Hz(z) * 1e3 / MPC
# ---------- grading helpers ----------
def egr(cur, S=None):
    S = GS if S is None else S; d = np.concatenate([np.log10(c) - np.log10(g.gl) for g, c in zip(S, cur)]); gb = np.concatenate([g.gb for g in S])
    per = np.array([np.sqrt(((np.log10(c) - np.log10(g.gl))**2).mean()) for g, c in zip(S, cur)]); b = np.floor(np.log10(gb) * 2) / 2
    e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50) if len(S) == len(GS) else np.nan
    return np.sqrt((d**2).mean()), np.percentile(per, 95), e3
def row(tag, fn, nk, hold, extra=''):
    cur = [fn(g) for g in GS]; grade(tag, cur, f'({nk} knobs{"; " + extra if extra else ""})'); e1, e2, e3 = egr(cur)
    ok = e1 <= .02 and e2 <= .04 and e3 <= .02 and hold <= .025; a = fit_a(ALLB, np.concatenate(cur))
    print(f' holdout unseen GS[1::2] rms to law {hold:.4f} [{P(hold <= .025)} <= 0.025]; law-equivalent a {a / A0:.4f} A0, kappa_eff {a / AC:.4f}; VERDICT {"EXACT" if ok else "NOT EXACT"}', flush=True)
    return dict(e1=e1, e2=e2, e3=e3, hold=hold, a=a, exact=ok, nk=nk)
def hold0(fn): return egr([fn(g) for g in GS[1::2]], GS[1::2])[0]
def tune1(fnk, S, lo, hi):
    return minimize_scalar(lambda k: egr([fnk(g, k) for g in S], S)[0], bounds=(lo, hi), method='bounded', options=dict(xatol=1e-3)).x
print(f'A34 recipe35; c sqrt(G rho_DE0) {AC:.4e}, A0 {A0:.4e}; f_b {FB:.4f}, Omega_B/Omega_CDM {FKT:.4f}; beta {BETA}; Burkert g(r0) {GR0:.3e} m s^-2', flush=True)
C0, s80 = mkP(BG['B0']); E0 = env(C0, 0.); ZG0 = zgrid(C0)
print(f'control: B0 footing P sigma8 {s80:.4f}, c-grid vs lib max rel {np.abs(E0["cg"] / CG - 1).max():.1e}; R200(1e12) {R200(E0, 1e12) / kpc:.1f} kpc', flush=True)
gt0 = GS[0]; print(f'control: des nu0 at lib r1 (no contraction) max |dlog| on {gt0.n}: {np.abs(np.log10(des(gt0, E0, 0)) - np.log10(r1(gt0, [0, 0, 0, 0]))).max():.1e}; '
                   f'des nu1 vs lib r1 f=1: {np.abs(np.log10(des(gt0, E0, 1)) - np.log10(r1(gt0, [0, 0, 0, 1.]))).max():.1e}', flush=True)
RES = {}
# ======================= (a) SPARC grades at base =======================
print('\n######## (a) SPARC, base cosmology', flush=True)
# --- KT
akt, zckt = kt(M2, C0, E0, ZG0, 'G'); akte, zcke = kt(M2, C0, E0, ZG0, 'E'); aam = np.array([ktnfw(M, E0, g.mbtot) for g, M in zip(GS, M2)])
a12, z12 = kt(1e12, C0, E0, ZG0, 'G'); a12e, z12e = kt(1e12, C0, E0, ZG0, 'E'); a17, _ = kt(1e12, C0, E0, ZG0, 'G', f=1 / 7.)
print(f'\nKT eq(4) at M200 1e12: growth reading z_c {z12[0]:.3f}, a0_eq = 2 a_DM {a12[0] / A0:.4f} A0 (paper reading a_DM {a12[0] / 2 / A0:.4f} A0); EdS reading z_c {z12e[0]:.3f}, a0_eq {a12e[0] / A0:.4f} A0; f = 1/7: {a17[0] / A0:.4f} A0', flush=True)
print(f' KT beta needed for kappa_eff 0.5 (growth, a0_eq): {BETA * np.sqrt(.5 * AC / a12[0]):.3f}; paper reading (a0_eq = a_DM): {BETA * np.sqrt(.5 * AC / (a12[0] / 2)):.3f}')
print(f' KT over SPARC: z_c (growth) median {np.median(zckt):.2f}, p5-p95 {np.percentile(zckt, 5):.2f}-{np.percentile(zckt, 95):.2f}; a0_eq median {np.median(akt) / A0:.3f} A0, rms {np.log10(akt).std():.3f} dex', flush=True)
kn = ktnfw(1e12, E0); print(f' KT NFW check at 1e12 (cosmic f_b): a0_eq {kn / A0:.4f} A0 (a_DM {kn / 2 * 100:.3e} cm s^-2 vs paper ~1e-8); KT-AM per galaxy median {np.median(aam) / A0:.4f} A0, rms {np.log10(aam).std():.3f} dex')
for tag, arr in (('KT-G eq(4) growth', akt), ('KT-E eq(4) EdS', akte), ('KT-AM NFW, own M_b', aam)):
    res = {}
    res['swap'] = row(f'{tag}: law with a = per-galaxy a0_eq', lambda g, A={g.n: a for g, a in zip(GS, arr)}: law(g.gb, A[g.n]), 1, hold0(lambda g, A={g.n: a for g, a in zip(GS, arr)}: law(g.gb, A[g.n])), 'beta 5 or f_b fixed, shape inherited from the law')
    A = {g.n: a for g, a in zip(GS, arr)}; fk = lambda g, k: law(g.gb, A[g.n] * 10**k)
    ko = tune1(fk, GS[::2], -1.5, 1.5); ka = tune1(fk, GS, -1.5, 1.5)
    res['fac'] = row(f'{tag}: plus one global factor', lambda g: fk(g, ka), 2, egr([fk(g, ko) for g in GS[1::2]], GS[1::2])[0], f'factor {10**ka:.3f}; holdout factor {10**ko:.3f}')
    RES['a_' + tag] = res
# --- MMW engine
row('MMW engine m_d 0.05, NFW Diemer19, Blumenthal', lambda g: mmw(g, E0), 0, hold0(lambda g: mmw(g, E0)))
fk = lambda g, k: mmw(g, E0, 10**k); ko = tune1(fk, GS[::2], -2.5, -.3); ka = tune1(fk, GS, -2.5, -.3)
RES['a_MMW'] = row('MMW engine, m_d one global knob', lambda g: fk(g, ka), 1, egr([fk(g, ko) for g in GS[1::2]], GS[1::2])[0], f'm_d {10**ka:.4f}; holdout m_d {10**ko:.4f}')
lam = []
for g in GS:
    M = g.Mb / MD; c = cof(E0, M); fc = 2 / 3 + (c / 21.5)**.7; lam.append(np.sqrt(2) * g.Rd * np.sqrt(fc) / R200(E0, M))
print(f' MMW implied lambda (j_d = m_d, f_R = 1): median {np.median(lam):.4f}, p16-p84 {np.percentile(lam, 16):.4f}-{np.percentile(lam, 84):.4f} (MMW median 0.05); log M200 = log M_b/m_d median {np.median(np.log10([g.Mb / MD for g in GS])):.2f} vs SHMR {np.median(np.log10(M2)):.2f}')
print(f' MMW BTFR scale 10 H V200 / m_d at 1e12: {btfr(1e12, E0, MD * 1e12 * Msun) / A0:.4f} A0; rms over log M200 11-12.5 {np.log10([btfr(10**m, E0, MD * 10**m * Msun) for m in LMH]).std():.3f} dex', flush=True)
# --- vdBD
row('vdBD: SHMR halo (eps_gf f_bar = M_b/M200), NFW Diemer19, Blumenthal', lambda g: vdbd(g, E0), 0, hold0(lambda g: vdbd(g, E0)))
fk = lambda g, k: vdbd(g, E0, k); ko = tune1(fk, GS[::2], -1., 1.); ka = tune1(fk, GS, -1., 1.)
RES['a_vdBD'] = row('vdBD, one global M200 shift', lambda g: fk(g, ka), 1, egr([fk(g, ko) for g in GS[1::2]], GS[1::2])[0], f'dlog M200 {ka:+.3f}; holdout {ko:+.3f}')
avb = np.array([btfr(M, E0, g.mbtot) for g, M in zip(GS, M2)]); vmx = np.array([(np.sqrt(vdbd(g, E0)[-1] * g.r[-1]))**4 / (G * g.mbtot) for g in GS])
print(f' vdBD eq(B3) scale V200^4/(G M_b): median {np.median(avb) / A0:.4f} A0, rms {np.log10(avb).std():.3f} dex (11-12.5: {np.log10(avb[SEL]).std():.3f}); V_last variant median {np.median(vmx) / A0:.4f} A0, rms {np.log10(vmx).std():.3f}', flush=True)
row('vdBD eq(B3) scale swapped into the law, per galaxy', lambda g, A={g.n: a for g, a in zip(GS, avb)}: law(g.gb, A[g.n]), 0, hold0(lambda g, A={g.n: a for g, a in zip(GS, avb)}: law(g.gb, A[g.n])))
# --- DL16
RES['a_DL16'] = row('DL16 DC14 + Dutton-Maccio c (memory), SHMR, x 0.842', lambda g: dl16(g, E0, 'dm14'), 0, hold0(lambda g: dl16(g, E0, 'dm14')))
row('DL16 DC14 + Diemer19 c', lambda g: dl16(g, E0), 0, hold0(lambda g: dl16(g, E0)))
res2 = lambda k, S: np.concatenate([np.log10(dl16(g, E0, 'dm14', k[0], k[1])) - np.log10(g.gl) for g in S])
ka = least_squares(lambda k: res2(k, GS), [0, 0], bounds=([-.5, -.3], [.5, .3]), max_nfev=30, diff_step=.02).x
ko = least_squares(lambda k: res2(k, GS[::2]), [0, 0], bounds=([-.5, -.3], [.5, .3]), max_nfev=30, diff_step=.02).x
row('DL16 DM14 + 2 global knobs (dlog M200, dlog c)', lambda g: dl16(g, E0, 'dm14', ka[0], ka[1]), 2, np.sqrt((res2(ko, GS[1::2])**2).mean()), f'knobs {np.round(ka, 3).tolist()}; holdout {np.round(ko, 3).tolist()}')
# --- Desmond
def d3(g, gt):
    D = gt / g.gb; i = np.where((D[:-1] < 3) & (D[1:] >= 3))[0]
    if len(i) == 0: return np.nan
    i = i[0]; t = (3 - D[i]) / (D[i + 1] - D[i]); return 6 * 10**(np.log10(g.gb[i]) + t * (np.log10(g.gb[i + 1]) - np.log10(g.gb[i])))
for nu in (0, 1):
    RES[f'a_Des{nu}'] = row(f'Desmond 2017 nu={nu} mean relation (SHMR, NFW Diemer19{", Blumenthal" if nu else ""})', lambda g: des(g, E0, nu), 0, hold0(lambda g: des(g, E0, nu)))
def shs(M): x = np.log10(M); return (np.log10(smhm(10**(x + .01))) - np.log10(smhm(10**(x - .01)))) / .02
SL = np.array([max(shs(M), .2) for M in M2]); rows = {0: [], 1: []}
for s in range(40):
    rng = np.random.default_rng(1000 + s); dm = np.clip(rng.normal(0, .16, len(GS)) / SL, -1, 1); dcc = rng.normal(0, .11, len(GS))
    for nu in (0, 1):
        cur = [des(g, E0, nu, a, b) for g, a, b in zip(GS, dm, dcc)]; gt = np.concatenate(cur)
        rows[nu].append((egr(cur)[0], np.sqrt(((np.log10(gt) - np.log10(ALLO))**2).mean()), np.nanstd(np.log10([d3(g, c) for g, c in zip(GS, cur)]))))
for nu in (0, 1):
    a = np.array(rows[nu]); print(f' Desmond nu={nu} scatter mocks (0.16 dex M*, 0.11 dex c, 40 seeds): rms to law median {np.median(a[:, 0]):.4f} (16-84 {np.percentile(a[:, 0], 16):.4f}-{np.percentile(a[:, 0], 84):.4f}); '
                              f'rms to observed {np.median(a[:, 1]):.4f} [{P(np.median(a[:, 1]) <= .205)} S <= 0.205]; D=3 scale spread {np.median(a[:, 2]):.3f} dex', flush=True)
for tag, cur in (('law', [g.gl for g in GS]), ('observed', [g.gobs for g in GS]), ('Desmond nu0', [des(g, E0, 0) for g in GS]), ('Desmond nu1', [des(g, E0, 1) for g in GS])):
    v = np.array([d3(g, c) for g, c in zip(GS, cur)]); ok = np.isfinite(v)
    print(f' D=3 scale a0_eq = 6 g_b,cross [{tag}]: {ok.sum()} galaxies cross; median {np.nanmedian(v) / A0:.4f} A0, spread {np.nanstd(np.log10(v)):.3f} dex; in log M200 11-12.5 spread {np.nanstd(np.log10(v[SEL])):.3f}', flush=True)
# --- Salucci / Donato
fk = burk; ko = tune1(fk, GS[::2], .1, 10.); ka = tune1(fk, GS, .1, 10.)
RES['a_Sal'] = row('Salucci/Donato Burkert, rho0 r0 = 10^2.15, r0 = k R_d', lambda g: fk(g, ka), 1, egr([fk(g, ko) for g in GS[1::2]], GS[1::2])[0], f'k {ka:.3f}; holdout k {ko:.3f}')
print(f' Burkert g(r0) {GR0 / A0:.4f} A0, kappa_eff raw {GR0 / AC:.4f}, x2 reading {2 * GR0 / AC:.4f}; mass-free (G4 pass by construction, empirical); NFW analogue g(r_s) at 1e12 {gnfw_rs(1e12, E0) / A0:.4f} A0', flush=True)
CKT = a12[0] / (c_ * E0['H']); print(f'\nKT coefficient C_KT = a0_eq(1e12)/(c H0) = {CKT:.4f} (paper says O(1))', flush=True)
# ======================= (b, c) scales across backgrounds =======================
ROUTES = ['KT-G', 'KT-E', 'KT-NFW', 'KT-AM', 'KT-H1', 'KT-H2', 'KT-H2-2pi', 'MMW-curve', 'MMW-BTFR', 'vdBD-curve', 'vdBD-B3', 'DL16-curve', 'Des0-curve', 'Des1-curve', 'Des0-D3', 'Sal-NFWrs', 'Sal-Burkert']
def scales(C, e, zg, zxh, fast=False):
    """all route scales (law-equivalent a) in environment e of background C; zxh = (z_x, H(z_x))."""
    s = {}; s['KT-G'] = float(kt(1e12, C, e, zg, 'G')[0][0]); s['KT-E'] = float(kt(1e12, C, e, zg, 'E')[0][0]); s['KT-NFW'] = ktnfw(1e12, e)
    s['KT-AM'] = float(np.median([ktnfw(M, e, g.mbtot) for g, M in zip(GS, M2)]))
    s['KT-H1'] = CKT * c_ * np.sqrt(8 * np.pi * G * e['rde'] / 3); s['KT-H2'] = CKT * c_ * zxh[1]; s['KT-H2-2pi'] = c_ * zxh[1] / (2 * np.pi)
    s['MMW-BTFR'] = btfr(1e12, e, MD * 1e12 * Msun); s['vdBD-B3'] = float(np.median([btfr(M, e, g.mbtot) for g, M in zip(GS, M2)]))
    s['Sal-NFWrs'] = gnfw_rs(1e12, e); s['Sal-Burkert'] = GR0
    for k, fn in (('MMW-curve', mmw), ('vdBD-curve', vdbd), ('DL16-curve', dl16), ('Des0-curve', lambda g, e: des(g, e, 0)), ('Des1-curve', lambda g, e: des(g, e, 1))):
        cur = [fn(g, e) for g in GS]; s[k] = fit_a(ALLB, np.concatenate(cur))
        if k == 'Des0-curve': s['Des0-D3'] = float(np.nanmedian([d3(g, c) for g, c in zip(GS, cur)]))
    return s
# G4 at base z 0
g4 = {k: 0. for k in ('KT-H1', 'KT-H2', 'KT-H2-2pi', 'Sal-Burkert')}
g4['KT-G'] = float(np.log10(kt(10**LMH, C0, E0, ZG0, 'G')[0]).std()); g4['KT-E'] = float(np.log10(kt(10**LMH, C0, E0, ZG0, 'E')[0]).std())
g4['KT-NFW'] = float(np.log10([ktnfw(10**m, E0) for m in LMH]).std()); g4['KT-AM'] = float(np.log10(aam[SEL]).std())
g4['MMW-BTFR'] = float(np.log10([btfr(10**m, E0, MD * 10**m * Msun) for m in LMH]).std()); g4['vdBD-B3'] = float(np.log10(avb[SEL]).std()); g4['Sal-NFWrs'] = float(np.log10([gnfw_rs(10**m, E0) for m in LMH]).std())
for k, fn, MM in (('MMW-curve', mmw, np.array([g.Mb / MD for g in GS])), ('vdBD-curve', vdbd, M2), ('DL16-curve', dl16, M2), ('Des0-curve', lambda g, e: des(g, e, 0), M2), ('Des1-curve', lambda g, e: des(g, e, 1), M2)):
    sel = (np.log10(MM) >= 11) & (np.log10(MM) <= 12.5); ai = np.array([fit_a(g.gb, fn(g, E0)) for g, s in zip(GS, sel) if s]); g4[k] = float(np.log10(ai).std())
v = np.array([d3(g, des(g, E0, 0)) for g in GS]); g4['Des0-D3'] = float(np.nanstd(np.log10(v[SEL])))
print('\nG4 (rms of log a over hosts log M200 11-12.5; per-galaxy routes use SPARC galaxies there): ' + '; '.join(f'{k} {v:.3f} [{P(v <= .1)}]' for k, v in g4.items()), flush=True)
G5 = {k: ('FAIL', 'hand rho_DE/H factor; no process carries it into the halo') if k.startswith('KT-H') else ('PASS', 'halo gravity at galaxy radii') for k in ROUTES}
G5['Sal-Burkert'] = ('PASS', 'halo gravity; scale empirical, not derived')
BR = {}
for foot in ('P', 'S'):
    print(f'\n===== footing {foot} ({"early amplitude fixed at z 30" if foot == "P" else "sigma8 0.811 today"})', flush=True)
    for bn, de in BG.items():
        key = f'{foot}_{bn}'
        if key in OUT: BR[key] = OUT[key]; print(f' {bn}: (from checkpoint)', flush=True); continue
        C, s8 = mkP(de) if foot == 'P' else (mk(de, .811), .811); zg = zgrid(C); zxh = zx(C); E = {z: env(C, z) for z in ZS}
        r = {z: E[z]['rde'] / E[0.]['rde'] for z in ZS}; S = {z: scales(C, E[z], zg, zxh) for z in ZS}
        lnr = np.log(max(r.values()) / min(r.values())); meas = lnr >= .1
        print(f'\n {bn} {de.get("w0", "")} {de.get("wa", "")}: sigma8 {s8:.4f}; rho_DE(z)/rho_DE0 ' + ' '.join(f'{r[z]:.4f}' for z in ZB) + f'; z_x (rho_DE = rho_m) {zxh[0]:.3f}; G2z {"measurable" if meas else "not measurable"}', flush=True)
        rr = {}
        for k in ROUTES:
            a = {z: S[z][k] for z in ZS}; ke = a[0.] / AC; g1 = abs(np.log10(ke / .5)) <= .05; rz = {z: a[z] / a[0.] for z in ZB}; g3 = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB)
            dv = gt_dev(a, r); gtp = all(abs(x) <= .05 for x in dv.values()); s2 = slope([r[z] for z in ZS], [a[z] for z in ZS]) if meas else None
            rr[k] = dict(k0=ke, rz=rz, gt=dv, GT=gtp, G1=g1, G3=g3, s2z=s2, a={z: a[z] for z in ZS})
            print(f'  {k:11s} a(0) {a[0.] / A0:.4f} A0 kappa_eff {ke:.4f} [{P(g1)} G1]; a(z)/a(0) ' + ' '.join(f'{rz[z]:.4f}' for z in ZB) + f' [{P(g3)} G3]; GT dev '
                  + ' '.join(f'{dv[z]:+.4f}' for z in ZB) + f' [{P(gtp)} GT]' + (f'; G2z {s2:+.3f}' if meas else ''), flush=True)
        BR[key] = dict(r=r, routes=rr, s8=s8, zx=zxh[0]); ck(key, BR[key])
def fz(d): return {float(k): v for k, v in d.items()}
for key in BR:
    BR[key]['r'] = fz(BR[key]['r'])
    for k in BR[key]['routes']:
        for f in ('rz', 'gt', 'a'): BR[key]['routes'][k][f] = fz(BR[key]['routes'][k][f])
EVO = ['B1', 'B1p', 'B1u', 'B2', 'B3', 'B4']; G2X = {}
print('\nG2x: pooled slope of ln[a(z)/a(0)] vs ln[rho_DE(z)/rho_DE0] over B1, B1p, B1u, B2, B3, B4 at z 1, 1.5, 2.33 (18 points)', flush=True)
for foot in ('P', 'S'):
    for k in ROUTES:
        x = [BR[f'{foot}_{b}']['r'][z] for b in EVO for z in ZB]; y = [BR[f'{foot}_{b}']['routes'][k]['rz'][z] for b in EVO for z in ZB]
        s = slope(x, y); G2X[(foot, k)] = s; print(f' {foot} {k:11s}: slope {s:+.4f} [{P(abs(s - .5) <= .05)} G2x]', flush=True)
# ---------- G2t across rho_DE today (A26 C1 physical footing), Lambda and B1 ----------
G2T = OUT.get('G2t', {})
for bn in ('B0', 'B1'):
    if bn in G2T: continue
    print(f'\nG2t in {bn}: rho_DE0 x f on the A26 C1 physical footing', flush=True); FS = [.5, .71, 1., 1.41, 2.]; rows = {k: [] for k in ROUTES}; rd = []
    for f in FS:
        wm, wb, wd = .315 * h0**2, .0493 * h0**2, f * .685 * h0**2; h = np.sqrt(wm + wd)
        C, s8 = mkP(BG[bn], 100 * h, wm / h**2, wb / h**2, R=8. * h / h0); e = env(C, 0.); rd.append(e['rde']); s = scales(C, e, zgrid(C), zx(C))
        for k in ROUTES: rows[k].append(s[k])
        print(f'  f {f}: h {h:.4f}, sigma8 {s8:.4f}, KT-G {s["KT-G"] / A0:.4f} A0, z_x {zx(C)[0]:.3f}', flush=True)
    G2T[bn] = {k: slope(rd, v) for k, v in rows.items()}; ck('G2t', G2T)
for bn in ('B0', 'B1'): print(f' G2t {bn}: ' + '; '.join(f'{k} {s:+.3f} [{P(abs(s - .5) <= .05)}]' for k, s in G2T[bn].items()), flush=True)
# ---------- verdict table and ranking (footing P) ----------
print('\nVERDICT TABLE (footing P; GT counted over B1, B1p, B1u, B2, B3, B4, B5)', flush=True)
EV = EVO + ['B5']; rank = []
for k in ROUTES:
    b0 = BR['P_B0']['routes'][k]; g1 = b0['G1']; g3 = b0['G3']; g2t = abs(G2T['B0'][k] - .5) <= .05 and abs(G2T['B1'][k] - .5) <= .05; g2x = abs(G2X[('P', k)] - .5) <= .05
    ngt = sum(BR[f'P_{b}']['routes'][k]['GT'] for b in EV); gtall = ngt == len(EV); g4p = g4[k] <= .1; g5 = G5[k][0] == 'PASS'
    n = sum([g1, g2t and g2x, g3, g4p, g5, gtall]); rank.append((n, k))
    print(f' {k:11s} kappa_eff {b0["k0"]:.3f} G1 {P(g1)}; G2 t(B0 {G2T["B0"][k]:+.3f}, B1 {G2T["B1"][k]:+.3f}) x {G2X[("P", k)]:+.3f} {P(g2t and g2x)}; G3 {P(g3)}; G4 {g4[k]:.3f} {P(g4p)}; '
          f'G5 {G5[k][0]} ({G5[k][1]}); GT {ngt}/{len(EV)} {P(gtall)}; tie gates passed {n}/6', flush=True)
print('\nRANK by tie gates passed (6 max):', ', '.join(f'{k} {n}' for n, k in sorted(rank, key=lambda x: -x[0])), flush=True)
print('SPARC (a) summary: ' + '; '.join(f'{k[2:]} E1 {v["swap"]["e1"] if "swap" in v else v["e1"]:.4f}' for k, v in RES.items()), flush=True)
print(f'\nruntime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
