"""IC1_inner_cluster_band shared machinery (read-only on SC1 -> X38 -> EM1/X30, exactly as OS1 loads it).

Exposes a generic halo shape so the Burkert profile of X38/SC1/OS1 can be swapped without touching their files:
    M(<r) = pi * Sigma * r0^2 * Bshape(r / r0),  Sigma = rho0 * r0.
Burkert: X38's B(x).  Non-singular isothermal sphere (King radius r0, rho0 r0^2 = 9 sigma^2 / 4 pi G, LN1 T7's premise):
Bshape = 4 m(x), m(x) = xi^2 psi'(xi) / 27 with xi = 3x (isothermal Lane-Emden, psi(0) = psi'(0) = 0).
"""
import os, sys, io, json, math, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
SC1SRC = os.path.join(REB, "SC1_self_coupled_core_law", "sc1_core_law.py"); TS = open(SC1SRC).read()
code = TS[:TS.index('checks = [("K1", k1)]')]
code = code.replace('os.path.join(HERE, "sc1_x30_machinery.log")', repr(os.path.join(HERE, "ic1b_x30_machinery.log")))
NS = {"__file__": SC1SRC, "__name__": "sc1_ro"}; _argv0 = sys.argv; sys.argv = [SC1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, SC1SRC, "exec"), NS)
sys.argv = _argv0
NX = NS["NX"]
(sparc_os1, grade_os1, BGS, line, FEET, HK, SREF, SIG, B_burk, prep, PREP, RM, N, ALLI, I, TID, T3M, BN, M, DC,
 X7J, bsum, wls1, X1m, GALS, fit_one, pooled, GE, MSUNE, MPCE, SIG_C, SIG_G, dvecN) = (NS[k] for k in (
    "sparc", "grade", "BGS", "line", "FEET", "HK", "SREF", "SIG", "B", "prep", "PREP", "RM", "N", "ALLI", "I", "TID", "T3M", "BN", "M",
    "DC", "X7J", "bsum", "wls1", "X1m", "GALS", "fit_one", "pooled", "GE", "MSUNE", "MPCE", "SIG_C", "SIG_G", "dvecN"))
O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))
MEAS = NX["MEAS"]; KT = np.asarray(NX["KT"], float); OKK = np.isfinite(KT) & (KT > 0)
OS1J = json.load(open(os.path.join(REB, "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")))
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
QF = {f: OS1J["footings"][f]["q_f"] for f in FEET}

# ---- isothermal sphere table (dimensionless; one ODE solve)
def _lane_emden():
    xi = np.logspace(-4, 8, 30000)
    s = solve_ivp(lambda t, y: [y[1], math.exp(-y[0]) - 2 * y[1] / t], (xi[0], xi[-1]),
                  [xi[0] ** 2 / 6, xi[0] / 3], t_eval=xi, rtol=1e-11, atol=1e-14, method="LSODA")
    return xi, s.y[1] * xi ** 2
_XI, _MU = _lane_emden()
_LX, _LB = np.log(_XI / 3), np.log(4 * _MU / 27)
def B_iso(x):
    x = np.asarray(x, float); lx = np.log(np.maximum(x, 1e-300))
    small = 4 * (x ** 3) / 3 * (1 - (3 * x) ** 2 / 10)          # series below the table
    return np.where(lx < _LX[0], small, np.exp(np.interp(lx, _LX, _LB, right=np.nan)))
SHAPES = {"burkert": B_burk, "isothermal": B_iso}

def solve_r0_shape(Mtot, Rout, Sig, Bf):
    """X38's A1 rule for any shape: compact root (r0 <= r0_pk); saturated at r0_pk if Mtot exceeds the peak."""
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(Bf(Rout / math.exp(lr))))
    lpk = float(minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded",
                                options={"xatol": 1e-10}).x)
    if lm(lpk) < math.log(Mtot): return math.exp(lpk), True
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14)), False

def sparc(foot, bg, q, shape="burkert"):
    a, b, h = bg["a"], bg["b"], bg["h"]; Bf = SHAPES[shape]
    if shape == "burkert": return sparc_os1(foot, a, b, h, q)
    rc = 3 * (100 * h * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []
    for j, g in enumerate(GALS):
        lM = a + b * (g["lMb"] - 10); M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
        Sg = SIG[foot] * (SIG_G[j] / SREF) ** q
        r0, _ = solve_r0_shape(M200, R200, Sg, Bf); gh = GE * math.pi * Sg * r0 ** 2 * Bf(g["Rm"] / r0) / g["Rm"] ** 2
        rows.append(fit_one(g, np.log10(np.maximum(g["GB"] + gh[:, None], 1e-300))))
    return pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])

def dvec_off(i, foot, hk, Msrc, offscale):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"] * offscale); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)

def cluster_vectors(foot, hk, q, shape="burkert", sig=None, offscale=1.0, mbcg=0.0):
    """Per-cluster 8-bin model vectors (OS1's grade internals) plus the C* denominator for this offscale."""
    Bf = SHAPES[shape]; sig = SIG_C if sig is None else sig; V = np.zeros((N, 8)); nsat = 0
    VC = DC[(foot, hk)] if offscale == 1.0 else np.zeros((N, 8))
    for i in ALLI:
        i = int(i); pp = prep(i, foot, hk); Sg = SIG[foot] * (sig[i] / SREF) ** q
        r0, sat = solve_r0_shape(pp["Mfair"], pp["rta"], Sg, Bf); nsat += sat
        Mh = math.pi * Sg * r0 ** 2 * Bf(np.minimum(RM, pp["rta"]) / r0)
        Msrc = pp["Mb"] + Mh + mbcg * MSUNE
        V[i] = dvecN(i, foot, hk, Msrc) if offscale == 1.0 else dvec_off(i, foot, hk, Msrc, offscale)
        if offscale != 1.0:
            g = NX["gfun"](pp["Mb"], foot); ML = g * RM ** 2 / NX["G"]
            VC[i] = dvec_off(i, foot, hk, ML, offscale)
    PREP.clear()
    return V, VC, nsat

def cells_from(foot, hk, V, VC=None):
    """OS1/SC1 grade() cell construction, verbatim arithmetic, from given vectors."""
    o = M[f"{foot}|{hk}"]; vB = bsum(V); vC = bsum(DC[(foot, hk)] if VC is None else VC); kt, ktC = vB[I], vC[I]; g = {}
    for bi, b in enumerate(BN):
        At = [float(kt[TID == t, bi].sum() / ktC[TID == t, bi].sum()) for t in range(3)]; Aa = float(kt[:, bi].sum() / ktC[:, bi].sum())
        bp = float(wls1(kt[:, bi], ktC[:, bi], X1m)[1])
        if b == "MID":
            for t in range(3): g[f"G-MID-T{t+1}"] = (o["KT_terc|MID"][t]["A"], o["KT_terc|MID"][t]["s"], At[t])
            g["G-MID-b"] = (o["KT_b|MID"]["b"], o["KT_b|MID"]["s_b"], bp)
        if b == "OUTER":
            g["G-OUT-all"] = (o["KT_all|OUTER"]["A"], o["KT_all|OUTER"]["s"], Aa)
            for t in range(3): g[f"G-OUT-T{t+1}"] = (o["KT_terc|OUTER"][t]["A"], o["KT_terc|OUTER"][t]["s"], At[t])
            g["G-OUT-b"] = (o["KT_b|OUTER"]["b"], o["KT_b|OUTER"]["s_b"], bp)
        if b == "INNER":
            g["G-IN-all"] = (o["KT_all|INNER"]["A"], o["KT_all|INNER"]["s_IN"], Aa)
    cl = f"{foot}|{hk}"; r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]
    Am = [[float(vB[T3M == t, bi].sum() / vC[T3M == t, bi].sum()) for t in range(3)] for bi in range(3)]
    Aall = [float(vB[:, bi].sum() / vC[:, bi].sum()) for bi in range(3)]
    g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"], Aall[2])
    for t in range(3): g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"], Am[2][t])
    g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"], Aall[0])
    return {k: dict(meas=v[0], s=v[1], pred=v[2], Z=(v[0] - v[2]) / v[1]) for k, v in g.items()}, vB, vC

def grade(foot, q, shape="burkert", **kw):
    out = {}; nsat = 0
    for hk in HK:
        V, VC, ns = cluster_vectors(foot, hk, q, shape, **kw); nsat += ns
        out[hk] = cells_from(foot, hk, V, VC if kw.get("offscale", 1.0) != 1.0 else None)[0]
    ok = {k: all(abs(out[hk][k]["Z"]) <= 2 for hk in HK) for k in out["h0672"]}
    return out, ok, nsat
