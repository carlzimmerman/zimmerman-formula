#!/usr/bin/env python3
"""HIS1: the history reading on DD1's frozen table (criteria 152ecaf5c4). TEST lane, quarantined; adopts nothing.
kappa = 1/2 FITTED; not theory closed. One thread.
Usage: python3 his1.py           -> his1.json / his1.out
       python3 his1.py --mutate  -> his1_MUTATE.json / his1_MUTATE.out
Y = log10(g_obs / g_bar) = log10(1 + X); d_L = Y - log10(1 + X_L(g_bar; a0)). Per system: medians over its points.
"""
import os, sys, csv, math, json, re, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data"); DD1 = os.path.join(REPO, "fable52_push", "DD1_deduce_from_data")
MUT = "--mutate" in sys.argv; TAG = "his1_MUTATE" if MUT else "his1"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
RES = dict(lane="HIS1", criteria="152ecaf5c4", table="DD1 441824e854 (origin f86496a251)", tag=TAG,
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, tests={}, controls={}, labels={}, reported={}, MUTATE={})
def XL(lgb, a0):
    t = a0 / 10 ** np.asarray(lgb, float); return 2 * t / (np.sqrt(1 + 4 * t) + 1)
def YL(lgb, a0): return np.log10(1 + XL(lgb, a0))
def norm(n): return re.sub(r"[^A-Z0-9]", "", n.upper())
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception: return None

# ======================================================================== DD1's frozen table, point level
with open(os.path.join(DD1, "dd1_table.csv")) as fh: lines = [l for l in fh if not l.startswith("#")]
ROWS = [r for r in csv.DictReader(lines) if r["bracket"] == ""]
PT = dict(cls=np.array([r["cls"] for r in ROWS]), sys=np.array([r["sys"] for r in ROWS]), lgb=np.array([float(r["lgb"]) for r in ROWS]),
          lgo=np.array([float(r["lgo"]) for r in ROWS]), eY=np.array([float(r["eY"]) for r in ROWS]), last=np.array([int(r["last"]) for r in ROWS]),
          r=np.array([float(r["r_kpc"]) for r in ROWS]))
PT["sk"] = np.array([c + "|" + s for c, s in zip(PT["cls"], PT["sys"])]); PT["Y"] = PT["lgo"] - PT["lgb"]
CLASSES = []
for c in PT["cls"]:
    if c not in CLASSES: CLASSES.append(c)
SK = sorted(set(PT["sk"])); IDX = {k: np.where(PT["sk"] == k)[0] for k in SK}

# ======================================================================== indicators (stated in the criteria)
IND = {k: {} for k in SK}
def put(cls, name, key, val):
    k = cls + "|" + name
    if k in IND and val is not None: IND[k][key] = val
UNGC = {}
for l in open(os.path.join(DATA, "ungc_karachentsev2013.tsv")):
    if l.startswith("#") or not l.strip(): continue
    t = l.rstrip("\n").split("\t")
    if len(t) < 17 or t[0].strip() in ("Name", "") or t[0].startswith("-"): continue
    v = fl(t[14])
    if v is not None: UNGC[norm(t[0])] = v
ALIAS = {"DDO99": "DDO099", "DDO53": "DDO053", "SEXTANSA": "SEXA", "SEXTANSB": "SEXB"}
# SPARC gas fraction and Ti1
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) != 19: continue
    try: L36, MHI = float(tok[7]), float(tok[13])
    except ValueError: continue
    put("SPARC", tok[0], "fg", 1.33 * MHI / (0.5 * L36 + 1.33 * MHI) if (0.5 * L36 + 1.33 * MHI) > 0 else None)
    put("SPARC", tok[0], "Ti1", UNGC.get(norm(tok[0])))
# faint rotators: gas fraction, Ti1, M_* and M_bary (for the brackets)
FR = os.path.join(DATA, "faint_rotators_mcquinn2022")
L = open(os.path.join(FR, "apjac9285t1_mrt.txt")).read().splitlines(); i0 = max(k for k, l in enumerate(L) if l.startswith("----"))
for l in L[i0 + 1:]:
    if not l.strip(): continue
    t = l.split(); lMs, lMb = float(l[46:50]), float(t[-2]); assert lMs <= lMb + 1e-9, (t[0], lMs, lMb)   # logMstar: bytes 47-50 (MRT)
    put("faint rotators", t[0], "fg", 1 - 10 ** (lMs - lMb)); put("faint rotators", t[0], "lMs", lMs); put("faint rotators", t[0], "lMb", lMb)
    put("faint rotators", t[0], "Ti1", UNGC.get(ALIAS.get(norm(t[0]), norm(t[0]))))
# tidal dwarfs
for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"), encoding="utf-8-sig")):
    nm = r.get("object") or r.get("Object")
    put("tidal dwarfs", nm, "Dp", fl(r["D_p_kpc"])); put("tidal dwarfs", nm, "fg", (float(r["M_atom_1e8"]) + float(r["M_mol_1e8"])) / float(r["M_bar_1e8"]))
    put("tidal dwarfs", nm, "MdynMbar", (float(r["Mdyn_over_Mbar"]), float(r["e_Mdyn_over_Mbar"])))
# massive spirals
for l in open(os.path.join(DATA, "diteodoro2023_massive_spirals.tsv")):
    if l.startswith("#") or l.startswith("name") or not l.strip(): continue
    t = l.rstrip("\n").split("\t"); Ms, Mg = 10 ** float(t[4]), 10 ** float(t[5]); put("massive spirals", t[0], "fg", Mg / (Ms + Mg))
# ATLAS3D Virgo flag
L = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")) if l.strip() and not l.startswith("#")]
for t in L[1:]:
    d = dict(zip(L[0], t)); put("ATLAS3D", d["name"], "virgo", fl(d["Virgo"]))
# CLASH merger flag (Umetsu+16 table 1 sections, HL3's key)
def ckey(name):
    n = name.replace("~", "").replace(" ", "").replace("*", "")
    m = re.match(r"^A(?:bell)?(\d+)$", n, re.I)
    if m: return "A" + m.group(1)
    m = re.search(r"(\d{4})", n); return m.group(1) if m else n
SECT = {}; sect = 0
for ln in open(os.path.join(REPO, "_external_data", "hl3", "umetsu16", "src", "table1.tex"), errors="replace"):
    if "High Magnification" in ln: sect = 1
    if ln.lstrip().startswith("~~"): SECT[ckey(ln.split("&")[0])] = sect
for k in SK:
    c, s = k.split("|", 1)
    if c == "CLASH": IND[k]["merger"] = SECT.get(ckey(s))
# LVD: host distance, age, HI
for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
        nm = r["name"]; dh = fl(r.get("distance_host"))
        if host == "M31" and dh is None: dh = fl(r.get("distance_m31"))
        for c in ("MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "LG field dwarfs"):
            put(c, nm, "dhost", dh); put(c, nm, "age", fl(r.get("age"))); put(c, nm, "MHI", fl(r.get("mass_HI")))
            put(c, nm, "Ti1", UNGC.get(norm(nm)))
# Coma UDGs
L = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "freundlich2022_coma_udgs.tsv"), encoding="utf-8") if l.strip() and not l.startswith("#")]
for t in L[1:]:
    d = dict(zip(L[0], t)); put("Coma UDGs", d["name"], "dmean", fl(d["dmean_kpc"])); put("Coma UDGs", d["name"], "dproj", fl(d["d_kpc"]))
put("NGC 1052 UDGs", "DF2", "dproj", 79.3); put("NGC 1052 UDGs", "DF4", "dproj", 165.3)     # NH2 / RB2, 20 Mpc

# ======================================================================== system level
def systems(Y, a0, cls_of=None):
    """per system: Y_sys, e_sys, dL_sys, dL_last (median of d_L at its last point(s))."""
    dl = Y - YL(PT["lgb"], a0); S = {}
    for k in SK:
        ix = IDX[k]; c = k.split("|", 1)[0] if cls_of is None else cls_of[k]
        lst = ix[PT["last"][ix] == 1]
        S[k] = dict(cls=c, Y=float(np.median(Y[ix])), e=float(np.median(PT["eY"][ix])), dL=float(np.median(dl[ix])),
                    dL_last=float(np.median(dl[lst])) if len(lst) else float("nan"), Y_last=float(np.median(Y[lst])) if len(lst) else float("nan"))
    return S
def cstat(vals, es):
    vals = np.asarray(vals, float); es = np.asarray(es, float); n = len(vals)
    if n == 0: return dict(n=0, med=float("nan"), se=float("nan"))
    m = float(np.median(vals))
    if n == 1: return dict(n=1, med=m, se=float(es[0]))
    mad = 1.4826 * float(np.median(np.abs(vals - np.median(vals))))
    return dict(n=n, med=m, se=max(1.2533 * mad / math.sqrt(n), math.sqrt(float(np.sum(es ** 2))) / n))
def sel(S, cls, cond=None):
    return [k for k, v in S.items() if v["cls"] == cls and (cond is None or cond(k))]
def stat(S, keys, field="dL"):
    return cstat([S[k][field] for k in keys], [S[k]["e"] for k in keys])

def H1(S):
    ks = sel(S, "tidal dwarfs"); sy, sd = stat(S, ks, "Y"), stat(S, ks, "dL")
    ok = abs(sy["med"]) <= 2 * sy["se"] and sd["med"] < -3 * sd["se"]
    return dict(holds=bool(ok), Y=sy, dL=sd, outcome="HOLDS" if ok else "FAILS")
def H2(S):
    below = [(k, S[k]["Y"], S[k]["e"]) for k in S if S[k]["Y"] < -3 * S[k]["e"]]
    cls_below = {}
    for c in CLASSES:
        s = stat(S, sel(S, c), "Y")
        if s["n"] and s["med"] < -3 * s["se"]: cls_below[c] = s
    dfc = {}
    for k in sorted(sel(S, "NGC 1052 UDGs")):          # DF2, DF4 (under shuffled labels: whichever systems carry the label)
        v = S[k]; dfc[k.split("|", 1)[1]] = dict(sys=k, Y=v["Y"], dL=v["dL"], e=v["e"], ok=bool(v["Y"] >= -3 * v["e"] and v["dL"] <= 3 * v["e"]))
    a, b, c_ = len(below) <= 3, not cls_below, all(v["ok"] for v in dfc.values())
    ok = a and b and c_
    return dict(holds=bool(ok), outcome="HOLDS" if ok else "FAILS", n_below=len(below), below=below, a=a, b=b, c=c_, classes_below=cls_below, DF=dfc)
def fr_iso(S):
    return sel(S, "faint rotators", lambda k: IND[k].get("Ti1") is not None and IND[k]["Ti1"] < 0)
def H3_sets(S):
    A = {"SPARC": sel(S, "SPARC"), "SPARC gas-rich (f_g >= 0.5)": sel(S, "SPARC", lambda k: IND[k].get("fg") is not None and IND[k]["fg"] >= 0.5),
         "faint rotators, Ti1 < 0": fr_iso(S)}
    B = {"SPARC": sel(S, "SPARC"), "KiDS": sel(S, "KiDS"), "LG field dwarfs": sel(S, "LG field dwarfs"), "faint rotators, Ti1 < 0": fr_iso(S),
         "ATLAS3D outside Virgo": sel(S, "ATLAS3D", lambda k: IND[k].get("virgo") == 0)}
    C = {c: sel(S, c) for c in ("MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs", "groups")}
    return A, B, C
def H3(S):
    A, B, C = H3_sets(S); out = dict(a={}, b={}, c={})
    for nm, ks in A.items(): s = stat(S, ks); out["a"][nm] = dict(s, ok=bool(s["n"] > 0 and abs(s["med"]) <= 3 * s["se"]))
    for nm, ks in B.items(): s = stat(S, ks); out["b"][nm] = dict(s, ok=bool(s["n"] > 0 and s["med"] >= -3 * s["se"]))
    for nm, ks in C.items(): s = stat(S, ks); out["c"][nm] = dict(s, ok=bool(s["n"] > 0 and s["med"] >= -3 * s["se"]))
    ok = all(v["ok"] for part in ("a", "b", "c") for v in out[part].values())
    out.update(holds=bool(ok), outcome="HOLDS" if ok else "FAILS"); return out
GPAIRS = [("G1", "SPARC", "fg", -1), ("G2", "faint rotators", "fg", -1), ("G3", "MW bright dwarfs", "dhost", +1),
          ("G4", "MW ultra-faints", "dhost", +1), ("G5", "M31 dwarfs", "dhost", +1), ("G6", "Coma UDGs", "dmean", +1)]
def pairs(S):
    out = {}
    for g, c, key, sgn in GPAIRS:
        ks = [k for k in sel(S, c) if IND[k].get(key) is not None]
        x = np.array([IND[k][key] for k in ks], float); y = np.array([S[k]["dL"] for k in ks], float)
        if len(ks) >= 4 and np.ptp(y) > 0 and np.ptp(x) > 0:
            rho, p = spearmanr(x, y); rho, p = float(rho), float(p)
        else: rho, p = float("nan"), float("nan")
        out[g] = dict(cls=c, ind=key, sign=sgn, n=len(ks), rho=rho, p=p)
    ps = sorted([(v["p"], g) for g, v in out.items() if np.isfinite(v["p"])]); m = len(ps); stop = False
    for i, (p, g) in enumerate(ps):
        sig = (not stop) and p <= 0.05 / (m - i)
        if not sig: stop = True
        out[g]["sig"] = bool(sig)
    for g in out: out[g].setdefault("sig", False)
    return out
def H5(S):
    pr = pairs(S); w = [g for g, v in pr.items() if v["sig"] and np.sign(v["rho"]) == v["sign"]]
    a = [g for g, v in pr.items() if v["sig"] and np.sign(v["rho"]) != v["sign"]]
    oc = "FAILS" if a else ("HOLDS" if w else "NO POWER")
    return dict(outcome=oc, holds=oc == "HOLDS", with_sign=w, against=a, pairs=pr)
H4Q = None
def H4():
    rb = json.load(open(os.path.join(REPO, "closure_2026_11_09", "RB1_form_b_hot_systems", "rb1.json")))["gate1"]["canonical"]
    cx, gh, r5 = rb["classes"]["C-X"], rb["classes"]["G-H"], rb["brackets"]["C-X at R500"]
    a = cx["lo"] <= 1 <= cx["hi"]; b = r5["median"] >= 1; c = gh["hi"] < 1
    R = 5.41
    return dict(outcome="HOLDS" if (a and b and c) else "FAILS", holds=bool(a and b and c), a=a, b=b, c=c,
                xcop_last=dict(fret=cx["median"], lo=cx["lo"], hi=cx["hi"], X=R / cx["median"], X_lo=R / cx["hi"], X_hi=R / cx["lo"]),
                xcop_R500=dict(fret=r5["median"], lo=r5["lo"], hi=r5["hi"], X=R / r5["median"]),
                groups=dict(fret=gh["median"], lo=gh["lo"], hi=gh["hi"], X=R / gh["median"], X_lo=R / gh["hi"], X_hi=R / gh["lo"]))
def force(S):
    t = {}
    s = stat(S, sel(S, "tidal dwarfs")); t["F1"] = dict(ok=bool(abs(s["med"]) <= 2 * s["se"]), dL=s)
    below = [k for k in S if S[k]["dL"] < -3 * S[k]["e"]]
    dfo = all(abs(S[k]["dL"]) <= 3 * S[k]["e"] for k in sel(S, "NGC 1052 UDGs"))
    t["F2"] = dict(ok=bool(len(below) <= 3 and dfo), n_below_law=len(below), DF_on_law=bool(dfo), below=sorted(below))
    A, B, C = H3_sets(S); sets = dict(A); sets.update(B); sets.update(C)
    for c in ("LG field dwarfs", "NGC 1052 UDGs"): sets[c] = sel(S, c)
    f3 = {nm: stat(S, ks) for nm, ks in sets.items()}; f3bad = [nm for nm, s in f3.items() if s["n"] and abs(s["med"]) > 3 * s["se"]]
    t["F3"] = dict(ok=not f3bad, off_law=f3bad, sets={nm: (s["med"], s["se"], s["n"]) for nm, s in f3.items()})
    s = cstat([S[k]["dL_last"] for k in sel(S, "X-COP")], [S[k]["e"] for k in sel(S, "X-COP")]); t["F4"] = dict(ok=bool(abs(s["med"]) <= 3 * s["se"]), dL_last=s)
    pr = pairs(S); t["F5"] = dict(ok=not any(v["sig"] for v in pr.values()), sig=[g for g, v in pr.items() if v["sig"]])
    t["score"] = sum(int(v["ok"]) for k, v in t.items() if k.startswith("F")); return t
def label(outs):
    fails = [h for h, o in outs.items() if o == "FAILS"]; nop = [h for h, o in outs.items() if o == "NO POWER"]
    if not fails and not nop: return "THE HISTORY READING HOLDS ON EVERY TEST"
    if len(fails) <= 1: return "HOLDS EXCEPT " + ", ".join([f"{h} (fails)" for h in fails] + [f"{h} (no power)" for h in nop])
    return "FAILS (" + ", ".join(fails) + ")"
def battery(Y, a0, cls_of=None):
    S = systems(Y, a0, cls_of)
    h = dict(H1=H1(S), H2=H2(S), H3=H3(S), H4=H4(), H5=H5(S)); return S, h, force(S)
def fmt(s): return f"{s['med']:+.3f} +- {s['se']:.3f} (n {s['n']})"
def show(h, F, f):
    P(f"  H1 tidal dwarfs: median Y {fmt(h['H1']['Y'])}; median d_L {fmt(h['H1']['dL'])} -> {h['H1']['outcome']}")
    P(f"  H2 systems below X = 0 beyond 3 e: {h['H2']['n_below']} ({', '.join(f'{k} {y:+.2f}+-{e:.2f}' for k, y, e in h['H2']['below'][:8])}); "
      f"classes below: {list(h['H2']['classes_below']) or 'none'}; DF2/DF4: " + ", ".join(f"{n} Y {v['Y']:+.3f} d_L {v['dL']:+.3f} e {v['e']:.3f} {'ok' if v['ok'] else 'OUT'}" for n, v in h['H2']['DF'].items())
      + f" -> {h['H2']['outcome']}")
    for part, txt in (("a", "on the law"), ("b", "isolated, not below"), ("c", "baryon-losers at or above")):
        P(f"  H3{part} ({txt}): " + "; ".join(f"{nm} {fmt(v)}{'' if v['ok'] else ' FAIL'}" for nm, v in h["H3"][part].items()))
    P(f"  H3 -> {h['H3']['outcome']}")
    q = h["H4"]; P(f"  H4 (RB1, no a0): X-COP last radius f_ret {q['xcop_last']['fret']:.3f} [{q['xcop_last']['lo']:.3f}, {q['xcop_last']['hi']:.3f}] -> X {q['xcop_last']['X']:.2f} "
                 f"[{q['xcop_last']['X_lo']:.2f}, {q['xcop_last']['X_hi']:.2f}]; at R500 f_ret {q['xcop_R500']['fret']:.3f} -> X {q['xcop_R500']['X']:.2f}; groups f_ret {q['groups']['fret']:.3f} "
                 f"[{q['groups']['lo']:.3f}, {q['groups']['hi']:.3f}] -> X {q['groups']['X']:.2f} [{q['groups']['X_lo']:.2f}, {q['groups']['X_hi']:.2f}] -> {q['outcome']}")
    P("  H5 " + "; ".join(f"{g} {v['cls']} vs {v['ind']} (sign {'+' if v['sign'] > 0 else '-'}): n {v['n']}, rho {v['rho']:+.2f}, p {v['p']:.3f}{' SIG' if v['sig'] else ''}" for g, v in h["H5"]["pairs"].items())
      + f" -> {h['H5']['outcome']}")
    P(f"  FORCE reading: F1 {F['F1']['ok']} (tidal dwarfs d_L {fmt(F['F1']['dL'])}); F2 {F['F2']['ok']} (systems below the law beyond 3 e: {F['F2']['n_below_law']}; DF2/DF4 on law {F['F2']['DF_on_law']}); "
      f"F3 {F['F3']['ok']} (off the law: {', '.join(F['F3']['off_law'])}); F4 {F['F4']['ok']} (X-COP last-point d_L {fmt(F['F4']['dL_last'])}); F5 {F['F5']['ok']} -> {F['score']} / 5")

if not MUT:
    # ==================================================================== known answers
    P("HIS1 run on DD1's frozen table: %d points, %d systems, %d classes." % (len(PT["Y"]), len(SK), len(CLASSES)))
    dj = json.load(open(os.path.join(DD1, "dd1.json"))); ka1 = {}
    for f in FOOT:
        S = systems(PT["Y"], A0[f]); mx = 0.0
        for c in CLASSES:
            mx = max(mx, abs(stat(S, sel(S, c))["med"] - float(dj["runs"][f]["L0"]["LOCO"][c]["off"])))
        ka1[f] = mx
    RES["KA"]["KA1"] = dict(max_dev=ka1, pass_=bool(all(v <= 1e-9 for v in ka1.values())))
    P(f"KA1 DD1 L0 class offsets reproduced: max dev {ka1} -> {'PASS' if RES['KA']['KA1']['pass_'] else 'FAIL'}")
    g2 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "G2_preinfall_retention", "g2_preinfall_retention_results.json")))["breakage"]["B1"]
    tk = sel(systems(PT["Y"], A0["canonical"]), "tidal dwarfs"); lr = np.array([math.log10(IND[k]["MdynMbar"][0]) for k in tk])
    er = np.array([IND[k]["MdynMbar"][1] / IND[k]["MdynMbar"][0] / math.log(10) for k in tk]); w = 1 / er ** 2
    mT, sT = float(np.sum(w * lr) / np.sum(w)), float(1 / math.sqrt(np.sum(w)))
    S0 = systems(PT["Y"], A0["canonical"]); dy = max(abs(S0[k]["Y"] - math.log10(IND[k]["MdynMbar"][0])) for k in tk)
    RES["KA"]["KA2"] = dict(mean=mT, se=sT, g2_mean=g2["mean_log_Mdyn_over_Mbar"], g2_se=g2["se"], max_dY=dy,
                            pass_=bool(abs(mT - g2["mean_log_Mdyn_over_Mbar"]) <= 1e-3 and abs(sT - g2["se"]) <= 1e-3 and dy <= 0.05))
    P(f"KA2 tidal dwarfs: mean log Mdyn/Mbar {mT:+.4f} +- {sT:.4f} (G2 {g2['mean_log_Mdyn_over_Mbar']:+.4f} +- {g2['se']:.4f}); table Y vs log Mdyn/Mbar max {dy:.3f} dex -> "
      f"{'PASS' if RES['KA']['KA2']['pass_'] else 'FAIL'}")
    # KA3 synthetic truths (noise free)
    k3 = {}; ok3 = True
    for f in FOOT:
        a0 = A0[f]; yl = YL(PT["lgb"], a0)
        Yh = yl.copy(); Yh[np.isin(PT["cls"], ["tidal dwarfs", "NGC 1052 UDGs"])] = 0.0
        Yh[np.isin(PT["cls"], ["MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs"])] += 0.3
        _, h, F = battery(Yh, a0)
        oki = h["H1"]["holds"] and h["H2"]["holds"] and h["H3"]["holds"] and not F["F1"]["ok"]
        _, h2, F2 = battery(yl.copy(), a0)
        okii = (not h2["H1"]["holds"]) and F2["F1"]["ok"] and F2["F2"]["ok"] and F2["F3"]["ok"]
        Yt = yl.copy()
        for c in ("SPARC", "faint rotators"):
            ks = [k for k in SK if k.startswith(c + "|") and IND[k].get("fg") is not None]; med = float(np.median([IND[k]["fg"] for k in ks]))
            for k in ks: Yt[IDX[k]] -= 0.3 * (IND[k]["fg"] - med)
        _, h3, _ = battery(Yt, a0)
        okiii = h3["H5"]["outcome"] == "HOLDS" and h2["H5"]["outcome"] == "NO POWER"
        k3[f] = dict(history=dict(H1=h["H1"]["outcome"], H2=h["H2"]["outcome"], H3=h["H3"]["outcome"], F1=F["F1"]["ok"], ok=bool(oki)),
                     force=dict(H1=h2["H1"]["outcome"], F1=F2["F1"]["ok"], F2=F2["F2"]["ok"], F3=F2["F3"]["ok"], ok=bool(okii)),
                     trend=dict(H5_planted=h3["H5"]["outcome"], H5_none=h2["H5"]["outcome"], ok=bool(okiii)))
        ok3 &= oki and okii and okiii
        P(f"KA3 [{f}] history truth: H1 {h['H1']['outcome']}, H2 {h['H2']['outcome']}, H3 {h['H3']['outcome']}, F1 {F['F1']['ok']}; force truth: H1 {h2['H1']['outcome']}, "
          f"F1-F3 {F2['F1']['ok']}/{F2['F2']['ok']}/{F2['F3']['ok']}; planted trend H5 {h3['H5']['outcome']}, none {h2['H5']['outcome']} -> {'PASS' if (oki and okii and okiii) else 'FAIL'}")
    RES["KA"]["KA3"] = dict(k3, pass_=bool(ok3))
    gg = np.logspace(-15, -8, 400); k4 = {}
    for f in FOOT:
        x = XL(np.log10(gg), A0[f]); k4[f] = dict(min_XL=float(x.min()), max_ratio=float(np.max(x / np.sqrt(A0[f] / gg))))
    RES["KA"]["KA4"] = dict(k4, pass_=bool(all(v["min_XL"] > 0 and v["max_ratio"] <= 1 for v in k4.values())))
    P(f"KA4 X_L > 0 and X_L <= sqrt(a0/g_bar): {k4} -> {'PASS' if RES['KA']['KA4']['pass_'] else 'FAIL'}")
    KA_OK = all(v["pass_"] for v in RES["KA"].values()); P(f"KNOWN ANSWERS: {'ALL PASS' if KA_OK else 'A KNOWN ANSWER FAILS -> NO VERDICT'}")

    # ==================================================================== the real table
    rng = np.random.default_rng(7); labs = [k.split("|", 1)[0] for k in SK]; perm = rng.permutation(len(SK)); SHUF = {SK[i]: labs[perm[i]] for i in range(len(SK))}
    for f in FOOT:
        P(f"\n== [{f}] the history reading")
        S, h, F = battery(PT["Y"], A0[f]); show(h, F, f)
        outs = {k: v["outcome"] for k, v in h.items()}
        lab = label(outs) if KA_OK else "NO VERDICT"
        _, hs, _ = battery(PT["Y"], A0[f], SHUF)
        shuf = {k: v["outcome"] for k, v in hs.items() if k != "H4"}
        RES["tests"][f] = h; RES["controls"][f] = dict(force=F, shuffled=shuf)
        RES["labels"][f] = dict(label=lab, outcomes=outs, force_score=F["score"], shuffled_holds=sum(1 for v in shuf.values() if v == "HOLDS"))
        P(f"  NO-RULE control (labels shuffled, seed 7): {shuf}")
        P(f"-> LABEL [{f}]: {lab}; force reading {F['score']} / 5; shuffled labels hold {RES['labels'][f]['shuffled_holds']} of 4 (H1, H2, H3, H5)")
        # reported: faint rotators, isolation and brackets
        if f == "canonical" or True:
            fr = sel(S, "faint rotators"); mt = [k for k in fr if IND[k].get("Ti1") is not None]; iso = fr_iso(S)
            P(f"  REPORTED faint rotators: {len(fr)} in the table, {len(mt)} with a UNGC Ti1, {len(iso)} isolated (Ti1 < 0): "
              + ", ".join(f"{k.split('|')[1]} {IND[k]['Ti1']:+.1f}" for k in mt))
            br = {}
            for nm, ks in (("all", fr), ("isolated", iso)):
                for lab2, kfun in (("M* x 2", ("ms", 2.0)), ("M* x 0.5", ("ms", 0.5)), ("D x 0.8", ("d", 0.8)), ("D x 1.2", ("d", 1.2))):
                    vals = []
                    for k in ks:
                        ix = IDX[k]; lgb = PT["lgb"][ix].copy(); Y = PT["Y"][ix].copy()
                        if kfun[0] == "ms":
                            Mb, Ms = 10 ** IND[k]["lMb"], 10 ** IND[k]["lMs"]; rat = (Mb + (kfun[1] - 1) * Ms) / Mb; lgb = lgb + math.log10(rat); Y = Y - math.log10(rat)
                        else: Y = Y - math.log10(kfun[1])
                        vals.append(float(np.median(Y - YL(lgb, A0[f]))))
                    s = cstat(vals, [S[k]["e"] for k in ks]); br[f"{nm} {lab2}"] = s
            RES["reported"].setdefault(f, {})["faint_rotator_brackets"] = br
            P("  REPORTED faint-rotator d_L brackets: " + "; ".join(f"{k} {fmt(v)} ({v['med'] / v['se']:+.1f} se)" for k, v in br.items()))
    # reported: other indicators (not graded)
    S = systems(PT["Y"], A0["canonical"]); rep = {}
    for c, key in (("SPARC", "Ti1"), ("tidal dwarfs", "Dp"), ("tidal dwarfs", "fg"), ("massive spirals", "fg"), ("ATLAS3D", "virgo"), ("CLASH", "merger"),
                   ("MW bright dwarfs", "age"), ("MW ultra-faints", "age"), ("M31 dwarfs", "age"), ("LG field dwarfs", "MHI"), ("LG field dwarfs", "Ti1"), ("Coma UDGs", "dproj")):
        ks = [k for k in sel(S, c) if IND[k].get(key) is not None]
        x = np.array([IND[k][key] for k in ks], float); y = np.array([S[k]["dL"] for k in ks], float)
        if len(ks) >= 4 and np.ptp(x) > 0: rho, p = spearmanr(x, y); rep[f"{c} vs {key}"] = dict(n=len(ks), rho=float(rho), p=float(p))
        else: rep[f"{c} vs {key}"] = dict(n=len(ks), rho=None, p=None)
    for c, key in (("ATLAS3D", "virgo"), ("CLASH", "merger")):
        g = {v: stat(S, [k for k in sel(S, c) if IND[k].get(key) == v]) for v in (0, 1)}; rep[f"{c} by {key}"] = g
    RES["reported"]["indicators_canonical"] = rep
    P("\nREPORTED indicators (canonical, not graded): " + "; ".join(f"{k}: n {v['n']}, rho {v['rho']:+.2f}, p {v['p']:.3f}" if isinstance(v, dict) and v.get("rho") is not None
                                                                   else (f"{k}: n {v['n']}" if isinstance(v, dict) and "n" in v else f"{k}: 0 {fmt(v[0])} / 1 {fmt(v[1])}") for k, v in rep.items()))
    # POST HOC, reported, grades nothing (added after the first run was read): H2(a) with ATLAS3D at Salpeter (DD1's bracket rows)
    sal = [r for r in csv.DictReader(lines) if r["bracket"] == "atlas_salp"]
    ys = {}
    for r in sal: ys.setdefault(r["sys"], []).append((float(r["lgo"]) - float(r["lgb"]), float(r["eY"])))
    nb = [(k, float(np.median([y for y, _ in v])), float(np.median([e for _, e in v]))) for k, v in ys.items()]
    below_s = [x for x in nb if x[1] < -3 * x[2]]; cs = cstat([x[1] for x in nb], [x[2] for x in nb])
    RES["reported"]["posthoc_H2_atlas_salpeter"] = dict(n=len(nb), below_X0_beyond_3e=len(below_s), class_median_Y=cs)
    P(f"POST HOC (reported, grades nothing): ATLAS3D at Salpeter: {len(below_s)} of {len(nb)} below X = 0 beyond 3 e; class median Y {fmt(cs)}")
    P("REPORTED DD1 X at the outermost point (system medians): X-COP %.2f, groups %.2f, CLASH %.2f (CLASH ends at <= 600 kpc)" % tuple(
        float(np.median([10 ** S[k]["Y_last"] - 1 for k in sel(S, c)])) for c in ("X-COP", "groups", "CLASH")))
else:
    def outcome(Y, a0, key):
        _, h, _ = battery(Y, a0); return h[key]["outcome"], h
    a0 = A0["canonical"]; base = {k: v["outcome"] for k, v in battery(PT["Y"], a0)[1].items()}
    Y = PT["Y"].copy(); m = PT["cls"] == "tidal dwarfs"; Y[m] = YL(PT["lgb"][m], a0)
    o1, _ = outcome(Y, a0, "H1"); RES["MUTATE"]["M1"] = dict(real=base["H1"], mut=o1, bites=bool(o1 == "FAILS"))
    P(f"M1 tidal dwarfs on the law: H1 {base['H1']} -> {o1} -> {'bites' if o1 == 'FAILS' else 'DOES NOT BITE'}")
    Y = PT["Y"].copy(); four = [k for k in SK if k.startswith("SPARC|")][:4]
    for k in four: Y[IDX[k]] = -0.6
    o2, h2 = outcome(Y, a0, "H2"); RES["MUTATE"]["M2"] = dict(real=base["H2"], mut=o2, n_below=h2["H2"]["n_below"], bites=bool(o2 == "FAILS"))
    P(f"M2 four SPARC galaxies at Y = -0.6: H2 {base['H2']} -> {o2} (below X = 0: {h2['H2']['n_below']}) -> {'bites' if o2 == 'FAILS' else 'DOES NOT BITE'}")
    # M2b POST HOC (added after M2 was seen not to bite; disclosed): the same four galaxies at Y = -1.0
    Y = PT["Y"].copy()
    for k in four: Y[IDX[k]] = -1.0
    o2b, h2b = outcome(Y, a0, "H2"); RES["MUTATE"]["M2b_posthoc"] = dict(mut=o2b, n_below=h2b["H2"]["n_below"], four=four, e=[float(np.median(PT["eY"][IDX[k]])) for k in four], bites=bool(o2b == "FAILS"))
    P(f"M2b POST HOC, the same four at Y = -1.0: H2 -> {o2b} (below X = 0: {h2b['H2']['n_below']}; their e_sys {', '.join(f'{x:.2f}' for x in RES['MUTATE']['M2b_posthoc']['e'])}) -> {'bites' if o2b == 'FAILS' else 'DOES NOT BITE'}")
    Y = PT["Y"].copy(); ks = [k for k in SK if k.startswith("SPARC|") and IND[k].get("fg") is not None]; med = float(np.median([IND[k]["fg"] for k in ks]))
    for k in ks: Y[IDX[k]] += 0.5 * (IND[k]["fg"] - med)
    o3, h3 = outcome(Y, a0, "H5"); RES["MUTATE"]["M3"] = dict(real=base["H5"], mut=o3, G1=h3["H5"]["pairs"]["G1"], bites=bool(o3 == "FAILS"))
    P(f"M3 opposite gas trend in SPARC: H5 {base['H5']} -> {o3} (G1 rho {h3['H5']['pairs']['G1']['rho']:+.2f}, p {h3['H5']['pairs']['G1']['p']:.1e}) -> {'bites' if o3 == 'FAILS' else 'DOES NOT BITE'}")
    _, h4, _ = battery(PT["Y"], 2 * a0); sp = h4["H3"]["a"]["SPARC"]
    RES["MUTATE"]["M4"] = dict(SPARC=sp, H3=h4["H3"]["outcome"], bites=bool(not sp["ok"]))
    P(f"M4 a0 x 2: H3(a) SPARC median d_L {fmt(sp)} -> {'fails' if not sp['ok'] else 'still on the law'} -> {'bites' if not sp['ok'] else 'DOES NOT BITE'}")

RES["runtime_s"] = time.time() - T0
P(f"\nruntime {RES['runtime_s']:.1f} s"); P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else str(float(o))
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
