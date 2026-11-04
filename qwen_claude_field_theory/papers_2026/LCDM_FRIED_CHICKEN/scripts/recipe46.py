"""A45: Vainshtein (DGP normal branch, cubic Galileon), Vainshtein breaking inside matter (beyond-Horndeski / DHOST),
non-local gravity (Mashhoon kernel; Deser-Woodard / RR), per ../FROZEN_A45.md. Rival modified-gravity routes, not LCDM.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.interpolate import CubicSpline
T0 = time.time()
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
H0 = cos.H0 * 1e3 / (kpc * 1e3); OM = cos.Om0; OL = cos.Ode0
BGS = {'B1': (-.752, -.86), 'B1p': (-.838, -.62), 'B1u': (-.667, -1.09)}
def rde_ratio(z, w0, wa): return (1 + z)**(3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
def Etrk(z): a3 = OM * (1 + z)**3; return np.sqrt(.5 * (a3 + np.sqrt(a3**2 + 4 * OL)))
EV, OD = GS[::2], GS[1::2]
GMS, AU, RSUN = 1.327e20, 1.496e11, 6.957e8; GME, RMOON = 3.986e14, 3.844e8
RSAT, RLIMB = 9.58 * AU, 1.6 * RSUN
def rms(x): return np.sqrt((np.asarray(x)**2).mean())
def P(s): print(s, flush=True)
P(f'cosmology OL {OL:.3f}, H0 {cos.H0}: AC = c sqrt(G rho_DE0) {AC:.4e}, A0 {A0:.4e} (kappa {A0 / AC:.4f}); c/H0 {c_ / H0 / kpc / 1e3:.1f} Mpc')
for b, (w0, wa) in BGS.items(): P(f'GT targets {b} (w0 {w0}, wa {wa}): ' + ', '.join(f'z {z}: {.5 * np.log10(rde_ratio(z, w0, wa)):+.4f}' for z in ZB))
P('Galileon tracker E(z): ' + ', '.join(f'z {z}: E {Etrk(z):.4f}, rho_DE/rho_DE0 = 1/E^2 {1 / Etrk(z)**2:.4f}' for z in ZB) + f'; E(0) {Etrk(0):.6f}')
LM2 = np.array([np.log10(m200_of(g.Ms)) for g in GS]); HOST = (LM2 >= 11) & (LM2 <= 12.5)
def gt_const(tag):
    allok = True
    for b, (w0, wa) in BGS.items():
        res = {z: -.5 * np.log10(rde_ratio(z, w0, wa)) for z in ZB}; ok = all(abs(v) <= .05 for v in res.values()); allok &= ok
        P(f' {tag} GT constant scale in {b}: residuals ' + ', '.join(f'{z}: {v:+.4f}' for z, v in res.items()) + f' [{"PASS" if ok else "FAIL"}]')
    return allok
def g1(tag, a):
    k = a / AC; ok = abs(np.log10(k / .5)) <= .05; P(f' {tag} kappa_eff {k:.4g} ({np.log10(k / .5):+.3f} dex) [{"PASS" if ok else "FAIL"} G1]'); return ok
def g4(tag, cur):
    la = np.log10([fit_a(g.gb, c) for g, c in zip(GS, cur)]); s = la[HOST].std(); ok = s <= .1
    P(f' {tag} G4 per-galaxy fit_a over {HOST.sum()} hosts log M200 11-12.5: rms {s:.3f} dex (all 171: {la.std():.3f}) [{"PASS" if ok else "FAIL"} G4]'); return ok
def g5(tag, cur, gns):
    gt, gn = np.concatenate(cur), np.concatenate(gns); f = np.median((gt - gn) / gn); ab = np.median((gt - gn) / A0); ok = f >= .1
    P(f' {tag} G5 median (g - g_N)/g_N {f:.4g}, median (g - g_N)/a0 {ab:.4g} [{"PASS" if ok else "FAIL"} G5]'); return ok
def unseen(cur_od): return rms(np.log10(np.concatenate(cur_od)) - np.log10(np.concatenate([g.gl for g in OD])))
def halo(g, dn=0.):
    M = m200_of(g.Ms, dn); c = np.interp(np.log10(M), LM, CG); fb = min(g.Mb / M, .5)
    mh, R = nfw_m(g.r, M, c); rs = R / c; return g.gb + G * (1 - fb) * mh / g.r**2, M, c, fb, rs
def lsfit(model, gs, x0, lo, hi):
    gt = np.concatenate([g.gl for g in gs]); res = lambda p: np.log10(np.concatenate(model(gs, p)[0])) - np.log10(gt); best = None
    for s in range(4):
        st = np.array(x0, float) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        r = least_squares(res, np.clip(st, np.array(lo) + 1e-6, np.array(hi) - 1e-6), bounds=(lo, hi), diff_step=1e-3, max_nfev=200)
        if best is None or r.cost < best.cost: best = r
    atb = [i for i, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
    return best.x, atb
def row(tag, model, p, nk, extra=''):
    cur, gns = model(GS, p); grade(tag, cur, f'({nk} knobs{extra})'); fa = fit_a(ALLB, np.concatenate(cur))
    ok1 = g1(tag, fa); ok4 = g4(tag, cur); ok5 = g5(tag, cur, gns); return cur, gns, ok1, ok4, ok5
def holdout(tag, model, p, x0, lo, hi):
    ph, atb = lsfit(model, EV, p, lo, hi); u = unseen(model(OD, ph)[0])
    P(f' {tag} holdout tuned on GS[::2] {np.round(ph, 4).tolist()} (at bound {atb}) unseen rms {u:.4f} [{"PASS" if u <= .025 else "FAIL"}]'); return u

# ======================= (a) Vainshtein: DGP normal branch / cubic Galileon
P('\n######## (a) Vainshtein screening: DGP normal branch, cubic Galileon (spherical, enclosed mass)')
def ydgp(gN, r, rc, B):
    Z = 16 * gN * rc**2 * B**2 / (c_**2 * r); return 2 * B * gN / (np.sqrt(1 + Z) + 1)
yt = ydgp(np.array([1e-30, 1e-6]), np.array([1e40, 1.]), 1e26, .1)  # control fixed: r 1e40 m so that Z << 1 (was r 1 m, Z 1.8e4: not unscreened)
P(f'control: unscreened y/g_N {yt[0] / 1e-30:.6f} (-> 1/(3 beta) = B = 0.1); deep y {yt[1]:.6e} vs c sqrt(g_N r)/(2 r_c) {c_ * np.sqrt(1e-6) / 2e26:.6e}')
beta0 = 1 + 2 * 1. * (1 - .5 * OM); B0 = 1 / (3 * beta0); RC0 = c_ / H0
P(f'nDGP natural: r_c H0 = 1, beta(0) = 1 + 2 (1 - Om/2) = {beta0:.4f}, unscreened boost B = 1/(3 beta) {B0:.4f}')
def dgp(gs, p, hal=False):
    rc, B = 10**p[0] * c_ / H0, 10**p[1]; out, gns = [], []
    for g in gs:
        gN = halo(g, p[2])[0] if hal else g.gb
        out.append(gN + ydgp(gN, g.r, rc, B)); gns.append(gN)
    return out, gns
def vains_scales(tag, rc, B):
    for rk in (1, 10, 30): P(f' {tag} deep-Vainshtein scale a_V(r) = c^2 r/(4 r_c^2) at {rk} kpc: {c_**2 * rk * kpc / (4 * rc**2):.3e} = {c_**2 * rk * kpc / (4 * rc**2) / AC:.3e} AC')
    gv = []
    for g in GS:
        M = g.mbtot; rv = (16 * G * M * rc**2 * B**2 / c_**2)**(1 / 3); gv.append(G * M / rv**2)
    gv = np.log10(gv); P(f' {tag} g_N at the Vainshtein radius (baryonic M): median {10**np.median(gv) / AC:.3e} AC; rms over hosts {gv[HOST].std():.3f} dex [{"PASS" if gv[HOST].std() <= .1 else "FAIL"} G4 on g_N(r_V)]; slope with log M_b {np.polyfit(np.log10([g.mbtot for g in GS]), gv, 1)[0]:.3f}')
    rmw = (16 * G * 6.5e10 * Msun * rc**2 * B**2 / c_**2)**(1 / 3); P(f' {tag} Vainshtein radius of a 6.5e10 Msun baryonic galaxy {rmw / kpc:.4g} kpc')
def cassini_dgp(tag, rc, B):
    gS = GMS / RSAT**2; yS = ydgp(gS, RSAT, rc, B); gL = GMS / RLIMB**2; yL = ydgp(gL, RLIMB, rc, B); gam = 2 * yL / (gL + yL)
    gE = GME / RMOON**2; yE = ydgp(gE, RMOON, rc, B); okS = yS < 1e-3 * A0; okL = gam < 2.3e-5
    P(f' {tag} Cassini: y at Saturn {yS:.3e} = {yS / A0:.3g} a0 [{"PASS" if okS else "FAIL"} <1e-3 a0]; |gamma-1| at 1.6 R_sun {gam:.3e} [{"PASS" if okL else "FAIL"}]; Moon (Earth alone) y/g_N {yE / gE:.2e} (LLR-scale ~1e-11, provisional) => {"PASS" if okS and okL else "FAIL"} Cassini')
    return okS and okL
pn = [0., np.log10(B0), 0.]
row('GD0 nDGP natural r_c H0 = 1, no halo', dgp, pn, 0, f', beta {beta0:.3f}'); vains_scales('GD0', RC0, B0); cassini_dgp('GD0', RC0, B0)
row('GD0h nDGP natural + LCDM halo', lambda gs, p: dgp(gs, p, True), pn, 0)
P(f' G2 (a): r_c, B Lagrangian constants: slope 0 natively [FAIL]; with r_c = c/H0 imposed a_V ~ H0^2 ~ rho_crit: slope 1 at fixed Omega [FAIL]')
lo, hi = [-6, -3], [1, 1.5]
p, atb = lsfit(dgp, GS, [-2.5, 0.], lo, hi); rc, B = 10**p[0] * c_ / H0, 10**p[1]
P(f'\nGA1 knobs log10(r_c H0/c) {p[0]:.4f} (r_c {rc / kpc / 1e3:.4g} Mpc), log10 B {p[1]:.4f} (B {B:.4g}, beta {1 / (3 * B):.4g}); at bound {atb}')
row('GA1 DGP/Galileon fit, no halo', dgp, [p[0], p[1], 0.], 2); vains_scales('GA1', rc, B); cassini_dgp('GA1', rc, B)
holdout('GA1', dgp, p, p, lo, hi)
P(f' r_c needed for a_V(10 kpc) = 0.5 AC: {c_ * np.sqrt(10 * kpc / (2 * AC)) / kpc / 1e3:.4g} Mpc = {c_ * np.sqrt(10 * kpc / (2 * AC)) * H0 / c_:.4g} c/H0')
dgph = lambda gs, p: dgp(gs, p, True)
lo, hi = [-6, -3, -.54], [1, 1.5, .54]
p, atb = lsfit(dgph, GS, [-2.5, 0., 0.], lo, hi); rc, B = 10**p[0] * c_ / H0, 10**p[1]
P(f'\nGH1 knobs log10(r_c H0/c) {p[0]:.4f} (r_c {rc / kpc / 1e3:.4g} Mpc), log10 B {p[1]:.4f}, dn {p[2]:+.4f}; at bound {atb}')
row('GH1 DGP/Galileon fit + LCDM halo', dgph, p, 3); cassini_dgp('GH1', rc, B)
holdout('GH1', dgph, p, p, lo, hi)
P('\n(a) GT readings:'); gt_const('(a) r_c constant')
P(' (a) nDGP own background = LCDM expansion (Schmidt 2009): rho_DE flat, constant r_c flat: trivial PASS, not tracking')
res = {z: np.log10(Etrk(z)) + np.log10(Etrk(z)) for z in ZB}; P(' (a) cubic-Galileon tracker, coefficient ~ H(z): a(z)/a(0) = E ' + ', '.join(f'{z}: {Etrk(z):.3f}' for z in ZB) + '; GT residuals ' + ', '.join(f'{z}: {v:+.4f}' for z, v in res.items()) + f' [{"PASS" if all(abs(v) <= .05 for v in res.values()) else "FAIL"}]; G3 {"PASS" if all(ZB[z][0] <= Etrk(z) <= ZB[z][1] for z in ZB) else "FAIL"}')
res = {z: np.log10(Etrk(z)) for z in ZB}; P(' (a) cubic-Galileon tracker, constant coefficient: GT residuals ' + ', '.join(f'{z}: {v:+.4f}' for z, v in res.items()) + f' [{"PASS" if all(abs(v) <= .05 for v in res.values()) else "FAIL"}]')
P(f'[{time.time() - T0:.0f} s]')

# ======================= (b) beyond-Horndeski / DHOST Vainshtein breaking
P('\n######## (b) beyond-Horndeski / DHOST: dPhi/dr = G M/r^2 + Upsilon1 G M\'\'/4 inside matter')
MBPP = [np.gradient(np.gradient(g.mb, g.r), g.r) for g in GS]
def mpp_halo(g, dn):
    gN, M, c, fb, rs = halo(g, dn); rhos = (1 - fb) * M * Msun / (4 * np.pi * rs**3 * mu(c)); x = g.r / rs
    rho = rhos / (x * (1 + x)**2); drho = -rho * (1 + 3 * x) / (g.r * (1 + x)); return gN, 4 * np.pi * (2 * g.r * rho + g.r**2 * drho)
def hb(gs, p, hal=False):
    U = p[0]; out, gns = [], []
    for g in gs:
        i = GS.index(g); mpp = MBPP[i]
        if hal: gN, mh = mpp_halo(g, p[1]); mpp = mpp + mh
        else: gN = g.gb
        out.append(np.maximum(gN + U * G * mpp / 4, .01 * gN)); gns.append(gN)
    return out, gns
hbh = lambda gs, p: hb(gs, p, True)
fr = np.concatenate([G * m / 4 / g.gb for m, g in zip(MBPP, GS)]); P(f'baryon M\'\' term G M_b\'\'/(4 g_b) per unit Upsilon1: median {np.median(fr):+.4f}, median |.| {np.median(abs(fr)):.4f}, p05/p95 {np.percentile(fr, 5):+.3f}/{np.percentile(fr, 95):+.3f}')
for U in (.027, -.11, -.6):
    row(f'HB0 Upsilon1 {U}, no halo', hb, [U], 0); row(f'HB0h Upsilon1 {U}, + LCDM halo', hbh, [U, 0.], 0)
p, atb = lsfit(hb, GS, [0.], [-2 / 3], [2.]); P(f'\nHA1 Upsilon1 {p[0]:.4f} at bound {atb} (allowed -2/3 < U < 0.027, provisional)')
row('HA1 Upsilon1 fit, no halo', hb, p, 1); holdout('HA1', hb, p, p, [-2 / 3], [2.])
p, atb = lsfit(hbh, GS, [0., 0.], [-2 / 3, -.54], [2., .54]); P(f'\nHH1 Upsilon1 {p[0]:.4f}, dn {p[1]:+.4f}, at bound {atb}')
row('HH1 Upsilon1 + dn, LCDM halo', hbh, p, 2); holdout('HH1', hbh, p, p, [-2 / 3, -.54], [2., .54])
w0, wa = BGS['B1']; Oz = {z: OL * rde_ratio(z, w0, wa) / (OM * (1 + z)**3 + OL * rde_ratio(z, w0, wa)) for z in ZB}
P(' (b) no acceleration scale: G2 0 natively [FAIL]; GT: nothing to track [FAIL]; if alpha_i ~ Omega_DE(a), Upsilon1(z)/Upsilon1(0) in B1 = ' + ', '.join(f'{z}: {Oz[z] / OL:.3f}' for z in ZB) + ' (dimensionless fraction, information only)')
P(' (b) Cassini: outside sources Vainshtein holds, extra force 0 at Saturn and the limb ray [PASS folder gate]; operative limits are stellar (-2/3 < U < 0.027, provisional)')
P(f'[{time.time() - T0:.0f} s]')

# ======================= (c1) Mashhoon non-local gravity
P('\n######## (c1) non-local gravity, Mashhoon kernel (Rahvar & Mashhoon 2014 Eq. 36, a_k -> 0), spherical shells')
lx = np.linspace(np.log(1e-14), np.log(1e8), 220001); X = np.exp(lx); dl = lx[1] - lx[0]
h = -np.expm1(-X) - .5 * X * np.exp(-X)
I = h / X; Pt = np.concatenate([np.cumsum(((I[1:] + I[:-1]) * .5 * dl)[::-1])[::-1], [0.]]) + 1 / X[-1]
J = Pt * X**2; Qt = np.concatenate([[Pt[0] * X[0]**2 / 2], Pt[0] * X[0]**2 / 2 + np.cumsum((J[1:] + J[:-1]) * .5 * dl)])
sel = slice(None, None, 10); lnP = CubicSpline(lx[sel], np.log(Pt[sel])); lnQ = CubicSpline(lx[sel], np.log(Qt[sel]))
def Pf(x): return np.exp(lnP(np.log(np.clip(x, 1e-14, 1e8))))
def Qf(x): return np.exp(lnQ(np.log(np.clip(x, 1e-14, 1e8))))
GK = G * Msun / kpc**2
def shellg(r, s, m, al, mu_):
    """inward extra acceleration (SI) at radii r [kpc] from shells s [kpc] of mass m [Msun]; arrays broadcast."""
    up, um = r + s, np.abs(r - s); Psi = lambda u: al / mu_ * Qf(mu_ * u); phi = lambda u: al * mu_ * Pf(mu_ * u)
    S = (Psi(up) - Psi(um)) / (2 * r * s); dS = -S / r + (phi(up) * up - np.sign(r - s) * phi(um) * um) / (2 * r * s)
    return -GK * (m * dS).sum(axis=-1)
def pointx(r, M, al, mu_): x = mu_ * r; return GK * M * al * (-np.expm1(-x) - .5 * x * np.exp(-x)) / r**2
for (r, s) in ((10., .1), (10., 1.), (3., .05)):
    a = shellg(np.array([[r]]), np.array([[s]]), 1e10, 10.94, .059)[0]; b = pointx(r, 1e10, 10.94, .059)
    P(f'control: shell s {s} kpc at r {r} kpc vs point mass Eq. 36: ratio {a / b:.6f}')
P(f'control: alpha 0 gives {shellg(np.array([[10.]]), np.array([[1.]]), 1e10, 0., .059)[0]:.1e}; shell interior r 0.5 s 1.0 extra {shellg(np.array([[.5]]), np.array([[1.]]), 1e10, 10.94, .059)[0]:.3e} (non-zero: no shell theorem)')
SH = []
for g in GS:
    rk = g.r / kpc; Mb = g.mb / Msun; k = np.arange(1, 6) / 5
    s = np.concatenate([rk[0] * k, .5 * (rk[1:] + rk[:-1])]); m = np.concatenate([Mb[0] * (k**3 - (k - .2)**3), np.diff(Mb)])
    SH.append((rk[:, None], s[None, :], m[None, :]))
nneg = sum((sh[2] < 0).sum() for sh in SH); P(f'shells: {sum(sh[2].size for sh in SH)} total, {nneg} with negative dM kept signed')
def nl(gs, p):
    al, mu_ = 10**p[0], 10**p[1]; out = []
    for g in gs:
        rk, s, m = SH[GS.index(g)]; out.append(np.maximum(g.gb + shellg(rk, s, m, al, mu_), .01 * g.gb))
    return out, [g.gb for g in gs]
def nl1(gs, p): mu_ = .059; return nl(gs, [np.log10(2 / (10**p[0] * mu_)), np.log10(mu_)])
AL, MU = 10.94, .059; P(f'published: alpha {AL}, mu {MU} kpc^-1, lambda0 = 2/(alpha mu) {2 / (AL * MU):.3f} kpc')
def nlscales(tag, al, mu_):
    lam = 2 / (al * mu_); ga = np.log10([G * g.mbtot / (lam * kpc)**2 for g in GS])
    P(f' {tag} implied G M_b/lambda0^2: median {10**np.median(ga) / AC:.3e} AC, rms over hosts {ga[HOST].std():.3f} dex [{"PASS" if ga[HOST].std() <= .1 else "FAIL"} G4 on this scale]')
    vf = []; ms = []
    for g in GS:
        rk, s, m = SH[GS.index(g)]; gt = g.gb[-1] + shellg(rk[-1:], s, m, al, mu_)[0]; vf.append(np.sqrt(gt * g.r[-1])); ms.append(g.mbtot)
    P(f' {tag} BTFR slope d log M_b / d log V(last point) of the model {np.polyfit(np.log10(vf), np.log10(ms), 1)[0]:.3f} (law ~4; mu r << 1 analytic 2)')
def cassini_nl(tag, al, mu_):
    lam = 2 / (al * mu_) * kpc; m = mu_ / kpc
    yS = GMS * al * (-np.expm1(-m * RSAT) - .5 * m * RSAT * np.exp(-m * RSAT)) / RSAT**2; gL = GMS / RLIMB**2
    yL = GMS * al * (-np.expm1(-m * RLIMB) - .5 * m * RLIMB * np.exp(-m * RLIMB)) / RLIMB**2; gam = 2 * yL / (gL + yL)
    yE = GME * al * (-np.expm1(-m * RMOON) - .5 * m * RMOON * np.exp(-m * RMOON)) / RMOON**2; okS = yS < 1e-3 * A0; okL = gam < 2.3e-5
    P(f' {tag} Cassini (a_k -> 0): y at Saturn {yS:.3e} = {yS / A0:.3g} a0 [{"PASS" if okS else "FAIL"}], check G M/(lambda0 r) {GMS / (lam * RSAT):.3e}; |gamma-1| limb {gam:.3e} [{"PASS" if okL else "FAIL"}]; Moon y/g_N {yE / (GME / RMOON**2):.2e} => {"PASS" if okS and okL else "FAIL"} Cassini')
    ak = 1e-3 * lam; y1 = GMS * RSAT / (3 * lam * ak**2); y2 = GMS / (2 * lam * ak)
    P(f' {tag} with a_k = 1e-3 lambda0 ({ak / kpc:.3g} kpc): q1 extra at Saturn ~ G M r/(3 lambda0 a_k^2) {y1:.3e} = {y1 / A0:.2e} a0 [{"PASS" if y1 < 1e-3 * A0 else "FAIL"}]; q2 ~ G M/(2 lambda0 a_k) {y2:.3e} = {y2 / A0:.2e} a0 [{"PASS" if y2 < 1e-3 * A0 else "FAIL"}] (a_k not fitted by SPARC; galaxy rows use a_k -> 0)')
pp = [np.log10(AL), np.log10(MU)]
row('NL0 Mashhoon published (alpha 10.94, mu 0.059/kpc)', nl, pp, 0); nlscales('NL0', AL, MU); cassini_nl('NL0', AL, MU)
p, atb = lsfit(nl1, GS, [np.log10(3.1)], [-1], [3]); lam = 10**p[0]
P(f'\nNL1 lambda0 {lam:.4g} kpc (mu fixed 0.059, alpha {2 / (lam * MU):.4g}), at bound {atb}')
row('NL1 lambda0 fit', nl1, p, 1); nlscales('NL1', 2 / (lam * MU), MU); cassini_nl('NL1', 2 / (lam * MU), MU); holdout('NL1', nl1, p, p, [-1], [3])
p, atb = lsfit(nl, GS, pp, [-2, -4], [3, 1]); al, mu_ = 10**p[0], 10**p[1]
P(f'\nNL2 alpha {al:.4g}, mu {mu_:.4g} kpc^-1 (lambda0 {2 / (al * mu_):.4g} kpc), at bound {atb}')
row('NL2 alpha, mu fit', nl, p, 2); nlscales('NL2', al, mu_); cassini_nl('NL2', al, mu_); holdout('NL2', nl, p, p, [-2, -4], [3, 1])
P(' (c1) G2: lambda0, mu Lagrangian constants, slope 0 [FAIL]; G3 ratio 1 trivial'); gt_const('(c1) lambda0 constant')

# ======================= (c2) Deser-Woodard / RR analytic
P('\n######## (c2) Deser-Woodard / RR non-local cosmology (analytic)')
m_rr = .28 * H0; P(f' RR m ~ 0.28 H0 (from memory): (m r/c)^2 at 10 kpc {(m_rr * 10 * kpc / c_)**2:.2e} => G5 FAIL; Deser-Woodard f(box^-1 R) fixed by the chosen expansion history (G2 by construction only), no static acceleration scale (from memory); non-local MOND realisations insert a0 by hand')
P(f'\nruntime {time.time() - T0:.0f} s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
P('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
