"""CFG945 -- the satellite hover (F2) in the collapse-gated tether (CFG941 R3theta).
Criteria: FROZEN_CRITERIA.md (618b2fc8b, committed alone before this script); AMENDMENT_A1_post_hoc.md (8943d188e).
Run (one core, one process, < 1 GB):
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg945.py              -> cfg945.out, cfg945_results.json (K + main)
    CFG945_STAGE=K ...                                          -> cfg945_K.out, cfg945_results_K.json (K only)
    CFG945_MUTATE=1 ...                                         -> cfg945_MUTATE.out, cfg945_results_MUTATE.json
MUTATE exits 1 by design when every tooth bites, 2 if a tooth fails, 3 if frozen M5 is toothless while A1's M5b and all others bite.
Exit 75 = memory guard tripped (rerun later).
kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed."""
import os, sys, io, csv, json, math, time, resource, contextlib, subprocess, re
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG945_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG945_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
OUT = []
RES = {"lane": "CFG945", "criteria": "618b2fc8b", "amendments": ["A1 8943d188e POST HOC (M5 toothless; M5b added; exit 3)"], "mutate": MUT, "stage": STAGE, "checks": {}, "tests": {}}
T0 = time.time()
RSS_LIMIT = 1.0e9


def P(s=""):
    if str(s).startswith("\n====="):
        s = str(s) + f"   [t = {time.time() - T0:.1f} s]"
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg945_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg945{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def mem_state():
    """(free + inactive GB, swap used GB) from vm_stat / sysctl (read-only)."""
    try:
        vm = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=10).stdout
        ps = int(re.search(r"page size of (\d+)", vm).group(1))
        fr = int(re.search(r"Pages free:\s+(\d+)", vm).group(1)); ina = int(re.search(r"Pages inactive:\s+(\d+)", vm).group(1))
        sw = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True, timeout=10).stdout
        m = re.search(r"used = ([\d.]+)([MG])", sw)
        used = float(m.group(1)) / (1.0 if m.group(2) == "G" else 1e3)
        return (fr + ina) * ps / 1e9, used
    except Exception:
        return None, None


FI0, SW0 = mem_state()
SWMIN = [SW0]
if FI0 is not None and FI0 < 12.0:
    print(f"MEMORY GUARD: free+inactive {FI0:.1f} GB < 12 GB at start; exit 75 (rerun later)"); sys.exit(75)


def guard(where=""):
    r = rss_val()
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)
    fi, sw = mem_state()
    if fi is None:
        return
    SWMIN[0] = min(SWMIN[0], sw) if SWMIN[0] is not None else sw
    if fi < 8.0 or (SWMIN[0] is not None and sw - SWMIN[0] > 1.0):
        P(f"MEMORY GUARD at {where}: free+inactive {fi:.1f} GB, swap {sw:.2f} GB (min {SWMIN[0]:.2f}); exit 75"); dump(); sys.exit(75)


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def is0(e):
    return sp.simplify(sp.expand(e)) == 0


# ------------------------------------------------------------------------------------------------ constants (as CFG941)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC, KPC = 6.67430e-11, 299792458.0, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e19
K_SI = 4 * math.pi * G_SI
MSUN847, KPC847 = 1.989e30, 3.0857e19
H0_SI = 67.4e3 / (1e6 * PC); RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
OB = 0.0493; OC = 5.364 * OB; RHO_C0 = OC * RHO_CRIT
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]
HOST938 = 6e10
RADII = (50.0, 100.0, 250.0)
MYR = 3.156e13


def law_g(gN, a0):
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def Rinv(x, a0):
    return 0.5 * (-x + math.sqrt(x * x + 4.0 * x * a0))


def R_num(u_, a0):
    return u_ * u_ / (a0 - u_)


def Rp_num(u_, a0):
    return u_ * (2 * a0 - u_) / (a0 - u_) ** 2


def dlaw_dgN(gN, a0):
    return 0.5 * (1.0 + (gN + 2 * a0) / np.sqrt(gN * gN + 4 * gN * a0))


_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MB_N = GN_N[-1] * R_N[-1] ** 2 / G_SI

P("CFG945  the satellite hover (F2) in the collapse-gated tether (CFG941 R3theta)" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P("  criteria 618b2fc8b; kappa = 1/2 FITTED; footings never pooled; cold energy; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e};  NGC 3198: {len(R_N)} radii;  memory at start: "
  f"free+inactive {FI0 if FI0 is None else round(FI0, 1)} GB, swap {SW0 if SW0 is None else round(SW0, 2)} GB")

# ================================================================================================ shared sympy (as CFG941)
r, G, a0s = sp.symbols("r G a_0", positive=True)
u, gN, qq = sp.symbols("u g_N q", positive=True)
KS = 4 * sp.pi * G
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / KS
Dfull = sp.simplify(KS * sp.diff(Wfull, u))
Rsym = sp.simplify(Dfull - u)                                          # R(u) = u^2/(a0 - u)


def EL_alg(Wuse, m=1, free_q=None):
    Mc = sp.Function("M_c")(r); Mb = sp.Function("M_b")(r); Mf = sp.Function("M_f")(r)
    Wf = sp.Lambda(u, Wuse)
    Lr = -G * (Mb + m * Mc + (Mf if free_q is not None else 0)) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wf(G * Mc / r ** 2)
    eq = sp.euler_equations(Lr, [Mc], [r])[0].lhs
    sub = {Mc: u * r ** 2 / G, Mb: gN * r ** 2 / G}
    if free_q is not None:
        eq = eq.subs(Mf, free_q * Mc)
    return sp.simplify(eq.subs(sub).doit())


def solve_static(Wuse, m, gNarr, a0, free_q=None):
    ex = EL_alg(Wuse, m, qq if free_q is not None else None)
    f = sp.lambdify((u, gN, a0s, G, qq), ex, "math")
    qv = 0.0 if free_q is None else free_q
    grid = a0 * np.unique(np.concatenate((np.logspace(-14, -1e-12, 900), np.linspace(1e-4, 1 - 1e-13, 3000))))
    us = []
    for gn in gNarr:
        vals = np.array([f(x, gn, a0, G_SI, qv) for x in grid])
        idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) <= 0)[0]
        if len(idx) == 0:
            us.append(float("nan")); continue
        i = idx[0]
        us.append(brentq(lambda x: f(x, gn, a0, G_SI, qv), grid[i], grid[i + 1], xtol=1e-40, rtol=1e-15, maxiter=800))
    us = np.array(us)
    return us, gNarr + m * us + qv * us, ex


def law_dev(g_tot, gNarr, a0):
    gl = law_g(gNarr, a0)
    return float(np.nanmax(np.abs(g_tot / gl - 1))), int(np.sum(~np.isfinite(g_tot)))


# ------------------------------------------------------------------------------------------------ CFG941's hover machinery (verbatim)
GL_X, GL_W = np.polynomial.legendre.leggauss(64)


def plummer_g(M, a, x):
    return G_SI * M * x / (x * x + a * a) ** 1.5


def satellite_hover(Mb_sun, a_pc, rkpc, a0, tether=True):
    """CFG941 verbatim: satellite (Plummer baryons + its isolated law phantom, truncated where u_s = u_h) at the centre of its
    medium, in the settled field of a 6e10 Msun host at r.  Delta a = a_medium(CoM) - a_stars along z (away from host)."""
    Mh = HOST938 * MSUN847; rh = rkpc * KPC847
    gbh = G_SI * Mh / rh ** 2; gh = law_g(gbh, a0); uh = gh - gbh
    M = Mb_sun * MSUN847; a = a_pc * PC
    us_of = lambda x: law_g(plummer_g(M, a, x), a0) - plummer_g(M, a, x)
    xg = np.logspace(math.log10(0.01 * a), math.log10(100 * a), 801); ug = np.array([us_of(x) for x in xg])
    above = np.where(ug >= uh)[0]
    if len(above) == 0:
        rt = a
    elif above[-1] == len(xg) - 1:
        rt = 100 * a
    else:
        j = above[-1]; rt = brentq(lambda x: us_of(x) - uh, xg[j], xg[j + 1])
    xs = np.logspace(math.log10(1e-4 * a), math.log10(rt), 4001)
    Ms = np.array([us_of(x) * x * x / G_SI for x in xs])
    dM = np.diff(Ms); xm = np.sqrt(xs[1:] * xs[:-1]); usm = np.array([us_of(x) for x in xm])
    mu = GL_X[None, :]; wq = GL_W[None, :] / 2
    wz = uh + usm[:, None] * mu; wmag = np.sqrt(uh ** 2 + usm[:, None] ** 2 + 2 * uh * usm[:, None] * mu)
    maxw = float(wmag.max() / a0)
    wm = np.minimum(wmag, a0 * (1 - 1e-12))
    Tz = (wm ** 2 / (a0 - wm)) * wz / wmag if tether else -(wz)
    Tz_avg = float(np.sum((Tz * wq).sum(axis=1) * dM) / np.sum(dM))
    a_m = -gbh + Tz_avg
    a_s = -(gbh + uh)
    gbs_a = plummer_g(M, a, a)
    efe = (gbs_a + (Rinv(gbh + gbs_a, a0) - uh)) / (gbs_a + Rinv(gbs_a, a0))
    return dict(g_host=gh, u_h=uh, g_bh=gbh, delta_a=a_m - a_s, ratio=(a_m - a_s) / gh, r_t_pc=rt / PC, max_w_over_a0=maxw,
                g_bs_at_a=gbs_a, efe_factor=efe, efe_dex=math.log10(efe))


def host_fields(rk, a0):
    Mh = HOST938 * MSUN847; rh = rk * KPC847; gbh = G_SI * Mh / rh ** 2; gh = law_g(gbh, a0)
    return Mh, rh, gbh, gh, gh - gbh


def us_fun(Mb_sun, a_pc, a0):
    M = Mb_sun * MSUN847; a = a_pc * PC
    return M, a, (lambda x: law_g(plummer_g(M, a, x), a0) - plummer_g(M, a, x))


# ------------------------------------------------------------------------------------------------ CFG874 estimator (replica, read-only data)
G874, MSUN874, PC874 = 6.674e-11, 1.989e30, 3.0857e16
A874LIT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # CFG874 hard-codes the rounded footings (CFG4_common.A0 is 2.65e-6 / 3.13e-6 higher)
nu_e = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for row in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", fn))):
        LVD[row["name"]] = row
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
DIRR = ("Leo A", "Sagittarius dIrr")
SAMPLE = []
for nm, row in LVD.items():
    if nm in EXCL and nm not in DIRR:
        continue
    s_ = fnum(row.get("vlos_sigma"))
    if s_ is None or fnum(row.get("vlos_sigma_ul")) is not None:
        continue
    rh_ = fnum(row.get("rhalf_sph_physical")) or fnum(row.get("rhalf_physical")); MV = fnum(row.get("M_V"))
    if rh_ is None or MV is None:
        continue
    dmw, dm31 = fnum(row.get("distance_gc")), fnum(row.get("distance_m31"))
    if dmw is None or dm31 is None:
        continue
    det = fnum(row.get("mass_HI")); dmin = min(dmw, dm31)
    grp = ("I" if dmin >= 300 else ("S" if det is None else "SG"))
    if nm in DIRR:
        grp = "DIRR" if dmin >= 300 else "x"
    SAMPLE.append(dict(name=nm, grp=grp, s=s_, rh=rh_, MV=MV, lHI=det, dmin=dmin, dmw=dmw, dm31=dm31))


def gas_in(lHI, r12_pc, mode):
    if lHI is None or mode == "zero":
        return 0.0
    Mg = 1.33 * 10 ** lHI
    if mode == "full":
        return Mg
    if mode == "half":
        return Mg / 2
    MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = (max(roots) if mode == "disc" else min(roots)) if roots else RHI / 2
    x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))


def build874(foot):
    """CFG874's primary rows (Ups_V = 2, gas 'disc') plus this lane's bound inputs: g_int = 3 sigma^2/r12 (CFG874's numerator),
    the nearer host's settled law field (MW 6e10 Msun at distance_gc, M31 1e11 Msun at distance_m31), and log10 nu_e(g_bar/a0)."""
    a0 = A874LIT[foot]; rows = []
    for d in SAMPLE:
        s_ = d["s"]; r12_pc = (4 / 3) * d["rh"]; r12 = r12_pc * PC874
        Ms = 2.0 * 10 ** (0.4 * (4.83 - d["MV"])); Mg = gas_in(d["lHI"], r12_pc, "disc")
        gb = G874 * (Ms / 2 + Mg) * MSUN874 / r12 ** 2
        gint = 3 * (s_ * 1e3) ** 2 / r12
        Mh = 6e10 if d["dmw"] <= d["dm31"] else 1e11
        gbh = G874 * Mh * MSUN874 / (d["dmin"] * 1e3 * PC874) ** 2
        rows.append(dict(d, Mg=Mg, Ms=Ms, gb=gb, lg=math.log10(gb), gint=gint, ghost=float(law_g(gbh, a0)),
                         dnu=math.log10(nu_e(gb / a0)), D=math.log10(gint / (gb * nu_e(gb / a0)))))
    return rows


def analyse874(rows, seed=874, nb=4000):
    """CFG874's primary analyse() (iso = I, restrict, mindist 300, seed 874, 4000 draws), literal replica."""
    I = [x for x in rows if x["grp"] == "I" and x["dmin"] >= 300.0]
    S = [x for x in rows if x["grp"] == "S"]
    lo, hi = min(x["lg"] for x in I) - 0.5, max(x["lg"] for x in I) + 0.5
    S = [x for x in S if lo <= x["lg"] <= hi]

    def fit(Ii, Si):
        X = np.array([[1.0, x["lg"] + 12.5, 1.0] for x in Ii] + [[1.0, x["lg"] + 12.5, 0.0] for x in Si])
        y = np.array([x["D"] for x in Ii + Si])
        return np.linalg.lstsq(X, y, rcond=None)[0]
    a_, b_, c_ = fit(I, S)
    rng = np.random.default_rng(seed); bc = []
    for _ in range(nb):
        Ii = [I[j] for j in rng.integers(0, len(I), len(I))]; Si = [S[j] for j in rng.integers(0, len(S), len(S))]
        bc.append(fit(Ii, Si)[2])
    return dict(c=float(c_), se_c=float(np.std(bc)), N_I=len(I), N_S=len(S)), I, S


class Boot874:
    """Vectorised replica of the same bootstrap (same draws), for c(eps) with modified residuals."""

    def __init__(self, I, S, seed=874, nb=4000):
        nI, nS = len(I), len(S)
        XI = np.array([[1.0, x["lg"] + 12.5, 1.0] for x in I]); XS = np.array([[1.0, x["lg"] + 12.5, 0.0] for x in S])
        rng = np.random.default_rng(seed); idx = []; W = np.empty((nb, nI + nS))
        for b in range(nb):
            ii = rng.integers(0, nI, nI); ss = rng.integers(0, nS, nS)
            idx.append(np.concatenate((ii, nI + ss))); W[b] = np.linalg.pinv(np.vstack((XI[ii], XS[ss])))[2]
        self.idx = np.array(idx); self.W = W; self.w0 = np.linalg.pinv(np.vstack((XI, XS)))[2]

    def c_se(self, y):
        return float(self.w0 @ y), float(np.std((self.W * y[self.idx]).sum(axis=1)))


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
k1 = {}
for foot in FOOTS:
    us_, gt_, ex_k1 = solve_static(Wfull, 1, GN_N, A0[foot])
    dv, nn = law_dev(gt_, GN_N, A0[foot]); k1[foot] = dict(max_rel_vs_law=dv, unsolved=nn)
K1 = chk("K1_NGC3198_law_CFG938_reduction", all(k1[f]["max_rel_vs_law"] < 1e-6 and k1[f]["unsolved"] == 0 for f in FOOTS),
         f"reduced EL {sp.factor(ex_k1)}; max |g/g_law - 1| canonical {k1['canonical']['max_rel_vs_law']:.2e}, alt {k1['alt']['max_rel_vs_law']:.2e} (CFG938 2.2e-16; line 1e-6)")
RES["K1"] = k1
J941 = json.load(open(os.path.join(LANES, "CFG941_self_gravity_repair", "cfg941_results.json")))["hover"]
HOV = {}
for foot in FOOTS:
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            HOV[f"{foot}|{hn}|{rk:g}"] = satellite_hover(Mb_, apc, rk, A0[foot])
k2dev = max(abs(HOV[k]["ratio"] / J941[k]["ratio"] - 1) for k in HOV)
K2 = chk("K2_CFG941_hover_ratios", k2dev < 1e-9 and len(HOV) == 18,
         f"18 ratios Delta a/g_host reproduced, max rel diff {k2dev:.1e}; range {min(v['ratio'] for v in HOV.values()):.4f} ... {max(v['ratio'] for v in HOV.values()):.4f}")
k3 = max(abs(satellite_hover(Mb_, apc, rk, A0[f], tether=False)["ratio"]) for f in FOOTS for hn, Mb_, apc in HOSTS882 for rk in RADII)
K3 = chk("K3_tether_off_universal_free_fall", k3 <= 1e-12, f"max |Delta a|/g_host with the tether off = {k3:.1e} (CFG941 M4 3.5e-16)")
J874 = json.load(open(os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874_results.json")))
ROWS874, A874, BOOT = {}, {}, {}
k4 = {}
for foot in FOOTS:
    rows = build874(foot); res, I_, S_ = analyse874(rows)
    ROWS874[foot] = (I_, S_); A874[foot] = res
    ref = J874[foot]["primary"]
    k4[foot] = dict(c=res["c"], se_c=res["se_c"], dc=abs(res["c"] - ref["c"]), dse=abs(res["se_c"] - ref["se_c"]), N_I=res["N_I"], N_S=res["N_S"])
K4 = chk("K4_CFG874_primary_reproduced", all(k4[f]["dc"] < 1e-12 and k4[f]["dse"] < 1e-12 and k4[f]["N_I"] == 11 and k4[f]["N_S"] == 54 for f in FOOTS),
         "; ".join(f"{f}: c = {k4[f]['c']:+.5f} +- {k4[f]['se_c']:.5f} (|diff| {k4[f]['dc']:.0e}, {k4[f]['dse']:.0e}; N_I {k4[f]['N_I']}, N_S {k4[f]['N_S']})" for f in FOOTS))
RES["K4"] = k4
# K5: gate at theta = 0 and theta of a uniformly translating medium
xg_, th_, ths_ = sp.symbols("x theta theta_s", positive=True)
S5 = 6 * xg_ ** 5 - 15 * xg_ ** 4 + 10 * xg_ ** 3
s_gate = 1 - S5.subs(xg_, th_ / ths_)
g0 = [sp.limit(sp.diff(s_gate, th_, n_), th_, 0, "+") for n_ in range(3)]
cc_, vv_, xx_ = sp.symbols("c v x", positive=True)
Phi_ = sp.Function("Phi")(xx_)
u0_ = 1 / sp.sqrt(1 + 2 * Phi_ / cc_ ** 2 - (1 - 2 * Phi_ / cc_ ** 2) * vv_ ** 2 / cc_ ** 2)
sqg = cc_ * sp.sqrt(1 + 2 * Phi_ / cc_ ** 2) * (1 - 2 * Phi_ / cc_ ** 2) ** sp.Rational(3, 2)
theta_wf = sp.diff(sqg * u0_ * vv_, xx_) / sqg
ep_ = sp.Symbol("epsilon", positive=True)
th_ser = sp.series(theta_wf.subs(cc_, 1 / ep_), ep_, 0, 3).removeO()
th_c0 = sp.simplify(th_ser.coeff(ep_, 0)); th_c2 = sp.simplify(th_ser.coeff(ep_, 2))
TH_COEF = sp.simplify(th_c2 / (vv_ * sp.diff(Phi_, xx_)))
K5 = chk("K5_gate_and_uniform_translation", g0 == [1, 0, 0] and th_c0 == 0 and TH_COEF.is_number,
         f"s(0+) = {g0[0]}, s'(0+) = {g0[1]}, s''(0+) = {g0[2]}; uniformly translating medium in a static weak field: theta = 0 at O(c^0), "
         f"theta = ({TH_COEF}) v dPhi/dx / c^2 + O(c^-4) (Minkowski: exactly 0)")
k6dev = max(abs(HOV[k]["efe_factor"] / J941[k]["efe_factor"] - 1) for k in HOV)
K6 = chk("K6_CFG941_EFE_factors", k6dev < 1e-9, f"18 EFE factors reproduced, max rel diff {k6dev:.1e}; dex range "
         f"{min(v['efe_dex'] for v in HOV.values()):.3f} ... {max(v['efe_dex'] for v in HOV.values()):.3f}")
K_ALL = K1 and K2 and K3 and K4 and K5 and K6
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> VOID'}")
RES["K_all"] = K_ALL
guard("K")
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)

# ================================================================================================ machinery used by MUTATE and main
for foot in FOOTS:
    BOOT[foot] = Boot874(*ROWS874[foot])
vec0 = {}
for foot in FOOTS:
    I_, S_ = ROWS874[foot]; y0 = np.array([x["D"] for x in I_ + S_])
    vec0[foot] = BOOT[foot].c_se(y0)
B0 = all(abs(vec0[f][0] - A874[f]["c"]) < 1e-12 and abs(vec0[f][1] - A874[f]["se_c"]) < 1e-12 for f in FOOTS)


def c_of_eps(foot, eps, kappa_r=1.0):
    I_, S_ = ROWS874[foot]; rows = I_ + S_
    y = np.array([x["D"] + (x["dnu"] if eps * x["ghost"] > kappa_r * x["gint"] else 0.0) for x in rows])
    nstrip = sum(1 for x in rows if eps * x["ghost"] > kappa_r * x["gint"])
    nsat = sum(1 for x in S_ if eps * x["ghost"] > kappa_r * x["gint"])
    c_, s_ = BOOT[foot].c_se(y)
    return c_, s_, nstrip, nsat


def eps_bound(foot, kappa_r):
    I_, S_ = ROWS874[foot]; rows = I_ + S_
    thr = sorted(set(kappa_r * x["gint"] / x["ghost"] for x in rows))
    steps = []
    for t in thr:
        c_, s_, ns, nss = c_of_eps(foot, t * (1 + 1e-12), kappa_r)
        steps.append((t, ns, nss, c_, s_))
        if c_ < -2 * s_:
            return t, steps
    return math.inf, steps


def h1_l2_radius(Mb_sun, a_pc, rk, a0):
    """L2 re-latch radius: outermost r in [a, 100a] where |tau_s(r)| >= |tau_h(R)|; |tau| = (sqrt 6/3)|u' - u/r| for a radial field."""
    Mh, rh, gbh, gh, uh = host_fields(rk, a0)
    M, a, us_of = us_fun(Mb_sun, a_pc, a0)
    uhost = lambda R: law_g(G_SI * Mh / R ** 2, a0) - G_SI * Mh / R ** 2

    def tmag(f, x, h=1e-5):
        return math.sqrt(6) / 3 * abs((f(x * (1 + h)) - f(x * (1 - h))) / (2 * h * x) - f(x) / x)
    tau_h = tmag(uhost, rh)
    xg = np.logspace(math.log10(a), math.log10(100 * a), 801); tg = np.array([tmag(us_of, x) for x in xg])
    above = np.where(tg >= tau_h)[0]
    if len(above) == 0:
        return a, tau_h, "a"
    if above[-1] == len(xg) - 1:
        return 100 * a, tau_h, "100a"
    j = above[-1]
    return brentq(lambda x: tmag(us_of, x) - tau_h, xg[j], xg[j + 1]), tau_h, "root"


def h1_delta_a(Mb_sun, a_pc, rk, a0, labels=True, tidal=True, tether=True):
    """H1 (per-label tether): the satellite's label-s medium feels the full host field (host baryons + host medium); its own
    tether reads chi_s only.  CoM accelerations of stars and label-s medium over the L2 domain, in the point-mass law host field
    (tidal=True) or a uniform field (tidal=False).  labels=False: the medium reads the total chi -> CFG941's machinery (hover)."""
    if not labels:
        return satellite_hover(Mb_sun, a_pc, rk, a0, tether=tether)["ratio"], {}
    Mh, rh, gbh, gh, uh = host_fields(rk, a0)
    M, a, us_of = us_fun(Mb_sun, a_pc, a0)
    rdom, tau_h, how = h1_l2_radius(Mb_sun, a_pc, rk, a0)
    xs = np.logspace(math.log10(1e-4 * a), math.log10(rdom), 4001)
    Mst = M * xs ** 3 / (xs ** 2 + a ** 2) ** 1.5
    Mph = np.array([us_of(x) * x * x / G_SI for x in xs])
    dMs, dMm = np.diff(Mst), np.diff(Mph); xm = np.sqrt(xs[1:] * xs[:-1])
    mu = GL_X[None, :]; wq = GL_W[None, :] / 2
    if tidal:
        X2 = rh ** 2 + 2 * rh * xm[:, None] * mu + xm[:, None] ** 2
        gz = -law_g(G_SI * Mh / X2, a0) * (rh + xm[:, None] * mu) / np.sqrt(X2)
    else:
        gz = -gh * np.ones((len(xm), len(GL_X)))
    gav = (gz * wq).sum(axis=1)
    a_s = float(np.sum(gav * dMs) / np.sum(dMs)); a_m = float(np.sum(gav * dMm) / np.sum(dMm))
    # tether off in H1: the medium is dust and feels the same host field -> the same CoM formula (own terms cancel)
    return abs(a_m - a_s) / gh, dict(r_dom_pc=rdom / PC, r_dom_rule=how, r_dom_over_R=rdom / rh, M_star_dom=float(Mst[-1] / MSUN847),
                                      M_med_dom=float(Mph[-1] / MSUN847), a_m=a_m, a_s=a_s, g_host=gh)


def restoring_and_dyn(Mb_sun, a_pc, rt_pc, a0, Da, gh, tether=True, T_Myr=1000.0):
    """Stars (extended Plummer cloud, mass M_b, to 100 a) vs their rigid truncated medium (isolated law phantom within r_t):
    the medium's mean pull on the offset star cloud P(d) (tabulated, linear near d = 0) and its reaction;
    external: stars -g_host, medium -g_host + Delta a (tether on) or -g_host (tether off)."""
    from scipy.interpolate import CubicSpline
    M, a, us_of = us_fun(Mb_sun, a_pc, a0); rt = rt_pc * PC
    Mmt = us_of(rt) * rt * rt / G_SI

    def Ppt(x):
        x = np.asarray(x, dtype=float)
        return np.where(x <= rt, law_g(plummer_g(M, a, x), a0) - plummer_g(M, a, x), G_SI * Mmt / np.maximum(x, 1e-300) ** 2)
    ss = np.logspace(math.log10(1e-3 * a), math.log10(100 * a), 801)
    Ms_ = M * ss ** 3 / (ss ** 2 + a ** 2) ** 1.5; dMs = np.diff(Ms_); sm = np.sqrt(ss[1:] * ss[:-1])
    mu = GL_X[None, :]; sn = np.sqrt(1 - mu ** 2); wq = GL_W[None, :] / 2
    dmax = 10 * max(rt, 100 * a)
    dtab = np.concatenate(([0.0], np.logspace(math.log10(1e-4 * min(a, rt)), math.log10(dmax), 300)))
    Ptab = []
    for dd in dtab:
        Xz = dd + sm[:, None] * mu; Xp = sm[:, None] * sn; Xn = np.sqrt(Xz ** 2 + Xp ** 2)
        Fz = -(Ppt(Xn) * Xz / Xn * wq).sum(axis=1)
        Ptab.append(float(-np.sum(Fz * dMs) / np.sum(dMs)))
    Ptab = np.array(Ptab); Ptab[0] = 0.0
    spl = CubicSpline(dtab, Ptab)

    def Pd(d):
        d = abs(d)
        return float(spl(d)) if d <= dmax else Ptab[-1] * (dmax / d) ** 2
    Pmax = float(Ptab.max()) * (1 + M / Mmt)
    L = rt; tu = MYR; sc = tu * tu / L
    dda = Da if tether else 0.0

    def rhs(t, y):
        zs, vs, zm, vm = y; d = (zs - zm) * L
        p = Pd(d) * sc; sg = 1.0 if d > 0 else (-1.0 if d < 0 else 0.0)
        return [vs, -gh * sc - sg * p, vm, (-gh + dda) * sc + sg * (M / Mmt) * p]
    tev = np.linspace(0.0, T_Myr, 4001)
    sol = solve_ivp(rhs, (0.0, T_Myr), [0.0, 0.0, 0.0, 0.0], method="DOP853", rtol=1e-9, atol=1e-12, max_step=0.5, t_eval=tev)
    dd_ = np.abs(sol.y[0] - sol.y[2])
    sep_idx = np.where(dd_ > 1.0)[0]
    vcm = (M * sol.y[1][-1] + Mmt * sol.y[3][-1]) / (M + Mmt)
    acm = vcm / sc / sol.t[-1]
    return dict(M_med_t=Mmt / MSUN847, f_m=Mmt / (M + Mmt), P_max_over_Da=Pmax / Da if Da > 0 else math.inf, bound=bool(Pmax > Da),
                max_sep_over_rt=float(dd_.max()), final_sep_over_rt=float(dd_[-1]), t_sep_Myr=float(sol.t[sep_idx[0]]) if len(sep_idx) else None,
                a_cm_over_g=float(acm / (-gh)), eta_composite=float(1 - acm / (-gh)), nfev=int(sol.nfev), ok=bool(sol.success))


def two_label_disp(r2, U, Aminus1=0.0):
    """Two co-located labels (units K = rho_1 = L* = 1): [(w - kU)^2 - O2^2][w^2 - O1^2] = r2;
    O_q^2 = rho_q (A_q - 1) + rho_q k^2/2.  Returns max Im w over k and the k-independent Jeans bound sqrt(1 + r2)."""
    mx = 0.0
    for k in np.logspace(-2, 3, 400):
        O1 = 1.0 * Aminus1 + 0.5 * k * k; O2 = r2 * Aminus1 + 0.5 * r2 * k * k
        # expand: (w^2 - 2kU w + k^2U^2 - O2)(w^2 - O1) - r2 = 0
        p1 = np.array([1.0, -2 * k * U, k * k * U * U - O2]); p2 = np.array([1.0, 0.0, -O1])
        poly = np.polymul(p1, p2); poly[-1] -= r2
        mx = max(mx, float(np.max(np.roots(poly).imag)))
    return mx, math.sqrt(1 + r2)


# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    m1 = max(abs(h1_delta_a(Mb_, apc, rk, A0[f], labels=False)[0] / J941[f"{f}|{hn}|{rk:g}"]["ratio"] - 1)
             for f in FOOTS for hn, Mb_, apc in HOSTS882 for rk in RADII)
    m1b = chk("M1_labels_removed_hover_returns", m1 < 1e-9, f"H1 with the satellite medium reading the total chi: ratios = CFG941's to {m1:.1e}")
    m2a = max(abs(satellite_hover(Mb_, apc, rk, A0[f], tether=False)["ratio"]) for f in FOOTS for hn, Mb_, apc in HOSTS882 for rk in RADII)
    m2b_ = max(h1_delta_a(Mb_, apc, rk, A0[f], tidal=False)[0] for f in FOOTS for hn, Mb_, apc in HOSTS882 for rk in RADII)
    m2b = chk("M2_tether_off_universal_free_fall", m2a <= 1e-12 and m2b_ <= 1e-12,
              f"P0/R3theta path tether off max {m2a:.1e}; H1 path in a uniform host field max {m2b_:.1e} (line 1e-12)")
    m3 = {}
    for foot in FOOTS:
        a0 = A0[foot]; gl = law_g(GN_N, a0); aR = dlaw_dgN(GN_N, a0) * (gl - GN_N)
        m3[foot] = (float(np.max(np.abs((gl - aR) / gl - 1))), float(np.max(np.abs(gl / gl - 1))))
    m3b = chk("M3_H2_reaction_tooth", all(m3[f][0] > 1e-6 and m3[f][1] < 1e-6 for f in FOOTS),
              "; ".join(f"{f}: reaction on dev {m3[f][0]:.3f}, off {m3[f][1]:.1e}" for f in FOOTS))
    m4 = {}
    for foot in FOOTS:
        a0 = A0[foot]; v = ((a0 - GN_N) + np.sqrt((a0 - GN_N) ** 2 + 8 * GN_N * a0)) / 4
        m4[foot] = law_dev(GN_N + 2 * v, GN_N, a0)[0]
    m4b = chk("M4_two_labels_break_law", all(m4[f] > 1e-6 for f in FOOTS), "; ".join(f"{f}: two equal labels dev {m4[f]:.3f}" for f in FOOTS))
    m5 = {}
    for foot in FOOTS:
        c0_, s0_, _, _ = c_of_eps(foot, 0.0); cB, sB, nB, _ = c_of_eps(foot, 100.0)
        m5[foot] = dict(c0=c0_, se0=s0_, c100=cB, se100=sB, n100=nB)
    m5b = chk("M5_bound_statistic_tooth", all(abs(m5[f]["c0"] - A874[f]["c"]) < 1e-12 and m5[f]["c100"] < -2 * m5[f]["se100"] for f in FOOTS),
              "; ".join(f"{f}: eps 0 c {m5[f]['c0']:+.4f}; eps 100 ({m5[f]['n100']} stripped) c {m5[f]['c100']:+.3f} +- {m5[f]['se100']:.3f}" for f in FOOTS)
              + (" -- TOOTHLESS as frozen (flagged, A1): stripping every dwarf is absorbed by the matched-g_bar regression" if not all(m5[f]["c100"] < -2 * m5[f]["se100"] for f in FOOTS) else ""))
    m5i = {}
    for foot in FOOTS:                                                   # A1 (post hoc): strip every matched satellite, no isolated dwarf
        I_, S_ = ROWS874[foot]
        y = np.array([x["D"] for x in I_] + [x["D"] + x["dnu"] for x in S_]); ci, si = BOOT[foot].c_se(y)
        m5i[foot] = dict(c=ci, se=si)
    m5bb = chk("M5b_A1_satellite_only_stripping_tooth", all(m5i[f]["c"] < -2 * m5i[f]["se"] for f in FOOTS),
               "(post hoc, A1) " + "; ".join(f"{f}: all 54 matched satellites stripped, isolated untouched: c {m5i[f]['c']:+.3f} +- {m5i[f]['se']:.3f} ({m5i[f]['c'] / m5i[f]['se']:+.1f} se)" for f in FOOTS))
    m5.update({f"{f}_A1_inject": m5i[f] for f in FOOTS})
    m6 = []
    for foot in FOOTS:
        for hn, Mb_, apc in HOSTS882:
            for rk in RADII:
                hv = HOV[f"{foot}|{hn}|{rk:g}"]
                dy = restoring_and_dyn(Mb_, apc, hv["r_t_pc"], A0[foot], hv["delta_a"], hv["g_host"], tether=False, T_Myr=1000.0)
                m6.append((dy["max_sep_over_rt"], abs(dy["a_cm_over_g"] - 1)))
    m6b = chk("M6_dynamics_tether_off_comove", max(x[0] for x in m6) < 1e-6 and max(x[1] for x in m6) < 1e-9,
              f"max separation/r_t {max(x[0] for x in m6):.1e}, max |a_cm/g_host - 1| {max(x[1] for x in m6):.1e} over 1 Gyr")
    RES["MUTATE"] = dict(M1=m1, M2=(m2a, m2b_), M3=m3, M4=m4, M5=m5, M6_max=(max(x[0] for x in m6), max(x[1] for x in m6)))
    others = m1b and m2b and m3b and m4b and m6b
    allbite = others and m5b
    flagged = others and (not m5b) and m5bb
    P(f"\n  MUTATE: " + ("ALL TEETH BITE (exit 1 by design)" if allbite else ("frozen M5 TOOTHLESS (flagged); A1 replacement M5b and every other tooth BITE (exit 3)" if flagged else "A TOOTH FAILED TO BITE (exit 2)")))
    RES["MUTATE"]["exit_rule"] = "1 all bite; 2 a tooth fails; 3 frozen M5 toothless with A1 replacement M5b biting (A1)"
    dump(); sys.exit(1 if allbite else (3 if flagged else 2))

# ================================================================================================ MAIN
TESTS = {}


def put(cand, key, ok, detail):
    TESTS.setdefault(cand, {})[key] = dict(pass_=ok if ok is None else bool(ok), detail=str(detail))
    tag = "PASS" if ok else ("FAIL" if ok is not None else "N/A ")
    P(f"   ({key}) {tag}: {detail}")


chk("B0_vectorised_bootstrap_equals_literal", B0, "; ".join(f"{f}: c {vec0[f][0]:+.6f} se {vec0[f][1]:.6f}" for f in FOOTS))

# ---------------------------------------------------------------- Q1: static nested hover lemma in R3theta
P("\n==================== Q1: the hover lemma in the gated theory (satellite nested in the host's collapsed region) ====================")
gbh_, uh_, us_ = sp.symbols("g_bh u_h u_s", positive=True)
s1 = sp.Symbol("s")
f_med_host = -gbh_ - uh_ + s1 * Dfull.subs(u, uh_)
f_star_host = -gbh_ - uh_
law_sub = {gbh_: Rsym.subs(u, uh_)}
Q1a = chk("Q1a_settled_gate_gives_hover", is0(f_med_host.subs(s1, 1).subs(law_sub)) and is0((f_med_host - f_star_host).subs(s1, 1).subs(law_sub) - (Rsym.subs(u, uh_) + uh_)),
          "theta = 0 (static or uniformly translating, K5) -> s = 1: host part of the force on satellite medium = -g_bh + R(u_h) = 0 on the "
          "host's law; stars feel -(g_bh + u_h); leading Delta a = u_h + R(u_h) = g_host. The nested satellite gate cannot differ from the host's (both theta = 0)")
P(f"  K2 reproduced: Delta a/g_host = {min(v['ratio'] for v in HOV.values()):.4f} ... {max(v['ratio'] for v in HOV.values()):.4f} (identical to CFG941: R3theta's settled sector is CFG938's)")
th_num = max(abs(float(TH_COEF)) * math.sqrt(HOV[k]["g_host"] * float(k.split('|')[2]) * KPC847) * HOV[k]["g_host"] / C_SI ** 2 for k in HOV)
P(f"  weak-field theta of a translating satellite medium <= |coef| v g/c^2 = {th_num:.1e} s^-1 vs theta_s = H0 = {H0_SI:.2e} s^-1 (ratio {th_num / H0_SI:.1e})")
RES["Q1"] = dict(hover_min=min(v["ratio"] for v in HOV.values()), hover_max=max(v["ratio"] for v in HOV.values()), theta_weak_max=th_num)

# ---------------------------------------------------------------- Q2: Theorem S
P("\n==================== Q2: Theorem S (same point) ====================")
Gh, F0, F1, vv, cst, dl = sp.symbols("G_h F_0 F_1 v c_star delta")
f_med = -Gh + F0 + F1 * vv / cst + dl
f_star = -Gh
dA = sp.simplify((f_med - f_star).subs(F0, Gh))
xq = sp.Symbol("x", real=True); aq_ = sp.Symbol("alpha", positive=True); Kq = sp.Symbol("K", positive=True)
chi_ex = -sp.exp(-xq ** 2)                                            # an example own-field profile (decaying gradient)
selfF = sp.integrate((sp.diff(chi_ex, xq, 2) / Kq) * aq_ * sp.diff(chi_ex, xq), (xq, -sp.oo, sp.oo))
Q2 = chk("Q2_theorem_S", is0(dA - (Gh + F1 * vv / cst + dl)) and selfF == 0,
         "force on any element = -grad Phi + F(x, v; own-flow gate scalars); host equilibrium F(x, 0) = grad Phi_h  =>  Delta a = g_host + F1 v/c* + delta_cross; "
         "the satellite's own linear self-term has zero CoM integral (example: int rho alpha chi' dx = 0). At leading order in (satellite field)/(host field) the hover "
         "is exact for every label-free F; the nonlinear cross terms delta_cross are F-specific and are computed per candidate (P0 raises eps above 1, QUMOND-type "
         "anchoring lowers it). Escapes: (E1) membership label, (E2) stream-specific (non-cold) support, (E3) O(1) velocity dependence, (E4) non-stationary satellite medium")
RES["Q2"] = dict(delta_a=str(dA))

# ---------------------------------------------------------------- Q3: dynamics estimates
P("\n==================== Q3: gate crossing time and the separation correction (estimates) ====================")
Q3 = {}
P(f"  {'case':18s} {'Da/g':>6s} {'t_gate Myr':>10s} {'regime':>7s} {'P_max/Da':>8s} {'bound':>5s} {'f_m':>6s} {'eta=f_m*eps':>11s} {'t_sep Myr (dyn)':>15s}")
for k, hv in HOV.items():
    foot, hn, rk = k.split("|"); a0 = A0[foot]; Mb_, apc = {h[0]: (h[1], h[2]) for h in HOSTS882}[hn]
    M, a, us_of = us_fun(Mb_, apc, a0)
    rr = np.linspace(0.01 * a, 5 * a, 2000)
    drho = np.abs(-5 * rr / a ** 2 * (3 * M / (4 * math.pi * a ** 3)) * (1 + rr ** 2 / a ** 2) ** -3.5)
    dmax = float(drho.max()); Da = hv["delta_a"]
    hh = 1e-5 * a
    rho_c = ((a + hh) ** 2 * us_of(a + hh) - (a - hh) ** 2 * us_of(a - hh)) / (2 * hh) / (K_SI * a * a)
    w2 = K_SI * rho_c * Rp_num(min(hv["u_h"] + us_of(a), 0.999 * a0), a0)
    t_free = (6 * H0_SI / (K_SI * dmax * Da)) ** (1 / 3)
    t_qs = H0_SI * w2 / (K_SI * dmax * Da)
    regime = "free" if math.sqrt(w2) * t_free < 1 else "q-stat"
    tg = t_free if regime == "free" else t_qs
    dy = restoring_and_dyn(Mb_, apc, hv["r_t_pc"], a0, Da, hv["g_host"])
    Q3[k] = dict(t_gate_Myr=tg / MYR, regime=regime, t_free_Myr=t_free / MYR, t_qs_Myr=t_qs / MYR, **dy)
    P(f"  {k:18s} {hv['ratio']:6.3f} {tg / MYR:10.3g} {regime:>7s} {dy['P_max_over_Da']:8.3f} {str(dy['bound']):>5s} {dy['f_m']:6.3f} "
      f"{dy['f_m'] * hv['ratio']:11.3f} {str(round(dy['t_sep_Myr'], 1)) if dy['t_sep_Myr'] is not None else 'never (1 Gyr)':>15s}")
nb_bound = sum(1 for v in Q3.values() if v["bound"])
eta_all = [v["eta_composite"] for v in Q3.values()]
P(f"  stars stay bound to their medium (medium's pull included) in {nb_bound}/18 cases; the composite falls at a_cm/g_host = 1 - f_m*eps "
  f"(momentum), eta = {min(eta_all):.3f} ... {max(eta_all):.3f}; gate crossing in {min(v['t_gate_Myr'] for v in Q3.values()):.2g} ... "
  f"{max(v['t_gate_Myr'] for v in Q3.values()):.2g} Myr (inside R3theta's ghost band)")
RES["Q3"] = Q3
guard("Q3")

# ---------------------------------------------------------------- BOUND eps_B and delta_c (from the record's numbers)
P("\n==================== the bound on |Delta a|/g_host from CFG874 (stripping model) and delta_c ====================")
BND = {}
for foot in FOOTS:
    eB1, st1 = eps_bound(foot, 1.0); eB2, st2 = eps_bound(foot, 2.0)
    hv_max = max(HOV[k]["ratio"] for k in HOV if k.startswith(foot)); hv_min = min(HOV[k]["ratio"] for k in HOV if k.startswith(foot))
    c_h1, s_h1, n_h1, ns_h1 = c_of_eps(foot, hv_min, 1.0); c_h2, s_h2, n_h2, ns_h2 = c_of_eps(foot, hv_max, 1.0)
    c_h2k, s_h2k, n_h2k, ns_h2k = c_of_eps(foot, hv_max, 2.0)
    I_, S_ = ROWS874[foot]
    ratios_sat = sorted(x["gint"] / x["ghost"] for x in S_)
    delta_c = A874[foot]["c"] + 2 * A874[foot]["se_c"]
    line_b = eB1 if eB1 < 1.11 else 0.01
    BND[foot] = dict(eps_B_k1=eB1, eps_B_k2=eB2, line_b=line_b, delta_c=delta_c, c_at_hover_min=(c_h1, s_h1, n_h1, ns_h1), c_at_hover_max=(c_h2, s_h2, n_h2, ns_h2),
                     c_at_hover_max_k2=(c_h2k, s_h2k, n_h2k, ns_h2k), gint_over_ghost_sat_min=ratios_sat[0], gint_over_ghost_sat_median=ratios_sat[len(ratios_sat) // 2],
                     steps_k1=st1[:12], n_steps_k1=len(st1))
    P(f"  [{foot}] satellites' g_int/g_host: min {ratios_sat[0]:.3f}, median {ratios_sat[len(ratios_sat) // 2]:.2f} (N_S {len(S_)}); "
      f"eps_B (kappa_r 1) = {eB1:.4g}, (kappa_r 2) = {eB2:.4g}; graded line for (b) = {line_b:.4g}")
    P(f"     under the hover (eps {hv_min:.3f} / {hv_max:.3f}, kappa_r 1): {n_h1} / {n_h2} dwarfs stripped ({ns_h1} / {ns_h2} matched satellites); "
      f"CFG874 c would read {c_h1:+.3f} +- {s_h1:.3f} / {c_h2:+.3f} +- {s_h2:.3f} ({c_h2 / s_h2:+.1f} se); kappa_r 2: {c_h2k:+.3f} +- {s_h2k:.3f}")
    P(f"     delta_c = c + 2 se_c = {delta_c:+.4f} dex (largest satellite-specific deficit CFG874 allows at 2 sigma)")
x873 = json.load(open(os.path.join(LANES, "CFG873_field_dwarf_environment", "cfg873_results.json")))
x875 = json.load(open(os.path.join(LANES, "CFG875_host_distance_trend", "cfg875_results.json")))
x860 = json.load(open(os.path.join(LANES, "CFG860_stripping_vs_isolated_dwarfs", "cfg860_results.json")))["variants"]["alt|base"]
cross = {"CFG873 D + 2 se (canonical)": x873["canonical"]["primary"]["D"] + 2 * x873["canonical"]["primary"]["se_D"],
         "CFG873 D + 2 se (alt)": x873["alt"]["primary"]["D"] + 2 * x873["alt"]["primary"]["se_D"],
         "CFG860 c0 + 2 se (canonical, README -0.150 +- 0.122)": -0.150 + 2 * 0.122, "CFG860 cG + 2 se (canonical, README -0.064 +- 0.093)": -0.064 + 2 * 0.093,
         "CFG860 c0 + 2 se (alt, JSON)": x860["c0"] + 2 * x860["s0"], "CFG860 cG + 2 se (alt, JSON)": x860["cG"] + 2 * x860["sG"],
         "CFG875 k + 2 se (canonical, dex per dex toward the host)": x875["canonical"]["primary"]["k"] + 2 * x875["canonical"]["primary"]["se_k"],
         "CFG875 k + 2 se (alt)": x875["alt"]["primary"]["k"] + 2 * x875["alt"]["primary"]["se_k"]}
for kx_, v in cross.items():
    P(f"     cross-check (reported): {kx_} = {v:+.3f}")
BND["cross_checks"] = cross
RES["bound"] = BND
guard("bound")

def btfr_numeric(a0, y=1e-14):
    rr_ = math.sqrt(G_SI * MB_N / (y * a0)); _, gt, _ = solve_static(Wfull, 1, np.array([y * a0]), a0)
    return float((gt[0] * rr_) ** 2 / (G_SI * MB_N * a0))


BTFR = {f: btfr_numeric(A0[f]) for f in FOOTS}
lim_btfr = sp.limit(((yy_ := sp.Symbol("yb", positive=True)) + sp.sqrt(yy_ ** 2 + 4 * yy_)) ** 2 / 4 / yy_, yy_, 0, "+")
BT_OK = all(abs(BTFR[f] - 1) < 1e-6 for f in FOOTS) and lim_btfr == 1
P(f"  deep BTFR (single-label / P0): sympy limit {lim_btfr}; numeric y = 1e-14: {BTFR['canonical'] - 1:+.2e} / {BTFR['alt'] - 1:+.2e}")
RES["btfr"] = dict(numeric=BTFR, limit=str(lim_btfr))

# ---------------------------------------------------------------- P0 / R3theta reference row (the unresolved gated theory)
P("\n==================== P0 = R3theta settled sector (unresolved reference) ====================")
hov_r = {f: [HOV[k]["ratio"] for k in HOV if k.startswith(f)] for f in FOOTS}
hov_e = {f: [abs(HOV[k]["efe_dex"]) for k in HOV if k.startswith(f)] for f in FOOTS}
put("P0", "a", K1 and BT_OK, f"K1 {k1['canonical']['max_rel_vs_law']:.1e} / {k1['alt']['max_rel_vs_law']:.1e}")
put("P0", "b", all(max(hov_r[f]) <= BND[f]["line_b"] for f in FOOTS),
    "; ".join(f"{f}: eps {min(hov_r[f]):.3f}-{max(hov_r[f]):.3f} vs line {BND[f]['line_b']:.3g}" for f in FOOTS))
put("P0", "c", all(max(hov_e[f]) <= BND[f]["delta_c"] for f in FOOTS),
    "; ".join(f"{f}: |EFE| {min(hov_e[f]):.3f}-{max(hov_e[f]):.3f} dex vs delta_c {BND[f]['delta_c']:.3f}" for f in FOOTS))
put("P0", "d", True, "CFG938 conditions (gamma > 0, rho c^2 > D u/K; settled min omega^2 >= 0); R3theta's transition-band ghost inherited (CFG944)")

# ---------------------------------------------------------------- H1
P("\n==================== H1: domain-local (per-label) tether ====================")
ax_, bx_ = sp.symbols("a b", real=True)
Wcross = Wfull.subs(u, ax_ + bx_) - Wfull.subs(u, ax_) - Wfull.subs(u, bx_)
cross_q = sp.simplify(sp.diff(Wcross, ax_, bx_).subs({ax_: 0, bx_: 0}))      # mixed derivative at the origin = W''(0)
H1nest = chk("H1_nesting_superposition", is0(cross_q - 1 / KS),
             "D^2 chi = K m n is linear: chi_total = sum_q chi_q (nesting compatible); P0 and H1 differ only in W: "
             f"W(|a+b|) - W(|a|) - W(|b|) = a.b x {cross_q} + O(3) (= the cancelled mutual gravity between label a and label b)")
f_lab = (-gbh_ - uh_) + (-sp.Symbol("g_bs") - us_ + Dfull.subs(u, us_))
f_star_lab = (-gbh_ - uh_) + (-sp.Symbol("g_bs") - us_)
H1force = chk("H1_force_uniform_field", is0((f_lab - f_star_lab) - Rsym.subs(u, us_) - us_) ,
              "label-s medium: host part -(g_bh + u_h) = the stars' host part exactly (no host chi in its tether); the remaining "
              "terms are the satellite's own (isolated) equilibrium -> Delta a = 0 in a uniform host field; EFE = 0 in the falling frame")
kx, xx, Bb, C1, C2 = sp.symbols("k x B C_1 C_2", positive=True)
c2g = sp.Symbol("c_2", real=True)
PhiM = -KS * (Bb + C1 + C2) * sp.cos(kx * xx) / kx ** 2
Lm = -sp.diff(PhiM, xx) ** 2 / (2 * KS) - (Bb + C1 + C2) * sp.cos(kx * xx) * PhiM \
     - c2g * ((KS * C1 * sp.sin(kx * xx) / kx) ** 2 + (KS * C2 * sp.sin(kx * xx) / kx) ** 2) / (2 * KS)
Lavg = sp.simplify(sp.integrate(Lm, (xx, 0, 2 * sp.pi / kx)) * kx / (2 * sp.pi))
cr12 = sp.simplify(sp.diff(Lavg, C1, C2))
H1mode = chk("H1_mode_average_labels", is0(Lavg - KS / (4 * kx ** 2) * ((Bb + C1 + C2) ** 2 - c2g * (C1 ** 2 + C2 ** 2))) and is0(cr12 - KS / (2 * kx ** 2)),
             f"<L> = (K/4k^2)[(B + C1 + C2)^2 - c2 (C1^2 + C2^2)]; d2<L>/dC1dC2 = {cr12} = 2 pi G/k^2 for every c2: different labels "
             "gravitate Newtonianly; each label keeps D-T's c2 = 1 cancellation of its own self-gravity")
# two-label reduced EL
M1f, M2f, Mbf = sp.Function("M_1")(r), sp.Function("M_2")(r), sp.Function("M_b")(r)
u1, u2 = sp.symbols("u_1 u_2", positive=True)
L2l = -G * (Mbf + M1f + M2f) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * (sp.Lambda(u, Wfull)(G * M1f / r ** 2) + sp.Lambda(u, Wfull)(G * M2f / r ** 2))
el2 = sp.euler_equations(L2l, [M1f, M2f], [r])
el2a = sp.simplify(el2[0].lhs.subs({M1f: u1 * r ** 2 / G, M2f: u2 * r ** 2 / G, Mbf: gN * r ** 2 / G}).doit())
vv2 = sp.Symbol("v", positive=True)
H1two = chk("H1_two_label_equilibrium", is0(sp.numer(sp.together(el2a.subs({u1: vv2, u2: vv2}))).subs(gN, Rsym.subs(u, vv2) - vv2)),
            f"two labels in one galaxy: EL_1 = {sp.factor(el2a)} -> R(u_1) = g_N + u_2; equal split R(v) = g_N + v, g = g_N + 2v")
yy = sp.Symbol("y", positive=True)
v_y = ((1 - yy) + sp.sqrt((1 - yy) ** 2 + 8 * yy)) / 4
floor2 = sp.limit(yy + 2 * v_y, yy, 0, "+")
P(f"  two equal labels: deep limit g -> {floor2} a0 (an acceleration floor; BTFR limit infinite)")
h1a = {}
for foot in FOOTS:
    a0 = A0[foot]; v = ((a0 - GN_N) + np.sqrt((a0 - GN_N) ** 2 + 8 * GN_N * a0)) / 4
    dv2 = law_dev(GN_N + 2 * v, GN_N, a0)[0]
    deb = {}
    for qv in (1e-6, 1e-3, 0.1, 1.0):
        _, gtq, _ = solve_static(Wfull, 1, GN_N, a0, free_q=qv); deb[qv] = law_dev(gtq, GN_N, a0)[0]
    h1a[foot] = dict(single_label=k1[foot]["max_rel_vs_law"], two_labels=dv2, debris=deb)
P("  " + "; ".join(f"{f}: single label {h1a[f]['single_label']:.1e}, two equal labels {h1a[f]['two_labels']:.3f}, free debris q = "
                   + ", ".join(f"{q:g}: {d:.2e}" for q, d in h1a[f]["debris"].items()) for f in FOOTS))
put("H1", "a", K1 and BT_OK, f"single-label galaxy = P0: {k1['canonical']['max_rel_vs_law']:.1e} / {k1['alt']['max_rel_vs_law']:.1e} (BTFR as P0). "
    f"Cost: two equal labels miss the law by {h1a['canonical']['two_labels']:.2f} / {h1a['alt']['two_labels']:.2f} (floor g -> a0); "
    f"re-latch-failed debris at q = 1e-6 already gives {h1a['canonical']['debris'][1e-6]:.1e} (line 1e-6): every settled galaxy must be single-label")
h1b = {}
for foot in FOOTS:
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            e_, info = h1_delta_a(Mb_, apc, rk, A0[foot])
            M, a, us_of = us_fun(Mb_, apc, A0[foot])
            xg = np.logspace(math.log10(0.01 * a), math.log10(100 * a), 801)
            l1_relatch = max(us_of(x) for x in xg) < host_fields(rk, A0[foot])[4]
            h1b[f"{foot}|{hn}|{rk:g}"] = dict(eps=e_, L1_whole_satellite_relatched=bool(l1_relatch), **info)
P(f"  {'case':18s} {'eps (tides)':>11s} {'r_dom pc':>9s} {'rule':>5s} {'r_dom/R':>8s} {'L1 relatch?':>11s}")
for k, v in h1b.items():
    P(f"  {k:18s} {v['eps']:11.2e} {v['r_dom_pc']:9.0f} {v['r_dom_rule']:>5s} {v['r_dom_over_R']:8.4f} {str(v['L1_whole_satellite_relatched']):>11s}")
h1e = {f: [v["eps"] for k, v in h1b.items() if k.startswith(f)] for f in FOOTS}
nL1 = sum(1 for v in h1b.values() if v["L1_whole_satellite_relatched"])
put("H1", "b", all(max(h1e[f]) <= BND[f]["line_b"] for f in FOOTS),
    "; ".join(f"{f}: eps {min(h1e[f]):.1e}-{max(h1e[f]):.1e} (tidal residual only; uniform part exactly 0) vs line {BND[f]['line_b']:.3g}; "
              f"CFG941 0.01 line {'met' if max(h1e[f]) <= 0.01 else 'NOT met'}" for f in FOOTS)
    + f". Rule L1 (field dominance) would re-latch the whole satellite to the host in {nL1}/18 cases (hover restored there): L2 required")
h1c = {}
for foot in FOOTS:
    a0 = A0[foot]
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            Mh, rh, gbh, gh, uh = host_fields(rk, a0)
            M, a, us_of = us_fun(Mb_, apc, a0)
            gbs = plummer_g(M, a, a); uiso = Rinv(gbs, a0)
            unif = (gbs + Rinv(gbs, a0)) / (gbs + uiso)                         # uniform field: R(u') = g_bs exactly
            dtid = law_g(G_SI * Mh / (rh - a) ** 2, a0) - gh
            arg = gbs - dtid
            tid = math.log10((gbs + Rinv(arg, a0)) / (gbs + uiso)) if arg > 0 else float("-inf")
            h1c[f"{foot}|{hn}|{rk:g}"] = dict(uniform_dex=math.log10(unif), tidal_dex=tid, tidal_over_gbs=dtid / gbs)
h1cu = max(abs(v["uniform_dex"]) for v in h1c.values()); h1ct = [v["tidal_dex"] for v in h1c.values()]
put("H1", "c", all(max(abs(v["uniform_dex"]) for k, v in h1c.items() if k.startswith(f)) <= BND[f]["delta_c"] for f in FOOTS),
    f"uniform-field EFE = {h1cu:.1e} dex (exact 0) vs delta_c {BND['canonical']['delta_c']:.3f} / {BND['alt']['delta_c']:.3f}; tidal term at the scale radius "
    f"(reported, present in any metric theory): {min(h1ct):.4f} ... {max(h1ct):.4f} dex")
d2 = {}
for r2 in (0.1, 1.0, 10.0):
    for U in (0.0, 0.1, 1.0, 10.0):
        for Am in (0.0, 1.0):
            mx, jb = two_label_disp(r2, U, Am); d2[f"r2={r2:g}|U={U:g}|A-1={Am:g}"] = dict(max_im=mx, jeans=jb)
d2ok = all(v["max_im"] <= v["jeans"] * (1 + 1e-9) for v in d2.values())
put("H1", "d", d2ok, f"per label: CFG938's conditions (gamma > 0; rho c^2 > D u/K, margins 5.9e4-2.5e8). Two co-located labels with relative speed U "
    f"(two-stream, mutual gravity uncancelled): max Im omega / sqrt(K(rho1 + rho2)) = {max(v['max_im'] / v['jeans'] for v in d2.values()):.3f} <= 1, "
    "k-independent (bounded Jeans-type; stiffness stabilises large k). Energy-momentum: diffeomorphism-invariant action for fixed labels; conserved only "
    "between label changes (cost). R3theta ghost inherited")
put("H1", "e", None, "different labels gravitate Newtonianly (H1_mode_average_labels): tethered-tethered gravity between distinct collapsed objects is "
    "RESTORED; within one label D-T still forces c2 = 1 (no self-gravity of a settled domain's medium); linear regime: gate off, dust, n = 1 (R3theta)")
RES["H1"] = dict(a=h1a, b=h1b, c=h1c, d=d2, floor_two_labels=str(floor2))
guard("H1")

# ---------------------------------------------------------------- H2
P("\n==================== H2: tether anchored to baryons ====================")
gNs_ = sp.Symbol("g_N", positive=True)
lawS = (gNs_ + sp.sqrt(gNs_ ** 2 + 4 * gNs_ * a0s)) / 2
aR = sp.diff(lawS, gNs_) * (lawS - gNs_)
limR = sp.limit(aR, gNs_, 0, "+")
H2lem = chk("H2_anchor_reaction_lemma", sp.simplify(limR - a0s / 2) == 0,
            "U_int = int M_c(r) nu(g_N) g_N dr (spherical, from -int rho_c psi d^3x); moving baryon mass outward changes U by -dm M_c G/r^2 d(nu g_N)/dg_N -> "
            f"extra OUTWARD acceleration on baryons a_R = (dg/dg_N) g_c; deep limit a_R -> {limR}")
# numeric finite-difference check of the reaction on a toy (point baryons of NGC 3198's mass + a test shell dm at r0):
# U(r0 + h) - U(r0 - h) = int_{r0-h}^{r0+h} M_c(r) [law(g_N) - law(g_N + G dm/r^2)] dr exactly; f = -dU/(2 h dm), outward positive
from scipy.integrate import quad
a0t = A0["canonical"]; Mbt = MB_N; r0 = 20 * KPC; dm = 1e-6 * Mbt; hfd = 0.2 * KPC
Mc_t = lambda x: (law_g(G_SI * Mbt / x ** 2, a0t) - G_SI * Mbt / x ** 2) * x * x / G_SI
dU = quad(lambda x: Mc_t(x) * (law_g(G_SI * Mbt / x ** 2, a0t) - law_g(G_SI * (Mbt + dm) / x ** 2, a0t)), r0 - hfd, r0 + hfd, epsabs=0, epsrel=1e-12)[0]
f_fd = -dU / (2 * hfd * dm)
f_an = Mc_t(r0) * G_SI / r0 ** 2 * float(dlaw_dgN(G_SI * Mbt / r0 ** 2, a0t))
H2fd = chk("H2_reaction_finite_difference", abs(f_fd / f_an - 1) < 1e-4, f"toy (NGC 3198 mass, test shell at 20 kpc): finite difference {f_fd:.4e} vs analytic {f_an:.4e} m/s^2 (outward)")
h2a = {}
for foot in FOOTS:
    a0 = A0[foot]; gl = law_g(GN_N, a0); aRn = dlaw_dgN(GN_N, a0) * (gl - GN_N)
    h2a[foot] = dict(dev_v=float(np.max(np.abs((gl - aRn) / gl - 1))), reaction_over_g_max=float(np.max(aRn / gl)),
                     n_outward=int(np.sum(gl - aRn < 0)))
put("H2", "a", all(h2a[f]["dev_v"] < 1e-6 for f in FOOTS), "H2v (variational): baryons feel g - a_R: NGC 3198 law dev " + " / ".join(f"{h2a[f]['dev_v']:.2f}" for f in FOOTS)
    + f" ({h2a['canonical']['n_outward']} / {h2a['alt']['n_outward']} of 43 radii pushed OUTWARD); re-tuning the medium so baryons obey the law leaves lensing "
    f"(rho_c) off the dynamics by a_R/g up to {h2a['canonical']['reaction_over_g_max']:.2f} (slip line 1.9e-5). H2n passes (a) only by having no reaction")
h2g = {}
for foot in FOOTS:
    a0 = A0[foot]
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            Mh, rh, gbh, gh, uh = host_fields(rk, a0); hv = HOV[f"{foot}|{hn}|{rk:g}"]
            M, a, us_of = us_fun(Mb_, apc, a0); rt = hv["r_t_pc"] * PC
            xs = np.logspace(math.log10(1e-4 * a), math.log10(rt), 4001)
            Mph = np.array([us_of(x) * x * x / G_SI for x in xs]); dMm = np.diff(Mph); xm = np.sqrt(xs[1:] * xs[:-1])
            mu = GL_X[None, :]; sn = np.sqrt(1 - mu ** 2); wq = GL_W[None, :] / 2
            gbs = plummer_g(M, a, xm)[:, None]
            vz = -gbs * mu - gbh; vp = -gbs * sn; mag = np.sqrt(vz ** 2 + vp ** 2)
            Lz_tot = law_g(mag, a0) * vz / mag
            term = (-gh) + (law_g(gbs, a0) * (-mu)) - Lz_tot                   # L(g_bh) + L(g_bs) - L(g_bh + g_bs), z
            a_m = float(np.sum((term * wq).sum(axis=1) * dMm) / np.sum(dMm))
            gbs_a = plummer_g(M, a, a)
            efe = (law_g(gbh + gbs_a, a0) - gh) / law_g(gbs_a, a0)
            h2g[f"{foot}|{hn}|{rk:g}"] = dict(eps=abs(a_m + gh) / gh, efe_dex=math.log10(efe))
h2ge = {f: [v["eps"] for k, v in h2g.items() if k.startswith(f)] for f in FOOTS}
h2gc = {f: [abs(v["efe_dex"]) for k, v in h2g.items() if k.startswith(f)] for f in FOOTS}
put("H2", "b", all(max(h2ge[f]) <= BND[f]["line_b"] for f in FOOTS),
    "H2g (global anchoring, Theorem S): " + "; ".join(f"{f}: eps {min(h2ge[f]):.3f}-{max(h2ge[f]):.3f} vs line {BND[f]['line_b']:.3g}" for f in FOOTS)
    + " (local approximation, as CFG941). H2o (own baryons) gives eps = 0 only with H1's labels")
put("H2", "c", all(max(h2gc[f]) <= BND[f]["delta_c"] for f in FOOTS),
    "H2g: QUMOND-type EFE " + "; ".join(f"{f}: {min(h2gc[f]):.3f}-{max(h2gc[f]):.3f} dex vs delta_c {BND[f]['delta_c']:.3f}" for f in FOOTS) + "; H2o: 0 (with labels)")
put("H2", "d", False, "H2v: action, conserves energy-momentum; settled state Jeans-unstable (bounded) since the anchor ignores medium perturbations. "
    "H2n: the medium is pushed with no reaction -> no action, partial_mu T^{mu nu} != 0: FAIL. H2o inherits the H2v/H2n dichotomy")
iL = -1
rho_last = {f: float(np.gradient(R_N ** 2 * (law_g(GN_N, A0[f]) - GN_N), R_N)[iL] / (K_SI * R_N[iL] ** 2)) for f in FOOTS}
tJ = {f: 1 / math.sqrt(K_SI * rho_last[f]) / MYR for f in FOOTS}
put("H2", "e", None, f"no chi tether: the settled medium has full Newtonian self-gravity (F1 and tethered-tethered gravity restored) but its law state is Jeans "
    f"unstable for k < sqrt(2)/L*, e-fold 1/sqrt(K rho_c) = {tJ['canonical']:.0f} / {tJ['alt']:.0f} Myr at NGC 3198's last radius; gated linear regime: n = 1")
RES["H2"] = dict(a=h2a, g=h2g, fd=(f_fd, f_an), tJ_Myr=tJ)
guard("H2")

# ---------------------------------------------------------------- H3
P("\n==================== H3: equivalence-principle restoration? ====================")
bsh = sp.Symbol("b", real=True)
shift = sp.diff(Wfull.subs(u, u + bsh), bsh).subs(bsh, 0)
H3sym = chk("H3_no_gradient_shift_symmetry", is0(KS * shift - Dfull) and sp.limit(KS * shift / u, u, 0) == 1,
            "dW(|grad chi + b|)/db at b = 0 = W'(u) = D_full(u)/K, with linear coefficient 1 (D-T): W is not invariant under chi -> chi + b.x; "
            "a uniform external chi gradient is physical (the Einstein elevator removes only the metric's)")
pm = sp.simplify((f_med_host.subs(s1, 1) / f_star_host).subs(law_sub))
H3pm = chk("H3_passive_mass_zero", pm == 0, f"passive gravitational mass of medium in a settled host's field / inertial mass = {pm} at leading order")
h3 = {}
beta0 = OC * H0_SI / 2
for foot in FOOTS:
    a0 = A0[foot]
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            Mh, rh, gbh, gh, uh = host_fields(rk, a0); Vc = math.sqrt(gh * rh)
            M, a, us_of = us_fun(Mb_, apc, a0); hh = 1e-5 * a
            rho_c = ((a + hh) ** 2 * us_of(a + hh) - (a - hh) ** 2 * us_of(a - hh)) / (2 * hh) / (K_SI * a * a)
            h3[f"{foot}|{hn}|{rk:g}"] = dict(betaV_over_g=beta0 * Vc / gh, betaV300_over_g=beta0 * 3e5 / gh, v2c2=Vc ** 2 / C_SI ** 2,
                                             inertia_corr=(OC / 6) * RHO_C0 / rho_c)
bv = [v["betaV_over_g"] for v in h3.values()]; bv3 = [v["betaV300_over_g"] for v in h3.values()]
P(f"  dynamic corrections to the hover: |beta V|/g_host = {min(bv):.1e} ... {max(bv):.1e} (V circular; 300 km/s: up to {max(bv3):.1e}); v^2/c^2 <= "
  f"{max(v['v2c2'] for v in h3.values()):.1e}; inertia correction (Omega_c/6)(rhobar_c/rho_c) <= {max(v['inertia_corr'] for v in h3.values()):.1e}")
P(f"  rigid two-component dynamics (Q3): stars bound in {nb_bound}/18 cases; either way the composite falls at 1 - f_m*eps of g_host (eta {min(eta_all):.3f}-{max(eta_all):.3f})")
put("H3", "a", K1 and BT_OK, "no change to the action: P0's static law and BTFR")
put("H3", "b", all(max(hov_r[f]) <= BND[f]["line_b"] for f in FOOTS), "the hover is real, not a static artefact: " +
    "; ".join(f"{f}: eps {min(hov_r[f]):.3f}-{max(hov_r[f]):.3f}" for f in FOOTS) + f"; dynamic corrections <= {max(bv3):.1e}")
put("H3", "c", all(max(hov_e[f]) <= BND[f]["delta_c"] for f in FOOTS), "; ".join(f"{f}: |EFE| {min(hov_e[f]):.3f}-{max(hov_e[f]):.3f} dex vs delta_c {BND[f]['delta_c']:.3f}" for f in FOOTS))
put("H3", "d", True, "P0's (CFG938 conditions)")
put("H3", "e", None, "nothing restored (P0's F1 and F2)")
RES["H3"] = h3

# ---------------------------------------------------------------- H4
P("\n==================== H4: dispersion-supported settled medium (tether share f_T) ====================")
fT, gq, Fp = sp.symbols("f_T g F_p", positive=True)
host_eq = sp.Eq(-gq + fT * gq + Fp, 0)
Fp_sol = sp.solve(host_eq, Fp)[0]
a_sat_med = -gq + fT * gq                                              # a separate cold stream feels the field force, not the host's pressure
dA4 = sp.simplify(a_sat_med - (-gq))
cold = sp.solve(sp.Eq(Fp_sol, 0), fT)
H4sym = chk("H4_support_split", is0(dA4 - fT * gq) and cold == [1],
            f"host element: -g + f_T g + F_p = 0 -> F_p = {Fp_sol}; satellite stream: Delta a = {dA4}; cold limit F_p -> 0 forces f_T = {cold[0]} (the hover)")
need = {f: BND[f]["line_b"] / max(hov_r[f]) for f in FOOTS}
put("H4", "a", True, "the cold, static limit (frozen (a)) exists only with f_T = 1, where it is P0's law")
put("H4", "b", all(max(hov_r[f]) <= BND[f]["line_b"] for f in FOOTS), "at f_T = 1 eps = the hover; (b) needs f_T <= " + " / ".join(f"{need[f]:.3g}" for f in FOOTS) + " (line / hover ratio), (a)'s cold limit needs f_T = 1: incompatible")
put("H4", "c", all(max(hov_e[f]) <= BND[f]["delta_c"] for f in FOOTS), "at f_T = 1 the satellite's tether reads the total chi: P0's EFE " + "; ".join(f"{f}: {min(hov_e[f]):.3f}-{max(hov_e[f]):.3f} dex" for f in FOOTS))
put("H4", "d", None, "multistream support is outside CFG938's single-stream EFT (not graded)")
put("H4", "e", None, "if the warm option were taken (f_T small), the medium would gravitate as collisionless matter (F1 and F2 restored): a different theory, "
    "the direction of CFG941's open item 2 and of class A's dispersion-supported particles")

# ---------------------------------------------------------------- corollaries of Theorem S
P("\n==================== corollaries of Theorem S (reported) ====================")
P("  velocity-gated tether: a satellite at rest relative to the host medium (apocentre, slow satellites) has F(x, 0) = host value -> hover exactly; "
  "a moving satellite's own support still needs a reading of its own chi alone -> a label (E1)")
P("  filtered tether (chi_f from (1 - l^2 D^2) chi_f = chi, one constant l): the host medium at the satellite's point is in equilibrium under the same "
  "filtered force, so the satellite medium hovers for every l (Theorem S); the host's own law needs l -> infinity (CFG941 R3ell)")

# ================================================================================================ CLASSES
P("\n==================== CLASSES (frozen rules, criteria sec. 4) ====================")
ae = lambda c_: all(TESTS[c_][k]["pass_"] for k in "abc")
NOTRES = {
    "H2": H2lem and H2fd and (not TESTS["H2"]["a"]["pass_"]) and (not TESTS["H2"]["b"]["pass_"]) and (not TESTS["H2"]["d"]["pass_"]) and Q2,
    "H3": H3sym and H3pm and Q2 and ((not TESTS["H3"]["b"]["pass_"]) or (not TESTS["H3"]["c"]["pass_"])),
    "H4": H4sym and ((not TESTS["H4"]["b"]["pass_"]) or (not TESTS["H4"]["c"]["pass_"])),
    "H1": False,
}
WHY = {
    "H1": "labels are the escape E1 of Theorem S; costs: non-variational label sector (L2 tidal re-latch; seeding at collapse open), a continuum of "
          "auxiliary chi_q, lambda_q, per-label single-stream, energy-momentum conserved only between label changes; open condition: every settled galaxy single-label",
    "H2": "variational -> reaction a_R on the baryons breaks (a) (deep limit a0/2); non-variational -> no conservation (d); global anchoring -> hover (Theorem S); "
          "own anchoring needs H1's labels and meets the same dichotomy",
    "H3": "no gradient-shift symmetry is compatible with W'(u) != 0 (forced by the law); passive gravitational mass 0; the hover is dynamic, not a static artefact",
    "H4": "(a)'s cold limit forces f_T = 1, which is the hover and P0's EFE",
}
CLASSES = {}
for cand in ("H1", "H2", "H3", "H4"):
    t_ = TESTS[cand]
    d_ok = t_["d"]["pass_"] is not False
    passes = all(t_[k]["pass_"] for k in "abc") and d_ok
    if passes and cand == "H1":
        cl = "RESOLVED-WITH-COST"                                         # costs are structural (label sector), listed in WHY
    elif passes:
        cl = "RESOLVED"
    elif NOTRES[cand]:
        cl = "NOT RESOLVABLE"
    else:
        cl = "UNCLASSIFIED (rule gap)"
    fails = [k for k in "abcd" if t_[k]["pass_"] is False]
    CLASSES[cand] = dict(cls=cl, fails=fails, why=WHY[cand])
    P(f"  {cand}  {cl:20s} fails: {','.join(fails) or '-'}   {WHY[cand]}")
if any(v["cls"] == "RESOLVED" for v in CLASSES.values()):
    OVERALL = "HOVER RESOLVED"
elif any(v["cls"] == "RESOLVED-WITH-COST" for v in CLASSES.values()):
    OVERALL = "CONDITIONAL"
elif all(v["cls"] == "NOT RESOLVABLE" for v in CLASSES.values()):
    OVERALL = "NO-GO"
else:
    OVERALL = "UNCLASSIFIED"
P(f"\n  OVERALL: {OVERALL}")
P("  Label-free tethers: the hover is exact at leading order (Theorem S), and every tested label-free candidate (P0/R3theta, H2g, H3, H4) keeps eps above "
  "eps_B with the full cross terms. With labels (H1): resolved at the cost of a membership sector equivalent to class A's per-catchment tether.")
RES["tests"] = TESTS; RES["classes"] = CLASSES; RES["overall"] = OVERALL
allchk = all(v["pass"] for v in RES["checks"].values())
P(f"\n  all checks pass: {allchk}; runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
guard("end")
dump()
sys.exit(0 if (allchk and K_ALL) else 1)
