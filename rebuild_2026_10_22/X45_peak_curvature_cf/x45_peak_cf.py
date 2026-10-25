#!/usr/bin/env python3
"""X45_peak_curvature_cf: formation concentration from the BBKS peak profile (height + curvature) on the record's own P(k),
spherical collapse shell by shell; X43's rule regraded with c_f(M).

Frozen criteria: FROZEN_CRITERIA.md (1fd8e1238a). EM1's CLASS (background A) and X43's committed script executed read-only.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x45_peak_cf.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x45_peak_cf.py --mutate   -> curvature term sign flipped (K1 must fail)
"""
import os, sys, json, math, time, io, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.special import erf
from scipy.integrate import quad

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
P(f"X45_peak_curvature_cf  {'MUTATE run (curvature term sign flipped)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; record P(k) (EM1 CLASS, bg A); BBKS peak statistics + spherical collapse; no simulation calibration; not theory closed")

# ------------------------------------------------------------------ EM1 CLASS (read-only)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- halo profiles")], EM1SRC, "exec"), NE)
sys.argv = argv0
bg = NE["BGS"]["A_c2b_refit"]; cc = bg["c"]; h = bg["h"]
checks = []
k3 = all(abs(NE["BGS"][t]["s8"] - NE["BGS"][t]["s8_F3"]) <= 1e-3 for t in NE["BGS"])
P(f"K3 EM1 sigma8 own vs F3: {'PASS' if k3 else 'FAIL'}"); checks.append(("K3", k3))
Om = float(cc.Omega_m()); RHOM = Om * 2.775e11 * h ** 2                       # Msun / Mpc^3 (comoving)
K = np.logspace(-4, 2.14, 4000); PK = np.array([cc.pk_lin(k, 0.0) for k in K])  # 1/Mpc, Mpc^3
ZG = np.concatenate([np.linspace(0, 10, 1001), np.geomspace(10.01, 3000, 800)])
DG = np.array([cc.scale_independent_growth_factor(z) for z in ZG]); DG /= DG[0]
def z_of_D(D): return float(np.interp(-D, -DG, ZG))                          # DG decreasing in z
sigTH = NE["BGS"]["A_c2b_refit"]["cB"].__defaults__[1]
lMg = np.linspace(7.0, 16.5, 191); s2TH = np.array([float(sigTH(10 ** l)[0]) ** 2 for l in lMg])
def zform(M):
    S = math.sqrt(max(float(np.interp(math.log10(M / 2), lMg, s2TH)) - float(np.interp(math.log10(M), lMg, s2TH)), 0.0))
    Df = 1.686 / (1.686 + 0.974 * S); return z_of_D(Df), Df

# ------------------------------------------------------------------ BBKS
def fBBKS(x):
    x = np.asarray(x, float)
    return ((x ** 3 - 3 * x) / 2 * (erf(math.sqrt(2.5) * x) + erf(math.sqrt(2.5) * x / 2))
            + math.sqrt(2 / (5 * math.pi)) * ((31 * x ** 2 / 4 + 1.6) * np.exp(-5 * x ** 2 / 8) + (x ** 2 / 2 - 1.6) * np.exp(-5 * x ** 2 / 2)))
def xmean(nu, gam):
    xs = np.linspace(1e-4, 30, 30001); w = fBBKS(xs) * np.exp(-(xs - gam * nu) ** 2 / (2 * (1 - gam ** 2)))
    return float(np.trapz(xs * w, xs) / np.trapz(w, xs))
def moments(RG):
    W2 = np.exp(-(K * RG) ** 2); base = PK * W2 * K ** 2 / (2 * math.pi ** 2)
    s = [math.sqrt(np.trapz(base * K ** (2 * j), K)) for j in range(3)]
    return s, base
CROSS = {"on": False}                                                        # A2: unsmoothed density around the smoothed peak (W^1)
def profile(RG, nu, r):
    (s0, s1, s2), base = moments(RG); gam = s1 ** 2 / (s0 * s2); x = xmean(nu, gam)
    if CROSS["on"]:
        base = PK * np.exp(-(K * RG) ** 2 / 2) * K ** 2 / (2 * math.pi ** 2)
    kr = np.outer(r, K); j0 = np.where(kr > 1e-8, np.sin(kr) / np.maximum(kr, 1e-300), 1.0)
    xi = np.trapz(base[None, :] * j0, K, axis=1); lap = -np.trapz(base[None, :] * K ** 2 * j0, K, axis=1)
    sgn = -1.0 if MUTATE else 1.0
    d = (nu - gam * x) / (1 - gam ** 2) * xi / s0 - sgn * (x - gam * nu) / (1 - gam ** 2) * lap / s2
    return d, dict(s0=s0, s1=s1, s2=s2, gam=gam, x=x)
# K1 identities at one mass
RG1 = (1e12 / ((2 * math.pi) ** 1.5 * RHOM)) ** (1 / 3); nu1 = 2.0
rr = np.array([0.0, 1e-3 * RG1, 2e-3 * RG1])
d1, m1 = profile(RG1, nu1, rr)
lap0 = 2 * (d1[1] - d1[0]) / rr[1] ** 2 * 3                                   # spherical Laplacian at 0: 3 d2/dr2 = 6 (d(h)-d(0))/h^2
lapc = (d1[2] - d1[0]) - 4 * (d1[1] - d1[0])                                 # Richardson for -del^2 delta(0)
h1 = rr[1]; l0 = 3 * 2 * ((4 * (d1[1] - d1[0]) - (d1[2] - d1[0]) / 4 * 4 / 4) / (3 * h1 ** 2))
# direct: -del^2 delta(0) = integral form
(s0, s1, s2), base = moments(RG1)
lapint = -(m1["s0"] * 0 + 1)                                                  # placeholder replaced below
xi0 = np.trapz(base, K); xi0lap = -np.trapz(base * K ** 2, K); xi0lap2 = np.trapz(base * K ** 4, K)
sgn = -1.0 if MUTATE else 1.0
g_, x_ = m1["gam"], m1["x"]
d0_formula = (nu1 - g_ * x_) / (1 - g_ ** 2) * xi0 / s0 - sgn * (x_ - g_ * nu1) / (1 - g_ ** 2) * xi0lap / s2
lap_formula = (nu1 - g_ * x_) / (1 - g_ ** 2) * xi0lap / s0 - sgn * (x_ - g_ * nu1) / (1 - g_ ** 2) * xi0lap2 / s2
k1a = abs(d0_formula / (nu1 * s0) - 1) < 1e-6 and abs(d1[0] / (nu1 * s0) - 1) < 1e-6
k1b = abs(-lap_formula / (x_ * s2) - 1) < 1e-6
k1 = k1a and k1b
P(f"K1 BBKS identities at M 1e12, nu 2: delta(0)/(nu s0) - 1 = {d0_formula / (nu1 * s0) - 1:+.1e}; -lap delta(0)/(x s2) - 1 = {-lap_formula / (x_ * s2) - 1:+.1e}: {'PASS' if k1 else 'FAIL'}")
checks.append(("K1", k1))
xhi = xmean(30.0, g_); k2 = abs(xhi / (g_ * 30.0) - 1) < 0.05   # A1: the limit is slow; checked at nu = 30
P(f"K2 high-nu limit <x|nu=30> / (gamma nu) = {xhi / (g_ * 30.0):.4f}: {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))

# ------------------------------------------------------------------ concentration from collapse of the peak profile
def cf_peak(M):
    zf, Df = zform(M); Mf = M / 2; RG = (Mf / ((2 * math.pi) ** 1.5 * RHOM)) ** (1 / 3)
    s0 = moments(RG)[0][0]
    qM = (3 * Mf / (4 * math.pi * RHOM)) ** (1 / 3)
    q = np.geomspace(qM * 1e-3, qM * 3, 700); r = np.geomspace(qM * 1e-4, qM * 3, 1400)
    def dbar_of(nu_):
        d_, m_ = profile(RG, nu_, r)
        cum_ = np.concatenate([[0], np.cumsum(0.5 * (d_[1:] * r[1:] ** 2 + d_[:-1] * r[:-1] ** 2) * np.diff(r))])
        return 3 * np.interp(q, r, cum_) / q ** 3, m_
    # A1: nu set so that the half-mass object (enclosed mean inside q_M) collapses at z_f, as the construction defines
    from scipy.optimize import brentq as _bq
    thr = 1.686 / Df
    nu = _bq(lambda nu_: float(np.interp(qM, q, dbar_of(nu_)[0])) - thr, 0.05, 50.0, xtol=1e-10)
    dbar, m = dbar_of(nu)
    coll = dbar >= 1.686 / Df
    if not coll.any(): return dict(M=M, flag="none collapsed", cf=1.85)
    Dta = 1.062 / dbar; zta = np.array([z_of_D(min(D_, 1.0)) for D_ in Dta]); ata = 1 / (1 + zta)
    rf = 0.5 * ata * q / 5.55 ** (1 / 3)
    Mq = 4 / 3 * math.pi * RHOM * q ** 3
    qc = q[coll]; rc = rf[coll]; Mc = Mq[coll]
    nonmono = int(np.sum(np.diff(rc) <= 0))
    o = np.argsort(rc); rc, Mc = rc[o], Mc[o]
    lr, lM = np.log(rc), np.log(Mc)
    # smoothed slope: dlnM/dlnr -> dlnrho/dlnr = dlnM/dlnr - 3
    kern = 15
    lMs = np.convolve(lM, np.ones(kern) / kern, mode="same"); lrs = np.convolve(lr, np.ones(kern) / kern, mode="same")
    sl = np.gradient(lMs, lrs) - 3.0
    sel = slice(kern, len(sl) - kern)
    rs_, sls = rc[sel], sl[sel]
    cross = np.where((sls[:-1] > -2) & (sls[1:] <= -2))[0]
    if len(cross) == 0:
        return dict(M=M, zf=zf, nu=nu, x=m["x"], gam=m["gam"], flag="no -2 crossing", cf=1.85, nonmono=nonmono,
                    slope_range=[float(sls.min()), float(sls.max())])
    i = cross[0]; rm2 = float(np.exp(np.interp(-2, [sls[i + 1], sls[i]], [math.log(rs_[i + 1]), math.log(rs_[i])])))
    rout = float(rc.max())
    return dict(M=M, zf=zf, nu=nu, x=m["x"], gam=m["gam"], cf=rout / rm2, r_out=rout, r_m2=rm2, nonmono=nonmono, flag="ok")
CROSS["on"] = True                                                           # A2: K1 above used the smoothed field (identities); collapse uses the cross profile
LMG = np.linspace(10.0, 15.5, 12)
TAB = []
for lm in LMG:
    tb = cf_peak(10 ** lm); TAB.append(tb)
    P(f"  M 1e{lm:.1f}: z_f {tb.get('zf', float('nan')):.2f}, nu {tb.get('nu', float('nan')):.2f}, <x> {tb.get('x', float('nan')):.2f}, gamma {tb.get('gam', float('nan')):.2f} -> "
      f"c_f,pk {tb['cf']:.2f} [{tb['flag']}; non-monotone shells {tb.get('nonmono', '-')}]")
CFT = np.array([t["cf"] for t in TAB])
def cf_of(M): return float(np.interp(math.log10(M), LMG, CFT))
B1 = 3 * math.log(2) - math.pi / 2
def eta_of_M(M): return 4.0 / (3.0 * B1) * cf_of(M) ** 1.25
P(f"  c_f,pk at 1e13 (groups) {cf_of(1e13):.2f}, 1e14 {cf_of(1e14):.2f}, 1e15 {cf_of(1e15):.2f}  (data need ~4-4.2, X44)   [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------------ regrade X43 with eta(M)
def run_x43(eta_fun, tag):
    src = open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")).read()
    old = 'sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2'; assert src.count(old) == 1
    src = src.replace(old, 'sc = (ETA_FUN(M) if (ETA_FUN is not None and ETA_USE["v"] == ETA) else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2')
    src = src.replace('f"x43_collapse_core{TAG}.out"', f'"x45_regrade_{tag}.out"').replace('f"x43_collapse_core_results{TAG}.json"', f'"x45_regrade_{tag}_results.json"')
    src = src.replace('"x43_x30_machinery"', '"x45_x30_machinery"').replace("sys.exit(0 if n == len(checks) else 1)", "pass")
    ns = {"__file__": os.path.join(HERE, "x43_copy.py"), "__name__": "x43_copy", "ETA_FUN": eta_fun}
    a0 = sys.argv; sys.argv = [ns["__file__"]]
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        exec(compile(src, ns["__file__"], "exec"), ns)
    sys.argv = a0
    return ns["RES"]
R4 = run_x43(None, "cf4")
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
dd = max(abs(R4["footings"][f]["groups"]["Z"] - X43J["footings"][f]["groups"]["Z"]) for f in ("canonical", "alt"))
k0 = dd < 1e-9
P(f"K0 constant c_f 4 reproduces X43: max |d groups Z| {dd:.1e}: {'PASS' if k0 else 'FAIL'}"); checks.append(("K0", k0))
RP = run_x43(eta_of_M, "cfpk")
RES = dict(frozen="1fd8e1238a", mutate=MUTATE, table=TAB, footings={})
for f in ("canonical", "alt"):
    F = RP["footings"][f]; c0 = F["clusters"]["cells"]["h0672"]; sp = F["sparc"]["A_c2b_refit"]; gr = F["groups"]
    fails = F["failing"]; v = "PK PASSES" if not fails else "PK FAILS: " + ", ".join(fails)
    RES["footings"][f] = dict(verdict=v, sparc=dict(rms=sp["rms"], U=sp["U_median"], line=sp["line"]), groups=dict(Z=gr["Z"], verdict=gr["verdict"]),
                              MID_T3=c0["G-MID-T3"], MID_b=c0["G-MID-b"], OUT_M3=c0["G-OUT-M3"], OUT_all=c0["G-OUT-all"])
    P(f"\n=== [{f}] c_f,pk(M)")
    P(f"  SPARC bg A: rms {sp['rms']:.4f}, U {sp['U_median']:.2f}, line {'PASS' if sp['line'] else 'FAIL'}; groups Z {gr['Z']:+.2f} {gr['verdict']}")
    P(f"  MID T3 pred {c0['G-MID-T3']['pred']:.3f} Z {c0['G-MID-T3']['Z']:+.2f}; MID slope Z {c0['G-MID-b']['Z']:+.2f}; OUTER all Z {c0['G-OUT-all']['Z']:+.2f}; MGAS T3 OUTER Z {c0['G-OUT-M3']['Z']:+.2f}")
    P(f"  VERDICT [{f}]: {v}")
V = {f: RES["footings"][f]["verdict"].split(":")[0] for f in RES["footings"]}
RES["verdict"] = RES["footings"]["canonical"]["verdict"] if V["canonical"] == V["alt"] else f"UNDECIDED {V}"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
checks.append(("K4", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x45_peak_cf{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x45_peak_cf_results{TAG}.json"), "w"), indent=1, default=float)
try: os.remove(os.path.join(HERE, "x43_copy.py"))
except OSError: pass
sys.exit(0 if n == len(checks) else 1)
