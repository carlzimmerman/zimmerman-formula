#!/usr/bin/env python3
"""CFG959 -- the excess family as UNRELAXED native cold energy (H-UNR), one kinematic rule for all classes.
Criteria: FROZEN_CRITERIA.md (3b52ca39f, committed alone before this script and before any number of this lane).

H-UNR: the law is the relaxed end state of a system's cold energy; relaxation needs a coherent rotating baryonic flow.
Retained (unrelaxed) fraction u = f_P = 3 sigma^2/(v^2 + 3 sigma^2) (derived in the criteria; zero constants).
Primary reading R-C (mass-conserving):  g = g_N + G [min(M_ph(<r), (1-u) M_c) + u M_cNFW(<r)] / r^2   (u = 1: CFG949 B0)
Secondary reading R-A (additive, non-conserving bracket):  g = g_law + u G M_cNFW(<r) / r^2
Native supply M_c = 5.364 x catchment baryons (census f_ret, CFG804 fixed point), CFG930 R930 NFW (C 3000, r_ta, native EPS z_c).

Stages (one at a time; OMP_NUM_THREADS=1 nice -n 10; from this directory):
  CFG959_MODE=K       python3 cfg959.py   -> cfg959_K.out, cfg959_results_K.json
  CFG959_MODE=MUTATE  python3 cfg959.py   -> cfg959_MUTATE.out, cfg959_results_MUTATE.json   (M-DISC, M-ZERO, M-PLANT)
                      python3 cfg959.py   -> cfg959.out, cfg959_results.json                 (main; K re-checked first)
Read-only reuse: CFG949 (exec'd slice: CFG686/687/922/932 machinery + its copy of CFG930's R930 functions), CFG880 (exec'd input
slice), CFG919 (lens/cell functions copied verbatim), CFG4_common (SPARC loader, footings), committed JSON of CFG919/930/933/936/
940/949/695/880/687; McQuinn+22 Table 2 (on disk, parsed by byte positions, never executed). Every file write outside this lane's
directory is refused by a guard on builtins.open / io.open. Nothing downloaded.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, time, resource, contextlib, builtins, warnings
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad, cumulative_trapezoid

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG959_MODE", "MAIN").upper(); assert MODE in ("K", "MUTATE", "MAIN")
TAG = {"K": "_K", "MUTATE": "_MUTATE", "MAIN": ""}[MODE]
for _e in ("MUTATE", "CFG880_MUTATE", "CFG919_MUTATE", "CFG914_MUTATE", "CFG932_MUTATE", "CFG949_MODE", "CFG930_MODE"):
    os.environ.pop(_e, None)
RSS_LIMIT_GB = 0.95

# ------------------------------------------------------------------------------------------------ write guard (whole run)
_REAL_OPEN = builtins.open


def _guarded_open(file, mode="r", *a, **k):
    if isinstance(file, (str, bytes, os.PathLike)) and any(c in mode for c in "wax+"):
        p = os.path.abspath(os.fsdecode(file))
        if not (p.startswith(HERE + os.sep) or p == os.devnull):
            raise PermissionError(f"CFG959 refuses to write {p!r}")
    return _REAL_OPEN(file, mode, *a, **k)


builtins.open = _guarded_open; io.open = _guarded_open

OUT = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r * 1024 / 1e9


def jdef(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_,)): return bool(o)
    return str(o)


RES = dict(lane="CFG959", criteria="3b52ca39f", mode=MODE, checks={})


def finish(code):
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_gb"] = round(rss_gb(), 3); RES["exit"] = code
    P(f"\n  done [{time.time() - T0:.0f} s, peak RSS {rss_gb():.3f} GB], exit {code}.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    with _REAL_OPEN(os.path.join(HERE, f"cfg959_results{TAG}.json"), "w") as fh: json.dump(RES, fh, indent=1, default=jdef)
    with _REAL_OPEN(os.path.join(HERE, f"cfg959{TAG}.out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
    sys.exit(code)


def guard(label):
    g = rss_gb()
    if g > RSS_LIMIT_GB:
        P(f"RSS GUARD: {g:.3f} GB > {RSS_LIMIT_GB} GB at '{label}' -> abort"); finish(3)
    return g


def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)


def J(*p):
    with _REAL_OPEN(os.path.join(LANES, *p)) as fh: return json.load(fh)


FOOTS = ("canonical", "alt"); LN10 = math.log(10.0)
P(f"CFG959 [{MODE}]  H-UNR: excess family as unrelaxed native cold energy; criteria 3b52ca39f")
P("  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; raw data, framework-native inputs; not theory closed")

# ================================================================================================ CFG949 slice (clusters + R930)
SRC949 = os.path.join(LANES, "CFG949_clusters_untethered", "cfg949.py")
with _REAL_OPEN(SRC949) as _fh: TXT949 = _fh.read()
_a = "# ============================================================================ CFG686 / CFG687 / CFG922 machinery (exec, read-only)"
_b = "# ============================================================================ K stage"
SL949 = TXT949[TXT949.index(_a):TXT949.index(_b)]
LOG949 = []
NS949 = dict(os=os, sys=sys, io=io, json=json, math=math, time=time, contextlib=contextlib, resource=resource, np=np, brentq=brentq,
             quad=quad, cumulative_trapezoid=cumulative_trapezoid, HERE=os.path.dirname(SRC949), LANES=LANES, MODE="MAIN",
             T0=T0, RSS_LIMIT_GB=RSS_LIMIT_GB, CHECKS=[], __file__=SRC949, __name__="cfg949_ro",
             P=lambda *a: LOG949.append(" ".join(str(x) for x in a)), guard=lambda label: rss_gb(),
             check=lambda name, ok, detail: bool(ok))
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    exec(compile(SL949, SRC949, "exec"), NS949)
for _l in LOG949: P("    cfg949> " + _l)
N9 = NS949
C4 = N9["C4"]; A0X = dict(N9["A0"])                                           # FP0 footings (CFG4_common), equal to rounded ones < 1e-15
prof930, mta_fixed, FBN, m_ = N9["prof930"], N9["mta_fixed"], N9["FBN"], N9["m_"]
STE, GAS, MB, NE, NR = N9["STE"], N9["GAS"], N9["MB"], N9["NE"], N9["NR"]
dsig_newton, dsig_law, classify949, s_model, lam_band = N9["dsig_newton"], N9["dsig_law"], N9["classify"], N9["s_model"], N9["lam_band"]
build_cold, supply949, cold_profile, PROFILES = N9["build_cold"], N9["supply"], N9["cold_profile"], N9["PROFILES"]
ZC, MG, MSUN9 = N9["ZC"], N9["MG"], N9["MSUN"]
guard("cfg949 slice")


def build_cold_x(prof, smult=1.0, zrule="own"):
    """CFG949 build_cold for the R930 family at S-cen, with a supply multiplier (CFG930's x2 corner) and z_i rule."""
    name, fam, a, b = [p for p in PROFILES if p[0] == prof][0]; assert fam == "930"
    Mg3 = GAS[:, -1] / MSUN9; out = np.empty((NE, NR))
    for i in range(NE):
        zi = float(ZC[i]) if zrule == "own" else 0.0
        Mta, f = supply949("S-cen", float(Mg3[i]), float(MG[i]), 0.20); Mta *= smult
        c, rs, rb, zc = prof930(Mta, zi, a, b)
        out[i] = cold_profile(Mta, c, rs, rb)
    return out


# ================================================================================================ galaxy-scale native halo (R930, z_i = 0)
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
CORNERS = [(C, bnd, sm) for sm in (1.0, 2.0) for C in (3000.0, 1500.0, 6000.0) for bnd in ("rta", "rvir")]
PRIM = (3000.0, "rta", 1.0)
_HC = {}


def halo_gal(Mb, cor=PRIM):
    key = (round(math.log10(Mb), 12), cor)
    if key not in _HC:
        C, bnd, sm = cor; f, Mta0 = mta_fixed(Mb); Mta = Mta0 * sm
        c, rs, rb, zc = prof930(Mta, 0.0, C, bnd)
        _HC[key] = dict(Mta=Mta, Mc=(1 - FBN) * Mta, c=c, rs=rs, rb=rb, zc=zc, mc=float(m_(c)), fret=f)
    return _HC[key]


def McNFW(h, r_kpc):
    return h["Mc"] * np.asarray(m_(np.minimum(np.asarray(r_kpc, float), h["rb"]) / h["rs"]), float) / h["mc"]


def g_model(gN, glaw, r_m, Mc, Mnfw, u, reading="RC", cap=True):
    """SI accelerations; r_m in metres; masses in Msun.  RC: mass-conserving; RA: additive; LAW: the uncapped law."""
    if reading == "LAW": return glaw
    if reading == "RA": return glaw + u * G * Mnfw * MSUN / r_m ** 2
    Mph = (glaw - gN) * r_m ** 2 / G / MSUN
    rel = np.minimum(Mph, (1 - u) * Mc) if cap else Mph * (1 - u)
    return gN + G * (rel + u * Mnfw) * MSUN / r_m ** 2


def fP(v, s): return 3.0 * s * s / (v * v + 3.0 * s * s)


def u_of(f, form):
    if form == "PLIN": return f
    if form == "VEQ": return 1.0 if f > 0.5 else 0.0
    if form == "VOP": return 1.0 if f > 0.72 else 0.0
    if form == "ONE": return 1.0
    if form == "ZERO": return 0.0
    raise ValueError(form)


nu_e15 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_s300 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-300)))


def lab(z):
    a = abs(z); return "CONSISTENT" if a < 2 else ("TENSION" if a < 3 else "CONTRADICTED")


# ================================================================================================ (a) SPARC, CFG695's S2 recipe
GAL = C4.load_sparc()
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
_gi = np.concatenate([np.full(len(q["R"]), i) for i, q in enumerate(GAL)])
Rk = np.concatenate([q["R"] for q in GAL]); Rm = Rk * KPC
Vo = np.concatenate([q["Vobs"] for q in GAL]); eV = np.concatenate([q["eV"] for q in GAL])
Vg = np.concatenate([q["Vgas"] for q in GAL]); Vd = np.concatenate([q["Vdisk"] for q in GAL]); Vb = np.concatenate([q["Vbul"] for q in GAL])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WW = np.where(OK, (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)[:, None], 0.0)
L36 = np.array([(q["meta"] or {}).get("L36", 0.0) * 1e9 for q in GAL]); MHI = np.array([(q["meta"] or {}).get("MHI", 0.0) * 1e9 for q in GAL])
VFL = []
for q in GAL:
    vf = (q["meta"] or {}).get("Vflat", 0.0)
    VFL.append(vf if vf > 0 else float(np.max(q["Vobs"])))
VFL = np.array(VFL)


_HSP = {}


def sparc_halos(cor):
    """native halo table per SPARC galaxy and Upsilon of the grid (footing-independent): Mc, rs, rb, m(c)."""
    if cor not in _HSP:
        C, bnd, sm = cor; T = np.empty((4, len(GAL), len(UPS)))
        for j, U in enumerate(UPS):
            Mbt = U * L36 + 1.33 * MHI
            for i in range(len(GAL)):
                f_, Mta0 = mta_fixed(max(Mbt[i], 1e3)); Mta = Mta0 * sm; c, rs, rb, zc = prof930(Mta, 0.0, C, bnd)
                T[:, i, j] = ((1 - FBN) * Mta, rs, rb, float(m_(c)))
        _HSP[cor] = T
    return _HSP[cor]


def sparc_fit(form="PLIN", reading="RC", cor=PRIM, sig=10.0, cap=True, ups_fixed=None):
    """weighted rms of log g_obs - log g_model on the CFG4 statistic; Upsilon refit on CFG695's grid (or fixed)."""
    uu = np.array([u_of(fP(v, sig), form) for v in VFL]); best = (np.inf, None); ncap = 0
    js = range(len(UPS)) if ups_fixed is None else [int(np.argmin(np.abs(UPS - ups_fixed)))]
    T = None if reading == "LAW" else sparc_halos(cor)
    for j in js:
        U = UPS[j]; gb = np.where(OK[:, j], GB[:, j], 1.0); gl = gb * nu_s300(gb / A0F)
        if reading == "LAW":
            gm = gl
        else:
            Mc, rs, rb, mc = (T[k, :, j] for k in range(4))
            Mn = Mc[_gi] * np.asarray(m_(np.minimum(Rk, rb[_gi]) / rs[_gi]), float) / mc[_gi]
            gm = g_model(gb, gl, Rm, Mc[_gi], Mn, uu[_gi], reading, cap)
            if j == (js[0] if ups_fixed is not None else int(np.argmin(np.abs(UPS - 0.6)))):
                Mph = (gl - gb) * Rm ** 2 / G / MSUN; ncap = int(np.sum(OK[:, j] & (Mph > (1 - uu[_gi]) * Mc[_gi])))
        with np.errstate(all="ignore"):
            r_ = np.log10(np.where(OK[:, j], GO[:, j], 1.0)) - np.log10(np.where(OK[:, j], np.maximum(gm, 1e-300), 1.0))
        mse = float((WW[:, j] * r_ ** 2).sum() / WW[:, j].sum())
        if mse < best[0]: best = (mse, float(U))
    rms = math.sqrt(best[0]); U = best[1]
    return dict(rms=rms, U=U, passes=bool(rms <= 0.110 and 0.50 <= U <= 0.80), ncap_at_U060=ncap,
                u_median=float(np.median(uu)), u_max=float(np.max(uu)))


# ================================================================================================ (b) dSphs: CFG880 input slice
SRC880 = os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880.py")
with _REAL_OPEN(SRC880) as _fh: _t880 = _fh.read()
N880 = {"__file__": SRC880, "__name__": "cfg880_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_t880.split("# ---------------- hierarchical likelihood ----------------")[0], SRC880, "exec"), N880)
R880 = J("CFG880_clump_sigma_universality", "cfg880_results.json")
GRID = np.arange(-20.0, 10.0001, 0.5); FLOOR0 = 0.05 * LN10


def cells_persys(cls, lg, E, sE, fm):                       # cfg919.py verbatim
    k = np.digitize(lg, GRID) - 1; out = []
    for b in sorted(set(k)):
        g = np.where(k == b)[0]; n = len(g)
        if n < 3: continue
        se = max(np.std(E[g], ddof=1) / math.sqrt(n), math.sqrt(np.sum(sE[g] ** 2)) / n)
        out.append(dict(cls=cls, w=int(b), lg=float(np.mean(lg[g])), E=float(np.mean(E[g])), f=float(np.mean(fm[g])), n=int(n), se_stat=float(se)))
    return out, np.diag([c["se_stat"] ** 2 for c in out])


def class_gls(cells, Cstat, floor=FLOOR0):
    if not cells: return dict(E=float("nan"), se=float("nan"), n_cells=0)
    E = np.array([c["E"] for c in cells]); Ct = Cstat + floor ** 2 * np.eye(len(cells)); Ci = np.linalg.inv(Ct); one = np.ones(len(E))
    m = float(one @ Ci @ E / (one @ Ci @ one)); s = float((one @ Ci @ one) ** -0.5)
    return dict(E=m, se=s, dex=m / LN10, z=m / s, n_cells=len(cells))


A0X_R = {"canonical": 9.3603e-11, "alt": 1.1312e-10}             # CFG880/914/919's rounded footings (dwarf, lens, UDG, rotator estimators)
DW = {}
for f in FOOTS:
    a0 = A0X_R[f]; A = N880["arrays"](N880["SAMP"], a0); law = np.sqrt(A["sl2"]); r12m = A["r12"] * PC
    gN, Mbt, hi = [], [], []
    for nm, r12pc in zip(A["names"], A["r12"]):
        L = N880["LVD"][nm]; Lv = 10 ** (0.4 * (4.83 - N880["fnum"](L["M_V"]))); Ms = 2.0 * Lv; lHI = N880["fnum"](L.get("mass_HI"))
        Mg = N880["gas_in"](lHI, r12pc); gN.append(G * (Ms / 2 + Mg) * MSUN / (r12pc * PC) ** 2)
        Mbt.append(Ms + (1.33 * 10 ** lHI if lHI is not None else 0.0)); hi.append(Mg > 0)
    gN = np.array(gN); gl = 3 * A["sl2"] * 1e6 / r12m
    s = A["s"]; E = 2 * np.log(s / law); e = np.where(s > law, A["em"], A["ep"]); sE = 2 * e / s
    DW[f] = dict(names=list(A["names"]), E=E, sE=sE, gN=gN, gl=gl, r12m=r12m, r12k=A["r12"] / 1e3, lg=np.log10(gN), Mbt=np.array(Mbt),
                 hi=np.array(hi), law=law, s=s)


def dw_pred(f, form="PLIN", reading="RC", cor=PRIM, bracket=None, cap=True):
    d = DW[f]; n = len(d["E"]); Ep = np.empty(n)
    for i in range(n):
        fp = 1.0 if bracket is None else (fP(1.0, 1.0) if d["hi"][i] else fP(0.5, 1.0))
        u = u_of(fp, form); h = halo_gal(d["Mbt"][i], cor)
        gm = g_model(d["gN"][i], d["gl"][i], d["r12m"][i], h["Mc"], float(McNFW(h, d["r12k"][i])), u, reading, cap)
        Ep[i] = math.log(gm / d["gl"][i])
    return Ep


def dw_class(f, Ep, Eobs=None):
    d = DW[f]; Eo = d["E"] if Eobs is None else Eobs
    c, C = cells_persys("DW", d["lg"], Eo - Ep, d["sE"], np.ones(len(Eo))); return class_gls(c, C)


def scatter_profile(E, sE):
    sg = np.concatenate([[0.0], np.arange(0.005, 4.0001, 0.005)]); m2 = np.empty(len(sg)); cs = np.empty(len(sg))
    for k, s in enumerate(sg):
        v = sE ** 2 + s ** 2; w = 1 / v; c = float(np.sum(w * E) / np.sum(w)); cs[k] = c
        m2[k] = float(np.sum(np.log(v) + (E - c) ** 2 / v))
    i = int(np.argmin(m2)); d = m2 - m2[i]
    hi_ = next((sg[j - 1] + (3.84 - d[j - 1]) * (sg[j] - sg[j - 1]) / (d[j] - d[j - 1]) for j in range(i + 1, len(sg)) if d[j] > 3.84), float("inf"))
    lo_ = next((sg[j] + (3.84 - d[j]) * (sg[j + 1] - sg[j]) / (d[j + 1] - d[j]) for j in range(i - 1, -1, -1) if d[j] > 3.84), 0.0)
    return dict(s_hat=float(sg[i]), s95=[float(lo_), float(hi_)], m2lnL=float(m2[i]), c_hat=float(cs[i]))


def dw_scatter(f, Ep, Eobs=None):
    d = DW[f]; Eo = d["E"] if Eobs is None else Eobs
    H = scatter_profile(Eo - Ep, d["sE"]); C0 = scatter_profile(Eo, d["sE"])
    w = 1 / (d["sE"] ** 2 + C0["s_hat"] ** 2); X = np.vstack([np.ones(len(Ep)), Ep]).T; Wm = np.diag(w)
    cov = np.linalg.inv(X.T @ Wm @ X); beta = cov @ X.T @ Wm @ Eo
    return dict(HUNR=H, const=C0, dm2lnL_const_minus_HUNR=C0["m2lnL"] - H["m2lnL"], slope=float(beta[1]), slope_se=float(math.sqrt(cov[1, 1])),
                Epred_sd=float(np.std(Ep, ddof=1)), passes=bool(H["s95"][1] < C0["s_hat"]))


# ================================================================================================ (a2), (e) lenses: CFG919 functions, verbatim
B21 = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
G_pc, PCm = 4.52e-30, 3.086e16
LWIN = (10 ** -13.3, 10 ** -10.9)


def b21_load(esd, cov, binmin=None):
    d = np.loadtxt(os.path.join(B21, esd)); gb, esdt, bias = d[:, 0], d[:, 1], d[:, 4]
    go = 4 * G_pc * esdt / bias * PCm
    c = np.loadtxt(os.path.join(B21, cov)); n = len(gb); C = np.zeros((n, n))
    sel = c if binmin is None else c[(np.isclose(c[:, 0], binmin)) & (np.isclose(c[:, 1], binmin))]
    def idx(x):
        k = int(np.argmin(np.abs(gb / x - 1))); return k if abs(gb[k] / x - 1) < 1e-3 else None
    for row in sel:
        i, j = idx(row[2]), idx(row[3])
        if i is not None and j is not None: C[i, j] = row[4] / row[6]
    return gb, go, C * (4 * G_pc * PCm) ** 2


LF = {"disc": ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
      "sph": ("Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0)}
LD_ = {k: b21_load(*v) for k, v in LF.items()}
LM_RED, LM_BLUE, SHIFT_N2, DIMF = 10.81, 10.45, 0.123, 0.172        # CFG921 class masses, CFG667 shift, CFG926 R5 IMF step


def lens_set(key, f, shift):
    gb, go, C = LD_[key]; gbs = gb * 10 ** shift; gl = gbs * nu_e15(gbs / A0X_R[f]); m = (gbs >= LWIN[0]) & (gbs < LWIN[1])
    return gbs[m], go[m], C[np.ix_(m, m)], gl[m]


def cells_lens(cls, gb, go, C, gl, fval):                  # cfg919.py verbatim (gl = the reference model)
    lr = np.log10(gb); k = np.digitize(lr, GRID) - 1; n = len(go); Ws, info = [], []
    for b in sorted(set(k)):
        S = np.where(k == b)[0]; Ci = np.linalg.inv(C[np.ix_(S, S)]); a = gl[S] @ Ci @ gl[S]
        w = np.zeros(n); w[S] = (Ci @ gl[S]) / a; A = float(w @ go); sA = math.sqrt(float(w @ C @ w))
        if A <= 0 or sA / A > 1: continue
        ww = np.abs(w[S] * gl[S]); ww = ww / ww.sum(); Ws.append(w)
        info.append(dict(cls=cls, w=int(b), lg=float(np.sum(ww * lr[S])), A=A, n=int(len(S)), f=float(fval)))
    if not Ws: return [], np.zeros((0, 0))
    Wm = np.array(Ws); CA = Wm @ C @ Wm.T; Av = np.array([i["A"] for i in info]); CE = CA / np.outer(Av, Av)
    for j, i in enumerate(info): i["E"] = math.log(i["A"]); i["se_stat"] = math.sqrt(CE[j, j])
    return info, CE




def lens_class(f, cls, form="PLIN", reading="RC", cor=PRIM, imf=False, fval=None, plant=False, cap=True):
    key = "sph" if cls == "LS" else "disc"; shift = (SHIFT_N2 + (DIMF if imf else 0.0)) if cls == "LS" else 0.0
    gbs, go, C, gl = lens_set(key, f, shift)
    fv = (0.80 if cls == "LS" else 0.20) if fval is None else fval
    lm = (LM_RED + shift) if cls == "LS" else LM_BLUE; M = 10 ** lm
    if reading == "LAW":
        gm = gl
    else:
        h = halo_gal(M, cor); Rmet = np.sqrt(G * M * MSUN / gbs); Mn = McNFW(h, Rmet / KPC)
        gm = g_model(gbs, gl, Rmet, h["Mc"], Mn, u_of(fv, form), reading, cap)
    goo = gm.copy() if plant else go
    c, CE = cells_lens(cls, gbs, goo, C, gm, fv)
    out = class_gls(c, CE); out["Epred_mean_cells"] = float(np.mean(np.log(gm / gl))); out["logM"] = lm; out["u"] = u_of(fv, form)
    return out


# ================================================================================================ (c) Coma UDGs (CFG933 membership, sealed estimator)
R933 = J("CFG933_udg_sealed_test", "cfg933_results.json")
COMA = [m for m in R933["membership"] if m["pop"] == "Coma" and m["admitted"]]
G8, MS8, PC8 = N880["G"], N880["Msun"], N880["PC"]


def coma_eval(f, form="PLIN", reading="RC", cor=PRIM, plant_rng=None, cap=True):
    a0 = A0X_R[f]; Eo, Ep, sE = [], [], []
    for m in COMA:
        r12pc = (4.0 / 3.0) * m["Re"] * 1e3; Mbin = m["Ms"] / 2; gb = G8 * Mbin * MS8 / (r12pc * PC8) ** 2; gL = gb * float(nu_e15(gb / a0))
        sl = math.sqrt(r12pc * PC8 * gL / 3) / 1e3; eo = 2 * math.log(m["sig"] / sl)
        if reading == "LAW":
            gm = gL
        else:
            h = halo_gal(m["Ms"], cor); r_m = r12pc * PC8
            gm = g_model(gb, gL, r_m, h["Mc"], float(McNFW(h, r12pc / 1e3)), u_of(1.0, form), reading, cap)
        ep = math.log(gm / gL); e = m["em"] if m["sig"] > sl * math.exp(ep / 2) else m["ep"]; se_i = 2 * e / m["sig"]
        if plant_rng is not None: eo = ep + plant_rng.normal(0, se_i)
        Eo.append(eo); Ep.append(ep); sE.append(se_i)
    Eo, Ep, sE = np.array(Eo), np.array(Ep), np.array(sE); n = len(Eo); r = Eo - Ep
    t_me = float(math.sqrt(np.sum(sE ** 2)) / n); t_sd_o = float(np.std(Eo, ddof=1) / math.sqrt(n)); t_sd_r = float(np.std(r, ddof=1) / math.sqrt(n))
    se_r = max(t_me, t_sd_r)
    return dict(N=n, mean_Eobs=float(Eo.mean()), se_obs=max(t_me, t_sd_o), mean_Epred=float(Ep.mean()), mean_res=float(r.mean()), se_res=se_r,
                z=float(r.mean() / se_r), dex_res=float(r.mean() / LN10), per=[dict(name=m["name"], Eobs=float(a), Epred=float(b), sE=float(c))
                                                                          for m, a, b, c in zip(COMA, Eo, Ep, sE)])


# ================================================================================================ (f) TDGs and DF2/DF4 (CFG936 rows; Newton)
R936 = J("CFG936_below_law_systems", "cfg936_results.json")


def stat936(r, s):
    n = len(r); se_me = math.sqrt(float(np.sum(np.square(s)))) / n; se_sd = float(np.std(r, ddof=1)) / math.sqrt(n)
    return dict(n=n, rbar=float(np.mean(r)), se=max(se_me, se_sd), se_meas=se_me, se_scatter=se_sd)


def f_items(f):
    T = R936["routes"][f]["route_i"]["T"]["per_object"]; U = R936["routes"][f]["route_i"]["U"]["per_object"]
    rT = np.array([o["Delta_obs"] + math.log10(o["nu"]) for o in T]); sT = np.array([o["s"] for o in T])     # Newton: Delta_pred = -log10 nu
    rU = np.array([o["E_obs"] + math.log(o["nu"]) for o in U]); sU = np.array([o["sE"] for o in U])         # Newton: E_pred = -ln nu
    sTt, sUt = stat936(rT, sT), stat936(rU, sU)
    sTt["z"] = sTt["rbar"] / sTt["se"]; sUt["z"] = sUt["rbar"] / sUt["se"]; sTt["label"] = lab(sTt["z"]); sUt["label"] = lab(sUt["z"])
    return dict(TDG_dex=sTt, DF_ln=sUt)


def df_debris_diag(f, cor=PRIM):
    """diagnostic (no weight): DF2/DF4 if they had kept their native debris (u = 1, R-C), CFG933 estimator."""
    out = []
    for m in [x for x in R933["membership"] if x["name"] in ("NGC1052-DF2", "NGC1052-DF4")]:
        a0 = A0X_R[f]; r12pc = (4.0 / 3.0) * m["Re"] * 1e3; gb = G8 * (m["Ms"] / 2) * MS8 / (r12pc * PC8) ** 2; gL = gb * float(nu_e15(gb / a0))
        sl = math.sqrt(r12pc * PC8 * gL / 3) / 1e3; eo = 2 * math.log(m["sig"] / sl); h = halo_gal(m["Ms"], cor)
        gm = g_model(gb, gL, r12pc * PC8, h["Mc"], float(McNFW(h, r12pc / 1e3)), 1.0, "RC"); ep = math.log(gm / gL)
        e = m["em"] if m["sig"] > sl * math.exp(ep / 2) else m["ep"]; se = 2 * e / m["sig"]
        out.append(dict(name=m["name"], Eobs=eo, Epred_u1=ep, Epred_newton=math.log(gb / gL), z_u1=(eo - ep) / se))
    return out


# ================================================================================================ (g) faint rotators (CFG940 table + Table 2 V_rot)
R940 = J("CFG940_faint_rotators_mcquinn22", "cfg940_results.json"); TAB940 = R940["table"]
T2 = os.path.join(REPO, "real_research", "data", "faint_rotators_mcquinn2022", "apjac9285t2_mrt.txt")
VROT, VCOR2 = {}, {}
with _REAL_OPEN(T2) as fh:
    for line in fh:
        nm = line[0:9].strip()
        if not nm or len(line) < 56 or line[10:11] not in ("R", "P"): continue
        try: VROT[nm] = float(line[47:49]); VCOR2[nm] = float(line[52:54])
        except ValueError: continue
FLOOR940 = 0.05


def se_of(E, s):                                             # cfg940.py verbatim
    n = len(E); sd = float(np.std(E, ddof=1)) / math.sqrt(n) if n > 1 else 0.0
    return max(sd, math.sqrt(float(np.sum(np.square(s)))) / n)


def rot_eval(f, est="B", form="PLIN", reading="RC", cor=PRIM, sig=10.0, plant_rng=None, cap=True):
    a0 = A0X_R[f]; Eo, Ep, sE, lg = [], [], [], []
    for t in TAB940:
        lgb = t["lgA"] if est == "A" else t["lgB"]; gb = 10 ** lgb; gl = gb * float(nu_e15(gb / a0)); R = t["R"]; r_m = R * KPC
        if reading == "LAW":
            gm = gl
        else:
            h = halo_gal(10 ** t["lMb"], cor); u = u_of(fP(VROT[t["name"]], sig), form)
            gm = g_model(gb, gl, r_m, h["Mc"], float(McNFW(h, R)), u, reading, cap)
        ep = math.log10(gm / gl); eo = t["E_A" if est == "A" else "E_B"][f]; se = t["sE_A" if est == "A" else "sE_B"]
        if plant_rng is not None: eo = ep + plant_rng.normal(0, se)
        Eo.append(eo); Ep.append(ep); sE.append(se); lg.append(lgb)
    Eo, Ep, sE, lg = map(np.array, (Eo, Ep, sE, lg)); r = Eo - Ep
    se = math.sqrt(se_of(r, sE) ** 2 + FLOOR940 ** 2)
    return dict(N=len(r), mean_Eobs=float(Eo.mean()), se_obs=math.sqrt(se_of(Eo, sE) ** 2 + FLOOR940 ** 2), mean_Epred=float(Ep.mean()),
                mean_res=float(r.mean()), se_res=se, z=float(r.mean() / se), label=lab(r.mean() / se), Eo=Eo, Ep=Ep, sE=sE, lg=lg)


def matched_cell(f, Ep_dw, rot):
    """(g2, reported): dSph - rotator difference in [1e-12, 10^-11.5), observed vs H-UNR predicted (dex)."""
    d = DW[f]; md = (d["lg"] >= -12.0) & (d["lg"] < -11.5); mr = (rot["lg"] >= -12.0) & (rot["lg"] < -11.5)
    if md.sum() < 3 or mr.sum() < 3: return dict(n_dsph=int(md.sum()), n_rot=int(mr.sum()))
    Edo, Edp, sEd = d["E"][md] / LN10, Ep_dw[md] / LN10, d["sE"][md] / LN10
    Do = float(Edo.mean() - rot["Eo"][mr].mean()); Dp = float(Edp.mean() - rot["Ep"][mr].mean())
    sD = math.sqrt(se_of(Edo, sEd) ** 2 + se_of(rot["Eo"][mr], rot["sE"][mr]) ** 2 + 2 * FLOOR940 ** 2)
    return dict(n_dsph=int(md.sum()), n_rot=int(mr.sum()), D_obs=Do, D_pred=Dp, sD=sD, z=(Do - Dp) / sD)


# ================================================================================================ (d) clusters
R687 = J("CFG687_erass1_shear_stack", "cfg687_results.json"); R949 = J("CFG949_clusters_untethered", "cfg949_results.json")
_PB = None; _PLAW = {}; _PC = {}


def Pb():
    global _PB
    if _PB is None: _PB = dsig_newton(MB)
    return _PB


def Plaw(f):
    if f not in _PLAW: _PLAW[f] = dsig_law(MB, A0X[f], C4.nu_mono)
    return _PLAW[f]


def Pcold(prof="C3000|rta", smult=1.0, zrule="own"):
    key = (prof, smult, zrule)
    if key not in _PC:                                       # (N x 8) DeltaSigma only; the (N x NR) cold arrays are transient
        _PC[key] = dsig_newton(build_cold_x(prof, smult, zrule))
    return _PC[key]


def prof_name(cor): return f"C{int(cor[0])}|{cor[1]}"


E7 = N9["E7"]; EN7 = np.where(np.isfinite(E7) & (E7 < 1e8), E7, 0.0)


def cluster_eval(f, form="PLIN", reading="RC", cor=PRIM, zrule="own", plant=False):
    u = u_of(1.0, form); Pc = Pcold(prof_name(cor), cor[2], zrule)
    if reading == "LAW": Pm = Plaw(f)
    elif reading == "RA": Pm = Plaw(f) + u * Pc
    else:
        assert u == 1.0                                      # f_P = 1 for clusters in every form: R-C at u = 1 is B0
        Pm = Pb() + Pc
    Dm = (Pm + np.random.default_rng(959).normal(0, 1, Pm.shape) * EN7) if plant else None     # plant: model + KiDS noise (CFG949 MI recipe)
    bd = STE.band(Pm, D=Dm); s = s_model(Pm); cl = classify949(bd, s)
    return dict(A=bd, s=s, cls=cl, label=cl["label"])


# ================================================================================================ K stage
def run_K():
    K = {}; ok = []
    # K1 CFG919 class means DW, LD, LS (rebuilt cells, law reference)
    R919 = J("CFG919_pressure_support_selector", "cfg919_results.json"); d1 = []
    for f in FOOTS:
        cs = R919["byfoot"][f]["V0"]["class_summary"]
        dw = dw_class(f, np.zeros(len(DW[f]["E"])))
        ls = lens_class(f, "LS", reading="LAW"); ld = lens_class(f, "LD", reading="LAW")
        for mine, key in ((dw, "DW"), (ls, "LS"), (ld, "LD")):
            d1 += [abs(mine["E"] - cs[key]["E"]), abs(mine["se"] - cs[key]["se"])]
            K.setdefault("K1_diffs", {})[f"{f}|{key}"] = (mine["E"] - cs[key]["E"], mine["se"] - cs[key]["se"])
        K[f"K1|{f}"] = dict(DW=dw, LS=ls, LD=ld)
    ok.append(check("K1 CFG919 class means DW, LS, LD (E, se; both footings) from this lane's rebuilt cells", max(d1) <= 1e-9,
                    f"max |diff| {max(d1):.1e}; canonical DW {K['K1|canonical']['DW']['E']:+.4f}+-{K['K1|canonical']['DW']['se']:.4f}, "
                    f"LS {K['K1|canonical']['LS']['E']:+.4f}, LD {K['K1|canonical']['LD']['E']:+.4f}; diffs " + ", ".join(f"{k} {v[0]:+.1e}/{v[1]:+.1e}" for k, v in K["K1_diffs"].items())))
    # K2 CFG687 A through CFG949 machinery
    d2 = []
    for f in FOOTS:
        bd = STE.band(Plaw(f)); st = R687["A"][f"{f}|b0.67|rc0.15|f0.20"]
        for b in ("MID", "OUTER"): d2 += [abs(bd[b][0] / st[b][0] - 1), abs(bd[b][1] / st[b][1] - 1)]
        K[f"K2|{f}"] = bd
    ok.append(check("K2 CFG687 A_MID, A_OUTER (value + jackknife, both footings) through CFG949's machinery", max(d2) <= 1e-6,
                    f"max rel {max(d2):.1e}; canonical MID {K['K2|canonical']['MID'][0]:.4f}+-{K['K2|canonical']['MID'][1]:.4f}, "
                    f"OUTER {K['K2|canonical']['OUTER'][0]:.4f}; alt MID {K['K2|alt']['MID'][0]:.4f}, OUTER {K['K2|alt']['OUTER'][0]:.4f}"))
    # K3 CFG949 B0 primary (and build_cold_x == build_cold)
    cold_ref, _m = build_cold("C3000|rta", "S-cen", GAS, 0.20); cold_x = build_cold_x("C3000|rta", 1.0, "own")
    dcx = float(np.max(np.abs(cold_x - cold_ref))); del cold_ref
    c3 = cluster_eval("canonical"); st = R949["main"]["B0_primary"]
    d3 = [abs(c3["A"][b][k] / st["A"][b][k] - 1) for b in ("MID", "OUTER") for k in (0, 1)] + [abs(c3["s"] / st["s"] - 1)]
    K["K3"] = dict(A=c3["A"], s=c3["s"], label=c3["label"], build_cold_x_maxabs=dcx)
    ok.append(check("K3 CFG949 B0 primary corner (A_MID, A_OUTER, s; stored JSON) = H-UNR R-C at u = 1; build_cold_x == build_cold", max(d3) <= 1e-9 and dcx == 0.0,
                    f"max rel {max(d3):.1e}; MID {c3['A']['MID'][0]:.4f}+-{c3['A']['MID'][1]:.4f} OUTER {c3['A']['OUTER'][0]:.4f}+-{c3['A']['OUTER'][1]:.4f} "
                    f"s {c3['s']:.4f} ({c3['label']}); cold arrays max |diff| {dcx:.1e}"))
    # K4 CFG930 SPARC halo facts (its 147-galaxy sample and conventions)
    R930 = J("CFG930_energy_limited_settling", "cfg930_results.json")["halo_facts_canonical"]["S"]; HF = dict(zc=[], c=[], rs=[], rb=[], mm=[])
    for q in GAL:
        mt = q["meta"]
        if mt is None or mt["Q"] > 2 or mt["Inc"] < 30: continue
        R, V, e_, vg, vd, vb = q["R"], q["Vobs"], q["eV"], q["Vgas"], q["Vdisk"], q["Vbul"]
        with np.errstate(all="ignore"):
            keep = (V > 0) & (R > 0) & (e_ / np.where(V > 0, V, 1) < 0.10)
            gb_ = (vg * np.abs(vg) + 0.5 * vd * np.abs(vd) + 0.7 * vb * np.abs(vb)) * 1e6 / (R * KPC)
        keep &= gb_ > 0
        if keep.sum() == 0: continue
        Mb = 0.5 * mt["L36"] * 1e9 + 1.33 * mt["MHI"] * 1e9; h = halo_gal(Mb)
        HF["zc"].append(h["zc"]); HF["c"].append(h["c"]); HF["rs"].append(h["rs"]); HF["rb"].append(h["rb"]); HF["mm"].append(h["Mta"] / Mb)
    mine = dict(zc_median=np.median(HF["zc"]), c_median=np.median(HF["c"]), rs_kpc_median=np.median(HF["rs"]), rb_kpc_median=np.median(HF["rb"]),
                Mta_over_Mb_median=np.median(HF["mm"]))
    d4 = [abs(mine[k] / R930[k] - 1) for k in R930]
    K["K4"] = dict(N=len(HF["zc"]), mine={k: float(v) for k, v in mine.items()}, stored=R930)
    ok.append(check("K4 CFG930 SPARC native halo facts (147 galaxies; median z_c, c, r_s, r_b, M_ta/M_b) through this lane's galaxy halo code",
                    max(d4) <= 1e-9 and len(HF["zc"]) == 147, f"N {len(HF['zc'])}; max rel {max(d4):.1e}; z_c {mine['zc_median']:.4f} c {mine['c_median']:.3f} "
                    f"r_s {mine['rs_kpc_median']:.3f} kpc r_b {mine['rb_kpc_median']:.2f} kpc M_ta/M_b {mine['Mta_over_Mb_median']:.2f}"))
    # K5 CFG695 S2
    R695 = J("CFG695_saturating_vacuum", "cfg695_results.json")["numbers"]["S2"]; d5 = []; K["K5"] = {}
    for f in FOOTS:
        globals()["A0F"] = A0X[f]; s2 = sparc_fit(reading="LAW"); K["K5"][f] = s2
        d5 += [abs(s2["rms"] - R695[f]["rms"]), abs(s2["U"] - R695[f]["U"])]
    ok.append(check("K5 CFG695 S2 rms and Upsilon (law, nu_simple, both footings) through this lane's SPARC engine", max(d5) <= 1e-6,
                    f"max |diff| {max(d5):.1e}; canonical {K['K5']['canonical']['rms']:.5f}@{K['K5']['canonical']['U']:.2f}, alt {K['K5']['alt']['rms']:.5f}@{K['K5']['alt']['U']:.2f}"))
    # K6 CFG933 Coma
    d6 = []; K["K6"] = {}
    for f in FOOTS:
        c = coma_eval(f, reading="LAW"); st = R933["byfoot"][f]["primary"]["samples"]["coma"]
        d6 += [abs(c["mean_Eobs"] - st["mean_Eobs"]), abs(c["se_obs"] - st["se_obs"]), abs(c["N"] - st["N"])]; K["K6"][f] = dict(N=c["N"], mean=c["mean_Eobs"], se=c["se_obs"])
    ok.append(check("K6 CFG933 Coma UDGs mean E_obs and se_obs (9 admitted; both footings)", max(d6) <= 1e-9,
                    f"max |diff| {max(d6):.1e}; canonical {K['K6']['canonical']['mean']:+.5f}+-{K['K6']['canonical']['se']:.5f} ln, alt {K['K6']['alt']['mean']:+.5f}"))
    # K7 CFG936 route (i) statistics from its rows; Newton-exact DF numbers == its 'S4 strict f=0' corner
    d7 = []; K["K7"] = {}
    for f in FOOTS:
        for key in ("T", "U"):
            ro = R936["routes"][f]["route_i"][key]; st = ro["stats"]
            mine = stat936(np.array([o["r"] for o in ro["per_object"]]), np.array([o["s"] for o in ro["per_object"]]))
            d7 += [abs(mine["rbar"] - st["rbar"]), abs(mine["se"] - st["se"])]
        fi = f_items(f); s4 = R936["routes"][f]["route_i"]["U"]["corners"]["S4 strict f=0"]
        d7 += [abs(fi["DF_ln"]["rbar"] - s4["rbar"]), abs(fi["DF_ln"]["se"] - s4["se"]), abs(fi["TDG_dex"]["rbar"] - R936["routes"][f]["route_i"]["T"]["stats"]["rbar"])]
        K["K7"][f] = fi
    ok.append(check("K7 CFG936 route (i) T/U statistics from its rows; Newton-exact DF2/DF4 == its 'S4 strict f=0' corner; TDG Newton == route (i)", max(d7) <= 1e-9,
                    f"max |diff| {max(d7):.1e}; canonical TDG {K['K7']['canonical']['TDG_dex']['rbar']:+.4f}+-{K['K7']['canonical']['TDG_dex']['se']:.4f} dex, "
                    f"DF {K['K7']['canonical']['DF_ln']['rbar']:+.4f}+-{K['K7']['canonical']['DF_ln']['se']:.4f} ln"))
    # K8 CFG940 WS means; Table 2 parse
    d8 = []; K["K8"] = {}
    for f in FOOTS:
        for est in ("A", "B"):
            r = rot_eval(f, est, reading="LAW"); st = R940["main"][f"WS|{est}|{f}|V0"]
            d8 += [abs(r["mean_Eobs"] - st["mean"]), abs(r["se_obs"] - st["se"])]; K["K8"][f"{est}|{f}"] = (r["mean_Eobs"], r["se_obs"])
    vc_ok = all(abs(VCOR2[t["name"]] - t["Vcor"]) < 1e-9 for t in TAB940) and len(VROT) == 25
    for f in FOOTS:                                          # this lane's g_law reproduces CFG940's stored E (A and B) from its stored logs
        for t in TAB940:
            for est, lk in (("A", "lgA"), ("B", "lgB")):
                gb = 10 ** t[lk]; d8.append(abs(t["lgobs"] - math.log10(gb * float(nu_e15(gb / A0X_R[f]))) - t[f"E_{est}"][f]))
    ok.append(check("K8 CFG940 WS means and se (A, B; both footings) from its stored table; its per-galaxy E from its stored logs with this lane's law; "
                    "Table 2 V_rot/V_cor parse (25; V_cor == CFG940)", max(d8) <= 1e-9 and vc_ok,
                    f"max |diff| {max(d8):.1e}; canonical A {K['K8']['A|canonical'][0]:+.4f}+-{K['K8']['A|canonical'][1]:.4f}, B {K['K8']['B|canonical'][0]:+.4f}+-{K['K8']['B|canonical'][1]:.4f} dex; "
                    f"V_rot {min(VROT.values()):.0f}-{max(VROT.values()):.0f} km/s"))
    # K9 CFG880 sample and its committed sigma_law
    d9 = []
    for f in FOOTS:
        rows = {r["name"]: r for r in R880[f]["primary"]["rows"]}
        d9 += [abs(DW[f]["law"][i] / rows[nm]["law"] - 1) for i, nm in enumerate(DW[f]["names"])]
    ok.append(check("K9 CFG880 sample N = 83 and its committed per-dwarf sigma_law (both footings)", len(DW["canonical"]["names"]) == 83 and max(d9) <= 1e-9,
                    f"N {len(DW['canonical']['names'])}; max rel {max(d9):.1e}"))
    guard("K stage")
    return all(ok), K


# ================================================================================================ evaluation of every item at one setting
def evaluate(form="PLIN", reading="RC", cor=PRIM, brackets=None, zrule="own", do_clusters=True, verbose=True):
    brackets = brackets or {}; R = {}
    for f in FOOTS:
        globals()["A0F"] = A0X[f]; it = {}
        it["a"] = sparc_fit(form, reading, cor, sig=brackets.get("sig", 10.0))
        it["a"]["drms"] = it["a"]["rms"] - {"canonical": 0.10090811294375761, "alt": 0.09943409571436324}[f]
        lf = brackets.get("lens_f")
        it["a2"] = lens_class(f, "LD", form, reading, cor, fval=(lf[0] if lf else None)); it["a2"]["label"] = lab(it["a2"]["z"])
        Ep = dw_pred(f, form, reading, cor, bracket=brackets.get("dw"))
        it["b"] = dw_class(f, Ep); it["b"]["label"] = lab(it["b"]["z"]); it["b"]["Epred_mean"] = float(np.mean(Ep)); it["b"]["Epred_median"] = float(np.median(Ep))
        it["b2"] = dw_scatter(f, Ep)
        it["c"] = coma_eval(f, form, reading, cor); it["c"]["label"] = lab(it["c"]["z"])
        if do_clusters:
            it["d"] = cluster_eval(f, form, reading, cor, zrule)
        e0 = lens_class(f, "LS", form, reading, cor, fval=(lf[1] if lf else None)); e1 = lens_class(f, "LS", form, reading, cor, imf=True, fval=(lf[1] if lf else None))
        e0["label"], e1["label"] = lab(e0["z"]), lab(e1["z"])
        it["e"] = dict(obs=e0, imf=e1, label=(e0["label"] if e0["label"] == e1["label"] else "IMF-DEPENDENT"))
        it["f"] = f_items(f); it["f"]["label"] = "CONSISTENT" if (it["f"]["TDG_dex"]["label"] == "CONSISTENT" and it["f"]["DF_ln"]["label"] == "CONSISTENT") else "NOT CONSISTENT"
        rB = rot_eval(f, "B", form, reading, cor, sig=brackets.get("sig", 10.0)); rA = rot_eval(f, "A", form, reading, cor, sig=brackets.get("sig", 10.0))
        it["g"] = dict(B={k: v for k, v in rB.items() if k not in ("Eo", "Ep", "sE", "lg")}, A={k: v for k, v in rA.items() if k not in ("Eo", "Ep", "sE", "lg")},
                       label=rB["label"], g2=matched_cell(f, Ep, rB))
        it["overall"] = overall(it, do_clusters)
        R[f] = it
        if verbose: P(fmt_items(f, it, do_clusters))
        guard(f"evaluate {form} {reading} {cor} {f}")
    return R


def overall(it, do_clusters=True):
    exc = dict(b=it["b"]["label"] == "CONSISTENT", c=it["c"]["label"] == "CONSISTENT",
               d=(it["d"]["label"] == "EXPLAINS") if do_clusters else False, e=it["e"]["label"] == "CONSISTENT")
    anchor = it["a"]["passes"] and it["a2"]["label"] != "CONTRADICTED" and it["g"]["label"] != "CONTRADICTED"
    explains = (it["a"]["passes"] and it["a2"]["label"] == "CONSISTENT" and exc["b"] and it["b2"]["passes"] and exc["c"] and exc["d"]
                and (exc["e"] or it["e"]["label"] == "IMF-DEPENDENT") and it["f"]["label"] == "CONSISTENT" and it["g"]["label"] == "CONSISTENT")
    if explains: cl = "EXPLAINS"
    elif (not anchor) or (not any(exc.values())) or it["f"]["label"] != "CONSISTENT": cl = "FAILS"
    else: cl = "PARTIAL"
    why = []
    if not it["a"]["passes"]: why.append("(a) SPARC fails")
    if it["a2"]["label"] == "CONTRADICTED": why.append("(a2) n<2 lenses CONTRADICTED")
    if it["g"]["label"] == "CONTRADICTED": why.append("(g) rotators CONTRADICTED")
    if not any(exc.values()): why.append("no excess class explained")
    return dict(cls=cl, explained=[k for k, v in exc.items() if v], not_explained=[k for k, v in exc.items() if not v], anchor_ok=anchor, why=why)


def fmt_items(f, it, do_clusters=True):
    a, a2, b, b2, c, e, g = it["a"], it["a2"], it["b"], it["b2"], it["c"], it["e"], it["g"]
    s = [f"  [{f}]",
         f"    (a)  SPARC rms {a['rms']:.4f} @ U {a['U']:.2f} (d {a['drms']:+.4f}) -> {'PASS' if a['passes'] else 'FAIL'}; u median {a['u_median']:.3f} max {a['u_max']:.3f}",
         f"    (a2) n<2 lenses resid {a2['E']:+.3f}+-{a2['se']:.3f} ln (z {a2['z']:+.1f}) {a2['label']}; u {a2['u']:.2f}, <E_pred> {a2['Epred_mean_cells']:+.3f}",
         f"    (b)  dSphs resid {b['E']:+.3f}+-{b['se']:.3f} ln ({b['dex']:+.3f} dex, z {b['z']:+.1f}) {b['label']}; E_pred mean {b['Epred_mean']:+.3f} median {b['Epred_median']:+.3f} ln",
         f"    (b2) scatter s_HUNR {b2['HUNR']['s_hat']:.3f} [95% {b2['HUNR']['s95'][0]:.3f}-{b2['HUNR']['s95'][1]:.3f}] vs s_const {b2['const']['s_hat']:.3f}; "
         f"d(-2lnL) const-HUNR {b2['dm2lnL_const_minus_HUNR']:+.2f}; slope {b2['slope']:+.3f}+-{b2['slope_se']:.3f}; sd(E_pred) {b2['Epred_sd']:.3f} -> {'PASS' if b2['passes'] else 'FAIL'}",
         f"    (c)  Coma UDGs E_obs {c['mean_Eobs']:+.3f}, E_pred {c['mean_Epred']:+.3f}, resid {c['mean_res']:+.3f}+-{c['se_res']:.3f} ln (z {c['z']:+.2f}) {c['label']}"]
    if do_clusters:
        d = it["d"]; s.append(f"    (d)  clusters MID {d['A']['MID'][0]:.3f}+-{d['A']['MID'][1]:.3f} (Z {d['cls']['Z_MID']:+.2f}) OUTER {d['A']['OUTER'][0]:.3f}+-{d['A']['OUTER'][1]:.3f} "
                              f"(Z {d['cls']['Z_OUT']:+.2f}) s {d['s']:.3f} ({d['cls']['dS_over_err']:+.2f} s_err) -> {d['label']}")
    s.append(f"    (e)  red lenses resid {e['obs']['E']:+.3f}+-{e['obs']['se']:.3f} ln (z {e['obs']['z']:+.1f}) {e['obs']['label']}; IMF {e['imf']['E']:+.3f}+-{e['imf']['se']:.3f} "
             f"(z {e['imf']['z']:+.1f}) {e['imf']['label']} -> {e['label']}; <E_pred> {e['obs']['Epred_mean_cells']:+.3f}")
    s.append(f"    (f)  TDG {it['f']['TDG_dex']['rbar']:+.3f}+-{it['f']['TDG_dex']['se']:.3f} dex, DF2/DF4 {it['f']['DF_ln']['rbar']:+.3f}+-{it['f']['DF_ln']['se']:.3f} ln -> {it['f']['label']} (inherited)")
    g2 = g["g2"]; g2s = (f"g2 matched cell D_obs {g2['D_obs']:+.3f} D_pred {g2['D_pred']:+.3f} +-{g2['sD']:.3f} (z {g2['z']:+.1f}; N {g2['n_dsph']}/{g2['n_rot']})"
                         if "D_obs" in g2 else f"g2 N {g2['n_dsph']}/{g2['n_rot']}")
    s.append(f"    (g)  rotators B resid {g['B']['mean_res']:+.3f}+-{g['B']['se_res']:.3f} dex (z {g['B']['z']:+.1f}) {g['label']}; A {g['A']['mean_res']:+.3f}+-{g['A']['se_res']:.3f}; "
             f"E_pred B {g['B']['mean_Epred']:+.3f}; {g2s}")
    o = it["overall"]; s.append(f"    OVERALL {o['cls']}  explained {o['explained']} not {o['not_explained']} {('; ' + '; '.join(o['why'])) if o['why'] else ''}")
    return "\n".join(s)


# ================================================================================================ stages
P("\n=== K-stage")
K_OK, KRES = run_K(); RES["K"] = KRES; RES["K_all_pass"] = K_OK
P(f"  K-stage {'ALL PASS' if K_OK else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_gb():.3f} GB]")
if not K_OK:
    P("  A K-test failed: per the criteria (section 7) the lane stops; no class is reported."); RES["class"] = None; finish(2)
if MODE == "K":
    finish(0)

if MODE == "MUTATE":
    M = {}
    P("\n=== M-DISC: u = 1 for every system (discs, n<2 lenses, rotators included); must break SPARC (a)")
    md = {}
    for f in FOOTS:
        globals()["A0F"] = A0X[f]; md[f] = sparc_fit("ONE", "RC")
        ld1 = lens_class(f, "LD", "ONE", "RC"); rt1 = rot_eval(f, "B", "ONE", "RC")
        md[f]["info_LD_u1"] = dict(E=ld1["E"], se=ld1["se"], z=ld1["z"]); md[f]["info_rot_B_u1"] = dict(res=rt1["mean_res"], se=rt1["se_res"], z=rt1["z"])
        P(f"  [{f}] SPARC rms {md[f]['rms']:.4f} @ U {md[f]['U']:.2f} -> {'PASS' if md[f]['passes'] else 'FAIL'};  (info) n<2 lenses at u = 1 "
          f"{ld1['E']:+.3f}+-{ld1['se']:.3f} ln (z {ld1['z']:+.1f}); rotators B at u = 1 {rt1['mean_res']:+.3f}+-{rt1['se_res']:.3f} dex (z {rt1['z']:+.1f})")
    M["M-DISC"] = dict(sparc=md, bites=all(not md[f]["passes"] for f in FOOTS))
    P(f"  M-DISC {'BITES' if M['M-DISC']['bites'] else 'DOES NOT BITE'}")
    P("\n=== M-ZERO: u = 0 everywhere, uncapped law (no retained debris); the record's offsets must come back exactly")
    mz = {}; dz = []
    R919 = J("CFG919_pressure_support_selector", "cfg919_results.json")
    for f in FOOTS:
        globals()["A0F"] = A0X[f]; cs = R919["byfoot"][f]["V0"]["class_summary"]
        Ep = dw_pred(f, "ZERO", "LAW"); b = dw_class(f, Ep); c = coma_eval(f, "ZERO", "LAW"); e = lens_class(f, "LS", "ZERO", "LAW")
        d = cluster_eval(f, "ZERO", "LAW"); a = sparc_fit("ZERO", "LAW")
        st933 = R933["byfoot"][f]["primary"]["samples"]["coma"]; st687 = R687["A"][f"{f}|b0.67|rc0.15|f0.20"]
        R695 = J("CFG695_saturating_vacuum", "cfg695_results.json")["numbers"]["S2"][f]
        dz += [abs(b["E"] - cs["DW"]["E"]), abs(c["mean_res"] - st933["mean_Eobs"]), abs(e["E"] - cs["LS"]["E"]),
               abs(d["A"]["MID"][0] / st687["MID"][0] - 1), abs(d["A"]["OUTER"][0] / st687["OUTER"][0] - 1), abs(a["rms"] - R695["rms"])]
        bc = dw_class(f, dw_pred(f, "ZERO", "RC")); ac = sparc_fit("ZERO", "RC")             # info: R-C at u = 0 keeps the supply cap
        mz[f] = dict(dSph=b, coma=dict(mean_res=c["mean_res"], se=c["se_res"]), red_lens=e, clusters=d["A"], sparc=a,
                     info_RC_u0_capped=dict(dSph_E=bc["E"], dSph_minus_law=bc["E"] - b["E"], sparc_rms=ac["rms"], sparc_U=ac["U"], sparc_ncap=ac["ncap_at_U060"]))
        P(f"  [{f}] (info) R-C at u = 0 with the supply cap: dSph {bc['E']:+.4f} (cap effect {bc['E'] - b['E']:+.1e}); SPARC {ac['rms']:.5f}@{ac['U']:.2f}, capped points {ac['ncap_at_U060']}")
        P(f"  [{f}] dSph resid {b['E']:+.4f}+-{b['se']:.4f} ln (z {b['z']:+.1f}); Coma {c['mean_res']:+.4f}; red lenses {e['E']:+.4f}; "
          f"clusters MID {d['A']['MID'][0]:.4f} OUTER {d['A']['OUTER'][0]:.4f}; SPARC {a['rms']:.5f}@{a['U']:.2f}")
    M["M-ZERO"] = dict(per=mz, maxdiff=max(dz), bites=bool(max(dz) <= 1e-6))
    P(f"  M-ZERO max diff vs record {max(dz):.1e} -> {'BITES (excesses return as deficits)' if M['M-ZERO']['bites'] else 'DOES NOT BITE'}")
    P("\n=== M-PLANT: observed := H-UNR primary prediction (+ noise, seed 959); planted items must come out CONSISTENT")
    mp = {}; okp = []
    for f in FOOTS:
        globals()["A0F"] = A0X[f]; rng = np.random.default_rng(959)
        Ep = dw_pred(f); Eo = Ep + rng.normal(0, DW[f]["sE"]); b = dw_class(f, Ep, Eobs=Eo); b["label"] = lab(b["z"])
        c = coma_eval(f, plant_rng=rng); c["label"] = lab(c["z"])
        g = rot_eval(f, "B", plant_rng=rng)
        el = lens_class(f, "LS", plant=True); el["label"] = lab(el["z"]); ed = lens_class(f, "LD", plant=True); ed["label"] = lab(ed["z"])
        d = cluster_eval(f, plant=True)
        mp[f] = dict(dSph=b, coma={k: v for k, v in c.items() if k != "per"}, rot={k: v for k, v in g.items() if k not in ("Eo", "Ep", "sE", "lg")},
                     LS=el, LD=ed, clusters=d)
        okp += [b["label"] == "CONSISTENT", c["label"] == "CONSISTENT", g["label"] == "CONSISTENT", el["label"] == "CONSISTENT",
                ed["label"] == "CONSISTENT", d["label"] == "EXPLAINS"]
        P(f"  [{f}] dSph {b['E']:+.3f}+-{b['se']:.3f} {b['label']}; Coma {c['mean_res']:+.3f}+-{c['se_res']:.3f} {c['label']}; rotators {g['mean_res']:+.3f}+-{g['se_res']:.3f} "
          f"{g['label']}; LS {el['E']:+.2e} {el['label']}; LD {ed['E']:+.2e} {ed['label']}; clusters MID {d['A']['MID'][0]:.4f} OUTER {d['A']['OUTER'][0]:.4f} {d['label']}")
    M["M-PLANT"] = dict(per=mp, bites=all(okp))
    P(f"  M-PLANT {'BITES (planted H-UNR recovered as CONSISTENT)' if all(okp) else 'DOES NOT BITE'}")
    RES["MUTATE"] = M; allb = all(M[k]["bites"] for k in M)
    P(f"\n  MUTATE: {sum(M[k]['bites'] for k in M)}/{len(M)} arms bite")
    finish(0 if allb else 1)

# ---------------------------------------------------------------------------------------------- MAIN
P("\n=== MAIN: primary form P-LIN (u = f_P), reading R-C, primary corner (C 3000, r_ta, census supply)")
PRIMR = evaluate("PLIN", "RC", PRIM)
RES["primary"] = PRIMR
cls = {f: PRIMR[f]["overall"]["cls"] for f in FOOTS}
head = cls["canonical"] if cls["canonical"] == cls["alt"] else min(cls.values(), key=lambda c: {"FAILS": 0, "PARTIAL": 1, "EXPLAINS": 2}[c])
P(f"\n  PRIMARY CLASS: canonical {cls['canonical']}, alt {cls['alt']} -> headline {head}")

P("\n=== diagnostics (no weight): DF2/DF4 if they had kept native debris (u = 1, R-C); per-dwarf extremes")
DIAG = {}
for f in FOOTS:
    globals()["A0F"] = A0X[f]; DIAG[f] = dict(df=df_debris_diag(f))
    for x in DIAG[f]["df"]:
        P(f"  [{f}] {x['name']}: E_obs {x['Eobs']:+.3f}, E_pred(u=1 debris) {x['Epred_u1']:+.3f} (z {x['z_u1']:+.1f}), Newton {x['Epred_newton']:+.3f} ln")
    Ep = dw_pred(f); d = DW[f]; Q = []
    for i in range(len(Ep)):
        h = halo_gal(d["Mbt"][i]); Mph = (d["gl"][i] - d["gN"][i]) * d["r12m"][i] ** 2 / G / MSUN; Q.append(float(McNFW(h, d["r12k"][i])) / Mph)
    Q = np.array(Q); DIAG[f]["dw_Qap"] = dict(median=float(np.median(Q)), min=float(Q.min()), max=float(Q.max()), n_gt1=int(np.sum(Q > 1)))
    Qc = []
    for m in COMA:
        r12pc = (4 / 3) * m["Re"] * 1e3; gb = G8 * (m["Ms"] / 2) * MS8 / (r12pc * PC8) ** 2; gL = gb * float(nu_e15(gb / A0X_R[f]))
        Mph = (gL - gb) * (r12pc * PC8) ** 2 / G8 / MS8; Qc.append(float(McNFW(halo_gal(m["Ms"]), r12pc / 1e3)) / Mph)
    DIAG[f]["coma_Qap"] = dict(median=float(np.median(Qc)), min=float(min(Qc)), max=float(max(Qc)))
    P(f"  [{f}] native debris / settled phantom at the aperture: dSphs median {DIAG[f]['dw_Qap']['median']:.3f} (range {Q.min():.3f}-{Q.max():.3f}, >1: {DIAG[f]['dw_Qap']['n_gt1']}/83); "
      f"Coma UDGs median {DIAG[f]['coma_Qap']['median']:.3f} ({min(Qc):.3f}-{max(Qc):.3f})")
LQ = []
for lm, fv in ((LM_BLUE, 0.20), (LM_RED + SHIFT_N2, 0.80)):                  # lens point masses: debris vs phantom (footing: canonical)
    M = 10 ** lm; h = halo_gal(M)
    for gg in (1e-11, 1e-12, 1e-13):
        Rk_ = math.sqrt(G * M * MSUN / gg) / KPC; nu_ = float(nu_e15(gg / A0X_R["canonical"])); Mph = (nu_ - 1) * M; Mn = float(McNFW(h, Rk_))
        Eu = math.log((M + min(Mph, (1 - fv) * h["Mc"]) + fv * Mn) / (nu_ * M)); E1 = math.log((M + Mn) / (nu_ * M))
        LQ.append(dict(logM=lm, g_bar=gg, R_kpc=Rk_, Mph_over_M=Mph / M, Mdeb_over_M=Mn / M, E_RC_uP=Eu, u=fv, E_RC_u1=E1))
        P(f"  [canonical] lens log M {lm:.3f} (Mc/M {h['Mc'] / M:.1f}, c {h['c']:.1f}, r_s {h['rs']:.1f} kpc): g_bar {gg:.0e} R {Rk_:5.0f} kpc  M_ph/M {Mph / M:6.2f}  "
          f"M_deb/M {Mn / M:6.2f}  E(R-C, u {fv:.1f}) {Eu:+.3f}  E(R-C, u 1) {E1:+.3f} ln")
DIAG["lens_debris_vs_phantom"] = LQ
ur = np.array([fP(VROT[t["name"]], 10.0) for t in TAB940])
DIAG["rotator_u"] = dict(min=float(ur.min()), median=float(np.median(ur)), max=float(ur.max()),
                         u_at_Vrot_10=fP(10.0, 10.0), u_at_Vrot_20=fP(20.0, 10.0))
P(f"  rotators (sigma 10 km/s): u = f_P min {ur.min():.3f} median {np.median(ur):.3f} max {ur.max():.3f}; u(V_rot 10) {fP(10.0, 10.0):.3f}, u(V_rot 20) {fP(20.0, 10.0):.3f}")
RES["diagnostics"] = DIAG

P("\n=== forms and readings at the primary corner (reported; they do not change the governing class)")
FR = {}
for form in ("PLIN", "VEQ", "VOP"):
    for reading in ("RC", "RA"):
        if (form, reading) == ("PLIN", "RC"): FR[f"{form}|{reading}"] = {f: PRIMR[f]["overall"] for f in FOOTS}; continue
        P(f"  --- form {form}, reading {reading}")
        r = evaluate(form, reading, PRIM, verbose=True); FR[f"{form}|{reading}"] = {f: r[f]["overall"] for f in FOOTS}
        RES.setdefault("forms_readings_full", {})[f"{form}|{reading}"] = r
RES["forms_readings"] = FR

P("\n=== brackets (P-LIN, R-C, primary corner; reported)")
BR = {}
for name, br, zr in (("dSph f_P V3a (HI v/s 1, others 0.5)", dict(dw="V3a"), "own"), ("sigma 6 km/s (SPARC, rotators)", dict(sig=6.0), "own"),
                     ("sigma 20 km/s (SPARC, rotators)", dict(sig=20.0), "own"), ("lens f_P (0.43, 0.57)", dict(lens_f=(0.43, 0.57)), "own"),
                     ("lens f_P (0.10, 0.97)", dict(lens_f=(0.10, 0.97)), "own"), ("clusters z_i = 0", {}, "zero")):
    P(f"  --- {name}")
    r = evaluate("PLIN", "RC", PRIM, brackets=br, zrule=zr, verbose=True)
    BR[name] = {f: r[f]["overall"] for f in FOOTS}
    BR[name]["clusters"] = {f: dict(A=r[f]["d"]["A"], s=r[f]["d"]["s"], label=r[f]["d"]["label"]) for f in FOOTS}
RES["brackets"] = BR

P("\n=== robustness: 12 corners (C 1500/3000/6000 x r_ta/r_vir x supply census/x2), P-LIN, R-C")
CO = {}; counts = {f: {} for f in FOOTS}
for cor in CORNERS:
    tag = f"C{int(cor[0])}|{cor[1]}|x{int(cor[2])}"
    if cor == PRIM:
        r = PRIMR
    else:
        P(f"  --- corner {tag}"); r = evaluate("PLIN", "RC", cor, verbose=True)
    CO[tag] = {f: dict(overall=r[f]["overall"], b=dict(E=r[f]["b"]["E"], se=r[f]["b"]["se"], label=r[f]["b"]["label"]),
                       c=dict(res=r[f]["c"]["mean_res"], se=r[f]["c"]["se_res"], label=r[f]["c"]["label"]),
                       d=dict(MID=r[f]["d"]["A"]["MID"], OUTER=r[f]["d"]["A"]["OUTER"], s=r[f]["d"]["s"], label=r[f]["d"]["label"]),
                       e=dict(E=r[f]["e"]["obs"]["E"], z=r[f]["e"]["obs"]["z"], label=r[f]["e"]["label"]),
                       a=dict(rms=r[f]["a"]["rms"], U=r[f]["a"]["U"], passes=r[f]["a"]["passes"]), a2=dict(E=r[f]["a2"]["E"], label=r[f]["a2"]["label"]),
                       g=dict(res=r[f]["g"]["B"]["mean_res"], label=r[f]["g"]["label"])) for f in FOOTS}
    for f in FOOTS:
        k = r[f]["overall"]["cls"]; counts[f][k] = counts[f].get(k, 0) + 1
    P(f"  corner {tag}: canonical {r['canonical']['overall']['cls']} {r['canonical']['overall']['explained']}, alt {r['alt']['overall']['cls']} {r['alt']['overall']['explained']}")
rob = {f: ("ROBUST" if counts[f].get(cls[f], 0) == len(CORNERS) else "FRAGILE") for f in FOOTS}
RES["corners"] = CO; RES["corner_counts"] = counts; RES["robustness"] = rob
P(f"\n  corner counts: canonical {counts['canonical']}, alt {counts['alt']} -> {rob}")
RES["class"] = dict(per_footing=cls, headline=head, robustness=rob)
P(f"\n  CLASS (governing: P-LIN, R-C, primary corner): canonical {cls['canonical']} ({rob['canonical']}), alt {cls['alt']} ({rob['alt']}); headline {head}")
finish(0)
