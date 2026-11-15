#!/usr/bin/env python3
"""CLR1 (FROZEN_CRITERIA.md, 7756d82189): does form B close the cluster residual that plain MOND leaves on Combes's 106
HIFLUGCS clusters? TEST lane; adopts nothing, relabels nothing. Rebuilds Combes's setup per cluster from Chen et al. 2007
(transcribed CSV), checks it against her aggregates (KA-C), then grades form B (RB1's cold, ZN4 native shape) per class
(NCC / weak-CC / CC) in three regions (OUTER R500, MIDDLE 0.1-0.5 R500, CORE 20-30 kpc), both footings, never pooled.
    python3 -I -B clr1.py <chen csv> <zn4_shapes.json> <qx15.json> <xcop dir> <out dir>
Writes clr1.out / clr1.json and clr1_MUTATE.out / clr1_MUTATE.json in <out dir>. Code COPIED (not imported) from RB1
(m_native, solve_R200, glaw) and RB1R (X-COP loader, f_ret). kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, csv, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import gammaln

CSV_IN, ZN4_IN, QX15_IN, XCOP_DIR, OUTD = sys.argv[1:6]
CRIT = "7756d82189"; T0 = time.time()
LINES, MLINES = [], []
def P(s=""): print(s, flush=True); LINES.append(str(s))
def PM(s=""): print("[MUTATE] " + str(s), flush=True); MLINES.append(str(s))

# ------------------------------------------------------------------ constants (SI)
G = 6.67430e-11; MP = 1.67262192e-27; KEV = 1.602176634e-16; MSUN = 1.98841e30; KPC = 3.0856775814913673e19
C_KMS = 299792.458; MU = 0.61
A0C = 1.2e-10                                                     # Combes
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
R_COS, R_BR = 5.41, 5.562
BAND = 0.08; NOPOW = 0.15; NBOOT = 10000; SEED = 1114
GK = G * MSUN / KPC                                               # G in m^2 s^-2 kpc / Msun  (g = GK*M/r_kpc / KPC)
def g_of(M, r): return G * M * MSUN / (r * KPC) ** 2               # m/s^2, M in Msun, r in kpc
def M_of(g, r): return g * (r * KPC) ** 2 / G / MSUN

# ------------------------------------------------------------------ interpolation laws
def glaw(g, a0): g = np.asarray(g, float); return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))   # RB1's (mu = x/(1+x))
def g_rar(gb, a0): gb = np.asarray(gb, float); return gb / (-np.expm1(-np.sqrt(np.maximum(gb, 1e-300) / a0)))
def g_comb_simple(gb, a0):                                         # Combes's text: nu^2 = (1 + sqrt(1 + 4/y^2)) / 2
    y = np.maximum(np.asarray(gb, float), 1e-300) / a0; return gb * np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y ** 2)))
def invert(fun, gobs, a0, it=200):
    """g_bar with fun(g_bar) = g_obs (fun monotonic, fun(g) >= g); bisection in log."""
    gobs = np.asarray(gobs, float); lo = np.log(np.maximum(gobs, 1e-300) * 1e-12); hi = np.log(np.maximum(gobs, 1e-300))
    for _ in range(it):
        mid = 0.5 * (lo + hi); v = fun(np.exp(mid), a0) > gobs; hi = np.where(v, mid, hi); lo = np.where(v, lo, mid)
    return np.exp(0.5 * (lo + hi))

# ------------------------------------------------------------------ cosmology
QX = json.load(open(QX15_IN))
FOOT_BG = {f: dict(h=float(QX["footings"][f]["main"]["h"]),
                   Om=(QX["footings"][f]["main"]["theta"]["omega_b"] + QX["footings"][f]["main"]["theta"]["omega_d"]) / float(QX["footings"][f]["main"]["h"]) ** 2) for f in FOOTS}
def DA_eds50(z): return 2 * C_KMS / 50.0 * (1 - 1 / math.sqrt(1 + z)) / (1 + z) * 1e3       # kpc
def DA_flat(z, h, Om): return C_KMS / (100 * h) * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0] / (1 + z) * 1e3
def rhoc_kpc(H_kms_mpc): H = H_kms_mpc * 1e3 / (KPC * 1e3); return 3 * H * H / (8 * math.pi * G) * KPC ** 3 / MSUN   # Msun/kpc^3
def rhoc_eds50(z): return rhoc_kpc(50.0) * (1 + z) ** 3
def rhoc_flat(z, h, Om): return rhoc_kpc(100 * h * math.sqrt(Om * (1 + z) ** 3 + 1 - Om))

# ------------------------------------------------------------------ data
def fnum(x): return float(x) if x not in ("", None) else None
with open(CSV_IN) as f: rows = [r for r in csv.DictReader(l for l in f if not l.startswith("#"))]
CL = []
for r in rows:
    c = {k: (fnum(v) if k not in ("name", "src_t12", "src_t45", "src_t3", "Tm_flag", "Th_flag") else v) for k, v in r.items()}
    c["double"] = int(c["double"] or 0)
    md = c["Mdot"]; c["cls"] = "NCC" if md == 0 else ("weak-CC" if md < 60 else "CC")
    if c["double"]:
        B = lambda b: math.sqrt(math.pi) * math.exp(gammaln(3 * b - 0.5) - gammaln(3 * b))
        c["A1"] = c["S01"] / (c["rc1_kpc"] * B(c["beta1"])); c["A2"] = c["S02"] / (c["rc2_kpc"] * B(c["beta2"]))
    CL.append(c)
CLASSES = ("NCC", "weak-CC", "CC")

# ------------------------------------------------------------------ cluster model (Chen coordinates, then frame map)
def n2(c, r, single=False):
    """unnormalised n^2 and dln n / dln r at Chen-frame radius r (kpc)."""
    r = np.asarray(r, float)
    if c["double"] and not single:
        a1 = 1 + (r / c["rc1_kpc"]) ** 2; a2 = 1 + (r / c["rc2_kpc"]) ** 2
        t1 = c["A1"] * a1 ** (-3 * c["beta1"]); t2 = c["A2"] * a2 ** (-3 * c["beta2"])
        dl = -3 * r ** 2 * (c["A1"] * c["beta1"] * a1 ** (-3 * c["beta1"] - 1) / c["rc1_kpc"] ** 2 + c["A2"] * c["beta2"] * a2 ** (-3 * c["beta2"] - 1) / c["rc2_kpc"] ** 2) / (t1 + t2)
        return t1 + t2, dl
    a = 1 + (r / c["rc_kpc"]) ** 2; return a ** (-3 * c["beta"]), -3 * c["beta"] * (r / c["rc_kpc"]) ** 2 / a

def Tprof(c, r, o):
    """T(r) keV and dlnT/dlnr (Chen frame)."""
    T = (c["Tm"] if o.get("Tsrc") == "Tm" else c["Th"]) * o.get("Tscale", 1.0); r = np.asarray(r, float)
    if c["cls"] == "NCC" or o.get("cc_grad", "lin") == "off" or (o.get("cc_only") and c["cls"] != "CC"): return T * np.ones_like(r), np.zeros_like(r)
    rT = c["rc_kpc"] if o.get("rT") == "rc" else 0.1 * c["r500_Mpc"] * 1e3
    t0 = o.get("Tc", 0.8); inside = r < rT; u = np.where(inside, r / rT, 1.0)
    f = np.where(inside, t0 + (1 - t0) * u, 1.0); d = np.where(inside, (1 - t0) * u / f, 0.0); return T * f, d

def Mdyn_chen(c, r, o):
    T, dT = Tprof(c, r, o); _, dn = n2(c, r, o.get("single", False))
    return -(T * KEV) * (np.asarray(r) * KPC) / (MU * MP * G) * (dT + dn) / MSUN

def gas_table(c, o):
    rr = np.geomspace(1e-3, 2e4, 6000); nn, _ = n2(c, rr, o.get("single", False)); n = np.sqrt(nn)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (4 * np.pi * rr[1:] ** 2 * n[1:] + 4 * np.pi * rr[:-1] ** 2 * n[:-1]) * np.diff(rr))])
    r5 = c["r500_Mpc"] * 1e3
    if o.get("gas") == "ncenter":   # rho = 1.17 m_p n_e, n_e(0) = n_center
        norm = 1.17 * MP * c["ncenter_1e2cm3"] * 1e-2 * 1e6 * KPC ** 3 / MSUN / math.sqrt(nn[0])
    else:
        norm = c["Mgas500_1e13"] * 1e13 / float(np.interp(math.log(r5), np.log(rr), cum))
    return rr, cum * norm

def hern(Mstar100, Re, r):
    a = Re / (1 + math.sqrt(2)); Mt = Mstar100 * (100 + a) ** 2 / 100 ** 2; return Mt * np.asarray(r) ** 2 / (np.asarray(r) + a) ** 2

def build(c, o, frame):
    """Profiles on the frame grid. frame: ('combes',) or ('foot', h, Om)."""
    z = c["z"]; ngrid = o.get("ngrid", 60); b = o.get("b", 0.0)
    if frame[0] == "combes": s = 1.0; rc_of = lambda z: rhoc_eds50(z)
    else: s = DA_flat(z, frame[1], frame[2]) / DA_eds50(z); rc_of = lambda z: rhoc_flat(z, frame[1], frame[2])
    md = lambda rf: s * Mdyn_chen(c, np.asarray(rf) / s, o) / (1 - b)
    rr, cum = gas_table(c, o); mg = lambda rf: s ** 2.5 * np.exp(np.interp(np.log(np.asarray(rf) / s), np.log(rr[1:]), np.log(cum[1:])))
    if frame[0] == "combes" and not o.get("resolve_r500"):
        R5 = c["r500_Mpc"] * 1e3; M5 = c["M500_1e14"] * 1e14
    else:
        rho = 500 * rc_of(z); fn = lambda lr: math.log(max(float(md(math.exp(lr))), 1e-30)) - math.log(rho * 4 * math.pi / 3 * math.exp(lr) ** 3)
        lg = np.log(np.geomspace(30.0, 1e4, 400)); fv = np.array([fn(v) for v in lg]); idx = np.where((fv[:-1] > 0) & (fv[1:] <= 0))[0]
        i = int(idx[-1])                                         # outermost crossing (M_dyn <= 0 points near the centre are skipped)
        R5 = math.exp(brentq(fn, lg[i], lg[i + 1], xtol=1e-12)); M5 = float(md(R5))
    r = np.concatenate([np.geomspace(20.0, R5, ngrid)]); r[-1] = R5
    Md = md(r); Mg = mg(r)
    fst = 0.05 * (M5 / 5e13) ** -0.37 * o.get("gio", 1.0)
    gal = fst * M5 * ((mg(r) / mg(R5)) if o.get("galprof") == "gas" else (Md / float(md(R5))))
    Mbcg = 10 ** (0.37 * math.log10(M5 / 2e14) + 11.92) * o.get("dem", 1.0)
    bcg = hern(Mbcg, o.get("Re", 30.0), r)
    Mv = Mg + gal + bcg
    return dict(name=c["name"], cls=c["cls"], z=z, s=s, r=r, R500=R5, M500=M5, Md=Md, Mg=Mg, Mgal=gal, Mbcg=bcg, Mv=Mv, rho_c=rc_of(z), frame=frame)

# ------------------------------------------------------------------ ZN4 native shape (COPIED from RB1 rb1.py, rho_c generalised)
ZN = json.load(open(ZN4_IN)); SH = {k: dict(ZN[k]["0.00"]) for k in ("1e14", "1e15")}
for k in SH: SH[k]["x_"] = np.array(SH[k]["x"], float); SH[k]["l_"] = np.array(SH[k]["lnm"], float)
def m_native(x, lgM, stretch=1.0, inner=None):
    x = np.asarray(x, float) / stretch; a, b = SH["1e14"], SH["1e15"]; w = float(np.clip((lgM - a["lgM"]) / (b["lgM"] - a["lgM"]), 0.0, 1.0)); out = []
    for s in (a, b):
        xe = s["x_edge"]; xx = np.minimum(x, xe); lx = np.log(np.maximum(xx, 1e-12)); l0 = np.log(s["x_"][0])
        v = np.where(xx >= s["x_"][0], np.interp(lx, np.log(s["x_"]), s["l_"]), s["l_"][0] + 2.0 * (lx - l0))
        if inner == "slope":   # N1 bracket: below x = 0.05 continue with the log slope over 0.05-0.1
            l05 = np.interp(np.log(0.05), np.log(s["x_"]), s["l_"]); l10 = np.interp(np.log(0.1), np.log(s["x_"]), s["l_"]); k = (l10 - l05) / math.log(2.0)
            v = np.where(xx < 0.05, l05 + k * (lx - math.log(0.05)), v)
        out.append(v)
    return np.exp((1 - w) * out[0] + w * out[1])
def m_nfw(x, c): mu = lambda t: np.log1p(t) - t / (1 + t); return mu(c * np.asarray(x, float)) / mu(c)
def duffy_c200(M200, z, h): return 5.71 * (M200 / (2e12 / h)) ** -0.084 * (1 + z) ** -0.47
def solve_R200(Ctarget, r_anchor, rho_c, z, R=R_COS, shape="native", stretch=1.0, inner=None, h=0.674):
    fc = R / (1 + R)
    def cold_in(R2):
        M200 = 200 * rho_c * 4 * math.pi / 3 * R2 ** 3
        m = m_native(r_anchor / R2, math.log10(M200), stretch, inner) if shape == "native" else m_nfw(r_anchor / R2, duffy_c200(M200, z, h))
        return fc * M200 * float(m)
    R2 = math.exp(brentq(lambda lr: math.log(cold_in(math.exp(lr))) - math.log(Ctarget), math.log(20.0), math.log(5e4), xtol=1e-12))
    M200 = 200 * rho_c * 4 * math.pi / 3 * R2 ** 3; return R2, M200, cold_in(R2) / Ctarget - 1
def cold_profile(p, anchor, o):
    R = o.get("R", R_COS); C = R * p["Mv"][-1] * o.get("Rmult", 1.0) if anchor == "A1" else max(p["Md"][-1] - p["Mv"][-1], 0.0)
    if anchor == "A1": R = R * o.get("Rmult", 1.0)
    if C <= 0: return np.zeros_like(p["r"]), 0.0
    h = p["frame"][1] if p["frame"][0] == "foot" else 0.5
    R2, M200, e = solve_R200(C, p["R500"], p["rho_c"], p["z"], R, o.get("shape", "native"), o.get("stretch", 1.0), o.get("inner"), h)
    fc = R / (1 + R)
    m = m_native(p["r"] / R2, math.log10(M200), o.get("stretch", 1.0), o.get("inner")) if o.get("shape", "native") == "native" else m_nfw(p["r"] / R2, duffy_c200(M200, p["z"], h))
    return fc * M200 * m, abs(e)

# ------------------------------------------------------------------ rows and cells
FLOOR = -3.0
def lq(Md, Mp):
    Md = np.asarray(Md, float); Mp = np.asarray(Mp, float)
    return np.where((Md > 0) & (Mp > 0), np.log10(np.maximum(Md, 1e-300) / np.maximum(Mp, 1e-300)), FLOOR)
def rows_of(p, o, foot=None):
    r = p["r"]; gv = g_of(p["Mv"], r); out = {}
    out["newton"] = lq(p["Md"], p["Mv"])
    out["mond_rar"] = lq(p["Md"], M_of(g_rar(gv, A0C), r))
    out["mond_simple_combes"] = lq(p["Md"], M_of(g_comb_simple(gv, A0C), r))
    if foot: out["law"] = lq(p["Md"], M_of(glaw(gv, A0[foot]), r))
    c1, e1 = cold_profile(p, "A1", o); c2, e2 = cold_profile(p, "A2", o)
    out["B_A1"] = lq(p["Md"], p["Mv"] + c1); out["B_A2"] = lq(p["Md"], p["Mv"] + c2); out["_anc"] = max(e1, e2)
    return out
def cells_of(p, rows, psf=False):
    r = p["r"]; x = r / p["R500"]; mid = (x >= 0.1) & (x <= 0.5); core = (r >= 20.0) & (r <= 30.0)
    if psf:
        kpc_per_arcsec = DA_flat(p["z"], p["frame"][1], p["frame"][2]) / 206264.806 if p["frame"][0] == "foot" else DA_eds50(p["z"]) / 206264.806
        if 25 * kpc_per_arcsec > 10.0: core = np.zeros_like(core)
    out = {}
    for k, v in rows.items():
        if k.startswith("_"): continue
        out[k] = dict(OUTER=float(v[-1]), MIDDLE=float(np.median(v[mid])) if mid.any() else float("nan"), CORE=float(np.mean(v[core])) if core.any() else float("nan"))
    out["B"] = dict(OUTER=out["B_A1"]["OUTER"], MIDDLE=out["B_A2"]["MIDDLE"], CORE=out["B_A2"]["CORE"])
    return out
def boot(vals, seed=SEED):
    v = np.asarray([x for x in vals if np.isfinite(x)], float); n = len(v)
    if n == 0: return dict(n=0, med=None, lo=None, hi=None)
    rng = np.random.default_rng(seed); meds = np.median(v[rng.integers(0, n, size=(NBOOT, n))], axis=1); lo, hi = np.percentile(meds, [2.5, 97.5])
    return dict(n=n, med=float(np.median(v)), lo=float(lo), hi=float(hi))
def cword(st):
    if st["n"] < 5: return "NOT EVALUABLE"
    if st["lo"] > BAND: w = "RESIDUAL REMAINS"
    elif st["hi"] < -BAND: w = "OVER-PREDICTS"
    else: w = "CLOSED"
    if 0.5 * (st["hi"] - st["lo"]) > NOPOW: w += " (NO POWER)"
    return w
REG = ("OUTER", "MIDDLE", "CORE")
def run(o, frame, foot=None, seed=SEED, psf=False, keep=False):
    P_ = [build(c, o, frame) for c in CL]; percl = []; anc = 0.0; nneg = 0
    for p in P_:
        rw = rows_of(p, o, foot); anc = max(anc, rw.pop("_anc")); nneg += int(np.sum(p["Md"] <= 0)); percl.append(dict(name=p["name"], cls=p["cls"], cells=cells_of(p, rw, psf), R500=p["R500"], M500=p["M500"], Mv=float(p["Mv"][-1]), Md=float(p["Md"][-1]), Mg=float(p["Mg"][-1]), rw=rw if keep else None, p=p if keep else None))
    stat = {}
    for row in ("newton", "mond_rar", "mond_simple_combes", "law", "B", "B_A1", "B_A2"):
        if row == "law" and not foot: continue
        stat[row] = {}
        for cl in CLASSES + ("All",):
            for rg in REG:
                vals = [q["cells"][row][rg] for q in percl if cl == "All" or q["cls"] == cl]
                st = boot(vals, seed); st["word"] = cword(st); stat[row][f"{cl}|{rg}"] = st
    # data-inconsistency and the B word
    for cl in CLASSES + ("All",):
        for rg in REG:
            k = f"{cl}|{rg}"
            for row in stat:
                stat[row][k]["data_inconsistent"] = stat["newton"][k]["word"].startswith("OVER-PREDICTS")
    return dict(stat=stat, percl=percl, anchor_err=anc, n_Mdyn_le0=nneg)
def bword(stat):
    """B's word for one run (graded classes only)."""
    fails, closed, nopow, ne = [], 0, [], 0
    for cl in CLASSES:
        for rg in REG:
            st = stat["B"][f"{cl}|{rg}"]
            if st["data_inconsistent"] or st["n"] < 5: ne += 1; continue
            w = st["word"]
            if "NO POWER" in w: nopow.append(f"{cl} {rg}")
            if w.startswith("RESIDUAL"): fails.append(f"{cl} {rg}: residual remains")
            elif w.startswith("OVER"): fails.append(f"{cl} {rg}: over-predicts")
            else: closed += 1
    if fails: return "STILL FAILS [" + "; ".join(fails) + "]", fails
    if nopow: return "NO VERDICT", nopow
    return "FORM B CLOSES THE RESIDUAL", []

def fmt(st): return "n/a" if st["n"] == 0 else f"{st['med']:+.3f} [{st['lo']:+.3f}, {st['hi']:+.3f}] n={st['n']}"

RES = dict(criteria=CRIT, note="TEST lane; adopts nothing; relabels nothing; kappa = 1/2 FITTED; not theory closed", band=BAND, footings={f: dict(a0=A0[f], **FOOT_BG[f]) for f in FOOTS})
P(f"CLR1 (criteria {CRIT}): form B on Combes's 106 HIFLUGCS clusters. R {R_COS}; band +-{BAND} dex; footings canonical a0 {A0['canonical']}, alt {A0['alt']}, never pooled.")
P(f"footing backgrounds: " + "; ".join(f"{f} h {FOOT_BG[f]['h']:.5f} Om {FOOT_BG[f]['Om']:.4f}" for f in FOOTS) + ". a0(z) = a0 (w = -1, record's convention).")

# ================================================================== KNOWN ANSWERS
KA = {}; STOP = []
cnt = {k: sum(1 for c in CL if c["cls"] == k) for k in CLASSES}
KA["P"] = dict(n=len(CL), n_double=sum(c["double"] for c in CL), classes=cnt, ok=(len(CL) == 106 and sum(c["double"] for c in CL) == 49 and cnt == {"NCC": 56, "weak-CC": 25, "CC": 25}))
P(); P(f"KA-P parse: {KA['P']}  -> {'PASS' if KA['P']['ok'] else 'FAIL'}")
if not KA["P"]["ok"]: STOP.append("KA-P")
# KA-U
iso = dict(cc_grad="off"); ra = []; rb = []; dens = []; dens0 = []
for c in CL:
    r5 = c["r500_Mpc"] * 1e3; M = float(Mdyn_chen(c, np.array([r5]), iso)[0]); rat = M / (c["M500_1e14"] * 1e14)
    (rb if c["double"] else ra).append(rat)
    dens.append(c["M500_1e14"] * 1e14 / (4 * math.pi / 3 * r5 ** 3) / rhoc_eds50(c["z"])); dens0.append(c["M500_1e14"] * 1e14 / (4 * math.pi / 3 * r5 ** 3) / rhoc_kpc(50.0))
KA["U"] = dict(single_med=float(np.median(ra)), double_med=float(np.median(rb)), single_n=len(ra), double_n=len(rb), single_p10_p90=[float(np.percentile(ra, 10)), float(np.percentile(ra, 90))],
               double_p10_p90=[float(np.percentile(rb, 10)), float(np.percentile(rb, 90))], dens_over_rhoc_z=float(np.median(dens)), dens_over_rhoc0=float(np.median(dens0)))
c85 = next(c for c in CL if c["name"] == "A0085"); r5 = c85["r500_Mpc"] * 1e3
si = 3 * c85["beta"] * c85["Th"] * KEV * r5 * KPC / (G * MU * MP) / MSUN
cgs = 3 * c85["beta"] * (c85["Th"] * 1.602176634e-9) * (r5 * 3.0856775814913673e21) / (6.67430e-8 * MU * 1.67262192e-24) / 1.98841e33
KA["U"]["A0085_asym_SI"] = si; KA["U"]["A0085_asym_cgs"] = cgs
KA["U"]["ok"] = (0.97 <= KA["U"]["single_med"] <= 1.03 and 0.95 <= KA["U"]["double_med"] <= 1.05 and 450 <= KA["U"]["dens_over_rhoc_z"] <= 550 and abs(si / cgs - 1) < 1e-9)
P(f"KA-U units: Chen M500 reproduced (isothermal T_h, Chen r500): single-beta median {KA['U']['single_med']:.4f} (n {len(ra)}, p10-p90 {KA['U']['single_p10_p90'][0]:.3f}-{KA['U']['single_p10_p90'][1]:.3f}), "
  f"double-beta {KA['U']['double_med']:.4f} (n {len(rb)}, p10-p90 {KA['U']['double_p10_p90'][0]:.3f}-{KA['U']['double_p10_p90'][1]:.3f}); M500/(4pi/3 r500^3)/rho_c(z) median {KA['U']['dens_over_rhoc_z']:.1f} (rho_c0: {KA['U']['dens_over_rhoc0']:.1f}); "
  f"A0085 3 beta kT r/(G mu m_p) at r500: SI {si:.6e}, cgs {cgs:.6e} Msun -> {'PASS' if KA['U']['ok'] else 'FAIL'}")
if not KA["U"]["ok"]: STOP.append("KA-U")

# KA-I identities
gb = np.geomspace(1e-14, 1e-8, 50); rt = invert(g_rar, g_rar(gb, A0C), A0C); rt2 = invert(g_comb_simple, g_comb_simple(gb, A0C), A0C)
KA["I"] = dict(rar_roundtrip=float(np.max(np.abs(rt / gb - 1))), simple_roundtrip=float(np.max(np.abs(rt2 / gb - 1))),
               m1={k: float(np.exp(np.interp(0.0, np.log(SH[k]["x_"]), SH[k]["l_"]))) for k in SH})
pt = build(CL[1], {}, ("foot", FOOT_BG["canonical"]["h"], FOOT_BG["canonical"]["Om"])); c1, _ = cold_profile(pt, "A1", {})
KA["I"]["B_A1_R500"] = float(abs(pt["Md"][-1] / (pt["Mv"][-1] + c1[-1]) / (pt["Md"][-1] / ((1 + R_COS) * pt["Mv"][-1])) - 1))
KA["I"]["newton_limit"] = float(np.max(np.abs(g_rar(gb, 1e-30) / gb - 1)))
KA["I"]["ok"] = KA["I"]["rar_roundtrip"] < 1e-10 and KA["I"]["simple_roundtrip"] < 1e-10 and all(abs(v - 1) < 1e-3 for v in KA["I"]["m1"].values()) and KA["I"]["B_A1_R500"] < 1e-8 and KA["I"]["newton_limit"] < 1e-8
P(f"KA-I identities: {KA['I']} -> {'PASS' if KA['I']['ok'] else 'FAIL'}")
if not KA["I"]["ok"]: STOP.append("KA-I")

# KA-C Combes's own residual
def combes_stats(frame, o=None, a0=A0C, fun=g_rar):
    o = o or {}; D1, D2, red, dg1, dg2 = [], [], [], [], []
    for c in CL:
        p = build(c, o, frame); r = p["r"]; gobs = g_of(p["Md"], r); Mm = M_of(invert(fun, gobs, a0), r)
        dm = Mm - p["Mv"]; D1.append(dm[-1] / Mm[-1]); D2.append(max(float(np.max(dm)), 0.0) / Mm[-1]); red.append(p["Md"][-1] / Mm[-1])
        dg1.append(dm[-1] / p["Mg"][-1]); dg2.append(max(float(np.max(dm)), 0.0) / p["Mg"][-1])
    return dict(D1_mean=float(np.mean(D1)), D2_mean=float(np.mean(D2)), red_med=float(np.median(red)), red_p10_p90=[float(np.percentile(red, 10)), float(np.percentile(red, 90))],
                dg_D1_med=float(np.median(dg1)), dg_D2_med=float(np.median(dg2)))
def ka_c(frame):
    rar = combes_stats(frame); sim = combes_stats(frame, fun=g_comb_simple); res = dict(rar=rar, simple=sim, defs={})
    for d in ("D1", "D2"):
        c1 = 0.33 <= rar[f"{d}_mean"] <= 0.49; c2 = (0.45 <= sim[f"{d}_mean"] <= 0.61) and sim[f"{d}_mean"] > rar[f"{d}_mean"]
        c3 = 3 <= rar["red_med"] <= 10; c4 = 0.3 <= rar[f"dg_{d}_med"] <= 1.0
        res["defs"][d] = dict(C1=c1, C2=c2, C3=c3, C4=c4, all=c1 and c2 and c3 and c4)
    res["ok_def"] = [d for d in ("D1", "D2") if res["defs"][d]["all"]]; return res
FR_C = ("combes",); FR_F = {f: ("foot", FOOT_BG[f]["h"], FOOT_BG[f]["Om"]) for f in FOOTS}
KA["C"] = {"combes_frame": ka_c(FR_C)}
for fr, v in KA["C"].items():
    P(f"KA-C [{fr}] RAR: <M_dark/M_MOND> D1 {v['rar']['D1_mean']:.3f}, D2 {v['rar']['D2_mean']:.3f}; simple (Combes's nu): D1 {v['simple']['D1_mean']:.3f}, D2 {v['simple']['D2_mean']:.3f}; "
      f"median M_dyn/M_MOND at R500 {v['rar']['red_med']:.2f} (p10-p90 {v['rar']['red_p10_p90'][0]:.2f}-{v['rar']['red_p10_p90'][1]:.2f}); median M_dark/M_gas D1 {v['rar']['dg_D1_med']:.3f}, D2 {v['rar']['dg_D2_med']:.3f}")
    P(f"      checks: {v['defs']} -> passing definition(s): {v['ok_def'] or 'NONE'}")
if not KA["C"]["combes_frame"]["ok_def"]:
    KA["C"]["footing_frame_canonical"] = ka_c(FR_F["canonical"]); v = KA["C"]["footing_frame_canonical"]
    P(f"KA-C [footing frame, canonical] RAR: D1 {v['rar']['D1_mean']:.3f}, D2 {v['rar']['D2_mean']:.3f}; simple D1 {v['simple']['D1_mean']:.3f}, D2 {v['simple']['D2_mean']:.3f}; red {v['rar']['red_med']:.2f}; dg D1 {v['rar']['dg_D1_med']:.3f} D2 {v['rar']['dg_D2_med']:.3f}; {v['defs']}")
KA["C"]["ok"] = any(KA["C"][k]["ok_def"] for k in KA["C"] if isinstance(KA["C"][k], dict) and "ok_def" in KA["C"][k])
P(f"KA-C -> {'PASS' if KA['C']['ok'] else 'FAIL'}")
if not KA["C"]["ok"]: STOP.append("KA-C")

# KA-X: RB1 X-COP number, loader COPIED from RB1R rb1r.py
from astropy.io import fits
def x_interp_loglog(rt, mt, r):
    rt = np.asarray(rt, float); mt = np.asarray(mt, float); ok = np.isfinite(rt) & np.isfinite(mt) & (rt > 0) & (mt > 0); rt, mt = rt[ok], mt[ok]
    o = np.argsort(rt); rt, mt = rt[o], mt[o]; r = np.atleast_1d(np.asarray(r, float)); out = np.full(r.shape, np.nan)
    inside = (r >= rt[0]) & (r <= rt[-1]) & (r > 0); out[inside] = np.exp(np.interp(np.log(r[inside]), np.log(rt), np.log(mt))); return out
def x_interp_loglin(rt, yt, r):
    rt = np.asarray(rt, float); yt = np.asarray(yt, float); ok = np.isfinite(rt) & np.isfinite(yt) & (rt > 0); rt, yt = rt[ok], yt[ok]
    o = np.argsort(rt); rt, yt = rt[o], yt[o]; r = np.atleast_1d(np.asarray(r, float)); out = np.full(r.shape, np.nan)
    inside = (r >= rt[0]) & (r <= rt[-1]) & (r > 0); out[inside] = np.interp(np.log(r[inside]), np.log(rt), yt); return out
def x_f_ret(mdyn, mb, R):
    mdyn, mb = np.broadcast_arrays(np.atleast_1d(np.asarray(mdyn, float)), np.atleast_1d(np.asarray(mb, float))); out = np.full(mdyn.shape, np.inf); ok = mdyn > mb
    out[ok] = R * mb[ok] / (mdyn[ok] - mb[ok]); return out
def x_load():
    names = sorted(d for d in os.listdir(XCOP_DIR) if os.path.isdir(os.path.join(XCOP_DIR, d))); cl = {}
    for n in names:
        d = os.path.join(XCOP_DIR, n)
        with fits.open(os.path.join(d, f"{n}_hydro_mass.fits")) as h:
            t = h[1].data; hdr = h[1].header; c = {"name": n, "R500_hdr": float(hdr["R500"]), "z": float(hdr["REDSHIFT"]), "h_r": np.array(t["RADIUS"], float)}
            for col in ["M_FORW", "EM_FORW"]: c["h_" + col] = np.array(t[col], float)
        with fits.open(os.path.join(d, f"{n}_fgas_profile.fits")) as g:
            t = g[1].data; c["g_x"] = np.array(t["RADIUS"], float); c["g_r"] = c["g_x"] * c["R500_hdr"]; c["g_m"] = np.array(t["MGAS"], float)
            lo = np.array(t["MGAS_LO"], float); hi = np.array(t["MGAS_HI"], float)
            c["g_sf"] = 0.5 * (lo + hi) / c["g_m"] if bool(np.all(hi < c["g_m"])) else 0.5 * (hi - lo) / c["g_m"]
        sp = os.path.join(d, f"{n}_mstar.fits"); c["has_star"] = os.path.exists(sp)
        if c["has_star"]:
            with fits.open(sp) as s:
                t = s[2].data; c["s_r"] = np.array(t["RADIUS"], float); c["s_m"] = np.array(t["MSTAR"], float)
                lo = np.array(t["MSTAR_LO"], float); hi = np.array(t["MSTAR_HI"], float); bounds = np.all((lo <= c["s_m"]) & (hi >= c["s_m"]))
                c["s_sf"] = np.where(c["s_m"] > 0, 0.5 * (hi - lo) / np.where(c["s_m"] > 0, c["s_m"], 1), np.nan) if bounds else 0.5 * (lo + hi) / c["s_m"]
        cl[n] = c
    return names, cl
def x_profile(c):
    r = c["g_r"]; md = x_interp_loglog(c["h_r"], c["h_M_FORW"], r); sd = x_interp_loglin(c["h_r"], c["h_EM_FORW"] / c["h_M_FORW"], r)
    mg = c["g_m"].copy(); sg = c["g_sf"].copy(); ms = x_interp_loglog(c["s_r"], c["s_m"], r); ss = x_interp_loglin(c["s_r"], c["s_sf"], r)
    keep = np.isfinite(md) & np.isfinite(mg) & np.isfinite(ms) & (mg > 0) & (md > 0) & np.isfinite(sd) & np.isfinite(sg) & np.isfinite(ss)
    return {"r": r[keep], "md": md[keep], "mg": mg[keep], "ms": ms[keep]}
XN, XC = x_load(); KAX = {}
for n in [n for n in XN if XC[n]["has_star"]]:
    pr = x_profile(XC[n]); i = int(np.argmax(pr["r"])); KAX[n] = float(x_f_ret(pr["md"][i], pr["mg"][i] + pr["ms"][i], R_COS)[0])
REFX = {"A1795": 0.885, "A2029": 0.934, "A2142": 1.235, "A2319": 1.259, "A644": 2.216, "A85": 1.095, "ZW1215": 0.511}
KA["X"] = dict(mine=KAX, ref=REFX, median=float(np.median(list(KAX.values()))), ok=(set(KAX) == set(REFX) and all(abs(KAX[k] - REFX[k]) <= 0.001 for k in REFX) and abs(float(np.median(list(KAX.values()))) - 1.095) <= 0.001))
P("KA-X RB1 X-COP f_ret (last radius, M_FORW, R 5.41): " + ", ".join(f"{k} {v:.3f}" for k, v in KAX.items()) + f"; median {KA['X']['median']:.3f} -> {'PASS' if KA['X']['ok'] else 'FAIL'}")
if not KA["X"]["ok"]: STOP.append("KA-X")
RES["known_answers"] = KA

def dump_out():
    with open(os.path.join(OUTD, "clr1.out"), "w") as f: f.write("\n".join(LINES) + "\n")
    with open(os.path.join(OUTD, "clr1.json"), "w") as f: json.dump(RES, f, indent=1, default=lambda x: None)
if STOP:
    P(); P(f"KNOWN-ANSWER FAILURE {STOP}: the lane stops before any word (criteria section 7)."); RES["word"] = {"stopped": STOP}; dump_out(); sys.exit(2)

# ================================================================== GRADED RUNS (footing frame)
P(); P("=" * 100); P("GRADED: per class median of per-cluster log10(M_dyn / M_pred) [95 % bootstrap]; OUTER = R500 (B anchor A1), MIDDLE = 0.1-0.5 R500, CORE = 20-30 kpc (B anchor A2)")
ROWS_SHOW = (("newton", "Newton baryons"), ("mond_rar", "Combes MOND (RAR 1.2e-10)"), ("law", "law only (footing a0)"), ("B", "FORM B (graded)"))
CENTRAL = {}
for f in FOOTS:
    R_ = run({}, FR_F[f], foot=f, keep=True); CENTRAL[f] = R_
    P(); P(f"---- footing {f}: h {FOOT_BG[f]['h']:.5f}; anchor solver max error {R_['anchor_err']:.1e}; grid points with M_dyn <= 0 (no hydrostatic solution): {R_['n_Mdyn_le0']}")
    for cl in CLASSES + ("All",):
        for rg in REG:
            k = f"{cl}|{rg}"; tag = " [DATA-INCONSISTENT]" if R_["stat"]["newton"][k]["data_inconsistent"] else ""
            P(f"  {cl:8s} {rg:6s}{tag}  " + " | ".join(f"{lab}: {fmt(R_['stat'][row][k])} {R_['stat'][row][k]['word']}" for row, lab in ROWS_SHOW))
    w, det = bword(R_["stat"]); R_["word"] = w; P(f"  ==> form B, footing {f}, central run: {w}")
RES["central"] = {f: dict(stat=CENTRAL[f]["stat"], word=CENTRAL[f]["word"], anchor_err=CENTRAL[f]["anchor_err"], n_Mdyn_le0=CENTRAL[f]["n_Mdyn_le0"],
                          per_cluster=[dict(name=q["name"], cls=q["cls"], R500_kpc=q["R500"], M500=q["M500"], Mvis500=q["Mv"], Mdyn500=q["Md"], Mgas500=q["Mg"], cells=q["cells"]) for q in CENTRAL[f]["percl"]]) for f in FOOTS}

# radial location (reported): per class median log Q in r/R500 bins and kpc bins, MOND and B (A2)
P(); P("RADIAL LOCATION (reported, canonical): class medians of log Q by radius; and the radius holding half of the positive MOND residual (Combes's delta M plateau)")
EDGES_X = [0.0, 0.05, 0.1, 0.2, 0.5, 1.01]; EDGES_K = [20, 30, 50, 100, 200, 500]
RL = {}
for cl in CLASSES:
    qs = [q for q in CENTRAL["canonical"]["percl"] if q["cls"] == cl]; RL[cl] = {}
    for row in ("mond_rar", "B_A2", "newton"):
        bx = [];
        for a, b in zip(EDGES_X[:-1], EDGES_X[1:]):
            v = [float(np.median(q["rw"][row][(q["p"]["r"] / q["R500"] >= a) & (q["p"]["r"] / q["R500"] < b)])) for q in qs if np.any((q["p"]["r"] / q["R500"] >= a) & (q["p"]["r"] / q["R500"] < b))]
            bx.append(float(np.median(v)) if v else float("nan"))
        bk = []
        for a, b in zip(EDGES_K[:-1], EDGES_K[1:]):
            v = [float(np.median(q["rw"][row][(q["p"]["r"] >= a) & (q["p"]["r"] < b)])) for q in qs if np.any((q["p"]["r"] >= a) & (q["p"]["r"] < b))]
            bk.append(float(np.median(v)) if v else float("nan"))
        RL[cl][row] = dict(x_bins=bx, kpc_bins=bk)
    rh = []
    for q in qs:
        p = q["p"]; Mm = M_of(invert(g_rar, g_of(p["Md"], p["r"]), A0C), p["r"]); dm = Mm - p["Mv"]; i = int(np.argmax(dm))
        if dm[i] > 0: rh.append(float(p["r"][np.argmax(dm[: i + 1] >= 0.5 * dm[i])]))
    RL[cl]["mond_half_residual_radius_kpc"] = dict(median=float(np.median(rh)) if rh else None, n=len(rh))
    P(f"  {cl:8s} r/R500 bins {EDGES_X}: MOND " + " ".join(f"{v:+.2f}" for v in RL[cl]['mond_rar']['x_bins']) + " | B(A2) " + " ".join(f"{v:+.2f}" for v in RL[cl]['B_A2']['x_bins']) + " | Newton " + " ".join(f"{v:+.2f}" for v in RL[cl]['newton']['x_bins']))
    P(f"  {cl:8s} kpc bins {EDGES_K}: MOND " + " ".join(f"{v:+.2f}" for v in RL[cl]['mond_rar']['kpc_bins']) + " | B(A2) " + " ".join(f"{v:+.2f}" for v in RL[cl]['B_A2']['kpc_bins']) + " | Newton " + " ".join(f"{v:+.2f}" for v in RL[cl]['newton']['kpc_bins']))
    P(f"           radius holding half the positive MOND residual (RAR delta M): median {RL[cl]['mond_half_residual_radius_kpc']['median']} kpc over {len(rh)} clusters")
RES["radial_location"] = RL

# ================================================================== BRACKETS
BR = {"H b0.1": dict(b=0.1), "H b0.2": dict(b=0.2), "S1 Re15": dict(Re=15.0), "S1 Re60": dict(Re=60.0), "S2 DeMaio x2": dict(dem=2.0), "S2 DeMaio /2": dict(dem=0.5),
      "S3 Giodini x1.5": dict(gio=1.5), "S3 Giodini /1.5": dict(gio=1 / 1.5), "S3 galaxies follow gas": dict(galprof="gas"), "G1 gas from n_center": dict(gas="ncenter"),
      "G2 single beta all": dict(single=True), "T1 T x0.9": dict(Tscale=0.9), "T1 T x1.1": dict(Tscale=1.1), "T2 T_m": dict(Tsrc="Tm"), "T3 isothermal": dict(cc_grad="off"),
      "T3 r_T = r_c": dict(rT="rc"), "T4 central 0.5 T_h": dict(Tc=0.5), "R 5.562": dict(R=R_BR), "N1 native inner slope": dict(inner="slope"), "P core PSF": dict(_psf=True)}
REP = {"Combes frame (h 0.5 EdS)": ("combes", {}), "h 0.7 Om 0.3": ("h07", {}), "NFW Duffy (EXTERNALLY CALIBRATED)": ("foot", dict(shape="nfw"))}
P(); P("=" * 100); P("BRACKETS (counted): B word per footing and every graded cell that changes")
BRES = {}
for f in FOOTS:
    BRES[f] = {}; base = CENTRAL[f]["stat"]["B"]
    for name, o in BR.items():
        oo = {k: v for k, v in o.items() if not k.startswith("_")}; R_ = run(oo, FR_F[f], foot=f, psf=o.get("_psf", False)); w, _ = bword(R_["stat"])
        ch = {f"{cl}|{rg}": R_["stat"]["B"][f"{cl}|{rg}"]["word"] + (" [DI]" if R_["stat"]["B"][f"{cl}|{rg}"]["data_inconsistent"] else "") for cl in CLASSES for rg in REG
              if (R_["stat"]["B"][f"{cl}|{rg}"]["word"], R_["stat"]["B"][f"{cl}|{rg}"]["data_inconsistent"]) != (base[f"{cl}|{rg}"]["word"], base[f"{cl}|{rg}"]["data_inconsistent"])}
        BRES[f][name] = dict(word=w, changed=ch, cells={k: dict(med=v["med"], lo=v["lo"], hi=v["hi"], word=v["word"], di=v["data_inconsistent"]) for k, v in R_["stat"]["B"].items()},
                             mond={k: dict(med=v["med"], word=v["word"]) for k, v in R_["stat"]["mond_rar"].items()})
        P(f"  [{f}] {name:28s} -> {w}" + (f"   changed: {ch}" if ch else ""))
RES["brackets"] = BRES
P(); P("REPORTED (not counted)")
REPR = {}
for name, (fr, o) in REP.items():
    frame = FR_C if fr == "combes" else (("foot", 0.7, 0.3) if fr == "h07" else FR_F["canonical"])
    R_ = run(o, frame, foot="canonical"); w, _ = bword(R_["stat"]); REPR[name] = dict(word=w, stat=R_["stat"])
    P(f"  {name}: B word {w}")
    for cl in CLASSES:
        P(f"     {cl:8s} " + " | ".join(f"{rg} B {fmt(R_['stat']['B'][f'{cl}|{rg}'])} {R_['stat']['B'][f'{cl}|{rg}']['word']}; MOND {R_['stat']['mond_rar'][f'{cl}|{rg}']['med']:+.3f}" for rg in REG))
# A1 inner and Combes simple function rows from the central run
for cl in CLASSES:
    s_ = CENTRAL["canonical"]["stat"]
    P(f"  A1 anchor in inner cells, canonical, {cl:8s}: MIDDLE {fmt(s_['B_A1'][f'{cl}|MIDDLE'])} {s_['B_A1'][f'{cl}|MIDDLE']['word']}; CORE {fmt(s_['B_A1'][f'{cl}|CORE'])} {s_['B_A1'][f'{cl}|CORE']['word']}"
      f"; Combes simple fn OUTER {fmt(s_['mond_simple_combes'][f'{cl}|OUTER'])}")
RES["reported"] = REPR

# X-COP overlap cross-check (reported): beta-model vs X-COP, h 0.7 Om 0.3
P(); P("X-COP OVERLAP (reported): median log10(beta-model / X-COP) at 0.3, 0.5, 1.0 R500(Ettori), h 0.7 Om 0.3, recipe M_dyn (CC gradient on) and M_gas")
ETT = json.load(open(os.path.join(XCOP_DIR, "xcop_r500_ettori2019.json")))
MAP = {"A85": "A0085", "A644": "A0644", "A1644": "A1644", "A1795": "A1795", "A2029": "A2029", "A2142": "A2142", "A2255": "A2255", "A2319": "A2319", "A3158": "A3158", "A3266": "A3266", "ZW1215": "ZwCl1215"}
XO = {}
for xn, cn in MAP.items():
    c = next(q for q in CL if q["name"] == cn); xc = XC[xn]; s = DA_flat(c["z"], 0.7, 0.3) / DA_eds50(c["z"]); R5 = ETT[xn]["R500"] * 1e3; rows_ = {}
    rr, cum = gas_table(c, {})
    for fx in (0.3, 0.5, 1.0):
        r = fx * R5; Mb = s * float(Mdyn_chen(c, np.array([r / s]), {})[0]); Mgb = s ** 2.5 * float(np.exp(np.interp(math.log(r / s), np.log(rr[1:]), np.log(cum[1:]))))
        Mx = float(x_interp_loglog(xc["h_r"], xc["h_M_FORW"], r)[0]); Mgx = float(x_interp_loglog(xc["g_r"], xc["g_m"], r)[0])
        rows_[fx] = (math.log10(Mb / Mx) if Mx > 0 and Mb > 0 else float("nan"), math.log10(Mgb / Mgx) if Mgx > 0 else float("nan"))
    XO[xn] = rows_
for fx in (0.3, 0.5, 1.0):
    a = [XO[k][fx][0] for k in XO if np.isfinite(XO[k][fx][0])]; g = [XO[k][fx][1] for k in XO if np.isfinite(XO[k][fx][1])]
    P(f"  r = {fx} R500: M_dyn median {np.median(a):+.3f} (n {len(a)}, range {min(a):+.2f} to {max(a):+.2f}); M_gas median {np.median(g):+.3f} (n {len(g)}, range {min(g):+.2f} to {max(g):+.2f})")
# Combes Table 2 analogue (reported, Combes frame): BCG+ICL overmassive = M_vis > M_dyn at 20 kpc; outer overmassive = M_vis > M_MOND(RAR) at R500
T2C = {cl: dict(bcg_over=0, outer_over=0, n=0) for cl in CLASSES}
for c in CL:
    p = build(c, {}, FR_C); Mm = M_of(invert(g_rar, g_of(p["Md"], p["r"]), A0C), p["r"]); t = T2C[c["cls"]]; t["n"] += 1
    t["bcg_over"] += int(p["Mv"][0] > p["Md"][0]); t["outer_over"] += int(p["Mv"][-1] > Mm[-1])
P("COMBES TABLE 2 ANALOGUE (reported, Combes frame): " + "; ".join(f"{cl}: n {v['n']}, visible above hydrostatic at 20 kpc {v['bcg_over']}, visible above M_MOND at R500 {v['outer_over']}" for cl, v in T2C.items())
  + "  [Combes: BCG+ICL overmassive 56 / 12 / 8; outer parts overmassive 8 / 7 / 6]")
RES["combes_table2_analogue"] = T2C
RES["xcop_overlap"] = {k: {str(fx): v for fx, v in d.items()} for k, d in XO.items()}

# ================================================================== WORD per footing
P(); P("=" * 100)
FINAL = {}
for f in FOOTS:
    w0 = CENTRAL[f]["word"]; bw = {n: BRES[f][n]["word"] for n in BR}; flips = {n: v for n, v in bw.items() if v != w0}
    nv = []
    for cl in CLASSES:
        for rg in REG:
            k = f"{cl}|{rg}"; ws = {BRES[f][n]["cells"][k]["word"].split(" (")[0] for n in BR if not BRES[f][n]["cells"][k]["di"]}
            if CENTRAL[f]["stat"]["B"][k]["word"].startswith("CLOSED") and "RESIDUAL REMAINS" in ws and "OVER-PREDICTS" in ws: nv.append(k)
    word = "NO VERDICT" if nv and not w0.startswith("STILL FAILS") else w0
    if flips: word += " FRAGILE"
    FINAL[f] = dict(word=word, central=w0, bracket_flips=flips, no_verdict_cells=nv)
    P(f"WORD [{f}]: {word}"); P(f"   brackets that change it: {flips if flips else 'none'}")
RES["word"] = FINAL; RES["seconds"] = time.time() - T0
dump_out()

# ================================================================== MUTATE and null twin
MR = {}
for f in ("canonical",):
    base = CENTRAL[f]["stat"]["B"]
    m1 = run(dict(stretch=3.0), FR_F[f], foot=f)["stat"]["B"]; d1 = {cl: abs(m1[f"{cl}|CORE"]["med"] - base[f"{cl}|CORE"]["med"]) for cl in CLASSES}
    MR["M1"] = dict(core_shift=d1, bites=all(v >= 0.10 for v in d1.values())); PM(f"M1 cold shape r x 3 (A2): CORE shifts {d1} -> {'BITES' if MR['M1']['bites'] else 'DOES NOT BITE (CORE = NO POWER for B)'}")
    m3 = run(dict(Rmult=2.0), FR_F[f], foot=f)["stat"]["B"]; d3 = {cl: abs(m3[f"{cl}|OUTER"]["med"] - base[f"{cl}|OUTER"]["med"]) for cl in CLASSES}
    MR["M3"] = dict(outer_shift=d3, bites=all(v >= 0.15 for v in d3.values())); PM(f"M3 R x 2 (A1): OUTER shifts {d3} -> {'BITES' if MR['M3']['bites'] else 'DOES NOT BITE'}")
okd = (KA["C"]["combes_frame"]["ok_def"] or ["D1"])[0]
m2 = combes_stats(FR_C, a0=1e-30)[f"{okd}_mean"]; MR["M2"] = dict(def_=okd, value=m2, bites=not (0.33 <= m2 <= 0.49)); PM(f"M2 Combes recipe with a0 -> 1e-30: <M_dark/M_MOND> ({okd}) = {m2:.3f} -> {'BITES' if MR['M2']['bites'] else 'DOES NOT BITE'}")
z1 = run(dict(ngrid=240), FR_F["canonical"], foot="canonical", seed=SEED + 1)["stat"]["B"]; base = CENTRAL["canonical"]["stat"]["B"]
dz = {k: abs(z1[k]["med"] - base[k]["med"]) for k in base if k.split("|")[0] in CLASSES}; wz = [k for k in dz if z1[k]["word"] != base[k]["word"]]
kz = max(dz, key=dz.get); MR["Z1"] = dict(max_shift=max(dz.values()), max_cell=kz, shifts=dz, word_changes=wz, quiet=max(dz.values()) < 0.01 and not wz)
PM(f"Z1 null (grid 240, seed 1115): max cell shift {max(dz.values()):.4f} in {kz}, word changes {wz} -> {'QUIET (as required)' if MR['Z1']['quiet'] else 'BITES (null twin fails)'}")
PM("    per-cell shifts: " + ", ".join(f"{k} {v:.4f}" for k, v in dz.items()))
a, b = CENTRAL["canonical"]["stat"]["B"], CENTRAL["alt"]["stat"]["B"]; dzz = max(abs(a[k]["med"] - b[k]["med"]) for k in a)
MR["Z2"] = dict(max_diff=dzz, quiet=dzz < 0.005); PM(f"Z2 null (canonical vs alt B rows): max diff {dzz:.5f} -> {'QUIET (as required)' if MR['Z2']['quiet'] else 'BITES'}")
with open(os.path.join(OUTD, "clr1_MUTATE.out"), "w") as f: f.write("\n".join(MLINES) + "\n")
with open(os.path.join(OUTD, "clr1_MUTATE.json"), "w") as f: json.dump(MR, f, indent=1, default=lambda x: None)
P(f"done in {time.time() - T0:.0f} s"); dump_out()
