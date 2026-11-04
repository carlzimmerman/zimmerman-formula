"""A32: the joint swoop, feedback/halo knobs (A25 15-knob point) and dark-energy parameters (CPL w0, wa; interaction
Q = xi(a) H rho_c) tuned at once, plus H-exponent terms; secondary with rho_DE hand terms. Per ../FROZEN_A32.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os, time, json, signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
from scipy.stats import qmc
from colossus.lss import mass_function as MF
T00 = time.time()
def tl(): return f'[{time.time() - T00:.0f} s]'
_s = open(os.path.join(HERE, 'recipe20.py'), encoding='utf-8').read(); exec(_s[_s.index('def cum_mass'):_s.index('def g_dc14')])
NG = len(GS); ALLI = list(range(NG)); ODD, EVEN = ALLI[::2], ALLI[1::2]
for g in GS:   # same per-galaxy attributes as recipe27
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); ok = vb2 > 0
    g.bul = float((np.abs(a[ok, 5]) > 0).any()); g.sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100; g.fg = max((g.Mb - g.Ms) / g.Mb, .01)
    g.gr = float(g.fg >= .5); g.lr = np.log(g.r); g.lmb = np.log(np.maximum(g.mb, 1e-30)); g.lgl = np.log10(g.gl)
LMSALL = np.array([np.log10(g.Ms) for g in GS]); LM0 = np.array([np.log10(m200_of(g.Ms)) for g in GS])
c_ = 2.998e8; ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZL = list(ZB)
GYR = 3.156e16
class Ctx: pass
BASE = Ctx(); BASE.z = 0.; BASE.rhoc = RHOC; BASE.CG = CG.copy(); BASE.tsf = 13.8 * GYR; BASE.tsidm = 10 * GYR
cc.setCurrent(cos)
# recipe27 knob table and recipe code, reused verbatim for the control
_s = open(os.path.join(HERE, 'recipe27.py'), encoding='utf-8').read()
exec(_s[_s.index('AH = np.gradient'):_s.index('print(f\'Tinker08')])
exec(_s[_s.index('# ---------------- knobs'):_s.index('# ---------------- SIDM response table')])
exec(_s[_s.index('# ---------------- the recipe'):_s.index('def lhs(')])
RDE0 = cos.Ode0 * RHOC; AN = c_ * np.sqrt(G * RDE0)
ck27 = json.load(open(os.path.join(HERE, 'recipe27_ckpt.json'))); W15 = [r for r in ck27['S2'] if r['k'] == 15][0]
ON = W15['on']; PW = np.array(W15['P']); assert not any(u in ON for u in ('SI', 'AC', 'HC'))
FR = free_of(ON); print(f'warm start: A25 Pareto 15 knobs, units {ON}, free {[NAMES[j] for j in FR]}, recorded table-mode rms {W15["rms"]:.4f}', flush=True)
# ---------------- recipe with family multipliers (copy of recipe27 gal without AC, SI, HC, which are off here)
FAM = ['SHMR', 'FB', 'CORE', 'CONTR', 'CONC']
def shmr_z(P, idx, z, dnx):
    dn, dm, db, dg = P[:4]; zt = z / (1 + z); x = 10**LMS / 10**(11.59 + dm + 1.195 * zt)
    s = 2 * (.0351 - .0247 * zt) * 10**(dn + dnx) * 10**LMS / (x**-(1.376 + db - .826 * zt) + x**(.608 + dg + .329 * zt)); i = np.argmax(s)
    ls, lm = np.log10(s[:i + 1]), LMS[:i + 1]; lMs = LMSALL[idx]; lM = np.interp(lMs, ls, lm)
    return lM + P[IX['sl']] * np.minimum(lMs - 9, 0)
def galm(i, P, ctx, lM, md):
    g = GS[i]; p = dict(zip(NAMES, P)); M = 10**lM; R = (3 * M * Msun / (4 * np.pi * 200 * ctx.rhoc))**(1 / 3)
    c = float(np.interp(lM, LM, ctx.CG)) * 10**p['dc'] * (M / 1e12)**p['sc'] * g.sb**p['N2'] * md['CONC']; A = max(.16 + p['N1'] * (lM - 12), .05); fb = min(g.Mb / M, .5)
    c = min(max(c, 1.01), 200.); gA = gammainc(3 / A, 2 / A * c**A)
    def Me(r): return np.maximum(M * Msun * gammainc(3 / A, 2 / A * (r * c / R)**A) / gA, 1e-30)
    e = 10**p['le'] * (g.Ms / M / .01)**p['a1'] * g.sb**p['a2'] * (g.fg / .5)**p['a4'] * md['FB']
    n = np.tanh(min(e, 50)); eta = 10**(p['le0'] + p['Dle0g'] * g.gr + p['Dle0b'] * g.bul) * (g.Ms / 1e9)**p['a3'] * g.sb**p['N5'] * md['CORE']
    f = np.clip(np.clip(p['f0'] + p['Df0g'] * g.gr + p['Df0b'] * g.bul + p['f1'] * (np.log10(g.Mb) - 9.5) + p['N4'] * np.log10(g.sb), -1, 1) * md['CONTR'], -1, 1)
    r = g.r; m0 = Me(r); ri = r.copy()
    for _ in range(12):
        mi = Me(ri); ri = .5 * ri + .5 * r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(r / (eta * 1.75 * g.Rd))**n
    if p['s14'] > 0:
        a_, b_, gm, lr = dc14_par(np.log10(g.Ms / M), p['s14']); cd = c * 10**lr; rs = R / cd / ((2 - gm) / (b_ - 2))**(1 / a_)
        rho = lambda x: (x / rs)**-gm * (1 + (x / rs)**a_)**(-(b_ - gm) / a_)
        rr, mm = cum_mass(rho, 1e-5 * rs, max(R, r[-1]) * 1.01, n=300, gin=gm); mR = np.interp(np.log(R), np.log(rr), mm)
        m = m * (np.interp(np.log(r), np.log(rr), mm) / mR) / (mu(r * c / R) / mu(c))
    return g.gb + G * m / r**2
ONE = {k: 1. for k in FAM}
d_ = max(np.abs(np.log10(a_) - np.log10(b_)).max() for a_, b_ in zip([galm(i, PW, BASE, l, ONE) for i, l in zip(ALLI, shmr_z(PW, ALLI, 0., 0.))], curves(PW, ON, mode='direct')))
print(f'control 1: recipe34 galm vs recipe27 gal at the warm point, max |dlog g| {d_:.2e} dex [{"PASS" if d_ < 1e-6 else "FAIL"} < 1e-6]', flush=True)
# ---------------- background and growth (own ODE; no radiation)
NA = 1201; LNA = np.linspace(np.log(1e-3), 0., NA); AA = np.exp(LNA); ZG = 1 / AA - 1; HSTEP = LNA[1] - LNA[0]
def bg(Om, Ob, w0, wa, x0, x1):
    """densities in units of rho_crit0 on the LNA grid; returns dict or None if the physical guard fails"""
    a = AA; rb = Ob * a**-3; rc = (Om - Ob) * a**-(3 + x0 + x1) * np.exp(x1 * (a - 1)); ode = 1 - Om
    F = a**(-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a)); xi = x0 + x1 * (1 - a); w = w0 + wa * (1 - a)
    q = xi * rc / F; I = np.concatenate([[0.], np.cumsum(.5 * (q[1:] + q[:-1]) * HSTEP)]); I = I - I[-1]   # integral from ln a = 0
    rd = F * (ode + I); E2 = rb + rc + rd
    zz = ZG <= 10
    if (rc[zz] <= 0).any() or (rd[zz] <= 0).any() or not np.all(np.isfinite(E2)) or abs(rd[0]) / (rb[0] + rc[0]) >= .05: return None
    dE2 = -3 * rb - 3 * rc - 3 * (1 + w) * rd; dl = .5 * dE2 / E2
    # growth: delta'' + (2 + dlnH/dlna) delta' = 1.5 (rho_c d_c + rho_b d_b)/E2, geodesic DM (coupling cancels), RK4 with step 2 HSTEP
    Om_c, Om_b = rc / E2, rb / E2; dc, db, u = AA[0], AA[0], AA[0]; Dc = np.empty(NA); Db = np.empty(NA); Dc[0], Db[0] = dc, db
    oc, ob, dlv = Om_c.tolist(), Om_b.tolist(), dl.tolist(); h2 = 2 * HSTEP
    def rhs(k, dc, db, u): return u, u, -(2 + dlv[k]) * u + 1.5 * (oc[k] * dc + ob[k] * db)
    k = 0
    while k + 2 < NA:
        k1 = rhs(k, dc, db, u); k2 = rhs(k + 1, dc + HSTEP * k1[0], db + HSTEP * k1[1], u + HSTEP * k1[2]); k3 = rhs(k + 1, dc + HSTEP * k2[0], db + HSTEP * k2[1], u + HSTEP * k2[2])
        k4 = rhs(k + 2, dc + h2 * k3[0], db + h2 * k3[1], u + h2 * k3[2])
        dc += h2 / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); db += h2 / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]); u += h2 / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]); k += 2
        Dc[k], Db[k] = dc, db
    ev = np.arange(0, NA, 2); Dm = (rc[ev] * Dc[ev] + rb[ev] * Db[ev]) / (rc[ev] + rb[ev])
    return dict(E2=E2, rd=rd, zD=ZG[ev], D=Dm)
def e2at(b, z): return float(np.interp(-z, -ZG, b['E2']))
def dat(b, z): return np.interp(-np.asarray(z), -b['zD'], b['D'])
CL = 400.; CCg = np.linspace(1.02, 200, 6000); YCg = CCg**3 * mu(1.) / mu(CCg)
def cmap(cL, z, bL, bm):
    """A20 Ludlow-style map of c(M, z) from LCDM reference bL to model bm (both normalised at a = 1e-3)."""
    rbar = 200 * e2at(bL, z) * cL**3 * mu(1.) / mu(cL)
    E2L = np.maximum.accumulate(bL['E2'][::-1]); zr = ZG[::-1]; zfL = np.interp(rbar / CL, E2L, zr)
    dlt = 1 / dat(bL, zfL) - 1 / dat(bL, z); iDm = np.maximum.accumulate((1 / bm['D'])[::-1]); zfm = np.interp(1 / dat(bm, z) + dlt, iDm, bm['zD'][::-1])
    E2m = np.maximum.accumulate(bm['E2'][::-1]); rbm = CL * np.interp(zfm, zr, E2m); return np.interp(rbm / (200 * e2at(bm, z)), YCg, CCg)
# growth control against colossus (LCDM base)
bL0 = bg(cos.Om0, cos.Ob0, -1, 0, 0, 0)
gd = max(abs(dat(bL0, z) / dat(bL0, 0.) / cos.growthFactor(z) - 1) for z in (.5, 1., 2.33, 5.))
print(f'control 2: own LCDM growth D(z)/D(0) vs colossus growthFactor at z 0.5, 1, 2.33, 5: max rel diff {gd:.1e} [{"PASS" if gd < 5e-3 else "FAIL"} < 5e-3]', flush=True)
# ---------------- environments (LCDM references from colossus, as recipe28 C1-A and Bz)
h0 = .674; S30 = cos.sigma(8., 30.)
def mkcos(name, H0, Om0, Ob0, s8): return cc.setCosmology(name, dict(flat=True, H0=H0, Om0=Om0, Ob0=Ob0, sigma8=s8, ns=.965, relspecies=False))
FS = [.5, 1., 2.]; ENV = {}
for f in FS:
    wm, wb, wd = .315 * h0**2, .0493 * h0**2, f * .685 * h0**2; h = np.sqrt(wm + wd)
    if f == 1.: C = cos; s8 = .811
    else:
        C = mkcos(f'a32_{f}_t', 100 * h, wm / h**2, wb / h**2, .811); s8 = .811 * S30 / C.sigma(8. * h / h0, 30.); C = mkcos(f'a32_{f}', 100 * h, wm / h**2, wb / h**2, s8)
    zs = [0.] + (ZL if f == 1. else [])
    ENV[f] = dict(h=C.h, Om=C.Om0, Ob=C.Ob0, rhoc0=C.rho_c(0) * C.h**2 * Msun / kpc**3, s8=s8,
                  CG={z: np.array([float(CM.concentration(10**m * C.h, '200c', z, model='diemer19')) for m in LM]) for z in zs})
    ENV[f]['bL'] = bg(C.Om0, C.Ob0, -1, 0, 0, 0); cc.setCurrent(cos)
    print(f' env f {f}: h {C.h:.4f}, Om0 {C.Om0:.4f}, sigma8 {s8:.4f}, rho_DE/rho_DE0 {(1 - C.Om0) * ENV[f]["rhoc0"] / RDE0:.4f}', flush=True)
assert np.allclose(ENV[1.]['CG'][0.], CG)
ROWS = [(1., 0.), (.5, 0.), (2., 0.)] + [(1., z) for z in ZL]
# ---------------- DE + exponent parameters
DEN = ['w0', 'wa', 'xi0', 'xi1']; DELO = np.array([-1.5, -3, -.3, -.3]); DEHI = np.array([-.3, 1.5, .3, .3]); DE_L = np.array([-1., 0., 0., 0.])
HN = [f'pH_{f}' for f in FAM]; RN = [f'pR_{f}' for f in FAM]
DESI = {'DESI+CMB+PantheonPlus': (-.838, -.62, .055, .21), 'DESI+CMB+Union3': (-.667, -1.09, .088, .30), 'DESI+CMB+DESY5': (-.752, -.86, .057, .215), 'DESI+CMB': (-.42, -1.75, .21, .58)}
def desi(w0, wa):
    out = {}
    for k, (m0, m1, s0, s1) in DESI.items():
        x, y, r = (w0 - m0) / s0, (wa - m1) / s1, -.9; out[k] = (x * x - 2 * r * x * y + y * y) / (1 - r * r)
    return out
class Par:
    """full parameter state: recipe vector P (recipe27 NAMES), de (4), pH (5), pR (5)"""
    def __init__(s, P, de, pH, pR): s.P, s.de, s.pH, s.pR = np.array(P, float), np.array(de, float), np.array(pH, float), np.array(pR, float)
def evaluate(S, idx=ALLI):
    """returns dict with z=0 residuals, a per row, slope, GT, guard flag; None-safe"""
    bm = {}
    for f in FS:
        b = bg(ENV[f]['Om'], ENV[f]['Ob'], *S.de)
        if b is None: return None
        bm[f] = b
    out = dict(a={}, S={}, cur0=None, gt={}, rz={}, rde={}, Hr={})
    for f, z in ROWS:
        E = ENV[f]; b = bm[f]; ctx = Ctx(); ctx.z = z; ctx.rhoc = E['rhoc0'] * e2at(b, z)
        ctx.CG = cmap(E['CG'][z], z, E['bL'], b) if not np.allclose(S.de, DE_L) else E['CG'][z]
        XH = np.sqrt(e2at(b, z)) * (E['h'] / h0) if z > 0 else E['h'] / h0
        XR = float(np.interp(-z, -ZG, b['rd'])) / (1 - E['Om']) * ((1 - E['Om']) * E['rhoc0'] / RDE0)
        md = {fam: XH**S.pH[k] * XR**S.pR[k] for k, fam in enumerate(FAM)}; dnx = np.log10(md.pop('SHMR')); md['SHMR'] = 1.
        lM = shmr_z(S.P, idx, z, dnx); cur = [galm(i, S.P, ctx, l, md) for i, l in zip(idx, lM)]
        gb = np.concatenate([GS[i].gb for i in idx]); gt = np.concatenate(cur); a = fit_a(gb, gt)
        out['a'][(f, z)] = a; out['S'][(f, z)] = float(np.sqrt(((np.log10(gt) - np.log10(law(gb, a)))**2).mean()))
        if (f, z) == (1., 0.): out['cur0'] = cur
        if f == 1.: out['rde'][z] = XR; out['Hr'][z] = float(np.sqrt(e2at(b, z) / e2at(ENV[1.]['bL'], z)))
    a0 = out['a'][(1., 0.)]
    out['slope'] = float(np.polyfit(np.log(FS), np.log([out['a'][(f, 0.)] for f in FS]), 1)[0])
    for z in ZL:
        out['rz'][z] = out['a'][(1., z)] / a0; out['gt'][z] = float(np.log10(out['rz'][z]) - .5 * np.log10(out['rde'][z]))
    return out
def resvec(S, idx, lam):
    o = evaluate(S, idx); N = sum(len(GS[i].r) for i in idx)
    if o is None: return np.concatenate([np.full(N, 10. / np.sqrt(N)), [10. * lam] * 4]), None
    d = np.concatenate([np.log10(c) - GS[i].lgl for i, c in zip(idx, o['cur0'])]) / (.02 * np.sqrt(N))
    return np.concatenate([d, [lam * (o['slope'] - .5) / .05], [lam * o['gt'][z] / .05 for z in ZL]]), o
# ---------------- free-vector packing
def layout(stage):
    names = [NAMES[j] for j in FR] + DEN + HN + (RN if stage == 'sec' else [])
    lo = np.concatenate([LO[FR], DELO, -5 * np.ones(5), (-5 * np.ones(5) if stage == 'sec' else [])])
    hi = np.concatenate([HI[FR], DEHI, 5 * np.ones(5), (5 * np.ones(5) if stage == 'sec' else [])]); return names, lo, hi
def unpack(x, base, stage):
    P = base.P.copy(); P[FR] = x[:15]; de = x[15:19]; pH = x[19:24]; pR = x[24:29] if stage == 'sec' else base.pR * 0
    return Par(P, de, pH, pR)
def pack(S, stage): return np.concatenate([S.P[FR], S.de, S.pH] + ([S.pR] if stage == 'sec' else []))
def tune(S0, stage, idx, lam, nfev, lo=None, hi=None):
    names, lo_, hi_ = layout(stage); lo = lo_ if lo is None else lo; hi = hi_ if hi is None else hi; eps = 1e-6 * (hi - lo)
    x0 = np.clip(pack(S0, stage), lo + eps, hi - eps); NC = [0]
    def fn(x): NC[0] += 1; return resvec(unpack(x, S0, stage), idx, lam)[0]
    r = least_squares(fn, x0, bounds=(lo, hi), x_scale='jac', diff_step=.02, max_nfev=nfev)
    S = unpack(r.x, S0, stage); atb = [n for n, v, a_, b_ in zip(names, r.x, lo, hi) if min(v - a_, b_ - v) < 1e-3 * (b_ - a_)]
    return S, float(2 * r.cost), atb, NC[0]
# ---------------- checkpoint
CK = os.path.join(HERE, 'recipe34.json'); ST = json.load(open(CK)) if os.path.exists(CK) else {}
def save(): json.dump(ST, open(CK + '.tmp', 'w'), default=float); os.replace(CK + '.tmp', CK)
signal.signal(signal.SIGTERM, lambda *a: (save(), print('SIGTERM: checkpoint saved', flush=True), sys.exit(0)))
def srec(S, cost, atb, extra=None): return dict(P=S.P.tolist(), de=S.de.tolist(), pH=S.pH.tolist(), pR=S.pR.tolist(), cost=cost, atb=atb, **(extra or {}))
def sload(d): return Par(d['P'], d['de'], d['pH'], d['pR'])
WARM = Par(PW, DE_L, np.zeros(5), np.zeros(5))
t = time.time(); o = evaluate(WARM); print(f'timing: one joint evaluation (6 rows x 171 galaxies) {time.time() - t:.2f} s', flush=True)
t = time.time(); _o = evaluate(Par(PW, [-.75, -.86, -.005, 0.], np.zeros(5), np.zeros(5))); print(f"timing: with DE mapping (w0 -0.75, wa -0.86, xi0 -0.005) {time.time() - t:.2f} s, guard ok {_o is not None}", flush=True)
_o = evaluate(Par(PW, [-.75, -.86, .005, .005], np.zeros(5), np.zeros(5))); print(f'guard check: xi0 = xi1 = +0.005 (dark matter into dark energy) with w0 -0.75, wa -0.86 passes the guard: {_o is not None}', flush=True)
# control 3: map identity at LCDM parameters
b1 = bg(ENV[1.]['Om'], ENV[1.]['Ob'], -1, 0, 0, 0); cm = max(np.abs(cmap(ENV[1.]['CG'][z], z, ENV[1.]['bL'], b1) / ENV[1.]['CG'][z] - 1).max() for z in [0.] + ZL)
print(f'control 3: Ludlow map at LCDM parameters returns Diemer19, max rel diff {cm:.1e} [{"PASS" if cm < 1e-3 else "FAIL"} < 1e-3]', flush=True)
if os.environ.get('A32_TEST'):
    print('A32_TEST stop'); sys.exit(0)
# ---------------- grading
def grade_pt(tag, S, nk, hand, stage, hold=None):
    o = evaluate(S); s = stats(o['cur0']); grade(f'A32 {tag}', o['cur0'], f'({nk} knobs, {hand} rho_DE hand terms)')
    a0 = o['a'][(1., 0.)]; ke = a0 / AN; g1 = abs(np.log10(ke / .5)) <= .05; g2 = abs(o['slope'] - .5) <= .05
    g3 = all(ZB[z][0] <= o['rz'][z] <= ZB[z][1] for z in ZL); gt = all(abs(o['gt'][z]) <= .05 for z in ZL)
    lM = shmr_z(S.P, ALLI, 0., np.log10(1.)); sel = [i for i in ALLI if 11 <= lM[i] <= 12.5]; la = np.log10([fit_a(GS[i].gb, o['cur0'][i]) for i in sel]); g4 = la.std() <= .1
    ex = s['e1'] <= .02 and s['e2'] <= .04 and s['e3'] <= .02
    xi = S.de[2] + S.de[3] * (1 - 1 / (1 + np.array([0.] + ZL))); dz = desi(S.de[0], S.de[1]); ins = min(dz.values()) <= 6.18
    print(f' DE: w0 {S.de[0]:+.3f} wa {S.de[1]:+.3f} xi0 {S.de[2]:+.4f} xi1 {S.de[3]:+.4f}; xi(z 0..2.33) {np.round(xi, 4).tolist()} [{"plausible" if np.abs(xi).max() <= .01 else "outside |xi| <= 0.01"}]; '
          f'DESI dchi2 ' + ', '.join(f'{k} {v:.1f}' for k, v in dz.items()) + f' [{"INSIDE" if ins else "OUTSIDE"} DESI-allowed]', flush=True)
    print(f' exponents H: ' + ' '.join(f'{f}^{p:+.3f}' for f, p in zip(FAM, S.pH)) + ('; rho_DE: ' + ' '.join(f'{f}^{p:+.3f}' for f, p in zip(FAM, S.pR)) if stage == 'sec' else ''), flush=True)
    print(f' G1 a {a0:.4e} kappa_eff {ke:.3f} [{"PASS" if g1 else "FAIL"}] (inherited); G2 a(f)/a(1) ' + ' '.join(f'{o["a"][(f, 0.)] / a0:.4f}' for f in FS) + f', slope {o["slope"]:+.4f} [{"PASS" if g2 else "FAIL"} G2]', flush=True)
    print(f' z rows: a(z)/a(0) ' + ' '.join(f'{o["rz"][z]:.3f}' for z in ZL) + f' [{"PASS" if g3 else "FAIL"} G3]; rho_DE(z)/rho_DE0 ' + ' '.join(f'{o["rde"][z]:.3f}' for z in ZL)
          + '; GT ' + ' '.join(f'{o["gt"][z]:+.3f}' for z in ZL) + f' [{"PASS" if gt else "FAIL"} GT]; shape S ' + ' '.join(f'{o["S"][(1., z)]:.4f}' for z in ZL)
          + '; H/H_LCDM ' + ' '.join(f'{o["Hr"][z]:.3f}' for z in ZL), flush=True)
    print(f' G4 {len(sel)} hosts rms log a_i {la.std():.3f} [{"PASS" if g4 else "FAIL"}]; G5 by definition; median dlogM200 vs base SHMR {np.median(lM - LM0):+.2f}', flush=True)
    hl = None
    if hold is not None:
        Sh = sload(hold); oe = evaluate(Sh, EVEN); hl = stats(oe['cur0'], EVEN)['e1']
        ae = oe['a'][(1., 0.)]; print(f' holdout (clean, tuned on GS[::2] from warm): unseen GS[1::2] rms to law {hl:.4f} [{"PASS" if hl <= .025 else "FAIL"} <= 0.025]; on GS[1::2] slope {oe["slope"]:+.4f}, GT '
                                     + ' '.join(f'{oe["gt"][z]:+.3f}' for z in ZL), flush=True)
    jp = ex and g2 and gt and (hl is not None and hl <= .025)
    print(f' VERDICT {tag}: E1-E3 {"PASS" if ex else "FAIL"}; G2 {"PASS" if g2 else "FAIL"}; GT {"PASS" if gt else "FAIL"}; holdout {"n/a" if hl is None else ("PASS" if hl <= .025 else "FAIL")}; JOINT {"PASS" if jp else "FAIL"} {tl()}', flush=True)
    return dict(e1=s['e1'], e2=s['e2'], e3=s['e3'], obs=s['obs'], slope=o['slope'], gt=[o['gt'][z] for z in ZL], rz=[o['rz'][z] for z in ZL], g=[bool(g1), bool(g2), bool(g3), bool(gt), bool(g4)],
                hold=hl, joint=bool(jp), desi=bool(ins), dz=dz, maxgt=float(max(abs(o['gt'][z]) for z in ZL)))
# ---------------- S0 control
print('\n######## S0 control: warm 15-knob point, LCDM, no exponents', flush=True)
G0 = grade_pt('S0 control (LCDM)', WARM, 15, 0, 'pri'); ST['G_S0'] = G0; save()
# ---------------- S1 primary multi-start
names, lo, hi = layout('pri'); NS = 6
X = qmc.LatinHypercube(d=9, seed=34).random(4)
def start(s):
    if s == 0: return WARM
    if s == 1: return Par(PW, [-.752, -.86, 0., 0.], np.zeros(5), np.zeros(5))
    v = lo[15:] + X[s - 2] * (hi[15:] - lo[15:]); return Par(PW, v[:4], v[4:9], np.zeros(5))
ST.setdefault('S1', [])
for s in range(len(ST['S1']), NS):
    S0 = start(s)
    if bg(.315, .0493, *S0.de) is None:   # guard-violating LHS start: move xi to 0 (disclosed in output)
        S0.de[2:] = 0.; print(f' S1 start {s}: LHS DE point violates the physical guard; xi set to 0', flush=True)
        if bg(.315, .0493, *S0.de) is None: S0.de[1] = min(S0.de[1], -S0.de[0] - .2); print(f'  and wa capped to {S0.de[1]:+.3f}', flush=True)
    S, cost, atb, nc = tune(S0, 'pri', ALLI, 1., 40); ST['S1'].append(srec(S, cost, atb, dict(nc=nc))); save()
    print(f'S1 start {s}: cost {cost:.2f}, w0 {S.de[0]:+.3f} wa {S.de[1]:+.3f} xi0 {S.de[2]:+.3f} xi1 {S.de[3]:+.3f}, evals {nc}, at bound {atb} {tl()}', flush=True)
B1 = min(ST['S1'], key=lambda d: d['cost']); print(f'S1 best cost {B1["cost"]:.2f}; all sorted {sorted(round(d["cost"], 2) for d in ST["S1"])}', flush=True)
# ---------------- S2 trade-off
ST.setdefault('S2', {}); cur = sload(B1)
for lam in (.1, .3, 0., 3., 10.):
    k = str(lam)
    if k not in ST['S2']:
        S, cost, atb, nc = tune(sload(B1) if lam in (0., 3.) else cur, 'pri', ALLI, lam, 25); ST['S2'][k] = srec(S, cost, atb); save()
    cur = sload(ST['S2'][k]); o = evaluate(cur); e1 = stats(o['cur0'])['e1']
    print(f'S2 lambda {lam}: E1 {e1:.4f}, slope {o["slope"]:+.3f}, GT ' + ' '.join(f'{o["gt"][z]:+.3f}' for z in ZL) + f', max|GT| {max(abs(o["gt"][z]) for z in ZL):.3f}; w0 {cur.de[0]:+.3f} wa {cur.de[1]:+.3f} xi0 {cur.de[2]:+.3f} xi1 {cur.de[3]:+.3f}; at bound {ST["S2"][k]["atb"]} {tl()}', flush=True)
    ST['S2'][k]['curve'] = dict(e1=e1, slope=o['slope'], maxgt=max(abs(o['gt'][z]) for z in ZL)); save()
# ---------------- S3 DESI-constrained
if 'S3' not in ST:
    lo3, hi3 = lo.copy(), hi.copy(); lo3[15:19] = [-.866, -1.29, -.01, -.01]; hi3[15:19] = [-.638, -.43, .01, .01]; best = None
    for S0 in (sload(B1), Par(PW, [-.752, -.86, 0., 0.], sload(B1).pH, np.zeros(5))):
        S, cost, atb, _ = tune(S0, 'pri', ALLI, 1., 40, lo3, hi3); print(f'S3 start: cost {cost:.2f} at bound {atb} {tl()}', flush=True)
        if best is None or cost < best[1]: best = (S, cost, atb)
    ST['S3'] = srec(*best); save()
# ---------------- S4 secondary with rho_DE hand terms
if 'S4' not in ST:
    S, cost, atb, _ = tune(sload(B1), 'sec', ALLI, 1., 40); ST['S4'] = srec(S, cost, atb); save(); print(f'S4 cost {cost:.2f} at bound {atb} {tl()}', flush=True)
# ---------------- holdouts (clean: from warm, tuned on GS[::2])
for key, stage in (('H1', 'pri'), ('H4', 'sec')):
    if key not in ST:
        S, cost, atb, _ = tune(WARM, stage, ODD, 1., 30); ST[key] = srec(S, cost, atb); save(); print(f'{key} holdout tune ({stage}) on GS[::2]: cost {cost:.2f} {tl()}', flush=True)
# ---------------- grades
RES = {}
print(f'\n######## S1 primary joint best (24 knobs: 15 recipe + 4 DE + 5 H exponents); knobs at bound {B1["atb"]}', flush=True)
RES['S1'] = grade_pt('S1 primary joint', sload(B1), 24, 0, 'pri', ST['H1'])
for lam in ('0.0', '0.1', '0.3', '3.0', '10.0'):
    print(f'\n######## S2 lambda {lam}; knobs at bound {ST["S2"][lam]["atb"]}', flush=True); RES['S2_' + lam] = grade_pt(f'S2 lambda {lam}', sload(ST['S2'][lam]), 24, 0, 'pri')
print(f'\n######## S3 DESI-constrained (24 knobs); knobs at bound {ST["S3"]["atb"]}', flush=True); RES['S3'] = grade_pt('S3 DESI-constrained', sload(ST['S3']), 24, 0, 'pri')
print(f'\n######## S4 secondary with rho_DE hand terms (29 knobs, 5 hand terms); knobs at bound {ST["S4"]["atb"]}', flush=True); RES['S4'] = grade_pt('S4 secondary', sload(ST['S4']), 29, 5, 'sec', ST['H4'])
ST['RES'] = RES; save()
print('\n==== A32 TRADE-OFF TABLE ====\n tag | E1 | E2 | E3 | slope | max|GT| | a(z)/a(0) | DESI | JOINT')
for k, r in RES.items(): print(f' {k} | {r["e1"]:.4f} | {r["e2"]:.4f} | {r["e3"]:.4f} | {r["slope"]:+.3f} | {r["maxgt"]:.3f} | {" ".join(f"{x:.2f}" for x in r["rz"])} | {"in" if r["desi"] else "out"} | {"PASS" if r["joint"] else "FAIL"}')
jp = [k for k, r in RES.items() if r['joint']]
print(f'\nA32 VERDICT: {"JOINT PASS at " + str(jp) if jp else "NO joint setting passes E1-E3, holdout, G2 and GT together"}; primary (no rho_DE hand term) G2+GT both pass at: {[k for k in RES if k != "S4" and RES[k]["g"][1] and RES[k]["g"][3]] or "none"} {tl()}')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
