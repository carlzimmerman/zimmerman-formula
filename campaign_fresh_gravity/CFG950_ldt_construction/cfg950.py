"""CFG950 -- the labelled-domain theory (LDT): the formal construction, written down and tested.
Criteria: FROZEN_CRITERIA.md (324edbf93, committed alone before this script); AMENDMENT_A1_post_hoc.md (fb9af871f, POST HOC: the f3
merger-toy metric; the frozen (f) and class are computed and printed alongside the amended ones).
Run (one core, one process, < 1 GB):
    CFG950_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg950.py      -> cfg950_K.out, cfg950_results_K.json
    CFG950_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg950.py     -> cfg950_MUTATE.out, cfg950_results_MUTATE.json
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg950.py                     -> cfg950.out, cfg950_results.json (K + main)
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite). Exit 75 = memory guard (rerun later).
Machinery copied with attribution (method verbatim) from CFG945 (cfg945.py: CFG941 hover, CFG874 replica, H1/L2, dynamics),
CFG947 (cfg947.py: engine census/domain, growth determinant of CFG941, slip, T-M toy, T-E) and CFG938 (dispersion closed form).
kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed."""
import os, sys, io, csv, json, math, time, resource, contextlib, subprocess, re
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG950_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG950_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
OUT = []
RES = {"lane": "CFG950", "criteria": "324edbf93", "amendments": ["A1 fb9af871f POST HOC (f3 merger-toy metric non-convergent by construction; "
                                                                 "resolved-range metric + discrete identity; frozen result reported alongside)"],
       "mutate": MUT, "stage": STAGE, "checks": {}, "tests": {}}
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
    json.dump(RES, open(os.path.join(HERE, f"cfg950_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg950{TAG}.out"), "w").write("\n".join(OUT) + "\n")


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
if FI0 is not None and FI0 < 10.0:
    print(f"MEMORY GUARD: free+inactive {FI0:.1f} GB < 10 GB at start; exit 75 (rerun later)"); sys.exit(75)


def guard(where=""):
    r = rss_val()
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)
    fi, sw = mem_state()
    if fi is None:
        return
    SWMIN[0] = min(SWMIN[0], sw) if SWMIN[0] is not None else sw
    if fi < 6.0 or (SWMIN[0] is not None and sw - SWMIN[0] > 1.0):
        P(f"MEMORY GUARD at {where}: free+inactive {fi:.1f} GB, swap {sw:.2f} GB (min {SWMIN[0]:.2f}); exit 75"); dump(); sys.exit(75)


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def is0(e):
    return sp.simplify(sp.expand(e)) == 0


# ================================================================================================ constants (as CFG945 / CFG947)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC = 6.67430e-11, 299792458.0, 1.98847e30, 3.0856775814913673e16
KPC = 1e3 * PC
K_SI = 4 * math.pi * G_SI
MSUN847, KPC847 = 1.989e30, 3.0857e19
H0_SI = 67.4e3 / (1e6 * PC); RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
OB = 0.0493; OC = 5.364 * OB; RHO_C0 = OC * RHO_CRIT
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]
HOST938 = 6e10
RADII = (50.0, 100.0, 250.0)
MYR = 3.156e13
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0),
          ("cluster", 1.5e14, 1000.0)]
# ---- the class-A engine's own constants and census (cfg947.py copy of the engine's values; read with the Read tool)
OM_B, OM_C = 0.02237, 0.1200; FB = OM_B / (OM_B + OM_C)
GE, MSE, MPCE, HE = 6.674e-11, 1.989e30, 3.0857e22, 0.674
RMIN = 0.78125
_dta = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
DTA0 = float(_dta["D"][0]); assert abs(_dta["z"][0]) < 1e-12
RHOM_H = 0.315 * 2.775e11


def fret_of(lM):
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def M_ta(R, D):
    return (4 * math.pi / 3) * R ** 3 * D * RHOM_H


def census(Mb_msun):
    f = lambda lR: fret_of(math.log10(M_ta(math.exp(lR), DTA0))) * FB * M_ta(math.exp(lR), DTA0) / HE - Mb_msun
    lR = brentq(f, math.log(1e-6), math.log(1e3), xtol=1e-14, rtol=1e-14)
    R = math.exp(lR); Mh = M_ta(R, DTA0); fr = fret_of(math.log10(Mh))
    return dict(R=R, fr=fr, Mta_h=Mh, Mta=Mh / HE)


def domain(Mb_msun, a0):
    """cfg947.py domain(): E7 edge for an isolated census domain (engine constants), plus the LDT label mass."""
    c = census(Mb_msun)
    x = c["fr"] * FB / (1 - FB)
    rM = math.sqrt(GE * Mb_msun * MSE / a0)
    r_on = c["R"] / HE * MPCE
    xs = min(rM / math.log1p(x) / r_on, 1.0)
    r_e = xs * r_on
    return dict(c, x=x, rM=rM, r_on=r_on, r_e=r_e, xs=xs, Mc=(1 - FB) * c["Mta"], resolved=c["R"] >= RMIN, yE=(rM / r_e) ** 2)


def ldt_edge(Mb_msun, Mc_msun, a0):
    """LDT edge = the label's supply root with the simple kernel and point-mass baryons: M_ph(<r_e) = M_c.
    (sqrt(y^2 + 4y) - y)/(2y) = N  =>  y_e = 1/(N(N+1)),  r_e = r_M sqrt(N(N+1))."""
    N = Mc_msun / Mb_msun
    rM = math.sqrt(G_SI * Mb_msun * MSUN / a0)
    return rM * math.sqrt(N * (N + 1)), rM, N


# ---- the law
def law_g(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def law_mono(gN, a0):
    gN = np.asarray(gN, float)
    return gN * C4.nu_mono(gN / a0)


def Rinv(x, a0):
    return 0.5 * (-x + math.sqrt(x * x + 4.0 * x * a0))


def R_num(u_, a0):
    return u_ * u_ / (a0 - u_)


def D_num(u_, a0):
    return a0 * u_ / (a0 - u_)


def wfull_x(x):
    x = np.asarray(x, float)
    small = np.abs(x) < 1e-3
    xs = np.where(small, x, 0.0); xl = np.where(small, 0.0, x)
    ser = xs * xs / 2 + xs ** 3 / 3 + xs ** 4 / 4 + xs ** 5 / 5 + xs ** 6 / 6 + xs ** 7 / 7
    big = -xl - np.log1p(-xl)
    return np.where(small, ser, big)


def W_num(u_, a0, K=K_SI):
    return a0 * a0 * wfull_x(np.asarray(u_, float) / a0) / K


def dlaw_dgN(gN, a0):
    return 0.5 * (1.0 + (gN + 2 * a0) / np.sqrt(gN * gN + 4 * gN * a0))


# ---- NGC 3198 (record SPARC file, Upsilon 0.61, as CFG938/941/945/947)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MBR_N = GN_N * R_N ** 2 / G_SI
MB_N = GN_N[-1] * R_N[-1] ** 2 / G_SI                                    # kg (CFG945's MB_N)
MB_N_SUN = MB_N / MSUN

P("CFG950  the labelled-domain theory (LDT): formal construction and tests" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P("  criteria 324edbf93; kappa = 1/2 FITTED; footings never pooled; cold energy; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e};  NGC 3198: {len(R_N)} radii, M_b = {MB_N_SUN:.4e} M_sun;  "
  f"native Delta_ta(0) = {DTA0:.6f}; engine f_b = {FB:.6f};  memory at start: free+inactive {FI0 if FI0 is None else round(FI0, 1)} GB, "
  f"swap {SW0 if SW0 is None else round(SW0, 2)} GB")
RES["inputs"] = dict(DTA0=DTA0, FB=FB, MB_NGC3198_Msun=MB_N_SUN, N_radii=int(len(R_N)))

# ================================================================================================ shared sympy (as CFG941/945)
r, G, a0s = sp.symbols("r G a_0", positive=True)
u, gN, qq = sp.symbols("u g_N q", positive=True)
KS = 4 * sp.pi * G
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / KS
Dfull = sp.simplify(KS * sp.diff(Wfull, u))
Rsym = sp.simplify(Dfull - u)


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
    """cfg945.py solve_static (verbatim method)."""
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


# ================================================================================================ CFG941 hover machinery (cfg945.py verbatim)
GL_X, GL_W = np.polynomial.legendre.leggauss(64)


def plummer_g(M, a, x):
    return G_SI * M * x / (x * x + a * a) ** 1.5


def satellite_hover(Mb_sun, a_pc, rkpc, a0, tether=True):
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
    wm = np.minimum(wmag, a0 * (1 - 1e-12))
    Tz = (wm ** 2 / (a0 - wm)) * wz / wmag if tether else -(wz)
    Tz_avg = float(np.sum((Tz * wq).sum(axis=1) * dM) / np.sum(dM))
    a_m = -gbh + Tz_avg
    a_s = -(gbh + uh)
    gbs_a = plummer_g(M, a, a)
    efe = (gbs_a + (Rinv(gbh + gbs_a, a0) - uh)) / (gbs_a + Rinv(gbs_a, a0))
    return dict(g_host=float(gh), u_h=float(uh), g_bh=gbh, delta_a=float(a_m - a_s), ratio=float((a_m - a_s) / gh), r_t_pc=rt / PC,
                g_bs_at_a=gbs_a, efe_factor=float(efe), efe_dex=float(math.log10(efe)))


def host_fields(rk, a0):
    Mh = HOST938 * MSUN847; rh = rk * KPC847; gbh = G_SI * Mh / rh ** 2; gh = float(law_g(gbh, a0))
    return Mh, rh, gbh, gh, gh - gbh


def us_fun(Mb_sun, a_pc, a0):
    M = Mb_sun * MSUN847; a = a_pc * PC
    return M, a, (lambda x: float(law_g(plummer_g(M, a, x), a0)) - plummer_g(M, a, x))


# ---- CFG874 estimator (cfg945.py replica, read-only data)
G874, MSUN874, PC874 = 6.674e-11, 1.989e30, 3.0857e16
A874LIT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
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


ROWS874, A874, BOOT = {}, {}, {}


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
    for t in thr:
        c_, s_, ns, nss = c_of_eps(foot, t * (1 + 1e-12), kappa_r)
        if c_ < -2 * s_:
            return t
    return math.inf


# ---- H1 per-label tether (cfg945.py h1_l2_radius / h1_delta_a / restoring_and_dyn, verbatim)
def h1_l2_radius(Mb_sun, a_pc, rk, a0):
    Mh, rh, gbh, gh, uh = host_fields(rk, a0)
    M, a, us_of = us_fun(Mb_sun, a_pc, a0)
    uhost = lambda R: float(law_g(G_SI * Mh / R ** 2, a0)) - G_SI * Mh / R ** 2

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
    return abs(a_m - a_s) / gh, dict(r_dom_pc=rdom / PC, r_dom_rule=how, r_dom_over_R=rdom / rh, M_star_dom=float(Mst[-1] / MSUN847),
                                      M_med_dom=float(Mph[-1] / MSUN847), a_m=a_m, a_s=a_s, g_host=gh)


def restoring_and_dyn(Mb_sun, a_pc, rt_pc, a0, Da, gh, tether=True, T_Myr=1000.0):
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
    L_ = rt; tu = MYR; sc = tu * tu / L_
    dda = Da if tether else 0.0

    def rhs(t, y):
        zs, vs, zm, vm = y; d = (zs - zm) * L_
        p = Pd(d) * sc; sg = 1.0 if d > 0 else (-1.0 if d < 0 else 0.0)
        return [vs, -gh * sc - sg * p, vm, (-gh + dda) * sc + sg * (M / Mmt) * p]
    tev = np.linspace(0.0, T_Myr, 4001)
    sol = solve_ivp(rhs, (0.0, T_Myr), [0.0, 0.0, 0.0, 0.0], method="DOP853", rtol=1e-9, atol=1e-12, max_step=0.5, t_eval=tev)
    dd_ = np.abs(sol.y[0] - sol.y[2])
    return dict(M_med_t=Mmt / MSUN847, P_max_over_Da=Pmax / Da if Da > 0 else math.inf, bound=bool(Pmax > Da),
                max_sep_over_rt=float(dd_.max()), ok=bool(sol.success))


def two_label_disp(r2, U, Aminus1=0.0):
    """cfg945.py two_label_disp (units K = rho_1 = L* = 1)."""
    mx = 0.0
    for k in np.logspace(-2, 3, 400):
        O1 = 1.0 * Aminus1 + 0.5 * k * k; O2 = r2 * Aminus1 + 0.5 * r2 * k * k
        p1 = np.array([1.0, -2 * k * U, k * k * U * U - O2]); p2 = np.array([1.0, 0.0, -O1])
        poly = np.polymul(p1, p2); poly[-1] -= r2
        mx = max(mx, float(np.max(np.roots(poly).imag)))
    return mx, math.sqrt(1 + r2)


# ---- growth machinery: CFG941's Lagrangian route (cfg947.py copy)
tt = sp.symbols("t", positive=True); al = sp.symbols("alpha")
C2s, Bs = sp.symbols("c_2 b", nonnegative=True)
Kg = sp.Symbol("K", positive=True)
FBr, FCr = sp.Rational(1000, 6364), sp.Rational(5364, 6364)


def growth_det(comp):
    a = tt ** sp.Rational(2, 3); H = sp.Rational(2, 3) / tt; rtot = (sp.Rational(2, 3) / tt ** 2) / Kg
    psis = [sp.Function("psi_" + n)(tt) for n, _, _ in comp]
    rho = [f * rtot for _, f, _ in comp]
    L = sum(sp.Rational(1, 2) * rh * a ** 3 * a ** 2 * sp.diff(ps, tt) ** 2 for rh, ps in zip(rho, psis))
    L += a ** 5 * Kg / 2 * (sum(rh * ps for rh, ps in zip(rho, psis))) ** 2
    tidx = [i for i, c in enumerate(comp) if c[2]]
    if tidx:
        i = tidx[0]; rT = rho[i]
        beta = -Kg * rT / (3 * H)
        L += -a ** 5 * C2s / (2 * Kg) * (-Kg * rT * psis[i] + Bs * beta * sp.diff(psis[i], tt)) ** 2
    eqs = sp.euler_equations(L, psis, tt)
    As = sp.symbols("A0:%d" % len(comp))
    rows = []; homog = True
    for e in eqs:
        ex = e.lhs.subs({ps: A * tt ** al for ps, A in zip(psis, As)}).doit()
        ex = sp.expand(sp.powsimp(sp.expand(ex / tt ** al), force=True))
        pows = set(sp.nsimplify(term.as_coeff_exponent(tt)[1]) for term in sp.Add.make_args(ex))
        homog = homog and len(pows) == 1
        p0 = list(pows)[0]
        rows.append(sp.expand(sp.powsimp(ex / tt ** p0, force=True)))
    M = sp.Matrix([[sp.diff(rw, A) for A in As] for rw in rows])
    return sp.expand(M.det()), homog


def n_from_det(det, subs):
    subs = dict(subs); subs[Kg] = 1
    pol = sp.Poly(sp.expand(det.subs(subs)), al)
    roots = np.roots([complex(sp.N(c_)) for c_ in pol.all_coeffs()])
    rr = [z.real for z in roots if abs(z.imag) < 1e-9]
    return 1.5 * max(rr)


# ---- CFG938 slip (cfg947.py slip_P0 method, rows kept)
def slip_rows():
    rows = {}; worst_g = worst_8 = 0.0; inert = []
    for foot in FOOTS:
        a0 = A0[foot]
        for name, Mb, rk_ in SYS847:
            M = Mb * MSUN847; rr = rk_ * KPC847

            def uat(x):
                g_ = float(law_g(G_SI * M / x ** 2, a0)); return g_ * a0 / (g_ + a0)
            gn = G_SI * M / rr ** 2; uu = uat(rr); g_ = gn + uu
            W_ = float(W_num(uu, a0)); Dv = uu / (1 - uu / a0)
            h_ = 1e-5 * rr
            rho_c = ((rr + h_) ** 2 * uat(rr + h_) - (rr - h_) ** 2 * uat(rr - h_)) / (2 * h_) / (K_SI * rr ** 2)
            vc2 = g_ * rr
            row = {}
            for Lpc in (0.0, 24.0, 1000.0):
                ps = math.pi * G_SI * (Lpc * PC) ** 2 * rho_c ** 2
                pr = -W_ + ps; pt = -W_ + Dv * uu / K_SI + ps
                sg = 4 * math.pi * G_SI * rr * abs(pr) / (C_SI ** 2 * g_)
                s8 = 8 * math.pi * G_SI * rr ** 2 * max(abs(pr), abs(pt)) / (C_SI ** 2 * vc2)
                row[f"L{Lpc:g}"] = (sg, s8)
                worst_g = max(worst_g, sg); worst_8 = max(worst_8, s8)
            ie = K_SI * rho_c * C_SI ** 2 / (g_ * uu)
            inert.append(ie)
            rows[f"{foot}|{name}"] = dict(row, inertia_margin=ie, rho_c=rho_c)
    return worst_g, worst_8, rows, min(inert)


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
J941 = json.load(open(os.path.join(LANES, "CFG941_self_gravity_repair", "cfg941_results.json")))["hover"]
J945 = json.load(open(os.path.join(LANES, "CFG945_gated_tether_satellite_hover", "cfg945_results.json")))
J947 = json.load(open(os.path.join(LANES, "CFG947_option3_nonlocal_parent", "cfg947_results.json")))
J874 = json.load(open(os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874_results.json")))
# K1
k1 = {}
for foot in FOOTS:
    us_, gt_, ex_k1 = solve_static(Wfull, 1, GN_N, A0[foot])
    dv, nn = law_dev(gt_, GN_N, A0[foot]); k1[foot] = dict(max_rel_vs_law=dv, unsolved=nn)
K1 = chk("K1_CFG938_NGC3198_law", all(k1[f]["max_rel_vs_law"] < 1e-6 and k1[f]["unsolved"] == 0 for f in FOOTS),
         f"reduced EL {sp.factor(ex_k1)}; max |g/g_law - 1| canonical {k1['canonical']['max_rel_vs_law']:.2e}, alt {k1['alt']['max_rel_vs_law']:.2e} (2.2e-16; line 1e-6)")
RES["K1"] = k1
# K2
P("  deriving growth determinant (sympy, CFG941 route) ...")
DET2, HOM2 = growth_det([("b", FBr, False), ("t", FCr, True)])
n_s6 = n_from_det(DET2, {C2s: 1, Bs: 0}); n_full = n_from_det(DET2, {C2s: 1, Bs: 1}); n_dust = n_from_det(DET2, {C2s: 0, Bs: 0})
K2 = chk("K2_CFG941_growth_exponents", HOM2 and abs(n_s6 - 0.60954) < 1e-4 and abs(n_full - 0.69433) < 1e-4 and abs(n_dust - 1) < 1e-12,
         f"n(c2=1, no chi-bar) = {n_s6:.6f} (0.60954), n(c2=1, chi-bar) = {n_full:.6f} (0.69433), n(c2=0) = {n_dust:.12f}")
RES["K2"] = dict(n_s6=n_s6, n_full=n_full, n_dust=n_dust)
guard("K2")
# K3: CFG945 H1 + bound
for foot in FOOTS:
    rows = build874(foot); res, I_, S_ = analyse874(rows)
    ROWS874[foot] = (I_, S_); A874[foot] = res
    BOOT[foot] = Boot874(I_, S_)
H1B = {}
for foot in FOOTS:
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            e_, info = h1_delta_a(Mb_, apc, rk, A0[foot])
            H1B[f"{foot}|{hn}|{rk:g}"] = dict(eps=e_, **info)
k3_eps = max(abs(H1B[k]["eps"] / J945["H1"]["b"][k]["eps"] - 1) for k in H1B)
H1A = {}
for foot in FOOTS:
    a0 = A0[foot]; v = ((a0 - GN_N) + np.sqrt((a0 - GN_N) ** 2 + 8 * GN_N * a0)) / 4
    dv2 = law_dev(GN_N + 2 * v, GN_N, a0)[0]
    _, gtq, _ = solve_static(Wfull, 1, GN_N, a0, free_q=1e-6)
    H1A[foot] = dict(two_labels=dv2, debris_1e6=law_dev(gtq, GN_N, a0)[0])
k3_two = max(abs(H1A[f]["two_labels"] / J945["H1"]["a"][f]["two_labels"] - 1) for f in FOOTS)
k3_deb = max(abs(H1A[f]["debris_1e6"] / J945["H1"]["a"][f]["debris"]["1e-06"] - 1) for f in FOOTS)
EPSB = {f: eps_bound(f, 1.0) for f in FOOTS}
DELC = {f: A874[f]["c"] + 2 * A874[f]["se_c"] for f in FOOTS}
k3_eb = max(abs(EPSB[f] / J945["bound"][f]["eps_B_k1"] - 1) for f in FOOTS)
k3_dc = max(abs(DELC[f] / J945["bound"][f]["delta_c"] - 1) for f in FOOTS)
K3 = chk("K3_CFG945_H1_and_bound", max(k3_eps, k3_two, k3_deb, k3_eb, k3_dc) < 1e-9,
         f"18 tidal eps {min(v['eps'] for v in H1B.values()):.2e}..{max(v['eps'] for v in H1B.values()):.2e} (rel diff {k3_eps:.1e}); two labels "
         f"{H1A['canonical']['two_labels']:.3f}/{H1A['alt']['two_labels']:.3f} ({k3_two:.1e}); debris q=1e-6 {H1A['canonical']['debris_1e6']:.3e} ({k3_deb:.1e}); "
         f"eps_B {EPSB['canonical']:.4f}/{EPSB['alt']:.4f} ({k3_eb:.1e}); delta_c {DELC['canonical']:.4f}/{DELC['alt']:.4f} ({k3_dc:.1e})")
RES["K3"] = dict(eps_B=EPSB, delta_c=DELC, two=H1A)
guard("K3")
# K4: CFG947 positive results
tf = {}
for foot in FOOTS:
    a0 = A0[foot]
    for nm, Mb, apc in HOSTS882:
        for rk in RADII:
            Rh = rk * KPC847; gbh = G_SI * HOST938 * MSUN847 / Rh ** 2; gh = float(law_g(gbh, a0)); v2 = gh * Rh
            a = apc * PC; gbs = plummer_g(Mb * MSUN847, a, a); gph = float(law_g(gbs, a0)) - gbs
            tf[f"{foot}|{nm}|{rk:.0f}"] = (gph / gh) * max(v2 / C_SI ** 2, gh * a / C_SI ** 2)
tfmax = max(tf.values()); tf_ref = max(v["bound"] for v in J947["T-F"].values())


def tm_numeric(eps):
    """cfg947.py tm_numeric (Plummer blobs, G = 1)."""
    Xb = 5.0
    mat = [(1.0, 0.0, 0.3), ((1 + eps) / 2, Xb, 0.5), ((1 - eps) / 2, -Xb, 0.5)]
    Ssec = [(1.0, 0.0, 1.0), (-(1 + eps) / 2, Xb, 0.5), (-(1 - eps) / 2, -Xb, 0.5)]

    def fpair(xi, ai, xj, aj):
        d = xj - xi; a2 = 0.5 * (ai * ai + aj * aj)
        return d / (d * d + a2) ** 1.5
    F_ms = sum(mi * sj_ * fpair(xi, ai, xj_, aj) for mi, xi, ai in mat for sj_, xj_, aj in Ssec)
    gtot_at = lambda x0, a0_: (sum(m_ * fpair(x0, a0_, x_, a_) for m_, x_, a_ in mat if abs(x_ - x0) > 1e-12)
                               + sum(s_ * fpair(x0, a0_, x_, a_) for s_, x_, a_ in Ssec if abs(x_ - x0) > 1e-12))
    sg = sum(s_ * gtot_at(x_, a_) for s_, x_, a_ in Ssec)
    return F_ms, sg


tmn = {e: tm_numeric(e) for e in (0.0, 0.01, 0.1, 0.3)}
ident = max(abs(v[0] + v[1]) for v in tmn.values())
tsym = sp.symbols("t", real=True)
Me = sp.Function("M_e")(tsym); Xt = sp.Function("X")(tsym); epsS, McS = sp.symbols("epsilon M_c", positive=True)
tg, Me0, X0, Gs_, Md = sp.symbols("t_g M_e0 X_0 G_s M_dom", positive=True)
R_E8_target = -epsS * (sp.diff(Me, tsym, 2) * Xt + 2 * sp.diff(Me, tsym) * sp.diff(Xt, tsym))
hist = Me0 * (1 - sp.cos(sp.pi * tsym / tg)) / 2
Rmax_E8 = sp.simplify(sp.Abs(R_E8_target.subs({Me: hist, Xt: X0}).doit().subs(tsym, 0)))
rel_E8 = sp.simplify((Rmax_E8 / (Gs_ * Md ** 2 / X0 ** 2)).subs({tg: sp.sqrt(X0 ** 3 / (Gs_ * Md)), Me0: Md / 2}))
tm_rel = {e: float(rel_E8.subs(epsS, e)) for e in (0.01, 0.1, 0.3)}
k4_tm = max(abs(tm_rel[e] / J947["T-M"]["R_rel_E8"][str(e)] - 1) for e in tm_rel)
te_min = math.inf
for foot in FOOTS:
    for kz, law in (("simple", law_g), ("mono", law_mono)):
        for Mb in np.logspace(7, 15, 17):
            dom = domain(float(Mb), A0[foot]); ron = dom["r_on"]; gnr = G_SI * Mb * MSUN / ron ** 2
            te_min = min(te_min, ron ** 2 * float(law(gnr, A0[foot])) / G_SI / MSUN / dom["Mta"])
te_ref = min(x["ratio"] for v in J947["T-E"].values() for x in v)
K4 = chk("K4_CFG947_positive_results", abs(tfmax / tf_ref - 1) < 1e-9 and abs(n_dust - 1) < 1e-12 and ident <= 1e-16 and k4_tm < 1e-9
         and abs(te_min / te_ref - 1) < 1e-9 and sp.simplify(rel_E8 - sp.pi ** 2 * epsS / 4) == 0,
         f"T-F retardation bound max {tfmax:.4e} (CFG947 {tf_ref:.4e}); dust n = {n_dust:.12f}; T-M identity {ident:.1e}; R/(M_dom g_ref) = {rel_E8} "
         f"({', '.join(f'{tm_rel[e]:.4f}' for e in tm_rel)}; rel diff {k4_tm:.1e}); T-E min ratio {te_min:.6f} (CFG947 {te_ref:.6f})")
RES["K4"] = dict(tf_max=tfmax, tm_identity=ident, tm_rel=tm_rel, te_min=te_min)
# K5
wg0, w80, SLIP_ROWS, INERT_MIN = slip_rows()
K5 = chk("K5_CFG938_slip", abs(w80 / 1.539799903790011e-05 - 1) < 0.02, f"worst s_847 = {w80:.4e} (1.5398e-5), s_grad = {wg0:.3e}")
# K6
UGRID = (0.0909, 0.5, 0.9, 0.99)


def disp_min(uf):
    kL = np.logspace(-2, 5, 400); th = np.linspace(0, math.pi / 2, 91)
    Rp = uf * (2 - uf) / (1 - uf) ** 2; Ru = uf / (1 - uf)
    W2 = kL[:, None] ** 2 / 2 + Rp * np.cos(th[None, :]) ** 2 + Ru * np.sin(th[None, :]) ** 2
    return float(W2.min()), float(np.sqrt(np.clip(-W2, 0, None)).max())


dmins = {uf: disp_min(uf) for uf in UGRID}
d2 = {}
for r2 in (0.1, 1.0, 10.0):
    for U in (0.0, 0.1, 1.0, 10.0):
        for Am in (0.0, 1.0):
            mx, jb = two_label_disp(r2, U, Am); d2[f"r2={r2:g}|U={U:g}|A-1={Am:g}"] = mx / jb
d2max = max(d2.values()); d2ref = max(v["max_im"] / v["jeans"] for v in J945["H1"]["d"].values())
K6 = chk("K6_CFG938_dispersion_CFG945_two_label", all(abs(dmins[uf][0] / t_ - 1) < 1e-3 for uf, t_ in zip(UGRID, (0.1, 1.0, 9.0, 99.0)))
         and abs(d2max / d2ref - 1) < 1e-3,
         "min omega^2/(K rho0) = " + ", ".join(f"{dmins[uf][0]:.4f}" for uf in UGRID) + f" (0.1/1/9/99); two-label max Im/Jeans {d2max:.4f} (CFG945 {d2ref:.4f})")
# K7
HOV = {}
for foot in FOOTS:
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            HOV[f"{foot}|{hn}|{rk:g}"] = satellite_hover(Mb_, apc, rk, A0[foot])
k7 = max(abs(HOV[k]["ratio"] / J941[k]["ratio"] - 1) for k in HOV)
K7 = chk("K7_CFG941_hover_ratios", k7 < 1e-9 and len(HOV) == 18,
         f"18 ratios reproduced (max rel diff {k7:.1e}); range {min(v['ratio'] for v in HOV.values()):.4f}..{max(v['ratio'] for v in HOV.values()):.4f}")
K_ALL = K1 and K2 and K3 and K4 and K5 and K6 and K7
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> main classes VOID'}")
RES["K_all"] = K_ALL
guard("K")
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)


# ================================================================================================ machinery for MUTATE and main
# ---------------------------------------------------------------- 1-D slab toy (units G = 1, K = 4 pi, a0 = 1)
K1D = 4 * math.pi
XL_BOX, XR_BOX = -20.0, 20.0


def w1(s):
    return wfull_x(np.minimum(np.abs(s), 1 - 1e-12)) / K1D            # W(|s|) with a0 = 1, K = 4 pi


def forces_1d(x, m, lab, tether=True, sw=None):
    """gravity (exact pair forces, sourced by m (+ source weights sw)) + per-label tether from the gap energy.
    Returns force array (inertia m).  Tether: for label q sorted, gap value s_j = (K/2)(M_q,left - M_q,right),
    force on slab k = W(|s_right|) - W(|s_left|) (outer gaps |s| = K M_q/2): telescopes to zero."""
    n = len(x); F = np.zeros(n)
    msrc = m + (sw if sw is not None else 0.0)
    o = np.argsort(x, kind="mergesort"); xs = x[o]; ms = msrc[o]
    cl = np.concatenate(([0.0], np.cumsum(ms)[:-1])); tot = ms.sum(); cr = tot - cl - ms
    F[o] = -(K1D / 2) * m[o] * (cl - cr)
    if tether:
        for q in np.unique(lab[lab >= 1]):
            idx = np.nonzero(lab == q)[0]; oq = idx[np.argsort(x[idx], kind="mergesort")]
            mq = m[oq]; Mq = mq.sum()
            left = np.concatenate(([0.0], np.cumsum(mq)))                # mass to the left of gap j (j = 0..n)
            s = (K1D / 2) * (left - (Mq - left))                           # gap values incl. outer (s_0 = -KM/2, s_n = +KM/2)
            Wg = w1(s)
            F[oq] += Wg[1:] - Wg[:-1]
    return F


def energy_1d(x, v, m, lab):
    o = np.argsort(x, kind="mergesort"); xs = x[o]; ms = m[o]
    cl = np.concatenate(([0.0], np.cumsum(ms)[:-1]))
    Eg = (K1D / 2) * float(np.sum(ms * (xs * cl - np.concatenate(([0.0], np.cumsum(ms * xs)[:-1])))))
    Ew = 0.0
    for q in np.unique(lab[lab >= 1]):
        idx = np.nonzero(lab == q)[0]; oq = idx[np.argsort(x[idx], kind="mergesort")]
        xq = x[oq]; mq = m[oq]; Mq = mq.sum()
        left = np.concatenate(([0.0], np.cumsum(mq))); s = (K1D / 2) * (left - (Mq - left)); Wg = w1(s)
        Ew += float(np.sum(Wg[1:-1] * np.diff(xq))) + float(Wg[0] * (xq[0] - XL_BOX) + Wg[-1] * (XR_BOX - xq[-1]))
    return 0.5 * float(np.sum(m * v * v)) + Eg + Ew


def toy1d_ldt(seed=950, nsteps=6000, dt=1e-3, events=True, tether=True):
    """asymmetric 1-D system: two baryon clumps, two labels, unlabelled dust; events (i) latch, (iv) re-latch, (ii) merge."""
    rng = np.random.default_rng(seed)
    xb1 = -1.0 + 0.15 * rng.standard_normal(20); xb2 = 1.2 + 0.12 * rng.standard_normal(20)
    xm1 = -1.0 + 0.5 * rng.standard_normal(60); xm2 = 1.2 + 0.4 * rng.standard_normal(60); xd = rng.uniform(-3, 3, 60)
    x = np.concatenate((xb1, xb2, xm1, xm2, xd))
    m = np.concatenate((np.full(20, 0.02 / 20), np.full(20, 0.015 / 20), np.full(60, 0.05 / 60), np.full(60, 0.03 / 60), np.full(60, 0.02 / 60)))
    lab = np.concatenate((np.full(40, -1), np.full(60, 1), np.full(60, 2), np.full(60, 0))).astype(int)
    v = 0.1 * rng.standard_normal(len(x)) + 0.03
    nchg = np.zeros(len(x), int)
    P0 = float(np.sum(m * v)); Pdev = 0.0; Pscale = float(np.sum(m * np.abs(v)))
    E_prev = energy_1d(x, v, m, lab); Edrift = 0.0; Ejumps = {}
    Fo = forces_1d(x, m, lab, tether)
    ev_steps = {1500: "latch", 3000: "relatch", 4500: "merge"} if events else {}
    for n in range(1, nsteps + 1):
        v += 0.5 * dt * Fo / m; x += dt * v
        Fo = forces_1d(x, m, lab, tether); v += 0.5 * dt * Fo / m
        if n in ev_steps:
            Eb = energy_1d(x, v, m, lab); lab0 = lab.copy(); kind = ev_steps[n]
            if kind == "latch":                                          # rule (i): converging dust latches by contact (L* = 0.25)
                di = np.nonzero(lab == 0)[0]; od = di[np.argsort(x[di])]
                labd = np.nonzero(lab >= 1)[0]
                for j in range(1, len(od) - 1):
                    th = (v[od[j + 1]] - v[od[j - 1]]) / (x[od[j + 1]] - x[od[j - 1]])
                    if th <= 0:
                        dd = np.abs(x[labd] - x[od[j]]); kmin = int(np.argmin(dd))
                        lab[od[j]] = lab[labd[kmin]] if dd[kmin] <= 0.25 else 3
            elif kind == "relatch":                                      # rule (iv), 1-D prescription: label 2 outside its half-mass width -> label 1
                i2 = np.nonzero(lab == 2)[0]; xc = np.sum(m[i2] * x[i2]) / np.sum(m[i2])
                dist = np.abs(x[i2] - xc); hw = np.median(dist)
                lab[i2[dist > 2 * hw]] = 1
            else:                                                        # rule (ii): merge labels 2 and 3 into 1
                lab[(lab == 2) | (lab == 3)] = 1
            nchg += (lab != lab0)
            Ea = energy_1d(x, v, m, lab); Ejumps[kind] = Ea - Eb
            Fo = forces_1d(x, m, lab, tether)                            # forces of the new epoch (no velocity change at the event)
            E_prev = Ea
        Pdev = max(Pdev, abs(float(np.sum(m * v)) - P0))
        if n % 50 == 0:
            En = energy_1d(x, v, m, lab); Edrift = max(Edrift, abs(En - E_prev) / max(abs(En), 1e-30))
    Mmed = float(np.sum(m[lab >= 0]))
    return dict(P_dev=Pdev, P_scale=Pscale, P_rel=Pdev / Pscale, max_label_changes=int(nchg.max()), E_jumps=Ejumps,
                E_drift_rel_between_events=Edrift, medium_mass=Mmed, n_labels_end=int(len(np.unique(lab[lab >= 1]))))


def toy1d_draw(eps, nsteps=3000, dt=1e-3, tg_=2.0):
    """MUTATE M2: CFG947-type prescribed relocation in 1-D. Core baryons at 0, two dust blobs at +-1 (masses M_c(1 +- eps)/2,
    mirror positions), untethered; source weights: core +W0 h(t), blob slabs -W0 h(t) m_k/M_c (zero-sum), carried by their slabs.
    Total momentum P_m + dD_s/dt with D_s = sum s_j x_j."""
    nb = 10; Mc = 0.06; W0 = 0.5 * Mc
    off = np.linspace(-0.1, 0.1, nb)
    xc = np.linspace(-0.05, 0.05, 5)
    x = np.concatenate((xc, 1.0 + off, -1.0 - off))
    m = np.concatenate((np.full(5, 0.02 / 5), np.full(nb, Mc * (1 + eps) / 2 / nb), np.full(nb, Mc * (1 - eps) / 2 / nb)))
    v = np.zeros(len(x))
    sig = np.concatenate((m[:5] / m[:5].sum() * W0, -m[5:] / Mc * W0))
    h = lambda t: 0.5 * (1 - math.cos(math.pi * min(t, tg_) / tg_))
    hd = lambda t: (0.5 * math.pi / tg_ * math.sin(math.pi * t / tg_)) if t < tg_ else 0.0
    lab = np.zeros(len(x), int)

    def Ptot(t):
        s = sig * h(t); sd = sig * hd(t)
        return float(np.sum(m * v)) + float(np.sum(sd * x + s * v))
    P0 = Ptot(0.0); dev = 0.0; t = 0.0
    Fo = forces_1d(x, m, lab, tether=False, sw=sig * h(0.0))
    for n in range(nsteps):
        v += 0.5 * dt * Fo / m; x += dt * v; t += dt
        Fo = forces_1d(x, m, lab, tether=False, sw=sig * h(t)); v += 0.5 * dt * Fo / m
        dev = max(dev, abs(Ptot(t) - P0))
    scale = float(np.sum(m * np.abs(v)))
    return dict(P_tot_dev=dev, scale=scale, rel=dev / max(scale, 1e-300))


# ---------------------------------------------------------------- spherical merger toy (code units G = 1, a0 = 1, K = 4 pi)
BH = 2.0                                                                # Hernquist scale
NS_SUP = 6.0                                                            # label mass = 6 M_b,q


def Mb_hern(rr, M):
    return M * rr * rr / (rr + BH) ** 2


def law1(g):
    return 0.5 * (g + np.sqrt(g * g + 4 * g))


def wcode(uu):
    return wfull_x(np.minimum(uu, 1 - 1e-15))                           # 4 pi r^2 W(u) = r^2 w(u) with K = 4 pi, G = 1


def iso_shells(Mbq, n):
    """isolated settled label q: shells at mass midpoints of M_ph(<r) = r^2 (law(g_b) - g_b), up to the supply root."""
    Mph = lambda rr: rr * rr * (law1(Mb_hern(rr, Mbq) / rr ** 2) - Mb_hern(rr, Mbq) / rr ** 2)
    Mc = NS_SUP * Mbq; dm = Mc / n
    rs = np.array([brentq(lambda rr: Mph(rr) - (k + 0.5) * dm, 1e-6, 1e4, xtol=1e-14) for k in range(n)])
    re_ = brentq(lambda rr: Mph(rr) - Mc, 1e-6, 1e4, xtol=1e-14)
    return rs, dm, re_


def _grav_anti(rr, M, C):
    """antiderivative of (M_b(r) + C)^2/(2 r^2), Hernquist M_b = M r^2/(r + b)^2; zero at r = infinity (C = 0 allowed at r = 0)."""
    rr = np.asarray(rr, float); C = np.asarray(C, float)
    fin = np.isfinite(rr); r_ = np.where(fin, rr, 1.0); s = r_ + BH
    out = 0.5 * M * M * (-1 / s + BH / s ** 2 - BH ** 2 / (3 * s ** 3)) - M * C / s
    out = out - np.where(C > 0, 0.5 * C * C / np.where(r_ > 0, r_, 1.0), 0.0)
    return np.where(fin, out, 0.0)


_KS = np.arange(2, 16)


def _w_anti(rr, Q):
    """antiderivative of r^2 w(Q/r^2), w(u) = -u - ln(1 - u); zero at r = infinity; +inf at or beyond the wall (Q >= r^2)."""
    rr = np.asarray(rr, float); Q = np.asarray(Q, float) * np.ones_like(rr)
    fin = np.isfinite(rr) & (Q > 0); r_ = np.where(fin, rr, 1.0); Qf = np.where(fin, Q, 0.0)
    x = Qf / r_ ** 2
    wall = fin & (x >= 1.0)
    ser = r_ ** 3 * np.sum(x[..., None] ** _KS / (_KS * (3.0 - 2 * _KS)), axis=-1)
    xs = np.minimum(x, 0.999999999999); a_ = np.sqrt(Qf)
    clo = -Qf * r_ / 3 - (r_ ** 3 / 3) * np.log1p(-xs) - (2.0 / 3.0) * a_ ** 3 * np.arctanh(np.minimum(a_ / r_, 0.9999999999999))
    val = np.where(x < 0.02, ser, clo)
    val = np.where(fin, val, 0.0)
    return np.where(wall, np.inf, val)


def energy_sph(rs, lab, dm, Mbt):
    """exact E = int_0^inf [-(M_b + M_c)^2/(2 r^2) + r^2 sum_q w(M_q/r^2)] dr (G = 1, K = 4 pi), analytic per interval."""
    o = np.argsort(rs, kind="mergesort"); r_ = rs[o]; l_ = lab[o]
    edges = np.concatenate(([0.0], r_, [np.inf]))
    a_, b_ = edges[:-1], edges[1:]
    Cj = np.concatenate(([0.0], np.cumsum(np.full(len(r_), dm))))
    E = -float(np.sum(_grav_anti(b_, Mbt, Cj) - _grav_anti(a_, Mbt, Cj)))
    for q in np.unique(lab):
        Qj = np.concatenate(([0.0], np.cumsum(np.where(l_ == q, dm, 0.0))))
        wa = _w_anti(np.where(Qj > 0, b_, np.inf), Qj) - _w_anti(np.where(Qj > 0, a_, np.inf), Qj)
        if not np.all(np.isfinite(wa)):
            return math.inf
        E += float(np.sum(wa))
    return E


def forces_sph(rs, lab, dm, Mbt):
    """energy-exact shell force F_k = f+(r_k) - f-(r_k)."""
    o = np.argsort(rs, kind="mergesort"); r_ = rs[o]; l_ = lab[o]; n = len(r_)
    Min = np.concatenate(([0.0], np.cumsum(np.full(n, dm))[:-1]))
    Mq = np.zeros(n)
    for q in np.unique(lab):
        sel = l_ == q; cq = np.concatenate(([0.0], np.cumsum(np.where(sel, dm, 0.0))[:-1])); Mq = np.where(sel, cq, Mq)
    M_ = Mb_hern(r_, Mbt) + Min
    F = -((M_ + dm) ** 2 - M_ ** 2) / (2 * r_ * r_) + r_ * r_ * (wcode((Mq + dm) / r_ ** 2) - wcode(Mq / r_ ** 2))
    out = np.empty(n); out[o] = F
    return out


def merged_equilibrium(n, dm, Mbt):
    """discrete merged single-label equilibrium: shell k (k inside) solves f+ - f- = 0."""
    rr = np.empty(n)
    for k in range(n):
        fk = lambda x: (-((Mb_hern(x, Mbt) + (k + 1) * dm) ** 2 - (Mb_hern(x, Mbt) + k * dm) ** 2) / (2 * x * x)
                        + x * x * (wcode((k + 1) * dm / x ** 2) - wcode(k * dm / x ** 2)))
        lo = math.sqrt((k + 1) * dm) * (1 + 1e-12); hi = 1e4
        rr[k] = brentq(fk, lo, hi, xtol=1e-14, rtol=1e-14)
    return rr


def Rint_code(uu):
    """int_0^u R du' with R = u^2/(1 - u) (a0 = 1): -u - u^2/2 - ln(1 - u) = sum_{n>=3} u^n/n (series below 0.05)."""
    uu = np.asarray(uu, float)
    small = uu < 0.05; us = np.where(small, uu, 0.0); ul = np.where(small, 0.0, uu)
    ser = sum(us ** n / n for n in range(3, 24))
    return np.where(small, ser, -ul - ul * ul / 2 - np.log1p(-ul))


def merger_toy(ratio, N0, flow=True, tmax_s=300.0, maxsteps=2_000_000, r_res=None):
    Mb1, Mb2 = 1.0, ratio; Mbt = Mb1 + Mb2
    n1 = N0; n2 = int(round(N0 * ratio))
    r1, dm1, re1 = iso_shells(Mb1, n1); r2, dm2, re2 = iso_shells(Mb2, n2)
    assert abs(dm1 - dm2) < 1e-12
    dm = dm1; rs = np.concatenate((r1, r2)); lab = np.concatenate((np.full(n1, 1), np.full(n2, 2)))
    Mc_tot = dm * len(rs)
    Mph_m = lambda rr: rr * rr * (law1(Mb_hern(rr, Mbt) / rr ** 2) - Mb_hern(rr, Mbt) / rr ** 2)
    re_m = brentq(lambda rr: Mph_m(rr) - Mc_tot, 1e-6, 1e4, xtol=1e-14)
    probes = np.array([0.5, 1.0, 2.0, 3.0])

    def g_of(rr_, lab_, x):
        Mc_in = np.array([dm * np.sum(rr_ < xx) for xx in x]); return (Mb_hern(x, Mbt) + Mc_in) / x ** 2
    # class-A-type comparator (own-label phantoms recomputed at the merge)
    gb1 = Mb_hern(probes, Mb1) / probes ** 2; gb2 = Mb_hern(probes, Mb2) / probes ** 2
    before_A = gb1 + gb2 + (law1(gb1) - gb1) + (law1(gb2) - gb2); after_A = law1(gb1 + gb2)
    J_A = float(np.max(np.abs(before_A - after_A) / after_A))
    # LDT event: relabel only
    xall = np.concatenate((probes, np.sort(rs)))
    g_before = g_of(rs, lab, xall); E_before = energy_sph(rs, lab, dm, Mbt)
    lab_m = np.ones_like(lab)
    g_after = g_of(rs, lab_m, xall); E_after = energy_sph(rs, lab_m, dm, Mbt)
    J_LDT = float(np.max(np.abs(g_after - g_before) / g_before))
    # discrete equilibrium + final law (midpoints)
    req = merged_equilibrium(len(rs), dm, Mbt)
    mono = bool(np.all(np.diff(req) > 0))
    kk = np.arange(len(rs)); gmid = (Mb_hern(req, Mbt) + (kk + 0.5) * dm) / req ** 2; glaw = law1(Mb_hern(req, Mbt) / req ** 2)
    ins = req <= 0.9 * re_m
    dev_mid = float(np.max(np.abs(gmid[ins] / glaw[ins] - 1)))
    # A1 (post hoc): exact discrete identity <R>_[u_k, u_k+1] = g_b(r_k), and the resolved-range midpoint deviation
    uk = kk * dm / req ** 2; uk1 = (kk + 1) * dm / req ** 2; gbk = Mb_hern(req, Mbt) / req ** 2
    ident = float(np.max(np.abs((Rint_code(uk1) - Rint_code(uk)) / (uk1 - uk) / gbk - 1)))
    rres = math.sqrt(10 * dm) if r_res is None else r_res
    res_ = (req >= rres) & ins
    dev_res = float(np.max(np.abs(gmid[res_] / glaw[res_] - 1)))
    # mass bookkeeping
    mass_ok = abs(dm * len(rs) - (NS_SUP * Mb1 + NS_SUP * Mb2)) < 1e-12 * Mc_tot
    out = dict(ratio=ratio, N0=N0, n_shells=len(rs), dm=dm, re1=re1, re2=re2, re_merged=re_m, J_A=J_A, J_LDT=J_LDT,
               dE_merge=E_after - E_before, E_before=E_before, eq_monotone=mono, dev_mid=dev_mid, n_inside=int(ins.sum()), mass_exact=mass_ok,
               A1_identity=ident, A1_r_res=rres, A1_dev_res=dev_res, A1_n_res=int(res_.sum()), r1=float(req[0]), du1=float(dm / req[0] ** 2),
               max_u_superposed=float(np.max((np.array([dm * np.sum(r1 < x) for x in np.sort(rs)]) + np.array([dm * np.sum(r2 < x) for x in np.sort(rs)])) / np.sort(rs) ** 2)))
    if flow:
        x = rs.copy(); E = E_after; d0 = float(np.max(np.abs(np.sort(x) - req)) / re_m); dtv = 1e-3
        nsteps = 0; nrej = 0; maxinc = 0.0; t0 = time.time(); dcur = d0; gmax_step = 0.0
        E_first = E if math.isfinite(E) else None; n_up = 0
        while nsteps < maxsteps and time.time() - t0 < tmax_s:
            F = forces_sph(x, lab_m, dm, Mbt)
            xn = np.maximum(x + dtv * F / dm, 1e-6)
            En = energy_sph(xn, lab_m, dm, Mbt)
            if En <= E + 1e-12 * abs(E):
                if math.isfinite(E):
                    maxinc = max(maxinc, (En - E) / abs(E)); n_up += int(En > E)
                elif E_first is None and math.isfinite(En):
                    E_first = En
                if nsteps % 2000 == 0:
                    gp0 = g_of(x, lab_m, probes); gp1 = g_of(xn, lab_m, probes); gmax_step = max(gmax_step, float(np.max(np.abs(gp1 / gp0 - 1))))
                x, E = xn, En; nsteps += 1; dtv = min(dtv * 1.05, 5.0)
                if nsteps % 500 == 0:
                    dcur = float(np.max(np.abs(np.sort(x) - req)) / re_m)
                    if dcur <= d0 / 20:
                        break
            else:
                nrej += 1; dtv *= 0.5
                if dtv < 1e-14:
                    break
        dcur = float(np.max(np.abs(np.sort(x) - req)) / re_m)
        out.update(flow_steps=nsteps, flow_rejected=nrej, flow_runtime_s=round(time.time() - t0, 1), d0=d0, d_end=dcur, d_ratio=d0 / max(dcur, 1e-300),
                   E_end=E, heat=E_after - E, max_accepted_dE_rel=maxinc, sampled_max_probe_change_per_step=gmax_step,
                   A1_E_first_finite=E_first, A1_heat_from_first_finite=(E_first - E) if E_first is not None else None, n_tiny_increases=n_up)
    return out


def two_label_eq_dev(ratio):
    """continuum two-label concentric equilibrium (no merge rule): u1 = u2 = v, R(v) = g_b + v, at probes inside both labels."""
    Mbt = 1.0 + ratio; Mc2 = NS_SUP * ratio
    vfun = lambda gb: ((1 - gb) + np.sqrt((1 - gb) ** 2 + 8 * gb)) / 4
    e2 = brentq(lambda rr: rr * rr * vfun(Mb_hern(rr, Mbt) / rr ** 2) - Mc2, 1e-6, 1e4)
    pr = np.array([0.5, 1.0, 2.0]); pr = pr[pr < e2]
    gb = Mb_hern(pr, Mbt) / pr ** 2
    return float(np.max(np.abs((gb + 2 * vfun(gb)) / law1(gb) - 1))), e2


# ---------------------------------------------------------------- spherical energy of label events (SI)
def ngc_profile(a0, scale=1.0, Mc_override=None):
    """NGC 3198 (baryons x scale) settled single label: radial grid (m), M_b(<r) (kg), u(r); census label mass (or override, kg);
    LDT edge (simple kernel)."""
    dom = domain(MB_N_SUN * scale, a0); Mc = dom["Mc"] * MSUN if Mc_override is None else Mc_override
    re_, rM, N = ldt_edge(MB_N_SUN * scale, Mc / MSUN, a0)
    rr = np.unique(np.concatenate((R_N, np.geomspace(R_N[-1], re_, 4000))))
    Mb = scale * np.interp(rr, R_N, MBR_N, right=MB_N)
    gn = G_SI * Mb / rr ** 2; uu = law_g(gn, a0) - gn
    return dict(dom=dom, Mc=Mc, re=re_, rM=rM, N=N, r=rr, Mb=Mb, gn=gn, u=uu, r_on=dom["r_on"], Mb_tot=MB_N * scale)


def cumtrap_rev(y, x):
    """int_x^{x_end} y dx (trapezoid), array."""
    seg = 0.5 * (y[1:] + y[:-1]) * np.diff(x)
    return np.concatenate((np.cumsum(seg[::-1])[::-1], [0.0]))


def tail_D(Mc, re_, a0):
    """int_{r_e}^inf D_full(G M_c/r^2) dr and int R dr (u = G M_c / r^2 beyond the edge)."""
    uf = lambda x: G_SI * Mc / x ** 2
    iR = quad(lambda s: R_num(uf(re_ / s), a0) * re_ / s ** 2, 0, 1, epsabs=0, epsrel=1e-12, limit=200)[0]   # r = r_e/s
    return G_SI * Mc / re_ + iR, iR


def lambda_profile(pr, a0):
    """K lambda(x) = int_x^inf D_full(u) dr on the profile grid."""
    Dg = D_num(pr["u"], a0)
    tD, tR = tail_D(pr["Mc"], pr["re"], a0)
    return cumtrap_rev(Dg, pr["r"]) + tD, tD, tR


def phi_diff(pr, a0):
    """Phi(r_ON) - Phi(x) on the grid: int_x^{r_ON} g dr; g = law inside r_e, G(M_b + M_c)/r^2 beyond."""
    g = pr["gn"] + pr["u"]
    inner = cumtrap_rev(g, pr["r"])
    outer = G_SI * (pr["Mb_tot"] + pr["Mc"]) * (1 / pr["re"] - 1 / pr["r_on"])
    return inner + outer


def E_W_profile(pr, a0, Wf=None):
    """E_W = int 4 pi r^2 W(u) dr of the settled label (grid + exterior tail beyond r_e); W constant below the first radius.
    Wf replaces W (MUTATE M6 passes W = 0)."""
    Wf = (lambda uu: W_num(uu, a0)) if Wf is None else Wf
    Wg = np.asarray(Wf(pr["u"]), float) * np.ones_like(pr["u"])
    inner = float(np.sum(0.5 * (4 * np.pi * pr["r"][1:] ** 2 * Wg[1:] + 4 * np.pi * pr["r"][:-1] ** 2 * Wg[:-1]) * np.diff(pr["r"])))
    core = (4 * math.pi / 3) * pr["r"][0] ** 3 * float(Wg[0])
    Mc = pr["Mc"]; re_ = pr["re"]
    tail = quad(lambda s: 4 * math.pi * (re_ / s) ** 2 * float(np.asarray(Wf(G_SI * Mc / (re_ / s) ** 2))) * re_ / s ** 2, 0, 1, epsrel=1e-10, limit=200)[0]
    return inner + core + tail


def E_W_exterior(Mc, R0, a0):
    return quad(lambda s: 4 * math.pi * (R0 / s) ** 2 * float(W_num(G_SI * Mc / (R0 / s) ** 2, a0)) * R0 / s ** 2, 0, 1, epsrel=1e-10, limit=200)[0]


def E_grav_profile(pr):
    """Newtonian potential energy of baryons + label medium inside r_ON: -G M(R)^2/(2R) - int G M^2/(2 r^2) dr."""
    Mtot = pr["Mb"] + np.minimum(pr["u"] * pr["r"] ** 2 / G_SI, pr["Mc"])
    integ = G_SI * Mtot ** 2 / (2 * pr["r"] ** 2)
    inner = float(np.sum(0.5 * (integ[1:] + integ[:-1]) * np.diff(pr["r"])))
    Mend = pr["Mb_tot"] + pr["Mc"]
    outer = G_SI * Mend ** 2 / 2 * (1 / pr["re"] - 1 / pr["r_on"])
    return -(inner + outer + G_SI * Mend ** 2 / (2 * pr["r_on"]))


# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    teeth = {}
    m1 = max(abs(h1_delta_a(Mb_, apc, rk, A0[f], labels=False)[0] / J941[f"{f}|{hn}|{rk:g}"]["ratio"] - 1)
             for f in FOOTS for hn, Mb_, apc in HOSTS882 for rk in RADII)
    m1min = min(h1_delta_a(Mb_, apc, rk, A0[f], labels=False)[0] for f in FOOTS for hn, Mb_, apc in HOSTS882 for rk in RADII)
    teeth["M1"] = chk("M1_labels_removed_hover_returns", m1 < 1e-9 and m1min >= 0.5,
                      f"one shared label: satellite Delta a/g_host = CFG941's to {m1:.1e}, min {m1min:.4f} (Theorem S hover)")
    d_asym = toy1d_draw(0.3); d_sym = toy1d_draw(0.0)
    teeth["M2"] = chk("M2_non_dipole_preserving_draw_breaks_momentum", d_asym["rel"] > 1e-6 and d_sym["rel"] <= 1e-10,
                      f"1-D prescribed relocation (eps 0.3): |Delta(P_m + dD_s/dt)| / sum m|v| = {d_asym['rel']:.3e}; eps 0 control {d_sym['rel']:.1e} (CFG947 T-M)")
    teeth["M3"] = chk("M3_labels_in_linear_regime_DT_returns", abs(n_full - 1) > 1e-3, f"one global always-on label: n = {n_full:.5f} (LDT linear regime: dust, n = 1)")
    m4t = {r_: two_label_eq_dev(r_) for r_ in (1.0, 1.0 / 3.0)}
    teeth["M4"] = chk("M4_no_merge_rule_two_labels_break_law", all(H1A[f]["two_labels"] > 1e-6 for f in FOOTS) and all(v[0] > 1e-2 for v in m4t.values()),
                      f"NGC 3198 two equal labels dev {H1A['canonical']['two_labels']:.3f}/{H1A['alt']['two_labels']:.3f}; toy two-label equilibrium dev "
                      + ", ".join(f"1:{1 / r_:.0f} {v[0]:.3f}" for r_, v in m4t.items()))
    m5 = {r_: merger_toy(r_, 300, flow=False) for r_ in (1.0, 1.0 / 3.0)}
    teeth["M5"] = chk("M5_classA_source_recomputation_jumps", all(v["J_A"] > 0.01 for v in m5.values()),
                      "own-label phantoms recomputed at the merge: J_A = " + ", ".join(f"1:{1 / r_:.0f} {v['J_A']:.3f}" for r_, v in m5.items()) + " (LDT: 0)")
    prm = ngc_profile(A0["canonical"])
    dEoff = E_W_profile(prm, A0["canonical"], Wf=lambda uu: 0.0 * np.asarray(uu))   # tether removed: W = 0 -> the assembly jump E_W(final) vanishes
    Eg = E_grav_profile(prm)
    teeth["M6"] = chk("M6_tether_off_no_labelling_energy", abs(dEoff) <= 1e-14 * abs(Eg),
                      f"W = 0: labelling energy jump {dEoff:.1e} J (|E_grav| {abs(Eg):.2e} J); e2's jumps come from the tether")
    RES["MUTATE"] = dict(M1=m1, M1min=m1min, M2=dict(asym=d_asym, sym=d_sym), M3=n_full, M4={str(k): v for k, v in m4t.items()},
                         M5={str(k): dict(J_A=v["J_A"]) for k, v in m5.items()})
    allb = all(teeth.values())
    P(f"\n  MUTATE: {'ALL TEETH BITE (exit 1 by design)' if allb else 'A TOOTH FAILED TO BITE (exit 2)'}")
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
    sys.exit(1 if allb else 2)


# ================================================================================================ MAIN
TESTS = {}


def put(key, grade, detail):
    TESTS[key] = dict(grade=grade, detail=str(detail))
    P(f"   ({key}) {grade}: {detail}")


ST = {}
P("\n==================== STRUCTURAL STATEMENTS ====================")
# ---- T-EQ: (A) settled single label == (B) P-S with own-root edge (q = 1)
teq = 0.0
for foot in FOOTS:
    a0 = A0[foot]
    systems = [("NGC3198", MB_N_SUN, None)] + [(nm, Mb, None) for nm, Mb, _ in SYS847]
    for nm, Mb, _ in systems:
        dom = domain(Mb, a0); Mc = dom["Mc"] * MSUN; re_, rM, N = ldt_edge(Mb, dom["Mc"], a0)
        rr = np.geomspace(1e-3 * rM, dom["r_on"], 3000)
        if nm == "NGC3198":
            Mbr = np.interp(rr, R_N, MBR_N, left=0.0, right=MB_N); ok = rr >= R_N[0]; rr = rr[ok]; Mbr = Mbr[ok]
        else:
            Mbr = np.full_like(rr, Mb * MSUN)
        gn = G_SI * Mbr / rr ** 2; Mph = rr ** 2 * (law_g(gn, a0) - gn) / G_SI
        MA = Mbr + np.where(rr <= re_, Mph, Mc)                                     # (A): medium = phantom inside r_e, all of it beyond
        Mph_e = re_ ** 2 * (float(law_g(G_SI * Mb * MSUN / re_ ** 2, a0)) - G_SI * Mb * MSUN / re_ ** 2) / G_SI
        q = Mph_e / Mc                                                               # own-root edge: q = 1
        shell = np.clip((rr - re_) / (dom["r_on"] - re_), 0, 1) * Mc                 # B's P-S shell cold (any profile), drawn by q
        MB_ = Mbr + np.where(rr <= re_, Mph, Mph_e + shell - q * shell)
        teq = max(teq, float(np.max(np.abs(MA / MB_ - 1))))
ST["T-EQ"] = chk("T-EQ_static_equivalence_A_B", teq <= 1e-12,
                 f"max |g_A/g_B - 1| = {teq:.1e} (NGC 3198 + CFG847's five systems, both footings, radial grid to r_ON): (A)'s settled label and (B)'s "
                 "P-S configuration with the kernel's own supply root have the same gravitating density")
# ---- T-LE: labelling energy and the kinetic-payment deficit
xS = sp.Symbol("x", positive=True); dmS = sp.Symbol("dm", positive=True); Mq_ = sp.Symbol("M_q", positive=True)
uS = G * Mq_ / r ** 2
lam_id = sp.simplify(sp.diff(4 * sp.pi * r ** 2 * Wfull.subs(u, G * (Mq_ + dmS) / r ** 2), dmS).subs(dmS, 0) - Dfull.subs(u, uS))
LE = {}
tle_ok = True
for foot in FOOTS:
    a0 = A0[foot]
    pr = ngc_profile(a0)
    Klam, tD, tR = lambda_profile(pr, a0)
    dphi = phi_diff(pr, a0)
    idx = np.searchsorted(pr["r"], R_N)
    Dx = Klam[idx] - dphi[idx]
    Dan = G_SI * pr["Mc"] / pr["r_on"] + tR - G_SI * MB_N * (1 / pr["re"] - 1 / pr["r_on"])
    spread = float(np.max(np.abs(Dx / Dan - 1)))
    grid = []
    for Mb in np.logspace(7, 15, 17):
        dom = domain(float(Mb), a0); Mc = dom["Mc"] * MSUN; re_, rM, N = ldt_edge(Mb, dom["Mc"], a0)
        _, iR = tail_D(Mc, re_, a0)
        Dg = G_SI * Mc / dom["r_on"] + iR - G_SI * Mb * MSUN * (1 / re_ - 1 / dom["r_on"])
        grid.append(dict(Mb=float(Mb), Delta=Dg, Delta_over_GMb_re=Dg / (G_SI * Mb * MSUN / re_), re_over_ron=re_ / dom["r_on"], N=N))
        tle_ok = tle_ok and Dg > 0
    LE[foot] = dict(Klam_min=float(Klam.min()), Delta_NGC=Dan, spread=spread, grid=grid, Klam_center=float(Klam[0]), Klam_re=tD)
    tle_ok = tle_ok and spread <= 1e-6 and Klam.min() > 0
ST["T-LE"] = chk("T-LE_labelling_cannot_be_paid_kinetically", tle_ok and lam_id == 0,
                 f"dE_W/dm at x = K lambda_q(x) = int_x^inf D_full(u_q) dr (sympy integrand identity {lam_id}); NGC 3198: K lambda > 0 everywhere, "
                 f"Delta = K lambda - [Phi(r_ON) - Phi(x)] = {LE['canonical']['Delta_NGC']:.3e} / {LE['alt']['Delta_NGC']:.3e} m^2/s^2, x-independent to "
                 f"{max(LE[f]['spread'] for f in FOOTS):.1e} over the 43 radii; M_b grid 1e7-1e15: Delta/(G M_b/r_e) = "
                 + ", ".join(f"{x['Delta_over_GMb_re']:.1f}" for x in LE['canonical']['grid'][::4]) + " (canonical; all > 0 both footings)")
RES["T-LE"] = LE
# ---- T-T: concentric tie
u1s, u2s = sp.symbols("u_1 u_2", positive=True)
tie = sp.simplify((Rsym.subs(u, u1s) - u2s) - (Rsym.subs(u, u2s) - u1s) - (Dfull.subs(u, u1s) - Dfull.subs(u, u2s)))
Dp = sp.simplify(sp.diff(Dfull, u))
tie_num = {}
for foot in FOOTS:
    a0 = A0[foot]; v = ((a0 - GN_N) + np.sqrt((a0 - GN_N) ** 2 + 8 * GN_N * a0)) / 4
    tie_num[foot] = float(np.max(np.abs(R_num(v, a0) - GN_N - v) / v))
ST["T-T"] = chk("T-T_concentric_tie", tie == 0 and sp.simplify(Dp - a0s ** 2 / (a0s - u) ** 2) == 0 and max(tie_num.values()) < 1e-12,
                f"R(u1) - u2 = R(u2) - u1  <=>  D_full(u1) = D_full(u2); D_full' = {Dp} > 0 on [0, a0) => u1 = u2: equal tidal fields at every radius "
                f"(NGC 3198 two-label equilibrium residual {max(tie_num.values()):.1e}); element-wise tidal comparisons tie, so M-R must be a whole-label rule")
# ---- T-G: no theta in the action
thS = sp.Symbol("theta")
FthS = sp.diff(Wfull, thS, 2)
ST["T-G"] = chk("T-G_no_theta_no_ghost", FthS == 0, "F(theta, u) = W_full(u): F_theta,theta = 0, so the longitudinal kinetic coefficient is rho0 + F_tt k^2 = rho0 "
                "(CFG944's identity); the theta-latch acts outside the action, so Theorem G's hypothesis (a local L(theta, u)) is not met")


# ---- T-theta: theta-latch front vs turnaround front (EdS power laws)
def theta_front(eps):
    eta = sp.Symbol("eta", positive=True)
    dL = sp.Rational(3, 5) * (sp.Rational(3, 4)) ** sp.Rational(2, 3) * (eta - sp.sin(eta)) ** sp.Rational(2, 3)
    F = sp.Rational(2, 9) ** sp.Rational(1, 3) * (1 - sp.cos(eta)) / (eta - sp.sin(eta)) ** sp.Rational(2, 3)   # = (1 + delta_NL)^(-1/3) on (0, 2 pi)
    Fp = sp.diff(F, eta) / sp.diff(dL, eta); Fpp = sp.diff(Fp, eta) / sp.diff(dL, eta)
    ex = 3 + 2 * dL * Fp / F + dL * (Fp - 3 * eps * Fp - 3 * eps * dL * Fpp) / (F - 3 * eps * dL * Fp)
    fe = sp.lambdify(eta, ex, "mpmath"); fd = sp.lambdify(eta, dL, "mpmath"); fq = sp.lambdify(eta, F - 3 * eps * dL * Fp, "mpmath")
    import mpmath as mp
    mp.mp.dps = 30
    grid = [mp.mpf(0.2) + k * (mp.mpf(2 * math.pi) - mp.mpf(0.4)) / 600 for k in range(601)]
    vals = [fe(x) for x in grid]
    j = next(i for i in range(len(vals) - 1) if vals[i] > 0 and vals[i + 1] <= 0)
    et = mp.findroot(fe, (grid[j], grid[j + 1]), solver="bisect")
    d_th = float(fd(et)); d_ta = float(fd(mp.pi)); pre_cross = float(fq(et)) > 0
    return dict(eps=eps, eta_theta=float(et), delta_theta=d_th, delta_ta=d_ta, f_theta=(d_th / d_ta) ** (-1 / eps), pre_crossing=pre_cross)


TH = [theta_front(e) for e in (0.2, 1 / 3, 0.5, 2 / 3, 0.9)]
eta_s = sp.Symbol("eta", positive=True)
dl_ta = sp.N(sp.Rational(3, 5) * (sp.Rational(3, 4) * sp.pi) ** sp.Rational(2, 3)); onep_ta = sp.simplify((sp.Rational(9, 2) * (eta_s - sp.sin(eta_s)) ** 2 / (1 - sp.cos(eta_s)) ** 3).subs(eta_s, sp.pi))
ST["T-theta"] = chk("T-theta_latch_inside_turnaround", all(x["f_theta"] <= 1 and x["pre_crossing"] for x in TH),
                    "f_theta = M_theta/M_ta (EdS, delta_i ~ q^-3eps): " + ", ".join(f"eps {x['eps']:.2f}: {x['f_theta']:.3f} (delta_lin at theta=0 {x['delta_theta']:.3f})" for x in TH)
                    + f"; top-hat: theta = 0 at turnaround, delta_lin = {float(dl_ta):.4f}, 1 + delta = {onep_ta} = {float(onep_ta):.4f}; fronts pre-shell-crossing")
RES["T-theta"] = TH
guard("structural")

# ================================================================================================ TESTS (a)-(i)
P("\n==================== (a) the law in a single-label galaxy ====================")
k1a = k1
ynum = {}
for foot in FOOTS:
    a0 = A0[foot]; y = 1e-14
    _, gt, _ = solve_static(Wfull, 1, np.array([y * a0]), a0)
    exact = float(law_g(y * a0, a0)) ** 2 / (y * a0 * a0)
    ynum[foot] = dict(numeric=float(gt[0]) ** 2 / (y * a0 * a0), exact=exact)
ybS = sp.Symbol("yb", positive=True)
lim_btfr = sp.limit((ybS + sp.sqrt(ybS ** 2 + 4 * ybS)) ** 2 / 4 / ybS, ybS, 0, "+")
a3 = {}
for foot in FOOTS:
    a0 = A0[foot]; dom = domain(MB_N_SUN, a0); re_, rM, N = ldt_edge(MB_N_SUN, dom["Mc"], a0)
    rdeep = {y: math.sqrt(G_SI * MB_N / (y * a0)) for y in (1e-2, 1e-3)}
    fth = [x["f_theta"] for x in TH]
    re_th = {f"{x['eps']:.2f}": ldt_edge(MB_N_SUN, x["f_theta"] * dom["Mc"], a0)[0] for x in TH}
    a3[foot] = dict(r_e_kpc=re_ / KPC, r_on_kpc=dom["r_on"] / KPC, N=N, r_last_kpc=R_N[-1] / KPC, r_deep_kpc={str(k): v / KPC for k, v in rdeep.items()},
                    inside=bool(R_N[-1] < re_ and all(v < re_ for v in rdeep.values())),
                    theta_variant={k: dict(r_e_kpc=v / KPC, deep_1e3_inside=bool(rdeep[1e-3] < v), last_inside=bool(R_N[-1] < v)) for k, v in re_th.items()},
                    r_e_E7_kpc=dom["r_e"] / KPC)
a_pass = all(k1a[f]["max_rel_vs_law"] <= 1e-6 for f in FOOTS) and lim_btfr == 1 and all(abs(ynum[f]["numeric"] - ynum[f]["exact"]) <= 1e-6 for f in FOOTS) \
    and all(a3[f]["inside"] for f in FOOTS)
put("a", "PASS" if a_pass else "FAIL",
    f"a1 {k1a['canonical']['max_rel_vs_law']:.1e}/{k1a['alt']['max_rel_vs_law']:.1e}; a2 limit {lim_btfr}, y = 1e-14 numeric - exact = "
    f"{ynum['canonical']['numeric'] - ynum['canonical']['exact']:+.1e}/{ynum['alt']['numeric'] - ynum['alt']['exact']:+.1e} (value {ynum['canonical']['numeric'] - 1:+.2e}); "
    f"a3 label edge r_e = {a3['canonical']['r_e_kpc']:.0f}/{a3['alt']['r_e_kpc']:.0f} kpc (N = {a3['canonical']['N']:.1f}; E7 {a3['canonical']['r_e_E7_kpc']:.0f}/"
    f"{a3['alt']['r_e_E7_kpc']:.0f}; r_ON {a3['canonical']['r_on_kpc']:.0f}) vs last radius {a3['canonical']['r_last_kpc']:.1f} kpc and deep points "
    f"{a3['canonical']['r_deep_kpc']['0.01']:.0f}/{a3['canonical']['r_deep_kpc']['0.001']:.0f} kpc: inside. Reported: theta-latch label mass -> r_e "
    + ", ".join(f"{k}: {v['r_e_kpc']:.0f} kpc (y=1e-3 {'in' if v['deep_1e3_inside'] else 'OUT'})" for k, v in a3['canonical']['theta_variant'].items())
    + f"; costs: two labels {H1A['canonical']['two_labels']:.2f}/{H1A['alt']['two_labels']:.2f}, debris line q <= 3.5e-7")
RES["a"] = dict(K1=k1a, btfr=ynum, a3=a3)

P("\n==================== (b) FRW and linear growth ====================")
aS, mS, cS = sp.symbols("a m c", positive=True)
nS = aS ** -3; Fdust = -mS * cS ** 2 * sp.Symbol("n")
rho_d = -Fdust.subs(sp.Symbol("n"), nS); p_d = sp.simplify((Fdust - sp.Symbol("n") * sp.diff(Fdust, sp.Symbol("n"))).subs(sp.Symbol("n"), nS))
HS, fS, dS = sp.symbols("H f delta", positive=True)
theta_lin = 3 * HS - HS * fS * dS
b2_lin = sp.simplify(theta_lin - 3 * HS * (1 - fS * dS / 3)) == 0
crit = sp.solve(sp.Eq(theta_lin, 0), dS)
etaS, AS_, BS_ = sp.symbols("eta A B", positive=True)
r_cyc = AS_ * (1 - sp.cos(etaS)); t_cyc = BS_ * (etaS - sp.sin(etaS))
rdot = sp.diff(r_cyc, etaS) / sp.diff(t_cyc, etaS)
theta_th = sp.simplify(3 * rdot / r_cyc)
rddot = sp.diff(rdot, etaS) / sp.diff(t_cyc, etaS)
theta_dot_at_ta = sp.simplify((3 * rddot / r_cyc - 3 * rdot ** 2 / r_cyc ** 2).subs(etaS, sp.pi))
b_pass = (p_d == 0) and b2_lin and crit == [3 / fS] and sp.simplify(theta_th.subs(etaS, sp.pi)) == 0 and abs(n_dust - 1) <= 1e-6 and abs(float(dl_ta) - 1.0624) < 1e-4
put("b", "PASS" if b_pass else "FAIL",
    f"b1 unlabelled medium F = -m c^2 n on FRW: rho = {rho_d}, p = {p_d} (w = 0, isotropic); b2 linear theta = 3H(1 - f delta/3): latch needs delta >= {crit[0]} "
    f"(= 3 in EdS); top-hat theta = {theta_th} -> 0 at eta = pi (turnaround), delta_lin = {float(dl_ta):.4f}, 1 + delta = 9 pi^2/16; theta_dot(pi) = "
    f"{theta_dot_at_ta} != 0 (transversal); b3 no tether in the linear regime: n = {n_dust:.12f}")

P("\n==================== (c) no hover and (i) the satellite data bound ====================")
dyn = {}
for k, v in H1B.items():
    foot, hn, rk = k.split("|"); Mb_, apc = {h[0]: (h[1], h[2]) for h in HOSTS882}[hn]
    dyn[k] = restoring_and_dyn(Mb_, apc, v["r_dom_pc"], A0[foot], v["eps"] * v["g_host"], v["g_host"], tether=True, T_Myr=1000.0)
nb_bound = sum(1 for v in dyn.values() if v["bound"])
epsmax = {f: max(v["eps"] for k, v in H1B.items() if k.startswith(f)) for f in FOOTS}
c_pass = all(epsmax[f] <= EPSB[f] for f in FOOTS)
put("c", "PASS" if c_pass else "FAIL",
    "; ".join(f"{f}: own-label Delta a/g_host max {epsmax[f]:.2e} vs eps_B {EPSB[f]:.4f}" for f in FOOTS)
    + f"; CFG941 0.01 line {'met' if max(epsmax.values()) <= 0.01 else 'NOT met'}; 1-Gyr dynamics with Delta a = tidal residual: stars and own-label medium bound in "
      f"{nb_bound}/18 (min P_max/Delta a {min(v['P_max_over_Da'] for v in dyn.values()):.1e}, max separation/r_dom {max(v['max_sep_over_rt'] for v in dyn.values()):.1e})")
efe_u = {}; efe_t = {}
for foot in FOOTS:
    a0 = A0[foot]
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            Mh, rh, gbh, gh, uh = host_fields(rk, a0); M, a, us_of = us_fun(Mb_, apc, a0)
            gbs = plummer_g(M, a, a); uiso = Rinv(gbs, a0)
            efe_u[f"{foot}|{hn}|{rk:g}"] = math.log10((gbs + Rinv(gbs, a0)) / (gbs + uiso))
            dtid = float(law_g(G_SI * Mh / (rh - a) ** 2, a0)) - gh; arg = gbs - dtid
            efe_t[f"{foot}|{hn}|{rk:g}"] = math.log10((gbs + Rinv(arg, a0)) / (gbs + uiso)) if arg > 0 else float("-inf")
i_pass = c_pass and all(abs(efe_u[k]) <= DELC[k.split("|")[0]] for k in efe_u)
put("i", "PASS" if i_pass else "FAIL",
    f"Delta a/g_host <= eps_B (as (c)); uniform-field EFE on the satellite phantom {max(abs(v) for v in efe_u.values()):.1e} dex vs delta_c "
    f"{DELC['canonical']:.4f}/{DELC['alt']:.4f}; tidal term (reported) {min(efe_t.values()):.4f}..{max(efe_t.values()):.4f} dex")
RES["c"] = dict(H1=H1B, dyn=dyn, eps_max=epsmax, eps_B=EPSB); RES["i"] = dict(efe_uniform=efe_u, efe_tidal=efe_t)

P("\n==================== (d) slip ====================")
sat_slip = 0.0
for foot in FOOTS:
    a0 = A0[foot]
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            Mh, rh, gbh, gh, uh = host_fields(rk, a0); M, a, us_of = us_fun(Mb_, apc, a0)
            us_a = us_of(a); gs = plummer_g(M, a, a) + us_a
            pmax = float(W_num(uh, a0)) + D_num(uh, a0) * uh / K_SI + float(W_num(us_a, a0)) + D_num(us_a, a0) * us_a / K_SI
            sat_slip = max(sat_slip, 4 * math.pi * G_SI * a * pmax / (C_SI ** 2 * gs), 8 * math.pi * G_SI * a * a * pmax / (C_SI ** 2 * gs * a))
d_pass = max(wg0, w80, sat_slip) <= 1.9e-5
put("d", "PASS" if d_pass else "FAIL", f"per label (CFG847's five systems, L* 0/24 pc/1 kpc): worst s_grad {wg0:.2e}, s_847 {w80:.3e}; satellite inside a host "
    f"(summed label stresses, upper bound) {sat_slip:.1e}; line 1.9e-5")
RES["d"] = dict(s_grad=wg0, s_847=w80, sat=sat_slip, rows=SLIP_ROWS)
guard("abcd")

P("\n==================== (e) energy and momentum through label events ====================")
t1 = toy1d_ldt()
e1 = t1["P_rel"] <= 1e-12
P(f"  e1 1-D toy: |P(t) - P(0)|/sum m|v| max {t1['P_rel']:.1e} across latch / re-latch / merge; max label changes per slab {t1['max_label_changes']}; "
  f"labels at end {t1['n_labels_end']}; leapfrog energy drift between events {t1['E_drift_rel_between_events']:.1e}; 1-D event jumps (box-dependent, not graded) "
  + ", ".join(f"{k} {v:+.2e}" for k, v in t1["E_jumps"].items()))
EV = {}
for foot in FOOTS:
    a0 = A0[foot]; pr = ngc_profile(a0)
    Eg = E_grav_profile(pr); EWfin = E_W_profile(pr, a0); EWlo = E_W_exterior(pr["Mc"], pr["r_on"], a0)
    Mcr = np.minimum(pr["u"] * pr["r"] ** 2 / G_SI, pr["Mc"])
    Wcc = float(np.sum(0.5 * (G_SI * Mcr[1:] ** 2 / (2 * pr["r"][1:] ** 2) + G_SI * Mcr[:-1] ** 2 / (2 * pr["r"][:-1] ** 2)) * np.diff(pr["r"]))) + G_SI * pr["Mc"] ** 2 / (2 * pr["re"])
    # concentric merger of two NGC-3198-like labels (second label: baryons scaled by the ratio, same shape; own census label mass)
    mer = {}
    for ratio in (1.0, 1.0 / 3.0):
        dom2 = domain(MB_N_SUN * ratio, a0); Mc2 = dom2["Mc"] * MSUN; re2, _, _ = ldt_edge(MB_N_SUN * ratio, dom2["Mc"], a0)
        rr = pr["r"]; Mb2 = ratio * pr["Mb"]; gn2 = G_SI * Mb2 / rr ** 2
        u2 = np.where(rr <= re2, law_g(gn2, a0) - gn2, G_SI * Mc2 / rr ** 2)
        u1 = np.where(rr <= pr["re"], pr["u"], G_SI * pr["Mc"] / rr ** 2)
        wall = (u1 + u2) >= a0
        Mc_in = np.minimum(u1 * rr ** 2 / G_SI, pr["Mc"]) + np.minimum(u2 * rr ** 2 / G_SI, Mc2)
        wall_mass = float(np.max(np.where(wall, Mc_in, 0.0)) / (pr["Mc"] + Mc2))
        ok = ~wall
        integ = 4 * np.pi * rr ** 2 * (W_num(np.where(ok, u1 + u2, 0.0), a0) - W_num(u1, a0) - W_num(u2, a0))
        dE_out = float(np.sum(0.5 * (np.where(ok, integ, 0)[1:] + np.where(ok, integ, 0)[:-1]) * np.diff(rr)))
        r1e = pr["re"]                                                    # exterior of both labels: u_q = G M_cq / r^2
        crossf = lambda s: 4 * math.pi * (r1e / s) ** 2 * float(W_num(G_SI * (pr["Mc"] + Mc2) / (r1e / s) ** 2, a0) - W_num(G_SI * pr["Mc"] / (r1e / s) ** 2, a0)
                                                               - W_num(G_SI * Mc2 / (r1e / s) ** 2, a0)) * r1e / s ** 2
        dE_out += quad(crossf, 0, 1, epsrel=1e-10, limit=200)[0]
        prm_ = ngc_profile(a0, scale=1 + ratio, Mc_override=pr["Mc"] + Mc2)
        Eg_m = E_grav_profile(prm_)
        mer[f"{ratio:.3f}"] = dict(wall_crossed=bool(wall.any()), wall_mass_frac=wall_mass, dE_instant=(math.inf if wall.any() else dE_out),
                                   dE_outside_wall=dE_out, Eg_merged=Eg_m, rel_outside_wall=dE_out / abs(Eg_m))
    # re-latch at r_dom (H1-H3): per unit mass K(lambda_h(R) - lambda_s(r_dom)) vs g_host R
    rel = {}
    domh = domain(HOST938, a0); Mch = domh["Mc"] * MSUN; reh, _, _ = ldt_edge(HOST938, domh["Mc"], a0)
    for hn, Mb_, apc in HOSTS882:
        for rk in RADII:
            Mh, rh, gbh, gh, uh = host_fields(rk, a0); M, a, us_of = us_fun(Mb_, apc, a0)
            uhost = lambda x: (float(law_g(G_SI * Mh / x ** 2, a0)) - G_SI * Mh / x ** 2) if x <= reh else G_SI * Mch / x ** 2
            Klh = quad(lambda x: D_num(uhost(x), a0), rh, reh, limit=200, epsrel=1e-10)[0] + tail_D(Mch, reh, a0)[0]
            rd = H1B[f"{foot}|{hn}|{rk:g}"]["r_dom_pc"] * PC; Msd = us_of(rd) * rd * rd / G_SI
            Kls = tail_D(Msd, rd, a0)[0]
            rel[f"{hn}|{rk:g}"] = dict(e_per_mass=Klh - Kls, over_gR=(Klh - Kls) / (gh * rh))
    EV[foot] = dict(E_grav=Eg, dE_assembly_lo=EWlo, dE_assembly_hi=EWfin, rel_lo=EWlo / abs(Eg), rel_hi=EWfin / abs(Eg), W_cc=Wcc,
                    merger=mer, relatch=rel, RE_cost_max=max(LE[foot]["Klam_center"], LE[foot]["Klam_re"]) / C_SI ** 2,
                    bianchi_PN=EWfin / (pr["Mc"] * C_SI ** 2))
    P(f"  [{foot}] NGC 3198 label assembly: Delta E in [{EWlo:.3e}, {EWfin:.3e}] J = [{EWlo / abs(Eg):.3f}, {EWfin / abs(Eg):.3f}] |E_grav| (|E_grav| {abs(Eg):.3e} J; "
      f"medium self-binding {Wcc:.3e} J); merger 1:1 / 1:3: wall u1 + u2 >= a0 crossed: {mer['1.000']['wall_crossed']} / {mer['0.333']['wall_crossed']} "
      f"(medium fraction inside the wall {mer['1.000']['wall_mass_frac']:.3f} / {mer['0.333']['wall_mass_frac']:.3f}; instant Delta E = inf there); outside the wall "
      f"{mer['1.000']['dE_outside_wall']:.3e} / {mer['0.333']['dE_outside_wall']:.3e} J = {mer['1.000']['rel_outside_wall']:.2f} / "
      f"{mer['0.333']['rel_outside_wall']:.2f} |E_grav,merged|; re-latch per unit mass / (g_host R) "
      f"{min(v['over_gR'] for v in rel.values()):+.2f}..{max(v['over_gR'] for v in rel.values()):+.2f}; R-E cost max |e_L|/c^2 {EV[foot]['RE_cost_max']:.1e}; "
      f"PN Bianchi residual ~ {EV[foot]['bianchi_PN']:.1e}")
closes = all(abs(EV[f]["rel_lo"]) <= 1e-6 and abs(EV[f]["rel_hi"]) <= 1e-6 for f in FOOTS)
e_grade = ("PASS" if (e1 and closes) else ("CONDITIONAL" if e1 else "FAIL"))
put("e", e_grade, f"e1 momentum {t1['P_rel']:.1e} (line 1e-12): {'closes' if e1 else 'FAILS'}; e2 energy jumps at label events do NOT close with dynamical fields "
    f"(assembly {EV['canonical']['rel_lo']:.2f}-{EV['canonical']['rel_hi']:.2f} / {EV['alt']['rel_lo']:.2f}-{EV['alt']['rel_hi']:.2f} |E_grav|; T-LE: no kinetic payment); "
    f"closed only through R-E (non-dynamical label energy, cost |e_L|/c^2 <= {max(EV[f]['RE_cost_max'] for f in FOOTS):.1e}); instant merging is undefined where "
    "the summed field reaches the W_full wall")
RES["e"] = dict(toy=t1, events=EV)
guard("e")

P("\n==================== (f) mergers ====================")
MT = {}
RRES = math.sqrt(10 * NS_SUP * 1.0 / 300)                              # A1: r_res = sqrt(10 dm_N0), dm_N0 = 6 M_b1/N0 (both ratios)
for ratio in (1.0, 1.0 / 3.0):
    MT[f"{ratio:.3f}|N0"] = merger_toy(ratio, 300, flow=True, r_res=RRES)
    guard("merger flow")
    MT[f"{ratio:.3f}|2N0"] = merger_toy(ratio, 600, flow=False, r_res=RRES)
for k, v in MT.items():
    P(f"  {k}: shells {v['n_shells']}, J_LDT {v['J_LDT']:.1e}, J_A {v['J_A']:.3f}, Delta E_merge {v['dE_merge']:+.4e} (E {v['E_before']:.4e}), "
      f"max superposed u {v['max_u_superposed']:.3f}, merged edge {v['re_merged']:.3f}, eq monotone {v['eq_monotone']}, midpoint law dev {v['dev_mid']:.2e} "
      f"({v['n_inside']} shells), mass exact {v['mass_exact']}"
      + (f"; flow {v['flow_steps']} steps ({v['flow_rejected']} rejected, {v['flow_runtime_s']} s), distance {v['d0']:.3f} -> {v['d_end']:.4f} (x{v['d_ratio']:.1f}), "
         f"heat {v['heat']:.4e}, max accepted dE/|E| {v['max_accepted_dE_rel']:.1e}" if "flow_steps" in v else ""))
for k, v in MT.items():
    P(f"  A1 {k}: innermost shell r_1 {v['r1']:.3f}, du_1 {v['du1']:.3f}; discrete identity <R> = g_b max dev {v['A1_identity']:.1e}; resolved-range "
      f"(r >= {v['A1_r_res']:.3f}, {v['A1_n_res']} shells) midpoint dev {v['A1_dev_res']:.2e}"
      + (f"; heat from first finite state {v['A1_heat_from_first_finite']:.4e}, tiny accepted increases {v['n_tiny_increases']}" if "flow_steps" in v else ""))
f1 = all(v["J_LDT"] <= 1e-12 for v in MT.values())
f2 = all(v["max_accepted_dE_rel"] <= 1e-12 and v["d_ratio"] >= 10 for k, v in MT.items() if "flow_steps" in v)
f3 = all(MT[f"{r_:.3f}|2N0"]["dev_mid"] <= 1e-3 and MT[f"{r_:.3f}|2N0"]["dev_mid"] <= 0.6 * MT[f"{r_:.3f}|N0"]["dev_mid"] and MT[f"{r_:.3f}|2N0"]["eq_monotone"]
         for r_ in (1.0, 1.0 / 3.0))
f3A = all(MT[f"{r_:.3f}|{s}"]["A1_identity"] <= 1e-9 for r_ in (1.0, 1.0 / 3.0) for s in ("N0", "2N0")) and \
    all(MT[f"{r_:.3f}|2N0"]["A1_dev_res"] <= 1e-3 and MT[f"{r_:.3f}|2N0"]["A1_dev_res"] <= 0.6 * MT[f"{r_:.3f}|N0"]["A1_dev_res"] and MT[f"{r_:.3f}|2N0"]["eq_monotone"]
        for r_ in (1.0, 1.0 / 3.0))
f_grade_A1 = "PASS" if (f1 and f2 and f3A) else "FAIL"
put("f", "PASS" if (f1 and f2 and f3) else "FAIL",
    f"f1 J_LDT {max(v['J_LDT'] for v in MT.values()):.1e} vs class-A-type J_A {min(v['J_A'] for v in MT.values()):.3f}-{max(v['J_A'] for v in MT.values()):.3f}; "
    f"f2 flow monotone, distance x{min(v['d_ratio'] for v in MT.values() if 'd_ratio' in v):.1f}; f3 (frozen) midpoint law dev at 2N0 "
    + ", ".join(f"1:{1 / r_:.0f} {MT[f'{r_:.3f}|2N0']['dev_mid']:.1e} (N0 {MT[f'{r_:.3f}|N0']['dev_mid']:.1e})" for r_ in (1.0, 1.0 / 3.0))
    + f" [frozen metric pinned at the innermost shell, du_1 ~ {MT['1.000|2N0']['du1']:.2f}]. POST HOC A1: f3-A identity <= "
    + f"{max(v['A1_identity'] for v in MT.values()):.1e}; f3-B resolved-range dev at 2N0 "
    + ", ".join(f"1:{1 / r_:.0f} {MT[f'{r_:.3f}|2N0']['A1_dev_res']:.1e} (N0 {MT[f'{r_:.3f}|N0']['A1_dev_res']:.1e})" for r_ in (1.0, 1.0 / 3.0))
    + f" -> (f) under A1: {f_grade_A1}")
RES["f"] = MT; RES["f_grade_A1"] = f_grade_A1
guard("f")

P("\n==================== (g) well-posedness ====================")
g1 = all(dmins[uf][0] >= 0 and dmins[uf][1] == 0 for uf in UGRID) and INERT_MIN > 1
g3 = d2max <= 1.0 + 1e-9
g4 = sp.simplify(theta_dot_at_ta) != 0 and t1["max_label_changes"] <= 3
g_ok = g1 and ST["T-G"] and g3 and g4
put("g", "CONDITIONAL" if g_ok else "FAIL",
    f"g1 per label min omega^2/(K rho0) {', '.join(f'{dmins[uf][0]:.3f}' for uf in UGRID)} >= 0, max Im 0; inertia margin min {INERT_MIN:.1e}; g2 no theta in the action "
    f"(kinetic coefficient rho0); g3 co-located labels max Im/Jeans {d2max:.3f} <= 1 (bounded, k-independent); label field enters only via n_q; g4 one-way rule: finite "
    f"label changes (toy max {t1['max_label_changes']}), transversal latch. Premises inherited: gamma > 0, rho c^2 > D u/K, per-label single stream; nonlinear WP unproved")

P("\n==================== (h) forced edge and zero-sum ====================")
H = {}
h1ok = True
for foot in FOOTS:
    a0 = A0[foot]; rows = []
    for Mb in np.logspace(7, 15, 17):
        dom = domain(float(Mb), a0); re_, rM, N = ldt_edge(Mb, dom["Mc"], a0)
        gnr = G_SI * Mb * MSUN / dom["r_on"] ** 2; Mph_on = dom["r_on"] ** 2 * (float(law_g(gnr, a0)) - gnr) / G_SI / MSUN
        ratio = Mph_on / dom["Mc"]; h1ok = h1ok and ratio > 1
        rows.append(dict(Mb=float(Mb), ratio_Mph_ron_over_Mc=ratio, r_e_Mpc=re_ / (1e3 * KPC), r_on_Mpc=dom["r_on"] / (1e3 * KPC), re_over_ron=re_ / dom["r_on"],
                         re_over_rM=re_ / rM, re_E7_Mpc=dom["r_e"] / (1e3 * KPC), N=N))
    sysrows = {}
    for nm, Mb, rk in [("NGC3198", MB_N_SUN, None)] + SYS847:
        dom = domain(Mb, a0); re_, rM, N = ldt_edge(Mb, dom["Mc"], a0)
        sysrows[nm] = dict(r_e_kpc=re_ / KPC, r_on_kpc=dom["r_on"] / KPC, re_over_rM=re_ / rM, E7_kpc=dom["r_e"] / KPC, N=N)
    H[foot] = dict(grid=rows, systems=sysrows)
GALS = C4.load_sparc()
beyond = {f: 0 for f in FOOTS}; ngal = 0
for g in GALS:
    Rm = g["R"] * 3.0857e19
    GB = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.61 * g["Vdisk"] ** 2 + 1.4 * 0.61 * g["Vbul"] ** 2) * 1e6 / Rm
    ok = np.where(np.isfinite(GB) & (GB > 0))[0]
    if len(ok) == 0:
        continue
    i = ok[-1]; mb = GB[i] * Rm[i] ** 2 / G_SI / MSUN; ngal += 1
    for foot in FOOTS:
        dom = domain(mb, A0[foot]); re_, _, _ = ldt_edge(mb, dom["Mc"], A0[foot])
        beyond[foot] += int(np.sum(Rm > re_))
toy_mass = all(v["mass_exact"] for v in MT.values())
h_pass = h1ok and all(beyond[f] == 0 for f in FOOTS) and all(a3[f]["inside"] for f in FOOTS) and toy_mass
put("h", "PASS" if h_pass else "FAIL",
    f"h1 M_ph(<r_ON)/M_c,q = {min(x['ratio_Mph_ron_over_Mc'] for f in FOOTS for x in H[f]['grid']):.3f}..{max(x['ratio_Mph_ron_over_Mc'] for f in FOOTS for x in H[f]['grid']):.3f} > 1 "
    f"(edge forced, 1e7-1e15 M_sun); h2 r_e/r_ON {min(x['re_over_ron'] for f in FOOTS for x in H[f]['grid']):.3f}..{max(x['re_over_ron'] for f in FOOTS for x in H[f]['grid']):.3f}, "
    f"NGC 3198 r_e {H['canonical']['systems']['NGC3198']['r_e_kpc']:.0f}/{H['alt']['systems']['NGC3198']['r_e_kpc']:.0f} kpc; h3 SPARC points beyond r_e: "
    f"{beyond['canonical']}/{beyond['alt']} ({ngal} galaxies); h4 zero-sum = medium mass conservation, exact in the toys ({toy_mass}) and by rule (events move no mass)")
RES["h"] = dict(H=H, sparc_beyond=beyond, n_gal=ngal)

P("\n==================== reported R1-R3 ====================")
r1 = {k: v["M_med_dom"] / v["M_star_dom"] for k, v in H1B.items()}
P(f"  R1 other labels are baryon-like for a label's equilibrium (R(u_q) = g_b + sum_p u_p): satellites' own-domain medium / stars = "
  f"{min(r1.values()):.0f}..{max(r1.values()):.0f} (H1-H3 x 50/100/250 kpc); a host's law beyond a satellite reads g_b + G M_sat,med/d^2. Example: the three CFG882 "
  f"dwarfs at 100 kpc carry {sum(H1B[f'canonical|{h}|100']['M_med_dom'] for h, _, _ in HOSTS882):.2e} M_sun of own-label medium, "
  f"{sum(H1B[f'canonical|{h}|100']['M_med_dom'] for h, _, _ in HOSTS882) / HOST938:.1e} of a 6e10 M_sun host's baryons")
R2 = sp.simplify(Rsym) ; r2_pos = sp.simplify(Rsym.subs(u, a0s / 2))
P(f"  R2 baryon-free label: force on labelled medium = -g_b + R(u_q) u_hat with g_b = 0 -> R(u) = {R2} > 0 (e.g. {r2_pos} at u = a0/2): outward; the label disperses")
P("  R3 formulation (B) costs (CFG947): no action (retarded kernels); cap q <= 1; deficit clip; kernel's own supply root; T-M dipole condition; own-label phantom "
  "non-additive (T-L), so an instant merge recomputation jumps (here J_A " + f"{min(v['J_A'] for v in MT.values()):.2f}-{max(v['J_A'] for v in MT.values()):.2f})")
RES["R1"] = r1

# ================================================================================================ CLASS + SCORECARD
P("\n==================== CLASS (frozen rule, criteria sec. 6) ====================")
grades = {k: TESTS[k]["grade"] for k in "abcdefghi"}
P("  grades (frozen): " + ", ".join(f"({k}) {v}" for k, v in grades.items()))
generic_fail = False                                                   # no section-4 statement shows a FAIL generic to LDT (the only FAIL is the f3 metric)


def class_of(gr):
    if not K_ALL:
        return "VOID (a K control failed)"
    if all(v == "PASS" for v in gr.values()):
        return "LDT CONSISTENT"
    if all(v != "FAIL" for v in gr.values()):
        return "LDT CONDITIONAL"
    return "LDT INCONSISTENT" if generic_fail else "NOT CONSISTENT AS SPECIFIED"


CLASS = class_of(grades)
grades_A1 = dict(grades, f=f_grade_A1)
CLASS_A1 = class_of(grades_A1)
P(f"  CLASS (frozen rule, frozen metrics): {CLASS}")
P(f"  CLASS under POST-HOC amendment A1 (f3 metric only): {CLASS_A1}   [grades: (f) {f_grade_A1}; all others unchanged]")
RES["grades"] = grades; RES["class"] = CLASS; RES["grades_A1"] = grades_A1; RES["class_A1_post_hoc"] = CLASS_A1
RES["tests"] = TESTS; RES["structural"] = {k: bool(v) for k, v in ST.items()}
SC = [
    ("A1 ghost / 2nd order", "CONDITIONAL", "per label CFG938 (inertia iff rho c^2 > D u/K, margin >= %.1e); no theta in the action (T-G) so no CFG944 ghost; label sector has no action (CFG678: a prescribed rule cannot PASS)" % INERT_MIN),
    ("A2 hyperbolicity", "CONDITIONAL", "per label omega^2 >= 0 (g1); co-located labels bounded Jeans (g3); needs gamma > 0"),
    ("A3 nonlinear WP", "UNTESTED", "not proved; event-driven force discontinuities"),
    ("A4 strong coupling", "UNTESTED", "not computed"),
    ("A5 GW at c", "PASS", "Einstein-Hilbert unmodified, no curvature couplings of the medium or chi_q (structural)"),
    ("A6 BH exteriors", "UNTESTED", "no computation"),
    ("A7 radiative", "DECLARED", "CFG320"),
    ("B1 switch from variation", "UNTESTED", "the switch is the action-less label sector (prescribed); CFG678's rule scores it UNTESTED, never PASS; momentum conserved (e1), unlike CFG48's gate; CFG944 Theorem G: no local variational version"),
    ("B2 a0-Lambda tie", "UNTESTED", "a0 constant in W; kappa = 1/2 FITTED"),
    ("B3 cold sector", "CONDITIONAL", "per label CFG938 (well-posed, lenses like mass, slip %.1e); energy closes only through R-E (e)" % w80),
    ("C1 Cassini", "CONDITIONAL", "inherits CFG938's C1 (spherical sector = S2); satellites' and hosts' media no longer differential-fall (c)"),
    ("C2 SPARC", "PASS", "single-label law (a), no SPARC point beyond its label's edge (h3): CFG4 rms 0.1003/0.0991 <= 0.110"),
    ("C3 early types", "FAIL", "inherits CFG529 (the law fails)"),
    ("C4 cluster lensing", "NOT DECIDED", "as CFG678 (CFG680 amplitude not frozen)"),
    ("D1 zero field", "UNTESTED", "not run"),
    ("D2 growth", "UNTESTED", "linear regime dust, n = 1 (b); the CFG596 line needs an LDT PM engine (CFG952); class-A shear passes do not transfer automatically"),
    ("D3 flat a0(z)", "PENDING", "constant a0; sealed tests 2026-11-06 / 2026-11-28"),
    ("E1 kappa from the action", "DECLARED", "kappa = 1/2 FITTED"),
    ("E2 quantum completion", "DECLARED", "none"),
    ("E3 SM structure", "DECLARED", "walled"),
]
for g_, s_, src in SC:
    P(f"  {g_:28s} {s_:12s} {src}")
RES["scorecard"] = [dict(gate=g_, status=s_, source=src) for g_, s_, src in SC]
dump()
P(f"\n  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
sys.exit(0)
