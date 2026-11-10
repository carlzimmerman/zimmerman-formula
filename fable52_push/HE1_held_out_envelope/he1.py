#!/usr/bin/env python3
"""HE1 held-out envelope (criteria 0e67f3c64a). TEST lane, quarantined; adopts nothing. kappa = 1/2 FITTED; not theory closed.

A cleared galaxy (law on inside R_w, no cold component there; Newtonian outside) whose share X M_b of the cold component sits
outside the wall as an isothermal envelope in Jeans equilibrium in the field of M_b plus itself.
  BC1  rho(R_w) sigma^2 = p_wall(R_w)          (SWT1 T3, exact W)
  BC2  rho(R_w) = sigma^2 / (2 pi G R_w^2)      (closure: singular isothermal at the wall; closure C reported)
  BC3  M_env(< R_out) = X M_b                   (the record's share)
Gates G1-G5 per footing; G6 and the pooled B21 gate reported.

    python3 he1.py                    -> he1.json / he1.out
    python3 he1.py --mutate M1|M2|M3  -> he1_MUTATE_<arm>.json / .out
Constants, the law, p_wall, r_ta, the GSMF and `compensated` come from ../SWT1_switch_theorems/swt1.py (library part, read
only); KO1's per-lens machinery is transcribed from ../KO1_kids_outer_points/ko1_extra.py.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.stats import chi2 as CHI2
from scipy.spatial import cKDTree
from astropy.io import fits
if not hasattr(np, "trapz"): np.trapz = np.trapezoid

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = None
if "--mutate" in sys.argv:
    MUT = sys.argv[sys.argv.index("--mutate") + 1]; assert MUT in ("M1", "M2", "M3"), MUT
TAG = f"he1_MUTATE_{MUT}" if MUT else "he1"
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
T0 = time.time()
CRIT = "0e67f3c64a"; AMEND = "22e1d5a6ba"; AMEND2 = "9163ca4fe6"

# ====================================================================== SWT1 library (read only)
SW = os.path.join(HERE, "..", "SWT1_switch_theorems", "swt1.py")
_src = open(SW).read(); _cut = _src.index("RES = dict(lane=")
NS = {"__file__": os.path.abspath(SW), "__name__": "swt1_lib"}
_a = sys.argv; sys.argv = ["swt1.py"]; exec(compile(_src[:_cut], "swt1.py", "exec"), NS); sys.argv = _a
G, MS, PC, MPC, KPC, A0, LINE = (NS[k] for k in ("G", "MS", "PC", "MPC", "KPC", "A0", "LINE"))
u_in, Wfun, p_wall_swt1, r_ta, Rms, compensated, radii_table = (NS[k] for k in
    ("u_in", "Wfun", "p_wall", "r_ta", "Rms", "compensated", "radii_table"))
R_DUST, RHO_D0, RHO_M0, H0s, Hs = (NS[k] for k in ("R_DUST", "RHO_D0", "RHO_M0", "H0s", "Hs"))
LG, LF, PD0 = NS["LG"], NS["LF"], NS["PD"].copy()
FOOT = ("canonical", "alt")
GK = 1.38e-15                                   # KiDS's lowest tabulated g_bar (SWT1, SNP1)
KIDS = (9.4, 10.45, 10.7, 10.9)
ZS = (0.0, 0.5, 1.0)
GAL1_LINE, GAL1_Z6 = 0.0197, 0.0134

sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG903_framework_two_halo_kids"))
import cfg903_lib as C903                        # N_of_declared (CFG902's declared fixed point), read only
X_CAP = 53.64
def X_of(which, lm):
    if which == "share": return R_DUST
    if which == "census": return 5.364 * C903.N_of_declared(lm)
    if which == "cap": return X_CAP
    raise ValueError(which)
XNAMES = ("share", "census", "cap")
ROUTS = ("rta", "1.5Mpc", "3Mpc")

RES = dict(lane="HE1", criteria=CRIT, amendment_A1=AMEND, amendment_A2=AMEND2, tag=TAG, mutate=MUT, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           KA={}, partB={}, G1={}, G2={}, G3={}, G4={}, G5={}, G6={}, B21={}, closureC={}, labels={}, MUTATE={})
P(f"HE1 {('MUTATE ' + MUT) if MUT else ''} run (criteria {CRIT}, amendments A1 {AMEND}, A2 {AMEND2}). R = OD/OB = {R_DUST:.6f}; rho_d0 {RHO_D0:.4e} kg/m^3")

# ====================================================================== the wall (dimensionless: x = r / r_M, y = 1 / x^2)
PSIGN = -1.0 if MUT == "M1" else 1.0
PSCALE = 0.01 if MUT == "M2" else 1.0
def Wd(x):
    """4 pi p_wall in units M_b v_f^2 / r_M^3 (p_wall = (a0^2 / 4 pi G) W = W / (4 pi) in these units)."""
    return PSIGN * PSCALE * float(Wfun(u_in(1.0 / (x * x))))
def wall_slope(x):
    """d ln p_wall / d ln R = -2 y (u - y) / W at the wall (sign and scale do not change it)."""
    y = 1.0 / (x * x); u = float(u_in(y)); W = float(Wfun(u))
    return -2.0 * y * (u - y) / W
# own implementation (KA2): the closed form written out separately, physical units
def p_wall_own(y, a0):
    u = (y + math.sqrt(y * (y + 4.0))) / 2.0
    W = u - math.log1p(u) - u * u / (2.0 * (1.0 + u) ** 2)
    return a0 * a0 / (4.0 * math.pi * G) * W

# ====================================================================== the envelope (Jeans, isothermal), dimensionless
def env_solve(xw, s, rho_w, x_end, m0=1.0, dense=False):
    """t = ln x; state (ln rho, m) with m the enclosed mass in M_b (baryons + envelope)."""
    def rhs(t, z):
        x = math.exp(t); return [-z[1] / (x * s), 4.0 * math.pi * x ** 3 * math.exp(z[0])]
    return solve_ivp(rhs, (math.log(xw), math.log(x_end)), [math.log(rho_w), m0], method="DOP853",
                     rtol=1e-10, atol=[1e-12, 1e-12], dense_output=dense)
def sA(xw):
    """closure A (BC1 + BC2): s^2 = x_w^2 W / 2, s = sigma^2 / v_f^2."""
    w = Wd(xw)
    return math.sqrt(xw * xw * w / 2.0) if w > 0 else None
def menv_A(xw, xo):
    s = sA(xw)
    if s is None: return None
    return env_solve(xw, s, s / (2 * math.pi * xw * xw), xo).y[1, -1] - 1.0

XWG = np.logspace(math.log10(0.05), math.log10(3e4), 500); XG = np.logspace(math.log10(0.05), math.log10(3e4), 900)
def build_tableA():
    T = np.full((XWG.size, XG.size), np.nan)
    for i, xw in enumerate(XWG):
        s = sA(xw)
        if s is None or xw >= XG[-1] * (1 - 1e-9): continue
        so = env_solve(xw, s, s / (2 * math.pi * xw * xw), XG[-1], dense=True); sel = XG >= xw
        T[i, sel] = so.sol(np.log(XG[sel]))[1] - 1.0
    return T
TA = build_tableA()
P(f"closure-A table: {np.isfinite(TA).any(axis=1).sum()} of {XWG.size} wall radii have a balance  [{time.time() - T0:.0f} s]")

class Env:
    """one solved envelope; x in r_M, masses in M_b; xw = None means NO BALANCE (fallback: wall at x_out, share as a thin shell)."""
    def __init__(s, closure, xo, X, roots, xw, sv, rho_w):
        s.closure, s.xo, s.X, s.roots, s.xw, s.s, s.rho_w = closure, xo, X, roots, xw, sv, rho_w
        s.balance = xw is not None
        if s.balance:
            so = env_solve(xw, sv, rho_w, xo, dense=True)
            s.xs = np.logspace(math.log10(xw), math.log10(xo), 1200); zz = so.sol(np.log(s.xs))
            s.lr = zz[0]; s.mc = zz[1] - 1.0; s.mc[0] = 0.0
            s.Mtot = float(s.mc[-1])
        else:
            s.xw_eff = xo; s.Mtot = X
    def rho(s, x):
        x = np.asarray(x, float); out = np.zeros_like(x)
        if s.balance:
            m = (x >= s.xw) & (x <= s.xo); out[m] = np.exp(np.interp(np.log(x[m]), np.log(s.xs), s.lr))
        return out
    def Menc(s, x):
        x = np.asarray(x, float)
        if not s.balance: return np.where(x >= s.xo, s.X, 0.0)
        return np.where(x <= s.xw, 0.0, np.where(x >= s.xo, s.Mtot, np.interp(np.log(np.clip(x, s.xw, s.xo)), np.log(s.xs), s.mc)))

BRACKET_MISSES = []
def solve_A(xo, X):
    if not np.isfinite(TA).any(): return Env("A", xo, X, [], None, None, None)
    lx = np.log(XG); idx = np.where(XWG < xo)[0]; Fv = []
    for i in idx:
        row = TA[i]; ok = np.isfinite(row)
        if ok.sum() > 1 and XG[ok][0] <= xo:
            Fv.append(np.interp(math.log(xo), lx[ok], row[ok]) - X)
        else:                                                                      # A2: the row starts beyond x_out; evaluate exactly
            mv = menv_A(XWG[i], xo); Fv.append(mv - X if mv is not None else np.nan)
    xs = list(XWG[idx]) + [xo * (1 - 1e-9)]; Fv = Fv + [-X]
    roots = []
    for j in range(len(xs) - 1):
        f1, f2 = Fv[j], Fv[j + 1]
        if not (np.isfinite(f1) and np.isfinite(f2)) or f1 * f2 > 0: continue
        fx = lambda lx_: menv_A(math.exp(lx_), xo) - X
        done = False
        for lo_, hi_ in ((j, j + 1), (j - 1, j + 1), (j, j + 2), (j - 2, j + 2)):    # A2: widen the bracket when the table's sign change is off by an interval
            lo_, hi_ = max(lo_, 0), min(hi_, len(xs) - 1)
            a_, b_ = math.log(xs[lo_]), math.log(min(xs[hi_], xo * (1 - 1e-9)))
            fa, fb = fx(a_), fx(b_)
            if fa * fb <= 0:
                r = math.exp(brentq(fx, a_, b_, xtol=1e-12, rtol=1e-12))
                if not any(abs(r / q - 1) < 1e-8 for q in roots): roots.append(r)
                done = True; break
        if not done:
            BRACKET_MISSES.append((xo, X, xs[j]))                                  # A2: a table sign change the exact function did not confirm
    if not roots: return Env("A", xo, X, [], None, None, None)
    xw = max(roots); s = sA(xw)
    return Env("A", xo, X, sorted(roots), xw, s, s / (2 * math.pi * xw * xw))

def solve_C(xo, X, n=100):
    """closure C: s = (1 + X) / (2 x_out); BC1 gives rho_w = W / (4 pi s); share fixes x_w."""
    s = (1.0 + X) / (2.0 * xo)
    def F(xw):
        w = Wd(xw)
        if w <= 0: return None
        return env_solve(xw, s, w / (4 * math.pi * s), xo).y[1, -1] - 1.0 - X
    xs = np.logspace(math.log10(0.05), math.log10(xo * (1 - 1e-9)), n); Fv = [F(x) for x in xs]
    roots = []
    for j in range(n - 1):
        f1, f2 = Fv[j], Fv[j + 1]
        if f1 is None or f2 is None or f1 * f2 > 0: continue
        roots.append(math.exp(brentq(lambda lx_: F(math.exp(lx_)), math.log(xs[j]), math.log(xs[j + 1]), xtol=1e-12, rtol=1e-12)))
    if not roots: return Env("C", xo, X, [], None, None, None)
    xw = max(roots)
    return Env("C", xo, X, sorted(roots), xw, s, Wd(xw) / (4 * math.pi * s))

# ====================================================================== R_out
_RTREF = {}
MREF = 1e11 * MS
def rta_scaled(M, z):
    aE = 1.0 / (1.0 + z)
    if z not in _RTREF: _RTREF[z] = r_ta(MREF, 0.0, aE)
    return _RTREF[z] * (M / MREF) ** (1.0 / 3.0)
def R_out(lm, X, rch, z=0.0):
    Mb = 10 ** lm * MS; base = rta_scaled((1 + X) * Mb, z)
    if rch == "rta": return base
    fix = {"1.5Mpc": 1.5, "3Mpc": 3.0}[rch] * MPC
    return fix * base / rta_scaled((1 + X) * Mb, 0.0)
def rM_of(lm, a0): return math.sqrt(G * 10 ** lm * MS / a0)
def vf_of(lm, a0): return (G * 10 ** lm * MS * a0) ** 0.25

def envelope(lm, a0, Xn, rch, z=0.0, closure="A"):
    X = X_of(Xn, lm); Ro = R_out(lm, X, rch, z); xo = Ro / rM_of(lm, a0)
    return (solve_A if closure == "A" else solve_C)(xo, X)

# ====================================================================== projection (dimensionless; P = 4 G DeltaSigma in a0)
NT = 400; TGX, TGW = np.polynomial.legendre.leggauss(NT)
def proj_tab(R, rho_fn, Mc_fn, a, b):
    """Sigma(R), M_cyl(R) of a spherical component with density rho_fn on [a, b]; Mc_fn(r) its mass inside radius r."""
    R = np.atleast_1d(np.asarray(R, float)); Sig = np.zeros_like(R); Mcyl = np.zeros_like(R)
    out = R >= b; Mcyl[out] = float(Mc_fn(np.array([b]))[0])
    inn = ~out
    if inn.any():
        Ri = R[inn]; lo = np.maximum(a, Ri)
        t0 = np.arccosh(np.maximum(lo / Ri, 1.0)); t1 = np.arccosh(b / Ri)
        h = 0.5 * (t1 - t0)[:, None]; tau = h * (TGX[None, :] + 1.0) + t0[:, None]; w = h * TGW[None, :]
        r = Ri[:, None] * np.cosh(tau); rho = rho_fn(r.ravel()).reshape(r.shape)
        e2 = np.exp(-2.0 * tau); omt = 2.0 * e2 / (1.0 + e2)                    # 1 - tanh(tau), stable
        Sig[inn] = 2.0 * np.sum(w * rho * r, axis=1)
        sph = np.where(Ri > a, Mc_fn(np.minimum(Ri, b)), 0.0)
        Mcyl[inn] = sph + np.sum(w * 4.0 * math.pi * r * r * rho * omt * Ri[:, None] * np.sinh(tau), axis=1)
    return Sig, Mcyl
def proj_point_shortcut(R, rho_fn, Mc_fn, a, b):
    """MUTATE M3: the component's enclosed mass treated as a point at the centre."""
    R = np.atleast_1d(np.asarray(R, float)); return np.zeros_like(R), np.where(R > a, Mc_fn(np.minimum(R, b)), 0.0)
proj_env = proj_point_shortcut if MUT == "M3" else proj_tab
def proj_shell(R, ms, b):
    R = np.atleast_1d(np.asarray(R, float)); inside = R < b; q = np.where(inside, (R / b) ** 2, 0.0)
    Sig = np.where(inside, ms / (2 * math.pi * b * np.sqrt(np.maximum(b * b - R * R, 1e-300))), 0.0)
    Mcyl = np.where(inside, ms * q / (1.0 + np.sqrt(1.0 - q)), ms)
    return Sig, Mcyl
def rho_ph(x): x = np.asarray(x, float); return 1.0 / (4 * math.pi * x * np.sqrt(0.25 + x * x))
def Mph(x): x = np.asarray(x, float); return x * x / (np.sqrt(0.25 + x * x) + 0.5)
def glaw_d(x): return u_in(1.0 / (np.asarray(x, float) ** 2))
def P_law(R):
    R = np.atleast_1d(np.asarray(R, float)); B = 1e4 * R.max()
    s1, m1 = proj_tab(R, rho_ph, Mph, 0.0, B)
    s1 = s1 + np.arcsin(R / B) / (2 * math.pi * R)                                 # singular tail beyond B
    m1 = m1 + R * np.arcsin(R / B) - (R * R / B) / (1.0 + np.sqrt(1.0 - (R / B) ** 2))
    return 4.0 * ((1.0 + m1) / (math.pi * R * R) - s1)
def P_model(R, env):
    R = np.atleast_1d(np.asarray(R, float))
    if env.balance:
        xw = env.xw
        s1, m1 = proj_tab(R, rho_ph, lambda r: Mph(np.minimum(r, xw)), 0.0, xw)
        s2, m2 = proj_shell(R, -float(Mph(xw)), xw)
        s3, m3 = proj_env(R, env.rho, env.Menc, xw, env.xo)
    else:                                                                          # NO BALANCE fallback (reported only)
        xw = env.xo
        s1, m1 = proj_tab(R, rho_ph, lambda r: Mph(np.minimum(r, xw)), 0.0, xw)
        s2, m2 = proj_shell(R, -float(Mph(xw)), xw)
        s3, m3 = proj_shell(R, env.X, xw)
    return 4.0 * ((1.0 + m1 + m2 + m3) / (math.pi * R * R) - (s1 + s2 + s3))

# ====================================================================== bin averages over KiDS's g_bar bins (in t = x^2)
NGB = 48; BGX, BGW = np.polynomial.legendre.leggauss(NGB)
def bin_nodes(t1, t2, bps):
    pts = sorted(b for b in bps if t1 < b < t2); edges = [t1] + pts + [t2]; T, Wt = [], []
    for p, q in zip(edges[:-1], edges[1:]):
        if q in pts or (q == t2 and any(abs(q - b) < 1e-12 * q for b in bps)):
            smax = math.sqrt(q - p); s = 0.5 * smax * (BGX + 1.0); T.append(q - s * s); Wt.append(0.5 * smax * BGW * 2.0 * s)
        else:
            T.append(0.5 * (q - p) * (BGX + 1.0) + p); Wt.append(0.5 * (q - p) * BGW)
    return np.concatenate(T), np.concatenate(Wt)
DLR = os.path.join(REPO, "real_research", "data", "lensing_rar")
EDGES = np.load(os.path.join(DLR, "cfg110_perlens.npz"))["gbar_edges"]; NB = 15
R3 = 3.0 * MPC
def bin_factors(env, a0, rM):
    """per bin k: avg(glaw P_model / P_law) / avg(glaw)  (graded, differential), avg(P_model) / avg(glaw)  (raw),
    avg(P_law) / avg(glaw) (raw law)."""
    bps = [] if env is None else ([env.xw ** 2, env.xo ** 2] if env.balance else [env.xo ** 2])
    allT, allW, allK = [], [], []
    for k in range(NB):
        t1 = a0 / EDGES[k + 1]; t2 = min(a0 / EDGES[k], (R3 / rM) ** 2)
        if t2 <= t1: continue
        T, Wt = bin_nodes(t1, t2, bps); allT.append(T); allW.append(Wt / (t2 - t1)); allK.append(np.full(T.size, k))
    T = np.concatenate(allT); Wt = np.concatenate(allW); K = np.concatenate(allK); x = np.sqrt(T)
    gl = glaw_d(x); pl = P_law(x); pm = pl.copy() if env is None else P_model(x, env)
    ag = np.bincount(K, Wt * gl, NB); ad = np.bincount(K, Wt * gl * pm / pl, NB); ar = np.bincount(K, Wt * pm, NB); al = np.bincount(K, Wt * pl, NB)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(ag > 0, ad / ag, 1.0), np.where(ag > 0, ar / ag, 1.0), np.where(ag > 0, al / ag, 1.0)

# ====================================================================== KNOWN ANSWERS (part 1: solver, wall, projection, r_ta, import)
KAOK = {}
# KA1 deep limit
ka1 = []
for xw in (1e3, 1e4):
    s = sA(xw)
    if s is None: ka1.append(dict(x_w=xw, ratio=None)); continue
    xdeep = 1.0 / (3.0 * s * s); ka1.append(dict(x_w=xw, ratio=xw / xdeep, bound=3.0 / xw, ok=bool(abs(xw / xdeep - 1) <= 3.0 / xw)))
# Jeans solver: singular start stays singular; negligible density follows the point-mass Boltzmann profile
s0 = 0.3; xw0 = 50.0
so = env_solve(xw0, s0, s0 / (2 * math.pi * xw0 ** 2), xw0 * 1e3, m0=2 * s0 * xw0, dense=True)
xx = np.logspace(math.log10(xw0), math.log10(xw0 * 1e3), 200); dev_sis = float(np.max(np.abs(np.exp(so.sol(np.log(xx))[0]) * 2 * math.pi * xx ** 2 / s0 - 1)))
rw0 = 1e-24; so = env_solve(xw0, s0, rw0, xw0 * 1e3, m0=1.0, dense=True)   # A1: 1e-14 was not negligible
dev_pt = float(np.max(np.abs(np.exp(so.sol(np.log(xx))[0]) / (rw0 * np.exp((1 / s0) * (1 / xx - 1 / xw0))) - 1)))
ok1 = (all(r.get("ok", False) for r in ka1) and dev_sis < 1e-6 and dev_pt < 1e-6) if MUT != "M1" else (dev_sis < 1e-6 and dev_pt < 1e-6)
KAOK["KA1"] = ok1
RES["KA"]["KA1"] = dict(deep=ka1, singular_dev=dev_sis, pointmass_dev=dev_pt, pass_=bool(ok1),
                        note=("M1: no balance exists, the deep-limit part is skipped" if MUT == "M1" else ""))
P("KA1 deep limit: " + "; ".join(f"x_w {r['x_w']:.0e}: R_exact / R_deep {r['ratio']:.6f} (bound {r.get('bound', 0):.0e})" if r['ratio'] else f"x_w {r['x_w']:.0e}: no balance" for r in ka1)
  + f"; singular start stays singular to {dev_sis:.1e}; point-mass profile to {dev_pt:.1e} -> {'PASS' if ok1 else 'FAIL'}")
# KA2 p_wall own vs swt1
ys = np.logspace(-8, 4, 20); rel = max(abs(p_wall_own(y, A0['canonical']) / float(p_wall_swt1(y, A0['canonical'])) - 1) for y in ys)
qd = []
for y in (1e-3, 0.1, 1.0, 10.0):
    val = quad(lambda t: math.sqrt(0.25 * t * t + t) - 0.5 * t, 0.0, y, epsabs=0, epsrel=1e-13, limit=400)[0]
    qd.append(abs(float(Wfun(u_in(y))) / val - 1))
ok2 = rel < 1e-12
KAOK["KA2"] = ok2
RES["KA"]["KA2"] = dict(max_rel=rel, quadrature_check_max_rel=max(qd), pass_=bool(ok2))
P(f"KA2 p_wall own vs swt1.py at 20 y in [1e-8, 1e4]: max rel {rel:.1e}; (W vs quadrature at 4 y: {max(qd):.1e}) -> {'PASS' if ok2 else 'FAIL'}")
# KA3 projection closed forms (through the projector the envelope uses)
def shell_thick_closed(R, rho0, a, b):
    Sig = 2 * rho0 * (np.sqrt(np.maximum(b * b - R * R, 0)) - np.sqrt(np.maximum(a * a - R * R, 0)))
    def cyl(c): return 4 * math.pi / 3 * rho0 * (c ** 3 - np.maximum(c * c - R * R, 0) ** 1.5)
    return Sig, cyl(b) - cyl(a)
def sis_trunc_closed(R, K, a, b):
    def asec(z):
        with np.errstate(invalid="ignore"): return np.arccos(np.minimum(1.0 / z, 1.0))
    Sig = np.where(R < b, (2 * K / R) * (asec(b / R) - asec(np.maximum(a, R) / R)), 0.0)
    def F(r): return r - np.sqrt(np.maximum(r * r - R * R, 0)) + R * np.arccos(np.minimum(R / r, 1.0))
    M = np.where(R <= a, 4 * math.pi * K * (F(b) - F(a)), np.where(R < b, 4 * math.pi * K * ((R - a) + F(b) - R), 4 * math.pi * K * (b - a)))
    return Sig, M
Rt = np.array([0.05, 0.2, 0.5, 0.9, 1.5]) * 100.0
a_, b_, rho0 = 60.0, 100.0, 1e-4
sc, mc = shell_thick_closed(Rt, rho0, a_, b_)
sn, mn = proj_env(Rt, lambda r: np.where((r >= a_) & (r <= b_), rho0, 0.0), lambda r: 4 * math.pi / 3 * rho0 * (np.clip(r, a_, b_) ** 3 - a_ ** 3), a_, b_)
e_shell = float(np.max(np.abs(np.concatenate([(sn - sc)[sc > 0] / sc[sc > 0], (mn - mc) / mc]))))
ths, thm = proj_shell(Rt, 1.0, b_); EPS = 1e-5                                       # A1: relative thickness 1e-5, tolerance 1e-4
sc2, mc2 = shell_thick_closed(Rt, 1.0 / (4 * math.pi / 3 * (b_ ** 3 - ((1 - EPS) * b_) ** 3)), (1 - EPS) * b_, b_)
e_thin = float(np.max(np.abs(np.concatenate([(thm - mc2) / mc2, (ths - sc2)[sc2 > 0] / sc2[sc2 > 0]]))))
Kk = 0.3 / (2 * math.pi); sc3, mc3 = sis_trunc_closed(Rt, Kk, 10.0, 100.0)
sn3, mn3 = proj_env(Rt, lambda r: np.where((r >= 10) & (r <= 100), Kk / r ** 2, 0.0), lambda r: 4 * math.pi * Kk * (np.clip(r, 10, 100) - 10), 10.0, 100.0)
e_sis_t = float(np.max(np.abs(np.concatenate([(sn3 - sc3)[sc3 > 0] / sc3[sc3 > 0], (mn3 - mc3) / mc3]))))
Rr = np.array([1.0, 10.0, 100.0]); sv = 0.3
sn4, mn4 = proj_env(Rr, lambda r: sv / (2 * math.pi * r * r), lambda r: 2 * sv * (np.asarray(r) - 1e-6 * 1.0), 1e-6, 1e6)
P_sis = 4 * (mn4 / (math.pi * Rr * Rr) - sn4); e_sis = float(np.max(np.abs(P_sis / (2 * sv / Rr) - 1)))
ok3 = e_shell < 1e-4 and e_thin < 1e-4 and e_sis_t < 1e-4 and e_sis < 1e-3
KAOK["KA3"] = ok3
RES["KA"]["KA3"] = dict(thick_shell=e_shell, thin_shell_vs_0p001_thick=e_thin, sis_truncated=e_sis_t, sis_untruncated_ratio=(P_sis / (2 * sv / Rr)).tolist(),
                        sis_untruncated_err=e_sis, pass_=bool(ok3))
P(f"KA3 projection: thick shell {e_shell:.1e}, thin shell vs a 1e-5-thick shell {e_thin:.1e}, truncated singular sphere {e_sis_t:.1e}, "
  f"untruncated 4 G DeltaSigma / (2 sigma^2 / R) = " + ", ".join(f"{v:.5f}" for v in P_sis / (2 * sv / Rr)) + f" -> {'PASS' if ok3 else 'FAIL'}")
# KA7 r_ta scaling
ka7 = []
for lm in (9.4, 10.9):
    M = 10 ** lm * MS * (1 + R_DUST); d = r_ta(M, 0.0, 1.0); sc_ = rta_scaled(M, 0.0); ka7.append(abs(sc_ / d - 1))
ok7 = max(ka7) < 1e-5; KAOK["KA7"] = ok7
RES["KA"]["KA7"] = dict(rel=ka7, pass_=bool(ok7))
P(f"KA7 Newtonian r_ta scaling vs direct swt1.r_ta: {max(ka7):.1e} -> {'PASS' if ok7 else 'FAIL'}")
# KA8 compensated import on SWT1's NC table at z 1
ka8 = {}
for f in FOOT:
    tab = radii_table("NC", A0[f], 1.0); ka8[f] = compensated(tab, A0[f], 1.0)["q_tot"]
ok8 = abs(round(ka8["canonical"], 4) - 0.0180) < 1e-9 and abs(round(ka8["alt"], 4) - 0.0182) < 1e-9; KAOK["KA8"] = ok8
RES["KA"]["KA8"] = dict(q_tot=ka8, swt1=dict(canonical=0.0180, alt=0.0182), pass_=bool(ok8))
P(f"KA8 compensated on SWT1's NC table, z 1: {ka8['canonical']:.4f} / {ka8['alt']:.4f} (SWT1 0.0180 / 0.0182) -> {'PASS' if ok8 else 'FAIL'}  [{time.time() - T0:.0f} s]")

# ====================================================================== PART B: the four KiDS masses
P("")
P("PART B. Envelopes (closure A), four KiDS masses. R_w, sigma, A = 2 sigma^2 / v_f^2, R_w / R_K, envelope mass inside 200 kpc / 1 Mpc / 3 Mpc (M_b);")
P("        departures from Part A: x_w A^2 3/4 (1 if the deep closed form held) and M_env(R_out) / (A (x_out - x_w)) (singular-shell form).")
ENV = {}
def env_row(lm, a0, e):
    rM = rM_of(lm, a0); vf = vf_of(lm, a0); RK = math.sqrt(G * 10 ** lm * MS / GK)
    if not e.balance:
        return dict(balance=False, x_out=e.xo, R_out_Mpc=e.xo * rM / MPC, X=e.X)
    A = 2 * e.s; Mi = [float(e.Menc(np.array([r / rM]))[0]) for r in (200 * KPC, 1 * MPC, 3 * MPC)]
    return dict(balance=True, X=e.X, x_out=e.xo, R_out_Mpc=e.xo * rM / MPC, x_w=e.xw, R_w_kpc=e.xw * rM / KPC, R_w_over_RK=e.xw * rM / RK,
                roots_x=e.roots, s=e.s, sigma_kms=math.sqrt(e.s) * vf / 1e3, sigma_over_vf=math.sqrt(e.s), A=A, Menv_200kpc_1Mpc_3Mpc=Mi,
                deep_ratio=e.xw * A * A * 0.75, shell_ratio=e.Mtot / (A * (e.xo - e.xw)), r_M_kpc=rM / KPC, v_f_kms=vf / 1e3, R_K_Mpc=RK / MPC)
PB = {}
for f in FOOT:
    a0 = A0[f]; PB[f] = {}
    for Xn in XNAMES:
        for rch in ROUTS:
            for lm in KIDS:
                e = envelope(lm, a0, Xn, rch); ENV[(f, Xn, rch, lm)] = e; row = env_row(lm, a0, e)
                PB[f][f"{Xn}|{rch}|{lm}"] = row
                if row["balance"]:
                    P(f"[{f}] X {Xn:6s} ({row['X']:.3f}) R_out {rch:6s} {row['R_out_Mpc']:.3f} Mpc | log M_b {lm}: R_w {row['R_w_kpc']:7.1f} kpc = {row['x_w']:6.1f} r_M = "
                      f"{row['R_w_over_RK']:.3f} R_K; sigma {row['sigma_kms']:5.1f} km/s = {row['sigma_over_vf']:.3f} v_f; A {row['A']:.3f}; M_env < 0.2/1/3 Mpc "
                      + " / ".join(f"{m:.2f}" for m in row["Menv_200kpc_1Mpc_3Mpc"]) + f"; deep {row['deep_ratio']:.3f}, shell {row['shell_ratio']:.3f}"
                      + (f"; roots {', '.join(f'{r:.2f}' for r in row['roots_x'])}" if len(row["roots_x"]) > 1 else ""))
                else:
                    P(f"[{f}] X {Xn:6s} ({row['X']:.3f}) R_out {rch:6s} {row['R_out_Mpc']:.3f} Mpc | log M_b {lm}: NO BALANCE")
RES["partB"] = PB
P(f"   [{time.time() - T0:.0f} s]")

# ====================================================================== GSMF grid (z 0, 0.5, 1): G1, G2, G3
P("")
P("GSMF grid (SWT1's, log M* 9-12 by 0.25), closure A.")
GRID = {}
for f in FOOT:
    a0 = A0[f]
    for Xn in XNAMES:
        for rch in ROUTS:
            for z in ZS:
                GRID[(f, Xn, rch, z)] = [envelope(lm, a0, Xn, rch, z) for lm in LG]
P(f"   grid solved [{time.time() - T0:.0f} s]")
# late-type fraction proxy
LNS = np.load(os.path.join(DLR, "lr_lenses.npz"))
lmS, typS = LNS["logM"], LNS["typ"]
be = np.arange(8.0, 12.26, 0.25); fl_c, fl_v = [], []
for lo, hi in zip(be[:-1], be[1:]):
    m = (lmS >= lo) & (lmS < hi)
    if m.sum() >= 50: fl_c.append(0.5 * (lo + hi)); fl_v.append(float((typS[m] == 0).mean()))
FLATE = np.interp(LF, fl_c, fl_v)
RES["G2_late_fraction_proxy"] = dict(centres=fl_c, late_fraction=fl_v)
P("late-type fraction proxy (lr_lenses typ == 0, 0.25-dex bins of log M*): " + ", ".join(f"{c:.3f}:{v:.2f}" for c, v in zip(fl_c, fl_v)))

def tab_of(envs, lm_arr, a0):
    return np.array([(e.xw if e.balance else e.xo) * rM_of(lm, a0) for e, lm in zip(envs, lm_arr)])
def comp(tab, a0, z, late=False):
    NS["PD"] = PD0 * FLATE if late else PD0
    try:
        return compensated(tab, a0, z)
    finally:
        NS["PD"] = PD0

G1, G2, G3 = {}, {}, {}
for f in FOOT:
    a0 = A0[f]; G1[f], G2[f], G3[f] = {}, {}, {}
    for Xn in XNAMES:
        for rch in ROUTS:
            key = f"{Xn}|{rch}"
            # G1 (z 0): KiDS masses and the grid
            ek = [ENV[(f, Xn, rch, lm)] for lm in KIDS]; eg = GRID[(f, Xn, rch, 0.0)]
            xk = [e.xw if e.balance else None for e in ek]; xg = [e.xw if e.balance else None for e in eg]
            nob = sum(x is None for x in xk + xg)
            g1 = (nob == 0) and all(x >= 10.0 for x in xk + xg)
            G1[f][key] = dict(x_w_kids=xk, x_w_grid=xg, min_x_w=min([x for x in xk + xg if x is not None], default=None), no_balance=nob,
                              component_inside_wall=0.0, pass_=bool(g1))
            # G2
            rows = {}
            for z in ZS:
                envs = GRID[(f, Xn, rch, z)]; tab = tab_of(envs, LG, a0)
                c = comp(tab, a0, z); cl = comp(tab, a0, z, late=True)
                rows[str(z)] = dict(f_V=c["f_V"], q_tot=c["q_tot"], dilute=c["dilute"], pass_line=bool(c["q_tot"] <= LINE),
                                    vs_GAL1_0p0197=bool(c["f_V"] <= GAL1_LINE), vs_GAL1_z6_0p0134=bool(c["f_V"] <= GAL1_Z6),
                                    late_only=dict(f_V=cl["f_V"], q_tot=cl["q_tot"], pass_line=bool(cl["q_tot"] <= LINE)),
                                    no_balance=int(sum(not e.balance for e in envs)))
            g2 = all(rows[str(z)]["pass_line"] for z in ZS)
            G2[f][key] = dict(rows=rows, pass_=bool(g2))
            # G3 (z 0): exact slopes at every KiDS and grid mass
            sl = []
            for e in ek + eg:
                if not e.balance: sl.append(None); continue
                sl.append((-1.0 / (e.xw * e.s), wall_slope(e.xw)))
            g3 = (nob == 0) and all(x[0] > x[1] for x in sl if x is not None)
            G3[f][key] = dict(slopes_env_wall=sl, worst_margin=(min(x[0] - x[1] for x in sl if x is not None) if any(x is not None for x in sl) else None),
                              no_balance=nob, pass_=bool(g3))
            P(f"[{f}] X {Xn:6s} R_out {rch:6s}: G1 min x_w {G1[f][key]['min_x_w'] if G1[f][key]['min_x_w'] is None else round(G1[f][key]['min_x_w'], 2)} "
              f"(no balance {nob}) -> {'PASS' if g1 else 'FAIL'} | G2 q_tot z 0/0.5/1 " + " / ".join(f"{rows[str(z)]['q_tot']:.4f}" for z in ZS)
              + f" (f_V " + " / ".join(f"{rows[str(z)]['f_V']:.4f}" for z in ZS) + "; late only q " + " / ".join(f"{rows[str(z)]['late_only']['q_tot']:.4f}" for z in ZS)
              + f") -> {'PASS' if g2 else 'FAIL'} | G3 worst s_env - s_wall {G3[f][key]['worst_margin'] if G3[f][key]['worst_margin'] is None else round(G3[f][key]['worst_margin'], 3)} -> {'PASS' if g3 else 'FAIL'}")
RES["G1"], RES["G2"], RES["G3"] = G1, G2, G3
P(f"   [{time.time() - T0:.0f} s]")

# G3 reported: swept-layer and quasi-static readings at the KiDS masses (primary R_out)
def quasi_static(e, frac):
    if not e.balance: return None
    xn = e.xw * (1 + frac)
    if xn >= e.xo: return None
    def F(lr): return env_solve(xn, e.s, math.exp(lr), e.xo).y[1, -1] - 1.0 - e.X
    try:
        lr = brentq(F, math.log(e.rho_w) - 30, math.log(e.rho_w) + 30, xtol=1e-12)
    except ValueError:
        return None
    pe = math.exp(lr) * e.s; pw = Wd(xn) / (4 * math.pi)
    return dict(p_env_over_p_wall=pe / pw, restoring=bool((pe > pw) if frac > 0 else (pe < pw)))
G3r = {}
for f in FOOT:
    G3r[f] = {}
    for Xn in XNAMES:
        for lm in KIDS:
            e = ENV[(f, Xn, "rta", lm)]
            if not e.balance: G3r[f][f"{Xn}|{lm}"] = None; continue
            sw = (Wd(e.xw * 1.05) - Wd(e.xw)) / (4 * math.pi)
            G3r[f][f"{Xn}|{lm}"] = dict(swept_layer_net_outward_at_plus5pct=sw, swept_restoring=bool(sw < 0), quasi_static_plus5=quasi_static(e, 0.05), quasi_static_minus5=quasi_static(e, -0.05),
                                        s_env=-1.0 / (e.xw * e.s), s_wall=wall_slope(e.xw))
RES["G3_reported"] = G3r

# ====================================================================== G4: KiDS late-type stacks (KO1's machinery)
P("")
P("G4. KiDS cleared lenses: W30 late and host-free late (KO1's machinery).")
Gk, Msun_k, Mpc_k = 6.674e-11, 1.989e30, 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc_k; NPAT = 50
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc_k
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
def mgal_of(logMs): return 10 ** logMs * (1 + 10 ** (-0.69 * logMs + 6.63))
PL = np.load(os.path.join(DLR, "cfg110_perlens.npz")); WG, WW = PL["WG"], PL["WW"]
f30 = np.load(os.path.join(DLR, "cfg96_isoflags.npz"))["f30"]; patch = np.load(os.path.join(DLR, "cfg96_stack.npz"))["patch"]
NL = len(LNS["ra"]); zl = LNS["z"]; logMs = LNS["logM"]; Mg = LNS["Mgal"] * Msun_k; chil = LNS["chi"]; LATE = LNS["typ"] == 0
XGL, WGL = np.polynomial.legendre.leggauss(24); R3k = (3.0 * Mpc_k) ** 2
def cells(fun):
    m = np.zeros((NL, NB))
    for k in range(NB):
        t_lo = Gk * Mg / EDGES[k + 1]; t_hi = np.minimum(Gk * Mg / EDGES[k], R3k); ok = t_hi > t_lo
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XGL[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            fv = fun(Gk * Mg[:, None] / t)
        m[:, k] = np.where(ok, (fv * WGL[None, :]).sum(1) / 2, 0.0)
    return m
def glaw_k(g, a0): return (0.5 + np.sqrt(0.25 + a0 / g)) * g
LAW = {f: cells(lambda g, a=A0[f]: glaw_k(g, a)) for f in FOOT}
def psum(arr, mask):
    pm = patch[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(arr.shape[1])], axis=1)
def amp(mask, Mo, cols):
    Sg = psum(WG[:, cols], mask); Sw = psum(WW[:, cols], mask); Sm = psum((WW * Mo)[:, cols], mask)
    tg, tw, tm = Sg.sum(0), Sw.sum(0), Sm.sum(0)
    D = 4 * Gk * tg / tw; M = tm / tw
    Dl = 4 * Gk * (tg - Sg) / (tw - Sw); Ml = (tm - Sm) / (tw - Sw)
    sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    A = float((D * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    Al = (Dl * Ml / sk ** 2).sum(1) / (Ml * Ml / sk ** 2).sum(1)
    s = float(np.sqrt((NPAT - 1) / NPAT * ((Al - Al.mean()) ** 2).sum()))
    return dict(A=A, s=s, Al=Al, D=D, M=M, sk=sk, tw=tw, cols=cols)
WINS = (("outer", [0, 1, 2, 3]), ("middle", [4, 5, 6]), ("inner", [7, 8, 9, 10, 11, 12]))

# host-free flag (KO1: Delta 0.3 dex, W 230 Mpc, veto radius R_h; plain float comparison)
HB = fits.open(os.path.join(DLR, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
HLp = fits.open(os.path.join(DLR, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HLp[1].data
r_ = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); z_ = np.array(b["zphot_ANNz2"], dtype="f8")
logM_ = np.array(Lp["MASS_MED"], dtype="f8") + 0.15; ra_ = np.array(b["RAJ2000"], dtype="f8"); dec_ = np.array(b["DECJ2000"], dtype="f8")
del b, Lp; HB.close(); HLp.close()
nbm = (r_ < 20) & (z_ >= 0.02) & (z_ <= 0.8) & np.isfinite(logM_) & (logM_ > 7); inb = np.where(nbm)[0]
xN = unitvec(ra_[inb], dec_[inb]); chiN = DC(z_[inb]); logMN = logM_[inb]
key_ = {(a, d): i for i, (a, d) in enumerate(zip(ra_[inb], dec_[inb]))}
selfN = np.array([key_[(a, d)] for a, d in zip(LNS["ra"], LNS["dec"])]); assert np.allclose(logMN[selfN], logMs)
treeN = cKDTree(xN); xL = xN[selfN]
def rh_of(logM): return np.minimum(3.0, np.sqrt(Gk * mgal_of(logM) * Msun_k / 1e-15) / Mpc_k)
def hostfree(fac, W=230.0, dmass=0.3, CH=400):
    chord = 2 * np.sin(fac * rh_of(logMs) * (1 + zl) / chil / 2); dmin = np.full(NL, np.inf)
    for i0 in range(0, NL, CH):
        i1 = min(i0 + CH, NL); lists = treeN.query_ball_point(xL[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
        if tot == 0: continue
        k = np.repeat(np.arange(len(c)), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot); li = i0 + k
        keep = (j != selfN[li]) & (logMN[j] >= logMs[li] + dmass); li, j = li[keep], j[keep]
        np.minimum.at(dmin, li, np.abs(chiN[j] - chil[li]))
    return dmin >= W
HF = {fac: hostfree(fac) for fac in (1.0, 1.3, 1.6)}
P(f"host-free lenses at veto radius 1.0 / 1.3 / 1.6 R_h: {int(HF[1.0].sum()):,} / {int(HF[1.3].sum()):,} / {int(HF[1.6].sum()):,}  [{time.time() - T0:.0f} s]")
SETS = {"W30 late": f30 & LATE, "host-free late": HF[1.0] & LATE}
SETS_R = {"host-free late, veto 1.3 R_h": HF[1.3] & LATE, "host-free late, veto 1.6 R_h": HF[1.6] & LATE}

# KA4: KO1 reproduced
ref = {}
cur = None
for ln_ in open(os.path.join(HERE, "..", "KO1_kids_outer_points", "ko1_extra.out")):
    if ln_.startswith("================ footing"): cur = ln_.split()[-1]
    for nm in ("host-free late", "W30 late"):
        if cur and ln_.strip().startswith(nm + " ") and "outer" in ln_ and cur not in ref.get(nm, {}):
            ref.setdefault(nm, {})[cur] = ln_.split("outer")[1].strip()
ka4 = {}; ok4 = int(HF[1.0].sum()) == 40667
DATA4 = {}
for f in FOOT:
    for nm, m in SETS.items():
        rs = [amp(m, LAW[f], cols) for _, cols in WINS]; DATA4[(f, nm)] = rs
        mine = f"{rs[0]['A']:+.3f} +- {rs[0]['s']:.3f} | middle {rs[1]['A']:+.3f} +- {rs[1]['s']:.3f} | inner {rs[2]['A']:+.3f} +- {rs[2]['s']:.3f}"
        same = mine == ref[nm][f]; ok4 &= same; ka4[f"{f}|{nm}"] = dict(mine=mine, ko1=ref[nm][f], equal=bool(same))
        P(f"KA4 [{f}] {nm:15s}: outer {mine}   KO1: outer {ref[nm][f]} -> {'equal' if same else 'DIFFERENT'}")
KAOK["KA4"] = bool(ok4); RES["KA"]["KA4"] = dict(rows=ka4, host_free=int(HF[1.0].sum()), pass_=bool(ok4))
P(f"KA4 -> {'PASS' if ok4 else 'FAIL'}")

# per-lens model factors on a mass grid, interpolated in log Mgal
LMG = np.round(np.arange(9.1, 11.1001, 0.005), 4)                       # A1: 0.005 dex (was 0.1)
LMG2 = LMG[::2]                                                           # the 0.01-dex subgrid for KA6
lmL = np.log10(LNS["Mgal"])
def factors_grid(a0, Xn, rch, closure="A", lms=LMG):
    Fd, Fr, Fl, envs = [], [], [], []
    for lm in lms:
        e = envelope(lm, a0, Xn, rch, 0.0, closure); envs.append(e)
        d, r, l = bin_factors(e, a0, rM_of(lm, a0)); Fd.append(d); Fr.append(r); Fl.append(l)
    return np.array(Fd), np.array(Fr), np.array(Fl), envs
def interp_rows(F, lms=LMG):
    out = np.empty((NL, NB))
    for k in range(NB): out[:, k] = np.interp(lmL, lms, F[:, k])
    return out
def window_model(mask, LAWc, MODc, rs):
    out = []
    for (wn, cols), r in zip(WINS, rs):
        Sw = WW[mask][:, cols].sum(0); MM = (WW[mask] * MODc[mask])[:, cols].sum(0) / Sw
        out.append(float((MM * r["M"] / r["sk"] ** 2).sum() / (r["M"] * r["M"] / r["sk"] ** 2).sum()))
    return np.array(out)
def chi2_stats(rs, Am):
    Ad = np.array([r["A"] for r in rs]); Al = np.array([r["Al"] for r in rs])
    C = (NPAT - 1) / NPAT * (Al - Al.mean(1, keepdims=True)) @ (Al - Al.mean(1, keepdims=True)).T
    Ci = np.linalg.inv(C); H = (NPAT - 3 - 2) / (NPAT - 1)
    D = Ad - Am; c2 = float(D @ Ci @ D); c2h = H * c2
    c = float((Am @ Ci @ Ad) / (Am @ Ci @ Am)); Dc = Ad - c * Am; c2c = H * float(Dc @ Ci @ Dc)
    return dict(A_data=Ad.tolist(), A_model=Am.tolist(), chi2=c2h, p=float(CHI2.sf(c2h, 3)), chi2_noHartlap=c2, p_noHartlap=float(CHI2.sf(c2, 3)),
                calib_c=c, chi2_calib=c2c, p_calib=float(CHI2.sf(c2c, 2)), errors=np.sqrt(np.diag(C)).tolist(),
                corr=(C / np.sqrt(np.outer(np.diag(C), np.diag(C)))).tolist(), shape_ratio_data=float(Ad[0] / Ad[2]), shape_ratio_model=float(Am[0] / Am[2]))
G4 = {}; FACT = {}; KA6MOVES = []
for f in FOOT:
    a0 = A0[f]; G4[f] = {}
    law_st = {nm: chi2_stats(DATA4[(f, nm)], np.ones(3)) for nm in SETS}
    G4[f]["law_alone"] = law_st
    P(f"[{f}] law alone: " + "; ".join(f"{nm}: A {', '.join(f'{v:+.3f}' for v in law_st[nm]['A_data'])}, chi2 {law_st[nm]['chi2']:.2f} p {law_st[nm]['p']:.4f} "
                                     f"(free calibration c {law_st[nm]['calib_c']:.2f}, p {law_st[nm]['p_calib']:.4f})" for nm in SETS))
    for Xn in XNAMES:
        for rch in ROUTS:
            Fd, Fr, Fl, envs = factors_grid(a0, Xn, rch); FACT[(f, Xn, rch)] = (Fd, Fr, Fl)
            MOD = LAW[f] * interp_rows(Fd); MODr = LAW[f] * interp_rows(Fr); MOD2 = LAW[f] * interp_rows(Fd[::2], LMG2)
            row = dict(no_balance_on_lens_grid=int(sum(not e.balance for e in envs)))
            for nm, m in SETS.items():
                rs = DATA4[(f, nm)]; st = chi2_stats(rs, window_model(m, LAW[f], MOD, rs)); st["raw_A_model"] = window_model(m, LAW[f], MODr, rs).tolist()
                st["A_model_grid_0p01"] = window_model(m, LAW[f], MOD2, rs).tolist(); KA6MOVES.append(float(np.max(np.abs(np.array(st["A_model_grid_0p01"]) - np.array(st["A_model"])))))
                row[nm] = st
            for nm, m in SETS_R.items():
                rs = [amp(m, LAW[f], cols) for _, cols in WINS]; st = chi2_stats(rs, window_model(m, LAW[f], MOD, rs)); row[nm] = st
            row["pass_"] = bool(all(row[nm]["p"] > 0.05 for nm in SETS)); row["pass_G4b"] = bool(all(row[nm]["p_calib"] > 0.05 for nm in SETS))
            G4[f][f"{Xn}|{rch}"] = row
            P(f"[{f}] X {Xn:6s} R_out {rch:6s}: " + "; ".join(f"{nm}: model A {', '.join(f'{v:+.3f}' for v in row[nm]['A_model'])} chi2 {row[nm]['chi2']:.2f} p {row[nm]['p']:.4f} "
                                                         f"(G4b c {row[nm]['calib_c']:.2f} p {row[nm]['p_calib']:.4f})" for nm in SETS)
              + f" -> G4 {'PASS' if row['pass_'] else 'FAIL'}, G4b {'PASS' if row['pass_G4b'] else 'FAIL'}" + (f" [no balance {row['no_balance_on_lens_grid']}]" if row['no_balance_on_lens_grid'] else ""))
RES["G4"] = G4
P(f"   [{time.time() - T0:.0f} s]")
# KA5 limits of the lens model
Fd0, Fr0, Fl0 = bin_factors(None, A0["canonical"], rM_of(10.5, A0["canonical"]))
m_ = SETS["host-free late"]; rs_ = DATA4[("canonical", "host-free late")]
Am0 = window_model(m_, LAW["canonical"], LAW["canonical"] * interp_rows(np.tile(Fd0, (LMG.size, 1))), rs_)
xx = np.array([5.0, 50.0, 500.0]); s0_, m0_ = proj_tab(xx, lambda r: np.zeros_like(np.asarray(r, float)), lambda r: np.zeros_like(np.asarray(r, float)), 1.0, 1e3)
s1_, m1_ = proj_shell(xx, 0.0, 1e3); ppt = 4.0 * ((1.0 + m0_ + m1_) / (math.pi * xx * xx) - (s0_ + s1_)); e5b = float(np.max(np.abs(ppt / ((4 / math.pi) / xx ** 2) - 1)))
ok5 = float(np.max(np.abs(Am0 - 1))) < 1e-9 and e5b < 1e-4; KAOK["KA5"] = ok5
RES["KA"]["KA5"] = dict(no_wall_amplitudes=Am0.tolist(), point_raw=e5b, pass_=bool(ok5))
P(f"KA5 no wall -> window amplitudes {', '.join(f'{v:.12f}' for v in Am0)}; point baryons raw vs (4/pi) g: {e5b:.1e} -> {'PASS' if ok5 else 'FAIL'}")
# KA6 (A1): window amplitudes converge between the 0.01- and 0.005-dex lens grids (closure A here; closure C added below)
ka6f_rel = ka6f_abs = 0.0
for f in FOOT:
    for Xn in ("share", "census"):
        Fd, _, _ = FACT[(f, Xn, "rta")]
        for lmm in (9.1525, 10.0525, 10.9525):
            d, _, _ = bin_factors(envelope(lmm, A0[f], Xn, "rta"), A0[f], rM_of(lmm, A0[f]))
            ii = np.array([np.interp(lmm, LMG, Fd[:, k]) for k in range(NB)])
            ka6f_rel = max(ka6f_rel, float(np.max(np.abs(ii / d - 1)))); ka6f_abs = max(ka6f_abs, float(np.max(np.abs(ii - d))))
RES["KA"]["KA6_frozen_pointwise_reported"] = dict(grid_dex=0.005, max_rel=ka6f_rel, max_abs=ka6f_abs, note="as frozen; replaced by A1, gates nothing")
P(f"KA6 as frozen (reported, A1): pointwise per-bin factor at mid-grid masses, 0.005-dex grid: max rel {ka6f_rel:.1e}, max abs {ka6f_abs:.1e}  [{time.time() - T0:.0f} s]")

# ====================================================================== G5: X-COP and Lovisari groups
P("")
P("G5. Hot systems: component pressure (hydrostatic, measured mass) against the wall pressure of their own baryons.")
def li(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
XD = os.path.join(REPO, "real_research", "data", "xcop")
G5 = {}
def pw_phys(Mb_kg, r_m, a0): return float(p_wall_swt1(G * Mb_kg / (a0 * r_m * r_m), a0)) * PSIGN * PSCALE
for f in FOOT:
    a0 = A0[f]; G5[f] = dict(xcop={}, groups={})
    for name in sorted(os.listdir(XD)):
        p_ = os.path.join(XD, name)
        if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))): continue
        with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = float(h[1].header["R500"])
        with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg5 = float(h[1].header["R500"])
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        gr = np.array(gas["RADIUS"], float) * rg5; gM = np.array(gas["MGAS"], float); sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float)
        out_ = {}
        for col in ("M_FORW", "M_NFW"):                                            # M_NFW: post hoc bracket (A1), reported only
            hr = np.array(hm["RADIUS"], float); hM = np.array(hm[col], float)
            rr, Mt, Mb = [], [], []
            for t in hr:
                mg = li(gr, gM, t)
                if not np.isfinite(mg): continue
                ms_ = li(sr, sM, t) if t <= sr[-1] else sM[-1]
                if not np.isfinite(ms_): continue
                rr.append(t); Mt.append(li(hr, hM, t)); Mb.append(mg + ms_)
            rr, Mt, Mb = np.array(rr) * KPC, np.array(Mt) * MS, np.array(Mb) * MS
            Mc = Mt - Mb; rho_c = np.clip(np.gradient(Mc, rr) / (4 * math.pi * rr ** 2), 0.0, None)
            integ = rho_c * G * Mt / rr ** 2
            pc = np.array([np.trapz(integ[i:], rr[i:]) for i in range(rr.size)])
            pwv = np.array([pw_phys(Mb[i], rr[i], a0) for i in range(rr.size)])
            sel = (rr >= 0.05 * r500 * KPC) & (rr <= r500 * KPC)
            ratio = pwv[sel] / np.maximum(pc[sel], 1e-300); xr_ = rr[sel] / KPC / r500
            bad = xr_[pwv[sel] >= pc[sel]]
            out_[col] = dict(max_pwall_over_pc=float(ratio.max()), at_R500_over=float(xr_[np.argmax(ratio)]), first_fail_R500=(float(bad.min()) if bad.size else None),
                             ratio_at_0p05_0p25_0p5=[float(np.interp(x, xr_, ratio)) for x in (0.05, 0.25, 0.5)], Mc_falls_beyond_R500=(float(xr_[np.argmax(Mc[sel])]) if np.any(np.diff(Mc[sel]) < 0) else None),
                             held=bool(np.all(pwv[sel] < pc[sel])), r_range_R500=[float(xr_.min()), float(xr_.max())], gas_extent_R500=float(rr.max() / KPC / r500))
        G5[f]["xcop"][name] = dict(R500_kpc=r500, **out_["M_FORW"], posthoc_M_NFW=out_["M_NFW"])
        held = out_["M_FORW"]["held"]
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
    hdr, rows = rows[0], rows[1:]
    for r in rows:
        d = dict(zip(hdr, r)); R5, R25 = float(d["R500_kpc"]), float(d["R2500_kpc"])
        M5, M25 = float(d["M500_1e13"]) * 1e13, float(d["M2500_1e13"]) * 1e13; g5, g25 = float(d["Mgas500_1e12"]) * 1e12, float(d["Mgas2500_1e12"]) * 1e12
        st_ = math.log(M5 / M25) / math.log(R5 / R25); sg_ = math.log(g5 / g25) / math.log(R5 / R25)
        for fst in (0, 1):
            rr = np.logspace(math.log10(0.05 * R5), math.log10(2 * R5), 400) * KPC; x = rr / (R25 * KPC)
            Mt = M25 * x ** st_ * MS; Mb = (1 + fst) * g25 * x ** sg_ * MS
            rho_c = np.clip((st_ * Mt - sg_ * Mb) / rr / (4 * math.pi * rr ** 2), 0.0, None)
            integ = rho_c * G * Mt / rr ** 2; pc = np.array([np.trapz(integ[i:], rr[i:]) for i in range(rr.size)])
            pwv = np.array([pw_phys(Mb[i], rr[i], a0) for i in range(rr.size)]); sel = rr <= R5 * KPC
            ratio = pwv[sel] / np.maximum(pc[sel], 1e-300)
            G5[f]["groups"][f"{d['name']}|f*{fst}"] = dict(slopes=[st_, sg_], max_pwall_over_pc=float(ratio.max()),
                                                          at_R500_over=float(rr[sel][np.argmax(ratio)] / KPC / R5), held=bool(np.all(pwv[sel] < pc[sel])))
    xc = G5[f]["xcop"]; gp = G5[f]["groups"]
    G5[f]["pass_"] = bool(all(v["held"] for v in xc.values()) and all(v["held"] for v in gp.values()))
    P(f"[{f}] X-COP ({len(xc)}), M_FORW (graded): max p_wall / p_c on [0.05, 1] R500 per cluster " + ", ".join(f"{k} {v['max_pwall_over_pc']:.3g}" + (f" (wall possible from {v['first_fail_R500']:.2f} R500)" if v['first_fail_R500'] else "") for k, v in xc.items()))
    P(f"[{f}] X-COP post hoc with M_NFW (reported): " + ", ".join(f"{k} {v['posthoc_M_NFW']['max_pwall_over_pc']:.3g}" + (f" (from {v['posthoc_M_NFW']['first_fail_R500']:.2f} R500)" if v['posthoc_M_NFW']['first_fail_R500'] else "") for k, v in xc.items()))
    P(f"[{f}] Lovisari groups ({len(gp) // 2} x f* 0, 1): max p_wall / p_c {max(v['max_pwall_over_pc'] for v in gp.values()):.3f} "
      f"(median {np.median([v['max_pwall_over_pc'] for v in gp.values()]):.3f}); held {sum(v['held'] for v in gp.values())} of {len(gp)} -> G5 {'PASS' if G5[f]['pass_'] else 'FAIL'}")
RES["G5"] = G5

# ====================================================================== G6 formation (reported)
P("")
P("G6 (reported). Formation requirement at the KiDS masses, primary R_out.")
G6 = {}
for f in FOOT:
    a0 = A0[f]; G6[f] = {}
    for Xn in XNAMES:
        for lm in KIDS:
            e = ENV[(f, Xn, "rta", lm)]
            if not e.balance: G6[f][f"{Xn}|{lm}"] = None; continue
            Mb = 10 ** lm * MS; rM = rM_of(lm, a0); vf = vf_of(lm, a0); Ro = e.xo * rM; rvir = Ro / 2
            sig = math.sqrt(e.s) * vf; svir = math.sqrt(G * (1 + e.X) * Mb / Ro)
            coll = [e.X * min(r / rvir, 1.0) for r in (200 * KPC, 1 * MPC, 3 * MPC)]
            envm = [float(e.Menc(np.array([r / rM]))[0]) for r in (200 * KPC, 1 * MPC, 3 * MPC)]
            f_never = min(e.xw * rM / rvir, 1.0)
            Rh = Rms("NC", Mb, 0.0, 1.0) if Xn == "share" else None
            rho_out = math.exp(float(e.lr[-1])) * Mb / rM ** 3; p_out = rho_out * sig ** 2
            G6[f][f"{Xn}|{lm}"] = dict(sigma_kms=sig / 1e3, sigma_vir_kms=svir / 1e3, ratio=sig / svir, Menv=envm, Mcollapsed_SIS_rvir=coll,
                                       frac_never_inside_Rw=f_never, frac_never_SWT1_placement=(min(e.xw * rM / Rh, 1.0) if Rh else None),
                                       p_out_over_mean_sigma2=p_out / (RHO_D0 * sig ** 2), p_out_over_ram=p_out / (RHO_M0 * (H0s * Ro) ** 2))
            g = G6[f][f"{Xn}|{lm}"]
            P(f"[{f}] X {Xn:6s} log M_b {lm}: sigma {g['sigma_kms']:.1f} vs virial {g['sigma_vir_kms']:.1f} km/s ({g['ratio']:.2f}); M < 0.2/1/3 Mpc envelope "
              + " / ".join(f"{v:.2f}" for v in envm) + " vs collapsed " + " / ".join(f"{v:.2f}" for v in coll) + f" M_b; share never inside R_w {g['frac_never_inside_Rw']:.2f}"
              + (f" (SWT1 placement {g['frac_never_SWT1_placement']:.2f})" if Rh else "") + f"; edge pressure / (rho_d sigma^2) {g['p_out_over_mean_sigma2']:.1f}, / ram {g['p_out_over_ram']:.2f}")
RES["G6"] = G6

# ====================================================================== pooled B21 gate (reported)
P("")
P("Pooled KiDS gate of the record (B21 Fig. 9, 59 points), every lens cleared, primary R_out.")
DB = os.path.join(DLR, "brouwer2021_rar"); Gpc = 4.52e-30
LE = []
for i, lm in enumerate(KIDS, 1):
    a = np.loadtxt(os.path.join(DB, f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")
    gbar = a[:, 0]; gobs = 4 * Gpc * a[:, 1] / a[:, 4] * PC; err = 4 * Gpc * a[:, 3] / a[:, 4] * PC
    for gb, go, er in zip(gbar, gobs, err):
        if go > 0: LE.append(dict(lm=lm, gbar=gb, gobs=go, err=er))
B21 = {}
for f in FOOT:
    a0 = A0[f]; B21[f] = {}
    chi_law = sum(((a0 * float(u_in(d["gbar"] / a0)) - d["gobs"]) / d["err"]) ** 2 for d in LE)
    for Xn in XNAMES:
        nb_d = nb_r = 0; c_d = c_r = 0.0; nout = 0
        for lm in KIDS:
            e = ENV[(f, Xn, "rta", lm)]; pts = [d for d in LE if d["lm"] == lm]
            x = np.array([math.sqrt(a0 / d["gbar"]) for d in pts]); gl = a0 * glaw_d(x); pl = P_law(x); pm = P_model(x, e)
            md = gl * pm / pl; mr = a0 * pm
            for d, xd, gd, mdd, mrr in zip(pts, x, gl, md, mr):
                nb_d += abs(math.log10(mdd / gd)) > 0.05 if mdd > 0 else 1; nb_r += abs(math.log10(mrr / gd)) > 0.05 if mrr > 0 else 1
                c_d += ((mdd - d["gobs"]) / d["err"]) ** 2; c_r += ((mrr - d["gobs"]) / d["err"]) ** 2
                nout += xd > (e.xw if e.balance else e.xo)
        B21[f][Xn] = dict(points=len(LE), outside_wall=int(nout), over_0p05_diff=int(nb_d), over_0p05_raw=int(nb_r), chi2_law=chi_law, chi2_model_diff=c_d, chi2_model_raw=c_r)
        P(f"[{f}] X {Xn:6s}: {nout} of {len(LE)} points outside the wall; beyond 0.05 dex of the law: {nb_d} (differential) / {nb_r} (raw); chi2 vs data: law {chi_law:.1f}, "
          f"model {c_d:.1f} (differential) / {c_r:.1f} (raw)")
RES["B21"] = B21

# ====================================================================== closure C (reported; primary R_out)
P("")
P("Closure C (reported): sigma^2 = G (1 + X) M_b / (2 R_out); gates G1-G4 at the primary R_out.")
CC = {}
for f in FOOT:
    a0 = A0[f]; CC[f] = {}
    for Xn in XNAMES:
        ek = [envelope(lm, a0, Xn, "rta", 0.0, "C") for lm in KIDS]
        eg = {z: [envelope(lm, a0, Xn, "rta", z, "C") for lm in LG] for z in ZS}
        xs_ = [e.xw if e.balance else None for e in ek + eg[0.0]]; nob = sum(x is None for x in xs_)
        g1 = nob == 0 and all(x >= 10 for x in xs_)
        q = {str(z): comp(tab_of(eg[z], LG, a0), a0, z)["q_tot"] for z in ZS}; g2 = all(v <= LINE for v in q.values())
        g3 = nob == 0 and all((-1.0 / (e.xw * e.s)) > wall_slope(e.xw) for e in ek + eg[0.0] if e.balance)
        Fd, _, _, envs = factors_grid(a0, Xn, "rta", "C"); MOD = LAW[f] * interp_rows(Fd); MOD2 = LAW[f] * interp_rows(Fd[::2], LMG2); g4 = {}
        for nm, m in SETS.items():
            rs = DATA4[(f, nm)]; g4[nm] = chi2_stats(rs, window_model(m, LAW[f], MOD, rs))
            g4[nm]["A_model_grid_0p01"] = window_model(m, LAW[f], MOD2, rs).tolist(); KA6MOVES.append(float(np.max(np.abs(np.array(g4[nm]["A_model_grid_0p01"]) - np.array(g4[nm]["A_model"])))))
        g4p = all(g4[nm]["p"] > 0.05 for nm in SETS)
        CC[f][Xn] = dict(kids=[env_row(lm, a0, e) for lm, e in zip(KIDS, ek)], G1=bool(g1), min_x_w=min([x for x in xs_ if x is not None], default=None), no_balance=nob,
                         G2_q=q, G2=bool(g2), G3=bool(g3), G4=g4, G4_pass=bool(g4p))
        P(f"[{f}] X {Xn:6s}: R_w / R_K at the KiDS masses " + ", ".join((f"{r['R_w_over_RK']:.3f}" if r["balance"] else "none") for r in CC[f][Xn]["kids"])
          + f"; A " + ", ".join((f"{r['A']:.3f}" if r["balance"] else "-") for r in CC[f][Xn]["kids"]) + f"; G1 {'PASS' if g1 else 'FAIL'} (min x_w {CC[f][Xn]['min_x_w']}), "
          f"G2 {'PASS' if g2 else 'FAIL'} (q " + " / ".join(f"{v:.4f}" for v in q.values()) + f"), G3 {'PASS' if g3 else 'FAIL'}, G4 {'PASS' if g4p else 'FAIL'} (p "
          + ", ".join(f"{g4[nm]['p']:.4f}" for nm in SETS) + ")")
RES["closureC"] = CC

RES["root_bracket_misses"] = [list(map(float, m)) for m in BRACKET_MISSES]
P(f"root bracketing (A2): {len(BRACKET_MISSES)} table sign changes not confirmed by the exact function")
ka6 = max(KA6MOVES); ok6 = ka6 < 0.01; KAOK["KA6"] = ok6
RES["KA"]["KA6"] = dict(max_window_move_0p01_to_0p005=ka6, cases=len(KA6MOVES), pass_=bool(ok6))
P(f"KA6 (A1): largest change of a model window amplitude between the 0.01- and 0.005-dex lens grids over {len(KA6MOVES)} case-stacks: {ka6:.4f} (line 0.01) -> {'PASS' if ok6 else 'FAIL'}")
# ====================================================================== labels
P("")
kaall = all(KAOK.values())
RES["KA_all"] = dict(KAOK, all=bool(kaall))
P("Known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in KAOK.items()))
LAB = {}
for f in FOOT:
    per = {}
    for rch in ROUTS:
        for Xn in XNAMES:
            k = f"{Xn}|{rch}"
            gates = dict(G1=G1[f][k]["pass_"], G2=G2[f][k]["pass_"], G3=G3[f][k]["pass_"], G4=G4[f][k]["pass_"], G5=G5[f]["pass_"])
            per[k] = dict(gates=gates, all_pass=bool(all(gates.values())), G4b=G4[f][k]["pass_G4b"])
    prim = [Xn for Xn in XNAMES if per[f"{Xn}|rta"]["all_pass"]]
    if not kaall: lab = "NO VERDICT (known answer failed; Lean status in compile.txt)"
    elif prim: lab = "PASSES STATIC GATES (X: " + ", ".join(prim) + ")"
    else: lab = "FAILS (" + "; ".join(f"{Xn}: " + ", ".join(g for g, v in per[f'{Xn}|rta']['gates'].items() if not v) for Xn in XNAMES) + ")"
    brk = [k for k, v in per.items() if v["all_pass"] and not k.endswith("|rta")]
    LAB[f] = dict(label=lab, per=per, brackets_passing=brk)
    P(f"LABEL [{f}] (pending Lean A1-A3, A5, A8): {lab}" + (f"; brackets passing all gates: {brk}" if brk else "; no bracket passes all gates"))
    for k, v in per.items():
        P(f"   [{f}] {k:14s}: " + " ".join(f"{g} {'P' if ok else 'F'}" for g, ok in v["gates"].items()) + f" | G4b {'P' if v['G4b'] else 'F'}")
RES["labels"] = LAB

if MUT == "M1":
    nob_all = all(not e.balance for e in ENV.values()) and all(not e.balance for v in GRID.values() for e in v)
    RES["MUTATE"]["M1"] = dict(no_balance_everywhere=bool(nob_all), bites=bool(nob_all))
    P(f"MUTATE M1 (wall pressure sign flipped): NO BALANCE for every mass, X and R_out -> {'BITES' if nob_all else 'NO BITE'}")
if MUT == "M2":
    bite = all(not G1[f][f"{Xn}|rta"]["pass_"] for f in FOOT for Xn in XNAMES)
    RES["MUTATE"]["M2"] = dict(G1_fails_every_X=bool(bite), bites=bool(bite))
    P(f"MUTATE M2 (p_wall / 100): G1 fails for every X at the primary R_out on both footings -> {'BITES' if bite else 'NO BITE'}")
if MUT == "M3":
    moved = None
    mj = os.path.join(HERE, "he1.json")
    if os.path.exists(mj):
        G4m = json.load(open(mj))["G4"]
        moved = max(abs(G4[f][k][nm]["A_model"][i] - G4m[f][k][nm]["A_model"][i]) for f in FOOT for k in G4[f] if k != "law_alone" for nm in SETS for i in range(3))
    bite = (not KAOK["KA3"]) and (moved is not None and moved > 1e-6)
    RES["MUTATE"]["M3_max_window_move"] = moved
    RES["MUTATE"]["M3"] = dict(KA3_fails=bool(not KAOK["KA3"]), sis_ratio=RES["KA"]["KA3"]["sis_untruncated_ratio"], bites=bool(bite),
                               note="compare the G4 model amplitudes in this file with he1.json")
    P(f"MUTATE M3 (envelope as a point mass in projection): KA3 singular-sphere ratio " + ", ".join(f"{v:.4f}" for v in RES['KA']['KA3']['sis_untruncated_ratio'])
      + f" (4/pi = {4 / math.pi:.4f}); largest move of a model window amplitude against he1.json {moved} -> {'BITES' if bite else 'NO BITE'}")
P(f"runtime {time.time() - T0:.0f} s. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
