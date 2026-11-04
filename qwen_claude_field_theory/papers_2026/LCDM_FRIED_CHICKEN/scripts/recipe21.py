"""A19: velocity-dependent SIDM, SIDM plus halo knobs, Ren-style per-galaxy SIDM, warm dark matter, per ../FROZEN_A19.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
t00 = time.time()
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
TY = 3.156e16; T10 = 10 * TY; RG = np.logspace(-3, 0, 100); NS, NR = 20, 28; SG = np.logspace(np.log10(.25), np.log10(1.5), NS); DR0 = np.linspace(0, 5, NR) * np.log(10)
print(f'c sqrt(G rho_DE) {AC:.4e} m/s^2, a0 {A0:.4e}')
# <sigma v> over the relative-speed Maxwellian (1D dispersion sqrt2 sigma0), x = v/sigma_r
XQ = np.linspace(1e-4, 8, 4000); FQ = np.sqrt(2 / np.pi) * XQ**2 * np.exp(-XQ**2 / 2); LU = np.linspace(-5, 5, 501)
FU = np.array([getattr(np, "trapezoid", getattr(np, "trapz", None))(XQ / (1 + (10**u * XQ)**4) * FQ, XQ) for u in LU])
def svm(s0, w=None):
    """<sigma v>/m in m^3/kg/s as a function of sigma0 [m/s]; s0 in cm^2/g, w in km/s (None = constant)."""
    if w is None: return lambda s: s0 * .1 * 4 * s / np.sqrt(np.pi)
    return lambda s: s0 * .1 * np.sqrt(2) * s * np.interp(np.log10(np.sqrt(2) * s / (w * 1e3)), LU, FU)
def sbar(g): return g.Mb / (g.Rd / kpc)**2 / 1e6 / 100
GAM = {'S12': (15., .3), 'B16': (60., .17)}
def halo(g, dn=0., dc=0., sc=0., lmhm=None, gam='S12'):
    M = m200_of(g.Ms, dn); c = float(cflat(M, dc, 0.)) * sbar(g)**sc
    if lmhm is not None: g1, g2 = GAM[gam]; c *= (1 + g1 * 10**lmhm / M)**(-g2)
    return M, c
def mbfun(g):
    lr, lm = np.log(g.r), np.log(np.maximum(g.mb, 1e-30))
    return lambda r: np.where(r < g.r[0], g.mb[0] * (r / g.r[0])**2, np.where(r > g.r[-1], g.mb[-1], np.exp(np.interp(np.log(r), lr, lm))))
def integ(lrho0, s, r, B):
    """Euler isothermal Jeans, A15 step; arrays broadcast over trajectories, r and B shape (..., n)."""
    n = r.shape[-1]; dr = np.diff(r, axis=-1, prepend=0); lrho = lrho0.copy(); m = np.zeros_like(lrho); s2 = s**2; Ms = []
    for i in range(n):
        m = m + 4 * np.pi * r[..., i]**2 * np.exp(lrho) * dr[..., i]; Ms.append(m)
        if i + 1 < n: lrho = lrho - G * (B[..., i] + m) / r[..., i]**2 / s2 * (r[..., i + 1] - r[..., i])
    return lrho, np.stack(Ms, -1)
def core(mb, M, c, fb, sv, T=T10, rhoc=RHOC, rd=None):
    """SIDM isothermal core matched to a (1-fb) NFW at r1. Returns dark mass at rd, sigma0, r1, mismatch, NFW rs."""
    R = (3 * M * Msun / (800 * np.pi * rhoc))**(1 / 3); rs = R / c; rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); w = 1 - fb
    rN = lambda r: w * rhos / ((r / rs) * (1 + r / rs)**2); mN = lambda r: w * M * Msun * mu(r / rs) / mu(c)
    xs = np.logspace(-4, np.log10(50), 400) * rs; lrN = np.log(rN(xs)); Vmax = np.sqrt(G * M * Msun * mu(2.163) / mu(c) / (2.163 * rs))
    def r1of(s):
        lk = -np.log(np.maximum(sv(s) * T, 1e-300)); return np.exp(np.interp(lk, lrN[::-1], np.log(xs)[::-1]))
    S = Vmax * SG; r1 = r1of(S); r = r1[:, None] * RG[None, :]; B = mb(r)
    lr0 = np.log(rN(r1))[:, None] + DR0[None, :]
    lre, Mm = integ(lr0, S[:, None], r[:, None, :] * np.ones((1, NR, 1)), B[:, None, :] * np.ones((1, NR, 1)))
    f = lre - np.log(rN(r1))[:, None]; h = np.log(Mm[..., -1]) - np.log(mN(r1))[:, None]; q = f**2 + h**2
    near = np.argwhere(q < .05)
    if len(near): j, k = min(near, key=lambda jk: (lr0[jk[0], jk[1]], q[jk[0], jk[1]]))
    else: j, k = np.unravel_index(np.argmin(q), q.shape)
    x = np.array([lr0[j, k], np.log(S[j])]); d = 1e-3
    def F(X):
        ss = np.exp(X[:, 1]); rr1 = r1of(ss); rr = rr1[:, None] * RG[None, :]; le, Mp = integ(X[:, 0], ss, rr, mb(rr))
        return np.stack([le - np.log(rN(rr1)), np.log(Mp[:, -1]) - np.log(mN(rr1))], -1)
    for _ in range(12):
        Fx = F(np.array([x, x + [d, 0], x + [0, d]])); J = np.stack([(Fx[1] - Fx[0]) / d, (Fx[2] - Fx[0]) / d], -1)
        if np.abs(Fx[0]).max() < 1e-3: break
        try: st = -np.linalg.solve(J, Fx[0])
        except np.linalg.LinAlgError: break
        x = x + st * min(1., .5 / max(np.abs(st).max(), 1e-12))
    lr0s, s = x[0], np.exp(x[1])
    r1s = float(r1of(np.array([s]))[0]); rr = r1s * RG; le, Mp = integ(np.array([lr0s]), np.array([s]), rr[None, :], mb(rr)[None, :])
    mis = max(abs(le[0] - np.log(rN(r1s))), abs(np.log(Mp[0, -1] / mN(r1s))))
    if rd is None: return s, r1s, mis, rs
    md = np.where(rd < r1s, np.exp(np.interp(np.log(rd), np.log(rr), np.log(np.maximum(Mp[0], 1e-300)))), mN(rd))
    return md, s, r1s, mis, rs
MBF = [mbfun(g) for g in GS]
def model(g, i, sv, dn=0., dc=0., sc=0., lmhm=None, gam='S12'):
    M, c = halo(g, dn, dc, sc, lmhm, gam); fb = min(g.Mb / M, .5)
    if sv is None:
        return g.gb + G * (1 - fb) * nfw_m(g.r, M, c)[0] / g.r**2, np.nan, np.nan, 0.
    md, s, r1, mis, _ = core(MBF[i], M, c, fb, sv, rd=g.r); return g.gb + G * md / g.r**2, s, r1, mis
IDX = {id(g): i for i, g in enumerate(GS)}
def run(S, kfun):
    out = [model(g, IDX[id(g)], *kfun) for g in S]; return out
def rms(S, out): return np.sqrt((np.concatenate([np.log10(o[0]) - np.log10(g.gl) for g, o in zip(S, out)])**2).mean())
def tune(S, mk, x0s, lo, hi, nfev):
    fn = lambda k: np.concatenate([np.log10(o[0]) - np.log10(g.gl) for g, o in zip(S, run(S, mk(k)))]); best = None
    for x0 in x0s:
        r = least_squares(fn, np.clip(x0, np.array(lo) + 1e-4, np.array(hi) - 1e-4), bounds=(lo, hi), max_nfev=nfev, diff_step=.05)
        if best is None or r.cost < best.cost: best = r
    return best.x
def atb(x, lo, hi): return [i for i, (v, a, b) in enumerate(zip(x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
def kprint(tag, out, extra=''):
    s = np.array([o[1] for o in out]); r1 = np.array([o[2] for o in out]); ok = np.isfinite(s) & (r1 > 0); gc = s[ok]**2 / r1[ok]
    print(f' {tag} K1 core g_c = sigma0^2/r1: median {np.median(gc) / A0:.3f} a0, rms {np.log10(gc).std():.3f} dex over {ok.sum()}, kappa_eff {np.median(gc) / AC:.3f} [{"PASS" if abs(np.log10(np.median(gc) / AC / .5)) <= .05 else "FAIL"}]; unmatched cores {sum(o[3] > .03 * np.log(10) for o in out)} of {len(out)} {extra}')
def kz(tag, sv):
    """K1 at z for a dark-only halo at the median SPARC M200 (no baryons)."""
    Mm = np.median([m200_of(g.Ms) for g in GS]); z0 = None; res = {}
    for z in (0., 1., 1.5, 2.33):
        rc = cos.rho_c(z) * cos.h**2 * Msun / kpc**3; cz = float(CM.concentration(Mm * cos.h, '200c', z, model='diemer19')); T = min(10., cos.age(z)) * TY
        s, r1, mis, _ = core(lambda r: np.full_like(r, 1e-30), Mm, cz, 0., sv, T=T, rhoc=rc); res[z] = s**2 / r1
    rr = {z: res[z] / res[0.] for z in ZB}; ok = all(ZB[z][0] <= rr[z] <= ZB[z][1] for z in ZB)
    print(f' {tag} K1 z-evolution, dark-only halo log M200 {np.log10(Mm):.2f}: g_c(0) {res[0.] / A0:.3f} a0; ' + ', '.join(f'{z}: {x:.3f}' for z, x in rr.items()) + f' [{"PASS" if ok else "FAIL"} band]')
def k2(tag, sm):
    ax = G / (sm * .1); print(f' {tag} K2 a_x = G/(sigma/m) at {sm:.3g} cm^2/g: {ax / A0:.3f} a0, kappa_eff {ax / AC:.3f} [{"PASS" if abs(np.log10(ax / AC / .5)) <= .05 else "FAIL"}]; constant of the particle, z ratio 1 [PASS band by construction]')
def holdout(mk, x0s, lo, hi, nfev):
    k = tune(GS[::2], mk, x0s, lo, hi, nfev); e = rms(GS[1::2], run(GS[1::2], mk(k)))
    print(f' holdout: knobs on GS[::2] {np.round(k, 3).tolist()}, unseen GS[1::2] rms to law {e:.4f} dex [{"PASS" if e <= .025 else "FAIL"} <= 0.025]', flush=True); return e
def head(t): print(f'\n######## {t}  ({time.time() - t00:.0f} s)', flush=True)

head('C0 control: fast solver, base halo, sigma/m 1 cm^2/g constant, against A15 U3 0.1212')
out = run(GS, (svm(1.),)); e = grade('C0', [o[0] for o in out]); kprint('C0', out)
print(f' C0 {"PASS" if abs(e - .1212) <= .01 else "FAIL"}: |{e:.4f} - 0.1212| = {abs(e - .1212):.4f} <= 0.01')
gt = np.concatenate([o[0] for o in out]); dd = np.log10(gt) - np.log10(ALLL); bb = np.floor(np.log10(ALLB) * 2) / 2
A15B = {-12.: .069, -11.5: .053, -11.: .042, -10.5: .007, -10.: .029, -9.5: .063, -9.: .078}
print(f' C0 added after the first-run bug (reported, not a frozen gate): mean residual to law {dd.mean():+.4f}, worst bin difference to A15 U3 bins {max(abs(dd[bb == x].mean() - v) for x, v in A15B.items()):.4f} dex')

head('(a) velocity-dependent SIDM, sigma/m = s0/(1+(v/w)^4), knobs log s0 [cm^2/g], log w [km/s]')
LOa, HIa = [-1, 1], [2, 3]; mka = lambda k: (svm(10**k[0], 10**k[1]),)
ka = tune(GS, mka, [[0., 2.]], LOa, HIa, 12); outa = run(GS, mka(ka))
grade('(a) v-dependent SIDM', [o[0] for o in outa], f'(2 knobs: s0 {10**ka[0]:.3g} cm^2/g, w {10**ka[1]:.3g} km/s; at bound {atb(ka, LOa, HIa)})'); kprint('(a)', outa)
k2('(a) at s0', 10**ka[0]); k2('(a) at v = w', 10**ka[0] / 2)
print(f' (a) K3 a_w = w/t: {10**ka[1] * 1e3 / T10 / A0:.2e} a0, kappa_eff {10**ka[1] * 1e3 / T10 / AC:.2e} [FAIL unless within 0.05 dex of 0.5]; z: t(z) = age(z) capped at 10 Gyr gives ' + ', '.join(f'{z}: {10 / min(10., cos.age(z)):.3f}' for z in ZB))
kz('(a)', mka(ka)[0]); ha = holdout(mka, [list(ka)], LOa, HIa, 8)

head('(b) v-dependent SIDM + SHMR dn + c norm dc + compactness exponent s_c')
LOb, HIb = [-1, 1, -.3, -.3, -.5], [2, 3, .3, .3, .5]; mkb = lambda k: (svm(10**k[0], 10**k[1]), k[2], k[3], k[4])
kb = tune(GS, mkb, [list(ka) + [0, 0, 0]], LOb, HIb, 12); outb = run(GS, mkb(kb))
grade('(b) v-dep SIDM + halo knobs', [o[0] for o in outb], f'(5 knobs {np.round(kb, 3).tolist()}; at bound {atb(kb, LOb, HIb)})'); kprint('(b)', outb)
k2('(b) at s0', 10**kb[0]); print(f' (b) K3 a_w = w/t: {10**kb[1] * 1e3 / T10 / A0:.2e} a0, kappa_eff {10**kb[1] * 1e3 / T10 / AC:.2e}')
kz('(b) (halo knobs off)', mkb(kb)[0]); hb = holdout(mkb, [list(kb)], LOb, HIb, 8)

head('(c) Ren et al. 2019 style: per-galaxy dlogM200 +-0.6, dlogc +-0.22, global constant sigma/m from {0.5,1,3,10}')
def pg(i, g, sv, sel=None):
    sel = slice(None) if sel is None else sel; M0 = m200_of(g.Ms); c0 = float(cflat(M0, 0., 0.)); fb0 = g.Mb
    def gt(k):
        M = M0 * 10**k[0]; c = c0 * 10**k[1]; fb = min(g.Mb / M, .5); md = core(MBF[i], M, c, fb, sv, rd=g.r)
        return g.gb + G * md[0] / g.r**2, md
    fn = lambda k: (np.log10(gt(k)[0]) - np.log10(g.gl))[sel]
    r = least_squares(fn, [0., 0.], bounds=([-.6, -.22], [.6, .22]), max_nfev=8, diff_step=.05); y, md = gt(r.x)
    return y, md[1], md[2], md[3], r.x
PC = {}
for sm in (.5, 1., 3., 10.):
    PC[sm] = [pg(i, g, svm(sm)) for i, g in enumerate(GS)]
    print(f'  sigma/m {sm}: rms to law all {rms(GS, PC[sm]):.4f}, even galaxies {rms(GS[::2], PC[sm][::2]):.4f}  ({time.time() - t00:.0f} s)', flush=True)
smc = min(PC, key=lambda s: rms(GS, PC[s])); outc = PC[smc]; kk = np.array([o[4] for o in outc])
grade(f'(c) per-galaxy M200, c; sigma/m {smc} cm^2/g', [o[0] for o in outc], f'(343 parameters: 2 x 171 + 1)'); kprint('(c)', outc)
nb = int((np.isclose(abs(kk[:, 0]), .6, atol=6e-4)).sum() + (np.isclose(abs(kk[:, 1]), .22, atol=2.2e-4)).sum())
print(f' (c) per-galaxy at bound {nb} of 342; dlogM200 p16/50/84 {np.round(np.percentile(kk[:, 0], [16, 50, 84]), 3).tolist()}, dlogc {np.round(np.percentile(kk[:, 1], [16, 50, 84]), 3).tolist()}')
k2('(c)', smc); kz('(c)', svm(smc))
sme = min(PC, key=lambda s: rms(GS[::2], PC[s][::2]))
pc0 = run(GS[1::2], (svm(sme),)); e0 = rms(GS[1::2], pc0)
print(f' holdout (gated): sigma/m on GS[::2] = {sme}; GS[1::2] at prior centre (unseen) rms to law {e0:.4f} [{"PASS" if e0 <= .025 else "FAIL"} <= 0.025]')
print(f' holdout (not gated, not unseen): GS[1::2] refitted per galaxy at {sme}: {rms(GS[1::2], PC[sme][1::2]):.4f}')
rh = [pg(i, g, svm(smc), np.arange(len(g.r)) % 2 == 1) for i, g in enumerate(GS)]
er = np.sqrt((np.concatenate([(np.log10(o[0]) - np.log10(g.gl))[::2] for g, o in zip(GS, rh)])**2).mean())
print(f' radius holdout (not gated): per-galaxy fit on odd radii, even radii rms to law {er:.4f} dex', flush=True)

head('(d) warm dark matter: c_WDM/c_CDM = (1 + g1 M_hm/M)^-g2; S12 (15, 0.3), B16 (60, 0.17), FROM MEMORY, unverified')
def k4(tag, lm):
    R = (3 * 10**lm * Msun / (800 * np.pi * RHOC))**(1 / 3); a = G * 10**lm * Msun / R**2
    print(f' {tag} K4 g200(M_hm) at log M_hm {lm:.2f}: {a / A0:.2e} a0, kappa_eff {a / AC:.2e} [{"PASS" if abs(np.log10(a / AC / .5)) <= .05 else "FAIL"}]; at fixed M_hm g200 goes as rho_c(z)^(2/3): ' + ', '.join(f'{z}: {(cos.rho_c(z) / cos.rho_c(0))**(2 / 3):.3f}' for z in ZB))
OD = {}
for gm in ('S12', 'B16'):
    mkd = lambda k, gm=gm: (None, 0., 0., 0., k[0], gm)
    kd = tune(GS, mkd, [[9.], [7.]], [6], [12], 15); outd = run(GS, mkd(kd)); OD[gm] = kd
    grade(f'(d1) WDM {gm}, NFW no core', [o[0] for o in outd], f'(1 knob log M_hm {kd[0]:.3f}; at bound {atb(kd, [6], [12])})'); k4(f'(d1 {gm})', kd[0])
    holdout(mkd, [list(kd)], [6], [12], 12)
mkd2 = lambda k: (svm(10**k[1]), 0., 0., 0., k[0], 'S12')
kd2 = tune(GS, mkd2, [[OD['S12'][0], 0.]], [6, -1], [12, 2], 12); outd2 = run(GS, mkd2(kd2))
grade('(d2) WDM S12 + constant SIDM core', [o[0] for o in outd2], f'(2 knobs: log M_hm {kd2[0]:.3f}, sigma/m {10**kd2[1]:.3g} cm^2/g; at bound {atb(kd2, [6, -1], [12, 2])})'); kprint('(d2)', outd2)
k2('(d2)', 10**kd2[1]); k4('(d2)', kd2[0]); holdout(mkd2, [list(kd2)], [6, -1], [12, 2], 8)
print(f'\nNo model reaches EXACT unless every E line and its holdout PASS above. Runtime {time.time() - t00:.0f} s.')
print('Rival language; every knob disclosed. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
