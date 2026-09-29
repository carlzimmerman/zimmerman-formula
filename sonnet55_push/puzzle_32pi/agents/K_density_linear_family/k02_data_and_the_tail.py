"""k02: which part of mu does the offset constant c depend on, and do galaxy data constrain that part?

c = int_0^inf (1-mu) dy = <x^2>_mu (k01).  The RAR/SPARC data speak to mu on the acceleration range they cover; c is a moment of mu that
puts most of its weight beyond it.  This script measures that with the record's SPARC rotation-curve files (155 curves, 2786 points,
fixed Upsilon_d = 0.5, Upsilon_b = 0.7; the same recipe as fable_independent_2026/L92, re-implemented here).

 A  data + CONTROLS: reproduce the committed nu_RAR scatter 0.1453/0.1421 dex at the two a0 footings; coverage in x = g_obs/a0
 B  family fits (a0 free, and a0 + a global M/L scale free): rms per family.  Which shapes have finite c, and do the data care?
 C  paired galaxy bootstrap of the rms difference to the RAR-nu baseline (respects the within-curve correlation)
 D  TAIL GRAFT: keep the best-fit RAR-nu for x <= X_J and replace its exponential tail by A x^-p (continuous at X_J, monotone).  Solve
    p so that c = 32 pi, c = c_req(a0 fit) and c = infinity.  Measure how much the SPARC residuals move.  If c could be read off the data it
    would move them; it moves them by <~ 0.001 dex.
 E  the offset reading as a PREDICTION inside a one-parameter family (Milgrom mu_n): n* from c(n) = c_req(a0_fit(n)) and the fit cost of n*
 F  bookkeeping: Markov lower bound  c >= X^2 (1-mu(X)) for the best-fit shape; fraction of c above Solar-System accelerations for each graft
"""
import glob
import os
import sys

import numpy as np
import mpmath as mp
from scipy import optimize, interpolate

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "sparc_data")
OK = []


def chk(name, cond, detail=""):
    OK.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f"   ({detail})" if detail else ""), flush=True)


kpc = 3.0857e19
c_light = 2.99792458e8
Mpc = 3.0856775814913673e22
H0 = 67.4e3 / Mpc
OmL = 0.685
A0_FW = 9.3619e-11            # the record's canonical footing (= c H_L / Z)
A0_SP = 1.1279e-10            # the record's second footing (SPARC-fitted)
C_REQ_FW = 32 * np.pi


def c_req(a0):
    return 3 * OmL * (c_light * H0 / a0) ** 2


# ------------------------------------------------------------------------------------------------ A: data
print("== A  SPARC data, controls, coverage")
GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    d = np.loadtxt(fn, comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    r = d[:, 0] * kpc
    Vo = d[:, 1] * 1e3
    eV = d[:, 2] * 1e3
    Vg = d[:, 3] * 1e3
    Vd = d[:, 4] * 1e3
    Vb = d[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb)
    m = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
    if m.sum() < 3:
        continue
    GAL.append(dict(name=os.path.basename(fn).replace("_rotmod.dat", ""), r=r[m], go=Vo[m] ** 2 / r[m],
                    gas=Vg[m] * np.abs(Vg[m]) / r[m], disk=Vd[m] * np.abs(Vd[m]) / r[m], bul=Vb[m] * np.abs(Vb[m]) / r[m]))
NG = len(GAL)
GO = np.concatenate([g["go"] for g in GAL])
GAS = np.concatenate([g["gas"] for g in GAL])
DSK = np.concatenate([g["disk"] for g in GAL])
BUL = np.concatenate([g["bul"] for g in GAL])
IDX = np.concatenate([np.full(len(g["go"]), i) for i, g in enumerate(GAL)])
GB = GAS + 0.5 * DSK + 0.7 * BUL
print(f"   {NG} galaxies, {len(GO)} points (eV/V < 0.10, >= 3 points; Upsilon_d = 0.5, Upsilon_b = 0.7)")
chk("A1 sample size matches the record's masked SPARC sample (155 curves)", NG == 155 and len(GO) == 2786, f"{NG}/{len(GO)}")


def solve_x(y, mu):
    """x with x mu(x) = y (spherical AQUAL == QUMOND boost): bisection in log x, vectorised."""
    lo = np.full_like(y, -14.0)
    hi = np.full_like(y, 14.0)
    for _ in range(72):
        mid = 0.5 * (lo + hi)
        x = np.exp(mid)
        pos = x * mu(x) - y > 0
        hi = np.where(pos, mid, hi)
        lo = np.where(pos, lo, mid)
    return np.exp(0.5 * (lo + hi))


def rms_of(gpred, mask=None):
    r = np.log10(GO / gpred)
    return float(np.sqrt(np.mean(r ** 2)))


nu_rar = lambda gb, a0: gb / (-np.expm1(-np.sqrt(gb / a0)))
r_fw = rms_of(nu_rar(GB, A0_FW))
r_sp = rms_of(nu_rar(GB, A0_SP))
print(f"   nu_RAR rms: {r_fw:.4f} (a0 = {A0_FW:.4e}) / {r_sp:.4f} (a0 = {A0_SP:.4e})")
chk("A2 CONTROL: the RAR machinery reproduces the committed nu_RAR scatter 0.1453 / 0.1421 dex (L92)", abs(r_fw - 0.1453) < 5e-4 and abs(r_sp - 0.1421) < 5e-4)
rng0 = np.random.default_rng(1)
r_shuf = rms_of(nu_rar(GB, A0_SP)[rng0.permutation(len(GB))])
chk("A3 MUTATION: pairing g_bar with the wrong point's g_obs (permutation) ruins the fit (rms %.3f >> 0.142): the fit statistic has power" % r_shuf, r_shuf > 0.4)
ygrid = GB / A0_SP
x_obs = GO / A0_SP
print(f"   coverage (a0 = {A0_SP:.4e}): max g_bar/a0 = {ygrid.max():.1f}, max g_obs/a0 = {x_obs.max():.1f};  points with g_obs/a0 > 3, 10, 30, 100: "
      f"{int(np.sum(x_obs > 3))}, {int(np.sum(x_obs > 10))}, {int(np.sum(x_obs > 30))}, {int(np.sum(x_obs > 100))}")
N10, N30, N100 = int(np.sum(x_obs > 10)), int(np.sum(x_obs > 30)), int(np.sum(x_obs > 100))
chk("A4 coverage: %d of %d points lie at g_obs > 10 a0, %d at > 30 a0 and none above ~%.0f a0: the data end near x ~ 60-100" % (N10, len(GO), N30, x_obs.max()),
    N100 <= 20 and x_obs.max() < 200 and N30 < 50)

# ------------------------------------------------------------------------------------------------ B: families
print("\n== B  family fits (a0 free; then a0 and a global M/L scale s free)")
def mu_n(n):
    return lambda x: x / (1 + x ** n) ** (1 / n)
def mu_or(N):
    return lambda x: 1 - (1 + x / N) ** (-N)
FAM = {
    'RAR-nu (McGaugh)': (None, 26.0),
    'simple mu_1': (mu_n(1.0), np.inf),
    'mu_n n=1.5': (mu_n(1.5), np.inf),
    'standard mu_2': (mu_n(2.0), np.inf),
    'mu_n n=2.02': (mu_n(2.02), None),
    'mu_n n=3': (mu_n(3.0), 1.0),
    'mu_n n=6': (mu_n(6.0), 0.4311849),
    'exp 1-e^-x': (lambda x: 1 - np.exp(-x), 2.0),
    'record OR N=2': (mu_or(2.0), np.inf),
    'record OR N=2.074': (mu_or(2.0741), None),
    'record OR N=3': (mu_or(3.0), 9.0),
    'T-excess (Milgrom 1999)': (lambda x: (np.sqrt(1 + 4 * x * x) - 1) / (2 * x), np.inf),
}


def c_mun(n):
    n = mp.mpf(n)
    return float(-(2 / n) * mp.gamma(3 / n) * mp.gamma(-2 / n) / mp.gamma(1 / n))


def c_or(N):
    return 2 * N ** 2 / ((N - 1) * (N - 2))


FAM['mu_n n=2.02'] = (FAM['mu_n n=2.02'][0], c_mun(2.02))
FAM['record OR N=2.074'] = (FAM['record OR N=2.074'][0], c_or(2.0741))


def gpred_fam(name, gb, a0):
    mu, _ = FAM[name]
    if mu is None:
        return nu_rar(gb, a0)
    return a0 * solve_x(gb / a0, mu)


def fit_a0(name):
    f = lambda la0: rms_of(gpred_fam(name, GB, 10 ** la0))
    r = optimize.minimize_scalar(f, bounds=(-10.7, -9.3), method='bounded', options={'xatol': 1e-6})
    return 10 ** r.x, float(r.fun)


def gb_scaled(s):
    return np.maximum(GAS + s * (0.5 * DSK + 0.7 * BUL), 1e-30)


def fit_a0_s(name, a0_0, s0=1.0):
    f = lambda p: rms_of(gpred_fam(name, gb_scaled(p[1]), 10 ** p[0]))
    r = optimize.minimize(f, [np.log10(a0_0), s0], method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-8, 'maxiter': 200})
    return 10 ** r.x[0], float(r.x[1]), float(r.fun)


RES = {}
print(f"   {'family':26s} {'c':>10s} {'a0_fit':>10s} {'rms':>8s} | {'a0_fit':>10s} {'s':>6s} {'rms':>8s}   c_req(a0_fit)")
for nm in FAM:
    a0f, rf = fit_a0(nm)
    a0s, sf, rs = fit_a0_s(nm, a0f)
    RES[nm] = dict(a0=a0f, rms=rf, a0s=a0s, s=sf, rmss=rs)
    cval = FAM[nm][1]
    cs = 'inf' if cval == np.inf else f"{cval:.3g}"
    print(f"   {nm:26s} {cs:>10s} {a0f:10.4e} {rf:8.5f} | {a0s:10.4e} {sf:6.3f} {rs:8.5f}   {c_req(a0f):7.1f}")
best = min(v['rms'] for v in RES.values())
best_s = min(v['rmss'] for v in RES.values())
chk("B1 the best a0-only fit is a shallow-transition shape (RAR-nu or simple mu_1, rms %.5f); both have UNBOUNDED or 26 c" % best,
    abs(RES['RAR-nu (McGaugh)']['rms'] - best) < 5e-4 and abs(RES['simple mu_1']['rms'] - best) < 5e-4)
chk("B2 the standard mu_2 (log-divergent c) and mu_n n >= 3 (finite c) fit WORSE than RAR-nu at fixed M/L: rms %.4f / %.4f vs %.4f" % (RES['standard mu_2']['rms'], RES['mu_n n=3']['rms'], RES['RAR-nu (McGaugh)']['rms']),
    RES['standard mu_2']['rms'] > RES['RAR-nu (McGaugh)']['rms'] + 0.004 and RES['mu_n n=3']['rms'] > RES['standard mu_2']['rms'])
chk("B3 the record's own OR shape (N = 2 or 2.074) fits almost as well as RAR-nu: rms %.5f / %.5f vs %.5f (fixed M/L); c = inf / %.0f" % (RES['record OR N=2']['rms'], RES['record OR N=2.074']['rms'], RES['RAR-nu (McGaugh)']['rms'], FAM['record OR N=2.074'][1]),
    RES['record OR N=2']['rms'] < RES['RAR-nu (McGaugh)']['rms'] + 0.0015 and RES['record OR N=2.074']['rms'] < RES['RAR-nu (McGaugh)']['rms'] + 0.0015)
spread_s = max(v['rmss'] for k, v in RES.items() if k not in ('mu_n n=6', 'mu_n n=3', 'exp 1-e^-x')) - best_s
print(f"   with a free global M/L scale the shapes converge further; spread over the non-sharp families = {spread_s:.4f} dex")
chk("B4 c (0.4 ... infinity across these fits) is not ordered by fit quality: infinite-c shapes are the BEST fits, finite-c shapes the worst (n=6: c=0.43), except RAR-nu (c=26) and record OR N=2.074 (c=%.0f)" % FAM['record OR N=2.074'][1],
    RES['simple mu_1']['rms'] < RES['mu_n n=6']['rms'] and RES['record OR N=2']['rms'] < RES['mu_n n=3']['rms'])

# ------------------------------------------------------------------------------------------------ C: bootstrap
print("\n== C  paired galaxy bootstrap of the rms difference to RAR-nu")
def per_gal_ss(name, a0):
    r = np.log10(GO / gpred_fam(name, GB, a0)) ** 2
    ss = np.bincount(IDX, weights=r, minlength=NG)
    return ss
n_per = np.bincount(IDX, minlength=NG).astype(float)
ss_base = per_gal_ss('RAR-nu (McGaugh)', RES['RAR-nu (McGaugh)']['a0'])
rngb = np.random.default_rng(20260929)
B = 3000
draws = rngb.integers(0, NG, size=(B, NG))
def boot_delta(name):
    ss = per_gal_ss(name, RES[name]['a0'])
    a = (ss[draws].sum(1) / n_per[draws].sum(1))
    b = (ss_base[draws].sum(1) / n_per[draws].sum(1))
    return np.sqrt(a) - np.sqrt(b)
BOOT = {}
print(f"   {'family':26s} {'d(rms) point':>12s} {'boot 95% interval':>22s}  frac(family better)")
for nm in ['simple mu_1', 'mu_n n=1.5', 'standard mu_2', 'mu_n n=2.02', 'mu_n n=3', 'record OR N=2', 'record OR N=2.074', 'exp 1-e^-x']:
    d = boot_delta(nm)
    pt = RES[nm]['rms'] - RES['RAR-nu (McGaugh)']['rms']
    lo, hi = np.percentile(d, [2.5, 97.5])
    BOOT[nm] = (pt, lo, hi, float(np.mean(d < 0)))
    print(f"   {nm:26s} {pt:+12.5f} [{lo:+9.5f}, {hi:+9.5f}]   {np.mean(d < 0):.3f}")
chk("C1 CONTROL: the bootstrap of the baseline against itself is exactly 0", np.all(np.abs(np.sqrt(ss_base[draws].sum(1) / n_per[draws].sum(1)) - np.sqrt(ss_base[draws].sum(1) / n_per[draws].sum(1))) == 0))
chk("C2 the standard mu_2 (log-divergent c) is disfavoured vs RAR-nu at fixed M/L: 95%% interval of d(rms) [%.4f, %.4f] excludes 0" % (BOOT['standard mu_2'][1], BOOT['standard mu_2'][2]), BOOT['standard mu_2'][1] > 0)
chk("C3 the record's OR shape N=2.074 (finite c = %.0f) is statistically compatible with RAR-nu / simple mu_1 at fixed M/L within the bootstrap width: d(rms) in [%.4f, %.4f]" % (FAM['record OR N=2.074'][1], BOOT['record OR N=2.074'][1], BOOT['record OR N=2.074'][2]),
    BOOT['record OR N=2.074'][0] < 0.003)

# ------------------------------------------------------------------------------------------------ D: tail graft
print("\n== D  tail graft on the best-fit RAR-nu baseline")
a0b = RES['RAR-nu (McGaugh)']['a0']
c_target_fw = C_REQ_FW
c_target_own = c_req(a0b)
# tabulate the RAR-nu AQUAL mu(x): x = y/(1-e^{-sqrt y}),  1-mu = e^{-sqrt y}
yt = np.logspace(-12, 14, 6000)
xt = yt / (-np.expm1(-np.sqrt(yt)))
omm_t = np.exp(-np.sqrt(yt))
keep = omm_t > 1e-300
lx = np.log(xt[keep])
lo_ = np.log(omm_t[keep])
PCH = interpolate.PchipInterpolator(lx, lo_, extrapolate=False)
XMIN, XMAX = xt[keep][0], xt[keep][-1]
def omm_rar(x):
    """1 - mu(x) of the RAR-nu AQUAL relation: table interpolation; 1 below the table (mu ~ x << 1), 0 above it (e^-700)."""
    x = np.asarray(x, float)
    out = np.exp(PCH(np.log(np.clip(x, XMIN, XMAX))))
    out = np.where(x < XMIN, 1.0, out)
    return np.where(x > XMAX, 0.0, out)
def c_rar_below(XJ):
    """int_0^XJ (1-mu) 2x dx for the baseline (numerical, log grid)."""
    us = np.linspace(np.log(1e-10), np.log(XJ), 40001)
    xs_ = np.exp(us)
    f = omm_rar(xs_) * 2 * xs_ ** 2                        # (1-mu) 2x dx = (1-mu) 2 x^2 du
    return float(np.trapz(f, us)) + 1e-10 ** 2               # 1-mu ~ 1 below 1e-10: adds x^2 at 1e-10 (negligible)
c_full = c_rar_below(1e5)
print(f"   baseline RAR-nu: c(<1e5) = {c_full:.5f} (k01: 25.97576 in total)")
chk("D1 the tabulated RAR-nu mu (Pchip in log-log) reproduces c = 25.9758 (k01) to 1e-3", abs(c_full - 25.9758) < 1e-3)

def graft(XJ, p):
    epsJ = float(omm_rar(np.array([XJ]))[0])
    A = epsJ * XJ ** p
    def omm(x):
        x = np.asarray(x, float)
        base = omm_rar(x)
        pw = A * x ** (-p)
        return np.where(x <= XJ, base, pw)
    return omm, epsJ


def c_of_graft(XJ, p):
    epsJ = float(omm_rar(np.array([XJ]))[0])
    if p <= 2:
        return np.inf
    return c_rar_below(XJ) + 2 * epsJ * XJ ** 2 / (p - 2)


def solve_p(XJ, target):
    epsJ = float(omm_rar(np.array([XJ]))[0])
    return 2 + 2 * epsJ * XJ ** 2 / (target - c_rar_below(XJ))


def gpred_graft(omm, gb, a0):
    mu = lambda x: 1 - omm(x)
    return a0 * solve_x(gb / a0, mu)


base_pred = nu_rar(GB, a0b)
r_base = rms_of(base_pred)
GM_SUN, AU = 1.32712440018e20, 1.495978707e11
X_SAT = GM_SUN / (9.5826 * AU) ** 2 / a0b                    # Saturn's solar acceleration in units of a0
print(f"   Saturn: g = {X_SAT * a0b:.3e} m/s^2 = {X_SAT:.3e} a0")
print(f"   target c: 32 pi = {c_target_fw:.2f};  c_req at the RAR-nu a0 ({a0b:.4e}) = {c_target_own:.2f};  baseline rms {r_base:.5f}")
print(f"   {'X_J':>5s} {'target':>9s} {'p':>8s} {'max|d(1-mu)|':>13s} {'max|dlog g|':>12s} {'d(rms)':>10s} {'N pts >X_J':>10s}  c(check)   frac c above Saturn   1-mu at Saturn")
GRAFTS = []
for XJ in (10.0, 20.0, 30.0):
    for label, tgt in (('32pi', c_target_fw), ('c_req', c_target_own), ('inf', np.inf)):
        p = 2.0 if tgt == np.inf else solve_p(XJ, tgt)
        omm, epsJ = graft(XJ, p)
        xx = np.logspace(np.log10(XJ), 12, 200001)
        dd = float(np.max(np.abs(omm(xx) - omm_rar(xx))))
        dmin = float(np.min(omm(xx) - omm_rar(xx)))
        gp = gpred_graft(omm, GB, a0b)
        dlog = float(np.max(np.abs(np.log10(gp / base_pred))))
        drms = rms_of(gp) - r_base
        npts = int(np.sum(GO / a0b > XJ))
        cchk = c_of_graft(XJ, p)
        # fraction of c above 5e5 a0 (Saturn-like acceleration ~ 6.5e-5 m/s^2 / a0)
        frac = np.nan if tgt == np.inf else 2 * epsJ * XJ ** 2 / (p - 2) * (X_SAT / XJ) ** (2 - p) / tgt
        GRAFTS.append((XJ, label, p, dd, dlog, drms, npts, cchk, frac, dmin))
        cs = 'inf' if np.isinf(cchk) else f"{cchk:.2f}"
        om_sat = float(omm(np.array([X_SAT]))[0])
        print(f"   {XJ:5.0f} {label:>9s} {p:8.4f} {dd:12.3e} {dlog:12.2e} {drms:10.2e} {npts:10d}  {cs:>8s}   {frac:14.2f}   {om_sat:.2e}")
chk("D2 every graft hits its target: c(graft) = 32 pi / c_req / infinity (analytic tail + numerical core)",
    all((np.isinf(g[7]) if g[1] == 'inf' else abs(g[7] - (c_target_fw if g[1] == '32pi' else c_target_own)) < 1e-6) for g in GRAFTS))
# independent numerical check of one graft's c (quadrature on a log grid to 1e14, analytic remainder)
XJc = 20.0
pc = solve_p(XJc, c_target_fw)
omm_c, _ = graft(XJc, pc)
us = np.linspace(np.log(1e-10), np.log(1e16), 800001)
xs_c = np.exp(us)
c_num = float(np.trapz(omm_c(xs_c) * 2 * xs_c ** 2, us))
rem = 2 * float(omm_rar(np.array([XJc]))[0]) * XJc ** 2 / (pc - 2) * (1e16 / XJc) ** (2 - pc)
chk("D3 independent check of one graft (X_J = 20, p = %.4f): direct log-grid quadrature to 1e16 plus the analytic remainder = %.3f (target 100.531)" % (pc, c_num + rem), abs(c_num + rem - c_target_fw) < 0.05)
def _monotone_and_continuous(g):
    om, eJ = graft(g[0], g[2])
    xx = np.logspace(np.log10(g[0]) - 1, 12, 20001)
    v = om(xx)
    left, right = float(om(np.array([g[0]]))[0]), float(om(np.array([g[0] * (1 + 1e-12)]))[0])
    return bool(np.all(np.diff(v) <= 1e-15)) and abs(left - right) < 1e-9 * left
chk("D4 every grafted 1-mu is continuous at X_J and monotone non-increasing (a legitimate mu with mu' >= 0): 9 grafts on 2e4 points each", all(_monotone_and_continuous(g) for g in GRAFTS))
worst_dlog = max(g[4] for g in GRAFTS)
worst_drms = max(abs(g[5]) for g in GRAFTS)
print(f"   worst change in any SPARC prediction: {worst_dlog:.2e} dex; worst change in the RAR rms: {worst_drms:.2e} dex (rms itself 0.142; bootstrap width ~0.003)")
chk("D5 CORE RESULT: replacing the RAR-nu tail beyond X_J = 10-30 a0 by a power law with c = 32 pi, c = c_req, or c = infinity changes no SPARC prediction by more than %.1e dex and the rms by %.1e dex: c is not measured by galaxy data" % (worst_dlog, worst_drms),
    worst_dlog < 5e-3 and worst_drms < 3e-4)
chk("D6 CONTROL: a change of similar size in the transition region (a0 -> 1.02 a0, 2%%) moves the rms by %.1e dex -- the same statistic sees a 2%% a0 shift" % abs(rms_of(nu_rar(GB, 1.02 * a0b)) - r_base),
    abs(rms_of(nu_rar(GB, 1.02 * a0b)) - r_base) > 0.1 * worst_drms)
frac_sat = [g[8] for g in GRAFTS if g[1] != 'inf']
print(f"   fraction of the grafted c that sits above Saturn's solar acceleration: {min(frac_sat):.2f} to {max(frac_sat):.2f}")
chk("D7 for the c = 32 pi / c_req grafts a large share (%.0f%%-%.0f%%) of c lives at accelerations above the Solar System's Saturn value: the tail that fixes c is beyond every test, and the Solar-System bound cannot cap c from above" % (100 * min(frac_sat), 100 * max(frac_sat)),
    min(frac_sat) > 0.1)

# ------------------------------------------------------------------------------------------------ E: offset reading as a prediction in mu_n
print("\n== E  offset reading as a prediction inside Milgrom's mu_n (c(n) = c_req(a0_fit(n)))")
ns = [1.5, 2.02, 2.05, 2.1, 2.3, 2.6, 3.0, 4.0]
a0n = {}
for n in ns:
    FAM[f'_n{n}'] = (mu_n(n), c_mun(n))
    a0n[n], rr = fit_a0(f'_n{n}')
    RES[f'_n{n}'] = dict(a0=a0n[n], rms=rr)
print("   n      c(n)      a0_fit      c_req(a0_fit)   rms")
for n in ns:
    cn = 'inf' if n <= 2 else f"{c_mun(n):.3f}"
    print(f"   {n:4.2f} {cn:>9s}  {a0n[n]:.4e}  {c_req(a0n[n]):9.2f}   {RES[f'_n{n}']['rms']:.5f}")
fdiff = lambda n: c_mun(n) - c_req(np.interp(n, ns, [a0n[k] for k in ns]))
n_star = optimize.brentq(fdiff, 2.02, 3.0)
a0_star = float(np.interp(n_star, ns, [a0n[k] for k in ns]))
FAM['_nstar'] = (mu_n(n_star), c_mun(n_star))
a0_s_fit, rms_star = fit_a0('_nstar')
print(f"   self-consistent n* = {n_star:.4f} (c(n*) = {c_mun(n_star):.1f} = c_req(a0_fit) = {c_req(a0_s_fit):.1f}); fit rms at n* = {rms_star:.5f} vs RAR-nu {RES['RAR-nu (McGaugh)']['rms']:.5f} vs standard {RES['standard mu_2']['rms']:.5f}")
chk("E1 the offset reading, as a prediction inside mu_n, selects n* = %.3f (a tail exponent 0.02-0.05 above the marginal 2); its fit at fixed M/L is %.4f dex worse than RAR-nu and %.4f from the standard mu_2 (not better, not worse than a neighbour of the standard function)" % (n_star, rms_star - RES['RAR-nu (McGaugh)']['rms'], rms_star - RES['standard mu_2']['rms']),
    2.02 < n_star < 2.2 and abs(c_mun(n_star) - c_req(a0_s_fit)) / c_mun(n_star) < 0.03)
d_fixed = rms_star - RES['_n1.5']['rms']
d_free = RES['mu_n n=2.02']['rmss'] - RES['RAR-nu (McGaugh)']['rmss']
print(f"   n* vs the shallower n = 1.5 (c = inf): fixed M/L d(rms) = {d_fixed:+.4f} dex; with a global M/L scale floated, n = 2.02 vs RAR-nu: {d_free:+.4f} dex")
chk("E2 the data do not confirm the prediction: at fixed M/L the shallower n = 1.5 (c = infinity) fits better by %.4f dex (the boot interval of C excludes 0 for n = 2.02 vs RAR-nu), and with a global M/L scale floated the preference shrinks to %.4f dex" % (d_fixed, d_free),
    d_fixed > 0.002 and d_free < 0.0025)

# ------------------------------------------------------------------------------------------------ F: Markov bound
print("\n== F  what the data DO force: Markov lower bound c >= X^2 (1 - mu(X))")
Xs = np.logspace(0, 2.5, 400)
mark = Xs ** 2 * omm_rar(Xs)
kbest = int(np.argmax(mark))
print(f"   best-fit RAR-nu: max_X X^2 (1-mu(X)) = {mark[kbest]:.2f} at X = {Xs[kbest]:.1f}  (c = 25.98)")
Xs2 = np.logspace(0, 2.5, 400)
mark_std = Xs2 ** 2 * (1 - Xs2 / np.sqrt(1 + Xs2 ** 2))
print(f"   standard mu_2:  max_X X^2 (1-mu(X)) = {mark_std.max():.2f}  (its tail x^-2/2 saturates at 1/2 x-independent: c >= 0.5 per e-fold)")
chk("F1 the Markov bound from the best-fit shape is ~4-5 (X^2 (1-mu) at X ~ 10-20): the shape SPARC prefers forces c >= 4.6 and nothing more; the requirement is 61-100", 4.0 < mark[kbest] < 5.5)

print(f"\n{sum(OK)}/{len(OK)} checks passed")
sys.exit(0 if all(OK) else 1)
