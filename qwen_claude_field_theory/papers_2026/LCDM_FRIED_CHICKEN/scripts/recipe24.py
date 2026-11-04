"""A22: superfluid dark matter (Berezhiani-Khoury 2015; Berezhiani, Famaey, Khoury 2018) against the law, per ../FROZEN_A22.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.optimize import minimize
T0 = time.time()
c_, e_, HB, HBC, MPL = 2.998e8, 1.602176634e-19, 6.582119569e-16, 1.97327e-7, 2.435e27   # hbar eV s, hbar c eV m, reduced M_Pl eV
HBSI = 1.054571817e-34
CONV = e_ / (c_**2 * HBC**3)              # rho natural eV^4 -> kg/m^3
PCONV = e_ / HBC**3                        # P natural eV^4 -> J/m^3
RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); RDEN = RDE / CONV   # rho_DE in eV^4
BETA = 2.; C1, C2 = 2 * BETA / 3 - 1, BETA - 1
print(f'base OL {cos.Ode0:.3f}; c sqrt(G rho_DE) {AC:.4e}; a0 {A0:.4e}; rho_DE^(1/4) {RDEN**.25 * 1e3:.3f} meV; beta {BETA}')
def a0bk(al, L): return al**3 * L**2 / MPL * c_ / HB
print(f'control: BFK fiducial alpha 5.7, Lambda 0.05 meV -> a0_BK {a0bk(5.7, 5e-5):.3e} m/s^2 (paper 0.87e-10 with reduced M_Pl)')
# u(k): (u^2 + c1 k) u = sqrt(u^2 + c2 k), u = A/sqrt(a0 g_b), k = K/(a0 g_b)
KG = np.logspace(-10, 10, 801)
UG = np.array([brentq(lambda u: (u * u + C1 * k) * u - np.sqrt(u * u + C2 * k), 1e-12, 10.) for k in KG])
LKG, LUG = np.log(KG), np.log(UG)
def ufk(k): k = np.maximum(k, 1e-300); return np.where(k < 1e-10, 1., np.where(k > 1e10, 3 / np.sqrt(k), np.exp(np.interp(np.log(k), LKG, LUG))))
print(f'control u(k): k 1e-6 {float(ufk(1e-6)):.4f} (->1), k 1e6 {float(ufk(1e6)) * 1e3:.4f} (3/sqrt k = 3.0000) x1e-3')
NG, NW = 400, 36; NGAL = len(GS)
LMB = np.array([np.log10(m200_of(g.Ms)) for g in GS])
def gbat(g, r):
    out = np.exp(np.interp(np.log(r), np.log(g.r), np.log(g.gb)))
    out = np.where(r < g.r[0], g.gb[0] * r / g.r[0], out); return np.where(r > g.r[-1], g.gb[-1] * (g.r[-1] / r)**2, out)
def halos(dn, dlM, dlc):
    M = np.array([m200_of(g.Ms, dn) for g in GS]) * 10**dlM; c = np.interp(np.log10(M), LM, CG) * 10**dlc
    fb = np.minimum(np.array([g.Mb for g in GS]) / M, .5); R = (3 * M * Msun / (800 * np.pi * RHOC))**(1 / 3); rs = R / c
    rhos = (1 - fb) * M * Msun / (4 * np.pi * rs**3 * mu(c)); return M, c, fb, R, rs, rhos
def setup(dn=0., dlM=0., dlc=0.):
    M, c, fb, R, rs, rhos = halos(dn, dlM, dlc)
    lo = np.array([g.r[0] * .02 for g in GS]); hi = np.maximum(2 * R, np.array([g.r[-1] * 1.5 for g in GS]))
    r = np.exp(np.linspace(np.log(lo), np.log(hi), NG).T)                     # (NGAL, NG)
    gb = np.array([gbat(g, r[j]) for j, g in enumerate(GS)])
    x = r / rs[:, None]; rn = rhos[:, None] / (x * (1 + x)**2); mn = 4 * np.pi * rhos[:, None] * rs[:, None]**3 * mu(x)
    # P_NFW(R) = int_R^inf rho_NFW G (M_NFW + M_b)/r^2 dr on an extended grid to 200 R200
    rp = np.exp(np.linspace(np.log(lo), np.log(200 * R), 900).T); xp = rp / rs[:, None]
    rnp = rhos[:, None] / (xp * (1 + xp)**2); mnp = 4 * np.pi * rhos[:, None] * rs[:, None]**3 * mu(xp)
    mbp = np.array([gbat(g, rp[j]) for j, g in enumerate(GS)]) * rp**2 / G
    f = rnp * G * (mnp + mbp) / rp**2; seg = .5 * (f[:, 1:] + f[:, :-1]) * np.diff(rp, axis=1)
    Pn = np.concatenate([np.cumsum(seg[:, ::-1], axis=1)[:, ::-1], np.zeros((NGAL, 1))], axis=1)
    return dict(M=M, c=c, fb=fb, R=R, rs=rs, rhos=rhos, r=r, gb=gb, rn=rn, mn=mn, rp=rp, Pn=Pn)
def integ(S, w0, al, L, m):
    """outward hydrostatic integration for w0 (NGAL, nw); returns rho (NGAL, NG, nw), Mcore, w."""
    a0 = a0bk(al, L); r, gb = S['r'], S['gb']; nw = w0.shape[1]
    KC = 2 * (al * L * m)**2 / (MPL * HB)**2      # K = KC w   (m^2 s^-4)
    CMK = (m / c_**2) / KC                       # muhat / K  (eV s^4 m^-2)
    pref = 2 * np.sqrt(2) * m**2.5 * L
    w = w0.copy(); M = None; RH = np.empty((NGAL, NG, nw)); MM = np.empty_like(RH); WW = np.empty_like(RH)
    for i in range(NG):
        ri = r[:, i:i + 1]; gi = gb[:, i:i + 1]; pos = w > 0; wp = np.where(pos, w, 0.)
        K = KC * wp; s2 = a0 * gi; A = np.sqrt(s2) * ufk(K / s2)
        mh = m * wp / c_**2; mv = A**2 * CMK
        rho = np.where(pos, pref * (3 * C2 * mh + (3 - BETA) * mv) / (3 * np.sqrt(C2 * mh + mv + 1e-300)) * CONV, 0.)
        if M is None: M = 4 * np.pi / 3 * ri**3 * rho
        RH[:, i], MM[:, i], WW[:, i] = rho, M, w
        if i + 1 < NG:
            dr = r[:, i + 1:i + 2] - ri; w = w - dr * (gi + G * M / ri**2); M = M + 4 * np.pi * ri**2 * rho * dr
    return RH, MM, WW
def match(S, RH, MM, L, m):
    """outermost crossing rho_SF -> rho_NFW; residuals log P_SF/P_NFW and log M_core/M_NFW at R; returns resP, resM, index, R."""
    d = RH > S['rn'][:, :, None]; nw = RH.shape[2]; res = np.full((NGAL, nw), np.nan); resm = res.copy(); Ri = np.full((NGAL, nw), -1); Rm = res.copy()
    last = NG - 1 - np.argmax(d[:, ::-1, :], axis=1); has = d.any(axis=1) & (last < NG - 1)
    J, W = np.nonzero(has)
    for j, k in zip(J, W):
        i = last[j, k]; r0, r1 = S['r'][j, i], S['r'][j, i + 1]; lr = np.log(S['r'][j])
        f0 = np.log(RH[j, i, k] / S['rn'][j, i]); f1 = np.log(RH[j, i + 1, k] / S['rn'][j, i + 1]) if RH[j, i + 1, k] > 0 else -50.
        t = f0 / (f0 - f1); R = np.exp(np.log(r0) + t * np.log(r1 / r0)); rnR = np.exp(np.interp(np.log(R), lr, np.log(S['rn'][j])))
        PSF = (rnR / CONV)**3 / (12 * L**2 * m**6) * PCONV; PN = np.exp(np.interp(np.log(R), np.log(S['rp'][j]), np.log(S['Pn'][j] + 1e-300)))
        McR = np.exp(np.interp(np.log(R), lr, np.log(MM[j, :, k] + 1e-300))); MnR = np.exp(np.interp(np.log(R), lr, np.log(S['mn'][j])))
        res[j, k] = np.log(PSF / PN); resm[j, k] = np.log(McR / MnR); Ri[j, k] = i; Rm[j, k] = R
    return res, resm, Ri, Rm
def solve(S, al, L, m, mode='M'):
    lw = np.tile(np.linspace(6, 13, NW), (NGAL, 1)); ok = np.zeros(NGAL, bool)
    for p in range(3):
        RH, MM, WW = integ(S, 10**lw, al, L, m); rP, rM = match(S, RH, MM, L, m)[:2]; res = rP if mode == 'P' else rM
        nl = lw.copy(); ok = np.zeros(NGAL, bool)
        for j in range(NGAL):
            for k in range(NW - 1, 0, -1):
                a, b = res[j, k - 1], res[j, k]
                if np.isfinite(a) and np.isfinite(b) and np.sign(a) != np.sign(b):
                    ok[j] = True; nl[j] = np.linspace(lw[j, k - 1], lw[j, k], NW) if p < 2 else lw[j, k - 1] + (lw[j, k] - lw[j, k - 1]) * a / (a - b); break
            if not ok[j] and p < 2:   # no bracket: zoom on the onset of a crossing (nan -> finite), where a root may hide
                fin = np.isfinite(res[j]); on = [k for k in range(1, NW) if fin[k] and not fin[k - 1]]
                if on: nl[j] = np.linspace(lw[j, on[0] - 1], lw[j, on[0]], NW)
        lw = nl
    lf = np.where(ok, lw[:, 0], 6.)
    RH, MM, WW = integ(S, 10**lf[:, None], al, L, m); rP, rM, Ri, Rm = match(S, RH, MM, L, m)
    return ok & np.isfinite(Rm[:, 0]), RH[:, :, 0], MM[:, :, 0], WW[:, :, 0], Rm[:, 0], Ri[:, 0], rP[:, 0], rM[:, 0]
def curves(S, sol, al, L, m):
    ok, RH, MM, WW, R, Ri = sol[:6]; a0 = a0bk(al, L); KC = 2 * (al * L * m)**2 / (MPL * HB)**2; out = []; info = []
    for j, g in enumerate(GS):
        rs, rhos = S['rs'][j], S['rhos'][j]; mN = lambda r: 4 * np.pi * rhos * rs**3 * mu(r / rs)
        if not ok[j]:
            gt = g.gb + G * mN(g.r) / g.r**2; out.append(gt); info.append((0., np.nan, G * mN(g.r[-1]) / g.r[-1]**2 / gt[-1], np.nan)); continue
        lr = np.log(S['r'][j]); inside = g.r < R[j]
        Mc = np.exp(np.interp(np.log(g.r), lr, np.log(MM[j] + 1e-300))); McR = np.exp(np.interp(np.log(R[j]), lr, np.log(MM[j])))
        Md = np.where(inside, Mc, McR + mN(g.r) - mN(R[j]))
        w = np.interp(np.log(g.r), lr, WW[j]); K = KC * np.maximum(w, 0); s2 = a0 * g.gb; A = np.where(inside & (w > 0), np.sqrt(s2) * ufk(K / s2), 0.)
        gt = g.gb + G * Md / g.r**2 + A; out.append(gt)
        info.append((inside.mean(), np.median(A[inside] / np.sqrt(s2[inside])) if inside.any() else np.nan, G * Md[-1] / g.r[-1]**2 / gt[-1], R[j]))
    return out, info
def model(x, dlM=0., dlc=0., mode='M'):
    la, lL, lm, dn = x; al, L, m = 10**la, 10**lL * 1e-3, 10**lm
    S = setup(dn, dlM, dlc); sol = solve(S, al, L, m, mode); cur, info = curves(S, sol, al, L, m); return cur, info, S, sol
def rms_on(cur, sel): return np.sqrt(np.mean(np.concatenate([(np.log10(cur[j]) - np.log10(GS[j].gl))**2 for j in sel])))
EV, OD = list(range(0, NGAL, 2)), list(range(1, NGAL, 2)); ALL = list(range(NGAL))
def kap(al, L): return a0bk(al, L) / AC
def g4(cur, M):
    sel = [j for j in ALL if 11 <= np.log10(M[j]) <= 12.5]; la = np.log10([fit_a(GS[j].gb, cur[j]) for j in sel]); return la.std(), len(sel), 10**np.median(la)
def report(tag, x, cur, info, S, sol, knobs):
    e1 = grade(tag, cur, f'({knobs})'); inf = np.array([i[:3] for i in info]); ok = sol[0]
    npin = sum(int(round(i[0] * len(g.r))) for g, i in zip(GS, info)); frac = npin / len(ALLB)
    s4, n4, am = g4(cur, S['M']); al, L = 10**x[0], 10**x[1] * 1e-3
    print(f' alpha {al:.3g}, Lambda {L * 1e3:.3g} meV, m {10**x[2]:.3g} eV, dn {x[3]:+.3f}; a0_BK {a0bk(al, L):.3e}; kappa_eff {kap(al, L):.3f} [{"PASS" if abs(np.log10(kap(al, L) / .5)) <= .05 else "FAIL"} G1]; Lambda/rho_DE^(1/4) {L / RDEN**.25:.3g}')
    print(f' superfluid matched in {ok.sum()} of {NGAL}; points inside R_NFW {npin} of {len(ALLB)} = {frac:.3f} [{"PASS" if frac >= .9 else "FAIL"} G5]; median R_NFW {np.nanmedian(sol[4]) / kpc:.1f} kpc')
    print(f' G4 per-galaxy effective a over log M200 11-12.5: rms {s4:.3f} dex over {n4} [{"PASS" if s4 <= .1 else "FAIL"} G4], median {am:.3e}')
    if np.any(ok): print(f' DIAG: at R_NFW median log(P_SF/P_NFW) {np.median(sol[6][ok]):+.2f}, median log(M_core/M_NFW) {np.median(sol[7][ok]):+.2f} (natural log)')
    print(f' DIAG: median phonon/sqrt(a0 g_b) inside {np.nanmedian(inf[:, 1]):.3f}; median dark share of g at last point {np.median(inf[:, 2]):.3f}')
    return e1, frac
def thermal(S, sol, m):
    ok, RH, MM, WW, R, Ri = sol[:6]; mk = m * e_ / c_**2; out = []
    for j in np.nonzero(ok)[0]:
        r = S['r'][j]; rho = RH[j]; gt = S['gb'][j] + G * MM[j] / r**2; v = np.sqrt(gt * r / 2); sel = rho > 0
        N = rho / mk * (2 * np.pi * HBSI / (mk * v))**3; ratio = 1e-3 * N * v * rho / np.sqrt(G * rho + 1e-300)
        i = np.nonzero(sel & (ratio >= 1))[0]; out.append((r[i[-1]] if len(i) else r[0]) / R[j])
    return np.median(out) if out else np.nan

# ---------------- (a) deep phonon force alone ----------------
print('\n(a) BK deep phonon alone, g = g_b + sqrt(a0_BK g_b) (no condensate gravity)')
grade('(a) at a0_BK = A0 (0 knobs)', [g.gb + np.sqrt(A0 * g.gb) for g in GS])
def fa(sel): return 10**minimize_scalar(lambda x: sum(((np.log10(GS[j].gb + np.sqrt(10**x * GS[j].gb)) - np.log10(GS[j].gl))**2).sum() for j in sel), bounds=(-12, -9), method='bounded').x
aa = fa(ALL); cura = [g.gb + np.sqrt(aa * g.gb) for g in GS]
e1a = grade('(a) a0_BK fitted on all (1 knob)', cura, f'(a0_BK {aa:.3e}, {np.log10(aa / A0):+.3f} dex vs A0, kappa_eff {aa / AC:.3f})')
ah = fa(EV); hua = rms_on([g.gb + np.sqrt(ah * g.gb) for g in GS], OD)
print(f'(a) holdout: tuned on GS[::2] a0_BK {ah:.3e}; unseen rms to law on GS[1::2] {hua:.4f} [{"PASS" if hua <= .025 else "FAIL"}]')
for alpha_ in (1., .86):
    Lr = np.sqrt(aa * HB / c_ * MPL / alpha_**3); print(f'(a) implied Lambda at alpha {alpha_}: {Lr * 1e3:.3f} meV = {Lr / RDEN**.25:.3f} rho_DE^(1/4)')
print(f' [{time.time() - T0:.0f} s]')

# ---------------- (b) hybrid with condensate gravity ----------------
XF = np.array([np.log10(5.7), np.log10(.05), 0., 0.])
cur, info, S, sol = model(XF, mode='P')
report('(b1-as-frozen) BFK fiducial, density + pressure match, envelope fixed at SHMR M200 and Diemer19 c', XF, cur, info, S, sol, '0 knobs tuned; unmatched galaxies graded as NFW + baryons')
DLC = np.linspace(-1, 1, 17); rmB = np.full((NGAL, len(DLC)), np.nan)
for q, d_ in enumerate(DLC):
    sq = model(XF, 0., d_, 'P')[3]; rmB[:, q] = np.where(sq[0], sq[7], np.nan)
dB = np.full(NGAL, np.nan)
for j in range(NGAL):
    for q in range(len(DLC) - 1):
        a, b = rmB[j, q], rmB[j, q + 1]
        if np.isfinite(a) and np.isfinite(b) and np.sign(a) != np.sign(b): dB[j] = DLC[q] + (DLC[q + 1] - DLC[q]) * a / (a - b); break
okB = np.isfinite(dB); print(f'\n(b1-BFK) density + pressure + mass continuity, M200 at SHMR, c free: solution in {okB.sum()} of {NGAL}; P-match exists at some c for {np.isfinite(rmB).any(axis=1).sum()}; median c offset {np.nanmedian(dB) if okB.any() else np.nan:+.2f} dex (p16-p84 {np.nanpercentile(dB, 16) if okB.any() else np.nan:+.2f} to {np.nanpercentile(dB, 84) if okB.any() else np.nan:+.2f})')
if okB.any():
    cB, iB, SB, sB = model(XF, 0., np.where(okB, dB, 0.), 'P')
    report('(b1-BFK) BFK fiducial, envelope c re-solved per galaxy (no-solution galaxies at Diemer19 c)', XF, cB, iB, SB, sB, f'0 global knobs tuned; {okB.sum()} per-galaxy c set by matching, not by the law')
cur, info, S, sol = model(XF)
e1b1, f1 = report('(b1) BFK fiducial hybrid, mode M (density + mass match), condensate + NFW + phonon', XF, cur, info, S, sol, '0 knobs tuned')
print(f' DIAG median R_T/R_NFW at sigma/m 0.01 cm^2/g: {thermal(S, sol, 1.):.2f}')
ab1 = fit_a(ALLB, np.concatenate(cur)); print(f' [{time.time() - T0:.0f} s]')
LOB, HIB = [-1, -3, -1, -.54], [2, 1, 1, .54]
def tune(sel, x0, nf=120):
    f = lambda x: rms_on(model(np.clip(x, LOB, HIB))[0], sel)
    r = minimize(f, x0, method='Nelder-Mead', bounds=list(zip(LOB, HIB)), options=dict(maxfev=nf, xatol=1e-3, fatol=1e-5, initial_simplex=np.array([x0] + [x0 + np.eye(4)[i] * (.3 if i < 3 else .2) for i in range(4)])))
    return np.clip(r.x, LOB, HIB), r.fun, r.nfev
xb, fb_, nf = tune(ALL, XF)
atb = [i for i in range(4) if min(xb[i] - LOB[i], HIB[i] - xb[i]) < 1e-3 * (HIB[i] - LOB[i])]
cur2, info2, S2, sol2 = model(xb)
e1b2, f2 = report('(b2) hybrid tuned on all', xb, cur2, info2, S2, sol2, f'4 global knobs, {nf} evaluations, at bound {atb}')
print(f' DIAG median R_T/R_NFW at sigma/m 0.01 cm^2/g: {thermal(S2, sol2, 10**xb[2]):.2f}')
xh, _, nfh = tune(EV, XF); hub = rms_on(model(xh)[0], OD)
print(f'(b2) holdout: tuned on GS[::2] knobs {np.round(xh, 3).tolist()} ({nfh} evals); unseen rms to law on GS[1::2] {hub:.4f} [{"PASS" if hub <= .025 else "FAIL"}]')
print(f' [{time.time() - T0:.0f} s]')

# ---------------- (c) per-galaxy halo freedom ----------------
def pergal(x, sel):
    bdM, bdc = np.zeros(NGAL), np.zeros(NGAL); best = np.full(NGAL, np.inf); bc = [None] * NGAL
    for grid in ((np.linspace(-.6, .6, 9), np.linspace(-.22, .22, 5)), None):
        if grid is None:   # refine around each galaxy's best
            cand = [(dM, dc) for dM in (-.075, 0, .075) for dc in (-.055, 0, .055)]
            pairs = [(np.clip(bdM + dM, -.6, .6), np.clip(bdc + dc, -.22, .22)) for dM, dc in cand]
        else: pairs = [(np.full(NGAL, dM), np.full(NGAL, dc)) for dM in grid[0] for dc in grid[1]]
        for pM, pc in pairs:
            cu = model(x, pM, pc)[0]
            for j in sel:
                v = np.mean((np.log10(cu[j]) - np.log10(GS[j].gl))**2)
                if v < best[j]: best[j], bdM[j], bdc[j], bc[j] = v, pM[j], pc[j], cu[j]
    return bdM, bdc, bc
dM, dc, cc_ = pergal(xb, ALL)
nb = int((abs(abs(dM) - .6) < 1e-6).sum() + (abs(abs(dc) - .22) < 1e-6).sum())
grade('(c) per-galaxy M200, c on (b2) globals', cc_, f'(342 per-galaxy + 4 global = 346 parameters; grid optimiser 45 + 9 x 9 steps; at bound {nb} of 342; median dlogM200 {np.median(dM):+.2f})')
print(f'(c) holdout: no per-galaxy value can be set on unseen galaxies without fitting the target; unseen = (b2) holdout {hub:.4f} [{"PASS" if hub <= .025 else "FAIL"}]')
print(f' [{time.time() - T0:.0f} s]')

# ---------------- swoop: Lambda tied to rho_DE ----------------
LD = RDEN**.25
print(f'\nSWOOP. rho_DE^(1/4) = {LD * 1e3:.3f} meV. kappa_eff = alpha^3 Lambda^2 sqrt(8 pi)/sqrt(rho_DE) at Lambda^4 = rho_DE: control sqrt(8 pi) = {np.sqrt(8 * np.pi):.3f}')
aN3 = (.5 / kap(1., LD))**(1 / 3)
for nm, al in (('N1 alpha 1', 1.), ('N2 alpha 5.7', 5.7), ('N3 alpha set to kappa 0.5 (hand)', aN3)):
    k = kap(al, LD); print(f' {nm}: alpha {al:.3f}, a0_BK {a0bk(al, LD):.3e}, kappa_eff {k:.3f} [{"PASS" if abs(np.log10(k / .5)) <= .05 else "FAIL"} G1]')
print(' G2: a0_BK = alpha^3 Lambda^2/M_Pl, Lagrangian constants; d ln a0/d ln rho_DE = 0 natively [FAIL G2]; 0.5 only with Lambda^4 = rho_DE written by hand')
print(' G3: constants and w = -1 give a(z)/a(0) = 1 in every band [PASS G3, trivial; condensate formation in z not modelled]')
for nm, lm in (('N3 at m 1 eV', 0.),):
    x3 = np.array([np.log10(aN3), np.log10(LD * 1e3), lm, 0.]); c3, i3, S3, s3 = model(x3)
    report(f'(N3) Lambda^4 = rho_DE, alpha {aN3:.3f}, {nm}, hybrid', x3, c3, i3, S3, s3, '0 knobs tuned; alpha by hand')
r3 = minimize_scalar(lambda lm: rms_on(model(np.array([np.log10(aN3), np.log10(LD * 1e3), lm, 0.]))[0], ALL), bounds=(-1, 1), method='bounded', options=dict(maxiter=25))
x3 = np.array([np.log10(aN3), np.log10(LD * 1e3), r3.x, 0.]); c3, i3, S3, s3 = model(x3)
report(f'(N3m) Lambda^4 = rho_DE, alpha {aN3:.3f}, m tuned, hybrid', x3, c3, i3, S3, s3, f'1 knob m, at bound {min(r3.x + 1, 1 - r3.x) < 2e-3}')
h3 = minimize_scalar(lambda lm: rms_on(model(np.array([np.log10(aN3), np.log10(LD * 1e3), lm, 0.]))[0], EV), bounds=(-1, 1), method='bounded', options=dict(maxiter=25))
hu3 = rms_on(model(np.array([np.log10(aN3), np.log10(LD * 1e3), h3.x, 0.]))[0], OD)
print(f'(N3m) holdout: m tuned on GS[::2] {10**h3.x:.3g} eV; unseen rms {hu3:.4f} [{"PASS" if hu3 <= .025 else "FAIL"}]')
import resource
print(f'\nruntime {time.time() - T0:.0f} s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6:.0f} MB')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
