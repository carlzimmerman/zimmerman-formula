"""A36: the logotropic dark fluid (Chavanis; P = A ln(rho/rho_P), A = B rho_Lambda c^2) on SPARC, its acceleration
readings on G1-G5, and tracking in its own and A29's backgrounds. Per ../FROZEN_A36.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os, time
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.integrate import solve_ivp
T00 = time.time()
c_, hbar, pc = 2.998e8, 1.0546e-34, 3.0857e16
MSPC = Msun / pc**2
NG = len(GS); TUNE, UNSEEN = list(range(NG))[::2], list(range(NG))[1::2]
RDE0 = cos.Ode0 * RHOC; AN = c_ * np.sqrt(G * RDE0)
print(f'c sqrt(G rho_DE0) = {AN:.4e} m/s^2 (2 A0 = {2 * A0:.4e})')

# ---------------- logotropic Lane-Emden: theta'' + 2 theta'/xi = 1/theta
def le_rhs(x, y): return [y[1], 1 / y[0] - 2 * y[1] / x]
x0 = 1e-4; sol = solve_ivp(le_rhs, (x0, 1e7), [1 + x0**2 / 6, x0 / 3], method='LSODA', rtol=1e-10, atol=1e-12, dense_output=True)
XI = np.logspace(-4, 7, 4000); TH, THP = sol.sol(XI)
xih = brentq(lambda x: sol.sol(x)[0] - 4, 1, 50); thph = sol.sol(xih)[1]
print(f'LE check: xi_h {xih:.4f} (paper 5.85), theta\'_h {thph:.4f} (paper 0.693), 4 pi theta\'_h/xi_h {4 * np.pi * thph / xih:.4f} (paper 1.49)')
print(f'LE asymptote: theta/xi at xi 1e6 {TH[-500] / XI[-500]:.5f} (1/sqrt2 = {1 / np.sqrt(2):.5f}); theta\' at 1e7 {THP[-1]:.5f}')
print(f'  => rho -> (A/2 pi G)^(1/2)/r from the ODE; the reader quoted (A/8 pi G)^(1/2)/r for eq. 148 (reading issue, ODE used)')
def thp(xi): return np.interp(np.log(xi), np.log(XI), THP, left=0., right=THP[-1])

# ---------------- constants
def consts(rL):
    rP = c_**5 / (hbar * G**2); B = 1 / np.log(rP / rL); A = B * rL * c_**2; S0 = xih * np.sqrt(A / (4 * np.pi * G)); return B, A, S0
B, A, S0 = consts(RDE0)
Lam = 8 * np.pi * G * RDE0   # s^-2 units, as the paper's c sqrt(Lambda)/G
print(f'B {B:.4e} (paper 3.53e-3); A {A:.4e} Pa; Sigma0 {S0:.4f} kg/m^2 = {S0 / MSPC:.1f} Msun/pc^2 (paper 133); '
      f'Sigma0 G/(c sqrt Lambda) {S0 * G / (c_ * np.sqrt(Lam)):.5f} (paper 0.01955); rho_DE0 {RDE0:.3e} kg/m^3 (paper 5.96e-27)')
GINF = 4 * np.pi * G * S0 / xih * THP[-1]
gdm = lambda r, rh: 4 * np.pi * G * S0 / xih * thp(xih * r / rh)

# ---------------- (a) SPARC
def curve(g, rh): return g.gb + gdm(g.r, rh)
def rh_rule(g, fb, s=1.): return np.sqrt(g.Mb * Msun / fb / (1.49 * S0 * s))
def gal_fit(g, s=1.):
    def obj(lx):
        gt = g.gb + s * 4 * np.pi * G * S0 / xih * thp(xih * g.r / (10**lx * kpc)); return ((np.log10(gt) - g.lgl)**2).sum()
    grid = np.linspace(np.log10(.05), np.log10(500), 61); v = [obj(x) for x in grid]; i = int(np.argmin(v))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, 60)]
    r = minimize_scalar(obj, bounds=(lo, hi), method='bounded'); return r.x, r.fun
for g in GS: g.lgl = np.log10(g.gl)
def rms_sub(cur, idx):
    d = np.concatenate([np.log10(cur[i]) - GS[i].lgl for i in idx]); return np.sqrt((d**2).mean())

print(f'\nhalo dark-acceleration ceiling g_inf = {GINF:.3e} m/s^2 = {GINF / A0:.3f} a0; law needs g_obs-g_b = 0.618 a0 at g_b = a0')
cur0 = [curve(g, rh_rule(g, .17)) for g in GS]
grade('L0 logotrope, 0 knobs, M_h = M_b/0.17, r_h from M_h = 1.49 Sigma0 r_h^2', cur0)
print(f' L0 median r_h {np.median([rh_rule(g, .17) for g in GS]) / kpc:.2f} kpc')
def l1obj(lf, idx): return sum(((np.log10(curve(GS[i], rh_rule(GS[i], 10**lf))) - GS[i].lgl)**2).sum() for i in idx)
lf_all = minimize_scalar(lambda x: l1obj(x, range(NG)), bounds=(-3, 0), method='bounded').x
cur1 = [curve(g, rh_rule(g, 10**lf_all)) for g in GS]
grade(f'L1 logotrope, 1 global knob f_b = {10**lf_all:.4f}', cur1)
lf_t = minimize_scalar(lambda x: l1obj(x, TUNE), bounds=(-3, 0), method='bounded').x
cur1t = [curve(g, rh_rule(g, 10**lf_t)) for g in GS]
ho = rms_sub(cur1t, UNSEEN); print(f' L1 holdout: f_b tuned on GS[::2] {10**lf_t:.4f}, unseen GS[1::2] rms {ho:.4f} dex [{"PASS" if ho <= .025 else "FAIL"} holdout]')

LRH = np.array([gal_fit(g)[0] for g in GS])
atb = int(((LRH < np.log10(.05) + 1e-3) | (LRH > np.log10(500) - 1e-3)).sum())
cur2 = [curve(g, 10**l * kpc) for g, l in zip(GS, LRH)]
grade('L2 logotrope, r_h per galaxy (171 knobs), Sigma0 fixed', cur2, f'(r_h at bound: {atb}; median r_h {np.median(10**LRH):.2f} kpc)')
print(f' L2 rms over GS[1::2] (no true holdout for per-galaxy knobs) {rms_sub(cur2, UNSEEN):.4f}')
a2 = fit_a(ALLB, np.concatenate(cur2))
d2 = np.concatenate(cur2) / ALLB; gd = np.concatenate([gdm(g.r, 10**l * kpc) for g, l in zip(GS, LRH)])
print(f' L2 max dark accel over all points {gd.max() / A0:.3f} a0; points with g_b > 3e-11: mean log(g/law) {np.mean((np.log10(np.concatenate(cur2)) - np.log10(ALLL))[ALLB > 3e-11]):+.4f}')
print(f' [{time.time() - T00:.0f} s]', flush=True)

# L3: hydrostatic in baryon + own potential, rho0 per galaxy
def l3_curve(g, lrho0, n=180):
    x = np.linspace(np.log(g.r[0] * .05), np.log(g.r[-1]), n); dx = x[1] - x[0]; lr0 = np.log(g.r)
    gbg = np.interp(x, lr0, g.gb); ins = x < lr0[0]; gbg[ins] = g.gb[0] * np.exp(x[ins] - lr0[0])
    rr = np.exp(x); rho0 = 10**lrho0; u = 1 / rho0; M = 4 * np.pi / 3 * rho0 * rr[0]**3; out = np.empty(n)
    for i in range(n):
        out[i] = M; r = rr[i]
        if i == n - 1: break
        # midpoint step in ln r
        du1 = r * (gbg[i] + G * M / r**2) / A; dM1 = 4 * np.pi * r**3 / u
        um, Mm, rm = u + .5 * dx * du1, M + .5 * dx * dM1, r * np.exp(.5 * dx); gm = .5 * (gbg[i] + gbg[i + 1])
        u += dx * rm * (gm + G * Mm / rm**2) / A; M += dx * 4 * np.pi * rm**3 / um
    return g.gb + G * np.interp(lr0, x, out) / g.r**2
LR3 = []
for g, l in zip(GS, LRH):
    lc = np.log10(S0 / (10**l * kpc)); obj = lambda y: ((np.log10(l3_curve(g, y)) - g.lgl)**2).sum()
    grid = np.linspace(lc - 3, lc + 3, 25); v = [obj(y) for y in grid]; i = int(np.argmin(v))
    LR3.append((minimize_scalar(obj, bounds=(grid[max(i - 1, 0)], grid[min(i + 1, 24)]), method='bounded').x, lc, i))
atb3 = sum(1 for _, _, i in LR3 if i in (0, 24))
cur3 = [l3_curve(g, y) for g, (y, _, _) in zip(GS, LR3)]
grade('L3 logotrope in baryon+own potential (not as published), rho0 per galaxy (171 knobs)', cur3, f'(grid-edge minima: {atb3})')
print(f' [{time.time() - T00:.0f} s]', flush=True)

# L4 probe: Sigma0 x s global, r_h per galaxy
best = None
for ls in np.linspace(-.5, 1.5, 21):
    tot = sum(gal_fit(g, 10**ls)[1] for g in GS)
    if best is None or tot < best[1]: best = (ls, tot)
s4 = 10**best[0]; LRH4 = np.array([gal_fit(g, s4)[0] for g in GS])
cur4 = [g.gb + s4 * gdm(g.r, 10**l * kpc) for g, l in zip(GS, LRH4)]
grade(f'L4 probe (not the model): Sigma0 x {s4:.3f} global + r_h per galaxy (172 knobs)', cur4, f'(Sigma0 needed {s4 * S0 / MSPC:.0f} Msun/pc^2; ceiling {s4 * GINF / A0:.3f} a0)')
print(f' [{time.time() - T00:.0f} s]', flush=True)

# ---------------- (b) acceleration readings
print('\n== (b) acceleration readings, kappa_eff = a/(c sqrt(G rho_DE0)); G1 window 0.5 +- 0.05 dex')
fbc = cos.Ob0 / cos.Om0
R = [('i  G Sigma0', G * S0), ('ii g = G M_h/r_h^2 = 1.49 G Sigma0 (paper 2.76e-11)', 1.49 * G * S0),
     ('iii a0 = g/f_b, f_b 0.17 (paper; PRIMARY)', 1.49 * G * S0 / .17), (f'iii\' a0 = g/f_b, f_b Ob0/Om0 {fbc:.4f}', 1.49 * G * S0 / fbc),
     ('iv halo ceiling g_inf', GINF), ('v a_fit of L2 pooled (what the law sees)', a2)]
for n, a in R:
    k = a / AN; print(f' {n}: a {a:.3e} m/s^2, kappa_eff {k:.4f}, |dex| {abs(np.log10(k / .5)):.3f} [{"PASS" if abs(np.log10(k / .5)) <= .05 else "FAIL"} G1]')
print(f' paper cross-check: H0 c/4 = {cos.H0 * 1e3 / 3.0857e22 * c_ / 4:.3e}; 0.0419 H0 c = {.0419 * cos.H0 * 1e3 / 3.0857e22 * c_:.3e}')
S_lo, S_hi = consts(RDE0 * .5)[2], consts(RDE0 * 2)[2]; sl = np.log(S_hi / S_lo) / np.log(4)
print(f' G2 slope d ln Sigma0/d ln rho_Lambda (rho_Lambda x 0.5..2, B recomputed) {sl:.4f} [{"PASS" if abs(sl - .5) <= .05 else "FAIL"} G2]; '
      f'with B held fixed 0.5000 identically; (0.5 + B/2 = {.5 + B / 2:.4f})')
print(' G3: A is an EoS constant, Sigma0(z) = Sigma0: a(z)/a(0) = 1.000 at z 1, 1.5, 2.33 inside all bands [PASS G3, by construction]')
lmh = np.log10(1.49 * S0 * (10**LRH * kpc)**2 / Msun); ai = np.array([fit_a(g.gb, c) for g, c in zip(GS, cur2)])
sel = (lmh >= 11) & (lmh <= 12.5); r4 = np.std(np.log10(ai[sel]))
print(f' G4: readings i-iv universal by construction [PASS]; per-galaxy a_i on L2, {sel.sum()} galaxies with log M_h 11-12.5: '
      f'median {np.median(ai[sel]) / A0:.3f} a0, rms log {r4:.3f} dex [{"PASS" if r4 <= .1 else "FAIL"} G4]; all 171 rms {np.std(np.log10(ai)):.3f}')
print(f'  log M_h (L2) range {lmh.min():.2f} to {lmh.max():.2f}, median {np.median(lmh):.2f}')
for rk in (1, 10, 30):
    v = np.array([gdm(rk * kpc, 10**l * kpc) for l in LRH]) / A0
    print(f' G5: g_DM at {rk} kpc over L2 galaxies: median {np.median(v):.3f} a0, 16-84% {np.percentile(v, 16):.3f}-{np.percentile(v, 84):.3f} [{"PASS" if np.median(v) >= .1 else "FAIL"} G5]')
print(' Cassini: not applicable (dark fluid, no force modification)')

# ---------------- (c) tracking
print('\n== (c) tracking GT: |log10 a(z)/a(0) - 0.5 log10 rho_DE(z)/rho_DE0| <= 0.05')
ZL = [1., 1.5, 2.33]
def gt_line(tag, rat, flat=True):
    dev = [(0. if flat else .5 * np.log10(q)) - .5 * np.log10(q) for q in rat]
    ok = all(abs(d) <= .05 for d in dev)
    print(f' {tag}: rho_DE ratio {" ".join(f"{q:.4f}" for q in rat)}; GT dev {" ".join(f"{d:+.4f}" for d in dev)} [{"PASS" if ok else "FAIL"} GT]')
la = lambda z: -np.log(1 + z)
gt_line('C1 own logotropic background, A constant', [1 + 3 * B * la(z) for z in ZL])
print(f'  C1 w_DE today -1 - B = {-1 - B:.5f}; at z 2.33 {-1 - B / (1 + 3 * B * la(2.33)):.5f} (phantom by B; DESI-like rows have w0 > -1)')
def cpl(z, w0, wa): a = 1 / (1 + z); return a**(-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
BG = dict(B0=(-1, 0), B1=(-.752, -.86), B1p=(-.838, -.62), B1u=(-.667, -1.09), B2=(-.9, -.1), B3=(-.95, .35), B4=(-1.1, .3))
for k, (w0, wa) in BG.items():
    rat = [cpl(z, w0, wa) for z in ZL]
    gt_line(f'C2a {k} (w0 {w0}, wa {wa}), A constant', rat)
    gt_line(f'C2b {k}, A re-identified as B rho_DE(z) c^2 by hand', rat, flat=False)
# B5 EDE (FROZEN_A29): Lambda + Poulin fluid, n = 3, z_c 3500, f 0.1 at z_c
h = cos.h; zc = 3500.; ac = 1 / (1 + zc); rm = lambda a: cos.Om0 * RHOC / a**3; rr = lambda a: 4.18e-5 / h**2 * RHOC / a**4
RL0 = RDE0; amp = .1 / .9 * (rm(ac) + rr(ac) + RL0)
rede = lambda a: 2 * amp / (1 + (a / ac)**4.5); RL = RDE0 - rede(1.)
rat5 = [(RL + rede(1 / (1 + z))) / RDE0 for z in ZL]
gt_line('C2a B5 EDE, A constant', rat5); print(f'  B5 EDE share of rho_DE today {rede(1.) / RDE0:.2e}')
print(f'\nruntime {time.time() - T00:.0f} s')
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
