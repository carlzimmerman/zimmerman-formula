"""CFG921 -- excess-selector constraint intersection: five candidate new posits (one constant each) vs the CFG820-920 facts.
Criteria: FROZEN_CRITERIA.md (0abd82098, committed alone before this script and before any number of this lane).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg921.py      (CFG921_MUTATE=sign|inject -> separate outputs named by mode).
Inputs: CFG919's input + cell code exec'd read-only (which exec's CFG914's input section: 83 LVD dwarfs of CFG880, SPARC,
B21 lenses, eRASS1 stack of CFG687, 31 globulars of CFG883); SPARC Table 1; committed JSON/out of CFG687, 829, 845, 850,
820, 876, 860, 920 for the quoted source numbers.  P5 = QUMOND thin-disc quadrature (no PDE solver).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, re, time, resource, contextlib, builtins, warnings
import numpy as np
from scipy.stats import chi2 as CHI2, norm
from scipy.optimize import brentq
from scipy.special import j0, j1, i0e, i1e, k0e, k1e

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG921_MUTATE", ""); assert MUT in ("", "sign", "inject"); SUF = f"_MUTATE_{MUT}" if MUT else ""
KONLY = os.environ.get("CFG921_KONLY", "") == "1"; assert not (KONLY and MUT)
if KONLY: SUF = "_K"
for _e in ("CFG919_MUTATE", "CFG914_MUTATE", "CFG880_MUTATE", "CFG829_MUTATE", "CFG850_MUTATE", "CFG883_MUTATE", "CFG828_MUTATE",
           "CFG849_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def J(*p): return json.load(builtins.open(os.path.join(LANES, *p)))
RES = dict(lane="CFG921", criteria="0abd82098", mutate=MUT or None, checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def jdef(o):
    if hasattr(o, "item"): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
def finish(code):
    RES["runtime_s"] = time.time() - T0; RES["peak_rss_mb"] = rss_mb()
    json.dump(RES, builtins.open(os.path.join(HERE, f"cfg921_results{SUF}.json"), "w"), indent=1, default=jdef)
    builtins.open(os.path.join(HERE, f"cfg921{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)

FOOTS = ("canonical", "alt"); A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LN10 = math.log(10.0)
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_s = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-15)))
POSITS = ("P1", "P2", "P3", "P4", "P5")
PNAME = {"P1": "stress coupling (theta = c_*, km/s)", "P2": "velocity-space capture (theta = v_2, km/s)",
         "P3": "late binding + post-binding escape (theta = v_w, km/s)", "P4": "phase-space-density capture (theta = Q_*, Msun pc^-3 (km/s)^-3)",
         "P5": "QUMOND geometry (no constant)"}
SG = (6.0, 10.0, 20.0); SD = (6.0, 10.0, 20.0)                            # dwarf gas sigma, SPARC disc sigma (km/s); nominal index 1
FPB = ((0.2, 0.8), (0.43, 0.57), (0.10, 0.97))                           # (LD, LS) f_P; nominal index 0
DMB = (-0.2, 0.0, 0.2); REB = (0.5, 1.0, 2.0); GFB = ((0.90, 0.50), (0.95, 0.65), (1.00, 0.80))   # nominal index 1, 1, 1
LENS_CORNERS = [(a, b, c, d) for a in range(3) for b in range(3) for c in range(3) for d in range(3)]
LENS_NOM = (0, 1, 1, 1)
LM_RED, LM_BLUE, SHIFT_N2 = 10.81, 10.45, 0.123
NBOOT = 2000

P("CFG921  excess-selector constraint intersection: five candidate new posits, one constant each, calibrated on the 83 LVD dwarfs"
  + (f"   [MUTATE {MUT}]" if MUT else ""))
P("  kappa = 1/2 FITTED; footings never pooled; criteria 0abd82098")

# =====================================================================================================================  K1: CFG919 exec'd read-only
P("\n=== K-stage")
F919 = os.path.join(LANES, "CFG919_pressure_support_selector", "cfg919.py")
def _cfg921_ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG921 refuses to write {file!r} from re-executed committed code")
    return builtins.open(file, mode, *a, **k)
class _Exit(Exception): pass
def _cfg921_exit(code=0): raise _Exit(code)
_src = builtins.open(F919).read(); _cut = _src.index("\nEXIT = 0\nif not MUT:")
_src = _src[:_cut].replace("builtins.open(", "_cfg921_ro_open(").replace("sys.exit(", "_cfg921_exit(")
N919 = {"__file__": F919, "__name__": "cfg919_ro", "_cfg921_ro_open": _cfg921_ro_open, "_cfg921_exit": _cfg921_exit}
_buf = io.StringIO(); _k1 = False
try:
    with contextlib.redirect_stdout(_buf), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        exec(compile(_src, F919, "exec"), N919)
    _k1 = bool(N919["K_ALL"]) and all(v["ok"] for v in N919["RES"]["checks"].values())
except _Exit:
    _k1 = False
_c919 = N919.get("RES", {}).get("checks", {})
KOK = [check("K1 CFG919 input/cell code exec'd read-only: all its K-checks pass (incl. CFG914's 9)", _k1,
             f"{sum(v['ok'] for v in _c919.values())}/{len(_c919)} CFG919 checks pass")]
if not KOK[0]:
    P("  K1 failed: lane stops (FROZEN_CRITERIA section 7)."); RES["class"] = None; finish(2)
build, FLOOR0, FLOOR_V6, GRID = N919["build"], N919["FLOOR0"], N919["FLOOR_V6"], N919["GRID"]
DWR, DWM, GCR, GKIN, gc_vs = N919["DWR"], N919["DWM"], N919["GCR"], N919["GKIN"], N919["gc_vs"]
SP, VGAL, SMALL, LARGE, lens_set = N919["SP"], N919["VGAL"], N919["SMALL"], N919["LARGE"], N919["lens_set"]
CLR, CW, CLP, N914, N880 = N919["CLR"], N919["CW"], N919["CLP"], N919["N914"], N919["N880"]
R919 = J("CFG919_pressure_support_selector", "cfg919_results.json")

# =====================================================================================================================  K2 / K3: CFG919 V0 cells, class means, F1
def gls_ops(cells, Ctot):
    cls = np.array([c["cls"] for c in cells]); out = {}
    for c in dict.fromkeys(cls):
        ix = np.where(cls == c)[0]; Ci = np.linalg.inv(Ctot[np.ix_(ix, ix)]); one = np.ones(len(ix)); a = float(one @ Ci @ one)
        out[c] = dict(ix=ix, w=(Ci @ one) / a, se=a ** -0.5)
    return out
OBS0 = {}
k2d, k3d = [], []
for f in FOOTS:
    cells, C, mem = build(f, {})
    ref = R919["byfoot"][f]["V0"]
    assert len(cells) == len(ref["cells"])
    for c, r in zip(cells, ref["cells"]):
        assert c["cls"] == r["cls"] and c["w"] == r["w"] and c["n"] == r["n"]
        k2d += [abs(c["E"] - r["E"]), abs(c["lg"] - r["lg"]), abs(c["f"] - r["f"]), abs(c["se_stat"] - r["se_stat"])]
    Ctot = C + FLOOR0 ** 2 * np.eye(len(cells)); E = np.array([c["E"] for c in cells]); ops = gls_ops(cells, Ctot)
    for cl, o in ops.items():
        k3d += [abs(float(o["w"] @ E[o["ix"]]) - ref["class_summary"][cl]["E"]), abs(o["se"] - ref["class_summary"][cl]["se"])]
    ng = np.array([c["cls"] != "GC" for c in cells]); x = np.array([c["f"] for c in cells])[ng]; Cg = Ctot[np.ix_(ng, ng)]
    with np.errstate(all="ignore"):
        Ci = np.linalg.inv(Cg); a = float(x @ Ci @ x); A = float(x @ Ci @ E[ng]) / a; r_ = E[ng] - A * x; chi = float(r_ @ Ci @ r_)
    F1r = ref["F"]["F1"]; k3d += [abs(A - F1r["A"]), abs(a ** -0.5 - F1r["sA"]), abs(chi - F1r["chi2"])]
    OBS0[f] = (cells, C)
KOK.append(check("K2 CFG919 V0 cells reproduced (cls, w, n exact; E, lg, f, se_stat), both footings", max(k2d) <= 1e-12, f"37 cells x 2; max |diff| {max(k2d):.1e}"))
KOK.append(check("K3 CFG919 V0 class means (7 classes) and F1 (A, sA, chi2) by this lane's GLS, both footings", max(k3d) <= 1e-9,
                 f"max |diff| {max(k3d):.1e}; canonical DW {R919['byfoot']['canonical']['V0']['class_summary']['DW']['E']:+.3f}"))

# =====================================================================================================================  K4: quoted source numbers
k4 = []
def q(name, val, quoted, tol):
    k4.append((name, float(val), quoted, abs(float(val) - quoted) <= tol))
R687 = J("CFG687_erass1_shear_stack", "cfg687_results.json")["A"]
for f, mid, smid, outr, sout in (("canonical", 1.910, 0.119, 1.012, 0.087), ("alt", 1.754, 0.109, 0.927, 0.080)):
    a = R687[f"{f}|b0.67|rc0.15|f0.20"]
    q(f"CFG687 A_MID {f}", a["MID"][0], mid, 5e-4); q(f"CFG687 sA_MID {f}", a["MID"][1], smid, 5e-4)
    q(f"CFG687 A_OUTER {f}", a["OUTER"][0], outr, 5e-4); q(f"CFG687 sA_OUTER {f}", a["OUTER"][1], sout, 5e-4)
R829 = J("CFG829_lensing_low_g_vs_dwarf_excess", "cfg829_results.json")["canonical|nu_e|blue (u-r<2.5)"]["window"]
q("CFG829 blue A", R829["A"], 1.016, 5e-4); q("CFG829 blue sA", R829["sA"], 0.086, 5e-4)
R850 = J("CFG850_red_split_mstar_systematic", "cfg850_results.json")["rows"]
for f, ar, asp, adi in (("canonical", 1.451, 1.486, 1.066), ("alt", 1.324, 1.356, 0.973)):
    r = R850[f"{f}|0.123|0.0"]; q(f"CFG850 A_red {f}", r["A_red"], ar, 5e-4); q(f"CFG850 A_sph {f}", r["A_sph"], asp, 5e-4)
    q(f"CFG850 A_disc {f}", r["A_disc"], adi, 5e-4)
R845 = J("CFG845_hprim_vs_sparc_dwarfs", "cfg845_results.json"); q("CFG845 D", R845["D"], -0.273, 5e-4); q("CFG845 sD", R845["sD"], 0.026, 5e-4)
R820 = J("CFG820_stiffness_from_globulars", "cfg820_results.json")
q("CFG820 L95 canonical", R820["primary (no Pal 3)|canonical"]["L95"], 23.96, 5e-3); q("CFG820 L95 alt", R820["primary (no Pal 3)|alt"]["L95"], 24.72, 5e-3)
R876 = J("CFG876_cold_floor_universality", "cfg876_results.json")
for f, e_ in (("canonical", 0.241), ("alt", 0.195)):
    q(f"CFG876 law-alone large E {f}", R876[f]["law alone (B)"]["E"], e_, 5e-4); q(f"CFG876 law-alone large se {f}", R876[f]["law alone (B)"]["se_E"], 0.105, 5e-4)
R860 = J("CFG860_stripping_vs_isolated_dwarfs", "cfg860_results.json")["variants"]["alt|base"]
q("CFG860 alt c0", R860["c0"], -0.150, 5e-4); q("CFG860 alt s0", R860["s0"], 0.122, 5e-4); q("CFG860 alt cG", R860["cG"], -0.064, 5e-4); q("CFG860 alt sG", R860["sG"], 0.093, 5e-4)
_o860 = builtins.open(os.path.join(LANES, "CFG860_stripping_vs_isolated_dwarfs", "cfg860.out")).read()
_m = re.search(r"\[canonical\] N S/I0/IG 69/6/5\s+b (\S+)\s+c0 (\S+)\+-(\S+)\s+cG (\S+)\+-(\S+)", _o860)
q("CFG860 canonical c0", float(_m.group(2)), -0.150, 5e-4); q("CFG860 canonical cG", float(_m.group(4)), -0.064, 5e-4)
R920 = J("CFG920_dwarf_baryon_loss_chemistry", "cfg920_results.json")
q("CFG920 median M_req canonical", R920["summary"]["canonical"]["median"]["-0.5|W1"]["M_req"], 3.815, 5e-4)
q("CFG920 median M_req alt", R920["summary"]["alt"]["median"]["-0.5|W1"]["M_req"], 3.185, 5e-4)
k4.append(("CFG920 overall class", 0.0, 0.0, R920["overall"] == "UNDERDETERMINED"))
KOK.append(check("K4 quoted source numbers (CFG687, 829, 850, 845, 820, 876, 860, 920) match the source files", all(x[3] for x in k4),
                 f"{sum(x[3] for x in k4)}/{len(k4)} match" + ("" if all(x[3] for x in k4) else "; FAIL: " + ", ".join(x[0] for x in k4 if not x[3]))))
RES["K4_values"] = {x[0]: x[1] for x in k4}

# =====================================================================================================================  per-system inputs
DWD = {}; k6 = []
for f in FOOTS:
    d = DWR[f]; a0 = A0[f]; names = list(d["names"]); r12 = np.asarray(d["r12"], float); lg = np.asarray(d["gbar"], float); gb = 10 ** lg
    Ms, Mg = [], []
    for nm, rp in zip(names, r12):
        L = N880["LVD"][nm]; Ms.append(2.0 * 10 ** (0.4 * (4.83 - N880["fnum"](L["M_V"])))); Mg.append(N880["gas_in"](N880["fnum"](L.get("mass_HI")), rp))
    Ms, Mg = np.array(Ms), np.array(Mg); w = (Ms / 2) / (Ms / 2 + Mg)
    nu = nu_e(gb / a0); gL = gb * nu; r12m = r12 * PC; sl = np.sqrt(r12m * gL / 3) / 1e3
    k6 += [float(np.max(np.abs(w - DWM[f]["fsph"]))), float(np.max(np.abs(sl / np.asarray(d["sig_law"], float) - 1)))]
    DWD[f] = dict(names=names, lg=lg, gb=gb, r12=r12, r12m=r12m, w=w, nu=nu, gL=gL, phi=1 - 1 / nu, sl=sl, Ms=Ms, Mg=Mg,
                  rho=(Ms / 2 + Mg) / (4 * math.pi / 3 * r12 ** 3), E=np.asarray(d["E"], float), sE=np.asarray(d["sE"], float),
                  hi=np.asarray(DWM[f]["hi"], bool), a0=a0, k=np.digitize(lg, GRID) - 1)
KOK.append(check("K6 per-dwarf inputs: w == CFG919 f_sph exactly; sigma_law^2 == r12 g_L/3", k6[0] == 0 and k6[2] == 0 and max(k6[1], k6[3]) <= 1e-9,
                 f"max |dw| {max(k6[0], k6[2]):.1e}; max rel d sigma_law {max(k6[1], k6[3]):.1e}; HI-bearing {int(DWD['canonical']['hi'].sum())}/83"))

# SPARC per point (CFG919 arrays) + Table 1
SPT = {}
for l in builtins.open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: SPT[v[0]] = dict(L=float(v[7]), Reff=float(v[9]), MHI=float(v[13]))
        except ValueError: pass
sp_gal = np.asarray(SP["gal"]); sp_gb = np.asarray(SP["gb"], float); sp_lg = np.log10(sp_gb)
sp_V = np.array([VGAL[g] for g in sp_gal], float)
sp_fs = np.array([0.5 * SPT[g]["L"] / (0.5 * SPT[g]["L"] + 1.33 * SPT[g]["MHI"]) if g in SPT else np.nan for g in sp_gal])
sp_rho = np.array([(0.5 * (0.5 * SPT[g]["L"] + 1.33 * SPT[g]["MHI"]) * 1e9) / (4 * math.pi / 3 * (4 / 3 * SPT[g]["Reff"] * 1e3) ** 3) if g in SPT else np.nan for g in sp_gal])
_gcode = {g: i for i, g in enumerate(sorted(set(sp_gal)))}; sp_code = np.array([_gcode[g] for g in sp_gal])
assert np.all(np.isfinite(sp_fs[SMALL | LARGE])) and np.all(np.isfinite(sp_rho[SMALL | LARGE])) and np.all(sp_V[SMALL | LARGE] > 0)

# clusters per (cluster, band) MID+OUTER
JSEL = [3, 4, 5, 6, 7]; RC6 = N914["RC6"]; MPC6 = N914["MPC6"]; G6 = N914["G6"]; nu_mono = N914["nu_mono"]; C4 = N914["C4"]
CLD = {}; k5c = []
for f in FOOTS:
    Mb = N914["CLMb"][f][:, JSEL]; ML = N914["CLML"][f][:, JSEL]; R = (RC6[JSEL] * MPC6)[None, :] * np.ones_like(Mb)
    gbc = G6 * Mb / R ** 2; a0c = C4.A0[f]
    k5c.append(float(np.max(np.abs(nu_mono(gbc / a0c) / (ML / Mb) - 1))))
    vc = np.sqrt(G6 * ML / R) / 1e3
    CLD[f] = dict(Mb=Mb, ML=ML, nu=ML / Mb, phi=1 - Mb / ML, gb=gbc, a0=a0c, vc=vc, sig=vc / math.sqrt(3),
                  rho=Mb / (4 * math.pi / 3 * R ** 3) * PC ** 3 / MSUN, lr=CLR[f]["gbar"][:, JSEL], W=CW[:, JSEL], Pm=CLP[f][:, JSEL])

# globulars (unscreened diagnostic)
GCD = {}
_vs_known = [v for v in gc_vs.values() if v is not None]; _vs_med = float(np.median(_vs_known))
for f in FOOTS:
    rows = GCR[f]; s0 = np.array([GKIN[r["name"]]["sig0"] if (r["name"] in GKIN and GKIN[r["name"]]["sig0"]) else np.nan for r in rows])
    vs = np.array([gc_vs.get(r["name"]) if gc_vs.get(r["name"]) is not None else _vs_med for r in rows])
    gbg = 10 ** np.array([r["gbar"] for r in rows]); nug = nu_e(gbg / A0[f])
    GCD[f] = dict(names=[r["name"] for r in rows], s0=s0, vrot=vs * s0, phi=1 - 1 / nug, nu=nug, rho=10 ** np.array([r["bar"] for r in rows]))

# =====================================================================================================================  posit engines
def Gfun(L, g, a0, nufun):
    """late-binding field ratio g/g_L: (1 + L nu(L g/a0) - L) / nu(g/a0)"""
    return (1 + L * nufun(L * g / a0) - L) / nufun(g / a0)

def bis(Ffun, lo, hi, n=72):
    lo = np.array(lo, float); hi = np.array(hi, float)
    for _ in range(n):
        mid = 0.5 * (lo + hi); pos = Ffun(mid) > 0; hi = np.where(pos, mid, hi); lo = np.where(pos, lo, mid)
    return 0.5 * (lo + hi)

def dw_pred(p, th, f, sg, rev=False):
    """per-dwarf self-consistent E_pred = 2 ln(u), u = sigma_*/sigma_law"""
    D = DWD[f]; w, nu, phi, sl, gb, a0, rho = D["w"], D["nu"], D["phi"], D["sl"], D["gb"], D["a0"], D["rho"]
    if p == "P5": return np.full(len(w), -DELTA)
    if p == "P1":
        c2 = th * th
        if not rev:
            den = 1 - 3 * w * sl ** 2 / (nu * c2); num = 1 + 3 * (1 - w) * sg ** 2 / (nu * c2)
            with np.errstate(divide="ignore", invalid="ignore"):
                u2 = np.where(den > 0, num / den, np.inf)
        else:
            u2 = np.maximum((1 - 3 * (1 - w) * sg ** 2 / (nu * c2)) / (1 + 3 * w * sl ** 2 / (nu * c2)), 1 - phi)
        return np.log(u2)
    if p == "P2":
        s_of = lambda t: w * (th / (np.exp(t) * sl)) ** 3 + (1 - w) * (th / sg) ** 3
    elif p == "P4":
        s_of = lambda t: (rho / th) * (w * (2 * math.pi * np.exp(2 * t) * sl ** 2) ** -1.5 + (1 - w) * (2 * math.pi * sg ** 2) ** -1.5)
    if p in ("P2", "P4"):
        if not rev:
            t = bis(lambda t: np.exp(2 * t) - 1 - phi * s_of(t), np.zeros(len(w)), np.full(len(w), 40.0))
            return 2 * t
        t = np.zeros(len(w))
        for _ in range(300):
            t = 0.5 * t + 0.5 * 0.5 * np.log(np.maximum(1 - phi * s_of(t), 1 - phi))
        return 2 * t
    if p == "P3":
        L_of = lambda t: 1 + w * th ** 2 / (3 * np.exp(2 * t) * sl ** 2)
        if not rev:
            t = bis(lambda t: np.exp(2 * t) - Gfun(L_of(t), gb, a0, nu_e), np.zeros(len(w)), np.full(len(w), 40.0))
            return 2 * t
        t = np.zeros(len(w))
        for _ in range(300):
            t = 0.5 * t + 0.5 * 0.5 * np.log(Gfun(1 / L_of(t), gb, a0, nu_e))
        return 2 * t
    raise ValueError(p)

def p1_bisect(th, f, sg):
    D = DWD[f]; w, nu, sl = D["w"], D["nu"], D["sl"]; c2 = th * th
    t = bis(lambda t: np.exp(2 * t) - 1 - 3 * (w * np.exp(2 * t) * sl ** 2 + (1 - w) * sg ** 2) / (nu * c2), np.zeros(len(w)), np.full(len(w), 40.0))
    return 2 * t

def p1_ccrit(f): D = DWD[f]; return float(np.max(np.sqrt(3 * D["w"] * D["sl"] ** 2 / D["nu"])))

def sp_pred(p, th, f, sd, rev=False):
    a0 = A0[f]; nu = nu_e(sp_gb / a0); phi = 1 - 1 / nu; sgn = -1.0 if rev else 1.0
    if p == "P5": return np.zeros(len(sp_gb))
    if p == "P1": X = sgn * 3 * sd ** 2 / th ** 2; return np.log(np.maximum(1 + X / nu, 1 - phi))
    if p == "P2": s = (th / sd) ** 3 * np.exp(-sp_V ** 2 / (2 * sd * sd)); return np.log(np.maximum(1 + sgn * s * phi, 1 - phi))
    if p == "P4": s = (sp_rho / th) * (2 * math.pi * sd * sd) ** -1.5 * np.exp(-sp_V ** 2 / (2 * sd * sd)); return np.log(np.maximum(1 + sgn * s * phi, 1 - phi))
    if p == "P3":
        L = 1 + sp_fs * th ** 2 / sp_V ** 2
        return np.log(Gfun(1 / L if rev else L, sp_gb, a0, nu_e))
    raise ValueError(p)

def lens_central(cls, f, corner, shift):
    fpi, dmi, rei, gfi = corner; fp = FPB[fpi][1 if cls == "LS" else 0]
    lm = (LM_RED + shift if cls == "LS" else LM_BLUE) + DMB[dmi]; M = 10 ** lm
    Re = 10 ** (0.56 * lm - 5.54) if cls == "LS" else 0.10 * M ** 0.14 * (1 + M / 3.98e10) ** 0.25
    r12 = (4 / 3) * Re * REB[rei] * KPC; gbc = G * (M / 2) * MSUN / r12 ** 2; gLc = gbc * nu_e(gbc / A0[f]); vc = math.sqrt(r12 * gLc) / 1e3
    return dict(vc=vc, sig=vc * math.sqrt(fp / 3), vrot=vc * math.sqrt(1 - fp), rho=(M / 2) / (4 * math.pi / 3 * (r12 / PC) ** 3),
                fsm=GFB[gfi][0 if cls == "LS" else 1], lm=lm, Re=Re * REB[rei])

def lens_pointE(p, th, f, cen, gbs, rev=False):
    a0 = A0[f]; nu = nu_e(gbs / a0); phi = 1 - 1 / nu; sgn = -1.0 if rev else 1.0
    if p == "P5": return np.full(len(gbs), -DELTA)
    if p == "P1": X = sgn * 3 * cen["sig"] ** 2 / th ** 2; return np.log(np.maximum(1 + X / nu, 1 - phi))
    if p == "P2": s = (th / cen["sig"]) ** 3 * math.exp(-cen["vrot"] ** 2 / (2 * cen["sig"] ** 2)); return np.log(np.maximum(1 + sgn * s * phi, 1 - phi))
    if p == "P4":
        s = (cen["rho"] / th) * (2 * math.pi * cen["sig"] ** 2) ** -1.5 * math.exp(-cen["vrot"] ** 2 / (2 * cen["sig"] ** 2))
        return np.log(np.maximum(1 + sgn * s * phi, 1 - phi))
    if p == "P3":
        L = 1 + cen["fsm"] * th ** 2 / cen["vc"] ** 2
        return np.log(Gfun(1 / L if rev else L, gbs, a0, nu_e))
    raise ValueError(p)

def cl_pred(p, th, f, rev=False):
    D = CLD[f]; sgn = -1.0 if rev else 1.0
    if p == "P5": return np.full(D["Mb"].shape, -DELTA)
    if p == "P1": X = sgn * 3 * D["sig"] ** 2 / th ** 2; return np.log(np.maximum(1 + X / D["nu"], 1 - D["phi"]))
    if p == "P2": s = (th / D["sig"]) ** 3; return np.log(np.maximum(1 + sgn * s * D["phi"], 1 - D["phi"]))
    if p == "P4": s = (D["rho"] / th) * (2 * math.pi * D["sig"] ** 2) ** -1.5; return np.log(np.maximum(1 + sgn * s * D["phi"], 1 - D["phi"]))
    if p == "P3":
        L = 1 + (0.2 / 1.2) * th ** 2 / D["vc"] ** 2
        return np.log(Gfun(1 / L if rev else L, D["gb"], D["a0"], nu_mono))
    raise ValueError(p)

def gc_diag(p, th, f):
    D = GCD[f]; ok = np.isfinite(D["s0"])
    if p == "P5": return dict(note="not applicable")
    if p == "P1": X = 3 * D["s0"][ok] ** 2 / th ** 2; E = np.log(1 + X / D["nu"][ok]); return dict(X_med=float(np.median(X)), E_unscreened_med=float(np.median(E)))
    if p == "P2": s = (th / D["s0"][ok]) ** 3 * np.exp(-D["vrot"][ok] ** 2 / (2 * D["s0"][ok] ** 2))
    elif p == "P4": s = (D["rho"][ok] / th) * (2 * math.pi * D["s0"][ok] ** 2) ** -1.5 * np.exp(-D["vrot"][ok] ** 2 / (2 * D["s0"][ok] ** 2))
    else:
        L = 1 + th ** 2 / (3 * D["s0"][ok] ** 2); return dict(L_med=float(np.median(L)), E_unscreened_med=float(np.median(0.5 * np.log(L))))
    E = np.log(1 + s * D["phi"][ok]); return dict(s_med=float(np.median(s)), E_unscreened_med=float(np.median(E)))

# =====================================================================================================================  P5: QUMOND thin-disc quadrature
P("\n=== P5 geometry: QUMOND thin exponential disc (Hankel quadrature, cell-exact kernels; units R_d = G = 1, 2 pi G Sigma0 = 1)")
KG = np.unique(np.concatenate([np.geomspace(1e-4, 0.05, 500), np.linspace(0.05, 20.0, 8000), np.geomspace(20.0, 2000.0, 1500)]))
def trapw(x):
    w = np.zeros(len(x)); w[1:-1] = 0.5 * (x[2:] - x[:-2]); w[0] = 0.5 * (x[1] - x[0]); w[-1] = 0.5 * (x[-1] - x[-2]); return w
KC = 50.0                                                                 # low-pass window exp(-(k/KC)^2) on the phantom fields (source smoothing ~0.02 R_d)
WK = trapw(KG); WKW = WK * np.exp(-(KG / KC) ** 2)
RP = np.geomspace(1e-3, 100.0, 480); ZP = np.geomspace(1e-4, 100.0, 360)
def cedges(x):
    e = np.empty(len(x) + 1); e[1:-1] = np.sqrt(x[1:] * x[:-1]); e[0] = 0.0; e[-1] = x[-1] * math.sqrt(x[-1] / x[-2]); return e
ER, EZ = cedges(RP), cedges(ZP)
REV = np.linspace(0.5, 8.0, 61)
with np.errstate(all="ignore"):                                          # spurious Accelerate FP flags; finiteness asserted below
    J0R = j0(np.outer(RP, KG)); J1R = j1(np.outer(RP, KG)); J1E = j1(np.outer(REV, KG))
    _xj = lambda x: x[:, None] * j1(np.outer(x, KG)) / KG[None, :]
    KR = _xj(ER[1:]) - _xj(ER[:-1])                                       # (R', k): exact cell integral of x J0(kx) dx
    KZ = (np.exp(-np.outer(KG, EZ[:-1])) - np.exp(-np.outer(KG, EZ[1:]))) / KG[:, None]   # (k, z'): exact cell integral of e^-kz dz
SK = (1.0 / (2 * math.pi)) / (1 + KG ** 2) ** 1.5                         # Hankel of Sigma0 e^-R, Sigma0 = 1/(2 pi), R_d = 1
RR, ZZ = np.meshgrid(RP, ZP, indexing="ij"); RSPH = np.sqrt(RR ** 2 + ZZ ** 2); TRUNC = RSPH <= 100.0
def mm(A, x):
    with np.errstate(all="ignore"):
        y = A @ x
    assert np.all(np.isfinite(y)); return y
def mid_field_from_volume(rho):
    """midplane g_R(REV) of an axisymmetric, z-symmetric density rho(cells RP x ZP>0) (both sides), G = 1, windowed"""
    H = mm(KR.T, rho); T = 2 * np.sum(KZ * H, axis=1)
    return -2 * math.pi * mm(J1E, KG * T * WKW)
def mid_field_from_surface(sig):
    S = mm(KR.T, sig); return -2 * math.pi * mm(J1E, KG * S * WKW)
def grad2(F):
    return np.gradient(F, RP, axis=0, edge_order=2), np.gradient(F, ZP, axis=1, edge_order=2)
GR_N = np.empty((len(RP), len(ZP))); GZ_N = np.empty((len(RP), len(ZP)))
for jz, z in enumerate(ZP):
    wt = KG * np.exp(-KG * z) * SK * WK; GR_N[:, jz] = -2 * math.pi * mm(J1R, wt); GZ_N[:, jz] = -2 * math.pi * mm(J0R, wt)
GR0 = -2 * math.pi * mm(J1R, KG * SK * WK); SIG_D = np.exp(-RP) / (2 * math.pi)
gN_raw = -2 * math.pi * mm(J1E, KG * SK * WK); gN_mid = -2 * math.pi * mm(J1E, KG * SK * WKW)
# K7a Freeman (unwindowed Newtonian)
yv = REV / 2; V2 = 2 * yv ** 2 * (i0e(yv) * k0e(yv) - i1e(yv) * k1e(yv))       # 4 pi G Sigma0 R_d y^2 [I0K0 - I1K1]
k7a = float(np.max(np.abs(gN_raw / (-V2 / REV) - 1)))
# K7b / K7c Plummer (M = b = 1), production (windowed) field path
rhoP = 3 / (4 * math.pi) * (1 + RSPH ** 2) ** -2.5 * TRUNC
gP = mid_field_from_volume(rhoP); gP_an = -REV / (REV ** 2 + 1) ** 1.5
k7b = float(np.max(np.abs(gP / gP_an - 1)))
def qumond_sphere_check(nufun, a0=1.0):
    gr = -RR / (RSPH ** 2 + 1) ** 1.5; gz = -ZZ / (RSPH ** 2 + 1) ** 1.5; gm = np.sqrt(gr ** 2 + gz ** 2); nu = nufun(gm / a0)
    dR, dZ = grad2(nu); rho_eff = (nu * 3 / (4 * math.pi) * (1 + RSPH ** 2) ** -2.5 - (gr * dR + gz * dZ) / (4 * math.pi)) * TRUNC
    gq = mid_field_from_volume(rho_eff); galg = nufun(np.abs(gP_an) / a0) * gP_an
    return float(np.max(np.abs(gq / galg - 1)))
k7c = max(qumond_sphere_check(nu_e, a0) for a0 in (0.1, 1.0, 10.0))
def qumond_disc(GRg, GZg, GR0g, SIGg, gmid, nufun, a0):
    gm = np.sqrt(GRg ** 2 + GZg ** 2); nu = nufun(gm / a0); dR, dZ = grad2(nu)
    rho_v = -(GRg * dR + GZg * dZ) / (4 * math.pi) * TRUNC
    nu0 = nufun(np.sqrt(GR0g ** 2 + (2 * math.pi * SIGg) ** 2) / a0); sig_ph = (nu0 - 1) * SIGg
    return gmid + mid_field_from_volume(rho_v) + mid_field_from_surface(sig_ph)
# K7d (added during implementation; stronger than (c) for the disc path): Kuzmin disc, exact QUMOND in-plane g_R = nu(|g_N(0+)|) g_N,R
_den = (RR ** 2 + (1 + ZZ) ** 2) ** 1.5; SKk = np.exp(-KG) / (2 * math.pi); SIGk = 1 / (2 * math.pi * (RP ** 2 + 1) ** 1.5)
gmk = -2 * math.pi * mm(J1E, KG * SKk * WKW); k7d = 0.0
for a0 in (0.1, 1.0, 10.0):
    gqk = qumond_disc(-RR / _den, -(1 + ZZ) / _den, -RP / (RP ** 2 + 1) ** 1.5, SIGk, gmk, nu_e, a0)
    gex = nu_e(np.sqrt(gmk ** 2 + (1 / (REV ** 2 + 1) ** 1.5) ** 2) / a0) * gmk
    k7d = max(k7d, float(np.max(np.abs(gqk / gex - 1))))
KOK.append(check("K7 P5 numerics: (a) thin-disc g_R vs Freeman; (b) Plummer volume field vs GM(<r)/r^2; (c) QUMOND Plummer vs algebraic; "
                 "(d, added) Kuzmin disc vs exact QUMOND", k7a <= 1e-3 and k7b <= 1e-2 and k7c <= 2e-2 and k7d <= 3e-3,
                 f"(a) {k7a:.1e} (<=1e-3)  (b) {k7b:.1e} (<=1e-2)  (c) {k7c:.1e} (<=2e-2)  (d) {k7d:.1e} (<=3e-3)"))
def disc_delta(y0, nufun):
    a0 = 1.0 / y0; gq = qumond_disc(GR_N, GZ_N, GR0, SIG_D, gN_mid, nufun, a0)
    return np.log(gq / (nufun(np.abs(gN_mid) / a0) * gN_mid))
DEL = {}; sel16 = (REV >= 1.0 - 1e-9) & (REV <= 6.0 + 1e-9)
for y0 in (0.1, 1.0, 10.0):
    DEL[y0] = dict(nu_e=disc_delta(y0, nu_e), nu_s=disc_delta(y0, nu_s))
DELTA = float(np.mean([DEL[y0]["nu_e"][sel16] for y0 in DEL]))
DELTA_S = float(np.mean([DEL[y0]["nu_s"][sel16] for y0 in DEL]))
for y0 in DEL:
    d_ = DEL[y0]["nu_e"]
    P(f"  y0 = {y0:>4}: delta(R) nu_e  R=0.5 {d_[0]:+.4f}  R=1 {d_[REV.searchsorted(1.0)]:+.4f}  R=2 {d_[REV.searchsorted(2.0)]:+.4f}  R=4 {d_[REV.searchsorted(4.0)]:+.4f}  "
      f"R=6 {d_[REV.searchsorted(6.0)]:+.4f}  R=8 {d_[-1]:+.4f};  mean over [1,6] {np.mean(d_[sel16]):+.4f} (nu_s {np.mean(DEL[y0]['nu_s'][sel16]):+.4f})")
P(f"  <delta_disc> = {DELTA:+.4f} (nu_e, ln units = {DELTA / LN10:+.4f} dex); diagnostic nu_s {DELTA_S:+.4f}.  P5 predicts E = -<delta> = {-DELTA:+.4f} "
  f"for spheres / point-mass lensing, 0 for SPARC discs.  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
RES["P5"] = dict(delta_mean=DELTA, delta_mean_nu_s=DELTA_S, window_kc=KC, per_y0={str(y0): dict(mean=float(np.mean(DEL[y0]["nu_e"][sel16])), min=float(DEL[y0]["nu_e"].min()),
                 max=float(DEL[y0]["nu_e"].max()), at_R05=float(DEL[y0]["nu_e"][0]), mean_nu_s=float(np.mean(DEL[y0]["nu_s"][sel16]))) for y0 in DEL},
                 K7=dict(a=k7a, b=k7b, c=k7c, d=k7d))
del J0R, J1R, KR, KZ, GR_N, GZ_N, RR, ZZ, RSPH, TRUNC, rhoP, _den

# =====================================================================================================================  K5: solvers
k5 = []
for f in FOOTS:
    for p, th0 in (("P1", 1e30), ("P2", 0.0), ("P3", 0.0), ("P4", 1e300)):
        k5.append(float(np.max(np.abs(dw_pred(p, th0, f, 10.0)))))
        k5.append(float(np.max(np.abs(sp_pred(p, th0, f, 10.0)))))
        k5.append(float(np.max(np.abs(cl_pred(p, th0, f)))))
        cen = lens_central("LS", f, LENS_NOM, SHIFT_N2); k5.append(float(np.max(np.abs(lens_pointE(p, th0, f, cen, np.geomspace(1e-14, 1e-11, 9))))))
    th = 3.0 * p1_ccrit(f); k5p1 = float(np.max(np.abs(dw_pred("P1", th, f, 10.0) - p1_bisect(th, f, 10.0))))
    D = DWD[f]; t2 = 0.5 * dw_pred("P2", 8.0, f, 10.0); r2 = np.exp(2 * t2) - 1 - D["phi"] * (D["w"] * (8.0 / (np.exp(t2) * D["sl"])) ** 3 + (1 - D["w"]) * (8.0 / 10.0) ** 3)
    t3 = 0.5 * dw_pred("P3", 30.0, f, 10.0); r3 = np.exp(2 * t3) - Gfun(1 + D["w"] * 900.0 / (3 * np.exp(2 * t3) * D["sl"] ** 2), D["gb"], D["a0"], nu_e)
    t4 = 0.5 * dw_pred("P4", 1e-5, f, 10.0)
    r4 = np.exp(2 * t4) - 1 - D["phi"] * (D["rho"] / 1e-5) * (D["w"] * (2 * math.pi * np.exp(2 * t4) * D["sl"] ** 2) ** -1.5 + (1 - D["w"]) * (2 * math.pi * 100.0) ** -1.5)
    k5 += [0.0]; RES.setdefault("K5", {})[f] = dict(p1_closed_vs_bisect=k5p1, resid=[float(np.max(np.abs(r2))), float(np.max(np.abs(r3))), float(np.max(np.abs(r4 / np.exp(2 * t4))))])
k5z = max(k5); k5b = max(RES["K5"][f]["p1_closed_vs_bisect"] for f in FOOTS); k5r = max(max(RES["K5"][f]["resid"]) for f in FOOTS)
KOK.append(check("K5 solvers: zero surplus -> E = 0 everywhere; P1 closed form = bisection; self-consistent roots satisfy their equations",
                 k5z <= 1e-12 and k5b <= 1e-9 and k5r <= 1e-10, f"zero-surplus max |E| {k5z:.1e}; P1 closed vs bisect {k5b:.1e}; root residual {k5r:.1e}; "
                 f"cluster nu identity {max(k5c):.1e}"))
K_ALL = all(KOK)
P(f"  K-stage {'ALL PASS (K8 checked below)' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
if not K_ALL:
    P("  A K-test failed: per FROZEN_CRITERIA section 7 the lane stops; no class is reported."); RES["class"] = None; finish(2)

# =====================================================================================================================  observed structures per footing / variant
VARS = {"V0": dict(opt={}, floor=FLOOR0, shift=SHIFT_N2), "V6": dict(opt={}, floor=FLOOR_V6, shift=SHIFT_N2),
        "V7": dict(opt={"noshift": True}, floor=FLOOR0, shift=0.0)}
def obs_struct(f, vk):
    V = VARS[vk]; cells, C = (OBS0[f] if vk != "V7" else build(f, V["opt"])[:2])
    Ct = C + V["floor"] ** 2 * np.eye(len(cells)); E = np.array([c["E"] for c in cells]); cls = np.array([c["cls"] for c in cells])
    wv = np.array([c["w"] for c in cells]); lgv = np.array([c["lg"] for c in cells]); ops = gls_ops(cells, Ct); S = dict(cells=cells, Ct=Ct, E=E, cls=cls, w=wv, lg=lgv, ops=ops)
    for c in ("DW", "CL"):                                                  # GLS slope operators
        ix = ops[c]["ix"]; x = lgv[ix] - lgv[ix].mean(); X = np.vstack([np.ones(len(ix)), x]).T; Ci = np.linalg.inv(Ct[np.ix_(ix, ix)])
        Cov = np.linalg.inv(X.T @ Ci @ X); S[f"slope_{c}"] = dict(ix=ix, B=(Cov @ X.T @ Ci)[1], se=math.sqrt(Cov[1, 1]))
    iD, iL = ops["DW"]["ix"], ops["LS"]["ix"]; shared = sorted(set(wv[iD]) & set(wv[iL]))
    jD = np.array([iD[list(wv[iD]).index(x)] for x in shared]); jL = np.array([iL[list(wv[iL]).index(x)] for x in shared])
    Cd = np.diag(np.diag(Ct)[jD]) + Ct[np.ix_(jL, jL)]; Ci = np.linalg.inv(Cd); one = np.ones(len(shared)); a = float(one @ Ci @ one)
    S["F7"] = dict(jD=jD, jL=jL, w=(Ci @ one) / a, se=a ** -0.5, windows=shared)
    S["DWCi"] = np.linalg.inv(Ct[np.ix_(iD, iD)])
    # lens window weight vectors
    S["lens"] = {}
    for cl, key in (("LD", "disc"), ("LS", "sph")):
        shift = V["shift"] if cl == "LS" else 0.0; gbs, go, C_, gl = lens_set(key, f, shift); kk = np.digitize(np.log10(gbs), GRID) - 1; Wl = []
        for i in ops[cl]["ix"]:
            Sx = np.where(kk == wv[i])[0]; Ci_ = np.linalg.inv(C_[np.ix_(Sx, Sx)]); a_ = gl[Sx] @ Ci_ @ gl[Sx]; Wl.append((Sx, (Ci_ @ gl[Sx]) / a_))
        S["lens"][cl] = dict(gbs=gbs, gl=gl, W=Wl, shift=shift)
    # SPARC window groupings
    S["sparc"] = {}
    for cl, msk in (("SS", SMALL), ("SL", LARGE)):
        idx = np.where(msk)[0]; kk = np.digitize(sp_lg[idx], GRID) - 1; grp = []
        for i in ops[cl]["ix"]:
            sel = idx[kk == wv[i]]; u, inv = np.unique(sp_code[sel], return_inverse=True); grp.append((sel, inv, len(u)))
        S["sparc"][cl] = grp
    # cluster windows
    D = CLD[f]; kk = np.digitize(D["lr"], GRID) - 1; S["clus"] = [(kk == wv[i]) for i in ops["CL"]["ix"]]
    # dwarf cell membership
    Dd = DWD[f]; S["dwcell"] = [Dd["k"] == wv[i] for i in ops["DW"]["ix"]]
    return S

def sec_dw(p, th, f, S, sg, rev=False):
    dwE = dw_pred(p, th, f, sg, rev); return np.array([np.mean(dwE[m]) for m in S["dwcell"]]), dwE
def sec_sp(p, th, f, S, sd, rev=False):
    spE = sp_pred(p, th, f, sd, rev)
    return {cl: np.array([np.mean(np.bincount(inv, spE[sel]) / np.bincount(inv)) for sel, inv, n in S["sparc"][cl]]) for cl in ("SS", "SL")}
def sec_lens(p, th, f, S, lc, rev=False):
    out = {}
    for cl in ("LD", "LS"):
        Ls = S["lens"][cl]; cen = lens_central(cl, f, lc, S["lens"]["LS"]["shift"]); pe = lens_pointE(p, th, f, cen, Ls["gbs"], rev)
        out[cl] = np.array([math.log(float(wv_ @ (Ls["gl"][Sx] * np.exp(pe[Sx])))) for Sx, wv_ in Ls["W"]])
    return out
def sec_cl(p, th, f, S, rev=False):
    D = CLD[f]; ce = cl_pred(p, th, f, rev); WP = D["W"] * D["Pm"]
    return np.array([math.log(float((WP[m] * np.exp(ce[m])).sum() / WP[m].sum())) for m in S["clus"]])
def pred_cells(p, th, f, S, sg, sd, lc, rev=False, flip=False):
    """predicted values for every non-GC cell (dict by class) + per-dwarf E"""
    dwc, dwE = sec_dw(p, th, f, S, sg, rev); out = {"DW": dwc}; out.update(sec_sp(p, th, f, S, sd, rev)); out.update(sec_lens(p, th, f, S, lc, rev))
    out["CL"] = sec_cl(p, th, f, S, rev)
    if flip:
        out = {k: -v for k, v in out.items()}; dwE = -dwE
    return out, dwE

def dw_mean(p, th, f, S, sg, rev=False):
    dwE = dw_pred(p, th, f, sg, rev); cellsE = np.array([np.mean(dwE[m]) for m in S["dwcell"]]); return float(S["ops"]["DW"]["w"] @ cellsE)

TH_BR = {"P2": (1e-3, 1e4), "P3": (1e-3, 1e5), "P4": (1e-14, 1e8)}
def calibrate(p, f, S, sg, target, rev=False, ccrit=None, root="low"):
    """theta with predicted DW class mean = target. root 'low' = first sign change (A1: P3's curve is non-monotone; the
    branch continuous with zero surplus is graded), 'high' = last sign change (diagnostic only)."""
    if p == "P5": return None
    if p == "P1":
        cc = ccrit if ccrit is not None else p1_ccrit(f); lo, hi = (cc * (1 + 1e-7), 1e6) if not rev else (1e-3, 1e6)
    else:
        lo, hi = TH_BR[p]
    g = lambda lt: dw_mean(p, math.exp(lt), f, S, sg, rev) - target
    grid = np.linspace(math.log(lo), math.log(hi), 121); vals = np.array([g(x) for x in grid])
    ok = np.isfinite(vals); sc = np.where(ok[:-1] & ok[1:] & (np.sign(vals[:-1]) != np.sign(vals[1:])))[0]
    if not len(sc): return None
    i = sc[0] if root == "low" else sc[-1]
    if root == "high" and len(sc) < 2: return None
    return math.exp(brentq(g, grid[i], grid[i + 1], xtol=1e-13, rtol=1e-13, maxiter=200))

def calib_table(p, f, S, sg, thc):
    """(sorted DW means, log theta) on the monotone branch of the DW-mean curve that contains thc (INJECT interpolation)"""
    lo = (p1_ccrit(f) * (1 + 1e-7)) if p == "P1" else TH_BR[p][0]; hi = 1e6 if p == "P1" else TH_BR[p][1]
    lg_ = np.linspace(math.log(max(lo, thc / 60)), math.log(min(hi, thc * 60)), 301); mv = np.array([dw_mean(p, math.exp(x), f, S, sg) for x in lg_])
    ic = int(np.argmin(np.abs(lg_ - math.log(thc)))); d = np.sign(np.diff(mv)); s0 = d[min(ic, len(d) - 1)]
    a = ic
    while a > 0 and d[a - 1] == s0 and np.isfinite(mv[a - 1]): a -= 1
    b = ic
    while b < len(d) and d[b] == s0 and np.isfinite(mv[b + 1]): b += 1
    seg_m, seg_l = mv[a:b + 1], lg_[a:b + 1]; o = np.argsort(seg_m)
    return seg_m[o], seg_l[o]

# =====================================================================================================================  facts
FACTS = ["F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8a", "F8b", "F9", "F10"]
FDESC = {"F0": "dwarf excess (P5 only)", "F1": "red/sph lenses LS", "F2": "blue/disc lenses LD", "F3": "SPARC small SS", "F4": "SPARC large SL",
         "F5": "clusters CL", "F6": "cluster slope dE/dlg", "F7": "DW - LS matched windows", "F8a": "DW cells chi2 (shape)", "F8b": "DW slope dE/dlg",
         "F9": "gas split c (HI - gas-free)", "F10": "size split d (log r12)"}
SIGN_FACTS = {"F1", "F5", "F6", "F7", "F8b", "F9", "F10"}
BOOT = {}
def boot_ops(f):
    if f in BOOT: return BOOT[f]
    D = DWD[f]; rng = np.random.default_rng(921); n = len(D["E"]); idx = rng.integers(0, n, (NBOOT, n)); out = {}
    for key, xc in (("F9", D["hi"].astype(float)), ("F10", np.log10(D["r12"]))):
        X = np.vstack([np.ones(n), D["lg"], xc]).T; M = np.linalg.pinv(X)[2]
        Xb = X[idx]; Mb = np.linalg.pinv(Xb)[:, 2, :]                       # (NBOOT, n)
        out[key] = dict(M=M, Mb=Mb, idx=idx)
    BOOT[f] = out; return out
def ols_obs(f, key, y):
    B = boot_ops(f)[key]; c = float(B["M"] @ y); cb = np.einsum("bn,bn->b", B["Mb"], y[B["idx"]]); return c, float(np.std(cb, ddof=1))

def fact_values(S, cellsE, dwE, f):
    """the fact statistics from a set of (observed or predicted) cell values; linear operators shared"""
    ops = S["ops"]; v = {}
    for fc, cl in (("F0", "DW"), ("F1", "LS"), ("F2", "LD"), ("F3", "SS"), ("F4", "SL"), ("F5", "CL")):
        v[fc] = float(ops[cl]["w"] @ cellsE[cl])
    v["F6"] = float(S["slope_CL"]["B"] @ cellsE["CL"]); v["F8b"] = float(S["slope_DW"]["B"] @ cellsE["DW"])
    F7 = S["F7"]; dw_w = {int(x): e for x, e in zip(S["w"][ops["DW"]["ix"]], cellsE["DW"])}; ls_w = {int(x): e for x, e in zip(S["w"][ops["LS"]["ix"]], cellsE["LS"])}
    v["F7"] = float(F7["w"] @ np.array([dw_w[x] - ls_w[x] for x in F7["windows"]]))
    v["F9"] = float(boot_ops(f)["F9"]["M"] @ dwE); v["F10"] = float(boot_ops(f)["F10"]["M"] @ dwE)
    return v

def obs_facts(S, f, cellsE=None, dwE=None):
    if cellsE is None:
        cellsE = {c: S["E"][S["ops"][c]["ix"]] for c in ("DW", "LS", "LD", "SS", "SL", "CL")}; dwE = DWD[f]["E"]
    v = fact_values(S, cellsE, dwE, f); se = {"F0": S["ops"]["DW"]["se"], "F1": S["ops"]["LS"]["se"], "F2": S["ops"]["LD"]["se"], "F3": S["ops"]["SS"]["se"],
                                              "F4": S["ops"]["SL"]["se"], "F5": S["ops"]["CL"]["se"], "F6": S["slope_CL"]["se"], "F8b": S["slope_DW"]["se"], "F7": S["F7"]["se"]}
    for key in ("F9", "F10"):
        v[key], se[key] = ols_obs(f, key, dwE)
    return v, se, cellsE["DW"]

ZTF = float(norm.isf(0.0027 / 2 / 55))

def grade(p, f, S, obsv, obsse, obsDW, mode=None, prec=None, withhold=()):
    """full grading of posit p on footing f for the observed facts (obsv, obsse, obsDW); prec = precomputed predictions"""
    target = obsv["F0"]; seD = obsse["F0"]
    corners_sg = [1] if p == "P5" else [0, 1, 2]
    rec = dict(calib={}, facts={}, nominal_ok=False)
    zs = {k: [] for k in FACTS}; signs = {k: [] for k in FACTS}; p8 = []; nom = {}
    for sgi in corners_sg:
        sg = SG[sgi]
        if prec is not None and (sgi, "th") in prec:
            th, thp, thm = prec[(sgi, "th")]
        elif p == "P5":
            th = thp = thm = None
        else:
            rev = (mode == "rev")
            th = calibrate(p, f, S, sg, target, rev); thp = calibrate(p, f, S, sg, target + seD, rev) if th else None
            thm = calibrate(p, f, S, sg, target - seD, rev) if th else None
        rec["calib"][SG[sgi]] = dict(theta=th, theta_plus=thp, theta_minus=thm)
        if p != "P5" and th is None: continue
        sgn = -1.0 if mode == "flip" else 1.0; rv = (mode == "rev"); cache = {}
        T3 = (th, thp if thp else th, thm if thm else th)
        def assemble(th_, sdi, lc):
            if th_ not in cache:
                dwc, dwE_ = sec_dw(p, th_, f, S, sg, rv); cache[th_] = dict(dw=(sgn * dwc, sgn * dwE_), cl=sgn * sec_cl(p, th_, f, S, rv), sp={}, lens={})
            c_ = cache[th_]
            if sdi not in c_["sp"]: c_["sp"][sdi] = {k: sgn * x for k, x in sec_sp(p, th_, f, S, SD[sdi], rv).items()}
            if lc not in c_["lens"]: c_["lens"][lc] = {k: sgn * x for k, x in sec_lens(p, th_, f, S, lc, rv).items()}
            o_ = {"DW": c_["dw"][0], "CL": c_["cl"]}; o_.update(c_["sp"][sdi]); o_.update(c_["lens"][lc]); return o_, c_["dw"][1]
        def pc(th_, sd, lc): return assemble(th_, SD.index(sd), lc)
        # dwarf-only + cluster facts (sd, lens corner nominal)
        base, dwE = pc(T3[0], SD[1], LENS_NOM); bp, dwp = pc(T3[1], SD[1], LENS_NOM); bm, dwm = pc(T3[2], SD[1], LENS_NOM)
        vb = fact_values(S, base, dwE, f); vp = fact_values(S, bp, dwp, f); vm = fact_values(S, bm, dwm, f)
        def zrec(key, val, vpv, vmv):
            sp = abs(vpv - vmv) / 2; z = (val - obsv[key]) / math.sqrt(obsse[key] ** 2 + sp ** 2)
            sw = (key in SIGN_FACTS and np.sign(val) == -np.sign(obsv[key]) and abs(obsv[key]) >= 2 * obsse[key] and abs(val) >= obsse[key])
            return z, bool(sw), sp
        for key in ("F0", "F5", "F6", "F8b", "F9", "F10"):
            z, sw, sp = zrec(key, vb[key], vp[key], vm[key]); zs[key].append(z); signs[key].append(sw)
            if sgi == 1 or p == "P5": nom[key] = dict(pred=vb[key], z=z, sign_wrong=sw, s_pred=sp)
        r = obsDW - base["DW"]; chi = float(r @ S["DWCi"] @ r); pv = float(CHI2.sf(chi, len(r) - 1)); p8.append(pv)
        if sgi == 1 or p == "P5": nom["F8a"] = dict(chi2=chi, dof=len(r) - 1, p=pv)
        # SPARC corners
        for sdi in range(3):
            b2, _ = pc(T3[0], SD[sdi], LENS_NOM); b2p = pc(T3[1], SD[sdi], LENS_NOM)[0]; b2m = pc(T3[2], SD[sdi], LENS_NOM)[0]
            v2 = fact_values(S, b2, dwE, f); v2p = fact_values(S, b2p, dwp, f); v2m = fact_values(S, b2m, dwm, f)
            for key in ("F3", "F4"):
                z, sw, sp = zrec(key, v2[key], v2p[key], v2m[key]); zs[key].append(z); signs[key].append(sw)
                if (sgi == 1 or p == "P5") and sdi == 1: nom[key] = dict(pred=v2[key], z=z, sign_wrong=sw, s_pred=sp)
        # lens corners
        for lc in (LENS_CORNERS if p != "P5" else [LENS_NOM]):
            b3, _ = pc(T3[0], SD[1], lc); b3p = pc(T3[1], SD[1], lc)[0]; b3m = pc(T3[2], SD[1], lc)[0]
            v3 = fact_values(S, b3, dwE, f); v3p = fact_values(S, b3p, dwp, f); v3m = fact_values(S, b3m, dwm, f)
            for key in ("F1", "F2", "F7"):
                z, sw, sp = zrec(key, v3[key], v3p[key], v3m[key]); zs[key].append(z); signs[key].append(sw)
                if (sgi == 1 or p == "P5") and lc == LENS_NOM: nom[key] = dict(pred=v3[key], z=z, sign_wrong=sw, s_pred=sp)
    graded = [k for k in FACTS if (k != "F0" or p == "P5") and k not in withhold]
    if not any(rec["calib"][s]["theta"] for s in rec["calib"]) and p != "P5":
        rec.update(cls="FAILS", reason="calibration impossible", decisive=None, robust_TF=True); return rec
    failed = {}
    for k in graded:
        if k == "F8a":
            if p8 and all(x < 0.0027 for x in p8): failed[k] = dict(min_p=float(max(p8)))
            continue
        if not zs[k]: continue
        mz = float(min(abs(z) for z in zs[k]))
        if mz >= 3 or all(signs[k]): failed[k] = dict(min_abs_z=mz, sign_wrong_all=bool(all(signs[k])))
    for k in graded:
        if k in nom: rec["facts"][k] = dict(obs=obsv.get(k), se=obsse.get(k), **nom[k])
        if k in zs and zs[k]: rec["facts"].setdefault(k, {})["min_abs_z"] = float(min(abs(z) for z in zs[k]))
        if k == "F8a" and p8: rec["facts"].setdefault(k, {})["max_p_over_corners"] = float(max(p8))
    jk = [k for k in ("F1", "F2", "F3", "F4", "F5") if k in graded and k in nom]
    chij = float(sum(nom[k]["z"] ** 2 for k in jk)); pj = float(CHI2.sf(chij, len(jk))) if jk else float("nan")
    rec.update(joint_chi2=chij, joint_dof=len(jk), joint_p=pj, failed=failed)
    have_nom = all(k in nom for k in graded)
    surv = have_nom and all(abs(nom[k]["z"]) < 2 and not nom[k]["sign_wrong"] for k in graded if k != "F8a") and nom["F8a"]["p"] >= 0.05 and pj >= 0.05
    if failed:
        dec = max(failed.items(), key=lambda kv: (kv[1].get("sign_wrong_all", False), kv[1].get("min_abs_z", 0.0)))
        rob = any(v.get("sign_wrong_all") or v.get("min_abs_z", 0) >= ZTF or ("min_p" in v and v["min_p"] < 2 * norm.sf(ZTF)) for v in failed.values())
        rec.update(cls="FAILS", decisive=dec[0], robust_TF=bool(rob))
    elif surv:
        rec.update(cls="SURVIVES", decisive=None, robust_TF=None)
    else:
        rec.update(cls="UNDERDETERMINED", decisive=None, robust_TF=None)
    return rec

def fmt_rec(p, rec):
    if rec.get("reason"): return f"    {p}: {rec['cls']} ({rec['reason']})"
    th = rec["calib"].get(10.0, {}).get("theta") if p != "P5" else None
    s = f"    {p}: {rec['cls']}" + (f"  theta_nom {th:.4g}" if th else "")
    if rec["cls"] == "FAILS":
        fl = ", ".join(f"{k} " + ("SIGN" if v.get("sign_wrong_all") else (f"min|z| {v['min_abs_z']:.1f}" if "min_abs_z" in v else f"max p {v['min_p']:.1e}")) for k, v in rec["failed"].items())
        s += f"  [{'robust to trials factor' if rec['robust_TF'] else 'local only'}]  failed: {fl}"
    s += f"  | joint chi2 {rec['joint_chi2']:.1f}/{rec['joint_dof']} p {rec['joint_p']:.2g}"
    return s

# =====================================================================================================================  MAIN
STRUCT = {f: {vk: obs_struct(f, vk) for vk in VARS} for f in FOOTS}
OBSF = {f: {vk: obs_facts(STRUCT[f][vk], f) for vk in VARS} for f in FOOTS}

# ---- K8: interpolated calibration (used only by INJECT) vs exact brentq; prints only the difference
k8 = []
for f in FOOTS:
    S = STRUCT[f]["V0"]; tgt = OBSF[f]["V0"][0]["F0"]
    for p in ("P1", "P2", "P3", "P4"):
        th = calibrate(p, f, S, SG[1], tgt)
        if th is None: continue
        tm, tl = calib_table(p, f, S, SG[1], th); thi = math.exp(np.interp(tgt, tm, tl))
        a_, _ = pred_cells(p, th, f, S, SG[1], SD[1], LENS_NOM); b_, _ = pred_cells(p, thi, f, S, SG[1], SD[1], LENS_NOM)
        k8.append(max(abs(float(S["ops"][c]["w"] @ a_[c]) - float(S["ops"][c]["w"] @ b_[c])) for c in a_))
ok8 = check("K8 interpolated calibration (INJECT only) vs exact brentq: every predicted class mean", len(k8) > 0 and max(k8) <= 1e-3,
            f"{len(k8)} posit-footings calibrated; max |d class mean| {max(k8) if k8 else float('nan'):.1e}")
if not ok8:
    P("  K8 failed: lane stops."); RES["class"] = None; finish(2)
P(f"  K-stage K1-K8 ALL PASS  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
if KONLY:
    P("  CFG921_KONLY=1: K-stage only (no prediction or class printed)."); finish(0)

if not MUT:
    P("\n=== observed facts (E in ln units; dex = E/ln10)")
    RES["observed"] = {}
    for f in FOOTS:
        v, se, _ = OBSF[f]["V0"]; RES["observed"][f] = {k: dict(obs=v[k], se=se[k]) for k in v}
        P(f"  [{f}] " + "  ".join(f"{k} {v[k]:+.3f}+-{se[k]:.3f}" for k in FACTS if k in v and k != "F8a"))
    # ---- stage P: predictions before comparison
    P("\n=== stage P: each posit's predictions at its calibrated constant (nominal corner), BEFORE any comparison")
    RES["predictions"] = {}
    for f in FOOTS:
        S = STRUCT[f]["V0"]; v, se, oDW = OBSF[f]["V0"]; RES["predictions"][f] = {}
        for p in POSITS:
            th = calibrate(p, f, S, SG[1], v["F0"]) if p != "P5" else None
            if p != "P5" and th is None:
                P(f"  [{f}] {p}: calibration impossible"); RES["predictions"][f][p] = dict(theta=None); continue
            pcs, dwE = pred_cells(p, th, f, S, SG[1], SD[1], LENS_NOM)
            pv = fact_values(S, pcs, dwE, f); gdi = gc_diag(p, th, f)
            cenS = lens_central("LS", f, LENS_NOM, SHIFT_N2); cenD = lens_central("LD", f, LENS_NOM, 0.0)
            resid = DWD[f]["E"] - dwE
            RES["predictions"][f][p] = dict(theta=th, facts=pv, cells={k: v_.tolist() for k, v_ in pcs.items()}, gc_unscreened=gdi,
                                            dw_resid_sd=float(np.std(resid, ddof=1)), dw_obs_sd=float(np.std(DWD[f]["E"], ddof=1)),
                                            dw_E_range=[float(np.min(dwE)), float(np.max(dwE))], lens_central=dict(LS=cenS, LD=cenD))
            P(f"  [{f}] {p} theta {('%.4g' % th) if th else '-':>9}: " + "  ".join(f"{k} {pv[k]:+.3f}" for k in FACTS if k != "F8a")
              + f"  | per-dwarf E {np.min(dwE):+.2f}..{np.max(dwE):+.2f}, resid sd {np.std(resid, ddof=1):.2f} (obs sd {np.std(DWD[f]['E'], ddof=1):.2f})")
            P(f"        DW cells pred " + " ".join(f"{x:+.2f}" for x in pcs["DW"]) + "  | CL cells pred " + " ".join(f"{x:+.2f}" for x in pcs["CL"])
              + "  | LS cells pred " + " ".join(f"{x:+.2f}" for x in pcs["LS"]) + f"  | GC unscreened {gdi}")
    # ---- stage G: grading
    P(f"\n=== stage G: grading (lenient-corner rule; FAIL = min|z| >= 3 or sign wrong at every corner; SURVIVES at nominal; z_TF = {ZTF:.3f})")
    RES["byfoot"] = {}
    for f in FOOTS:
        RES["byfoot"][f] = {}
        for vk in ("V0", "V6", "V7"):
            S = STRUCT[f][vk]; v, se, oDW = OBSF[f][vk]; RES["byfoot"][f][vk] = {}
            P(f"  [{f} | {vk}]")
            for p in POSITS:
                rec = grade(p, f, S, v, se, oDW); RES["byfoot"][f][vk][p] = rec; P(fmt_rec(p, rec))
                if vk == "V0":
                    recC = grade(p, f, S, v, se, oDW, withhold=("F5", "F6")); RES["byfoot"][f]["VC_" + p] = recC
                    P("      VC (clusters withheld): " + fmt_rec(p, recC).strip())
                    if p in ("P1", "P2", "P3", "P4", "P5") and rec.get("facts"):
                        P("      nominal z: " + "  ".join(f"{k} {rec['facts'][k]['z']:+.1f}" + ("!" if rec["facts"][k].get("sign_wrong") else "")
                                                     for k in FACTS if k in rec["facts"] and "z" in rec["facts"][k])
                          + (f"  F8a p {rec['facts']['F8a']['p']:.2g}" if "F8a" in rec["facts"] and "p" in rec["facts"]["F8a"] else ""))
    # ---- classes
    P("\n=== classes")
    CLS = {}; FRAG = {}; COND = {}
    for p in POSITS:
        per = {f: RES["byfoot"][f]["V0"][p]["cls"] for f in FOOTS}
        ov = per["canonical"] if per["canonical"] == per["alt"] else "UNDERDETERMINED (SPLIT BY FOOTING)"
        ch = [f"{f}:{vk}" for f in FOOTS for vk in ("V6", "V7") if RES["byfoot"][f][vk][p]["cls"] != per[f]]
        perC = {f: RES["byfoot"][f]["VC_" + p]["cls"] for f in FOOTS}
        ovC = perC["canonical"] if perC["canonical"] == perC["alt"] else "UNDERDETERMINED (SPLIT BY FOOTING)"
        CLS[p] = dict(per_footing=per, overall=ov, fragile=bool(ch), variants_changing=ch, VC_per_footing=perC, VC_overall=ovC,
                      robust_TF={f: RES["byfoot"][f]["V0"][p].get("robust_TF") for f in FOOTS}, decisive={f: RES["byfoot"][f]["V0"][p].get("decisive") for f in FOOTS})
        P(f"  {p} {PNAME[p]}: canonical {per['canonical']}, alt {per['alt']} -> {ov}{' [FRAGILE: ' + ', '.join(ch) + ']' if ch else ''}"
          f"  | VC (clusters withheld, pending CFG922): {perC['canonical']} / {perC['alt']} -> {ovC}")
    RES["classes"] = CLS; RES["trials"] = dict(N_T=5, n_facts=11, z_TF=ZTF)
    surv = [p for p in POSITS if any(CLS[p]["per_footing"][f] == "SURVIVES" for f in FOOTS)]
    RES["survivors"] = surv
    P(f"  survivors (any footing): {surv if surv else 'NONE'}; trials factor N_T = 5 (z_TF {ZTF:.2f})")
    # ---- AMENDMENT A1 diagnostics (post-freeze, NO class weight)
    P("\n=== A1 diagnostics (post-freeze; no class weight)")
    RES["A1_diagnostics"] = {}
    ZK = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8b", "F9", "F10")
    for f in FOOTS:
        S = STRUCT[f]["V0"]; v, se, oDW = OBSF[f]["V0"]; D = DWD[f]; cel = np.zeros(len(D["w"]), bool)
        for m in S["dwcell"]: cel |= m
        vb2 = 3 * D["w"] * D["sl"] ** 2 / D["nu"]; icrit = int(np.argmax(vb2)); cc_all = math.sqrt(vb2[icrit]); cc_cel = math.sqrt(vb2[cel].max())
        mean_max = dw_mean("P1", cc_all * (1 + 1e-7), f, S, SG[1]); th_r = calibrate("P1", f, S, SG[1], v["F0"], ccrit=cc_cel)
        icc = int(np.where(cel)[0][np.argmax(vb2[cel])])
        with np.errstate(all="ignore"):
            mean_rel = dw_mean("P1", cc_cel * (1 + 1e-7), f, S, SG[1]); mean_rel12 = dw_mean("P1", cc_cel * (1 + 1e-12), f, S, SG[1])
        dg = dict(critical_dwarf=D["names"][icrit], critical_lg=float(D["lg"][icrit]), critical_in_cells=bool(cel[icrit]), c_crit_all=cc_all,
                  c_crit_celled=cc_cel, critical_celled_dwarf=D["names"][icc], max_class_mean_in_domain=mean_max,
                  relaxed_class_mean_eps1e7=mean_rel, relaxed_class_mean_eps1e12=mean_rel12, theta_relaxed=th_r)
        if th_r:
            run = np.where(vb2 >= th_r ** 2)[0]
            with np.errstate(all="ignore"):
                pcs_r, dwE_r = pred_cells("P1", th_r, f, S, SG[1], SD[1], LENS_NOM); pv_r = fact_values(S, pcs_r, dwE_r, f)
            r_ = oDW - pcs_r["DW"]; chi_r = float(r_ @ S["DWCi"] @ r_)
            dg.update(n_runaway=int(len(run)), runaway=[D["names"][i] for i in run], dw_chi2=chi_r, dw_dof=len(r_) - 1,
                      z_nominal={k: float((pv_r[k] - v[k]) / se[k]) for k in ZK}, pred={k: float(pv_r[k]) for k in ZK})
        RES["A1_diagnostics"][f"{f}|P1_relaxed"] = dg
        P(f"  [{f}] P1 in the frozen equilibrium domain (all 83 dwarfs): runaway threshold c_crit {cc_all:.3f} km/s set by {D['names'][icrit]} "
          f"(log g_bar {D['lg'][icrit]:.2f}, in a graded cell: {bool(cel[icrit])}); max DW class mean {mean_max:.4f} < observed {v['F0']:.3f} -> calibration impossible")
        P(f"        relaxed (equilibrium only for dwarfs in graded cells): threshold {cc_cel:.3f} km/s set by {D['names'][icc]}; DW class mean at "
          f"c_* = threshold x (1 + 1e-7) {mean_rel:.3f}, x (1 + 1e-12) {mean_rel12:.3f} (E diverges only logarithmically); "
          f"dwarfs outside the cells in runaway at that threshold: {int(np.sum(vb2 > vb2[icc]))} -> "
          + ("calibratable within the 1e-7 bracket" if th_r else "not reachable within the 1e-7 bracket; reachable only with c_* fine-tuned to "
             f"between 1e-12 and 1e-7 (fractional) of {D['names'][icc]}'s runaway, the class mean then carried by one dwarf at the edge of runaway"))
        dg["n_runaway_at_relaxed_threshold"] = int(np.sum(vb2 > vb2[icc]))
        dg["runaway_at_relaxed_threshold"] = [D["names"][i] for i in np.where(vb2 > vb2[icc])[0]]
        if th_r:
            P(f"        relaxed (equilibrium only for dwarfs in graded cells): c_* {th_r:.3f} km/s; runaway dwarfs {len(run)} ({', '.join(dg['runaway'][:6])}"
              f"{'...' if len(run) > 6 else ''}); DW chi2 {chi_r:.1f}/{len(r_) - 1}; z: " + "  ".join(f"{k} {dg['z_nominal'][k]:+.1f}" for k in ZK))
        th_hi = calibrate("P3", f, S, SG[1], v["F0"], root="high"); dh = dict(theta_high=th_hi)
        if th_hi:
            pcs_h, dwE_h = pred_cells("P3", th_hi, f, S, SG[1], SD[1], LENS_NOM); pv_h = fact_values(S, pcs_h, dwE_h, f); r_ = oDW - pcs_h["DW"]
            dh.update(z_nominal={k: float((pv_h[k] - v[k]) / se[k]) for k in ZK}, pred={k: float(pv_h[k]) for k in ZK}, dw_chi2=float(r_ @ S["DWCi"] @ r_))
            P(f"  [{f}] P3 upper root (diagnostic): v_w {th_hi:.4g} km/s; DW chi2 {dh['dw_chi2']:.1f}; z: " + "  ".join(f"{k} {dh['z_nominal'][k]:+.1f}" for k in ZK))
        else:
            P(f"  [{f}] P3 upper root: none")
        RES["A1_diagnostics"][f"{f}|P3_high_root"] = dh
    P(f"\n  runtime {time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB")
    finish(0)

# =====================================================================================================================  MUTATE sign
if MUT == "sign":
    P("\n=== MUTATE sign: M1a reversed-surplus posits must be uncalibratable (FAILS); M1b sign-flipped predictions must FAIL")
    res = {}; allfail = True
    for f in FOOTS:
        S = STRUCT[f]["V0"]; v, se, oDW = OBSF[f]["V0"]
        for p in ("P1", "P2", "P3", "P4"):
            ra = grade(p, f, S, v, se, oDW, mode="rev"); rb = grade(p, f, S, v, se, oDW, mode="flip")
            res[f"{f}|{p}|M1a"] = dict(cls=ra["cls"], reason=ra.get("reason")); res[f"{f}|{p}|M1b"] = dict(cls=rb["cls"], decisive=rb.get("decisive"))
            allfail &= (ra["cls"] == "FAILS" and rb["cls"] == "FAILS")
            P(f"  [{f}] {p}: M1a {ra['cls']} ({ra.get('reason') or ra.get('decisive')});  M1b {rb['cls']} (decisive {rb.get('decisive')})")
    RES["mutate_sign"] = res; RES["bites"] = bool(allfail)
    P(f"  MUTATE sign {'BITES (all 16 FAIL)' if allfail else 'DOES NOT BITE'}  [{time.time() - T0:.0f} s]")
    finish(1 if allfail else 0)

# =====================================================================================================================  MUTATE inject
if MUT == "inject":
    P("\n=== MUTATE inject: 200 realizations per posit and footing from the posit's own nominal predictions; full grading")
    NREAL = 200; res = {}; allok = True
    for f in FOOTS:
        S = STRUCT[f]["V0"]; v, se, oDW = OBSF[f]["V0"]; Ct = S["Ct"]; Lc = np.linalg.cholesky(Ct)
        D = DWD[f]
        X9 =np.vstack([np.ones(83), D["lg"], D["hi"].astype(float)]).T; beta = np.linalg.lstsq(X9, D["E"], rcond=None)[0]; rr = D["E"] - X9 @ beta
        tau2 = max(0.0, float(np.var(rr, ddof=3)) - float(np.mean(D["sE"] ** 2))); sdi = np.sqrt(D["sE"] ** 2 + tau2)
        for p in POSITS:
            rng = np.random.default_rng(921)
            th0 = calibrate(p, f, S, SG[1], v["F0"]) if p != "P5" else None
            if p != "P5" and th0 is None:
                res[f"{f}|{p}"] = dict(fractions=None, ok=None, theta=None, note="not injectable: calibration impossible on the real data (A1)")
                P(f"  [{f}] {p}: not injectable (calibration impossible on the real data; AMENDMENT_A1)"); continue
            pcs, dwE0 = pred_cells(p, th0, f, S, SG[1], SD[1], LENS_NOM)
            mu = np.empty(len(S["E"]))
            for c, o in S["ops"].items():
                if c in pcs: mu[o["ix"]] = pcs[c]
                else: mu[o["ix"]] = S["E"][o["ix"]]
            # calibration tables (interpolation) per sigma_g corner
            tabs = {}
            if p != "P5":
                for sgi in (0, 1, 2):
                    thc = calibrate(p, f, S, SG[sgi], v["F0"]) or th0
                    tabs[sgi] = calib_table(p, f, S, SG[sgi], thc)
            cnt = {"FAILS": 0, "SURVIVES": 0, "UNDERDETERMINED": 0}
            for r_ in range(NREAL):
                cs = mu + Lc @ rng.standard_normal(len(mu)); dws = dwE0 + sdi * rng.standard_normal(83)
                cellsE = {c: cs[S["ops"][c]["ix"]] for c in ("DW", "LS", "LD", "SS", "SL", "CL")}
                ov, ose, oD = obs_facts(S, f, cellsE, dws)
                prec = None
                if p != "P5":
                    prec = {}
                    for sgi in (0, 1, 2):
                        mvv, lgg = tabs[sgi]
                        def itp(t):
                            return math.exp(np.interp(t, mvv, lgg)) if mvv[0] <= t <= mvv[-1] else None
                        prec[(sgi, "th")] = (itp(ov["F0"]), itp(ov["F0"] + ose["F0"]), itp(ov["F0"] - ose["F0"]))
                rec = grade(p, f, S, ov, ose, oD, prec=prec); cnt[rec["cls"]] += 1
            fr = {k: c_ / NREAL for k, c_ in cnt.items()}; ok_ = fr["FAILS"] <= 0.10 and fr["SURVIVES"] >= 0.40; allok &= ok_
            res[f"{f}|{p}"] = dict(fractions=fr, ok=ok_, theta=th0)
            P(f"  [{f}] {p}: FAILS {fr['FAILS']:.1%}  SURVIVES {fr['SURVIVES']:.1%}  UNDERDETERMINED {fr['UNDERDETERMINED']:.1%}  -> {'OK' if ok_ else 'NOT MET'}"
              f"  [{time.time() - T0:.0f} s]")
    RES["mutate_inject"] = res; RES["recovered"] = bool(allok)
    P(f"  MUTATE inject {'RECOVERED (all posits, both footings)' if allok else 'NOT MET'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
    finish(0 if allok else 1)
