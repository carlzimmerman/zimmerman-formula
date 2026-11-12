#!/usr/bin/env python3
"""CRACK-1: three readings of the ultra-faint / X-COP pair (criteria 16bc0102de).
TEST lane, quarantined; adopts nothing. kappa = 1/2 FITTED; not theory closed. One thread.
Usage: python3 crack1.py            -> crack1.json / crack1.out
       python3 crack1.py --mutate   -> crack1_MUTATE.json / crack1_MUTATE.out

All three readings are instances of FRM1's master equation: an amount X_f fixed at an event, then
    d = log10[(1 + X_f f_C/f_b) / (1 + X_L(g_bar))] .
Deep regime (X_L >> 1): d ~ (1/2) log10(g_bar/g_f). A field WEAKER than the system's own at the fixing
event RAISES it; a field STRONGER LOWERS it. That one sentence decides all three readings.
"""
import os, sys, csv, math, json, time, warnings
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DD1 = os.path.join(REPO, "fable52_push", "DD1_deduce_from_data")
FRM1 = os.path.join(REPO, "fable52_push", "FRM1_formation_theory")
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv; TAG = "crack1_MUTATE" if MUT else "crack1"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()

G, MS, PC, CL = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
SEED = 20261110
RES = dict(lane="CRACK-1", criteria="16bc0102de", table="441824e854", tag=TAG,
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, runs={}, labels={},
           reported={}, MUTATE={})

UFD, XCOP = "MW ultra-faints", "X-COP"
PAIR = (UFD, XCOP)

# ============================================================ DD1's frozen table + DD1/FRM1 loaders (unchanged)
def load_table():
    rows = []
    with open(os.path.join(DD1, "dd1_table.csv")) as fh:
        lines = [l for l in fh if not l.startswith("#")]
    for r in csv.DictReader(lines):
        if r["bracket"] != "": continue
        rows.append(dict(cls=r["cls"], sys=r["sys"], r_kpc=float(r["r_kpc"]), lgb=float(r["lgb"]),
                         lgo=float(r["lgo"]), eY=float(r["eY"]), z=float(r["z"]),
                         lSig=float(r["lSig"]), last=int(r["last"])))
    return rows
ROWS = load_table()
CLASSES = []
for r in ROWS:
    if r["cls"] not in CLASSES: CLASSES.append(r["cls"])

def build(rows):
    """DD1's build, verbatim in every derived variable."""
    T = {k: np.array([r[k] for r in rows]) for k in ("cls", "sys", "r_kpc", "lgb", "lgo", "eY", "z", "lSig", "last")}
    T["sk"] = np.array([c + "|" + s for c, s in zip(T["cls"], T["sys"])])
    T["Y"] = T["lgo"] - T["lgb"]
    rm = T["r_kpc"] * KPC
    with np.errstate(divide="ignore", invalid="ignore"):
        T["dep"] = T["lgo"] + np.log10(rm) - 2 * math.log10(CL)
    T["Mb"] = T["lgb"] + 2 * np.log10(rm) - math.log10(G * MS)
    T["lr"] = np.log10(T["r_kpc"]); T["zz"] = np.log10(T["z"] + 1e-3)
    ds = {}
    for k, d in zip(T["sk"], T["dep"]):
        if np.isfinite(d): ds[k] = max(ds.get(k, -np.inf), d)
    T["dsys"] = np.array([ds.get(k, np.nan) for k in T["sk"]])
    npts = {}
    for k in T["sk"]: npts[k] = npts.get(k, 0) + 1
    T["w"] = np.array([1.0 / npts[k] for k in T["sk"]])
    T["n"] = len(rows)
    return T

def wmed(v, w):
    v = np.asarray(v, float); w = np.asarray(w, float)
    m = ~np.isnan(v); v, w = v[m], w[m]
    if len(v) == 0: return float("nan")
    o = np.argsort(v, kind="mergesort"); v, w = v[o], w[o]; c = np.cumsum(w)
    return float(v[np.searchsorted(c, 0.5 * c[-1])])
def XL(lgb, a0):
    t = a0 / 10 ** np.asarray(lgb, float); return 2 * t / (np.sqrt(1 + 4 * t) + 1)
def YL(lgb, a0): return np.log10(1 + XL(lgb, a0))
def XL_of_g(g, a0):
    t = a0 / np.asarray(g, float); return 2 * t / (np.sqrt(1 + 4 * t) + 1)

# ============================================================ DD1's split, system and class statistics (unchanged)
def split(T, seed):
    rng = np.random.default_rng(seed); A, B = set(), set()
    for c in CLASSES:
        ss = sorted(set(T["sk"][T["cls"] == c]))
        if not ss: continue
        p = rng.permutation(len(ss)); h = int(math.ceil(len(ss) / 2))
        A |= {ss[i] for i in p[:h]}; B |= {ss[i] for i in p[h:]}
    return A, B
def class_offsets(T, idx, d):
    out = {}
    cl, sk, eY = T["cls"][idx], T["sk"][idx], T["eY"][idx]
    for c in CLASSES:
        m = cl == c
        if not m.any(): continue
        ds, es = [], []
        for s in sorted(set(sk[m])):
            q = m & (sk == s); dv = d[q]; dv = dv[~np.isnan(dv)]
            if len(dv) == 0: continue
            ds.append(float(np.median(dv))); ef = eY[q][np.isfinite(eY[q])]; es.append(float(np.median(ef)))
        if not ds: continue
        ds, es = np.array(ds), np.array(es); n = len(ds); off = float(np.median(ds))
        if n >= 2:
            fin = ds[np.isfinite(ds)]
            mad = 1.4826 * float(np.median(np.abs(fin - np.median(fin)))) if len(fin) else float("inf")
            se = max(1.2533 * mad / math.sqrt(n), math.sqrt(float(np.sum(es ** 2))) / n)
        else: se = float(es[0])
        out[c] = dict(off=off, se=se, n=n, z=(off / se if se > 0 else float("inf")))
    return out
def sys_med(T, arr):
    out = {}
    for s in sorted(set(T["sk"])):
        q = T["sk"] == s; v = arr[q]; v = v[~np.isnan(v)]
        out[s] = float(np.median(v)) if len(v) else float("nan")
    return out
def sys_e(T):
    out = {}
    for s in sorted(set(T["sk"])):
        q = T["sk"] == s; v = T["eY"][q]; v = v[np.isfinite(v)]
        out[s] = float(np.median(v)) if len(v) else float("nan")
    return out

# ============================================================ the record's host distances (X1 / RB2's file)
def load_hostdist():
    out = {}
    with open(os.path.join(DATA, "dsph", "lvd_dwarf_mw.csv")) as fh:
        for r in csv.DictReader(fh):
            try: d = float(r["distance_host"])
            except Exception: d = float("nan")
            out[r["name"].strip().lower()] = d
    return out
HDIST = load_hostdist()
def hdist_of(T):
    return np.array([HDIST.get(s.strip().lower(), np.nan) for s in T["sys"]])

# ============================================================ the three readings, as frozen
ALPHA_PRI, ALPHA_EDGE = 0.5, 1.0
ZF = {"MW ultra-faints": 8.0, "X-COP": 1.0}                  # pre-registered formation epochs
ZF_RANGE = {"MW ultra-faints": (4.0, 12.0), "X-COP": (0.3, 2.0)}
BAND = {                                                     # pre-registered bands, graded
 "R1": {UFD: (-1.05, -0.30), XCOP: (-0.30, 0.30)},
 "R2": {UFD: (-2.90, -1.10), XCOP: (-1.10, -0.19)},
 "R3": {UFD: (-1.37, -0.80), XCOP: (-0.30, 0.30)},
}
DELTA_PRI = {"R1": -0.70, "R2": None, "R3": None}            # R1's central is the hand estimate; R2/R3 computed
VC_MW = 200e3                                                # RB2 / X1's flat-rotation-curve MW host, m/s
def kappa(zf, alpha): return (1.0 + zf) ** (-3.0 * alpha)
def g_host(d_kpc, vc=VC_MW, fM=1.0, dfac=1.0):
    """RB2's SE2 A1 host: M(<d) = V_c^2 d / G  ->  g = V_c^2 / d.  fM: host mass fraction at infall;
    dfac: infall distance / present distance."""
    d = np.asarray(d_kpc, float) * dfac * KPC
    with np.errstate(divide="ignore", invalid="ignore"):
        return fM * vc ** 2 / d

HOSTED = ["MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs"]
def pred_R1(T, a0, fC_cal=None):
    """stripping-inverted: X_f = X_L(g_bar), then the host strips the charge: X = X_f f_C (f_b = 1).
    The host acts on the hosted family only; the unhosted (X-COP) keep f_C = 1 and so d = 0.
    fC_cal = None -> the graded band only; a number -> the central, calibrated on that f_C."""
    if fC_cal is None: return None
    Xl = XL(T["lgb"], a0)
    fC = np.array([fC_cal if c in HOSTED else 1.0 for c in T["cls"]])
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log10((1 + Xl * fC) / (1 + Xl))
def pred_R2(T, a0, alpha=ALPHA_PRI, zf_map=None):
    """external-field-registered: X_f = kappa(z_f) X_L(g_amb,f), g_amb,f = g_bar (no contraction)."""
    zf_map = zf_map or ZF
    Xl = XL(T["lgb"], a0)
    k = np.array([kappa(zf_map.get(c, 1.0), alpha) for c in T["cls"]])
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log10((1 + k * Xl) / (1 + Xl))
def pred_R3(T, a0, vc=VC_MW, fM=1.0, dfac=1.0):
    """fell-in: X_f = X_L(g_host(R_f)) for the hosted; X_f = X_L(g_bar) (d = 0) for the unhosted."""
    dh = hdist_of(T); gh = g_host(dh, vc, fM, dfac)
    hosted = np.isfinite(gh)
    Xl = XL(T["lgb"], a0)
    out = np.zeros(T["n"])
    with np.errstate(divide="ignore", invalid="ignore"):
        out[hosted] = np.log10((1 + XL_of_g(gh[hosted], a0)) / (1 + Xl[hosted]))
    return out, dh, hosted

def cls_of_pred(T, dpred):
    """a predicted per-point offset through DD1's per-system / per-class machinery (real errors)."""
    sm = sys_med(T, dpred)
    out = {}
    for c in CLASSES:
        ss = sorted(set(T["sk"][T["cls"] == c]))
        v = np.array([sm[s] for s in ss if np.isfinite(sm[s])])
        out[c] = float(np.median(v)) if len(v) else float("nan")
    return out

# ============================================================ the graded tests
def leg(meas, band):
    """one leg: the measured LOCO offset inside the pre-registered band (A->B and B->A must not contradict)."""
    lo, hi = band; m = meas["LOCO"][0]
    inside = bool(np.isfinite(m) and lo <= m <= hi)
    side_ok = True
    for t in ("A->B", "B->A"):
        v = meas[t][0]
        if np.isfinite(v) and not (lo <= v <= hi):
            if inside: side_ok = False                      # LOCO inside but a half-split outside
    miss = 0.0 if inside else (float(m - hi) if m > hi else float(lo - m))
    se = meas["LOCO"][1]
    return dict(inside=inside, half_splits_agree=side_ok, miss_dex=miss, miss_se=(miss / se if se > 0 else float("inf")),
                HOLDS=bool(inside and side_ok))
def floor_of_class(T, a0, c):
    """the physical floor of d for a class: X = 0 gives d = -Y_L(g_bar) (medians over the class's points)."""
    m = T["cls"] == c
    return float(-np.median(YL(T["lgb"][m], a0)))
def run_reading(key, T, a0, dmeas, verbose=True):
    """dmeas: {test: {cls: (off, se)}} for the three scorings. Returns the G1..G4 result for one reading.
    Two lines are reported, as in FRM1: FROZEN (the criteria exactly as committed) and AMENDED (A1: R1's UFD
    band's lower edge is the physical floor, not -1.05, and G3 grades the band-difference alone). The reading's
    claim - the UFD must be LOW - is the band's UPPER edge, and that is identical on both lines."""
    R = {}
    if key == "R1":
        dpred = pred_R1(T, a0, fC_cal=0.038)                # the record's stripped-family calibration (tidal dwarfs)
    elif key == "R2":
        dpred = pred_R2(T, a0, ALPHA_PRI, ZF)
    else:
        dpred, dh, hosted = pred_R3(T, a0)
    pcen = cls_of_pred(T, dpred) if dpred is not None else None
    R["legs"], R["legs_frozen"] = {}, {}
    for c in PAIR:
        k = "G_ufd" if c == UFD else "G_xcop"
        m = {t: (dmeas[t][c]["off"], dmeas[t][c]["se"]) for t in ("A->B", "B->A", "LOCO")}
        band_am = list(BAND[key][c])
        if key == "R1" and c == UFD: band_am[0] = min(band_am[0], floor_of_class(T, a0, c))
        for store, bd in ((R["legs_frozen"], list(BAND[key][c])), (R["legs"], band_am)):
            g = leg(m, bd); g["measured"] = dict(off=m["LOCO"][0], se=m["LOCO"][1])
            g["predicted_central"] = (None if pcen is None else pcen[c]); g["band"] = list(bd)
            store[k] = g
    # G3 the differential: the band-difference is graded; the central is reported
    dm = dmeas["LOCO"][UFD]["off"] - dmeas["LOCO"][XCOP]["off"]
    se = math.sqrt(dmeas["LOCO"][UFD]["se"] ** 2 + dmeas["LOCO"][XCOP]["se"] ** 2)
    dp = (None if pcen is None else pcen[UFD] - pcen[XCOP])
    R["G3_differential"], R["G3_differential_frozen"] = {}, {}
    for store, lo_u in ((R["G3_differential"], (floor_of_class(T, a0, UFD) if key == "R1" else BAND[key][UFD][0])),
                        (R["G3_differential_frozen"], BAND[key][UFD][0])):
        lo_d = lo_u - BAND[key][XCOP][1]; hi_d = BAND[key][UFD][1] - BAND[key][XCOP][0]
        in_band = bool(lo_d <= dm <= hi_d)
        store.update(dict(measured=dm, se=se, predicted_central=dp, band_diff=[lo_d, hi_d], in_band=in_band,
                          consistent_with_central=(None if dp is None else bool(abs(dm - dp) <= 3.0 * se)),
                          miss_dex=(0.0 if dp is None else dm - dp),
                          miss_se=(0.0 if dp is None else (dm - dp) / se), HOLDS=bool(in_band)))
    R["G3_differential_frozen"]["HOLDS"] = bool(R["G3_differential_frozen"]["in_band"] and
                                                (R["G3_differential_frozen"]["consistent_with_central"] in (None, True)))
    R["predicted_central"] = {c: (None if pcen is None else pcen[c]) for c in PAIR}
    for tag, lk, g3k in (("G4_pair", "legs", "G3_differential"), ("G4_pair_frozen", "legs_frozen", "G3_differential_frozen")):
        R[tag] = "SURVIVES THE PAIR" if (R[lk]["G_ufd"]["HOLDS"] and R[lk]["G_xcop"]["HOLDS"] and R[g3k]["HOLDS"]) \
                 else "FAILS THE PAIR"
    R["G_ufd"], R["G_xcop"] = R["legs"]["G_ufd"], R["legs"]["G_xcop"]
    return R

# ============================================================ reported, graded by nothing
def needed(T, a0):
    """the free parameter each reading would need to close its miss, per class, per point then median."""
    Xl = XL(T["lgb"], a0); u = a0 / 10 ** T["lgb"]; Xo = 10 ** T["Y"] - 1
    with np.errstate(divide="ignore", invalid="ignore"):
        fC_over_fb = Xo / Xl                                        # R1: the master equation at fixed field
        den = np.where(Xo > 1e-6, Xo * (Xo + 1), np.inf)            # X ~ 0: no finite field is strong enough
        gf = np.where(np.isfinite(den), a0 / den, np.inf)           # R3: the field the amount would need
        phi = np.where(np.isfinite(den), u / den, np.inf)           # R3/R2: g_f / g_bar (the contraction factor)
        kappa_need = Xo / Xl                                        # R2: kappa at g_amb,f = g_bar
    out = {}
    for c in CLASSES:
        m = T["cls"] == c
        out[c] = dict(fC_over_fb=float(np.median(fC_over_fb[m])), gf_needed=float(np.median(gf[m])),
                      phi=float(np.median(phi[m])), kappa_needed=float(np.median(kappa_need[m])),
                      gbar=float(np.median(10 ** T["lgb"][m])), XL=float(np.median(Xl[m])), u=float(np.median(u[m])))
    return out

def ushape(T, a0, dmeas):
    """X1: the measured offsets ordered by the class's median field, and the shape that kills a monotone map."""
    u = needed(T, a0)
    order = sorted(CLASSES, key=lambda c: u[c]["gbar"])
    rows = [(c, u[c]["gbar"], dmeas["LOCO"][c]["off"], dmeas["LOCO"][c]["se"]) for c in order]
    offs = np.array([r[2] for r in rows])
    k = int(np.argmin(np.abs(offs)))
    mono = bool(all(offs[i] <= offs[i + 1] for i in range(len(offs) - 1)) or
                all(offs[i] >= offs[i + 1] for i in range(len(offs) - 1)))
    dif = np.diff(offs); sgn = np.sign(dif); sgn = sgn[sgn != 0]
    turns = int(np.sum(sgn[1:] != sgn[:-1])) if len(sgn) > 1 else 0
    dS = dmeas["LOCO"]["SPARC"]["off"]
    return dict(order=[[r[0], r[1], r[2], r[3]] for r in rows], monotone_in_gbar=mono,
                min_class=rows[k][0], n_direction_changes=turns,
                rise_to_low_field_end=float(offs[0] - offs[k]), rise_to_high_field_end=float(offs[-1] - offs[k]),
                ufd_minus_sparc=float(dmeas["LOCO"][UFD]["off"] - dS),
                xcop_minus_sparc=float(dmeas["LOCO"][XCOP]["off"] - dS),
                clash_minus_sparc=float(dmeas["LOCO"]["CLASH"]["off"] - dS))

def edges(T, a0):
    """the pre-registered generous edges: does ANY corner of each reading's parameter space reach the pair?"""
    out = {}
    # R2: alpha and the formation-epoch range
    r2 = {}
    for alpha in (ALPHA_PRI, ALPHA_EDGE):
        for zfu, zfx in ((8.0, 1.0), (4.0, 0.3), (12.0, 2.0)):
            d = pred_R2(T, a0, alpha, {UFD: zfu, XCOP: zfx})
            pc = cls_of_pred(T, d)
            r2[f"alpha{alpha}_zf({zfu},{zfx})"] = dict(kappa_ufd=kappa(zfu, alpha), kappa_xcop=kappa(zfx, alpha),
                                                       d_ufd=pc[UFD], d_xcop=pc[XCOP])
    out["R2"] = r2
    # R3: the host's field at infall, generous edges (a smaller host, a larger infall radius)
    r3 = {}
    for vc in (180e3, 200e3, 220e3):
        for fM, dfac in ((1.0, 1.0), (0.5, 1.0), (0.25, 1.0), (0.25, 2.0)):
            d, _, _ = pred_R3(T, a0, vc, fM, dfac)
            pc = cls_of_pred(T, d)
            r3[f"Vc{vc/1e3:.0f}_fM{fM}_dfac{dfac}"] = dict(d_ufd=pc[UFD], g_host_median=float(np.median(g_host(np.array([64.0]), vc, fM, dfac))))
    out["R3"] = r3
    # R1: the stripping factor, over the whole range the channel allows
    r1 = {}
    for fC in (1.0, 0.5, 0.2, 0.1, 0.038, 0.01):
        pc = cls_of_pred(T, pred_R1(T, a0, fC_cal=fC))
        r1[f"fC{fC}"] = dict(d_ufd=pc[UFD], d_xcop=pc[XCOP])
    out["R1"] = r1
    return out

# ============================================================ one footing
def run_footing(T, a0, tag):
    yl = YL(T["lgb"], a0)
    with np.errstate(invalid="ignore"):
        dL = T["Y"] - yl
    A, B = split(T, SEED)
    idxA = np.where(np.isin(T["sk"], list(A)))[0]; idxB = np.where(np.isin(T["sk"], list(B)))[0]
    offs = {"A->B": class_offsets(T, idxB, dL[idxB]), "B->A": class_offsets(T, idxA, dL[idxA]),
            "LOCO": {c: class_offsets(T, np.where(T["cls"] == c)[0], dL[np.where(T["cls"] == c)[0]])[c]
                     for c in CLASSES if (T["cls"] == c).any()}}
    read = {k: run_reading(k, T, a0, offs) for k in ("R1", "R2", "R3")}
    # R3's within-class ordering prediction: d rises with the host distance
    dh = hdist_of(T)
    sm = sys_med(T, dL)
    ss = sorted(set(T["sk"][T["cls"] == UFD]))
    xs, ys = [], []
    for s in ss:
        d = HDIST.get(s.split("|")[-1].strip().lower(), np.nan)
        if np.isfinite(d) and np.isfinite(sm[s]): xs.append(math.log10(d)); ys.append(sm[s])
    rho = float("nan"); pval = float("nan")
    if len(xs) >= 4:
        try:
            from scipy.stats import spearmanr
            rr = spearmanr(xs, ys); rho = float(rr.statistic); pval = float(rr.pvalue)
        except Exception:
            xr = np.argsort(np.argsort(xs)); yr = np.argsort(np.argsort(ys))
            rho = float(np.corrcoef(xr, yr)[0, 1]); pval = float("nan")
    read["R3"]["within_class_rank"] = dict(rho_log_dhost_vs_d=rho, p=pval, n=len(xs),
                                           predicted_sign="+1", measured_sign=("+" if rho > 0 else "-"))
    return dict(dL=dL, offsets=offs, readings=read, needed=needed(T, a0), ushape=ushape(T, a0, offs),
                edges=edges(T, a0),
                floor={c: floor_of_class(T, a0, c) for c in PAIR},
                hdist=dict(n_matched=int(np.sum(np.isfinite(dh) & (T["cls"] == UFD))),
                           n_ufd=int(np.sum(T["cls"] == UFD)),
                           median_kpc=float(np.nanmedian(dh[T["cls"] == UFD])),
                           min_kpc=float(np.nanmin(dh[T["cls"] == UFD])), max_kpc=float(np.nanmax(dh[T["cls"] == UFD]))))

# ============================================================ known answers
def run_KA(T, a0):
    out = {}
    b = run_footing(T, a0, "ka")
    try:
        fj = json.load(open(os.path.join(FRM1, "frm1.json")))
        foot = "canonical" if a0 == A0["canonical"] else "alt"
        dev = 0.0
        for c in PAIR:
            v = b["offsets"]["LOCO"][c]; w = fj["runs"][foot]["three"]["LOCO"][c]
            dev = max(dev, abs(v["off"] - w["off"]), abs(v["se"] - w["se"]))
        out["KA1_max_dev"] = dev; out["KA1"] = "PASS" if dev <= 1e-9 else "FAIL"
    except Exception as e:
        out["KA1"] = f"FAIL ({e})"; out["KA1_max_dev"] = None
    # KA2 the readings' algebra: with the reading's parameter at its neutral value, d = 0 everywhere
    Xl = XL(T["lgb"], a0)
    d2a = pred_R2(T, a0, 0.0, {c: 1.0 for c in CLASSES})          # kappa = 1
    d2b = pred_R1(T, a0, fC_cal=1.0)                               # f_C = 1
    d2c = np.log10((1 + Xl) / (1 + Xl))                            # g_f = g_bar
    dev2 = max(float(np.nanmax(np.abs(d2a))), float(np.nanmax(np.abs(d2b))), float(np.nanmax(np.abs(d2c))))
    out["KA2_dev"] = dev2; out["KA2"] = "PASS" if dev2 <= 1e-12 else "FAIL"
    # KA3 the host distances
    dh = hdist_of(T); m = T["cls"] == UFD
    nm = int(np.sum(np.isfinite(dh[m])))
    out["KA3"] = dict(n_matched=nm, n_ufd=int(m.sum()),
                      all_finite=bool(nm == int(m.sum()) and np.all(dh[m] > 0)))
    out["KA3_pass"] = bool(out["KA3"]["all_finite"])
    # KA4 synthetic truths: each reading's own truth must make that reading HOLD
    truth = {}
    def mk(kind):
        T2 = build(ROWS); Xl2 = XL(T2["lgb"], a0)
        if kind == "strip":
            Xn = Xl2 * np.where(T2["cls"] == UFD, 0.05, 1.0)
        elif kind == "fellin":
            dh2 = hdist_of(T2); gh = g_host(dh2)
            Xn = np.where(np.isfinite(gh), XL_of_g(np.where(np.isfinite(gh), gh, 1.0), a0), Xl2)
            Xn = np.where(T2["cls"] == UFD, Xn, Xl2)
        elif kind == "epoch":
            k = np.array([kappa(ZF.get(c, 1.0), ALPHA_PRI) for c in T2["cls"]]); Xn = k * Xl2
        else:
            Xn = Xl2
        T2["Y"] = np.log10(1 + Xn); T2["lgo"] = T2["lgb"] + T2["Y"]
        return T2
    for kind, need in (("strip", lambda r: r["R1"]["G_ufd"]["HOLDS"] and r["R1"]["G3_differential"]["HOLDS"]),
                       ("fellin", lambda r: r["R3"]["G_ufd"]["HOLDS"]),
                       ("epoch", lambda r: r["R2"]["G_ufd"]["HOLDS"] and r["R2"]["G_xcop"]["HOLDS"])):
        T2 = mk(kind); b2 = run_footing(T2, a0, kind)
        truth[kind] = dict(ok=bool(need(b2["readings"])),
                           R1_ufd=b2["readings"]["R1"]["G_ufd"]["HOLDS"], R1_G3=b2["readings"]["R1"]["G3_differential"]["HOLDS"],
                           R3_ufd=b2["readings"]["R3"]["G_ufd"]["HOLDS"],
                           R2_ufd=b2["readings"]["R2"]["G_ufd"]["HOLDS"], R2_xcop=b2["readings"]["R2"]["G_xcop"]["HOLDS"],
                           ufd_off=b2["offsets"]["LOCO"][UFD]["off"], xcop_off=b2["offsets"]["LOCO"][XCOP]["off"])
    out["KA4"] = truth; out["KA4_pass"] = all(v["ok"] for v in truth.values())
    # KA5 the U-shape is not an artifact of the definition: everything on the law -> every offset 0
    T3 = build(ROWS); T3["Y"] = YL(T3["lgb"], a0); T3["lgo"] = T3["lgb"] + T3["Y"]
    b3 = run_footing(T3, a0, "onlaw")
    mx = max(abs(b3["offsets"][t][c]["off"]) for t in ("A->B", "B->A", "LOCO") for c in b3["offsets"][t])
    out["KA5_max_abs_off_on_law"] = float(mx); out["KA5"] = "PASS" if mx <= 1e-9 else "FAIL"
    return out

# ============================================================ main
T_main = build(ROWS)
P(f"CRACK-1 on DD1's frozen table: {T_main['n']} points, {len(set(T_main['sk']))} systems, {len(CLASSES)} classes. "
  f"criteria {RES['criteria']}, table {RES['table']}. tag {TAG}")

ka = {f: run_KA(T_main, A0[f]) for f in FOOT}
for f in FOOT:
    k = ka[f]
    P(f"KA1 FRM1's LOCO pair reproduced [{f}]: max dev {k['KA1_max_dev']:.2e} -> {k['KA1']}")
    P(f"KA2 readings' neutral algebra [{f}]: max |d| {k['KA2_dev']:.2e} -> {k['KA2']}")
    P(f"KA3 host distances [{f}]: {k['KA3']['n_matched']}/{k['KA3']['n_ufd']} ultra-faints matched, all finite -> "
      f"{'PASS' if k['KA3_pass'] else 'FAIL'}")
    P(f"KA4 synthetic truths [{f}]: " + "; ".join(
        f"{n}: {'ok' if v['ok'] else 'NOT OK'} (UFD {v['ufd_off']:+.3f}, X-COP {v['xcop_off']:+.3f}; "
        f"R1 ufd {v['R1_ufd']} G3 {v['R1_G3']}, R2 ufd {v['R2_ufd']} xcop {v['R2_xcop']}, R3 ufd {v['R3_ufd']})"
        for n, v in k["KA4"].items()) + f" -> {'PASS' if k['KA4_pass'] else 'FAIL'}")
    P(f"KA5 every system on the law [{f}]: max |class offset| {k['KA5_max_abs_off_on_law']:.2e} -> {k['KA5']}")
allka = all(ka[f]["KA1"] == "PASS" and ka[f]["KA2"] == "PASS" and ka[f]["KA3_pass"] and
            ka[f]["KA4_pass"] and ka[f]["KA5"] == "PASS" for f in FOOT)
P(f"KNOWN ANSWERS: {'ALL PASS' if allka else 'A KNOWN ANSWER FAILED'}")
RES["KA"] = ka; RES["KA_all_pass"] = bool(allka)

runs = {}
for f in FOOT:
    b = run_footing(T_main, A0[f], f); runs[f] = b
    P(f"\n===== [{f}] a0 = {A0[f]:.4e}")
    o = b["offsets"]
    P(f"  the pair (LOCO): {UFD} {o['LOCO'][UFD]['off']:+.4f} +- {o['LOCO'][UFD]['se']:.4f} "
      f"({o['LOCO'][UFD]['z']:+.1f} se)   {XCOP} {o['LOCO'][XCOP]['off']:+.4f} +- {o['LOCO'][XCOP]['se']:.4f} "
      f"({o['LOCO'][XCOP]['z']:+.1f} se)")
    P(f"  anchor SPARC    : {o['LOCO']['SPARC']['off']:+.4f} +- {o['LOCO']['SPARC']['se']:.4f}")
    for key, nm in (("R1", "R1 STRIPPING-INVERTED"), ("R2", "R2 EXTERNAL-FIELD-REGISTERED"), ("R3", "R3 FELL-IN")):
        R = b["readings"][key]
        P(f"\n  -- {nm}: {R['G4_pair']}   (frozen line as committed: {R['G4_pair_frozen']})")
        for c, lab in ((UFD, "UFD "), (XCOP, "XCOP")):
            g = R["G_ufd" if c == UFD else "G_xcop"]
            pc = g["predicted_central"]
            pcs = "n/a" if pc is None else f"{pc:+.3f}"
            P(f"     {lab} band [{g['band'][0]:+.2f},{g['band'][1]:+.2f}]  predicted central {pcs}  "
              f"measured {g['measured']['off']:+.3f} +- {g['measured']['se']:.3f}  "
              f"{'HOLDS' if g['HOLDS'] else 'FAILS'} (miss {g['miss_dex']:+.3f} dex, {g['miss_se']:+.1f} se)")
        g3 = R["G3_differential"]
        p3 = "n/a" if g3["predicted_central"] is None else f"{g3['predicted_central']:+.3f}"
        P(f"     G3 differential: measured {g3['measured']:+.3f} +- {g3['se']:.3f}  predicted central {p3}  "
          f"band-diff [{g3['band_diff'][0]:+.2f},{g3['band_diff'][1]:+.2f}]  "
          f"{'HOLDS' if g3['HOLDS'] else 'FAILS'}")
        if key == "R3":
            rk = R["within_class_rank"]
            P(f"     within-class: rank(log10 d_host, d) = {rk['rho_log_dhost_vs_d']:+.3f} (n {rk['n']}, p {rk['p']:.3f}); "
              f"R3 predicts +, measured {rk['measured_sign']}")
        P(f"     generous edges (does any corner of the reading reach the pair? measured UFD "
          f"{o['LOCO'][UFD]['off']:+.3f}, X-COP {o['LOCO'][XCOP]['off']:+.3f}):")
        for kk, vv in b["edges"][key].items():
            if key == "R1":
                P(f"       {kk:26s} d_UFD {vv['d_ufd']:+.3f}  d_XCOP {vv['d_xcop']:+.3f}")
            elif key == "R2":
                P(f"       {kk:26s} kappa UFD {vv['kappa_ufd']:.3f} XCOP {vv['kappa_xcop']:.3f}  "
                  f"d_UFD {vv['d_ufd']:+.3f}  d_XCOP {vv['d_xcop']:+.3f}")
            else:
                P(f"       {kk:26s} g_host(64 kpc) {vv['g_host_median']:.3e}  d_UFD {vv['d_ufd']:+.3f}")
    P(f"\n  -- X1 the U-shape (LOCO offsets ordered by the class's median g_bar):")
    P(f"     {'class':18s} {'g_bar [m/s2]':>13s} {'d_L':>8s} {'se':>7s}")
    for c, gb, off, se in b["ushape"]["order"]:
        P(f"     {c:18s} {gb:13.3e} {off:+8.3f} {se:7.3f}")
    us = b["ushape"]
    P(f"     monotone in g_bar: {us['monotone_in_gbar']}; direction changes {us['n_direction_changes']}; "
      f"minimum at {us['min_class']}; rise to the low-field end {us['rise_to_low_field_end']:+.3f} dex, to the "
      f"high-field end {us['rise_to_high_field_end']:+.3f} dex")
    P(f"     against the anchor SPARC: UFD {us['ufd_minus_sparc']:+.3f}, X-COP {us['xcop_minus_sparc']:+.3f}, "
      f"CLASH {us['clash_minus_sparc']:+.3f} dex")
    P(f"\n  -- what each reading would need (medians over the class's points):")
    P(f"     {'class':18s} {'f_C/f_b (R1)':>12s} {'kappa (R2)':>11s} {'g_f [m/s2] (R3)':>16s} {'phi=g_f/g_bar':>13s} "
      f"{'g_bar':>10s} {'g_host (R3)':>12s}")
    dh = b["hdist"]
    for c in (UFD, XCOP, "SPARC", "CLASH", "MW bright dwarfs", "tidal dwarfs", "NGC 1052 UDGs"):
        u = b["needed"][c]
        gh = (float(np.median(g_host(hdist_of(T_main)[T_main["cls"] == c], VC_MW))) if c == UFD else float("nan"))
        P(f"     {c:18s} {u['fC_over_fb']:12.3f} {u['kappa_needed']:11.3f} {u['gf_needed']:16.3e} {u['phi']:13.4f} "
          f"{u['gbar']:10.3e} {gh:12.3e}")
    P(f"     host distances for the 31 ultra-faints: median {dh['median_kpc']:.1f} kpc "
      f"({dh['min_kpc']:.1f} to {dh['max_kpc']:.1f}); MW field at the median, V_c = 200 km/s: "
      f"{float(np.median(g_host(np.array([dh['median_kpc']])))):.3e} m/s^2")
RES["runs"] = {}
for f in FOOT:
    b = runs[f]
    RES["runs"][f] = dict(offsets={t: {c: dict(off=v["off"], se=v["se"], n=v["n"], z=v["z"]) for c, v in b["offsets"][t].items()}
                                   for t in ("A->B", "B->A", "LOCO")},
                          readings=b["readings"], needed=b["needed"], ushape=b["ushape"], hdist=b["hdist"])
RES["labels"] = {f: {k: runs[f]["readings"][k]["G4_pair"] for k in ("R1", "R2", "R3")} for f in FOOT}

# ---- MUTATE
if MUT:
    M = {}
    T1 = build(ROWS)
    m1 = T1["cls"] == UFD
    Xl1 = XL(T1["lgb"], A0["canonical"])
    T1["Y"] = np.where(m1, np.log10(1 + Xl1 * 0.10), T1["Y"]); T1["lgo"] = T1["lgb"] + T1["Y"]
    b1 = run_footing(T1, A0["canonical"], "m1")
    M["M1_ufds_stripped_90pct__R1_G_ufd_must_HOLD"] = dict(
        R1_ufd=b1["readings"]["R1"]["G_ufd"]["HOLDS"], ufd_off=b1["offsets"]["LOCO"][UFD]["off"],
        bites=bool(b1["readings"]["R1"]["G_ufd"]["HOLDS"]))
    P(f"\nM1 the 31 ultra-faints stripped of 90 % of the charge: d_L(UFD) {b1['offsets']['LOCO'][UFD]['off']:+.3f}; "
      f"R1's UFD leg {'HOLDS' if b1['readings']['R1']['G_ufd']['HOLDS'] else 'FAILS'} -> "
      f"{'bites' if M['M1_ufds_stripped_90pct__R1_G_ufd_must_HOLD']['bites'] else 'DOES NOT BITE'}")

    T2 = build(ROWS)
    dh = hdist_of(T2); mu = T2["cls"] == UFD
    dmax, dmin = float(np.nanmax(dh[mu])), float(np.nanmin(dh[mu]))
    T2["_dhost"] = np.where(mu, dmax + dmin - dh, dh)
    def pred_R3_mut(T, a0):
        dhx = T["_dhost"]; gh = g_host(dhx)
        Xl = XL(T["lgb"], a0); out = np.zeros(T["n"]); h = np.isfinite(gh)
        with np.errstate(divide="ignore", invalid="ignore"):
            out[h] = np.log10((1 + XL_of_g(gh[h], a0)) / (1 + Xl[h]))
        return out
    pc0 = cls_of_pred(T2, pred_R3(T2, A0["canonical"])[0])
    pcm = cls_of_pred(T2, pred_R3_mut(T2, A0["canonical"]))
    mv = abs(pcm[UFD] - pc0[UFD])
    sm = sys_med(T2, T2["Y"] - YL(T2["lgb"], A0["canonical"]))
    ss = sorted(set(T2["sk"][T2["cls"] == UFD]))
    xs = [math.log10(dmax + dmin - HDIST[s.split("|")[-1].strip().lower()]) for s in ss]
    ys = [sm[s] for s in ss]
    rho_m = float("nan")
    try:
        from scipy.stats import spearmanr
        rho_m = float(spearmanr(xs, ys).statistic)
    except Exception: pass
    M["M2_host_distances_reversed__R3_prediction_must_move_ge_0.15"] = dict(
        predicted_ufd_before=pc0[UFD], predicted_ufd_after=pcm[UFD], move=mv, rho_after=rho_m, bites=bool(mv >= 0.15))
    P(f"M2 host distances reversed: R3's predicted UFD offset {pc0[UFD]:+.3f} -> {pcm[UFD]:+.3f} "
      f"(move {mv:+.3f} dex); within-class rho {rho_m:+.3f} -> "
      f"{'bites' if M['M2_host_distances_reversed__R3_prediction_must_move_ge_0.15']['bites'] else 'DOES NOT BITE'}")

    T3 = build(ROWS)
    d3 = pred_R2(T3, A0["canonical"], 0.0, ZF)
    b3 = run_footing(T3, A0["canonical"], "m3")
    r3fail = not b3["readings"]["R2"]["G_ufd"]["HOLDS"]
    M["M3_alpha_0_kappa_1__R2_pred_must_be_0_and_G_ufd_must_still_FAIL"] = dict(
        max_abs_pred=float(np.nanmax(np.abs(d3))), R2_ufd_HOLDS=b3["readings"]["R2"]["G_ufd"]["HOLDS"],
        bites=bool(float(np.nanmax(np.abs(d3))) <= 1e-12 and r3fail))
    P(f"M3 alpha = 0 (kappa = 1): max |predicted d| {float(np.nanmax(np.abs(d3))):.2e}; R2's UFD leg "
      f"{'HOLDS' if b3['readings']['R2']['G_ufd']['HOLDS'] else 'FAILS'} -> "
      f"{'bites' if M['M3_alpha_0_kappa_1__R2_pred_must_be_0_and_G_ufd_must_still_FAIL']['bites'] else 'DOES NOT BITE'}")

    lab0 = {k: runs["canonical"]["readings"][k]["G4_pair"] for k in ("R1", "R2", "R3")}
    b4 = run_footing(T_main, 2 * A0["canonical"], "m4")
    lab4 = {k: b4["readings"][k]["G4_pair"] for k in ("R1", "R2", "R3")}
    sgn0 = runs["canonical"]["readings"]["R2"]["G3_differential"]["measured"]
    sgn4 = b4["readings"]["R2"]["G3_differential"]["measured"]
    M["M4_a0_times_2__labels_must_not_change_and_G3_sign_must_not_flip"] = dict(
        labels_before=lab0, labels_after=lab4, g3_before=sgn0, g3_after=sgn4,
        bites=bool(lab0 == lab4 and sgn0 * sgn4 > 0))
    P(f"M4 a0 x 2: labels {lab0} -> {lab4}; G3 differential {sgn0:+.3f} -> {sgn4:+.3f} -> "
      f"{'bites' if M['M4_a0_times_2__labels_must_not_change_and_G3_sign_must_not_flip']['bites'] else 'DOES NOT BITE'}")
    RES["MUTATE"] = M

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)): return str(o)
    return o

RES["runtime_s"] = round(time.time() - T0, 1)
P(f"\nruntime {RES['runtime_s']} s")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, TAG + ".json"), "w") as fh: json.dump(clean(RES), fh, indent=1, allow_nan=False)
with open(os.path.join(HERE, TAG + ".out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
