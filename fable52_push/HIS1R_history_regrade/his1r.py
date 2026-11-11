#!/usr/bin/env python3
"""HIS1R: blind regrade of HIS1's frozen criteria on DD1's frozen table. TEST lane, quarantined; adopts nothing.
Reading: READING.md (committed alone first). Written from scratch; no HIS1 file is read.
Usage: python3 his1r.py            -> his1r.json, his1r.out
       python3 his1r.py --mutate   -> his1r_MUTATE.json, his1r_MUTATE.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, csv, json, math, re
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.stats import spearmanr, rankdata

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data"); EXT = os.path.join(REPO, "_external_data")
DD1 = os.path.join(REPO, "fable52_push", "DD1_deduce_from_data")
MUT = "--mutate" in sys.argv
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LN10 = math.log(10.0)
def norm(n): return re.sub(r"[^A-Z0-9]", "", str(n).upper())
def fnum(x):
    try:
        v = float(x); return v if math.isfinite(v) else float("nan")
    except Exception:
        return float("nan")

# ------------------------------------------------------------------ table (main rows; brackets kept apart)
ROWS = [r for r in csv.DictReader(l for l in open(os.path.join(DD1, "dd1_table.csv")) if not l.startswith("#"))]
def arr(rows, k, f=float): return np.array([f(r[k]) for r in rows])
MAIN = [r for r in ROWS if r["bracket"] == ""]
SALP = [r for r in ROWS if r["bracket"] == "atlas_salp"]
KEYS = []; SID = {}
for r in MAIN:
    k = (r["cls"], r["sys"])
    if k not in SID: SID[k] = len(KEYS); KEYS.append(k)
NS = len(KEYS)
CLS0 = np.array([k[0] for k in KEYS], dtype=object); NAME = np.array([k[1] for k in KEYS], dtype=object)
sid = np.array([SID[(r["cls"], r["sys"])] for r in MAIN])
lgb, lgo = arr(MAIN, "lgb"), arr(MAIN, "lgo"); eY, elgb = arr(MAIN, "eY"), arr(MAIN, "e_lgb")
last = arr(MAIN, "last", int).astype(bool)
Y0 = lgo - lgb
CLASSES = list(dict.fromkeys(CLS0))
PTS = [np.where(sid == i)[0] for i in range(NS)]
LASTPT = np.array([p[last[p]][0] if last[p].any() else p[-1] for p in PTS])

def XL(lgbv, a0):
    gb = 10.0 ** lgbv; return (np.sqrt(1.0 + 4.0 * a0 / gb) - 1.0) / 2.0
def YL(lgbv, a0): return np.log10(1.0 + XL(lgbv, a0))

def systems(Ypt, a0, drop_inf=False, alt_err=False, lgbv=None):
    """per-system Y, d_L, e (DD1's rule) and the last-point values"""
    lb = lgb if lgbv is None else lgbv
    yl = YL(lb, a0); d = Ypt - yl
    if alt_err:
        h = 1e-4; s = (YL(lb + h, a0) - YL(lb - h, a0)) / (2 * h)
        ept = np.sqrt(np.maximum(eY ** 2 - elgb ** 2, 0.0) + (1.0 + s) ** 2 * elgb ** 2)
    else:
        ept = eY
    Ys, Ds, Es, Ed = np.empty(NS), np.empty(NS), np.empty(NS), np.empty(NS)
    for i, p in enumerate(PTS):
        q = p[np.isfinite(Ypt[p])] if drop_inf else p
        if len(q) == 0: q = p
        Ys[i] = np.median(Ypt[q]); Ds[i] = np.median(d[q])
        Es[i] = np.median(eY[p][np.isfinite(eY[p])]); Ed[i] = np.median(ept[p][np.isfinite(ept[p])])
    j = LASTPT
    return dict(Y=Ys, D=Ds, E=Es, ED=Ed, Ylast=Ypt[j], Dlast=d[j], Elast=eY[j], EDlast=ept[j])

def cstat(v, e):
    v = np.asarray(v, float); e = np.asarray(e, float); n = len(v)
    if n == 0: return dict(n=0, med=float("nan"), se=float("nan"))
    if n == 1: return dict(n=1, med=float(v[0]), se=float(e[0]))
    med = float(np.median(v)); dev = np.abs(v - med); mad = float(np.median(dev)) if np.isfinite(med) else float("nan")
    se = max(1.2533 * 1.4826 * mad / math.sqrt(n), math.sqrt(float(np.sum(e ** 2))) / n)
    return dict(n=n, med=med, se=se)

# ------------------------------------------------------------------ indicators (per original system; they travel with it)
IND = {k: np.full(NS, np.nan) for k in ("fg_sparc", "fg_fr", "ti1", "dhost", "dmean", "virgo", "Mstar_fr", "Mbar_fr",
                                         "tdg_dp", "tdg_gas", "ms_fg", "clash_hm", "age", "mass_hi", "fr_no_ti1")}
# SPARC mrt
sp = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    t = line.split()
    if len(t) != 19: continue
    try: sp[t[0]] = (float(t[7]), float(t[13]))
    except ValueError: continue
# UNGC
U = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "ungc_karachentsev2013.tsv")) if l.strip() and not l.startswith("#")]
UH = U[0]; UT = {norm(u[0]): fnum(u[UH.index("Ti1")]) for u in U[3:]}
ALIAS = {"DDO99": "DDO099", "DDO53": "DDO053", "SEXTANSA": "SEXA", "SEXTANSB": "SEXB"}
def ti1(name):
    k = ALIAS.get(norm(name), norm(name)); return UT.get(k, float("nan")), (k in UT)
# McQuinn t1 (bytes: logMstar 47-50, logMbary 84-87)
MQ = {}
L = open(os.path.join(DATA, "faint_rotators_mcquinn2022", "apjac9285t1_mrt.txt")).read().splitlines()
i0 = max(k for k, l in enumerate(L) if l.startswith("----"))
for l in L[i0 + 1:]:
    if not l.strip(): continue
    t = l.split(); lms = float(l[46:50]); lmb = float(l[83:87]); assert abs(lmb - float(t[-2])) < 1e-9
    MQ[t[0]] = (lms, lmb)
# LVD
LVD = {}
for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
        LVD[(host, r["name"])] = dict(dh=fnum(r.get("distance_host")), dm31=fnum(r.get("distance_m31")), age=fnum(r.get("age")),
                                      mhi=fnum(r.get("mass_HI")))
def tsv(fn):
    T = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, fn)) if l.strip() and not l.startswith("#")]
    return [dict(zip(T[0], x)) for x in T[1:]]
FRE = {r["name"]: fnum(r["dmean_kpc"]) for r in tsv("freundlich2022_coma_udgs.tsv")}
A3 = {r["name"]: fnum(r["Virgo"]) for r in tsv("atlas3d_fj_table.tsv")}
DTS = {r["name"]: r for r in tsv("diteodoro2023_massive_spirals.tsv")}
TDG = {r["object"]: r for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"), encoding="utf-8-sig"))}
def ckey(name):
    n = name.replace("~", "").replace(" ", "").replace("*", "")
    m = re.match(r"^A(?:bell)?(\d+)$", n, re.I)
    if m: return "A" + m.group(1)
    m = re.search(r"(\d{4})", n); return m.group(1) if m else n
HM = set(); sect = None
for ln in open(os.path.join(EXT, "hl3", "umetsu16", "src", "table1.tex"), errors="replace"):
    if "High Magnification" in ln: sect = "hm"
    if ln.lstrip().startswith("~~") and sect == "hm": HM.add(ckey(ln.split("&")[0]))
UNMATCHED = {}
for i, (c, n) in enumerate(KEYS):
    if c == "SPARC":
        L36, MHI = sp[n]; IND["fg_sparc"][i] = 1.33 * MHI / (0.5 * L36 + 1.33 * MHI); IND["ti1"][i] = ti1(n)[0]
    elif c == "faint rotators":
        lms, lmb = MQ[n]; IND["fg_fr"][i] = 1 - 10 ** (lms - lmb); IND["Mstar_fr"][i] = 10 ** lms; IND["Mbar_fr"][i] = 10 ** lmb
        t, ok = ti1(n); IND["ti1"][i] = t; IND["fr_no_ti1"][i] = 0.0 if np.isfinite(t) else 1.0
        if not np.isfinite(t): UNMATCHED[n] = "no UNGC name" if not ok else "blank Ti1"
    elif c in ("MW bright dwarfs", "MW ultra-faints"):
        d = LVD[("MW", n)]; IND["dhost"][i] = d["dh"]; IND["age"][i] = d["age"]
    elif c == "M31 dwarfs":
        d = LVD[("M31", n)]; IND["dhost"][i] = d["dh"] if np.isfinite(d["dh"]) else d["dm31"]; IND["age"][i] = d["age"]
    elif c == "LG field dwarfs":
        d = LVD[("field", n)]; IND["mass_hi"][i] = d["mhi"]; IND["ti1"][i] = ti1(n)[0]
    elif c == "Coma UDGs": IND["dmean"][i] = FRE[n]
    elif c == "ATLAS3D": IND["virgo"][i] = A3.get(n, float("nan"))
    elif c == "tidal dwarfs":
        r = TDG[n]; IND["tdg_dp"][i] = float(r["D_p_kpc"]); IND["tdg_gas"][i] = (float(r["M_atom_1e8"]) + float(r["M_mol_1e8"])) / float(r["M_bar_1e8"])
    elif c == "massive spirals":
        r = DTS[n]; ms, mg = 10 ** float(r["logMs_W1"]), 10 ** float(r["logMgas"]); IND["ms_fg"][i] = mg / (ms + mg)
    elif c == "CLASH": IND["clash_hm"][i] = 1.0 if ckey(n) in HM else 0.0

# ------------------------------------------------------------------ grading
GP = [("G1", "SPARC", "fg_sparc", -1), ("G2", "faint rotators", "fg_fr", -1), ("G3", "MW bright dwarfs", "dhost", +1),
      ("G4", "MW ultra-faints", "dhost", +1), ("G5", "M31 dwarfs", "dhost", +1), ("G6", "Coma UDGs", "dmean", +1)]
RB1 = dict(xcop_last=(1.095, 0.885, 1.259), xcop_r500=(1.057, 1.046, 1.072), groups=(0.597, 0.556, 0.637))

def perm_p(x, y, nperm=20000, seed=11):
    rx, ry = rankdata(x), rankdata(y); rx = (rx - rx.mean()) / rx.std(); ry = (ry - ry.mean()) / ry.std()
    r0 = float(np.mean(rx * ry)); rng = np.random.default_rng(seed)
    P_ = np.array([rng.permutation(ry) for _ in range(nperm)]); rr = (P_ @ rx) / len(rx)
    return (1 + int(np.sum(np.abs(rr) >= abs(r0) - 1e-12))) / (nperm + 1)

def h5(S, lab, alt_p=False, ind=IND):
    res = []
    for g, c, k, sg in GP:
        m = (lab == c) & np.isfinite(ind[k]) & np.isfinite(S["D"])
        x, y = ind[k][m], S["D"][m]; n = int(m.sum())
        if n >= 3 and np.ptp(x) > 0 and np.ptp(y) > 0:
            rho, p = spearmanr(x, y); rho = float(rho); p = float(p)
            if alt_p: p = perm_p(x, y)
        else:
            rho, p = float("nan"), 1.0
        res.append(dict(pair=g, cls=c, n=n, rho=rho, p=p, sign=sg))
    order = sorted(range(6), key=lambda i: res[i]["p"]); rej = set()
    for j, i in enumerate(order):
        if res[i]["p"] <= 0.05 / (6 - j): rej.add(i)
        else: break
    for i, r in enumerate(res):
        r["holm_reject"] = i in rej
        r["with_sign"] = bool(i in rej and np.isfinite(r["rho"]) and np.sign(r["rho"]) == r["sign"])
        r["against"] = bool(i in rej and np.isfinite(r["rho"]) and np.sign(r["rho"]) == -r["sign"])
    if any(r["against"] for r in res): out = "FAILS"
    elif any(r["with_sign"] for r in res): out = "HOLDS"
    else: out = "NO POWER"
    return dict(pairs=res, outcome=out)

def sets(lab, opt, ind=IND):
    fg = ind["fg_sparc"]; sp_m = (lab == "SPARC")
    if opt.get("alt_half"):
        med = np.median(fg[sp_m & np.isfinite(fg)]); gr = sp_m & np.isfinite(fg) & (fg > med)
    else:
        gr = sp_m & np.isfinite(fg) & (fg >= 0.5)
    t = ind["ti1"]; fr = lab == "faint rotators"
    iso = fr & np.isfinite(t) & ((t <= 0) if opt.get("alt_iso1") else (t < 0))
    if opt.get("alt_iso2"): iso = iso | (fr & (ind["fr_no_ti1"] == 1))
    return {"SPARC": sp_m, "SPARC gas-rich": gr, "faint rotators Ti1<0": iso, "KiDS": lab == "KiDS",
            "LG field dwarfs": lab == "LG field dwarfs", "ATLAS3D outside Virgo": (lab == "ATLAS3D") & (ind["virgo"] == 0),
            "MW bright dwarfs": lab == "MW bright dwarfs", "MW ultra-faints": lab == "MW ultra-faints",
            "M31 dwarfs": lab == "M31 dwarfs", "Coma UDGs": lab == "Coma UDGs", "groups": lab == "groups",
            "tidal dwarfs": lab == "tidal dwarfs", "NGC 1052 UDGs": lab == "NGC 1052 UDGs"}
H3A = ["SPARC", "SPARC gas-rich", "faint rotators Ti1<0"]
H3B = ["SPARC", "KiDS", "LG field dwarfs", "faint rotators Ti1<0", "ATLAS3D outside Virgo"]
H3C = ["MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs", "groups"]

def grade(S, lab=CLS0, opt=None, ind=IND, controls=True):
    opt = opt or {}; E = S["ED"] if opt.get("alt_err") else S["E"]; El = S["EDlast"] if opt.get("alt_err") else S["Elast"]
    R = {}
    # H1
    td = lab == "tidal dwarfs"; y = cstat(S["Y"][td], S["E"][td]); d = cstat(S["D"][td], E[td])
    c1 = abs(y["med"]) <= 2 * y["se"]; c2 = d["med"] < -3 * d["se"]
    R["H1"] = dict(Y=y, dL=d, Y_in_se=y["med"] / y["se"], dL_in_se=d["med"] / d["se"], at_newton=bool(c1), below_law=bool(c2),
                   outcome="HOLDS" if (c1 and c2) else "FAILS")
    # H2
    below = S["Y"] < -3 * S["E"]; cnt = int(below.sum())
    cl = {}
    for c in CLASSES:
        m = lab == c; s = cstat(S["Y"][m], S["E"][m]); s["in_se"] = s["med"] / s["se"] if s["n"] else float("nan"); cl[c] = s
    b_ok = all(not (s["n"] and s["med"] < -3 * s["se"]) for s in cl.values())
    ngc = np.where(lab == "NGC 1052 UDGs")[0]
    cc = [dict(sys=str(NAME[i]), Y=float(S["Y"][i]), dL=float(S["D"][i]), e=float(S["E"][i]), eD=float(E[i]),
               Y_in_e=float(S["Y"][i] / S["E"][i]), dL_in_e=float(S["D"][i] / E[i]),
               ok=bool(S["Y"][i] >= -3 * S["E"][i] and S["D"][i] <= 3 * E[i])) for i in ngc]
    c_ok = all(x["ok"] for x in cc)
    R["H2"] = dict(a_count=cnt, a_systems=[f"{CLS0[i]}/{NAME[i]}" for i in np.where(below)[0]], a_ok=cnt <= 3,
                   b_classes=cl, b_ok=bool(b_ok), c=cc, c_ok=bool(c_ok), outcome="HOLDS" if (cnt <= 3 and b_ok and c_ok) else "FAILS")
    # H3
    ST = sets(lab, opt, ind); st = {}
    for k, m in ST.items():
        s = cstat(S["D"][m], E[m]); s["in_se"] = s["med"] / s["se"] if s["n"] else float("nan"); st[k] = s
    a = {k: (st[k]["n"] == 0 or abs(st[k]["med"]) <= 3 * st[k]["se"]) for k in H3A}
    b = {k: (st[k]["n"] == 0 or st[k]["med"] >= -3 * st[k]["se"]) for k in H3B}
    c = {k: (st[k]["n"] == 0 or st[k]["med"] >= -3 * st[k]["se"]) for k in H3C}
    R["H3"] = dict(sets=st, a=a, b=b, c=c, a_ok=all(a.values()), b_ok=all(b.values()), c_ok=all(c.values()),
                   outcome="HOLDS" if (all(a.values()) and all(b.values()) and all(c.values())) else "FAILS")
    # H4 (quoted from RB1)
    h4 = (RB1["xcop_last"][1] <= 1 <= RB1["xcop_last"][2]) and RB1["xcop_r500"][0] >= 1 and RB1["groups"][2] < 1
    R["H4"] = dict(rb1=RB1, outcome="HOLDS" if h4 else "FAILS")
    # H5
    R["H5"] = h5(S, lab, opt.get("alt_p", False), ind)
    outs = [R[h]["outcome"] for h in ("H1", "H2", "H3", "H4", "H5")]
    nf = outs.count("FAILS")
    if nf == 0 and all(o == "HOLDS" for o in outs): lab_ = "THE HISTORY READING HOLDS ON EVERY TEST"
    elif nf <= 1: lab_ = "HOLDS EXCEPT"
    else: lab_ = "FAILS"
    R["label"] = lab_; R["outcomes"] = dict(zip(("H1", "H2", "H3", "H4", "H5"), outs))
    if controls:
        F = {}
        F["F1"] = bool(abs(d["med"]) <= 2 * d["se"])
        fc = int(np.sum(S["D"] < -3 * E)); f2b = all(abs(S["D"][i]) <= 3 * E[i] for i in ngc)
        F["F2"] = bool(fc <= 3 and f2b); F["F2_count"] = fc; F["F2_ngc"] = bool(f2b)
        keys = list(dict.fromkeys(H3A + H3B + H3C + (["tidal dwarfs", "NGC 1052 UDGs"] if opt.get("alt_host") else [])))
        f3 = {k: bool(st[k]["n"] == 0 or abs(st[k]["med"]) <= 3 * st[k]["se"]) for k in keys}
        F["F3"] = all(f3.values()); F["F3_sets"] = f3
        xm = lab == "X-COP"; xs = cstat(S["Dlast"][xm], El[xm]); F["F4_stat"] = xs
        F["F4"] = bool(abs(xs["med"]) <= 3 * xs["se"])
        F["F5"] = not any(p["holm_reject"] for p in R["H5"]["pairs"])
        F["score"] = int(sum(F[k] for k in ("F1", "F2", "F3", "F4", "F5")))
        R["force"] = F
    return R

def holds_count(R): return sum(R[h]["outcome"] == "HOLDS" for h in ("H1", "H2", "H3", "H5"))
def norule(S, opt, rng="default", seed=7):
    perm = (np.random.default_rng(seed).permutation(NS) if rng == "default" else np.random.RandomState(seed).permutation(NS))
    lab = CLS0[perm]
    R = grade(S, lab, opt, controls=False); return holds_count(R), {h: R[h]["outcome"] for h in ("H1", "H2", "H3", "H5")}

def short(R):
    o = R["outcomes"]
    return f"{R['label']}: " + ", ".join(f"{h} {o[h]}" for h in o) + (f"; force {R['force']['score']}/5" if "force" in R else "")

# ------------------------------------------------------------------ known answers
def known_answers():
    KA = {}
    # KA1
    d1 = json.load(open(os.path.join(DD1, "dd1.json"))); mx = 0.0; nc = 0; missing = []
    for f, a0 in FOOT.items():
        S = systems(Y0, a0)
        for c in CLASSES:
            try: ref = d1["runs"][f]["L0"]["LOCO"][c]["off"]
            except KeyError: missing.append((f, c)); continue
            v = float(np.median(S["D"][CLS0 == c]))
            if not (np.isfinite(v) and np.isfinite(ref)): dv = 0.0 if v == ref else float("inf")
            else: dv = abs(v - ref)
            mx = max(mx, dv); nc += 1
    KA["KA1"] = dict(compared=nc, missing=missing, max_abs_diff=mx, pass_=bool(mx <= 1e-9 and not missing))
    # KA2
    rat = np.array([float(TDG[n]["Mdyn_over_Mbar"]) for n in NAME[CLS0 == "tidal dwarfs"]])
    erat = np.array([float(TDG[n]["e_Mdyn_over_Mbar"]) for n in NAME[CLS0 == "tidal dwarfs"]])
    ly = np.log10(rat); el = erat / (rat * LN10); w = 1 / el ** 2
    m, s = float(np.sum(w * ly) / np.sum(w)), float(1 / math.sqrt(np.sum(w)))
    md = np.array([float(TDG[n]["M_dyn_1e8"]) for n in NAME[CLS0 == "tidal dwarfs"]]); emd = np.array([float(TDG[n]["e_M_dyn_1e8"]) for n in NAME[CLS0 == "tidal dwarfs"]])
    mb = np.array([float(TDG[n]["M_bar_1e8"]) for n in NAME[CLS0 == "tidal dwarfs"]]); emb = np.array([float(TDG[n]["e_M_bar_1e8"]) for n in NAME[CLS0 == "tidal dwarfs"]])
    ly2 = np.log10(md / mb); el2 = np.sqrt((emd / md) ** 2 + (emb / mb) ** 2) / LN10; w2 = 1 / el2 ** 2
    S = systems(Y0, FOOT["canonical"]); ty = S["Y"][CLS0 == "tidal dwarfs"]
    KA["KA2"] = dict(ivw=m, ivw_se=s, alt_ivw=float(np.sum(w2 * ly2) / np.sum(w2)), alt_se=float(1 / math.sqrt(np.sum(w2))),
                     table_minus_logratio=[float(x) for x in ty - ly2],
                     pass_=bool(abs(m - 0.083) <= 1e-3 and abs(s - 0.096) <= 1e-3 and np.all(np.abs(ty - ly2) <= 0.05)))
    # KA3
    k3 = {}
    for f, a0 in FOOT.items():
        yl = YL(lgb, a0)
        hosted = ["MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs"]
        for tag, hl in (("i", hosted), ("i_alt_groups", hosted + ["groups"])):
            Yh = yl.copy(); c0 = CLS0[sid]
            Yh[np.isin(c0, ["tidal dwarfs", "NGC 1052 UDGs"])] = 0.0; Yh[np.isin(c0, hl)] += 0.3
            R = grade(systems(Yh, a0), opt={}); k3[f"{f}_{tag}"] = dict(H1=R["H1"]["outcome"], H2=R["H2"]["outcome"], H3=R["H3"]["outcome"], F1=R["force"]["F1"],
                                                                  pass_=bool(R["H1"]["outcome"] == R["H2"]["outcome"] == R["H3"]["outcome"] == "HOLDS" and not R["force"]["F1"]))
        R = grade(systems(yl.copy(), a0), opt={})
        k3[f"{f}_ii"] = dict(H1=R["H1"]["outcome"], F1=R["force"]["F1"], F2=R["force"]["F2"], F3=R["force"]["F3"], H5=R["H5"]["outcome"],
                             pass_=bool(R["H1"]["outcome"] == "FAILS" and R["force"]["F1"] and R["force"]["F2"] and R["force"]["F3"] and R["H5"]["outcome"] == "NO POWER"))
        Yt = yl.copy()
        for c, k in (("SPARC", "fg_sparc"), ("faint rotators", "fg_fr")):
            m_ = CLS0 == c; med = np.median(IND[k][m_]); pm = CLS0[sid] == c
            Yt[pm] -= 0.3 * (IND[k][sid[pm]] - med)
        R = grade(systems(Yt, a0), opt={}); k3[f"{f}_iii"] = dict(H5=R["H5"]["outcome"], pass_=R["H5"]["outcome"] == "HOLDS")
    KA["KA3"] = dict(cases=k3, pass_=all(v["pass_"] for v in k3.values()))
    # KA4
    g = np.logspace(-15, -6, 2001); ok = True
    for a0 in FOOT.values():
        x = (np.sqrt(1 + 4 * a0 / g) - 1) / 2; ok &= bool(np.all(x > 0) and np.all(x <= np.sqrt(a0 / g) * (1 + 1e-12)))
    KA["KA4"] = dict(pass_=ok)
    KA["all_pass"] = all(KA[k]["pass_"] for k in ("KA1", "KA2", "KA3", "KA4"))
    return KA

# ------------------------------------------------------------------ main
def main():
    P("HIS1R blind regrade of HIS1 (criteria as on disk; reading READING.md). TEST lane; adopts nothing.")
    P(f"table: {len(ROWS)} rows, {len(MAIN)} main points, {len(SALP)} atlas_salp, {NS} systems, {len(CLASSES)} classes")
    for c in CLASSES: P(f"  {c:18s} systems {int(np.sum(CLS0 == c)):4d} points {int(np.sum(CLS0[sid] == c)):5d}")
    P(f"faint rotators without UNGC Ti1: {UNMATCHED}")
    P(f"CLASH high-magnification clusters matched: {sorted(set(NAME[(CLS0 == 'CLASH') & (IND['clash_hm'] == 1)]))}")
    KA = known_answers()
    P(f"KA1 L0 class offsets vs dd1.json: {KA['KA1']['compared']} compared, max |diff| {KA['KA1']['max_abs_diff']:.2e} -> {KA['KA1']['pass_']}")
    P(f"KA2 IVW log10(Mdyn/Mbar) {KA['KA2']['ivw']:+.4f} +- {KA['KA2']['ivw_se']:.4f} (alt columns {KA['KA2']['alt_ivw']:+.4f} +- {KA['KA2']['alt_se']:.4f}); "
      f"table Y - log ratio max {max(abs(x) for x in KA['KA2']['table_minus_logratio']):.4f} -> {KA['KA2']['pass_']}")
    P(f"KA3 {json.dumps(KA['KA3']['cases'])} -> {KA['KA3']['pass_']}"); P(f"KA4 -> {KA['KA4']['pass_']}")
    J = dict(lane="HIS1R", reading="READING.md", KA=KA, footings={})
    ALTS = {"main": {}, "ALT-INF": {"drop_inf": True}, "ALT-ERR": {"alt_err": True}, "ALT-ISO1": {"alt_iso1": True},
            "ALT-ISO2": {"alt_iso2": True}, "ALT-HALF": {"alt_half": True}, "ALT-P": {"alt_p": True}, "ALT-HOST": {"alt_host": True}}
    for f, a0 in FOOT.items():
        P(); P(f"==================== footing {f} (a0 {a0:.4e})")
        FJ = {}
        for an, opt in ALTS.items():
            S = systems(Y0, a0, drop_inf=opt.get("drop_inf", False), alt_err=opt.get("alt_err", False))
            R = grade(S, CLS0, opt)
            nr, nro = norule(S, opt)
            R["norule"] = dict(holds=nr, outcomes=nro)
            if not KA["all_pass"]: R["label"] = "NO VERDICT"
            FJ[an] = R
            P(f"[{an}] {short(R)}; no rule {nr}/4 {nro}")
        R = FJ["main"]; S = systems(Y0, a0)
        P("-- main reading, details")
        h = R["H1"]; P(f"H1 tidal dwarfs: median Y {h['Y']['med']:+.3f} se {h['Y']['se']:.3f} ({h['Y_in_se']:+.2f} se); median d_L {h['dL']['med']:+.3f} se {h['dL']['se']:.3f} ({h['dL_in_se']:+.2f} se) -> {h['outcome']}")
        h = R["H2"]; P(f"H2 (a) count Y_sys < -3 e_sys: {h['a_count']} {h['a_systems']}; (b) ok {h['b_ok']}; (c) ok {h['c_ok']} -> {h['outcome']}")
        for c, s in h["b_classes"].items(): P(f"   class {c:18s} n {s['n']:4d} median Y {s['med']:+.3f} se {s['se']:.3f} ({s['in_se']:+.2f} se)")
        for x in h["c"]: P(f"   {x['sys']}: Y {x['Y']:+.3f} ({x['Y_in_e']:+.2f} e)  d_L {x['dL']:+.3f} ({x['dL_in_e']:+.2f} e)  e {x['e']:.3f} ok {x['ok']}")
        h = R["H3"]
        for k, s in h["sets"].items(): P(f"H3 set {k:22s} n {s['n']:4d} median d_L {s['med']:+.3f} se {s['se']:.3f} ({s['in_se']:+.2f} se)")
        P(f"H3 (a) {h['a']} (b) {h['b']} (c) {h['c']} -> {h['outcome']}")
        P(f"H4 quoted from RB1 {RB1} -> {R['H4']['outcome']}")
        for p in R["H5"]["pairs"]: P(f"H5 {p['pair']} {p['cls']:18s} n {p['n']:4d} rho {p['rho']:+.3f} p {p['p']:.4f} holm {p['holm_reject']} with {p['with_sign']} against {p['against']}")
        P(f"H5 -> {R['H5']['outcome']}")
        F = R["force"]; P(f"force: F1 {F['F1']} F2 {F['F2']} (count {F['F2_count']}, DF2/DF4 {F['F2_ngc']}) F3 {F['F3']} F4 {F['F4']} "
                          f"(X-COP last median d_L {F['F4_stat']['med']:+.3f} se {F['F4_stat']['se']:.3f}) F5 {F['F5']} -> {F['score']}/5")
        P(f"F3 sets: {F['F3_sets']}")
        # reported items
        rep = {}
        fr = CLS0 == "faint rotators"; t = IND["ti1"][fr]
        rep["fr_isolated_fraction"] = dict(iso=int(np.sum(t < 0)), all=int(fr.sum()), with_ti1=int(np.isfinite(t).sum()))
        iso = fr & (IND["ti1"] < 0)
        for tag, kM, fD in (("M*x2", 2.0, 1.0), ("M*x0.5", 0.5, 1.0), ("Dx0.8", 1.0, 0.8), ("Dx1.2", 1.0, 1.2)):
            lb2 = lgb.copy(); lo2 = lgo.copy(); pm = CLS0[sid] == "faint rotators"
            Mb, Ms = IND["Mbar_fr"][sid[pm]], IND["Mstar_fr"][sid[pm]]
            lb2[pm] = lgb[pm] + np.log10((Mb + (kM - 1) * Ms) / Mb); lo2[pm] = lgo[pm] - math.log10(fD)
            S2 = systems(lo2 - lb2, a0, lgbv=lb2)
            a_ = cstat(S2["D"][iso], S2["E"][iso]); b_ = cstat(S2["D"][fr], S2["E"][fr])
            rep[f"fr_{tag}"] = dict(iso_med=a_["med"], iso_se=a_["se"], iso_in_se=a_["med"] / a_["se"], all_med=b_["med"], all_se=b_["se"], all_in_se=b_["med"] / b_["se"])
        b_ = cstat(S["D"][fr], S["E"][fr]); rep["fr_all"] = dict(med=b_["med"], se=b_["se"], in_se=b_["med"] / b_["se"])
        # X at last points (H4 beside)
        xl = {}
        rng = np.random.default_rng(3)
        for c in CLASSES:
            m = CLS0 == c; X = 10 ** S["Ylast"][m] - 1; eX = LN10 * (1 + X) * S["Elast"][m]; s = cstat(X, eX)
            bs = [np.median(rng.choice(X, len(X))) for _ in range(2000)] if len(X) > 1 else [X[0]]
            xl[c] = dict(n=s["n"], med=s["med"], se=s["se"], q025=float(np.percentile(bs, 2.5)), q975=float(np.percentile(bs, 97.5)))
        rep["X_last"] = xl
        # reported correlations
        def sp_(k, c):
            m = (CLS0 == c) & np.isfinite(IND[k])
            if m.sum() < 3 or np.ptp(IND[k][m]) == 0: return dict(n=int(m.sum()))
            r, p = spearmanr(IND[k][m], S["D"][m]); return dict(n=int(m.sum()), rho=float(r), p=float(p))
        rep["corr"] = {"SPARC Ti1": sp_("ti1", "SPARC"), "faint rotators Ti1": sp_("ti1", "faint rotators"), "tidal dwarfs D_p": sp_("tdg_dp", "tidal dwarfs"),
                       "tidal dwarfs gas share": sp_("tdg_gas", "tidal dwarfs"), "massive spirals f_g": sp_("ms_fg", "massive spirals"),
                       "MW bright age": sp_("age", "MW bright dwarfs"), "MW ultra-faint age": sp_("age", "MW ultra-faints"), "M31 age": sp_("age", "M31 dwarfs"),
                       "LG field mass_HI": sp_("mass_hi", "LG field dwarfs"), "LG field Ti1": sp_("ti1", "LG field dwarfs")}
        for c, k in (("ATLAS3D", "virgo"), ("CLASH", "clash_hm")):
            for v in (0, 1):
                m = (CLS0 == c) & (IND[k] == v); s = cstat(S["D"][m], S["E"][m]); rep[f"{c} {k}={v}"] = s
        # brackets: ATLAS3D at Salpeter
        sal = {}
        Ys = np.array([float(r["lgo"]) - float(r["lgb"]) for r in SALP]); es = np.array([float(r["eY"]) for r in SALP])
        yls = YL(np.array([float(r["lgb"]) for r in SALP]), a0)
        s1 = cstat(Ys, es); s2 = cstat(Ys - yls, es)
        sal = dict(n=len(Ys), median_Y=s1["med"], se_Y=s1["se"], Y_in_se=s1["med"] / s1["se"], count_below=int(np.sum(Ys < -3 * es)),
                   median_dL=s2["med"], se_dL=s2["se"])
        rep["ATLAS3D_Salpeter_bracket"] = sal
        # no-rule distribution over seeds and alt RNG
        nr_seeds = [norule(S, {}, seed=s_)[0] for s_ in range(1, 201)]
        rep["norule_seed7_default"] = R["norule"]; rep["norule_seed7_RandomState"] = dict(zip(("holds", "outcomes"), norule(S, {}, rng="rs")))
        rep["norule_seeds_1_200"] = {str(k): nr_seeds.count(k) for k in range(5)}
        R["reported"] = rep
        P(f"reported: faint rotators isolated {rep['fr_isolated_fraction']}; all 20: {rep['fr_all']}")
        for tag in ("M*x2", "M*x0.5", "Dx0.8", "Dx1.2"):
            q = rep[f"fr_{tag}"]; P(f"   faint rotators {tag}: isolated {q['iso_med']:+.3f} se {q['iso_se']:.3f} ({q['iso_in_se']:+.2f} se); all {q['all_med']:+.3f} ({q['all_in_se']:+.2f} se)")
        for c in ("X-COP", "groups"): q = xl[c]; P(f"   X at last point {c}: median {q['med']:.3f} se {q['se']:.3f} boot95 [{q['q025']:.3f}, {q['q975']:.3f}] n {q['n']}")
        P(f"   correlations reported: {json.dumps(rep['corr'])}")
        for c in ("ATLAS3D virgo=0", "ATLAS3D virgo=1", "CLASH clash_hm=0", "CLASH clash_hm=1"): q = rep[c]; P(f"   {c}: n {q['n']} median d_L {q['med']:+.3f} se {q['se']:.3f}")
        P(f"   ATLAS3D Salpeter bracket: {sal}")
        P(f"   no rule: seed 7 default {R['norule']}; RandomState {rep['norule_seed7_RandomState']}; seeds 1..200 holds-count histogram {rep['norule_seeds_1_200']}")
        J["footings"][f] = FJ
    return J

# ------------------------------------------------------------------ own checks: planted signals and shuffles
def own_checks():
    C = {}
    for f, a0 in FOOT.items():
        yl = YL(lgb, a0); c0 = CLS0[sid]; base = yl.copy(); Sb = systems(base, a0); out = {}
        def g(Y, lab=CLS0): return grade(systems(Y, a0), lab, {})
        # H1
        Y = base.copy(); Y[c0 == "tidal dwarfs"] = 0.0; out["H1_tdg_at_0"] = g(Y)["H1"]["outcome"]
        out["H1_tdg_on_law"] = g(base)["H1"]["outcome"]
        Y = base.copy(); Y[c0 == "tidal dwarfs"] = 0.4; out["H1_tdg_at_+0.4"] = g(Y)["H1"]["outcome"]
        # H2 (a): plant k systems in RC100 at Y = -5 e_sys
        rc = np.where(CLS0 == "RC100")[0]
        for k in (3, 4):
            Y = base.copy()
            for i in rc[:k]: Y[PTS[i]] = -5 * Sb["E"][i]
            out[f"H2a_planted_{k}"] = dict(count=g(Y)["H2"]["a_count"], a_ok=g(Y)["H2"]["a_ok"])
        # H2 (b): RC100 moved to median -4 se / -2 se
        s = cstat(np.zeros(len(rc)), Sb["E"][rc])["se"]
        for z in (-4, -2):
            Y = base.copy(); Y[c0 == "RC100"] = z * s; out[f"H2b_RC100_at_{z}se"] = g(Y)["H2"]["b_ok"]
        # H2 (c)
        df = {str(NAME[i]): i for i in np.where(CLS0 == "NGC 1052 UDGs")[0]}
        Y = base.copy(); Y[PTS[df["DF2"]]] = -4 * Sb["E"][df["DF2"]]; out["H2c_DF2_at_-4e"] = g(Y)["H2"]["c_ok"]
        Y = base.copy(); Y[PTS[df["DF4"]]] = yl[PTS[df["DF4"]]] + 4 * Sb["E"][df["DF4"]]; out["H2c_DF4_dL_+4e"] = g(Y)["H2"]["c_ok"]
        Y = base.copy(); Y[c0 == "NGC 1052 UDGs"] = 0.0; out["H2c_both_at_0"] = g(Y)["H2"]["c_ok"]
        # H3: SPARC moved by -4 / +4 se; MW ultra-faints by -4 se
        sp_ = CLS0 == "SPARC"; s = cstat(np.zeros(sp_.sum()), Sb["E"][sp_])["se"]
        for z in (-4, 4):
            Y = base.copy(); Y[c0 == "SPARC"] += z * s; R = g(Y)["H3"]; out[f"H3_SPARC_{z:+d}se"] = dict(a=R["a"]["SPARC"], b=R["b"]["SPARC"])
        uf = CLS0 == "MW ultra-faints"; s = cstat(np.zeros(uf.sum()), Sb["E"][uf])["se"]
        Y = base.copy(); Y[c0 == "MW ultra-faints"] -= 4 * s; out["H3c_UF_-4se"] = g(Y)["H3"]["c"]["MW ultra-faints"]
        # shuffle that should destroy the planted SPARC shift: labels permuted
        Y = base.copy(); Y[c0 == "SPARC"] -= 4 * cstat(np.zeros(sp_.sum()), Sb["E"][sp_])["se"]; S_ = systems(Y, a0)
        out["H3_SPARC_-4se_shuffled_fail_fraction"] = float(np.mean([not grade(S_, CLS0[np.random.default_rng(s_).permutation(NS)], {}, controls=False)["H3"]["a"]["SPARC"] for s_ in range(100)]))
        # H5 planted per pair, with and against the sign, then indicator shuffled within class
        h5o = {}
        for gname, c, k, sg in GP:
            m = (CLS0 == c) & np.isfinite(IND[k]); x = IND[k][m]; z = (rankdata(x) - rankdata(x).mean()) / rankdata(x).std()
            for tag, sgn in (("with", sg), ("against", -sg)):
                Y = base.copy(); ids = np.where(m)[0]
                for i, zi in zip(ids, z): Y[PTS[i]] += sgn * 0.3 * zi
                S_ = systems(Y, a0); h5o[f"{gname}_{tag}"] = h5(S_, CLS0)["outcome"]
                if tag == "with":
                    nop = 0
                    for s_ in range(100):
                        ind2 = {kk: v.copy() for kk, v in IND.items()}; rr = np.random.default_rng(1000 + s_)
                        ind2[k][ids] = IND[k][ids][rr.permutation(len(ids))]
                        nop += h5(S_, CLS0, ind=ind2)["outcome"] == "NO POWER"
                    h5o[f"{gname}_with_indicator_shuffled_NO_POWER_fraction"] = nop / 100
        out["H5"] = h5o
        # F4 planted
        xc = c0 == "X-COP"
        out["F4_xcop_on_law"] = g(base)["force"]["F4"]
        Y = base.copy(); Y[xc] += 0.5; out["F4_xcop_+0.5"] = g(Y)["force"]["F4"]
        S_ = systems(Y, a0)
        out["F4_xcop_+0.5_labels_shuffled_pass_fraction"] = float(np.mean([grade(S_, CLS0[np.random.default_rng(s_).permutation(NS)], {})["force"]["F4"] for s_ in range(100)]))
        # H1 history truth, labels shuffled
        Y = base.copy(); Y[c0 == "tidal dwarfs"] = 0.0; S_ = systems(Y, a0)
        out["H1_tdg_at_0_labels_shuffled_hold_fraction"] = float(np.mean([grade(S_, CLS0[np.random.default_rng(s_).permutation(NS)], {}, controls=False)["H1"]["outcome"] == "HOLDS" for s_ in range(100)]))
        C[f] = out
    return C

def mutate():
    M = {}
    for f, a0 in FOOT.items():
        yl = YL(lgb, a0); c0 = CLS0[sid]; o = {}
        Y = Y0.copy(); Y[c0 == "tidal dwarfs"] = yl[c0 == "tidal dwarfs"]; o["M1_H1"] = grade(systems(Y, a0))["H1"]["outcome"]
        Y = Y0.copy(); spi = np.where(CLS0 == "SPARC")[0][:4]; S0 = systems(Y0, a0)
        for i in spi: Y[PTS[i]] = -0.6
        R = grade(systems(Y, a0)); o["M2_H2"] = R["H2"]["outcome"]; o["M2_detail"] = dict(systems=[str(NAME[i]) for i in spi], e_sys=[float(S0["E"][i]) for i in spi],
                                                                                         a_count=R["H2"]["a_count"], b_ok=R["H2"]["b_ok"], c_ok=R["H2"]["c_ok"])
        Y = Y0.copy(); m = CLS0 == "SPARC"; med = np.median(IND["fg_sparc"][m]); pm = c0 == "SPARC"
        Y[pm] += 0.5 * (IND["fg_sparc"][sid[pm]] - med); R = grade(systems(Y, a0)); o["M3_H5"] = R["H5"]["outcome"]; o["M3_G1"] = R["H5"]["pairs"][0]
        R = grade(systems(Y0, 2 * a0)); o["M4_H3a_SPARC"] = R["H3"]["a"]["SPARC"]; o["M4_SPARC"] = R["H3"]["sets"]["SPARC"]
        o["bites"] = dict(M1=o["M1_H1"] == "FAILS", M2=o["M2_H2"] == "FAILS", M3=o["M3_H5"] == "FAILS", M4=o["M4_H3a_SPARC"] is False)
        M[f] = o
    return M

def jclean(o):
    if isinstance(o, dict): return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jclean(v) for v in o]
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating, float)): v = float(o); return v if math.isfinite(v) else str(v)
    return o

if __name__ == "__main__":
    if MUT:
        M = mutate()
        for f, o in M.items(): P(f"MUTATE {f}: {json.dumps(jclean(o))}")
        P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
        json.dump(jclean(dict(lane="HIS1R", mutate=M, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")), open(os.path.join(HERE, "his1r_MUTATE.json"), "w"), indent=1)
        open(os.path.join(HERE, "his1r_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    else:
        J = main()
        P(); P("-- own checks (planted signals, shuffles)")
        C = own_checks(); J["own_checks"] = C
        for f, o in C.items(): P(f"{f}: {json.dumps(jclean(o))}")
        J["note"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
        P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
        json.dump(jclean(J), open(os.path.join(HERE, "his1r.json"), "w"), indent=1)
        open(os.path.join(HERE, "his1r.out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
