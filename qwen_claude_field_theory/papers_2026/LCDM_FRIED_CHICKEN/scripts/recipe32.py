"""A30: screened, matter-coupled dynamical dark energy (k-mouflage, chameleon f(R), symmetron, DM-coupled quintessence), per ../FROZEN_A30.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
T0 = time.time()
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
W0, WA = -.75, -.86
def rde_ratio(z): return (1 + z)**(3 * (1 + W0 + WA)) * np.exp(-3 * WA * z / (1 + z))
def wz(z): return W0 + WA * z / (1 + z)
TZ = {z: .5 * np.log10(rde_ratio(z)) for z in ZB}
EV, OD = GS[::2], GS[1::2]
GMS, AU, RSUN = 1.327e20, 1.496e11, 6.957e8
RSAT, RLIMB = 9.58 * AU, 1.6 * RSUN
def rms(x): return np.sqrt((np.asarray(x)**2).mean())
def P(s): print(s, flush=True)
P(f'cosmology OL {cos.Ode0:.3f}: c sqrt(G rho_DE) AC {AC:.4e}, A0 {A0:.4e} (kappa {A0 / AC:.4f})')
P('GT targets 0.5 log10 rho_DE(z)/rho_DE0 (CPL w0 -0.75, wa -0.86): ' + ', '.join(f'z {z}: {t:+.4f}' for z, t in TZ.items()))
LM2 = np.array([np.log10(m200_of(g.Ms)) for g in GS]); HOST = (LM2 >= 11) & (LM2 <= 12.5)
def gt_const(tag):
    res = {z: 0. - TZ[z] for z in ZB}; ok = all(abs(v) <= .05 for v in res.values())
    P(f' {tag} GT (a(z)/a(0) = 1): residuals ' + ', '.join(f'{z}: {v:+.4f}' for z, v in res.items()) + f' [{"PASS" if ok else "FAIL"} GT]'); return ok
def gt_ratio(tag, rat):
    res = {z: np.log10(rat[z]) - TZ[z] for z in ZB}; ok = all(abs(v) <= .05 for v in res.values()); g3 = all(ZB[z][0] <= rat[z] <= ZB[z][1] for z in ZB)
    P(f' {tag} a(z)/a(0) ' + ', '.join(f'{z}: {rat[z]:.3f}' for z in ZB) + f' [{"PASS" if g3 else "FAIL"} G3]; GT residuals ' + ', '.join(f'{z}: {v:+.4f}' for z, v in res.items()) + f' [{"PASS" if ok else "FAIL"} GT]'); return ok, g3
def g1(tag, a):
    k = a / AC; ok = abs(np.log10(k / .5)) <= .05; P(f' {tag} kappa_eff {k:.4g} ({np.log10(k / .5):+.3f} dex) [{"PASS" if ok else "FAIL"} G1]'); return ok
def g4(tag, cur):
    la = np.log10([fit_a(g.gb, c) for g, c in zip(GS, cur)]); s = la[HOST].std(); ok = s <= .1
    P(f' {tag} G4 per-galaxy fit_a over {HOST.sum()} hosts log M200 11-12.5: rms {s:.3f} dex (all 171: {la.std():.3f}) [{"PASS" if ok else "FAIL"} G4]'); return ok
def unseen(cur_od):
    return rms(np.log10(np.concatenate(cur_od)) - np.log10(np.concatenate([g.gl for g in OD])))
def halo_gN(g, dn=0., dlc=0.):
    M = m200_of(g.Ms, dn); c = np.interp(np.log10(M), LM, CG) * 10**dlc; fb = min(g.Mb / M, .5)
    mh, R = nfw_m(g.r, M, c); return g.gb + G * (1 - fb) * mh / g.r**2, M, c, fb, R / c
gl_over_gb = ALLL / ALLB
P(f'law boost g_law/g_b on SPARC: median {np.median(gl_over_gb):.2f}, p95 {np.percentile(gl_over_gb, 95):.2f}, max {gl_over_gb.max():.2f}; a linear boost (1 + 2 beta^2) reaching the max needs beta >= {np.sqrt((gl_over_gb.max() - 1) / 2):.2f}')

# ======================= (a) k-mouflage
P('\n######## (a) k-mouflage')
def kmy(gN, b2, a_s, n):
    """solve y [1 + (y/a_s)^(2n)] = b2 gN for y (log bisection, exact bracket)."""
    S = b2 * gN; lS, la = np.log(S), np.log(a_s)
    lo = lS - np.logaddexp(0, 2 * n * (lS - la)); hi = lS.copy()
    for _ in range(70):
        m = .5 * (lo + hi); f = m + np.logaddexp(0, 2 * n * (m - la)) - lS
        hi = np.where(f > 0, m, hi); lo = np.where(f > 0, lo, m)
    return np.exp(.5 * (lo + hi))
y_test = kmy(np.array([1e-14, 1e-6]), 2., 1e-10, 2); P(f'control kmy: unscreened y/(2b^2 gN) {y_test[0] / 2e-14:.6f} (->1); screened y {y_test[1]:.4e} vs asymptote a_s (2b^2 gN/a_s)^(1/5) {1e-10 * (2e-6 / 1e-10)**.2:.4e}')
SQ16 = np.sqrt(16 * np.pi)
def as_tied(beta, n): return SQ16 * beta * AC * (n + 1)**(-1 / (2 * n))   # M^4 = rho_DE, K0 = 1, m = n + 1, lambda = n + 1
def kcurve(gs, p, halo=False, tie=False):
    if tie: lb, n = p; beta = 10**lb; a_s = as_tied(beta, n)
    else: lb, las, n = p[:3]; beta = 10**lb; a_s = 10**las * A0
    out, gns = [], []
    for g in gs:
        gN = halo_gN(g, p[3])[0] if halo else g.gb
        out.append(gN + kmy(gN, 2 * beta**2, a_s, n)); gns.append(gN)
    kcurve.gn = gns
    return out, beta, a_s, n
def kfit(gs, x0, lo, hi, halo=False, tie=False):
    gt = np.concatenate([g.gl for g in gs])
    res = lambda p: np.log10(np.concatenate(kcurve(gs, p, halo, tie)[0])) - np.log10(gt)
    best = None
    for s in range(4):
        st = np.array(x0, float) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        r = least_squares(res, np.clip(st, np.array(lo) + 1e-6, np.array(hi) - 1e-6), bounds=(lo, hi), diff_step=1e-3, max_nfev=200)
        if best is None or r.cost < best.cost: best = r
    atb = [i for i, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
    return best.x, atb
def cassini_k(tag, beta, a_s, n):
    gS = GMS / RSAT**2; yS = kmy(np.array([gS]), 2 * beta**2, a_s, n)[0]; gL = GMS / RLIMB**2; yL = kmy(np.array([gL]), 2 * beta**2, a_s, n)[0]
    gam = 2 * yL / (gL + yL); okS = yS < 1e-3 * A0; okL = gam < 2.3e-5
    P(f' {tag} Cassini: y at Saturn {yS:.3e} m/s^2 = {yS / A0:.3g} a0 [{"PASS" if okS else "FAIL"} <1e-3 a0]; |gamma-1| at 1.6 R_sun {gam:.3e} [{"PASS" if okL else "FAIL"} <2.3e-5]; y/g_N at Saturn {yS / gS:.2e} => {"PASS" if okS and okL else "FAIL"} Cassini')
    return okS and okL
def kreport(tag, cur, beta, a_s, n, nk, tied, gns):
    e1 = grade(tag, cur, f'({nk} knobs; beta {beta:.4g}, a_s {a_s:.4e} = {a_s / A0:.4g} a0, n {n:.3f}, 2beta^2 {2 * beta**2:.4g})')
    gst = a_s / (2 * beta**2); P(f' switch in g_N: g_* = a_s/(2 beta^2) = {gst:.4e} = {gst / A0:.4g} a0, kappa_* = g_*/AC {gst / AC:.4g}')
    gt = np.concatenate(cur); P(f' fit_a of the law form to the model curve: {fit_a(ALLB, gt):.4e}')
    ok1 = g1(tag, fit_a(ALLB, gt)); ok4 = g4(tag, cur)
    gn = np.concatenate(gns); y = gt - gn
    med = np.median(y / gn); ok5 = med >= .1; P(f' {tag} G5 median y/g_N {med:.4g} [{"PASS" if ok5 else "FAIL"} G5]')
    P(f' {tag} G2: {"0.5 by construction (M^4 = rho_DE imposed)" if tied else "0 natively (M, beta Lagrangian constants)"} => {"PASS by construction, not derived" if tied else "FAIL"}'); P(f' {tag} G3: ratio 1 at all z, trivial PASS')
    okt = gt_const(tag); okc = cassini_k(tag, beta, a_s, n); return e1, ok1, ok4, ok5, okt, okc
# KA0 / KH0 natural
b0, n0 = .1, 2; as0 = SQ16 * b0 * AC * 3**(-1 / 4)
P(f'natural: m 3, K0 1, beta 0.1, M^4 = rho_DE: a_K = sqrt(16 pi) beta AC = {SQ16 * b0 * AC:.4e}, a_s = a_K 3^(-1/4) = {as0:.4e}; analytic kappa_* (lambda 1) = sqrt(4 pi)/beta = {np.sqrt(4 * np.pi) / b0:.3f}')
cur = [g.gb + kmy(g.gb, 2 * b0**2, as0, n0) for g in GS]; kreport('KA0 natural no halo', cur, b0, as0, n0, 0, True, [g.gb for g in GS])
F0K = [halo_gN(g)[0] for g in GS]; cur = [gn + kmy(gn, 2 * b0**2, as0, n0) for gn in F0K]; kreport('KH0 natural LCDM + k-mouflage', cur, b0, as0, n0, 0, True, F0K)
# KA1 shape fit, no halo
lo, hi = [-2, -4, .25], [1.5, 4, 10]
p, atb = kfit(GS, [.4, 0., 2.], lo, hi); cur, beta, a_s, n = kcurve(GS, p); GN_ = kcurve.gn; P(f'\nKA1 knobs {np.round(p, 4).tolist()} at bound {atb}')
r_ka1 = kreport('KA1 shape fit no halo', cur, beta, a_s, n, 3, False, GN_)
ph, _ = kfit(EV, p, lo, hi); u = unseen(kcurve(OD, ph)[0]); P(f' KA1 holdout unseen rms {u:.4f} [{"PASS" if u <= .025 else "FAIL"}]')
# KH1 shape fit, LCDM + k-mouflage
lo, hi = [-2, -4, .25, -.54], [1.5, 4, 10, .54]
p, atb = kfit(GS, [0., 0., 2., 0.], lo, hi, halo=True); cur, beta, a_s, n = kcurve(GS, p, halo=True); GN_ = kcurve.gn; P(f'\nKH1 knobs {np.round(p, 4).tolist()} at bound {atb}')
r_kh1 = kreport('KH1 shape fit LCDM + k-mouflage', cur, beta, a_s, n, 4, False, GN_)
ph, _ = kfit(EV, p, lo, hi, halo=True); u = unseen(kcurve(OD, ph, halo=True)[0]); P(f' KH1 holdout unseen rms {u:.4f} [{"PASS" if u <= .025 else "FAIL"}]')
# KT tie row
lo, hi = [-2, .25], [1.5, 10]
p, atb = kfit(GS, [.4, 2.], lo, hi, tie=True); cur, beta, a_s, n = kcurve(GS, p, tie=True); GN_ = kcurve.gn; P(f'\nKT knobs {np.round(p, 4).tolist()} at bound {atb} (M^4 = rho_DE, K0 = 1 imposed)')
r_kt = kreport('KT tie row no halo', cur, beta, a_s, n, 2, True, GN_)
ph, _ = kfit(EV, p, lo, hi, tie=True); u = unseen(kcurve(OD, ph, tie=True)[0]); P(f' KT holdout unseen rms {u:.4f} [{"PASS" if u <= .025 else "FAIL"}]')
P(f' KT beta needed {beta:.3f} against the Solar-System/LLR scale beta ~ 0.1 (provisional); at kappa_* = 0.5 with lambda = 1, beta would be sqrt(4 pi)/0.5 = {np.sqrt(4 * np.pi) / .5:.2f}')
P(f'[{time.time() - T0:.0f} s]')

# ======================= (b1) chameleon f(R), Hu-Sawicki n = 1
P('\n######## (b1) chameleon f(R), Hu-Sawicki n = 1')
RM0 = cos.Om0 * RHOC; RBARR = RM0 + 4 * RDE; R0 = 8 * np.pi * G * RBARR / c_**2
def lamC(f, R=R0): return np.sqrt(6 * f / R)
def gC(f, R=R0): return c_**2 * f / lamC(f, R)
PRE = []
for g in GS:
    gN, M, c, fb, rs = halo_gN(g); Mt = gN * g.r**2 / G
    Ib = np.concatenate([np.cumsum((.5 * (g.gb[1:] + g.gb[:-1]) * np.diff(g.r))[::-1])[::-1], [0.]]) + g.gb[-1] * g.r[-1]
    rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); Ph = (1 - fb) * 4 * np.pi * G * rhos * rs**3 * np.log(1 + g.r / rs) / g.r
    PRE.append((Ib + Ph) / c_**2)
def cham(gs, pre, f, dn=0.):
    out, ns, nl = [], 0, 0
    for g, ph0 in zip(gs, pre):
        gN, M, c, fb, rs = halo_gN(g, dn)
        if dn == 0.: ph = ph0
        else:
            Ib = np.concatenate([np.cumsum((.5 * (g.gb[1:] + g.gb[:-1]) * np.diff(g.r))[::-1])[::-1], [0.]]) + g.gb[-1] * g.r[-1]
            rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); ph = (Ib + (1 - fb) * 4 * np.pi * G * rhos * rs**3 * np.log(1 + g.r / rs) / g.r) / c_**2
        Mt = gN * g.r**2 / G; thr = 1.5 * f; ph0c = ph[0] + gN[0] * g.r[0] / 2 / c_**2
        if ph[-1] > thr: y = 0 * gN; nl += 1; ns += 1
        else:
            if ph[0] < thr:
                if ph0c <= thr: Ms = 0.
                else: x2 = (ph0c - thr) / (gN[0] * g.r[0] / 2 / c_**2); Ms = Mt[0] * max(x2, 0)**1.5
                rsc = 0.
            else:
                ns += 1; i = np.nonzero(ph >= thr)[0][-1]; t = (ph[i] - thr) / (ph[i] - ph[i + 1])
                rsc = np.exp(np.log(g.r[i]) + t * np.log(g.r[i + 1] / g.r[i])); Ms = np.exp(np.log(Mt[i]) + t * np.log(Mt[i + 1] / Mt[i]))
            y = np.where(g.r > rsc, np.maximum(G * (Mt - Ms) / g.r**2, 0) / 3, 0.)
        out.append(gN + y)
    return out, ns, nl
P(f'R0 = 8 pi G (rho_m + 4 rho_L)/c^2 = {R0:.4e} m^-2; lambda_C at 1e-7, 1e-6, 1e-5: ' + ', '.join(f'{lamC(f) / kpc / 1e3:.2f}' for f in (1e-7, 1e-6, 1e-5)) + ' Mpc (Yukawa ignored inside galaxies)')
P(f'median |Phi|/c^2 at the last point {np.median([p[-1] for p in PRE]):.3e}, at the first point {np.median([p[0] for p in PRE]):.3e}')
F0 = [halo_gN(g)[0] for g in GS]; grade('F0 control, plain NFW + baryons (= Q0, f_R0 -> 0)', F0, '(0 knobs)')
for f in (1e-7, 1e-6, 1e-5):
    cur, ns, nl = cham(GS, PRE, f); grade(f'F{-int(np.log10(f))} |f_R0| {f:.0e}', cur, f'(0 knobs; screened core in {ns}/171, screened past the last point {nl}/171)')
    yy = np.concatenate(cur) / np.concatenate(F0) - 1; P(f' median y/g_N {np.median(yy):.4f}, max {yy.max():.4f} (bound 1/3)')
    if f == 1e-6: med6 = np.median(yy); g4('F6', cur)
LF, DN = np.linspace(-8, -4, 17), np.linspace(-.54, .54, 11)
def grid_cham(gs, pre):
    gt = np.concatenate([g.gl for g in gs]); best = (np.inf, None)
    for lf in LF:
        for dn in DN:
            e = rms(np.log10(np.concatenate(cham(gs, pre, 10**lf, dn)[0])) - np.log10(gt))
            if e < best[0]: best = (e, (lf, dn))
    return best
e, (lf, dn) = grid_cham(GS, PRE); cur = cham(GS, PRE, 10**lf, dn)[0]
grade('FK grid fit', cur, f'(2 knobs; log f_R0 {lf:.2f}, dn {dn:+.3f}; at grid edge: {lf in (LF[0], LF[-1])}, {dn in (DN[0], DN[-1])})'); g4('FK', cur)
e2, (lf2, dn2) = grid_cham(EV, PRE[::2]); u = unseen(cham(OD, PRE[1::2], 10**lf2, dn2)[0]); P(f' FK holdout (tuned on even-index: log f_R0 {lf2:.2f}, dn {dn2:+.3f}) unseen rms {u:.4f} [{"PASS" if u <= .025 else "FAIL"}]')
P('\nf(R) derived acceleration g_C = c^2 |f_R0|/lambda_C = c^2 sqrt(|f_R0| R0/6):')
for f in (1e-7, 1e-6): P(f' |f_R0| {f:.0e}: g_C {gC(f):.3e} = {gC(f) / A0:.4f} a0'); g1(f'f(R) g_C at {f:.0e}', gC(f))
fneed = 6 * (.5 * AC / c_**2)**2 / R0; P(f' |f_R0| needed for kappa_eff 0.5: {fneed:.3e} (allowed <~ 1e-6, provisional)')
rows = []
for OL, H0 in ((.70, 67.4), (.685, 73.), (.65, 73.)):
    h = H0 / 100; rc = 3 * (H0 * 1e3 / (kpc * 1e3))**2 / (8 * np.pi * G); rl, rm = OL * rc, (1 - OL) * rc
    rows.append((rl, gC(1e-6, 8 * np.pi * G * (rm + 4 * rl) / c_**2)))
sl = [np.log(rows[i][1] / rows[0][1]) / np.log(rows[i][0] / rows[0][0]) for i in (1, 2)]
P(f' G2 slopes d ln g_C / d ln rho_DE over the J cosmologies at fixed f_R0: {sl[0]:+.3f}, {sl[1]:+.3f} [{"PASS" if all(abs(s - .5) <= .05 for s in sl) else "FAIL"} G2]')
def Rz(z): return 8 * np.pi * G * (RM0 * (1 + z)**3 + (1 - 3 * wz(z)) * RDE * rde_ratio(z)) / c_**2
gt_ratio('f(R) g_C (CPL background, f_R(z) = f_R0 (R0/R)^2)', {z: np.sqrt(Rz(0) / Rz(z)) for z in ZB})
P(f' f(R) G5 median y/g_N at 1e-6 {med6:.4f} [{"PASS" if med6 >= .1 else "FAIL"} G5]')
PSUN = GMS / (RSUN * c_**2); Mmw = 1e12; cmw = np.interp(12, LM, CG); Rmw = (3 * Mmw * Msun / (800 * np.pi * RHOC))**(1 / 3); rsm = Rmw / cmw
rhm = Mmw * Msun / (4 * np.pi * rsm**3 * mu(cmw)); PMW = (4 * np.pi * G * rhm * rsm**3 * np.log(1 + 8 * kpc / rsm) / (8 * kpc) + G * 6.5e10 * Msun / (8 * kpc)) / c_**2
RLOC = .1 * Msun / (3.0857e16)**3
P(f'Cassini f(R): Phi_sun {PSUN:.3e}, |Phi_MW(8 kpc)| {PMW:.3e}, rho_loc {RLOC:.3e} kg/m^3, rho_bar_R {RBARR:.3e}')
for f in (1e-7, 1e-6, 1e-5):
    x = min(1, 4.5 * f / PSUN) / 3; gam = 2 * x / (1 + x)
    scr = PMW > 1.5 * f; fa = f * (RBARR / RLOC)**2 if scr else f; xa = min(1, 4.5 * fa / PSUN) / 3; gama = 2 * xa / (1 + xa)
    P(f' |f_R0| {f:.0e}: Sun alone |gamma-1| {gam:.3e} [{"PASS" if gam < 2.3e-5 else "FAIL"}]; MW screened {scr}, ambient f_R {fa:.2e}, |gamma-1| {gama:.3e} [{"PASS" if gama < 2.3e-5 else "FAIL"} Cassini]')
P(f'[{time.time() - T0:.0f} s]')

# ======================= (b2) symmetron, adiabatic stand-in
P('\n######## (b2) symmetron, adiabatic stand-in')
SYM = []
for g in GS:
    gN, M, c, fb, rs = halo_gN(g); rb = np.maximum(np.gradient(g.mb, g.r) / (4 * np.pi * g.r**2), 0); drb = np.gradient(rb, g.r)
    rhos = (1 - fb) * M * Msun / (4 * np.pi * rs**3 * mu(c)); x = g.r / rs; rh = rhos / (x * (1 + x)**2); drh = -rh * (1 + 3 * x) / (g.r * (1 + x))
    SYM.append((gN, rb, drb, rb + rh, drb + drh))
def symm(idx, lrs, lps, halo):
    rs_, ps = 10**lrs, 10**lps; out = []
    for i in idx:
        gN, rb, drb, rt, drt = SYM[i]
        if halo: gn, rho, dr = gN, rt, drt
        else: gn, rho, dr = GS[i].gb, rb, drb
        a5 = np.where(rho < rs_, -c_**2 * ps * dr / rs_, 0.); out.append(np.maximum(gn + a5, .01 * gn))
    return out
ALLI = list(range(len(GS)))
mins = min(SYM[i][3].min() for i in ALLI); P(f'S0: rho_SSB = rho_DE {RDE:.3e} kg/m^3; min total density over all measured points {mins:.3e} ({mins / RDE:.3g} rho_DE)')
cur = symm(ALLI, np.log10(RDE), -6, True); grade('S0 DE-scale symmetron, with halo', cur, '(0 knobs; rho_SSB = rho_DE, Phi_s 1e-6)')
s0y = np.median(np.concatenate(cur) / np.concatenate(F0) - 1); P(f' S0 G5 median a5/g_N {s0y:.4g} [{"PASS" if s0y >= .1 else "FAIL"} G5]')
LR, LP = np.linspace(-27, -18, 19), np.linspace(-9, -3, 25)
def grid_sym(idx, halo):
    gt = np.concatenate([GS[i].gl for i in idx]); best = (np.inf, None)
    for a in LR:
        for b in LP:
            e = rms(np.log10(np.concatenate(symm(idx, a, b, halo))) - np.log10(gt))
            if e < best[0]: best = (e, (a, b))
    return best
SB = {}
for tag, halo in (('SH with halo', True), ('SB baryons only', False)):
    e, (a, b) = grid_sym(ALLI, halo); cur = symm(ALLI, a, b, halo); SB[tag] = (e, a, b, halo)
    grade(tag, cur, f'(2 knobs; log rho_SSB {a:.2f}, log Phi_s {b:.2f}; grid edge {a in (LR[0], LR[-1])}, {b in (LP[0], LP[-1])})')
    fa = fit_a(ALLB, np.concatenate(cur)); g1(tag + ' (diagnostic of fitted level)', fa); g4(tag, cur)
    rsw = 1.2e-20 * (RSAT / AU)**-2; a5 = c_**2 * 10**b * 2 * rsw / (RSAT * 10**a) if rsw < 10**a else 0.
    P(f' {tag} Cassini: solar-wind rho at Saturn {rsw:.2e}; a5 {a5:.3e} = {a5 / A0:.3g} a0 [{"PASS" if a5 < 1e-3 * A0 else "FAIL"}]')
best = min(SB, key=lambda k: SB[k][0]); _, a, b, halo = SB[best]
e2, (a2, b2) = grid_sym(list(range(0, len(GS), 2)), halo); u = unseen(symm(list(range(1, len(GS), 2)), a2, b2, halo))
P(f' holdout for {best} (tuned even-index: {a2:.2f}, {b2:.2f}) unseen rms {u:.4f} [{"PASS" if u <= .025 else "FAIL"}]')
P(' symmetron G2: rho_SSB = rho_DE only if imposed; the force scale c^2 Phi_s |d ln rho/dr| is not an acceleration constant => no tie'); gt_const('symmetron')
rsw = 1.2e-20 * (RSAT / AU)**-2; P(f' S0 Cassini: rho_SSB {RDE:.2e} < solar-wind {rsw:.2e}: symmetry restored, a5 = 0 [PASS]')
P(f'[{time.time() - T0:.0f} s]')

# ======================= (c) coupled quintessence, DM-only coupling
P('\n######## (c) coupled quintessence, DM-only coupling, beta 0.05')
BQ = .05
DC = np.linspace(-.3, .3, 13)
def grid_q(gs):
    gt = np.concatenate([g.gl for g in gs]); best = (np.inf, None)
    for dc in DC:
        for dn in DN:
            e = rms(np.log10(np.concatenate([halo_gN(g, dn, dc)[0] for g in gs])) - np.log10(gt))
            if e < best[0]: best = (e, (dc, dn))
    return best
e, (dc, dn) = grid_q(GS); grade('QK halo response as knobs', [halo_gN(g, dn, dc)[0] for g in GS], f'(2 knobs; log c shift {dc:+.2f}, dn {dn:+.3f}; grid edge {dc in (DC[0], DC[-1])}, {dn in (DN[0], DN[-1])})')
e2, (dc2, dn2) = grid_q(EV); u = unseen([halo_gN(g, dn2, dc2)[0] for g in OD]); P(f' QK holdout (even-index: {dc2:+.2f}, {dn2:+.3f}) unseen rms {u:.4f} [{"PASS" if u <= .025 else "FAIL"}]')
gs_ = []
for g in GS:
    M = m200_of(g.Ms); c = np.interp(np.log10(M), LM, CG); R = (3 * M * Msun / (800 * np.pi * RHOC))**(1 / 3); rs = R / c
    gs_.append(2 * np.pi * G * (1 + 2 * BQ**2) * M * Msun / (4 * np.pi * rs**3 * mu(c)) * rs)
gs_ = np.array(gs_); lg = np.log10(gs_)
P(f'halo scale felt by DM, 2 pi G (1 + 2 beta^2) rho_s r_s: median {np.median(gs_) / A0:.3f} a0; boost factor {1 + 2 * BQ**2:.4f}')
g1('CQ halo scale (median)', np.median(gs_)); s = lg.std(); sh = lg[HOST].std()
P(f' CQ G4 rms all 171 {s:.3f}, hosts 11-12.5 {sh:.3f} dex [{"PASS" if sh <= .1 else "FAIL"} G4]')
P(' CQ Cassini: baryons uncoupled, no fifth force on baryons [PASS trivially]; field mass ~ H, no acceleration (A14 T8)')
P(f'[{time.time() - T0:.0f} s] colossus cosmology switches follow (lib arrays already built)')
def gsc(C, M=1e12, z=0):
    rc = C.rho_c(z) * C.h**2 * Msun / kpc**3; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3); c = float(CM.concentration(M * C.h, '200c', z, model='diemer19')); rs = R / c
    return 2 * np.pi * G * (1 + 2 * BQ**2) * M * Msun / (4 * np.pi * rs**3 * mu(c)) * rs
J = []
for OL, H0 in ((.70, 67.4), (.685, 73.), (.65, 73.)):
    C = cc.setCosmology(f'a30_{OL}_{H0}', dict(flat=True, H0=H0, Om0=1 - OL, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False))
    J.append((OL * C.rho_c(0) * C.h**2 * Msun / kpc**3, gsc(C)))
sl = [np.log(J[i][1] / J[0][1]) / np.log(J[i][0] / J[0][0]) for i in (1, 2)]
P(f' CQ G2 slopes at M 1e12 over J cosmologies: {sl[0]:+.3f}, {sl[1]:+.3f} [{"PASS" if all(abs(x - .5) <= .05 for x in sl) else "FAIL"} G2]')
CP = cc.setCosmology('a30_cpl', dict(flat=True, H0=67.4, Om0=.315, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False, de_model='w0wa', w0=W0, wa=WA))
P(f' control: colossus CPL rho_DE(z)/rho_DE0 at z 2.33 {CP.Ode(2.33) * CP.rho_c(2.33) / (CP.Ode(0) * CP.rho_c(0)):.4f} vs formula {rde_ratio(2.33):.4f}')
gt_ratio('CQ halo scale at M 1e12, CPL background', {z: gsc(CP, z=z) / gsc(CP) for z in ZB})
CL = cc.setCosmology('a30_lcdm', dict(flat=True, H0=67.4, Om0=.315, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False))
P(' (LCDM reference a(z)/a(0) at M 1e12: ' + ', '.join(f'{z}: {gsc(CL, z=z) / gsc(CL):.3f}' for z in ZB) + ')')
cc.setCurrent(cos)
P(f'\nruntime {time.time() - T0:.0f} s')
P('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
